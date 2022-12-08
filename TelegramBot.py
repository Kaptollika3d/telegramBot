from pickle import TRUE
from typing import Any
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from aiogram_dialog import DialogManager, DialogRegistry, Window, Dialog, StartMode
from aiogram_dialog.widgets.kbd import Select, Button, Column
from aiogram_dialog.widgets.text import Format, Const

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.session import DBSession
import operator

import db.queries

TOKEN = '5135989684:AAHpRL6cpxJNMFSHCseWNrSgnuDQYLrMHxM'
bot = Bot(token = TOKEN)
admin_id = 209880137

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)

class MySG(StatesGroup):
    main = State()
    select_timetable = State()

main_window = Window(
    Const("Hello, unknown person"),
    Button(Const("Useless button"), id="nothing"),
    state=MySG.main,
)
#dialog = Dialog(main_window)

# let's assume this is our window data getter
async def get_timetable(**kwargs):
    engine = create_engine("sqlite:///db/DB.db")
    session_factory = sessionmaker(bind=engine)
    db_session = DBSession(session_factory())
    times = db.queries.get_timetable(db_session)
    print(times)
    return {
      "times": times,
    }

async def on_timetable_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    print("Times selected: ", item_id)   

timetable_kbd = Select(
    Format("{item[1]}"),  
    id="s_times",
    item_id_getter=operator.itemgetter(0), 
    items="times",
    on_click=on_timetable_selected,
        ) 
dialog = Dialog(
    Window(Format("Выберите время:"), Column(timetable_kbd), state=MySG.select_timetable, getter=get_timetable)
)
registry.register(dialog)

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
    await dialog_manager.start(MySG.select_timetable, mode=StartMode.RESET_STACK)

async def on_fruit_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    print("Fruit selected: ", item_id)

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    print(msg.text.lower())
    await msg.answer('Не понимаю, что это значит.209880137' & msg.co)

@dp.message_handler(content_types=['contact'])
async def get_contact_info(msg: types.Message):
    await msg.answer('Поздравляю! Регистрация прошла успешно!')
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

 