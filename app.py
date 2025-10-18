from flask import Flask, render_template, request
from calc.input_handler import parse_form
from calc.validator import validate_input
from calc.calculator import calculate_costs
from calc.formatter import format_results
import os

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route("/", methods=["GET"])
def index():
    initial_people = 4
    names = [f"メンバー{i+1}" for i in range(initial_people)]
    form_food_exempt = [False] * initial_people
    form_transport_exempt = [False] * initial_people
    form_camp_exempt = [False] * initial_people

    return render_template(
        "index.html",
        form_people=initial_people,
        form_names=names,
        form_food=10000,
        form_transport=8000,
        form_camp=12000,
        form_food_exempt=form_food_exempt,
        form_transport_exempt=form_transport_exempt,
        form_camp_exempt=form_camp_exempt,
        results=None,
        errors=[]
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    data = parse_form(request.form)
    errors = validate_input(data)
    if errors:
        return render_template(
            "index.html",
            errors=errors,
            form_people=data.people,
            form_names=data.names,
            form_food=int(data.food),
            form_transport=int(data.transport),
            form_camp=int(data.camp),
            form_food_exempt=[bool(x) for x in data.food_exempt],
            form_transport_exempt=[bool(x) for x in data.transport_exempt],
            form_camp_exempt=[bool(x) for x in data.camp_exempt],
            results=None
        )

    results_raw = calculate_costs(data)
    results = format_results(results_raw, as_integer=True)  # 整数・カンマ付き表示対応

    return render_template(
        "index.html",
        results=results,
        errors=[],
        form_people=data.people,
        form_names=data.names,
        form_food=int(data.food),
        form_transport=int(data.transport),
        form_camp=int(data.camp),
        form_food_exempt=[bool(x) for x in data.food_exempt],
        form_transport_exempt=[bool(x) for x in data.transport_exempt],
        form_camp_exempt=[bool(x) for x in data.camp_exempt],
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
