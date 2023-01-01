import scrapy
from scrapy.crawler import CrawlerProcess
import json

class Shopping(scrapy.Spider):
    name = 'shopping'
    base_url = 'https://www.flipkart.com/search?q=earphones'
    
    def start_requests(self):

        with open('flipkart_earphones.json', 'w') as f:
            f.write('')
        for page in range(1,100):
            yield scrapy.Request(url = self.base_url+"&page="+str(page), callback = self.parse)

    def parse(self, response):
        temp = ""
        for item in response.css('a[target="_blank"][href*="&marketplace=FLIPKART"]::attr(href)').getall():
            if temp!=str(item):
                # print(item)
                temp = item
                yield scrapy.Request(url = self.base_url+str(item), callback = self.parse_product)
            # break
    def parse_product(self, response):
        # print("/n/nResponse", response.status)
        items =  {
            'link':response.url,
            'Name': response.css('span[class="B_NuCI"] ::text').get(),
            'Price':response.css('div[class="_30jeq3 _16Jk6d"] ::text').get(),
            'Rating':response.css('div[class = "_3LWZlK"] ::text').get(),
            'Description':response.css('div[class="_2418kt"] ::text').getall()
        }

        with open('flipkart_earphones.json', 'a') as f:
            f.write(json.dumps(items, indent = 2)+ '\n')


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(Shopping)
    process.start() 