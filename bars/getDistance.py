from geopy.distance import vincenty
from geopy.geocoders import GoogleV3
geolocator = GoogleV3()


def findDistance(lat1, lon1, lat2, lon2):
	current = (lat1, lon1)
	new = (lat2, lon2)
	d=vincenty(current, new).miles
	return d

def findLocation(location):
	address, (latitude, longitude) = geolocator.geocode(location)
	return (latitude, longitude)
	
#print findDistance(42.500851,-83.359439,42.3314,-83.0458)
#print findLocation("9 Doyers St New York, NY 10013")