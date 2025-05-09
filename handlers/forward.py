from pyrogram import Client, filters
from pyrogram.types import Message, ChatAction
import asyncio
import re
import time

# Ganti dengan ID grup admin kamu
ADMIN_GROUP_ID = -1001234567890

# Dictionary untuk melacak admin yang sedang mengetik
typing_admins = {}

def register_forward_handlers(app: Client):
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client: Client, message: Message):
        await message.reply_text(
            "Selamat datang! Silakan kirimkan pesan Anda dan admin akan segera membalas."
        )

    @app.on_message(filters.private & ~filters.command(["start", "typing"]))
    async def forward_user_message(client: Client, message: Message):
        try:
            # Forward pesan ke grup admin
            fwd = await message.forward(ADMIN_GROUP_ID)

            # Kirim tag referensi sebagai reply ke pesan yang diforward
            await client.send_message(
                ADMIN_GROUP_ID,
                f"#balas_{message.chat.id}_{message.id}\n\n"
                f"Untuk mengirim status 'mengetik...' ke pengguna, gunakan perintah:\n"
                f"/typing {message.chat.id}",
                reply_to_message_id=fwd.id
            )

            # Kirim konfirmasi ke pengguna
            await message.reply_text("Pesan Anda telah diteruskan ke admin. Mohon tunggu balasannya.")

            # Hapus pesan user setelah 7 menit
            await asyncio.sleep(420)
            try:
                await message.delete()
            except Exception as e:
                print(f"Gagal menghapus pesan pengguna: {e}")

        except Exception as e:
            print(f"Gagal meneruskan pesan: {e}")
            await message.reply_text("Maaf, terjadi kesalahan. Silakan coba lagi nanti.")

    # Handler untuk mendeteksi ketika admin mulai mengetik balasan
    @app.on_message(filters.chat(ADMIN_GROUP_ID) & filters.command("typing"))
    async def start_typing_indication(client: Client, message: Message):
        try:
            # Format: /typing user_id
            if len(message.command) != 2:
                await message.reply_text("Format: /typing [user_id]")
                return

            user_id = int(message.command[1])
            admin_id = message.from_user.id

            # Catat admin yang sedang mengetik
            typing_admins[admin_id] = {
                "user_id": user_id,
                "start_time": time.time()
            }

            # Kirim notifikasi "mengetik..." ke pengguna
            await client.send_chat_action(user_id, ChatAction.TYPING)
            await message.reply_text(f"✓ Status 'mengetik...' dikirim ke pengguna {user_id}")

            # Pertahankan status mengetik selama 30 detik (dapat disesuaikan)
            for _ in range(6):  # 6 x 5 detik = 30 detik
                await asyncio.sleep(5)
                # Periksa apakah admin masih dalam status mengetik
                if admin_id in typing_admins:
                    await client.send_chat_action(user_id, ChatAction.TYPING)
                else:
                    break

            # Hapus status mengetik setelah 30 detik
            if admin_id in typing_admins:
                del typing_admins[admin_id]

        except Exception as e:
            await message.reply_text(f"❌ Gagal mengirim status mengetik: {e}")

    @app.on_message(filters.chat(ADMIN_GROUP_ID) & filters.reply)
    async def reply_from_admin(client: Client, message: Message):
        if not message.text:
            return  # Abaikan jika bukan pesan teks

        try:
            # Cek apakah membalas pesan tag referensi
            replied_msg = message.reply_to_message
            if not replied_msg:
                return  # Tidak membalas pesan apapun

            # Cari pesan tag yang mungkin berada di thread balasan
            tag_pattern = r"#balas_(\d+)_(\d+)"
            
            # Periksa pesan yang dibalas
            user_id = None
            user_msg_id = None
            
            # Cek jika replied_msg adalah pesan yang diforward dari user
            if replied_msg.forward_from_chat or replied_msg.forward_sender_name:
                # Cari tag di pesan berikutnya
                next_messages = await client.get_messages(
                    ADMIN_GROUP_ID, 
                    replied_msg.id + 1,
                    limit=1
                )
                
                if next_messages and next_messages[0].text:
                    match = re.search(tag_pattern, next_messages[0].text)
                    if match:
                        user_id = int(match.group(1))
                        user_msg_id = int(match.group(2))
            
            # Jika belum menemukan, cek di pesan yang dibalas langsung
            if not user_id and replied_msg.text:
                match = re.search(tag_pattern, replied_msg.text)
                if match:
                    user_id = int(match.group(1))
                    user_msg_id = int(match.group(2))
            
            # Jika masih tidak ditemukan tag referensi
            if not user_id:
                await message.reply_text("❌ Tidak dapat menemukan referensi pengguna untuk dibalas.")
                return

            # Jika admin ini sedang dalam status mengetik untuk user ini, hapus status
            admin_id = message.from_user.id
            if admin_id in typing_admins and typing_admins[admin_id]["user_id"] == user_id:
                del typing_admins[admin_id]

            # Kirim balasan ke pengguna
            sent = await client.send_message(
                user_id, 
                message.text  # Kirim teks asli tanpa awalan
            )

            # Konfirmasi ke admin
            await message.reply_text(f"✅ Pesan berhasil dikirim ke pengguna.")

            # Hapus balasan admin setelah 7 menit (opsional)
            await asyncio.sleep(420)
            try:
                await message.delete()
            except Exception as e:
                print(f"Gagal menghapus pesan admin: {e}")

        except Exception as e:
            print(f"Gagal membalas: {e}")
            await message.reply_text(f"❌ Gagal mengirim pesan: {e}")