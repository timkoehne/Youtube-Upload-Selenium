import datetime
from youtube_upload import (
    Video,
    schedule_multiple_videos,
    upload_multiple_videos
)

# under windows these are saved in C:/Users/<user>/AppData/Roaming/Mozilla/Firefox/Profiles/
firefox_profile_path = "path_to_firefox_profile"

videos: list[Video] = [
    Video("title0", "description0", "thumbnail_file_path0", "video_file_path0"),
    Video("title1", "description1", "thumbnail_file_path1", "video_file_path1"),
    Video("title2", "description2", "thumbnail_file_path2", "video_file_path2")
]
first_upload_date_time = datetime.datetime.strptime(
    "13.01.2024 12:00", "%d.%m.%Y %H:%M"
)

#scheduling is optional. if videos are not scheduled they are published instantly
videos = schedule_multiple_videos(
    videos, first_upload_date_time, datetime.timedelta(hours=6)
)
upload_multiple_videos(videos, firefox_profile_path)
