import subprocess
import os

def add_watermark(input_path, output_path, watermark_path):
    if not os.path.exists(input_path):
        print(f"⚠️ فایل ویدیو پیدا نشد: {input_path}")
        return None

    if not os.path.exists(watermark_path):
        print(f"⚠️ فایل واترمارک پیدا نشد: {watermark_path}")
        return None

    command = [
        "ffmpeg",
        "-i", input_path,
        "-i", watermark_path,
        "-filter_complex", "overlay=10:10",  # موقعیت لوگو (10,10)
        "-codec:a", "copy",
        output_path
    ]

    print(f"🎬 در حال واترمارک کردن {input_path}")
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path
