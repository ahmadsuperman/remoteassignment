#GraphQL
from flask import Flask, request, jsonify
import graphene

app = Flask(__name__)


stock_data = {
    "Apple": {
        "historical_price_data": [150.0, 155.0, 160.0, 165.0, 170.0],
        "highest_price": 170.0,
        "lowest_price": 150.0,
        "trading_volume": 1000000,
    },
    "Google": {
        "historical_price_data": [2200.0, 2250.0, 2300.0, 2350.0, 2400.0],
        "highest_price": 2400.0,
        "lowest_price": 2200.0,
        "trading_volume": 500000,
    },
    "Microsoft": {
        "historical_price_data": [290.0, 295.0, 300.0, 305.0, 310.0],
        "highest_price": 310.0,
        "lowest_price": 290.0,
        "trading_volume": 5000000,
    },
    "Tesla": {
        "historical_price_data": [220.0, 225.0, 230.0, 235.0, 240.0],
        "highest_price": 240.0,
        "lowest_price": 220.0,
        "trading_volume": 1000000,
    },
    "Amazon": {
        "historical_price_data": [110.0, 115.0, 120.0, 125.0, 130.0],
        "highest_price": 130.0,
        "lowest_price": 110.0,
        "trading_volume": 3000000,
    },
}


class StockInfo(graphene.ObjectType):
    name = graphene.String(description="Stock name")
    historical_price_data = graphene.List(
        graphene.Float, description="List of historical prices"
    )
    highest_price = graphene.Float(description="Highest price")
    lowest_price = graphene.Float(description="Lowest price")
    trading_volume = graphene.Float(description="Trading volume")


class Query(graphene.ObjectType):
    stock_info = graphene.Field(
        StockInfo, name=graphene.String(description="Stock name")
    )

    def resolve_stock_info(self, info, name):
        if name in stock_data:
            data = stock_data[name]
            return StockInfo(
                name=name,
                historical_price_data=data["historical_price_data"],
                highest_price=data["highest_price"],
                lowest_price=data["lowest_price"],
                trading_volume=data["trading_volume"],
            )
        else:
            return None


schema = graphene.Schema(query=Query)


html_form = """
<!DOCTYPE html>
<html>
<head>
  <title>Stock Query</title>
  <style>
    body {
      font-family: sans-serif;
    }

    h1 {
      font-size: 24px;
      margin-bottom: 20px;
      text-align: center;
    }

    form {
      display: flex;
      flex-direction: column;
    }

    label {
      margin-bottom: 10px;
    }

    textarea {
      width: 100%;
      height: 200px;
      margin-bottom: 10px;
    }

    input {
      width: 100%;
      padding: 10px 20px;
      background-color: #000;
      color: #fff;
      border: none;
      cursor: pointer;
    }

    .query-result {
      margin-top: 20px;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <h1>Stock Query</h1>
  <form method="post" action="/get_stock">
    <label for="query">Enter GraphQL Query:</label>
    <textarea id="query" name="query" rows="5" required></textarea>
    <input type="submit" value="Execute Query">
  </form>
  <div class="query-result">
    <h2>Query Result</h2>
    <pre id="result"></pre>
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return html_form


@app.route("/get_stock", methods=["POST"])
def get_stock_by_ui():
    query = request.form.get("query")
    result = schema.execute(query)
    return jsonify(result.data)


if __name__ == "__main__":
    app.run(debug=True)
