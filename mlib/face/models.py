""" face models """
from django.db import models

import re

BOOK_ROOT = '/b'

class Book(models.Model):
    """ Book """

    num = models.IntegerField()
    author1 = models.CharField(max_length=80, db_index=True)
    author2 = models.CharField(max_length=80)
    author3 = models.CharField(max_length=80)
    title = models.CharField(max_length=300)
    year =  models.CharField(max_length=4)
    publication = models.CharField(max_length=100)
    file_name = models.CharField(max_length=30)
    ed2k_hash = models.CharField(max_length=32, db_index=True)
    language =  models.CharField(max_length=2)

    def authors(self):
        """ Get authors list as single string """
        authors = self.author1
        if self.author2:
            authors += ', ' + self.author2
        if self.author3:
            authors += ', ' + self.author3
        return authors

    def path(self):
        """ Get book path related to Lib folder """
        return self.file_name[0:6] + '/' + self.file_name

    def link(self):
        return BOOK_ROOT + '/' + self.path()

    def download_link(self):
        return 'download/' + str(self.id)

    def ext(self):
        return re.sub(r'.*\.', '', self.file_name)

    def __unicode__(self):
        result = self.authors()
        if result:
            result += ' '
        result += self.title + ' '
        if self.year:
            result += '[' + self.year + '] '

        return result
