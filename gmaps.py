"""
labels.py
Scraper to extract labels from gmaps entry 
@author Justin Tinker (jatinker@stanford.edu)
"""
# -*- coding: utf-8 -*-
import json
from jsonparsers import parse_place, parse_response
from util import submit_followed_suggestion, submit_place_data, submit_review_summaries, submit_reviews, get_driver
import time
import logging
from selenium.common.exceptions import TimeoutException
from random import randrange

log = logging.getLogger(__name__)

MAX_REVIEWS = 100

MIN_CLICK_DELAY = 10
def random_click_delay():
    return MIN_CLICK_DELAY + randrange(0, 15)

REDIRECT_MAX_TRIES = 3
MIN_REDIRECT_DELAY = 10
def random_redirect_delay():
    return MIN_REDIRECT_DELAY + randrange(0, 15)

PLACE_MAX_TRIES = 4 #number of times to look for indicators that label information has loaded
MIN_PLACE_DELAY = 5 #number of seconds to wait between tries
def random_place_delay():
    return MIN_PLACE_DELAY + randrange(0, 15)

MIN_REVIEWS_DELAY = 5
def random_reviews_delay():
    return MIN_REVIEWS_DELAY + randrange(0, 15)

REVIEWS_MAX_TRIES = 5

PLACE_API_IDENTIFIER = "maps/preview/place"
REVIEW_API_IDENTIFIER = "maps/preview/review/listentitiesreviews"
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
    ad = len(list(driver.find_elements_by_xpath("//div[contains(@aria-label,'Results') and //span[. = ' Ad ']]"))) > 0
    for elem in driver.find_elements_by_xpath("//div[contains(@aria-label,'Results')]//a[@href]"):
        if PLACE_URL_IDENTIFIER in str(elem.get_attribute("href")):
            return str(elem.get_attribute("href")), ad
    return None, ad

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

def check_new_review_api_call(driver, prev_api_calls):
    for _ in range(REVIEWS_MAX_TRIES):
        for req in driver.requests:
            if req and req.response and req.response.headers['Content-Type'].startswith("application/json") and REVIEW_API_IDENTIFIER in req.url and req.url not in prev_api_calls:
                prev_api_calls.add(req.url)
                return req.url
        time.sleep(random_reviews_delay())
    return None

def check_place_api_call(driver):
    for _ in range(PLACE_MAX_TRIES):
        for req in driver.requests:
            if req and req.response and req.response.headers['Content-Type'].startswith("application/json") and "maps/preview/place" in req.url:
                return req.url
        time.sleep(random_place_delay())
    return None

def wait_for_new_reviews(driver, prev_num, max_num, prev_api_calls):
    if prev_num >= MAX_REVIEWS or prev_num >= max_num:
        return None

    scroll_to_bottom_reviews(driver)
    try:
        request_url = check_new_review_api_call(driver, prev_api_calls)
        return request_url
    except TimeoutException:
        return None

def get_reviews(cursor, url_id, driver):
    (avg_rating, num_ratings) = -1, -1
    default_labels = {"black": False, "women": False, "lgbtq": False, "veteran": False}
    place_data = ([], default_labels, [])
    current_num_reviews = 0
    print("set defaults")
    log.info("set defaults")

    def try_click(xpath_selector):
        elems = driver.find_elements_by_xpath(xpath_selector)
        if len(elems) > 0:
            try:
                elems[0].click()
                return True
            except:
                return False
        print("fail",  xpath_selector)
        return False
    
    if not try_click("//div[@jsaction='pane.reviewChart.moreReviews']"):
        print("more reviews click failed")
        log.info("more reviews click failed")

        return (avg_rating, num_ratings, current_num_reviews), place_data
    
    time.sleep(random_click_delay())

    if not try_click("//img[@alt='Sort']"):
        print("sort click failed")
        log.info("sort click failed")
        return (avg_rating, num_ratings, current_num_reviews), place_data

    time.sleep(random_click_delay())

    if not try_click("//li[@class='nbpPqf-menu-x3Eknd' and div/div[. = 'Newest']]"):
        print("newestt click failed")
        log.info("newestt click failed")
        return (avg_rating, num_ratings, current_num_reviews), place_data

    time.sleep(random_click_delay())

    print("all sort clicks succeeded")
    log.info("all sort clicks succeeded")

    avg_rev_elems = driver.find_elements_by_xpath("//div[@class='gm2-display-2']")
    try:
        avg_rating = float(avg_rev_elems[0].text) if len(avg_rev_elems) > 0 else -1
        print(f"got avg rating: {avg_rating}")
        log.info(f"got avg rating: {avg_rating}")

    except:
        avg_rating = -1

    total_rev_elems = driver.find_elements_by_xpath("//div[@class='gm2-caption']")
    try:
        valid_total_counts = [float(e.text.strip()[:-len(" reviews")].replace(",","")) for e in total_rev_elems if e.text.strip().endswith(" reviews")]
        num_ratings = valid_total_counts[0] if len(valid_total_counts) > 0 else -1
        print(f"got num ratings: {num_ratings}")
        log.info(f"got num ratings: {num_ratings}")

    except:
        num_ratings = -1
    
    place_api_url = check_place_api_call(driver)
    if place_api_url:
        print("found place api url")
        log.info("found place api url")
        place_data = parse_place(parse_response(place_api_url))
    else:
        print("did not find place api url")
        log.info("did not find place api url")
        return (avg_rating, num_ratings, current_num_reviews), place_data
    
    if avg_rating < 0 or num_ratings < 0:
        print("0 check failed")
        log.info("0 check failed")
        return (avg_rating, num_ratings, current_num_reviews), place_data

    prev_api_calls = set()

    while True:
        review_api_url = wait_for_new_reviews(driver, current_num_reviews, num_ratings, prev_api_calls)
        if not review_api_url:
            break
        current_num_reviews += submit_reviews(cursor, url_id, review_api_url)

    print("got all reviews needed")
    log.info("got all reviews needed")

    return (avg_rating, num_ratings, current_num_reviews), place_data





def get_info(cursor, search_url, url_id,  debug=False):
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
    print(f"got search url id: {url_id}")
    log.info(f"got search url id: {url_id}")

    for _ in range(REDIRECT_MAX_TRIES):
        time.sleep(random_redirect_delay())
        scroll_to_bottom(driver)

        if check_redirected(driver) and check_identifiers_loaded(driver):
            print("redirected and identifiers loaded")
            log.info("redirected and identifiers loaded")
            reviews_summary, place_data = get_reviews(cursor, url_id, driver)
            submit_review_summaries(cursor, url_id, reviews_summary)
            submit_place_data(cursor, url_id, place_data)
            break
        
        elif not check_redirected(driver) and check_suggestion_available(driver):
            print("suggestion available")
            log.info("suggestion available")
            suggestion, ad = get_first_suggestion(driver)
            
            if suggestion:
                driver.get(suggestion)
                submit_followed_suggestion(cursor, url_id, ad)
            else:
                continue
    print("quitting")
    log.info("quitting")
    driver.quit()