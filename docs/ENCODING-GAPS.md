# Encoding gaps

## `ug/statutes/cap-230/national-social-security-fund-act/section-10-payment-of-standard-contribution-by-employers.yaml`

- `0.15` encodes the standard contribution rate. It is stated as “fifteen percent” in `ug/statute/cap-230/national-social-security-fund-act/section-10-payment-of-standard-contribution-by-employers`.
- `15` encodes the standard-contribution payment deadline in days. It is stated as “within fifteen days” in `ug/statute/cap-230/national-social-security-fund-act/section-10-payment-of-standard-contribution-by-employers`.
- `0.05` encodes the employee share rate. It is stated as “five percent” in `ug/statute/cap-230/national-social-security-fund-act/section-11-employees-share-of-standard-contribution`.

All Uganda provisions in the pinned corpus release were searched. Sections 10 and 11 each support their respective values, but no single provision contains all three numbers. The module-level `source_verification.corpus_citation_path` currently names the bodyless Act parent; under the release's resolution rule that parent has no own body or `/document-N` child body, so it supplies no grounding text. Narrowing the citation to section 10 would leave `0.05` ungrounded, while narrowing it to section 11 would leave `0.15` and `15` ungrounded. This is a structural encoding/validator gap for a module spanning multiple source provisions. The encoded values are not judged wrong, and the source text is not missing from the release.
