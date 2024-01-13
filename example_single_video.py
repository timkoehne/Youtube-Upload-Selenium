import datetime
from youtube_upload import (
    Video,
    upload_single_video,
)

# in windows firefox profiles are saved at C:/Users/\<user\>/AppData/Roaming/Mozilla/Firefox/Profiles/
firefox_profile_path = "path_to_firefox_profile"

upload_date_time = datetime.datetime.strptime(
    "13.01.2024 12:00", "%d.%m.%Y %H:%M"
)

vid = Video("title0", "description0", "thumbnail_file_path0", "video_file_path0", ["tag0", "tag1"], "en", upload_date_time)

upload_single_video(vid, firefox_profile_path, headless=True)
