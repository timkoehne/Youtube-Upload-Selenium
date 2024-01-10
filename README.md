# Youtube Uploader
This is a python module that uses [selenium webdriver](https://github.com/SeleniumHQ/selenium) to upload videos to youtube.

Since this uses selenium to nagivate the HTML of youtube, this WILL probably break when youtube updates their frontend. Last verified to work on 10 Jan 2024. 


# Requirements
- Firefox - tested on 121.0 but should work on most modern versions
- Python - tested on 3.10.13 but should work on most modern versions

- ```pip install selenium```

- be logged into the youtube-account with your firefox profile


# Usage

Uploading a single video
```python
import datetime
from youtube_upload import (
    Video,
    upload_single_video,
)

# under windows these are saved in C:/Users/<user>/AppData/Roaming/Mozilla/Firefox/Profiles/
firefox_profile_path = "path_to_firefox_profile"

upload_date_time = datetime.datetime.strptime(
    "13.01.2024 12:00", "%d.%m.%Y %H:%M"
)

vid = Video("title0", "description0", "thumbnail_file_path0", "video_file_path0", upload_date_time)

upload_single_video(vid, firefox_profile_path)
```


Uploading multiple videos and scheduling them
```python
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

#scheduling is optional
#if videos are not scheduled they are published instantly
videos = schedule_multiple_videos(
    videos, first_upload_date_time, datetime.timedelta(hours=6)
)
upload_multiple_videos(videos, firefox_profile_path)

```


# Possible problems
- I found this to be very reliable, but depending on your internet speed you might want to change the sleep-timings in ```youtube_upload.py```
- This enters date and time in german formats. It seems youtube is able to convert this automatically, but i have not tested it thoroughly