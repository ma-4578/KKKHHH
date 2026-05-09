import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = (
        "✨ **Bot Help Menu (အသုံးပြုနည်း)** ✨\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        
        "👫 **General Features:**\n"
        "• `/couple` - Group ထဲက ကံထူးရှင် အတွဲလေးကို ရွေးပေးမှာပါ။\n"
        "• `/happy` - စိတ်ညစ်နေရင် ဟာသနဲ့ အားပေးစာလေးတွေ ပို့ပေးမှာပါ။\n"
        "• `/tr` [စာသား] - ဘယ်ဘာသာစကားမဆို မြန်မာလို ပြန်ပေးမှာပါ။\n"
        "• `/love` - အချစ်ရေး ကံစမ်းဟောကြားပေးမှာပါ။\n"
        "• `/id` - မိမိရဲ့ Telegram User ID ကို ကြည့်ရန်။\n"
        
        "👮 **Admin & Safety:**\n"
        "• **Welcome** - Group ထဲ လူအသစ်ဝင်ရင် Auto ကြိုဆိုပေးမှာပါ။\n"
        "• **Anti-Spam** - Link တွေ၊ Forward တွေ အများကြီးပို့ရင် Auto Mute ပေးမှာပါ။\n"
        "• `/all` - Group Member အားလုံးကို Tag ခေါ်ပေးမှာပါ။\n"        
        "━━━━━━━━━━━━━━━━━━━━"
    )

    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Add Me To Your Group ➕", url=f"https://t.me/{client.me.username}?startgroup=true")
        ]
    ])

    await message.reply_text(help_text, reply_markup=buttons)
