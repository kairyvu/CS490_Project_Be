from django.db import models

# Create your models here.

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country
    class Meta:
        db_table = "country"

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city
    class Meta:
        db_table = "city"

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address
    class Meta:
        db_table = "address"

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    class Meta:
        db_table = "customer"