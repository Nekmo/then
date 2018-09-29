from dataclasses import dataclass

from then.components.command import CommandMessageBase, CommandBase, PathComponent, PathMessage


@dataclass
class AudioMessage(PathMessage, CommandMessageBase):
    """:class:`AudioMessage` instance created by :class:`Audio` component. Create It using::

        from then.components import Audio

        message = Audio().message(file='/path/to/audio.flac')
        message.send()

    :arg path: Audio file path to play.
    """
    path: str
    component: 'Audio' = None

    def get_cmd(self):
        return ["ffplay", "-nodisp", "-autoexit", self.get_next()]


@dataclass
class Audio(PathComponent, CommandBase):
    """Create a Audio instance to send a message to a user or channel::

        from then.components import Audio

        Audio().send(path='/path/to/audio.mp3')

    Without params.
    """
    action: str = 'ordered'
    pattern: str = '*'
    on_end: str = 'repeat'
    _message_class = AudioMessage
