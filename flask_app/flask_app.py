from flask import Flask, request, render_template, url_for, send_file, redirect, jsonify
from module import yt_downloader as ytd

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
