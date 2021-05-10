"""
labels.py
Scraper to extract labels from gmaps entry 
@author Justin Tinker (jatinker@stanford.edu)
"""
# -*- coding: utf-8 -*-
from util import get_driver, labels_response, name_not_found, labels_not_found
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

log = logging.getLogger(__name__)

MAX_WAIT = 8 #time in seconds to wait for redirect
MAX_TRIES = 4 #number of times to look for indicators that label information has loaded
DELAY = 2 #number of seconds to wait between tries
PLACE_URL_IDENTIFIER = "google.com/maps/place" #indicates gmaps has found the place we're searching for
PANEL_LOADED_IDENTIFIERS = ['Suggest an edit', 'About this data'] #presence of one of these texts indicates label information has loaded

def wait_for_panel_data(driver):
    """Holds the browser until the panel containing the labels is loaded, if  possible

    Args:
        driver (webdriver.Firefox): Browser Instance

    Returns:
        tuple(string, bool): Text of the panel (if available), bool indicating whether the panel was successfully loaded (true if yes, false if timed out)
    """
    panel_text = ""
    
    #check panel fully loaded
    for i in range(MAX_TRIES):
        for identifier in PANEL_LOADED_IDENTIFIERS:
            if identifier in panel_text:
                return (panel_text, True)

        time.sleep(DELAY)

        #collect text from all the panels
        panel_text = ""
        widget_panes = driver.find_elements_by_class_name('widget-pane')
        for element in widget_panes:
            panel_text += element.text

        #scroll to the bottom each of the panel to force content to load
        driver.execute_script("Array.from(document.getElementsByClassName('widget-pane-content scrollable-y')).map(div => div.scrollTop = div.scrollHeight)")

    #if we exit at MAX_TRIES, indicate that content never loaded
    log.debug(f"Reached max tries, panel text: {panel_text}")
    return (panel_text, False)
 
def check_labels(search_url, debug=False):
    """Get the labels (black owned, women-led, etc.) for a particular business on googlemaps

    Args:
        search_url (string): url describing place in the form https://www.google.com/maps/search/{name}+near+{address}'
        debug (bool, optional): If true, run visible browser, if false run headless. Defaults to False.

    Returns:
        dict: {
                success (bool): True if the place was found and the label information was loaded. False otherwise
                error_type (str or None): If not successful, 'missing_place' if place not found and 'missing_labels' if labels not loaded. None if not successful
                url (str or None): If not successful, search url of the place that generated this request. None if successful
                lgbtq (bool or None): If successful, True if place identifies as lgbtq friendly. None if not successful
                veteran (bool or None): If successful, True if place identifies as verteran-owned. None if not successful
                women (bool or None): If successful, True if place identifies as women-led. None if not successful
                black (bool or None): If successful, True if place identifies as black owned. None if not successful
            }
    """

    driver = get_driver(debug)
    driver.get(search_url)
    wait = WebDriverWait(driver, MAX_WAIT)

    #wait until page redirects from the search view to the place details view
    try:
        wait.until(EC.url_contains(PLACE_URL_IDENTIFIER))
    except TimeoutException:
        driver.quit()
        return name_not_found(search_url)

    panel_text, ok = wait_for_panel_data(driver)
    driver.quit()

    if not ok:
         return labels_not_found(search_url)

    return labels_response(panel_text)