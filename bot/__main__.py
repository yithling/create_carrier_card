import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN, LOG_FILE
from bot.handlers import (
    start,
    help_bot,
    carrier_card,
    osgop_carrier_card
)


async def main() -> None:
    #Активация бота
    bot = Bot(
        token=str(BOT_TOKEN), 
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
            )
    )

    #Создание диспетчера
    dp = Dispatcher(storage=MemoryStorage())

    #Импорт хендлеров
    dp.include_routers(
        start.router,
        help_bot.router,
        carrier_card.router,
        osgop_carrier_card.router
        )

    #Запуск бота
    await bot.delete_webhook(
        drop_pending_updates=True
    )
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == "__main__":
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    asyncio.run(main())
