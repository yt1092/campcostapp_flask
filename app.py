from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # 初期値
    food = 10000
    transport = 8000
    camp = 12000
    people = 1
    names = ["メンバー1"]
    food_ex = [False]
    transport_ex = [False]
    camp_ex = [False]
    results = None

    if request.method == "POST":
        # POSTから値を取得
        food = int(float(request.form.get("food", food)))
        transport = int(float(request.form.get("transport", transport)))
        camp = int(float(request.form.get("camp", camp)))
        people = int(request.form.get("people", people))

        # メンバー情報
        names = [request.form.get(f"name_{i}", f"メンバー{i+1}") for i in range(people)]
        food_ex = [f"food_exempt_{i}" in request.form for i in range(people)]
        transport_ex = [f"transport_exempt_{i}" in request.form for i in range(people)]
        camp_ex = [f"camp_exempt_{i}" in request.form for i in range(people)]

        # 計算
        results = []
        for i in range(people):
            total = 0
            if not food_ex[i]:
                total += food // people
            if not transport_ex[i]:
                total += transport // people
            if not camp_ex[i]:
                total += camp // people
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
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True, port=10000)
