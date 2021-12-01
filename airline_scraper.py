from __future__ import annotations
from datetime import date
import json
from streamlit.elements.button import ButtonMixin
from streamlit.type_util import Key
import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import random
from abc import ABC, abstractmethod
from typing import Any, Optional
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import time as time2
from webdriver_manager.chrome import ChromeDriverManager
from typing import Any, Optional

with open('final_search_list2.json', 'r') as myfile:
    pstate=myfile.read()
fstate = json.loads(pstate) 
myfile.close()

def get_min_data(soup):
    data={}
    data['data']= []
    flight= soup.find('div',{'class': 'inner-grid keel-grid'})
    obd_time = flight.find_all("span", {"class": "depart-time base-time"})[0].text +flight.findAll("span", {"class": "time-meridiem meridiem"})[0].text
    oba_time= flight.find_all("span", {"class": "arrival-time base-time"})[0].text + flight.findAll("span", {"class": "time-meridiem meridiem"})[1].text
    ibd_time = flight.find_all("span", {"class": "depart-time base-time"})[1].text +flight.findAll("span", {"class": "time-meridiem meridiem"})[2].text
    iba_time= flight.find_all("span", {"class": "arrival-time base-time"})[1].text + flight.findAll("span", {"class": "time-meridiem meridiem"})[3].text
    airlines=flight.find_all("div", {"class": "bottom"})
    ob_airlines=airlines[0].text.replace("\n", "")
    ib_airlines=airlines[3].text.replace("\n", "")
    flight_len= flight.find_all("div", {"class": "section duration allow-multi-modal-icons"})
    obfl= flight_len[0].find("div", {"class": "top"}).text.replace("\n", "")
    ibfl= flight_len[1].find("div", {"class": "top"}).text.replace("\n", "")
    ob_stops=flight.findAll("span", {"class": "stops-text"})[0].text.replace("\n", "")
    ib_stops=flight.findAll("span", {"class": "stops-text"})[1].text.replace("\n", "")
    price=flight.find("span", {"class": "price-text"}).text.replace("\n", "")
    flighturl='kayak.com'+flight.find('a').get('href')
    if 'pm' in obd_time and 'am' in oba_time:
        ob_xd='+1'
    else:
        ob_xd= None
    if 'pm' in ibd_time and 'am' in iba_time:
        ib_xd='+1'
    else:
        ib_xd= None
    
    data['data'].append({
        'ob_carrier':ob_airlines,
        'ib_carrier':ib_airlines,
        'obd_time':obd_time,
        'oba_time':oba_time,
        'ibd_time':ibd_time,
        'iba_time':iba_time,
        'flighturl': flighturl,
        'obfl': obfl,
        'ibfl': ibfl,
        'ob_stops':ob_stops,
        'ib_stops':ib_stops,
        'flighturl': flighturl,
        'ob_xd': ob_xd,
        'ib_xd':ib_xd,
        'price': price,
    })
    return data

def get_info(home_port, dest_port, home_date, dest_date):
    PATH=r"C:\Users\frank\anaconda3\Lib\chromedriver.exe"
    rint= random.randint(0,10)
    ipad= free_proxies[rint]['IP Address']
    port= free_proxies[rint]['Port']
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = f"http://{ipad}:{port}"
    prox.https_proxy = f"https://{ipad}:{port}"
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)
    driver = webdriver.Chrome(desired_capabilities=capabilities)
    scrape_url= 'https://www.kayak.com/flights/'+home_port+"-"+dest_port+'/'+home_date+'/'+dest_date+'?sort=price_a'
    driver.get(scrape_url)
    time2.sleep(random.randint(22,33))
    html_from_page = driver.page_source
    driver.close() 
    soup = BeautifulSoup(html_from_page)
    return soup

def get_free_proxies(driver):
    driver.get('https://sslproxies.org')

    table = driver.find_element(By.TAG_NAME, 'table')
    thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
    tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tbody:
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, 'td')
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)
    
    return proxies
    
PATH=r"C:\Users\frank\anaconda3\Lib\chromedriver.exe"
driver = webdriver.Chrome(ChromeDriverManager().install())
free_proxies = get_free_proxies(driver)
rint= random.randint(0,9)
ipad= free_proxies[rint]['IP Address']
port= free_proxies[rint]['Port']
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = f"http://{ipad}:{port}"
prox.https_proxy = f"https://{ipad}:{port}"
capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

class search():
    singleton_instance = None              
    singleton_instance_count=0
    def __new__(cls, *args, **kwargs):     #initiates the simpleton object
        if cls.singleton_instance_count<=1:
            cls.singleton_instance_count+=1
            cls.singleton_instance = super(search, cls).__new__(
                                cls, *args, **kwargs)
    def search_flights(): #searches flights
        data={}
        data['data']= []
        search_list=['LAX', 'DTW', 'MSY', 'MIA', 'SEA']
        date_list=['2022-03-01', '2022-03-02', '2022-03-03','2022-03-04','2022-03-05','2022-03-06']
        s=0
        for s_item in search_list:
            for item in fstate['data']:
                for d_item in date_list:
                    try:
                        if s_item==item['FAA']:
                            continue
                        if (s %15 == 0) & (s != 0):
                            driver = webdriver.Chrome(desired_capabilities=capabilities)
                            free_proxies = get_free_proxies(driver)
                            time2.sleep(2)
                        flight_quote= get_info(s_item, item['FAA'], "2022-02-26", d_item)
                        parsequote=get_min_data(flight_quote)
                        parsequote['data'][0]['ib']=item['FAA']
                        parsequote['data'][0]['ob']=s_item
                        parsequote['data'][0]['date']=d_item
                        parsequote['data'][0]['Continent']=item['Continent']
                        parsequote['data'][0]['Country']=item['Country']
                        parsequote['data'][0]['City']=item['City']
                        data['data'].append(parsequote['data'][0])
                        print(parsequote)
                        time2.sleep(random.randint(20,30))
                        s+=1
                    except:
                        print('errored out on ', s_item,' ', item['FAA'], ' ',d_item)
                        time2.sleep(random.randint(20,30))
        dataf = open("final_search_list2.json", "w")
        json.dump(data, dataf)
        dataf.close()
        return "Finished!"