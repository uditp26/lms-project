from django.contrib import admin

from .models import Assignment, ClassAttendance, SendAttendance, SendMessage, SendResult

admin.site.register(Assignment)
admin.site.register(ClassAttendance)
admin.site.register(SendAttendance)
admin.site.register(SendMessage)
admin.site.register(SendResult)