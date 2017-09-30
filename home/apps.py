from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class HomeConfig(AppConfig):
    name = 'home'


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
