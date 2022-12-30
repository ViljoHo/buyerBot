
from cgi import test
from operator import imod
import os
import ownSecrets
from timeit import repeat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import json

#Dictionary import from json file
with open("BRANDS_AND_MODELS.json", 'r+') as file:
        BRANDS_AND_MODELS = json.load(file)




driver = webdriver.Chrome("C:\SeleniumDrivers\chromedriver.exe")
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, )

interesting_cars_urls = [] #List of all cars
prices = [] #

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
    driver.maximize_window()
    driver.implicitly_wait(5)

    #accept cookies
    cookies = driver.find_element(By.XPATH, "/html/body/reach-portal/div[2]/div/div/div/div/div/div[3]/div/button[1]")
    cookies.click()

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
    brand = brand_and_model.split()[0]
    model = brand_and_model.split()[1]          #.lower()
    

    info_boxes.clear()

    return brand, model, annual_model, kilometers    



#Function which calculates price of each car based on nettiautos data
def optimal_price_calculator(brand, model, annual_model, kilometers):
    brand_value = BRANDS_AND_MODELS[brand]["brand_int"]
    model_value = BRANDS_AND_MODELS[brand][model]
    kilometersFrom = kilometers - 50000
    kilometersTo = kilometers + 50000

    myToken = ownSecrets.get('myToken')
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
    print("Average prices for similar cars: {average_price:.2f}".format(average_price = average_price))
    print()
    print("*" * 50)
    print()
    print("The cheapest similar car: {cheapest_price:.2f}".format(cheapest_price = cheapest_price))
    print()
    print("*" * 50)
    print()
    print("The bot would buy a car for: {optimal_price:.2f}".format(optimal_price = optimal_price))
    print()
    print("*" * 50)

def testi():
    print(BRANDS_AND_MODELS)
    automerkin_arvo = BRANDS_AND_MODELS["Ford"]["brand_int"]
    automerkin_mallin_arvo = BRANDS_AND_MODELS["Ford"]["B-Max"]
    print(automerkin_arvo)
    print(automerkin_mallin_arvo)
    

def main():
    #testi()
    brand, model, annual_model, kilometers = info_collector_newest_ad()
    #info_collector_newest_ad()
    optimal_price_calculator(brand, model, annual_model, kilometers)

    driver.quit()

if __name__ == "__main__":
    main()







