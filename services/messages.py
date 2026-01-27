import random

WARNING_MESSAGES = [
    """⚠️ **Diqqat! Instagram va qisqa videolar zararlari:**
    
🧠 **Dopamin qopqoni:** Qisqa videolar (Reels, Shorts) miyangizda doimiy "yangilik" hissini uyg'otib, sun'iy dopamin chiqarishga majbur qiladi. Bu esa diqqatni jamlash qobiliyatini pasaytiradi va xotirani susaytiradi.""",

    """⚠️ **Vaqtingizni qadrlang!**
    
⏳ Instagramga kirib, soatlab vaqt yo'qotganingizni sezmay qoldingizmi? Bu tasodif emas. Ilova algoritmlari sizni imkon qadar uzoqroq ushlab turish uchun yaratilgan. Bu vaqtni ilm olish yoki yaqinlaringiz bilan suhbatlashishga sarflashingiz mumkin edi.""",

    """⚠️ **Dunyo tajribasi:**
    
🚫 Xitoyda TikTok va shu kabi ilovalar yoshlar uchun qat'iy cheklangan (kuniga 40 daqiqa). Chunki ular bu ilovalar kelajak avlodining aqliy salohiyatini "zombilashtirishi"dan xavotirda. Bizchi? Biz o'z kelajagimizga befarq emasmizmi?""",

    """⚠️ **Psixologik ta'sir:**
    
depressiya, xavotir va o'ziga past baho berish — bularning barchasi "ideal hayot" aks etgan videolarni ko'p tomosha qilish oqibatidir. Hayot Instagramdagi kabi silliq va benuqar emas. O'z hayotingizni seving, birovlarnikini kuzatishni bas qiling.""",
    
    """⚠️ **Eslatma:**
    
Qisqa videolar ko'rishni to'xtatish — chekishni tashlash bilan barobar qiyin bo'lishi mumkin. Lekin bu sizning miyangiz va kelajagingiz uchun eng to'g'ri qaror. Bugun telefondan bosh ko'taring va atrofga qarang!"""
]

def get_random_warning() -> str:
    return random.choice(WARNING_MESSAGES)
