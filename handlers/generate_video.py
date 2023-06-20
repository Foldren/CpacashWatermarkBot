from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from aiogram import Router, Bot
from aiogram.filters import Text
from config import ACTIVE_USERS_STORAGE
from source.buttons import keyboard_cancel_configured, keyboard_start_configured
from source.filters import IsAdminFilter
from source.states import StepsGenerateVideo
from source.tools.create_watermark import Watermark
from source.tools.tools import Tools

rt = Router()
rt.message.filter(IsAdminFilter())


@rt.message(Text(text="🎞 Сгенерировать видео"))
async def start_generate_video(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StepsGenerateVideo.send_watermark)
    message_text = f"Отправьте фото в виде файла, либо же \n" \
                   f"напишите текст который хотите увидеть на видео ✍️\n\n" \
                   f"Пример текста:\n" \
                   f"<code>@test_watermark\ntest</code>"
    await message.answer(message_text, parse_mode="html", reply_markup=keyboard_cancel_configured)


@rt.message(Text(text="❌ Отмена"))
async def cancel_generate_video(message: Message, state: FSMContext, bot_object: Bot):
    await state.clear()

    data = await ACTIVE_USERS_STORAGE.get_data(
        bot=bot_object,
        key=StorageKey(bot_id=bot_object.id, chat_id=message.chat.id, user_id=message.from_user.id)
    )

    if 'task_obj' in data:
        print("[USER]: STOP UNIQUE")
        data['task_obj'].cancel()

    if 'ffmpeg_proccess' in data:
        print("[USER]: STOP FFMPEG")
        data['ffmpeg_proccess'].kill()

    await Tools.remove_temp_files(message.from_user.id)
    await message.answer("Процесс остановлен ❎", parse_mode="html", reply_markup=keyboard_start_configured)


@rt.message(StepsGenerateVideo.send_watermark)
async def send_watermark(message: Message, state: FSMContext, bot_object: Bot):
    await state.clear()
    await state.set_state(StepsGenerateVideo.send_video)

    if message.document:
        if message.document.mime_type[:5] == 'image':
            await Tools().download_watermark_in_user_dir(
                file_id=message.document.file_id,
                bot_object=bot_object,
                message=message
            )
        await message.answer("Теперь отправьте видео 🎞")

    elif message.text:
        href_and_name = message.text.split("\n")
        await Watermark().create(
            name=href_and_name[0],
            kas=href_and_name[1],
            message=message
        )
        await message.answer("Теперь отправьте видео 🎞")

    else:
        await message.answer('Ожидалось фото в виде файла или текст 🤷‍♂️\nПопробуйте еще раз.',
                             reply_markup=keyboard_start_configured)


@rt.message(StepsGenerateVideo.send_video)
async def end_generate_video(message: Message, state: FSMContext, bot_object: Bot):
    await state.clear()
    await state.set_state(StepsGenerateVideo.send_watermark)

    try:
        if message.video:
            await Watermark().run_get_video_with_watermark_coroutine(message.video.file_id, bot_object, message)
        elif message.document.mime_type[:5] == 'video':
            await Watermark().run_get_video_with_watermark_coroutine(message.document.file_id, bot_object, message)
        else:
            await message.answer('Ожидалось видео 🤷‍♂️\nПопробуйте еще раз.')
    except Exception as e:
        print(e)
        await message.answer("Размер видео слишком большой (>20мб). Необходимо либо урезать видео, либо сжать 👏")
