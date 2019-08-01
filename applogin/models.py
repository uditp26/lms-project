from django.db import models

from django.urls import reverse

class Admin(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250) 
    
    def __str__(self):
        return self.username

class Principal(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250)  

    def __str__(self):
        return self.username

class Teachers(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250)

    def __str__(self):
        return self.username

class Students(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250)

    def __str__(self):
        return self.username

class Parents(models.Model):
    username = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250)

    def __str__(self):
        return self.username
    
class User(models.Model):
    # username = models.CharField(max_length = 250) 
    # email = models.CharField(max_length = 250)
    # password = models.CharField(max_length = 250) 
    a_obj = Admin()
    p_obj = Principal()

    name = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 250) 
    school_name = models.CharField(max_length = 500)
    school_address_line_1 = models.CharField(max_length = 1000) 
    line_2 = models.CharField(max_length = 1000)

    city = models.CharField(max_length = 100)
    district = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    principal_name = models.CharField(max_length = 100)
    principal_email = models.CharField(max_length = 100)

    def get_absolute_url(self):
        return reverse('applogin:login')