# программа
# поднимающая 
# сервер 
# Lingua Compare

# навреное

# может быть

# возможно

from flask import Flask, flash, redirect, render_template, request, url_for, session
from data import db_session
from data.users import User
import requests

# переменная с языковыми семьями
# нужна для передачи соответствующего
# языка для определённой языковой
# семьи.
# является глобальной
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

# апи ключ для доступа
# к сервису яндекс словарь

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


# функция для получения перевода
# слов
# на вход получает
# original - слово
# family - языковая семья
# lang_1 - язык на котором написан слово

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
    print(family)
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


# запуск базы данных
# в ней четыре колонки
# в каждой строке записаны
# номер записи имя пользователя,
# пароль и история его поиска
# история поиска записана
# в строку, каждое слово в
# истории поиска записано в
# паре (слово + языковая семья)

# содержит 4 колонки:
# id - порядковый номер записи
# username - имя пользователя
# password - пароль пользователя

db_session.global_init("db/users.db")

# запуск приложения flask

app = Flask(__name__)

app.secret_key = b'_6#y2L"F4Q8z\n\xec]/'

# главная страница
# на ней отоброжается
# поле для ввода
# кнопка для входа в
# акаунт, если пользователь
# уже вошёл, то отоброжается
# вся история его поиска.
#
# Поиск слов из
# истории производится
# по слову и в какой
# языковой группе
# его искали

@app.route('/', methods=['POST', 'GET'])
def main_page():
    try:

        username = session['username']
        print(2)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == session['username']).first()

        if user.words:

            history = [{'word': x.split(',')[0], 'family': x.split(',')[1]} for x in user.words.split()]

        else:

            history = []

    except Exception:
# яркий пример гениального шедеврокодинга 
        print(1)

        try:

            session.pop('username')

        except Exception:
            pass

        username = 0
        history = 0

    if request.method == 'GET' and 'word' not in session:

        return render_template('LinguaCompare_main.html', username=username, history=history)

    elif request.method == 'POST' or 'word' in session:

        # responce равен вводу пользователя
        if 'word' in session:

            responce = session.pop('word')
            family = session.pop('family')

        else:

            responce = request.form['text']
            family = request.form['family']

        lang_1 = 'en'
        original = responce

        if 'username' in session:

            username = session['username']
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.username == session['username']).first()

            if user.words:

                user.words = user.words + f' {responce},{family}'

            else:

                user.words = f'{responce},{family}'

            db_sess.commit()
            history = [{'word': x.split(',')[0], 'family': x.split(',')[1]} for x in user.words.split()]

        orig_w = f'{lang_1}: {original} [{get_transcription(original, original, lang_1, family, lang_1)}]'

        if get_translated_word(original, family, lang_1) == 'your word is not in dictionary':

            translations = get_translated_word(original, family, lang_1)

        else:

            translations = get_translated_word(original, family, lang_1)

        return render_template('LinguaCompare_main.html', defff=' '.join(get_definition(original)),
                               origgg=orig_w, trans=' '.join(translations), username=username, history=history)


# функция для
# поиска слов
# из истории
# она вызывается
# из главной страницы
# и имеет две передаваемые
# переменные
# нужные для поиска
# а именно слово и
# языковая семья в которой
# искали это слово
#
# эта функция
# передаёт значения
# в session откуда
# после
@app.route('/search/<word>/<family>')
def search(word, family):
    session['word'] = word
    session['family'] = family
    return redirect(url_for('main_page'))


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    error = None

    if request.method == 'GET':

        return render_template('sign_in.html')

    elif request.method == 'POST':

        # responce равен вводу пользователя
        password = request.form['password']
        username = request.form['username']
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter((User.username == username) & (User.password == password))

        if not users.first():

            error = u'try a different username or password'

        else:

            session['username'] = username
            session['password'] = password
            return redirect(url_for('main_page'))

    return render_template('sign_in.html', error=error)


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':

        return render_template('sign_up.html')

    elif request.method == 'POST':

        # принимает ввод
        # пользователя

        password = request.form['password']

        username = request.form['username']

        # создаёт нового
        # пользователя в таблице с
        # пустой историей
        # поиска
        # на данном этапе
        # проверяет, что
        # введённое имя не
        # занято

        new = User()
        new.username = username
        new.password = password
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.username == username)

        if users.first():

            # если это имя уже занято
            # то  выдаёт ошибку

            return render_template('sign_up.html', error="This username already exists")

        else:

            # проверив, что
            # имя не занято
            # программа
            # создаёт нового
            # пользователя с
            # пустой историей

            session['username'] = username
            session['password'] = password

            db_sess.add(new)
            db_sess.commit()

            return redirect(url_for('main_page'))

# функция для выхода
# пользователя из акаунта
# очищает session
# от параметров
# имя пользователя
# и пароль

@app.route('/log_out')
def logout():

    session.pop('username', None)
    session.pop('password', None)

    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

# if __name__ == '__main__':
# *app.run(debug=True)D:/Milena/PycharmProjects/pythonProject_LINGUA_COMPARE
