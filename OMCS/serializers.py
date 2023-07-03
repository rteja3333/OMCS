from rest_framework import serializers
from .models import hospital,doctor,patient
 
class hospitalserializer(serializers.ModelSerializer):
    class Meta:
        model=hospital
        fields='__all__'

class doctorserializer(serializers.ModelSerializer):
    class Meta:
        model=doctor
        fields='__all__'


class patientserializer(serializers.ModelSerializer):
    class Meta:
        model=patient
        fields='__all__'
