# Project: Titan Cloud Tech (Telegram Bot)
# Path: core/telegram/admin_handlers.py

import re
from aiogram import Router, types, F
from core.utils.settings import settings
from core.utils.logger import logger

admin_router = Router()


# 1. Ловим нажатие кнопки "Взять в работу" (Универсальный: текст и медиа)
@admin_router.callback_query(F.data.startswith("claim_"))
async def claim_ticket(callback: types.CallbackQuery):
    admin_username = callback.from_user.username or callback.from_user.first_name
    user_id = callback.data.split("_")[1]
    
    # Извлекаем текст из обычного сообщения или подписи под медиафайлом
    old_text = callback.message.text or callback.message.caption or ""
    
    updated_text = (
        f"{old_text}\n\n"
        f"🔒 **Тикет взял в работу:** @{admin_username}"
    )
    
    try:
        # Если тикет прилетел с картинкой или документом — редактируем подпись
        if callback.message.document or callback.message.photo:
            await callback.message.edit_caption(caption=updated_text, reply_markup=None)
        else:
            await callback.message.edit_text(text=updated_text, reply_markup=None)
        
        # Пишем клиенту в личку без палева админских ников
        await callback.bot.send_message(
            chat_id=int(user_id),
            text="⏳ **Ваше обращение взято в работу.** Специалист уже изучает проблему."
        )
        
        await callback.answer("Тикет зафиксирован!")
    except Exception as e:
        logger.error(f"Ошибка при обновлении статуса тикета: {e}")
        await callback.answer("Произошла ошибка при взятии тикета.", show_alert=True)


# 2. Ловим ОТВЕТ админа через Reply (Универсальный: текст, фото, файлы)
@admin_router.message(
    F.chat.id == settings.TG_ADMIN_GROUP_ID, 
    F.message_thread_id == settings.TG_TOPIC_SUPPORT_ID, 
    F.reply_to_message
)
async def reply_back_to_user(message: types.Message):
    try:
        # Достаем текст исходного обращения (из сообщения или подписи к фото)
        original_text = message.reply_to_message.text or message.reply_to_message.caption
        if not original_text:
            await message.reply("❌ Не удалось прочитать данные исходного сообщения.")
            return

        # Ищем ID пользователя регуляркой, чтобы исключить любые сбои парсинга
        match = re.search(r"ID:\s*`?(\d+)`?", original_text)
        if not match:
            await message.reply("❌ Не могу найти ID пользователя в этом сообщении.")
            return
            
        user_id = int(match.group(1))
        
        # Если админ ответил обычным текстом, оформляем красивой плашкой
        if message.text:
            await message.bot.send_message(
                chat_id=user_id,
                text=f"💬 **Ответ техподдержки Titan Cloud:**\n\n{message.text}",
                parse_mode="Markdown"
            )
        # Если админ прикрепил в ответ файл, скриншот или лог
        else:
            await message.copy_to(chat_id=user_id)
            
        await message.reply("✅ Отправлено")
        
        # Авто-взятие в работу, если забыл нажать кнопку перед ответом
        if "Тикет взял в работу:" not in original_text:
            admin_username = message.from_user.username or message.from_user.first_name
            updated_text = f"{original_text}\n\n🔒 **Тикет взял в работу (авто):** @{admin_username}"
            
            if message.reply_to_message.document or message.reply_to_message.photo:
                await message.reply_to_message.edit_caption(caption=updated_text, reply_markup=None)
            else:
                await message.reply_to_message.edit_text(text=updated_text, reply_markup=None)
        
    except Exception as e:
        logger.error(f"Ошибка при отправке ответа пользователю: {e}")
        await message.reply(f"❌ Не удалось отправить ответ. Ошибка: {e}")