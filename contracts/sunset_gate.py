# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Minimal, immutable consumer demonstrating automatic restriction expiry.

No funds are moved. Replace the operation with an application-specific action.
This demo's owner cannot substitute another registry, rule, or fingerprint.
"""
from genlayer import *


@gl.contract_interface
class ISunset:
    class View:
        def rule_exists(self, rule_id: str) -> bool: ...
        def rule_fingerprint(self, rule_id: str) -> str: ...
        def is_restricted(self, rule_id: str) -> bool: ...


class SunsetGate(gl.Contract):
    registry: Address
    rule_id: str
    expected_fingerprint: str
    execution_count: u256
    executed: TreeMap[str, bool]

    def __init__(self, registry: Address, rule_id: str, fingerprint: str):
        if not (3 <= len(rule_id) <= 64 and len(fingerprint) == 64):
            raise gl.vm.UserError("INVALID_GATE_BINDING")
        source = ISunset(registry)
        if not source.view().rule_exists(rule_id):
            raise gl.vm.UserError("UNKNOWN_BOUND_RULE")
        if source.view().rule_fingerprint(rule_id) != fingerprint:
            raise gl.vm.UserError("FINGERPRINT_MISMATCH")
        self.registry = registry
        self.rule_id = rule_id
        self.expected_fingerprint = fingerprint
        self.execution_count = u256(0)

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

    @gl.public.write
    def execute_once(self, operation_id: str) -> u256:
        if not (3 <= len(operation_id) <= 64 and all(
                c.isascii() and (c.isalnum() or c in "-_") for c in operation_id)):
            raise gl.vm.UserError("INVALID_OPERATION_ID")
        if operation_id in self.executed:
            raise gl.vm.UserError("REPLAY")
        if not self._allowed():
            raise gl.vm.UserError("SUNSET_RESTRICTION_ACTIVE_OR_UNVERIFIABLE")
        self.executed[operation_id] = True
        self.execution_count += u256(1)
        return self.execution_count
