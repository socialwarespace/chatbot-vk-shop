# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json
from vk_acc import prs as vk, vk as vkuser
import vk_api
from service import user_reqs, get_waiters, get_price, get_at, sizes, key_in_text, load_wall_photos
import os
from codecs import open
from bot_mode import new_req, could_be_req

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return "Hello, this is a thesender-bot portal"

def new_comment():
    return "ok"

tmrkt = -120508713
toptovar = -83390588
album = 247566796

def is_search_post(post):
    stop_words, li = [u'ищу', u'куплю', u'поиск'], [n.strip(",. \n") for n in post['text'].lower().split()]
    for n in stop_words:
        if n in li:
            return True
    return False

def is_news_post(post):
    if "#" in post['text']:
        return True

def get_daily_usernots(ui):
    photos = vkuser.method('photos.get', {'count': 100, 'owner_id': toptovar, 'album_id': album, 'offset': 0, 'rev': 1})['items']
    good = []
    for p in photos:
        if ui in get_waiters_many(p):
            good.append(p)
    posts = good[:5]
    ats = ",".join([get_at(n) for n in posts])
    text = ""
    for post in posts:
        text+=u'vk.com/photo{}_{} {}\n\n'.format(str(post['owner_id']), str(post['id']), get_price(post['text']))
    return text, ats
                             

def new_not(message, new=False):
    li = user_reqs(message['user_id'])
    ats = ""
    if new:
        text = u"Обновлен список подписок:\n\n" + "\n".join(li)
    else:
        today, ats = get_daily_usernots(message['user_id'])
        text = u"Спасибо, что воспользовались услугами бота! На данный момент Вами оформлены подписки на получение уведомлений о появлении товаров по следующим запросам:\n\n" + "\n".join(li) + u"\n\nПоследние посты по вашим подпискам (уведомления о следующих постах будут приходить мгновенно):\n" + today
    
    vk.method('messages.send', {'peer_id': message['user_id'], 'message': text, 'attachment': ats})
    return "ok"


def new_post(post):
    if is_search_post(post):
        return "this is search post!"
    if is_news_post(post):
        return "this is news post!"
    waiters = get_waiters(post)
    text = u'vk.com/photo{}_{} {}'.format(str(post['owner_id']), str(post['id']), get_price(post['text']))
    for ui in waiters:
        try:
            vk.method('messages.send', {'peer_id': ui, 'message': text, 'attachment': get_at(post)})
        except vk_api.ApiError:
            return str(ui)
    return "messages sent"+",".join([str(n) for n in waiters]+["124"])

def log_error(e):
    e = str(e)
    link = os.path.join(os.path.dirname(__file__), "error.txt")
    try:
        with open(link, "a", encoding='utf-8') as f:
            f.write("\n"+e)
    except Exception:
        with open(link, "w", encoding='utf-8') as f:
            f.write(e)        
    print e

@app.route("/api")
def api():
    li, final = load_wall_photos()[:10], []
    s = ",".join([str(n['signer_id']) for n in li])
    users = vkuser.method("users.get", {'user_ids': s})
    #return jsonify({"resp": users, "resp2": li})
    for n in li:
        n['name'] = ""
        for u in users:
            if n['signer_id'] == u['id']:
                n['name'] = u['first_name'] + u" " + u['last_name']
        if not n['link'] in [f['link'] for f in final]:
            final.append(n)
    answer = jsonify({"resp": final})
    answer.headers['Access-Control-Allow-Origin'] = '*'
    return answer

@app.route("/work", methods=["POST"])
def work():
    try:
        dic = request.json
        if dic['type'] == "confirmation":
            return "08453f76"
            #return "c2b06afe"
        elif dic['type'] == 'message_allow':
            message = dic['object']
            vk.method('messages.send', {'peer_id': message['user_id'], 'message': u"Добро пожаловать!"})
            return "ok"
        elif dic['type'] == 'message_new':
            message = dic['object']
            #if message['body'].lower() == "last":
            #    answer = get_daily_usernots(message['user_id'])
            #    vk.method('messages.send', {'peer_id': message['user_id'], 'message': answer[0], 'attachment': answer[1]})
            if could_be_req(message['body']):
                new_req(message)
            else:
                vk.method('messages.send', {'peer_id': message['user_id'], 'message': u'Запрос не распознан.\n\nО том как составить запрос:\nvk.com/topic-83390588_36293940'})
            return "ok"
        elif dic['type'] == 'new_photo':
            new_post(dic['photo'])
            return "ok"
        else:
            return "ok"
    except Exception as e:
        log_error(e)
        return "ok"

@app.route("/work2", methods=["POST"])
def work2():
    dic = request.json
    if dic['type'] == "confirmation":
        return "08453f76"
    return "ok"



if __name__ == "__main__":
    app.run("127.0.0.1", 80)
