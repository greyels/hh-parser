#!/usr/bin/python3
import requests
import statistics as st
import sys

API_URL = 'https://api.hh.ru/vacancies'
AREA_DICT = {'Moscow': 1, 'NN': 66, 'Russia': 113}
PER_PAGE = '100'
PAGES = 21
USD_RATE = 63.89
EUR_RATE = 71.80

def get_salaries(url, vacancy, area_number):
    salaries = []
    try:
        for page in range(PAGES):
            param = {'text': vacancy, 'only_with_salary': 'true', 'area': area_number,
                     'per_page': PER_PAGE, 'page': str(page)}
            r = requests.get(url, param).json()
            for i in r['items']:
                salaries.append(i['salary'])
    except KeyError:
        pass
    finally:
        return salaries

def remove_bad_currencies(salaries):
    return list(filter(lambda item: item['currency'] in ('RUR', 'USD', 'EUR'), salaries))

def refine_salaries(salaries):
    ref_salaries = []
    for item in salaries:
        if item['from'] and item['to']:
            salary = (float(item['to']) + float(item['from']))/2
        elif item['from']:
            salary = float(item['from'])
        else:
            salary = float(item['to'])
        if item['currency'] == 'USD':
            salary *= USD_RATE
        elif item['currency'] == 'EUR':
            salary *= EUR_RATE
        if item['gross'] is True:
            salary *= 0.87
        ref_salaries.append(salary)
    return ref_salaries

def get_area_number_by_name(area_name):
    try:
        assert area_name in AREA_DICT
    except AssertionError:
        available_names = []
        for key in AREA_DICT:
            available_names.append(key)
        raise AssertionError ("Incorrect area! Please specify one of the next areas: "
                              + str(available_names) + ".")
    return AREA_DICT.get(area_name)

def main():
    try:
        assert len(sys.argv) == 3, "Usage: " + __file__ + " <vacancy> <Russia/Moscow/NN>"
        vacancy = sys.argv[1]
        area_number = get_area_number_by_name(sys.argv[2])
        salaries = get_salaries(API_URL, vacancy, area_number)
        salaries = remove_bad_currencies(salaries)
        salaries = refine_salaries(salaries)
        average_salary = sum(salaries)/len(salaries)
        median_salary = st.median(salaries)
        print("Found " + str(len(salaries)) + " vacancies of '" + vacancy + "' in " + sys.argv[2] + ".\n"
              "Average salary for '" + vacancy + "' is " + str(round(average_salary,2)) + " RUR.\n"
              "Median salary for '" + vacancy + "' is " + str(median_salary) + " RUR.")
    except AssertionError as error:
        print(error)
        return 1
    return 0

if __name__ == '__main__':
    exit(main())
