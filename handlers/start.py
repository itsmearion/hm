from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

def register_start_handler(app: Client):
    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(client, message: Message):
        welcome = await message.reply_text("Halo! Selamat datang di toko kami.")
        await asyncio.sleep(2)
        await welcome.delete()

        # Menampilkan tombol "Format Order"
        await message.reply_text(
    "Klik tombol di bawah untuk melihat format order atau menghubungi owner:",
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Format Order", callback_data="show_format_menu"),
                InlineKeyboardButton("Owner", url="https://t.me/ampuv")  # Ganti URL jika perlu
            ]
        ]
    )
)
