from flask import Flask, request
import logging
import json
import random
import math
import requests


app = Flask(__name__)


logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

anecs = open( "apij.txt", "r" ).read().split("@")
languages = json.loads( open( "languages.json", "r" ).read() )
rev_langs = json.loads( open( "rev_langs.json", "r" ).read() )

sessionStorage = dict()

def brea(user_id):
    sessionStorage[user_id] = { "game": None,
                                "words": list(),
                                "law": "" }




@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False,
            "buttons": [
                {
                    "title": "Активная гиперссылка на сервис Яндекс.Переводчик",
                    "payload": {},
                    "url": "http://translate.yandex.ru/",
                    "hide": False
                }
            ]
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    res["response"]["text"] = ""


    def redraw_field(x, y):
        w, h, m, field, smf, flags = sessionStorage[user_id]["words"]
        if field[y][x] == 9:
            return False
        if field[y][x] != 0:
            smf[y][x] = '0'
            return True
        smf[y][x] = ' '
        lasmf = []
        for i in range(h):
            lasmf.append(['='] * w)
        while True:
            for b in range(h):
                for a in range(w):
                    if smf[b][a] == ' ':
                        x, y = a, b
                        break
            tech(x, y, [0], ' ', ['='])
            tech(x, y, [1, 2, 3, 4, 5, 6, 7, 8], 'H', ['=', ' ', '0'])
            smf[y][x] = '0'
            if lasmf == smf:
                break
            for i in range(h):
                for j in range(w):
                    lasmf[i][j] = smf[i][j]
        return True


    def print_field():
        w, h, m, field, smf, flags = sessionStorage[user_id]["words"]
        ans = ""
        if w > 9 and h > 9:
            print('____' + '__'.join([str(e + 1) for e in range(9)]) + '__' +
                  '_'.join([str(e + 1) for e in range(9, w)]))
        elif h > 9:
            print('___' + '_'.join([str(e + 1) for e in range(w)]))
        elif w > 9:
            print('____' + '__'.join([str(e + 1) for e in range(9)]) + '__' +
                  '_'.join([str(e + 1) for e in range(9, w)]))
        else:
            print('__' + '_'.join([str(e + 1) for e in range(w)]))
        for a in range(h):
            if a < 9 < h and w > 9:
                n = '_' + str(a + 1) + '__'
            elif w > 9:
                n = str(a + 1) + '__'
            elif a < 9 < h:
                n = '_' + str(a + 1) + '_'
            else:
                n = str(a + 1) + '_'
            for b in range(w):
                if smf[a][b] == 'Δ':
                    n += 'Δ'
                elif smf[a][b] != '=' and field[a][b] != 0:
                    n += str(field[a][b])
                elif smf[a][b] != '=':
                    n += '_'
                else:
                    n += '='
                if w > 9:
                    n += '__'
                else:
                    n += ''
            print(n)


    def tech(x, y, args, rep, rags):
        w, h, m, field, smf, flags = sessionStorage[user_id]["words"]
        if y > 0 and field[y - 1][x] in args and smf[y - 1][x] in rags:
            smf[y - 1][x] = rep
        if x > 0 and field[y][x - 1] in args and smf[y][x - 1] in rags:
            smf[y][x - 1] = rep
        if y < h - 1 and field[y + 1][x] in args and smf[y + 1][x] in rags:
            smf[y + 1][x] = rep
        if x < w - 1 and field[y][x + 1] in args and smf[y][x + 1] in rags:
            smf[y][x + 1] = rep

    def print(string):
        res["response"]["text"] += string + "\n"

    if req["session"]["new"]:
        sessionStorage[user_id] = { "game": None,
                                    "words": list(),
                                    "law": "" }
        res["response"]["text"] = """ПРИВЕЕЕЕЕЕЕТ!!!!
        я -- кибернетический организм, вот список моих комманд:
        переведи {русское слово} на {язык}
        определи язык {слова или предложения}
        переведи {иностранное слово} на русский
        расскажи анекдот
        сыграем в слова рус/анг
        сыграем в сапера"""
        return
    try:
        rq = req["request"]["original_utterance"]
    except:
        res["response"]["text"] = "а теперь введите команду"
        return
    if rq == "конец!":
        sessionStorage[user_id] = { "game": None,
                                    "words": list(),
                                    "law": "" }
    if sessionStorage[user_id]["game"] == "рус":
        res["response"]["text"] = ""
        inp = open( "rus.txt", "r" )
        if sessionStorage[user_id]["law"] and rq[0] != sessionStorage[user_id]["law"][-1]:
            res["response"]["text"] = "ты говоришь неправильное слово!, подумай еще и найди слово на {}".format(sessionStorage[user_id]["law"][-1])
            return
        l = 1
        while True:
            for j in range(1000):
                wd = inp.readline()[:-1]

                if wd[0] == rq[-l] and j not in sessionStorage[user_id]["words"]:
                    sessionStorage[user_id]["words"].append(j)
                    res["response"]["text"] += " а вот и слово: " + wd
                    sessionStorage[user_id]["law"] = wd
                    if wd[-1] == "ь":
                        res["response"]["text"] += " тебе на {}".format(wd[-2])
                        sessionStorage[user_id]["law"] = wd[:-1]
                    return
            inp.seek(0)
            res["response"]["text"] += "слово на {} не нашел, ищу на {}".format(rq[-l], rq[-l-1])
            l += 1
            if l > len(rq):
                res["response"]["text"] = "я не могу найти ответа на это слово, можешь считать что я проиграл, но игра продолжается"
                return

    if sessionStorage[user_id]["game"] == "анг":
        res["response"]["text"] = ""
        inp = open( "eng.txt", "r" )
        if sessionStorage[user_id]["law"] and rq[0] != sessionStorage[user_id]["law"][-1]:
            res["response"]["text"] = "ты говоришь неправильное слово!, подумай еще и найди слово на {}".format(sessionStorage[user_id]["law"][-1])
            return
        l = 1
        while True:
            for j in range(1000):
                wd = inp.readline()[:-1]

                if wd[0] == rq[-l] and j not in sessionStorage[user_id]["words"]:
                    sessionStorage[user_id]["words"].append(j)
                    res["response"]["text"] += " а вот и слово: " + wd
                    sessionStorage[user_id]["law"] = wd
                    if wd[-1] == "ь":
                        res["response"]["text"] += " тебе на {}".format(wd[-1])
                        sessionStorage[user_id]["law"] = wd[:-1]
                    return
            inp.seek(0)
            res["response"]["text"] += "слово на {} не нашел, ищу на {}".format(rq[-l], rq[-l-1])
            l += 1
            if l > len(rq):
                res["response"]["text"] = "я не могу найти ответа на это слово, можешь считать что я проиграл, но игра продолжается"
                return

    if sessionStorage[user_id]["game"] == "mine":
        if sessionStorage[user_id]["law"] == "wh":
            try:
                w, h = [int(i) for i in rq.split()]
            except:
                print("вы ввели какие-то странные данные, попробуйте еще раз")
                return
            sessionStorage[user_id]["words"] += [w, h]
            if w > 30 or h > 30:
                print("извините, но размеры поля привышают 30х30, попробуйте снова")
                sessionStorage[user_id]["words"] = list()
                return
            else:
                sessionStorage[user_id]["law"] = "wh+"

        if sessionStorage[user_id]["law"] == "wh+":
            print('УСТАНОВИТЕ КОЛИЧЕСТВО БОМБ')
            sessionStorage[user_id]["law"] = "m"
        elif sessionStorage[user_id]["law"] == "m":
            try:
                m = int( rq )
            except:
                print("вы ввели какие-то странные данные, попробуйте еще раз")
                return
       
            w, h = sessionStorage[user_id]["words"][:2]
            if m > w * h:
                print("извините, но количество бомб выше количества клеток поля, попробуйте снова")
                return
            else:
                sessionStorage[user_id]["words"].append(m)
                sessionStorage[user_id]["law"] = "m+"
        if sessionStorage[user_id]["law"] == "m+":
            w, h, m = sessionStorage[user_id]["words"]
            flags = m
            restart = False
            # Создаем и заполняем техническое поле.И создаем и заполняем визуальное поле
            field = []
            smf = []
            for a in range(h):
                field.append([0] * w)
                smf.append(['='] * w)
            # Создаем список всех координат, на которых может быть бомба
            # И устанавливаем случайным образом m бомб
            sessionStorage[user_id]["words"] += [field, smf, flags]

            t = [(a, b) for a in range(h) for b in range(w)]
            for i in range(m):
                p = random.randrange(len(t))
                y, x = t[p]
                del t[p]
                field[y][x] = 9
                if y > 0 and x > 0 and field[y - 1][x - 1] != 9:
                    field[y - 1][x - 1] += 1
                if y > 0 and field[y - 1][x] != 9:
                    field[y - 1][x] += 1
                if y > 0 and x < w - 1 and field[y - 1][x + 1] != 9:
                    field[y - 1][x + 1] += 1
                if y < h - 1 and field[y + 1][x] != 9:
                    field[y + 1][x] += 1
                if y < h - 1 and x > 0 and field[y + 1][x - 1] != 9:
                    field[y + 1][x - 1] += 1
                if y < h - 1 and x < w - 1 and field[y + 1][x + 1] != 9:
                    field[y + 1][x + 1] += 1
                if x < w - 1 and field[y][x + 1] != 9:
                    field[y][x + 1] += 1
                if x > 0 and field[y][x - 1] != 9:
                    field[y][x - 1] += 1

            print('СПРАВКА           для справки напишите s')
            print('ЗАБЕЙТЕ КООРДИНАТЫ ПО X И Y ЧЕРЕЗ БРОБЕЛ')
            print('ДЛЯ УСТАНОВКИ ФЛАГА НАПИШИТЕ       X Y d')

            # НАЧИНАЕМ ИГРАТЬ))
            print_field()
            sessionStorage[user_id]["law"] = "w+++"
        elif sessionStorage[user_id]["law"] == "w+++":
            w, h, m, field, smf, flags = sessionStorage[user_id]["words"]

            it = rq.split()
            # Здесь мы добавляем возможность ставить флажки
            if len(it) == 1:
                print('СПРАВКА    для справки напишите s')
                print('ЗАБЕЙТЕ КООРДИНАТЫ ПО X И Y ЧЕРЕЗ БРОБЕЛ')
                print('ДЛЯ УСТАНОВКИ ФЛАГА НАПИШИТЕ X Y d')
                return
            if len(it) == 3:
                try:
                    x, y = int(it[0]) - 1, int(it[1]) - 1
                except:
                    print("вы ввели какие-то странные данные, попробуйте еще раз")
                    return
                            
                if x > w or h > y:
                    print("координаты вышли за границы, попробуйте еще")
                    return

                if smf[y][x] == 'Δ':
                    smf[y][x] = '='
                    flags += 1
                    print_field()
                    return
                if flags == 0:
                    print('У ВАС ЗАКОНЧИИЛИСЬ ФЛАГИ, ПОСТАВЬТЕ НА '
                          'ТУ ЖЕ КЛЕТКУ, ЧТОБЫ УБРАТЬ')
                    print_field()
                    return
                if smf[y][x] == '=':
                    smf[y][x] = 'Δ'
                else:
                    print('НЕЛЬЗЯ ПОСТАВИТЬ ФЛАГ НА ИЗВЕСТНУЮ КЛЕТКУ')
                    print_field()
                    return
                flags -= 1
                print_field()
                fg = False
                for a in range(h):
                    for b in range(w):
                        if field[a][b] == 9 and smf[a][b] != 'Δ':
                            fg = True
                            brea(user_id)
                            return
                    if fg:
                        brea(user_id)
                        return
                else:
                    print('ВЫ ВЫИГРАЛИ')
                    brea(user_id)
                    return
                return
            try:
                x, y = int(it[0]) - 1, int(it[1]) - 1
            except:
                print("вы ввели какие-то странные данные, попробуйте еще раз")
                return
            if x > w or y > h:
                print("координаты вышли за границы, попробуйте еще")
                return

            
            if not redraw_field(x, y):
                print('GAME OVER')
                brea(user_id)
                return
            print_field()
            sessionStorage[user_id][3] = field
            sessionStorage[user_id][4] = smf

        return

    if rq.endswith( "на русский" ):
        word = rq.split()[1]
        url = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
        key = "key=trnsl.1.1.2019041    7T145812Z.69aff170ae6543ff.5e8cfd7482419796d98656726fd70c0a061374ef&"
        tr = requests.get( url + key + "lang=ru" + "&text=" + word ).json()["text"][0]

        res["response"]["text"] = "а вот и перевод: " + tr + " Перевод осуществлён сервисом Яндекс.Переводчик"

    elif rq.startswith("переведи"):
        word = rq.split()[1]
        lang = languages[ rq.split()[-1] ]
        url = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
        key = "key=trnsl.1.1.20190417T145812Z.69aff170ae6543ff.5e8cfd7482419796d98656726fd70c0a061374ef&"

        tr = requests.get( url + key + "lang=" + "ru-" + lang + "&text=" + word ).json()["text"][0]

        res["response"]["text"] = "а вот и оно: " + tr + " Перевод осуществлён сервисом Яндекс.Переводчик"

    elif rq.startswith("определи язык"):
        word = " ".join( rq.split()[2:] )
        url = "https://translate.yandex.net/api/v1.5/tr.json/detect?"
        key = "key=trnsl.1.1.20190417T145812Z.69aff170ae6543ff.5e8cfd7482419796d98656726fd70c0a061374ef&"
        lang = requests.get( url + key + "text=" + word ).json()["lang"]
        res["response"]["text"] = "высока вероятность, что язык текста " + rev_langs[lang] + " анализ осуществлён сервисом Яндекс.Переводчик"

    elif rq == "расскажи анекдот":
        res["response"]["text"] = random.choice( anecs )

    elif rq == "сыграем в слова рус":
        res["response"]["text"] = "игра в слова, только сразу предупрежу, у меня запас словарный не очень. Чтобы выйти из игры напиши конец!"
        sessionStorage[user_id]["game"] = "рус"

    elif rq == "сыграем в слова анг":
        res["response"]["text"] = "игра в слова, только сразу предупрежу, у меня запас словарный не очень. Чтобы выйти из игры напиши конец!"
        sessionStorage[user_id]["game"] = "анг"

    elif rq == "конец!":
        res["response"]["text"] = "игра закончилась, дальше давай команды"

    elif rq == "сыграем в сапера":


        print( """УСТАНОВИТЕ РАЗМЕРЫ ПОЛЯ  ширина высота
                 (до 30х30) """)
        sessionStorage[user_id]["game"] = "mine"
        sessionStorage[user_id]["law"] = "wh"


    else:
        res["response"]["text"] = "команда не распознана, попробуй снова"


if __name__ == "__main__":
    app.run()

