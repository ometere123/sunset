"""Strict, offline preflight for source, tooling and network identity."""
import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SDK_HEADER = '# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }'


def main():
    package = json.loads((ROOT / "package.json").read_text())
    assert package["devDependencies"] == {"genlayer": "0.39.1"}
    assert package["config"] == {
        "network": "studionet", "chainId": 61999,
        "rpc": "https://studio.genlayer.com/api"
    }
    assert not (ROOT / "frontend").exists()
    checks = 4
    for filename, target in (("sunset.py", "Sunset"), ("sunset_gate.py", "SunsetGate")):
        source = (ROOT / "contracts" / filename).read_text()
        assert source.startswith(SDK_HEADER)
        tree = ast.parse(source)
        assert len([n for n in tree.body if isinstance(n, ast.ClassDef)
                    and any(isinstance(base, ast.Attribute) and base.attr == "Contract"
                            for base in n.bases)]) == 1
        assert target in [n.name for n in tree.body if isinstance(n, ast.ClassDef)]
        assert not re.search(r"\b(eval|exec|subprocess|requests)\s*\(", source)
        checks += 4
    contract = (ROOT / "contracts/sunset.py").read_text()
    for fragment in (
        "run_nondet_unsafe", "source_digest", "expected_epoch", "expected_expiry",
        "hard_stop", "INCONCLUSIVE", "STALE_AFTER_CONSENSUS",
        "timestamp < int(rule.expiry)", "current.expiry = u256(next_expiry)",
    ):
        assert fragment in contract, fragment
        checks += 1
    gate = (ROOT / "contracts/sunset_gate.py").read_text()
    for fragment in ("rule_fingerprint", "is_restricted", "REPLAY"):
        assert fragment in gate
        checks += 1
    guard = (ROOT / "scripts/guarded-deploy.mjs").read_text()
    for fragment in ("61999", "0.39.1", "studionet", "node_modules", "eth_chainId",
                     "https://studio.genlayer.com/api"):
        assert fragment in guard
        checks += 1
    print(f"PASS: {checks} structural / network / security assertions")


if __name__ == "__main__":
    main()
