import os
import database
import watermark

videos = database.get_all_videos()
for video in videos:
    # video[7] -> watermarked_path
    if not video[7]:
        input_path = video[4]  # video[4] -> file_path
        output_path = f"videos/watermarked/{os.path.basename(input_path)}"
        wm_path = "logo.png"

        watermarked_file = watermark.add_watermark(input_path, output_path, wm_path)
        if watermarked_file:
            database.update_watermarked_path(video[0], watermarked_file)
            print(f"✅ واترمارک شد و ذخیره شد: {watermarked_file}")
        else:
            print(f"⚠️ واترمارک نشد برای ویدیو: {input_path}")
