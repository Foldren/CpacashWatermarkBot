from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from source.buttons import keyboard_start_configured
from source.filters import IsAdminFilter

rt = Router()


# Хэндлер на команду /start
@rt.message(Command(commands=["start"]), IsAdminFilter())
async def start_admin(message: Message, state: FSMContext):
    await state.clear()
    message_text = f"Добрый день {message.from_user.full_name}!👋\n" \
                   f"Я бот добавляющий вотермарки в видео🎞💦\n\n" \
                   f"Рабочие кнопки бота:\n\n" \
                   f"1️⃣ 🎞 Сгенерировать видео - отправьте png файл и видео после чего я прикреплю вотермарк к видео," \
                   f" вместо картинки можете также просто написать любой текст, я создам из него вотерку и добавлю к видео\n" \
                   f"2️⃣ 💦 Создать вотерку - напишите нужный текст, из него я создам вотермарк картинку\n"
    await message.answer(message_text, reply_markup=keyboard_start_configured)
