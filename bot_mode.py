# -*- coding: utf-8 -*-
from service import get_price, get_at, sizes, key_in_text, good_size, load_photos
from vk_acc import prs as vk, vk as vkuser

toptovar = -83390588
album = 247566796


def new_req(message):
    ui = message['user_id']
    text = message['body']

    items = load_photos(text)[:6]

    if len(items) == 0:
        vk.method("messages.send", {"peer_id": ui, "message": u'Данный товар не был найден в паблике toptovar'})

    ats = ",".join([get_at(n) for n in items])
    text = ""
    for post in items:
        text+=u'vk.com/{} {}\n\n'.format(post['link'], get_price(post['text']))

    vk.method("messages.send", {"peer_id": ui, "message": text, "attachment": ats})

    return "ok"

def could_be_req(text, splitter=" "):
    li = text.rsplit(splitter, 1)
    if len(li) < 2:
        return False
    if not li[1].upper() in sizes:
        return False
    return True
