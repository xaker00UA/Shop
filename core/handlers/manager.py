from aiogram import F, Router
from aiogram.types import CallbackQuery, Message,FSInputFile
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from core import keyboard
from core.database import Database
import pandas as pd
manager = Router()


class Order(StatesGroup):
    id=State()
    message=State()







class ManagerProtect(Filter):
    async def __call__(self, event):
        manager = await Database.Manager().get_all()
        manager = [d["id"] for d in manager]
        if isinstance(event,Message):
            return event.from_user.id in manager
        if isinstance(event,CallbackQuery):
            return event.from_user.id in manager
        


@manager.message(ManagerProtect(),Command('manager'))
async def manager_menu(message:Message):
    print('asdf')
    await message.answer("Главное меню",reply_markup=keyboard.manager)

# Создаем таблицу
@manager.callback_query(ManagerProtect(), F.data == "create_table")
async def create_table(callback:CallbackQuery):
    callback.answer("")
    orders = await Database.Order().get_all_orders_open()
    if orders:
        df=pd.DataFrame(orders, columns=['id',"Сметана","Творог","Молоко","Брынза","Сливки", 'name', 'time','data'])
        total=df[["Сметана","Творог","Молоко","Брынза","Сливки"]].sum().to_frame().T
        df=pd.concat([df,total],ignore_index=False)
        df.to_excel('data.xlsx',index=False)
        file=FSInputFile(path='data.xlsx')
        await callback.message.answer_document(document=file,reply_markup=keyboard.manager)

    else:
        await callback.message.answer("Нет заказов")
     
    
    




# Изменяем статус заказа
@manager.callback_query(ManagerProtect(), F.data == "change_order")
async def change_order(callback:CallbackQuery,state:FSMContext):
    await callback.answer("")
    await state.set_state(Order.id)
    await callback.message.answer("Введите номер или id заказа")
# Получаем id 
@manager.message(ManagerProtect(), Order.id)
async def search_order(message:Message,state:FSMContext):
    order = await Database.Order().get_all_open(message.text)
    if len(order) == 1:
        order = order[0]
        order["Статус"]="Закрыт"
        await Database.Order().add(order)
        await state.clear()
        await message.answer("Заказ закрыт",reply_markup=keyboard.manager)
        await state.clear()
    elif len(order) >= 1:
        await message.answer("Введите id-заказа полностью")
    else:
        await message.answer("Заказ не найден",reply_markup=keyboard.manager)
        await state.clear()
# Удаление закрытых заказов
@manager.callback_query(ManagerProtect(), F.data == "delete_order_close")
async def delete_order_close(callback:CallbackQuery):
    await callback.answer("")
    count = await Database.Order().delete_order_close()
    await callback.message.answer(f"Удалено {count.deleted_count} заказов")





# Рассылка сообщений
@manager.callback_query(ManagerProtect(), F.data == "write_order_open")
async def message(callback:CallbackQuery,state:FSMContext):
    await callback.answer("")
    state.set_state(Order.message)
    await callback.message.answer("Введите сообщение")

@manager.message(ManagerProtect(), Order.message)
async def send_message(message:Message,state:FSMContext):
    open = await Database.Order().get_all_orders_open()
    open=[int(d["id"])for d in open]
    for user_id in open:
        await message.bot.send_message(user_id,message.text)
    await message.answer("Рассылка завершена")
    state.clear()


@manager.callback_query(ManagerProtect(), F.data == "")
async def protect(callback:CallbackQuery):
    pass

