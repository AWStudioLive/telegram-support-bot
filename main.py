# Project: Titan Cloud Tech (Telegram Bot)
# Path: main.py
# Compliance: PROJECT_DNA_V6.5 (Main Entry Point)

import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.utils.settings import settings
from core.telegram.client_handlers import client_router
from core.telegram.admin_handlers import admin_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    logger.info(f"Инициализация бота поддержки: @{settings.TG_SUPPORT_BOT_NAME}")
    
    bot = Bot(token=settings.TG_SUPPORT_BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем наши разделенные рутеры к главному диспетчеру
    dp.include_router(client_router)
    dp.include_router(admin_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот поддержки остановлен.")