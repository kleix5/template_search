import re
import json
import numpy as np
from tinydb import Query, TinyDB, where


db = TinyDB('db.json')
User = Query()


def valid(in_dict):
    re_text = re.compile(r'.*')
    re_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    re_phone = re.compile(r'\+\d*[\s(-]{0,2}\d*[\s)-]{0,2}\d*[\s-]?\d*[\s-]?\d*')
    re_date = re.compile(r'\d{1,4}\W\d{1,2}\W\d{1,4}')  
    for k, v in in_dict.items():
        if re.fullmatch(re_date, v):
            in_dict[k] = 'date'
        elif re.fullmatch(re_phone, v):
            in_dict[k] = 'phone'
        elif re.fullmatch(re_email, v):
            in_dict[k] = 'email'
        else:
            in_dict[k] = 'text'
    in_dict = namechek(in_dict)
    return in_dict


def match_tmp(in_dict):
    '''Этой функцией мы пробегаемся по клучам поступившего шаблона 
       и ищем совпадающие шаблоны'''
    in_dict = valid(in_dict)
    matches = []
    for i in range(len(list(in_dict))):    
        test_func = lambda s: s == in_dict[list(in_dict)[i]]
        match = db.search(User[list(in_dict)[i]].test(test_func))
        if len(match) != 0:
            matches.append(db.search(User[list(in_dict)[i]].test(test_func)))
    super_match = []
    for i in matches:
        for j in i:
            super_match.append(j)
    where_are_you = np.array(super_match)
    return where_are_you
         

def search(in_dict):
    '''Тут идёт проверка совпадений по ключам входящего словаря
       и ключам найденных, подходящих шаблонов. Из ключей создаются массивы, сортируются,
       сначала происходит проверка поэлементно, потом применяется логическое И к результатам массива.
       В переменную answer помещается numpy.ndarray имён подходящих шаблонов.'''
    db_array = match_tmp(in_dict)
    answer = []
    for item in range(len(db_array)):
        if np.all(np.isin(np.sort(np.array(list(db_array[item]))), np.sort(np.array(list(in_dict))))):
            result = db_array[item]['name']
            answer.append(result)
        else:
            continue
    answer = np.unique(np.array(answer))
    if len(answer):
        return answer[0]
    else:
        del in_dict['name']
        return in_dict


def namechek(in_dict):
    if 'name' in in_dict:
        True
    else:
        in_dict['name'] = 'text'
    return in_dict
