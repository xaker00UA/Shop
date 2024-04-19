from aiogram import Dispatcher, Bot
from config import TOKEN
import asyncio
import logging
from core.handlers import basket, product,order,manager,admin




async def main():
    # Create the bot
    bot = Bot(token=TOKEN)
    dp =Dispatcher()
    #Подключаем роутеры
    dp.include_routers(order,product,basket,manager,admin)

    # Запуск бота
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exiting...')
