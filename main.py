from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
import logging
import asyncio
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        logging.FileHandler("bot.log")
    ]
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Inisialisasi client
        app = Client(
            "Lamlucu", 
            api_id=API_ID, 
            api_hash=API_HASH, 
            bot_token=BOT_TOKEN
        )
        
        # Import handlers (diletakkan di sini untuk menghindari circular import)
        from handlers.start import register_start_handler
        from handlers.callbacks import register_callback_handlers
        from handlers.forward import register_forward_handlers

        # Registrasi semua handler
        register_start_handler(app)
        register_callback_handlers(app)
        register_forward_handlers(app)
        
        # Mulai bot
        logger.info("Bot starting...")
        await app.start()
        logger.info("Bot started successfully!")
        
        # Tunggu hingga bot dihentikan
        await idle()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        # Pastikan bot berhenti dengan baik
        if 'app' in locals():
            await app.stop()
            logger.info("Bot stopped")

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Keyboard Interrupt)")