from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

# Ganti dengan ID grup admin kamu
ADMIN_GROUP_ID = -1001234567890

def register_forward_handlers(app: Client):
    @app.on_message(filters.private & ~filters.command("start"))
    async def forward_user_message(client: Client, message: Message):
        fwd = await message.forward(ADMIN_GROUP_ID)
        await client.send_message(
            ADMIN_GROUP_ID,
            f"#balas_{message.chat.id}_{message.message_id}",
            reply_to_message_id=fwd.id
        )

        # Hapus pesan user setelah 7 menit
        await asyncio.sleep(420)
        await message.delete()

    @app.on_message(filters.group & filters.reply)
    async def reply_from_admin(client: Client, message: Message):
        if message.text and message.reply_to_message:
            try:
                tag_msg = await message.chat.get_messages(message.reply_to_message.id + 1)
                if tag_msg.text.startswith("#balas_"):
                    parts = tag_msg.text.split("_")
                    user_id = int(parts[1])
                    user_msg_id = int(parts[2])
                    await client.send_message(user_id, message.text)

                    # Hapus balasan admin setelah 7 menit
                    await asyncio.sleep(420)
                    await message.delete()
            except Exception as e:
                print("Gagal membalas:", e)
