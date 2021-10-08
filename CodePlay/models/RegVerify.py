from datetime import datetime
from django.db import models
import django

class RegVerify(models.Model):
    email = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    createdAt = models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return "%s : %s Created at (%s)" % (self.email, self.code, str(self.createdAt))

class PassReset(models.Model):
    email = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    createdAt = models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return "%s : %s Created at (%s)" % (self.email, self.code, str(self.createdAt))
