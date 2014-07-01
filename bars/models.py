from django.db import models

class Bars(models.Model):
	old_bars = models.CharField(max_length=50)
	new_city = models.CharField(max_length=50)
	dist_miles=models.IntegerField(max_length=10)
	
	def __unicode__(self):
		return self.old_rest
		
