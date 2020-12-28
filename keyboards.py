from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# InlineMarkup
payment = InlineKeyboardMarkup()
inline_button_1 = InlineKeyboardButton("Проблемы с оплатой.", callback_data='button_1')
inline_button_2 = InlineKeyboardButton("Как использовать пресет?", callback_data='button_2')
inline_button_3 = InlineKeyboardButton("Как оформить заказ пресета?", callback_data='button_3')
inline_button_4 = InlineKeyboardButton("Как получить бесплатный пресет?", callback_data='button_4')
inline_button_5 = InlineKeyboardButton("Сотрудничество.", callback_data='button_5')
payment.add(inline_button_1).add(inline_button_2).add(inline_button_3).add(inline_button_4).add(inline_button_5)


inline_kb2 = InlineKeyboardMarkup()
inline_button_UA = InlineKeyboardButton("Цитата...", callback_data='quote')
inline_kb2.add(inline_button_UA)
