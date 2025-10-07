"""
Crossref DOI helpers (network call is optional in v0.1).
"""
from __future__ import annotations
import re, requests
from typing import Optional, Dict, Any, List

CROSSREF_API = "https://api.crossref.org/works/{}"
DOI_REGEX = re.compile(r'\b10\.\d{4,9}/\S+\b')

def extract_dois(text: str) -> List[str]:
    return list({m.group(0).rstrip(").,;") for m in DOI_REGEX.finditer(text)})

def resolve_doi(doi: str, timeout: float = 10.0) -> Optional[Dict[str, Any]]:
    r = requests.get(CROSSREF_API.format(doi), timeout=timeout, headers={"User-Agent":"exa/0.1 (Executable Answers)"})
    if r.status_code != 200:
        return None
    try:
        return r.json().get("message", {})
    except Exception:
        return None
