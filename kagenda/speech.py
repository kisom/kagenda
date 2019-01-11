import datetime
import natural.number
import pyttsx3

ENGINE = pyttsx3.init()

def init():
    ENGINE.setProperty('rate', 140)

def day_to_text(date):
    month = date.strftime('%B')
    day = natural.number.ordinal(date.day)
    return month + ' the ' + day
