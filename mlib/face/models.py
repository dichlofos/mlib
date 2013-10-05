from django.db import models

class Book(models.Model):
    num = models.IntegerField()
    author1 = models.CharField(max_length=50)
    author2 = models.CharField(max_length=50)
    author3 = models.CharField(max_length=50)
    title = models.CharField(max_length=200)

    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

