from calc.m_types import InputData

def _as_list_from_form(form, key):
    """
    form may be ImmutableMultiDict (has getlist) or a plain dict (no getlist).
    This returns a list (possibly empty).
    """
    if hasattr(form, "getlist"):
        return form.getlist(key)
    # plain dict: maybe keys like "food_exempt[]" or "food_exempt" present with comma-separated value
    v = form.get(key, [])
    if isinstance(v, list):
        return v
    if v is None or v == "":
        return []
    # single string -> put into list
    return [v]

def _to_float_safe(s):
    try:
        if s is None:
            return 0.0
        if isinstance(s, (int, float)):
            return float(s)
        # remove commas and spaces
        s2 = str(s).replace(",", "").strip()
        if s2 == "":
            return 0.0
        return float(s2)
    except Exception:
        return 0.0

def parse_form(form) -> InputData:
    """
    フォームデータを InputData に変換
    - 数値はカンマありでもOK
    - チェックボックスは name="xxx_exempt[]" で送られる想定
    """
    # 人数（int）
    try:
        people_raw = form.get("people", 1)
        people = int(float(str(people_raw).replace(",", "").strip() or 1))
    except Exception:
        people = 1

    # 各費用（float）
    food = _to_float_safe(form.get("food", 0))
    transport = _to_float_safe(form.get("transport", 0))
    camp = _to_float_safe(form.get("camp", 0))

    # メンバー名（人数に応じてリスト化）
    names = []
    for i in range(people):
        # form key name_{i}
        key = f"name_{i}"
        raw = form.get(key, "")
        name = str(raw).strip() if raw is not None else ""
        if not name:
            name = f"メンバー{i+1}"
        names.append(name)

    # チェックボックス -> bool リスト
    # We expect checkboxes named like "food_exempt[]" in HTML
    def parse_checkbox_list(key: str, length: int) -> list[bool]:
        raw_list = _as_list_from_form(form, key)
        # common behavior: checked checkboxes send "on" (or value), so treat truthy strings as True
        bool_list = []
        for v in raw_list:
            if isinstance(v, bool):
                bool_list.append(v)
            else:
                vs = str(v).lower()
                bool_list.append(vs in ("on", "true", "1"))
        # pad to length
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
