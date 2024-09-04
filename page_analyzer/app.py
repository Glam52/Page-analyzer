from flask import Flask, render_template, request, redirect, abort, flash
import os
import psycopg2
import re
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup


# Загружаем переменные окружения из файла secret.env
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "blablabla")
# Настройки подключения к базе данных
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    default="postgresql://postgres:postgres@localhost:5432/hexlet",
)


# Функция для получения соединения с базой данных
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


# Главная страница
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == "POST":
        return add_url()
    return list_urls()


def add_url():
    url = request.form["url"]

    # Валидация
    if len(url) > 255 or not re.match(r"^https?://", url):
        flash("Некорректный URL")
        return render_template("index.html")

    # Добавление URL в БД
    conn = get_db_connection()
    cur = conn.cursor()

    # Проверяем, существует ли URL в БД
    cur.execute("SELECT id FROM urls WHERE name = %s", (url,))
    existing_url = cur.fetchone()

    if existing_url:
        flash("Страница уже существует.")
        return redirect(f"/urls/{existing_url[0]}")

    # Добавление нового URL в БД
    cur.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,))
    new_url_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    flash("Страница успешно добавлена")
    return redirect(f"/urls/{new_url_id}")


def list_urls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
    SELECT urls.id, urls.name, MAX(url_checks.created_at) AS last_check, 
    MAX(url_checks.status_code) AS status_code FROM urls
    LEFT JOIN url_checks ON urls.id = url_checks.url_id
    GROUP BY urls.id
    ORDER BY urls.created_at DESC
        """
    )
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("list_urls.html", urls=urls)


@app.route("/urls/<int:id>")
def show_url(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
    url = cur.fetchone()

    if url is None:
        abort(404)

    # Преобразуем дату в строку формата 'YYYY-MM-DD'
    created_at_formatted = url[2].strftime("%Y-%m-%d")
    url = (url[0], url[1], created_at_formatted)
    # Получение всех проверок по url_id
    cur.execute(
        "SELECT id,"
        " created_at,"
        " status_code,"
        " h1,"
        " title,"
        " description"
        " FROM url_checks"
        " WHERE url_id = %s"
        " ORDER BY created_at DESC",
        (id,),
    )
    checks = cur.fetchall()

    # Форматирование даты для проверок
    for i in range(len(checks)):
        checks[i] = list(
            checks[i]
        )  # Преобразуем кортеж в список для мутабельности
        checks[i][1] = checks[i][1].strftime(
            "%Y-%m-%d"
        )  # Форматируем created_at

    cur.close()
    conn.close()

    return render_template("show_url.html", url=url, checks=checks)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def create_check(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
    result = cur.fetchone()

    if not result:
        abort(404)

    url = result[1]

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        h1_tag = soup.find("h1")
        h1_content = h1_tag.text.strip() if h1_tag else None

        title_content = soup.title.text.strip() if soup.title else None
        description_content = ""
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag and "content" in description_tag.attrs:
            description_content = description_tag["content"].strip()

        cur.execute(
            "INSERT INTO url_checks (url_id,"
            " status_code,"
            " h1,"
            " title,"
            " description)"
            " VALUES (%s, %s, %s, %s, %s)"
            " RETURNING id, created_at;",
            (
                id,
                response.status_code,
                h1_content,
                title_content,
                description_content,
            ),
        )
        check_id, created_at = cur.fetchone()
        flash("Проверка выполнена успешно!")

    except requests.RequestException:
        flash("Произошла ошибка при проверке URL.")
    except Exception as e:
        flash(f"Произошла неожиданная ошибка: {str(e)}")
    finally:
        conn.commit()
        cur.close()
        conn.close()

    return redirect(f"/urls/{id}")


if __name__ == "__main__":
    app.run(debug=True)
