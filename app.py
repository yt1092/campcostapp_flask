from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # 初期値
    food = 10000
    transport = 8000
    camp = 12000
    people = 3
    names = [f"メンバー{i+1}" for i in range(people)]
    food_ex = [False for _ in range(people)]
    transport_ex = [False for _ in range(people)]
    camp_ex = [False for _ in range(people)]
    results = None

    if request.method == "POST":
        # フォーム入力を取得
        food = int(float(request.form.get("food", 0)))
        transport = int(float(request.form.get("transport", 0)))
        camp = int(float(request.form.get("camp", 0)))
        people = int(request.form.get("people", people))

        names = [request.form.get(f"name_{i}", f"メンバー{i+1}") for i in range(people)]
        food_ex = [request.form.get(f"food_exempt_{i}") == "on" for i in range(people)]
        transport_ex = [request.form.get(f"transport_exempt_{i}") == "on" for i in range(people)]
        camp_ex = [request.form.get(f"camp_exempt_{i}") == "on" for i in range(people)]

        # 各費用の人数あたり
        food_share = food // people
        transport_share = transport // people
        camp_share = camp // people

        # 計算
        results = []
        for i in range(people):
            total = 0
            if not food_ex[i]:
                total += food_share
            if not transport_ex[i]:
                total += transport_share
            if not camp_ex[i]:
                total += camp_share
            results.append(total)

    return render_template(
        "index.html",
        food=food,
        transport=transport,
        camp=camp,
        people=people,
        names=names,
        food_ex=food_ex,
        transport_ex=transport_ex,
        camp_ex=camp_ex,
        results=results,
    )

if __name__ == "__main__":
    app.run(debug=True)
