# Project: Telegram Support Bot
# Path: core/utils/locales/en.py

messages = {
    # Client-side strings
    "welcome": (
        "👋 Hello! This is the official **Titan Cloud Tech** support bot.\n\n"
        "Please describe your issue, send a screenshot or a file directly to this chat, "
        "and our specialists will reply to you shortly."
    ),
    "ticket_delivered": "🚀 Your message has been delivered to support!",
    "send_error": "⚠️ An error occurred while sending your message. Please try again later.",
    "ticket_claimed_client": "⏳ **Your request has been taken into work.** A specialist is already looking into the issue.",
    "support_reply_header": "💬 **Titan Cloud Support Reply:**",

    # Admin-side strings
    "new_ticket_title": "📩 **New Support Ticket**",
    "user_label": "👤 User",
    "id_label": "🆔 ID",
    "lang_label": "🌐 Language",
    "claim_btn": "🛠️ Claim Ticket",
    "ticket_claimed_admin": "🔒 **Ticket claimed by:** @{admin_username}",
    "ticket_claimed_admin_auto": "🔒 **Ticket claimed by (auto):** @{admin_username}",
    "ticket_fixed_toast": "Ticket claimed!",
    "err_read_msg": "❌ Failed to read original message.",
    "err_no_id": "❌ Cannot find user ID.",
    "sent_success": "✅ Sent",
    "err_send_reply": "❌ Failed to send reply. Error: {error}"
}