from kagenda import cal, printer, speech, wx
import datetime


def today_for_printing(date, forecast, events_today, events_tomorrow):
    date = datetime.date.today()
    s = date.isoformat() + '\n==========\n\n'
    s += forecast.string() + '\n'

    s += '\nCAL\n----------------\n'
    if len(events_today) == 0:
        s += '\nNo events today.\n'
    else:
        s += "\nScheduled today:\n"
        for event in events_today:
            s += event.string() + '\n'

    if len(events_tomorrow) == 0:
        s += '\nNo events tomorrow.\n'
    else:
        s += "\nScheduled tomorrow:\n"
        for event in events_tomorrow:
            s += event.string() + '\n'

    return s


def today_for_speaking(date, forecast, events_today, events_tomorrow):
    s = 'Today is ' + speech.day_to_text(date) + '. '
    s += forecast.text()

    if len(events_today) == 0:
        s += 'No events today.'
    else:
        s += "\nScheduled today:\n"
        for event in events_today:
            s += event.text() + '\n'

    if len(events_tomorrow) == 0:
        s += 'No events tomorrow.'
    else:
        s += "\nScheduled tomorrow:\n"
        for event in events_tomorrow:
            s += event.text() + '\n'

    return s


def today(lpt=None, speak=False):
    date = datetime.date.today()
    forecast = wx.forecast()
    events_today = cal.get_events(date)
    events_tomorrow = cal.get_events(date + datetime.timedelta(days=1))

    if lpt:
        printer_text = today_for_printing(date, forecast, events_today,
                                          events_tomorrow)
        print(printer_text)

    if speak:
        speech.init()
        script = today_for_speaking(date, forecast, events_today, events_tomorrow)
        speech.ENGINE.say(script)
        speech.ENGINE.runAndWait()
