import datetime
from pathlib import Path

import telebot
from telebot import types

bot = telebot.TeleBot("1671490286:AAEM2tPzf4WvH_k0HN04LxzD2rooWHVnbcc")
data_ = {
    '9009': {
        1: {'text': "1 неделя", 'callback_data': "pod is1"},
        2: {'text': "2 неделя", 'callback_data': "pod is2"},
        3: {'text': "3 неделя", 'callback_data': "pod is3"},
        4: {'text': "4 неделя", 'callback_data': "pod is4"},
    },
    '2112': {
        1: {'text': "Получить расписание недели 1", 'callback_data': "sama1"},
        2: {'text': "Получить расписание недели 2", 'callback_data': "sama2"},
        3: {'text': "Получить расписание недели 3", 'callback_data': "sama3"},
        4: {'text': "Получить расписание недели 4", 'callback_data': "sama4"},
    },
    'menu': [
        {'text': "Меню на 1 500 ккал.", 'callback_data': "m1500"},
        {'text': "Меню на 1 600 ккал.", 'callback_data': "m1600"},
        {'text': "Меню на 1 600п ккал.", 'callback_data': "m1600p"},
        {'text': "Меню на 1 600п ккал.", 'callback_data': "m1700"},
        {'text': "Меню на 1 800 ккал.", 'callback_data': "m1800"},
        {'text': "Меню на 1 800п ккал.", 'callback_data': "m1800p"},
        {'text': "Меню на 1 900 ккал.", 'callback_data': "m1900"},
        {'text': "Меню на 1 900п ккал.", 'callback_data': "m1900p"},
        {'text': "Меню на 2 200 ккал..", 'callback_data': "m2200"}]
}

call_dict = {
    'pod is1': "https://www.notion.so/d133ca7d63e24222ba0d50f48e364f30",
    "pod is2": "https://www.notion.so/f06d594d039f456a9b0809327c3772aa",
    "pod is3": "https://www.notion.so/9fd254d86f1d46d3bc6753215910c5c8",
    "pod is4": "https://www.notion.so/ca3dd85702434c6f851586b4e80d26b4",
    "sama1": "https://www.notion.so/00faffe6aa4b47d49061012b2f381f16",
    "sama2": "https://www.notion.so/3b5d73a0d1d94b6f8fda17db13bc35e2",
    "sama3": "https://www.notion.so/1c5a4801d619486ca1104ba39af32b17",
    "sama4": "https://www.notion.so/b94c438532124d96a00adaa9942f21c0",
    "m1500": "https://drive.google.com/drive/folders/13a8li1ogJcUUcvVLzjY0KPbSVeSbHyr3",
    "m1600": "https://drive.google.com/drive/folders/1aEhGO2NcmUb_15jgRXE_eroK3-OgBeuD",
    "m1600p": "https://drive.google.com/drive/folders/1pxctHoFHWfBL3bH5HeJ3lURO0iO-zqLY",
    "m1700": "https://drive.google.com/drive/folders/1U2UsDKpVI_36Qj5pAx6LsH3FBIir50cG",
    "m1800": "https://drive.google.com/drive/folders/18Mg-uaUu-JpX70n5Jomowst3mbO4oLek",
    "m1800p": "https://drive.google.com/drive/folders/1Z3onRF-lT1KwsDAPVX5Gp75RLHIZKim0",
    "m1900": "https://drive.google.com/drive/folders/1ZpkXvME2f6b7WRP153CEatKgUEO2wICs",
    "m1900p": "https://drive.google.com/drive/folders/16Z_5nzC9xsgQYSHaLn8lJhqdlgZAl3Lt",
    "m2200": "https://drive.google.com/drive/folders/1NDPgIUmcAWG7Xr6DdIiYAxWkXcut1aDP"
}
date_start = datetime.datetime.now().date()


def set_date_start():
    file = Path('data_start.txt')
    file.touch()
    file.write_text(datetime.date.today().strftime('%Y.%m.%d'))


def get_date_start():
    return Path.read_text(Path('data_start.txt'))


def get_week_number():
    year, mouth, day = get_date_start().split('.')
    data_start = datetime.date(int(year), int(mouth), int(day))
    today = datetime.date.today()
    week_number = ((today - data_start).days // 7) + 1
    return week_number if week_number in range(1, 5) else 4


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, пришли код")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    keyboard = types.InlineKeyboardMarkup()
    if message.text in data_ and message.text != 'menu':
        keyboard.add(types.InlineKeyboardButton(text=data_.get(message.text).get(get_week_number()).get('text'),
                                                callback_data=data_.get(message.text).get(get_week_number()).get(
                                                    'callback_data')))
    if message.text.lower() == "menu":
        for i in data_.get('menu'):
            keyboard.add(types.InlineKeyboardButton(text=i.get('text'),
                                                    callback_data=i.get('callback_data')))

    if message.text.lower() == 'старт марафон':
        set_date_start()
        bot.send_message(message.from_user.id, text="Марафон стартовал сегодня, ура!!!")

    if message.text.lower() == 'дата начала':
        bot.send_message(message.from_user.id, text=f"Марафон стартовал {get_date_start()}")

    if message.text.lower() == 'help':
        bot.send_message(message.from_user.id, text='команды:\ncтарт марафон,\nдата начала')

    bot.send_message(message.from_user.id, text="Нажмите на кнопку", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data in call_dict:
        bot.send_message(call.message.chat.id, call_dict.get(call.data))


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
