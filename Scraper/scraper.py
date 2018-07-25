from bs4 import BeautifulSoup
from selenium import webdriver
from Scraper import navigator as nav
from Shopper.models import *

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

def scrape():
    # Frukt
    # driver.get('https://www.ica.se/handla/kategori/frukt---gront-id_627/#s=maxi-ica-stormarknad-linkoping-id_08900/')

    # Mejeri, ost & ägg
    # driver.get('https://www.ica.se/handla/kategori/mejeri--ost---agg-id_256/#s=maxi-ica-stormarknad-linkoping-id_08900/')

    # Läkemedel
    driver.get('https://www.ica.se/handla/kategori/receptfria-lakemedel-id_860/#s=maxi-ica-stormarknad-linkoping-id_08900/')
    raw_html = nav.scroll_bottom(driver)

    html = BeautifulSoup(raw_html, 'html.parser')

    for item in html.find_all('article', attrs={'data-addtional-info': True}):
        info = item['data-addtional-info']
        a = info.split("\"")

        product = Product(
            product_title=item['data-title'],
            product_price=a[3],
            product_category=a[7],
            product_brand=a[11]
        )

        ##product.print_product()
        product.save()

    alla = Product.objects.all()
    print(alla[0].get_title())




