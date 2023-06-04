#!/usr/bin/env python3
"""Infer approp t zone
"""
import pytz
from flask_babel import Babel
from typing import Union, Dict
from flask import Flask, render_template, request, g


class Config:
    """Reps a Flask Babel config.
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
default_locale = app.config["BABEL_DEFAULT_LOCALE"]
default_timezone = app.config["BABEL_DEFAULT_TIMEZONE"]


def get_user() -> Union[Dict, None]:
    """Retrieves a user based frm user id.
    """
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """Routines before each request's resolution.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Retrieves the locale.
    """
    locale = request.args.get('locale', '')
    if locale in valid_languages:
        return locale
    if g.user and g.user.get('locale') in valid_languages:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in valid_languages:
        return header_locale
    return default_locale


@babel.timezoneselector
def get_timezone() -> str:
    """Retrieves the timezone.
    """
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user.get('timezone', '')
    if timezone:
        return timezone if timezone in pytz.all_timezones else default_timezone
    return default_timezone


@app.route('/')
def get_index() -> str:
    """Home/index page.
    """
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
