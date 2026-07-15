# Project: Titan Cloud Tech (Telegram Bot)
# Path: core/telegram/admin_handlers.py

import re
from aiogram import Router, types, F
from core.utils.settings import settings
from core.utils.locales import get_text, LOCALES
from core.utils.smart_translator import translator
from core.utils.system_logger import log_system_event

admin_router = Router()

@admin_router.callback_query(F.data.startswith("claim_"))
async def claim_ticket(callback: types.CallbackQuery):
    admin_username = callback.from_user.username or callback.from_user.first_name
    user_id = callback.data.split("_")[1]
    
    old_text = callback.message.text or callback.message.caption or ""
    admin_lang = settings.DEFAULT_TRANSLATION_LANG.lower()
    
    lang_match = re.search(r"(?:Language|Язык клиента):\s*`?(\w+)`?", old_text, re.IGNORECASE)
    user_lang = lang_match.group(1).lower() if lang_match else "en"
    
    claimed_msg = get_text("ticket_claimed_admin", admin_lang, admin_username=admin_username)
    updated_text = f"{old_text}\n\n{claimed_msg}"
    
    try:
        if callback.message.document or callback.message.photo:
            await callback.message.edit_caption(caption=updated_text, reply_markup=None)
        else:
            await callback.message.edit_text(text=updated_text, reply_markup=None)
        
        if user_lang in LOCALES:
            client_notification = get_text("ticket_claimed_client", user_lang)
        else:
            english_base = get_text("ticket_claimed_client", "en")
            # Исправлено: await для асинхронного метода translator.translate
            client_notification = await translator.translate(
                text=english_base,
                from_lang="en",
                to_lang=user_lang
            )
        
        await callback.bot.send_message(
            chat_id=int(user_id),
            text=client_notification,
            parse_mode="Markdown"
        )
        
        await callback.answer(get_text("ticket_fixed_toast", admin_lang))
    except Exception as e:
        log_system_event(
            text=f"Ошибка при обновлении статуса тикета для пользователя {user_id}: {e}",
            log_code="CLAIM_ERR",
            level="ERROR"
        )
        await callback.answer("Error processing ticket", show_alert=True)


@admin_router.message(
    F.chat.id == settings.TG_ADMIN_GROUP_ID, 
    F.message_thread_id == settings.TG_TOPIC_SUPPORT_ID, 
    F.reply_to_message
)
async def reply_back_to_user(message: types.Message):
    admin_lang = settings.DEFAULT_TRANSLATION_LANG.lower()
    
    try:
        original_text = message.reply_to_message.text or message.reply_to_message.caption
        if not original_text:
            await message.reply(get_text("err_read_msg", admin_lang))
            return

        match = re.search(r"ID:\s*`?(\d+)`?", original_text)
        if not match:
            await message.reply(get_text("err_no_id", admin_lang))
            return
            
        user_id = int(match.group(1))
        
        lang_match = re.search(r"(?:Language|Язык клиента):\s*`?(\w+)`?", original_text, re.IGNORECASE)
        user_lang = lang_match.group(1).lower() if lang_match else "en"
        
        header = get_text("support_reply_header", user_lang)
        
        if message.text:
            # УСТРАНЕНО состояние гонки: передаем user_lang третьим аргументом to_lang напрямую
            if admin_lang != user_lang:
                try:
                    client_reply_text = await translator.translate(
                        text=message.text,
                        from_lang=admin_lang,
                        to_lang=user_lang
                    )
                except Exception as trans_err:
                    client_reply_text = message.text
                    log_system_event(
                        text=f"Сбой автоперевода ответа для пользователя {user_id}: {trans_err}",
                        log_code="TRANS_WARN",
                        level="WARNING"
                    )
            else:
                client_reply_text = message.text

            await message.bot.send_message(
                chat_id=user_id,
                text=f"{header}\n\n{client_reply_text}",
                parse_mode="Markdown"
            )
        else:
            await message.copy_to(chat_id=user_id)
            
        await message.reply(get_text("sent_success", admin_lang))
        
        if "Ticket claimed" not in original_text and "Тикет взял" not in original_text:
            admin_username = message.from_user.username or message.from_user.first_name
            claimed_msg_auto = get_text("ticket_claimed_admin_auto", admin_lang, admin_username=admin_username)
            updated_text = f"{original_text}\n\n{claimed_msg_auto}"
            
            if message.reply_to_message.document or message.reply_to_message.photo:
                await message.reply_to_message.edit_caption(caption=updated_text, reply_markup=None)
            else:
                await message.reply_to_message.edit_text(text=updated_text, reply_markup=None)
        
    except Exception as e:
        log_system_event(
            text=f"Ошибка при отправке ответа пользователю {user_id}: {e}",
            log_code="REPLY_ERR",
            level="ERROR"
        )
        await message.reply(get_text("err_send_reply", admin_lang, error=str(e)))