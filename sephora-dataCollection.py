# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 21:27:57 2018

@author: Yingqi Li
"""
import urllib
from urllib.request import urlretrieve, Request, urlopen
import datetime
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
import csv

path = "https://www.sephora.com/brand/list.jsp"

def requests_bs(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',}
    req = requests.get(url,headers=headers)
    bsobj = BeautifulSoup(req.text, 'html.parser')
    return bsobj


def get_ori_url(url):
    bsobj = requests_bs(url)
    raws = bsobj.select('a.u-hoverRed.u-db.u-p1')
    hrefs = []
    names = []
    for raw in raws:
        hrefs.append(raw.get('href'))
        names.append(raw.get_text())
    return hrefs, names

def get_brand_url(oris):
    brand_home_urls = []
    for url in oris:
        brand_home_urls.append('https://www.sephora.com' + url + '?products=all&pageSize=-1')
    return brand_home_urls

def get_product_links(bsobj):
    #
    raws = bsobj.select('a.u-size1of4.SkuItem.SkuItem--135')
    urls = []
    i=0
    ######################################################################################3
    for raw in raws:
        urls.append(raw.get('href'))
        print('prosesing {} of {}'.format(i,len(raws)))
        i = i+1
        time.sleep(1)
    return urls

def get_product_detail(bsobj):
    # get brand_name
    if bsobj.select('title') != []:
        title = bsobj.select('title')[0]
        title = title.get_text()
        title = title.replace(' | Sephora','')
        r_title = title.split(' - ')
        if len(r_title) >= 2:
            brand_name = r_title[1].strip()
            product_name = r_title[0].strip()
        else:
            brand_name = ''
            product_name = ''
    else:
        brand_name = ''
        product_name = ''
    return brand_name, product_name

def get_product_price(bsobj):
    #price = bsobj.select('css-18suhml')[0]
    price = bsobj.find_all('div',{'data-comp':'Price Box'})
    if price != []:
        price = price[0].get_text()
    else:
        price = ''
    return price

def get_product_image_url(bsobj):
    product_image_url = bsobj.find_all('image',{'style':'mask: url(#heroHoverMediaMask)'})
    if product_image_url != []:

        product_image_url = product_image_url[0].get('xlink:href')
        product_image_url = 'https://www.sephora.com' + product_image_url
    else:
        product_image_url = ''
    return product_image_url

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 10:
            print("Timing out after 5 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

def writecsv(file,row):
    with open(file,'a+',encoding='utf_8_sig',newline='') as file:
        w = csv.writer(file)
        w.writerow(row)

if __name__ == '__main__':
    oris, urlnames = get_ori_url(path)
    brand_urls = get_brand_url(oris)

    for brand_url in brand_urls[59:]:
        driver = webdriver.PhantomJS(executable_path=r'C:\Users\wolu0\Downloads\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs')
        driver.get(brand_url)
        waitForLoad(driver)
        html = driver.page_source
        bsobj_0 = BeautifulSoup(html, 'html.parser')
        product_links = get_product_links(bsobj_0)
        time.sleep(5)
        for product_link in product_links:
            product_link = 'https://www.sephora.com' + product_link
            print("processing {}".format(product_link))
            driver = webdriver.PhantomJS(executable_path=r'C:\Users\wolu0\Downloads\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs')
            driver.get(product_link)
            waitForLoad(driver)
            html = driver.page_source
            bsobj = BeautifulSoup(html, 'html.parser')
            brand_name, product_name = get_product_detail(bsobj)
            price = get_product_price(bsobj)
            product_image_url = get_product_image_url(bsobj)
            print(brand_name,product_name,price,product_image_url)
            result = [brand_name,product_name,price,'',product_image_url, product_link]
            writecsv('Sephora_new2.csv',result)
#
