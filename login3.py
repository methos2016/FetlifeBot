# -*- coding: utf-8 -*-
#import scrapy

# BASE_URL = 'https://www.fetlife.com'
# USER_NAME = 'fetlife.aws@gmail.com'
# PASSWORD = 'uCrtt5omeTEW'
# PAGES = ['1', '/users/2', '/users/3']
#
#
# class MySpider(scrapy.Spider):
#     name = 'fet_spider'
#     start_urls = [BASE_URL + '/users/sign_in']
#
#     def parse(self, response):
#         yield scrapy.FormRequest.from_response(
#             response,
#             formxpath='//form[@id="new_user"]',
#             formdata={
#                 'user_login': USER_NAME,
#                 'user_password': PASSWORD,
#             },
#             callback=self.after_login)
#
#     def after_login(self, response):
#         if "authentication failed" in response.body:
#             self.logger.error("Login failed")
#
#         scrapy.Request(url=BASE_URL+PAGES)
#         set_selector = 'span-6'
#         for fet in response.css(set_selector):
#
#             user_selector = 'h2 a ::text'
#             yield dict(name=fet.css(user_selector).extract_first())


import scrapy
import time

class MySpider(scrapy.Spider):
    name = 'fetlifespider3'
    allowed_domains = ['www.fetlife.com']
    login_page = 'https://www.fetlife.com/users/sign_in'
    start_urls = ['https://www.fetlife.com/users/1',
                  'https://www.fetlife.com/users/2']


    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@id="new_user"]',
            formdata={
                'user_login': USER_NAME,
                'user_password': PASSWORD,
            },
            callback=self.after_login)

    time.sleep(2)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "Hi Herman" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse_item(self, response):
        # Scrape data from page
        set_selector = 'span-6'
        for fet in response.css(set_selector):
            user_selector = 'h2 a ::text'
            yield dict(name=fet.css(user_selector).extract_first())