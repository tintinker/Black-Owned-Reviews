"""
labels.py
Scraper to extract labels from gmaps entry 
@author Justin Tinker (jatinker@stanford.edu)
"""
# -*- coding: utf-8 -*-
from util import get_driver, gmaps_reponse, labels_response, name_not_found, labels_not_found, no_reviews_response, reviews_response
import time
import logging

log = logging.getLogger(__name__)

MAX_TRIES = 4 #number of times to look for indicators that label information has loaded
DELAY = 2 #number of seconds to wait between tries

REVIEWS_DELAY = 1
REVIEWS_MAX_TRIES = 3

PLACE_URL_IDENTIFIER = "google.com/maps/place" #indicates gmaps has found the place we're searching for
PANEL_LOADED_IDENTIFIERS = ['Suggest an edit', 'About this data'] #presence of one of these texts indicates label information has loaded
SUGGESTION_IDENTIFIERS = ['Partial match', 'Partial matches', 'Showing results']

def get_panel_text(driver):
    panel_text = ""
    widget_panes = driver.find_elements_by_class_name('widget-pane')
    for element in widget_panes:
        panel_text += element.text
    return panel_text

def get_first_suggestion(driver):
    for elem in driver.find_elements_by_xpath("//a[@href]"):
        if PLACE_URL_IDENTIFIER in str(elem.get_attribute("href")):
            return str(elem.get_attribute("href"))

def check_redirected(driver):
    return PLACE_URL_IDENTIFIER in driver.current_url

def check_identifiers_loaded(driver):
    for identifier in PANEL_LOADED_IDENTIFIERS:
        if identifier in get_panel_text(driver):
            return True
    return False

def check_suggestion_available(driver):
    for identifier in SUGGESTION_IDENTIFIERS:
        if identifier in get_panel_text(driver):
            return True
    return False

def scroll_to_bottom(driver):
    driver.execute_script("Array.from(document.getElementsByClassName('widget-pane-content scrollable-y')).map(div => div.scrollTop = div.scrollHeight)")

def scroll_to_bottom_reviews(driver):
    driver.execute_script("Array.from(document.getElementsByClassName('section-scrollbox')).map(div => div.scrollTop = div.scrollHeight)")

def wait_for_new_reviews(driver, prev_num, max_num):
    if prev_num >= max_num:
        return False, prev_num

    scroll_to_bottom_reviews(driver)
    review_elems = driver.find_elements_by_xpath("//div[@class='ODSEW-ShBeI-content']")
    
    for _ in range(REVIEWS_MAX_TRIES):
        time.sleep(REVIEWS_DELAY)
        if len(review_elems) > prev_num:
            return True, len(review_elems)
        scroll_to_bottom_reviews(driver)
    return False, prev_num

def get_category(driver):
    elems = driver.find_elements_by_xpath("//button[@jsaction='pane.rating.category']")
    return elems[0].text if len(elems) > 0 else ""

def get_reviews(driver):
    elems = driver.find_elements_by_xpath("//div[@jsaction='pane.reviewChart.moreReviews']")
    if len(elems) > 0:
        elems[0].click()
    else:
        return None, None, []

    time.sleep(DELAY)
    
    avg_rev_elems = driver.find_elements_by_xpath("//div[@class='gm2-display-2']")
    avg_rating = float(avg_rev_elems[0].text) if len(avg_rev_elems) > 0 else -1

    total_rev_elems = driver.find_elements_by_xpath("//div[@class='gm2-caption']")
    valid_total_counts = [float(e.text.strip()[:-len(" reviews")].replace(",","")) for e in total_rev_elems if e.text.strip().endswith(" reviews")]
    num_ratings = valid_total_counts[0] if len(valid_total_counts) > 0 else -1

    previous_num_reviews = 0
    if avg_rating < 0 or num_ratings < 0:
            return avg_rating, num_ratings, []

    while True:
        another, previous_num_reviews = wait_for_new_reviews(driver, previous_num_reviews, num_ratings)
        if not another:
            break
    
    return avg_rating, num_ratings, [review_elem.text for review_elem in driver.find_elements_by_xpath("//div[@class='ODSEW-ShBeI-content']")]

def get_info(search_url, debug=False):
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

    followed_suggestion = False

    import pdb;pdb.set_trace()
    for _ in range(MAX_TRIES):
        time.sleep(DELAY)
        scroll_to_bottom(driver)
        if check_redirected(driver) and check_identifiers_loaded(driver):
            labels = labels_response(get_panel_text(driver), get_category(driver), followed_suggestion)
            reviews = reviews_response(search_url, get_reviews(driver))
            driver.quit()
            return gmaps_reponse(labels, reviews)
        elif not check_redirected(driver) and check_suggestion_available(driver):
            driver.get(get_first_suggestion(driver))
            followed_suggestion = True

    labels = labels_not_found(search_url) if followed_suggestion else name_not_found(search_url)
    reviews = reviews_response(search_url, get_reviews(driver)) if check_redirected(driver) else no_reviews_response("name_not_found", search_url)
    driver.quit()
    
    return gmaps_reponse(labels, reviews)