# NSSF excerpt repair after the corpus transcription fix (2026-09-25)

Repair round, no model regeneration. rulespec-ug runs with
`run-generated-guard: false`. No rule, formula, parameter value or
companion test changes.

## Trigger

[axiom-corpus#751](https://github.com/TheAxiomFoundation/axiom-corpus/pull/751)
re-extracted the NSSF Act (Cap. 230) ss. 10-12 rows as
`2026-09-25-ug-nssf-contributions` and cut `ug-rulespec-2026-09-25`. The July
rows (`2026-07-08-ug-nssf-contributions`, in `ug-rulespec-2026-07-12`) carried
OCR misreads and words cut at the right margin of the scan. This repository
quoted five of those damaged strings as proof excerpts, and they stop being
verbatim once the toolchain re-pins.

## Findings

| Module | Excerpt on `main` (July text) | Repaired excerpt (corrected text) |
| --- | --- | --- |
| s.10, `nssf_employee_share` | employee’s share **ofa** standard **contributi** of five percent calculated on the total wages | employee’s share of a standard contribution of five percent calculated on the total wages |
| s.10, `nssf_employer_net_share` | same | same |
| s.12, excepted-employee condition | ... fifty-five years in **respec** of whom the Minister has specifically applied this section | ... in respect of whom ... |
| s.12, wage rounding | total wages payable to such persons calculated from **fifly** cents or more to the nearest multiple of a shilling | ... from fifty cents ... |
| composed pipeline, employee share | deduct from the monthly **wa** payment ... share **ofa** standard **contributi** of five percent ... | deduct from the monthly wage payment ... share of a standard contribution of five percent ... |

Also repaired:

- **s.10 summary.** It quoted "to that employce" and gave the s.11 rate as "5 percent". The print says "five percent".
- **s.11 and s.12 `source_verification.source_sha256`.** Each pin is the SHA-256 of its row body, so both are updated to the new rows: s.11 `e11cbc40…`, s.12 `086014e1…`.

## Checks

- All 26 NSSF excerpts on `main` are verbatim in the July rows. All 26 on this branch are verbatim in the 2026-09-25 rows. No excerpt outside the five above changes.
- The s.11 excerpts all quote text that the correction left unchanged.
- Numbers: no parameter value or formula literal changes. `fifty cents` is now readable in the s.12 row; the module still computes the rounding threshold as `wage_rounding_multiple / 2`.
