from .glob_variables import BotState
from .buttons import Buttons
from utils import db, TweetCapture
from telethon.errors.rpcerrorlist import MessageNotModifiedError


class BotMessageHandler:
    start_message = """
**Musiqa Yuklab Olish** botiga xush kelibsiz! 🎧

Menga qo'shiq yoki ijrochi nomini yuboring, va men sizga yuklab olish mumkin bo'lgan trekni topaman va jo'nataman. 🎶

Mening imkoniyatlarimni ko'rish uchun: /help ni kiriting
Yoki quyidagi Ko'rsatmalar tugmasini bosing. 👇
"""

    instruction_message = """
🎧 Musiqa Yuklab Olish 🎧

1. Spotify/YouTube qo'shiq havolasini yuboring 🔗
2. Yuklab olish tasdiqini kuting 📣
3. Qo'shiq faylini oling 💾
4. Yoki qo'shiq namunasi bilan ovozli xabar jo'nating
   va eng yaxshi moslik va tafsilotlar uchun tekshirish 🎤🔍📩
5. Qo'shiq matni, ijrochi haqida ma'lumot va boshqalarni so'rang 📜👨‍🎤

💡 Maslahat: Nom, qo'shiq matni yoki boshqa tafsilotlar bo'yicha izlang!

📺 YouTube Yuklab Olish 📺

1. YouTube video havolasini yuboring 🔗
2. Video sifatini tanlang (agar so'ralsa) 🎥
3. Yuklab olishni kuting ⏳
4. Video faylini oling 📤

📸 Instagram Yuklab Olish 📸

1. Instagram post/Reel/IGTV havolasini yuboring 🔗
2. Yuklab olishni kuting ⏳
3. Faylni oling 📤

🐦 TweetCapture 🐦

1. Tweet havolasini kiriting 🔗
2. Screenshotni kuting 📸
3. Screenshotni oling 🖼️
4. Media kontenti uchun, "Media Yuklab Olish" 
   tugmasini screenshot olgandan so'ng foydalaning 📥

Savollar? @KhayitovdDev ga murojaat qiling
        """

    search_result_message = """🎵 Sizning so'rovingizga mos keladigan eng yaxshi qidiruv natijalari:
"""

    core_selection_message = """🎵 Yuklab olish uchun kerakli yadroni tanlang 🎵

"""
    JOIN_CHANNEL_MESSAGE = """Ko'rinib turibdiki, siz hali bizning kanalimizga a'zo emassiz.
Davom etish uchun iltimos, qo'shiling."""

    search_playlist_message = """PlayListda quyidagi qo'shiqlar mavjud:"""

    @staticmethod
    async def send_message(event, text, buttons=None):
        chat_id = event.chat_id
        user_id = event.sender_id
        await BotState.initialize_user_state(user_id)
        await BotState.BOT_CLIENT.send_message(chat_id, text, buttons=buttons)

    @staticmethod
    async def edit_message(event, message_text, buttons=None):
        user_id = event.sender_id

        await BotState.initialize_user_state(user_id)
        try:
            await event.edit(message_text, buttons=buttons)
        except MessageNotModifiedError:
            pass

    @staticmethod
    async def edit_quality_setting_message(e):
        music_quality = await db.get_user_music_quality(e.sender_id)
        if music_quality:
            message = (f"Sizning sifat sozlamalaringiz:\nFormat: {music_quality['format']}\nSifat: {music_quality['quality']}"
                       f"\n\nMavjud sifatlar:")
        else:
            message = "Hech qanday sifat sozlamalari topilmadi."
        await BotMessageHandler.edit_message(e, message, buttons=Buttons.get_quality_setting_buttons(music_quality))

    @staticmethod
    async def edit_core_setting_message(e):
        downloading_core = await db.get_user_downloading_core(e.sender_id)
        if downloading_core:
            message = BotMessageHandler.core_selection_message + f"\nYadro: {downloading_core}"
        else:
            message = BotMessageHandler.core_selection_message + "\nHech qanday yadro sozlamasi topilmadi."
        await BotMessageHandler.edit_message(e, message, buttons=Buttons.get_core_setting_buttons(downloading_core))

    @staticmethod
    async def edit_subscription_status_message(e):
        is_subscribed = await db.is_user_subscribed(e.sender_id)
        message = f"Obuna sozlamalari:\n\nSizning Obuna Holatingiz: {is_subscribed}"
        await BotMessageHandler.edit_message(e, message,
                                             buttons=Buttons.get_subscription_setting_buttons(is_subscribed))

    @staticmethod
    async def edit_tweet_capture_setting_message(e):
        night_mode = await TweetCapture.get_settings(e.sender_id)
        mode = night_mode['night_mode']
        mode_to_show = "Yorug'"
        match mode:
            case "1":
                mode_to_show = "Dark"
            case "2":
                mode_to_show = "Black"
        message = f"Tweet screenshot sozlamalari:\n\nSizning Tun Rejimingiz: {mode_to_show}"
        await BotMessageHandler.edit_message(e, message, buttons=Buttons.get_tweet_capture_setting_buttons(mode))
