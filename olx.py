from concurrent.futures import process

from pyparsing import line
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv
import pandas as pd


class Olx(scrapy.Spider):
    name = "olx"

    url = "https://www.olx.in/api/relevance/feed?lang=en-IN&latitude=20.5937&location=1000001&longitude=78.9629"
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    df = pd.DataFrame()

    # def __init__(self):



    def start_requests(self):
        for page in range(100):
            yield scrapy.Request(url = self.url+ '&page=' + str(page), headers = self.headers, callback = self.parse )

    def parse(self, response):
        # print()
        data = response.text
        # with open('res.json', 'r') as json_file:
        #     for line in json_file.read():
        #         data+=line
        data = json.loads(data)
        # print(json.dumps(data, indent =2))

        title,description,price,location,date,features = [],[],[],[],[],[]

        for offer in data['data']:
            # print(json.dumps(data, indent =2))
            items = {
            'title' : offer['title'],
            'description': offer['description'],
            'price': offer['price']['value']['display'],
            'location': offer['locations_resolved']['COUNTRY_name']+", "+
                        offer['locations_resolved']['ADMIN_LEVEL_1_name']+", "+
                        offer['locations_resolved']['ADMIN_LEVEL_3_name'],
                        # offer['locations_resolved']['SUBLOCALITY_LEVEL_1_name']
            'date': offer['display_date'],
            'features':offer['main_info']
            }
            # print(json.dumps(items, indent =2))
            # print(items.keys())
            # with open('results.csv', 'a') as csv_file:
            #     writer = csv.DictWriter(csv_file, fieldnames = items.keys())
            #     writer.writerow(items)           
            self.df = self.df.append(items, ignore_index =True)
        self.df.to_csv('olx.csv')



process = CrawlerProcess()
process.crawl(Olx)
process.start()

# Olx.parse(Olx, '')