from flask import Flask, render_template
import requests

app = Flask(__name__)

product_links = {
    "macbook-air": "https://www.apple.com/macbook-air/",
    "macbook-pro": "https://www.apple.com/macbook-pro/",
    "imac": "https://www.apple.com/imac/",
    "mac-mini": "https://www.apple.com/mac-mini/",
    "mac-studio": "https://www.apple.com/mac-studio/",
    "mac-pro": "https://www.apple.com/mac-pro/",
    "ipad": "https://www.apple.com/ipad/",
    "ipad-air": "https://www.apple.com/ipad-air/",
    "ipad-mini": "https://www.apple.com/ipad-mini/",
    "ipad-pro": "https://www.apple.com/ipad-pro/",
    "iphone": "https://www.apple.com/iphone/",
    "iphone-se": "https://www.apple.com/iphone-se/",
    "apple-watch": "https://www.apple.com/watch/",
    "apple-watch-ultra": "https://www.apple.com/apple-watch-ultra/",
    "apple-tv": "https://www.apple.com/apple-tv-4k/",
    "airpods": "https://www.apple.com/airpods/",
    "homepod": "https://www.apple.com/homepod/"
}

@app.route("/")
def index():
    response = requests.get("https://raw.githubusercontent.com/spencerwooo/apple-product-guide/refs/heads/master/data.json")
    data = response.json()

    products = []
    for key, value in data.items():
        slug = key.replace(" ", "-").replace("\"", "").lower()
        product = {
            'name': value.get('name', key),
            'advice': value.get('advice', 'N/A'),
            'average': value.get('average', 'N/A'),
            'daysSinceLastRelease': value.get('daysSinceLastRelease', 'N/A'),
            'releaseDate': value.get('releaseDate', 'N/A'),
            'status': value.get('status', 'N/A'),
            'image': value.get('image'),
            'slug': slug
        }
        products.append(product)

    return render_template("index.html", products=products)

@app.route("/product/<slug>")
def product_detail(slug):
    response = requests.get("https://raw.githubusercontent.com/spencerwooo/apple-product-guide/refs/heads/master/data.json")
    data = response.json()

    for key, value in data.items():
        generated_slug = key.replace(" ", "-").replace("\"", "").lower()
        if generated_slug == slug:
            product = value
            product['name'] = value.get('name', key)
            product['slug'] = slug

            matched_link = "https://www.apple.com"
            for applethingy in product_links:
                if applethingy in slug:
                    matched_link = product_links[applethingy]
                    break

            product['apple_link'] = matched_link
            return render_template("product.html", product=product)

    return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True)
