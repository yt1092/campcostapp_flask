from typing import List
from calc.m_types import InputData, PersonResult

def calculate_costs(data: InputData) -> List[PersonResult]:
    """
    Returns list of PersonResult containing name and total amount (float).
    Calculation rules:
      - Each category is split among non-exempt members.
      - If all are exempt for a category, that category cost is ignored (0 distributed).
    """
    n = data.people

    food_contributors = sum(1 for v in data.food_exempt if not v)
    transport_contributors = sum(1 for v in data.transport_exempt if not v)
    camp_contributors = sum(1 for v in data.camp_exempt if not v)

    food_per = (data.food / food_contributors) if food_contributors > 0 else 0.0
    transport_per = (data.transport / transport_contributors) if transport_contributors > 0 else 0.0
    camp_per = (data.camp / camp_contributors) if camp_contributors > 0 else 0.0

    results = []
    for i in range(n):
        total = 0.0
        if not data.food_exempt[i]:
            total += food_per
        if not data.transport_exempt[i]:
            total += transport_per
        if not data.camp_exempt[i]:
            total += camp_per
        results.append(PersonResult(name=data.names[i], total=total))
    return results