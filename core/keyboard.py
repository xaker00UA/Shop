from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.database import Database


main =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Продукты",callback_data="product"),InlineKeyboardButton(text="Корзина",callback_data="basket")],
    [InlineKeyboardButton(text="Просмотреть заказ",callback_data="read_order"),InlineKeyboardButton(text="Отменить заказ",callback_data="cancel_order")]])

basket = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Очистить корзину",callback_data="drop_basket"),InlineKeyboardButton(text="Оформить заказ",callback_data="save_order")]
])

admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить менеджера",callback_data="save_manager"),InlineKeyboardButton(text="Удалить менеджера",callback_data="drop_manager")]
])

manager = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать таблицу",callback_data="create_table"),InlineKeyboardButton(text="Удалить закрытые заказы",callback_data="delete_order_close")],
    [InlineKeyboardButton(text="Изменить статус заказа",callback_data="change_order"),InlineKeyboardButton(text="Написать сообщение открытым заказам",callback_data="write_order_open")]
])

True_and_False = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да",callback_data="Yes"),InlineKeyboardButton(text="Нет",callback_data="No")]
])
async def product():
    product = await Database.Product().get_all()
    keyboard = InlineKeyboardBuilder()
    for i in product:
        keyboard.button(text=i.get("name"),callback_data=f'product_{i.get("name")}')
    keyboard.button(text="Назад",callback_data="menu")
    keyboard.adjust(3)
    return keyboard.as_markup()


class Quantity:
    def __init__(self,name) -> None:
        self.name = name
    async def define(self):
        if self.name == "Творог":
            quantity =[200,300,500,700,800,1000,1200,1500,2000]
        elif self.name == "Молоко":
            quantity =[0.5,1.0,1.5,2.0,3.0]
        elif self.name == "Сметана":
            quantity =[0.5,1.0]
        elif self.name == "Сливки":
            quantity =[65,75,85,95,100,115,135,150]
        elif self.name == "Брынза":
            quantity =[200,300,500,600,700,800,1000]
        return quantity
        
    async def quantity(self):
        quantity =await Quantity.define(self)
        keyboard = InlineKeyboardBuilder()
        for i in quantity:
            keyboard.button(text=str(i),callback_data=f'quantity_{self.name}_{i}')
        keyboard.button(text="Назад",callback_data="product")
        keyboard.adjust(3)
        return keyboard.as_markup()