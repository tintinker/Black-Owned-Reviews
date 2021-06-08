import os
from selenium import webdriver
import logging

log = logging.getLogger(__name__)

def gmaps_reponse(labels_response, reviews_response):
    return {
        "labels": labels_response,
        "reviews": reviews_response
    }

def flatten_gmaps_response(response):
    flattened = {}
    for key in response["labels"]:
        flattened[f"labels_{key}"] = response["labels"][key]
    for key in response["reviews"]:
        flattened[f"reviews_{key}"] = response["reviews"][key]
    return flattened

def not_found_response(error_type, followed_suggestion, url):
    """Auxilary function for generating an error response. This function should not be exported. Use name_not_found orlabels_not_fund instead
    """
    return {
        "success": False, 
        "error_type": error_type,
        "url": url,
        "category": None,
        "followed_suggestion": followed_suggestion,
        "lgbtq": None, 
        "veteran": None, 
        "women": None, 
        "black": None
    }

def labels_response(panel_text, category, followed_suggestion):
    return {
        "success": True,
        "error_type": None,
        "url": None,
        "category": category,
        "followed_suggestion": followed_suggestion,
        "lgbtq": bool("LGBTQ friendly" in panel_text),
        "veteran": bool("Identifies as veteran-led" in panel_text),
        "women": bool("Identifies as women-led" in panel_text),
        "black": bool("Identifies as Black-owned" in panel_text),
    }

def reviews_response(search_url, review_tuple):
    avg_rating, num_ratings, text_list =  review_tuple

    if avg_rating is None or num_ratings is None:
        return no_reviews_response("review_link_not_found", search_url)
    if avg_rating < 0 or num_ratings < 0:
        return no_reviews_response("summary_not_found", search_url)

    return {
        "success": True,
        "error_type": None,
        "url": None,
        "avg_rating": avg_rating,
        "num_ratings": num_ratings,
        "text_list": text_list
    }

def no_reviews_response(error_type, search_url):
    return {
        "success": True,
        "error_type": error_type,
        "url": search_url,
        "avg_rating": None,
        "num_ratings": None,
        "text_list": None
    }

def name_not_found(url):
    return not_found_response("missing_name", False, url)

def labels_not_found(url):
    return not_found_response("missing_labels", True, url)

def get_range():
    try:
        if os.getenv("USE_RANGE", 'False').lower() in ('true', '1', 't'):
            return int(os.getenv("RANGE_START", -1)), int(os.getenv("RANGE_END", -1))
        return -1,-1
    except:
        return -1,-1

def running_on_ec2():
    log.debug("Check running on ec2")
    return os.getenv("RUN_ENVIRONMENT").lower() == "ec2"

def get_driver(debug=False):
    """Get new driver to run scraper
    Note: Chrome does not work headless

    Args:
        debug (bool, optional): If false run headless. Defaults to False.

    Returns:
        selenium.webdriver.Firefox:
    """
    options = webdriver.FirefoxOptions()
    if running_on_ec2():
        log.debug(f"Running on ec2")
        options.binary_location = '/home/ec2-user/firefox/firefox'
    options.add_argument('--log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--no-sandbox')
    options.add_argument('--enable-automation')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--dns-prefetch-disable')    
    options.add_argument('--hide-scrollbars')

    if not debug:
        options.add_argument('--headless')

    return webdriver.Firefox(executable_path=os.getenv('FIREFOX_DRIVER'), options=options)
