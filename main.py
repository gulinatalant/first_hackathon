import json
import csv
import lxml
from typing import List
import requests
from bs4 import BeautifulSoup, Tag


url = 'https://www.mashina.kg/search/all/'

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    raise Exception('сайт не отвечает')
    # print(response.text)    

def get_soup(html:str) -> BeautifulSoup:
    soup = BeautifulSoup(html, 'lxml')
    return soup
    # print(soup)    

def get_cards_from_soup(soup: BeautifulSoup) -> List[Tag]:
    cards = soup.find_all('div', {'class':'list-item list-label'})
    return cards

    # print(cards)

def get_data_from_cards(cards: List[Tag]) -> List[dict]:
    data = []
    for card in cards:
        cars = {
            'title': card.find('a').find('div', {'class': 'block title'}).find('h2', {'class': 'name'}).text.replace('\n', '').strip(),
            'price':card.find('a').find('div', {'class': 'block price'}).find('strong').text.replace('\n', '').strip(),
            # 'image':card.find('a').find('div', {'class':'thumb-item-carousel brazzers-daddy'}).find('div', {'class':'image-wrap'}).find('img', {'class':'lazy-image visible'}).get('scr')
            'year':card.find('a').find('div', {'class': 'block info-wrapper item-info-wrapper'}).find('p', {'class': 'year-miles'}).text.replace('\n', '').strip(),
            'body-type':card.find('a').find('div', {'class': 'block info-wrapper item-info-wrapper'}).find('p', {'class':'body-type'}).text.replace('\n', '').strip()
        }
        data.append(cars)
    return data



def write_to_json(data: List[dict]):
    with open('cars.json','w') as cars:
        json.dump(data, cars, indent=4, ensure_ascii=False)


def write_to_csv(data: List[dict]):
    with open('cars.csv', 'w') as cars:
        filenames = data[0].keys()
        writer = csv.DictWriter(cars, fieldnames=filenames, delimiter='/')
        writer.writeheader()
        writer.writerows(data)      


def main():
    html = get_html(url)
    soup = get_soup(html)
    cards = get_cards_from_soup(soup)
    data = get_data_from_cards(cards)
    write_to_csv(data)
    write_to_json(data)


if __name__ == '__main__':
    main()