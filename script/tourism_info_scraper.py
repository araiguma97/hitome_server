import requests
from bs4 import BeautifulSoup
import time
import json
import re
import datetime
import os

def main():
    tourist_spot_urls = [
        'https://ja.wikipedia.org/wiki/%E8%8C%A8%E5%9F%8E%E7%9C%8C%E3%81%AE%E8%A6%B3%E5%85%89%E5%9C%B0',
    ]

    for tourist_spot_url in tourist_spot_urls:
        tourism_info_dicts = []
        for url in scrape_all_urls(tourist_spot_url):
            try:
                tourism_info_dict = scrape_tourism_info(url)
                tourism_info_dicts.append(tourism_info_dict)
                print(tourism_info_dict['name'], tourism_info_dict['latitude'], tourism_info_dict['longitude'])
            except AttributeError:
                pass
        dump_tourism_info_dicts(tourism_info_dicts)

# ページ内の全てのURLを取得する
def scrape_all_urls(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    time.sleep(1)

    for tag in soup.find('div', id='bodyContent').find_all('a'):
        link = tag.get('href')
        if link == None:
            continue
        if link.startswith('/wiki/'):
            yield 'https://ja.wikipedia.org' + link

# 観光情報を取得する
def scrape_tourism_info(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    time.sleep(1)

    return {
        'name': scrape_name(soup),
        'latitude': scrape_latitude(soup), 
        'longitude': scrape_longitude(soup),
        'image': scrape_image(soup),
    }

# 観光地の名前を取得する
def scrape_name(soup):
    # 見出しを観光地の名前とする
    name = soup.find('h1')
    if name.text.startswith('ファイル:'):
        raise AttributeError
    return re.sub(r' \(.*\)', '', name.text)

# 観光地の緯度を取得する
def scrape_latitude(soup):
    latitude = soup.find('span', class_='latitude')
    return toDecimalLatitude(latitude.text)

# 観光地の経度を取得する
def scrape_longitude(soup):
    longitude = soup.find('span', class_='longitude')
    return toDecimalLongitude(longitude.text)

# 観光地の画像を取得する
def scrape_image(soup):
    url = ''
    for img in soup.find_all("img"):     #soup.find_all("img")でimgタグを抽出
        try:
            if int(img["width"]) > 100 and int(img['height']) > 100:
                url = 'https:' + img["src"]
                break
        except KeyError:
            pass
    if url == '':
        return ''

    if not os.path.exists('img'):
        os.mkdir('img')
    res = requests.get(url)
    path = 'img' + '/' + os.path.basename(url)
    with open(path, "wb") as pi:
        pi.write(res.content)

    time.sleep(1)

    return path

# 度分秒緯度を10進数緯度に変換する
def toDecimalLatitude(latitude):
    m = re.search(r'北緯(.*)度(.*)分(.*)秒', latitude)
    if not m:
        raise AttributeError
    
    degree = float(m.group(1))
    minute = float(m.group(2))
    seconds = float(m.group(3))

    return degree + minute / 60 + seconds / 3600

# 度分秒経度を10進数経度に変換する
def toDecimalLongitude(longitude):
    m = re.search(r'東経(.*)度(.*)分(.*)秒', longitude)
    if not m:
        raise AttributeError
    
    degree = float(m.group(1))
    minute = float(m.group(2))
    seconds = float(m.group(3))

    return degree + minute / 60 + seconds / 3600

# 観光情報を出力する
def dump_tourism_info_dicts(tourism_info_dicts):
    if not os.path.exists('json'):
        os.makedirs('json')
    dt_now = datetime.datetime.now()
    file_name = 'json/tourism_info_' + dt_now.strftime('%Y%m%d%H%M%S') + '.json'
    with open(file_name, 'w', encoding='utf_8') as f:
        json.dump(tourism_info_dicts, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
