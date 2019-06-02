from requests import session
from os import getcwd, path
from sys import exit
from time import sleep
from datetime import datetime
import json

api_url = 'https://api-pl-points.easypack24.net/v1/'


def poi_get(page_no=1, per_page=25):

    request_url = f'{api_url}points?page={page_no}&per_page={per_page}'

    with session() as session_req:
        data_collected = session_req.get(
            url=request_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
            }
        )

        return data_collected.json()


def app_error():
    print('[!] unable to collect data')
    exit()


def save_to_file(collected_items):
    file_name = datetime.now().strftime('%Y%m%d%H%M%S')
    file_path = path.join(getcwd(), f'{file_name}.json')

    with open(file_path, 'w') as items_file:
        json.dump(collected_items, items_file)


if __name__ == '__main__':
    print('Collecting data')

    items_per_page = 1000
    items_discovered = 0
    last_page = 9999
    collected = []

    api_response = poi_get(
        page_no=1,
        per_page=items_per_page
    )

    if api_response.get("items", None) is None:
        app_error()

    items_discovered = int(api_response.get('count', 0))
    print(f'[?] available to collect: {items_discovered}')

    if items_discovered == 0:
        app_error()

    collected = api_response.get("items", [])

    last_page = round(items_discovered / items_per_page)

    print(f'[1] items collected: {len(collected)} / {items_discovered}')

    for tmp_page_no in range(2, last_page + 2):
        collected_in_loop = poi_get(
            page_no=tmp_page_no,
            per_page=items_per_page
        )
        collected += collected_in_loop.get("items", [])
        print(f'[{tmp_page_no}] items collected: {len(collected)} / {items_discovered}')
        sleep(1)

    save_to_file(collected)

