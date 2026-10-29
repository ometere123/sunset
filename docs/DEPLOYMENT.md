# Deployment and verification record

**Target only:** StudioNet (`studionet`), chain **61999**,
`https://studio.genlayer.com/api`; local `genlayer@0.39.1`.
Never reuse addresses or receipts from a different network.

## Required execution

```bash
npm ci
python3 -m pip install -r requirements-dev.txt
python3 scripts/preflight.py
python3 -B -m unittest discover -s tests -p test_offline.py -v
genvm-lint check contracts/sunset.py
genvm-lint check contracts/sunset_gate.py
genvm-lint schema contracts/sunset.py
genvm-lint schema contracts/sunset_gate.py
python3 -m pytest -q tests/direct
./node_modules/.bin/genlayer network set studionet
./node_modules/.bin/genlayer network info
npm run deploy:sunset
```

The guarded deploy script independently queries `eth_chainId`, checks that
CLI network info matches the exact stable endpoint, and verifies local package
version before touching the deploy command. The CLI may prompt for account
unlock. No account password, seed phrase, token, or private key belongs in
this repository or CI.

## Production evidence ledger

Fill in the following **only from actual observations**:

| Field | Verified value |
|---|---|
| Contract source SHA-256 | Run `python3 scripts/source_hashes.py` |
| StudioNet RPC / chain | `https://studio.genlayer.com/api` / 61999 |
| CLI package | `genlayer@0.39.1` (repository-local) |
| Sunset deployment tx | NOT YET VERIFIED |
| Sunset IC address | NOT YET VERIFIED |
| Finality + execution result | NOT YET VERIFIED |
| On-chain code/source byte parity | NOT YET VERIFIED |
| Rule registration receipt | NOT YET VERIFIED |
| PERSISTS/ENDED/INCONCLUSIVE lifecycle | NOT YET VERIFIED |
| Optional SunsetGate address | NOT YET VERIFIED |
| Gate after-expiry operation receipt | NOT YET VERIFIED |

Deployment verification must establish a successful *execution* and status
`FINALIZED`, not merely acceptance or existence of a ghost/address. Query
the deployed contract code using the local CLI's `code` command or the
GenLayer RPC, verify it exactly matches the committed UTF-8 source bytes,
and record the resulting digest plus explorer receipt.

The consumer must only be deployed after Sunset and a real registered rule
exist. Its constructor arguments are the exact Sunset address, rule ID, and
fingerprint from `get_rule`.

### Hard stop

If the local account cannot be unlocked, lacks GEN, the network guard fails,
the official runtime cannot be installed, or the transaction never finalizes,
stop and report the specific blocker. Do not invent a deployment address,
validator agreement, test count or chain receipt.
