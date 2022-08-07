# (c) @EverythingSuckz | @AbirHasan2005 | @PredatorHackerzZ

import asyncio
from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio) & filters.user(Var.OWNER_ID) & ~filters.edited, group=4)
async def private_receive_handler(c: Client, m: Message):
    
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = "https://{}/{}".format(Var.FQDN, log_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                    Var.PORT,
                                    log_msg.message_id)
        file_size = None
        if m.video:
            file_size = f"{humanbytes(m.video.file_size)}"
        elif m.document:
            file_size = f"{humanbytes(m.document.file_size)}"
        elif m.audio:
            file_size = f"{humanbytes(m.audio.file_size)}"

        file_name = None
        if m.video:
            file_name = f"{m.video.file_name}"
        elif m.document:
            file_name = f"{m.document.file_name}"
        elif m.audio:
            file_name = f"{m.audio.file_name}"

        msg_text = "**Your Link Generated!** 🤓\n\n📂 **File Name:** `{}`\n\n📦**File Size:** `{}`\n\n📥 **Download Link:** `{}`\n\n🚸 Nᴏᴛᴇ : Tʜɪs ᴘᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ, Nᴏᴛ Exᴘɪʀᴇᴅ\n\n© @TheTeleRoid"
        await log_msg.reply_text(text=f"Requested by [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**User ID:** `{m.from_user.id}`\n**Download Link:** {stream_link}\n\n🚸 @TheTeleRoid", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Download Now", url=stream_link)]]),
            quote=True
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Got FloodWait of {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n👤**User ID:** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode="Markdown")

