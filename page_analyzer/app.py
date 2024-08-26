from flask import Flask, render_template, request, redirect, abort, flash
import os
import psycopg2
import re
from dotenv import load_dotenv
import requests

# Загружаем переменные окружения из файла secret.env
load_dotenv('secret.env')
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", 'blablabla')  # Используйте ключ из env или дефолтный

# Настройки подключения к базе данных
DATABASE_URL = os.environ.get("DATABASE_URL", default="postgresql://postgres:postgres@localhost:5432/hexlet")

# Функция для получения соединения с базой данных
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

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
        flash('Некорректный URL.')
        return redirect('/urls')

    # Добавление URL в БД
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
    conn.commit()
    cur.close()
    conn.close()

    flash('URL успешно добавлен!')
    return redirect("/")

def list_urls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT urls.id, urls.name, MAX(url_checks.created_at) AS last_check
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id
        ORDER BY urls.created_at DESC
    """)
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

    if url is None:
        abort(404)

    # Получение всех проверок по url_id
    cur.execute("SELECT id, created_at, status_code FROM url_checks WHERE url_id = %s ORDER BY created_at DESC", (id,))
    checks = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('show_url.html', url=url, checks=checks)

@app.route("/urls/<int:id>/checks", methods=["POST"])
def create_check(id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Получаем URL из БД
    cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
    result = cur.fetchone()

    if not result:
        abort(404)

    url = result[1]  # Получаем URL из результата запроса

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на наличие ошибок
        status_code = response.status_code

        # Создание новой проверки с url_id
        cur.execute(
            "INSERT INTO url_checks (url_id, status_code) VALUES (%s, %s) RETURNING id, created_at;",
            (id, status_code)
        )
        check_id, created_at = cur.fetchone()
        flash('Проверка выполнена успешно!')
    except requests.RequestException:
        flash('Произошла ошибка при проверке URL.')
    except Exception as e:
        flash(f'Произошла неожиданная ошибка: {str(e)}')
    finally:
        conn.commit()
        cur.close()
        conn.close()

    return redirect(f"/urls/{id}")

if __name__ == "__main__":
    app.run(debug=True)
