from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram import Router
from aiogram.filters import Text
from source.buttons import keyboard_cancel_configured, keyboard_start_configured
from source.filters import IsAdminFilter
from source.states import StepsCreateWatermark
from source.tools.create_watermark import Watermark

rt = Router()
rt.message.filter(IsAdminFilter())


@rt.message(Text(text="💦 Создать вотерку"))
async def start_generate_video(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StepsCreateWatermark.send_text)
    message_text = f"Напишите текст который хотите увидеть на вотермарке ✍️\n\n" \
                   f"Пример текста:\n" \
                   f"<code>@test_watermark\ntest</code>"
    await message.answer(message_text, parse_mode="html", reply_markup=keyboard_cancel_configured)


@rt.message(StepsCreateWatermark.send_text)
async def send_watermark(message: Message, state: FSMContext):
    await state.clear()

    if message.text:
        href_name = message.text.split("\n")
        image_path = await Watermark().create(href_name[0], href_name[1], message)

        await message.answer("Вотермарк готов! ✅")
        await message.answer_document(
            document=FSInputFile(image_path),
            reply_markup=keyboard_start_configured
        )
    else:
        await message.answer('Ожидался текст 🤷‍♂️\nПопробуйте еще раз.', reply_markup=keyboard_start_configured)




