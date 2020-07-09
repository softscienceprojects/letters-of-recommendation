import re
from markupsafe import Markup, escape

_paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')


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