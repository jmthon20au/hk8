from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio

# ضع هنا API ID و API HASH الخاصين بحسابك
api_id = 24484469  # غيّر هذا إلى API ID الخاص بك
api_hash = 'f864ff1bb135fe7faa895d260ce57ba9'  # غيّر هذا إلى API HASH الخاص بك

async def main():
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        print("🔑 سجل دخولك الآن...")
        await client.send_message('me', '📤 جاري استخراج كود الجلسة...')

        session_str = client.session.save()

        # تقسيم الكود الطويل إلى أجزاء إذا كان أطول من الحد المسموح
        max_length = 4096
        if len(session_str) <= max_length:
            await client.send_message('me', f'✅ كود الجلسة:\n\n`{session_str}`')
        else:
            await client.send_message('me', '⚠️ الكود طويل، سيتم إرساله على أجزاء:')
            parts = [session_str[i:i+max_length] for i in range(0, len(session_str), max_length)]
            for i, part in enumerate(parts, 1):
                await client.send_message('me', f'📦 جزء {i}:\n\n`{part}`')

        print("✅ تم إرسال كود الجلسة في الرسائل المحفوظة.")

asyncio.run(main())