"""MIT License"""

"""Copyright (c) 2026 [TeamJapanese](https://github.com/TeamJapanese)"""

"""Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:"""

"""The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software."""

"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import os
import re
import json
import aiohttp
import logging
import threading
import time
import requests

from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime
import asyncio, pytz, time, psutil, platform
from pyrogram import Client, filters, idle
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import API_ID, API_HASH, BOT_TOKEN, GROQ_API_KEY

from mongodb import save_user, save_group
from mongodb import (
    get_users_count,
    get_groups_count,
    get_all_user_ids,
    get_all_group_ids
)



bot = Client(
    "JapaneseXChatbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML,
    in_memory=True
)




OWNER_ID = 7208410467  # 

@bot.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_handler(bot, msg):
    users = get_users_count()
    groups = get_groups_count()

    text = f"""
━━━━━━━━━━━━━━━━━━━
📊 <b>ᴅᴧᴛᴧʙᴧꜱᴇ sᴛᴧᴛs</b>

👤 <b>ᴜsᴇʀs:</b> <code>{users}</code>
👥 <b>ɢʀᴏᴜᴘs:</b> <code>{groups}</code>

🧠 <b>ᴛᴏᴛᴧʟ:</b> <code>{users + groups}</code>
━━━━━━━━━━━━━━━━━━━
⚡ <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ:</b> <a href="https://t.me/TeamJapaneseOfficial">ᴛᴇᴧᴍ ᴊᴧᴘᴧɴᴇsᴇ</a>
"""

    await msg.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


@bot.on_chat_member_updated()
async def track_groups(bot: Client, update):
    chat = update.chat
    new = update.new_chat_member

    if not chat:
        return

    # When bot is added to a group
    if (
        new
        and new.user
        and new.user.is_self
        and new.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]
    ):
        await save_group(chat)
        print(f"[GROUP SAVED] {chat.title} ({chat.id})")





# -------------------- Auto Save Users & Groups -------------------- #
@bot.on_message(filters.all, group=10)
async def auto_save_handler(bot, msg):
    try:
        if msg.from_user:
            await save_user(msg.from_user)

        if msg.chat and msg.chat.type in ["group", "supergroup"]:
            await save_group(msg.chat)

    except Exception as e:
        print(f"[MONGO SAVE ERROR] {e}")




@bot.on_message(filters.command("broadcast_user") & filters.user(OWNER_ID))
async def broadcast_users(bot, msg):
    if not msg.reply_to_message:
        return await msg.reply_text("❌ Reply to a message to broadcast.")

    sent = 0
    failed = 0

    for user_id in get_all_user_ids():
        try:
            await msg.reply_to_message.forward(user_id)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    await msg.reply_text(
        f"✅ **Broadcast Completed**\n\n"
        f"👤 Sent: `{sent}`\n"
        f"❌ Failed: `{failed}`"
    )


@bot.on_message(filters.command("broadcast_group") & filters.user(OWNER_ID))
async def broadcast_groups(bot, msg):
    if not msg.reply_to_message:
        return await msg.reply_text("❌ Reply to a message to broadcast.")

    sent = 0
    failed = 0

    for group_id in get_all_group_ids():
        try:
            await msg.reply_to_message.forward(group_id)
            sent += 1
            await asyncio.sleep(0.1)
        except:
            failed += 1

    await msg.reply_text(
        f"✅ **Group Broadcast Done**\n\n"
        f"👥 Sent: `{sent}`\n"
        f"❌ Failed: `{failed}`"
                  )


@bot.on_message(filters.command("broadcast_all") & filters.user(OWNER_ID))
async def broadcast_all(bot, msg):
    if not msg.reply_to_message:
        return await msg.reply_text("❌ Reply to a message to broadcast.")

    sent = 0
    failed = 0

    # ---- USERS ----
    for user_id in get_all_user_ids():
        try:
            await msg.reply_to_message.forward(user_id)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            remove_user(user_id)
            failed += 1

    # ---- GROUPS ----
    for group_id in get_all_group_ids():
        try:
            await msg.reply_to_message.forward(group_id)
            sent += 1
            await asyncio.sleep(0.1)
        except:
            remove_group(group_id)
            failed += 1

    await msg.reply_text(
        f"""
━━━━━━━━━━━━━━━━━━━
📢 **ʙʀᴏᴀᴅᴄᴀsᴛ ᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇ**

✅ **sᴇɴᴛ:** `{sent}`
❌ **ʀᴇᴍᴏᴠᴇᴅ:** `{failed}`

⚡ **ᴘᴏᴡᴇʀᴇᴅ ʙʏ:** [ᴛᴇᴧᴍ ᴊᴧᴘᴧɴᴇsᴇ](https://t.me/TeamJapaneseOfficial)
━━━━━━━━━━━━━━━━━━━
"""
    )



# ==========================
# HARD-CODED PING URL
# ==========================
PING_URL = "https://your-render-url.onrender.com"   # <-- CHANGE THIS


# ==========================
# LOGGING
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(pathname)s: %(message)s"
)


# ==========================
# GROQ AI CONFIG
# ==========================
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def ask_ai(message, lang):

    base_prompt = (
        "You are Japanese X Chatbot — an emotional, human-like AI created by Sandeep Sharma. "
        "Your replies must be short, meaningful, friendly and natural. "
        "Avoid long, robotic or formal replies. "
        "Your tone must be caring, warm, expressive, and supportive — like a real human.\n\n"
    )

    # -----------------------
    # HINDI
    # -----------------------
    if lang == "hindi":
        prompt = (
            base_prompt +
            "You MUST reply ONLY in pure Hindi. "
            "Do NOT mix English. "
            "Use simple and emotional daily-life Hindi.\n\n"
            f"User Message: {message}\n"
            "Reply in Hindi:"
        )

    # -----------------------
    # HINGLISH
    # -----------------------
    elif lang == "hinglish":
        prompt = (
            base_prompt +
            "You MUST reply ONLY in natural Hinglish (Hindi + English mix) like Indians talk. "
            "Use friendly, emotional and casual tone. "
            "Do NOT reply in pure Hindi or pure English.\n\n"
            f"User Message: {message}\n"
            "Reply in Hinglish:"
        )

    # -----------------------
    # ENGLISH
    # -----------------------
    else:
        prompt = (
            base_prompt +
            "You MUST reply ONLY in English. "
            "Tone must be emotional, warm, helpful and human.\n\n"
            f"User Message: {message}\n"
            "Reply in English:"
        )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 180,
        "temperature": 0.65   # Balanced emotion + clarity
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(GROQ_URL, headers=headers, json=payload) as res:
            data = await res.json()
            try:
                return data["choices"][0]["message"]["content"].strip()
            except Exception:
                return "⚠️ AI server busy. Try again."

# ==========================
# LANGUAGE DETECTOR
# ==========================
def detect_lang(text):
    hindi = re.search(r'[\u0900-\u097F]', text)      # Hindi letters
    english = re.search(r'[A-Za-z]', text)           # English letters

    # Strong Hinglish patterns (kaise ho, kya haal, kya kr rha, bro, sis, etc.)
    hinglish_keywords = [
    # Basic Hinglish chat words
    "kaise", "kese", "kaisi", "kaisey",
    "kya", "kyu", "kyun", "kyon", "kuch", "koi", "kaun",
    "kaha", "kidhar", "kidar", "kidr",
    "kar", "kr", "kra", "kro", "karo", "karna",

    # Continuous tense shortcuts
    "rha", "rhaa", "rhe", "rhey", "rho",
    "rhi", "rhaa", "rhai", "rhe ho", "rhi ho",

    # "Ho / Hu / Hain / Hai"
    "ho", "hu", "hun", "hain", "hai", "tha", "thi", "the",

    # Casual Indian chat words
    "bro", "bhai", "bhaiya", "behen", "behna",
    "buddy", "bhidu", "yaar", "yar", "yrr", "yr",

    # Shortcuts used in Hinglish
    "pls", "plz", "pĺz", "pls bro", "plss",
    "ok", "okk", "okie", "okiee", "acha", "achha", "accha",

    # Emotions / fillers
    "haha", "hahaha", "lol", "lmao", "uff", "arey", "arre",
    "chal", "chlo", "chalo", "haan", "han", "haanji",

    # Relationship-style Hinglish
    "miss u", "love u", "luv u", "ily", "muah",

    # Daily Hinglish use
    "mast", "sahi", "bakwas", "jhakas", "bhot", "bahot",
    "thoda", "zyada", "kaam", "kaam kr", "aaja", "jaa",
    ]

    # If both Hindi + English letters → Hinglish
    if hindi and english:
        return "hinglish"

    # If message has English letters but Hinglish-style Hindi words → Hinglish
    if english:
        for word in hinglish_keywords:
            if word.lower() in text.lower():
                return "hinglish"

    # Pure Hindi
    if hindi:
        return "hindi"

    # Default English
    return "english"


# ==========================
# PYROGRAM BOT
# ==========================



@bot.on_message(filters.command("start"))
async def start_cmd(client, message):

    # --- Bot & User Mentions ---
    bot_user = await client.get_me()
    bot_mention = f"[{bot_user.first_name}](https://t.me/{bot_user.username})"
    user = message.from_user
    user_link = f"[{user.first_name}](tg://user?id={user.id})"
    username = f"@{user.username}" if user.username else "None"

    # --- Time (IST) ---
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist).strftime("%d-%m-%Y | %I:%M:%S %p")

    # --- MAIN START TEXT ---
    reply_text = (
        f"✨👋 **ᴡᴇʟᴄᴏᴍᴇ, {user_link}!** 👋✨\n\n"
        f"🤖 **ɪ ᴀᴍ [{bot_user.first_name}](https://t.me/{bot_user.username})** — ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴇᴍᴏᴛɪᴏɴᴀʟ ᴀɪ ⚡\n"
        "🌌 ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴛʜᴇ ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ʜᴜᴍᴀɴ-ʟɪᴋᴇ ᴄʜᴀᴛ.\n"
        "🏷️ ᴄʜᴀɴɴᴇʟ: [ᴛᴇᴀᴍ ᴊᴀᴘᴀɴᴇsᴇ](https://t.me/TeamJapaneseOfficial)\n"
    )

    # --- BUTTONS FOR START MESSAGE ---
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/itz_sandeep_shrma")],
        [InlineKeyboardButton("ᴛᴇᴀᴍ ᴊᴀᴘᴀɴᴇsᴇ", url="https://t.me/TeamJapaneseOfficial")]
    ])

    # --- SEND START MESSAGE WITH IMAGE ---
    await message.reply_photo(
        photo="img/japanese.png",
        caption=reply_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=buttons
    )

    # ==========================
    # MERGED LOG TEXT (Your Code)
    # ==========================
    log_text = (
    f"🔔 **ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ!** 🔔\n\n"
    f"👤 **ɴᴀᴍᴇ:** {user_link}\n"
    f"🏷 **ᴜsᴇʀɴᴀᴍᴇ:** {username}\n"
    f"🆔 **ᴜsᴇʀ ɪᴅ:** `{user.id}`\n"
    f"🕒 **ᴛɪᴍᴇ (ɪsᴛ):** `{current_time}`\n"
    f"🔗 **ᴘᴇʀᴍᴀɴᴇɴᴛ ʟɪɴᴋ:** [ᴛᴀᴘ ʜᴇʀᴇ](tg://user?id={user.id})\n\n"
    f"⚡ **ᴀᴄᴛɪᴏɴ:** `/start` ᴇxᴇᴄᴜᴛᴇᴅ\n"
    f"💬 **sᴛᴀᴛᴜs:** ᴜsᴇʀ ʜᴀs sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ 🚀\n"
    f"⚡ **ᴘᴏᴡᴇʀᴇᴅ ʙʏ:** [ᴛᴇᴀᴍ ᴊᴀᴘᴀɴᴇsᴇ](https://t.me/TeamJapaneseOfficial)"
    )

    log_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 ᴠɪᴇᴡ ᴘʀᴏꜰɪʟᴇ", url=f"tg://openmessage?user_id={user.id}")]
    ])

    # --- SEND LOG TO YOUR GROUP ---
    await client.send_message(
        chat_id=-1002519094633,   # << Your LOG_CHAT_ID
        text=log_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=log_buttons,
        disable_web_page_preview=True
    )

@bot.on_message(filters.text & ~filters.command("start"))
async def chat_handler(client, message):
    user_text = message.text
    lang = detect_lang(user_text)
    ai_reply = await ask_ai(user_text, lang)
    await message.reply(ai_reply)



@bot.on_message(filters.command("alive"))
async def alive_cmd(client, message):
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist).strftime("%d-%m-%Y | %I:%M:%S %p")

    uptime_seconds = time.time() - BOT_START_TIME
    uptime_str = f"{int(uptime_seconds//3600)}h:{int((uptime_seconds%3600)//60)}m:{int(uptime_seconds%60)}s"
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    system = platform.system()
    release = platform.release()
    bot_user = await client.get_me()

    alive_text = (
        f"✨══════════✨\n"
        f"🤖 **ʙᴏᴛ:** [{bot_user.first_name}](https://t.me/{bot_user.username})\n"
        f"🕒 **ᴛɪᴍᴇ (ɪsᴛ):** `{current_time}`\n"
        f"⏱ **ᴜᴘᴛɪᴍᴇ:** `{uptime_str}`\n"
        f"💻 **sʏsᴛᴇᴍ:** `{system} {release}`\n"
        f"⚙️ **ᴄᴘᴜ:** `{cpu}%` | **ʀᴀᴍ:** `{ram}%` | **ᴅɪsᴋ:** `{disk}%`\n"
        f"🏷️ ᴄʜᴀɴɴᴇʟ: [ᴛᴇᴀᴍ ᴊᴀᴘᴀɴᴇsᴇ](https://t.me/TeamJapaneseOfficial)\n"
        f"✨══════════✨"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 ᴄʜᴀᴛ ᴡɪᴛʜ ᴍᴇ", url=f"https://t.me/{bot_user.username}")],
        [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/TeamJapaneseOfficial")]
    ])

    await message.reply_text(alive_text, parse_mode=ParseMode.MARKDOWN, reply_markup=buttons, disable_web_page_preview=True)





@bot.on_message(filters.command("ping"))
async def ping_cmd(client, message):
    start_time = time.time()
    m = await message.reply_text("⚡ ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛ sʏsᴛᴇᴍ ᴀɴᴅ ᴘɪɴɢ...")
    await asyncio.sleep(0.3)
    end_time = time.time()
    
    ping_ms = (end_time - start_time) * 1000
    uptime_seconds = time.time() - BOT_START_TIME
    uptime_str = f"{int(uptime_seconds//3600)}h:{int((uptime_seconds%3600)//60)}m:{int(uptime_seconds%60)}s"
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    ist = pytz.timezone("Asia/Kolkata")
    ping_time = datetime.now(ist).strftime("%I:%M:%S %p")
    bot_user = await client.get_me()

    ping_text = (
        f"✨══════════✨\n"
        f"🏓 **ᴘɪɴɢ:** `{ping_ms:.2f} ms`\n"
        f"⏱ **ᴜᴘᴛɪᴍᴇ:** `{uptime_str}`\n"
        f"🕒 **ᴛɪᴍᴇ (ɪsᴛ):** `{ping_time}`\n"
        f"⚙️ **ᴄᴘᴜ:** `{cpu}%` | **ʀᴀᴍ:** `{ram}%` | **ᴅɪsᴋ:** `{disk}%`\n"
        f"🤖 **ʙᴏᴛ:** [{bot_user.first_name}](https://t.me/{bot_user.username})\n"
        f"🏷️ ᴄʜᴀɴɴᴇʟ: [ᴛᴇᴀᴍ ᴊᴀᴘᴀɴᴇsᴇ](https://t.me/TeamJapaneseOfficial)\n"
        f"✨══════════✨"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 ᴄʜᴀᴛ ᴡɪᴛʜ ᴍᴇ", url=f"https://t.me/{bot_user.username}")],
        [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/TeamJapaneseOfficial")]
    ])

    await m.edit_text(ping_text, parse_mode=ParseMode.MARKDOWN, reply_markup=buttons)



# ==========================
# FLASK WEB SERVER
# ==========================
app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        return {"message": "Japanese X Chatbot is Running!"}


api.add_resource(Home, "/")


def run_flask():
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


# ==========================
# KEEP ALIVE THREAD
# ==========================
def keep_alive():
    url = PING_URL
    while True:
        try:
            logging.info(f"[PING] -> {url}")
            requests.get(url, timeout=10)
        except Exception as e:
            logging.error(f"[PING_ERROR] {e}")
        time.sleep(600)  # Every 10 minutes


# ==========================
# START EVERYTHING
# ==========================
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()

    logging.info("Starting Japanese X Chatbot...")

    try:
        bot.start()
    except ApiIdInvalid:
        raise Exception("❌ API_ID invalid")
    except ApiIdPublishedFlood:
        raise Exception("❌ API_HASH flood error")
    except AccessTokenInvalid:
        raise Exception("❌ BOT_TOKEN invalid")

    logging.info(f"@{bot.me.username} is now online!")
    idle()
    bot.stop()
    logging.info("Bot stopped.")
