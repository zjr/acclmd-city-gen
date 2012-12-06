from bs4 import BeautifulSoup
import mechanize
import cookielib
import re

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

ucs = 'Cypress'
ucu = 'Cypress'
ucp = 'Cypress'
ucd = 'Cypress'
lc  = 'cypress'

# Open city page, read and make soup.
r = br.open('http://www.city-data.com/city/'+ucd+'-California.html')
cData = r.read()
cSoup = BeautifulSoup(cData, 'lxml')

# Statistical Variables
pop  = str(cSoup.find("b", text="Population in 2010:").next_sibling.replace(' ', '').replace('.', ''))
age  = str(cSoup.find(text=re.compile("Median resident age")).parent.parent.next_sibling.get_text().replace(u'\xa0', u'').replace(' years', ''))
inc  = str(cSoup.find(text=re.compile("median household income")).parent.next_sibling.replace(' ', '').replace('(', ''))
home = str(cSoup.find(text=re.compile("median house or condo value")).parent.next_sibling.replace(' ', '').replace('(', ''))

# Image check
hasImg = cSoup.find('a', href=re.compile('picfiles'))

if hasImg:
	# Image link
	iLink = cSoup.find('a', href=re.compile('picfiles'))['href']
	
	# Open city image page, read and make soup.
	r = br.open('http://www.city-data.com'+iLink)
	iPage = r.read()
	iSoup = BeautifulSoup(iPage, 'lxml')
	
	# Image Variables
	iAlt = iSoup.img['alt']
	iSrc = iSoup.img['src']

	# Image download
	br.retrieve(iSrc, 'city-gen/images/'+ucu+'.jpg')
else:
	iAlt = 'A map of '+ucs
	iSrc = 'http://maps.googleapis.com/maps/api/staticmap?center='+ucp+'+CA&zoom=11&size=550x400&sensor=false'
	br.retrieve(iSrc, 'city-gen/images/'+ucu+'.jpg')
