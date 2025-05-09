from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.format_menu import FORMAT_LIST

def register_callback_handlers(app: Client):
    # Menampilkan menu format ketika tombol "Format Order" diklik
    @app.on_callback_query(filters.regex("show_format_menu"))
    async def show_format_menu(_, cb: CallbackQuery):
        try:
            buttons = [
                [InlineKeyboardButton(data["label"], callback_data=f"format_{key}")]
                for key, data in FORMAT_LIST.items()
            ]
            buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_menu")])
            await cb.message.edit_text("Pilih salah satu format order:", reply_markup=InlineKeyboardMarkup(buttons))
            # Acknowledge the callback query
            await cb.answer()
        except Exception as e:
            await cb.answer(f"Error: {str(e)}", show_alert=True)

    # Menampilkan format spesifik ketika tombol format tertentu diklik
    @app.on_callback_query(filters.regex("^format_"))
    async def show_format_detail(_, cb: CallbackQuery):
        try:
            key = cb.data.split("_", 1)[1]
            if key in FORMAT_LIST:
                text = FORMAT_LIST[key]["text"]
                buttons = [
                    [InlineKeyboardButton("⬅️ Back", callback_data="show_format_menu")]
                ]
                await cb.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
                await cb.answer()
            else:
                await cb.answer(f"Format '{key}' tidak ditemukan", show_alert=True)
        except Exception as e:
            await cb.answer(f"Error: {str(e)}", show_alert=True)

    # Menutup menu ketika tombol "Close" diklik
    @app.on_callback_query(filters.regex("close_menu"))
    async def close_menu(_, cb: CallbackQuery):
        try:
            await cb.message.delete()
            await cb.answer()
        except Exception as e:
            await cb.answer(f"Error: {str(e)}", show_alert=True)
            
    # Catch-all untuk callback query yang tidak dikenali
    @app.on_callback_query(group=1)
    async def unknown_callback(_, cb: CallbackQuery):
        if not any(handler_filter(cb) for handler_filter in [
            filters.regex("show_format_menu"),
            filters.regex("^format_"),
            filters.regex("close_menu")
        ]):
            await cb.answer("Perintah tidak dikenali", show_alert=True)