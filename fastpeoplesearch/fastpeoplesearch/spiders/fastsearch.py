import scrapy
from scrapy import Request

class FastsearchSpider(scrapy.Spider):
    name = 'fastsearch'
    # name = 'laptop'
    def start_requests(self):
        url = 'https://www.fastpeoplesearch.com/name/siddyant-das'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        # for p in range(20):
        #     yield scrapy.Request(url+"/page/"+str(p), callback=self.parse)        
        yield scrapy.Request(url,headers=headers, callback=self.parse)        

    def parse(self, response):
        # with open('out1.html', 'w') as html_file:
        #     html_file.write(response.text)
        
        persons = response.css('div.card')
        for person in persons:
            yield {
                # "full_name": person.xpath("//h3/following-sibling::text()")[1].extract(),
                # "age": person.xpath("//h3/following-sibling::text()")[0].extract(), 
                "current_address": "".join(person.css('strong').css('a[title*="Search people living at"]::text').getall()),
                # 'locations_text': person.css('h3').css('span')[0].getall(),
                'past_addresses' : person.css('div.row').css('a::text').getall(),
                # 'contact_text':person.css('h3').css('span')[1].getall(),
                'contacts': person.css('a[title*="Search people with phone number"]::attr(href)').getall(),
                'alias': person.css('span.nowrap::text').getall(),
                'relatives':person.css('a[title*="Fast People Search for"]::text').getall(),
                'relatives_page':person.css('a[title*="Fast People Search for"]::attr(href)').getall()
            }
        
        # if not response.body:
        #     yield Request(url=response.url, dont_filter=True)
        # print(response.css('rezults-item-user-body"'))