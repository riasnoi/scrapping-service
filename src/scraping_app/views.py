from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def vacancy_view(request):
    language = request.GET.get('language')
    city = request.GET.get('city')

    form = FindForm()
    qs = []
    _filter = {}
    if city or language:
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

    qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping_app/home.html', {'object_list': qs, 'form': form})
