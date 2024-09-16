import pandas as pd
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from solution import parse_pdf_hh_resume, parse_docx_hh_resume, parse_doc_hh_resume

# Базовые тесты выходных данных для pdf-parser
def test_pdf_output_format():
    dct = parse_pdf_hh_resume('module_1/data/resume.pdf')
    assert isinstance(dct, dict), 'Неправильный тип выходных данных'

def test_doc_output_format():
    dct = parse_doc_hh_resume('module_1/data/resume.doc')
    assert isinstance(dct, dict), 'Неправильный тип выходных данных'

def test_docx_output_format():
    dct = parse_docx_hh_resume('module_1/data/resume.docx')
    assert isinstance(dct, dict), 'Неправильный тип выходных данных'

def test_pdf_output_keys():
    dct = parse_pdf_hh_resume('module_1/data/resume.pdf')
    assert 'Email' in dct.keys(), 'Нет ключа <Email>'
    assert 'City' in dct.keys(), 'Нет ключа <City>'
    assert 'Position' in dct.keys(), 'Нет ключа <Position>'
    assert 'Experience' in dct.keys(), 'Нет ключа <Experience>'
    assert 'Images' in dct.keys(), 'Нет ключа <Images>'

def test_doc_output_keys():
    dct = parse_doc_hh_resume('module_1/data/resume.doc')
    assert 'Email' in dct.keys(), 'Нет ключа <Email>'
    assert 'City' in dct.keys(), 'Нет ключа <City>'
    assert 'Position' in dct.keys(), 'Нет ключа <Position>'
    assert 'Experience' in dct.keys(), 'Нет ключа <Experience>'

def test_docx_output_keys():
    dct = parse_docx_hh_resume('module_1/data/resume.docx')
    assert 'Email' in dct.keys(), 'Нет ключа <Email>'
    assert 'City' in dct.keys(), 'Нет ключа <City>'
    assert 'Position' in dct.keys(), 'Нет ключа <Position>'
    assert 'Experience' in dct.keys(), 'Нет ключа <Experience>'

# Тесты бизнес-логики для pdf-parser
def test_pdf_parser_consistency():
    dct = parse_pdf_hh_resume('module_1/data/resume.pdf')
    assert dct['Email'] == 'alekander@pushkin.ru', 'Неверный Email'
    assert dct['City'] == 'Санкт-Петербург, м. Невский проспект', 'Неверное место жительства'
    assert dct['Position'] == 'Программист, системный администратор, системный инженер', 'Неверная должность'
    assert dct['Experience'] == '13 лет 7 месяцев', 'Неверный опыт работы'

def test_doc_parser_consistency():
    dct = parse_doc_hh_resume('module_1/data/resume.doc')
    assert dct['Email'] == 'alekander@pushkin.ru', 'Неверный Email'
    assert dct['City'] == 'Санкт-Петербург, м. Невский проспект', 'Неверное место жительства'
    assert dct['Position'] == 'Программист, системный администратор, системный инженер', 'Неверная должность'
    assert dct['Experience'] == '13 лет 7 месяцев', 'Неверный опыт работы'

def test_doc_parser_consistency():
    dct = parse_docx_hh_resume('module_1/data/resume.docx')
    assert dct['Email'] == 'alekander@pushkin.ru', 'Неверный Email'
    assert dct['City'] == 'Санкт-Петербург, м. Невский проспект', 'Неверное место жительства'
    assert dct['Position'] == 'Программист, системный администратор, системный инженер', 'Неверная должность'
    assert dct['Experience'] == '13 лет 7 месяцев', 'Неверный опыт работы'