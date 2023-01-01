import json
import scrapy
from scrapy.utils.reactor import install_reactor 
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess
import webbrowser
import argparse



install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

# from helper import should_abort_request

def arguments():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--out", dest="out", help="Name of output file")
    parser.add_argument("--query", dest="query", help="Keyword")

    options = parser.parse_args()

    if not options.out:
        print("Please specify the type of search, use --help for more info")
        exit()
    if not options.query:
        print("Please specify the query, use --help for more info")
        exit()

    return options

SearchOpt = arguments()
FILE_NAME = str(SearchOpt.out)
QUERY = str(SearchOpt.query)



class PwspiderSpider(scrapy.Spider):
    name = 'scrape_buzz'
    
    custom_settings = dict(

            DOWNLOAD_HANDLERS = {
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },

            TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor",

            PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 100000,

            PLAYWRIGHT_LAUNCH_OPTIONS = {"headless":True} 
    )

    def start_requests(self):

        with open(FILE_NAME, 'w') as f:
            f.write('')

        yield scrapy.Request('http://www.social-searcher.com/social-buzz/?q5='+QUERY.lower(), 
            meta=dict(
            playwright=True, 
            playwright_include_page= True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'div.rezults-item-body'),
                ],
                errback=self.errback,)
            )

    async def parse(self, response):

        page = response.meta['playwright_page']
        for i in range(5):  # 2 to 10
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")  
            await page.wait_for_selector(f'div.rezults-item-body')

        s  = scrapy.Selector(text=await page.content())
        await page.close()
        
        # s = response

        f = open("social_temp3.html", "w")
        f.write(str(response.body))
        f.close()

        tr_tags  = response.css('tr')
        # yield {"well":tr_tags.css("td").getall()}
                
        for tr in tr_tags[::-1]:
            use = tr.css('td::text')
            x = use.re(r"\b(view|like|retweet|note)\b")
            # print(x)
            if len(x) != 0:
                try:
                    like  = use[use.getall().index(x[-1])+1].getall()
                except:
                    like = "Not Available"
            try:
                items = {
                    'platform':tr.css('td::text').getall()[0],
                    'uploaded_by':tr.css('td::text').getall()[1],
                    'links':tr.css('td::text').re(r'(?:(?:(?:ftp|http)[s]*:\/\/|www\.)[^\.]+\.[^ \n]+)'),
                    'upload_date':tr.css('td::text').getall()[3],
                    'post_content':tr.css('td')[4].css('*::text').getall(),
                    'sentiment': tr.css('td::text').re(r"\b(positive|neutral|negative)\b"),
                    'number_of_interactions': like,
                    }
                
                with open(FILE_NAME, 'a') as f:
                    f.write(json.dumps(items, indent = 2)+ '\n')
            except:
                continue
        
    
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(PwspiderSpider)
    process.start() 