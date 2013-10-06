from django.db import models

class Book(models.Model):
    num = models.IntegerField()
    author1 = models.CharField(max_length=80)
    author2 = models.CharField(max_length=80)
    author3 = models.CharField(max_length=80)
    title = models.CharField(max_length=300)
    year =  models.CharField(max_length=4)
    publication = models.CharField(max_length=100)
    file_name = models.CharField(max_length=30)
    ed2k_hash = models.CharField(max_length=32)
    language =  models.CharField(max_length=2)

    def authors(self):
        authors = self.author1
        if self.author2:
            authors += ', ' + self.author2
        if self.author3:
            authors += ', ' + self.author3
        return authors

    def __unicode__(self):
        result = self.authors()
        if result:
            result += '. '
        result += self.title
        return result
