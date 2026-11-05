# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Minimal, immutable consumer demonstrating automatic restriction expiry.

No funds are moved. Replace the operation with an application-specific action.
This demo's owner cannot substitute another registry, rule, or fingerprint.
"""
from genlayer import *
import json


@gl.contract_interface
class ISunset:
    class View:
        def rule_exists(self, rule_id: str) -> bool: ...
        def rule_fingerprint(self, rule_id: str) -> str: ...
        def is_restricted(self, rule_id: str) -> bool: ...


def _payload_commitment(registry: Address, rule_id: str, fingerprint: str,
                        operation_id: str, payload: str) -> str:
    return Keccak256(json.dumps({
        "domain": "SUNSET_GATE_ACTION_V1",
        # Address identity is canonicalized to lowercase in the commitment
        # domain, matching the external commitment helper and avoiding
        # checksum-casing-dependent action identities.
        "registry": registry.as_hex.lower(),
        "rule_id": rule_id,
        "fingerprint": fingerprint,
        "operation_id": operation_id,
        "payload": payload,
    }, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()


class SunsetGate(gl.Contract):
    registry: Address
    rule_id: str
    expected_fingerprint: str
    executor: Address
    expected_action_commitment: str
    execution_count: u256
    executed: TreeMap[str, bool]

    def __init__(self, registry: Address, rule_id: str, fingerprint: str,
                 executor: Address, action_commitment: str):
        if not (3 <= len(rule_id) <= 64 and len(fingerprint) == 64
                and len(action_commitment) == 64
                and all(ch in "0123456789abcdef" for ch in fingerprint.lower())
                and all(ch in "0123456789abcdef" for ch in action_commitment.lower())):
            raise gl.vm.UserError("INVALID_GATE_BINDING")
        source = ISunset(registry)
        if not source.view().rule_exists(rule_id):
            raise gl.vm.UserError("UNKNOWN_BOUND_RULE")
        if source.view().rule_fingerprint(rule_id) != fingerprint:
            raise gl.vm.UserError("FINGERPRINT_MISMATCH")
        self.registry = registry
        self.rule_id = rule_id
        self.expected_fingerprint = fingerprint
        self.executor = executor
        self.expected_action_commitment = action_commitment
        self.execution_count = u256(0)

    def _payload_commitment(self, operation_id: str, payload: str) -> str:
        return _payload_commitment(self.registry, self.rule_id,
                                   self.expected_fingerprint, operation_id, payload)

    def _allowed(self) -> bool:
        source = ISunset(self.registry)
        # A missing/mismatched registry fails closed; we never infer "expired".
        if not source.view().rule_exists(self.rule_id):
            return False
        if source.view().rule_fingerprint(self.rule_id) != self.expected_fingerprint:
            return False
        return not source.view().is_restricted(self.rule_id)

    @gl.public.view
    def can_execute(self) -> bool:
        return self._allowed()

    @gl.public.view
    def can_execute_bound(self, operation_id: str, payload: str) -> bool:
        if not (3 <= len(operation_id) <= 64 and all(
                c.isascii() and (c.isalnum() or c in "-_") for c in operation_id)):
            return False
        if not (1 <= len(payload) <= 2048) or operation_id in self.executed:
            return False
        return (gl.message.sender_address == self.executor
                and self._allowed()
                and self._payload_commitment(operation_id, payload)
                == self.expected_action_commitment)

    @gl.public.view
    def get_execution_count(self) -> u256:
        """Return the number of exact, finalized actions completed by this gate."""
        return self.execution_count

    @gl.public.view
    def is_executed(self, operation_id: str) -> bool:
        """Return whether this exact operation identifier has been consumed."""
        return operation_id in self.executed

    @gl.public.write
    def execute_once(self, operation_id: str, payload: str) -> u256:
        if not (3 <= len(operation_id) <= 64 and all(
                c.isascii() and (c.isalnum() or c in "-_") for c in operation_id)):
            raise gl.vm.UserError("INVALID_OPERATION_ID")
        if not (1 <= len(payload) <= 2048):
            raise gl.vm.UserError("INVALID_ACTION_PAYLOAD")
        if operation_id in self.executed:
            raise gl.vm.UserError("REPLAY")
        if gl.message.sender_address != self.executor:
            raise gl.vm.UserError("ONLY_EXECUTOR")
        if not self._allowed():
            raise gl.vm.UserError("SUNSET_RESTRICTION_ACTIVE_OR_UNVERIFIABLE")
        if self._payload_commitment(operation_id, payload) != self.expected_action_commitment:
            raise gl.vm.UserError("ACTION_COMMITMENT_MISMATCH")
        self.executed[operation_id] = True
        self.execution_count += u256(1)
        return self.execution_count
