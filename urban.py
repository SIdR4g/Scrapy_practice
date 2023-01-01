from calendar import c
import scrapy 
import requests
import requests
import json
from scrapy.crawler import CrawlerProcess
import string

class Urban(scrapy.Spider):
    name = 'urban'
    url = 'https://www.urbandictionary.com/browse.php?character='

    def start_requests(self):

        with open('urban.json', 'w') as f:
            f.write('')
        
        for letter in string.ascii_uppercase:
            next_page = self.url + letter
            for page in range(1,40):
                yield scrapy.Request(url = next_page+"&page="+str(page), callback = self.parse)
                break
            break
    
    def parse(self, response):
        # print('\n\nResponse:', response.status)
        links = []
        for item in response.css("ul.mt-3.columns-2.md\:columns-3").css('li'):
            links.append( {
                'word': item.css('a::text').get(),
                'link': item.css('a::attr(href)').get()

            })
            # print(json.dumps(items, indent = 2))
        for link in links:
            yield response.follow(
                url = link['link'], 
                meta = {
                    'word':link['word'], 
                }, callback = self.parse_link)

    def parse_link(self, response):
        # print("/n/nREXPONSE", response.status)

        word = response.meta.get('word')
        description = ''.join(response.css('div.p-5.md\:p-8').css('div.break-words.meaning.mb-4 ::text').getall())

        items = {
                'word':word,
                'description':description
            }

        with open('urban.json', 'a') as f:
            f.write(json.dumps(items, indent = 2)+ '\n')

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Urban)
    process.start()
