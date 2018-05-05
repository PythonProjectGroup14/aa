# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 21:27:57 2018

@author: Yingqi Li
"""
import csv
import requests
from bs4 import BeautifulSoup

#The address of the Belk website used to do the web scraping
path = "https://www.belk.com/beauty/"

#Return the beautifulsoup object
def requests_bs(url):
    req = requests.get(url)
    bsobj = BeautifulSoup(req.text, 'html.parser')
    return bsobj

#Get the original hrl used to do scraping
def ori_url(url):
    bsobj = requests_bs(url)
    raws = bsobj.select('div.refinement.brand')
    hrefs = []
    for raw in raws:
        for r in raw.select('a.refinement-link'):
            hrefs.append(r.get('href'))
    return hrefs

#Get all the brand page URLs
def getTotalBrandUrls(brandUrls):
    i = 1
    totalBrandUrls = []
    for singleBrandUrl in brandUrls:
        print(i, ": ", singleBrandUrl)
        i = i + 1
        totalBrandUrls.append(singleBrandUrl)
        bsobj = requests_bs(singleBrandUrl)
        pageClass = bsobj.select('div.pagination')[0].select('a')
        if len(pageClass) == 0:
            continue
        else:
            for li in pageClass:
                pageUrl = li.get("href")
                totalBrandUrls.append(pageUrl)
                print(i, ": ", pageUrl)
                i = i + 1
    return totalBrandUrls

#Get all the product urls
def product(urls):
    list = []
    for url in urls:
        bsobj = requests_bs(url)
        raws = bsobj.select('a.product-link')
        for raw in raws:
            pro_url = raw.get('href')
            if pro_url[0:4] != 'http':
                continue;
            list.append(pro_url)
    return list

#Scrape the information from those product urls
def concreteProduct(urls):
    finalResults = []
    for url in urls:
        print(url)
        bsobj = requests_bs(url)
        if len(bsobj.select('div.brand-name')) == 0 or len(bsobj.select('div.brand-name')[0].select('span.visually-hidden')) == 0:
            continue
        brand = bsobj.select('div.brand-name')[0].select('span.visually-hidden')[0].get_text()
        name = bsobj.select('div.brand-name')[0].get_text()[len(brand):].strip()
        if (len(bsobj.select('div.standardprice')) == 0 and len(bsobj.select('div.standardprice')) != 0):
            price =bsobj.select('span.price-sales')[0].select('span.visually-hidden')[0].get_text()
        elif len(bsobj.select('div.standardprice')) != 0 and len(bsobj.select('div.standardprice')[0].select('span')) != 0:
            price = bsobj.select('div.standardprice')[0].select('span')[0].get_text()
        else:
            price = ''
        category = ""
        tmp = bsobj.select('a.hide-mobile.breadcrumb-element')
        if len(tmp) > 0:
            category = bsobj.select('a.hide-mobile.breadcrumb-element')[-1].get_text()
        list = [brand, name, price, category, '', url]
        finalResults.append(list)
    return finalResults

#Write the collected data into csv file
def writecsv(file,rows):
    with open(file,'a+',encoding='utf_8_sig',newline='') as file:
        w = csv.writer(file)
        for list in rows:
            w.writerow(list)

        
if __name__ == '__main__':
    oris = ori_url(path)
    brand_urls = getTotalBrandUrls(oris[150:])


    product_urls = product(brand_urls)
    finalResults = concreteProduct(product_urls)
    writecsv('data1.csv', finalResults)

    
    
    
