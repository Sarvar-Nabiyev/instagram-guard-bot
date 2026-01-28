import random

def _random_hours():
    """Random hours per day (2.0 - 4.5)"""
    return round(random.uniform(2.0, 4.5), 1)

def _random_percent():
    """Random percentage for research stats (25-75)"""
    return random.randint(25, 75)

def _random_days():
    """Calculate days lost per year based on hours"""
    hours = _random_hours()
    days = round((hours * 365) / 24)
    return hours, days

def _random_country():
    """Random country with social media restrictions"""
    countries = [
        ("Xitoy", "TikTok kuniga 40 daqiqa bilan cheklangan"),
        ("Janubiy Koreya", "yoshlar uchun kechki soatlarda taqiqlangan"),
        ("Avstraliya", "16 yoshgacha ijtimoiy tarmoqlar taqiqlangan"),
        ("Fransiya", "maktablarda telefonlar to'liq taqiqlanadi"),
        ("Buyuk Britaniya", "reels algoritmlari qonun bilan cheklanmoqda"),
    ]
    return random.choice(countries)


# ═══════════════════════════════════════════════════════════════════════════════
# STATIK OGOHLANTIRISH XABARLARI (10+ xil)
# ═══════════════════════════════════════════════════════════════════════════════

STATIC_WARNINGS = [
    """⚠️ **Diqqat! Instagram va qisqa videolar zararlari:**

🧠 Qisqa videolar (Reels, Shorts) miyangizda doimiy "yangilik" hissini uyg'otib, sun'iy dopamin chiqarishga majbur qiladi. Bu esa diqqatni jamlash qobiliyatini pasaytiradi va xotirani susaytiradi.""",

    """⚠️ **Vaqtingizni qadrlang!**

⏳ Instagramga kirib, soatlab vaqt yo'qotganingizni sezmay qoldingizmi? Bu tasodif emas. Ilova algoritmlari sizni imkon qadar uzoqroq ushlab turish uchun yaratilgan.""",

    """⚠️ **Psixologik ta'sir:**

😔 Depressiya, xavotir va o'ziga past baho berish — bularning barchasi "ideal hayot" aks etgan videolarni ko'p tomosha qilish oqibatidir.""",

    """⚠️ **Eslatma:**

🚭 Qisqa videolar ko'rishni to'xtatish — chekishni tashlash bilan barobar qiyin. Lekin bu sizning miyangiz va kelajagingiz uchun eng to'g'ri qaror.""",

    """⚠️ **Uyqu buzilishi:**

🌙 Kechqurun telefon ekraniga qarab o'tirish uyqu sifatini keskin pasaytiradi. Ko'k yorug'lik melatonin ishlab chiqarishni to'xtatadi.""",

    """⚠️ **Ijodkorlik o'limi:**

🎨 Doimiy kontentni iste'mol qilish miyangizning ijodiy qismini "yoqib qo'yadi". O'z fikrlaringiz va g'oyalaringiz bilan qoling!""",

    """⚠️ **FOMO sindroma:**

😰 "Fear Of Missing Out" — biror narsani o'tkazib yuborish qo'rquvi. Instagram bu hissiyotni ataylab kuchaytiradi. Ammo hayot ekranda emas!""",

    """⚠️ **Haqiqiy aloqalar:**

👥 Ijtimoiy tarmoqlar "ijtimoiy" deb atalsa-da, ular haqiqiy insoniy aloqalarni zaifslashtiradi. Yaqinlaringiz bilan jonli suhbatlashing!""",

    """⚠️ **Miya plastikligi:**

🧬 Yoshlikda miya juda moslashuvchan. Uni qisqa videolar bilan "o'rgatish" — kelajakda chuqur o'ylash qobiliyatini yo'qotish demak.""",

    """⚠️ **Taqqoslash tuzog'i:**

📉 Har bir post — eng yaxshi momentlarning tanlangani. Siz o'zingizni boshqalarning "highlight reel"iga taqqoslayapsiz, ular ham sizning ko'rmagan qiyinchiliklaringiz bor.""",

    """⚠️ **Vaqt — eng qimmat boylik:**

💎 Jeff Bezos, Elon Musk, Bill Gates — ularning barchasi bir xil 24 soatga ega. Farq shundaki, ular bu vaqtni qanday sarflashini tanlaydi.""",

    """⚠️ **Dopamin detox:**

🔋 Miyangiz "reset" qilishni talab qiladi. Haftada bir kun ijtimoiy tarmoqlarsiz o'tkazing — hayratlanarli farqni sezasiz.""",
]


# ═══════════════════════════════════════════════════════════════════════════════
# DINAMIK OGOHLANTIRISH SHABLONLARI (har safar boshqa raqamlar)
# ═══════════════════════════════════════════════════════════════════════════════

def _generate_dynamic_warnings():
    """Har safar yangi raqamlar bilan warning generatsiya qiladi"""
    
    hours, days = _random_days()
    country, restriction = _random_country()
    percent = _random_percent()
    
    dynamic_templates = [
        f"""📊 **Statistika:**

O'rtacha foydalanuvchi Instagramda kuniga **{hours} soat** sarflaydi. Yiliga bu **{days} kun** demak! 

Bu vaqtni yangi til o'rganish yoki kasb egallashga sarflash mumkin edi.""",

        f"""🌍 **Dunyo tajribasi:**

{country}da {restriction}. Chunki ular bu ilovalar kelajak avlodining aqliy salohiyatini "zombilashtirishi"dan xavotirda. 

Bizchi? Biz o'z kelajagimizga befarq emasmizmi?""",

        f"""🧪 **Tadqiqot natijasi:**

So'nggi ilmiy tadqiqotlarga ko'ra, kuniga 3+ soat ijtimoiy tarmoqlarga sarflaydigan odamlarda xavotirlanish darajasi **{percent}%** ga yuqori.

Miyangizni himoya qiling!""",

        f"""📱 **Raqamlar gapiradi:**

Agar siz kuniga {hours} soat Instagramda bo'lsangiz:
• Haftada: **{round(hours * 7)} soat**
• Oyda: **{round(hours * 30)} soat** 
• Yilda: **{days} kun** yo'qotasiz!

Bu vaqt bilan nima qilish mumkin edi?""",

        f"""🎓 **Ta'lim vs Instagram:**

{hours} soat × 365 kun = **{round(hours * 365)} soat** yilda.

Bu vaqt ichida:
• 2-3 ta til o'rganish mumkin
• Dasturlashni o'rganish mumkin
• Yangi kasb egallash mumkin

Tanlov sizniki!""",

        f"""🧠 **Miya haqida fakt:**

Tadqiqotchilar aniqlashicha, muntazam qisqa video ko'ruvchilarning diqqatni saqlash vaqti **{_random_percent()}%** ga qisqargan.

Kitob o'qing — miyangizni mashq qildiring!""",

        f"""⚡ **Energiya sarfi:**

Har bir scroll — miyangizdan energiya oladi. Kuniga **{random.randint(200, 400)}** ta scroll... 

Bu energiyani foydali ishga sarflang!""",
    ]
    
    return random.choice(dynamic_templates)


def get_random_warning() -> str:
    """
    Tasodifiy warning qaytaradi.
    50% statik, 50% dinamik (har safar yangi raqamlar bilan).
    """
    if random.random() < 0.5:
        return random.choice(STATIC_WARNINGS)
    else:
        return _generate_dynamic_warnings()
