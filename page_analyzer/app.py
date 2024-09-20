from flask import Flask
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


if __name__ == "__main__":
    app.run(debug=True)
