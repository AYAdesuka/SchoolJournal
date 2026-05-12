from django.shortcuts import render
from journal.models import Subject

# Create your views here.

def search(request):
    search_query = request.GET.get('search', '')
    subject = Subject.objects.all()

    if search_query:
        lessons = subject.filter(name__icontains=search_query)

    context = {
        'lessons': lessons,
        'search_query': search_query
    }
    return render(request, 'pages/dishes/list.html', context)