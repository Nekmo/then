from .yeelight import Yeelight, YeelightMessage
from .broadlink import BroadLink, BroadLinkMessage
from .slack import Slack, SlackMessage
from .email import Email, EmailMessage
from .command import Command, CommandMessage
from .homeassistant import HomeAssistant, HomeAssistantMessage
from .audio import Audio, AudioMessage
from .discord import Discord, DiscordMessage
from .hangouts import Hangouts, HangoutsMessage
from .http import Http, HttpMessage
from .ifttt import Ifttt, IftttMessage
from .line import Line, LineMessage
from .log import Log, LogMessage
from .openhab import OpenHab, OpenHabMessage
from .sms import Sms, SmsMessage
from .telegram import Telegram, TelegramMessage
from .xmpp import Xmpp, XmppMessage

__all__ = [
    'Yeelight',
    'BroadLink',
    'Slack',
    'Email',
    'Command',
    'HomeAssistant',
    'Audio',
    'Discord',
    'Hangouts',
    'Http',
    'Ifttt',
    'Line',
    'Log',
    'OpenHab',
    'Sms',
    'Telegram',
    'Xmpp',
]


def get_component_by_name(name: str):
    name = name.lower()
    return getattr(globals(), {component_name.lower(): component_name for component_name in __all__}[name])
