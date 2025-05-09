from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

def register_start_handler(app: Client):
    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(client, message: Message):
        try:
            # Kirim pesan selamat datang
            welcome = await message.reply_text("Halo! Selamat datang di toko kami.")
            
            # Tunggu 2 detik
            await asyncio.sleep(2)
            
            # Hapus pesan selamat datang
            try:
                await welcome.delete()
            except Exception as e:
                print(f"Error deleting welcome message: {str(e)}")
            
            # Menampilkan tombol "Format Order"
            await message.reply_text(
                "Klik tombol di bawah untuk melihat format order atau menghubungi owner:",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Format Order", callback_data="show_format_menu"),
                            InlineKeyboardButton("Owner", url="https://t.me/ampuv")
                        ]
                    ]
                )
            )
        except Exception as e:
            print(f"Error in start command: {str(e)}")
            await message.reply_text("Terjadi kesalahan. Silakan coba lagi nanti.")