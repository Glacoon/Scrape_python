import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Selenium in headless mode
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

PHRASE_RECHERCHE = "Diagnostic immobilier"
URL_WIKI = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"

def get_soup_page(url):
    # Get the soup of the page
    driver.get(url)
    return BeautifulSoup(driver.page_source, "html.parser")

def get_x_biggest_town(x):
    # Get the x biggest towns of France
    soup = get_soup_page(URL_WIKI)
    table = soup.find("table", class_="wikitable").findAll('tr')[2:x + 2]
    return [ligne.find("b").find("a")["title"] for ligne in table]

def get_word_in_page(url, word):
    # Check if a word is anywhere in the page
    response = requests.get(url)
    html = response.text.lower()

    if word in url.lower() or word in html:
        return True

    soup = BeautifulSoup(html, "html.parser")
    img_tags = soup.find_all('img')
    a_tags = soup.find_all('a')

    if any(word in img.get('alt', '').lower() for img in img_tags):
        return True

    if any(word in a.get('href', '').lower() for a in a_tags):
        return True

    return False

def create_csv(filename, headers):
    # Create a CSV file with headers
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

def scrape_urls(cities, filename):
    headers = ["Villes", "URLs"]
    create_csv(filename, headers)

    for city in cities:
        print(city)

        query = f"{PHRASE_RECHERCHE} {city}"
        url_google = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        soup = get_soup_page(url_google)
        results = soup.find("div", id='rso').findAll("div", recursive=False)

        urls = [
            div.find("a")["href"]
            for div in results
            if div.find("a")["href"].startswith("https")
        ]

        urls = [url for url in urls if "www.dimo-diagnostic.net" not in url]

        sorted_urls = []
        for url in urls:
            if url == "Annuaire":
                sorted_urls.append(url)
            elif not get_word_in_page(url, "quotidiag"):
                sorted_urls.append(url)

        sorted_urls.insert(0, city)

        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(sorted_urls)

if __name__ == "__main__":
    cities = get_x_biggest_town(102)

    scrape_urls(cities[:51], "CSV_Url_page1.csv")
    scrape_urls(cities[:51], "CSV_Url_page2.csv")
