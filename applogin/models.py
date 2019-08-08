from django.db import models

from django.urls import reverse

class LocalAdmin(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)

    joining_date = models.DateField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Register(models.Model):
    first_name = models.CharField(max_length = 50) 
    last_name = models.CharField(max_length = 50) 
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 200) 
    confirm_password = models.CharField(max_length = 200)
    is_school_registered = models.IntegerField()
    def get_absolute_url(self):
        return reverse('applogin:registerschool')
    def __str__(self):
        return self.first_name

class School(models.Model):
    school_name = models.CharField(max_length = 500)
    school_address_line_1 = models.CharField(max_length = 500) 
    line_2 = models.CharField(max_length = 500)
    city = models.CharField(max_length = 50)
    district = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)

    def get_absolute_url(self):
        return reverse('applogin:successful_reg')

    def __str__(self):
        return self.school_name

