# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import logging
import traceback
import argparse


GM_WEBPAGE = 'https://www.google.com/maps/'
MAX_WAIT = 10
MAX_RETRY = 5
MAX_SCROLLS = 40

def get_driver(debug=True):
        options = Options()

        if not debug:
            options.add_argument("--headless")
        else:
            options.add_argument("--window-size=1366,768")

        options.add_argument("--disable-notifications")
        options.add_argument("--lang=en-GB")
        input_driver = webdriver.Chrome(chrome_options=options)

        return input_driver

def get_business_urls(search_url, outputfile="urls.txt", debug=True):
    with open(outputfile, 'w') as f:
        driver = get_driver()
        driver.get(search_url)
        wait = WebDriverWait(driver, MAX_WAIT)
        links = driver.find_elements_by_xpath('//div[@class=\'section-result\']')
        for i in range(1, len(links)+1):
            item = wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[@data-result-index=\'{i}\']')))
            item.click()
            time.sleep(2)  
            try:
                item = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@jsaction=\'pane.rating.moreReviews\']')))
                item.click()   
            except:
                item = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@jsaction=\'pane.place.backToList\']')))
                item.click() 
                time.sleep(3) 
                continue
            time.sleep(2)  
            
            print(driver.current_url, file=f)
            
            if debug:
                print("Found business",driver.current_url)
            
            
            item = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label=\'Back\']'))) 
            item.click()  
            time.sleep(2)  
            item = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@jsaction=\'pane.place.backToList\']')))
            item.click() 
            time.sleep(3)  


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps Search URL scraper.')
    parser.add_argument('--u', type=str, required=True, help='Search URL, ex. https://www.google.com/maps/search/black+owned+business/@42.2534104,-83.8367374,11z/data=!3m1!4b1?hl=en')
    parser.add_argument('--o', type=str, default='urls.txt', help='output URLs file')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run scraper using browser graphical interface')
    parser.set_defaults(debug=True)
    args = parser.parse_args()
    get_business_urls(args.u, args.o, args.debug)
