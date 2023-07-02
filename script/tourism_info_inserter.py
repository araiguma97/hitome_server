import mysql.connector as mydb
import os
import glob
import json

import config

def main():
    tourism_info_json_paths = glob.glob('./json/tourism_info_*.json')
    for tourism_info_json_path in tourism_info_json_paths:
        insert_tourism_info(tourism_info_json_path)

def insert_tourism_info(tourism_info_json_path):
    tourism_info_json_path
    with open(tourism_info_json_path, mode='r', encoding='utf-8') as f:
        tourism_info_dicts = json.load(f)

    conn = mydb.connect(
        user=config.user,
        host=config.host,
        database=config.database,
    )
    conn.ping(reconnect=True)

    unique_tourism_info_dicts = list({tourism_info_dict['name']: tourism_info_dict for tourism_info_dict in tourism_info_dicts}.values())
    for tourism_info_dict in unique_tourism_info_dicts:
        with conn.cursor() as cursor:
            name = tourism_info_dict['name']
            latitude = str(tourism_info_dict['latitude'])
            longitude = str(tourism_info_dict['longitude'])
            cursor.execute('INSERT INTO tourism_info (name, latitude, longitude) VALUES (%s, %s, %s)', (name, latitude, longitude))
     
        conn.commit()

    conn.close()

if __name__ == '__main__':
    main()
