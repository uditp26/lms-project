from django.db import models

# from django.contrib.auth.models import User
from applogin.models import User

from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_file_extension
import os

def get_upload_path(instance, filename):
    return 'resume/' + 'user_{0}/{1}'.format(instance.user.id, filename)

def get_upload_path_feeCircular(instance, filename):
    return 'fee_circulars/' + 'school_admin_{0}/{1}'.format(instance.school_admin.id, filename)

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
        return self.school_code


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrolment_no = models.CharField(max_length=20)
    roll_no = models.CharField(max_length=20)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    address = models.TextField(max_length=500)
    admission_date = models.DateField()
    study = models.PositiveIntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def name_to_url(self):
        return self.first_name + '-' + self.last_name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    address = models.TextField(max_length=500)
    joining_date = models.DateField()
    is_class_teacher = models.BooleanField(default=False)
    class_teacher_of = models.IntegerField(null=True)
    subject = models.CharField(max_length=100, null=True)
    resume = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension])
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def name_to_url(self):
        return self.first_name + '-' + self.last_name

class Principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    address = models.TextField(max_length=500)
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

class Feecircular(models.Model):
    ref_no = models.CharField(max_length=20)
    school_admin = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_issue = models.DateField()
    file_name = models.CharField(max_length=100)
    pdf_ver = models.FileField(upload_to=get_upload_path_feeCircular, validators=[validate_file_extension])

    def __str__(self):
        return self.ref_no
    