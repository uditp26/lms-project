from django.db import models         
from phonenumber_field.modelfields import PhoneNumberField                  
from adminhome.validators import validate_file_extension  
from adminhome.models import School, Teacher, Student
import os

def get_upload_path(instance, filename):
    path = 'media/' 
    name = ""
    if type(instance) == Assignment:
        path += 'assignments/user_' + str(instance.assigned_by.id) 
        name += str(instance.class_number)+'/' + str(instance.subject)+'/'

    format2 = str(instance.class_number)+'_'+str(instance.subject)+'_'+str(instance.assign_number) + '.pdf'
    return 'assignments/'+'user_{0}/{1}'.format(instance.assigned_by.id,format2)

class Assignment(models.Model):
    class_number = models.IntegerField()
    subject = models.CharField(max_length = 30)

    assigned_by = models.ForeignKey(Teacher, on_delete = models.DO_NOTHING)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING)
    assign_number = models.IntegerField()
    start_date = models.DateField()      
    due_date = models.DateField()
    assignment_file = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension])
    def __str__(self):
        return str(str(self.assignment_file).replace("/","_").split(".")[0])

class Attendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    study = models.PositiveIntegerField()
    absent_on = models.DateField()
    
    def __str__(self):
        return str(self.school) +' ' + str(self.absent_on) + ' ' + self.name

class Marksdetails(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    study = models.PositiveIntegerField()
    roll_no = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    half_yearly_marks = models.PositiveIntegerField(default=0, blank=True, null=True)
    final_marks = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return self.name

    def name_to_url(self):
        return self.study + '-' + self.roll_no

# The structure of the below table is not appropriately defined.(Just for testing :) ) 
# class SendAttendance(models.Model):
#     roll_number = models.CharField(max_length = 1000)
#     email_id = models.CharField(max_length = 50)
#     attendance_message = models.CharField(max_length = 1000)
#     def __str__(self):
#         return self.roll_number + ' ' +self.email_id

# class SendMessage(models.Model):
#     roll_number = models.CharField(max_length = 1000)
#     email_id = models.CharField(max_length = 50)
#     report_message = models.CharField(max_length = 1000)
#     def __str__(self):
#         return self.roll_number + ' ' +self.email_id

# class SendResult(models.Model):
#     roll_number = models.CharField(max_length = 1000)
#     email_id = models.CharField(max_length = 50)
#     result = models.FileField()
#     def __str__(self):
#         return self.roll_number + ' ' +self.email_id
