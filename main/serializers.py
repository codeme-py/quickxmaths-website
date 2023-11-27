'''
from rest_framework import serializers
from .models import CoreSetting

class SDat(serializers.ModelSerializer):
	class Meta:
		model = CoreSetting
		fields = ['instagram', 'facebook', 'twitter']'''