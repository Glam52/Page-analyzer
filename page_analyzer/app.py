# app.py
from flask import (Flask, render_template,
                   Response, redirect, abort, request, flash)
from page_analyzer.config import Config
from .validator import Validate
from .url_manager import URLManager
from .check import Check
from .exception import InvalidUrl


app = Flask(__name__)
app.config.from_object(Config)

url_manager = URLManager()


@app.route("/")
def home() -> Response:
    return render_template("index.html")


@app.route("/urls", methods=["GET", "POST"])
def urls() -> str:
    if request.method == "POST":
        url = request.form["url"]

        validator = Validate()

        valid = validator.validate_url(url)
        if not valid:
            flash("Некорректный URL")
            return render_template("index.html"), 422
        try:
            new_url_id = url_manager.create_url(url)
            if new_url_id:
                flash("Страница успешно добавлена")
                return redirect(f"/urls/{new_url_id}")
        except InvalidUrl as exc:
            flash(str(exc.detail))
            existing_url = url_manager.get_existing_urls(url)
            if existing_url:
                return redirect(f"/urls/{existing_url}")

    urls = url_manager.list_urls()
    return render_template("list_urls.html", urls=urls)


@app.route("/urls/<int:id>")
def show_url(id: int) -> str:
    data = url_manager.get_url(id)
    if data is None:
        abort(404)

    url_id, url_name, created_at, checks = data
    return render_template(
        "show_url.html", url=(url_id, url_name, created_at), checks=checks
    )


@app.route("/urls/<int:id>/checks", methods=["POST"])
def create_check(id: int):
    print(f"Проверка ID: {id}")
    check_instance = Check(url_manager.database)
    flash("Страница успешно проверена")  #
    if not check_instance.create_check(id):
        abort(404)
    return redirect(f"/urls/{id}")


@app.errorhandler(422)
def handle_422_error(e: Exception) -> tuple:
    return render_template("index.html"), 422


if __name__ == "__main__":
    app.run(debug=True)
