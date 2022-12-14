import abc

from ..utils import ObjectMetaclass

class Provider(metaclass=ObjectMetaclass):

    @abc.abstractmethod
    def get_device(self, device_id, device_name):
        pass

class Device(metaclass=ObjectMetaclass):

    def __init__(self, device, name):
        self.device = device
        self.device_name = name

    @abc.abstractmethod
    def turn_on(self):
        pass

    @abc.abstractmethod
    def turn_off(self):
        pass

    @abc.abstractmethod
    def switch(self):
        pass

    @property
    def name(self):
        return f'{super().name} {self.device_name}'
