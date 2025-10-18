from flask import Flask, render_template, request
from calc.input_handler import parse_form
from calc.validator import validate_input
from calc.calculator import calculate_costs
from calc.formatter import format_results

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route("/", methods=["GET"])
def index():
    # 初期値（表示用はカンマ区切りの文字列）
    return render_template(
        "index.html",
        form_names=[],
        form_people=4,
        form_food=f"{10000:,}",
        form_transport=f"{8000:,}",
        form_camp=f"{12000:,}",
        form_food_exempt=[],
        form_transport_exempt=[],
        form_camp_exempt=[],
        errors=[]
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    form = request.form  # ImmutableMultiDict
    data = parse_form(form)  # InputData に変換（parse_form はカンマを許容）

    errors = validate_input(data)
    if errors:
        return render_template(
            "index.html",
            errors=errors,
            form_people=data.people,
            # 表示用はカンマ区切りの文字列にしてテンプレートへ渡す
            form_food=f"{int(data.food):,}",
            form_transport=f"{int(data.transport):,}",
            form_camp=f"{int(data.camp):,}",
            form_names=data.names,
            form_food_exempt=[bool(x) for x in data.food_exempt],
            form_transport_exempt=[bool(x) for x in data.transport_exempt],
            form_camp_exempt=[bool(x) for x in data.camp_exempt],
        )

    results_raw = calculate_costs(data)
    results = format_results(results_raw)  # 例: "メンバー1: ¥3,000"

    return render_template(
        "index.html",
        results=results,
        form_people=data.people,
        form_food=f"{int(data.food):,}",
        form_transport=f"{int(data.transport):,}",
        form_camp=f"{int(data.camp):,}",
        form_names=data.names,
        form_food_exempt=[bool(x) for x in data.food_exempt],
        form_transport_exempt=[bool(x) for x in data.transport_exempt],
        form_camp_exempt=[bool(x) for x in data.camp_exempt],
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
