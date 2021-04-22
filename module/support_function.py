import re
import os
from zipfile import ZipFile
from requests_html import AsyncHTMLSession, HTMLSession
from bs4 import BeautifulSoup as bs
import asyncio
from module.fix_html_session import FixedHTMLSession


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


def crawl_youtube_html(url):
    # sample youtube video url
    channel_url = url
    # init an HTML Session

    # get the html content
    response = get_request_response(channel_url)
    # execute Java-script
    try:
        response.html.render()
    except RuntimeError as e:
        if "There is no current event loop in thread" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.get_event_loop()

    response.html.render()
    # create bs object to parse HTML
    soup = bs(response.html.html, "lxml")

    prefix = "https://www.youtube.com/"

    videos_url = []
    a_tags = soup.findAll('a')

    for a in a_tags:
        if (a.attrs.get("id") == "video-title"):
            videos_url.append(prefix + a.attrs.get('href'))

    return videos_url


def get_request_response(channel_url):
    try:
        session = HTMLSession()
        response = session.get(channel_url)
    except RuntimeError as e:
        if "There is no current event loop in thread" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.get_event_loop()
    finally:
        session = HTMLSession()
        response = session.get(channel_url)
        return response



