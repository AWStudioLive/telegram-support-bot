# Project: Telegram Support Bot
# Path: core/utils/locales/__init__.py

from .en import messages as en_messages
from .ru import messages as ru_messages

# Регистрируем поддерживаемые языки
LOCALES = {
    "en": en_messages,
    "ru": ru_messages
}

def get_text(key: str, lang: str = "en", **kwargs) -> str:
    """
    Возвращает строку на нужном языке по ключу.
    Если язык не поддерживается, берет английский (en) по умолчанию.
    Позволяет форматировать строки через kwargs.
    """
    lang = lang.lower().strip()
    if lang not in LOCALES:
        lang = "en"  # Фоллбэк на английский
        
    translation = LOCALES[lang].get(key, LOCALES["en"].get(key, key))
    
    # Если в строке есть плейсхолдеры (например, {admin_username}), форматируем их
    if kwargs:
        try:
            return translation.format(**kwargs)
        except KeyError:
            return translation
            
    return translation