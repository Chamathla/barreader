import json
import ast
import sqlite3
from sqlite3 import *
from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
import numpy as np
from pandas import DataFrame
import pandas
from sklearn import linear_model
from sklearn.externals import joblib
from pygeocoder import Geocoder
from bars.models import Bars


import compare_bars as cp
import getDistance



def hello(request):
	return render_to_response('bars/index.html')

def maps(request):
	lat1=[]
	lon1=[]
	if 'bar' in request.GET and 'zipcode' in request.GET and 'miles' in request.GET:
		bar=request.GET['bar']
		zipcode=request.GET['zipcode']
		miles=request.GET['miles']
		lattitude,longitude=getDistance.findLocation(zipcode)
		lat1=lattitude
		lon1=longitude
		cp.compare_bars(bar, lattitude,longitude,miles)
	con = connect("bar_data_test.db") 
	c = con.cursor()

	x1=c.execute("SELECT * FROM BAR_MATCH " )
	x=c.fetchall()
	bar=[]
	longitude=[]
	lattitude=[]
	distance=[]
	for y in x:
		i=1
		bars=y[0]
		longitudes=y[1]
		lattitudes=y[2]
		distances=getDistance.findDistance(lat1,lon1,lattitudes,longitudes)
		bar.append(bars)
		longitude.append(longitudes)
		lattitude.append(lattitudes)
		distance.append(distances)
		i+=1
	s= sorted(range(len(distance)), key=lambda k: distance[k])
	#print s[0]
	result={'bar_1':bar[s[0]],'bar_2':bar[s[1]],'bar_3':bar[s[2]],'bar_4':bar[s[3]],'bar_5':bar[s[4]],\
	'longitude_1':longitude[s[0]],'longitude_2':longitude[s[1]],'longitude_3':longitude[s[2]],'longitude_4':longitude[s[3]],'longitude_5':longitude[s[4]],\
	'lattitude_1':lattitude[s[0]],'lattitude_2':lattitude[s[1]],'lattitude_3':lattitude[s[2]],'lattitude_4':lattitude[s[3]],'lattitude_5':lattitude[s[4]]}
	print result
	return render(request,'bars/maps.html',result)


def bar(request):
    #Get input arguments
	bar = request.GET.get("bar")
	miles = request.GET.get("miles")
	zipcode = request.GET.get("zipcode")
	return result

def list_bars(bar,zipcode,miles):
	if 'bar' in request.GET and 'zipcode' in request.GET and 'miles' in request.GET:
		bar=request.GET['bar']
		zipcode=request.GET['zipcode']
		miles=request.GET['miles']

	else:
		return HttpResponse('You submitted an empty form.')

funcs = {
        "bars": list_bars
}

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3306)   
