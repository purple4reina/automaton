import abc
import datetime
import inspect
import random

from .sensors import AQISensor, TimeSensor, WeatherSensor, WebhookSensor
from .utils import ObjectMetaclass

class _Trigger(metaclass=ObjectMetaclass):

    @abc.abstractmethod
    def check(self):
        pass

class AQITrigger(_Trigger):

    def __init__(self, check_func, api_key, latitude, longitude,
            aqi_sensor=None):
        self.check_func = check_func
        self.aqi_sensor = aqi_sensor or AQISensor(api_key, latitude, longitude)

    def check(self):
        aqi = self.aqi_sensor.get_aqi()
        return self.check_func(aqi)

class IsoWeekdayTrigger(_Trigger):

    # TODO: test timezone

    def __init__(self, isoweekdays, time_sensor):
        self.isoweekdays = isoweekdays
        self.time_sensor = time_sensor or TimeSensor()

    def check(self):
        now = self.time_sensor.get_current_datetime()
        return now.isoweekday() in self.isoweekdays

class TimeTrigger(_Trigger):

    # TODO: test timezone

    def __init__(self, times, time_sensor):
        self.times = times
        self.time_sensor = time_sensor or TimeSensor()

    def check(self):
        now = self.time_sensor.get_current_datetime()
        now_minutes = 60*now.hour + now.minute
        for minutes in self.times:
            if minutes == now_minutes:
                return True
        return False

class RandomTrigger(_Trigger):

    def __init__(self, probability):
        self.probability = probability

    def check(self):
        return random.random() < self.probability

class _SunTrigger(_Trigger):

    # TODO: test timezone
    # TODO: test lat/long

    def __init__(self, timedeltas, latitude, longitude, time_sensor,
            sun_sensor=None):
        from .sensors import SunSensor
        self.timedeltas = timedeltas
        self.time_sensor = time_sensor or TimeSensor()
        self.sun_sensor = sun_sensor or SunSensor(latitude=latitude,
                longitude=longitude, time_sensor=self.time_sensor)
        self.sun_sensor_method = getattr(self.sun_sensor,
                self.sun_sensor_method_name)

    def check(self):
        sun_time = self.sun_sensor_method()
        sun_minutes = 60*sun_time.hour + sun_time.minute
        now = self.time_sensor.get_current_datetime()
        now_minutes = 60*now.hour + now.minute
        return now_minutes - sun_minutes in self.timedeltas

class SunriseTrigger(_SunTrigger):

    sun_sensor_method_name = 'get_sunrise'

class SunsetTrigger(_SunTrigger):

    sun_sensor_method_name = 'get_sunset'

class TemperatureTrigger(_Trigger):

    def __init__(self, check_func, weather_sensor=None, api_key=None,
            latitude=None, longitude=None):
        self.check_func = check_func
        self.weather_sensor = weather_sensor or WeatherSensor(api_key,
                latitude, longitude)

    def check(self):
        temp = self.weather_sensor.current_temperature()
        return self.check_func(temp)

class WebhookTrigger(_Trigger):

    # TODO: test webhook trigger

    def __init__(self, path, webhook_sensor=None):
        self.path = path
        self.webhook_sensor = webhook_sensor or WebhookSensor()

    def check(self):
        return self.webhook_sensor.path == self.path and \
                self.webhook_sensor.method == 'POST'
