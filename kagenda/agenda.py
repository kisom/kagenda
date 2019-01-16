from kagenda import cal, config, printer, speech, todo, wx
import datetime


def today_for_printing(date, forecast, events_today, events_tomorrow, todos):
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

    if len(todos) != 0:
        s += '\nTODO\n' + todos.string()
    return s


def today_for_speaking(date, forecast, events_today, events_tomorrow, todos):
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

    if len(todos) != 0:
        s += '\nTwo dues\n' + todos.text()
    return s


def today(lpt=None, speak=False):
    creds = config.get_creds_file('credentials.json')
    date = datetime.date.today()
    forecast = wx.forecast(creds)
    events_today = cal.get_events(date)
    events_tomorrow = cal.get_events(date + datetime.timedelta(days=1))
    todos = todo.get_todo_list(creds)

    if lpt:
        printer_text = today_for_printing(date, forecast, events_today,
                                          events_tomorrow, todos)
        print(printer_text)

    if speak:
        speech.init()
        script = today_for_speaking(date, forecast, events_today,
                                    events_tomorrow, todos)
        speech.ENGINE.say(script)
        speech.ENGINE.runAndWait()
