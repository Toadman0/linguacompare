from flask import Flask, flash, redirect, render_template, request, url_for
import requests

language_family = {
    'Altaic':
        {'turkic': ['tr']},

    'Uralic':
        {'finno-ugric': ['et', 'fi']},

    'Indo-European':
        {'baltic': ['lt', 'lv'],
         'germanic': ['de', 'da', 'nl', 'no', 'sv'],
         'italic (romance)': ['es', 'fr', 'it', 'pt'],
         'slavic': ['cs', 'ru', 'sk', 'uk'],
         'greek': ['el']}
}

transcription_lang = ['en', 'fr', 'de', 'it', 'es']

ya_apikey = 'dict.1.1.20240109T131316Z.71e2c62d901c4efe.0fccfa5c1185841d0dbd117d64db1692293ba6c6'
mw_apikey = 'e4a1c6a2-09e6-4f31-9192-716b98c020b4'

'''
        cs чешский
        da датский
        de немецкий
        el греческий
        en английский
        es испанский
        et эстонский
        fi финнский
        fr франц
        it итальяно
        lt литовский
        lv латышский
        nl голландский
        no норвежский
        pt португальский
        ru русский
        sk словацкий
        sv шведский
        tr турецк
        uk укр
'''


def get_translated_word(original, family, lang_1):
    translations = []
    for group in language_family[family]:
        for lang_2 in language_family[family][group]:
            url = f"https://dictionary.yandex.net/api/v1/dicservice.json/" \
                  f"lookup?key={ya_apikey}&lang={lang_1}-{lang_2}&text={original}"
            response = requests.get(url)

            if response:
                if response.json() == {'head': {}, 'def': []}:
                    # print(response.json())
                    return 'your word is not in dictionary'
                tr_word = response.json()['def'][0]['tr'][0]['text']
                tr = '—'

                if lang_2 not in transcription_lang:
                    tr = '—'

                tr_url = f"https://dictionary.yandex.net/api/v1/dicservice.json/" \
                         f"lookup?key={ya_apikey}&lang={lang_2}-{lang_1}&text={tr_word}"
                tr_response = requests.get(tr_url)
                if tr_response:
                    try:
                        transcription = tr_response.json()['def'][0]['ts']
                        tr = transcription
                    except IndexError:
                        tr = '—'
                    except KeyError:
                        tr = '—'

                back = f'{lang_2}: {tr_word} [{tr}]'

                translations.append(back)

    return translations


def get_definition(original):
    url_mw = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{original}?key={mw_apikey}"
    response_mw = requests.get(url_mw)
    shortdef = response_mw.json()[0]['shortdef']
    def_of_word = f'definition:', '; '.join(shortdef)
    return def_of_word


def get_translated_word(original, family, lang_1):
    translations = []
    for group in language_family[family]:
        for lang_2 in language_family[family][group]:
            url = f"https://dictionary.yandex.net/api/v1/dicservice.json/" \
                  f"lookup?key={ya_apikey}&lang={lang_1}-{lang_2}&text={original}"
            response = requests.get(url)

            if response:
                if response.json() == {'head': {}, 'def': []}:
                    # print(response.json())
                    return 'your word is not in dictionary'
                tr_word = response.json()['def'][0]['tr'][0]['text']
                tr = '—'

                if lang_2 not in transcription_lang:
                    tr = '—'

                tr_url = f"https://dictionary.yandex.net/api/v1/dicservice.json/" \
                         f"lookup?key={ya_apikey}&lang={lang_2}-{lang_1}&text={tr_word}"
                tr_response = requests.get(tr_url)
                if tr_response:
                    try:
                        transcription = tr_response.json()['def'][0]['ts']
                        tr = transcription
                    except IndexError:
                        tr = '—'
                    except KeyError:
                        tr = '—'

                back = f'{lang_2}: {tr_word} [{tr}]'

                translations.append(back)

    return translations


def get_transcription(original, word, lang_tr, family, lang_1='en'):
    if word == get_translated_word(original, family, lang_1):
        lang_1_, lang_2_ = lang_1, lang_tr
    else:
        lang_1_, lang_2_ = lang_tr, lang_1

    if lang_2_ not in transcription_lang:
        return '—'

    tr_url = f"https://dictionary.yandex.net/api/v1/dicservice.json/" \
             f"lookup?key={ya_apikey}&lang={lang_2_}-{lang_1_}&text={word}"
    tr_response = requests.get(tr_url)
    if tr_response:
        try:
            transcription = tr_response.json()['def'][0]['ts']
            return transcription
        except IndexError:
            return '—'


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main_page():
    if request.method == 'GET':
        return render_template('LinguaCompare_main.html')
    elif request.method == 'POST':
        # responce равен вводу пользователя
        responce = request.form['text']
        family = request.form['family']

        lang_1 = 'en'
        original = responce

        orig_w = f'{lang_1}: {original} [{get_transcription(original, original, lang_1, family, lang_1)}]'
        if get_translated_word(original, family, lang_1) == 'your word is not in dictionary':
            translations = get_translated_word(original, family, lang_1)
        else:
            translations = get_translated_word(original, family, lang_1)

        return render_template('LinguaCompare_main.html', defff=' '.join(get_definition(original)),
                               origgg=orig_w, trans=' '.join(translations))

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    error = None
    if request.method == 'GET':
        return render_template('test.html')
    elif request.method == 'POST':
        # responce равен вводу пользователя
        password = request.form['password']
        username = request.form['username']
        if password != 'a' or username != 'a':
            error = u'error'
        else:
            flash(u'sakses')
            return redirect(url_for(''))
        print(password, username)
    return render_template('test.html', error=error)



@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    elif request.method == 'POST':
        # responce равен вводу пользователя
        password = request.form['password']
        username = request.form['username']
        print(password, username)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

# if __name__ == '__main__':
# *app.run(debug=True)D:/Milena/PycharmProjects/pythonProject_LINGUA_COMPARE
