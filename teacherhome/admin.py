from django.contrib import admin

from .models import Assignment, Attendance, Marksdetails

admin.site.register(Assignment)
admin.site.register(Attendance)
admin.site.register(Marksdetails)