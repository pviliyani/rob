from pyrogram import Client
import os
import time
from tqdm import tqdm
import database
from utils import convert_to_mp4

api_id = 20971978
api_hash = "40e4d280d678ac35a7b660d573118d8a"
app = Client("my_session",
             api_id=api_id,
             api_hash=api_hash,
             proxy=dict(
                 hostname="127.0.0.1",
                 port=1080,
                 scheme="socks5")
             )
download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

def download_videos_from_all_channels():
    app.start()
    try:
        channels = database.get_channels()
        print(f"📡 شروع بررسی {len(channels)} کانال...")

        for channel_id, username, last_msg_id in channels:
            print(f"\n🔍 چک کردن کانال {username}")

            messages = list(app.get_chat_history(username, limit=200))

            # اطمینان که last_msg_id عدد صحیحه
            if last_msg_id is not None:
                last_msg_id = int(last_msg_id)

            new_messages = [msg for msg in messages if (last_msg_id is None or msg.id > last_msg_id)]

            if not new_messages:
                print(f"⚠️ هیچ پیام جدیدتری در {username} نبود.")
                continue

            video_messages = [msg for msg in new_messages if msg.video]
            print(f"✅ در مجموع {len(video_messages)} پیام ویدیویی جدید یافت شد.")
            print('new_messages[0].id',new_messages[0].id)
            for idx, msg in enumerate(tqdm(video_messages[:20]), start=1):
                if msg.video and not msg.animation:
                    if not database.video_exists(msg.id, msg.video.file_unique_id):
                        print(f"\n🚀 ({idx}) پردازش ویدیو id={msg.id}")

                        t1 = time.time()
                        path = app.download_media(msg.video)
                        print(f"⏱️ دانلود در {time.time() - t1:.2f} ثانیه")

                        ext = os.path.splitext(path)[1].lower()
                        if ext == '.mp4':
                            database.add_video(msg.id, channel_id, msg.video.file_unique_id, path, msg.caption)
                            print(f"✅ ذخیره مستقیم mp4: {path}")
                        else:
                            t2 = time.time()
                            mp4_path = convert_to_mp4(path)
                            print(f"⏱️ تبدیل در {time.time() - t2:.2f} ثانیه")

                            if mp4_path:
                                database.add_video(msg.id, channel_id, msg.video.file_unique_id, mp4_path, msg.caption)
                                print(f"✅ ذخیره پس از تبدیل: {mp4_path}")
                            else:
                                print(f"⚠️ خطا در تبدیل: {path}")

            # آپدیت آخرین پیام بررسی‌شده
            database.update_last_checked(channel_id, new_messages[0].id)
            print(f"✅ بررسی کانال {username} تمام شد.")

    finally:
        app.stop()






# def download_videos_from_all_channels():
#     with app:
#         channels = database.get_channels()
#         print(f"📡 شروع بررسی {len(channels)} کانال...")
#
#         for channel_id, username, last_msg_id in channels:
#             print(f"\n🔍 چک کردن کانال {username}")
#
#             messages = list(app.get_chat_history(username, limit=200))
#             new_messages = [msg for msg in messages if (last_msg_id is None or msg.id > last_msg_id)]
#
#             if not new_messages:
#                 print(f"⚠️ هیچ پیام جدیدتری در {username} نبود.")
#                 continue
#
#             video_messages = [msg for msg in new_messages if msg.video]
#             print(f"✅ در مجموع {len(video_messages)} پیام ویدیویی جدید یافت شد.")
#
#             for idx, msg in enumerate(tqdm(video_messages[:20]), start=1):
#                 if msg.video and not msg.animation:
#                     if not database.video_exists(msg.id, msg.video.file_unique_id):
#                         print(f"\n🚀 ({idx}) پردازش ویدیو id={msg.id}")
#
#                         t1 = time.time()
#                         path = app.download_media(msg.video)
#                         print(f"⏱️ دانلود در {time.time() - t1:.2f} ثانیه")
#
#                         ext = os.path.splitext(path)[1].lower()
#                         if ext == '.mp4':
#                             database.add_video(msg.id, channel_id, msg.video.file_unique_id, path, msg.caption)
#                             print(f"✅ ذخیره مستقیم mp4: {path}")
#                         else:
#                             t2 = time.time()
#                             mp4_path = convert_to_mp4(path)
#                             print(f"⏱️ تبدیل در {time.time() - t2:.2f} ثانیه")
#
#                             if mp4_path:
#                                 database.add_video(msg.id, channel_id, msg.video.file_unique_id, mp4_path, msg.caption)
#                                 print(f"✅ ذخیره پس از تبدیل: {mp4_path}")
#                             else:
#                                 print(f"⚠️ خطا در تبدیل: {path}")
#
#             # آپدیت آخرین پیام بررسی‌شده
#             database.update_last_checked(channel_id, new_messages[0].id)
#             print(f"✅ بررسی کانال {username} تمام شد.")
#
#
#
#
#             # for msg in video_messages[:20]:
#             #     if not database.video_exists(msg.id, msg.video.file_unique_id):
#             #         path = app.download_media(msg.video)
#             #         mp4_path = convert_to_mp4(path)
#             #         if mp4_path:
#             #             database.add_video(msg.id, channel_id, msg.video.file_unique_id, mp4_path, msg.caption)
#             #             print(f"🎥 ویدیو جدید دانلود و تبدیل شد: {mp4_path}")
#             #         else:
#             #             print(f"⚠️ خطا در تبدیل ویدیو: {path}")

