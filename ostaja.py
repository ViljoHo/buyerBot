
from cgi import test
import imp
from operator import imod
import os
from timeit import repeat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

BRANDS_AND_MODELS = {
    "alfa-romeo": {"brand_int": 1, 
                    "105": 4507, 
                    "147": 1,},                
    "amc": 89,
    "armstrong-siddeley": 435,
    "aston-martin": 2,
    "audi": {"brand_int": 4, 
                "100": 37, 
                "200": 38,
                "60": 40, 
                "80": 41,
                "90": 42, 
                "a1": 3974,
                "a2": 43, 
                "a3": 44,
                "a4": 45, 
                "a4-allroad": 3961,},
    "austin": 5,
    "bedford": 6,
    "bentley": 7,
    "bmw": {"brand_int": 4, 
                "535": 2995, 
                "200": 38,
                "60": 40, 
                "80": 41,
                "90": 42, 
                "a1": 3974,
                "a2": 43, 
                "a3": 44,
                "a4": 45, 
                "a4-allroad": 3961,},
    "bmw-alpina": 208,
    "borgward": 323,
    "buick": 9,
    "byd": 517,
    "cadillac": 10,
    "chevrolet": 11,
    "chrysler": 12,
    "ford": 23,
    "mercedes-benz": 45,
    "nissan": 55,
    "opel": 57,
    "skoda": 72,
    "toyota": 79,
    "volkswagen": {"brand_int": 84, 
                    "passat": 967, 
                    "200": 38,
                    "60": 40, 
                    "80": 41,
                    "90": 42, 
                    "a1": 3974,
                    "a2": 43, 
                    "a3": 44,
                    "a4": 45, 
                    "a4-allroad": 3961,},
    "volvo": 85,
    "citroen": {"brand_int": 13, 
                    "c3": 1064, 
                    "200": 38,
                    "60": 40, 
                    "80": 41,
                    "90": 42, 
                    "a1": 3974,
                    "a2": 43, 
                    "a3": 44,
                    "a4": 45, 
                    "a4-allroad": 3961,},
    "kia": {"brand_int": 230, 
                    "cerato": 2543, 
                    "200": 38,
                    "60": 40, 
                    "80": 41,
                    "90": 42, 
                    "a1": 3974,
                    "a2": 43, 
                    "a3": 44,
                    "a4": 45, 
                    "a4-allroad": 3961,},
    "ford": {"brand_int": 23, 
                    "mondeo": 323, 
                    "147": 1,},
}




driver = webdriver.Chrome("C:\SeleniumDrivers\chromedriver.exe")
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, )

interesting_cars_urls = [] #List of all cars
prices = [] #ddd

def open_saved_ads():
    #Go through all ads and opens them to the new tabs
    for i in range(len(interesting_cars_urls)):
        url = interesting_cars_urls[i]
        whole_specific_script_url = "window.open(\""+ url + "\""+","+ "\"" + "_blank" + "\"" +");"
        driver.execute_script(whole_specific_script_url)

#Function which collects all information from cars
def info_collector_newest_ad():
    #Go to huutokaupat.com and clicks newest ad in the page
    driver.get("https://huutokaupat.com/nettihuutokaupat/14/henkiloautot?jarjestys=uusimmat&tyyppi=kaikki")
    #driver.get("https://huutokaupat.com/3665129/volkswagen-golf-2009")
    driver.implicitly_wait(4)
    newest_ad = driver.find_element(By.CLASS_NAME, "forge-lineclamp")
    newest_ad.click()
    driver.forward()
    driver.implicitly_wait(4)

    

    #Adds url of ad to the list
    current_url = driver.current_url
    interesting_cars_urls.append(current_url)

    #Lists all dd tag elements 
    info_boxes = WebDriverWait(driver, 4, ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, "dd"))) 
    
    #Go through dd tags and adds all of them to the list (except empty ones)
    cars_informations = []
    for i in range(len(info_boxes)):
        content = info_boxes[i].text
        if content.strip():
            #print(f"{content}")
            cars_informations.append(content)

    #Take all necessary information from ad
    brand_and_model = cars_informations[0]
    annual_model = int(cars_informations[2])
    kilometers = cars_informations[4].split()
    kilometers.pop(-1)
    kilometers = int("".join(kilometers))
    #separate brand and model from the add
    brand = brand_and_model.split()[0].lower()
    model = brand_and_model.split()[1].lower()
    

    info_boxes.clear()

    return brand, model, annual_model, kilometers    



#Function which calculates price of each car based on nettiautos data
def optimal_price_calculator(brand, model, annual_model, kilometers):
    brand_value = BRANDS_AND_MODELS[brand]["brand_int"]
    model_value = BRANDS_AND_MODELS[brand][model]
    kilometersFrom = kilometers - 50000
    kilometersTo = kilometers + 50000

    myToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6ImJlNGFhMGY5YjEwZDU5N2M1NjU1MWFmMDc1N2NmNTE1NDIxYzMyZWMiLCJqdGkiOiJiZTRhYTBmOWIxMGQ1OTdjNTY1NTFhZjA3NTdjZjUxNTQyMWMzMmVjIiwiaXNzIjoiIiwiYXVkIjoiYW5vbnltb3VzIiwic3ViIjoiVmlsam9Ib2xtYSIsImV4cCI6MTY2MzAwNTU2NiwiaWF0IjoxNjYzMDAxOTY2LCJ0b2tlbl90eXBlIjoiYmVhcmVyIiwic2NvcGUiOiJyZWFkIHdyaXRlLXVzZXIiLCJ1c2VyX2dyb3VwIjoidXNlciIsImVtYWlsIjoidmlra2UwMEBob3RtYWlsLmNvbSIsIm5hbWUiOiJWaWxqbyBIb2xtYSIsIm5ldHRpeF9pZCI6MTEzNTM3Mn0.gHvGqoyyBLO2TDFTCDKjDFofJ_TONdest-ZPndmEbuwITmbF4PY2YAy07fPgciGLsVrVwmm5FiKa5NMHqHQYmfujHih8k_SR5uDerd-kLb6dz45XuPObCxuuFL_MAwfhuibqKGRBWl66QTbPmkTSRasyVDWxasgwYjLF4VsBH8nfo_nqzXffghzEdoOXgObLoc936BPQLRmmALeorb-tkRsrCIzorK0C5PVDVHBlUrb7Z4dasnRQXvhfrGanJRlSGmKcQJSVXZ0Qx7aZlhfmbLaRazCmn6CKk89yQr35ZTBrxEjvUY3w4JhnlEUpkJwbyt0sF8DeDDwKDxxpta6whg'
    myUrl = 'https://api.nettix.fi/rest/car/search'
    headers = { 'X-Access-Token': myToken }
    response = requests.get(myUrl, headers=headers, params={'make': brand_value, 'model': model_value, 'yearFrom': annual_model, 'yearTo': annual_model, 'kilometersFrom': kilometersFrom, 'kilometersTo': kilometersTo })
    data_json = response.text

    data = json.loads(data_json)


    cheapest_price = data[0]['price']

    sum = 0
    for i in range(len(data)):
        sum += data[i]['price']
        #print(data[i]['price'])

    average_price = sum / len(data)
    optimal_price = (average_price + cheapest_price) / 2 * 0.6

    print()
    print("*" * 50)
    print()
    print("Vastaavanlaisten autojen hintojen keskiarvo: {average_price:.2f}".format(average_price = average_price))
    print()
    print("*" * 50)
    print()
    print("Halvin samanlainen auto: {cheapest_price:.2f}".format(cheapest_price = cheapest_price))
    print()
    print("*" * 50)
    print()
    print("Botti ostaisi auton hinnalla: {optimal_price:.2f}".format(optimal_price = optimal_price))
    print()
    print("*" * 50)

def testi():
    automerkin_arvo = BRANDS_AND_MODELS["audi"]["brand_int"]
    automerkin_mallin_arvo = BRANDS_AND_MODELS["audi"]["a1"]
    print(automerkin_arvo)
    print(automerkin_mallin_arvo)
    


#testi()
brand, model, annual_model, kilometers = info_collector_newest_ad()
#info_collector_newest_ad()
optimal_price_calculator(brand, model, annual_model, kilometers)

#driver.quit()






