# Project: Telegram Support Bot
# Path: core/utils/tg_sender.py

import sys
import requests
import asyncio
import re
from core.utils.settings import settings

def send_telegram_log(text: str, log_code: str = "SYS", level: str = "INFO"):
    """
    Универсальная утилита для быстрой отправки уведомлений/логов в админ-чат.
    - Автоматически переводит ТЕКСТ сообщения на язык админки (DEFAULT_TRANSLATION_LANG).
    - Код в квадратных скобках [LOG_CODE] всегда остается на английском.
    """
    token = getattr(settings, "TG_SUPPORT_BOT_TOKEN", None)
    chat_id = getattr(settings, "TG_ADMIN_GROUP_ID", None)
    topic_id = getattr(settings, "TG_TOPIC_LOGS_ID", None)
    
    if not token or not chat_id or topic_id is None:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 🌍 --- [ АВТО-ПЕРЕВОД ТЕКСТА ] ---
    target_lang = settings.DEFAULT_TRANSLATION_LANG.lower().strip()
    translated_text = text

    try:
        from core.utils.smart_translator import translator
        
        # Определяем язык исходного текста (если есть кириллица — 'ru', иначе 'en')
        detected_lang = "ru" if re.search('[а-яА-Я]', text) else "en"
        
        # Если язык текста не совпадает с целевым языком админки — переводим
        if detected_lang != target_lang:
            translation = translator.translate(text, from_lang=detected_lang)
            if translation and translation.strip():
                translated_text = translation.strip()
    except Exception as e:
        # Если перевод упал (например, переводчик еще не инициализирован), 
        # просто пишем ошибку в консоль и отправляем оригинальный текст.
        sys.stdout.write(f"[TG_SENDER_WARNING] Не удалось перевести лог: {e}\n")

    # 🎨 --- [ ВЫБОР ЭМОДЗИ ПО УРОВНЮ ] ---
    level = level.upper().strip()
    if level == "ERROR":
        emoji = "❌"  # Строгий красный крест для ошибок
    elif level == "WARNING":
        emoji = "⚠️"  # Предупреждение
    else:
        emoji = "🔹"  # Стильный синий значок для важных уведомлений (NOTIFY)

    # Форматируем тег в верхнем регистре
    code_tag = f"[{log_code.upper().strip()}]"
    
    # Экранируем спецсимволы HTML
    safe_text = translated_text.replace("<", "&lt;").replace(">", "&gt;")
    
    # Собираем чистое сообщение на целевом языке
    formatted_message = f"{emoji} <b>{code_tag}</b> {safe_text}"
    
    payload = {
        "chat_id": chat_id,
        "text": formatted_message,
        "parse_mode": "HTML"
    }

    if topic_id > 1:
        payload["message_thread_id"] = topic_id

    def _send():
        try:
            res = requests.post(url, json=payload, timeout=5)
            if res.status_code != 200:
                sys.stdout.write(f"[TG_SENDER_ERROR] Ошибка Telegram API: {res.text}\n")
        except Exception as e:
            sys.stdout.write(f"[TG_SENDER_ERROR] Ошибка сети при отправке в TG: {e}\n")

    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            loop.run_in_executor(None, _send)
        else:
            _send()
    except RuntimeError:
        _send()