from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from core import keyboard
from core.database import Database


class Status(StatesGroup):
    confirm=State()

product = Router()


@product.message(CommandStart())
async def start(message:Message):
    await message.answer("Привет с моей помощью можно сделать заказ",reply_markup=keyboard.main)

@product.callback_query(F.data == "menu")
async def client_menu(callback:CallbackQuery):
    await callback.answer("")
    await start(callback.message)
@product.callback_query(F.data  =="product")
async def select_product(callback:CallbackQuery,state:FSMContext):
    await callback.answer("")
    order = await Database.Order().get_order(callback.from_user.id)
    if not order:
        await callback.message.answer("Выберите товар",reply_markup=await keyboard.product())   
    else:
        await state.set_state(Status.confirm)
        await callback.message.answer("У вас уже есть заказ хотите его изменить?",reply_markup=keyboard.True_and_False)

@product.callback_query(Status.confirm,F.data=="Yes")
async def yes_order(callback:CallbackQuery,state:FSMContext):
    await callback.answer("")
    await state.clear()
    await callback.message.answer("Выберите товар",reply_markup=await keyboard.product())

@product.callback_query(Status.confirm,F.data=="No")
async def no_order(callback:CallbackQuery,state:FSMContext):
    await callback.answer("")
    await state.clear()
    await start(callback.message)




@product.callback_query(F.data.startswith("product_"))
async def order(callback:CallbackQuery):
    await callback.answer("")
    product = callback.data.split("_")[1]
    await callback.message.answer("Выберите количество",reply_markup=await keyboard.Quantity(product).quantity())

@product.callback_query(F.data.startswith("quantity_"))
async def quantity(callback:CallbackQuery):
    await callback.answer("")
    product = callback.data.split("_")[1]
    quantity = callback.data.split("_")[2]
    await Database.Basket().add({"id":callback.from_user.id,product:quantity})
    await callback.message.answer("Товар добавлен в корзину",reply_markup=await keyboard.product())