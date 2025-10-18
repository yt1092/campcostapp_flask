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
        errors=[]
    )

@app.route("/calculate", methods=["POST"])
def calculate():
    form = request.form
    cleaned = {}
    for k in ["food", "transport", "camp", "people"]:
        v = form.get(k, "0")
        cleaned[k] = int(v.replace(",", ""))
    names = []
    i = 0
    while f"name_{i}" in form:
        names.append(form.get(f"name_{i}", f"メンバー{i+1}"))
        i += 1
    cleaned["names"] = names

    data = parse_form(cleaned)
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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)


