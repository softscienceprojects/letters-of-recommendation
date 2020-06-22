from markupsafe import Markup

def make_erin(value):
    return "Erin"


def datetimeformat(value, format='%d/%m/%Y %H:%M'):
    return value.strftime(format)