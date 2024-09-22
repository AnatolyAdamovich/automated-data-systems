import pandas as pd
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from solution.html_parser import parse_habr_career_html

# Технические тесты
def test_output_format():
    df = parse_habr_career_html()
    assert isinstance(df, pd.DataFrame), 'Неправильный тип выходных данных'

def test_output_columns():
    df = parse_habr_career_html()
    assert 'Company Name' in df.columns, 'Нет столбца <Company Name>'
    assert 'Company Rating' in df.columns, 'Нет столбца <Company Rating>'
    assert 'Vacancy' in df.columns, 'Нет столбца <Vacancy>'
    assert 'Salary' in df.columns, 'Нет столбца <Salary>'

def test_output_length():
    df = parse_habr_career_html(n_pages=1)
    assert len(df) == 25, 'Парсинг первой страницы дает 25 вакансий'

# Тесты соблюдения бизнес-логики
def test_vacancy_existency():
    df = parse_habr_career_html(n_pages=3, employment_type='part_time')
    assert df.loc[df['Vacancy']=='Стажер DevSecOps', 'Company Name'].values[0] == 'Солар'