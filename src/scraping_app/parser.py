import requests, codecs
from bs4 import BeautifulSoup as BS

__all__ = ('headhunter_find_vacancies', 'habr_find_vacancies')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36'}


def headhunter_find_vacancies(url, language=None):
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers)
    try:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            if soup.find("div", attrs={'class': 'vacancy-serp-content'}):
                main_div = soup.find("div", attrs={'class': 'vacancy-serp-content'})
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})

                for div in div_list:
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
                    job_link = title['href']
                    title = title.text

                    if div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}):
                        responsibility = div.find('div',
                                                  attrs={
                                                      'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    else:
                        responsibility = "Описание вакансии не задано"
                    if div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}):
                        requirement = div.find('div',
                                               attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    else:
                        requirement = "Особых требований к вакансии нет"

                    desc = responsibility + ' ' + requirement
                    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    city = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
                    jobs.append({
                        'title': title,
                        'url': job_link,
                        'description': desc,
                        'company': company,
                        'city': city,
                        'language_id': language
                    })
            else:
                errors.append({'url': url, 'title': 'Main div not found'})
        else:
            errors.append({'url': url, 'title': 'Page not response, status code: ' + str(resp.status_code)})
    except Exception as err:
        errors.append({
            'url': url,
            'title': err
        })
    return jobs, errors


def habr_find_vacancies(url, language=None):
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers)
    domain = 'https://career.habr.com'
    try:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            if soup.find("div", attrs={'class': 'section-group section-group--gap-medium'}):
                main_div = soup.find("div", attrs={'class': 'section-group section-group--gap-medium'})
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-card'})

                for div in div_list:
                    title = div.find('a', attrs={'class': 'vacancy-card__title-link'})
                    job_link = domain + title['href']
                    title = title.text

                    if div.find('div', attrs={'class': 'vacancy-card__skills'}):
                        skills = div.find('div',
                                          attrs={
                                              'class': 'vacancy-card__skills'}).text
                    else:
                        skills = "Особых навыков не требуется."

                    desc = skills
                    company = div.find('div', attrs={'class': 'vacancy-card__company-title'}).a.text

                    if div.find('div', attrs={'class': 'vacancy-card__meta'}).a:
                        city = div.find('div', attrs={'class': 'vacancy-card__meta'}).a.text
                    else:
                        city = 'Город не указан'

                    jobs.append({
                        'title': title,
                        'url': job_link,
                        'description': desc,
                        'company': company,
                        'city': city,
                        'language_id': language
                    })
            else:
                errors.append({'url': url, 'title': 'Main div not found'})
        else:
            errors.append({'url': url, 'title': 'Page not response, status code: ' + str(resp.status_code)})
    except Exception as err:
        errors.append({
            'url': url,
            'title': err
        })
    return jobs, errors


# if __name__ == '__main__':
#     url = 'https://career.habr.com/vacancies?page=1&skills[]=446&sort=date&type=all'
#     habr_jobs, habr_errors = habr_find_vacancies(url)
#     handler = codecs.open('habr.txt', 'w', 'utf-8')
#     handler.write(str(habr_jobs))
#     handler.close()