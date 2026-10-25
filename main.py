from aiogram import Bot, Dispatcher
from handlers import user
from dotenv import load_dotenv
import os

load_dotenv()
async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)

token = os.getenv('TOKEN')
if not token:
    raise ValueError('Не найден токен бота в файле .env!')

Bot(token=token)


if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
