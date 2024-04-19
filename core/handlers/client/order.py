from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from core import keyboard
from core.database import Database






order = Router()


@order.callback_query(F.data == "read_order")
async def read_order(callback:CallbackQuery):
    await callback.answer("")
    order = await Database.Order().get_order(callback.from_user.id)
    if order:
        print(order)
        await callback.message.answer("Ваш заказ")
        await callback.message.answer(f"Номер заказа: {str(callback.from_user.id%10000)}")
        await callback.answer("\n".join([f"{key} - {value}"for key,value in order.items()]))
        await callback.message.answer(reply_markup=keyboard.main)
    else:
        print("error")
        await callback.message.answer("У вас нет заказов", reply_markup=keyboard.main)
        


@order.callback_query(F.data == "cancel")
async def drop_order(callback:CallbackQuery):
    await callback.answer("")
    await Database.Order().delete_order(callback.from_user.id)
    await callback.message.answer("Ваш заказ удален", reply_markup=keyboard.main)