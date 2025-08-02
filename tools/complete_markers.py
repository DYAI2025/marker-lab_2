#!/usr/bin/env python3
"""Utility to normalize marker YAML files to Lean Deep 3.11 structure.

The script scans the ``marker`` directory and rewrites each ``*.yaml`` file so
that it matches the template defined in ``marker_templates/lean_deep_marker_template.yaml``.
If a marker provides fewer than five examples, placeholder examples will be
added based on the marker id. Existing ids are preserved and no new prefix is
introduced.
"""
from __future__ import annotations

import datetime as _dt
import yaml
from pathlib import Path
from typing import Dict, Any, List

MARKER_DIR = Path("marker")

REQUIRED_FRAME_FIELDS = ["signal", "concept", "pragmatics", "narrative"]


def _ensure_frame(data: Dict[str, Any]) -> Dict[str, Any]:
    frame = data.get("frame", {}) or {}
    if not isinstance(frame, dict):
        frame = {}
    for field in REQUIRED_FRAME_FIELDS:
        frame.setdefault(field, "")
    data["frame"] = frame
    return data


def _ensure_examples(data: Dict[str, Any]) -> Dict[str, Any]:
    examples: List[str] = []
    if isinstance(data.get("examples"), list):
        examples = [str(e) for e in data["examples"] if isinstance(e, str)]
    elif isinstance(data.get("beispiele"), list):  # legacy field
        examples = [str(e) for e in data["beispiele"] if isinstance(e, str)]
        data.pop("beispiele", None)
    # pad with generic examples if fewer than five
    while len(examples) < 5:
        examples.append(f"{data.get('id', 'MARKER')} example {len(examples)+1}")
    data["examples"] = examples
    return data


def _ensure_tags(data: Dict[str, Any]) -> Dict[str, Any]:
    tags: List[str] = []
    for key in ("tags", "semantic_tags"):
        if isinstance(data.get(key), list):
            tags.extend(str(t) for t in data[key])
            if key != "tags":
                data.pop(key, None)
    data["tags"] = list(dict.fromkeys(tags))  # deduplicate
    return data


def _ensure_meta(data: Dict[str, Any], marker_path: Path) -> Dict[str, Any]:
    # id
    if not isinstance(data.get("id"), str) or not data["id"]:
        data["id"] = marker_path.stem
    # author
    if not isinstance(data.get("author"), str):
        data["author"] = "unknown"
    # created
    if not isinstance(data.get("created"), str):
        created_fields = ["created_at", "created" ]
        for f in created_fields:
            if isinstance(data.get(f), str):
                data["created"] = data[f]
                break
        else:
            data["created"] = _dt.date.today().isoformat()
    # remove legacy fields
    for legacy in ("marker_name", "marker", "level", "version", "status", "lang",
                   "name", "description", "beschreibung", "atomic_pattern", "pattern",
                   "regex_flags", "created_at"):
        data.pop(legacy, None)
    return data


def normalize_marker(marker_path: Path) -> None:
    with open(marker_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    data = _ensure_frame(data)
    data = _ensure_examples(data)
    data = _ensure_tags(data)
    data = _ensure_meta(data, marker_path)

    with open(marker_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def main() -> None:
    for file in MARKER_DIR.glob("*.yaml"):
        normalize_marker(file)


if __name__ == "__main__":
    main()
