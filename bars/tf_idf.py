from sqlite3 import *
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
import os
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from pygeocoder import Geocoder

regex = re.compile('[%s]' % re.escape(string.punctuation))
client = MongoClient
exclude = set(string.punctuation)
sw = set(stopwords.words('english'))
stemmer = nltk.PorterStemmer()

def tf_idf(review1, review2):
	def get_tokens(document):
		#remove the punctuation using the character deletion step of translate
		#no_punctuation = document.translate(None, string.punctuation)
		tokens = nltk.word_tokenize(document)
		return tokens

	def tokenize(text):
		tokens = nltk.word_tokenize(text)
		stems = stem_tokens(tokens, stemmer)
		return stems
	
	def stem_tokens(tokens, stemmer):
		stemmed = []
		for item in tokens:
			stemmed.append(stemmer.stem(item))
		return stemmed

	#document1 = ("I think this is one of the higher crazy selection end Chinese restaurants in Michigan, one of the best that I've ever been to in the US. The seating is great, with professional waiters and waitresses. My boyfriend and I went to this place to have a taste of their famous Peking Duck, and the dish turned out to be really amazing! I like how they came to your desk and serve directly to your plate for the first round, and the second round comes out very quickly too. The shrimp dumplings are great too, much better than the usual ones you may get at a Dim Sun place. Of course the price is a bit higher too. ")
	#document2 = ("Yummms.coms!! This is some good Chinese food!! They have a full bar, great selection super good location right by my house. My only issue is cost...beer is like 8 bucks and they did not have my favorite the night I was there and it's was a Saturday night. Look I know this is not Chicago...I should not hold them to that standard but dang....Chinese bar should have Tsingtao coming out of their ears on Saturdays. ")	
	#print document1
	#token1 = get_tokens(document1.lower()) 
	#token2 = get_tokens(document2.lower()) 
	#print token1
	token1 = get_tokens(review1) 
	token2 = get_tokens(review2) 
	count1 = Counter(token1)
	#count1=Counter(review1)
	#count2=Counter(review2)
	#print count1.most_common(10)
	count2 = Counter(token2)
	#print count2.most_common(10)
	#print "\n"

	filtered1 = [w for w in token1 if not w in stopwords.words('english')]
	count_filter1 = Counter(filtered1)
	#print count_filter1.most_common(10)
	filtered2 = [w for w in token2 if not w in stopwords.words('english')]
	count_filter2 = Counter(filtered2)
	#print count_filter2.most_common(10)
	#print "\n"

	stemmer = PorterStemmer()
	stemmed1 = stem_tokens(filtered1, stemmer)
	stemmed2 = stem_tokens(filtered2, stemmer)
	count_stem1 = Counter(stemmed1)
	count_stem2 = Counter(stemmed2)
	
	stemmed1=' '.join(stemmed1)
	stemmed2=' '.join(stemmed2)
	#print stemmed1
	#print stemmed2
	documents=[stemmed1,stemmed2]
	tfidf_vectorizer = TfidfVectorizer()
	tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
	#print tfidf_matrix.shape

	#print cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
	return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
	

if __name__ == '__main__':
	document1 = ("I think this is one of the higher crazy selection end Chinese restaurants in Michigan, one of the best that I've ever been to in the US. The seating is great, with professional waiters and waitresses. My boyfriend and I went to this place to have a taste of their famous Peking Duck, and the dish turned out to be really amazing! I like how they came to your desk and serve directly to your plate for the first round, and the second round comes out very quickly too. The shrimp dumplings are great too, much better than the usual ones you may get at a Dim Sun place. Of course the price is a bit higher too. ")
	document2 = ("Yummms.coms!! This is some one of the best good Chinese food!! They have a full bar, great selection super good location right by my house. My only issue is cost...beer is like 8 bucks and they did not have my favorite the night I was there and it's was a Saturday night. Look I know this is not Chicago...I should not hold them to that standard but dang....Chinese bar should have Tsingtao coming out of their ears on Saturdays. ")	
	print tf_idf(document1, document2)
    #print tf_idf("Review1", "Review2")
