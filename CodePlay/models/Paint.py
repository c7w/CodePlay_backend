import datetime
from django.db import models
from CodePlay.models import Accounts
from django.db.models.fields import BigAutoField

from CodePlay.models.Accounts import User

class Scheme(models.Model):
    id = models.BigAutoField(primary_key=True)
    submission_time = models.BigIntegerField(default=datetime.datetime.now().timestamp())
    sketch_id = models.IntegerField()
    name = models.TextField()
    description = models.TextField()
    likes = models.BigIntegerField(default=0)
    voted_people = models.ManyToManyField(Accounts.User, related_name='scheme_voted')
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    colors = models.TextField()

# Create Sketches manually
class Sketch(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    colors = models.IntegerField()
    data = models.TextField()
    hidden = models.BooleanField(default=False)
    defaultValue = models.TextField()