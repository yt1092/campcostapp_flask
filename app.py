from flask import Flask, render_template, request
from calc.input_handler import parse_form
from calc.validator import validate_input
from calc.calculator import calculate_costs
from calc.formatter import format_results
from calc.utils import safe_float

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/", methods=["GET"])
def index():
    # 初期表示
    return render_template(
        "index.html",
        form_people=1,
        form_food=0,
        form_transport=0,
        form_camp=0,
        form_names=["メンバー1"],
        form_food_exempt=[False],
        form_transport_exempt=[False],
        form_camp_exempt=[False],
        results=None,
        errors=None
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    form_data = request.form.to_dict(flat=False)
    single_form = {k: v[0] if isinstance(v, list) and v else v for k, v in form_data.items()}
    for k in ["food", "transport", "camp"]:
        if k in single_form:
            single_form[k] = single_form[k].replace(",", "")

    # 入力解析
    data = parse_form(single_form)
    errors = validate_input(data)
    if errors:
        return render_template(
            "index.html",
            results=None,
            errors=errors,
            form_people=data.people,
            form_food=data.food,
            form_transport=data.transport,
            form_camp=data.camp,
            form_names=data.names,
            form_food_exempt=data.food_exempt,
            form_transport_exempt=data.transport_exempt,
            form_camp_exempt=data.camp_exempt
        )

    # 計算
    results = calculate_costs(data)
    formatted = format_results(results)

    return render_template(
        "index.html",
        results=formatted,
        errors=None,
        form_people=data.people,
        form_food=f"{data.food:,.0f}",
        form_transport=f"{data.transport:,.0f}",
        form_camp=f"{data.camp:,.0f}",
        form_names=data.names,
        form_food_exempt=data.food_exempt,
        form_transport_exempt=data.transport_exempt,
        form_camp_exempt=data.camp_exempt
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
