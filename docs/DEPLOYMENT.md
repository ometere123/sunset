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
| Final branch / commit | Updated after the final local verification commit; GitHub CI status is recorded below |
| `contracts/sunset.py` SHA-256 | `cd82caa8d881d54521ed0f16c159da95c59c9e21fbd759d7468f02c017c05eed` |
| `contracts/sunset_gate.py` SHA-256 | `0edd5c49191d50241dc8a58e94488bdaf9a9367e67301cc6684d7674badec902` |
| Local CLI version | `genlayer@0.39.1` verified locally |
| GenVM linter | `genvm-linter==0.11.0`, runner `v0.2.12`, both contracts passed |
| Sunset address | `0x58EECE051565E256Cf02060E4478900D69fDCfc0` |
| Sunset deployment transaction | `0x8e2180638fcc6bfedc71df67b82fbe2a011332f1d22f3209ecdfa2793094eb7c` |
| Sunset finality and execution | `FINALIZED`, `MAJORITY_AGREE`, leader/validator execution `SUCCESS` |
| Sunset explorer | Explorer base recorded; address-specific page was not independently verified because the explorer returned HTTP 503 during verification |
| SunsetGate address | `0xFeFF39c5A3641d28e649e1508B704fa01F0B4DF1` |
| SunsetGate deployment transaction | `0x428d477c18988bec320d94c4edec0493c562b825412d22cff46e379a05485f6c` |
| SunsetGate finality and execution | `FINALIZED`, `MAJORITY_AGREE`, constructor execution `SUCCESS` |
| Consumer explorer | Explorer base recorded; address-specific page was not independently verified because the explorer returned HTTP 503 during verification |
| On-chain source byte parity | Sunset: exact bytes, 25,767 bytes, SHA-256 above. SunsetGate: exact bytes, 4,857 bytes, SHA-256 above. |

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

## Live StudioNet readbacks

The finalized demonstration uses the corrected primary deployment and one
short-lived rule. Registration of `sunset-final` finalized with transaction
`0xfb7df734bda474d9f58ebdb76fd353e9be3e128577de9ba983feceb26128983a` and
`MAJORITY_AGREE`. The readback froze fingerprint
`0d479eb09662a6fa76729a771b7f4289162388891f161f5f75e266112432334b`, source
`https://www.iana.org/domains/example`, expiry `1793892891`, and owner
`0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`. It was read as `ACTIVE` before
expiry and `is_restricted: false` after expiry.

The IANA page is public demonstration material only. It does not prove a
real-world actor, identity, action completion, source ownership or legal fact.

The final gate was read back with `can_execute: true` and
`can_execute_bound: true` only after the rule expired. Exact action execution
finalized successfully in transaction
`0x3c2dd90eb5e5d4611e89e6160983eef4d89cc1eefc9a4d3dcb4f228de596d26f`, with
consensus `MAJORITY_AGREE` and return value `1`. Repeating the same action
finalized with rollback reason `REPLAY` in transaction
`0x495b8fbd306a1c2d4f78c805297deda9d7bcea9c603885f3d277c5f76fa6017b`.
Substituting the operation/payload finalized with rollback reason
`ACTION_COMMITMENT_MISMATCH` in transaction
`0x2326c22fcbf821835624d4710730b56d2037fccf586cecb680d0dc70ff555a42`.

An earlier bounded assessment transaction
`0x77fe84104999b9c7ef3d490e42c473e78da8a69a75294f28b3016bab1e12c912`
finalized `MAJORITY_DISAGREE`; its rule remained unchanged and later expired.
This is recorded as fail-closed consensus disagreement, not as a renewal.
The first consumer deployment attempt also exposed a checksum-canonicalization
defect in the helper/consumer boundary; that deployment was not used as final
evidence. The corrected primary and final gate deployments above are the only
release artifacts claimed here.

The explorer returned HTTP 503 during address-page checks, so no
address-specific explorer URL is claimed as verified.
