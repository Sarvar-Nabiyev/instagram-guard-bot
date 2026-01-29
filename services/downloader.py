import os
import glob
import logging
import tempfile
import yt_dlp

logger = logging.getLogger(__name__)

from typing import Optional


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

def download_video(url: str, output_dir: str = "downloads") -> Optional[str]:
    """
    Downloads video from URL (Instagram, YouTube, etc.) using yt-dlp.
    Returns the path to the downloaded file or None if failed.
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
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': user_agent,
        },
    }
    
    # Add cookies if available
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id')
            ext = info.get('ext')
            
            expected_path = f"{output_dir}/{video_id}.{ext}"
            
            # Strict check: Validate file actually exists
            found_files = glob.glob(f"{output_dir}/{video_id}.*")
            if found_files and os.path.exists(found_files[0]):
                return found_files[0]
            
            # Fallback check for expected path
            if os.path.exists(expected_path):
                return expected_path
                
            # If we reached here, no file was found
            logger.warning(f"Download finished but no file found for {video_id}")
            return None
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None
