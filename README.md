# rulespec-ug

Uganda RuleSpec source registry.

This repository targets a Uganda tax-benefit surface: national income tax (PAYE), the rental income regime, the presumptive small-business tax, social security contributions (NSSF), the Local Service Tax, VAT and excise duties, and the cash-transfer programmes needed for household-level calculations (Senior Citizens Grant). Uganda is a unitary state, so all encoded law lives under a single `ug/` national namespace; the Local Service Tax is levied by local governments under a national schedule and is encoded nationally.

Uganda's tax year runs 1 July to 30 June. The validation year for encoded amounts is **FY2025/26**; effective dates follow the amending Act's commencement (typically 1 July of the fiscal year).

## Source priority

Policy must come from the furthest upstream available source.

1. Uganda Gazette Acts of Parliament (assented prints from the Parliament of Uganda; Uganda Gazette supplements) and the Law Development Centre revised editions — the authentic text of the Income Tax Act (Cap 340), the Value Added Tax Act (Cap 349), the Excise Duty Act, the National Social Security Fund Act, the Local Governments Act, and their amending Acts.
2. Uganda Revenue Authority (URA) rate tables, PAYE guides, and practice notes only after the governing Act is identified.
3. Ministry of Gender, Labour and Social Development official programme documentation for the Senior Citizens Grant (SAGE/SCG) and other rules set administratively rather than by Act.
4. Oracles only for household-level parity tests against an external source that can calculate the same household case, never as law.

## Oracle scope

An oracle is an executable, pinned external calculator that accepts household-level inputs and returns household-level tax-benefit outputs comparable to Axiom outputs. Aggregate simulators, distributional reports, parameter documentation, and public model summaries are not oracles for RuleSpec parity, even when they are useful as background references.

The Uganda household oracle is **UGAMOD**, the SOUTHMOD tax-benefit microsimulation model for Uganda (UNU-WIDER). UNU-WIDER approved access to the SOUTHMOD A4.0 bundle on 2026-07-07, and UGAMOD is wired by nine per-case comparison suites in [axiom-oracles](https://github.com/TheAxiomFoundation/axiom-oracles) (`comparisons/ug-*.yaml`), run on system UG_2025 (FY2025/26). The SOUTHMOD_A4.0 Adhesion Agreement bars giving the bundle to third parties, so those suites run only on the machine that holds it, never on shared CI; the committed reports are the record. `data/oracles/oracle-index.json` pins the bundle hash and lists each suite with the outputs it compares.

## Layout

- `ug/statutes/`: Uganda primary law encoded as RuleSpec (Acts of Parliament — Income Tax Act Cap 340, VAT Act, Excise Duty Act, NSSF Act, Local Governments Act, amending Acts).
- `ug/regulations/`: statutory instruments and delegated instruments made under the governing Acts.
- `ug/policies/`: URA administrative guidance and rate surfaces, and social-protection programme rules (Senior Citizens Grant) set administratively.
- `ug/programs/`: declarative compose specs, one per (jurisdiction, program, period).
- `data/corpus/`: source inventory, ingestion manifests, provision locators, and promoted official extracts.
- `data/coverage/`: tax-benefit coverage backlog and official source map (`tax-benefit-source-map.json`: one track per instrument, citing governing law and pointing at modules and comparison suites).
- `data/oracles/`: the pinned household-level comparison oracle (UGAMOD) and its wired comparison suites.

## Money proof-atom coverage

Every policy-bearing monetary value — currency parameters, currency parameter-table cells, and currency literals in derived formulas — must carry a proof atom whose source cites a provision. The shared `validate-rulespec` workflow enforces this with `axiom-encode proof-validate --money-atoms-only`, reading the repo-root ratchet `known-missing-money-atoms.yaml`.

`known-missing-money-atoms.yaml` is seeded at `total_allowed: 0`: because the repo starts with no encoded monetary values, there is no backlog to burn down, and CI enforces a strict zero allowance from the first encoded module onward. Every monetary value added by encoding must ship with a proof atom citing a Uganda provision. This floor may only be lowered, never raised.

## Listing gates (app visibility)

This lane is marked `app_visibility = "experimental"` in `.axiom/registry.toml`, which keeps its encodings off the axiom.org app surfaces (encoded search, jurisdiction tiles, navigation encoding badges) while it matures; corpus provisions remain visible under release-scopes gating. Flip the marker to `"public"` in a one-line PR when all four gates hold:

1. **Composed end-to-end calculation** — a `ug/programs/` compose spec chains the modules so the flagship calculation (gross income to individual income-tax liability, and onward to disposable income) runs as one program. Status: **open** — `ug/programs/income-tax/fy-2025-26.yaml` composes income tax and the employee NSSF share, but the pipeline takes chargeable income as an input, has no Local Service Tax stage and does not declare `module.kind: composition` ([rulespec-ug#21](https://github.com/TheAxiomFoundation/rulespec-ug/issues/21) item 2).
2. **Independent numerical validation** — UGAMOD (SOUTHMOD Uganda) per-case parity, or independently published worked figures (URA PAYE tables) reproduced exactly as companion fixtures citing their sources. Status: **partially met** — UGAMOD comparisons run for nine suites, and all 64 comparisons on 58 synthetic cases match, none dispositioned (see `data/oracles/oracle-index.json`). Not all of that is independent validation. ug-paye-rate-schedule and ug-dispy give Axiom the gross pay as chargeable income, so they test the rates and the composition, not how chargeable income is derived; ug-vat takes its taxable value from the model's own VAT base, so it tests the 18% rate only; ug-dispy leaves out the Local Service Tax on both sides; ug-lst tests a gross-pay base only; and ug-fuel-excise checks the 2024 rows, not the FY2025/26 law. The compared modules carry manual-attestation manifests and are not supervised-encoder output ([rulespec-ug#21](https://github.com/TheAxiomFoundation/rulespec-ug/issues/21)), and not every module has a comparison (NSSF sections 11 and 12 and the section 22 rental deduction have none). No URA worked figures are reproduced as fixtures yet.
3. **Open legal questions closed or prominently caveated** — Status: **open**. Recorded questions: whether the Local Service Tax base ("monthly take-home salary") is gross or net pay, and whether the Income Tax Act allows the tax as a deduction from employment income (rulespec-ug#21 item 2); whether Cap. 230 limits contributions by age, which needs the Act's eligible-employee definition (rulespec-ug#21 item 1); and the FY2025/26 vintage of the excise rows, pending capture of the FY2025/26 amendment package.
4. **Second-maintainer review** — another maintainer has reviewed module scope and semantics. Status: **open**.
