import asyncio

from loader import dp, on_startup, on_shutdown


async def main():
    on_startup(dp)
    await dp.start_polling(dp, on_shutdown=on_shutdown)


if __name__ == "__main__":
    asyncio.run(main())
