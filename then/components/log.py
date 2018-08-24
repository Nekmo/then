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
    """:class:`LogMessage` instance created by :class:`Log` component. Create It using::

        from then.components import Log

        message = Log().message(body="Log message")
        message.send()

    :arg body: message to log
    """
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
    """Create a Log instance to log to file or console::

        from then.components import Log

        Log(file="/path/to/file.log", console=True)\\
            .send(body="Log message")

    :param file: Path to log file
    :param console: Boolean. Log to screen
    :param formatter: Log handler formatter
    """
    file: str = None
    console: bool = False
    formatter: str = '%(asctime)s - %(name)s - %(levelname)-7s - %(message)s'
    level: int = logging.DEBUG

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
