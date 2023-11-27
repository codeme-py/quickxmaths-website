from django.db import models

class CoreSetting(models.Model):
	#time_to_execute = models.TimeField()
	instagram = models.CharField(max_length=1000, null=True)
	facebook = models.CharField(max_length=1000, null=True)
	twitter = models.TextField(null=True)
	def __str__(self):
		return 'CoreSettings'
