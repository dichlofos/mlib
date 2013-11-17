# -*- coding: utf-8 -*-
"""
Load ed2k hashes calculated on the files
using calc-ed2k.sh
"""

from django.core.management.base import BaseCommand, CommandError
from face.models import Book

class Command(BaseCommand):
    """ Django command """

    args = '<file_name>'
    help = 'Loads ed2k hashes calculated on files using calc-ed2k.sh'

    def handle(self, *args, **options):
        if not args or not args[0]:
            raise CommandError('File name to load does not specified')

        input_handle = open(args[0], 'r')
        book_count = 0
        for line in input_handle:
            line = line.strip()
            if not line:
                continue

            elements = line.split(' ')
            path = elements[0].strip()
            ed2k_hash = elements[1].strip()

            path_elem = path.split('/')
            file_name = path_elem[3]
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

        input_handle.close()
        self.stdout.write('Successfully processed "%d"' % book_count)
