"""This file defines all requests to get fuel stations, based on different criteria."""

from .server import app
from flask import request, Response
from .read_db import get_stations_by_postal_code, get_stations_by_town_name, get_stations_by_dept_code
from json import dumps


@app.route("/func/find_fuel_station/postal_code/")
def find_fuel_station_pc() -> Response:
    postal_code = request.args.get("pc")
    data = get_stations_by_postal_code(postal_code)
    for el in data:
        del el["_id"]
        del el["cityNMLZ"]
    res = app.response_class(
        response=dumps(data),
        status=200,
        mimetype="application/json"
    )
    return res


@app.route("/func/find_fuel_station/town/")
def find_fuel_station_town() -> Response:
    town_name = request.args.get("tn")
    data = get_stations_by_town_name(town_name)
    for el in data:
        del el["_id"]
        del el["cityNMLZ"]
    res = app.response_class(
        response=dumps(data),
        status=200,
        mimetype="application/json"
    )
    return res


@app.route("/func/find_fuel_station/dept/")
def find_fuel_station_dept() -> Response:
    dept_code = request.args.get("dc")
    data = get_stations_by_dept_code(dept_code)
    for el in data:
        del el["_id"]
        del el["cityNMLZ"]
    res = app.response_class(
        response=dumps(data),
        status=200,
        mimetype="application/json"
    )
    return res
