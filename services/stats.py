"""
Bot Statistics Module
---------------------
Anonim statistika yig'adi - shaxsiy ma'lumotlarni saqlamaydi.
Faqat hashed user_id lar orqali unique userlarni hisoblaydi.
"""

import os
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Optional
import threading

# Thread-safe database access
_db_lock = threading.Lock()

# Database path - Railway uchun /data papkasida bo'ladi
DB_PATH = os.getenv('STATS_DB_PATH', 'data/stats.db')


def _get_connection():
    """SQLite connection olish"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Database va jadvallarni yaratish"""
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        
        # Unique users jadval (faqat hashed ID lar)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_hash TEXT PRIMARY KEY,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Requests jadval (umumiy statistika)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_hash TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN,
                request_type TEXT DEFAULT 'video_download'
            )
        ''')
        
        # Daily summary jadval (tez statistika uchun)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT PRIMARY KEY,
                total_requests INTEGER DEFAULT 0,
                successful INTEGER DEFAULT 0,
                failed INTEGER DEFAULT 0,
                unique_users INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()


def _hash_user_id(user_id: int) -> str:
    """User ID ni hash qilish - shaxsiy ma'lumot saqlanmaydi"""
    # Salt qo'shib hash qilish
    salt = os.getenv('STATS_SALT', 'instagram_guard_bot_2024')
    data = f"{salt}:{user_id}".encode()
    return hashlib.sha256(data).hexdigest()[:16]


def track_request(user_id: int, success: bool, request_type: str = 'video_download'):
    """
    Requestni saqlash
    - user_id hash qilinadi (anonim)
    - success/fail holati
    - request turi
    """
    user_hash = _hash_user_id(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        
        try:
            # Yangi user bo'lsa qo'shish
            cursor.execute(
                'INSERT OR IGNORE INTO users (user_hash) VALUES (?)',
                (user_hash,)
            )
            
            # Request yozish
            cursor.execute(
                'INSERT INTO requests (user_hash, success, request_type) VALUES (?, ?, ?)',
                (user_hash, success, request_type)
            )
            
            # Daily stats yangilash
            cursor.execute('''
                INSERT INTO daily_stats (date, total_requests, successful, failed, unique_users)
                VALUES (?, 1, ?, ?, 1)
                ON CONFLICT(date) DO UPDATE SET
                    total_requests = total_requests + 1,
                    successful = successful + ?,
                    failed = failed + ?
            ''', (today, 1 if success else 0, 0 if success else 1, 
                  1 if success else 0, 0 if success else 1))
            
            conn.commit()
        finally:
            conn.close()


def get_stats() -> dict:
    """
    Umumiy statistika olish
    Returns dict with all statistics
    """
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        
        try:
            # Jami unique userlar
            cursor.execute('SELECT COUNT(*) as count FROM users')
            total_users = cursor.fetchone()['count']
            
            # Jami requestlar
            cursor.execute('SELECT COUNT(*) as count FROM requests')
            total_requests = cursor.fetchone()['count']
            
            # Muvaffaqiyatli/Muvaffaqiyatsiz
            cursor.execute('SELECT COUNT(*) as count FROM requests WHERE success = 1')
            successful = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM requests WHERE success = 0')
            failed = cursor.fetchone()['count']
            
            # Bugun
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                'SELECT COUNT(*) as count FROM requests WHERE DATE(timestamp) = ?',
                (today,)
            )
            today_requests = cursor.fetchone()['count']
            
            cursor.execute(
                'SELECT COUNT(DISTINCT user_hash) as count FROM requests WHERE DATE(timestamp) = ?',
                (today,)
            )
            today_users = cursor.fetchone()['count']
            
            # Oxirgi 7 kun
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            cursor.execute(
                'SELECT COUNT(*) as count FROM requests WHERE DATE(timestamp) >= ?',
                (week_ago,)
            )
            week_requests = cursor.fetchone()['count']
            
            cursor.execute(
                'SELECT COUNT(DISTINCT user_hash) as count FROM requests WHERE DATE(timestamp) >= ?',
                (week_ago,)
            )
            week_users = cursor.fetchone()['count']
            
            # Oxirgi 30 kun
            month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            cursor.execute(
                'SELECT COUNT(*) as count FROM requests WHERE DATE(timestamp) >= ?',
                (month_ago,)
            )
            month_requests = cursor.fetchone()['count']
            
            cursor.execute(
                'SELECT COUNT(DISTINCT user_hash) as count FROM requests WHERE DATE(timestamp) >= ?',
                (month_ago,)
            )
            month_users = cursor.fetchone()['count']
            
            # Success rate
            success_rate = (successful / total_requests * 100) if total_requests > 0 else 0
            
            # Eng faol soatlar (oxirgi 7 kun)
            cursor.execute('''
                SELECT strftime('%H', timestamp) as hour, COUNT(*) as count 
                FROM requests 
                WHERE DATE(timestamp) >= ?
                GROUP BY hour 
                ORDER BY count DESC 
                LIMIT 3
            ''', (week_ago,))
            peak_hours = [row['hour'] for row in cursor.fetchall()]
            
            return {
                'total_users': total_users,
                'total_requests': total_requests,
                'successful': successful,
                'failed': failed,
                'success_rate': round(success_rate, 1),
                'today': {
                    'requests': today_requests,
                    'users': today_users
                },
                'week': {
                    'requests': week_requests,
                    'users': week_users
                },
                'month': {
                    'requests': month_requests,
                    'users': month_users
                },
                'peak_hours': peak_hours
            }
        finally:
            conn.close()


def format_stats_message(stats: dict) -> str:
    """Statistikani chiroyli format qilish"""
    peak_hours_str = ', '.join([f"{h}:00" for h in stats['peak_hours']]) if stats['peak_hours'] else "Ma'lumot yo'q"
    
    return f"""📊 **Bot Statistikasi**

👥 **Foydalanuvchilar:**
├ Jami: **{stats['total_users']}** ta unique user
├ Bugun: **{stats['today']['users']}** ta
├ Oxirgi 7 kun: **{stats['week']['users']}** ta
└ Oxirgi 30 kun: **{stats['month']['users']}** ta

📥 **So'rovlar:**
├ Jami: **{stats['total_requests']}** ta
├ Bugun: **{stats['today']['requests']}** ta
├ Oxirgi 7 kun: **{stats['week']['requests']}** ta
└ Oxirgi 30 kun: **{stats['month']['requests']}** ta

✅ **Natijalar:**
├ Muvaffaqiyatli: **{stats['successful']}** ta
├ Muvaffaqiyatsiz: **{stats['failed']}** ta
└ Success rate: **{stats['success_rate']}%**

⏰ **Eng faol soatlar:** {peak_hours_str}

🔒 _Barcha ma'lumotlar anonim. Shaxsiy ma'lumotlar saqlanmaydi._"""
