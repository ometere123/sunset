# SUNSET — stable StudioNet deployment and live verification ledger

This file records only observed artifacts. Historical failed or superseded
deployments are labelled as such and are not used as proof for the corrected
release.

## Locked environment

| Field | Verified value |
|---|---|
| Network | `studionet` |
| Chain ID | `61999` / `0xf22f` |
| RPC | `https://studio.genlayer.com/api` |
| Local CLI | repository-local `genlayer@0.39.1` |
| Runner | `v0.2.12` |
| Linter | `genvm-linter==0.11.0` |
| Direct Mode | `genlayer-test==0.29.2` |
| Global CLI | not used |

`node scripts/assert_studionet.mjs` independently queried `eth_chainId` and
returned `0xf22f`. No deployment or test in this ledger uses chain 61997,
Studio Dev, Studio Next or a global CLI.

Release commit: `099b7123e1b32c172a0442f8851c0e8247deab31` on `main`.
The corresponding GitHub Actions run
[`42128664898`](https://github.com/ometere123/sunset/actions/runs/42128664898)
completed successfully for the offline, GenVM and pinned-CLI jobs.

## Final source artifacts

| File | SHA-256 | Deployed-byte check |
|---|---|---|
| `contracts/sunset.py` | `beb85615ee8f5ddc785db76f54962f1749d8b479143e000f4b4c4f57e57cb6e5` | exact byte equality; 37,031 bytes |
| `contracts/sunset_gate.py` | `aecb925a4465b0977bbe9512cc9cf97056b9146e1cbe6b50fe1655c3adb9e384` | exact byte equality; 5,251 bytes |

The deployed source was read from the finalized deployment data returned by the
stable RPC and decoded before byte-for-byte comparison. The final committed
source is rechecked after the documentation closeout commit.

## Current hardened primary deployment

- Contract: `0xBDEAF4190a85d1aDA0BD6f82530B0711b25E306f`
- Deployment transaction: `0x3cdcd6c8d0dfe732e76c2e17e60df88f53495dfac6764f0aadc409cd17f4958f`
- Receipt: finalized; `MAJORITY_AGREE`; `eth_getTransactionReceipt.status = 0x1`
- Leader execution: `SUCCESS`
- Deployed source: 37,031 bytes; SHA-256 exactly matches the final committed `contracts/sunset.py`, including the oversized-source fail-closed guard.

## Consumer deployments

### Ended-rule gate

- Address: `0x5Ed933fc2992d466cCa5157160AB9a5d53A7b045`
- Deployment transaction: `0xdc63230d9c831c6eb10c17f57e9fab14537ec10c088cddf996705698649ad686`
- Binding: hardened primary; rule `sunset-hardening-ended-v3`; fingerprint `90c4adf00173de91c443f0b087acfc2eb4895903aafe8f88e41f24fd5f561254`; executor `0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`; operation `sunset-hardening-ended-action-v3`; payload `apply-hardening-ended-policy`
- Action commitment: `46cb7b81085c535a71b414213388e1ae87261e5a07e7dabbf5e9c64e61d5dd04`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; constructor execution `SUCCESS`

### Positive-renewal active-rule gate

- Address: `0x3770b26E4377FF920867A8cfF2A14da18A4d1B93`
- Deployment transaction: `0x7846aa6f9d936b8be8c59ae5c99f75fa243af5e8aa05f15e5a027aa4b5c02422`
- Binding: hardened primary; rule `sunset-hardening-positive-v4`; fingerprint `efc10a0cf412f5081d07e1a0e7cfbbac9b279924ed808714cad5be4c2f0bfb4a`; executor `0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`; operation `sunset-hardening-positive-action-v4`; payload `apply-hardening-positive-policy-v4`
- Action commitment: `515e710233797902fc9af98ca3b587ad4a8c2d2ea467d8c2ad20d2329f93ca36`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; constructor execution `SUCCESS`

### Automatic-expiry gate

- Address: `0x3A6C995b1A41daf1DbBC5B72c02b2dd4826fB812`
- Deployment transaction: `0x9c7939b88370ed5c68273ba77f1b54d72962fb6a99717b872f9f0034df133244`
- Binding: hardened primary; rule `sunset-hardening-expiry-v3`; fingerprint `cfa02007be96b2938dc03d410c75fddf6161f2b10dd645067f0cfd39b7a5af43`; executor `0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`; operation `sunset-hardening-expiry-action-v3`; payload `apply-hardening-expiry-policy`
- Action commitment: `0dac450afc785028e61c66463d0b79f725b06a531e4cab98aa7451a6577da97e`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; constructor execution `SUCCESS`

The explorer service returned HTTP 503 during address-page verification. No
address-specific explorer URL is therefore claimed as independently verified.

## Live StudioNet lifecycle evidence

### Hardened deployment live proofs

These are the final corrected-source proofs. Every transaction below finalized
on StudioNet chain 61999 with `MAJORITY_AGREE`; a contract execution marked
`ERROR` is recorded as an intentional fail-closed rejection, never as success.
The three disposable rules use 900-second epochs and 720-second renewal
windows. These accelerated values demonstrate lifecycle behavior and are not a
production timing recommendation.

The controlled GitHub raw fixtures are protocol-mechanics fixtures. They do not
prove real-world identity, source ownership, actor action, subjective reliance,
legal liability or unrelated external facts.

#### Positive renewal

- Registration `sunset-hardening-positive-v4`: `0x23559d704b6791a9177965da83a99c69461c49172852bc3c04afc6d2b1e4fd7c`; fingerprint `efc10a0cf412f5081d07e1a0e7cfbbac9b279924ed808714cad5be4c2f0bfb4a`; epoch/window/cap `900 / 720 / 1`; initial expiry `1793920297`; hard stop `1793921197`.
- Assessment `0x24bceb10dc338a774badfcec50d2e9fcb670dd6bc44013a01ffe39a6dfde940f`: finalized `MAJORITY_AGREE`, leader and validator executions successful, `JUSTIFICATION_PERSISTS` with a `SAFE` audit.
- Readback: `renewals = 1`, `assessed_epoch = 1`, `expires_at = 1793921197`, `hard_stop = 1793921197`, `status = ACTIVE`, `is_restricted = true`. The extension was exactly one original 900-second epoch.
- The positive gate `0x3770b26E4377FF920867A8cfF2A14da18A4d1B93` read `can_execute = false`, exact bound predicate `false`, count `0`.
- Active exact-action rejection `0x5838cbd70ef71bef40756759ebb2fce3b5d8fb047c5367f8bc0d7662714cefb5` finalized with rollback `SUNSET_RESTRICTION_ACTIVE_OR_UNVERIFIABLE`; count remained `0`.

#### Affirmative early termination

- Registration `sunset-hardening-ended-v3`: `0x925d6f88568792089711367dd3d3a87546ff00d46e28ab12693f420504a6301e`; fingerprint `90c4adf00173de91c443f0b087acfc2eb4895903aafe8f88e41f24fd5f561254`; source `https://raw.githubusercontent.com/ometere123/sunset/main/docs/fixtures/sunset-demo-status-hardening-early.txt`; epoch/window/cap `900 / 720 / 1`; initial expiry `1793919842`; hard stop `1793920742`.
- The fixture was registered while ACTIVE, then published with an explicit RESOLVED update. Assessment `0xa62b93e794f7c8bd30df26a5ec6339f34a566d6679d193d590da8d5d79d87ff3` finalized `MAJORITY_AGREE`, leader execution `SUCCESS`, `JUSTIFICATION_ENDED`.
- Readback: `status = ENDED_EARLY`, `last_verdict = JUSTIFICATION_ENDED`, `renewals = 0`, `is_restricted = false`, `expires_at = 1793919462`.
- The ended-rule gate `0x5Ed933fc2992d466cCa5157160AB9a5d53A7b045` read `can_execute = true` and exact bound predicate `true`.
- Authorized exact action `0x615a70003d6cdce3eea9c268d5ec2b6d1807938c2aa801dd221ea2cbbad51dc2` finalized with return value `1`; `get_execution_count() = 1` and the operation was marked executed.

#### Automatic expiry

- Registration `sunset-hardening-expiry-v3`: `0x90aa10d3db5ae3a4964bb10415d458a7828b318d3eb796d2e2d7857ac9247212`; fingerprint `cfa02007be96b2938dc03d410c75fddf6161f2b10dd645067f0cfd39b7a5af43`; epoch/window/cap `900 / 720 / 0`; initial expiry and hard stop `1793919874`.
- After the real chain clock passed `1793919874`, readback was `status = EXPIRED`, `is_restricted = false`. The expiry gate `0x3A6C995b1A41daf1DbBC5B72c02b2dd4826fB812` read `can_execute = true` and exact bound predicate `true`.
- Exact post-expiry action `0x0ab574372c7148496ebd21bdd019f685358e712c43b9ce2a07124fc9a150382e` finalized with return value `1`; `get_execution_count() = 1` and the operation was marked executed.

#### Consumer authorization, substitution and replay

- Unauthorized executor `0xf240e6cf640d782415494d1b35bb570ab6e37781` submitted `0xfb07b8f582c3a07253ca2b72af56adb33806dbc9a23c7644dfc5ebd59c971f4f` to the ended gate; it finalized with rollback `ONLY_EXECUTOR`, and the count remained `1`.
- New-operation payload substitution `0x49030a14107df815a927448602c805d710f5ecef96a5ad47819c577d850bdde9` finalized with `ACTION_COMMITMENT_MISMATCH`; the count remained `1`.
- Replaying the already consumed exact operation `0xdba87219273d68d88369917f6a087d8525a0f1b2ef42d0bb501083dc2511acdd` finalized with `REPLAY`; the count remained `1`.

#### Fail-closed and oversized evidence

- A separate rule on the corrected primary, `sunset-hardening-positive-v3`, was assessed in `0x31ae5ede97af55753275059e134094217b146d66f4b5842014d36f711cba8032`. The transaction layer finalized `MAJORITY_AGREE`, but the contract result was terminal `INCONCLUSIVE` with `SELF_REFERENTIAL_UNVERIFIABLE_SOURCE`; no extension occurred. This is a finalized negative proof, not a positive renewal.
- Offline and native Direct Mode tests independently cover an oversized source containing an old witness followed beyond the former 12,000-character cutoff by a material contradiction. `_clean_page()` now returns `SOURCE_TOO_LARGE`; neither persistence nor early termination is approved, and expiry is unchanged. Those simulated results are not claimed as live consensus receipts.

### Historical pre-hardening deployment live proofs (superseded)

These superseded proofs used the pre-hardening primary
`0x0Fd9A98eC49Ea04c2b71D7552B62F603D1b12970` and its then-current gates. They
remain historical only. The controlled fixture files are
protocol-mechanics fixtures, not evidence of unrelated real-world incidents,
identity, source ownership, actor action or legal facts.

#### Affirmative early termination

- Rule registration `sunset-fixture-ended-v2`: `0x0e341ef2dafd58137bcb498786c03125db6166807af9a2bf229bc72d0f05569e`; fingerprint `e18606f5fbd4cec96b0f0e062808306d0562a7e1e7cdb3dde8462bd64c7c5fbd`; source `https://raw.githubusercontent.com/ometere123/sunset/main/docs/fixtures/sunset-demo-status-early.txt`; epoch/window/cap `900 / 720 / 1`; initial expiry `1793911952`.
- The source was first observed in its ACTIVE state, then committed and independently retrieved in its RESOLVED state; the no-redirect raw response was confirmed before assessment.
- Assessment `0xb17f12513c6f2702593a04c18fb7b7e86f892ef8a6accc04e50d8ad4f8c7a6d2`: finalized `MAJORITY_AGREE`, leader execution `SUCCESS`, leader result `JUSTIFICATION_ENDED`.
- Readback: `status = ENDED_EARLY`, `last_verdict = JUSTIFICATION_ENDED`, `renewals = 0`, `is_restricted = false`, `expires_at = 1793911519`.
- Ended-rule gate `0x0351CFA149FeB4090Bff1D9EBaDAF77a6badF11F`: `can_execute = true`, exact bound predicate `true`.
- Authorized exact action `0x0fb2430bd893409f63180e7a32e6ce5d979bb1d330b7c70af24b25de7fd7cf0f` finalized with return value `1`; `get_execution_count() = 1`.
- Unauthorized executor `0xf7aa4bcfca965e77bfbf3fdf79057755b09f8ec8e6058b5b5422e1f9eab70298` finalized with leader rollback `ONLY_EXECUTOR`; count remained `1`.
- Replay `0x9298e860ac9e52ab36fd40879ea01742e2c28236019d762c59bcaae95a42a1da` finalized with rollback `REPLAY`; count remained `1`.
- Substituted payload `0x371971d7680bc629f9acecd038221fb85a7e52a5cf3d4f2e88683c49ca2a92a7` finalized with rollback `ACTION_COMMITMENT_MISMATCH`; count remained `1`.

#### Positive renewal and active enforcement

- Rule registration `sunset-positive-v2`: `0x2bda0aa11ad024f35d95a328a496fc5edfdf7510faa0e82ecc45791d040af42b`; fingerprint `a6c935db116a2ffc6f89341dfc14f03c8675e54f07492193648ff9d95575fedf`; source `https://raw.githubusercontent.com/ometere123/sunset/main/docs/fixtures/sunset-demo-status-positive.txt`; epoch/window/cap `900 / 720 / 1`; initial expiry `1793913590`; hard stop `1793914490`.
- Assessment `0x40e377b37d31a307fbf2e0ceb5045ded7b4b345b2d5ea3e7456761f95df04f30`: finalized `MAJORITY_AGREE`, leader execution `SUCCESS`, `JUSTIFICATION_PERSISTS`, `SAFE` audit.
- Readback: `renewals = 1`, `assessed_epoch = 1`, `expires_at = 1793914490`, `hard_stop = 1793914490`, `status = ACTIVE`, `is_restricted = true`; exact extension was one 900-second epoch.
- Positive gate `0xcd69aF94ED4C3CD40bcB3226F46CF4133d6C857C`: `can_execute = false`, bound predicate `false`, count `0`.
- Active exact-action rejection `0x95cfbd5fb8d6e529cf5f1bb824e229dcc79ff68fb3bd5106019f0404d893a0e0` finalized with the expected active/unverifiable restriction rollback; count remained `0`.

#### Fail-closed live negative

- IANA rule registration `sunset-iana-renewed-v2`: `0x64f4ac600b41beb5941070c1b3d5d160cdc91749db7d89d8ccbfa44021e12a3c`.
- Assessment `0xf88aef75a8d46ac1052224ade1133f3493a7803f2650c151cc913a0240e0aead` finalized `MAJORITY_AGREE` at the transaction layer, but the leader result was `INCONCLUSIVE/NO_SOURCE_WITNESS`; no extension occurred. Later readback was `INCONCLUSIVE`, `renewals = 0`, and the rule expired normally. This is not counted as a positive renewal.

#### Automatic expiry

- Rule registration `sunset-expiry-v2`: `0x5ada80000a1644916e37c03a5b5a2bff5bcb423a777778784273f8983e4dee2c`; fingerprint `6300306882480b1ed4babe412cad53f585864758a4f32d339b32ce901437b41d`; epoch/window/cap `900 / 720 / 0`; initial expiry and hard stop `1793913991`.
- Before expiry, gate `0xbb98ad6d84bAd27cA2F51A5c5FEF545b72C40c3E` read `can_execute = false` and exact bound predicate `false`.
- After the real chain clock reached `1793913991`, the rule read back `status = EXPIRED`, `is_restricted = false`; the gate read `can_execute = true` and its exact bound predicate `true`.
- Exact post-expiry action `0x09ea163c7db1ca40e144e5eb67e7faa6fe52e27771f05a3791e206c07669c250` finalized `MAJORITY_AGREE` with leader `SUCCESS` and return value `1`.
- Readback after the exact action: `get_execution_count() = 1`; `is_executed("expiry-v2-action-1") = true`.
- Replay attempt using the same operation with a substituted payload `0xba0190a110d7c9de239f2e75d27b733a01b4164acf45158bfed2dbc8d315ac88` finalized with rollback `REPLAY`; count remained `1`.
- New-operation payload substitution `0xf07c3f32aa2e03d08c0f4370a271f4496d6d4d9f0851bae9ff05cef0d1c13478` finalized with rollback `ACTION_COMMITMENT_MISMATCH`; count remained `1`.

### Historical superseded deployment: positive renewal and active enforcement

Rule `sunset-iana-proof-final` was registered on the corrected primary in:

- Registration: `0x2b83915fddc2294e7da7f712ae8f412a2e43069a6703c098a10914bc88e92ab7`
- Fingerprint: `eb208aed6616dc48c8de610e9278d57b09125adb51af31e9a7dc4ab3877e3fbe`
- Source: `https://www.iana.org/help/example-domains`
- Epoch/window/cap: `900 / 720 / 1`
- Initial expiry: `1793901751`
- Hard stop: `1793902651`

The assessment finalized in:

- Assessment: `0x7c75c7c2dffc3ae5046fe2763f400ff52468b6ff160421946947b86a821408d0`
- Consensus: `MAJORITY_AGREE`
- Leader result: `JUSTIFICATION_PERSISTS`, with a source witness and `SAFE` audit
- Readback: `renewals = 1`, `assessed_epoch = 1`, `expires_at = 1793902651`, `hard_stop = 1793902651`, `status = ACTIVE`, `is_restricted = True`
- Exact extension: `1793901751` to `1793902651`, exactly one original 900-second epoch

The same active rule was bound to the positive-rule gate. The exact active
execution attempt finalized in:

- `0x7e5adf636080be0684af780847e857fd8700a37f55f39e158603b1ee63a3a874`
- Finalized/accepted `MAJORITY_AGREE`; leader execution `ERROR`
- Gate readback: `can_execute = false`, `can_execute_bound = false`, execution count `0`

The error is the expected fail-closed active restriction rejection; it is not
reported as a successful downstream action.

### Historical superseded deployment: automatic expiry, exact action, substitution and replay

Rule `sunset-expiry-final` was registered with cap zero:

- Registration: `0x5b046d115d4491f34e9b36814940e7f2c9560e66f56b31deee20734cdfd5d010`
- Fingerprint: `53d5083ff75ae89f73dbbbc04556d9bdfc5bb1211b6c64357d0a29f30b2b782f`
- Epoch/window/cap: `900 / 720 / 0`
- Initial expiry and hard stop: `1793902376`
- Before expiry: bound gate `can_execute = false`

After waiting for the actual 900-second expiry without changing transaction
timestamps, the rule read back as `EXPIRED`, `is_restricted = false`, and the
gate read back `can_execute = true`.

- Wrong-payload transaction: `0xf23869e6cda96daaf9928f3998f208cc6823982f5630613dc606b685abe1f44d`; finalized/accepted, leader execution `ERROR`, expected payload mismatch, count unchanged
- Exact action transaction: `0x4755e1412544e266775d9e4d2e2452135a6ffc99085892040503e9b05ecb72e9`; finalized/accepted `MAJORITY_AGREE`, leader execution `SUCCESS`, return value `1`
- Exact readback: `get_execution_count() = 1`; `is_executed("iana-expiry-action-1") = true`
- Replay transaction: `0x177c3dcb0f7f3a9e04328cc9f707e73cd11c572113702d69d25c8fc06e609fe1`; finalized/accepted, leader execution `ERROR`, expected `REPLAY`, count remained `1`

### Historical bounded failure and prior deployment evidence

Earlier corrected deployments recorded bounded `PROOF_RETRYABLE` and terminal
`INCONCLUSIVE` assessments without extending expiry. These are retained as
fail-closed historical evidence, not as successful renewals. The former
assessment transactions `0x6a105cbc898484c75b8549179be9835dd6cdee591a85e49462ffc84fc143a79c`
and `0x77fe84104999b9c7ef3d490e42c473e78da8a69a75294f28b3016bab1e12c912`
finalized `MAJORITY_DISAGREE`; no renewal was applied.

The previous `https://www.iana.org/domains/example` demonstration was not used
for the corrected positive proof. The corrected positive proof used
`https://www.iana.org/help/example-domains`, observed as HTTP 200 with no
redirect header by the pinned web observation path and containing the quoted
material. Public-page retrieval still does not prove real-world identity,
actor performance, source ownership, subjective reliance or legal liability.

An additional disposable rule `sunset-ended-final` was registered on the
corrected primary in `0xa246532188994b03a19554bff9c270d66d4daf23b5a0c888ddaff39439097651`.
Its immutable criterion asked whether the same IANA source affirmatively stated
that example domains were available for registration or transfer, while the
source said the opposite. An initial assessment
`0xd7e1a694c1f34fc8fd55e40e7459f662d5bf228a0c9469392b72228efad72118` finalized
with leader/validator agreement on the transaction but rolled back as
`TOO_EARLY` before the renewal window. A second eligible attempt
`0x813c408a85e19349d4a6d07c80601093f537fe95dd15fc0091dfa65494019fac`
finalized `MAJORITY_DISAGREE`; the leader proposed `JUSTIFICATION_ENDED`, but
the disagreement prevented any state transition. Readback remained
`ACTIVE`, `renewals = 0`, `assessed_epoch = 0`, and no assessment receipt was
created. This is live evidence of correct fail-closed disagreement handling,
not proof of early termination.

The older deployment lacked a finalized unauthorized-executor transaction
because its available funded alternate signer could not be unlocked. The
corrected deployment proof above supersedes that limitation: the disposable
alternate signer `0xf240e6cf640d782415494d1b35bb570ab6e37781` produced the
finalized `ONLY_EXECUTOR` rollback and the bound gate counter remained `1`.

## Tool and dependency evidence

- `node scripts/assert_studionet.mjs`: passed, `eth_chainId = 0xf22f`
- Local CLI: `0.39.1`
- Offline tests: 60 passed
- Direct Mode: 18 passed, including native `run_validator()` calls
- Preflight: 45 assertions passed
- GenVM lint/schema: both contracts passed under linter `0.11.0`, runner `v0.2.12`
- `pip check`: passed
- `npm audit --omit=dev --audit-level=high`: passed
- `pip-audit --strict`: not clean; 17 advisories across five pinned development-tool packages. These are documented toolchain findings, not deployed-contract findings.
- Final GitHub Actions: the final successful run is recorded in the release
  report and linked from the repository Actions history after closeout.

Only finalized receipts and readbacks above are release evidence. A submitted
transaction hash, `ACCEPTED` status without successful execution, an offline
mock or an explorer URL that was not independently reachable is not treated as
proof of a live successful operation.
