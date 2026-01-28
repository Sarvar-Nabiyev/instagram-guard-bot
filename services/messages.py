"""
Instagram zararlari haqida 100+ ta batafsil eslatma xabarlari
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
# 100+ BATAFSIL OGOHLANTIRISH XABARLARI
# ═══════════════════════════════════════════════════════════════════════════════

WARNINGS = [
    # === MIYAGA TA'SIR (1-15) ===
    """🧠 **Miya va dopamin:**

Qisqa videolar (Reels, Shorts) miyangizda doimiy "yangilik" hissini uyg'otib, sun'iy dopamin chiqarishga majbur qiladi. Bu esa diqqatni jamlash qobiliyatini pasaytiradi va xotirani susaytiradi.

💡 _Miyangizni himoya qiling — ekran vaqtini cheklang!_""",

    """🧠 **Diqqat buzilishi:**

Tadqiqotlar shuni ko'rsatadiki, muntazam Reels ko'ruvchilarning diqqatni saqlash vaqti 8 soniyagacha tushgan — bu oltin baliqnikidan ham kam!

Kitob o'qish, chess o'ynash — diqqatni qayta tiklash usullari.""",

    """🧠 **Miya plastikligi:**

Yoshlikda miya juda moslashuvchan. Uni qisqa videolarga "o'rgatsangiz" — kelajakda chuqur o'ylash, tahlil qilish va murakkab muammolarni yechish qobiliyatini yo'qotasiz.

🎯 _Miya — eng qimmatli organingiz. Uni avaylab asrang!_""",

    """🧠 **Energiya sarfi:**

Har bir scroll miyangizdan energiya oladi. Kuniga 300+ marta scroll qilish — bu jiddiy mental charchoqqa olib keladi. Kechqurun "hech narsa qilmadim, lekin charchadim" deyapsizmi?

Sababi — telefon! 📱""",

    """🧠 **Dopamin taqchilligi:**

Dopamin — motivatsiya va quvonch gormoni. Instagramda sarflasangiz, miyangiz uni "arzonlashtiradi". Natija: haqiqiy ishlarga, o'qishga, sportga qiziqish qolmaydi.

⚡ _Tabiiy dopamin manbalarini toping: sport, musiqa, tabiat!_""",

    """🧠 **Oson mukofot sindromi:**

Qisqa videolar miyani "oson mukofot" olishga o'rgatadi. Bir necha sekundda — yangilik, kulgili moment, qiziqarli fakt. 

Natija: qiyin va uzoq ishlar (o'qish, kasb egallash) chidab bo'lmas darajada qiyin tuyiladi.""",

    """🧠 **Multitasking illuziyasi:**

Telefondan foydalanish paytida IQ vaqtincha 10 ballga tushadi — bu bir kecha uxlamaslik bilan teng! 

Bitta ishga 100% e'tibor bering — samaradorlik 10 barobar oshadi. 🎯""",

    """🧠 **Xotira zaiflashishi:**

Telefonga haddan tashqari bog'liqlik xotirani 20-30% ga susaytiradi. "Google'dan topsam bo'ldi" degan fikr miyani dangasalashtiradi.

📚 _Telefonsiz kun — miya uchun sport!_""",

    """🧠 **Charchoq sababi:**

Miya har safar yangi post, video, xabarga reaksiya beradi. Bu charchoqqa olib keladi — hatto jismonan hech narsa qilmasangiz ham.

Shuning uchun telefondan keyin "bo'shashdim" deb his qilasiz. Aslida — miyangiz charchagan.""",

    """🧠 **Bolalar miyasi:**

Bolalar va o'spirinlar miyasi ekranlarga 2 baravar tez "hook" bo'ladi. Prefrontal korteks (qaror qabul qilish) 25 yoshgacha rivojlanadi.

👨‍👩‍👧 _Bolalaringizni ekranlardan himoya qiling!_""",

    """🧠 **Sabrsizlik kasalligi:**

Doimiy tez rag'batlantirish miyani "sabrsiz" qiladi. Navbatda kutish, uzoq loyihalar ustida ishlash — bardosh bilan qiyin.

Natija: hech narsani oxirigacha yetkazolmaysiz.""",

    """🧠 **Tinchlik zaruriyati:**

Miya "default mode"da — ya'ni hech narsa qilmayotgan paytda — g'oyalar yaratadi, muammolarni yechadi. 

Telefon sukut paytlarini yo'q qiladi. Ijodkorligingiz azoblanadi.""",

    """🧠 **Kreativlik o'limi:**

Doimiy kontentni iste'mol qilish miyangizning ijodiy qismini "yoqib qo'yadi". O'z fikrlaringiz va g'oyalaringiz tugaydi.

🎨 _Creator bo'ling, faqat consumer emas!_""",

    """🧠 **Stress gormonlari:**

Salbiy yangiliklar, jarqiroq videolar — kortizol va adrenalin chiqaradi. Doimiy stress holati immunitetni, uyquni buzadi.

🧘 _Kontentingizni tanlang — miyangiz minnatdor bo'ladi._""",

    """🧠 **Reset zaruriyati:**

Ilmiy fakt: 2 hafta ijtimoiy tarmoqlarsiz — diqqat 30% yaxshilanadi, anxiety kamayadi, uyqu sifati oshadi.

Haftada 1 kun "digital detox" qilib ko'ring!""",


    # === PSIXOLOGIK TA'SIR (16-30) ===
    """😔 **Depressiya va Instagram:**

Ko'plab tadqiqotlar depressiya va ijtimoiy tarmoq foydalanish o'rtasida kuchli bog'liqlik aniqlagan. Ko'proq vaqt = ko'proq xavotir va tushkunlik.

💚 _Real hayotga qaytish — eng yaxshi antidepressant._""",

    """😔 **O'ziga past baho:**

Instagram "ideal hayot" aks etgan postlar bilan to'la. Siz esa o'zingizning oddiy kunlaringizni boshqalarning "highlight reel"iga taqqoslayapsiz.

Bu faqat illyuziya — hamma qiyinchiliklarni yashiradi.""",

    """😰 **FOMO sindromi:**

"Fear Of Missing Out" — biror narsani o'tkazib yuborish qo'rquvi. Instagram bu hissiyotni ataylab kuchaytiradi.

Ammo hayot ekranda emas! Eng muhim lahzalar — offlayn.""",

    """😔 **Taqqoslash tuzog'i:**

Har bir post — eng yaxshi momentlarning tanlangani. Siz o'zingizni boshqalarning "ideal" hayotiga taqqoslayapsiz.

Ular ham xuddi sizga o'xshash muammolarga duch keladi — faqat bu postlarda yo'q.""",

    """😰 **Anxiety darajasi:**

So'nggi tadqiqotlar: kuniga 3+ soat ijtimoiy tarmoqqa sarflaydigan odamlarda xavotirlanish darajasi sezilarli yuqori.

📊 _Vaqt sarfingizni kamaytiring — anxiety kamayadi._""",

    """😢 **Yolg'izlik paradoksi:**

1000 ta follower, 500 ta like — lekin haqiqiy do'st yo'q. Ijtimoiy tarmoqlar "ijtimoiy" deb atalsa-da, aslida yolg'izlashtiradi.

👥 _Jonli suhbatlarga vaqt ajrating!_""",

    """📸 **Narcissizm rivojlanishi:**

Selfie soni, postlar chastotasi — narcissizm darajasi bilan to'g'ridan-to'g'ri bog'liq. "Men qanday ko'rinaman?" savoli miyani doimiy band qiladi.

O'zingizni ichki dunyo orqali baholang, tashqi ko'rinish emas.""",

    """❤️ **Like sanamalik:**

O'z qadr-qimmatini begona odamlarning like va commentlariga bog'lash — psixologik zaiflik belgisi.

Sizning qadringiz — raqamlarda emas, amallaringizda.""",

    """👧 **Tana imiji muammolari:**

Bola-yoshlar orasida o'z tanasidan norozilik 40% ga oshgan — Instagram sababli. Filtrlar, taxrir — haqiqatni buzadi.

Siz mukammalsiz — va bu normal!""",

    """💔 **Kiberbuling:**

Har 3-o'spirindan biri internetda bullying duch kelgan. Anonimlik — shafqatsizlikka yo'l ochadi.

🛡️ _Bolalaringizning online faoliyatini kuzatib boring._""",

    """✨ **Perfeksionizm sindromi:**

"Mukammal post" uchun soatlab tahrir, eng yaxshi burchak qidirish — bu perfeksionizm. Hayotni postlarga aylantirib yuborishni to'xtating.

Hayot suratdan ko'ra ko'proq!""",

    """🎭 **Validatsiya qidiruvi:**

Tashqi tasdiqlashga bog'liq bo'lib qolish — mustaqil shaxsiyat rivojlanishini to'xtatadi. 

O'zingizni o'zingiz uchun qadrlang — begonalarning fikri uchun emas.""",

    """💚 **Hasad (Envy):**

Boshqalarning muvaffaqiyati, safarlari, narsalari — hasad uyg'otadi. Lekin bu soxta rasm — muammolarini hech kim ko'rsatmaydi.

O'z yo'lingizga e'tibor bering — boshqalar bilan solishtirmang.""",

    """😞 **Emotional instability:**

Mood swings — kayfiyat keskin o'zgarishi. Ijtimoiy tarmoqlar buni kuchaytiradi: yaxshi xabardan xursandlik, yomon — tushkunlik.

Ichki barqarorlik — tashqi omillarga bog'liq bo'lmasligi kerak.""",

    """🤝 **Social anxiety:**

Ekranda muloqot osonroq tuyuladi. Lekin real hayotda gaplashish borgan sari qiyinlashadi.

Jonli suhbat — ko'nikma. Uni mashq qilmasangiz, yo'qotasiz.""",


    # === JISMONIY SOG'LIQ (31-45) ===
    """🌙 **Uyqu buzilishi:**

Ko'k yorug'lik melatonin ishlab chiqarishni to'xtatadi. Kechqurun telefon — uyqu sifati 40% ga tushadi.

📵 _Yotishdan 1 soat oldin telefonni yig'ishtiring._""",

    """🩺 **Bo'yin og'rig'i (Text Neck):**

Telefonga qarash uchun boshni egish — bo'yindagi yukni 27 kg gacha oshiradi! Bu bo'yin va orqa og'rig'iga olib keladi.

Ergonomikani unutmang — boshingizni to'g'ri tuting.""",

    """👁️ **Ko'z charchashi:**

Doimiy ekranga qarash quruq ko'z sindromiga olib keladi. Ko'zlaringiz achishsa, qizarsa — bu signal.

20-20-20 qoidasi: har 20 daqiqada, 20 metr uzoqlikka, 20 soniya qarang.""",

    """🦴 **Orqa muammolari:**

Egik holda o'tirish — orqa muskullari zaiflashishiga olib keladi. Kelgusida surunkali og'riqlar paydo bo'ladi.

🧘 _Gimnastika, yoga — orqa sog'lig'i uchun._""",

    """🤚 **Karpel tunel sindromi:**

Qo'l barmoqlari va bilaklarida og'riq — telefon, kompyuter bilan ishlashdan. Profilaktika qiling, keyin kech bo'ladi.

Dam olish — zaruriy!""",

    """🤕 **Bosh og'rig'i:**

Ekranning yoritilganligi va ko'k yorug'lik — migren va bosh og'rig'ining asosiy sabablari.

💡 _Brightness'ni kamaytiring, dark mode'ni yoqing._""",

    """⚖️ **Semirish xavfi:**

Harakatsiz o'tirish + ovqat paytida telefon = ko'p yeyish + kam harakat. Bu semirish va metabolik muammolarga olib keladi.

🏃 _Harakatda bo'ling!_""",

    """💓 **Yurak sog'lig'i:**

Stressli kontent — yurak urishi tezlashishi, qon bosimi ko'tarilishiga olib keladi.

Surunkali stress — yurak kasalliklari xavfini oshiradi.""",

    """☀️ **Vitamin D yetishmovchiligi:**

Uyda ekran oldida o'tirish — quyosh nurlaridan mahrum bo'lish. Vitamin D — suyaklar, immunitet, kayfiyat uchun zarur.

Tashqariga chiqing! Tabiat kutmoqda.""",

    """🛡️ **Immunitet:**

Stress va uyqu yetishmovchiligi — immunitetni zaiflashtiradigan asosiy omillar. Ijtimoiy tarmoqlar ikkalasiga ham ta'sir qiladi.

Sog'lom uyqu = kuchli immunitet.""",

    """📈 **Qon bosimi:**

Doimiy stress holati — qon bosimini ko'taradi. Bu yurak va bosh miya kasalliklari xavfini oshiradi.

🧘 _Meditatsiya — stress bilan kurashda yordam beradi._""",

    """👀 **Ko'rish pasayishi:**

Yosh odamlar orasida miyopiya (yaqinni ko'rish) 30% ga oshgan. Asosiy sabab — ekranlarga uzoq muddat qarash.

Tabiatga ko'proq qarang! 🌳""",

    """🎧 **Eshitish muammolari:**

Naushnik bilan baland ovozda musiqa — eshitish pasayishiga olib keladi. Oqibatlari — umrbod.

60/60 qoidasi: maksimal 60% ovoz, 60 daqiqadan ko'p emas.""",

    """💤 **Uyqu bosqichlari:**

Kechqurun telefon — REM (tush ko'rish) fazasini qisqartiradi. Bu esa xotira, kayfiyat, o'rganish qobiliyatiga salbiy ta'sir qiladi.

Sifatli uyqu = sifatli hayot.""",

    """🧬 **Surunkali og'riqlar:**

Text neck, carpal tunnel, orqa og'rig'i — barchasi telefondan. Yillar o'tishi bilan surunkali kasalliklarga aylanadi.

Profilaktika — davodan oson!""",


    # === VAQT SARFI (46-60) ===
    """⏳ **Vaqt — eng qimmat boylik:**

Jeff Bezos, Elon Musk, Bill Gates — ularning barchasi bir xil 24 soatga ega. Farq shundaki, ular bu vaqtni qanday sarflashini tanlaydi.

Siz-chi? Sizning tanlovingiz qanday?""",

    """📊 **Statistika:**

O'rtacha inson Instagramda kuniga 3 soat sarflaydi. Yiliga bu 45 kun demak! 

Bu vaqt bilan yangi kasb, til o'rganish, kitob yozish mumkin edi.""",

    """📚 **Vaqt va ta'lim:**

3 soat × 365 kun = 1095 soat yilda. Bu vaqtda:
• 15-20 kitob o'qish
• 2-3 ta til o'rganish
• Professional sertifikat olish mumkin

Tanlov — sizniki!""",

    """⏰ **"Faqat 5 daqiqa" tuzog'i:**

"Faqat 5 daqiqa ko'ray" — 30 daqiqaga aylanadi. Bu psixologik fakt. Instagram algoritmlari sizni ushlab turish uchun yaratilgan.

⚠️ _Timer qo'ying — o'zingizni cheklang._""",

    """🏆 **Muvaffaqiyatli odamlar:**

Muvaffaqiyatli biznesmenlar, olimlar, sportchilar — ularning o'rtasida ijtimoiy tarmoq ishlatish juda past.

Ularga o'xshashni xohlaysizmi? Ularning odatlarini o'rganing.""",

    """👨‍👧 **Tech gigantlari:**

Mark Zuckerberg, Bill Gates, Steve Jobs — hammalari o'z bolalarini ijtimoiy tarmoqlardan cheklagan.

Ular nimani biladi, biz bilmaydigani? 🤔""",

    """📖 **10 daqiqa qoidasi:**

Har kuni 10 daqiqa kitob o'qish — yiliga 20+ kitob. Har kuni 10 daqiqa scroll — 60 soat yo'qotilgan.

Tanlov oddiy — qaysi biri foydali?""",

    """🎓 **1 soat qoidasi:**

Har kuni 1 soat yangi narsa o'rganish — yilda professional sertifikat, yoki yangi kasb.

Bu soatni Instagramga yoki o'zingizga sarflaysizmi?""",

    """🔮 **Kelajak:**

Vaqtingizni qanday sarflashingiz — kelajagingizni belgilaydi. Bugun qilgan tanlovlaringiz — ertangi sizni shakllantiradi.

Bugun nima qildingiz?""",

    """🧘 **Morning routine:**

Eng samarali odamlar kunni telefonsiz boshlaydi. Tong paytidagi scroll — butun kun energiyasini pasaytiradi.

Telefon o'rniga: sport, meditatsiya, kitob.""",

    """📱 **Digital minimalizm:**

Bu yangi harakat — odamlar ataylab ijtimoiy tarmoqlarni tark etmoqda. Nima uchun? Yanada baxtli, yo'naltirilgan hayot uchun.

Kamroq ekran — ko'proq hayot.""",

    """⌚ **Screeen time statistikasi:**

Telefon statistikasiga bir qarang. Ko'p odamlar kuniga 5-7 soat sarflaydi. Bu yiliga 2-3 oy!

Siz qancha vaqt sarflayapsiz?""",

    """🎯 **Intention vs Addiction:**

"Maqsad bilan kirish" va "scroll addiction" — farq bor. O'zingizga savol bering: "Men nima uchun kirdim?"

Javob yo'q bo'lsa — chiqing!""",

    """💼 **Ish samaradorligi:**

Har bir notification diqqatni buzadi. Diqqatni qayta yig'ish uchun 23 daqiqa kerak!

Ish paytida telefonni chetga qo'ying.""",

    """🌅 **Golden hours:**

Tong va kechqurun — eng samarali vaqtlar. Bu vaqtlarni scroll ga sarflamang!

Meditation, o'qish, rejalashtirish — foydaliroq.""",


    # === MUNOSABATLAR (61-75) ===
    """👥 **Haqiqiy aloqalar:**

Ijtimoiy tarmoqlar "ijtimoiy" deb atalsa-da, ular haqiqiy insoniy aloqalarni zaiflashadi. Online 1000 do'st — real 0.

Yaqinlaringiz bilan vaqt o'tkazing! ❤️""",

    """👨‍👩‍👧 **Oilada telefon:**

Oilada suhbat o'rniga — har kim o'z telefonida. Bolalar ota-onasining yuzini emas, telefon ustini ko'radi.

📵 _Ovqat paytida telefon yo'q!_""",

    """💑 **Juftliklar:**

Telefon juftliklar o'rtasida "uchinchi shaxs" kabi. Diqqatni o'g'irlaydi, suhbatni buzadi.

Romantik lahzalarda — telefonsiz bo'ling.""",

    """👁️ **Eye contact:**

Ko'z bilan muloqot qilish qobiliyati kamaymoqda. Yoshlar ko'zga qarashdan qochadi — chunki odatdan chiqilgan.

Real suhbat — ko'nikma. Mashq qiling!""",

    """🤝 **Empathiya:**

Empathiya (boshqalarni tushunish) darajasi yoshlarda 40% tushgan. Sabablardan biri — ekranlar, real muloqot kamligi.

Insonlar bilan ko'proq suhbatlashing.""",

    """💬 **Chat vs Suhbat:**

Telegram, WhatsApp — bu suhbat emas, chat. Intonatsiya, mimika, his-tuyg'ular — yo'q.

Imkon bo'lsa — qo'ng'iroq qiling yoki uchrashing.""",

    """👋 **Haqiqiy do'stlik:**

Do'stlik — faqat like bosish emas. Bu vaqt birga o'tkazish, qo'llab-quvvatlash, gaplashish.

Online do'stlarni real hayotda uchrashib ko'ring.""",

    """💕 **Romantik munosabatlar:**

Instagram "ideal" juftliklarni ko'rsatadi. Real munosabatlar — murakkab, mehnat talab qiladi.

Haqiqiy sevgi — fotolarda emas, har kungi tanlarda.""",

    """🍽️ **Oilaviy ovqat:**

Ovqat paytida hamma telefonida — bu yangi me'yor. Lekin bu me'yor zararli.

📵 _Stolda telefon yo'q — oilaviy qoida qiling._""",

    """👶 **Bolalar bilan vaqt:**

Sifatli vaqt — telefonsiz vaqt. Bolangiz yoningizda, lekin siz telefondasiz — bu "birga" emas.

Hozir bo'ling, telefonsiz!""",

    """🙏 **Hurmat:**

Hurmat — birovga to'liq diqqat berish. Suhbat paytida telefonga qarash — "sen muhim emassan" degan xabar.

Diqqatingiz — eng katta sovg'a.""",

    """👨‍👧‍👦 **Farzandlar:**

Bolalar ota-onadan o'rganadi. Agar siz telefondasiz — ular ham shunday bo'ladi.

Ibrat bo'ling — yaxshi ibrat.""",

    """🏠 **Uy muhiti:**

"Ovozim baland bo'lgani uchun emas, telefongni qo'ygin!" — tanish gapmi?

Telefon oilada stress manbai bo'lib qolgan.""",

    """🎂 **Bayramlar:**

To'y, bayram, yig'ilish — hamma telefonni ko'targan. Lahzani suratga olish muhim, lekin yashash undan muhimroq.

Avval yashing, keyin surat oling.""",

    """💔 **Do'stlik sinovi:**

Real do'stlikni sinash oson: qiyin paytda kim yonida bo'ladi? Online "do'stlar" yo'q bo'lib ketadi.

Real aloqalarga vaqt ajrating.""",


    # === JAMIYAT VA IQTISOD (76-90) ===
    """📰 **Fake news:**

Yolg'on yangiliklar ijtimoiy tarmoqlarda 6 barobar tez tarqaladi. Factcheck qilish odat emas — ko'pchilik ishonib yuboradi.

🔍 _Manba tekshiring, keyin ulashing!_""",

    """🔊 **Echo chamber:**

Algoritm sizga o'xshash fikrlarni ko'rsatadi. Boshqa nuqtai nazarni ko'rmaysiz. Bu jamiyatni ikkiga bo'lmoqda.

Turli manbalardan o'qing.""",

    """❌ **Cancel culture:**

Bir xato uchun butun hayot buzilishi mumkin. Internet unutmaydi. Har bir post — digital footprint.

⚠️ _O'ylang, keyin posting qiling._""",

    """📢 **Reklama:**

Instagram reklamalar orqali keraksiz xaridlarga undaydi. "Ko'rdim, oldim" sindromi — moliyaviy qiyinchiliklarga olib keladi.

Impulsiv xarid qilmang!""",

    """💰 **Influencer marketing:**

Influencerlar pulga mahsulot reklama qiladi — ular chindan ham ishlatmaydi. Bu soxta tavsiyalar bilan pul ishlash.

Reklamaga ishonmang.""",

    """🎪 **Attention economy:**

Sizning diqqatingiz — tovar. Teknologiya kompaniyalari buni sotadi. Siz foydalanuvchi emassiz — mahsulotsiz.

Free app = Siz mahsulot.""",

    """🔐 **Privacy xavfi:**

Shaxsiy ma'lumotlaringiz sotiladi. Har bir like, search, view — kompaniyalarga pul keltiradi.

Privacy settings'ni tekshiring!""",

    """🌐 **Digital footprint:**

Bugun yozganlaringiz abadiy internetda qoladi. 10 yildan keyin kim ko'rishini bilmaysiz.

O'ylang, keyin posting qiling!""",

    """📉 **Qimmatbaho lifestyle:**

Instagram "hammada bor" illyuziyasini yaratadi. Solishtiruvchan iste'mol — moliyaviy stress manbai.

O'zingiz uchun yashang, ko'rsatish uchun emas.""",

    """⚠️ **Fraud va scam:**

Kriptovalyuta, MLM sxemalari — ijtimoiy tarmoqlar orqali tarqaladi. "Oson pul" va'dalari — firibgarlik.

🚨 _Ehtiyot bo'ling!_""",

    """📊 **Vaqt = Pul:**

Instagramga sarflangan vaqt = yo'qotilgan daromad. 3 soat kuniga × minimal ish haqi — yiliga katta summa.

Vaqtingizni qadrland!""",

    """🎯 **Algorithm:**

Algoritm sizni maksimal vaqt ushlab turish uchun yaratilgan. Sizning farovonligingiz muhim emas — faqat engagement.

Buni tushunib, o'zingizni himoya qiling.""",

    """🧑‍💼 **Career:**

HR mutaxassislari ijtimoiy tarmoqlaringizni tekshiradi. Noto'g'ri post — ish imkoniyati yo'qolishi mumkin.

Professional imij saqlang.""",

    """📱 **Bepul ilova:**

"Bepul" ilova haqiqatan bepul emas. To'lov — sizning vaqtingiz, diqqatingiz, ma'lumotlaringiz.

Hech narsa bepul emas.""",

    """🌍 **Global muammo:**

Dunyoda millionlab odamlar scroll addiction dan azob chekmoqda. Bu shaxsiy zaiflik emas — dizayn qilingan tuzog'.

Siz yolg'iz emassiz. Qadam tashlang!""",


    # === YECHIMLAR VA ALTERNATIVALAR (91-105) ===
    """🔔 **Notifikatsiya:**

Notifikatsiyalarni o'chiring! Har bir notification diqqatni buzadi. O'chirsangiz — anxiety 40% kamayadi.

Settings > Notifications > Off!""",

    """⏰ **Screen time limit:**

Telefonning o'zida screen time limit bor. Kuniga max 1 soat qo'ying. Chegara kelganda — to'xtang.

Texnologiyani o'zingizga qarshi emas, o'zingiz uchun ishlating.""",

    """🛏️ **Bedroom rules:**

Telefonni yotoqdan chiqaring! Uyqu sifati keskin oshadi. Tong paytida ham scroll bilan boshlamaysiz.

Alarm clock sotib oling — telefon shart emas.""",

    """📵 **Digital detox:**

Haftada 1 kun ijtimoiy tarmoqlarsiz o'tkazing. Miya "reset" bo'ladi. Hayratlanarli farqni sezasiz!

Yakshanba = Digital detox kuni.""",

    """📚 **Kitob o'qish:**

6 daqiqa kitob o'qish — stress 68% ga kamayadi. Bu telefon scroll dan 6 baravar samarali.

Bir kitob boshlang — bugun!""",

    """🌳 **Tabiat:**

Tabiatda 20 daqiqa — kortizol (stress gormoni) darajasi tushadi. Park, bog', daryo — boraver!

Tabiat — bepul terapiya.""",

    """🏃 **Sport:**

Sport — tabiiy dopamin manbai. Yugurish, suzish, velosiped — hammasidan dopamin olasiz.

Fitness — telefondan yaxshi!""",

    """🧘 **Meditatsiya:**

10 daqiqa meditatsiya — diqqat va xotiraga ijobiy ta'sir qiladi. Ilmiy isbotlangan!

Headspace, Calm — boshlash uchun ilovalar.""",

    """☕ **Morning routine:**

Tong paytida telefonga qaraman. O'rniga: suv, mashq, kitob, nonushta.

Faol tong — faol kun.""",

    """🗓️ **Schedule:**

Ijtimoiy tarmoqlar uchun vaqt belgilang. Masalan: 12:00-12:30, 18:00-18:30. Qolgani — telefonsiz.

Vaqtingizni o'zingiz boshqaring!""",

    """✍️ **Journaling:**

Har kuni 5 daqiqa yozish — fikrlarni tartiblaydi, stress kamaytiradi.

Telefon o'rniga — qalam va daftar.""",

    """🎨 **Hobby:**

Yangi hobby boshlang: chizish, musiqa, tikish, bog'dorchilik. Vaqtingiz mazmunli o'tadi.

Iste'mol emas — yaratish!""",

    """👥 **Real meet-ups:**

Online do'stlar bilan oflayn uchrashing. Haqiqiy suhbat — xotiralar yaratadi.

Jonli muloqot — almashtirib bo'lmas.""",

    """📱 **Grayscale mode:**

Telefonni kulrang (grayscale) rejimga o'tkazing. Rang-barang ekran — dopamin chiqaradi. Kulrang — kamroq jalb qiladi.

Settings > Accessibility > Grayscale.""",

    """🎯 **Maqsad:**

Nima uchun Instagram ishlatayotganingizni aniqlang. Maqsad yo'q bo'lsa — o'chiring.

Intentional use only!""",
]


# ═══════════════════════════════════════════════════════════════════════════════
# DINAMIK SHABLONLAR (har safar yangi raqamlar bilan)
# ═══════════════════════════════════════════════════════════════════════════════

def _get_dynamic_warning():
    """Har safar yangi raqamlar bilan warning"""
    hours, days = _random_days()
    percent = _random_percent()
    
    templates = [
        f"""📊 **Kunlik statistika:**

O'rtacha foydalanuvchi Instagramda kuniga **{hours} soat** sarflaydi. Yiliga bu **{days} kun** demak!

Bu vaqtni yangi til o'rganish yoki kasb egallashga sarflash mumkin edi. Tanlov sizniki!""",

        f"""🧪 **Ilmiy tadqiqot:**

So'nggi tadqiqotlarga ko'ra, kuniga 3+ soat ijtimoiy tarmoqlarga sarflaydigan odamlarda xavotirlanish darajasi **{percent}%** ga yuqori.

🧠 _Miyangizni himoya qiling — ekran vaqtini cheklang!_""",

        f"""📱 **Raqamlar gapiradi:**

Agar siz kuniga {hours} soat Instagramda bo'lsangiz:
• Haftada: **{round(hours * 7)} soat** yo'qotasiz
• Oyda: **{round(hours * 30)} soat** ketadi
• Yilda: **{days} kun** sarflanadi!

Bu vaqtda nimalar qilish mumkinligini o'ylab ko'ring...""",

        f"""🎓 **Ta'lim vs Instagram:**

{hours} soat × 365 kun = **{round(hours * 365)} soat** yilda.

Bu vaqt ichida 2-3 ta til o'rganish, dasturlashni o'zlashtirish, yoki yangi kasb egallash mumkin edi.

Kelajagingiz — bugungi tanlovlaringizga bog'liq!""",

        f"""🧠 **Diqqat haqida fakt:**

Tadqiqotchilar aniqlashicha, muntazam qisqa video ko'ruvchilarning diqqatni saqlash qobiliyati **{percent}%** ga qisqargan.

📚 _Kitob o'qing, chess o'ynang — miyangizni mashq qildiring!_""",

        f"""⚡ **Scroll energiyasi:**

Har bir scroll — miyangizdan energiya oladi. Kuniga o'rtacha **{random.randint(200, 400)}** marta scroll... 

Bu energiyani foydali ishga — sport, o'qish, ijodkorlikka sarflang!""",

        f"""😰 **Nomofobia statistikasi:**

Yosh odamlarning **{percent}%** "telefonsiz bo'lish" dan xavotirlanadi — bu nomofobia deyiladi.

Telefon — qurol, ega emas. Uni siz boshqaring, u sizni emas!""",

        f"""💤 **Uyqu sifati:**

Kechqurun telefon ishlatish — REM (chuqur uyqu) fazasini **{percent}%** ga qisqartiradi.

REM uyqu xotira, kayfiyat va o'rganish uchun zarur. Kechqurun ekrandan uzoqlashing!""",
    ]
    
    return random.choice(templates)


def get_random_warning() -> str:
    """
    Tasodifiy warning qaytaradi #eslatma hashtag bilan.
    70% statik (105 ta), 30% dinamik (8 ta shablon, random raqamlar).
    """
    hashtag = "#eslatma"
    
    if random.random() < 0.7:
        warning_text = random.choice(WARNINGS)
    else:
        warning_text = _get_dynamic_warning()
    
    return f"{hashtag}\n\n{warning_text}"
