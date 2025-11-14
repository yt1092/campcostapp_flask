from flask import Flask, render_template, request
from calc.input_handler import parse_form
from calc.validator import validate_input
from calc.calculator import calculate_costs
from calc.formatter import format_results

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        form_names=[],
        form_people=4,
        form_food=10000,
        form_transport=8000,
        form_camp=12000,
        form_food_exempt=[False, False, False, False],  # ← 初期値
        form_transport_exempt=[False, False, False, False],
        form_camp_exempt=[False, False, False, False],
        errors=[],
    )
def calculate():
    data = parse_form(request.form)
    errors = validate_input(data)
    if errors:
        return render_template(
            "index.html",
            errors=errors,
            form_people=data.people,
            form_food=data.food,
            form_transport=data.transport,
            form_camp=data.camp,
            form_names=data.names,
            form_food_exempt=data.food_exempt,
            form_transport_exempt=data.transport_exempt,
            form_camp_exempt=data.camp_exempt,
        )
    results_raw = calculate_costs(data)
    results = format_results(results_raw)
    return render_template(
        "index.html",
        results=results,
        form_people=data.people,
        form_food=data.food,
        form_transport=data.transport,
        form_camp=data.camp,
        form_names=data.names,
        form_food_exempt=data.food_exempt,
        form_transport_exempt=data.transport_exempt,
        form_camp_exempt=data.camp_exempt,
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


