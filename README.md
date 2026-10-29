# SUNSET — Emergency powers that expire unless justified again

> **Invariant:** A temporary restriction becomes inoperative at its on-chain
> deadline without any cleanup transaction. Only independently verified,
> current evidence satisfying a *frozen continuation criterion* can extend
> it — by exactly one precommitted epoch, within an immutable lifetime cap.

Sunset is a reusable **GenLayer Intelligent Contract primitive** for expiring
temporary restrictions: emergency withdrawal limits, incident controls,
special administrative permissions, access suspensions, and other time-bound
governance measures. It is **contract-only**: no frontend, no backend,
no off-chain authority and no Docker requirement.

The interesting mechanism is the **default-to-expiration safety property**.
GenLayer consensus only interprets evidence relative to an immutable rule; a
small deterministic state machine controls deadlines, replay resistance,
authorization, and the maximum possible lifetime.

| Evidence conclusion | Effect |
|---|---|
| `JUSTIFICATION_PERSISTS` | Extend exactly one original epoch, subject to hard cap |
| `JUSTIFICATION_ENDED` | Mark terminal and stop restricting immediately |
| `INCONCLUSIVE` | Never extend; restriction dies at current deadline |
| No assessment / failed consensus | No state change; deadline still arrives |

**Network locked:** `studionet`, chain **61999**,
RPC `https://studio.genlayer.com/api`. The repository depends on local,
**stable GenLayer CLI 0.39.1**, not a global CLI or a release candidate.

## The mechanism

1. A rule owner commits to a restriction, the exact public HTTPS evidence
   source, a continuation criterion, an epoch duration, an assessment window
   and a maximum number of renewals.
2. A rule begins active with its first epoch's deadline. Its immutable
   fingerprint binds all original terms and the owner.
3. In the final renewal window, **any wallet** may request an assessment,
   supplying the expected epoch and deadline (optimistic concurrency guard).
4. The leader and validators independently fetch the frozen source, compare
   source digests and independently classify the same immutable question.
   Decisive judgments carry a verbatim excerpt. Disagreement cannot certify
   an extension.
5. The contract applies exactly one of the three fixed outcomes. No owner,
   caller or LLM can extend the epoch length, modify the criterion, switch
   the source, resurrect an expired rule, or breach the absolute hard stop.
6. Consumers call `is_restricted(id)` at execution time. At or after expiry
   it returns false *even if nobody calls* `seal_expired`.

The rule owner may **revoke early**, never prolong directly. There is no
administrator override and no rule-editing API. An `INCONCLUSIVE` assessment
consumes its epoch attempt; callers cannot repeatedly sample models until they
obtain a favourable renewal verdict.

## Repository

| Path | Purpose |
|---|---|
| `contracts/sunset.py` | Main intelligent contract and standalone registry |
| `contracts/sunset_gate.py` | Immutable-fingerprint IC consumer; a demonstrator, not a transfer contract |
| `tests/test_offline.py` | Executable state-machine / adversarial shim tests |
| `tests/direct/` | Official GenLayer Direct Mode tests |
| `scripts/preflight.py` | Offline network/structure/security assertions |
| `scripts/guarded-deploy.mjs` | Fail-closed local CLI + live chain pre-sign guard |
| `docs/` | Consensus rules, security, deployment, reviewer walkthrough |

## Setup and verification

Requirements: Python 3.12+, Node 20+, an ordinary Git checkout.

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
python3 scripts/source_hashes.py
```

The CLI is invoked at `./node_modules/.bin/genlayer`. Check the selected
network before signing:

```bash
./node_modules/.bin/genlayer network set studionet
./node_modules/.bin/genlayer network info
npm run deploy:sunset
```

`deploy:sunset` rechecks the installed CLI package, selected network alias,
RPC URL, and an independent live `eth_chainId` response **before** the
CLI can send a deployment. It requires an unlocked/funded local account.
Never interpret a submitted transaction or an `ACCEPTED` response as
`FINALIZED` success.

After registering a demonstration rule, deploy the optional consumer:

```bash
npm run deploy:gate -- 0xSUNSET_ADDRESS rule-id EXACT_64_HEX_FINGERPRINT
```

The gate binds to the registry address, rule ID and fingerprint in its
constructor. It refuses actions while the rule is active, and permits them
after the deadline *without requiring anyone to settle expiry*. It contains
no funds and has no mutable owner switch. See [reviewer demo](docs/REVIEWER_DEMO.md).

## What Sunset does **not** assert

- A consensus certificate means validators independently agreed under the
  specified evidence procedure. It is not proof that a website is authentic,
  that an incident exists, or that a policy is lawful.
- Rules are only restrictions **inside applications that voluntarily integrate
  the gate**. Registering a rule does not seize rights over unrelated wallets.
- The first 12,000 decoded characters of the source are assessed. Dynamic or
  inconsistent pages can cause inconclusive results, which fail toward expiry.
- Time follows the GenVM transaction timestamp, not the validator machine's
  wall clock. Deployment finality and liveness have separate limitations.

Deployment IDs, validator votes, transaction hashes and source-parity evidence
are never assumed. See [deployment evidence](docs/DEPLOYMENT.md) for the
verification gates that must be completed with a real StudioNet wallet.
