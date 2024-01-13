# Youtube Uploader
This is a python module that uses [selenium webdriver](https://github.com/SeleniumHQ/selenium) to upload videos to youtube.

Since this uses selenium to nagivate the HTML of youtube, this WILL probably break when youtube updates their frontend. Last verified to work on 12 Jan 2024. 


# Requirements
- Firefox - tested on 121.0 but should work on most modern versions
- Python - tested on 3.10.13 but should work on most modern versions

- ```pip install selenium```


# Usage

you need to be logged in on youtube in your firefox profile

see example usage in ```example_single_video.py``` and ```example_multiple_videos.py```


# Possible problems
- I found this to be very reliable, but depending on your internet speed you might want to change the sleep-timings in ```youtube_upload.py```
- This enters date and time in german formats. It seems youtube is able to convert this automatically, but i have not tested it thoroughly
- if firefox is installed through snap, selenium has problems finding and accessing the geckdriver and any profiles. To solve this install firefox without snap. 
For ubuntu [this](https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04#:%7E:text=Installing%20Firefox%20via%20Apt%20(Not%20Snap)&text=You%20add%20the%20Mozilla%20Team,%2C%20bookmarks%2C%20and%20other%20data) explains how to do it since apt installs firefox through snap by default.