# -*- coding: utf-8 -*-
import scrapy
import json

class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['fetlife.com']
    login_page = 'http://www.fetlife.com/users/sign_in'
    start_urls = ['https://fetlife.com/users/1']

#    rules = (
#        Rule(SgmlLinkExtractor(allow=r'-\w+.html$'),
#             callback='parse_item', follow=True),
#    )

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'user_login': 'ThisGonnaBeGud', 'user_password': 'uCrtt5omeTEW'},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "What’s on your kinky mind?" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

# Scrape data from page, wrote this myself, no clue if it's even close to being correct.
# Kind of followed example here https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3

    def parse(self, response):
        Div_Selector = 'span-13 append-1'
        for myspider in response.body(Div_Selector):
                UserName_Selector = 'h2 ::text'
                yield {
                'username': myspider.body(UserName_Selector).extract_first()
    }


#Saving to JSON

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item




#next_page_url = response.css("li.next > a::attr(href)").extract_first()
#if next_page_url is not None:
#yield scrapy.Request(response.urljoin(next_page_url))