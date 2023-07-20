import sqlite3
import telebot
from telebot import types
bot = telebot.TeleBot('5913582630:AAH-1PK3PJ3NqB1kPsPHfWiJQDxfu0WTLRE')


@bot.message_handler(commands = ['start'])
def start(message):
    cnnct = sqlite3.connect('test_database.sql')
    crsr = cnnct.cursor()
    crsr.execute('CREATE TABLE IF NOT EXISTS users (id integer primary key, name varchar(50), email varchar(100))')
    cnnct.commit()
    crsr.close()
    cnnct.close()
    bot.send_message(message.from_user.id, "Здравствуйте!\nВас приветствует бот журнала «Упаковка. Исследование и Развитие»! Меня зовут Пак-э-Джин.\nКак я могу обращаться к Вам?")
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    userid = message.from_user.id
    name = message.text.strip()
    cnnct = sqlite3.connect('test_database.sql')
    crsr = cnnct.cursor()
    crsr.execute("SELECT id FROM users WHERE id = ?", (userid, ))
    data = crsr.fetchone()
    print(data)
    if not data:
        crsr.execute("INSERT INTO users (id, name) VALUES(?, ?)", (userid, name))
        bot.send_message(message.chat.id, "Рад знакомству, " + str(name) + "!")
    else:
        bot.send_message(message.chat.id, "Рад Вас видеть снова, " + str(name) + "!")
    cnnct.commit()
    crsr.close()
    cnnct.close()
    main_message(message)


def main_message(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Подписаться на журнал", callback_data = 'subscribe'))
    button1 = types.InlineKeyboardButton("Реклама в журнале", url = 'https://packagingrd.ru/prd/category/advertising/advert_magazine/')
    button2 = types.InlineKeyboardButton("Реклама на сайте", url = 'https://packagingrd.ru/prd/category/advertising/advert_site/')
    markup.row(button1, button2)
    markup.add(types.InlineKeyboardButton("Услуги", callback_data = 'services'))
    markup.add(types.InlineKeyboardButton("Пообщаться с представителем журнала", url = 'https://packagingrd.ru/feedback.html'))
    bot.send_message(message.chat.id, "Какой у Вас вопрос?", reply_markup = markup)


def get_email(message):
    userid = message.from_user.id
    email = message.text.strip()
    cnnct = sqlite3.connect('test_database.sql')
    crsr = cnnct.cursor()
    crsr.execute("UPDATE users SET email = ? WHERE id = ?", (email, userid))
    cnnct.commit()
    crsr.close()
    cnnct.close()
    bot.send_message(message.chat.id, "Спасибо за подписку!")
    main_message(message)


@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == 'subscribe':
        bot.send_message(callback.message.chat.id, "Пожалуйста, введите Ваш адрес электронной почты.")
        bot.register_next_step_handler(callback.message, get_email)
    elif callback.data == 'services':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Верстка", callback_data = 'craft'))
        markup.add(types.InlineKeyboardButton("Дизайн", callback_data = 'design'))
        markup.add(types.InlineKeyboardButton("Видео- и фотосъемка", callback_data = 'video_and_photo'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data = 'back_to_main'))
        bot.send_message(callback.message.chat.id, "Выберите интересующую Вас услугу.", reply_markup = markup)
    elif callback.data == 'craft':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Верстка журналов", url = 'https://packagingrd.ru/prd/services/service_layout/verstka-zhurnalov.html'))
        markup.add(types.InlineKeyboardButton("Верстка книг", url = 'https://packagingrd.ru/prd/category/services/service_layout/layout_books/'))
        markup.add(types.InlineKeyboardButton("Верстка малых форм", url = 'https://packagingrd.ru/prd/category/services/service_layout/layout_littleforms/'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data = 'services'))
        bot.send_message(callback.message.chat.id, "Возможны следующие варианты:", reply_markup = markup)
    elif callback.data == 'design':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Брендинг", url = 'https://packagingrd.ru/prd/category/services/services_design/design_branding/'))
        markup.add(types.InlineKeyboardButton("Упаковка", url = 'https://packagingrd.ru/prd/category/services/services_design/design_packaging/'))
        markup.add(types.InlineKeyboardButton("Полиграфия", url = 'https://packagingrd.ru/prd/category/services/services_design/design_polygraphy/'))
        markup.add(types.InlineKeyboardButton("Наружная реклама", url = 'https://packagingrd.ru/prd/category/services/services_design/design_outside/'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data = 'services'))
        bot.send_message(callback.message.chat.id, "Возможны следующие варианты:", reply_markup = markup)
    elif callback.data == 'video_and_photo':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Предметная съемка", url = 'https://packagingrd.ru/prd/category/services/services_photovideo/photovideo_subjects/'))
        markup.add(types.InlineKeyboardButton("Мероприятия", url = 'https://packagingrd.ru/prd/category/services/services_photovideo/photovideo_events/'))
        markup.add(types.InlineKeyboardButton("Промышленная съемка", url = 'https://packagingrd.ru/prd/category/services/services_photovideo/photovideo_industry/'))
        markup.add(types.InlineKeyboardButton("Съемка с квадрокоптера", url = 'https://packagingrd.ru/prd/category/services/services_photovideo/photovideo_flying/'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data = 'services'))
        bot.send_message(callback.message.chat.id, "Возможны следующие варианты:", reply_markup = markup)
    elif callback.data == 'back_to_main':
        main_message(callback.message)


bot.polling(none_stop = True)
