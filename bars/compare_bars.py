from sqlite3 import * 
from lxml import etree 
#from __future__ import division
import pymongo
from pymongo import MongoClient
import unicodedata
import nltk, re, pprint
import string
from nltk.corpus import stopwords
from string import punctuation
from string import maketrans
import requests
import urllib2
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from pygeocoder import Geocoder
import tf_idf
import numpy as np
from operator import itemgetter, attrgetter

import getDistance
#from django.core.management import setup_environ
#from django.contrib.auth.models import User

#import settings
#from models import *

#setup_environ(settings)

regex = re.compile('[%s]' % re.escape(string.punctuation))
client = MongoClient
exclude = set(string.punctuation)
sw = set(stopwords.words('english'))
stemmer = nltk.PorterStemmer()
word_match=([
("Bars Dive Bars Dive Bars Music Venues Music Venues", "Bars Dive Bars Dive Bars Burgers"), 
("Bars Dive Bars Dive Bars Music Venues Music Venues", "Bars Pubs Pubs"), 
("Bars Pubs Pubs", "Bars Dive Bars Dive Bars Burgers"), 
("German Bars Pubs Pubs", ), 
("american (new)", "pubs"), 
("pubs", "dive bars"),
("bars lounges lounges","bars lounges lounges dance clubs"),
("bars lounges lounges lounges","bars lounges lounges"),
("bars lounges lounges lounges","bars lounges lounges dance clubs"),
("bars pubs pubs american (new)","bars"),
("pubs","bars pubs pubs american (new)"),
("bars lounges lounges","bars"),
("lounges","bars lounges lounges"),
("bars lounges lounges lounges","bars lounges lounges")])



def clean_content(contents):
	content = " ".join(contents)
	content = content.split()
	return " ".join(content)
def any(seq):
	for s in seq:
		if s:
			return True
		return False

def compare_bars(bar,lat1,lon1,miles):
	con = connect("bar_data_test.db") 
	c1 = con.cursor()
	print bar
	review11=c1.execute("SELECT REVIEW FROM BARS WHERE name like '%s' " %bar)
	review1=c1.fetchone()
	#print review1
	for review in review1:
		r1=review
	
		#print r1
	old_category1=c1.execute("SELECT CATEGORY FROM BARS WHERE name like '%s'" %bar)
	old_category=c1.fetchone()
	c=[category_new for category_new in old_category]

	c=clean_content(c).lower()
	print c
#**************	
	def unique_list(l):
		ulist = []
		[ulist.append(x) for x in l if x not in ulist]
		return ulist
	
	comp=' '.join(unique_list(c.split()))
	comp = comp.split()
	categry_match=[]
	comp_list=[]
	sort_before=[]
	length=''
	#print comp
	def words_in_string(word_list, a_string):
		return set(word_list).intersection(a_string.split())
	rows = c1.execute("SELECT NAME, CATEGORY	from BARS ")
	for row in rows:
		print row[1]
		i=0
		for word in words_in_string(comp, row[1]):
			print(word)
			i+=1
		categry_match.append([i,row[0]])
	categry_match.sort(key=lambda x: x[0], reverse=True)
	j=0
	while j<5:
		bar_match = categry_match[j][1]
		review22=c1.execute("SELECT REVIEW FROM BARS WHERE NAME like '%s'" %bar_match)
		review2=c1.fetchall()
		for review in review2:
			r2=clean_content(review)	
			#print r1,r2
		compare_bar=tf_idf.tf_idf(r1,r2)[0]
		comp_list.append(compare_bar[1])
		sort_before.append(bar_match)
		j+=1
	comp=comp_list	
	bar_list=sort_before
	bars=[]	
	p=zip(comp,bar_list)
	#print p
	x=sorted(p, key=itemgetter(0),reverse=True)
	print x

	c1.execute('DROP TABLE IF EXISTS BAR_MATCH')
	con.commit()
	sql="""CREATE TABLE `BAR_MATCH` (
			NAME  TEXT,
			LATTITUDE TEXT,
			LONGITUDE TEXT
			)"""


	c1.execute(sql)
	
	for row in x:
		bars=row[1]
		y11=c1.execute("SELECT NAME, ADDRESS FROM BARS WHERE NAME like '%s'" %bars)
		y=c1.fetchall()
		
		for y1 in y:
			print y1
			lattitude, longitude = getDistance.findLocation(y1[1]) 
			print lattitude, longitude
			c1.execute("insert into BAR_MATCH values (?,?,?)",(y1[0],longitude, lattitude))
			con.commit()
