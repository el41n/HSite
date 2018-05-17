from bs4 import BeautifulSoup
import urllib.request
import re
import abc


class Parser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def request(self, url):
        pass

    @abc.abstractmethod
    def find_processor_list(self):
        pass

    @abc.abstractmethod
    def find_processor_info(self):
        pass
