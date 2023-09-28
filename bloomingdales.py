import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import csv
from lxml import etree


data_list = []

class Blooming:
    
    def __init__(self):
        self.url = "https://www.kohls.com/catalog/kids-clothing.jsp?CN=AgeAppropriate:Kids+Department:Clothing&BL=y&icid=hpmf-PZshopdept-shopkids&sks=true&kls_sbp=29291642462297973543468974376028802037&PPP=48&WS=96&S=1"
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("window-size=1420,1080")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--enable-javascript")
        self.driver = webdriver.Chrome(options=self.options)
        self.base_url = "https://www.kohls.com"
        self.urls = []

    
    def select_agent(self):

        list_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        ]
        return random.choice(list_agents)
    
    def get_urls(self):

        headers = {"User-Agent": self.select_agent()}

        # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.
        r = requests.get(url=self.url, headers=headers)

        soup = BeautifulSoup(r.content, "html5lib")
        table = soup.find("ul", attrs={"class": "products"})
        li = table.findAll("li", attrs={"class" : "products_grid"})
        for i in li:
            div_valu = i.find("div",attrs = {"class":"prod_img_block"})
            data_url = div_valu.a['href']
            self.urls.append(self.base_url + data_url)
        return self.urls
    
    def scraper(self,url):

        self.driver.get(url)        
        link = url.strip()
        data_dict = self.driver.execute_script("return productV2JsonData")
        upc = data_dict['SKUS'][0]['UPC']['ID'].strip()
        soup = BeautifulSoup(self.driver.page_source, "html5lib")
        current_price = soup.find("span", attrs={"class": "pdpprice-row2-main-text pdpprice-row2-main-text-red"}).text.replace('$','').strip()
        regular_price = soup.find("span", attrs={"class": "pdpprice-row1-reg-price pdpprice-row1-reg-price-striked"}).text.replace('$','').replace('Reg','').strip()
        product_name = soup.find("h1", attrs={"class": "product-title"}).text.strip()
        sale_price = current_price
        data_list.append([upc,product_name,link,current_price,regular_price,sale_price])
           

if __name__ == '__main__':

    blooming = Blooming()
    urls = blooming.get_urls()
    for i in urls:
        try:
            blooming.scraper(i)
        except:
            continue


    with open('kohls.csv', 'w') as f:
     
        write = csv.writer(f)
        fields = ['UPC', 'Name', 'Link', 'Current Price' , 'Regular Price' , 'Sale Price']
        write.writerow(fields)
        write.writerows(data_list)