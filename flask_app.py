from flask import Flask, request
import logging
import json
import random
import math
import requests


app = Flask(__name__)
 
# Добавляем логирование в файл. Чтобы найти файл, 
# перейдите на pythonwhere в раздел files, он лежит в корневой папке
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

anecs = open( "apij.txt", "r" ).read().split("@")
languages = {"азербайджанский": "az",
             "малаялам": "ml",
             "албанский": "sq",
             "мальтийский": "mt",
             "амхарский": "am",
             "македонский": "mk",
             "английский": "en",
             "маори": "mi",
             "арабский": "ar",
             "маратхи": "mr",
             "армянский": "hy",
             "марийский": "mhr",
             "африкаанс": "af",
             "монгольский": "mn",
             "баскский": "eu",
             "немецкий": "de",
             "башкирский": "ba",
             "непальский": "ne",
             "белорусский": "be",
             "норвежский": "no",
             "бенгальский": "bn",
             "панджаби": "pa",
             "бирманский": "my",
             "папьяменто": "pap",
             "болгарский": "bg",
             "персидский": "fa",
             "боснийский": "bs",
             "польский": "pl",
             "валлийский": "cy",
             "португальский": "pt",
             "венгерский": "hu",
             "румынский": "ro",
             "вьетнамский": "vi",
             "русский": "ru",
             "гаитянский": "ht",
             "себуанский": "ceb",
             "галисийский": "gl",
             "сербский": "sr",
             "голландский": "nl",
             "сингальский": "si",
             "горномарийский": "mrj",
             "словацкий": "sk",
             "греческий": "el",
             "словенский": "sl",
             "грузинский": "ka",
             "суахили": "sw",
             "гуджарати": "gu",
             "сунданский": "su",
             "датский": "da",
             "таджикский": "tg",
             "иврит": "he",
             "тайский": "th",
             "идиш": "yi",
             "тагальский": "tl",
             "индонезийский": "id",
             "тамильский": "ta",
             "ирландский": "ga",
             "татарский": "tt",
             "итальянский": "it",
             "телугу": "te",
             "исландский": "is",
             "турецкий": "tr",
             "испанский": "es",
             "удмуртский": "udm",
             "казахский": "kk",
             "узбекский": "uz",
             "каннада": "kn",
             "украинский": "uk",
             "каталанский": "ca",
             "урду": "ur",
             "киргизский": "ky",
             "финский": "fi",
             "китайский": "zh",
             "французский": "fr",
             "корейский": "ko",
             "хинди": "hi",
             "коса": "xh",
             "хорватский": "hr",
             "кхмерский": "km",
             "чешский": "cs",
             "лаосский": "lo",
             "шведский": "sv",
             "латынь": "la",
             "шотландский": "gd",
             "латышский": "lv",
             "эстонский": "et",
             "литовский": "lt",
             "эсперанто": "eo",
             "люксембургский": "lb",
             "яванский": "jv",
             "малагасийский": "mg",
             "японский": "ja",
             "малайский": "ms",
}

rev_langs = {"az": "азербайджанский",
             "ml": "малаялам",
             "sq": "албанский",
             "mt": "мальтийский",
             "am": "амхарский",
             "mk": "македонский",
             "en": "английский",
             "mi": "маори",
             "ar": "арабский",
             "mr": "маратхи",
             "hy": "армянский",
             "mhr": "марийский",
             "af": "африкаанс",
             "mn": "монгольский",
             "eu": "баскский",
             "de": "немецкий",
             "ba": "башкирский",
             "ne": "непальский",
             "be": "белорусский",
             "no": "норвежский",
             "bn": "бенгальский",
             "pa": "панджаби",
             "my": "бирманский",
             "pap": "папьяменто",
             "bg": "болгарский",
             "fa": "персидский",
             "bs": "боснийский",
             "pl": "польский",
             "cy": "валлийский",
             "pt": "португальский",
             "hu": "венгерский",
             "ro": "румынский",
             "vi": "вьетнамский",
             "ru": "русский",
             "ht": "гаитянский",
             "ceb": "себуанский",
             "gl": "галисийский",
             "sr": "сербский",
             "nl": "голландский",
             "si": "сингальский",
             "mrj": "горномарийский",
             "sk": "словацкий",
             "el": "греческий",
             "sl": "словенский",
             "ka": "грузинский",
             "sw": "суахили",
             "gu": "гуджарати",
             "su": "сунданский",
             "da": "датский",
             "tg": "таджикский",
             "he": "иврит",
             "th": "тайский",
             "yi": "идиш",             
             "tl": "тагальский",
             "id": "индонезийский",
             "ta": "тамильский",
             "ga": "ирландский",
             "tt": "татарский",
             "it": "итальянский",
             "te": "телугу",
             "is": "исландский",
             "tr": "турецкий",
             "es": "испанский",
             "udm": "удмуртский",
             "kk": "казахский",
             "uz": "узбекский",
             "kn": "каннада",
             "uk": "украинский",
             "ca": "каталанский",
             "ur": "урду",
             "ky": "киргизский",
             "fi": "финский",
             "zh": "китайский",
             "fr": "французский",
             "ko": "корейский",
             "hi": "хинди",
             "xh": "коса",
             "hr": "хорватский",
             "km": "кхмерский",
             "cs": "чешский",
             "lo": "лаосский",
             "sv": "шведский",
             "la": "латынь",
             "gd": "шотландский",
             "lv": "латышский",
             "et": "эстонский",
             "lt": "литовский",
             "eo": "эсперанто",
             "lb": "люксембургский",
             "jv": "яванский",
             "mg": "малагасийский",
             "ja": "японский",
             "ms": "малайский",
}

sessionStorage = dict()

@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)
 
 
def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req["session"]["new"]:
        sessionStorage[user_id] = { "game": None,
                                    "words": list(),
                                    "law": "" }
        res["response"]["text"] = """ПРИВЕЕЕЕЕЕЕТ!!!!
        я -- кибернетический организм, вот список моих комманд:
        переведи {русское слово} на {язык}
        определи язык {слова}
        расскажи анекдот
        сыграем в слова рус/анг"""
        return    

    rq = req["request"]["original_utterance"]
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
            
    if rq.startswith("переведи"):
        word = rq.split()[1]
        lang = languages[ rq.split()[-1] ]
        url = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
        key = "key=trnsl.1.1.20190417T145812Z.69aff170ae6543ff.5e8cfd7482419796d98656726fd70c0a061374ef&"

        tr = requests.get( url + key + "lang=" + "ru-" + lang + "&text=" + word ).json()["text"][0]
        res["response"]["text"] = "а вот и оно: " + tr
    
    elif rq.startswith("определи язык"):
        word = " ".join( rq.split()[2:] )
        url = "https://translate.yandex.net/api/v1.5/tr.json/detect?"
        key = "key=trnsl.1.1.20190417T145812Z.69aff170ae6543ff.5e8cfd7482419796d98656726fd70c0a061374ef&"
        lang = requests.get( url + key + "text=" + word ).json()["lang"]
        res["response"]["text"] = "высока вероятность, что язык текста " + rev_langs[lang]
    
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

    else:
        res["response"]["text"] = "команда не распознана, попробуй снова"
        
    


    #if rq.startswith("переведите слово"):
     #   lang = get_lang(rq[16:])
      #  lang = {"en": "ru", "ru": "en"}[lang]
       # url = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
        #key = "key=trnsl.1.1.20190417T145812Z.69aff170ae6543ff.5e8cfd7482419796d98656726fd70c0a061374ef&"
    #    tr = requests.get( url + key + "lang=" + lang + "&text=" + rq[16:] ).json()["text"][0]
     #   res["response"]["text"] = tr
    #elif rq.startswith("переведи слово"):
     #   lang = get_lang(rq[14:])
      #  lang = {"en": "ru", "ru": "en"}[lang]
       # url = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
    #    key = "key=trnsl.1.1.20190417T145812Z.69aff170ae6543ff.5e8cfd7482419796d98656726fd70c0a061374ef&"
     #   tr = requests.get( url + key + "lang=" + lang + "&text=" + rq[14:] ).json()["text"][0]
      #  res["response"]["text"] = tr
        

if __name__ == "__main__":
    app.run()
    
