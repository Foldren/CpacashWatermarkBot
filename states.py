from aiogram.fsm.state import State, StatesGroup


class StepsGenerateVideo(StatesGroup):
    send_watermark = State()
    send_video = State()


class StepsCreateWatermark(StatesGroup):
    send_text = State()
