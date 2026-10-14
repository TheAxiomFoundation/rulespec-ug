"""Encoding-manifest state recorded on 2026-10-14.

KNOWN_STALE_ATTESTATIONS lists manifest claims that were already stale. Each
entry is one claim in one manifest under .axiom/encoding-manifests/: the
file it attests, the sha256 the manifest records for that file, the sha256
the file had on 2026-10-14, the sha256 of the manifest file itself, and the
commits that changed the file after it was attested.

All of these changes landed in July 2026 (rulespec-ug#11, rulespec-ug#17),
while this repository's generated-RuleSpec guard was off
(run-generated-guard: false until 2026-10-11), so CI never compared the
edited files with their manifests.

The listed manifests are manual attestations (runner: manual-attestation,
schema axiom-encode/applied-rulespec/v1), not encoder apply records. Listing
a claim here records the drift. It does not attest the current bytes, and
the manifest still attests the earlier ones.

KNOWN_UNMANIFESTED_MODULES lists the RuleSpec modules that had no encoding
manifest on 2026-10-14. Any other module without one fails.

Both lists are closed and may only shrink. test_encoding_manifests.py fails
if a listed file changes again, if a listed manifest is edited or removed
other than by an encoder replacement, if a module loses its manifest, or if
an entry is added or rewritten (each entry's digest must be in that file's
ADOPTED_LIST_SHA256). It warns when an entry resolves, for example once the
supervised encoder replaces a module's manifest; delete the entry then. New
drift is fixed through the encoder, not listed.
"""

from __future__ import annotations

from typing import NamedTuple


class StaleAttestation(NamedTuple):
    manifest: str
    manifest_sha256: str
    path: str
    attested_sha256: str
    current_sha256: str
    changed_by: tuple[str, ...]
    change: str


KNOWN_STALE_ATTESTATIONS: tuple[StaleAttestation, ...] = (
    StaleAttestation(
        manifest=".axiom/encoding-manifests/ug/policies/mglsd-scg/sage-handbook.json",
        manifest_sha256="9e85567b2c244eae25d4b8ad9ad7f4c5c38cc323ac219a133c0d7d54bfaf0ddb",
        path="ug/policies/mglsd-scg/sage-handbook.yaml",
        attested_sha256="5d32031433a296e03411808294c6fbc4445daa28f33fbd31b057016059de493f",
        current_sha256="13e8c2f35244ecf2e86d0197958d40b11765cfbcfb39919e31bab55dce52c80c",
        changed_by=("f0106a82667c31aa9ee0068629a8b01a11bd0f66",),
        change=(
            "no formula, parameter or import changed: upstream_source_check "
            "removed, 1 proof excerpt changed"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/ug/statutes/act-2022-11/income-tax-amendment-2022/third-schedule-rental-rate-part-substituted.json",
        manifest_sha256="2bd51bfd1a008fc2f1adfc16b421dee105c3dd0b3c28e06deb2df6b8146c3fee",
        path="ug/statutes/act-2022-11/income-tax-amendment-2022/third-schedule-rental-rate-part-substituted.yaml",
        attested_sha256="4db62a0758aff66307512f174da9d99e1290ce5b5aec578d367092003123d251",
        current_sha256="e05c3b05a3b195a3eb1124acd3dc36c91b4561c1bf0ae9603c00a523813fe991",
        changed_by=("f0106a82667c31aa9ee0068629a8b01a11bd0f66",),
        change=(
            "no formula, parameter or import changed: module citation list "
            "collapsed to one corpus_citation_path"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/ug/statutes/act-2024-excise/excise-duty-amendment-2024.json",
        manifest_sha256="b4abc5df04653457a4907629496b861fa49086f0c5c5c1d5fedbeeea7163ea01",
        path="ug/statutes/act-2024-excise/excise-duty-amendment-2024.yaml",
        attested_sha256="2ada8e717362abd74f58ca490ea9a1d26a444dbcae28f2e4bdc3491103263b39",
        current_sha256="69448525f6d7655a0e7bdc40d44ebbaa76b74d743b8cd310ffb89385fbf83d11",
        changed_by=(
            "f0106a82667c31aa9ee0068629a8b01a11bd0f66",
            "beead8c7e9723ae27b48293cbebdd7a308cf8d9a",
        ),
        change=(
            "no formula, parameter or import changed: 4 proof excerpts changed, "
            "1 rule source label changed"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/ug/statutes/cap-230/national-social-security-fund-act/section-10-payment-of-standard-contribution-by-employers.json",
        manifest_sha256="af8cb856121bb98be2b6e64f5d3378db66364fdef83faa0407d01ace4d064d64",
        path="ug/statutes/cap-230/national-social-security-fund-act/section-10-payment-of-standard-contribution-by-employers.yaml",
        attested_sha256="7ea90537a6b491fadeab11ae4d6caf23dff38841770efb72ac721e856e6aaad1",
        current_sha256="38eea3b005643978b2254de519e22c4245960e1d9726237f6a5e997eeb8dfdc7",
        changed_by=("f0106a82667c31aa9ee0068629a8b01a11bd0f66",),
        change=(
            "no formula, parameter or import changed: module citation list "
            "collapsed to one corpus_citation_path, 4 proof excerpts changed"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/ug/statutes/composed/pilot-worker-disposable-income-pipeline.json",
        manifest_sha256="dcacf9687f59afd6abac8f48f50574a3fb759b749785a651989b309d44e5c9f2",
        path="ug/statutes/composed/pilot-worker-disposable-income-pipeline.yaml",
        attested_sha256="f70fb72a8f2c610bbde4ebf935283024eeacb1559365aeea87755a3adb161189",
        current_sha256="8ddf83bd656deb6fb1ea67989c16094586a7cf25478d7d9a46874802bbdb5420",
        changed_by=("f0106a82667c31aa9ee0068629a8b01a11bd0f66",),
        change=(
            "no formula, parameter or import changed: module citation list "
            "collapsed to one corpus_citation_path, upstream_source_check "
            "removed, 1 proof excerpt changed"
        ),
    ),
)

KNOWN_UNMANIFESTED_MODULES: tuple[str, ...] = (
    "ug/statutes/cap-230/national-social-security-fund-act/section-11-employees-share-of-standard-contribution.yaml",
    "ug/statutes/cap-230/national-social-security-fund-act/section-12-special-contribution.yaml",
)
