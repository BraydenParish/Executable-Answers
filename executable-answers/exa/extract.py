"""
Extraction of atomic claims from free-form answers.

v0.1 focuses on a single claim type: numeric growth (YoY-like statements).
Patterns covered:
  A) "from $100 to $112"  -> base=100, current=112, delta=12, pct≈12
  B) "grew 12% YoY"       -> pct=12 (unchecked if base/current/delta absent)
"""
from __future__ import annotations
import re
from typing import List, Dict, Any

_money = r'(?:\$)?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]+)?|[0-9]+(?:\.[0-9]+)?)'
_pct = r'([0-9]+(?:\.[0-9]+)?)\s*%'

def _to_float(x: str) -> float:
    return float(x.replace(",", ""))

def extract_numeric_growth_claims(text: str) -> List[Dict[str, Any]]:
    claims: List[Dict[str, Any]] = []

    # A) "... from $100 to $112"
    pat_from_to = re.compile(
        rf'(?:grew|rose|increased|went up)?\s*from\s*{_money}\s*to\s*{_money}',
        flags=re.IGNORECASE
    )
    for m in pat_from_to.finditer(text):
        base = _to_float(m.group(1))
        current = _to_float(m.group(2))
        delta = current - base
        pct = (delta / base) * 100 if base != 0 else None
        claims.append({
            "id": f"c_fromto_{m.start()}",
            "type": "numeric_growth",
            "text": m.group(0),
            "evidence": [],
            "calc": {"base": base, "current": current, "delta": delta, "pct": pct},
            "status": "unchecked"
        })

    # B) "... grew 12% YoY" or "increased by 12% year-over-year"
    pat_pct = re.compile(
        rf'(?:grew|rose|increased|went up)\s*(?:by\s*)?{_pct}\s*(?:yoy|year[-\s]?over[-\s]?year)?',
        flags=re.IGNORECASE
    )
    for m in pat_pct.finditer(text):
        pct = float(m.group(1))
        claims.append({
            "id": f"c_pct_{m.start()}",
            "type": "numeric_growth",
            "text": m.group(0),
            "evidence": [],
            "calc": {"pct": pct},
            "status": "unchecked"
        })
    return claims
