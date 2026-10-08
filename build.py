#!/usr/bin/env python3
"""Regenerate fmorm-all.xml from the individual custom function files in src/.

Usage:
    python3 build.py            Rebuild fmorm-all.xml from the working tree.
    python3 build.py --check    Exit 1 if fmorm-all.xml is out of date (writes nothing).
    python3 build.py --check --staged
                                Same check, but against the files staged in git
                                (used by the pre-commit hook in .githooks/).

src/ is the source of truth; never edit fmorm-all.xml by hand. Each src file must
be an fmxmlsnippet holding exactly one <CustomFunction> whose name matches the
file name. Functions are grouped into sections (internal helpers, public builders,
utility) and, within each section, ordered so every function follows the
functions it calls (ties broken alphabetically).
"""

import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUNDLE = "fmorm-all.xml"

# Sections in bundle order: (banner title, predicate on the src-relative path)
SECTIONS = [
    ("INTERNAL HELPERS", lambda p: p.startswith("src/internal/")),
    ("PUBLIC BUILDERS", lambda p: p.count("/") == 1 and Path(p).name.startswith("Query")),
    ("UTILITY", lambda p: p.count("/") == 1 and not Path(p).name.startswith("Query")),
]

CF_BLOCK = re.compile(r"^[ \t]*<CustomFunction\b.*?</CustomFunction>", re.S | re.M)
CALC = re.compile(r"<!\[CDATA\[(.*?)\]\]>", re.S)
# String literals and comments in one pass, so "//" inside a string or a quote
# inside a comment is never mistaken for the other.
STRINGS_AND_COMMENTS = re.compile(r'"(?:[^"\\]|\\.)*"|//[^\n]*|/\*.*?\*/', re.S)
LIBRARY_CALL = re.compile(r"\b(Query[A-Z]\w*)\s*\(")


class BuildError(Exception):
    pass


def read_sources(staged):
    """Return {relative path: text} for every src/**/*.xml file."""
    if staged:
        listed = git("ls-files", "--cached", "--", "src").splitlines()
        paths = [p for p in listed if p.endswith(".xml")]
        return {p: git("show", f":{p}") for p in paths}
    return {
        p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted((ROOT / "src").rglob("*.xml"))
    }


def read_bundle(staged):
    if staged:
        try:
            return git("show", f":{BUNDLE}")
        except BuildError:
            return ""
    path = ROOT / BUNDLE
    return path.read_text(encoding="utf-8") if path.exists() else ""


def git(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if result.returncode != 0:
        raise BuildError(f"git {' '.join(args)} failed: {result.stderr.decode().strip()}")
    return result.stdout.decode("utf-8")


def parse_function(path, text):
    """Validate one src file and return (name, verbatim CustomFunction block, calc)."""
    text = text.replace("\r\n", "\n")
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except ET.ParseError as e:
        raise BuildError(f"{path}: not well-formed XML ({e})")
    functions = root.findall("CustomFunction")
    if root.tag != "fmxmlsnippet" or len(functions) != 1:
        raise BuildError(f"{path}: expected an fmxmlsnippet with exactly one <CustomFunction>")

    cf = functions[0]
    name = cf.get("name", "")
    if name != Path(path).stem:
        raise BuildError(f'{path}: function is named "{name}" but the file is "{Path(path).name}"')

    params = [p for p in cf.get("parameters", "").split(";") if p]
    arity = cf.get("functionArity", "")
    if arity != str(len(params)):
        raise BuildError(f"{path}: functionArity={arity} but {len(params)} parameter(s) are declared")

    block = CF_BLOCK.search(text)
    calc = CALC.search(block.group(0)) if block else None
    if not block or not calc:
        raise BuildError(f"{path}: could not locate the <CustomFunction> block / CDATA body")
    return name, block.group(0), calc.group(1)


def calls_in(calc):
    """Library function names called by a calculation, ignoring comments and string literals."""
    code = STRINGS_AND_COMMENTS.sub(" ", calc)
    return set(LIBRARY_CALL.findall(code))


def dependency_order(names, deps):
    """Order names so each follows its in-section dependencies; ties alphabetical, cycles tolerated."""
    remaining = set(names)
    ordered = []
    while remaining:
        ready = [n for n in remaining if not (deps[n] & remaining) - {n}]
        # Mutual recursion leaves nothing ready: break the cycle alphabetically
        pick = min(ready or remaining)
        remaining.discard(pick)
        ordered.append(pick)
    return ordered


def build(sources):
    functions = {}  # name -> (path, block, calls)
    for path, text in sorted(sources.items()):
        name, block, calc = parse_function(path, text)
        if name in functions:
            raise BuildError(f'"{name}" is defined in both {functions[name][0]} and {path}')
        functions[name] = (path, block, calls_in(calc))

    missing = [
        f'{functions[n][0]}: calls {c}, which has no file in src/'
        for n in sorted(functions)
        for c in sorted(functions[n][2])
        if c not in functions
    ]
    if missing:
        raise BuildError("undefined custom function reference(s):\n  " + "\n  ".join(missing))

    sections = []
    for title, belongs in SECTIONS:
        names = [n for n in functions if belongs(functions[n][0])]
        deps = {n: functions[n][2] for n in names}
        sections.append((title, dependency_order(names, deps)))

    unplaced = set(functions) - {n for _, names in sections for n in names}
    if unplaced:
        raise BuildError("file(s) outside any bundle section: " + ", ".join(sorted(functions[n][0] for n in unplaced)))

    return render(sections, {n: functions[n][1] for n in functions})


def render(sections, blocks):
    total = sum(len(names) for _, names in sections)
    ranges, start = [], 1
    for title, names in sections:
        ranges.append(f"{title.lower()} ({start}–{start + len(names) - 1})" if names else f"{title.lower()} (none)")
        start += len(names)

    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!--",
        "  fmorm-all.xml — combined fmxmlsnippet for one-shot FileMaker import.",
        "",
        "  GENERATED FILE — do not edit by hand. Edit the files in src/ and run:",
        "      python3 build.py",
        "",
        f"  Contains all {total} custom functions, grouped as:",
        "    " + ", ".join(ranges) + ".",
        "  Within each group a function follows the functions it calls.",
        "  FileMaker resolves function references at runtime so import order does",
        "  not strictly matter.",
        "",
        "  Import via Edit > Paste (with the XML on the clipboard), or use your",
        "  PHPStorm fmCuttingBoard tooling to paste the snippet directly into FM.",
        "-->",
        '<fmxmlsnippet type="FMObjectList">',
    ]
    index = 0
    for title, names in sections:
        if not names:
            continue
        out += [
            "",
            "    <!-- " + "=" * 60 + " -->",
            f"    <!-- {f'{title} ({len(names)})':<60} -->",
            "    <!-- " + "=" * 60 + " -->",
        ]
        for name in names:
            index += 1
            out += ["", f"    <!-- {index} of {total} -->", blocks[name]]
    out += ["", "</fmxmlsnippet>", ""]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if the bundle is out of date; write nothing")
    parser.add_argument("--staged", action="store_true", help="with --check: compare the files staged in git")
    args = parser.parse_args()
    if args.staged and not args.check:
        parser.error("--staged requires --check")

    try:
        expected = build(read_sources(args.staged))
        current = read_bundle(args.staged).replace("\r\n", "\n")
    except BuildError as e:
        print(f"build.py: {e}", file=sys.stderr)
        return 2

    count = len(CF_BLOCK.findall(expected))
    if args.check:
        if current == expected:
            print(f"{BUNDLE} is up to date ({count} functions).")
            return 0
        where = "staged " if args.staged else ""
        print(f"{BUNDLE} is out of date with the {where}files in src/.\n"
              f"Run:  python3 build.py && git add {BUNDLE}", file=sys.stderr)
        return 1

    if current == expected:
        print(f"{BUNDLE} already up to date ({count} functions).")
    else:
        (ROOT / BUNDLE).write_text(expected, encoding="utf-8", newline="\n")
        print(f"Wrote {BUNDLE} ({count} functions).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
