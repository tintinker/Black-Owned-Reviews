from jsonparsers import parse_response, parse_review_list
import os
from seleniumwire import webdriver
import logging
import psycopg2


log = logging.getLogger(__name__)
MAX_REVIEW_TEXT_LENGTH = 1250

def get_db_connection():
    conn = psycopg2.connect(os.getenv("DB_CONNECTION_STRING"))
    conn.autocommit = True
    return conn


def check_cache(cursor, url_id):
    try:
        cursor.execute("SELECT * from cache WHERE url_id = %s", (url_id,))
        if cursor.fetchone() is not None:
            return True
    except psycopg2.Error as e:
        log.error(f"DB Error checking cache: {e}")
    return False

def save_cache(cursor, url_id):
    try:
        cursor.execute(f"INSERT INTO cache(url_id) VALUES (%s)", (url_id,))
    except psycopg2.Error as e:
        log.error(f"DB Error inserting into cache: {e}")

def submit_place_data(cursor, search_url_id, place_data_tuple):
    (tags, labels, descriptors) = place_data_tuple
    try:
        cursor.execute(f"INSERT INTO tags(url_id, tags) VALUES (%s,%s)",(search_url_id,tags))
    except psycopg2.Error as e:
        log.error(f"DB Error inserting place data tags: {e}")
    try:
        cursor.execute(f"INSERT INTO labels(url_id, black, women, lgbtq, veteran) VALUES (%s,%s,%s,%s,%s)", (search_url_id,labels['black'],labels['women'],labels['lgbtq'],labels['veteran']))
    except psycopg2.Error as e:
        log.error(f"DB Error inserting place data labels: {e}")
    try:
        cursor.execute(f"INSERT INTO descriptors(url_id, descriptors) VALUES (%s,%s)",(search_url_id,descriptors))
    except psycopg2.Error as e:
        log.error(f"DB Error inserting place data descriptors: {e}")

def submit_review_summaries(cursor, search_url_id, review_summary_tuple):
    (avg_rating, num_ratings, num_downloaded) = review_summary_tuple
    try:
        cursor.execute(f"INSERT INTO review_summary(url_id, avg_rating, num_reviews, num_downloaded_reviews) VALUES (%s,%s,%s,%s)",(search_url_id,avg_rating,num_ratings,num_downloaded))
    except psycopg2.Error as e:
        log.error(f"DB Error inserting review summary data: {e}")

def trunc_text(text, max_length):
    if text and type(text) is str:
        return text[:max_length]
    return text
def submit_reviews(cursor, search_url_id, request_url):
    review_list = parse_review_list(parse_response(request_url))
    review_tuples =  [(search_url_id, r["author_id"], r["author_name"], r["timeframe"], trunc_text(r["text"], MAX_REVIEW_TEXT_LENGTH),r["rating"]) for r in review_list]
    args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s)", t).decode("utf-8") for t in review_tuples)
    try:
        cursor.execute("INSERT INTO reviews(shop_url_id, author_id, author_name, timeframe, text, rating) VALUES " + args_str) 
    except psycopg2.Error as e:
        log.error(f"DB Error inserting review data: {e}")
    return len(review_list)

def submit_followed_suggestion(cursor, url_id, was_ad = False):
    try:
        cursor.execute(f"INSERT INTO followed_suggestion(url_id,followed,was_ad) VALUES (%s,%s,%s)",(url_id,True, was_ad))
    except psycopg2.Error as e:
        log.error(f"DB Error inserting into followed_suggestion: {e}")


def get_range():
    try:
        if os.getenv("USE_RANGE", 'False').lower() in ('true', '1', 't'):
            return int(os.getenv("RANGE_START", -1)), int(os.getenv("RANGE_END", -1))
        return -1,-1
    except:
        return -1,-1

def running_on_ec2():
    log.debug("Check running on ec2")
    return os.environ["RUN_ENVIRONMENT"].lower() == "ec2"

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
