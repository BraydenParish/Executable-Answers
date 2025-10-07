"""
JSON-only prompt templates for external model critique.
"""

SUPPORT_CHECK_PROMPT = """You are an impartial claim auditor. Read the ANSWER and list each atomic factual claim.
For each claim, decide if it is SUPPORTED by the provided SOURCES.
Definitions:
- SUPPORTED: has a citation with a specific locator (page/table/section).
- PARTIALLY_SUPPORTED: has a citation but no locator.
- UNSUPPORTED: no citation provided or the cited source does not contain the claim.
Return STRICT JSON only (no prose), schema:
{"claims":[{"id":"c1","text":"...","status":"SUPPORTED|PARTIALLY_SUPPORTED|UNSUPPORTED","sources":[{"id":"s1","locator":"p.3"}]}]}
"""

COMPUTATION_CHECK_PROMPT = """You are a numeric auditor. For each numeric growth claim in ANSWER,
extract any numbers you can: base, current, delta, pct. Recompute pct if possible.
Mark consistent=true if recomputed pct matches provided pct within 0.1 percentage points (pp).
Return STRICT JSON only:
{"claims":[{"id":"c1","calc":{"base":100,"current":112,"delta":12,"pct":12.0},"consistent":true,"tolerance_pp":0.1}]}
"""

CONTRADICTION_SCAN_PROMPT = """You are a consistency checker. Given a set of claims, return any pair that cannot both be true simultaneously, with a short reason.
Return STRICT JSON only:
{"contradictions":[{"c_i":"c1","c_j":"c2","reason":"..."}]}
"""
