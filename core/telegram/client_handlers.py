# Project: Titan Cloud Tech (Telegram Bot)
# Path: core/telegram/client_handlers.py

import logging
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.settings import settings
from core.utils.logger import logger

client_router = Router()


@client_router.message(CommandStart(), F.chat.type == "private")
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Это официальный бот поддержки **Titan Cloud Tech**.\n\n"
        "Опишите вашу проблему, отправьте скриншот или файл прямо в этот чат, "
        "и наши специалисты ответят вам в ближайшее время.",
        parse_mode="Markdown"
    )


@client_router.message(F.chat.type == "private")
async def forward_to_admin_topic(message: types.Message):
    # Формируем заголовок обращения с данными пользователя
    user_info = (
        f"📩 **Новое сообщение от клиента!**\n"
        f"От: @{message.from_user.username or 'без_юзернейма'}\n"
        f"ID: `{message.from_user.id}`\n\n"
    )
    
    # Извлекаем текст, если он есть, либо подпись к медиафайлу
    user_content = message.text or message.caption or "[Медиафайл без описания]"
    full_info_text = f"{user_info}💬 {user_content}"
    
    # Кнопка "Взять в работу"
    kb = InlineKeyboardBuilder()
    kb.button(text="🛠️ Взять в работу", callback_data=f"claim_{message.from_user.id}")
    
    try:
        # Если пользователь прислал обычный текст
        if message.text:
            await message.bot.send_message(
                chat_id=settings.TG_ADMIN_GROUP_ID,
                text=full_info_text,
                message_thread_id=settings.TG_TOPIC_SUPPORT_ID,
                reply_markup=kb.as_markup(),
                parse_mode="Markdown"
            )
        # Если прислал фото, документ, лог-файл или видео
        else:
            await message.copy_to(
                chat_id=settings.TG_ADMIN_GROUP_ID,
                message_thread_id=settings.TG_TOPIC_SUPPORT_ID,
                caption=full_info_text,
                reply_markup=kb.as_markup(),
                parse_mode="Markdown"
            )
            
        await message.answer("🚀 Ваше сообщение доставлено поддержке!")
        
    except Exception as e:
        logger.error(f"Ошибка при пересылке обращения в админку: {e}")
        await message.answer("⚠️ Произошла ошибка при отправке сообщения. Попробуйте позже.")