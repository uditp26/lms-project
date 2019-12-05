from django.db import models         
from phonenumber_field.modelfields import PhoneNumberField                  
from adminhome.validators import validate_file_extension  
from adminhome.models import School, Teacher, Student
import os

def get_upload_path(instance, filename):
    format2 = str(instance.class_number)+'_'+str(instance.subject)+'_'+str(instance.assign_number) + '.pdf'
    return 'assignments/'+'user_{0}/{1}'.format(instance.assigned_by.id,format2)

def get_upload_marksheet_path(instance, filename):
    format2 = 'class_'+str(instance.teacher.class_teacher_of)+'_'+'rollno_'+str(instance.roll_no)+ '.pdf'
    return 'marksheets/'+'user_{0}/{1}'.format(instance.teacher.id,format2)

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
    teacher = models.ForeignKey(Teacher, on_delete = models.DO_NOTHING)
    name = models.CharField(max_length=20)
    roll_no = models.CharField(max_length=20)
    marksheet_file = models.FileField(upload_to=get_upload_marksheet_path, validators=[validate_file_extension])
    date = models.DateField()

    def __str__(self):
        return str(str(self.marksheet_file).replace("/","_").split(".")[0])

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
