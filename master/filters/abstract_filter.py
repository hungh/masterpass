from abc import ABCMeta, abstractmethod


class AbstractFilter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def filter(self, request_handler):
        pass
