"""Deterministic audit manifest for model inputs and results."""
import hashlib
import json
from dataclasses import asdict, is_dataclass

def _serialisable(value):
    if is_dataclass(value):
        return asdict(value)
    return value

def audit_manifest(model_name, assumptions, results, source_notes=None):
    """Canonical JSON hashes allow comparisons of successive model runs.
    SHA-256 here detects changes; it is not a digital signature or assurance.
    """
    if not model_name:
        raise ValueError("model name required")
    payload = {"model": model_name, "assumptions": _serialisable(assumptions),
               "results": _serialisable(results), "sources": source_notes or []}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         allow_nan=False).encode("utf-8")
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "payload": payload}
