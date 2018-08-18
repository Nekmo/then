from dataclasses import dataclass

from then.components.command import CommandMessageBase, CommandBase


@dataclass
class AudioMessage(CommandMessageBase):
    file: str
    component: 'Audio' = None

    def get_cmd(self):
        return ["ffplay", "-nodisp", "-autoexit", self.file]


@dataclass
class Audio(CommandBase):
    _message_class = AudioMessage
