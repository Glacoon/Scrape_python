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


def get_url_painting_page(url: str) -> list:
    soup = get_soup_page(url)
    vanGoghsPaintingsPages = []

    rows = soup.find_all('td', style="vertical-align: middle; text-align: left;")
    for row in rows:
        link_element = row.find('a')
        link_url = URL_BASE + link_element['href']
        vanGoghsPaintingsPages.append(link_url)

    return vanGoghsPaintingsPages


def get_url_paintings_in_page(url: str) -> list:
    # Obtient l'objet BeautifulSoup en utilisant l'URL spécifiée
    soup = get_soup_page(url)

    # Initialise une liste vide pour stocker les informations sur les peintures
    vanGoghsPaintings = []

    # Recherche la balise <td> avec l'attribut style="padding-left:10px" ou style="padding-left:20px"
    placeImg = soup.find('td', style="padding-left:10px") or soup.find('td', style="padding-left:20px") or soup.find(
        'td', style="padding-left: 100px;")

    # Vérifie si la balise <td> a été trouvée
    if placeImg:
        # Recherche la balise <a> à l'intérieur de la balise <td>
        a_element = placeImg.find('a')

        # Vérifie si la balise <a> a été trouvée
        if a_element:
            # Obtient le nom de la peinture à partir de l'attribut title de la balise <a>
            painting_name = a_element['title']

            # Recherche la balise <img> à l'intérieur de la balise <a>
            img_element = a_element.find('img')

            # Vérifie si la balise <img> a été trouvée
            if img_element:
                # Construit l'URL de l'image en concaténant l'URL de base et l'attribut src de la balise <img>
                img_url = URL_BASE + img_element['src']

                # Crée un dictionnaire avec les informations sur la peinture (URL de l'image et nom de la peinture)
                painting = {
                    'img_url': img_url,
                    'painting_name': painting_name
                }

                # Ajoute le dictionnaire à la liste des peintures
                vanGoghsPaintings.append(painting)

    # Renvoie la liste des peintures
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
    paintings_page = get_url_painting_page(URL)
    for painting_page in paintings_page:
        paintings = get_url_paintings_in_page(painting_page)
        download_paintings(paintings)
    print("Téléchargement terminé !")

DRIVER.quit()

"""
Fin ===============================================================================================================
"""
