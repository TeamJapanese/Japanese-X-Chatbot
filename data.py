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


from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Data:
    # -------------------- INLINE BUTTONS -------------------- #
    start_buttons = [
        [
            InlineKeyboardButton("ᴛᴇᴀᴍ ᴊᴀᴘᴀɴᴇsᴇ", url="https://t.me/TeamJapaneseOfficial")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/itz_sandeep_shrma")
        ]
    ]


    # -------------------- MESSAGES -------------------- #
    START = """
✨ **ʜᴇʟʟᴏ, {}!**
ɪ ᴀᴍ **{}** 🤍  
ɪ ʀᴇᴘʟʏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ɪɴ ʜɪɴᴅɪ, ᴇɴɢʟɪsʜ, ᴏʀ ʜɪɴɢʟɪsʜ.

💡 **ᴛɪᴘ:** ᴛʏᴘᴇ ᴀɴʏᴛʜɪɴɢ ᴛᴏ sᴛᴀʀᴛ ᴄʜᴀᴛᴛɪɴɢ!

⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ **[ᴛᴇᴀᴍ ᴊᴀᴘᴀɴᴇsᴇ](https://t.me/TeamJapaneseOfficial)**
"""


    HELP = """
📘 **ʜᴇʀᴇ ᴀʀᴇ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs:**  

━━━━━━━━━━━━━━━━━━━━━━━
**/start** — sᴛᴀʀᴛ ᴛʜᴇ ᴄʜᴀᴛʙᴏᴛ  
**/help** — ᴅɪsᴘʟᴀʏ ᴛʜɪs ᴍᴇɴᴜ  
**/about** — ʟᴇᴀʀɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ʙᴏᴛ  
**/alive** — ᴄʜᴇᴄᴋ ɪꜰ ʙᴏᴛ ɪs ᴏɴʟɪɴᴇ  
**/ping** — ᴄʜᴇᴄᴋ ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ  
━━━━━━━━━━━━━━━━━━━━━━━
💡 *ᴛɪᴘ:* ᴜsᴇ ʙᴜᴛᴛᴏɴs ᴏɴ ᴍᴇssᴀɢᴇ ᴛᴏ ɪɴᴛᴇʀᴀᴄᴛ ꜰᴀsᴛᴇʀ ⚡
    """

    ABOUT = """
💫 **ᴀʙᴏᴜᴛ ᴊᴀᴘᴀɴᴇsᴇ x ᴄʜᴀᴛʙᴏᴛ**  

ɪ ᴀᴍ ᴀ ʜᴜᴍᴀɴ-ʟɪᴋᴇ ᴇᴍᴏᴛɪᴏɴᴀʟ ᴄʜᴀᴛʙᴏᴛ.  
ᴛʀɪᴇs ᴛᴏ ʀᴇᴘʟʏ ɪɴ ᴇɴɢʟɪsʜ, ʜɪɴᴅɪ, ᴀɴᴅ ʜɪɴɢʟɪsʜ.  

🌸 ɢᴇᴛ ᴄᴀʀɪɴɢ ᴀɴᴅ ᴇᴍᴏᴛɪᴏɴᴀʟ ʀᴇᴘʟɪᴇs ᴏɴ ʏᴏᴜʀ ᴍᴇssᴀɢᴇs.  

👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: [sᴧɴᴅᴇᴇᴘ sʜᴧʀᴍᴧ](https://t.me/itz_sandeep_shrma)  
⚡ ᴛᴇᴀᴍ ᴊᴀᴘᴀɴᴇsᴇ: [ᴄʜᴀɴɴᴇʟ](https://t.me/TeamJapaneseOfficial)
    """
