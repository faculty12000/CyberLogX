from django.db import models

class LogFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='logs/')

    def __str__(self):
        return self.file.name
# Create your models here.
