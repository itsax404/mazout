"""This is the Flask app."""

from flask import Flask, Response
from threading import Thread
from .pull_prices import pull_prices, pull_prices_thread
from .parse_vehicles import pull_cars

app = Flask(__name__)

pull_cars()

pull_prices(init=True)

Thread(target=pull_prices_thread).start()


@app.route("/ping/")
def ping() -> Response:
    return "pong", 200


from . import fuel_stations_api
