import time


def scroll_bottom(driver, total_products):
    # Get scroll height

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)

        # Calculate new scroll height and compare with last scroll height
        loaded_products = driver.execute_script(
            'return document.getElementById("productList")'
            '.getElementsByTagName("li").length;'
        )

        if loaded_products >= total_products:
            break

    return driver.page_source
