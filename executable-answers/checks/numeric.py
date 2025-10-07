"""
Property-based numeric identities for growth computations.
Run with: pytest -q
"""
from hypothesis import given, strategies as st
from math import isclose

@given(st.integers(min_value=1, max_value=10_000),
       st.integers(min_value=0, max_value=10_000))
def test_growth_identity(base, delta):
    pct = (delta / base) * 100
    assert isclose(((base + delta) / base - 1) * 100, pct, rel_tol=1e-12)

@given(st.integers(min_value=1, max_value=10_000),
       st.integers(min_value=0, max_value=10_000))
def test_roundtrip(base, delta):
    pct = (delta / base) * 100
    current = base * (1 + pct / 100)
    assert isclose(current, base + delta, rel_tol=1e-12)
