"""Parse the following dataset : https://static.data.gouv.fr/resources/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/20151015-121340/fic_etiq_edition_40-mars-2015.zip"""
import dataclasses
from pymongo import MongoClient
import csv
import requests
from io import BytesIO
from zipfile import ZipFile
import os.path


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
    emissions_hc : float
    emissions_nox : float
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
            return (other.puissance_administrative == self.puissance_administrative) and (other.puissance_heure == self.puissance_heure) and (self.puissance_maximale == other.puissance_maximale) and (self.consommation_urbaine == other.consommation_urbaine) and (self.consommation_extra_urbaine == other.consommation_extra_urbaine)and (self.consommation_mixte == other.consommation_mixte)            
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
                "emissions_nox ":self.emissions_nox,
                "emissions_hc_nox": self.emissions_hc_nox,
                "emissions_particules": self.emissions_particules,
                "masse_minimale": self.masse_minimale,
                "masse_maximale": self.masse_maximale,
                "champ_homologation_europeene": self.champ_homologation_européeene,
                "date_mise_a_jour": self.date_mise_a_jour
                }
        return data

def download_and_unzip(url_website):
    http_response = requests.get(url_website)
    zipfile = ZipFile(BytesIO(http_response.content))
    zipfile.extractall(path=".././data")


def filter_and_add_cars():
    
    """
    This function filters same cars and add cars to the database
    """
    file = open(".././data/fic_etiq_edition_40-mars-2015.csv", "r")

    csv_reader = csv.reader(file, delimiter=";")

    voitures = list()
    variantes = list()
    voitures_par_variantes = dict()

    for line in csv_reader:
        if not line[0] == "lib_mrq_doss":
            for i in range(len(line)):
                element = line[i]
                if(len(element) != 0):
                    if element[-1] == " ":
                        line[i] = element[:-1]

            infos_boite = line[12].split(" ")
            type_boite = infos_boite[0]
            nb_rapports = int(infos_boite[1]) if infos_boite[1] != "." else 0
            voiture = Voiture(line[0], line[1], line[4], line[5], line[6], line[7], True if line[8]=="oui" else False, int(line[9]), float(line[10]) if line[10] != "" else 0, 0 if line[11] == "" else float(line[11]), type_boite, nb_rapports, float(line[13]) if line[13] != "" else 0.0, float(line[14]) if line[14] != "" else 0.0, float(line[15]) if line[15] != "" else 0.0, float(line[16]) if line[16] != "" else 0.0, float(line[17]) if line[17] != "" else 0.0, float(line[18]) if line[18] != "" else 0.0, float(line[19]) if line[19] != "" else 0.0, float(line[20]) if line[20] != "" else 0.0, float(line[21]) if line[21] != "" else 0.0, int(line[22]), int(line[23]),line[24], line[25])
            if not voiture in voitures:
                voitures.append(voiture)
                variantes.append(voiture.type_variante)
                voitures_par_variantes[voiture.type_variante] = voiture    

    database = MongoClient("127.0.0.1").mazout
    collection = database.co2Data
    for variante, voiture in voitures_par_variantes.items():
        collection.insert_one(voiture.get_json_data())
def pull_cars():
    if(not os.path.isfile("fic_etiq_edition_40-mars-2015.csv")):
        download_and_unzip("https://static.data.gouv.fr/resources/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/20151015-121340/fic_etiq_edition_40-mars-2015.zip")
        filter_and_add_cars()