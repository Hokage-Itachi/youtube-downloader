import re
import os
from zipfile import ZipFile


def title_formatter(title):
    title = re.sub("[!@#$%\^&*()<>/?`~\'\" ]", "-", title)
    return title


def video_has_exist(title):
    title = title_formatter(title) + ".mp4"
    if title in os.listdir("video"):
        return "video/" + title
    return None


def to_zip_file(list_video):
    zip_path = "zip/playlist.zip"
    zip_obj = ZipFile(zip_path, "w")

    for video in list_video:
        zip_obj.write(video)

    return zip_path
