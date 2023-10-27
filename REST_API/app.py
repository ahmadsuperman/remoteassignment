#REST_API
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


stocks = [
    {"name": "Apple Inc.", "ticker": "AAPL", "price": 100.0},
    {"name": "Google LLC", "ticker": "GOOGL", "price": 2500.0},
    {"name": "Tesla, Inc.", "ticker": "TSLA", "price": 700.0},
    {"name": "Microsoft Corporation", "ticker": "MSFT", "price": 300.0},
    {"name": "Amazon.com, Inc.", "ticker": "AMZN", "price": 3000.0},
]


@app.route("/stocks", methods=["POST"])
def add_stock():
    data = request.get_json()
    if "name" in data and "ticker" in data and "price" in data:
        stock = {"name": data["name"], "ticker": data["ticker"], "price": data["price"]}
        stocks.append(stock)
        return jsonify({"message": "Stock added successfully"}), 201
    else:
        return jsonify({"error": "Wrong data entered"}), 400


@app.route("/")
def index():
    return render_template("index.html", stocks=stocks)


if __name__ == "__main__":
    app.run()
