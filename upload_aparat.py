import database
import os
import json
import hashlib
import urllib3
import certifi
import requests

def hash_password(password: str) -> str:
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    sha1_hash = hashlib.sha1(md5_hash.encode()).hexdigest()
    return sha1_hash


def upload_to_aparat(video_id):
    # اطلاعات کاربری
    username = "mihanghab"
    password = "Q8n4dZERQQPa5Uw"

    # مرحله 1: لاگین
    lpass = hash_password(password)
    login_url = f"https://www.aparat.com/etc/api/login/luser/{username}/lpass/{lpass}"
    login_response = requests.get(login_url)
    login_data = login_response.json()
    ltoken = login_data['login']['ltoken']
    # مرحله گرفتن ایدی فرم
    uploadform_url = f"https://www.aparat.com/etc/api/upload%E2%80%8Bform/luser/{username}/ltoken/{ltoken}"
    uploadform_response = requests.get(uploadform_url)
    uploadform_data = uploadform_response.json()
    frm_id = uploadform_data['uploadform']['frm-id']
    upload_url = uploadform_data['uploadform']['formAction']
    # print(upload_url)
    # video_id=23
    # فرض کنیم video_id رو داریم
    video_info = database.get_video_info(video_id)

    if video_info:
        file_path, title, description = video_info
        data = {
            'frm-id': frm_id,
            'data[title]': title,
            'data[category]': 10,
            'data[tags]': "قاب گوشی-قاب گوشی آیفون-قاب موبایل",
            'data[comment]': "yes",
            'data[descr]': description,
            'data[video_pass]': 'false',
        }

        # خواندن داده فایل
        with open(file_path, 'rb') as video_file:
            video_data = video_file.read()

        # فقط نام فایل (با پسوند) نه مسیر کامل
        file_name = os.path.basename(file_path)

        # ارسال با urllib3
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        resp = http.request(
            "POST",
            upload_url,
            fields={
                "video": (file_name, video_data),
                **data
            }
        )

        if resp.status != 200:
            print("Upload failed with HTTP status:", resp.status)
        else:
            try:
                response_json = json.loads(resp.data.decode('utf-8'))
                vid = response_json['uploadpost']['uid']
                video_url = f"https://www.aparat.com/v/{vid}";
                print("Upload response:", response_json)
                database.update_aparat_status(video_id, video_url)
            except Exception as e:
                print("خطا در تبدیل پاسخ به JSON:", e)
                print("متن پاسخ:", resp.data.decode('utf-8'))

    else:
        print("ویدیو با این شناسه پیدا نشد.")




if __name__ == "__main__":
    upload_to_aparat()
