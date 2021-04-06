import pandas as pd
from urllib.request import urlopen
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time


def init_webdriver():
    # configuring the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless') 
    options.add_argument('--lang=en_US')  # needs this if not headless will not work 
    options.add_argument("--height=1000")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


def scroll_down(driver):
    # from https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_number_of_businesses(driver): 
    return int(driver.find_element_by_class_name('_3tWAU').text.split()[0])


def get_city(city_url, city_name):
    driver = init_webdriver()
    driver.get(city_url)    
    scroll_down(driver)
    time.sleep(3)
    business_cards = driver.find_elements_by_class_name("_4ZzO0")
    if len(business_cards) < get_number_of_businesses(driver):
        print('something wrong, not enough business cards!')
        return
    
    business_directory = pd.DataFrame(columns=["business_name", "address", "business_type", "website", "city_name"])
    for card in business_cards:
        business_name = card.find_element_by_class_name('_29upa').text
        address = card.find_element_by_class_name('_3ytiC').text
        business_type = card.find_element_by_class_name('_2PVWy').text
        website = card.find_element_by_tag_name('a').get_attribute('href')
        business_dict = {"business_name": business_name, "address": address, "business_type": business_type, "website":website, "city_name":city_name}
        business_directory = business_directory.append(business_dict, ignore_index=True)
    
    driver.close()
    return business_directory


city_url = 'https://byblack.us/search/Atlanta--GA/businesses/?query='
city_name = 'Atlanta, GA'
atl_directory = get_city(city_url, city_name)
print(atl_directory)
