#!/usr/bin/python3
import requests
import statistics as st
import sys

API_URL = 'https://api.hh.ru/vacancies'
PER_PAGE = '100'
PAGES = 21
USD_RATE = 63.89
EUR_RATE = 71.80

def get_salaries(url, vacancy, area):
    salaries = []
    try:
        for page in range(PAGES):
            param = {'text': vacancy, 'only_with_salary': 'true', 'area': area,
                     'per_page': PER_PAGE, 'page': str(page)}
            r = requests.get(url, param).json()
            for i in r['items']:
                salaries.append(i['salary'])
    except KeyError:
        pass
    finally:
        return salaries

def remove_bad_currencies(salaries):
    salaries = list(filter(lambda item: item['currency'] in ('RUR', 'USD', 'EUR'), salaries))
    return salaries

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

def main():
    if len(sys.argv) != 3:
        print("Usage: " + __file__ + " <vacancy> <Russia/Moscow/NN>")
        return 1
    VACANCY = sys.argv[1].replace('+', ' ')
    if sys.argv[2] == 'Moscow': AREA = 1
    elif sys.argv[2] == 'NN': AREA = 66
    else: AREA = 113
    salaries = get_salaries(API_URL, VACANCY, AREA)
    salaries = remove_bad_currencies(salaries)
    salaries = refine_salaries(salaries)
    average_salary = sum(salaries)/len(salaries)
    median_salary = st.median(salaries)
    print("Found " + str(len(salaries)) + " vacancies of '" + VACANCY + "' in " + sys.argv[2] + ".\n"
          "Average salary for '" + VACANCY + "' is " + str(round(average_salary,2)) + " RUR.\n"
          "Median salary for '" + VACANCY + "' is " + str(median_salary) + " RUR.")
    return 0

if __name__ == '__main__':
    exit(main())
