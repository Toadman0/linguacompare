from flask import Flask, redirect, render_template, request, url_for, session
import requests
import sqlalchemy as db

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
app.secret_key = b'_6#y2L"F4Q8z\n\xec]/'

@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def main_page():
    if 'username' in session:
        username = session['username']
    else:
        username = False
    if request.method == 'GET':
        return render_template('LinguaCompare_main.html', username=username)
    elif request.method == 'POST':
        # responce равен вводу пользователя
        responce = request.form['text']
        family = request.form['family']
        if 'username' in session:
            print(0)
            insertion = users.insert().values([{"word": responce, "family": family, "username": session["username"], "password": session['password']}])
            connection.execute(insertion)
            select_all = db.select(users)
            select = connection.execute(select_all)
            print(select.fetchall())

        lang_1 = 'en'
        original = responce

        orig_w = f'{lang_1}: {original} [{get_transcription(original, original, lang_1, family, lang_1)}]'
        if get_translated_word(original, family, lang_1) == 'your word is not in dictionary':
            translations = get_translated_word(original, family, lang_1)
        else:
            translations = get_translated_word(original, family, lang_1)

        return render_template('LinguaCompare_main.html', username=username, defff=' '.join(get_definition(original)),
                               origgg=orig_w, trans=' '.join(translations))


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    error = None
    if request.method == 'GET':
        return render_template('sign_in.html', error='')
    elif request.method == 'POST':
        # responce равен вводу пользователя
        password = request.form['password']
        username = request.form['username']
        select_all = db.select(users)
        select = connection.execute(select_all)
        print(select.fetchall())

        if select.fetchall() == []:
            print(3)
            return render_template('sign_in.html', error='error')
        else:
            print(2)
            session['username'] = username
            session['password'] = password
            return redirect(url_for('main_page'))


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html', error='')
    elif request.method == 'POST':
        # responce равен вводу пользователя
        password = request.form['password']
        username = request.form['username']
        session['username'] = username
        session['password'] = password
        return redirect(url_for('main_page'))


@app.route('/log_out')
def log_out():
    print(1)
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('main_page'))


engine = db.create_engine('sqlite:///users.bd', echo=False)
connection = engine.connect()
metadata = db.MetaData()
users = db.Table('users', metadata,
                 db.Column('word_id', db.Integer, primary_key=True),
                 db.Column('word', db.Text),
                 db.Column('family', db.Text),
                 db.Column('username', db.Text),
                 db.Column('password', db.Text))
metadata.create_all(engine)
select_all = db.select(users)
select = connection.execute(select_all)
print(select.fetchall())
app.run(port=8080, host='127.0.0.1', debug=True)

# if __name__ == '__main__':
# *app.run(debug=True)D:/Milena/PycharmProjects/pythonProject_LINGUA_COMPARE
