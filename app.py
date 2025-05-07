from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json")
    data = response.json()
    return render_template("index.html", elements=data)

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
