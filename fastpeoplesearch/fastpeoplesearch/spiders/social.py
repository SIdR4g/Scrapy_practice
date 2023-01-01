
from lxml import html
from scrapy_splash import SplashRequest
import scrapy
class FastsearchSpider(scrapy.Spider):
    name = 'social'

    def start_requests(self):
        url = 'https://www.social-searcher.com/social-buzz/?q5=rishisunak'
        yield SplashRequest(url, callback = self.parse)        

    def parse(self, response):
        f = open("social.html", "a")
        f.write(str(response.body))
        f.close()
        # print(response.css('div.rezults-container::text'))#.css('div.rezults-item'))