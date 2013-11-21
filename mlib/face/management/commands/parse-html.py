# -*- coding: utf-8 -*-
"""
Parse html pages and merge them into database
"""

from django.core.management.base import BaseCommand, CommandError
from face.models import Book
import re
import sys

import lxml.html


def html_to_text(html):
    """ Translate html to plain text """
    if html is None:
        return ''
    html = html.strip()
    if html == '':
        return ''
    text = lxml.html.fromstring(html)
    content = text.text_content()
    if content is None:
        content = ''
    return content


def parse_book(books_path, index):
    """ Merge one book """
    dir_name = str(index % 256)
    file_name = books_path + '/' + dir_name + '/book.' + str(index)
    contents = open(file_name, 'r').read().decode('cp1251')
    matches = re.finditer("<b>(.*?)</b>(.*?)<br><br>", contents)
    print str(index) + ": [ " + file_name + " ]"

    authors = ''
    title = ''
    year = ''
    publication = ''
    ed2k_link = ''

    for match in matches:
        key = match.group(1).strip()
        if key == u"Название:":
            title = html_to_text(match.group(2))
        elif key == u"Авторы:":
            authors = html_to_text(match.group(2))
        elif key == u"Год издания:":
            year = html_to_text(match.group(2))
        elif key == u"Издание:":
            publication = html_to_text(match.group(2))
        elif key == u"ed2k:":
            ed2k_link = match.group(2)

    author_list = []
    if authors:
        author_list = authors.split(',')

    while len(author_list) < 3:
        author_list.append('')

    for author in author_list:
        if author:
            author = author.strip()

    ed2k_hash = ''

    if ed2k_link:
        hash_match = re.search("hash=([0-9a-f]+)", ed2k_link)
        if hash_match is not None:
            ed2k_hash = hash_match.group(1)
        else:
            print "ed2k error: ", ed2k_link
    if not ed2k_hash:
        print "Hash not found on page, cannot merge"
        return (0, 1, 0, 0)

    srch = Book.objects.filter(ed2k_hash=ed2k_hash)
    if not srch:
        print "Unknown ed2k hash:", ed2k_hash
        return (0, 0, 1, 0)

    #print srch
    book = srch[0]
    if book.num != 0:
        return (0, 0, 0, 1)

    print "Merging", ed2k_hash

    # apply some fixups
    if index == 94131:
        year = 1951
    elif index == 111029:
        year = 1989

    try:
        book.num = unicode(index)
        book.author1 = unicode(author_list[0])
        book.author2 = unicode(author_list[1])
        book.author3 = unicode(author_list[2])
        book.title = unicode(title)
        book.year = unicode(year)
        book.publication = unicode(publication)
        book.save()
    except BaseException as exc:
        print "Problem with book:"
        print exc
        print '----------------------'
        print index, year
        print 'Import FAILED'

        sys.exit(1)

    return (1, 0, 0, 0)


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
        no_hash_count = 0
        unk_hash_count = 0
        already_count = 0

        for i in xrange(111029, 122528):
            good, no_hash, unk_hash, already = parse_book(books_path, i)
            book_count += good
            no_hash_count += no_hash
            unk_hash_count += unk_hash
            already_count += already

        self.stdout.write(
            'Successfully parsed %d book(s)\n' \
            'Already done %d book(s)\n' \
            'No hash found in %d book(s)\n' \
            'Unknown hash in %d book(s)' % \
            (book_count, already_count,
            no_hash_count, unk_hash_count))
