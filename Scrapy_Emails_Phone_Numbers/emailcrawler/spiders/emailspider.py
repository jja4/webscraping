# -*- coding: utf-8 -*-
import scrapy
import sys
import re
from bs4 import BeautifulSoup
import requests
import regex

'''
to use: 
1. open anaconda prompt/terminal
2. cd to folder containing scrapy project
3. enter: scrapy crawl emailspider -o output.csv

The code is a web spider written using Scrapy, a Python web crawling framework. 
The spider crawls Google search results pages and extracts information from the URLs found. 
The information extracted includes email addresses, phone numbers, prices, and PDF or XML file URLs. 
To run the spider, open the terminal, go to the folder containing the Scrapy project, 
and enter "scrapy crawl emailspider -o output.json". 

The spider starts by asking the user to input a search query, then crawls the Google search results 
pages, extracts the desired information, and saves it to a JSON file named "output.json". 
The spider uses regular expressions to extract email addresses, phone numbers, and prices.

'''



class EmailspiderSpider(scrapy.Spider):
    name = 'emailspider'
    # allowed_domains = ['www.neuromarketingworldforum.com',
    # 'www.nmsba.com',
    # 'www.thinkneuro.de']
    start_urls = ['https://google.com/search?q=']
    results_pages_to_scrape = 1
    page_num = 0

    # custom_settings = {
    #     'FEED_URI': 'output.json',
    #     'FEED_FORMAT': 'jsonlines',
    #     'FEED_EXPORTERS': {'json': 'emailcrawler.exporters.NewlineJsonItemExporter'},
    # }

    def start_requests(self):
        query = input("Enter your query: ")
        for url in self.start_urls:
            yield scrapy.Request("{}{}".format(url, query))

    def parse(self, response):
        # url_to_follow = response.css(".r>a::attr(href)").extract()
        url_to_follow = response.css("a::attr(href)").extract()
        # print('RAW URLs')
        # print(url_to_follow)
        url_to_follow = [url.replace('/search?q=', 'https://google.com/search?q=') for url in url_to_follow]
        # print(url_to_follow)
        url_to_follow = [url for url in url_to_follow if '://' in url and 'google.com/' not in url and '.google.com/sorry' not in url ]
        print('CLEAN URLs')
        # print(url_to_follow)
        for url in url_to_follow[:]:
            yield scrapy.Request(
                url=url, callback=self.parse_url, dont_filter=True)

        print(f'Processing {response.url}')
        next_pages_urls = response.xpath("//a[@id='pnnext']/@href").extract()

        # next_pages_urls = response.css("li.next a::attr(href)").extract_first()
        # next_pages_urls = response.css("#foot table a::attr(href)").extract()
        # print('NEXT PAGE URLs')
        # print(next_pages_urls)
        next_pages_urls = [url.replace('/search?q=', 'https://google.com/search?q=') for url in next_pages_urls]
        for num, url in enumerate(next_pages_urls):
            if(self.page_num < self.results_pages_to_scrape):
                next_page_url = response.urljoin(url)
                print(f'RESULTS PAGE {self.page_num}')
                print(next_page_url)
                self.page_num +=1
                yield scrapy.Request(
                    url=next_page_url, callback=self.parse, dont_filter=True)
            else:
                break

    def parse_url(self, response):
        html_str = response.text
        url_str = response.url
        emails = self.extract_emails(html_str)
        phone_no = self.extract_phone_numbers(html_str)
        prices = self.extract_prices(html_str)
        pdfs_xlsx = self.extract_pdfs_xls(html_str)
        yield{
            "url": response.url,
            "emails": emails,
            "phone numbers": phone_no,
            "prices": prices,
            "pdfs or xlsx": pdfs_xlsx
        }


    def extract_emails(self,html_string):
        # Regular expression pattern for matching email addresses
        # pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        # Find all email addresses in the HTML string
        emails = re.findall(pattern, html_string)
        return emails

    # def extract_phone_number(self, html_as_str): #original
    #     return re.findall(r'\+\d{2}\s?0?\d{10}', html_as_str)

    def extract_phone_numbers(self,html_string):
        # Regular expression pattern for matching European phone numbers
        # pattern = re.compile(r'\+[1-9]{2}[\s\.-]?[1-9]{1}[\s\.-]?\d{3}[\s\.-]?\d{4}[\s\.-]?\d{2,4}')
        pattern = re.compile(r'\(?\+\d{1,3}\)?[-. ]?\(?\d{2,4}\)?[-. ]?\d{2,4}[-. ]?\d{2,4}')
        # Find all European phone numbers in the HTML string
        phones = re.findall(pattern, html_string)
        return phones
    
    def extract_prices(self,html_string):
        # Regular expression pattern for matching European or American prices
        pattern = r'\p{Sc}[\d]+(?:[\d.,]+)?(?:[.,]\d{2})?'
        # pattern = re.compile(r'\p{Sc}[\d.,]+(?:[.,]\d{2})?')
        # pattern = re.compile(r'(\$|€)\s*\d+(?:\.\d+)?')
        # Find all European or American prices in the HTML string
        prices = regex.findall(pattern, html_string)
        return prices

    # def extract_prices(self,html_string):
    #     prices = []
    #     soup = BeautifulSoup(html_string, 'html.parser')
    #     for price in soup.select('span[class*="price"]'):
    #         prices.append(price.text)
    #     return prices
    


    def extract_pdfs_xls(self,html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        urls = []
        for link in soup.find_all("a"):
            href = link.get('href')
            if href and href.endswith(('.pdf', '.xls','.xlsx')):
                urls.append(href)
        return urls


    def extract_invested_money(self,html_string):
        #do something

    def extract_annual_revenue(self,html_string):
        #do something

    def extract_investors_names(self,html_string):
        #do something
