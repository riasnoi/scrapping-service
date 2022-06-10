from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def main_view(request):
    form = FindForm()
    return render(request, 'scraping_app/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    language = request.GET.get('language')
    city = request.GET.get('city')
    qs = []

    context = {'city': city, 'language': language, 'form': form}

    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj

    return render(request, 'scraping_app/list.html', context)
