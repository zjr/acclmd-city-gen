from peewee import *

mysql_db = MySQLDatabase('mauth_db', user='mauth_usr', passwd='&*4ccl41m3d*&')

class MySQLModel(Model):
	class Meta:
		database = mysql_db

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

cCity = 'van nuys'

cQuery = Cities.select().where(Cities.city == cCity, Cities.state == 'CA')

for c in cQuery:
	cLat = str(c.lat)
	cLon = str(c.lon)

dQuery = 'SELECT id, city, state, ( 3959 * acos( cos( radians('+cLat+') ) * cos( radians( lat ) ) * cos( radians( lon ) - radians('+cLon+') ) + sin( radians('+cLat+') ) * sin( radians( lat ) ) ) ) AS distance FROM cities HAVING distance < 100 ORDER BY distance LIMIT 0 , 2000;'

rq = Cities.raw(dQuery)

i = 0

for obj in rq.execute():
	if i <= 12 :
		try:
			z = Cities_On.get(Cities_On.city == obj.city)
			if i > 0:
				print i, obj.city, obj.distance, '//', obj.state
			i = i + 1
		except Exception:
			pass
