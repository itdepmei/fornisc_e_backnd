from rest_framework import serializers
from .models import *


class IncidentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentImage
        fields = '__all__'

class IncidentSerializer(serializers.ModelSerializer):
        uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
        images = IncidentImageSerializer(many=True, read_only=True)


        class Meta:
            model = Incident
            fields = '__all__'




class IncidentStatisticsSerializer(serializers.Serializer):

    incident_type = serializers.CharField()
    count = serializers.IntegerField()



class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

class InspectionFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionForm
        fields = '__all__'



