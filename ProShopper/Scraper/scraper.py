from bs4 import BeautifulSoup
from selenium import webdriver
from Scraper import navigator as nav


def scrape():
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

    # Frukt
    # driver.get('https://www.ica.se/handla/kategori/frukt---gront-id_627/#s=maxi-ica-stormarknad-linkoping-id_08900/')

    # Mejeri, ost & ägg
    # driver.get('https://www.ica.se/handla/kategori/mejeri--ost---agg-id_256/#s=maxi-ica-stormarknad-linkoping-id_08900/')

    # Läkemedel
    driver.get('https://www.ica.se/handla/kategori/receptfria-lakemedel-id_860/#s=maxi-ica-stormarknad-linkoping-id_08900/')
    raw_html = nav.scroll_bottom(driver)

    html = BeautifulSoup(raw_html, 'html.parser')
    chunks = html.find_all('div', {"class": "productTextContent"})
    total = 0;
    for link in chunks:
        heading = link.find('h3')
        heading_data = heading.text
        print(heading_data)
        total += 1
    print(total)
