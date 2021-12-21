from pymongo import MongoClient

client = MongoClient("127.0.0.1").mazout


def get_stations_by_postal_code(postal_code: str) -> list:
    db = client.fuelPrices2 if list(client.static.find({"field": "fuel_db_id"}))[0]["value"] == 1 \
        else client.fuelPrices1
    return list(db.find({"postalCode": postal_code}))


def get_stations_by_town_name(town_name: str) -> list:
    db = client.fuelPrices1 if list(client.static.find({"field": "fuel_db_id"}))[0]["value"] == 1 \
        else client.fuelPrices2
    return list(db.find({"cityNMLZ": town_name.lower().replace('-', ' ')}))
