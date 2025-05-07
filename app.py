from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json")
    data = response.json()

    # --- Filtering ---
    group_block = request.args.get("groupBlock")
    standard_state = request.args.get("standardState")

    if group_block:
        data = [el for el in data if el["groupBlock"].lower() == group_block.lower()]
    if standard_state:
        data = [el for el in data if el["standardState"].lower() == standard_state.lower()]

    # --- Sorting ---
    sort_by = request.args.get("sortBy")
    order = request.args.get("order", "asc")

    if sort_by:
        reverse = order == "desc"
        try:
            data.sort(key=lambda x: float(x.get(sort_by, 0)) if x.get(sort_by) not in [None, ""] else 0, reverse=reverse)
        except ValueError:
            data.sort(key=lambda x: x.get(sort_by, "").lower(), reverse=reverse)

    # For filter options in the form
    group_blocks = sorted(set(el["groupBlock"] for el in data if el["groupBlock"]))
    standard_states = sorted(set(el["standardState"] for el in data if el["standardState"]))

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
    response = requests.get("https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json")
    data = response.json()
    element_data = next((el for el in data if el['symbol'].lower() == symbol.lower()), None)
    if element_data:
        return render_template("element.html", element=element_data)
    else:
        return f"Element '{symbol}' not found", 404

if __name__ == "__main__":
    app.run(debug=True)
