# rulespec-ug Agent Notes

This repo stores Uganda RuleSpec source registry materials, oracle references, and encoded policy rules. Uganda is a unitary state, so all encoded law lives under a single `ug/` national namespace.

## Scope

- `ug/statutes/`: Uganda Acts of Parliament — the Income Tax Act (Cap 340) as amended, the VAT Act (Cap 349), the Excise Duty Act, the NSSF Act, the Local Governments Act, and other primary law needed for tax-benefit modeling.
- `ug/regulations/`: statutory instruments made under the governing Acts.
- `ug/policies/`: URA administrative guidance, PAYE rate surfaces, practice notes, and social-protection programme rules (Senior Citizens Grant) set administratively.
- `programs/`: declarative compose specs (one per jurisdiction/program/period).
- `data/corpus/`: source inventory, ingestion notes, provision locators, and promoted official-source extracts.
- `data/coverage/`: tax-benefit coverage backlog and source map.
- `data/oracles/`: executable or documentary comparison references. These are never legal authority.

## Do

- Treat the scope as a Uganda tax-benefit surface backed by Uganda upstream law.
- Start from the furthest upstream available source: Uganda Gazette assented Act prints (Parliament of Uganda) and Law Development Centre revised editions first, URA rate tables/guides and Ministry of Gender programme documentation only after the governing Act is identified. ULII document pages are bot-gated; hunt prints via parliament.go.ug and gazettes.africa.
- Add RuleSpec under `ug/statutes/`, `ug/regulations/`, or `ug/policies/` with companion `.test.yaml` files.
- Keep source law provenance in corpus artifacts and cite those corpus paths from RuleSpec modules via `module.source_verification.corpus_citation_path`.
- Use FY2025/26 (Uganda's tax year runs 1 July–30 June) as the validation year for encoded amounts; indexed/annual values must be corpus-grounded, never invented. UGAMOD system UG_2025 corresponds to FY2025/26.
- Keep exact oracle versions in `data/oracles/oracle-index.json`. The UGAMOD bundle (SOUTHMOD A4.0) is licensed and non-redistributable — never commit bundle bytes, dataset rows, or model XML; only comparison statistics and UGAMOD-produced values may be recorded.
- Sync `axiom-encode` and `.axiom/toolchain.toml` before substantial encoding runs.

## Do Not

- Use URA calculator pages, PAYE ready-reckoners, or third-party summaries as the first legal source when an Act governs the rule.
- Invent, round, or interpolate any Ugandan monetary amount, rate band, or threshold. Every number must come verbatim from a captured official provision.
- Migrate UGAMOD, EUROMOD/SOUTHMOD, or agency calculator code mechanically as RuleSpec.
- Add generated source payload dumps, formula artifacts, `parameters.yaml`, or standalone YAML fixtures outside allowed RuleSpec roots.
- Hand-copy statute text into RuleSpec without a corpus `citation_path`.
