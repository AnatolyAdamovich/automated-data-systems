from bs4 import BeautifulSoup
import requests
import pandas as pd


def parse_habr_career_html(n_pages: "int" = 1, 
                           qid: "int" = 1, 
                           employment_type: "str" = 'full_time') -> pd.DataFrame:
    '''
    Функция парсит сайт https://career.habr.com/vacancies.
    На выходе получаем pandas.DataFrame со столбцами:
    ['Company', 'Company Rating', 'Vacancy', 'Salary']

    Parameters
    ----------
    n_pages : int
        количество страниц, которые нужно спарсить (1, 2, 3, 4, 5)
    qid : int
        уровень вакансии (1, 3, 4, 5, 6 от intern до lead)
    employment_type : str
        формат работы (full_time, part_time)
    '''
    assert n_pages in (1, 2, 3, 4, 5), 'Значение n_pages должны быть в области [1, 2, 3, 4, 5]'
    assert qid in (1, 3, 4, 5, 6), 'Значение qid должны быть в области [1, 3, 4, 5, 6, None]'
    assert employment_type in ('full_time', 'part_time'), 'Значение employment_type должны быть в области [full_time, part_time, None]'
    
    class_card_info = 'vacancy-card__info'
    class_vacancy = 'vacancy-card__title-link'
    class_company = 'vacancy-card__company-title'
    class_company_rating = 'vacancy-card__company-rating'
    class_salary = 'basic-salary'
    
    dict_with_data = {'Company Name': [],
                      'Company Rating': [],
                      'Vacancy': [],
                      'Salary': []}
    
    for page in range(1, n_pages+1):
        URL = f"https://career.habr.com/vacancies?employment_type={employment_type}&page={page}&qid={qid}&type=all"
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        for element in soup.findAll(class_=class_card_info):
            
            vacancy = element.find('a', class_=class_vacancy).text

            company = element.find('div', class_=class_company).a.text
            
            company_rating = element.find('div', class_=class_company_rating)
            if company_rating is not None:
                company_rating = company_rating.text
            else:
                company_rating = 'Без рейтинга'
            
            salary = element.find('div', class_=class_salary)
            if salary is not None:
                salary = salary.text
        
            dict_with_data['Company Name'].append(company)
            dict_with_data['Vacancy'].append(vacancy)
            dict_with_data['Company Rating'].append(company_rating)
            dict_with_data['Salary'].append(salary)

    return pd.DataFrame(dict_with_data)