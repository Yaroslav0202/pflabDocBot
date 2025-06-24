from telebot import types

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Создать PDF с подписями")
    btn2 = types.KeyboardButton("Помощь")
    markup.add(btn1, btn2)
    return markup

def get_cancel_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Отмена")
    markup.add(btn)
    return markup
