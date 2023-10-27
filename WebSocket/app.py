# app.py WebSocket

from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import random
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)


def get_stock_price():
    while True:
        price = round(random.uniform(100, 200), 2)
        yield price
        time.sleep(1)


def send_stock_price():
    price_generator = get_stock_price()
    while True:
        price = next(price_generator)
        socketio.emit("stock_price", {"price": price})
        time.sleep(1)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


if __name__ == "__main__":
    data_thread = Thread(target=send_stock_price)
    data_thread.daemon = True
    data_thread.start()
    socketio.run(app, debug=True)
