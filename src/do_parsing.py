import codecs
import os
import sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scrapping_service.settings"

import django

django.setup()

from django.db import DatabaseError
from scraping_app.parser import *
from scraping_app.models import City, Language, Vacancy, Error, UrlToParse
from scraping_app.text_transform import transform_to_eng

User = get_user_model();

parsers = (
    (headhunter_find_vacancies, 'hh'),
    (habr_find_vacancies, 'habr')
)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = UrlToParse.objects.all().values()
    url_dct = {(q['language_id']): q['data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp_dct = {}
        tmp_dct['language'] = pair
        tmp_dct['data'] = url_dct[pair]
        urls.append(tmp_dct)
    return urls


langs_id = get_settings()  # получаем список с id языков, вакансии по которым интересуют пользователей
url_list = get_urls(langs_id)

# language = Language.objects.filter(slug='python').first()


jobs, errors = [], []
for url_elem in url_list:
    for func, key in parsers:
        url = url_elem['data'][key]
        j, e = func(url, language=url_elem['language'])
        jobs += j
        errors += e

for job in jobs:
    if len(City.objects.filter(name=job['city'])) == 0:
        c = City(name=job['city'], slug=transform_to_eng(job['city']))
        c.save()
        city = City.objects.filter(name=job['city']).first()
    else:
        city = City.objects.filter(name=job['city']).first()

    if len(Vacancy.objects.filter(url=job['url'])) == 0:
        v = Vacancy(
            url=job['url'],
            title=job['title'],
            company=job['company'],
            description=job['description'],
            city=city,
            language=Language.objects.filter(id=job['language_id']).first()
        )
        v.save()
    else:
        pass

if errors:
    er = Error(data=errors).save()

handler = codecs.open('jobs.txt', 'w', 'utf-8')
handler.write(str(jobs))
handler.close()
