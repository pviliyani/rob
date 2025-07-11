from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google.auth.transport.requests
import os
import database

# این اسکوپ فقط دسترسی به آپلود میده
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

def upload_video(id_vide,file, title, description):
    youtube = get_authenticated_service()
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["قاب گوشی", "خرید", "میهن قاب"],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=file
    )

    response = insert_request.execute()

    video_id = response.get('id')
    upload_status = response.get('status', {}).get('uploadStatus')

    if video_id and upload_status == 'uploaded':
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print("آپلود موفق بود!")
        print("لینک ویدیو:", video_url)
        # اینجا می‌تونی اطلاعات رو تو دیتابیس ذخیره کنی
        database.update_youtube_status(id_vide,video_url)
    else:
        print("آپلود موفق نبود یا اطلاعات ناقصه")

    print(f"✅ ویدیو با موفقیت آپلود شد. لینک: https://www.youtube.com/watch?v={response['id']}")


# if __name__ == "__main__":
    # id_video =21
    # info_video = database.get_video_info(id_video)
    #  این رو از دیتابیس خودت بگیر
    # if info_video:
    #     video_file, title, description = info_video
    # upload_video(youtube, video_file, title, description)
