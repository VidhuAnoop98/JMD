from rest_framework import serializers
from .models import *

class CustomerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInformation
        fields = '__all__'

class JobNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobNumber
        fields = '__all__'

class JobItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobItems
        fields = '__all__'

class anodising_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobItems
        fields = ['anodising_type']

class thicknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobItems
        fields = ['thickness']

class colorSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobItems
        fields = ['color_finish']

class process_chargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobItems
        fields = ['process_charges']

class materialSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobItems
        fields = ['material']

class totalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobItems
        fields = ['Total','area','material']

class calculateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobItems
        fields = ['Total','area','material']
        
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'