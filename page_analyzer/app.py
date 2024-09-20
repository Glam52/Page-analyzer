from flask import Flask, render_template
from page_analyzer.config import Config
from page_analyzer.views import AppViews


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def home():
    return AppViews.home()


@app.route("/urls", methods=["GET", "POST"])
def urls():
    return AppViews.urls()


@app.route("/urls/<int:id>")
def show_url(id):
    return AppViews.show_url(id)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def create_check(id):
    return AppViews.create_check(id)


# Обработчик для ошибки 422
@app.errorhandler(422)
def handle_422_error(e):
    return render_template("index.html"), 422


if __name__ == "__main__":
    app.run(debug=True)
