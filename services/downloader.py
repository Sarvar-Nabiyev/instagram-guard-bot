import os
import glob
import logging
import tempfile
import random
import yt_dlp

logger = logging.getLogger(__name__)

from typing import Optional, List


def _get_proxy() -> Optional[str]:
    """
    Get proxy URL from environment variable.
    Supports multiple proxies (comma-separated) with random rotation.
    Format: http://user:pass@host:port or socks5://host:port
    """
    proxy_url = os.getenv('PROXY_URL', '')
    if not proxy_url:
        return None
    
    # Support multiple proxies separated by comma
    proxies = [p.strip() for p in proxy_url.split(',') if p.strip()]
    if not proxies:
        return None
    
    selected = random.choice(proxies)
    logger.info(f"Using proxy: {selected[:20]}...")
    return selected


def _create_cookies_file() -> Optional[str]:
    """
    Get path to cookies file.
    1. Checks if 'cookies.txt' exists in current directory.
    2. If not, tries to create from environment variables.
    Returns path to the cookies file or None.
    """
    # 1. Check local cookies.txt
    local_cookies = "cookies.txt"
    if os.path.exists(local_cookies):
        logger.info(f"Using local file: {local_cookies}")
        return local_cookies

    # 2. Fallback to Env Variables
    session_id = os.getenv('INSTAGRAM_SESSION_ID')
    csrf_token = os.getenv('INSTAGRAM_CSRF_TOKEN', '')
    ds_user_id = os.getenv('INSTAGRAM_DS_USER_ID', '')
    mid = os.getenv('INSTAGRAM_MID', '')
    
    if not session_id:
        logger.warning("No cookies.txt found and INSTAGRAM_SESSION_ID not set")
        return None
    
    # Create Netscape format cookies file
    cookies_content = """# Netscape HTTP Cookie File
# This file was generated for yt-dlp
.instagram.com	TRUE	/	TRUE	0	sessionid	{sessionid}
.instagram.com	TRUE	/	FALSE	0	csrftoken	{csrftoken}
.instagram.com	TRUE	/	FALSE	0	ds_user_id	{ds_user_id}
.instagram.com	TRUE	/	FALSE	0	mid	{mid}
""".format(
        sessionid=session_id,
        csrftoken=csrf_token,
        ds_user_id=ds_user_id,
        mid=mid
    )
    
    # Write to temp file
    cookies_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    cookies_file.write(cookies_content)
    cookies_file.close()
    
    logger.info(f"Created temp cookies file at {cookies_file.name}")
    return cookies_file.name


import random

USER_AGENTS = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
]

def download_video(url: str, output_dir: str = "downloads") -> Optional[dict]:
    """
    Downloads video from URL (Instagram, YouTube, etc.) using yt-dlp.
    Returns dict {'path': str, 'caption': str} or None if failed.
    """
    # Ensure output_dir is absolute to prevent CWD issues with Pyrogram
    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # REMOVED: Aggressive cleanup that deletes concurrent downloads
    # Each handler is responsible for deleting its own file after upload

    # Create cookies file for Instagram authentication
    cookies_file = _create_cookies_file()

    # Use random User-Agent for each request to avoid rate limits
    user_agent = random.choice(USER_AGENTS)
    logger.info(f"Using User-Agent: {user_agent}")

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
        'format': 'best[width<=640]/best[width<=720]/best',  # Filter by width for vertical videos
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': user_agent,
        },
    }
    
    # Add cookies if available
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    # Add proxy if configured
    proxy = _get_proxy()
    if proxy:
        ydl_opts['proxy'] = proxy

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id')
            ext = info.get('ext')
            
            expected_path = f"{output_dir}/{video_id}.{ext}"
            
            # Use glob to find the downloaded file (sometimes extension differs)
            found_files = glob.glob(f"{output_dir}/{video_id}.*")
            
            # Fallback check for expected path
            video_path = None
            if found_files and os.path.exists(found_files[0]):
                video_path = found_files[0]
            elif os.path.exists(expected_path):
                video_path = expected_path

            if video_path:
                # Get caption (title or description)
                caption = info.get('description') or info.get('title') or ""
                # Truncate caption to 1024 chars (Telegram limit)
                if len(caption) > 1024:
                    caption = caption[:1021] + "..."
                
                return {
                    'path': video_path,
                    'caption': caption
                }
                
            # If we reached here, no file was found
            logger.warning(f"Download finished but no file found for {video_id}")
            return None
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None


def download_audio(url: str, output_dir: str = "downloads") -> Optional[dict]:
    """
    Downloads audio from URL as MP3.
    Returns dict {'path': str, 'caption': str} or None if failed.
    """
    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cookies_file = _create_cookies_file()
    user_agent = random.choice(USER_AGENTS)

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': user_agent,
        },
    }
    
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    # Add proxy if configured
    proxy = _get_proxy()
    if proxy:
        ydl_opts['proxy'] = proxy

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id')
            
            # Expected path is .mp3 after conversion
            expected_path = f"{output_dir}/{video_id}.mp3"
            
            if os.path.exists(expected_path):
                caption = info.get('description') or info.get('title') or ""
                if len(caption) > 1024:
                    caption = caption[:1021] + "..."
                
                return {
                    'path': expected_path,
                    'caption': caption,
                    'performer': info.get('artist') or info.get('uploader') or "Instagram",
                    'title': info.get('track') or info.get('title') or "Audio"
                }
            
            logger.warning(f"Audio download finished but no file found for {video_id}")
            return None
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        return None
