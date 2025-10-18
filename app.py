from flask import Flask, render_template, request
from calc.input_handler import parse_form
from calc.validator import validate_input
from calc.calculator import calculate_costs
from calc.formatter import format_results
import os

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route("/", methods=["GET"])
def index():
    # 初期値
    initial_people = 4
    return render_template(
        "index.html",
        form_names=[f"メンバー{i+1}" for i in range(initial_people)],
        form_people=initial_people,
        form_food=10000,
        form_transport=8000,
        form_camp=12000,
        form_food_exempt=[False]*initial_people,
        form_transport_exempt=[False]*initial_people,
        form_camp_exempt=[False]*initial_people,
        results=None,
        errors=[]
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    form = request.form
    data = parse_form(form)

    errors = validate_input(data)
    if errors:
        return render_template(
            "index.html",
            errors=errors,
            form_people=data.people,
            form_food=int(data.food),
            form_transport=int(data.transport),
            form_camp=int(data.camp),
            form_names=data.names,
            form_food_exempt=[bool(x) for x in data.food_exempt],
            form_transport_exempt=[bool(x) for x in data.transport_exempt],
            form_camp_exempt=[bool(x) for x in data.camp_exempt],
            results=None
        )

    results_raw = calculate_costs(data)
    results = format_results(results_raw)
    return render_template(
        "index.html",
        results=results,
        form_people=data.people,
        form_food=int(data.food),
        form_transport=int(data.transport),
        form_camp=int(data.camp),
        form_names=data.names,
        form_food_exempt=[bool(x) for x in data.food_exempt],
        form_transport_exempt=[bool(x) for x in data.transport_exempt],
        form_camp_exempt=[bool(x) for x in data.camp_exempt],
        errors=[]
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
