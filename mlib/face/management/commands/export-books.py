# -*- coding: utf-8 -*-
"""
Export books to external file
"""

from django.core.management.base import BaseCommand, CommandError
from face.models import Book
import uuid

BOOKS_DEST = '~/disk'
#BOOKS_SOURCE = '/storage/whiterose/libraries/lib.mexmat.ru/Lib'
BOOKS_SOURCE = '/home/mvel/disk/mlib'


def export_book(book, cat, script):
    """ Export one book """

    dest_root = BOOKS_DEST + '/lmr-books'

    dir_name = str(book.id % 512)
    command = 'mkdir -p ' + dest_root + '/' + dir_name
    script.write(command + '\n')
    download_name = str(uuid.uuid4()) + '.' + book.ext()
    html_path = dir_name + '/' + download_name

    #command = 'cp \'' + BOOKS_SOURCE + '/' + book.path() + \
    #   '\' ' + dest_root + '/' + html_path

    command = 'mv \'' + BOOKS_SOURCE + '/' + book.path() + \
        '\' ' + dest_root + '/' + html_path

    script.write(command + '\n')

    link = '<li><a href="%s">%s</a></li>' % (html_path, unicode(book))
    cat.write(link.encode('utf-8') + '\n')


class Command(BaseCommand):
    """ Django command """

    args = '<output_catalog> <copy_script>'
    help = 'Parse html pages and merge them into database'

    def handle(self, *args, **options):
        """ Command handler """
        if not args or len(args) < 2:
            raise CommandError('Output files were not specified')

        output_catalog = args[0]
        copy_script = args[1]

        cat = open(output_catalog, 'w')
        script = open(copy_script, 'w')

        script.write('#!/usr/bin/env bash\n')
        script.write('set -xe\n')

        cat.write(
            '<!DOCTYPE html>\n<html>\n' +
            '<head>\n<meta charset="utf-8"/>\n' +
            '<title>Some books</title>\n</head>\n<body>\n')

        for book in Book.objects.all():
            if book.num == 0:
                continue
            export_book(book, cat, script)

        cat.write('</body></html>\n')

        self.stdout.write(
            'Successfully exported catalogue to "{0}"\n'
            'Copy script is written to "{1}"\n'.format(
            output_catalog, copy_script))
