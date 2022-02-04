"""Parse the following dataset : https://static.data.gouv.fr/resources/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/20151015-121340/fic_etiq_edition_40-mars-2015.zip"""
import dataclasses
from pymongo import MongoClient
from csv import reader
from requests import get
from io import BytesIO
from zipfile import ZipFile
import os.path
from . import logger


@dataclasses.dataclass
class Voiture:
    """
    """
    marque: str
    modèle: str
    description_commerciale: str
    code_identification: str
    type_variante: str
    energie: str
    hybride: bool
    puissance_administrative: int
    puissance_maximale: float
    puissance_heure: float
    type_boite: str
    nombre_rapports: int
    consommation_urbaine: float
    consommation_extra_urbaine: float
    consommation_mixte: float
    emissions_co2_mixte: float
    emissions_co_type_1: float
    emissions_hc: float
    emissions_nox: float
    emissions_hc_nox: float
    emissions_particules: float
    masse_minimale: int
    masse_maximale: int
    champ_homologation_européeene: str
    date_mise_a_jour: str

    def __eq__(self, other: object) -> bool:
        """
        This function return a boolean if two Voiture class are same.
        """
        if isinstance(other, Voiture):
            if other.description_commerciale != self.description_commerciale:
                return False
            return (other.puissance_administrative == self.puissance_administrative) and (
                        other.puissance_heure == self.puissance_heure) and (
                               self.puissance_maximale == other.puissance_maximale) and (
                               self.consommation_urbaine == other.consommation_urbaine) and (
                               self.consommation_extra_urbaine == other.consommation_extra_urbaine) and (
                               self.consommation_mixte == other.consommation_mixte)
        return False

    def __repr__(self) -> str:
        """
        Just a function who make a representation of a Voiture class
        """
        return f"{self.marque} {self.modèle} {self.description_commerciale} {self.code_identification} {self.type_variante} {self.energie} {self.hybride} {self.puissance_administrative} {self.puissance_maximale} {self.puissance_heure} {self.type_boite} {self.nombre_rapports} {self.consommation_urbaine} {self.consommation_extra_urbaine} {self.consommation_mixte} {self.emissions_co2_mixte} {self.emissions_co_type_1} {self.emissions_hc} {self.emissions_nox} {self.emissions_hc_nox} {self.emissions_particules} {self.masse_minimale} {self.masse_maximale} {self.champ_homologation_européeene} {self.date_mise_a_jour}"

    def get_json_data(self) -> str:
        """Parse the Voiture data into JSON"""
        data = {"marque": self.marque,
                "modele": self.modèle,
                "description_commerciale": self.description_commerciale,
                "code_identification": self.code_identification,
                "type_variante": self.type_variante,
                "energie": self.energie,
                "hybride": self.hybride,
                "puissance_administrative": self.puissance_administrative,
                "puissance_maximale": self.puissance_maximale,
                "puissance_heure": self.puissance_heure,
                "type_boite": self.type_boite,
                "nombre_rapports": self.nombre_rapports,
                "consommation_urbaine": self.consommation_urbaine,
                "consommation_extra_urbaine": self.consommation_extra_urbaine,
                "consommation_mixte": self.consommation_mixte,
                "emissions_co2_mixte": self.emissions_co2_mixte,
                "emissions_co_type_1": self.emissions_co_type_1,
                "emissions_hc ": self.emissions_hc,
                "emissions_nox ": self.emissions_nox,
                "emissions_hc_nox": self.emissions_hc_nox,
                "emissions_particules": self.emissions_particules,
                "masse_minimale": self.masse_minimale,
                "masse_maximale": self.masse_maximale,
                "champ_homologation_europeene": self.champ_homologation_européeene,
                "date_mise_a_jour": self.date_mise_a_jour
                }
        return data


def download_and_unzip(url_website):
    http_response = get(url_website)
    zipfile = ZipFile(BytesIO(http_response.content))
    zipfile.extractall(path="./data")


def filter_and_add_cars() -> dict:
    """
    This function filters same cars and add cars to the database
    """
    with open("./data/fic_etiq_edition_40-mars-2015.csv", "r", encoding='ISO-8859-1') as file:
        csv_reader = reader(file, delimiter=";")

        cars = list()
        variants = list()
        cars_by_variants = dict()

        for line in csv_reader:
            if not line[0] == "lib_mrq_doss":
                for i in range(len(line)):
                    element = line[i]
                    if len(element) != 0:
                        if element[-1] == " ":
                            line[i] = element[:-1]

                gearbox_details = line[12].split(" ")
                type_of_gearbox = gearbox_details[0]
                number_of_speeds = int(gearbox_details[1]) if gearbox_details[1] != "." else 0
                car = Voiture(line[0], line[1], line[4], line[5], line[6], line[7], True if line[8] == "oui" else False,
                              int(line[9]), float(line[10]) if line[10] != "" else 0,
                              0 if line[11] == "" else float(line[11]), type_of_gearbox, number_of_speeds,
                              float(line[13]) if line[13] != "" else 0.0, float(line[14]) if line[14] != "" else 0.0,
                              float(line[15]) if line[15] != "" else 0.0, float(line[16]) if line[16] != "" else 0.0,
                              float(line[17]) if line[17] != "" else 0.0, float(line[18]) if line[18] != "" else 0.0,
                              float(line[19]) if line[19] != "" else 0.0, float(line[20]) if line[20] != "" else 0.0,
                              float(line[21]) if line[21] != "" else 0.0, int(line[22]), int(line[23]), line[24], line[25])
                if car not in cars:
                    cars.append(car)
                    variants.append(car.type_variante)
                    cars_by_variants[car.type_variante] = car

    database = MongoClient("127.0.0.1").mazout
    database.co2Data.rename("co2Data_old")
    collection = database.co2Data
    try:
        for variant, car in cars_by_variants.items():
            collection.insert_one(car.get_json_data())
        database.co2Data_old.drop()
        return {"status": True}
    except Exception as e:
        database.co2Data.drop()
        database.co2Data_old.rename("co2Data")
        return {"status": False, "exception": str(e)}


def pull_cars():
    logger.log("Trying to parse cars...")
    url_to_pull = "https://static.data.gouv.fr/resources/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/20151015-121340/fic_etiq_edition_40-mars-2015.zip"
    # try:
    if not os.path.isfile("fic_etiq_edition_40-mars-2015.csv"):
        download_and_unzip(url_to_pull)
        status = filter_and_add_cars()
        if status["status"]:
            logger.log("Successfully parsed cars.")
        else:
            logger.log_err("Cars not parsed. Using data already in the db. Exception : " + status["exception"])
    # except Exception as e:
        # logger.log_err("Cars not parsed. Using data already in the db. Exception : " + str(e))
