# -*- coding: utf-8 -*-
import scrapy

class MySpider(scrapy.Spider):
    name = 'fetlifespider'
    allowed_domains = ['domain.com']
    login_page = 'https://www.fetlife.com/users/sign_in'
    start_urls = ['https://www.fetlife.com/users/1',
                  'https://www.fetlife.com/users/2']


    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'user_login': 'fetlife.aws@gmail.com', 'user_password': 'uCrtt5omeTEW'},
                    callback=self.check_login_response)

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