import urllib2
import json
import sys
from random import randint
from time import sleep
from re import findall

def main():
    if len(sys.argv) < 2:
        print 'Usage:  fetscraper.py <value of logged in session token>'
        sys.exit()

    else:
        scraper(sys.argv[1])


def scraper (sessionToken):
    minProfile = int(raw_input('Enter the minimum profile integer to start culling from: '))
    maxProfile = int(raw_input('Enter the maximum profile integer to cull to: '))
    profiles = range(minProfile,maxProfile)

    print 'Starting profile culling...'

    while len(profiles) > 0:
        currentProfile = profiles[randint(0,len(profiles)-1)]
	print 'Grabbing https://fetlife.com/users/' + str(currentProfile)
        request = urllib2.Request('https://fetlife.com/users/' + str(currentProfile))
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.add_header('Accept-Language','en-US,en;q=0.5')
        request.add_header('Cookie','language=en; _fl_sessionid=' + sessionToken)
        request.add_header('Connection', 'close')

	try:
        	response = urllib2.urlopen(request)

	except urllib2.HTTPError:
		print 'Got an error.  plugging on.'
		continue

        if response.getcode() == 200:
            PageToParse = response.read()
            text = PageToParse.decode('utf-8')
            # Use regular expressions to find the data we want, which looks like: <a class="fl-member-card__user" href="/users/6762775">pinkrose84</a>
            user = findall("<a class=\"fl-member-card__user\" href=\"\/users\/[0-9]{1,7}\">[A-Za-z0-9-]{1,20}<\/a>", text)
	    print user
            # Fill in the parser and JSON converstion stuff here once Amanda sends me schema

#        elif response.getcode == 404:
#            print 'Profile ' + str(currentProfile) + ' returned a 404 error.'

        elif response.getcode() == 302 and response.read().index('tripped our security system.') != -1:
            print 'Whoops, the security system caught us.   If at first you don\'t succeed, try try again.'
            sys.exit()

        elif response.getcode() == 302:
            print 'Looks like we got signed out.  Need a new session token.'
            sys.exit()

        else:
	    print response.getcode()
            print 'Got some bad non-200 OK thing.  Going to move on.'

        profiles.remove(currentProfile)
        print 'Sleeping to avoid tripping security system...'
        sleep(randint(30,300))

        #Need to introduce some kind of something to make Fetlife think we're not a bot..60% of the time, load the test account's profile page, 40% of the time, keep spidering

        randomPlacesToGo = ['https://fetlife.com/explore/stuff-you-love/','https://fetlife.com/home'] #More URLs can be added here without editing the rest of the script
        diceRoll = randint(1,10)

        if diceRoll < 7:
            print 'Making a request back to a random place to make the bot counter go away...'
            garbageRequest = urllib2.Request(randomPlacesToGo[randint(0,len(randomPlacesToGo)-1)])
            garbageRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
            garbageRequest.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            garbageRequest.add_header('Accept-Language', 'en-US,en;q=0.5')
            garbageRequest.add_header('Cookie', 'language=en; _fl_sessionid=' + sessionToken)
            garbageRequest.add_header('Connection', 'close')
            throwAwayResponse = urllib2.urlopen(request)
            sleep(randint(30,180)) #wait for a little bit before continuing


if __name__ == '__main__':
    main()