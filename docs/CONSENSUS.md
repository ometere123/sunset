# Consensus specification

The question is **not** whether an AI believes a restriction is useful.
The frozen question is: *Does affirmative, fresh evidence at the original
public HTTPS source establish that the original continuation condition
continues to hold at the assessment timestamp?*

The three categories are ordered as independent symbols; no score or arbitrary
confidence threshold may choose an extension.

| Verdict | Required observation | Deterministic result |
|---|---|---|
| JUSTIFICATION_PERSISTS | Current affirmative support, direct source quote | old expiry + fixed epoch |
| JUSTIFICATION_ENDED | Current affirmative resolution, direct source quote | terminal, expiry now |
| INCONCLUSIVE | Insufficient, stale, conflicting, unavailable evidence | current expiry unchanged; epoch attempt consumed |

For each assessment:

1. The deterministic precheck verifies an active rule, matching epoch and
   deadline, unused assessment slot, remaining renewal capacity and permitted
   renewal window.
2. The leader fetches the immutable URL, extracts at most 12,000 characters,
   normalizes whitespace, hashes the normalized extract with Keccak-256, and
   asks a narrow, injection-aware question about the frozen criterion.
3. A decisive answer must contain a direct contiguous source quote of 12–220
   characters and a bounded reason code. Unsupported output normalizes to
   INCONCLUSIVE.
4. Each validator independently re-fetches the source and asks the same
   semantic question. It checks exact source digest, exact categorical verdict,
   and matching verbatim quote for a decisive result.
5. Only a consensus-accepted result reaches deterministic state transitions.
   Recheck the epoch and expiry after consensus. The receipt binds the assessed
   epoch, old and resulting deadlines, outcome, source digest and excerpt.

An unavailable source may deterministically yield INCONCLUSIVE if validators
observe the same unavailable extract. A source that changes during verification
may produce disagreement and no accepted write. **Both situations still result
in natural expiry** unless a successful renewal transaction is finalized first.

Positive assessments may advance `renewals` by one, up to the cap. The absolute
`hard_stop` is committed at registration as `created + epoch * (cap + 1)`.
Repeated attempts cannot extend beyond it. An ended or revoked rule is terminal.

No model sets an expiry, votes for a governance amendment, chooses a beneficiary,
or awards funds. The classifier only returns a bounded evidence relationship.

### Known limits

- Exact source digest agreement prioritizes safety over liveness on volatile
  pages. Some dynamic status pages are unsuitable for this primitive.
- Evidence is public; source authenticity, truthful publisher operation and
  source continuity are integration concerns.
- The source may change after an assessment; its digest and excerpt provide
  an audit witness, not immutable storage of the whole webpage.
- No live observability is promised when the source cannot be reached or a
  transaction cannot finalize. Expiry remains the fallback.
