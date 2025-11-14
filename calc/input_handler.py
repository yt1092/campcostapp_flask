from calc.m_types import InputData

def parse_form(form) -> InputData:

    # 人数
    try:
        people = int(form.get("people", 1) or 1)
    except ValueError:
        people = 1

    # 各費用
    try:
        food = float(form.get("food", 0) or 0)
    except ValueError:
        food = 0

    try:
        transport = float(form.get("transport", 0) or 0)
    except ValueError:
        transport = 0

    try:
        camp = float(form.get("camp", 0) or 0)
    except ValueError:
        camp = 0

    # メンバー名
    names = []
    for i in range(people):
        name = form.get(f"name_{i}", "").strip()
        if not name:
            name = f"メンバー{i+1}"
        names.append(name)

    # チェックボックス（免除） → bool リスト
    def get_exempt_list(prefix: str) -> list[bool]:
        lst = []
        for i in range(people):
            lst.append(form.get(f"{prefix}{i}") == "on")
        return lst

    food_exempt = get_exempt_list("foodExempt_")
    transport_exempt = get_exempt_list("transportExempt_")
    camp_exempt = get_exempt_list("campExempt_")

    return InputData(
        people=people,
        food=food,
        transport=transport,
        camp=camp,
        names=names,
        food_exempt=food_exempt,
        transport_exempt=transport_exempt,
        camp_exempt=camp_exempt,
    )
