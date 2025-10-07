# Executable Answers v0.1 — Claim-Validator MVP

Validate numeric-growth claims in any prose answer. Emits a ClaimGraph and a verification report.

## Install
```bash
pip install -e .

Usage

exa-validate validate tests/fixtures/answer_pass.md --outdir out
exa-report report --outdir out

Artifacts:
•out/claimgraph.json — extracted claims with normalized calc fields.
•out/verification_report.json — pass/fail/unchecked counts and per-claim details.
•out/sources.json — any DOIs detected in the text.

Notes
•Scope is intentionally tight (one claim type) for shippability.
•Extend extraction patterns and add tests before broadening claim types.
