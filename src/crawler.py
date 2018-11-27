# -*- coding: utf-8 -*-

'''
Created on 2018. 11. 27.

@author: jason96
'''

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


class NaverNewsCrawler():
    
    base_url = 'https://news.naver.com'
    sectionIds = ['100', '102', '103', '104', '105', '003', '115']
    
    def __init__(self):
        pass
        
    def get_article_link(self):
        links = []
        for sectionId in self.sectionIds:
            url = self.base_url + '/main/ranking/popularMemo.nhn?' + \
                'rankingType=popular_memo&sectionId=' + sectionId
            res = requests.get(url)
            if res.status_code == 200:
                body = res.content.decode('euc-kr', 'utf-8')
                soup = BeautifulSoup(body, features="html.parser")
                for div in soup.find_all("div", class_="ranking_headline"):
                    for a in div.find_all('a', href=True):
                        links.append(self.base_url + a['href'])
                    break
                    
        return links

    def extract_memo(self, article_url):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(article_url)
        memo_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//ul[@class='u_cbox_list']"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for li in soup.find_all("li", class_="u_cbox_comment"):
            print li.find("span", class_="u_cbox_contents").getText()
            print li.find("span", class_="u_cbox_nick").getText()
            print li.find("span", class_="u_cbox_date").getText()
            
        
    def crawl(self,):
        for article_url in self.get_article_link():
            self.extract_memo(article_url)
            break
                

if __name__ == '__main__':
    crawler = NaverNewsCrawler()
    # crawler.crawl()
    crawler.extract_memo("https://news.naver.com/main/ranking/read.nhn?rankingType=popular_day&oid=417&aid=0000359051&date=20181127&type=1&rankingSectionId=101&rankingSeq=1")
    
