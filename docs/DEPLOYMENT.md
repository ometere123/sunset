# Deployment and live verification ledger

This file is an evidence ledger, not a template for invented receipts.
Deployment is permitted only on stable StudioNet:

- network: `studionet`
- chain ID: `61999` / `0xf22f`
- RPC: `https://studio.genlayer.com/api`
- local CLI: repository `genlayer@0.39.1`
- contract runner: pinned header and Direct Mode SDK `v0.2.12`

## Predeployment gate

```bash
npm ci
python3 -m pip install -r requirements-dev.txt
python3 scripts/preflight.py
python3 -B -m unittest discover -s tests -p test_offline.py -v
GENVM_VERSION=v0.2.12 genvm-lint check contracts/sunset.py
GENVM_VERSION=v0.2.12 genvm-lint check contracts/sunset_gate.py
python3 -m pytest -q tests/direct
node scripts/assert_studionet.mjs
```

`scripts/guarded-deploy.mjs` repeats local CLI/package/network checks and makes
an independent `eth_chainId` request before invoking the local deploy binary.
It never accepts Studio Dev, Studio Next or chain 61997. No secret, private key
or password is stored in this repository or CI.

## Finalized evidence

| Field | Verified value |
|---|---|
| Final branch / commit | NOT YET VERIFIED |
| `contracts/sunset.py` SHA-256 | NOT YET VERIFIED |
| `contracts/sunset_gate.py` SHA-256 | NOT YET VERIFIED |
| Local CLI version | `genlayer@0.39.1` verified locally |
| GenVM linter | `0.11.0`, result pending final run |
| Sunset address | NOT YET VERIFIED |
| Sunset deployment transaction | NOT YET VERIFIED |
| Sunset finality and execution | NOT YET VERIFIED |
| Sunset explorer | NOT YET VERIFIED |
| SunsetGate address | NOT YET VERIFIED |
| SunsetGate deployment transaction | NOT YET VERIFIED |
| SunsetGate finality and execution | NOT YET VERIFIED |
| Consumer explorer | NOT YET VERIFIED |
| On-chain source byte parity | NOT YET VERIFIED |

Only a finalized receipt with successful execution may fill these fields.
`ACCEPTED`, a submitted hash, an address with no successful code deployment or
an asynchronous status is not a proof of deployment success.

The primary deployment command is:

```bash
npm run deploy:sunset
```

The consumer command requires all frozen bindings, including the executor and
action commitment:

```bash
npm run deploy:gate -- <sunset-address> <rule-id> <fingerprint> <executor-address> <action-commitment>
```

## Required live sequence

After deployment, record each transaction hash and readback separately:

1. register a bounded rule from the deployment signer;
2. read its owner, immutable fingerprint, source and deadlines;
3. exercise owner assessment with independently retrievable public evidence;
4. record positive renewal, ended, semantic inconclusive and transient recovery
   behavior where each transaction actually finalizes;
5. deploy a gate with the exact registry/rule/fingerprint/executor/action
   commitment;
6. prove active-rule rejection, exact cleared action success, unauthorized
   executor rejection, payload substitution rejection and replay rejection; and
7. fetch the deployed source/code using the stable RPC/CLI and compare exact
   bytes and SHA-256 against the final committed files.

If any step cannot be independently verified, it remains `NOT YET VERIFIED` in
this ledger and in the final release report.
