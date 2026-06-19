from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .types import TraceRecord


def trace_to_dict(trace: TraceRecord) -> dict:
    data = asdict(trace)
    data["goal"] = asdict(trace.goal)
    data["complexity_mode"] = trace.complexity_mode.value
    return data


def write_trace(trace: TraceRecord, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(trace_to_dict(trace), indent=2, sort_keys=True) + "\n")
    return target
