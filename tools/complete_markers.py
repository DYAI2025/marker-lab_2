#!/usr/bin/env python3
"""Utility to normalize marker YAML files to Lean Deep 3.11 structure.

Run from repository root:
    python tools/complete_markers.py

The script traverses `marker/`, attempts to parse every `*.yaml` file and
normalises it so that it conforms to the Lean Deep 3.11 template:
• ensures a full `frame` block (signal / concept / pragmatics / narrative)
• guarantees **≥ 5** examples (pads generic placeholders if needed)
• consolidates / deduplicates tags
• fills in minimal metadata (id, author, created) if missing
• strips legacy / deprecated fields

Any file that **cannot** be parsed as YAML is **skipped**, an error is printed,
and the script continues – so one broken file no longer stops the whole batch.
"""
from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────
MARKER_DIR = Path("marker")           # where raw markers live
SUMMARY_LOG = Path("tools/normalize_report.tsv")  # quick human‑readable log
REQUIRED_FRAME_FIELDS = ["signal", "concept", "pragmatics", "narrative"]
MIN_EXAMPLES = 5

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def _ensure_frame(data: Dict[str, Any]) -> Dict[str, Any]:
    frame = data.get("frame") or {}
    if not isinstance(frame, dict):
        frame = {}
    for field in REQUIRED_FRAME_FIELDS:
        frame.setdefault(field, "")
    data["frame"] = frame
    return data


def _ensure_examples(data: Dict[str, Any]) -> Dict[str, Any]:
    examples: List[str] = []
    for key in ("examples", "beispiele"):
        if isinstance(data.get(key), list):
            examples.extend(str(e) for e in data.pop(key, []))
    # remove duplicates while preserving order
    seen = set()
    examples = [e for e in examples if not (e in seen or seen.add(e))]
    marker_id = data.get("id", "MARKER")
    while len(examples) < MIN_EXAMPLES:
        examples.append(f"TODO: Add example for {marker_id}")
    data["examples"] = examples
    return data


def _ensure_tags(data: Dict[str, Any]) -> Dict[str, Any]:
    tags: List[str] = []
    for key in ("tags", "semantic_tags"):
        if isinstance(data.get(key), list):
            tags.extend(str(t) for t in data.pop(key, []))
    data["tags"] = list(dict.fromkeys(tags))  # deduplicate
    return data


def _slugify(text: str) -> str:
    """Return a lowercase slug consisting of alphanumerics and underscores."""
    text = re.sub(r"[^0-9A-Za-z]+", "_", text)
    return text.strip("_").lower()


def _ensure_meta(data: Dict[str, Any], marker_path: Path) -> Dict[str, Any]:
    # id
    raw_id = data.get("id") or marker_path.stem
    slug = _slugify(str(raw_id))
    if not slug.startswith("ld32_"):
        slug = f"ld32_{slug}"
    data["id"] = slug.upper()
    # author
    if not isinstance(data.get("author"), str):
        data["author"] = "unknown"
    # created
    if not isinstance(data.get("created"), str):
        for key in ("created_at", "created"):
            if isinstance(data.get(key), str):
                data["created"] = data[key]
                break
        else:
            data["created"] = _dt.date.today().isoformat()
    # strip legacy fields
    legacy = {
        "marker_name", "marker", "level", "version", "status", "lang",
        "name", "beschreibung", "atomic_pattern", "pattern", "regex_flags",
        "created_at",
    }
    for field in legacy:
        data.pop(field, None)
    return data

# ──────────────────────────────────────────────────────────────────────────────
# CORE
# ──────────────────────────────────────────────────────────────────────────────

def normalize_marker(marker_path: Path) -> tuple[str, str]:
    """Return (filename, status) where status ∈ {OK, YAML_ERROR}."""
    try:
        with marker_path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except yaml.YAMLError as exc:
        return marker_path.name, f"YAML_ERROR: {exc.__class__.__name__}"

    if not isinstance(data, dict):
        return marker_path.name, "YAML_ERROR: not a mapping"

    data = _ensure_meta(data, marker_path)
    data = _ensure_frame(data)
    data = _ensure_examples(data)
    data = _ensure_tags(data)

    with marker_path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False)

    return marker_path.name, "OK"


def main() -> None:
    if not MARKER_DIR.exists():
        sys.exit("[fatal] marker/ directory not found – run from repo root")

    SUMMARY_LOG.parent.mkdir(parents=True, exist_ok=True)
    ok, bad = 0, 0
    with SUMMARY_LOG.open("w", encoding="utf-8") as summary:
        summary.write("file\tstatus\n")
        for file in sorted(MARKER_DIR.glob("*.yaml")):
            fname, status = normalize_marker(file)
            summary.write(f"{fname}\t{status}\n")
            if status == "OK":
                ok += 1
                print(f"[✓] {fname}")
            else:
                bad += 1
                print(f"[⚠] {fname} → {status}")

    print("\n────────── SUMMARY ──────────")
    print(f"Processed: {ok + bad}")
    print(f"Normalised: {ok}")
    print(f"Skipped (YAML errors): {bad}")
    print(f"Detailed log: {SUMMARY_LOG}")


if __name__ == "__main__":
    main()
