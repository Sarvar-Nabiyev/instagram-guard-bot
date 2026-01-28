import os
import glob
import logging
import tempfile
import yt_dlp

logger = logging.getLogger(__name__)

from typing import Optional


def _create_cookies_file() -> Optional[str]:
    """
    Create a Netscape format cookies file from environment variables.
    Returns path to the cookies file or None if cookies not configured.
    """
    session_id = os.getenv('INSTAGRAM_SESSION_ID')
    csrf_token = os.getenv('INSTAGRAM_CSRF_TOKEN', '')
    ds_user_id = os.getenv('INSTAGRAM_DS_USER_ID', '')
    mid = os.getenv('INSTAGRAM_MID', '')
    
    if not session_id:
        logger.warning("INSTAGRAM_SESSION_ID not set, cookies won't be used")
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
    
    logger.info(f"Created cookies file at {cookies_file.name}")
    return cookies_file.name


def download_video(url: str, output_dir: str = "downloads") -> Optional[str]:
    """
    Downloads video from URL (Instagram, YouTube, etc.) using yt-dlp.
    Returns the path to the downloaded file or None if failed.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Clean up old files in downloads/ (optional, simple cleanup)
    # For production, might want a better cleanup strategy
    files = glob.glob(f"{output_dir}/*")
    for f in files:
        try:
            os.remove(f)
        except Exception:
            pass

    # Create cookies file for Instagram authentication
    cookies_file = _create_cookies_file()

    # Always use Instagram-specific mobile User-Agent logic
    # (Since we are now restricted to Instagram only per user request)
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
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
            
            # Simple check
            found_files = glob.glob(f"{output_dir}/{video_id}.*")
            if found_files:
                return found_files[0]
            return expected_path
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None
