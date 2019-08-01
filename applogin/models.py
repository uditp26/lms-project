from django.db import models

from django.urls import reverse

class Admin(models.Model):
    username = models.CharField(max_length = 100) 
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100) 
    
    def __str__(self):
        return self.username

class Principal(models.Model):
    username = models.CharField(max_length = 100) 
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)  

    def __str__(self):
        return self.username
    
class School(models.Model):
    name = models.CharField(max_length = 250) 
    email = models.CharField(max_length = 100) 
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

    def __str__(self):
        return self.school_name