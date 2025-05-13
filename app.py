from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from requests.exceptions import RequestException

app = Flask(__name__)
app.secret_key = "supersceret"

@app.route("/")
def index():
    try:
        response = requests.get("https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json")
        response.raise_for_status()
        data = response.json()
    except RequestException:
        flash("Error fetching data. Please try again later.", "error")
        data = []


    group_block = request.args.get("groupBlock")
    standard_state = request.args.get("standardState")

    if group_block:
        data = [el for el in data if el["groupBlock"].lower() == group_block.lower()]
    if standard_state:
        data = [el for el in data if el["standardState"].lower() == standard_state.lower()]


    sort_by = request.args.get("sortBy")
    order = request.args.get("order", "asc")

    if sort_by:
        reverse = order == "desc"
        try:
            data.sort(key=lambda x: float(x.get(sort_by, 0)) if x.get(sort_by) not in [None, ""] else 0, reverse=reverse)
        except ValueError:
            data.sort(key=lambda x: x.get(sort_by, "").lower(), reverse=reverse)


    group_blocks = sorted(set(el["groupBlock"] for el in data if el.get("groupBlock")))
    standard_states = sorted(set(el["standardState"] for el in data if el.get("standardState")))

    return render_template(
        "index.html",
        elements=data,
        group_blocks=group_blocks,
        standard_states=standard_states,
        selected_group_block=group_block,
        selected_standard_state=standard_state,
        selected_sort_by=sort_by,
        selected_order=order
    )


@app.route("/element/<symbol>")
def element(symbol):
    try:
        response = requests.get("https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json")
        response.raise_for_status()
        data = response.json()
    except RequestException:
        flash("Failed to load element data.", "error")
        return redirect(url_for("index"))

    element_data = next((el for el in data if el["symbol"].lower() == symbol.lower()), None)
    if element_data:
        return render_template("element.html", element=element_data)
    else:
        return render_template("404.html", symbol=symbol), 404

if __name__ == "__main__":
    app.run(debug=True)
