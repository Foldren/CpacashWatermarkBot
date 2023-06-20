from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Клавиатуры
keyboard_start = [[KeyboardButton(text="🎞 Сгенерировать видео"), KeyboardButton(text="💦 Создать вотерку")]]
keyboard_cancel = [[KeyboardButton(text="❌ Отмена")]]


# Конфигурации
keyboard_start_configured = ReplyKeyboardMarkup(
    keyboard=keyboard_start,
    resize_keyboard=True,  # меняем размер клавиатуры
)

keyboard_cancel_configured = ReplyKeyboardMarkup(
    keyboard=keyboard_cancel,
    resize_keyboard=True,
)
