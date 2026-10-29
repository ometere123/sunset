"""Print source SHA-256 for verifiable deployment receipts. Does not mutate files."""
from hashlib import sha256
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for rel in ("contracts/sunset.py", "contracts/sunset_gate.py"):
    path = root / rel
    print(f"{sha256(path.read_bytes()).hexdigest()}  {rel}")
