cities = [
	"palmdale", 
	"anaheim", 
	"santa ana", 
	"irvine", 
	"huntington beach", 
	"garden grove", 
	"fullerton", 
	"costa mesa", 
	"mission viejo", 
	"westminster", 
	"newport beach", 
	"buena park", 
	"lake forest", 
	"tustin", 
	"yorba linda", 
	"san clemente", 
	"laguna niguel", 
	"la habra", 
	"fountain valley", 
	"placentia", 
	"rancho santa margarita", 
	"aliso viejo", 
	"cypress", 
	"brea", 
	"stanton", 
	"san juan capistrano", 
	"dana point", 
	"laguna hills", 
	"seal beach", 
	"laguna beach", 
	"laguna woods", 
	"la palma", 
	"los alamitos", 
	"villa park", 
	"mira monte", 
	"meiners oaks", 
	"casa conejo", 
	"channel islands beach", 
	"saticoy", #
	"santa maria", 
	"santa barbara", 
	"lompoc", 
	"orcutt", 
	"isla vista", 
	"guadalupe", 
	"vandenberg village", 
	"solvang", 
	"buellton", 
	"santa ynez", 
	"mission canyon", 
	"los alamos", 
	"los olivos", #
	"new cuyama", #
	"ballard", #
	"sisquoc", #
	"casmalia", #
	"garey", #
	"cuyama", 
	"riverside", 
	"moreno valley", 
	"corona", 
	"murrieta", 
	"temecula", 
	"hemet", 
	"menifee", #
	"indio", 
	"perris", 
	"eastvale", #
	"lake elsinore", 
	"cathedral city", 
	"palm desert", 
	"palm springs", 
	"san jacinto", 
	"coachella", 
	"la quinta", 
	"beaumont", 
	"wildomar", 
	"banning", 
	"norco", 
	"desert hot springs", 
	"blythe", 
	"rancho mirage", 
	"canyon lake", 
	"calimesa", 
	"indian wells"
]

from bs4 import BeautifulSoup
from peewee import *
import mechanize
import cookielib
import time
import sys
import re

## Set up percent counter
piX   = 0.0
pi100 = len(cities)

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
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=4)

# User-Agent
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

for city in cities:
	### Variables for Template
	## LowerCaseUnderscore
	lcu = city.replace(' ', '_')	
	## LowerCaseDash
	lcd = city.replace(' ', '-')
	## LowerCase
	lc  = city.replace(' ', '')
	## UpperCaseUnderscore
	ucu = city.replace(' ', '_').title()
	## UpperCaseSpace
	ucs = city.title()
	## UpperCaseDash
	ucd = city.replace(' ', '-').title()
	## UpperCasePlus
	ucp = city.replace(' ', '+').title()

	# Open city page, read and make soup.
	##
	### This needs to be refactored for cities with no info on city-data.
	##
	#
	def openPage(e):
		try:
			r = br.open('http://www.city-data.com/city/'+ucd+'-California.html')
		except Exception:
			e = e + 1
			if e < 3:
				time.sleep(1)
				openPage(e)
			else:
				print 'Mechanize failed to connect.'
	openPage(0)

	cData = r.read()
	cSoup = BeautifulSoup(cData, 'lxml')

	# Statistical Variables
	pop  = str(cSoup.find("b", text=re.compile("Population in")).next_sibling.replace(' ', '').replace('.', ''))
	age  = str(cSoup.find(text=re.compile("Median resident age")).parent.parent.next_sibling.get_text().replace(u'\xa0', u'').replace(' years', ''))
	inc  = str(cSoup.find(text=re.compile("median household income")).parent.next_sibling.replace(' ', '').replace('(', ''))
	home = str(cSoup.find(text=re.compile("median house or condo value")).parent.next_sibling.replace(' ', '').replace('(', ''))

	Image check
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
		# Gets static google map of location if no city-data img found.
		iAlt = 'A map of '+ucs+'.'
		iSrc = 'http://maps.googleapis.com/maps/api/staticmap?center='+ucp+'+CA&zoom=11&size=550x400&sensor=false'
		br.retrieve(iSrc, 'city-gen/images/'+ucu+'.jpg')
	
	### Replacements dictionary
	replacements = {
		'UpperCaseUnderscore': ucu,
		'UpperCaseSpace'     : ucs,
		'UpperCaseDash'      : ucd,
		'UpperCasePlus'      : ucp,
		'LowerCase'          : lc,
		'CityPop'            : pop,
		'CityAge'            : age,
		'CityIncome'         : inc,
		'CityHome'           : home,
		'CityImgCap'         : iAlt,
		'cityImgCap'         : iAlt
	}

	## Keylist
	keylist = replacements.keys()
	keylist.sort()

	## File Name
	fname = [lcd]
	## Filetype
	fname.append('php')
	fname = '.'.join(fname)
	
	# Read template file.
	cTemp  = open('city_template.php', 'r')
	cTempR = cTemp.read()

	## Replace placeholder words with city name
	for key in keylist:
		cTempR = cTempR.replace(key, replacements[key])

	##
	## Start Nearby Cities
	##
	# Connect to Database
	mysql_db = MySQLDatabase('mauth_db', user='mauth_usr', passwd='&*4ccl41m3d*&')

	# Set DB as mysql for Peewee ORM
	class MySQLModel(Model):
		class Meta:
			database = mysql_db

	# Model/Table defs for peewee
	class Cities(MySQLModel):
		country = CharField()
		city = CharField()
		city_accented = CharField()
		state = CharField()
		pop = IntegerField()
		lat = DecimalField()
		lon = DecimalField()

	class Cities_On(MySQLModel):
		city = CharField()

	mysql_db.connect()

	# One variable equals another!
	# Thought this might make things less confusing --
	# -- since there is a city of Cities and a city --
	# -- of the list of cities
	cCity = city

	# Select the city from the lat/lon DB which matches --
	# both the city name and the state -> CA
	cQuery = Cities.select().where(Cities.city == cCity, Cities.state == 'CA')

	# Peewee's .where() needs to be broken with a for
	for c in cQuery:
		cLat = str(c.lat)
		cLon = str(c.lon)

	# Ridiculous sines and cosines to compute an accurate measure of distance
	# This pulls a shitload of cities from the DB, however seeing as these need -- 
	# -- to match another, considerably smaller, list, it is necessary.
	# Worth noting: it is pulling id, city, state, and computed distance -- 
	# -- only those will be available.
	dQuery = 'SELECT id, city, state, ( 3959 * acos( cos( radians('+cLat+') ) * cos( radians( lat ) ) * cos( radians( lon ) - radians('+cLon+') ) + sin( radians('+cLat+') ) * sin( radians( lat ) ) ) ) AS distance FROM cities HAVING distance < 200 ORDER BY distance LIMIT 0 , 2000;'

	# Runs and stores the result of above ridiculous query.
	rq = Cities.raw(dQuery)

	# Start a counter that ought to be in a while loop or something instead.
	# Refactor later.
	i = 0

	for obj in rq.execute():
		# We only want 12 cities to go on the list.
		if i <= 12 :
			# Check if matches list of other cities aleady on Acclaimed.
			try:
				z = Cities_On.get(Cities_On.city == obj.city)
				# i = 0 is actually the city in question so we exclude it.
				# (e.g. LA is close to LA because it is 0.0 miles away)
				if i > 0:
					# format in templace is c#lcd, c#ucs
					cstring = 'c'+str(i)
					zlcd = z.city.replace(' ', '-')
					zucs = z.city.title()
					cTempR = cTempR.replace(cstring+'lcd', zlcd).replace(cstring+'ucs', zucs)
				i = i + 1
			except Exception:
				pass
	##
	## End Nearby Cities
	##

	## Open directory/fname to write pages
	cPage = open('city-gen/'+fname, 'w')
	cPage.write(cTempR)
	cPage.close()

	## Write percentage complete
	piX = piX + 1.0
  percent = piX / pi100
  hashes = '#' * int(round(percent * bar_length))
  spaces = ' ' * (bar_length - len(hashes))
  sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
  sys.stdout.flush()