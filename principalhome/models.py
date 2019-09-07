from django.db import models
from adminhome.models import Principal

class Announcement(models.Model):
    announcer = models.ForeignKey(Principal, on_delete=models.CASCADE)
    subject = models.CharField(max_length = 100)
    announcement_date = models.DateField()
    expiry_date = models.DateField()
    audience = models.CharField(max_length = 20)
    message = models.TextField()

    def __str__(self):
        return self.subject[:20]
