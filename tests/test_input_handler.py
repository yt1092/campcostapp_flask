from calc.input_handler import parse_form

def test_parse_minimal():
    form = {'people': '2', 'name_0': 'A', 'name_1': 'B'}
    data = parse_form(form)
    assert data.people == 2
    assert data.names == ['A', 'B']
    assert data.food_exempt == [False, False]