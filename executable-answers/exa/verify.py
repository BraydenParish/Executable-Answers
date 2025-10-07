"""
Deterministic verification for numeric-growth claims.
Tolerance is absolute in percentage points (default 0.1 pp).
"""
from __future__ import annotations
from typing import Dict, Any, List
from math import isclose

DEFAULT_EPSILON_PP = 0.1

def _pct_from_base_current(base: float, current: float) -> float:
    return ((current / base) - 1.0) * 100.0

def _pct_from_base_delta(base: float, delta: float) -> float:
    return (delta / base) * 100.0

def verify_numeric_growth_claim(claim: Dict[str, Any], epsilon_pp: float = DEFAULT_EPSILON_PP) -> Dict[str, Any]:
    calc = claim.get("calc", {})
    base = calc.get("base")
    current = calc.get("current")
    delta = calc.get("delta")
    pct = calc.get("pct")

    verdict = {"id": claim["id"], "type": claim["type"], "status": "unchecked", "reason": ""}

    try:
        if base is not None and current is not None:
            pct_est = _pct_from_base_current(base, current)
            if pct is None:
                verdict["status"] = "passed"
                verdict["reason"] = f"Computed pct={pct_est:.4f} from base/current."
                return verdict
            if isclose(pct_est, float(pct), abs_tol=epsilon_pp):
                verdict["status"] = "passed"
                verdict["reason"] = f"pct matches within {epsilon_pp} pp (est={pct_est:.4f}, given={pct})."
            else:
                verdict["status"] = "failed"
                verdict["reason"] = f"pct mismatch (est={pct_est:.4f}, given={pct}); tol={epsilon_pp} pp."
            return verdict

        if base is not None and delta is not None:
            pct_est = _pct_from_base_delta(base, delta)
            if pct is None:
                verdict["status"] = "passed"
                verdict["reason"] = f"Computed pct={pct_est:.4f} from base/delta."
                return verdict
            if isclose(pct_est, float(pct), abs_tol=epsilon_pp):
                verdict["status"] = "passed"
                verdict["reason"] = f"pct matches within {epsilon_pp} pp (est={pct_est:.4f}, given={pct})."
            else:
                verdict["status"] = "failed"
                verdict["reason"] = f"pct mismatch (est={pct_est:.4f}, given={pct}); tol={epsilon_pp} pp."
            return verdict

        verdict["status"] = "unchecked"
        verdict["reason"] = "Insufficient numeric components to verify."
        return verdict

    except Exception as e:
        verdict["status"] = "error"
        verdict["reason"] = f"Exception: {e}"
        return verdict

def verify_claims(claims: List[Dict[str, Any]], epsilon_pp: float = DEFAULT_EPSILON_PP) -> Dict[str, Any]:
    results = []
    counts = {"passed": 0, "failed": 0, "unchecked": 0, "error": 0}
    for c in claims:
        if c.get("type") == "numeric_growth":
            r = verify_numeric_growth_claim(c, epsilon_pp)
        else:
            r = {"id": c.get("id"), "type": c.get("type"), "status": "unchecked", "reason": "Unknown claim type"}
        results.append(r)
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return {"results": results, "summary": counts}
