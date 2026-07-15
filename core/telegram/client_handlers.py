# Project: Titan Cloud Tech (Telegram Bot)
# Path: core/telegram/client_handlers.py

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.settings import settings
from core.utils.smart_translator import translator
from core.utils.locales import get_text
from core.utils.system_logger import log_system_event

client_router = Router()


@client_router.message(CommandStart(), F.chat.type == "private")
async def cmd_start(message: types.Message):
    user_lang = (message.from_user.language_code or "en").lower()
    
    # Берем текст приветствия на языке клиента (или en по умолчанию)
    welcome_text = get_text("welcome", lang=user_lang)
    await message.answer(welcome_text, parse_mode="Markdown")


@client_router.message(F.chat.type == "private")
async def forward_to_admin_topic(message: types.Message):
    user_lang = (message.from_user.language_code or "en").lower()
    target_lang = settings.DEFAULT_TRANSLATION_LANG.lower()
    
    # Язык админки берем из конфигурации settings.py (по умолчанию 'en')
    admin_lang = target_lang 
    
    user_content = message.text or message.caption or ""
    
    # Автоперевод для админов (если язык клиента отличается от целевого языка админки)
    translated_content = ""
    if user_content and user_lang != target_lang:
        try:
            # Добавлен await!
            translation = await translator.translate(user_content, from_lang=user_lang, to_lang=target_lang)
            if translation.lower() != user_content.lower():
                translated_content = f"\n\n🤖 **Translation [{user_lang.upper()} -> {target_lang.upper()}]:**\n_{translation}_"
        except Exception as trans_err:
            log_system_event(
                text=f"Не удалось перевести входящее сообщение от {message.from_user.id}: {trans_err}",
                log_code="IN_TRANS_ERR",
                level="WARNING"
            )
    
    # Формируем заголовок для админов на языке админки
    user_info = (
        f"{get_text('new_ticket_title', admin_lang)}\n"
        f"{get_text('user_label', admin_lang)}: @{message.from_user.username or 'no_username'}\n"
        f"{get_text('id_label', admin_lang)}: `{message.from_user.id}`\n"
        f"{get_text('lang_label', admin_lang)}: `{user_lang.upper()}`\n\n"
    )
    
    full_info_text = f"{user_info}💬 {user_content or '[Media File]'}{translated_content}"
    
    # Кнопка действия (на языке админки)
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("claim_btn", admin_lang), 
        callback_data=f"claim_{message.from_user.id}"
    )
    
    try:
        if message.text:
            await message.bot.send_message(
                chat_id=settings.TG_ADMIN_GROUP_ID,
                text=full_info_text,
                message_thread_id=settings.TG_TOPIC_SUPPORT_ID,
                reply_markup=kb.as_markup(),
                parse_mode="Markdown"
            )
        else:
            await message.copy_to(
                chat_id=settings.TG_ADMIN_GROUP_ID,
                message_thread_id=settings.TG_TOPIC_SUPPORT_ID,
                caption=full_info_text,
                reply_markup=kb.as_markup(),
                parse_mode="Markdown"
            )
            
        # Подтверждение отправки (на языке клиента)
        await message.answer(get_text("ticket_delivered", user_lang))
        
    except Exception as e:
        # Записываем ошибку пересылки
        log_system_event(
            text=f"Ошибка при пересылке обращения от @{message.from_user.username or 'no_username'} ({message.from_user.id}): {e}",
            log_code="FWD_ERR",
            level="ERROR"
        )
        await message.answer(get_text("send_error", user_lang))