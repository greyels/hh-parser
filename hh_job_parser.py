#!/usr/bin/python3
import requests
import re
from collections import Counter

API_URL = 'https://api.hh.ru/vacancies/'
VACANCY = 'python developer'
AREA_NUMBER = 1
PER_PAGE = '100'
PAGES = 21

def get_ids(url, vacancy, area_number):
    ids = []
    try:
        for page in range(PAGES):
            param = {'text': vacancy, 'area': area_number,
                     'per_page': PER_PAGE, 'page': str(page)}
            r = requests.get(url, param).json()
            for i in r['items']:
                ids.append(i['id'])
    except KeyError:
        pass
    finally:
        return ids

def get_descriptions_from_url(url, ids):
    descriptions = []
    for id in ids:
        id_url = url + id
        print(id_url)
        r = requests.get(id_url).json()
        descriptions.append(r['description'])
    return descriptions

def get_text_from_html(html):
    text = []
    for i in html:
        text.append(re.sub('<.*?>', '', i))
    return text

def normalize_text(text):
    norm_text = []
    skips_1 = [".", ",", ":", ";", "'", '"', "(", ")", "!", "«", "»", 
               "?", "•", "·"]
    skips_2 = ["/", "\\", "\\\\", "  ", "   ", "-", "–"]
    for i in text:
        i = i.lower()
        for char in skips_1:
            i = i.replace(char, "")
        for char in skips_2:
            i = i.replace(char, " ")
        norm_text.append(i)
    return norm_text

def count_words(text):
    word_counts = Counter(text.split(" ")).most_common(500)
    return word_counts

def get_string_from_lists(list):
    descriptions_str = ' '.join(list)
    return descriptions_str

def main():
    ids = get_ids(API_URL, VACANCY, AREA_NUMBER)
    print(len(ids))
    descriptions = get_descriptions_from_url(API_URL, ids)
    descriptions = get_text_from_html(descriptions)
    descriptions = normalize_text(descriptions)
    print(descriptions)
    descriptions_str = get_string_from_lists(descriptions)
    word_counts = count_words(descriptions_str)
    normal_words = []
    for i in word_counts:
        if len(i[0]) >= 3:
            normal_words.append(i)
    print(normal_words)
    return 0

if __name__ == '__main__':
    exit(main())
