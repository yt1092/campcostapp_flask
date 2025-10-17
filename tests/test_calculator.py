from calc.types import InputData
from calc.calculator import calculate_costs

def test_basic_split():
    data = InputData(
        people=2,
        food=1000.0,
        transport=500.0,
        camp=0.0,
        names=['A', 'B'],
        food_exempt=[False, False],
        transport_exempt=[False, False],
        camp_exempt=[False, False],
    )
    results = calculate_costs(data)
    assert len(results) == 2
    assert results[0].total == 1000.0/2 + 500.0/2