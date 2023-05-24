#!/usr/bin/env python3
"""User locale
"""
from flask_babel import Babel
from typing import Union, Dict
from flask import Flask, render_template, request, g


class Config:
    """Reps a Flask Babel configuration.
    """
    LANGUAGES = {"en", "fr"}
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

valid_languages = app.config["LANGUAGES"]


def get_user() -> Union[Dict, None]:
    """Retrieves user based on a user id.
    """
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    """Runs routines before each request's resolution.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """To fetch the locale for a web page.
    """
    locale = request.args.get('locale', '')
    user_locale = g.user['locale'] if g.user else None

    if locale in valid_languages:
        return locale
    if user_locale in valid_languages:
        return user_locale

    header_locale = request.headers.get('locale', '')
    return header_locale if header_locale in valid_languages else request.accept_languages.best_match(valid_languages)


@app.route('/')
def get_index() -> str:
    """Home/index page.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
