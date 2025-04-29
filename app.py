from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    # Fetch Apple product data
    response = requests.get("https://raw.githubusercontent.com/spencerwooo/apple-product-guide/refs/heads/master/data.json")
    data = response.json()

    # Convert the JSON dict to a list of products
    products = []
    for key, value in data.items():
        product = {
            'name': value.get('name', key),
            'advice': value.get('advice', 'N/A'),
            'average': value.get('average', 'N/A'),
            'daysSinceLastRelease': value.get('daysSinceLastRelease', 'N/A'),
            'releaseDate': value.get('releaseDate', 'N/A'),
            'status': value.get('status', 'N/A'),
            'image': value.get('image'),
            'slug': key.replace(" ", "-").replace("\"", "")  # For URL routing
        }
        products.append(product)

    return render_template("index.html", products=products)

@app.route("/product/<slug>")
def product_detail(slug):
    # Re-fetch the data (or cache it in a real app)
    response = requests.get("https://raw.githubusercontent.com/spencerwooo/apple-product-guide/refs/heads/master/data.json")
    data = response.json()

    # Find the product by matching slug
    for key, value in data.items():
        generated_slug = key.replace(" ", "-").replace("\"", "")
        if generated_slug == slug:
            product = value
            product['name'] = value.get('name', key)
            product['slug'] = slug
            return render_template("product.html", product=product)

    return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True)