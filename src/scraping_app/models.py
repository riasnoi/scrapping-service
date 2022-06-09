from django.db import models
from .text_transform import transform_to_eng
import jsonfield


def default_urls():
    return {'hh': '', 'habr': ''}


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название города', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transform_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Язык программирования', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transform_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True, verbose_name='Дата добавления в базу')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True, verbose_name='Дата ошибки')
    data = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Ошибку'
        verbose_name_plural = 'Ошибки'


class UrlToParse(models.Model):
    language = models.OneToOneField('Language', on_delete=models.CASCADE, verbose_name='Язык программирования',
                                    unique=True)
    data = jsonfield.JSONField(default=default_urls())

    class Meta:
        verbose_name = 'Адрес для парсера'
        verbose_name_plural = 'Адреса для парсера'

    def __str__(self):
        return self.language.name
