import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import create_watermark
from source.handlers import start, generate_video


async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=TOKEN)
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(start.rt, generate_video.rt, create_watermark.rt)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, bot_object=bot)


if __name__ == "__main__":
    asyncio.run(main())
