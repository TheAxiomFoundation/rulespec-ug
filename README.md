# rulespec-ug

Uganda RuleSpec source registry.

This repository targets a Uganda tax-benefit surface: national income tax (PAYE), the rental income regime, the presumptive small-business tax, social security contributions (NSSF), the Local Service Tax, and the cash-transfer programmes needed for household-level calculations (Senior Citizens Grant). Uganda is a unitary state, so all encoded law lives under a single `ug/` national namespace; the Local Service Tax is levied by local governments under a national schedule and is encoded nationally.

Uganda's tax year runs 1 July to 30 June. The validation year for encoded amounts is **FY2025/26**; effective dates follow the amending Act's commencement (typically 1 July of the fiscal year).

## Source Priority

Policy must come from the furthest upstream available source.

1. Uganda Gazette Acts of Parliament (assented prints from the Parliament of Uganda; Uganda Gazette supplements) and the Law Development Centre revised editions — the authentic text of the Income Tax Act (Cap 340), the Value Added Tax Act (Cap 349), the Excise Duty Act, the National Social Security Fund Act, the Local Governments Act, and their amending Acts.
2. Uganda Revenue Authority (URA) rate tables, PAYE guides, and practice notes only after the governing Act is identified.
3. Ministry of Gender, Labour and Social Development official programme documentation for the Senior Citizens Grant (SAGE/SCG) and other rules set administratively rather than by Act.
4. Oracles only for household-level parity tests against an external source that can calculate the same household case, never as law.

## Oracle Scope

An oracle is an executable, pinned external calculator that accepts household-level inputs and returns household-level tax-benefit outputs comparable to Axiom outputs. Aggregate simulators, distributional reports, parameter documentation, and public model summaries are not oracles for RuleSpec parity, even when they are useful as background references.

The Uganda household oracle target is **UGAMOD**, the SOUTHMOD tax-benefit microsimulation model for Uganda (UNU-WIDER, in collaboration with the Ministry of Finance, Planning and Economic Development). The licensed SOUTHMOD A4.0 bundle is in hand (the same bundle and runtime already wired for Ghana parity in rulespec-gh) with systems UG_2016–UG_2025 and three bundled input datasets; oracle wiring follows the Ghana recipe. `data/oracles/` records the pinned bundle.

## Layout

- `ug/statutes/`: Uganda primary law encoded as RuleSpec (Acts of Parliament — Income Tax Act Cap 340, VAT Act, Excise Duty Act, NSSF Act, Local Governments Act, amending Acts).
- `ug/regulations/`: statutory instruments and delegated instruments made under the governing Acts.
- `ug/policies/`: URA administrative guidance and rate surfaces, and social-protection programme rules (Senior Citizens Grant) set administratively.
- `programs/`: declarative compose specs, one per (jurisdiction, program, period), guarded by `guard-programs-root`.
- `data/corpus/`: source inventory, ingestion manifests, provision locators, and promoted official extracts.
- `data/coverage/`: tax-benefit coverage backlog and official source map.
- `data/oracles/`: pinned household-level comparison references (UGAMOD).

## Money proof-atom coverage

Every policy-bearing monetary value — currency parameters, currency parameter-table cells, and currency literals in derived formulas — must carry a proof atom whose source cites a provision. The shared `validate-rulespec` workflow enforces this with `axiom-encode proof-validate --money-atoms-only`, reading the repo-root ratchet `known-missing-money-atoms.yaml`.

`known-missing-money-atoms.yaml` is seeded at `total_allowed: 0`: because the repo starts with no encoded monetary values, there is no backlog to burn down, and CI enforces a strict zero allowance from the first encoded module onward. Every monetary value added by encoding must ship with a proof atom citing a Uganda provision. This floor may only be lowered, never raised.

## Listing gates (app visibility)

This lane is marked `app_visibility = "experimental"` in `.axiom/registry.toml`, which keeps its encodings off the axiom-foundation.org app surfaces (encoded search, jurisdiction tiles, navigation encoding badges) while it matures; corpus provisions remain visible under release-scopes gating. Flip the marker to `"public"` in a one-line PR when all four gates hold:

1. **Composed end-to-end calculation** — a `programs/` compose spec chains the modules so the flagship calculation (gross income to individual income-tax liability, and onward to disposable income) runs as one program. Status: **open**.
2. **Independent numerical validation** — UGAMOD (SOUTHMOD Uganda) per-case parity, or independently published worked figures (URA PAYE tables) reproduced exactly as companion fixtures citing their sources. Status: **open**.
3. **Open legal questions closed or prominently caveated** — Status: **open** (none recorded yet).
4. **Second-maintainer review** — another maintainer has reviewed module scope and semantics. Status: **open**.
