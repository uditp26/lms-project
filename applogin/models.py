from django.db import models

from django.urls import reverse

class Admin(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250) 


class Principal(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250)  

class Teachers(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    models.CharField(max_length = 250)

class Students(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    models.CharField(max_length = 250)

class Parents(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    models.CharField(max_length = 250)
    
class User(models.Model):
    # username = models.CharField(max_length = 250) 
    # email = models.CharField(max_length = 250)
    # password = models.CharField(max_length = 250) 
    a_obj = Admin()
    p_obj = Principal()

    Name = models.CharField(max_length = 250) 
    Email = models.CharField(max_length = 250) 
    School_Name = models.CharField(max_length = 500)
    School_Address_Line_1 = models.CharField(max_length = 1000) 
    Line_2 = models.CharField(max_length = 1000)

    City = models.CharField(max_length = 100)
    District = models.CharField(max_length = 100)
    State = models.CharField(max_length = 100)
    Principal_Name = models.CharField(max_length = 100)
    Principal_Email = models.CharField(max_length = 100)

    # a_obj.username = Name
    # a_obj.email = Email

    # p_obj.username = Principal_Name
    # p_obj.email = Principal_Email