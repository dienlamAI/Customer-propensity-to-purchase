from rest_framework import serializers
from .models import *

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = '__all__'
 

class DataSerializer(serializers.Serializer):
    file = serializers.FileField()
    number = serializers.IntegerField()
    threading = serializers.IntegerField()