from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from core import keyboard
from core.database import Database
from config import ADMIN_ID



admin =Router()

class Manager(StatesGroup):
    id = State()
    name = State()


class Admin_protect(Filter):
    async def __call__(self,event):
        if isinstance(event,Message):
            return event.from_user.id == str(ADMIN_ID)
        if isinstance(event,CallbackQuery):
            return event.from_user.id == str(ADMIN_ID)
    
    

@admin.message(Admin_protect(),Command('admin'))
async def admin_panel(message:Message):
    await message.answer("Admin panel",reply_markup=keyboard.admin)

@admin.callback_query(Admin_protect(),F.data =="save_manager")
async def save_manager(callback:CallbackQuery,state:FSMContext):
    await callback.answer("")
    await state.set_state(Manager().name)
    await callback.message.answer("Введите название менеджера")

@admin.message(Admin_protect(),Manager.name)
async def name_manager(message:Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Manager.id)
    await message.answer("Введите ID менеджера")


@admin.message(Admin_protect(),Manager.id)
async def id_manager(message:Message, state:FSMContext):
    manager = await state.update_data(id=message.text)
    await state.clear()
    await Database.Manager().add(manager)
    await message.answer("Менеджер добавлен", replay_markup=keyboard.admin)


@admin.callback_query(Admin_protect(),F.data =="drop_manager")
async def drop_manager(callback:CallbackQuery,state:FSMContext):
    await callback.answer("")
    await state.set_state(Manager.name)
    await callback.message.answer("Введите имя менеджера или айди")

@admin.message(Admin_protect(),Manager.name)
async def name_manager(message:Message, state:FSMContext):
    await state.clear()
    if await Database.Manager().delete_manger(message.text):
        await message.answer("Менеджер удален")
    else:
        await message.answer("Менеджер не найден")