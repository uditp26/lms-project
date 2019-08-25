from django.db import models         
from phonenumber_field.modelfields import PhoneNumberField                  
from adminhome.validators import validate_file_extension  
from adminhome.models import School, Teacher, Student
import os

def get_upload_path(instance, filename):
    path = 'media/' + instance.assigned_by.school.school_code
    # name =  instance.first_name + '_' + instance.last_name + '/'
    rel_dir = ''
    
    if type(instance) == Assignment:
        path += '/Assignment/' + str(instance.class_number)+'/' + str(instance.subject)+'/' + str(instance.assign_number)+'/'
        rel_dir = '/Assignment/' + str(instance.class_number)+'/' + str(instance.subject)+'/' + str(instance.assign_number)+'/'

    os.makedirs(os.path.join(path), exist_ok=True)
    rel_path = instance.school.school_code + rel_dir
    return os.path.join(rel_path, filename)

class Assignment(models.Model):
    class_number = models.IntegerField()
    subject = models.CharField(max_length = 30)
    assigned_by = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    assign_number = models.IntegerField(default=0)
    start_date = models.DateField()
    due_date = models.DateField()
    assignement_file = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension])

    def __str__(self):
        return str(self.class_number) + '/ ' + self.subject + '/ ' + str(self.assign_number) +'/ '+ str(self.due_date)
                                                        
class ClassAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    roll_number = models.CharField(max_length = 30)
    name = models.CharField(max_length = 30)
    is_present = models.BooleanField()
    def __str__(self):
        return self.roll_number + '  '+  self.name + '  ' + self.is_present

# The structure of the below table is not appropriately defined.(Just for testing :) ) 
class SendAttendance(models.Model):
    roll_number = models.CharField(max_length = 1000)
    email_id = models.CharField(max_length = 50)
    attendance_message = models.CharField(max_length = 1000)
    def __str__(self):
        return self.roll_number + ' ' +self.email_id

class SendMessage(models.Model):
    roll_number = models.CharField(max_length = 1000)
    email_id = models.CharField(max_length = 50)
    report_message = models.CharField(max_length = 1000)
    def __str__(self):
        return self.roll_number + ' ' +self.email_id

class SendResult(models.Model):
    roll_number = models.CharField(max_length = 1000)
    email_id = models.CharField(max_length = 50)
    result = models.FileField()
    def __str__(self):
        return self.roll_number + ' ' +self.email_id
                                                    