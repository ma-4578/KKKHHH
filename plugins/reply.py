import os
from pyrogram import Client, filters
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient

# --- Database Setup (တိုက်ရိုက်ချိတ်ဆက်ခြင်း) ---
# bot.py က db ကို မသုံးတော့ဘဲ ဒီမှာတင် တန်းချိတ်လိုက်ပါမယ်
MONGO_URL = os.environ.get("MONGO_URL", "")
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["Khh_db"] 
replies = db["auto_replies"]

#
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

@Client.on_message(filters.group & ~filters.bot)
async def auto_learn_and_reply(client: Client, message: Message):
    # --- ၁။ Auto Learning (စာသင်ယူခြင်း) ---
    if message.reply_to_message:
        reply_to = message.reply_to_message
        
        trigger = None
        trigger_type = None
        
        if reply_to.text:
            trigger = reply_to.text.lower().strip()
            trigger_type = "text"
        elif reply_to.sticker:
            trigger = reply_to.sticker.file_unique_id
            trigger_type = "sticker"

        if trigger:
            reply_data = message.text if message.text else (message.sticker.file_id if message.sticker else None)
            reply_type = "text" if message.text else ("sticker" if message.sticker else None)

            if reply_data:
                # အမေးစာရှိပြီးသားဆိုရင် Update လုပ်မယ်၊ မရှိရင် အသစ်ထည့်မယ်
                await replies.update_one(
                    {"trigger": trigger},
                    {"$set": {
                        "trigger_type": trigger_type,
                        "reply": reply_data,
                        "reply_type": reply_type
                    }},
                    upsert=True
                )

    # --- ၂။ Auto Reply (ပြန်ဖြေခြင်း) ---
    else:
        current_trigger = None
        if message.text:
            current_trigger = message.text.lower().strip()
        elif message.sticker:
            current_trigger = message.sticker.file_unique_id

        if current_trigger:
            found = await replies.find_one({"trigger": current_trigger})
            if found:
                if found["reply_type"] == "text":
                    await message.reply_text(found["reply"])
                else:
                    await message.reply_sticker(found["reply"])

# --- ၃။ Delete Command (Owner သီးသန့်) ---
@Client.on_message(filters.command("del"))
async def delete_reply(client: Client, message: Message):
    # Owner ID စစ်ဆေးခြင်း
    if message.from_user.id != OWNER_ID:
        return 

    if not message.reply_to_message:
        return await message.reply_text("❌ ဖျက်ချင်တဲ့ အမေးစာကို Reply ပြန်ပြီး `/del` လို့ ရိုက်ပါ။")

    reply_to = message.reply_to_message
    trigger_to_del = reply_to.text.lower().strip() if reply_to.text else (reply_to.sticker.file_unique_id if reply_to.sticker else None)

    if trigger_to_del:
        result = await replies.delete_many({"trigger": trigger_to_del})
        if result.deleted_count > 0:
            await message.reply_text(f"🗑️ '{trigger_to_del}' အတွက် အဖြေကို Database ထဲက ဖျက်လိုက်ပါပြီ။")
        else:
            await message.reply_text("❌ ဒီစာသားအတွက် မှတ်ထားတဲ့ အဖြေမရှိပါဘူး။")
