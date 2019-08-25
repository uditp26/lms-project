from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_file_extension
import os

def get_upload_path(instance, filename):
    path = 'media/' + instance.school.school_code
    name =  instance.first_name + '_' + instance.last_name + '/'
    rel_dir = ''

    if type(instance) == Teacher:
        path += '/Teachers/'
        rel_dir = '/Teachers/'
    elif type(instance) == Principal:
        path += '/Principal/'
        rel_dir = '/Principal/'
    os.makedirs(os.path.join(path, name), exist_ok=True)
    rel_path = instance.school.school_code + rel_dir + name
    return os.path.join(rel_path, filename)

class School(models.Model):
    school_code = models.CharField(max_length=20)
    school_admin = models.OneToOneField(User, on_delete=models.CASCADE)
    is_registered = models.BooleanField(default=False)
    has_principal = models.BooleanField(default=False)

    school_name = models.CharField(max_length=200)
    class_upto = models.PositiveIntegerField(null=True)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length = 50)
    district = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    # filling address fields based on pincode
    pincode = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.school_name


class LocalAdmin(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    joining_date = models.DateField()
    school = models.OneToOneField(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Student(models.Model):
    enrolment_no = models.CharField(max_length=20)
    roll_no = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    admission_date = models.DateField()
    study = models.PositiveIntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    
    # email = models.OneToOneField(User, on_delete=models.CASCADE)
    
    joining_date = models.DateField()
    is_class_teacher = models.BooleanField(default=False)
    subject = models.CharField(max_length=100, null=True)
    resume = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension])
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Principal(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    joining_date = models.DateField()
    is_teacher = models.BooleanField(default=False)
    subject = models.CharField(max_length=100, null=True)
    resume = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension])
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Parent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    parent_of = models.ForeignKey(Student, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name