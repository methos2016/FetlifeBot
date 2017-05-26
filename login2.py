# -*- coding: utf-8 -*-
import scrapy

BASE_URL = 'https://www.fetlife.com'
USER_NAME = 'ThisGonnaBeGud'
PASSWORD = 'uCrtt5omeTEW'
PAGES = ['1', '/users/2', '/users/3']


class MySpider(scrapy.Spider):


    name = 'fetspider'
    start_urls = [BASE_URL + '/users/sign_in']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@id="new_user"]',
            formdata={
                'user_login': USER_NAME,
                'user_password': PASSWORD,
            },
            callback=self.after_login)

    def after_login(self, response):
        base_url = BASE_URL + '/users/'
        for page in PAGES:
            yield Request(
                url=base_url + page + "1",
                callback=self.action)

    def action(self, response):
        page = re.search('users/(.*)1', response.url)
        if page:
            page_name = page.group(1)
            title = response.xpath('//title/text()').extract_first('').strip()
            item = PageItem()
            item['pagename'] = page_name
            item['description'] = title
            yield item

# Scrape data from page, wrote this myself, no clue if it's even close to being correct.
# Kind of followed example here https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3

    def parse(self, response):
        Div_Selector = 'span-13 append-1'
        for fetspider in response.body(Div_Selector):
                UserName_Selector = 'h2 ::text'
                yield {
                'username': myspider.body(UserName_Selector).extract_first()
    }
