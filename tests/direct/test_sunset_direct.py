"""Official GenLayer Direct Mode tests. Requires genlayer-test and GenVM SDK."""
import json

SOURCE = "https://status.example.org/incidents/inc42"
RESTRICTION = "Emergency withdrawals are suspended while incident INC42 is unresolved."
CRITERION = "Current official incident data must affirmatively show INC42 remains unresolved."
PAGE = ("Official incident INC42 update published today: the affected service "
        "remains unavailable and recovery work is ongoing. Investigations continue.")
QUOTE = "the affected service remains unavailable"


def setup(direct_vm, direct_deploy, cap=2):
    direct_vm.warp("2026-10-29T10:00:00+00:00")
    sunset = direct_deploy("contracts/sunset.py", sdk_version="v0.2.12")
    fingerprint = sunset.register_rule(
        "inc42", "Emergency withdrawals", RESTRICTION, CRITERION,
        SOURCE, 3600, 1800, cap
    )
    return sunset, fingerprint


def mock_evidence(direct_vm, status="JUSTIFICATION_PERSISTS", quote=QUOTE):
    direct_vm.mock_web(r"status\.example\.org/incidents/inc42",
                       {"status": 200, "body": PAGE})
    direct_vm.mock_llm(
        r"SUNSET: skeptical",
        json.dumps({"verdict": status, "quote": quote, "reason_code": "OFFICIAL_UPDATE"})
    )


def test_time_expiry_without_keeper(direct_vm, direct_deploy):
    sunset, _ = setup(direct_vm, direct_deploy)
    assert sunset.is_restricted("inc42") is True
    direct_vm.warp("2026-10-29T11:00:00+00:00")
    assert sunset.is_restricted("inc42") is False
    assert sunset.get_rule("inc42")["status"] == "EXPIRED"


def test_too_early_and_stale_expected_head(direct_vm, direct_deploy):
    sunset, _ = setup(direct_vm, direct_deploy)
    expiry = int(sunset.get_rule("inc42")["expires_at"])
    with direct_vm.expect_revert("TOO_EARLY"):
        sunset.assess_renewal("inc42", 0, expiry)
    direct_vm.warp("2026-10-29T10:40:00+00:00")
    with direct_vm.expect_revert("STALE_OR_ALREADY_ASSESSED"):
        sunset.assess_renewal("inc42", 1, expiry)


def test_positive_one_epoch_renewal(direct_vm, direct_deploy):
    sunset, _ = setup(direct_vm, direct_deploy)
    direct_vm.warp("2026-10-29T10:40:00+00:00")
    mock_evidence(direct_vm)
    expiry = int(sunset.get_rule("inc42")["expires_at"])
    assert sunset.assess_renewal("inc42", 0, expiry) == "JUSTIFICATION_PERSISTS"
    assert int(sunset.get_rule("inc42")["expires_at"]) == expiry + 3600
    assert int(sunset.get_rule("inc42")["renewals"]) == 1
    assert direct_vm.run_validator() is True


def test_inconclusive_cannot_extend(direct_vm, direct_deploy):
    sunset, _ = setup(direct_vm, direct_deploy)
    direct_vm.warp("2026-10-29T10:40:00+00:00")
    mock_evidence(direct_vm, "INCONCLUSIVE", "")
    expiry = int(sunset.get_rule("inc42")["expires_at"])
    assert sunset.assess_renewal("inc42", 0, expiry) == "INCONCLUSIVE"
    assert int(sunset.get_rule("inc42")["expires_at"]) == expiry
    with direct_vm.expect_revert("STALE_OR_ALREADY_ASSESSED"):
        sunset.assess_renewal("inc42", 0, expiry)
    direct_vm.warp("2026-10-29T11:00:00+00:00")
    assert sunset.is_restricted("inc42") is False


def test_ended_closes_before_deadline(direct_vm, direct_deploy):
    sunset, _ = setup(direct_vm, direct_deploy)
    direct_vm.warp("2026-10-29T10:40:00+00:00")
    mock_evidence(direct_vm, "JUSTIFICATION_ENDED")
    expiry = int(sunset.get_rule("inc42")["expires_at"])
    assert sunset.assess_renewal("inc42", 0, expiry) == "JUSTIFICATION_ENDED"
    assert sunset.is_restricted("inc42") is False
    assert sunset.get_rule("inc42")["status"] == "ENDED_EARLY"


def test_validator_rejects_disagreement(direct_vm, direct_deploy):
    sunset, _ = setup(direct_vm, direct_deploy)
    direct_vm.warp("2026-10-29T10:40:00+00:00")
    mock_evidence(direct_vm)
    expiry = int(sunset.get_rule("inc42")["expires_at"])
    sunset.assess_renewal("inc42", 0, expiry)
    direct_vm.clear_mocks()
    mock_evidence(direct_vm, "JUSTIFICATION_ENDED")
    assert direct_vm.run_validator() is False


def test_revoke_owner_only(direct_vm, direct_deploy, direct_owner, direct_alice):
    sunset, _ = setup(direct_vm, direct_deploy)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("ONLY_OWNER"):
        sunset.revoke("inc42")
    direct_vm.sender = direct_owner
    sunset.revoke("inc42")
    assert sunset.is_restricted("inc42") is False
    assert sunset.get_rule("inc42")["status"] == "REVOKED"


def test_no_renewal_at_zero_cap(direct_vm, direct_deploy):
    sunset, _ = setup(direct_vm, direct_deploy, cap=0)
    direct_vm.warp("2026-10-29T10:40:00+00:00")
    expiry = int(sunset.get_rule("inc42")["expires_at"])
    with direct_vm.expect_revert("RENEWAL_CAP"):
        sunset.assess_renewal("inc42", 0, expiry)
