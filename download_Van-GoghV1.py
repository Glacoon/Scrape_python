"""
Created on Sat 17th June 2023 by C.Guillian Projet de Scrapping de Van-Gogh Objectif: Trouver et télécharger les
images des peintures de Van-Gogh sur le site vincentvangogh.org ainsi que les noms des peintures
"""

"""
Imports ===============================================================================================================
"""

import requests
import os
from slugify import slugify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
Setup ===============================================================================================================
"""

options = Options()
options.add_argument("--headless")
DRIVER = webdriver.Chrome(options=options)

"""
Variables ===============================================================================================================
"""

URL = "https://www.vincentvangogh.org/van-gogh-paintings.jsp"
URL_BASE = "https://www.vincentvangogh.org/"

"""
Fonctions ===============================================================================================================
"""


def get_soup_page(url: str) -> BeautifulSoup:
    DRIVER.get(url)
    return BeautifulSoup(DRIVER.page_source, "html.parser")


def get_url_paintings(url: str) -> list:
    soup = get_soup_page(URL)
    vanGoghsPaintings = []

    rows = soup.find_all('tr', style='border-bottom: 1px dashed #888;')
    for row in rows:
        img_element = row.find('img')
        img_url = URL_BASE + img_element['src']

        name_element = row.find_all('a')[1]
        painting_name = name_element.text.strip()

        painting = {
            'img_url': img_url,
            'painting_name': painting_name
        }
        vanGoghsPaintings.append(painting)

    return vanGoghsPaintings


def download_paintings(vanGoghPainting: list):
    for painting in vanGoghPainting:
        print(painting['painting_name'] + " is downloading...")
        img_url = painting['img_url']
        painting_name = painting['painting_name']
        response = requests.get(img_url)

        # Utilisez la fonction slugify pour générer un nom de fichier valide
        filename = f"{slugify(painting_name)}.jpg"
        filepath = os.path.join("/Users/guilliancelle/Documents/RepositoryGithub/scrape_guiguou/van-gogh_paintings",
                                filename)

        with open(filepath, "wb") as file:
            file.write(response.content)


"""
Main ===============================================================================================================
"""

if __name__ == '__main__':
    paintings = get_url_paintings(URL)
    download_paintings(paintings)
    print("Téléchargement terminé !")

DRIVER.quit()

"""
Fin ===============================================================================================================
"""

