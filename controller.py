# -*- coding: utf-8 -*-
import requests
from vk_acc import vk
import time
from codecs import open
from json import load, loads
import os

cache = os.path.join(os.path.dirname(__file__), 'basa', 'cache.txt')

toptovar = -83390588
album = 247566796

def load_last_photos():
    limit = 40000
    li = []
    photos = vk.method('photos.get', {'count': 10, 'owner_id': toptovar, 'album_id': album, 'offset': 0, 'rev': 1})['items']
    for photo in photos:
        if time.time() - photo['date']  > limit:
            return li
        else:
            li.append(photo)
    return li

def photo_is_new(post):
    with open(cache, 'r', encoding='utf-8') as f:
        li = f.read().split()
    if str(post) in li:
        return False
    return True

def notificate_photo(post):
    link = "http://vkbc.ru/work"
    with open(cache, 'a', encoding='utf-8') as f:
        f.write(str(post['id'])+u' ')
    return requests.post(link, json={"type": "new_photo", "photo": post}).text

def main():
    start_time = time.time()
    n = 0
    while time.time() - start_time < 56:
        n += 1
        try:
            photos = load_last_photos()
            for photo in photos:
                if photo_is_new(photo['id']):
                    print notificate_photo(photo) + str(photo['id'])
            print "no new photos"
        except requests.ConnectionError:
            print "Connection Error"
        time.sleep(1)

if __name__ == "__main__":
    main()
