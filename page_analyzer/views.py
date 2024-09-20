from flask import render_template, request, redirect, abort, flash, Response
from page_analyzer.url_manager import URLManager
import re


class AppViews:
    @staticmethod
    def home() -> Response:
        """
        Render the home page.
        :return: Rendered HTML content of the home page.
        """
        return render_template("index.html")

    @staticmethod
    def urls() -> Response:
        """
        Handle addition and listing of URLs.
        :return: Rendered HTML content of the list of URLs
        or redirect to a specific URL.
        """
        if request.method == "POST":
            url = request.form["url"]
            # Проверка на валидность URL
            if not re.match(r"^(?:http|ftp)s?://", url):
                flash("Некорректный URL")  # Добавляем флеш-сообщение
                abort(422)  # Генерируем ошибку 422

            new_url_id = URLManager.add_url(url)
            if new_url_id:
                return redirect(f"/urls/{new_url_id}")

        urls = URLManager.list_urls()
        return render_template("list_urls.html", urls=urls)

    @staticmethod
    def show_url(id: int) -> Response:
        """
        Display a specific URL and its check details.
        :param id: Unique identifier of the URL.
        :return: Rendered HTML content for the URL and its checks.
        """
        data = URLManager.get_url(id)
        if data is None:
            abort(404)

        url, checks = data
        return render_template("show_url.html", url=url, checks=checks)

    @staticmethod
    def create_check(id: int) -> Response:
        """
        Create a check for a specific URL.
        :param id: Unique identifier of the URL.
        :return: Redirects to the URL's detail page after creating the check.
        """
        if not URLManager.create_check(id):
            abort(404)
        return redirect(f"/urls/{id}")
