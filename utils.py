# import subprocess
# import os
#
# def convert_to_mp4(input_path):
#     base, ext = os.path.splitext(input_path)
#     output_path = base + ".mp4"
#
#     if ext.lower() == ".mp4":
#         return input_path  # اگر قبلاً mp4 بود، تغییر نده
#
#     command = [
#         "ffmpeg",
#         "-i", input_path,
#         "-c:v", "libx264",
#         "-preset", "fast",
#         "-c:a", "aac",
#         "-strict", "-2",
#         output_path
#     ]
#
#     result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     if result.returncode == 0:
#         print(f"🎬 تبدیل به MP4 با موفقیت انجام شد: {output_path}")
#         return output_path
#     else:
#         print(f"⚠️ خطا در تبدیل ویدیو به MP4: {result.stderr.decode()}")
#         return None
import subprocess
import os

def convert_to_mp4(input_path):
    base, ext = os.path.splitext(input_path)
    output_path = base + ".mp4"

    # اگر خودش mp4 بود
    if ext.lower() == ".mp4":
        return input_path

    # اول با copy (خیلی سریع)
    copy_command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-c", "copy",
        output_path
    ]

    result = subprocess.run(copy_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print(f"🎬 تبدیل سریع (stream copy) به MP4 انجام شد: {output_path}")
        return output_path
    else:
        print(f"⚠️ stream copy جواب نداد، می‌ریم سراغ re-encode...")

    # اگر copy جواب نداد re-encode با ultrafast
    encode_command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "aac",
        output_path
    ]

    result = subprocess.run(encode_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print(f"🎬 تبدیل به MP4 با موفقیت انجام شد: {output_path}")
        return output_path
    else:
        print(f"⚠️ خطا در تبدیل ویدیو به MP4: {result.stderr.decode()}")
        return None
