"""This is the Flask app."""

from flask import Flask, Response
from threading import Thread
from .pull_prices import pull_prices, pull_prices_thread
from .algorithms import parse_vehicles

app = Flask(__name__)

pull_prices(init=True)
parse_vehicles.pull_cars()

Thread(target=pull_prices_thread).start()

@app.route("/ping/")
def ping() -> Response:
    return "pong", 200


from . import fuel_stations_api
