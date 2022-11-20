import asyncio

from loader import bot, dp, on_startup, on_shutdown


async def main():
    on_startup(dp)
    await dp.start_polling(bot, on_shutdown=on_shutdown)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(main())
