"""This is the Flask app."""

from flask import Flask, request
from threading import Thread
from .pull_prices import pull_prices, pull_prices_thread
from .read_db import get_stations_by_postal_code, get_stations_by_town_name

app = Flask(__name__)

pull_prices(init=True)

Thread(target=pull_prices_thread).start()


@app.route("/func/find_fuel_station/postal_code/")
def find_fuel_station_pc():
    postal_code = request.args.get("pc")
    print(get_stations_by_postal_code(postal_code))
    return "ok", 200


@app.route("/func/find_fuel_station/town/")
def find_fuel_station_town():
    town_name = request.args.get("tn")
    print(get_stations_by_town_name(town_name))
    return "ok", 200
