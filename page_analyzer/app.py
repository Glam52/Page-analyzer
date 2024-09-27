from flask import Flask, render_template, Response
from page_analyzer.config import Config
from page_analyzer.views import AppViews


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def home() -> Response:
    """
    Render the home page.
    :return: Response: Rendered HTML content of the home page.
    """
    return render_template("index.html")


@app.route("/urls", methods=["GET", "POST"])
def urls() -> Response:
    """
    Handle URL addition and listing
    :return: Response: Rendered HTML content
    of the URLs list or redirect to a newly added URL.
    """
    return AppViews.urls()


@app.route("/urls/<int:id>")
def show_url(id: int) -> Response:
    """
    Display details of a specific URL.
    :param id (int): Unique identifier of the URL.
    :return: Response: Rendered HTML content showing the details of the URL.
    """
    return AppViews.show_url(id)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def create_check(id: int) -> Response:
    """

    :param id (int): Unique identifier of the URL.
    :return: Response: Redirects to the URL's detail page
    after creating the check.
    """
    return AppViews.create_check(id)


# Обработчик для ошибки 422
@app.errorhandler(422)
def handle_422_error(e: Exception) -> tuple:
    """
    Handle 422 error.
    :param e (Exception): Exception raised.
    :return: tuple: Rendered HTML content and HTTP status code 422.
    """
    return render_template("index.html"), 422


if __name__ == "__main__":
    app.run(debug=True)
