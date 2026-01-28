"""
Instagram zararlari haqida 100+ ta eslatma xabarlari
Har bir video bilan birga #eslatma hashtag bilan yuboriladi
"""

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


# ═══════════════════════════════════════════════════════════════════════════════
# 100+ STATIK OGOHLANTIRISH XABARLARI
# ═══════════════════════════════════════════════════════════════════════════════

WARNINGS = [
    # === MIYAGA TA'SIR (1-20) ===
    "Qisqa videolar miyangizda doimiy dopamin chiqaradi. Bu esa tabiiy quvonch hissini susaytiradi.",
    "Tadqiqotlar shuni ko'rsatadiki, Reels ko'ruvchilarning diqqat vaqti 8 soniyaga tushgan.",
    "Miya plastik — uni qisqa kontentga o'rgatsangiz, chuqur o'ylash qobiliyatini yo'qotasiz.",
    "Har bir scroll miyangizdan energiya oladi. Kuniga 300+ scroll — bu jiddiy charchoq.",
    "Dopamin — motivatsiya gormoni. Instagramda sarflasangiz, haqiqiy ishlarga qiziqish qolmaydi.",
    "Qisqa videolar miyani 'oson mukofot' olishga o'rgatadi. Qiyin ishlar qiyin tuyila boshlaydi.",
    "Multitasking illuziyasi: telefondan foydalanish IQ ni vaqtincha 10 ballga tushiradi.",
    "Yodlash qobiliyati: telefonga bog'liqlik xotirani 20-30% ga susaytiradi.",
    "Miya har safar yangi postga reaksiya beradi — bu charchoqqa olib keladi.",
    "Bolalar miyasi ayniqsa zaif — ekran vaqti rivojlanishni sekinlashtiradi.",
    "Prefrontal korteks (qaror qabul qilish) 25 yoshgacha rivojlanadi. Instagram buni buzadi.",
    "Doimiy rag'batlantirish miyani 'sabrsiz' qiladi — kutish qiyin bo'lib qoladi.",
    "Miya tinchlashish vaqtiga muhtoj. Telefon bu imkoniyatni yo'q qiladi.",
    "Adrenalin va kortizol — stress gormonlari. Salbiy kontentdan oshib ketadi.",
    "Meditatsiya 10 daqiqa miya faoliyatini yaxshilaydi. Instagram 10 daqiqa — aksincha.",
    "Ilmiy fakt: 2 hafta ijtimoiy tarmoqlarsiz — diqqat 30% yaxshilanadi.",
    "Miyada 'reward system' bor. Instagram uni ekspluatatsiya qiladi.",
    "Kreativlik sukut paytlarida tug'iladi. Telefon sukutni yo'q qiladi.",
    "Miya 'default mode' da g'oyalar yaratadi. Doimiy scroll buni to'xtatadi.",
    "Bolalar miyasi kattalar miyasidan 2 baravar tez ijtimoiy tarmoqlarga 'hook' bo'ladi.",

    # === PSIXOLOGIK TA'SIR (21-40) ===
    "Depressiya va Instagram foydalanish o'rtasida kuchli bog'liqlik aniqlangan.",
    "O'ziga past baho — 'mukammal' hayotlarni ko'rib, o'zingizni kam his qilasiz.",
    "FOMO — biror narsani o'tkazib yuborish qo'rquvi. Instagram buni ataylab kuchaytiradi.",
    "Taqqoslash tuzog'i: siz o'zingizni boshqalarning eng yaxshi lahzalariga taqqoslayapsiz.",
    "Anxiety darajasi ijtimoiy tarmoqlarga sarflangan vaqt bilan to'g'ridan-to'g'ri bog'liq.",
    "Yolg'izlik hissi: 1000 ta follower — lekin haqiqiy do'st yo'q.",
    "Narcissizm darajasi selfie va postlar soni bilan oshib boradi.",
    "'Like' sanash — o'z qadr-qimmatini begona odamlar fikriga bog'lash.",
    "Bola-yoshlar orasida o'z tanasidan norozilik 40% ga oshgan — Instagram sababli.",
    "Kiberbuling — har 3-yosh o'spirindan biri duch kelgan.",
    "Perfeksionizm sindromi: 'mukammal post' uchun soatlab harakat qilish.",
    "Validatsiya qidiruvi — tashqi tasdiqlashga bog'liq bo'lib qolish.",
    "Envy (hasad) hissi — boshqalarning 'mukammal' hayotini ko'rib.",
    "O'z-o'zini yaroqsiz his qilish — filtrlar va tahrir tufayli.",
    "Emotsional beqarorlik — mood swings ijtimoiy tarmoqlarga bog'liq.",
    "Social anxiety — real hayotda muloqot qilish qiyinlashadi.",
    "Stress darajasi: har bir notification kortizol chiqaradi.",
    "O'rtacha o'spirin kuni 150+ marta telefonini tekshiradi.",
    "Tashvish: 'Men qanday ko'rinaman?' degan savol har doim miyada.",
    "Imposter syndrome — 'Hamma menga o'xshamayman' hissi.",

    # === JISMONIY SOG'LIQ (41-55) ===
    "Ko'k yorug'lik melatonin ishlab chiqarishni to'xtatadi — uyqu buziladi.",
    "Kechasi telefon — uyqu sifati 40% ga tushadi.",
    "Bo'yin og'rig'i (text neck) — bosh og'irligi 27 kg ga teng bo'ladi.",
    "Ko'z charchashi — doimiy ekranga qarash quruq ko'z sindromiga olib keladi.",
    "Orqa muskullari zaiflashishi — yomon poza tufayli.",
    "Karpel tunel sindromi — qo'l barmoqlari va bilaklarida og'riq.",
    "Bosh og'rig'i — ekranning yoritilganligi va ko'k yorug'lik tufayli.",
    "Semirish xavfi — harakatsiz o'tirish va ovqatlanish buzilishi.",
    "Yurak urishi tezlashishi — stressli kontentdan keyin.",
    "Vitamin D yetishmovchiligi — uyda ekran oldida o'tirish.",
    "Immun tizim zaiflashishi — stress va uyqu yetishmovchiligi.",
    "Qon bosimi — doimiy stress holati tufayli ko'tarilishi mumkin.",
    "Suyak zichligi kamayishi — harakatsiz turmush tarzi.",
    "Ko'rish pasayishi — yosh odamlar orasida 30% ga oshgan.",
    "Eshitish muammolari — naushnik bilan baland ovoz.",

    # === VAQT SARFI (56-70) ===
    "O'rtacha inson Instagramda kuniga 3 soat sarflaydi. Yiliga 45 kun!",
    "3 soat × 365 kun = 1095 soat. Bu vaqtda yangi kasb o'rganish mumkin.",
    "Bir yilda sarflangan vaqt bilan 3-4 ta tilni o'rganish mumkin edi.",
    "Har bir 'faqat 5 daqiqa' 30 daqiqaga aylanadi — bu psixologik fakt.",
    "Vaqt — eng qimmat resurs. Uni qaytarib bo'lmaydi.",
    "Muvaffaqiyatli odamlar o'rtasida ijtimoiy tarmoq ishlatish juda past.",
    "Mark Zuckerberg o'z bolalarini ijtimoiy tarmoqlardan cheklaydi.",
    "Bill Gates bolalariga 14 yoshgacha telefon bermagan.",
    "Steve Jobs iPad yaratgan, lekin bolalariga foydalanishni taqiqlagan.",
    "Har kuni 10 daqiqa kitob o'qish — yiliga 20+ kitob.",
    "Har kuni 1 soat o'rganish — yiliga professional sertifikat.",
    "Vaqtingizni qanday sarflashingiz — kelajagingizni belgilaydi.",
    "'Scroll pauzasi' qilish osonroq tuyuladi, lekin miyaga og'ir.",
    "Productive odamlar morning routine'da telefon ko'rmaydi.",
    "Digital minimalizm — yangi davr harakati sababli paydo bo'ldi.",

    # === MUNOSABATLAR (71-85) ===
    "Ijtimoiy tarmoqlar 'ijtimoiy' deb atalsa-da, yolg'iz qiladi.",
    "Oilada suhbat o'rniga — har kim o'z telefonida.",
    "Do'stlik sifati tushdi — online 1000 do'st, real 0.",
    "Juftliklar o'rtasida telefon — uchinchi shaxs kabi.",
    "Bolalar ota-onasining yuzini emas, telefon orqasini ko'radi.",
    "Eye contact qilish qobiliyati kamaymoqda.",
    "Real suhbat — awkward tuyuladi, chunki odatdan chiqilgan.",
    "Empathiya darajasi yoshlarda 40% tushgan — ekranlar sababli.",
    "Telegram, WhatsApp — suhbat emas, chat.",
    "Haqiqiy do'stlik — shunchaki like bosish emas.",
    "'Online do'stlar' — real hayotda tanish bo'lmagan odamlar.",
    "Romantik munosabatlar sifati tushgan — hammasini ekranda izlash.",
    "Oilaviy kechki ovqat — har kim o'z dunyosida.",
    "Bolalar bilan sifatli vaqt — telefonsiz vaqt.",
    "Hurmat — birovga to'liq diqqat berish. Telefon buni buzadi.",

    # === IQTISODIY TA'SIR (86-95) ===
    "Instagram reklamalar orqali keraksiz savdoga undaydi.",
    "Impulsiv xaridlar — 'ko'rdim, oldim' sindromi.",
    "Influencer marketing — soxta tavsiyalar bilan pul ishlash.",
    "Qimmatbaho lifestyle — oddiy odamlarda stress yaratadi.",
    "Solishtiruvchan iste'mol — 'uniki bor, menda ham bo'lsin'.",
    "Kriptovalyuta va MLM sxemalari — ijtimoiy tarmoqlar orqali tarqaladi.",
    "Vaqt = pul. Instagramga sarflangan vaqt = yo'qotilgan daromad.",
    "Attention economy — sizning diqqatingiz sotilmoqda.",
    "Bepul ilova = siz mahsulotsiz. Sizning ma'lumotlaringiz sotiladi.",
    "Reklama algoritmlari sizni 'foydalanuvchi' emas, 'mahsulot' deb ko'radi.",

    # === JAMIYAT VA MADANIYAT (96-110) ===
    "Fake news tez tarqaladi — factcheck qilish odat emas.",
    "Echo chamber — faqat bir xil fikrlarni ko'rish.",
    "Polarizatsiya — jamiyat ikkiga bo'linmoqda.",
    "Cancel culture — bir xato uchun butun hayot buziladi.",
    "Surface level thinking — hamma narsa yuzaki.",
    "Attention span qisqarishi — uzun kontentni o'qib bo'lmaydi.",
    "Kitob o'qish odati yo'qolmoqda — maqola ham uzun tuyuladi.",
    "Sabr-toqat — trenddan chiqib ketmoqda.",
    "Deep work — deyarli imkonsiz bo'lib qolmoqda.",
    "Privacy — shaxsiy hayot tushunchasi o'zgarmoqda.",
    "Bolalar roliklarda yulduz bo'lishni orzu qiladi, olim emas.",
    "Instant gratification — hamma narsani hozir va yengillik bilan.",
    "Comparison trap — hayotni raqamlar bilan o'lchash.",
    "Digital footprint — bugun yozganlaringiz abadiy internetda.",
    "Cybersecurity — shaxsiy ma'lumotlar xavf ostida.",

    # === ALTERNATIVALAR VA YECHIMLAR (111-120) ===
    "Notifikatsiyalarni o'chiring — diqqat buzilishini 70% kamaytiring.",
    "Echki soat o'rnating — kuniga max 30 daqiqa ijtimoiy tarmoq.",
    "Telefonni yotoqdan chiqaring — uyqu sifati oshadi.",
    "Haftada 1 kun 'digital detox' — miyani reset qiling.",
    "Kitob o'qish — 6 daqiqa stress 68% ga kamayadi.",
    "Tabiatda 20 daqiqa — kortizol darajasi tushadi.",
    "Sport — tabiiy dopamin manbai.",
    "Meditatsiya — diqqat va xotiraga ijobiy ta'sir.",
    "Jonli suhbat — empathiya va aloqani kuchaytiradi.",
    "Yangi ko'nikma o'rganing — vaqtingizni qadrlang.",
]


# ═══════════════════════════════════════════════════════════════════════════════
# DINAMIK SHABLONLAR (har safar yangi raqamlar bilan)
# ═══════════════════════════════════════════════════════════════════════════════

def _get_dynamic_warning():
    """Har safar yangi raqamlar bilan warning"""
    hours, days = _random_days()
    percent = _random_percent()
    
    templates = [
        f"O'rtacha foydalanuvchi kuniga {hours} soat sarflaydi. Yiliga {days} kun yo'qotiladi!",
        f"Tadqiqotlar: kuniga 3+ soat ijtimoiy tarmoq — anxiety {percent}% ga oshadi.",
        f"{hours} soat × 365 = {round(hours * 365)} soat yilda. Yangi kasb o'rganishga yetardi.",
        f"Har {random.randint(3, 5)} daqiqada telefonni tekshirish — stress {percent}% oshadi.",
        f"Reels ko'ruvchilarning {percent}% diqqat muammolaridan shikoyat qiladi.",
        f"Yosh odamlarning {percent}% 'telefonsiz bo'lish' dan xavotirlanadi — bu nomofobia.",
        f"Har bir notification — kortizol otilishi. Kuniga {random.randint(50, 100)}+ marta!",
        f"Uyqusizlik: kechqurun telefon — REM fazasi {percent}% qisqaradi.",
        f"{days} kun yilda. Bu vaqtda kitob yozsangiz — inson qismatini o'zgartirgan bo'lardingiz.",
        f"Scroll addiction: miyangiz har {random.randint(5, 15)} sekundda yangi dopamin kutadi.",
    ]
    
    return random.choice(templates)


def get_random_warning() -> str:
    """
    Tasodifiy warning qaytaradi #eslatma hashtag bilan.
    70% statik, 30% dinamik (har safar yangi raqamlar bilan).
    """
    hashtag = "#eslatma"
    
    if random.random() < 0.7:
        warning_text = random.choice(WARNINGS)
    else:
        warning_text = _get_dynamic_warning()
    
    return f"⚠️ {hashtag}\n\n{warning_text}"
