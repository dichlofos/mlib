from django.shortcuts import render
from django.db.models import Q

from face.models import Book

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



