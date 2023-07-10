import requests as req
import csv
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
Setup
"""
options = Options()
options.add_argument("--headless")
DRIVER = webdriver.Chrome(options=options)

"""
Variables
"""
PHRASE_RECHERCHE = "Diagnostic immobilier"
URL_WIKI = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"

"""
Fonctions
"""


def get_soup_page(url: str) -> bs:
    DRIVER.get(url)
    return bs(DRIVER.page_source, "html.parser")


def get_x_biggest_town(x: int) -> list:
    soup = get_soup_page(URL_WIKI)
    table = soup.find("table", class_="wikitable").findAll('tr')[2:x + 2]
    return [ligne.find("b").find("a")["title"] for ligne in table]


def get_word_in_page(url: str, word: str) -> bool:
    response = req.get(url)
    html = response.text
    if word in url.lower() or word in html.lower():
        return True
    img_tags = bs(html, "html.parser").find_all('img')
    for img in img_tags:
        alt_text = img.get('alt', '')
        if word in alt_text.lower():
            return True
    a_tags = bs(html, "html.parser").find_all('a')
    for a in a_tags:
        a_text = a.get('href', '')
        if word in a_text.lower():
            return True
    return False


def create_csv(name: str, entetes: list[str]) -> csv:
    with open(f"{name}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(entetes)


def ban_url_casse(soup: list):
    new_soup = []
    for item in soup:
        if "www.dimo-diagnostic.net" not in str(item):
            new_soup.append(item)
    return new_soup


def verif_arobiz(soup: list, listurl: list):
    new_listurl = []
    for urlRecherche in soup:
        if get_word_in_page(urlRecherche, "arobiz"):
            new_listurl.append(urlRecherche)
    listurl.extend(new_listurl)


def verif_quotidiag(listurl: list):
    new_listurl = []
    quotidiag_urls = []
    for url in listurl:
        if get_word_in_page(url, "quotidiag"):
            quotidiag_urls.append(url)
        else:
            new_listurl.append(url)
    listurl.clear()
    listurl.extend(new_listurl)
    listurl.append("Annuaire")
    listurl.extend(quotidiag_urls)


def get_links_from_search(url: str) -> list:
    soup = get_soup_page(url)
    links = [
        div.find("a")["href"]
        for div in soup.find("div", id='rso').findAll("div", recursive=False)
        if div.find("a") and "href" in div.find("a").attrs and div.find("a")["href"].startswith("https")
    ]
    return ban_url_casse(links)


"""
Main
"""


def main():
    entetes = ["Villes", "URLs"]
    create_csv('CSV_Url_page1', entetes)
    create_csv('CSV_Url_page2', entetes)
    cities = get_x_biggest_town(5)  # We want the 5 biggest cities of France
    for city in cities:
        print(city)
        QUERY = f"{PHRASE_RECHERCHE} {city}"  # We want to search for the phrase + the current city

        # Utilisation de la fonction pour récupérer les liens de la première page de recherche
        URL_GOOGLE = f"https://www.google.com/search?q={QUERY.replace(' ', '+')}"
        soup = get_links_from_search(URL_GOOGLE)

        # Utilisation de la fonction pour récupérer les liens de la deuxième page de recherche
        URL_GOOGLE_PAGE2 = f"https://www.google.com/search?q={QUERY.replace(' ', '+')}&start=10"
        soup2 = get_links_from_search(URL_GOOGLE_PAGE2)

        soup = ban_url_casse(soup)
        soup2 = ban_url_casse(soup2)
        list_url = []
        list_url2 = []
        verif_arobiz(soup, list_url)
        verif_arobiz(soup2, list_url2)
        verif_quotidiag(list_url)
        verif_quotidiag(list_url2)
        list_url.insert(0, city)
        list_url2.insert(0, city)
        with open('CSV_Url_page1.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list_url)
        with open('CSV_Url_page2.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list_url2)


if __name__ == "__main__":
    main()
