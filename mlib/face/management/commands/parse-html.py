# -*- coding: utf-8 -*-
"""
Parse html pages and merge them into database
"""

from django.core.management.base import BaseCommand, CommandError
from face.models import Book
import re

def html_to_text(html):
    return html

def parse_book(books_path, index):
    """ Merge one book """
    dir_name = str(index % 256)
    file_name = books_path + '/' + dir_name + '/book.' + str(index)
    contents = open(file_name, 'r').read().decode('cp1251')
    matches = re.finditer("<b>(.*?)</b>(.*?)<br><br>", contents)
    for match in matches:
        key = match.group(1).strip()
        if key == u"Название:":
            title = html_to_text(match.group(2))
        elif key == u"Авторы:":
            authors = html_to_text(match.group(2))
        elif key == u"Авторы:":
            authors = html_to_text(match.group(2))
        elif key == u"ed2k:":
            ed2k_link = html_to_text(match.group(2))

        print title, authors, ed2k_link


class Command(BaseCommand):
    """ Django command """

    args = '<books_path>'
    help = 'Parse html pages and merge them into database'

    def handle(self, *args, **options):
        """ Command handler """
        if not args or not args[0]:
            raise CommandError('Books path does not specified')

        books_path = args[0]
        book_count = 0
        for i in xrange(1, 150000):
            parse_book(books_path, i)

        """
            srch = Book.objects.filter(ed2k_hash=ed2k_hash)
            if not srch:
                print "Loading", ed2k_hash
                try:
                    book = Book(
                            num=0,
                            file_name=file_name,
                            ed2k_hash=ed2k_hash)
                    book.save()
                    book_count += 1
                except BaseException as exc:
                    print "Problem with book:"
                    print exc
                    print '----------------------'
            else:
                print "Exists:", srch[0]
        """
        self.stdout.write('Successfully parsed "%d"' % book_count)
