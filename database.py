import sqlite3
from datetime import datetime

conn = sqlite3.connect('videos.db', check_same_thread=False)
c = conn.cursor()

# ایجاد جدول channels
c.execute('''
CREATE TABLE IF NOT EXISTS channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    added_at TEXT,
    last_checked_message_id INTEGER
)
''')

# ایجاد جدول videos
c.execute('''
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_message_id INTEGER,
    channel_id INTEGER,
    file_unique_id TEXT,
    file_path TEXT,
    caption TEXT,
    downloaded_at TEXT,
    watermarked_path TEXT,
    uploaded_aparat INTEGER DEFAULT 0,
    aparat_link TEXT,
    uploaded_youtube INTEGER DEFAULT 0,
    youtube_link TEXT,
    uploaded_instagram INTEGER DEFAULT 0,
    instagram_link TEXT,
    FOREIGN KEY (channel_id) REFERENCES channels(id)
)
''')

conn.commit()

# مدیریت کانال‌ها
def add_channel(username):
    now = datetime.utcnow().isoformat()
    c.execute('INSERT OR IGNORE INTO channels (username, added_at) VALUES (?, ?)', (username, now))
    conn.commit()

def get_channels():
    c.execute('SELECT id, username, last_checked_message_id FROM channels')
    return c.fetchall()

def update_last_checked(channel_id, message_id):
    c.execute('UPDATE channels SET last_checked_message_id = ? WHERE id = ?', (message_id, channel_id))
    conn.commit()

# مدیریت ویدیوها
def video_exists(message_id, file_unique_id):
    c.execute('SELECT 1 FROM videos WHERE telegram_message_id = ? OR file_unique_id = ?', (message_id, file_unique_id))
    return c.fetchone() is not None

# def add_video(message_id, channel_id, file_unique_id, file_path, caption):
#     now = datetime.utcnow().isoformat()
#     c.execute('''
#     INSERT OR IGNORE INTO videos (telegram_message_id, channel_id, file_unique_id, file_path, caption, downloaded_at)
#     VALUES (?, ?, ?, ?, ?, ?)
#     ''', (message_id, channel_id, file_unique_id, file_path, caption, now))
#     conn.commit()
def add_video(message_id, channel_id, file_unique_id, file_path, caption, title="", description=""):
    now = datetime.utcnow().isoformat()
    c.execute('''
    INSERT OR IGNORE INTO videos (telegram_message_id, channel_id, file_unique_id, file_path, caption, downloaded_at, title, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (message_id, channel_id, file_unique_id, file_path, caption, now, title, description))
    conn.commit()

def get_all_videos():
    c.execute('SELECT * FROM videos')
    return c.fetchall()
def delete_channel(channel_id):
    c.execute('DELETE FROM channels WHERE id = ?', (channel_id,))
    conn.commit()

def delete_video(video_id):
    c.execute('DELETE FROM videos WHERE id = ?', (video_id,))
    conn.commit()

def update_watermarked_path(video_id, watermarked_path):
    c.execute('UPDATE videos SET watermarked_path = ? WHERE id = ?', (watermarked_path, video_id))
    conn.commit()
def get_no_upload_aparat_video():
    c.execute('SELECT * FROM videos WHERE uploaded_aparat =0')
    return c.fetchall()

def get_no_upload_youtube_video():
    c.execute('SELECT * FROM videos WHERE uploaded_youtube =0')
    return c.fetchall()

def update_aparat_status(video_id, link):
    c.execute('UPDATE videos SET uploaded_aparat = 1, aparat_link = ? WHERE id = ?', (link, video_id))
    conn.commit()

def get_video_by_id(video_id):
    c.execute('SELECT * FROM videos WHERE id = ?', (video_id,))
    return c.fetchone()

def update_video_info(video_id, title, description):
    c.execute('UPDATE videos SET title = ?, description = ? WHERE id = ?', (title, description, video_id))
    conn.commit()

def get_video_info(video_id):
    c.execute('SELECT file_path, title, description FROM videos WHERE id = ?', (video_id,))
    return c.fetchone()  # برمی‌گردونه (file_path, title, description)

def update_youtube_status(video_id, link):
    c.execute('UPDATE videos SET uploaded_youtube = 1, youtube_link = ? WHERE id = ?', (link, video_id))
    conn.commit()

