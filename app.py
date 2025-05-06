from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_URL = "https://raw.githubusercontent.com/weiy-1/random-api/refs/heads/main/data_api.json"

@app.route("/")
def index():
    response = requests.get(API_URL)
    data = response.json()
    return render_template("index.html", products=data)

@app.route("/product/<product_name>")
def product(product_name):
    response = requests.get(API_URL)
    data = response.json()
    product_data = data.get(product_name)
    if product_data:
        return render_template("product.html", product=product_data)
    else:
        return f"Product '{product_name}' not found", 404

if __name__ == "__main__":
    app.run(debug=True)
