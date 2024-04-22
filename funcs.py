import requests
# from pprint import pprint


ya_apikey = 'dict.1.1.20240109T131316Z.71e2c62d901c4efe.0fccfa5c1185841d0dbd117d64db1692293ba6c6'
mw_apikey = 'e4a1c6a2-09e6-4f31-9192-716b98c020b4'


# print('enter original language:')

lang_1 = 'en'
print('enter translation family:')
family = input()
print('enter your word:')
original = input()


def get_definition():
    url_mw = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{original}?key={mw_apikey}"
    response_mw = requests.get(url_mw)
    shortdef = response_mw.json()[0]['shortdef']
    return f'definition:', '; '.join(shortdef)
    # pprint(response.json())

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


# urlxx = f'https://dictionary.yandex.net/api/v1/dicservice.json/getLangs?key={apikey}'
# print(urlxx)


def get_translated_word(original):
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


def get_transcription(word, lang_tr):

    if word == get_translated_word(original):
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


print(*get_definition(), sep='\n')
print(f'{lang_1}: {original} [{get_transcription(original, lang_1)}]')
if get_translated_word(original) == 'your word is not in dictionary':
    print(get_translated_word(original))
else:
    print(*get_translated_word(original), sep='\n')
