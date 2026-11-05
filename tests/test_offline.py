"""Executable tests of the actual contract under a deterministic GenLayer shim.

Not a substitute for GenVM lint, Direct Mode, or finalized StudioNet evidence.
No external package or network access is required.
"""
import copy
import hashlib
import importlib.util
from pathlib import Path
import sys
import types
import unittest


class Address(str):
    @property
    def as_hex(self):
        return str(self)


class TreeMap:
    def __class_getitem__(cls, item):
        return dict


class Return:
    def __init__(self, calldata):
        self.calldata = calldata


class Response:
    def __init__(self, content, status=200, headers=None, url=None, history=None):
        self.body = content.encode("utf-8")
        self.status = status
        self.headers = headers or {}
        self.url = url
        self.history = history


class FakeGl:
    class Contract:
        def __init__(self):
            for name, kind in type(self).__annotations__.items():
                if kind is dict:
                    setattr(self, name, {})

    class UserError(Exception):
        pass

    def __init__(self):
        self.message = types.SimpleNamespace(sender_address=Address("0x" + "a" * 40))
        self.public = types.SimpleNamespace(write=lambda f: f, view=lambda f: f)
        self.storage = types.SimpleNamespace(copy_to_memory=copy.deepcopy)
        self.vm = types.SimpleNamespace(Return=Return, UserError=self.UserError,
                                        run_nondet_unsafe=self.run_consensus)
        self.page = ("Incident report from 2026-10-29: the affected service remains "
                     "unavailable and recovery work is ongoing. Official status update.")
        self.answers = []
        self.snapshots = []
        self.nondet = types.SimpleNamespace(
            web=types.SimpleNamespace(get=self.fetch), exec_prompt=self.prompt
        )

    def contract_interface(self, cls):
        return cls

    def fetch(self, url):
        if self.snapshots:
            snapshot = self.snapshots.pop(0)
            if isinstance(snapshot, dict):
                return Response(snapshot.get("body", ""), snapshot.get("status", 200),
                                snapshot.get("headers"), snapshot.get("url"),
                                snapshot.get("history"))
            return Response(snapshot)
        return Response(self.page)

    def prompt(self, text, response_format=None):
        if self.answers:
            return self.answers.pop(0)
        return {"verdict": "INCONCLUSIVE", "quote": "", "reason_code": "UNCERTAIN"}

    def run_consensus(self, leader, validator):
        proposed = leader()
        if not validator(Return(proposed)):
            raise self.UserError("VALIDATORS_DISAGREE")
        return proposed


def load_contract():
    fake = FakeGl()
    gl_module = types.ModuleType("genlayer")
    gl_module.gl = fake
    gl_module.Address = Address
    gl_module.TreeMap = TreeMap
    gl_module.u256 = int
    gl_module.allow_storage = lambda cls: cls
    gl_module.Keccak256 = lambda data: hashlib.sha3_256(data)
    sys.modules["genlayer"] = gl_module
    source = Path(__file__).resolve().parents[1] / "contracts" / "sunset.py"
    spec = importlib.util.spec_from_file_location("sunset_under_test", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, fake


class SunsetTests(unittest.TestCase):
    def setUp(self):
        self.mod, self.gl = load_contract()
        self.clock = 1000000000
        self.mod._now = lambda: self.clock
        self.sunset = self.mod.Sunset()
        # The shim initializes TreeMap storage; production does this in GenVM.
        self.sunset.rules, self.sunset.receipts = {}, {}
        self.owner = self.gl.message.sender_address
        self.source = "https://status.example.org/incidents/incident-42"
        self.criteria = ("There is affirmative and recent official evidence "
                         "that incident INC-42 remains unresolved.")
        self.restriction = ("Emergency withdrawals are suspended while incident "
                            "INC-42 is actively unresolved.")

    def register(self, rid="incident-42", epoch=100, window=40, cap=2):
        return self.sunset.register_rule(
            rid, "Emergency withdrawal control", self.restriction,
            self.criteria, self.source, epoch, window, cap
        )

    def outcome(self, verdict, quote="Some sufficiently long quoted evidence.", reason="SOURCE_CONFIRMED"):
        return {"verdict": verdict, "source_digest": "a" * 64,
                "quote": quote if verdict != self.mod.INCONCLUSIVE else "",
                "reason": reason, "retryable": False,
                "audit_verdict": (self.mod.AUDIT_SAFE if verdict == self.mod.PERSISTS
                                   else self.mod.AUDIT_NOT_APPLICABLE),
                "audit_quote": ""}

    def assessment(self, verdict, rid="incident-42"):
        rule = self.sunset._rule(rid)
        self.sunset._consensus = lambda *args: self.outcome(verdict)
        return self.sunset.assess_renewal(rid, rule.renewals, rule.expiry)

    def gate(self, rule_id="incident-42", fingerprint=None):
        if fingerprint is None:
            fingerprint = self.sunset.rule_fingerprint(rule_id)
        file = Path(__file__).resolve().parents[1] / "contracts" / "sunset_gate.py"
        spec = importlib.util.spec_from_file_location("sunset_gate_under_test", file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        sunset = self.sunset

        class Registry:
            def view(self):
                return self

            def rule_exists(self, name):
                return sunset.rule_exists(name)

            def rule_fingerprint(self, name):
                return sunset.rule_fingerprint(name)

            def is_restricted(self, name):
                return sunset.is_restricted(name)

        module.ISunset = lambda address: Registry()
        registry = Address("0x" + "c" * 40)
        operation_id, payload = "withdrawal-1", "withdrawal:incident-42"
        commitment = module._payload_commitment(registry, rule_id, fingerprint,
                                                operation_id, payload)
        gate = module.SunsetGate(registry, rule_id, fingerprint, self.owner, commitment)
        gate.executed = {}
        return gate

    def assertRejected(self, method, *args):
        with self.assertRaises(self.gl.UserError):
            method(*args)

    def test_initial_restriction_active(self):
        self.register()
        self.assertTrue(self.sunset.is_restricted("incident-42"))
        self.assertEqual(self.sunset.get_rule("incident-42")["status"], "ACTIVE")

    def test_exact_boundary_expiry_requires_no_keeper(self):
        self.register()
        self.clock += 100
        self.assertFalse(self.sunset.is_restricted("incident-42"))
        self.assertEqual(self.sunset.get_rule("incident-42")["status"], "EXPIRED")
        self.assertEqual(self.sunset._rule("incident-42").terminal, "LIVE")

    def test_one_second_before_expiry_is_restricted(self):
        self.register()
        self.clock += 99
        self.assertTrue(self.sunset.is_restricted("incident-42"))

    def test_positive_extends_exactly_one_original_epoch(self):
        self.register()
        self.clock += 65
        self.assertEqual(self.assessment(self.mod.PERSISTS), self.mod.PERSISTS)
        rule = self.sunset._rule("incident-42")
        self.assertEqual(rule.expiry, 1000000200)
        self.assertEqual(rule.renewals, 1)
        self.assertEqual(self.sunset.get_assessment("incident-42", 0)["expiry_after"],
                         "1000000200")

    def test_positive_never_uses_now_plus_duration(self):
        self.register()
        self.clock += 99
        self.assessment(self.mod.PERSISTS)
        self.assertEqual(self.sunset._rule("incident-42").expiry, 1000000200)

    def test_second_positive_and_hard_stop(self):
        self.register()
        for at in (65, 165):
            self.clock = 1000000000 + at
            self.assessment(self.mod.PERSISTS)
        self.assertEqual(self.sunset._rule("incident-42").expiry, 1000000300)
        self.assertEqual(self.sunset._rule("incident-42").hard_stop, 1000000300)
        self.clock = 1000000261
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 2, 1000000300)
        self.clock = 1000000300
        self.assertFalse(self.sunset.is_restricted("incident-42"))

    def test_inconclusive_never_extends(self):
        self.register()
        self.clock += 65
        self.assessment(self.mod.INCONCLUSIVE)
        self.assertEqual(self.sunset._rule("incident-42").expiry, 1000000100)
        self.clock += 35
        self.assertFalse(self.sunset.is_restricted("incident-42"))

    def test_inconclusive_consumes_epoch_to_prevent_reprompting(self):
        self.register()
        self.clock += 65
        self.assessment(self.mod.INCONCLUSIVE)
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 0, 1000000100)

    def test_ended_evidence_closes_immediately(self):
        self.register()
        self.clock += 65
        self.assessment(self.mod.ENDED)
        self.assertFalse(self.sunset.is_restricted("incident-42"))
        self.assertEqual(self.sunset.get_rule("incident-42")["status"], "ENDED_EARLY")

    def test_ended_cannot_resurrect(self):
        self.register()
        self.clock += 65
        self.assessment(self.mod.ENDED)
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 0, 1000000065)

    def test_early_attempt_rejected(self):
        self.register()
        self.clock += 59
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 0, 1000000100)

    def test_window_opens_at_inclusive_boundary(self):
        self.register()
        self.clock += 60
        self.assessment(self.mod.INCONCLUSIVE)
        self.assertEqual(self.sunset._rule("incident-42").assessed_epoch, 1)

    def test_post_expiry_attempt_rejected(self):
        self.register()
        self.clock += 100
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 0, 1000000100)

    def test_stale_expected_epoch_rejected(self):
        self.register()
        self.clock += 65
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 1, 1000000100)

    def test_stale_expiry_rejected(self):
        self.register()
        self.clock += 65
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 0, 1000000099)

    def test_concurrent_stale_head_rejected_after_consensus(self):
        self.register()
        self.clock += 65
        def racing(*args):
            rule = self.sunset._rule("incident-42")
            rule.expiry += 100
            self.sunset.rules["incident-42"] = rule
            return self.outcome(self.mod.PERSISTS)
        self.sunset._consensus = racing
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 0, 1000000100)
        self.assertEqual(len(self.sunset.receipts), 0)

    def test_zero_renewal_cap(self):
        self.register(cap=0)
        self.clock += 65
        self.assertRejected(self.sunset.assess_renewal, "incident-42", 0, 1000000100)
        self.clock += 35
        self.assertFalse(self.sunset.is_restricted("incident-42"))

    def test_nonowner_cannot_revoke(self):
        self.register()
        self.gl.message.sender_address = Address("0x" + "b" * 40)
        self.assertRejected(self.sunset.revoke, "incident-42")

    def test_owner_revoke_is_terminal(self):
        self.register()
        self.sunset.revoke("incident-42")
        self.assertFalse(self.sunset.is_restricted("incident-42"))
        self.assertEqual(self.sunset.get_rule("incident-42")["status"], "REVOKED")
        self.assertRejected(self.sunset.revoke, "incident-42")

    def test_permissionless_expiry_seal_is_not_required(self):
        self.register()
        self.clock += 100
        self.gl.message.sender_address = Address("0x" + "b" * 40)
        self.sunset.seal_expired("incident-42")
        self.assertEqual(self.sunset.get_rule("incident-42")["status"], "SEALED_EXPIRED")
        self.assertFalse(self.sunset.is_restricted("incident-42"))
        self.assertRejected(self.sunset.seal_expired, "incident-42")

    def test_sealing_while_live_rejected(self):
        self.register()
        self.assertRejected(self.sunset.seal_expired, "incident-42")

    def test_duplicate_rule_cannot_replace_criterion(self):
        self.register()
        self.assertRejected(self.register)

    def test_fingerprint_and_source_are_immutable(self):
        fingerprint = self.register()
        self.assertEqual(self.sunset.rule_fingerprint("incident-42"), fingerprint)
        self.clock += 65
        self.assessment(self.mod.PERSISTS)
        r = self.sunset.get_rule("incident-42")
        self.assertEqual(r["fingerprint"], fingerprint)
        self.assertEqual(r["criterion"], self.criteria)
        self.assertEqual(r["source_url"], self.source)

    def test_unknown_rule_fails_closed(self):
        self.assertRejected(self.sunset.is_restricted, "does-not-exist")
        self.assertFalse(self.sunset.rule_exists("does-not-exist"))

    def test_invalid_timing_configurations(self):
        for epoch, window, cap in (
            (59, 30, 1), (60, 29, 1), (60, 60, 1),
            (2592001, 30, 1), (100, 40, 25), (100, 40, -1)
        ):
            with self.subTest(epoch=epoch, window=window, cap=cap):
                self.assertRejected(self.register, "test-" + str(epoch) + "-" + str(cap),
                                    epoch, window, cap)

    def test_https_only_and_private_source_rejection(self):
        for url in ("http://status.example.org", "https://localhost/status",
                    "https://127.0.0.1/", "https://internal.local/status",
                    "https://user:pass@example.org/status", "https://example.org/#fragment",
                    "https://example.org/?source=127.0.0.1", "https://example.org:443/status",
                    "https://[::1]/status", "https://2130706433/status",
                    "https://127.0.0.1.nip.io/status", "https://example.org/%2fprivate"):
            with self.subTest(url=url):
                self.assertFalse(self.mod._safe_url(url))

    def test_source_url_is_canonicalized_once(self):
        self.assertEqual(self.mod._normalize_source_url("https://status.example.org"),
                         "https://status.example.org/")
        self.assertEqual(self.mod._normalize_source_url("https://STATUS.example.org"),
                         "https://status.example.org/")
        self.assertEqual(self.mod._normalize_source_url(self.source), self.source)

    def test_contract_text_and_ids_rejected(self):
        self.assertRejected(self.register, "x")
        self.assertRejected(self.register, "spaces invalid")
        self.assertRejected(self.register, "bad<script>")

    def test_classifier_needs_source_witness(self):
        for raw in (
            {"verdict": self.mod.PERSISTS, "quote": "invented passage over twelve", "reason_code": "OK"},
            {"verdict": self.mod.ENDED, "quote": "", "reason_code": "OK"},
            {"verdict": "RENEW_FOREVER", "quote": "", "reason_code": "OK"},
            {"verdict": self.mod.PERSISTS, "quote": "x" * 221, "reason_code": "OK"},
            {"verdict": self.mod.PERSISTS, "quote": "", "reason_code": "bad"},
            {"verdict": self.mod.PERSISTS, "quote": "", "extra": "x"},
            "not json", None
        ):
            with self.subTest(raw=raw):
                self.assertEqual(self.mod._classify(raw, self.gl.page)["verdict"],
                                 self.mod.INCONCLUSIVE)

    def test_classifier_accepts_exact_quote(self):
        quote = "the affected service remains unavailable"
        raw = {"verdict": self.mod.PERSISTS, "quote": quote, "reason_code": "CURRENT_REPORT"}
        self.assertEqual(self.mod._classify(raw, self.gl.page)["verdict"], self.mod.PERSISTS)

    def test_json_normalization_ignores_incidental_model_fields(self):
        quote = "the affected service remains unavailable"
        raw = {"verdict": self.mod.PERSISTS, "quote": quote,
               "reason_code": "CURRENT_REPORT", "explanation": "ignored"}
        self.assertEqual(self.mod._classify(raw, self.gl.page)["verdict"], self.mod.PERSISTS)
        fenced = ('```json\n{"verdict":"JUSTIFICATION_ENDED",'
                  '"quote":"recovery work is ongoing",'
                  '"reason":"RESOLVED_REPORT"}\n```')
        self.assertEqual(self.mod._classify(fenced, self.gl.page)["verdict"], self.mod.ENDED)

    def test_validator_independently_rechecks_status(self):
        self.register()
        quote = "the affected service remains unavailable"
        self.gl.answers = [
            {"verdict": self.mod.PERSISTS, "quote": quote, "reason_code": "CURRENT_REPORT"},
            {"verdict": self.mod.ENDED, "quote": quote, "reason_code": "CURRENT_REPORT"},
        ]
        self.assertRejected(self.sunset._consensus, self.source, self.criteria,
                            self.restriction, "2026-10-29T00:00:00+00:00")

    def test_validator_rejects_source_drift(self):
        self.register()
        quote = "the affected service remains unavailable"
        self.gl.answers = [
            {"verdict": self.mod.PERSISTS, "quote": quote, "reason_code": "CURRENT_REPORT"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "NO_EXCEPTION_FOUND"},
            {"verdict": self.mod.PERSISTS, "quote": quote, "reason_code": "CURRENT_REPORT"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "NO_EXCEPTION_FOUND"},
        ]
        changed = self.gl.page.replace(
            "recovery work is ongoing", "recovery work has ended"
        )
        self.gl.snapshots = [self.gl.page, changed, changed]
        self.assertRejected(self.sunset._consensus, self.source, self.criteria,
                            self.restriction, "2026-10-29T00:00:00+00:00")

    def test_nonmaterial_page_difference_does_not_break_consensus(self):
        quote = "the affected service remains unavailable"
        self.gl.page = ("Historical context. " * 30) + self.gl.page + (" Archived note. " * 30)
        self.gl.answers = [
            {"verdict": self.mod.PERSISTS, "quote": quote,
             "reason_code": "CURRENT_REPORT"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "NO_EXCEPTION_FOUND"},
            {"verdict": self.mod.PERSISTS, "quote": quote,
             "reason_code": "FRESH_STATUS"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "NO_EXCEPTION_FOUND"},
        ]
        changed = self.gl.page + " Unrelated navigation banner updated."
        self.gl.snapshots = [self.gl.page, changed, changed]
        result = self.sunset._consensus(
            self.source, self.criteria, self.restriction,
            "2026-10-29T00:00:00+00:00"
        )
        self.assertEqual(result["verdict"], self.mod.PERSISTS)

    def test_same_positive_verdict_allows_different_valid_quotes_and_reasons(self):
        quote_one = "the affected service remains unavailable"
        quote_two = "recovery work is ongoing"
        self.gl.page += " Official status remains current."
        self.gl.answers = [
            {"verdict": self.mod.PERSISTS, "quote": quote_one,
             "reason_code": "CURRENT_REPORT"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "NO_EXCEPTION_FOUND"},
            {"verdict": self.mod.PERSISTS, "quote": quote_two,
             "reason_code": "FRESH_STATUS"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "QUALIFICATIONS_REVIEWED"},
        ]
        result = self.sunset._consensus(
            self.source, self.criteria, self.restriction,
            "2026-10-29T00:00:00+00:00"
        )
        self.assertEqual(result["verdict"], self.mod.PERSISTS)

    def test_same_ended_verdict_allows_different_valid_quotes_and_reasons(self):
        quote_one = "the affected service remains unavailable"
        quote_two = "recovery work is ongoing"
        self.gl.page += " Official status remains current."
        self.gl.answers = [
            {"verdict": self.mod.ENDED, "quote": quote_one,
             "reason_code": "RESOLVED_REPORT"},
            {"verdict": self.mod.ENDED, "quote": quote_two,
             "reason_code": "FRESH_STATUS"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "NO_EXCEPTION_FOUND"},
        ]
        result = self.sunset._consensus(
            self.source, self.criteria, self.restriction,
            "2026-10-29T00:00:00+00:00"
        )
        self.assertEqual(result["verdict"], self.mod.ENDED)

    def test_inconclusive_quote_is_normalized_to_terminal_uncertainty(self):
        result = self.mod._classify(
            {"verdict": self.mod.INCONCLUSIVE,
             "quote": "misleading but nondecisive text",
             "reason_code": "AMBIGUOUS"},
            self.gl.page,
        )
        self.assertEqual(result["verdict"], self.mod.INCONCLUSIVE)
        self.assertEqual(result["quote"], "")
        self.assertFalse(result["retryable"])

    def test_audit_uncertainty_without_quote_is_valid_and_fail_closed(self):
        audit = self.mod._classify_audit(
            {"audit_verdict": self.mod.AUDIT_UNCERTAIN,
             "quote": "", "reason_code": "AMBIGUOUS_CONTEXT"},
            self.gl.page,
        )
        self.assertFalse(audit["retryable"])
        result = {
            "verdict": self.mod.INCONCLUSIVE, "quote": "",
            "reason": audit["reason"], "source_digest": "a" * 64,
            "retryable": False, "audit_verdict": audit["audit_verdict"],
            "audit_quote": audit["quote"],
        }
        self.assertTrue(self.mod.Sunset()._valid_result(result))

    def test_redirect_and_http_error_are_retryable_without_clearance(self):
        self.gl.snapshots = [
            {"status": 302, "body": "", "headers": {"location": "https://other.example"}},
        ]
        redirect = self.sunset._observe(
            self.source, self.criteria, self.restriction,
            "2026-10-29T00:00:00+00:00"
        )
        self.assertEqual(redirect["reason"], "SOURCE_HTTP_STATUS")
        self.assertTrue(redirect["retryable"])
        self.gl.snapshots = [{"status": 503, "body": ""}]
        error = self.sunset._observe(
            self.source, self.criteria, self.restriction,
            "2026-10-29T00:00:00+00:00"
        )
        self.assertEqual(error["reason"], "SOURCE_HTTP_STATUS")
        self.assertTrue(error["retryable"])

    def test_matching_independent_source_and_verdict_passes(self):
        quote = "the affected service remains unavailable"
        self.gl.answers = [
            {"verdict": self.mod.PERSISTS, "quote": quote, "reason_code": "CURRENT_REPORT"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "NO_EXCEPTION_FOUND"},
            {"verdict": self.mod.PERSISTS, "quote": quote, "reason_code": "CURRENT_REPORT"},
            {"audit_verdict": self.mod.AUDIT_SAFE, "quote": "",
             "reason_code": "NO_EXCEPTION_FOUND"},
        ]
        outcome = self.sunset._consensus(self.source, self.criteria,
                                         self.restriction, "2026-10-29T00:00:00+00:00")
        self.assertEqual(outcome["verdict"], self.mod.PERSISTS)

    def test_source_unavailable_is_inconclusive(self):
        self.gl.page = ""
        outcome = self.sunset._consensus(self.source, self.criteria,
                                         self.restriction, "2026-10-29T00:00:00+00:00")
        self.assertEqual(outcome["verdict"], self.mod.INCONCLUSIVE)

    def test_gate_blocks_while_active_and_opens_at_expiry(self):
        self.register()
        gate = self.gate()
        self.assertFalse(gate.can_execute())
        self.assertFalse(gate.can_execute_bound("withdrawal-1", "withdrawal:incident-42"))
        self.assertRejected(gate.execute_once, "withdrawal-1", "withdrawal:incident-42")
        self.clock += 100
        self.assertTrue(gate.can_execute())
        self.assertTrue(gate.can_execute_bound("withdrawal-1", "withdrawal:incident-42"))
        self.assertEqual(gate.execute_once("withdrawal-1", "withdrawal:incident-42"), 1)

    def test_gate_no_replay_after_expiry(self):
        self.register()
        gate = self.gate()
        self.clock += 100
        self.assertEqual(gate.execute_once("withdrawal-1", "withdrawal:incident-42"), 1)
        self.assertRejected(gate.execute_once, "withdrawal-1", "withdrawal:incident-42")
        self.assertEqual(gate.execution_count, 1)

    def test_gate_constructor_rejects_wrong_fingerprint(self):
        self.register()
        self.assertRejected(self.gate, "incident-42", "a" * 64)

    def test_gate_rejects_substituted_payload_and_unauthorized_executor(self):
        self.register()
        gate = self.gate()
        self.clock += 100
        self.assertRejected(gate.execute_once, "withdrawal-1", "different-action")
        self.gl.message.sender_address = Address("0x" + "b" * 40)
        self.assertRejected(gate.execute_once, "withdrawal-1", "withdrawal:incident-42")
        self.gl.message.sender_address = self.owner
        self.assertEqual(gate.execute_once("withdrawal-1", "withdrawal:incident-42"), 1)

    def test_mutation_payload_binding_would_fail_security_regression(self):
        self.register()
        gate = self.gate()
        self.clock += 100
        # Simulate the critical mutation: accept every payload as the frozen one.
        gate._payload_commitment = lambda operation_id, payload: gate.expected_action_commitment
        with self.assertRaises(AssertionError):
            self.assertRejected(gate.execute_once, "withdrawal-1", "tampered-payload")

    def test_mutation_dynamic_expiry_check_would_fail_security_regression(self):
        self.register()
        original_live = self.sunset._live
        self.sunset._live = lambda rule, timestamp: rule.terminal == self.mod.LIVE
        self.clock += 100
        with self.assertRaises(AssertionError):
            self.assertFalse(self.sunset.is_restricted("incident-42"))
        self.sunset._live = original_live

    def test_gate_open_after_ended_evidence(self):
        self.register()
        gate = self.gate()
        self.clock += 65
        self.assessment(self.mod.ENDED)
        self.assertTrue(gate.can_execute())
        self.assertEqual(gate.execute_once("withdrawal-1", "withdrawal:incident-42"), 1)

    def test_gate_stays_blocked_after_positive_renewal(self):
        self.register()
        gate = self.gate()
        self.clock += 65
        self.assessment(self.mod.PERSISTS)
        self.clock = 1000000100
        self.assertFalse(gate.can_execute())
        self.clock = 1000000200
        self.assertTrue(gate.can_execute())


if __name__ == "__main__":
    unittest.main()
