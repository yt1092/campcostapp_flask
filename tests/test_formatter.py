from calc.types import PersonResult
from calc.formatter import format_results

def test_format():
    r = [PersonResult(name='A', total=1234.5)]
    out = format_results(r)
    assert '¥' in out[0]
    assert '1,235' in out[0] or '1235' in out[0]