from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect

from face.models import Book

import os
import uuid

def index(request):
    if 'search' in request.POST:
        text = request.POST['search']

        if text:
            # split by spaces
            words = text.split()
            query = Q()
            for word in words:
                query = query & (
                    Q(title__icontains=word) |
                    Q(author1__icontains=word) |
                    Q(author2__icontains=word) |
                    Q(author3__icontains=word)
                )

            book_items = Book.objects.filter(query).distinct()[:10]

            context = {
                'search_text': text,
                'book_items': book_items,
            }
        else:
            context = {
                'error_message': 'Empty search request'
            }
        return render(request, 'face/index.html', context)

    return render(request, 'face/index.html', {})


def download(request, book_id):
    """ Make a symlink to real file to obfuscate its real name """

    book = Book.objects.get(id=book_id)
    download_name = str(uuid.uuid4()) + '.' + book.ext()

    os.symlink(
        '/storage/whiterose/libraries/lib.mexmat.ru/Lib/' + book.path(),
        '/var/www/vhosts/mlib/b/storage/' + download_name)
    response = HttpResponseRedirect('/b/storage/' + download_name)
    return response
