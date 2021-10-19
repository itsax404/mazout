import os
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


def download_and_unzip(url_website):
    http_response = urlopen(url_website)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path="./datas")

def clean_data_folder():
    for file_name in os.listdir("./datas"):
        os.remove(f"./datas/{file_name}")

def download_all_datas():
    clean_data_folder()
    url_websites = ["https://donnees.roulez-eco.fr/opendata/jour", "https://www.data.gouv.fr/fr/datasets/r/bc42c2e3-d24c-4499-a966-d35656c6cfc1"]
    for url_website in url_websites:
        download_and_unzip(url_website)

download_all_datas()