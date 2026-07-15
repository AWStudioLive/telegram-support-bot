# Project: Telegram Support Bot
# Path: core/utils/smart_translator.py

import os
import json
import asyncio
from .logger import logger
from deep_translator import GoogleTranslator
from core.utils.settings import settings

CACHE_DIR = "translations_cache"

class SmartTranslator:
    def __init__(self):
        if not os.path.exists(CACHE_DIR):
            try:
                os.makedirs(CACHE_DIR)
            except Exception as e:
                logger.error(f"Не удалось создать директорию для кэша переводов: {e}")
                raise SystemExit("Критическая ошибка инициализации файловой системы для кэша.")
        
        self._loaded_caches = {}

    def _get_cache_path(self, lang: str) -> str:
        return os.path.join(CACHE_DIR, f"{lang.lower()}.json")

    def _load_cache_for_lang(self, lang: str) -> dict:
        lang = lang.lower().strip()
        
        if lang in self._loaded_caches:
            return self._loaded_caches[lang]
            
        file_path = self._get_cache_path(lang)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._loaded_caches[lang] = data
                    return data
            except Exception as e:
                logger.error(f"Не удалось загрузить кэш для языка '{lang}': {e}")
        
        self._loaded_caches[lang] = {}
        return self._loaded_caches[lang]

    def _save_cache_for_lang(self, lang: str):
        lang = lang.lower().strip()
        if lang not in self._loaded_caches:
            return
            
        file_path = self._get_cache_path(lang)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self._loaded_caches[lang], f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Не удалось сохранить кэш для языка '{lang}': {e}")

    # Оборачиваем синхронные методы в неблокирующие асинхронные вызовы
    async def load_cache_async(self, lang: str) -> dict:
        return await asyncio.to_thread(self._load_cache_for_lang, lang)

    async def save_cache_async(self, lang: str):
        await asyncio.to_thread(self._save_cache_for_lang, lang)

    async def translate(self, text: str, from_lang: str, to_lang: str = None) -> str:
        """
        Асин перевод текста. Больше не использует глобальный settings напрямую для записи,
        а принимает to_lang как аргумент, предотвращая Race Condition.
        """
        if not text or not text.strip():
            return ""

        from_lang = from_lang.lower().strip()
        target_lang = (to_lang or settings.DEFAULT_TRANSLATION_LANG).lower().strip()
        clean_text = text.strip().lower()

        if from_lang == target_lang:
            return text

        # Загружаем кэш асинхронно
        lang_cache = await self.load_cache_async(from_lang)

        # Ключ кэша должен учитывать целевой язык, иначе перевод 'привет' -> 'en' перезапишет 'привет' -> 'es'.
        cache_key = f"{clean_text}::{target_lang}"

        if cache_key in lang_cache:
            logger.info(f"[{from_lang.upper()} -> {target_lang.upper()}] Из кэша: '{clean_text}' -> '{lang_cache[cache_key]}'")
            return lang_cache[cache_key]

        try:
            logger.info(f"[{from_lang.upper()} -> {target_lang.upper()}] Сетевой запрос автоперевода для: '{text}'")
            
            # GoogleTranslator делает синхронный сетевой запрос, отправляем его в thread pool
            translator_instance = GoogleTranslator(source=from_lang, target=target_lang)
            translated = await asyncio.to_thread(translator_instance.translate, text)
            
            lang_cache[cache_key] = translated
            await self.save_cache_async(from_lang)
            
            return translated
        except Exception as e:
            logger.error(f"Ошибка сети при автопереводе с языка '{from_lang}' на '{target_lang}': {e}")
            return text

translator = SmartTranslator()