import datetime
from django.db import models
from django.db.models.fields import BigAutoField

from CodePlay.models.Accounts import User

class Scheme(models.Model):
    id = models.BigAutoField(primary_key=True)
    submission_time = models.BigIntegerField(default=datetime.datetime.now().timestamp())
    sketch_id = models.IntegerField()
    name = models.TextField()
    description = models.TextField()
    likes = models.BigIntegerField(default=0)
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    colors = models.TextField()
