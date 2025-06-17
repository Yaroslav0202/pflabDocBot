import telebot

def main_keyboard():
    """Создает основную клавиатуру с инлайн кнопками."""
    keyboard = telebot.types.InlineKeyboardMarkup()  # Используем InlineKeyboardMarkup
    buttons = [
        telebot.types.InlineKeyboardButton("Выбор олимпиады", callback_data='olymp'),
        telebot.types.InlineKeyboardButton("Профиль", callback_data='profile'),
        telebot.types.InlineKeyboardButton("О нас", callback_data='about'),
    ]
    keyboard.add(*buttons)
    return keyboard


def back_keyboard(callback='olymp'):
    """Создает основную клавиатуру с инлайн кнопками."""
    keyboard = telebot.types.InlineKeyboardMarkup()  # Используем InlineKeyboardMarkup
    buttons = [
        telebot.types.InlineKeyboardButton("Назад", callback_data=callback),
    ]
    keyboard.add(*buttons)
    return keyboard