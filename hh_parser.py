#!/usr/bin/python3
import requests

API_URL = 'https://api.hh.ru/vacancies'
VACANCY = 'python developer'
PER_PAGE = '100'
PAGES = 21
USD_RATE = 63.89
EUR_RATE = 71.80

def get_salaries(url):
    salaries = []
    try:
        for page in range(PAGES):
            param = {'text': VACANCY, 'only_with_salary': 'true', 
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

def calculate_average_salaries(salaries):
    average_salaries = []
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
        average_salaries.append(salary)
    return average_salaries

def main():
    salaries = get_salaries(API_URL)
    salaries = remove_bad_currencies(salaries)
    average_salaries = calculate_average_salaries(salaries)
    av_salary = sum(average_salaries)/len(average_salaries)
    print("Found " + str(len(average_salaries)) + " vacancies of '" + VACANCY + "'. "
          "Average salary for '" + VACANCY + "' is " + str(round(av_salary,2)) + " RUR.")
    return 0

if __name__ == '__main__':
    exit(main())
