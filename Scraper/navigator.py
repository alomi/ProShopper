import time


def scroll_bottom(driver, total_products):

    loaded_products = 0
    while loaded_products < total_products:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)

        # Calculate new scroll height and compare with last scroll height
        loaded_products = driver.execute_script(
            'return document.getElementById("productList")'
            '.getElementsByTagName("li").length;'
        )

    return driver.find_element_by_xpath(
        '//*[@id="productList"]'
    ).get_attribute("outerHTML")
