from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
import subprocess
import module.support_function as spf
import os


def get_youtube_object(url):
    try:
        yt = YouTube(url)
    except VideoUnavailable:
        print(f"Video {url} not available.")
    else:
        return yt


def get_highest_resolution_stream(yt):
    return yt.streams.get_highest_resolution()


def get_by_resolution(yt, resolution):
    return yt.streams.get_by_resolution(resolution)


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
    res_list = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
    # s = time.time()
    streams = yt.streams
    index = 0
    for stream in streams:
        if (stream.is_progressive):
            index += 1
        else:
            break
    highest_resolution_stream = streams[index]
    # print(highest_resolution_stream)
    # print(time.time() - s)
    highest_resolution = highest_resolution_stream.resolution
    i = res_list.index(highest_resolution)
    for j in range(i):
        res_list.remove(res_list[0])
    return res_list


def download(yt, resolution):
    video_stream = get_video_stream(yt, resolution)
    audio_stream = get_audio_stream(yt, "128kbps")
    download_stream(video_stream, "video", "video")
    download_stream(audio_stream, "video", "audio")
    title = spf.title_formatter(yt.title)
    output_path = "video/" + title + ".mp4"
    combine_video_audio("video/video.mp4", "video/audio.mp4",
                        output_path)

    os.remove("video/video.mp4")
    os.remove("video/audio.mp4")

    return output_path
