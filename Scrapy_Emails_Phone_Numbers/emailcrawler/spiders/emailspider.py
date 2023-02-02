# -*- coding: utf-8 -*-
import scrapy
import sys
import re

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

    def start_requests(self):
        query = input("Enter your query: ")
        for url in self.start_urls:
            yield scrapy.Request("{}{}".format(url, query))

    def parse(self, response):
        # url_to_follow = response.css(".r>a::attr(href)").extract()
        url_to_follow = response.css("a::attr(href)").extract()
        print('RAW URLs')
        print(url_to_follow)
        url_to_follow = [url.replace('/search?q=', 'https://google.com/search?q=') for url in url_to_follow]
        print(url_to_follow)
        url_to_follow = [url for url in url_to_follow if '://' in url and '.google.com' not in url]
        print('CLEAN URLs')
        print(url_to_follow)
        for url in url_to_follow[:]:
            yield scrapy.Request(
                url=url, callback=self.parse_email, dont_filter=True)

        print(f'Processing {response.url}')
        next_pages_urls = response.css("#foot table a::attr(href)").extract()
        print('NEXT PAGE URLs')
        print(next_pages_urls)
        for page_num, url in enumerate(next_pages_urls):
            if(page_num < 11):
                next_page_url = response.urljoin(url)
                yield scrapy.Request(
                    url=next_page_url, callback=self.parse, dont_filter=True)
            else:
                break

    def parse_email(self, response):
        html_str = response.text
        emails = self.extract_email(html_str)
        phone_no = self.extract_phone_number(html_str)
        yield{
            "url": response.url,
            "emails": emails,
            "phone numbers": phone_no
        }

    def extract_email(self, html_as_str):
        return re.findall(r'[\w\.-]+@[\w\.-]+', html_as_str)

    def extract_phone_number(self, html_as_str):
        return re.findall(r'\+\d{2}\s?0?\d{10}', html_as_str)



