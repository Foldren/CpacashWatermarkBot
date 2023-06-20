from os import getcwd
from aiogram.fsm.storage.memory import MemoryStorage

IS_LOCAL = "Pycharm" in getcwd()
TEMP_FILES_DIR = f"{getcwd()}\\source\\temp_files" if IS_LOCAL else f"{getcwd()}\\temp_files"
FONT_FILES_DIR = f"{getcwd()}\\source\\tools\\fonts" if IS_LOCAL else f"{getcwd()}\\tools\\fonts"
ACTIVE_USERS_STORAGE = MemoryStorage()
FFMPEG_PATH = f'{getcwd()}\\source\\tools\\ffmpeg_drivers\\ffmpeg-windows.exe' if IS_LOCAL else f'{getcwd()}\\tools\\ffmpeg_drivers\\ffmpeg-linux'
