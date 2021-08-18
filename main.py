import telebot
import config
from text_extracting import to_text
from ner import ner_predict
import os
import model
from PIL import Image
from pipeline import parse_tif

bot = telebot.TeleBot(config.token)


def text_extraction(message):  # Функция обработки файлов 1 задания
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'C:\\Users\\Student\\PycharmProjects\\izh_it\\photos' + file_info.file_path.split('/')[1]
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Файл обрабатывается")
    answer = to_text(src)
    os.remove(src)
    bot.send_message(message.chat.id, answer)


def classifier(message):  # Функция обработки файлов 3 задания
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'C:\\Users\\\Student\PycharmProjects\\izh_it\\photos\\' + file_info.file_path.split('/')[1]
    print(src)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Файл обрабатывается")
    text = to_text(src)

    predict = model.predict(text)
    if predict[0] == 1:
        final = 'main'
    else:
        final = 'other'
    im = Image.open(src)
    (width, height) = im.size

    bot.send_message(message.chat.id, str({'source': {'width': width, 'height': height, 'type': final}}))


def data_extraction(message):  # Функция обработки файлов 4 задания
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'C:\\Users\\\Student\PycharmProjects\\izh_it\\photos\\' + file_info.file_path.split('/')[1]
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Файл обрабатывается")
    text = to_text(src)
    predict_dict = ner_predict(text)
    bot.send_message(message.chat.id, str(predict_dict))


def pipeline(message):  # Функция обработки файлов 5 задания
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    tiff = 'C:\\Users\\\Student\PycharmProjects\\izh_it\\pipeline_photos\\' + file_info.file_path.split('/')[1]
    with open(tiff, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Файл обрабатывается")
    paths = parse_tif(tiff)
    for i in paths:
        text = to_text(i)
        predict = model.predict(text)
        if predict[0] == 1:
            final = 'main'
        else:
            final = 'other'
        im = Image.open(i)
        (width, height) = im.size
        final_json = {}
        final_json['text'] = text
        final_json['source'] = {'width': width, 'height': height, 'type': final}
        final_json['facts'] = ner_predict(text)['facts']
        if len(str(final_json)) > 4096:
            for x in range(0, len(str(final_json)), 4096):
                bot.send_message(message.chat.id, str(final_json)[x:x + 4096])
        else:
            bot.send_message(message.chat.id, str(final_json))


@bot.message_handler(commands=['start'])  # Обработчик функции /start
def start_f(message):
    bot.send_message(message.chat.id, config.start_text)
    menu_func(message)


@bot.message_handler(commands=['menu'])  # Обработчик функции /menu
def menu_func(message):
    kb = telebot.types.InlineKeyboardMarkup()
    a = telebot.types.InlineKeyboardButton(text="Извлечение текстового слоя", callback_data="text_extracting")
    b = telebot.types.InlineKeyboardButton(text="Поиск объектов", callback_data="find_objects")
    c = telebot.types.InlineKeyboardButton(text="Классификация", callback_data="Classifier")
    d = telebot.types.InlineKeyboardButton(text="Извлечение значимых данных", callback_data="data_extraction")
    e = telebot.types.InlineKeyboardButton(text="Pipeline обработки документа", callback_data="pipeline")
    help_button = telebot.types.InlineKeyboardButton(text="Помощь", callback_data="help")
    creators = telebot.types.InlineKeyboardButton(text="Разработчики", callback_data="creators")
    kb.add(a, b, c, d, e, help_button, creators)
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=kb)


@bot.message_handler(commands=['help'])  # Обработчик функции /help
def help_func(message, *dop):
    if dop:
        bot.send_message(dop[0], config.help_text)
    else:
        bot.send_message(message.chat.id, config.help_text)


@bot.callback_query_handler(func=lambda call: True)  # Обработчик коллбэков от функции menu_func
def callback_func(callback):
    if callback.data == "help":
        help_func(callback.data, callback.from_user.id)
    elif callback.data == "creators":
        bot.send_message(callback.from_user.id,
                         text="Рекалов Артём - @a_rekalov \n"
                              "Караваев Антон - @lastyear1",
                         parse_mode="html")
    elif callback.data == "text_extracting":
        mes = bot.send_message(callback.from_user.id, "Отправьте файл для обработки")
        bot.register_next_step_handler(mes, text_extraction)
    elif callback.data == "find_objects":
        bot.send_message(callback.from_user.id, 'Раздел в разработке')
    elif callback.data == "Classifier":
        mes = bot.send_message(callback.from_user.id, "Отправьте файл для обработки")
        bot.register_next_step_handler(mes, classifier)
    elif callback.data == "data_extraction":
        mes = bot.send_message(callback.from_user.id, "Отправьте файл для обработки")
        bot.register_next_step_handler(mes, data_extraction)
    elif callback.data == "pipeline":
        mes = bot.send_message(callback.from_user.id, "Отправьте файл для обработки")
        bot.register_next_step_handler(mes, pipeline)


@bot.message_handler(content_types=["photo", "sticker", "document", "text"])  # Обработчик мусора
def trash_func(message):
    bot.send_message(message.chat.id, 'Неверный режим работы с ботом')


bot.polling(none_stop=True, interval=0)
