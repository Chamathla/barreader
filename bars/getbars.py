import web_scrapper

# get bars in Detroit MI
url_MI="http://www.yelp.com/search?find_desc=bars&find_loc=Detroit%2C+MI&ns"
web_scrapper.webscrapper(url_MI)
i=1
print i
while i<2:
	url="http://www.yelp.com/search?find_desc=bars&find_loc=Detroit%2C+MI&start="+str(10*i)
	web_scrapper.webscrapper(url)
	i+=1
	print i

# get bars in New York NY	
url_IL="http://www.yelp.com/search?find_desc=bars&find_loc=New+York%2C+NY&ns"
web_scrapper.webscrapper(url_IL)
i=1
print i+2
while i<2:
	url="http://www.yelp.com/search?find_desc=bars&find_loc=New+York%2C+NY&start="+str(10*i)
	web_scrapper.webscrapper(url)
	i+=1
	print i+2
	
