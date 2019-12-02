from django.db import models         
from phonenumber_field.modelfields import PhoneNumberField                  
from adminhome.validators import validate_file_extension  
from adminhome.models import School, Teacher, Student
import os

##dont delete
# def get_upload_path(instance, filename):
#     path = 'media/' + instance.school.school_code
#     # name =  instance.first_name + '_' + instance.last_name + '/'
#     rel_dir = ''
    
#     if type(instance) == Assignment:
#         path += '/Assignment/' + str(instance.class_number)+'/' + str(instance.subject)+'/'  #+ str(instance.assign_number)+'/'
#         rel_dir = '/Assignment/' + str(instance.class_number)+'/' + str(instance.subject)+'/' # + str(instance.assign_number)+'/'

#     os.makedirs(os.path.join(path), exist_ok=True)
#     rel_path = instance.school.school_code + rel_dir

#     format1 = str(instance.subject) + str(instance.assign_number) + '.pdf'
#     return os.path.join(rel_path, format1)

def get_upload_path(instance, filename):
    path = 'media/' + instance.school.school_code
    name = str(instance.school.school_code)+"_"
    rel_dir = ''
    
    if type(instance) == Assignment:
        path += '/Teachers/'+ str(instance.assigned_by).replace(' ','_') +'/Assignment/'
        rel_dir = '/Teachers/'+ str(instance.assigned_by).replace(' ','_') +'/Assignment/'
        name += str(instance.class_number)+'/' + str(instance.subject)+'/'
    rel_path = instance.school.school_code + rel_dir
    format1 = str(name) + str(instance.subject) + str(instance.assign_number) + '.pdf'
    format1 = format1.replace("/",'_')
    format1 = format1.split('_')
    format2 = str(format1[1])+'_'+str(format1[2])+'_'+str(format1[3])
    return os.path.join(rel_path, format2)

class Assignment(models.Model):
    class_number = models.IntegerField()
    subject = models.CharField(max_length = 30)
    assigned_by = models.CharField(max_length = 30)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING)
    assign_number = models.IntegerField()
    start_date = models.DateField()      
    due_date = models.DateField()
    assignment_file = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension])
    
    def __str__(self):
        # assignment = str(self.assignment_file).replace("/","_").split(".")[0]
        # return str(assignment.replace(" ","_"))
        return str(str(self.assignment_file).replace("/","_").split(".")[0]+'_____'+str(self.assigned_by).replace(' ','_'))

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