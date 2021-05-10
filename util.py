from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os

def not_found_response(error_type, url):
    """Auxilary function for generating an error response. This function should not be exported. Use name_not_found orlabels_not_fund instead
    """
    return {
        "success": False, 
        "error_type": error_type,
        "url": url,
        "lgbtq": None, 
        "veteran": None, 
        "women": None, 
        "black": None
    }

def labels_response(panel_text):
    return {
        "success": True,
        "error_type": None,
        "url": None,
        "lgbtq": bool("LGBTQ friendly" in panel_text),
        "veteran": bool("Identifies as veteran-led" in panel_text),
        "women": bool("Identifies as women-led" in panel_text),
        "black": bool("Identifies as Black-owned" in panel_text),
    }

def name_not_found(url):
    return not_found_response("missing_name", url)

def labels_not_found(url):
    return not_found_response("missing_labels", url)

def get_driver(debug=False):
    """Get new driver to run scraper
    Note: Chrome does not work headless

    Args:
        debug (bool, optional): If false run headless. Defaults to False.

    Returns:
        selenium.webdriver.Firefox:
    """
    options = webdriver.FirefoxOptions()
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
