from flask import Flask, render_template, request, redirect, abort
import os
import psycopg2
import re
from dotenv import load_dotenv


# Загружаем переменные окружения из файла secret.env
load_dotenv('secret.env')
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Настройки подключения к базе данных
# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = os.environ.get("DATABASE_URL", default="postgresql://postgres:postgres@localhost:5432/hexlet")

# Функция для получения соединения с базой данных
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Главная страница
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == "POST":
        return add_url()
    return list_urls()

def add_url():
    url = request.form['url']

    # Валидация
    if len(url) > 255 or not re.match(r'^https?://', url):
        return 'Некорректный url.'

    # Добавление URL в БД
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")

def list_urls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('list_urls.html', urls=urls)



@app.route("/urls/<int:id>")
def show_url(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
    url = cur.fetchone()
    cur.close()
    conn.close()

    if url is None:
        abort(404)

    return render_template('show_url.html', url=url)

if __name__ == "__main__":
    app.run(debug=True)