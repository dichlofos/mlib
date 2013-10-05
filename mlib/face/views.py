from django.shortcuts import render


def index(request):
    results = []
    search_text = ''
    if 'search' in request.POST:
        search_text = request.POST['search']

    context = {
        'search_text': search_text,
    }
    return render(request, 'face/index.html', context)

