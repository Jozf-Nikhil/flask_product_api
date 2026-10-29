from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {
        "id": 1,
        "name": "keyboard",
        "price": 1200
    },
    {
        "id": 2,
        "name": "mouse",
        "price": 500
    },
    {
        "id": 3,
        "name": "monitor",
        "price": 5000
    }
]

nextProductId = 4

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Product API server is running"
    })

@app.route("/api/products", methods=["GET"])
def getProducts():
    return jsonify({
        "success": True,
        "message": "Fetch all Products successfully",
        "data": products
    }),200

@app.route("/api/products/<int:product_id>", methods=["GET"])
def getProduct(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify({
                "success": True,
                "message": "Fetch Product successfully",
                "data": product
            }),200

    return jsonify({
        "success": False,
        "message": "Product not found"
    }), 404

@app.route("/api/products", methods=["POST"])
def createProduct():
    global nextProductId

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": True,
            "message": "A JSON object is required"
        })

    name = data.get("name")
    price = data.get("price")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "success": False,
            "message": "Product name is required"
        })

    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        return jsonify({
            "success": False,
            "message": "Price must be a non-negative number"
        }), 400

    newProduct = {
        "id": nextProductId,
        "name": name.strip(),
        "price": price
    }

    products.append(newProduct)
    nextProductId += 1

    return jsonify({
        "success": True,
        "message": "Product created successfully",
        "data": newProduct
    }), 201


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def updateProduct(product_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "A JSON object is required"
        }), 400

    name = data.get("name")
    price = data.get("price")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "success": False,
            "message": "Product name is required"
        }), 400

    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        return jsonify({
            "success": False,
            "message": "Price must be a non-negative number"
        }), 400

    for product in products:
        if product["id"] == product_id:
            product["name"] = name.strip()
            product["price"] = price

            return jsonify({
                "success": True,
                "message": "Product updated successfully",
                "data" : product
            }), 200

    return jsonify({
        "success": False,
        "message": "Product not found"
    }), 404


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def deleteProduct(product_id):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            deleteProduct = products.pop(index)

            return jsonify({
                "success": True,
                "message": "Product deleted successfully",
                "data": deleteProduct
            }), 200

        return jsonify({
            "success": False,
            "message": "Product not found"
        }), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)