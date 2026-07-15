# Project: Telegram Support Bot
# Path: main.py

import asyncio
from aiogram import Bot, Dispatcher
from core.utils.settings import settings
from core.telegram.client_handlers import client_router
from core.telegram.admin_handlers import admin_router
from core.utils.system_logger import log_system_event

async def main():
    # Запишется только в консоль Docker (уровень INFO)
    log_system_event(
        text=f"Инициализация бота поддержки: @{settings.TG_SUPPORT_BOT_NAME}",
        log_code="BOT_INIT",
        level="INFO"
    )
    
    bot = Bot(token=settings.TG_SUPPORT_BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем разделенные рутеры к главному диспетчеру
    dp.include_router(client_router)
    dp.include_router(admin_router)

    try:
        # Сбрасываем старые обновления
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Запишется в Docker + прилетит синяя кнопка 🔹 в Telegram
        log_system_event(
            text=f"Бот поддержки @{settings.TG_SUPPORT_BOT_NAME} запущен.\nЯзык: {settings.DEFAULT_TRANSLATION_LANG.upper()}",
            log_code="BOT_START",
            level="NOTIFY"
        )
        
        # Запуск прослушивания сети
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию при завершении работы
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Запишется в Docker + прилетит красный крестик ❌ в Telegram
        log_system_event(
            text="Бот поддержки остановлен администратором.",
            log_code="BOT_STOP",
            level="ERROR"
        )