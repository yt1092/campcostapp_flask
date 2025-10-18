from calc.m_types import InputData

def parse_form(form) -> InputData:
    """
    フォームデータを InputData に変換
    空文字や不正な値が来ても安全に処理
    """
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

    # メンバー名（人数に応じてリスト化）
    names = []
    for i in range(people):
        name = form.get(f"name_{i}", "").strip()
        if not name:
            name = f"メンバー{i+1}"
        names.append(name)

    # チェックボックス（免除） → bool リスト
    def parse_checkbox_list(key: str, length: int) -> list[bool]:
        raw_list = form.getlist(key)
        # "true" とか文字列のリストを bool に変換、足りなければ False で補完
        bool_list = [(v.lower() == "true") for v in raw_list]
        while len(bool_list) < length:
            bool_list.append(False)
        return bool_list[:length]

    food_exempt = parse_checkbox_list("food_exempt[]", people)
    transport_exempt = parse_checkbox_list("transport_exempt[]", people)
    camp_exempt = parse_checkbox_list("camp_exempt[]", people)

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
