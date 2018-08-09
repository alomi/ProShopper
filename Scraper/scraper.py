import time

from bs4 import BeautifulSoup
from selenium import webdriver
from Scraper import navigator as nav
from Shopper.models import *

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_experimental_option("prefs",{"profile.managed_default_content_settings.images": 2})
prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)

base_url = 'https://www.ica.se/handla/maxi-ica-stormarknad-linkoping-id_08900/'
base_url_left = 'https://www.ica.se/handla/kategori/'
base_url_right = '/#s=maxi-ica-stormarknad-linkoping-id_08900/'
base_url_products = "/cujFlow/maxi-ica-stormarknad-linkoping-id_08900/?icaRequestType=ajax&currentStoreId=08900"

TOTAL_CATEGORIES_PATH = '//*[@id="categoryNavigation"]/ol/child::*'
CATEGORIES_PATH = '//*[@id="categoryNavigation"]/ol/child::*[%s]/div/a'

driver.get(base_url)

# total categories ( + 1 because they are indexed starting from 1 on web page)
number_of_categories = len(driver.execute_script(
        'return document.getElementsByClassName("category-tree left-navigation__links--group")'
)[0].find_elements_by_xpath(TOTAL_CATEGORIES_PATH)) + 1

# Dict that stores all categories and number of products/category
category_size = {}


def init():
    clear_db()

    # Gets the 'a' tag based on xpath, gets the URL and splits it
    # retrieves the category specific part of the URL
    for i in range(1, number_of_categories):
        category_a = driver.find_element_by_xpath((CATEGORIES_PATH % str(i)))
        category_size[category_a.get_attribute('href').split("/")[5]] = 0

    # Går igenom alla kategorier och tar fram antalet produkter, (url, antal)
    for category in category_size:
        html = get_html(base_url_left + category + base_url_products)
        size = int(html.find('strong').text)
        category_size[category] = size
        print(size)

    scrape()
    driver.close()


def get_html_scroll(url, category):
    driver.get(url)

    # Scroll down the page to get all HTML then parse that HTML
    return BeautifulSoup(nav.scroll_bottom(
        driver, category_size[category]), 'html.parser'
    )


def get_html(url):
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
    for category in category_size:
        partial_time = time.time()
        html = get_html_scroll(
            base_url_left + category + base_url_right, category
        )
        scroll_time = time.time() - partial_time

        product_num = 0

        # Hämta alla article taggar som har attributet 'data-addtional-info'
        articles = html.find_all('article', {'data-addtional-info': True})
        for art in articles:
            # Spara produkten i databasen
            Product().store_product(art)
            product_num = product_num + 1

        tot = time.time() - partial_time
        print("Kategori: " + category.partition("-")[0] + " (" + str(product_num) + ")")
        print("Tid: ", int(tot))
        print("Scroll-time: ", int(scroll_time))
        print()

    total_time = time.time() - start
    print("Closing driver\n")
    print("Database count", get_db_size())
    print("Total time: %.2f" % (int(total_time) / 60) + " min")
