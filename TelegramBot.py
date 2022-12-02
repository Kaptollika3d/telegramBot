from pickle import TRUE
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import DBquery 

TOKEN = '5135989684:AAHpRL6cpxJNMFSHCseWNrSgnuDQYLrMHxM'
bot = Bot(token = TOKEN)

dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    conn = DBquery.connectToDB()
    if DBquery.analyzeUser(conn, msg.from_user.id) is None:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        regButton = types.KeyboardButton(text='Регистрация', request_contact=True)
        keyboard.add(regButton)
        cancelButton = types.KeyboardButton(text='Отмена')
        keyboard.add(cancelButton)
        await msg.answer("Хотите зарегистрироваться?", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        cancelRegButton = types.KeyboardButton(text='Отмена регистрации')
        keyboard.add(cancelRegButton)
        await msg.answer('Выберите команду:', reply_markup=keyboard)
    conn.close()

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    print(msg.text.lower())
    if msg.text.lower() == 'отмена регистрации':
        conn = DBquery.connectToDB()
        cur = conn.cursor()
        cur.execute('DELETE FROM USERS WHERE ID = ?', (msg.from_user.id,))
        conn.commit()
        conn.close()
        await msg.answer('Отменено!')
    else:
        await msg.answer('Не понимаю, что это значит.209880137')

@dp.message_handler(content_types=['contact'])
async def get_contact_info(msg: types.Message):
    conn = DBquery.connectToDB()
    DBquery.createNewUser(conn, msg.from_user.id, msg.from_user.full_name, msg.contact.phone_number)
    await msg.answer('Поздравляю! Регистрация прошла успешно!')
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

 