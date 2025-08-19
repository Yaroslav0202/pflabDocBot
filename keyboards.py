from telebot import types

def get_main_keyboard():
    """Основная клавиатура (старт/помощь)."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("Создать PDF с подписями"),
        types.KeyboardButton("Помощь")
    ]
    markup.add(*buttons)
    return markup

# def get_cancel_keyboard():
#     """Клавиатура с кнопкой 'Отмена'."""
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     markup.add(types.KeyboardButton("Отмена"))
#     return markup