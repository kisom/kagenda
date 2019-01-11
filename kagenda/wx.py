import kagenda.config as config
import darksky
import json
import math

def get_api_key(path='credentials.json'):
    with open(path, 'rt') as credentials:
        parsed_creds = json.loads(credentials.read())
        return parsed_creds['darksky']

def f2c(temp, low=False):
    ctemp = (temp - 32) * 5.0 / 9.0
    if low:
        return math.floor(ctemp)
    return math.ceil(ctemp)

def forecast():
    api_key = get_api_key()
    forecast = darksky.forecast(api_key, config.OAKLAND[0], config.OAKLAND[1])
    return Forecast(forecast)


class Forecast:

    def __init__(self, ds_forecast):
        today = ds_forecast.daily[0]
        self.low = f2c(today.temperatureLow, low=True)
        self.high = f2c(today.temperatureHigh)
        self.humidity = today.humidity
        self.summary = today.summary

    def string(self):
        return 'WX\n----------------\nL: {}C / H: {}C\nHUM: {}\n{}'.format(
            self.low, self.high, self.humidity, self.summary
        )

    def text(self):
        s = 'Today is forecasted to have a low of {} degrees '.format(self.low)
        s += 'with a high of {} degrees, '.format(self.high)

        humidity = round(self.humidity * 100)
        s += ' with {} percent humidity. '.format(humidity)
        s += 'It is expected to be ' + self.summary.lower() + '. '
        return s