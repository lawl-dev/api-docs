#!/usr/bin/env python3
"""Regenerate the inline RESOURCES object in snippets/language-table.jsx
from the vended /v3/languages responses under data/v3-languages/.

The JSX file must contain `// BEGIN GENERATED` and `// END GENERATED`
marker lines; everything between them is replaced. The output is a
JavaScript object literal keyed by resource name. Each value is the
verbatim JSON array returned by `GET /v3/languages?resource=<name>`,
formatted with one language entry per line for readable diffs.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "v3-languages"
JSX = ROOT / "snippets" / "language-table.jsx"
BEGIN = "    // BEGIN GENERATED: RESOURCES (do not edit; run scripts/generate_language_table.py)"
END = "    // END GENERATED"

# Resource files to inline. Order is preserved in the output.
RESOURCE_NAMES = [
    "translate_text",
    "translate_document",
    "voice",
    "write",
    "glossary",
    "style_rules",
    "translation_memory",
]


def render_entry(entry: dict) -> str:
    return json.dumps(entry, ensure_ascii=False)


def render() -> str:
    lines = [BEGIN, "    const RESOURCES = {"]
    for name in RESOURCE_NAMES:
        entries = json.loads((DATA / f"{name}.json").read_text())
        lines.append(f'        {json.dumps(name)}: [')
        for entry in entries:
            lines.append(f"            {render_entry(entry)},")
        lines.append("        ],")
    lines.append("    }")
    lines.append(END)
    return "\n".join(lines)


text = JSX.read_text()
start = text.index(BEGIN)
end = text.index(END, start) + len(END)
JSX.write_text(text[:start] + render() + text[end:])
total = sum(
    len(json.loads((DATA / f"{name}.json").read_text())) for name in RESOURCE_NAMES
)
print(f"regenerated {total} entries across {len(RESOURCE_NAMES)} resources")
