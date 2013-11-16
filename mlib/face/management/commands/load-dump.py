# -*- coding: utf-8 -*-
""" Load books from TSV dump converted to utf8 encoding """

from django.core.management.base import BaseCommand, CommandError
from face.models import Book

import sys

def apply_fixes(elem):
    """ Fix some invalid lines """
    # fix swapped year and publication
    if elem[0] == '43726':
        tmp = elem[5]
        elem[5] = elem[6]
        elem[6] = tmp

    # fix shifted book
    if elem[0] == '74707':
        elem[2] = u'Голованов Н.'
        elem[3] = elem[4]
        elem[4] = elem[5]
        elem[5] = elem[6]
        elem[6] = elem[7]
        elem[7] = elem[8]
        elem[8] = elem[9]

    # fix shifted book
    if elem[0] == '75275':
        elem[1] = u'Акимушкин И.И.'
        elem[2] = ''
        elem[3] = ''
        elem[4] = elem[5]
        elem[5] = elem[6]
        elem[6] = elem[7]
        elem[7] = elem[8]
        elem[8] = elem[9]


class Command(BaseCommand):
    """ Django command """
    args = '<file_name>'
    help = 'Loads books into library from dump'

    def handle(self, *args, **options):
        """ Command handler """
        if not args or not args[0]:
            raise CommandError('File name to load does not specified')

        file_name = args[0]
        input_handle = open(file_name, 'r')
        book_count = 0
        for line in input_handle:
            line = line.strip()
            if not line:
                continue

            line = line.decode('utf8')
            elements = line.split('\t')
            # elements contain quoted values, we need to dequote them
            elem = []
            for tok in elements:
                tok = tok.strip()
                if tok[0:1] == '"':
                    tok = tok[1:len(tok) - 1]
                tok = tok.replace('""', '"')
                tok = tok.replace('""', '"')
                elem.append(tok)

            if len(elem) < 8:
                print elem
                sys.exit(1)

            book_file_name = elem[7]
            # skip phantom book
            if '20070623_D41D8CD9' in book_file_name:
                continue

            if len(elem) < 9:
                print elem
                sys.exit(1)

            apply_fixes(elem)

            try:
                book = Book(
                        num=elem[0],
                        author1 = elem[1],
                        author2=elem[2],
                        author3=elem[3],
                        title=elem[4],
                        year=elem[5],
                        publication=elem[6],
                        file_name=elem[7],
                        ed2k_hash=elem[8])
                book.save()
                book_count += 1
            except BaseException as exc:
                print "There is a problem with book:"
                print elem
                print exc
                print '----------------------'

        input_handle.close()
        self.stdout.write('Successfully processed "%d"' % book_count)
