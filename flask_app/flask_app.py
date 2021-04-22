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

        output_path = "../" + ytd.download(yt, resolution)
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
        video_file = spf.video_has_exist(video.title)
        if (video_file):
            list_video.append(video_file)
        else:
            list_video.append(ytd.download(video, resolution))

    zip_file = "../" + spf.to_zip_file(list_video)

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


@app.route("/test")
def test():
    import requests

    response = requests.get("https://www.youtube.com/channel/UCWkdXRJdvjT9TvXHx5FFx9g/videos")

    return response.text
