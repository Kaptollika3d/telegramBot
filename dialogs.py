from typing import Any
import operator

from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, DialogRegistry, Window, Dialog, StartMode, ChatEvent
from aiogram_dialog.widgets.kbd import Select, Button, Column, Multiselect, Next, Back, ManagedMultiSelectAdapter
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

import getdata

class MySG(StatesGroup):    
    select_timetable = State()
    main = State()
    multiselect_clients_by_time= State()

main_window = Window(
    Const("Hello, unknown person"),
    Button(Const("Useless button"), id="nothing"),
    state=MySG.main,
)

async def on_clients_by_time_selected(c: CallbackQuery, multi:ManagedMultiSelectAdapter, widget: Any, dialog_manager: DialogManager):
    #print("Clients selected: ", dialog_manager.current_context().dialog_data.get("clients"))  
    print(multi.get_checked())
    #dialog_manager.current_context().dialog_data["s_times"] = item_id
    #await dialog_manager.start(MySG.multiselect_clients_by_time, mode=StartMode.RESET_STACK)
    #await dialog.next(dialog_manager)

clients_by_time_select = Multiselect(
    Format("✓ {item[1]}"),
    Format("{item[1]}"),
    id="m_clients_by_time",
    item_id_getter=operator.itemgetter(0),
    items="clients",
    on_click=on_clients_by_time_selected,
)

clients_by_time_select_window = Window(
    Format("Выберите посетителей:"),
    Column(clients_by_time_select),
    Button(Const("ОК"), id="ok"),# on_click=on_clients_by_time_selected),
    Back(Const('Назад')),
    state=MySG.multiselect_clients_by_time,
    getter=getdata.get_clients_by_time,
    preview_add_transitions=[Next()],
)

async def on_timetable_selected(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    print("Times selected: ", item_id)  
    dialog_manager.current_context().dialog_data["s_times"] = item_id
    #await dialog_manager.start(MySG.multiselect_clients_by_time, mode=StartMode.RESET_STACK)
    await dialog.next(dialog_manager)

timetable_select = Select(
    Format("{item[1]}"),  
    id="s_times",
    item_id_getter=operator.itemgetter(0), 
    items="times",
    on_click=on_timetable_selected,
        ) 

timetable_select_window =  Window(
    Format("Выберите время:"), 
    Column(timetable_select), 
    state=MySG.select_timetable, 
    getter=getdata.get_timetable,
)

dialog = Dialog(
    main_window,
    timetable_select_window,
    clients_by_time_select_window,
)

def DialogReg(dp: Dispatcher):
    registry = DialogRegistry(dp)
    registry.register(dialog)