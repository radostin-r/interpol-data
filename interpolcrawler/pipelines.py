# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

import requests


class InterpolcrawlerPipeline(object):

    def __init__(self):
        self.conn = None
        self.curr = None
        self.create_db_connection()
        self.create_table()

    def create_db_connection(self):
        self.conn = sqlite3.connect('interpoldata.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS person_data_tb""")
        self.curr.execute("""
            create table person_data_tb(
                person_id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                place_of_birth TEXT,
                date_of_birth TEXT,
                nationality TEXT,
                eye_color TEXT,
                hair_color TEXT,
                sex TEXT,
                height INTEGER,
                weight INTEGER,
                image_url TEXT,
                link TEXT
            )
        """)

    def store_record(self, person):
        # check for person img url
        img_url = None
        person_link = None

        if '_links' in person:
            if 'self' in person['_links'] and 'href' in person['_links']['self']:
                person_link = person['_links']['self']['href']

            if 'images' in person['_links'] and 'href' in person['_links']['images']:
                img_data = requests.get(person['_links']['images']['href']).json()
                if '_embedded' in img_data and 'images' in img_data['_embedded'] and img_data['_embedded']['images']:
                    img_url = img_data['_embedded']['images'][0]

                    if '_links' in img_url and 'self' in img_url['_links'] and 'href' in img_url['_links']['self']:
                        img_url = img_url['_links']['self']['href']

        self.curr.execute("""INSERT INTO person_data_tb values (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            person['entity_id'],
            person['forename'],
            person['name'],
            person['place_of_birth'],
            person['date_of_birth'],
            ', '.join(person['nationalities']),
            ', '.join(person['eyes_colors_id']) if person['eyes_colors_id'] else None,
            ', '.join(person['hairs_id']) if person['hairs_id'] else None,
            person['sex_id'],
            person['height'],
            person['weight'],
            img_url,
            person_link
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        # get self data from request and save to db
        if '_links' in item and 'self' in item['_links'] and 'href' in item['_links']['self']:
            person_data = requests.get(item['_links']['self']['href'])
            self.store_record(person_data.json())
        return item

