import requests, codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36'}


def headhunter_find_vacancies(url, headers):
    jobs = []
    errors = []
    url = 'https://hh.ru/search/vacancy?text=&professional_role=96&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true'
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
                    jobs.append({
                        'title': title,
                        'url': job_link,
                        'description': desc,
                        'company': company
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


def habr_find_vacancies(url, headers):
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

                    if div.find('div', attrs={'class': 'vacancy-card__skills'}):
                        skills = div.find('div',
                                          attrs={
                                              'class': 'vacancy-card__skills'}).text
                    else:
                        skills = "Особых навыков не требуется."

                    desc = skills
                    company = div.find('div', attrs={'class': 'vacancy-card__company-title'}).a.text
                    jobs.append({
                        'title': title,
                        'url': job_link,
                        'description': desc,
                        'company': company
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


if __name__ == '__main__':
    url = 'https://career.habr.com/vacancies?skills[]=446&type=all'
    habr_jobs, habr_errors = habr_find_vacancies(url, headers)
    handler = codecs.open('habr.txt', 'w', 'utf-8')
    handler.write(str(habr_jobs))
    handler.close()
