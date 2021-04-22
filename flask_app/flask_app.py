from flask import Flask, request, render_template, url_for, send_file, redirect, jsonify
from module import yt_downloader as ytd
from module import support_function as spf

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/video_download", methods=["POST", "GET"])
def download():
    if request.method == "POST":
        url = request.form["video_url"]
        resolution = request.form["resolution"]
        yt = ytd.get_youtube_object(url)

        output_file = ytd.download(yt, resolution)
        if (not output_file):
            output_file = spf.video_not_available_file(yt.title, resolution)
        output_path = "../" + output_file
        return send_file(output_path, as_attachment=True)
    else:
        return redirect(url_for('home'))


@app.route("/possible_resolution", methods=["POST"])
def get_possible_resolution():
    # start = time.time()
    video_url = request.get_data().decode("utf-8")
    yt = ytd.get_youtube_object(video_url)
    res_list = ytd.get_possible_resolution(yt)
    # end = time.time()
    # print(end - start)
    return jsonify(res_list)


@app.route("/get_playlist_videos", methods=["POST"])
def get_playlist_videos():
    playlist_url = request.get_data().decode("utf-8")

    playlist_videos = ytd.get_playlist_videos(playlist_url)

    if not playlist_videos:
        # print(playlist_videos)
        return "Playlist not found", 404

    data = []
    for video in playlist_videos:
        video_url = video.watch_url
        title = spf.title_formatter(video.title)
        available_resolutions = ytd.get_possible_resolution(video)

        data.append(
            {
                "url": video_url,
                "title": title,
                "resolutions": available_resolutions
            }
        )
    # print(data)
    return jsonify(data)


@app.route("/playlist_download", methods=["POST"])
def playlist_download():
    playlist_url = request.form["playlist_url"]
    resolution = request.form['resolution']

    playlist_videos = ytd.get_playlist_videos(playlist_url)

    list_video = []
    for video in playlist_videos:
        output_file = ytd.download(video, resolution)
        if (not output_file):
            output_file = spf.video_not_available_file(video.title, resolution)
        list_video.append(output_file)

    zip_file = "../" + spf.to_zip_file(list_video, "playlist.zip")

    return send_file(zip_file, as_attachment=True)


@app.route("/get_channel_videos", methods=["POST"])
def get_channel_video():
    channel_url = request.get_data().decode("utf-8")
    videos_url = spf.crawl_youtube_html(channel_url)

    data = []
    for url in videos_url:
        video = ytd.get_youtube_object(url)

        title = spf.title_formatter(video.title)
        available_resolutions = ytd.get_possible_resolution(video)

        data.append(
            {
                "url": url,
                "title": title,
                "resolutions": available_resolutions
            }
        )

    return jsonify(data)


@app.route("/channel_download", methods=["POST"])
def channel_download():
    pattern = "[\[\] ]"
    replace = ""
    channel_videos_url = spf.string_formatter(pattern, replace, request.form["channel_videos_url"]).split(",")
    channel_gennerl_resolution = request.form["channel_general_resolution"]
    list_video = []
    for url in channel_videos_url:
        video = ytd.get_youtube_object(url)
        output_file = ytd.download(video, channel_gennerl_resolution)
        if (not output_file):
            output_file = spf.video_not_available_file(video.title, channel_gennerl_resolution)
        list_video.append(output_file)

    zip_file = "../" + spf.to_zip_file(list_video, "channel.zip")

    return send_file(zip_file, as_attachment=True)


@app.route("/test")
def test():
    import requests

    response = requests.get("https://www.youtube.com/channel/UCWkdXRJdvjT9TvXHx5FFx9g/videos")

    return response.text
