
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# قم بتعيين توكن البوت الخاص بك هنا
BOT_TOKEN = "6418845303:AAFNx_TT6oRMUv8lLhMpeqAmTO_L1516ymY"
# قم بتعيين معرف المدير الخاص بك هنا
ADMIN_ID = 6454550864 # مثال: 123456789

# قم بتمكين التسجيل (Loggings) للمساعدة في تصحيح الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- بيانات الخدمات، القنوات، المواقع، التصاميم، البوتات ---
# يمكنك تعديل هذه القوائم حسب خدماتك ومنصاتك
# تمت إضافة حقل 'media' لكل عنصر
SERVICES = {
    "تصميم مواقع الويب": {
        "description": "تصميم وتطوير مواقع الويب الاحترافية والمتجاوبة (Responsive) باستخدام أحدث التقنيات.",
        "link": "https://yourwebsite.com/web_design",
        "media": "ss.png" # مثال لصور
    },
    "تطوير بوتات التليجرام": {
        "description": "بناء بوتات تليجرام مخصصة لمختلف الأغراض، من بوتات الخدمة الذاتية إلى بوتات إدارة المجموعات.",
        "link": "https://yourwebsite.com/telegram_bots",
        "media": "https://via.placeholder.com/600x400/33FF57/FFFFFF?text=Telegram+Bots+Image" # مثال لصور
    },
    "خدمات التصميم الجرافيكي": {
        "description": "تصميم شعارات، هويات بصرية، منشورات سوشيال ميديا، ومواد تسويقية جذابة.",
        "link": "https://yourwebsite.com/graphic_design",
        "media": "https://via.placeholder.com/600x400/3357FF/FFFFFF?text=Graphic+Design+Image" # مثال لصور
    }
}

CHANNELS = {
    "قناة التليجرام": {
        "description": "أحدث الأخبار والتحديثات والمشاريع التي نعمل عليها.",
        "link": "https://t.me/YourTelegramChannel",
        "media": "https://via.placeholder.com/600x400/FF33A1/FFFFFF?text=Telegram+Channel"
    },
    "حساب انستغرام": {
        "description": "معرض لأعمال التصميم والجرافيك التي قمنا بها.",
        "link": "https://instagram.com/YourInstagram",
        "media": "https://via.placeholder.com/600x400/A133FF/FFFFFF?text=Instagram+Account"
    },
    "صفحة فيسبوك": {
        "description": "تواصل معنا وتابع أحدث منشوراتنا ومشاريعنا.",
        "link": "https://facebook.com/YourFacebookPage",
        "media": "https://via.placeholder.com/600x400/33A1FF/FFFFFF?text=Facebook+Page"
    }
}

WEBSITES = {
    "الموقع الشخصي/الشركة": {
        "description": "موقعي الرسمي الذي يعرض جميع خدماتي ومعرض أعمالي.",
        "link": "https://yourwebsite.com",
        "media": "https://via.placeholder.com/600x400/FF3333/FFFFFF?text=Personal+Website"
    },
    "مدونة التقنية": {
        "description": "مقالات وموارد حول تطوير الويب والبرمجة.",
        "link": "https://yourblog.com",
        "media": "https://via.placeholder.com/600x400/33FF33/FFFFFF?text=Tech+Blog"
    }
}

DESIGNS = {
    "تصميم الشعار XYZ": {
        "description": "شعار مبتكر لشركة ناشئة متخصص في [المجال].",
        "link": "https://yourportfolio.com/logo_xyz",
        "media": "https://via.placeholder.com/600x400/3333FF/FFFFFF?text=Logo+Design+XYZ"
    },
    "تصميم واجهة مستخدم (UI) لتطبيق A": {
        "description": "تصميم واجهة مستخدم حديثة وسهلة الاستخدام لتطبيق جوال.",
        "link": "https://yourportfolio.com/app_ui_a",
        "media": "https://via.placeholder.com/600x400/FFFF33/000000?text=UI+Design+App+A"
    }
}

BOTS = {
    "بوت إدارة المجموعات": {
        "description": "بوت متعدد الوظائف لإدارة مجموعات التليجرام بكفاءة.",
        "link": "https://t.me/YourGroupManagerBot",
        "media": "https://via.placeholder.com/600x400/FF5733/FFFFFF?text=Group+Manager+Bot"
    },
    "بوت التسوق الإلكتروني": {
        "description": "بوت يتيح للمستخدمين تصفح وشراء المنتجات مباشرة من التليجرام.",
        "link": "https://t.me/YourShopBot",
        "media": "https://via.placeholder.com/600x400/57FF33/FFFFFF?text=E-commerce+Bot"
        # مثال لفيديو: "media": "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4"
    }
}

# --- وظائف الأوامر الرئيسية ---
async def start(update: Update, context):
    """يرسل رسالة ترحيبية مع الأزرار الرئيسية."""
    keyboard = [
        [InlineKeyboardButton("خدماتي", callback_data='show_services')],
        [InlineKeyboardButton("قنواتي على السوشيال ميديا", callback_data='show_channels')],
        [InlineKeyboardButton("مواقعي الإلكترونية", callback_data='show_websites')],
        [InlineKeyboardButton("تصاميمي", callback_data='show_designs')],
        [InlineKeyboardButton("بوتاتي", callback_data='show_bots')],
        [InlineKeyboardButton("تواصل مع المدير", callback_data='contact_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('أهلاً بك! اختر من القائمة أدناه لعرض تفاصيل أعمالي وخدماتي:', reply_markup=reply_markup)

# --- وظائف عرض التفاصيل لكل قسم ---
async def show_section_details(update: Update, context, section_data, section_name):
    """دالة عامة لعرض تفاصيل أي قسم."""
    query = update.callback_query
    await query.answer()

    keyboard = []
    for item_name, item_details in section_data.items():
        keyboard.append([InlineKeyboardButton(item_name, callback_data=f'detail_{section_name}_{item_name.replace(" ", "_")}')])
    keyboard.append([InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data='main_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'اختر {section_name} لعرض تفاصيله:', reply_markup=reply_markup)

async def show_services(update: Update, context):
    await show_section_details(update, context, SERVICES, "services")

async def show_channels(update: Update, context):
    await show_section_details(update, context, CHANNELS, "channels")

async def show_websites(update: Update, context):
    await show_section_details(update, context, WEBSITES, "websites")

async def show_designs(update: Update, context):
    await show_section_details(update, context, DESIGNS, "designs")

async def show_bots(update: Update, context):
    await show_section_details(update, context, BOTS, "bots")

# --- وظائف عرض تفاصيل عنصر محدد ---
async def show_item_detail(update: Update, context, section_data, section_name_for_callback):
    """دالة عامة لعرض تفاصيل عنصر معين مع دعم للصور/الفيديوهات."""
    query = update.callback_query
    await query.answer()
    
    # استخراج اسم العنصر من callback_data
    item_name_raw = query.data.replace(f'detail_{section_name_for_callback}_', '')
    item_name = item_name_raw.replace('_', ' ') # لإعادة المسافات الأصلية

    item_details = section_data.get(item_name)

    if item_details:
        description = item_details.get("description", "لا يوجد وصف متوفر.")
        link = item_details.get("link")
        media = item_details.get("media") # استخراج حقل الميديا الجديد

        message_text = f"**{item_name}**\n\n{description}"
        
        keyboard = []
        if link:
            keyboard.append([InlineKeyboardButton("الذهاب إلى الرابط", url=link)])
        
        # زر العودة للقسم المحدد
        keyboard.append([InlineKeyboardButton("العودة لقائمة " + section_name_for_callback.replace("_", " "), callback_data=f'show_{section_name_for_callback}')])
        # زر العودة للقائمة الرئيسية
        keyboard.append([InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data='main_menu')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)

        # التحقق مما إذا كان هناك محتوى ميديا (صورة أو فيديو) للعنصر
        if media:
            if media.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # إرسال صورة
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=media, caption=message_text, reply_markup=reply_markup, parse_mode='Markdown')
            elif media.lower().endswith(('.mp4', '.avi', '.mov')):
                # إرسال فيديو
                await context.bot.send_video(chat_id=query.message.chat_id, video=media, caption=message_text, reply_markup=reply_markup, parse_mode='Markdown')
            else:
                # إذا كان الرابط لا يشير إلى صورة أو فيديو معروف، أرسل النص فقط
                await query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            # إذا لم يكن هناك ميديا، أرسل النص فقط
            await query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await query.edit_message_text("عذراً، لم يتم العثور على التفاصيل لهذا العنصر.")

# ربط كل قسم بوظيفة عرض تفاصيل العنصر الخاص به
async def show_service_detail(update: Update, context):
    await show_item_detail(update, context, SERVICES, "services")

async def show_channel_detail(update: Update, context):
    await show_item_detail(update, context, CHANNELS, "channels")

async def show_website_detail(update: Update, context):
    await show_item_detail(update, context, WEBSITES, "websites")

async def show_design_detail(update: Update, context):
    await show_item_detail(update, context, DESIGNS, "designs")

async def show_bot_detail(update: Update, context):
    await show_item_detail(update, context, BOTS, "bots")

# --- وظيفة العودة للقائمة الرئيسية ---
async def back_to_main_menu(update: Update, context):
    """يعود للقائمة الرئيسية."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("خدماتي", callback_data='show_services')],
        [InlineKeyboardButton("قنواتي على السوشيال ميديا", callback_data='show_channels')],
        [InlineKeyboardButton("مواقعي الإلكترونية", callback_data='show_websites')],
        [InlineKeyboardButton("تصاميمي", callback_data='show_designs')],
        [InlineKeyboardButton("بوتاتي", callback_data='show_bots')],
        [InlineKeyboardButton("تواصل مع المدير", callback_data='contact_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # ملاحظة: عند العودة للقائمة الرئيسية، يجب استخدام `reply_text` بدلاً من `edit_message_text` 
    # إذا كانت الرسالة الأصلية (التي تحتوي على القائمة الرئيسية) قد تم حذفها أو تعديلها بواسطة محتوى وسائط.
    # في هذه الحالة، سنفترض أننا نرسل رسالة جديدة.
    await query.message.reply_text('اختر من القائمة أدناه لعرض تفاصيل أعمالي وخدماتي:', reply_markup=reply_markup)


# --- وظائف التواصل مع المدير ---
async def contact_admin_start(update: Update, context):
    """يخبر المستخدم بكيفية التواصل مع المدير."""
    query = update.callback_query
    await query.answer()
    
    message_text = "للتواصل مع المدير، قم بإرسال رسالتك مباشرة في هذه المحادثة. سأقوم بإعادة توجيه رسالتك للمدير."
    keyboard = [
        [InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message_text, reply_markup=reply_markup)
    
    # تفعيل حالة "تواصل_مع_المدير" للمستخدم
    context.user_data['contact_admin_mode'] = True

async def forward_message_to_admin(update: Update, context):
    """يقوم بإعادة توجيه رسائل المستخدم إلى المدير."""
    if context.user_data.get('contact_admin_mode'):
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        first_name = update.message.from_user.first_name
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"رسالة جديدة من المستخدم:\n"
                 f"ID: {user_id}\n"
                 f"Username: @{username if username else 'غير متوفر'}\n"
                 f"الاسم: {first_name}\n\n"
                 f"الرسالة:\n{update.message.text}"
        )
        await update.message.reply_text("تم إرسال رسالتك إلى المدير بنجاح! سيتم الرد عليك قريباً.")
        # تعطيل وضع "تواصل_مع_المدير" بعد الإرسال
        context.user_data['contact_admin_mode'] = False
    else:
        # إذا لم يكن المستخدم في وضع التواصل، يمكن معالجة الرسائل العادية هنا أو تجاهلها
        pass

async def reply_to_user_from_admin(update: Update, context):
    """يتيح للمدير الرد على المستخدم."""
    if update.message.reply_to_message and update.message.chat_id == ADMIN_ID:
        # البحث عن ID المستخدم الأصلي في الرسالة التي تم الرد عليها
        original_message_text = update.message.reply_to_message.text
        user_id_line = next((line for line in original_message_text.split('\n') if line.startswith('ID: ')), None)
        
        if user_id_line:
            user_id = int(user_id_line.split(': ')[1])
            reply_text = update.message.text
            
            try:
                await context.bot.send_message(chat_id=user_id, text=f"المدير يرد عليك:\n{reply_text}")
                await update.message.reply_text("تم إرسال ردك للمستخدم بنجاح.")
            except Exception as e:
                await update.message.reply_text(f"حدث خطأ أثناء إرسال الرد: {e}")
        else:
            await update.message.reply_text("لم يتم العثور على معرف المستخدم في الرسالة الأصلية.")
    elif update.message.chat_id == ADMIN_ID:
        await update.message.reply_text("يرجى الرد على رسالة المستخدم الأصلية لضمان وصول ردك إليه.")


# --- وظيفة معالجة الأخطاء ---
async def error_handler(update: object, context):
    """سجل الأخطاء التي تسببها التحديثات."""
    logger.error(f"حدث خطأ: {context.error}", exc_info=True)
    if update and update.effective_message:
        await update.effective_message.reply_text("عذراً، حدث خطأ ما. يرجى المحاولة مرة أخرى لاحقاً.")

# --- الوظيفة الرئيسية لتشغيل البوت ---
def main():
    """تشغيل البوت."""
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))

    # إضافة معالجات Callbacks للأزرار الشفافة
    application.add_handler(CallbackQueryHandler(show_services, pattern='^show_services$'))
    application.add_handler(CallbackQueryHandler(show_channels, pattern='^show_channels$'))
    application.add_handler(CallbackQueryHandler(show_websites, pattern='^show_websites$'))
    application.add_handler(CallbackQueryHandler(show_designs, pattern='^show_designs$'))
    application.add_handler(CallbackQueryHandler(show_bots, pattern='^show_bots$'))

    application.add_handler(CallbackQueryHandler(show_service_detail, pattern='^detail_services_'))
    application.add_handler(CallbackQueryHandler(show_channel_detail, pattern='^detail_channels_'))
    application.add_handler(CallbackQueryHandler(show_website_detail, pattern='^detail_websites_'))
    application.add_handler(CallbackQueryHandler(show_design_detail, pattern='^detail_designs_'))
    application.add_handler(CallbackQueryHandler(show_bot_detail, pattern='^detail_bots_'))

    application.add_handler(CallbackQueryHandler(contact_admin_start, pattern='^contact_admin$'))
    application.add_handler(CallbackQueryHandler(back_to_main_menu, pattern='^main_menu$'))

    # معالج الرسائل النصية لإعادة توجيهها للمدير
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
    
    # معالج الرسائل النصية للرد على المستخدمين من قبل المدير
    application.add_handler(MessageHandler(filters.TEXT & filters.REPLY & filters.User(ADMIN_ID), reply_to_user_from_admin))

    # إضافة معالج الأخطاء
    application.add_error_handler(error_handler)

    # بدء تشغيل البوت
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
