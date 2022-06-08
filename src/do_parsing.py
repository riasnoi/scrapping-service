import codecs
import os
import sys


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scrapping_service.settings"


import django
django.setup()

from django.db import DatabaseError
from scraping_app.parser import *
from scraping_app.models import City, Language, Vacancy
from scraping_app.text_transform import transform_to_eng


parsers = (
    (headhunter_find_vacancies,
     'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&items_on_page=20&no_magic=true' \
     '&ored_clusters=true&professional_role=96&search_period=1&hhtmFrom=vacancy_search_list '),
    (habr_find_vacancies, 'https://career.habr.com/vacancies?page=1&skills[]=446&sort=date&type=all')
)

language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e


for job in jobs:
    if len(City.objects.filter(name=job['city'])) == 0:
        c = City(name=job['city'], slug=transform_to_eng(job['city']))
        c.save()
        city = City.objects.filter(name=job['city']).first()
    else:
        city = City.objects.filter(name=job['city']).first()

    if len(Language.objects.filter(name='python')) == 0:
        lang = Language(name='Python', slug=transform_to_eng('Python'))
        lang.save()
        language = Language.objects.filter(slug='python').first()
    else:
        language = Language.objects.filter(slug='python').first()

    v = Vacancy(
        url=job['url'],
        title=job['title'],
        company=job['company'],
        description=job['description'],
        city=city,
        language=language
        )
    v.save()

handler = codecs.open('jobs.txt', 'w', 'utf-8')
handler.write(str(jobs))
handler.close()
