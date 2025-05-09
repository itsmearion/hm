from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.start import register_start_handler
from handlers.callbacks import register_callback_handlers
from handlers.forward import register_forward_handlers

app = Client("Lamlucu", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Registrasi semua handler
register_start_handler(app)
register_callback_handlers(app)
register_forward_handlers(app)

# Menjalankan bot
app.run()
