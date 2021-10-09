import datetime
from django.db import models

class User(models.Model):
    student_id = models.BigIntegerField(primary_key=True)
    name = models.TextField()
    fullname = models.TextField()
    email = models.TextField()
    role = models.TextField(default="User") # User or Designer

# Hold all sessions
class SessionPool(models.Model):
    sessionId = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expireAt = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=3))
