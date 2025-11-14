from typing import List
from calc.m_types import PersonResult

def format_yen(amount: float) -> str:
    # integer yen formatting, no locale dependency
    return f"¥{amount:,.0f}"

def format_results(results: List[PersonResult]) -> List[str]:
    return [f"{r.name}: {format_yen(r.total)}" for r in results]
