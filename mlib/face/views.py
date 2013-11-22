from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect

from face.models import Book

import os

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

    uuid = '94bcaa9d-864b-4b51-87a2-af67cfd42d09'
    book = Book.objects.get(id=book_id)

    os.symlink('/storage/whiterose/libraries/lib.mexmat.ru/Lib/' + \
        book.file_name,
        '/var/www/vhosts/mlib/b/storage/' + uuid)
    response = HttpResponseRedirect('/b/storage/' + uuid)
    return response
