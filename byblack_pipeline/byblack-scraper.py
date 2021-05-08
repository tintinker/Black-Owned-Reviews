import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time


def init_webdriver():
    # configuring the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless') 
    options.add_argument('--lang=en_US')  # needs this if not headless will not work 
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
    
    business_directory = pd.DataFrame(columns=["business_name", "address", "zipcode", "business_type", "website", "city_name"])
    driver.implicitly_wait(5)
    for card in business_cards:
        business_name, address, zipcode, business_type, website = "", "", "", "", ""
        try: 
            business_name = card.find_element_by_class_name('_29upa').text
            address = card.find_element_by_class_name('_3ytiC').text.split('\n')[-1]
            zipcode = address.split(', ')[-1]
            business_type = card.find_element_by_class_name('_2PVWy').text
            website = card.find_element_by_link_text('Visit Website').get_attribute('href')
        except NoSuchElementException:
            pass        
        business_dict = {"business_name": business_name, "address": address, "zipcode": zipcode, "business_type": business_type, "website":website, "city_name":city_name}
        business_directory = business_directory.append(business_dict, ignore_index=True)
    driver.close()
    return business_directory

 
biz_directory = get_city('https://byblack.us/search/Atlanta--GA/businesses/?query=', 'Atlanta')
biz_directory = biz_directory.append(get_city('https://byblack.us/search/New-York--NY/businesses/?query=', 'New York'))
biz_directory = biz_directory.append(get_city('https://byblack.us/search/San-Francisco--CA/businesses/?query=', 'San Francisco'))
biz_directory = biz_directory.append(get_city('https://byblack.us/search/Chicago--IL/businesses/?query=', 'Chicago'))
biz_directory.reset_index(drop=True, inplace=True)
biz_directory.to_csv('byblack_directory.csv')
