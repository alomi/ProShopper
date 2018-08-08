from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scraper import navigator as nav
from Shopper.models import *
import time
import math
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
#driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()

base_url_left = 'https://www.ica.se/handla/kategori/'
base_url_right = '/#s=maxi-ica-stormarknad-linkoping-id_08900/'
base_url_products = "/cujFlow/maxi-ica-stormarknad-linkoping-id_08900/?icaRequestType=ajax&currentStoreId=08900"

real_url_list = ['grilla-id_cat960004', 'kott--fagel---fisk-id_1',
                'mejeri--ost---agg-id_256',
                'frukt---gront-id_627', 'brod---kakor-id_358', 'fryst-id_628',
                'skafferi-id_939', 'fardigmat-id_208', 'dryck-id_306',
                'godis---snacks-id_399', 'barn-id_434', 'stad---disk-id_515',
                'halsa---skonhet-id_629', 'receptfria-lakemedel-id_860', 'djur-id_491',
                'kok-id_557', 'hem---fritid-id_556', 'kiosk-id_1627',
                'icas-egna-varor-id_cat860002', 'inspiration-id_cat1050001'
            ]

url_list = ['receptfria-lakemedel-id_860',

            ]


category_size = {}


def init():
    clear_db()

    # Behöver besökas för att resten av koden ska fungera?
    driver.get(get_url(url_list[0]))

    # Går igenom alla kategorier och tar fram antalet produkter, (url, antal)
    for category in url_list:
        html = get_html(base_url_left + category + base_url_products)
        size = int(html.find('strong').text)
        category_size[category] = size

    scrape()


def get_url(category):
    return base_url_left + category + base_url_right


def get_html_scroll(url, category):
    driver.implicitly_wait(5)
    driver.get(url)
    nav.scroll_bottom(driver, category_size[category])

    return BeautifulSoup(driver.page_source, 'html.parser')


def get_html(url):
    driver.implicitly_wait(5)
    driver.get(url)

    return BeautifulSoup(driver.page_source, 'html.parser')


def clear_db():
    print("Database has been cleared...\n")
    Product.objects.all().delete()


def get_db_size():
    return Product.objects.all().count()


# TODO: Lägg till wait tills att produktelementet finns på sidan, ingen mening
# att försöka scrapa innan det.
def scrape():
    print('Starting scraping...\n')
    start = time.time()
    for category in url_list:
        partial_time = time.time()
        html = get_html_scroll(get_url(category), category)

        # Hämta alla article taggar som har attributet 'data-addtional-info'
        product_num = 0

        articles = html.find_all('article', attrs={'data-addtional-info': True})
        for art in articles:
            # Spara produkten i databasen
            Product().store_product(art)
            product_num = product_num + 1

        tot = time.time() - partial_time
        print("Kategori: " + category.partition("-")[0] + " (" + str(product_num) + ")")
        print("Tid: ", int(tot))
        print()

    total_time = time.time() - start
    print("Closing driver\n")
    print("Database count", get_db_size())
    print("Total time: ", int(total_time))


base_url = 'https://www.ica.se/handla/maxi-ica-stormarknad-linkoping-id_08900/'
FORM = (By.ID, 'search')
DROP_DOWN = (By.ID, 'filter3')
OPTION = (By.XPATH, '//*[@id="filter3"]/option[2]')
ALL = (By.CSS_SELECTOR, '.product-filter__show-all')


'''
def testa():
    driver.maximize_window()
    driver.get(base_url)

    input_form = WebDriverWait(driver, 10).until(EC.presence_of_element_located(FORM))
    input_form.click()
    input_form.send_keys('#a', Keys.RETURN)

    form = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(FORM)
    )
    form.click()
    form.send_keys(Keys.RETURN)

    drop_down = WebDriverWait(driver, 10).until(EC.presence_of_element_located(DROP_DOWN))
    drop_down.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(OPTION)
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(ALL)
    ).click()

    print("first")
    nav.scroll_bottom(driver)
'''