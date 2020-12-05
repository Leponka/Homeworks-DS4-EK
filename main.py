import wiki
import config
from config import token

print(token)
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import telebot
from random import randint
import dbworker
import numpy as np
from tabulate import tabulate
# print(config.states.S_START)
bot = telebot.TeleBot(config.token)

pict = (
    'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/World_Population.svg/400px-World_Population.svg.png',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/World_Population.svg/800px-World_Population.svg.png',
    'https://media.professionali.ru/processor/topics/original/2020/10/27/11.jpg',
    'http://www.fresher.ru/manager_content/images2/zhizn-v-peru/big/1.jpg',
    'https://avatars.mds.yandex.net/get-zen_doc/3731867/pub_5f2340f56a489e1550b01c5c_5f2341e26dfa086d51538531/scale_1200',
    'https://expert.ru/data/public/507016/507025/05.jpg',
    'https://fb.ru/media/i/3/0/4/6/5/4/i/304654.jpg',
    'https://www.culture.ru/storage/images/4068b5d838e24b7938eb2626bcdeabbc/237e8918266613eec363d4e142224804.jpeg'
)


@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(message.chat.id,
                     message.from_user.first_name + ', привет! Очень рад, что вы со мной решили пообщаться =) '
                                                    'Предлагаю такую последовать: сначала наберите команду /about, почитайте, что я могу; '
                                                    'потом посмотрите /help, '
                                                    'и уже потом попробуйте /map или /table')
    bot.send_photo(message.chat.id, pict[randint(2, 8)])
    dbworker.set_state(message.chat.id, config.states.S_START.value)


@bot.message_handler(commands=['about'])
def send_welcome(message):
    bot.reply_to(message, "Я сделан для того, чтобы показать вам информацию о численности населения земли. "
                          "Могу вывести список самых малочисленных стран, или, наоборот, самых больших по численности"
                          " (вы можете выбрать количество стран в таком списке). "
                          "Могу, конечно, вывести в чат численность по конкретной стране. "
                          "Я даже даю вам ссылку на статью Wikipedia про страну\ страны. "
                          "А еще я могу показать карту мира )). Напишите /help, чтобы посмотреть команды и начать работу ")
    bot.send_photo(message.chat.id, pict[randint(2, 8)])


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "/start - поздороваться \n"
                          "/about - информация обо мне \n"
                          "/help - посмотреть команды, которые можно выбрать \n"
                          "/map - показать карту численности \n"
                          "/table - показать информацию из таблицы численности \n"
                          "/reset - вернуться к началу \n"
                          "/finish - попрощаться"
                          "")


@bot.message_handler(commands=["finish"])
def hello(message):
    bot.send_message(message.chat.id, message.from_user.first_name + ', всего самого хорошего! До встречи! ')
    bot.send_photo(message.chat.id, pict[randint(2, 8)])
    dbworker.set_state(message.chat.id, config.states.S_START.value)


@bot.message_handler(commands=['map'])
def send_welcome(message):
    bot.send_photo(message.chat.id, pict[1])
 #   bot.send_message(message.chat.id, dbworker.get_current_state(message))


#  bot.send_message(message.chat.id, config.states.S_START.value)
# state = dbworker.get_current_state(message)
#  print(state)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Вернемся к началу.\n"
                                      "Хотите посмотреть карту численности населения /map или информацию по странам /table? \n"
                                      "Или выбирайте /about или  /help , чтобы посмотреть информацию обо мне." )
    bot.send_photo(message.chat.id, pict[randint(2, 8)])
    dbworker.set_state(message.chat.id, config.states.S_START.value)

@bot.message_handler(commands=['table'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Хотите посмотреть численность одной конкретной страны? Тогда выбирайте: /country \n"
                                      "Или показать список стран? Тогда выбирайте: \n"
                                      "/list_tail  список самых малочисленных стран  или \n"
                                      "/list_head с самой большой численностью населения")
    dbworker.set_state(message.chat.id, config.states.S_LIST_OR_COUNTRY.value)

@bot.message_handler(func=lambda message: message.text.lower()  not in ('/start' , '/help', '/map', '/table', '/finish', '/about', '/reset')
                     and dbworker.get_current_state(message.chat.id) == config.states.S_LIST_OR_COUNTRY.value)
def get_detail(message):
   # dbworker.del_state(str(message.chat.id) + 'detail')
    if message.text.lower().strip() == '/list_tail':
        bot.send_message(message.chat.id, "Список из какого числа стран вам показать? Напишите любое число от 1 до "
                         + str(wiki.count_of_country))
        dbworker.set_state(str(message.chat.id) + 'detail', 'list_tail')
        dbworker.set_state(message.chat.id, config.states.S_TAIL_LIST.value)
    elif message.text.lower().strip() == '/list_head':
        bot.send_message(message.chat.id, "Список из которого числа стран вам показать? Напишите любое число от 0 до "
                         + str(wiki.count_of_country))
        dbworker.set_state(str(message.chat.id) + 'detail', 'list_head')
        dbworker.set_state(message.chat.id, config.states.S_HEAD_LIST.value)
    elif message.text.lower().strip() == '/country':
        bot.send_message(message.chat.id, "Напишите название страны (или 3 первые буквы)")
        dbworker.set_state(str(message.chat.id) + 'detail', 'country')
        dbworker.set_state(message.chat.id, config.states.S_COUNTRY.value)
    else:
        bot.send_message(message.chat.id, "\n"
                                          "Я не понял, что вы написали.\n"
                                          "Хотите посмотреть численность одной конкретной страны? Тогда выбирайте: /country \n"
                                          "Или показать список стран? Тогда выбирайте: \n"
                                          "/list_tail  список самых малочисленных стран  или \n"
                                          "/list_head с самой большой численностью населения \n"
                                          "Чтобы посмотреть другие доступные команды, наберите  /help.\n"
                                          "Выбирайте /reset, чтобы начать сначала.")


@bot.message_handler(func=lambda message: message.text.lower() not in ('/start' , '/help', '/map', '/table', '/finish', '/about', '/reset')
                     and dbworker.get_current_state(message.chat.id) == config.states.S_TAIL_LIST.value)
def tail_list(message):
    if message.text.lower().strip().isdigit() and int(message.text.lower().strip()) <= wiki.count_of_country and int(message.text.lower().strip()) >= 1:
        x = wiki.country_pop_info.country
        bot.send_message(message.chat.id,'\n '.join(i for i in list(x[wiki.count_of_country-int(message.text.lower()):]) if i != '')
                         + '\n' + '\n' + "Теперь можете перейти в /table /reset /help  или ввести число еще раз")
    elif message.text.lower().strip() == "/list_tail":
        bot.send_message(message.chat.id, "Список из которого числа стран вам показать? Напишите любое число от 1 до "
                         + str(wiki.count_of_country))
    elif message.text.lower().strip() in ( "/list_head", "/country"):
        bot.send_message(message.chat.id, "Прежде, чем воспользоваться этой командой, перейдите в /table,  \n"
                                          "или введите все-таки любое число от 1 до " + str(wiki.count_of_country) + " ,\n"
                                          "и я покажу вам список самых малочисленных стран")
    else:
        bot.send_message(message.chat.id, "Что-то не то (( Напишите любое число от 1 до " + str(wiki.count_of_country) + "\n"
                                            "Или воспользуйтесь командами /table /reset /help")



@bot.message_handler(func=lambda message: message.text.lower() not in ('/start' , '/help', '/map', '/table', '/finish', '/about', '/reset')
                     and dbworker.get_current_state(message.chat.id) == config.states.S_HEAD_LIST.value)
def tail_list(message):
    if message.text.lower().strip().isdigit() and int(message.text.lower().strip()) <= wiki.count_of_country and int(message.text.lower().strip()) >= 1:
        x = wiki.country_pop_info.country
        bot.send_message(message.chat.id,', '.join(i for i in list(x[:int(message.text.lower())]) if i != '')
                         + '\n' + '\n' + "Теперь можете перейти в /table /reset /help или ввести число еще раз")
    elif message.text.lower().strip() == "/list_head":
        bot.send_message(message.chat.id, "Список из которого числа стран вам показать? Напишите любое число от 1 до "
                         + str(wiki.count_of_country))
    elif message.text.lower().strip() in ( "/list_tail", "/country"):
        bot.send_message(message.chat.id, "Прежде, чем воспользоваться этой командой, перейдите в /table,  \n"
                                          "или введите все-таки любое число от 1 до " + str(wiki.count_of_country) + " ,\n"
                                          "и я покажу вам список стран с самой большой численностью населения")
    else:
        bot.send_message(message.chat.id, "Что-то не то (( Напишите любое число от 1 до " + str(wiki.count_of_country) + "\n"
                                            "Или воспользуйтесь командами /table /reset /help")

@bot.message_handler(func=lambda message: message.text.lower() not in ('/start' , '/help', '/map', '/table', '/finish', '/about', '/reset')
                     and dbworker.get_current_state(message.chat.id) == config.states.S_COUNTRY.value)
def tail_list(message):
    df = wiki.country_pop_info.loc[:, 'position':'link']
    leng = len(message.text.capitalize().strip())
    if leng>=3 and len(df[df['country'].str.contains(message.text.capitalize().strip())]) >=1:
        x = df[df['country'].str.contains(message.text.capitalize().strip())]#.style.hide_index()
        bot.send_message(message.chat.id, tabulate(x, headers=["Позиция","Страна", "Численность","Ссылка на статью о стране"],showindex=False) #, tablefmt="grid")
                         + '\n' + '\n' + "Теперь можете перейти в /table /reset /help или ввести число еще раз")
    elif message.text.lower().strip() == "/country":
        bot.send_message(message.chat.id, "Напишите как минимум 3 первые буквы в названии страны:")
    elif message.text.lower().strip() in ( "/list_tail", "/list_head"):
        bot.send_message(message.chat.id, "Прежде, чем воспользоваться этой командой, перейдите в /table,  \n"
                                          "или напишите как минимум 3 первые буквы в названии страны, " 
                                          "и я покажу вам информацию о её численности")
    else:
        bot.send_message(message.chat.id, "Что-то не то (( Напишите название страны или хотя бы первые 3 буквы названия. Кириллицей. \n"
                                            "Или воспользуйтесь командами /table /reset /help")


@bot.message_handler(func=lambda message: message.text.lower()  not in ('/start' , '/help', '/map', '/table', '/finish', '/about', '/reset')
                    and dbworker.get_current_state(message.chat.id) in (config.states.S_TAIL_LIST.value,
                                                                            config.states.S_LIST_OR_COUNTRY.value,
                                                                            config.states.S_HEAD_LIST.value,
                                                                            config.states.S_COUNTRY.value))
def echo(message):
    bot.send_message(message.chat.id, 'Я не понимаю, что такое "' + message.text + '", может вы хотите получить информацию о численности? '
                                                                                   'Тогда выбирайте: /map или /table \n'
                     "Также можете воспользоваться командами /help, /about, /reset, /finish ")

if __name__ == '__main__':
    bot.infinity_polling()
