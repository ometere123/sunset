"""Compatibility shim for genlayer-test 0.29.2 on Windows.

The pinned Direct Mode loader uses a named temporary file for the import-time
message and unlinks it immediately after dup2(). Windows keeps the duplicated
stdin handle open, so the unlink raises WinError 32 before the contract is
loaded. An anonymous pipe provides the same byte stream without a pathname.
This is test-only and is inactive on non-Windows platforms.
"""

from __future__ import annotations

import os
import sys


if sys.platform == "win32":
    from gltest.direct import loader

    def _inject_message_to_fd0_windows(vm) -> None:
        # The SDK path is installed by load_contract_class immediately before
        # this hook is called, so these imports must remain lazy.
        from genlayer.py import calldata
        from genlayer.py.types import Address

        sender_addr = vm.sender
        if isinstance(sender_addr, bytes):
            sender_addr = Address(sender_addr)

        contract_addr = vm._contract_address
        if isinstance(contract_addr, bytes):
            contract_addr = Address(contract_addr)

        origin_addr = vm.origin
        if isinstance(origin_addr, bytes):
            origin_addr = Address(origin_addr)

        message_data = {
            "contract_address": contract_addr,
            "sender_address": sender_addr,
            "origin_address": origin_addr,
            "stack": [],
            "value": vm._value,
            "datetime": vm._datetime,
            "is_init": False,
            "chain_id": vm._chain_id,
            "entry_kind": 0,
            "entry_data": b"",
            "entry_stage_data": None,
        }
        encoded = calldata.encode(message_data)

        read_fd, write_fd = os.pipe()
        try:
            os.write(write_fd, encoded)
        finally:
            os.close(write_fd)

        vm._original_stdin_fd = os.dup(0)
        os.dup2(read_fd, 0)
        os.close(read_fd)

    loader._inject_message_to_fd0 = _inject_message_to_fd0_windows
