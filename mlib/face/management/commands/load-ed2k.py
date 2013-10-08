# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from face.models import Book

import os
import sys

class Command(BaseCommand):
    args = '<file_name>'
    help = 'Loads ed2k hashes calculated on files using calc-ed2k.sh'

    def handle(self, *args, **options):
        if not args or not args[0]:
            raise CommandError('File name to load does not specified')

        file_name = args[0]
        f = open(file_name, 'r')
        book_count = 0
        for line in f:
            line = line.strip()
            if not line:
                continue

            al = line.split(' ')
            path = al[0].strip()
            ed2k_hash = al[1].strip()

            af = path.split('/')
            file_name = af[3]
            srch = Book.objects.filter(ed2k_hash=ed2k_hash)
            if not srch:
                print "Loading", ed2k_hash
                try:
                    b = Book(
                            num=0,
                            file_name=file_name,
                            ed2k_hash=ed2k_hash)
                    b.save()
                    book_count += 1
                except BaseException as e:
                    print "Problem with book:"
                    print e
                    print '----------------------'
            else:
                print "Exists:", srch[0]

        f.close()
        self.stdout.write('Successfully processed "%d"' % book_count)
