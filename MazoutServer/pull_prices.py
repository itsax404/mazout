"""This is the algorithm that pulls fuel prices, regularly."""

from requests import get
from io import BytesIO
from zipfile import ZipFile
from xml.etree import ElementTree
from pymongo import MongoClient
from sys import exit
from time import sleep
from . import logger


def pull_prices_thread():
    while True:
        sleep(300)  # pulled every 5 minutes
        pull_prices()


def pull_prices(init: bool = False) -> None:
    logger.log("Trying to pull prices...")
    try:
        response = get("https://donnees.roulez-eco.fr/opendata/instantane")
        if response.status_code != 200:
            raise Exception("Response status code is not 200.")
        zipfile = ZipFile(BytesIO(response.content))
        zipfile.extractall(path="./data")
        stations = ElementTree.parse("./data/PrixCarburants_instantane.xml").getroot()
        client = MongoClient("127.0.0.1").mazout
        if init:
            client.static.delete_many({"field": "fuel_db_id"})
            client.static.insert({"field": "fuel_db_id"})
            db = client.fuelPrices1
        else:
            fuel_db_id = list(client.static.find({"field": "fuel_db_id"}))
            if len(fuel_db_id) < 1:
                db = client.fuelPrices1
            else:
                db = client.fuelPrices2 if fuel_db_id[0]["value"] == 1 else client.fuelPrices1
        logger.log("Chose collection " + db.name + ".")
        db.drop()
        for station in stations:
            try:
                st_data = {
                    "coordinates": [
                        float(station.attrib["latitude"]) / 100000,
                        float(station.attrib["longitude"]) / 100000
                    ],
                    "postalCode": station.attrib["cp"],
                    "fuels": []
                }
                for attr in station:
                    if attr.tag == "adresse":
                        st_data["address"] = attr.text
                    elif attr.tag == "ville":
                        st_data["city"] = attr.text
                    elif attr.tag == "horaires":
                        st_data["24-24"] = False if attr.attrib["automate-24-24"] == "0" else True
                    elif attr.tag == "prix":
                        st_data["fuels"].append({
                            "fuel": attr.attrib["nom"],
                            "price": float(attr.attrib["valeur"])
                        })
                for attr in ["address", "city"]:
                    if attr not in st_data.keys():
                        st_data[attr] = ""
                if "24-24" not in st_data.keys():
                    st_data["24-24"] = False
                db.insert(st_data)
            except Exception as e:
                logger.log_err("One station could not be parsed. Exception : " + str(e))
        client.static.find_one_and_update({"field": "fuel_db_id"}, {"$set": {"value": int(db.name[-1])}})
        logger.log("Successfully pulled prices.")
    except Exception as e:
        logger.log_err("Prices not pulled. Exception : " + str(e))
        if init:
            exit(1)
        pass
