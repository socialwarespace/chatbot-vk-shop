# -*- coding: utf-8 -*-
from vk_acc import vk, vk as vkuser
import re
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

toptovar = -83390588
group_id = 156904742
topic_id = 36354028


def get_jsizes(to_re=False):
    SYM = ""
    if to_re:
        SYM = "[ ]*"
    sizes = []
    for first in range(27, 37):
        for second in range(27, 39):
            sizes.append("{}{}X{}{}".format(first, SYM, SYM, second))
            if to_re:
                sizes.append("{}{}/{}{}".format(first, SYM, SYM, second))
    return sizes

sizes = [ "all", "ALL", "All", \
          "XS", "S", "M", "L", "XL", "XXL", "XXXL", \
          "37", "37.5", "38", "38.5", "39", "39.5", "40", "40.5", \
          "41", "41.5", "42", "42.5", "43", "43.5", "44", "44.5", "45", '27X27', '27X28', '27X29', '27X30', '27X31', '27X32', '27X33', '27X34', '27X35', '27X36', '27X37', '27X38', '28X27', '28X28', '28X29', '28X30', '28X31', '28X32', '28X33', '28X34', '28X35', '28X36', '28X37', '28X38', '29X27', '29X28', '29X29', '29X30', '29X31', '29X32', '29X33', '29X34', '29X35', '29X36', '29X37', '29X38', '30X27', '30X28', '30X29', '30X30', '30X31', '30X32', '30X33', '30X34', '30X35', '30X36', '30X37', '30X38', '31X27', '31X28', '31X29', '31X30', '31X31', '31X32', '31X33', '31X34', '31X35', '31X36', '31X37', '31X38', '32X27', '32X28', '32X29', '32X30', '32X31', '32X32', '32X33', '32X34', '32X35', '32X36', '32X37', '32X38', '33X27', '33X28', '33X29', '33X30', '33X31', '33X32', '33X33', '33X34', '33X35', '33X36', '33X37', '33X38', '34X27', '34X28', '34X29', '34X30', '34X31', '34X32', '34X33', '34X34', '34X35', '34X36', '34X37', '34X38', '35X27', '35X28', '35X29', '35X30', '35X31', '35X32', '35X33', '35X34', '35X35', '35X36', '35X37', '35X38', '36X27', '36X28', '36X29', '36X30', '36X31', '36X32', '36X33', '36X34', '36X35', '36X36', '36X37', '36X38']

def get_at(photo):
    return "photo"+str(photo['owner_id'])+u'_'+str(photo['id'])

def user_reqs(ui):
    good = []
    li = get_comments()
    for n in li:
        if n['from_id'] == ui:
            good.append(n['text'].lower().split("\n")[0])
    return good

def get_comments():
    #exampling  return [{u'date': 1511092576, u'text': u'all\nXL', u'id': 9, u'from_id': 163663706},\
    #        {u'date': 1511208089, u'text': u'all', u'id': 10, u'from_id': 337409123}]
    n, le, li = 0, 100, []
    while le == 100:
        resp = vk.method('board.getComments', {'count': 100, 'topic_id': topic_id,
                                        'group_id': group_id, 'offset': 1+n*100})
        li += resp['items']
        n += 1
        le = len(resp['items'])
    return li

def good_size(expected, text, maxi=True):
    if expected.lower() == "all":
        return True
    
    expected_sizes = expected.upper().split(",")
    if len(expected_sizes) == 0:
        return True

    sizes_in_text = get_size(text)
    if len(sizes_in_text) == 0:
        if maxi:
            return True
        return False

    for size in expected_sizes:
        if size in sizes_in_text:
            return True

    return False


def key_in_text(key, text):
    if key.lower() == "all":
        return True
    SYM = "!.,:-?\n"
    words = [n.strip(SYM) for n in key.lower().split()]
    for word in words:
        if not word in text.lower():
            return False
    return True 

def get_waiters(photo):
    li = get_comments()
    waiters = []

    for comment in li:
        if len(comment['text'].split("\n")) >= 2 or comment['text'] == "all":
            if key_in_text(comment['text'].split("\n")[0], photo['text']) and \
               good_size(comment['text'].split("\n")[-1], photo['text']):
                waiters.append(comment['from_id'])

    return list(set(waiters))

def get_price(text):

    return get_bel_price(text)

    li, bo = [n for n in re.findall(u'([boоб\\/\.]+)', text.lower()) if len(n) == 3 and len(re.findall("[\\/\.]", n)) > 0], ''
    if len(li) > 0:
        bo = 'b/o'

    r = '&#8381; '

    text = re.sub("\&\#8381\;", " ", text)
    text = re.sub("\(", " ", text)

    # 1 : 9,000 / 9.000 / 9 000
    first = [n for n in re.findall(u'([0-9\.\,оoоОO]+[\,\. ][0-9\.\,оoоОO]+)', text) if len(n) > 4]
    # 2 : 9k / 9к
    second = [re.sub("[ \.]", "", n+u'0'*(4-len((n+" . ").split(".")[1]))) for n in re.findall(u'([0-9\.\,]+)[ ]*[kк]', text)]
    # 3 : 9000
    third = [re.sub(u"[oооОO]", u"0", n) for n in re.findall(u'[\n ]([0-9оoоОO]+)[\n rр]', " " + text + " ") if len(n) > 3]
    prices = [int(re.sub(",", "", re.sub(" ", "", n))) for n in first + second + third]
    if len(prices) == 0:
        return bo
    prices.sort()
    return (str(prices[0]) + r + " " + bo).strip()


def get_bel_price(text):
    text = " " + re.sub("[\n\t ]+", " ", text) + " "

    li, bo = [n for n in re.findall(u'([boоб\\/\.]+)', text.lower()) if len(n) == 3 and len(re.findall("[\\/\.]", n)) > 0], ''
    full_bo = ""
    if len(li) > 0:
        bo = 'b/o'
        full_bo = '; b/o'

    def stand_price(s):
        return str(int(float(s)))

    r = u"(BYN|r|р|рублей|руб|rub|byn|Р|R)"
    USYM = u"\-\,\;\: "
    price_format = u"[0-9\.\,]+"

    price = re.findall(u"[{}]+({})[ ]*{}[{}]+".format(USYM, price_format, r, USYM), text)
    if len(price) > 0:
        return stand_price(price[0][0]) + " BYN" + full_bo

    return bo

def get_size(text):
    return get_ssize(text) + get_csize(text) + get_jsize(text)

def get_jsize(text):
    text = text.upper()
    li = re.findall("([23][0-9][ /X]+[23][0-9])", text)
    sizes = [re.sub("[\[\]\*Xx/ ]+", "X", size) for size in li]

    return sizes

def get_csize(text):
    text = " " + re.sub("[\n\t ]+", " ", text) + " "  # deleting all difficult spaces and adding spaces on borders
    #control: print text

    #### sizes of cloths
    sizes = [n.upper() for n in [ "xs", "s", "m", "l", "xl", "xxl", "xxxl" ]]
    ru_sizes = [ "хс", "с", "м", "л", "хл", "ххл", "хххл" ]
    ru_usizes = [ u"хс", u"с", u"м", u"л", u"хл", u"ххл", u"хххл" ]
    def get_ru_size(size, u=0):
        if u:
            return ru_usizes[sizes.index(size.upper())].upper()
        return ru_sizes[sizes.index(size.upper())].upper()
    found = {}

    ## expecting: 'NNN: S{SYM}M' => we need letter to have distance on one of two sizes
    SYM = "\-\,\;\: "
    USYM = u"\-\,\;\: "
    RASM = u"(размер|размеры|сайзы|size|сайз)"

    for size in sizes:
        found[size] = len(re.findall(u"([{}]{} )".format(USYM, size), text)) \
                      + len(re.findall(u"( {}[{}])".format(size, USYM), text)) \
                      + len(re.findall(u"([{}]{} )".format(USYM, get_ru_size(size, 1)), text)) \
                      + len(re.findall(u"( {}[{}])".format(get_ru_size(size, 1), USYM), text))

    ## expecting '{RASM} {SYM} X'
        found[size] += len(re.findall(u"{}[ ]*[{}]*[ ]*{}".format(RASM, USYM, size.lower()), text.lower())) \
                       + len(re.findall(u"{}[ ]*[{}]*[ ]*{}".format(RASM, USYM, get_ru_size(size, 1).lower()), text.lower()))
        
        # control: print size + str(found[size])
    cloth_sizes = [size for size in found if found[size] > 0]

    return cloth_sizes

def get_ssize(text):
    text = " " + re.sub("[\n\t ]+", " ", text) + " "
    def get_zsize(size):
        """ . -> ,  (zap size)"""
        return re.sub("\.", "\,", size)
    found = {}

    sizes = ["37", "37.5", "38", "38.5", "39", "39.5", "40", "40.5", \
             "41", "41.5", "42", "42.5", "43", "43.5", "44", "44.5", "45"]
    RASM = u"(размер|размеры|сайзы|size)"
    USYM = u"\-\,\;\: "

    for size in sizes:
        found[size] = len(re.findall("[{}]+{}[{}]+".format(USYM, size, USYM), text)) + \
                      len(re.findall("[{}]+{}[{}]+".format(USYM, get_zsize(size), USYM), text))

    shoes_sizes = [ n for n in found if found[n] > 0 ]
    return shoes_sizes

def get_post_descs(text, count):
    if count == 0:
        return []
    elif count == 1:
        return [text]

    pars = text.split("\n\n")

    if len(pars) == 1:  # maybe many photos of one item
        return [text]
    if len(pars) == count:
        return pars
    
    descs = []
    for p in pars:
        try:
            int(p[0])
            descs.append(p)
        except ValueError:
            pass
    if count > len(descs):
        return [""] * count
    return descs[:count]

def load_wall_photos():
    wall = vkuser.method("wall.get", {"owner_id": toptovar, "count": 100,\
                                       "filter": "owner", "offset": 1})['items']
    wall_photos = []
    for n in wall:
        descs = get_post_descs(n['text'], len(n.get("attachments", [])))
        if len(descs) == 1:
            n["attachments"] = n.get("attachments", [])[:1]
        for step, p in enumerate(n.get("attachments", [])):
            if p['type'] == 'photo':
                obj = p['photo']
                obj['text'] += u"    " + descs[step]
                #obj['signer_id'] = n.get('signer_id', '')
                obj['link'] = 'wall{}_{}'.format(str(n['owner_id']), str(n['id']))
                wall_photos.append(obj)

    return wall_photos

def load_photos(text, count=6, splitter=" "):
    items, n = [], 0
    tli = text.rsplit(splitter, 1)
    for p in load_wall_photos():
        print p['link']
        if key_in_text(tli[0], p['text']) and \
           good_size(tli[1], p['text'], False) and \
           len(items) < count:
            items.append(p)

    while len(items) < count and n < count:
        photos = vkuser.method('photos.getAll', {'count': 200, 'owner_id': toptovar, \
                                                 'offset': n*200, 'rev': 1})['items'] 

        for p in photos:
            if p['album_id'] != 242356583 and p['album_id'] != 221657593:
                if key_in_text(tli[0], p['text']) and \
                   good_size(tli[1], p['text'], False):
                    p['link'] = 'photo{}_{}'.format(str(p['owner_id']), str(p['id']))
                    items.append(p)
        n += 1

    return items

