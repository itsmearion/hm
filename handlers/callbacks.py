from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.format_menu import FORMAT_LIST

def register_callback_handlers(app: Client):
    # Menampilkan menu format ketika tombol "Format Order" diklik
    @app.on_callback_query(filters.regex("show_format_menu"))
    async def show_format_menu(_, cb: CallbackQuery):
        buttons = [
            [InlineKeyboardButton(data["label"], callback_data=f"format_{key}")]
            for key, data in FORMAT_LIST.items()
        ]
        buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_menu")])
        await cb.message.edit_text("Pilih salah satu format order:", reply_markup=InlineKeyboardMarkup(buttons))

    # Menampilkan format spesifik ketika tombol format tertentu diklik
    @app.on_callback_query(filters.regex("^format_"))
    async def show_format_detail(_, cb: CallbackQuery):
        key = cb.data.split("_", 1)[1]
        if key in FORMAT_LIST:
            text = FORMAT_LIST[key]["text"]
            buttons = [
                [InlineKeyboardButton("⬅️ Back", callback_data="show_format_menu")]
            ]
            await cb.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))

    # Menutup menu ketika tombol "Close" diklik
    @app.on_callback_query(filters.regex("close_menu"))
    async def close_menu(_, cb: CallbackQuery):
        await cb.message.delete()
