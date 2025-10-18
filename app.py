from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    food_cost = 0
    transport_cost = 0
    camp_cost = 0
    members = [
        {"name": "メンバー1", "food": False, "transport": False, "camp": False},
        {"name": "メンバー2", "food": False, "transport": False, "camp": False},
        {"name": "メンバー3", "food": False, "transport": False, "camp": False},
    ]
    results = []

    if request.method == "POST":
        food_cost = int(float(request.form.get("food_cost", 0)))
        transport_cost = int(float(request.form.get("transport_cost", 0)))
        camp_cost = int(float(request.form.get("camp_cost", 0)))

        for i, member in enumerate(members):
            member["food"] = f"food_exempt_{i}" in request.form
            member["transport"] = f"transport_exempt_{i}" in request.form
            member["camp"] = f"camp_exempt_{i}" in request.form

        active_members = len(members)
        for member in members:
            total = 0
            if not member["food"]:
                total += food_cost / active_members
            if not member["transport"]:
                total += transport_cost / active_members
            if not member["camp"]:
                total += camp_cost / active_members
            results.append(int(total))

    return render_template(
        "index.html",
        food_cost=food_cost,
        transport_cost=transport_cost,
        camp_cost=camp_cost,
        members=members,
        results=results,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
