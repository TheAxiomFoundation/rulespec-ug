"""Tripwire for SOUTHMOD (UGAMOD) model internals in committed text.

This repository is public, and the SOUTHMOD_A4.0 Adhesion Agreement bars
giving the model to third parties. CLAUDE.md therefore lets us record only
UGAMOD output variable names used as comparison bindings, outputs observed
on synthetic households, and comparison statistics.

The scan below catches the syntactic forms that model content takes when it
slips into prose: income-list names and compositions, policy and function
names, switch and constant syntax, and output variable names that are not
comparison bindings. It cannot recognise a parameter value, a condition or
a model input-variable name written in plain words; review still owns those.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Every UTF-8 file under these roots is scanned, whatever its suffix, so a
# committed bundle file (EUROMOD parameters are XML) is caught too, and so is
# every file at the repository root. `.github/` holds workflow shell code and
# `tests/` holds these patterns, so neither is scanned; nor are CI's transient
# `_axiom/` toolchain checkouts. The compose specs live under `ug/programs/`.
SCAN_DIRS = (".axiom", "data", "docs", "ug")

# UGAMOD output variables that axiom-oracles' ug suites compare against
# (`comparisons/ug-*.yaml`). Keep in step with the `wired` block of
# data/oracles/oracle-index.json; test_bindings_match_oracle_index checks it.
COMPARISON_BINDINGS = frozenset(
    {
        "boa_s",
        "tex10_s",
        "tgv_s",
        "tin_s",
        "tpr_s",
        "tscee_s",
        "tscer_s",
        "ttn_s",
        "tva_s",
    }
)
# The disposable-income income list is compared by name; its composition is
# model content.
COMPARED_INCOME_LIST = "ils_dispy"
NOT_POLICY_NAMES = frozenset({"rulespec_ug"})

# EUROMOD-convention policy names end in a country code. Catch every SOUTHMOD
# country's suffix, not only Uganda's, so a record pasted from another
# country's repository is caught here too.
POLICY_SUFFIXES = ("gh", "ug", "zm", "rw", "et", "tz", "mz")

PATTERNS = {
    "income_list": re.compile(r"\bils?_[a-z][a-z0-9_]*"),
    "policy_name": re.compile(
        r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)*_(?:" + "|".join(POLICY_SUFFIXES) + r")\b"
    ),
    "function_name": re.compile(
        r"\b(?:ArithOp|BenCalc|ChangeParam|ChangeSwitch|DefConst|DefIL"
        r"|DefOutput|DefTU|DefVar|DropUnit|Elig|IlVarOp|KeepUnit|SchedCalc"
        r"|SetDefault|UnitLoop|UpdateTU)\b"
    ),
    "switch": re.compile(r"\bsw\s*=\s*(?:on|off|n/a)\b", re.IGNORECASE),
    # Model constants are mixed or lower case; all-caps names are shell
    # variables ($HOME, $GITHUB_WORKSPACE).
    "constant": re.compile(r"\$(?![A-Z][A-Z0-9_]*\b)[A-Za-z][A-Za-z0-9_]*"),
    "period_suffix": re.compile(r"\b\d+(?:\.\d+)?#[ymwqd]\b"),
    "output_variable": re.compile(r"\b[a-z]{2,8}\d{0,2}_s\b"),
}

# Instances already on main inside encoded RuleSpec, which only the
# supervised encoder may change. Every entry is listed in rulespec-ug#21
# item 4, which queues the repair round that removes it. Delete an entry when
# that repair lands; the test fails on any change, so the list only shrinks on
# purpose.
PENDING_ENCODER_REPAIR = {
    # rulespec-ug#21 item 4: a companion-test comment names a model parameter
    # and gives its value.
    (
        "ug/regulations/vat-rate-of-tax-order-2006/rate-of-tax-order-2006.test.yaml",
        "constant",
    ): 1,
    # rulespec-ug#21 item 4: a companion-test comment names a model policy.
    (
        "ug/statutes/act-2008-8/local-governments-amendment-no2-2008.test.yaml",
        "policy_name",
    ): 1,
    # rulespec-ug#21 item 4: a deferred-output reason names a model policy.
    (
        "ug/statutes/act-2008-8/local-governments-amendment-no2-2008.yaml",
        "policy_name",
    ): 1,
    # rulespec-ug#21 item 4: a companion-test comment names a model constant.
    (
        "ug/statutes/act-2024-excise/excise-duty-amendment-2024.test.yaml",
        "constant",
    ): 1,
    # rulespec-ug#21 item 4: the summary restates the disposable-income
    # income-list composition and equates a model tax-base variable with a
    # model input variable.
    (
        "ug/statutes/composed/pilot-worker-disposable-income-pipeline.yaml",
        "income_list",
    ): 5,
    (
        "ug/statutes/composed/pilot-worker-disposable-income-pipeline.yaml",
        "output_variable",
    ): 1,
}


def find_internals(text: str) -> list[tuple[int, str]]:
    """Return (line number, category) for each model-internal token in text."""
    hits: list[tuple[int, str]] = []
    for category, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            token = match.group(0)
            if (
                category == "income_list"
                and token == COMPARED_INCOME_LIST
                and not re.match(r"\s*=", text[match.end() :])
            ):
                continue
            if category == "policy_name" and token in NOT_POLICY_NAMES:
                continue
            if category == "output_variable" and token in COMPARISON_BINDINGS:
                continue
            hits.append((text.count("\n", 0, match.start()) + 1, category))
    return sorted(hits)


def iter_scanned_files() -> list[Path]:
    files = [
        path
        for directory in SCAN_DIRS
        if (ROOT / directory).is_dir()
        for path in (ROOT / directory).rglob("*")
        if path.is_file()
    ]
    files.extend(path for path in ROOT.iterdir() if path.is_file())
    return sorted(files)


def scan_repository() -> dict[tuple[str, str], list[int]]:
    found: dict[tuple[str, str], list[int]] = defaultdict(list)
    for path in iter_scanned_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line, category in find_internals(text):
            found[(path.relative_to(ROOT).as_posix(), category)].append(line)
    return dict(found)


def test_no_new_model_internals() -> None:
    found = scan_repository()
    counts = {key: len(lines) for key, lines in found.items()}
    # Report path, line and category only: CI logs are public too.
    new = [
        f"{path}:{','.join(map(str, sorted(set(found[(path, category)]))))} ({category})"
        for (path, category), count in sorted(counts.items())
        if count > PENDING_ENCODER_REPAIR.get((path, category), 0)
    ]
    assert not new, (
        "SOUTHMOD model content in committed text; describe UGAMOD only by "
        "comparison-binding outputs, observed outputs and comparison "
        "statistics (CLAUDE.md):\n" + "\n".join(new)
    )
    stale = [
        f"{path} ({category}): expected {expected}, found {counts.get((path, category), 0)}"
        for (path, category), expected in sorted(PENDING_ENCODER_REPAIR.items())
        if counts.get((path, category), 0) != expected
    ]
    assert not stale, (
        "PENDING_ENCODER_REPAIR is out of date; lower or delete these entries:\n"
        + "\n".join(stale)
    )


def test_bindings_match_oracle_index() -> None:
    payload = json.loads((ROOT / "data/oracles/oracle-index.json").read_text())
    wired = [
        oracle["wired"]
        for oracle in payload.get("oracles", [])
        if oracle.get("id") == "ugamod" and "wired" in oracle
    ]
    assert wired, "data/oracles/oracle-index.json lost its UGAMOD wired block"
    names = {name for suite in wired[0]["suites"] for name in suite["ugamod_variables"]}
    assert names == COMPARISON_BINDINGS | {COMPARED_INCOME_LIST}


# The detector checks below use made-up tokens of the same shape, plus one
# generic EUROMOD function name and the platform's switch syntax, so this
# file names no UGAMOD content.
def categories(text: str) -> Counter[str]:
    return Counter(category for _, category in find_internals(text))


def test_detector_flags_each_form() -> None:
    assert categories("the example list ils_zzexample") == {"income_list": 1}
    assert categories("il_zzbase3 feeds the base") == {"income_list": 1}
    assert categories("ils_dispy = ils_zza + ils_zzb") == {"income_list": 3}
    assert categories("policy zzz_ug runs") == {"policy_name": 1}
    assert categories("a SchedCalc step") == {"function_name": 1}
    assert categories("it is sw=off here") == {"switch": 1}
    assert categories("uses $zzconstant") == {"constant": 1}
    assert categories("uses $ZzMixedRate and $ZZ_part") == {"constant": 2}
    assert categories("above 77#q") == {"period_suffix": 1}
    assert categories("output zzz01_s differs") == {"output_variable": 1}


def test_detector_flags_other_countries_policy_names() -> None:
    for suffix in POLICY_SUFFIXES:
        assert categories(f"policy zzz_{suffix} runs") == {"policy_name": 1}
    assert categories("policy zzz_zz runs") == {}


def test_detector_allows_bindings_and_ordinary_text() -> None:
    clean = (
        "UGAMOD's tin_s matches the statutory schedule at every case. "
        "Compared output: ils_dispy. Pinned rulespec_ug c0b6597; see "
        "rulespec-ug#21. income_tax_s, ${{ secrets.TOKEN }}, $HOME and "
        "$GITHUB_WORKSPACE are not model names."
    )
    assert categories(clean) == {}


def test_detector_reports_line_numbers() -> None:
    assert find_internals("first\nsecond ils_zzexample\n") == [(2, "income_list")]
