# SUNSET — bounded, consensus-backed expiry of temporary restrictions

Sunset is a reusable GenLayer Intelligent Contract primitive for temporary
restrictions that expire unless an immutable continuation rule is independently
supported again. A rule owner commits the restriction, criterion, public HTTPS
source, epoch, renewal window and lifetime cap. GenLayer leader and validator
paths independently fetch and classify that same frozen source; deterministic
contract code alone controls whether one fixed epoch is renewed or the rule
falls toward expiry.

This is a protocol for bounded on-chain enforcement, not proof of website
ownership, real-world identity, action completion, subjective reliance, legal
liability or external truth.

## Security invariant

At every execution-time read, a rule is restricted only while its terminal state
is `LIVE` and the transaction timestamp is before both its current expiry and
immutable hard stop. No cleanup transaction is needed. Only an exactly agreed
`JUSTIFICATION_PERSISTS` result can extend the previous expiry by one original
epoch. `JUSTIFICATION_ENDED` ends the rule immediately. `INCONCLUSIVE`, failed
consensus, unavailable evidence and unresolved recovery never extend it.

## Lifecycle

1. The owner registers a unique rule. The source URL is canonicalized to a
   conservative HTTPS form and the fingerprint binds every immutable term.
2. The owner may request an assessment only inside the fixed renewal window,
   with the expected epoch and expiry. This owner authentication prevents a
   third party from consuming another party's recovery allowance during an
   outage.
3. The leader fetches the source and runs the primary semantic classification.
   A positive result receives one bounded adversarial compatible-reading audit.
4. The validator independently repeats the source fetch, primary classification
   and positive audit. It accepts only an exact, typed match of the full result,
   including source digest, witness quote, reason, retryability and audit.
5. A transient fetch/model/audit failure returns `PROOF_RETRYABLE` without
   changing the expiry. At most two such attempts exist for an epoch; exhaustion
   finalizes `INCONCLUSIVE`. A genuine semantic `INCONCLUSIVE` is terminal for
   that epoch immediately.
6. Consumers read the rule at execution time. `SunsetGate` additionally binds a
   typed registry address, rule fingerprint, executor address and a domain-
   separated commitment to one exact operation ID and payload.

## Public contracts

`contracts/sunset.py` exposes `register_rule`, `assess_renewal`, `revoke`,
`seal_expired`, `is_restricted`, `get_rule`, `get_assessment` and
`get_assessment_attempt`. Rule terms, evidence namespace and hard stop are
immutable after registration. Assessment receipts preserve each bounded
attempt.

`contracts/sunset_gate.py` is a minimal interoperability consumer. Its
constructor verifies the registry, rule and fingerprint, then freezes the
executor and action commitment. `execute_once(operation_id, payload)` fails
closed on an active/unverifiable rule, wrong executor, substituted payload or
replay. It moves no funds and is not a wallet, escrow or application backend.

Compute the exact consumer binding with:

```bash
node scripts/action_commitment.mjs <registry> <rule-id> <fingerprint> <operation-id> <payload>
```

## Locked environment

- Network: `studionet`
- Chain ID: `61999` (`0xf22f`)
- RPC: `https://studio.genlayer.com/api`
- Repository-local CLI: `genlayer@0.39.1`
- GenVM linter: `0.11.0`
- Direct Mode: `genlayer-test==0.29.2`
- Stable Direct Mode runner: `v0.2.12`

The global GenLayer CLI is not used. There is no frontend, backend, database,
Docker service, scheduler dependency, custody or application wallet UI.

## Verification

```bash
npm ci
python3 -m pip install -r requirements-dev.txt
python3 scripts/preflight.py
python3 -m compileall -q contracts scripts tests
python3 -B -m unittest discover -s tests -p test_offline.py -v
GENVM_VERSION=v0.2.12 genvm-lint check contracts/sunset.py
GENVM_VERSION=v0.2.12 genvm-lint check contracts/sunset_gate.py
GENVM_VERSION=v0.2.12 genvm-lint schema contracts/sunset.py
GENVM_VERSION=v0.2.12 genvm-lint schema contracts/sunset_gate.py
python3 -m pytest -q tests/direct
python3 scripts/source_hashes.py
node scripts/assert_studionet.mjs
```

The repository's verified Direct Mode command is `python3 -m pytest -q
tests/direct`; the commonly shown `gltest direct_tests -v -s` command is not
applicable because this repository uses the pinned pytest plugin layout. The
Direct Mode suite explicitly calls `direct_vm.run_validator()` where supported.
On Windows, `tests/direct/conftest.py` is a test-only compatibility shim for a
file-unlink defect in genlayer-test 0.29.2; it is inactive on CI's Linux runner.

## Evidence and limitations

Public HTTPS material is treated as untrusted data and is independently
retrieved by leader and validator. Exact quotes must occur in the retrieved,
whitespace-normalized extract. The source URL filter rejects credentials,
explicit ports, queries, fragments, percent-encoding, IP literals, private
namespaces and common DNS-to-private-IP wrapper domains. The GenVM v0.2.12 web
response exposes status, headers and body but not a cryptographically
authenticated DNS owner or final redirect destination; those remain explicit
trust limitations. Public pages do not independently prove the real-world
actor, action, identity, source ownership or legal consequence.

No live StudioNet deployment, receipt, address or source-parity claim is made
until it appears in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) with a finalized,
successful execution result.
