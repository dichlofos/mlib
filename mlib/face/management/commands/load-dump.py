# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from face.models import Book

import os
import sys

class Command(BaseCommand):
    args = '<file_name>'
    help = 'Loads books into library from dump'

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

            line = line.decode('utf8')
            al = line.split('\t')
            # al contain quoted values, we need to dequote them
            bl = []
            btok = ''
            for tok in al:
                tok = tok.strip()
                if tok[0:1] == '"':
                    tok = tok[1:len(tok) - 1]
                tok = tok.replace('""', '"')
                tok = tok.replace('""', '"')
                bl.append(tok)

            if len(bl) < 8:
                print bl
                sys.exit(1)

            book_file_name = bl[7]
            # skip phantom book
            if '20070623_D41D8CD9' in book_file_name:
                continue

            if len(bl) < 9:
                print bl
                sys.exit(1)

            # fix swapped year and publication
            if bl[0] == '43726':
                tmp = bl[5]
                bl[5] = bl[6]
                bl[6] = tmp

            # fix shifted book
            if bl[0] == '74707':
                bl[2] = u'Голованов Н.'
                bl[3] = bl[4]
                bl[4] = bl[5]
                bl[5] = bl[6]
                bl[6] = bl[7]
                bl[7] = bl[8]
                bl[8] = bl[9]

            # fix shifted book
            if bl[0] == '75275':
                bl[1] = u'Акимушкин И.И.'
                bl[2] = ''
                bl[3] = ''
                bl[4] = bl[5]
                bl[5] = bl[6]
                bl[6] = bl[7]
                bl[7] = bl[8]
                bl[8] = bl[9]

            try:
                b = Book(
                        num=bl[0],
                        author1 = bl[1],
                        author2=bl[2],
                        author3=bl[3],
                        title=bl[4],
                        year=bl[5],
                        publication=bl[6],
                        file_name=bl[7],
                        ed2k_hash=bl[8])
                b.save()
                book_count += 1
            except BaseException as e:
                print "There is a problem with book:"
                print bl
                print e
                print '----------------------'

        f.close()
        self.stdout.write('Successfully processed "%d"' % book_count)
