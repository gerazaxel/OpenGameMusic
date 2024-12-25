from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from waitress import serve

app = Flask(__name__)

DATABASE = 'Z:/OpenGameMusic/OpenGameMusic.db'  # Путь к базе данных


# Функция для подключения к базе данных
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к столбцам как к атрибутам
    return conn


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Страница о проекте
@app.route('/about')
def about():
    return render_template('about.html')


# Страница для загрузки музыки
@app.route('/upload', methods=['GET', 'POST'])
def upload_music():
    if request.method == 'POST':
        title = request.form['music-title']
        file = request.files['music-file']
        tags = request.form['tags'].split(',')  # Разделяем теги по запятой

        # Сохраняем файл в директорию /static/music
        music_folder = 'static/music'
        if not os.path.exists(music_folder):
            os.makedirs(music_folder)
        file_path = os.path.join(music_folder, file.filename)
        file.save(file_path)

        # Добавляем трек в базу данных
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO tracks (title, file_path, user_id) VALUES (?, ?, ?)", (title, file_path, 1))  # user_id=1, так как это тест
        track_id = cur.lastrowid

        # Добавляем теги для трека
        for tag in tags:
            tag = tag.strip()
            # Если тег не существует, добавляем его
            cur.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
            cur.execute("SELECT id FROM tags WHERE name=?", (tag,))
            tag_id = cur.fetchone()['id']
            cur.execute("INSERT INTO track_tags (track_id, tag_id) VALUES (?, ?)", (track_id, tag_id))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('upload.html')


# Страница для исследования музыки
@app.route('/explore')
def explore():
    conn = get_db()
    cur = conn.cursor()

    # Получаем все треки из базы данных
    cur.execute("SELECT * FROM tracks")
    tracks = cur.fetchall()

    # Получаем теги для каждого трека
    track_data = []
    for track in tracks:
        cur.execute("SELECT name FROM tags "
                    "JOIN track_tags ON track_tags.tag_id = tags.id "
                    "WHERE track_tags.track_id = ?", (track['id'],))
        tags = [row['name'] for row in cur.fetchall()]
        track_data.append({'track': track, 'tags': tags})

    conn.close()
    return render_template('explore.html', tracks=track_data)


# Запуск приложения
if __name__ == '__main__':
    serve(app,host='0.0.0.0', port=5001)
    app.run(debug=True)
