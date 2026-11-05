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
  fabricated classification, substantive quote/reason divergence and
  adversarial positive audit;
- Gate registry/rule/fingerprint binding, executor authentication, exact action
  payload commitment, wrong payload/operation rejection and replay protection;
- stable RPC identity, local CLI pin, source hash reporting and contract schemas.

## Baseline and current observations

The preserved baseline commit is
`4f7a088e6e31234230deea95640975cb7df03a1f`. The historical reviewed release
had 52 offline tests and 16 Direct Mode tests. The current release includes 60
offline pytest tests, 18 Direct Mode tests (78 total), 45 preflight assertions
and two focused mutation tests. The initial Windows Direct Mode run failed before
contract import because genlayer-test 0.29.2 unlinked an open temp stdin file;
the repository test-only pipe shim then made the native suite executable.

The final truncation-hardening pass started from commit
`1650f737c07bcfa21b3ef6f9de648e8e53618253` and added the oversized-source
regressions in both offline and native Direct Mode suites. The contract change
was deployed as the hardened primary recorded in `docs/DEPLOYMENT.md`.

The current local run is 60 passing offline tests and 18 passing Direct Mode
tests. Both native validator paths and the Windows-only test shim were exercised
locally. Simulated/offline tests are not live StudioNet consensus evidence; the
finalized live receipts are recorded in `docs/DEPLOYMENT.md`.

The final workflow result and commit are recorded after the documentation
closeout in the repository release ledger and the GitHub Actions run linked
from the final release commit. Historical run `42086859791` and commit
`07b933c08d79152244f6bb627730307918ddea88` are retained only as prior evidence.
