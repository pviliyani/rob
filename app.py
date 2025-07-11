import time

from flask import Flask, render_template, request, redirect, url_for, flash,send_from_directory
import database
import telegram_downloader
import upload_aparat
import upload_to_youtube
import watermark

app = Flask(__name__)
app.secret_key = "supersecretkey"

DOWNLOADS_DIR = '/home/peyman/PycharmProjects/telgram/downloads'

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOADS_DIR, filename)
@app.route("/")
def dashboard():
    channels = database.get_channels()
    videos = database.get_all_videos()
    return render_template("dashboard.html", channels=channels, videos=videos)

@app.route("/download", methods=["POST"])
def download_from_telegram():
    telegram_downloader.download_videos_from_all_channels()
    flash("✅ دانلود ویدیوها از تلگرام انجام شد.")
    return redirect(url_for("dashboard"))

@app.route('/aparat',methods=["POST"])
def upload_all_aparat():
    videos = database.get_no_upload_aparat_video()
    for video in videos:
        if video[7]:
            video_id= video[0]
            upload_aparat.upload_to_aparat(video_id)
            time.sleep(5)
    flash("🚀 همه ویدیوها در اپارات اپلود شدند")
    return redirect(url_for("dashboard"))

@app.route("/youtube",methods=["POST"])
def upload_all_youtube():
    videos = database.get_no_upload_youtube_video()
    for video in videos:
        if video[7]:
            video_file = video[4]
            title = video[14]
            description = video[15]
            video_id = video[0]
            upload_to_youtube.upload_video(video_id, video_file, title, description)
            time.sleep(5)
    flash("🚀 همه ویدیوها در یوتیوب اپلود شدند")
    return redirect(url_for("dashboard"))

@app.route("/upload", methods=["POST"])
def upload_all():
    videos = database.get_all_videos()
    for video in videos:
        if not video[7]:  # watermarked_path
            input_path = video[4]
            output_path = f"videos/watermarked/{input_path.split('/')[-1]}"
            wm_file = watermark.add_watermark(input_path, output_path, "logo.png")
            if wm_file:
                database.update_watermarked_path(video[0], wm_file)
    flash("🚀 همه ویدیوها واترمارک شدند (برای آپلود آماده).")
    return redirect(url_for("dashboard"))

@app.route("/add_channel", methods=["POST"])
def add_channel():
    username = request.form.get("username")
    if username:
        database.add_channel(username)
    return redirect(url_for("dashboard"))

@app.route("/delete_channel/<int:channel_id>")
def delete_channel(channel_id):
    database.delete_channel(channel_id)
    return redirect(url_for("dashboard"))

@app.route("/delete_video/<int:video_id>")
def delete_video(video_id):
    database.delete_video(video_id)
    return redirect(url_for("dashboard"))

@app.route("/edit_video/<int:video_id>", methods=["GET", "POST"])
def edit_video(video_id):
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        database.update_video_info(video_id, title, description)
        return redirect(url_for("dashboard"))

    video = database.get_video_by_id(video_id)
    return render_template("edit_video.html", video=video)

if __name__ == '__main__':
    app.run()
