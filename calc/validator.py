from calc.m_types import InputData

def validate_input(data: InputData) -> list:
    """
    Returns list of error messages (empty if no errors).
    """
    errors = []
    if not (1 <= data.people <= 100):
        errors.append("人数は1〜100の間で指定してください。")
    for v in (data.food, data.transport, data.camp):
        if v < 0:
            errors.append("費用は0以上で指定してください。")
            break
    # lists length checks
    n = data.people
    if not (len(data.names) == len(data.food_exempt) == len(data.transport_exempt) == len(data.camp_exempt) == n):
        errors.append("メンバー情報の個数が人数と一致していません。")
    return errors