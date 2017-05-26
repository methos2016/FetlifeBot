# -*- coding: utf-8 -*-
import scrapy

BASE_URL = 'https://www.fetlife.com'
USER_NAME = 'fetlife.aws@gmail.com'
PASSWORD = 'uCrtt5omeTEW'
PAGES = ['1', '/users/2', '/users/3']


class MySpider(scrapy.Spider):
    name = 'fet_spider'
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
        set_selector = 'span-6'
        for fet in response.css(set_selector):

            user_selector = 'h2 a ::text'
            yield dict(name=fet.css(user_selector).extract_first())
