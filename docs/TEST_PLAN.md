# Test plan and verification record

## Commands

```text
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
node scripts/assert_studionet.mjs
```

`tests/direct` is the verified Direct Mode location for this repository. The
pinned `genlayer-test==0.29.2` API exposes `VMContext.run_validator`; the suite
uses it directly for false leader proofs, fabricated ended/consistent results,
extra fields, source drift, provider failure and recovery. On Windows the
test-only `tests/direct/conftest.py` replaces the package's unlink-before-close
temporary stdin implementation with an anonymous pipe. The contract and pinned
runner remain unchanged; Linux CI does not activate the shim.

## Coverage targets

- immutable rule registration, canonical source and domain-separated fingerprint;
- HTTPS/userinfo/port/query/fragment/encoding/IP/private-wrapper rejection;
- owner-only assessment, revoke authorization, duplicate/stale heads and expiry;
- exact one-epoch renewal, hard stop, ended terminal state and fail-closed
  semantic inconclusive result;
- unavailable HTTP source, malformed model/audit output, bounded retry and
  exhausted recovery with preserved receipts;
- independent validator re-fetch, source drift, malformed leader result,
  fabricated classification and adversarial positive audit;
- Gate registry/rule/fingerprint binding, executor authentication, exact action
  payload commitment, wrong payload/operation rejection and replay protection;
- stable RPC identity, local CLI pin, source hash reporting and contract schemas.

## Baseline and current observations

The preserved baseline commit is `2d3929c9c4ab2dfd6b3e7d1720fddcea5f224976`.
The baseline had 38 offline tests, 30 preflight assertions, both contracts linted,
and 8 Direct Mode tests. The initial Windows Direct Mode run failed before
contract import because genlayer-test 0.29.2 unlinked an open temp stdin file;
the repository test-only pipe shim then made the native suite executable.

The current local run is 56 passing pytest tests, including 14 Direct Mode
tests, with 45 preflight assertions. Both native validator paths and the
Windows-only test shim were exercised locally. Simulated/offline tests are not
live StudioNet consensus evidence; the finalized live receipts are recorded in
`docs/DEPLOYMENT.md`.

The code-and-contract evidence workflow passed all three jobs: [GitHub Actions
run 42058870267](https://github.com/ometere123/sunset/actions/runs/42058870267).
The final documentation-only closeout reruns the same workflow; its result is
reported with the final remote SHA.
