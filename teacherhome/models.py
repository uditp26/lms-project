from django.db import models

class Assignment(models.Model):
    class_number = models.IntegerField()
    subject = models.CharField(max_length = 50)
    start_date = models.DateField()
    due_date = models.DateField()
    assignement_file = models.FileField()

    def __str__(self):
        return str(self.class_number) + ' ' + self.subject + ' ' + str(self.due_date)


class ClassAttendance(models.Model):
    roll_number = models.CharField(max_length= 50)
    is_present = models.BooleanField()
    def __str__(self):
        return self.roll_number + ' ' + self.is_present

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

