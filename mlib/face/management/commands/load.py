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
        fo = open('list-conv.txt', 'w')

        for line in f:
            line = line.decode('utf8')
            al = line.split('\t')
            # al contain quoted values, we need to dequote them
            bl = []
            btok = ''
            for tok in al:
                tok = tok.strip()
                print "tok=QQQ" + tok + "ZZZ"
                if tok[0:1] == '"':
                    tok = tok[1:len(tok) - 1]
                tok = tok.replace('""', '"')
                tok = tok.replace('""', '"')
                bl.append(tok)

            for x in bl:
                fo.write(x.encode('utf8') + '\t')
            fo.write('\n')
            sys.exit(0)

        f.close()
        fo.close()



        """
        for  in args:
            try:
                poll = Poll.objects.get(pk=int(poll_id))
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write('Successfully closed poll "%s"' % poll_id)
        """