from django.contrib import admin
from .models import School, LocalAdmin, Student, Teacher, Principal, Parent

admin.site.register(School)
admin.site.register(LocalAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Principal)
admin.site.register(Parent)
