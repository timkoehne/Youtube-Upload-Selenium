from datetime import timedelta
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
import html


class Video:
    def __init__(
        self,
        video_title: str,
        video_description: str,
        thumbnail_file_path: str,
        video_file_path: str,
        tags: list[str] = [],
        language: str = "en",
        upload_date_time: datetime.datetime | None = None,
    ) -> None:
        self.video_title = video_title
        self.video_description = video_description
        self.thumbnail_file_path = thumbnail_file_path
        self.video_file_path = video_file_path
        self.tags = tags
        self.language = language
        self.upload_date_time = upload_date_time


def upload_single_video(
    video: Video, firefox_profile_path: str, headless: bool = False
):
    driver = _create_Webdriver(firefox_profile_path, headless)

    _upload_video(
        driver,
        video.video_file_path,
        video.video_title,
        video.video_description,
        video.thumbnail_file_path,
        video.tags,
        video.language,
        video.upload_date_time,
    )

    driver.quit()


def upload_multiple_videos(
    videos: list[Video], firefox_profile_path: str, headless: bool = False
):
    driver = _create_Webdriver(firefox_profile_path, headless)

    for video in videos:
        _upload_video(
            driver,
            video.video_file_path,
            video.video_title,
            video.video_description,
            video.thumbnail_file_path,
            video.tags,
            video.language,
            video.upload_date_time,
        )

    driver.quit()


def schedule_multiple_videos(
    videos: list[Video], start_time: datetime.datetime, interval: timedelta
):
    for num, video in enumerate(videos):
        publish_time = start_time + num * interval
        print(f"scheduling video {num} for {publish_time.strftime('%d.%m.%Y %H:%M')}")
        video.upload_date_time = publish_time
    return videos


def _create_Webdriver(firefox_profile_path: str, headless: bool = False) -> WebDriver:
    profile = webdriver.FirefoxProfile(firefox_profile_path)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference("useAutomationExtension", False)
    profile.update_preferences()
    
    

    options = webdriver.FirefoxOptions()
    options.profile = profile
    if headless:
        options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(30)
    return driver


def _upload_video(
    driver: WebDriver,
    video_file_path: str,
    video_title: str,
    video_description: str,
    thumbnail_file_path: str,
    tags: list[str],
    language: str,
    upload_date_time: datetime.datetime | None = None,
):
    driver.get("https://www.youtube.com")
    sleep(5)

    # click upload button
    upload_button = driver.find_elements(by=By.ID, value="masthead-container")[0]
    upload_button = upload_button.find_elements(by=By.ID, value="button")[5]
    upload_button.click()

    upload_button = driver.find_elements(by=By.ID, value="items")
    # print(len(upload_button))
    upload_button = upload_button[len(upload_button) - 1]
    upload_button = upload_button.find_elements(
        by=By.CSS_SELECTOR, value=".style-scope.yt-multi-page-menu-section-renderer"
    )[0]
    upload_button.click()

    # upload video file
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(video_file_path)
    print("uploading video file")
    sleep(2)

    # input title
    title_textarea = driver.find_element(by=By.ID, value="title-textarea")
    title_textarea = title_textarea.find_element(by=By.ID, value="textbox")
    title_textarea.clear()
    print("entering title")
    sleep(1)
    title_textarea.send_keys(video_title)

    # input description
    description_textarea = driver.find_element(by=By.ID, value="description-textarea")
    description_textarea = description_textarea.find_element(by=By.ID, value="textbox")
    description_textarea.clear()
    print("entering description")
    sleep(1)
    description_textarea.send_keys(video_description)

    # select thumbnail
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(thumbnail_file_path)
    print("uploading thumbnail")

    # select not-for-kids
    driver.find_element(By.NAME, value="VIDEO_MADE_FOR_KIDS_NOT_MFK").click()

    # show more settings
    driver.find_element(By.ID, value="toggle-button").click()

    # add tags
    tags_input = driver.find_element(By.ID, value="tags-container")
    tags_input = tags_input.find_element(By.ID, value="text-input")
    tags_input.send_keys(",".join(tags))
    print("entering tags")

    # language input
    driver.find_element(By.ID, "language-input").click()
    language_input = driver.find_elements(By.ID, "paper-list")[-1]
    langs = language_input.find_elements(By.CLASS_NAME, "selectable-item")
    lang = langs[0]
    for l in langs:
        if l.get_attribute("test-id") == language:
            lang = l
            break
    print(f"selected language {lang.get_attribute('test-id')}")
    lang.click()
    driver.find_element(By.ID, value="next-button").click()
    sleep(1)
    driver.find_element(By.ID, value="next-button").click()
    sleep(1)
    driver.find_element(By.ID, value="next-button").click()
    sleep(1)

    # select publication date
    if upload_date_time != None:
        upload_date = upload_date_time.strftime("%d.%m.%Y")
        upload_time = upload_date_time.strftime("%H:%M")
        driver.find_element(By.ID, value="second-container-expand-button").click()
        driver.find_element(By.ID, value="datepicker-trigger").click()

        dialog = driver.find_elements(By.ID, value="dialog")[6]
        input = dialog.find_element(By.CSS_SELECTOR, "input")
        input.clear()
        input.send_keys(upload_date, "\ue007")

        # select publication time
        inputs = driver.find_elements(By.CSS_SELECTOR, "input")
        # print(len(inputs))

        inputs[2].clear()
        inputs[2].send_keys(upload_time)
        print("selected publication date")

    else:
        public_radiobutton = driver.find_elements(By.ID, "radioContainer")[2]
        public_radiobutton.click()

    sleep(1)
    driver.find_element(By.ID, value="done-button").click()
    sleep(1)

    # wait for upload to finish
    progress_label = driver.find_element(By.CLASS_NAME, "progress-label")
    while True:
        print("waiting for upload to finish...")
        text: str = html.unescape(progress_label.get_attribute("innerHTML"))  # type: ignore
        if "%" not in text:
            print("finished uploading")
            break
        print(text)
        sleep(5)
    close_buttons = driver.find_elements(By.ID, "close-button")
    close_buttons[len(close_buttons) - 1].click()
