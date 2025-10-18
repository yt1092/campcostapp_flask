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
        form_food_exempt=[],
        form_transport_exempt=[],
        form_camp_exempt=[],
        results=[],
        errors=[]
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    form = request.form
    data = parse_form(form)

    # 小数(.0)除去
    try:
        data.food = int(float(data.food))
        data.transport = int(float(data.transport))
        data.camp = int(float(data.camp))
    except ValueError:
        pass

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
            results=[]
        )

    results_raw = calculate_costs(data)
    results = format_results(results_raw)

    return render_template(
        "index.html",
        results=results,
        errors=[],
        form_people=data.people,
        form_food=data.food,
        form_transport=data.transport,
        form_camp=data.camp,
        form_names=data.names,
        form_food_exempt=data.food_exempt,
        form_transport_exempt=data.transport_exempt,
        form_camp_exempt=data.camp_exempt,
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
