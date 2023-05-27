from flask import Flask, render_template, request
import vk_api
from datetime import datetime, timedelta
import csv
from concurrent.futures import ThreadPoolExecutor
import threading
import os

os.environ['FLASK_ENV'] = 'development'

app = Flask(__name__)

# Константы
TOKEN = '' # Токен API VK
GROUP_ID = # ID группы VK
LIKES_VALUE = 5 #цена за лайк
COMMENTS_VALUE = 10 #цена за комент
NUM_THREADS = 10
UPDATE_INTERVAL = 15 #интервал обновлений

def get_stats(vk):
    today = datetime.now()
    month_ago = today - timedelta(days=30)
    posts = vk.wall.get(owner_id=-GROUP_ID, count=100)
    stats = {}
    user_cache = {}

    def process_post(post):
        nonlocal stats, user_cache
        date = datetime.fromtimestamp(post['date'])
        if date < month_ago:
            return

        post_id = post['id']
        likes = vk.likes.getList(type='post', owner_id=-GROUP_ID, item_id=post_id, extended=1, fields='first_name,last_name')
        for user in likes['items']:
            user_id = user['id']
            if user_id not in stats:
                stats[user_id] = 0
                user_cache[user_id] = user
            stats[user_id] += LIKES_VALUE

        comments = vk.wall.getComments(owner_id=-GROUP_ID, post_id=post_id, extended=1, fields='first_name,last_name')
        for comment in comments['profiles']:
            user_id = comment['id']
            if user_id not in stats:
                stats[user_id] = 0
                user_cache[user_id] = comment
            stats[user_id] += COMMENTS_VALUE

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        executor.map(process_post, posts['items'])

    return stats, user_cache

def save_stats(stats, user_cache):
    csv_path = os.path.join('data', 'stats.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'profile_url', 'points'])
        for user_id, points in stats.items():
            user = user_cache[user_id]
            name = f"{user['first_name']} {user['last_name']}"
            profile_url = f"https://vk.com/id{user_id}"
            writer.writerow([name, profile_url, points])

def update_stats():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    stats, user_cache = get_stats(vk)
    save_stats(stats, user_cache)

    # Запускаем таймер для обновления статистики
    threading.Timer(UPDATE_INTERVAL, update_stats).start()

def load_stats():
    data = []
    csv_path = os.path.join('data', 'stats.csv')
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = sorted(reader, key=lambda x: int(x[2]), reverse=True)
    return headers, data

# Запускаем обновление статистики
update_stats()

@app.route('/', methods=['GET'])
def index():
    headers, data = load_stats()
    search = request.args.get('search')

    if search:
        search = search.lower()
        data = [row for row in data if search in row[0].lower()]

    return render_template('index.html', headers=headers, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

