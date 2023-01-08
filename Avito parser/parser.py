import requests
from bs4 import BeautifulSoup
import csv
import time
from random import uniform
import random
from datetime import datetime
from multiprocessing import Pool


a = uniform(3, 6)
now = datetime.now()


url = 'https://www.avito.ru/moskva'
base_url = 'https://www.avito.ru/moskva/telefony?cd=1'
page_part = '&p='
pmin_part = '&pmin=12000'
pmax_part = '&pmax=12500'
query_part = '&q=iphone+7'
user_part = '&user=1'


def make_all(url):
    time.sleep(a)
    html = get_html(url)
    get_profile_data(html)


def get_html(url):
    s = requests.session()
    r = s.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages clearfix') \
        .find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


titles = []
prices = []
urlses = []
ratings = []
otzivi = []
registrs = []

urls = []


def write_csv(rows):
    with open('avito69.csv', 'a', encoding='cp1251') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=';', lineterminator='\n')
        for row in rows:
            writer.writerow(row)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='js-catalog_serp').find_all('div', class_='item_table')
    for ad in ads:
        try:
            price = ad.find('span', class_='snippet-price').text.split()[0] \
                    + ad.find('span', class_='snippet-price').text.split()[1]
            print(price)
            prices.append(price)
        except:
            price = ''
            prices.append(price)

        try:
            title = ad.find('a', class_='snippet-link').text.strip()
            print(title)
            titles.append(title)
        except:
            title = ''
            titles.append(title)

        try:
            url = 'https://www.avito.ru' + ad.find('a', class_='snippet-link').get('href')
            urlses.append(url)
            print(url)
            urls.append(url)
        except:
            url = ''
            urlses.append(url)
            urls.append(url)


def get_profile_data(html):
    soup = BeautifulSoup(html, 'lxml')
    mains = soup.find('div', class_='seller-info-value')
    try:
        registr = mains.find_next_sibling('div', class_='seller-info-value').text.strip()
        print(registr)
        registrs.append(registr)
    except:
        registr = ''
        registrs.append(registr)

    try:
        rating = soup.find('div', class_='seller-info-value').find('div', class_='seller-info-rating') \
            .find('span', class_='seller-info-rating-score').text.strip()
        print(rating)
        ratings.append(rating)
    except:
        rating = ''
        ratings.append(rating)

    try:
        otziv = soup.find('div', class_='seller-info-value') \
            .find('span', class_='seller-info-rating-caption').text.strip().replace(' ', '')
        print(otziv)
        otzivi.append(otziv)
    except:
        otziv = ''
        otzivi.append(otziv)


def main():
    print('Начало работы', datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
    html = get_html(url)
    r = get_total_pages(html)
    for i in range(1, 2):
        url_gen = base_url + user_part + query_part + page_part + str(i) + pmin_part + pmax_part
        html = get_html(url_gen)
        get_page_data(html)

    with Pool(7) as p:
        p.map(make_all, urls)

    rows = zip(titles, prices, registrs, urlses, ratings, otzivi)

    write_csv(rows)

    print('Конец работы', datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))


if __name__ == '__main__':
    main()
