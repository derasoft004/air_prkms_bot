import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

token = '5413309092:AAHrkL7B8MB9djiYS4-C0cAGO0fxVVTgFO4'
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'], content_types=['text'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup()
    item1 = types.KeyboardButton('/faculty')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет, абитуриент! \nЧтобы увидеть список факультетов, нажми на кнопку \
"/faculty"', reply_markup=markup)


names = []
for x in range(83):
    names.append(f'https://ssau.ru/ratings/bakalavr/{x}?priority=false')
# btd _s/_n/_b - big td - список со всеми снилсами/номерами/баллами
btd_s, btd_n, btd_b = [], [], []
names_fak = faks_and_snils = []
zvlnya = []
new_s = []
count_n = []
for name_page in names:
    response = requests.get(name_page)
    soup_page = BeautifulSoup(response.text, 'html.parser')
    name_fak = soup_page.find('h5', class_='h5-text text-white')
    tbody = soup_page.find_all('tr')
    zvl = soup_page.find('div', class_='subtitle1-text text-white')
    zvlnya.append(zvl.text)
    # tr - строка принадлежащая одному абитуриенту
    p = len(btd_n)
    for tr in tbody:
        tds = []
# tds - список составляющих td: порядковый номер, снилс, сумма баллов, мат, инф/физ, рус, ид...(остальное неважно)
        for td in tr:
            tds.append(td.text)
        btd_s.append(tds[1][2:])
        btd_n.append(tds[0])
        btd_b.append(tds[2])
    if name_fak != '':
        names_fak.append(name_fak.text)
    # cn = len(btd_n)
    # count_n.append(len(btd_n) - p)
    count_n.append(len(btd_n))
    # if len(names_fak) >= 4: break
    print(len(names_fak))
print(btd_s, len(btd_s))
print(btd_n, len(btd_n))
print(zvlnya)
count_n.append(0)
print(count_n)
for j in range(len(btd_n)):
    if int(btd_n[j]) == 1 and int(btd_n[j-1]) >= 10:
        new_s.append(btd_n[j-1])
print(new_s, len(new_s))

@bot.message_handler(commands=['faculty'])
def first_message(message):
    for i in range(len(names_fak)):
        bot.send_message(message.chat.id, f'{i}.{names_fak[i]}')
    bot.send_message(message.chat.id, f'Выберите свой факультет, чтобы увидеть кол-во заявлений/мест '
                                      f'(введите только цифру от 0 до {i}) или СНИЛС (все цифры следует '
                                      'вводить через дефис: '
                                      'xxx-xxx-xxx-xx, по-другому программа Вас не поймет), '
                                      'чтобы увидеть свое место в списке'
                                      '(факультет определится сам, если Вы подали документы на одно или несколько '
                                      'направлений)')

@bot.message_handler(content_types='text')
def second_message(message):
    print(len(message.text))
    for num in range(len(names_fak)):
        if message.text == str(num):
            bot.send_message(message.chat.id, names_fak[num])
            bot.send_message(message.chat.id, f'Заявлений/мест на Ваш факультет:{zvlnya[num]} \nВведите свой СНИЛС:')
            break
    for n in range(len(btd_s)):
        if message.text == btd_s[n] and len(message.text) == 14:
            bot.send_message(message.chat.id, f'Ваш снилс:{btd_s[n]}; Ваше место в списке: {btd_n[n]}; Ваши баллы ЕГЭ: \
{btd_b[n]} \n')
            for j in range(len(count_n)):
                if count_n[j] >= n >= count_n[j - 1]: bot.send_message(message.chat.id, f'{names_fak[count_n.index(count_n[j])]}')
            if message.text != btd_s[n]: break


# url = 'https://ssau.ru/ratings/bakalavr/15?priority=false'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
# name_str = soup.find('h5', class_='h5-text text-white')
# print('Наименование Вашего направления -', name_str.text, sep='')
#
#
# # for i in range(len(btd_n)):
# #     print(btd_n[i], btd_s[i], btd_b[i])
#
# print('Для того, чтобы получить результат, пожалуйста, введите свой СНИЛС:')
# snils = str(input())
# for i in range(len(btd_s)):
#     if snils == btd_s[i]:
#         print(f'Ваш СНИЛС:{btd_s[i]}, Ваш порядковый номер: {btd_n[i]}; Ваша итоговая сумма баллов ЕГЭ: {btd_b[i]}')
#     else:
#         pass


bot.polling(none_stop=True)