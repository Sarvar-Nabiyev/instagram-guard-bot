import os
import glob
import logging
import yt_dlp

logger = logging.getLogger(__name__)

from typing import Optional

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

    # distinct options for Instagram vs YouTube
    if "instagram.com" in url:
        ydl_opts = {
            'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            },
        }
    else:
        # For YouTube and others, use default options (or specific ones if needed)
        # Avoid custom Mobile UA for YouTube as it triggers "Sign in" prompts
        # Limit to 1080p to save space and bandwidth
        ydl_opts = {
            'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'quiet': True,
            'no_warnings': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id')
            ext = info.get('ext')
            # yt-dlp might change extension (e.g. mkv -> mp4), so we locate the file
            # or just use the expected filename
            expected_path = f"{output_dir}/{video_id}.{ext}"
            
            # Search for the file if extension differs or unsure
            found_files = glob.glob(f"{output_dir}/{video_id}.*")
            if found_files:
                return found_files[0]
            return expected_path
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None
