from django.db import models

class LocalAdmin(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    joining_date = models.DateField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    admission_date = models.DateField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    joining_date = models.DateField()
    is_class_teacher = models.BooleanField()
    resume = models.FileField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Principal(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    joining_date = models.DateField()


    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Parent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name