# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

MAX_WAIT = 10
MAX_TRIES = 4
PLACE_URL_IDENTIFIER = "google.com/maps/place"

def get_driver(debug=False):
        options = Options()

        if not debug:
            options.add_argument("--headless")
        else:
            options.add_argument("--window-size=1366,768")

        options.add_argument("--disable-notifications")
        options.add_argument("--lang=en-GB")
        input_driver = webdriver.Chrome(options=options)

        return input_driver

def wait_for_panel_data(driver, debug=False):
    panel_text = ""
    tries = 0

    #check panel fully loaded
    while 'Suggest an edit' not in panel_text and 'About this data' not in panel_text and tries < MAX_TRIES:
        time.sleep(2)
        tries += 1

        #collect text from all the panels
        panel_text = ""
        widget_panes = driver.find_elements_by_class_name('widget-pane')
        for element in widget_panes:
            panel_text += element.text

        #scroll to the bottom each of the panel to force content to load
        driver.execute_script("Array.from(document.getElementsByClassName('widget-pane-content scrollable-y')).map(div => div.scrollTop = div.scrollHeight)")

    #if we exit at MAX_TRIES, indicate that content never loaded
    if tries == MAX_TRIES:
        if debug:
            print(panel_text)
        return (panel_text, False)

    return (panel_text, True)
    
def check_labels(search_url, debug=False):
    driver = get_driver(debug=debug)
    driver.get(search_url)
    wait = WebDriverWait(driver, MAX_WAIT)

    #wait until page redirects from the search view to the place details view
    wait.until(EC.url_contains(PLACE_URL_IDENTIFIER))

    #if we never reach the place details view, exit
    if PLACE_URL_IDENTIFIER not in driver.current_url:
        driver.quit()
        return {
            "success": False
        }


    panel_text, ok = wait_for_panel_data(driver, debug)
    driver.quit()

    if not ok:
         return {
            "success": False
        }

    return {
        "success": True,
        "lgbtq": bool("LGBTQ friendly" in panel_text),
        "veteran": bool("Identifies as veteran-led" in panel_text),
        "women": bool("Identifies as women-led" in panel_text),
        "black": bool("Identifies as Black-owned" in panel_text),
    }

if __name__ == '__main__':
    URL = "https://www.google.com/maps/place/First+Goal+Heating+and+Cooling/@40.8861359,-74.5471438,17z/data=!3m1!4b1!4m5!3m4!1s0x89c301744a6ab527:0xde887089293ef0c2!8m2!3d40.8861319!4d-74.5449551"
    print(check_labels(URL, debug=True))
