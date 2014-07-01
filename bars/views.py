from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "bars/index.html")
    
def city(request):    
	return render(request, "bars/city.html")
    
def about(request):
	return render(request, "bars/about.html")

def contact(request):
	return render(request, "bars/contact.html")

def maps(request):
	if 'bar' in request.GET and 'zipcode' in request.GET and 'miles' in request.GET:
		restaurant=request.GET['bar']
		zipcode=request.GET['zipcode']
		miles=request.GET['miles']
		message = 'You entered bar: %r and city : %r ' % (bar, zipcode)
		return render(request,'bars/maps.html',{'bar':bar,'zipcode':zipcode,'miles':miles})
	else:
		return HttpResponse('You submitted an empty form.')
    
# Create all your page views here.