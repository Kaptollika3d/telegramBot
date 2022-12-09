from pickle import TRUE
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram_dialog import DialogManager, StartMode

import dialogs

TOKEN = '5135989684:AAHpRL6cpxJNMFSHCseWNrSgnuDQYLrMHxM'
bot = Bot(token = TOKEN)
admin_id = 209880137

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dialogs.DialogReg(dp)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if msg.from_user.id == admin_id:       
        visitButton = types.KeyboardButton(text="Отметить посещения")
        keyboard.add(visitButton)

    cancelButton = types.KeyboardButton(text='Отмена')
    keyboard.add(cancelButton)
    await msg.answer('Выберите команду:', reply_markup=keyboard)

@dp.message_handler(content_types=['text'], text="Отметить посещения")
async def set_visit(msg: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(dialogs.MySG.select_timetable, mode=StartMode.RESET_STACK)

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    print(msg.text.lower())
    await msg.answer('Не понимаю, что это значит.209880137' & msg.co)

@dp.message_handler(content_types=['contact'])
async def get_contact_info(msg: types.Message):
    await msg.answer('Поздравляю! Регистрация прошла успешно!')
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

 