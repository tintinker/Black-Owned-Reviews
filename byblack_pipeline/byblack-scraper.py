import pandas as pd
from bs4 import BeautifulSoup
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


def get_city(city_url, city_name):
    driver = init_webdriver()
    driver.get(city_url)    
    i=1
    more_to_scroll = True
    while more_to_scroll:
        driver.execute_script("window.scrollTo(0, 1000*{i});".format(i=i))  
        i += 1
        time.sleep(3)
        if 1500 * i > driver.execute_script("return document.body.scrollHeight;"):
            more_to_scroll = False
    
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    business_cards = soup.find_all('div', class_="_4ZzO0")
    business_directory = pd.DataFrame(columns=["business_name", "address", "business_type", "website", "city_name"])
    for card in business_cards:
        business_name = ""
        if card.find(class_="_29upa") is not None:
            business_name = card.find(class_="_29upa").text
        elif card.find(class_="u1r86") is not None:
            business_name = card.find(class_="u1r86").text
        address = card.find(class_="_3ytiC").find_all('div')[-1].text
        business_type = card.find(class_="_2PVWy").text
        website = card.a.get('href')
        business_dict = {"business_name": business_name, "address": address, "business_type": business_type, "website":website, "city_name":city_name}
        business_directory = business_directory.append(business_dict, ignore_index=True)
    return business_directory


city_url = 'https://byblack.us/search/Atlanta--GA/businesses/?query='
city_name = 'Atlanta, GA'
atl_directory = get_city(city_url, city_name)
print(atl_directory)
