from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, BufferedInputFile,InputFile,FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from core import keyboard
from core.database import Database
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO





basket = Router()




@basket.callback_query(F.data=="basket")
async def read_basket(callback:CallbackQuery):
    await callback.answer("")
    basket =  await Database.Basket().read(callback.from_user.id)
    print(basket)
    if basket is not None:
        await callback.message.answer("\n".join([f"{key} - {value}"for key,value in basket.items()]),reply_markup=keyboard.basket)
    else: 
        await callback.message.answer("Корзина пуста",reply_markup=keyboard.main)

@basket.callback_query(F.data == "drop_basket")
async def drop_basket(callback:CallbackQuery):
    await callback.answer("")
    drop = await Database.Basket().drop(callback.from_user.id)
    if drop is not None:
        await callback.message.answer("Корзина очищена",reply_markup=keyboard.main)

@basket.callback_query(F.data == "save_order")
async def save_order(callback:CallbackQuery):
    await callback.answer("")
    drop = await Database.Basket().drop(callback.from_user.id)
    if drop is not None:
        drop["time"]=datetime.datetime.now().time().replace(microsecond=0).strftime("%H:%M:%S")
        drop["data"]=datetime.datetime.now().strftime("%d.%m.%Y")
        drop["name"]=f"@{callback.from_user.username}"
        drop["Статус"]="Открыт"
        user_id=drop.get("id")
        image = Image.new("RGB", (200, 100), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 50)
        draw.text((20, 20), str(user_id%10000), fill="black", font=font)
        b=BytesIO()
        image.save(b, format="JPEG")
        byte_image = b.getvalue()
        await Database.Order().add(drop)
        await callback.message.answer("Ваш номер заказа")
        await callback.message.answer_photo(photo=BufferedInputFile(file=byte_image, filename="dfsf.JPEG"),reply_markup=keyboard.main)
        b.close()
    else:
        await callback.message.answer("Error",reply_markup=keyboard.main)