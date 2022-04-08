import telebot
from telebot import types
import config
import time
import datetime
import os
import mySQLer

bot = telebot.TeleBot(config.token)


def salesFunnel(period):
    dt = dateStart = dateEnd = datetime.datetime.now()

    if period == 'day':
        dateStart = datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0)
        dateEnd = datetime.datetime(dt.year, dt.month, dt.day, 23, 59, 59, 342380)
    elif period == 'week':
        monday = dt - datetime.timedelta(days=dt.weekday())
        Sunday = monday + datetime.timedelta(days=6)
        dateStart = datetime.datetime(monday.year, monday.month, monday.day, 0, 0, 0)
        dateEnd = datetime.datetime(Sunday.year, Sunday.month, Sunday.day, 23, 59, 59, 342380)
    elif period == 'month':
        dateStart = datetime.datetime(dt.year, dt.month, 1, 0, 0, 0)
        dateEnd = datetime.datetime(dt.year, dt.month + 1, 1, 23, 59, 59, 342380) - datetime.timedelta(days=1)

    tDataStart = dateStart.strftime('%Y.%m.%d')
    tDataEnd = dateEnd.strftime('%Y.%m.%d')
    textMessage = f'Данные за период \n c {tDataStart} по {tDataEnd}'

    # Запрос всех строк за период
    answ = mySQLer.selectBdPeriod(dateStart, dateEnd)
    answRevers = [0] * 7
    for i in range(len(answ)):
        for j in range(7):
            if not answ[i][j]:
                continue
            answRevers[j] += 1
    step = 1
    for s in answRevers:
        textMessage += f'\n шаг {step} - {str(s)}'
        step += 1
    return textMessage


def selectDataByUser(quantity):
    count = 0
    if quantity == 'last':
        count = 1
    elif quantity == 'several':
        count = 10
    listUser = mySQLer.selectBdLast(count)
    return listUser


def sendVideo(call, text, callbackData):
    bot.send_message(call.message.chat.id, text)

    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Смотреть дальше", callback_data=callbackData)
    keyboard.add(button1)

    f = open(f'video/video{call.data}.mp4', 'rb')
    bot.send_video(call.message.chat.id, f, None, reply_markup=keyboard)


def questionStart(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Продюсер", callback_data="Продюсер")
    button2 = types.InlineKeyboardButton("Эксперт", callback_data="Эксперт")
    button3 = types.InlineKeyboardButton("Другое", callback_data="Другое")
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)

    text = 'Здраствуйте, {0.first_name}!'.format(message.from_user)
    bot.send_message(message.chat.id, text)
    text = 'Скажите, какая Ваша роль в онлайн-школе?'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def question2(call):
    text = 'Опишите примерную модель своей онлайн-школы:'
    text += '\n' + '1 - Я эксперт и продюсер в одном лице'
    text += '\n' + '2 - Есть продюсер и несколько наемных работников'
    text += '\n' + '3 - Действующая онлайн-школа с отделами по направлениям'
    text += '\n' + '4 - Большой продюсерский центр'

    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("1", callback_data="1")
    button2 = types.InlineKeyboardButton("2", callback_data="2")
    button3 = types.InlineKeyboardButton("3", callback_data="3")
    button4 = types.InlineKeyboardButton("4", callback_data="4")
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)
    bot.send_message(call.message.chat.id, text, reply_markup=keyboard)


def question3(call):
    if call.data == '1':
        text = 'Отлично, {0.first_name}! ' \
               'Посмотри, какие основные риски существуют ' \
               'у эксерта при открытии онлайн-школы'.format(call.from_user)
        sendVideo(call, text, '5')
    elif call.data == '2':
        text = 'Отлично, {0.first_name}! ' \
               'Посмотри, какие основные риски существуют в онлайн-школе'.format(call.from_user)
        sendVideo(call, text, '6')
    elif call.data == '3':
        text = 'Отлично, {0.first_name}! ' \
               'Посмотри, какие основные риски существуют в онлайн-школе'.format(call.from_user)
        sendVideo(call, text, '7')
    elif call.data == '4':
        text = 'Отлично, {0.first_name}! ' \
               'Посмотри, какие основные риски существуют в онлайн-школе'.format(call.from_user)
        sendVideo(call, text, '8')


def question4(call):
    if call.data == '5':
        text = 'Что нужно делать, чтобы избежать проблем в видео ниже'
        sendVideo(call, text, '9')
    elif call.data == '6':
        text = 'Что нужно делать, чтобы избежать проблем в видео ниже'
        sendVideo(call, text, '9')
    elif call.data == '7':
        text = 'Что нужно делать, чтобы избежать проблем в видео ниже'
        sendVideo(call, text, '9')
    elif call.data == '8':
        text = 'Что нужно делать, чтобы избежать проблем в видео ниже'
        sendVideo(call, text, '9')


def question5(call):
    text = 'Как прямо сейчас получить бесплатный анализ Вашей онлайн-школы и получить рекомендации. Смотрите видео'
    bot.send_message(call.message.chat.id, text)

    text = 'Нажмите Пройти тестирование, для получения рекомендаций'
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Пройти тестирование", callback_data='playTest')
    keyboard.add(button1)

    f = open(f'video/video{call.data}.mp4', 'rb')
    bot.send_video(call.message.chat.id, f, text, None, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    if call.data == 'Продюсер' or call.data == 'Эксперт' or call.data == 'Другое':
        question2(call)
        keyAnsw = 'step1'
    elif call.data == '1' or call.data == '2' or call.data == '3' or call.data == '4':
        question3(call)
        keyAnsw = 'step2'
    elif call.data == '5' or call.data == '6' or call.data == '7' or call.data == '8':
        question4(call)
        keyAnsw = 'step3'
    elif call.data == '9':
        question5(call)
        keyAnsw = 'step4'
    elif call.data == 'playTest':
        bot.send_message(call.message.chat.id, 'Тест аналогично онлайн-формам с формированием отчета в PDF')
        keyAnsw = 'step5'

    if call.from_user.id in config.botIdAdmin:
        if call.data == 'day' or call.data == 'week' or call.data == 'month':
            textSalesFunnel = salesFunnel(call.data)
            bot.send_message(call.message.chat.id, textSalesFunnel)
        elif call.data == 'last' or call.data == 'several':
            listUser = selectDataByUser(call.data)
            for us in listUser:
                text2 = text3 = text4 = text5 = ''
                if us[8] == '1':
                    text2 = 'Эксперт и продюсер в одном лице'
                elif us[8] == '2':
                    text2 = 'Есть продюсер и несколько наемных работников'
                elif us[8] == '3':
                    text2 = 'Действующая онлайн-школа с отделами по направлениям'
                elif us[8] == '4':
                    text2 = 'Большой продюсерский центр'

                if us[9] != '':
                    text3 = 'Посмотрел видео'
                if us[10] != '':
                    text4 = 'Посмотрел видео'
                if us[11] != '':
                    text5 = 'Перешёл на заполнение анкеты'

                text = f'Пользователь {us[3]} {us[2]}, \n' \
                       f'{us[4]} \n' \
                       f'Роль - {us[7]} \n' \
                       f'Модель школы - {text2} \n' \
                       f'Шаг 3 - {text3} \n' \
                       f'Шаг 4 - {text4} \n' \
                       f'Шаг 5 - {text5}'

                bot.send_message(call.message.chat.id, text)
        else:
            # Запишем в БД данные о том, что пользователь ответил на вопрос.
            valuesAnsw = dict(userId=call.from_user.id,
                              dataLast=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            valuesAnsw[keyAnsw] = call.data
            mySQLer.updateBdAction(valuesAnsw)


@bot.message_handler(commands=['start'])
def messagesStart(message):
    user = message.from_user
    if user.id in config.botIdAdmin:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton('Воронка продаж')
        button2 = telebot.types.KeyboardButton('Данные о заполняющем')
        button3 = telebot.types.KeyboardButton('Старт бота')
        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        bot.send_message(message.chat.id, 'Вся информация о работе бота доступна по кнопке внизу экрана',
                         reply_markup=keyboard)
    else:
        questionStart(message)
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        mySQLer.insertBdActionNew(dict(userId=user.id,
                                       userName=user.username,
                                       firstName=user.first_name,
                                       lastName=user.last_name,
                                       dataStart=timestamp,
                                       dataLast=timestamp,
                                       start=1,
                                       step1='',
                                       step2='',
                                       step3='',
                                       step4='',
                                       step5='',
                                       step6='',
                                       ))


@bot.message_handler(commands=['info'])
def printInfo(message):
    print(message)
    bot.send_message(message.chat.id, message)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == 'Воронка продаж':
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton("Данные за день", callback_data="day")
        button2 = telebot.types.InlineKeyboardButton("Данные за неделю", callback_data="week")
        button3 = telebot.types.InlineKeyboardButton("Данные за месяц", callback_data="month")
        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        text = 'Укажите период отчета'
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif message.text == 'Данные о заполняющем':
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton("Последний", callback_data="last")
        button2 = telebot.types.InlineKeyboardButton("10 последних", callback_data="several")
        keyboard.add(button1)
        keyboard.add(button2)
        text = 'Сколько пользователей выводить'
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    if message.text == 'Старт бота':
        questionStart(message)
        user = message.from_user
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        mySQLer.insertBdActionNew(dict(userId=user.id,
                                       userName=user.username,
                                       firstName=user.first_name,
                                       lastName=user.last_name,
                                       dataStart=timestamp,
                                       dataLast=timestamp,
                                       start=1,
                                       step1='',
                                       step2='',
                                       step3='',
                                       step4='',
                                       step5='',
                                       step6='',
                                       ))


if __name__ == '__main__':
    bot.polling(none_stop=True)
