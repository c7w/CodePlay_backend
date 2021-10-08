from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=127)
    time = models.DateTimeField()
    content = models.TextField()
    
    def __str__(self):
        return self.title
    

class SearchRecord(models.Model):
    email = models.CharField(max_length=255)
    record = models.CharField(max_length=255)
    fuzzy = models.BooleanField()
    time = models.DateTimeField()
    
    def __str__(self):
        return self.record
