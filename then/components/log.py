import logging
import uuid

from dataclasses import dataclass

from then.components.base import Message, Component
from then.exceptions import ValidationError

LEVELS = {
    'CRITICAL',
    'ERROR',
    'WARNING',
    'INFO',
    'DEBUG',
}


@dataclass
class LogMessage(Message):
    body: str
    level: str = 'INFO'
    component: 'Log' = None

    def __post_init__(self):
        if self.level.upper() not in LEVELS:
            raise ValidationError('Error on {}: Invalid logger level {}'.format(self.component.name, self.level))

    def send(self):
        getattr(self.component.logger, self.level.lower())(self.body)


@dataclass
class Log(Component):
    level: int = logging.DEBUG
    formatter: str = '%(asctime)s - %(name)s - %(levelname)-7s - %(message)s'
    file: str = None
    console: bool = False

    _message_class = LogMessage

    def __post_init__(self):
        self.logger = logging.getLogger(uuid.uuid4().hex)
        self.logger.setLevel(self.level)
        if self.console:
            self.add_handler(logging.StreamHandler())
        if self.file:
            self.add_handler(logging.FileHandler(self.file))

    def add_handler(self, handler):
        handler.setLevel(self.level)
        # create formatter
        formatter = logging.Formatter(self.formatter)
        # add formatter to handler
        handler.setFormatter(formatter)
        # add handler to logger
        self.logger.addHandler(handler)
