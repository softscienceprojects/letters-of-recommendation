import re
from markupsafe import Markup, escape

_paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')

##### JINJA FILTERS ###################

def display_blog_post(value):
    #re.sub()
    return Markup(value)

def test_erin(value):
    return "Erin"


def datetimeformat(value, format='%d/%m/%Y %H:%M'):
    return value.strftime(format)

def daydateformat(value, format='%A, %d %B %Y'):
    """
    see https://strftime.org/
    """
    return value.strftime(format)

def poststatus(value):
    if value == False:
        return "Draft"
    else:
        return ""


####### DECORATORS ####################

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function