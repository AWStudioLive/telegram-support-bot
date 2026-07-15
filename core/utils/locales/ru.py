# Project: Telegram Support Bot
# Path: core/utils/locales/ru.py

messages = {
    # Client-side strings
    "welcome": (
        "👋 Привет! Это официальный бот поддержки **Titan Cloud Tech**.\n\n"
        "Опишите вашу проблему, отправьте скриншот или файл прямо в этот чат, "
        "и наши специалисты ответят вам в ближайшее время."
    ),
    "ticket_delivered": "🚀 Ваше сообщение доставлено поддержке!",
    "send_error": "⚠️ Произошла ошибка при отправке сообщения. Попробуйте позже.",
    "ticket_claimed_client": "⏳ **Ваше обращение взято в работу.** Специалист уже изучает проблему.",
    "support_reply_header": "💬 **Ответ техподдержки Titan Cloud:**",

    # Admin-side strings
    "new_ticket_title": "📩 **Новое обращение в поддержку**",
    "user_label": "👤 Пользователь",
    "id_label": "🆔 ID",
    "lang_label": "🌐 Язык клиента",
    "claim_btn": "🛠️ Взять в работу",
    "ticket_claimed_admin": "🔒 **Тикет взял в работу:** @{admin_username}",
    "ticket_claimed_admin_auto": "🔒 **Тикет взял в работу (авто):** @{admin_username}",
    "ticket_fixed_toast": "Тикет зафиксирован!",
    "err_read_msg": "❌ Не удалось прочитать данные исходного сообщения.",
    "err_no_id": "❌ Не могу найти ID пользователя в этом сообщении.",
    "sent_success": "✅ Отправлено",
    "err_send_reply": "❌ Не удалось отправить ответ. Ошибка: {error}"
}