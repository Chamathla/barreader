from bs4 import BeautifulSoup 
import urllib2, cookielib


#import htql
from lxml import etree 
from pandas.core.common import isnull 
from sqlite3 import * 
import nltk
import string
import re
import pymongo
from pymongo import MongoClient
from nltk.corpus import stopwords
con = connect("bar_data_test.db") 
c = con.cursor()

c.execute('DROP TABLE IF EXISTS BARS')
con.commit()
sql = """CREATE TABLE BARS (
	NAME  FLOAT,
	DESCRIPTION FLOAT,
	TELEPHONE INT,  
	ADDRESS FLOAT,
	LATTITUDE INT,
	LONGITUDE INT,
	CATEGORY FLOAT,
	REVIEW FLOAT,
	PRICE FLOAT,
	RESERVATIONS FLOAT,
	DELIVERY FLOAT,
	TAKEOUT FLOAT,
	CREDITCARD FLOAT,
	GOODFOR FLOAT,
	PARKING FLOAT,
	WHEELCHAIR FLOAT,
	GOODFORKIDS FLOAT,	
	GOODFORGROUPS FLOAT,
	ATTIRE FLOAT,
	AMBIENCE FLOAT,
	NOISELEVEL FLOAT,
	ALCOHOL FLOAT,
	OUTDOOR FLOAT,
	WIFI FLOAT,
	HASTV FLOAT,
	WAITERS FLOAT,
	CATERS FLOAT,
	MUSIC FLOAT,
	HAPPYHOURS FLOAT,
	BESTNIGHTS FLOAT,
	COATCHECK FLOAT,
	SMOKING FLOAT,
	DRIVETHRU FLOAT, 
	DOGSALLOWED FLOAT,	
	DANCING FLOAT
	)"""
 

c.execute(sql)

def webscrapper(url):
	page=urllib2.urlopen(url) 
	soup = BeautifulSoup(page.read()) 
	bars=soup.findAll('a','biz-name') 

	for eachbar in bars: 
		bar_url= "http://www.yelp.com"+ eachbar['href']  
		org_url=urllib2.urlopen(bar_url) 
		soup1=BeautifulSoup(org_url.read()) 
		# get the address of bars
		def get_address(spans, itemprop):
			address = ""
			addresses = [span.contents for span in spans if span.get("itemprop")==itemprop]
			if len(addresses)>0: 
				address = addresses[0][0]
			return address
		dts = soup1.findAll('dt')
		# get the price / price change
		def get_price(dts, TextInfo):
			for dt in soup1.findAll('dt',{"attribute-key"}):
				info=dt.contents[0]
				textinfo=info
				dds = soup1.findAll('dd')
				for dd in dds:	
					content=dd.contents[0]
					bar_info=content.strip().lstrip("$")
					return bar_info	
		# get other business information
		def get_moredetail(divs, TextInfo):
			dts=soup1.findAll('dt')
			bar_info_q= []
			for dt in dts:
				content=dt.contents[0]
				bar_info=content.strip()
				bar_info_q.append(bar_info)
	
			dds = soup1.findAll('dd')
			bar_info_a=[]
			for dd in dds:	
				content=dd.contents[0]
				bar_info=content.strip()
				bar_info_a.append(bar_info)
			p1=zip(reversed(bar_info_q),reversed(bar_info_a))
			#print p1
			q=[]
			a=[]
			for x,y in p1:
				
				q=x
				a=y
				if x==TextInfo:
					if not a:
						a = "No"
					#print a
					return a
		
		# get all details
		def get_detail(detail):
			g_name=""
			g_description=""
			g_lattitude=""
			g_longitude=""
		
			bar_name=soup1.findAll('meta',{'property':'og:title'})
			bar_longitude=soup1.findAll('meta',{'property':'place:location:longitude'})
			bar_latitude=soup1.findAll('meta',{'property':'place:location:latitude'})
			bar_description=soup1.findAll('meta',{'property':'og:description'})
		
			if len(detail)>0:
				for eachbar_name in bar_name:
					g_name=eachbar_name['content']
				for eachbar_longitude in bar_longitude:
					g_longitude=eachbar_longitude['content']
				for eachbar_lattitude in bar_latitude:
					g_lattitude=eachbar_lattitude['content']
				for eachbar_description in bar_description:
					g_description=eachbar_description['content']
			
			return g_name, g_description,g_lattitude,g_longitude
		
		review_tag  = {'itemprop':re.compile("description")}
		all_reviews = soup1.findAll(attrs=review_tag)
		review_list=[]
		for text in all_reviews:
			if soup1.findAll('meta',{'content':'5.0'}):
				review= ''.join(text.findAll(text=True)).strip()
				review_list.append(review)
		review = review_list
		# clean data
		def clean_content(contents):
			content = " ".join(contents)
			content = content.split()
			content = content
			return " ".join(content)
		
		newreview = clean_content(review).encode('ascii',errors='ignore')
		
		# remove accents
	   	def remove_accents(input_str):
			new= ''.join( c for c in input_str if  c not in '?:!/;&#\@$%^*~",.<>(){}[]-=+' )
			new=new.replace("'", "")
			new="".join(i for i in new if ord(i)<128)
			return new.lower()
		new_review=remove_accents(newreview)
		spans = soup1.findAll('span')
		dds = soup1.findAll('dd')	
	
		oldname, description, lattitude, longitude =get_detail('detail')
		name=remove_accents(oldname)
		telephone = get_address(spans, "telephone")
		street = get_address(spans, "streetAddress")
		city = get_address(spans, "addressLocality")
		state = get_address(spans, "addressRegion")
		zipcode = get_address(spans, "postalCode")

		price_range = get_price(dts,"Price Range")
		reservations = get_moredetail(dts,"Takes Reservations")
		delivery = get_moredetail(dts,"Delivery")
		takeout = get_moredetail(dts,"Take-out")
		creditCard = get_moredetail(dts,"Accepts Credit Cards")
		goodfor = get_moredetail(dts,"Good For")
		parking = get_moredetail(dts,"Parking")
		wheelchair = get_moredetail(dts,"Wheelchair Accessible")
		goodforKids = get_moredetail(dts,"Good for Kids")
		goodforGroups = get_moredetail(dts,"Good for Groups")
		attire = get_moredetail(dts,"Attire")
		ambience = get_moredetail(dts,"Ambience")
		noiselevel = get_moredetail(dts,"Noise Level")
		music = get_moredetail(dts,"Music")
		dancing = get_moredetail(dts,"Good For Dancing")
		alcohol = get_moredetail(dts,"Alcohol")
		happyhours = get_moredetail(dts,"Happy Hour")
		bestnights = get_moredetail(dts,"Best Nights")
		coatcheck = get_moredetail(dts,"Coat Check")
		smoking = get_moredetail(dts,"Smoking")
		outdoor = get_moredetail(dts,"Outdoor Seating")
		wifi = get_moredetail(dts,"Wi-Fi")
		tv = get_moredetail(dts,"Has TV")
		waiter = get_moredetail(dts,"Waiter Service")
		drivethru = get_moredetail(dts,"Drive-Thru")
		caters = get_moredetail(dts,"Caters")
		dogsallowed = get_moredetail(dts,"Dog Allowed")
	
		category_tag  = {'itemprop':re.compile("child")}
		all_category = soup1.findAll(attrs=category_tag)
		category_list=[]
		for text in all_category:
			if soup1.findAll('span'):
				#category= ''.join(text.findAll(text=True)).strip()
				category= ''.join(text.findAll(text=True)).strip()
				category_list.append(category)
			
		categories = category_list
		category = clean_content(categories).encode('ascii',errors='ignore')
		category = category.lower()
		def unique_list(l):
			ulist = []
			[ulist.append(x) for x in l if x not in ulist]
			return ulist
		category=' '.join(unique_list(category.split()))
		street_address = street + ' ' + city + ', ' + state + ' ' + zipcode
		
		c.execute("INSERT INTO BARS  (name,description, telephone, address, lattitude,\
			longitude,category, review,price,reservations,delivery,takeout, creditCard, \
			goodfor, parking, wheelchair, goodforKids, goodforGroups, attire, ambience,\
			noiselevel, alcohol,outdoor, wifi, hastv, waiters, caters, music, happyhours, bestnights,\
			coatcheck, smoking, drivethru, dogsallowed, dancing) VALUES  \
			(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
			(name,description, telephone, street_address, lattitude,longitude, category, new_review, price_range, \
			reservations, delivery, takeout, creditCard, goodfor, parking, wheelchair, goodforKids, goodforGroups, attire,\
			ambience, noiselevel,alcohol, outdoor,wifi, tv, waiter, caters, music, happyhours,bestnights,\
			coatcheck, smoking, drivethru, dogsallowed, dancing))
		
		'''c.execute("INSERT INTO BARS  (name,description, telephone, address, lattitude,\
			longitude,category, review, price, goodforGroups, attire, ambience,\
			noiselevel, outdoor, hastv, music,\
			coatcheck, dancing) VALUES  \
			(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
			(name,description, telephone, street_address, lattitude,longitude, category, new_review, price_range, goodforGroups, attire,\
			ambience, noiselevel,outdoor, tv, music, \
			coatcheck,  dancing))'''
		con.commit()
	c.execute("DELETE FROM BARS WHERE name = ''	")
	con.commit()
	c.execute("SELECT NAME, CATEGORY,\
				AMBIENCE, NOISELEVEL, OUTDOOR, HASTV, MUSIC, \
				COATCHECK, DANCING	from BARS")
	for row in c:
		print row
	
	c.close
	
