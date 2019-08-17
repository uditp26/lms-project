from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    school_code = models.CharField(max_length=20)
    school_admin = models.OneToOneField(User, on_delete=models.CASCADE)
    is_registered = models.BooleanField(default=False)

    school_name = models.CharField(max_length=200)
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
    joining_date = models.DateField()
    is_class_teacher = models.BooleanField(default=False)
    resume = models.FileField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Principal(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    joining_date = models.DateField()
    is_teacher = models.BooleanField(default=False)
    resume = models.FileField()
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Parent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    parent_of = models.ForeignKey(Student, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
