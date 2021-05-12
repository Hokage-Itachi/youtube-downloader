import urllib.error

import pytube.exceptions
from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
import subprocess
import module.support_function as spf
import os
import urllib.request as rq


def get_youtube_object(url):
    try:
        yt = YouTube(url)
    except VideoUnavailable:
        print(f"Video {url} not available.")
    else:
        return yt


def get_highest_resolution_stream(yt):
    return yt.streams.get_highest_resolution()


def get_available_video(yt):
    videos = yt.streams.filter(progressive=True)
    return videos


def get_video_stream(yt, resolution):
    return yt.streams.filter(res=resolution, mime_type="video/mp4").first()


def get_audio_stream(yt, abr):
    return yt.streams.filter(abr=abr, mime_type="audio/mp4").first()


def combine_video_audio(video_path, audio_path, output_path):
    ffmpeg_path = "./venv/Scripts/ffmpeg-4.4-full_build/bin/ffmpeg.exe "

    cmd = ffmpeg_path + f"-i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path}"
    subprocess.run(cmd)


def download_stream(stream, location, filename=""):
    if filename == "":
        return stream.download(location)
    else:
        return stream.download(location, filename)


def get_possible_resolution(yt):
    res_list = []
    # s = time.time()
    streams = yt.streams.filter(mime_type="video/mp4")
    # print(streams)
    for stream in streams:
        # stream = stream.first()
        if not stream.is_progressive:
            if is_stream_exist(stream):
                if stream.resolution and stream.resolution not in res_list:
                    res_list.append(stream.resolution)

    return res_list


def download(yt, resolution):
    video_stream = get_video_stream(yt, resolution)
    video_file = spf.video_has_exist(yt.title, resolution)
    path = "video/" + resolution + "/"

    if video_file:
        return video_file

    title = spf.title_formatter(yt.title)

    if video_stream in get_available_video(yt):
        video_stream.download(path, title)
        return path + title + ".mp4"

    audio_stream = get_audio_stream(yt, "128kbps")
    try:
        download_stream(video_stream, "video", "video")
    except pytube.exceptions.MaxRetriesExceeded as e:
        print(e)
        return None
    download_stream(audio_stream, "video", "audio")
    output_path = path + title + ".mp4"
    combine_video_audio("video/video.mp4", "video/audio.mp4",
                        output_path)

    os.remove("video/video.mp4")
    os.remove("video/audio.mp4")

    return output_path


def get_playlist_videos(playlist_url):
    playlist = Playlist(playlist_url)
    if not playlist:
        print("Playlist not exist")
        return None
    videos = playlist.videos

    if not videos:
        print("Playlist has no video")
        return None

    return playlist.videos


def is_stream_exist(stream):
    try:
        response = rq.urlopen(stream.url)
    except urllib.error.HTTPError as e:
        print(e, "for", stream)
        print(stream.url)
        return False

    if response:
        return True
