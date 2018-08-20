from dataclasses import dataclass

from then.components.command import CommandMessageBase, CommandBase


@dataclass
class AudioMessage(CommandMessageBase):
    """:class:`AudioMessage` instance created by :class:`Audio` component. Create It using::

        from then.components import Audio

        message = Audio().message(file='/path/to/audio.flac')
        message.send()

    :arg file: Audio file path to play.
    """
    file: str
    component: 'Audio' = None

    def get_cmd(self):
        return ["ffplay", "-nodisp", "-autoexit", self.file]


@dataclass
class Audio(CommandBase):
    """Create a Audio instance to send a message to a user or channel::

        from then.components import Audio

        Audio().send(file='/path/to/audio.mp3')

    Without params.
    """
    _message_class = AudioMessage
