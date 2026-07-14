# Project: Telegram Support Bot
# Path: core/utils/system_logger.py

from core.utils.logger import logger
from core.utils.tg_sender import send_telegram_log

def log_system_event(text: str, log_code: str = "SYSTEM", level: str = "INFO"):
    """
    Универсальный фасад управления логами проекта.
    
    Уровни (level):
    - "DEBUG":     Только в консоль Docker.
    - "INFO":      Только в консоль Docker (обычные фоновые логи).
    - "NOTIFY":    В консоль (INFO) + в Telegram с эмодзи 🔹 (старт, новые тикеты).
    - "WARNING":   В консоль (WARNING) + в Telegram с эмодзи ⚠️ (предупреждения).
    - "ERROR":     В консоль (ERROR) + в Telegram с эмодзи ❌ (ошибки / сбои).
    """
    level = level.upper().strip()
    console_message = f"[{log_code.upper()}] {text}"

    # --- [ ШАГ 1. ЗАПИСЬ В КОНСОЛЬ СЕРВЕРА (Всегда) ] ---
    if level == "ERROR":
        logger.error(console_message)
    elif level == "WARNING":
        logger.warning(console_message)
    elif level == "DEBUG":
        logger.debug(console_message)
    else:
        # Для INFO и NOTIFY пишем в консоль как обычный INFO
        logger.info(console_message)

    # --- [ ШАГ 2. ФИЛЬТРАЦИЯ ДЛЯ TELEGRAM ] ---
    # Если это дебаг или обычная фоновая инфа — в Telegram не шлем
    if level in ["DEBUG", "INFO"]:
        return

    # Отправляем в Telegram
    send_telegram_log(text=text, log_code=log_code, level=level)