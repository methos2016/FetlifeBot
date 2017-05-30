import bs4
import sys
import requests

URL = ("https://www.fetlife.com/users/sign_in")

client = requests.session()

# Retrieve the CSRF token first
client.get(URL)
# sets cookie
csrftoken = client.cookies['csrf']

login_data = dict(user_login=fetlife.aws@gmail.com, user_password=uCrtt5omeTEW, csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(URL, data=login_data, headers=dict(Referer=URL))


PAGE = requests.get("http://www.fetlife.com/users/1")
SOUP = bs4.profiles(response.text)
links = soup.select('div.span-13 append-1 ')