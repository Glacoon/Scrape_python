"""
Created on Thu 4th 2023 by C.Guillian
Projet de Scrapping pour Arobiz
Objectif: trouver et archiver les sites créés par Arobiz (annuaires/clients) dans les 100 plus grandes villes de France
"""

"""
Imports ===============================================================================================================
"""
import requests
from bs4 import BeautifulSoup
import csv
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
Setup ===============================================================================================================
"""
# Headless mode
options = Options()
options.add_argument("--headless")
DRIVER = webdriver.Chrome(options=options)

"""
Variables ============================================================================================================
"""

LISTES_MOTS_CLES = [
    "DPE Tours",
    "Diagnostic immobilier Joué-lès-Tours",
    "DPE Joué-lès-Tours",
    "Diagnostic immobilier Saint-Cyr-sur-Loire",
    "DPE Saint-Cyr-sur-Loire",
    "Diagnostic immobilier Saint-Pierre-des-Corps",
    "DPE Saint-Pierre-des-Corps",
    "Diagnostic immobilier Saint-Avertin",
    "DPE Saint-Avertin",
    "Diagnostic immobilier Amboise",
    "Diagnostic immobilier Chambray-lès-Tours",
    "DPE Chambray-lès-Tours",
    "Diagnostic immobilier Fondettes",
    "Diagnostic immobilier Montlouis-sur-Loire",
    "DPE Montlouis-sur-Loire",
    "Diagnostic immobilier La riche",
    "DPE La riche",
    "Diagnostic immobilier Chinon",
    "DPE Chinon",
    "Diagnostic immobilier Ballan-Miré",
    "DPE Ballan-Miré",
    "Diagnostic immobilier Monts",
    "DPE Monts",
    "Diagnostic immobilier Loches",
    "DPE Loches",
    "Diagnostic immobilier Blois",
    "DPE Blois",
    "Diagnostic immobilier Vendôme",
    "DPE Vendôme",
    "Diagnostic immobilier Romorantin-Lanthenay",
    "DPE Romorantin-Lanthenay",
    "Diagnostic immobilier Vineuil",
    "DPE Vineuil",
    "Diagnostic immobilier Mer",
    "DPE Mer",
    "Diagnostic immobilier Salbris",
    "DPE Salbris"
]

URL_RECHERCHE = "sodiatec.net"  # URL à rechercher
trouve = False

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

"""
Fonctions ============================================================================================================
"""


def create_csv(name: str, entetes: list[str]) -> csv:
    """
    Create a CSV file with the name and the entetes.

    Args:
       name (str): The name of the CSV file.
       entetes (str): The name of the begining line of the file.

    Returns:
       csv: The CSV file.
    """
    with open(f"{name}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(entetes)


"""
Main ===============================================================================================================
"""
entetes = ['Mot-clé', 'Page', 'Date']  # Entêtes du fichier CSV
create_csv('Positionnement_mots_clés_' + URL_RECHERCHE, entetes)  # Création du fichier CSV

# Code pour trouver le site dans les 10 premières pages de Google pour chaque mot-clé
for mot_cle in LISTES_MOTS_CLES:
    trouve = False  # Réinitialise 'trouve' pour chaque mot-clé
    for page in range(10):
        date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')  # Date et heure de la recherche
        url = f"https://www.google.com/search?q={mot_cle}&start={page * 10}"  # URL de la recherche avec le mot-clé
        # dans google
        response = requests.get(url, headers=headers)  # Requête HTTP GET (pour récupérer le code source de la page)

        # Vérifier si le quota de recherche a été atteint
        if response.status_code == 429:
            # Afficher un message d'erreur de dépassement de quota
            print("Quota de recherche dépassé. Veuillez réessayer plus tard.")
            break

        # Vérifier si le site a été trouvé
        soup = BeautifulSoup(response.text, "html.parser")  # Parser le code source de la page
        rso_div = soup.find("div", id="rso")  # Trouver la div avec l'id 'rso' qui correspond au résultat hors publicité

        if rso_div:
            # class="Wt5Tfe"
            search_results = soup.find_all("div", class_="g")  # Trouver tous les résultats
            # de recherche
            for position, result in enumerate(search_results, start=1):
                link = result.find("a")
                if link and URL_RECHERCHE in link.get("href", ""):
                    trouve = True
                    print(
                        f"Le site se situe en page {page + 1} pour le "
                        f"mot-clé:{mot_cle}")

                    with open('Positionnement_mots_clés_' + URL_RECHERCHE + '.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([mot_cle, page + 1, date])
                    break  # Sortir de la boucle du résultat de recherche
            if trouve:
                break
            # Sortir de la boucle du mot clé si le site est trouvé

        if not trouve and page == 9:  # Si le site n'est pas trouvé après avoir parcouru les 10 pages

            # Ajouter une ligne dans le CSV pour indiquer "non trouvé"
            with open('Positionnement_mots_clés_' + URL_RECHERCHE + '.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([mot_cle, "non trouvé", "non trouvé", date])

            # Afficher un message dans la console
            print(f"Le site n'a pas été trouvé dans les 10 premières pages pour le mot-clé: {mot_cle}")
