# -*- coding: utf-8 -*-
import scrapy
import sys
import re
from bs4 import BeautifulSoup

'''
to use: 
1. open terminal
2. cd to folder containing scrapy project
3. enter: scrapy crawl emailspider -o output.json
'''


class EmailspiderSpider(scrapy.Spider):
    name = 'emailspider'
    # allowed_domains = ['www.neuromarketingworldforum.com',
    # 'www.nmsba.com',
    # 'www.thinkneuro.de']
    start_urls = ['https://google.com/search?q=']
    results_pages_to_scrape = 2
    page_num = 0

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
        url_to_follow = [url for url in url_to_follow if '://' in url and '.google.com/' not in url]
        print('CLEAN URLs')
        print(url_to_follow)
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
        emails = self.extract_emails(html_str)
        phone_no = self.extract_phone_numbers(html_str)
        prices = self.extract_prices(html_str)
        pdfs_xmls = self.extract_pdfs_xmls(html_str)
        yield{
            "url": response.url,
            "emails": emails,
            "phone numbers": phone_no,
            "prices": prices,
            "pdfs or xmls": pdfs_xmls
        }

    # def extract_email(self, html_as_str): #original
    #     return re.findall(r'[\w\.-]+@[\w\.-]+', html_as_str)

    # def extract_emails(self,html_string):
    #     # Regular expression pattern for matching email addresses
    #     pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
    #     # Find all email addresses in the HTML string
    #     emails = re.findall(pattern, html_string)
    #     return emails

    def extract_emails(self,html_string):
        # Regular expression pattern for matching email addresses
        pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        # Find all email addresses in the HTML string
        emails = re.findall(pattern, html_string)
        return emails

    # def extract_phone_number(self, html_as_str): #original
    #     return re.findall(r'\+\d{2}\s?0?\d{10}', html_as_str)

    def extract_phone_numbers(self,html_string):
        # Regular expression pattern for matching European phone numbers
        pattern = re.compile(r'\+[1-9]{2}[\s\.-]?[1-9]{1}[\s\.-]?\d{3}[\s\.-]?\d{4}[\s\.-]?\d{2,4}')
        # Find all European phone numbers in the HTML string
        phones = re.findall(pattern, html_string)
        return phones
    
    def extract_prices(self,html_string):
        # Regular expression pattern for matching European or American prices
        pattern = re.compile(r'[€$]\d+(?:\.\d{2})?')
        # pattern = re.compile(r'(\$|€)\s*\d+(?:\.\d+)?')
        # Find all European or American prices in the HTML string
        prices = re.findall(pattern, html_string)
        return prices

    # def extract_prices(self,html_string):
    #     prices = []
    #     soup = BeautifulSoup(html_string, 'html.parser')
    #     for price in soup.select('span[class*="price"]'):
    #         prices.append(price.text)
    #     return prices
    
    # def extract_pdfs_xmls(self,html_string):
    #     # Regular expression pattern for matching PDF or XML file URLs
    #     # pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(pdf|xml)')
    #     pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(.pdf|.xml)')
    #     # Find all PDF or XML file URLs in the HTML string
    #     urls = re.findall(pattern, html_string)
    #     return urls

    def extract_pdfs_xmls(self,html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        urls = []
        for link in soup.find_all("a"):
            href = link.get('href')
            if href and href.endswith(('.pdf', '.xml')):
                urls.append(href)
        return urls
    #add price parsing column
    # find pdf, xls documents

    def extract_invested_money(self,html_string):
        #do something

    def extract_annual_revenue(self,html_string):
        #do something

    def extract_investors_names(self,html_string):
        #do something




