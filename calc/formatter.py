from typing import List
from calc.m_types import PersonResult

def format_yen(amount: float) -> str:
    return f"¥{amount:,.0f}"

def format_results(results: List[PersonResult]) -> List[str]:
    formatted = []
    for r in results:

        formatted.append(f"{r.name}: {format_yen(r.total)}")
    return formatted
