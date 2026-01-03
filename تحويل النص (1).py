import telebot
from gtts import gTTS
import os

# توكن البوت
TOKEN = '8467223117:AAGxBLiYMQA6RFNmFcEyn1Th54kfenOZlX8'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 6454550864 # استبدل هذا بالآيدي الخاص بك لتلقي الإشعارات

# [تعديل] معلومات القناة للاشتراك الإجباري
# **تأكد من استبدال هذه القيم بآيدي قناتك الصحيح و username قناتك**
CHANNEL_ID = '-1002172915287' # آيدي القناة (يبدأ بـ -100)، ضروري للتحقق
CHANNEL_USERNAME = 'xx28z' # يوزر القناة بدون @، ضروري لإنشاء الرابط
CHANNEL_LINK = f'https://t.me/{CHANNEL_USERNAME}' # رابط القناة للمستخدمين

# الإعدادات الافتراضية
default_lang = 'ar'
default_speed = False

# قائمة اللغات المدعومة
SUPPORTED_LANGS = {
    'ar': 'العربية',
    'en': 'English',
    'fr': 'Français',
    'es': 'Español',
    'de': 'Deutsch',
    'it': 'Italiano',
    'tr': 'Türkçe',
    'zh-cn': '中文 (Mandarin)',
    'ja': '日本語',
    'ru': 'Русский',
    'hi': 'हिंदी'
}

# الإحصائيات
total_conversions = 0
unique_users = set()



# **[تعديل] التحقق من الاشتراك الإجباري**
def is_subscribed(user_id):
    try:
        # التحقق من حالة العضوية في القناة باستخدام الـ ID
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # إذا كان مشتركاً (عضو، مسؤول، مالك)، فهو OK
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False # غير مشترك (left) أو تم حظره (kicked)
    except Exception as e:
        # في حال حدوث خطأ (مثلاً البوت ليس مسؤولاً في القناة أو آيدي القناة خاطئ)
        print(f"Error checking subscription for channel {CHANNEL_ID}: {e}")
        return False # نعتبره غير مشترك لتجنب المشاكل

# ---

# مساعدة المستخدم
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global unique_users
    user_id = message.from_user.id
    unique_users.add(user_id)
    if user_id in banned_users:
        bot.send_message(message.chat.id, "🚫 عذرًا، لا يمكنك استخدام هذا البوت. لقد تم حظرك.")
        return
        
    if not is_subscribed(user_id):
        # إذا لم يكن مشتركاً، أرسل له رسالة الاشتراك الإجباري
        markup = telebot.types.InlineKeyboardMarkup()
        # زر يوجه المستخدم للقناة باستخدام الرابط
        subscribe_button = telebot.types.InlineKeyboardButton("اشترك في القناة", url=CHANNEL_LINK)
        # زر يسمح للمستخدم بالتحقق بعد الاشتراك
        check_button = telebot.types.InlineKeyboardButton("✔️ لقد اشتركت", callback_data="check_subscription")
        markup.add(subscribe_button, check_button)
        bot.send_message(message.chat.id,
                         "✋ **مرحباً بك! لاستخدام البوت، يجب عليك الاشتراك في قناتنا أولاً.**\n\n"
                         "اضغط على الزر أدناه للاشتراك، ثم اضغط 'لقد اشتركت' للمتابعة.",
                         reply_markup=markup, parse_mode="Markdown")
        return # توقف هنا، لا تكمل تنفيذ أمر /start

    # [بقية كود دالة send_welcome إذا كان مشتركاً]
    bot.reply_to(message, """
🎙️ **بوت تحويل النص إلى صوت!**

🛠️ **الأوامر المتاحة:**

🌐 **اللغة:** /lang [رمز اللغة] — لتغيير لغة الصوت (مثال: /lang en)
🌐 **قائمة اللغات:** /langs — لعرض جميع اللغات المدعومة
🎚️ **السرعة:** /speed [fast/slow] — لتغيير سرعة الصوت (مثال: /speed slow)

🎧 **تحويل النص:** أرسل أي نص، وسيتم تحويله إلى صوت!
    """, parse_mode="Markdown")

    # إرسال إشعار الدخول للمشرف
    first_name = message.from_user.first_name
    username = message.from_user.username

    # [التعديل هنا]
    # إنشاء رابط عميق لملف المستخدم
    user_profile_link = f"tg://user?id={user_id}"
    
    # تنسيق الاسم ليكون رابطاً قابلاً للضغط
    # نستخدم {first_name or 'لا يوجد'} لتجنب ظهور "None" إذا لم يكن هناك اسم
    linked_first_name = f"<a href='{user_profile_link}'>{first_name or 'لا يوجد'}</a>"

    notification_message = (
        f"🚨 <b>دخول مستخدم جديد!</b>\n\n"
        f"👤 <b>الاسم:</b> {linked_first_name}\n" # تم تعديل هذا السطر
        f"🆔 <b>الآيدي:</b> <code>{user_id}</code>\n"
        f"🔗 <b>اليوزر:</b> @{username or 'لا يوجد'}"
    )


    try:
        bot.send_message(ADMIN_ID, notification_message, parse_mode="HTML")
    except Exception as e:
        print(f"❌ خطأ في إرسال إشعار للمشرف: {e}")

# ---
banned_users = set()
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    parts = message.text.split(' ')
    if len(parts) > 1:
        try:
            user_to_ban_id = int(parts[1])
            if user_to_ban_id == ADMIN_ID:
                bot.reply_to(message, "لا يمكنك حظر نفسك يا مشرف!")
                return
            
            banned_users.add(user_to_ban_id)
            bot.reply_to(message, f"✅ تم حظر المستخدم: <code>{user_to_ban_id}</code>.", parse_mode="HTML")
            try:
                bot.send_message(user_to_ban_id, "🚫 لقد تم حظرك من استخدام هذا البوت.")
            except Exception:
                pass
        except ValueError:
            bot.reply_to(message, "❌ الرجاء إدخال آيدي مستخدم صحيح للحظر. مثال: /ban 123456789")
    else:
        bot.reply_to(message, "❌ الرجاء تحديد آيدي المستخدم المراد حظره. مثال: /ban 123456789")

# ---

# **أمر إلغاء حظر المستخدم (للمشرف فقط)**
@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    parts = message.text.split(' ')
    if len(parts) > 1:
        try:
            user_to_unban_id = int(parts[1])
            if user_to_unban_id in banned_users:
                banned_users.remove(user_to_unban_id)
                bot.reply_to(message, f"✅ تم إلغاء حظر المستخدم: <code>{user_to_unban_id}</code>.", parse_mode="HTML")
                try:
                    bot.send_message(user_to_unban_id, "✅ تم إلغاء حظرك. يمكنك الآن استخدام البوت.")
                except Exception:
                    pass
            else:
                bot.reply_to(message, f"❌ المستخدم <code>{user_to_unban_id}</code> ليس محظوراً حالياً.", parse_mode="HTML")
        except ValueError:
            bot.reply_to(message, "❌ الرجاء إدخال آيدي مستخدم صحيح لإلغاء الحظر. مثال: /unban 123456789")
    else:
        bot.reply_to(message, "❌ الرجاء تحديد آيدي المستخدم المراد إلغاء حظره. مثال: /unban 123456789")
# [تعديل] معالج لزر "لقد اشتركت" مع رسالة تأكيد
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_sub_callback(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        # [تعديل] رسالة التأكيد التلقائية بعد الاشتراك
        bot.answer_callback_query(call.id, "✅ شكراً لاشتراكك! يمكنك الآن استخدام البوت.", show_alert=True) # show_alert لإظهار الرسالة كـ pop-up
        
        # تعديل الرسالة الأصلية لتجنب ظهور زر "لقد اشتركت" مرة أخرى
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="✅ **تم التحقق من اشتراكك بنجاح!**\n\n"
                                   "يمكنك الآن استخدام البوت.\n"
                                   "أرسل /help لعرض الأوامر.",
                              parse_mode="Markdown")
        # لا نحتاج لاستدعاء send_welcome(call.message) مرة أخرى هنا إذا عدلنا الرسالة
    else:
        bot.answer_callback_query(call.id, "🤔 لم يتم التحقق من اشتراكك بعد. تأكد من الاشتراك في القناة.", show_alert=True)
        # يمكننا إعادة إرسال رسالة الاشتراك الإجباري مع الأزرار إذا لم ينجح التحقق
        # bot.send_message(call.message.chat.id,
        #                  "✋ **مرحباً بك! لاستخدام البوت، يجب عليك الاشتراك في قناتنا أولاً.**\n\n"
        #                  "اضغط على الزر أدناه للاشتراك، ثم اضغط 'لقد اشتركت' للمتابعة.",
        #                  reply_markup=call.message.reply_markup, parse_mode="Markdown") # إعادة استخدام نفس الأزرار

# ---

# [تعديل] تطبيق التحقق من الاشتراك على جميع الرسائل (middleware)
@bot.message_handler(func=lambda message: True) # هذا سيعالج جميع الرسائل
def check_and_process_message(message):
    # تجاهل رسائل المسؤولين لكي يتمكنوا من اختبار البوت دون الاشتراك (اختياري)
    # if message.from_user.id == ADMIN_ID:
    #     if message.text.startswith('/lang'):
    #         change_language(message)
    #     elif message.text.startswith('/langs'):
    #         list_supported_languages(message)
    #     elif message.text.startswith('/speed'):
    #         change_speed(message)
    #     elif message.text.startswith('/stats'):
    #         send_stats(message)
    #     else:
    #         text_to_speech_logic(message)
    #     return

    if not is_subscribed(message.from_user.id):
        # إذا لم يكن مشتركاً، أرسل له رسالة الاشتراك الإجباري مرة أخرى
        # ونمنع البوت من معالجة الأوامر الأخرى
        markup = telebot.types.InlineKeyboardMarkup()
        subscribe_button = telebot.types.InlineKeyboardButton("اشترك في القناة", url=CHANNEL_LINK)
        check_button = telebot.types.InlineKeyboardButton("✔️ لقد اشتركت", callback_data="check_subscription")
        markup.add(subscribe_button, check_button)
        bot.send_message(message.chat.id,
                         "✋ **مرحباً بك! لاستخدام البوت، يجب عليك الاشتراك في قناتنا أولاً.**\n\n"
                         "اضغط على الزر أدناه للاشتراك، ثم اضغط 'لقد اشتركت' للمتابعة.",
                         reply_markup=markup, parse_mode="Markdown")
        return

    # [هنا نضع الكود الموجود في text_to_speech والأوامر الأخرى]
    # الفكرة هي توجيه جميع رسائل المستخدم (بعد التحقق من الاشتراك) إلى الدالة المناسبة

    # التحقق من الأوامر المعروفة أولاً
    if message.text.startswith('/lang'):
        change_language(message)
    elif message.text.startswith('/langs'):
        list_supported_languages(message)
    elif message.text.startswith('/speed'):
        change_speed(message)
    elif message.text.startswith('/stats'):
        send_stats(message)
    # لا داعي لإعادة توجيه /start أو /help لأنها تعالجها دالة send_welcome
    else:
        # إذا لم يكن أمراً، فافترض أنه نص للتحويل إلى صوت
        text_to_speech_logic(message)


# ---

# [تعديل] دالة منفصلة لتحويل النص إلى صوت
# تم فصل هذه الدالة لأن دالة text_to_speech الأصلية كانت هي الـ handler لكل الرسائل،
# والآن check_and_process_message هي الـ handler الرئيسية
def text_to_speech_logic(message):
    global total_conversions
    text = message.text.strip()
    user_id = message.from_user.id
    unique_users.add(user_id)
    if user_id in banned_users:
        bot.send_message(message.chat.id, "🚫 عذرًا، لا يمكنك استخدام هذا البوت. لقد تم حظرك.")
        return    
    if len(text) > 500:
        bot.reply_to(message, "⚠️ النص طويل جدًا! الرجاء إدخال نص أقصر.")
        return
    
    bot.send_message(message.chat.id, "🎧 جارٍ تحويل النص إلى صوت...")
    try:
        tts = gTTS(text=text, lang=default_lang, slow=default_speed)
        
        file_name = f"{message.from_user.username}_output.mp3" if message.from_user.username else "output.mp3"
        tts.save(file_name)

        total_conversions += 1

        markup = telebot.types.InlineKeyboardMarkup()
        developer_button = telebot.types.InlineKeyboardButton("👨‍💻 المطور", url="https://t.me/my00002")
        download_button = telebot.types.InlineKeyboardButton("📥 تحميل الصوت", callback_data=f"download_{file_name}")
        markup.add(developer_button, download_button)

        with open(file_name, 'rb') as audio_file:
            bot.send_voice(message.chat.id, audio_file, caption=f"🔊 تم تحويل النص إلى صوت:\n\n{text}", reply_markup=markup)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ حدث خطأ: {str(e)}")

# ---

# [بقية الدوال لا تحتاج لتعديل كبير، فقط تأكد أنها معرفة بشكل صحيح]

# تغيير اللغة (تم تعديلها سابقاً)
@bot.message_handler(commands=['lang'])
def change_language(message):
    global default_lang
    user_id = message.from_user.id
    unique_users.add(user_id)
    if user_id in banned_users:
        bot.send_message(message.chat.id, "🚫 عذرًا، لا يمكنك استخدام هذا البوت. لقد تم حظرك.")
        return    
    parts = message.text.split(' ')
    if len(parts) > 1:
        lang_code = parts[1].lower()
        if lang_code in SUPPORTED_LANGS:
            default_lang = lang_code
            bot.reply_to(message, f"🌍 تم تغيير اللغة إلى: {SUPPORTED_LANGS[lang_code]}")
        else:
            lang_list_formatted = "\n".join([f"• `{code}` - {name}" for code, name in SUPPORTED_LANGS.items()])
            bot.reply_to(message, f"❌ اللغة غير مدعومة. الرجاء اختيار لغة من القائمة التالية:\n{lang_list_formatted}", parse_mode="Markdown")
    else:
        lang_list_formatted = "\n".join([f"• `{code}` - {name}" for code, name in SUPPORTED_LANGS.items()])
        bot.reply_to(message, f"🌍 لغتك الحالية هي: {SUPPORTED_LANGS[default_lang]}.\n"
                               f"لاستخدام لغة أخرى، اكتب /lang [رمز اللغة].\n"
                               f"اللغات المدعومة هي:\n{lang_list_formatted}", parse_mode="Markdown")

# ---

# عرض قائمة اللغات المدعومة
@bot.message_handler(commands=['langs'])
def list_supported_languages(message):
    lang_list = "🌐 **اللغات المدعومة:**\n\n"
    for code, name in SUPPORTED_LANGS.items():
        lang_list += f"• `{code}` - {name}\n"
    lang_list += "\nيمكنك تغيير اللغة باستخدام الأمر /lang [رمز اللغة]."
    bot.reply_to(message, lang_list, parse_mode="Markdown")

# ---

# تغيير السرعة
@bot.message_handler(commands=['speed'])
def change_speed(message):
    global default_speed
    parts = message.text.split(' ')
    speed = parts[1].lower() if len(parts) > 1 else 'fast'

    if speed == 'slow':
        default_speed = True
        bot.reply_to(message, "🐢 الصوت الآن بطيء.")
    elif speed == 'fast':
        default_speed = False
        bot.reply_to(message, "🚀 الصوت الآن سريع (افتراضي).")
    else:
        bot.reply_to(message, "❌ السرعة المدعومة: fast, slow")

# ---

# إحصائيات البوت للمشرف
@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.from_user.id == ADMIN_ID:
        stats_message = (
            f"📊 **إحصائيات البوت:**\n\n"
            f"👥 **عدد المستخدمين الفريدين:** {len(unique_users)}\n"
            f"🎙️ **إجمالي التحويلات الصوتية:** {total_conversions}"
        )
        bot.send_message(message.chat.id, stats_message, parse_mode="Markdown")
    else:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")

# ---

# تحميل الصوت (إرسال الملف للمستخدم)
@bot.callback_query_handler(func=lambda call: call.data.startswith("download_"))
def download_audio(call):
    try:
        file_name = call.data.split('_', 1)[1]
        caption_text = call.message.caption
        text_from_caption = ""
        if caption_text and ":" in caption_text:
            text_from_caption = caption_text.split(":", 1)[1].strip()
        else:
            text_from_caption = "لا يتوفر النص الأصلي."

        with open(file_name, 'rb') as audio_file:
            bot.send_document(call.message.chat.id, audio_file, caption=f"📥 حمل الصوت على جهازك:\n\nالنص المرسل:\n{text_from_caption}")

        os.remove(file_name)
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "❌ عذرًا، الملف الصوتي المطلوب غير موجود. ربما تم حذفه مسبقًا.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ حدث خطأ أثناء التحميل: {str(e)}")

# ---

# تشغيل البوت
print("✅ البوت يعمل الآن...")
bot.polling()
