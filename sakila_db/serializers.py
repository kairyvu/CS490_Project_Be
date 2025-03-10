from rest_framework import serializers

class UpdateCustomerSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=45)
    last_name = serializers.CharField(max_length=45)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=100)
    district = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=20)

class CreateCustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=45)
    last_name = serializers.CharField(max_length=45)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=100)
    district = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=20)
