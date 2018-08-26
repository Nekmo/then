"""This component allows you to control a Xiaomi Yeelight Bulb
device.
"""
from __future__ import absolute_import

import inspect
from dataclasses import dataclass

from then.components.base import Component, Message
from then.components.log import Log
from then.exceptions import ExecuteError
from then.utils import COLORS_NAMES

logger = Log(logger_name=__name__, console=True)


def list_devices(bulbs):
    for bulb in bulbs:
        logger.info('Yeelight bulb detected. IP: {}.'.format(bulb['ip']))
    if len(bulbs) > 1:
        logger.info('More than one Yeelight bulb detected It will try to use the first device. '
                    'To improve performance and avoid errors, add your device to the configuration.')
    elif bulbs:
        logger.info('One Yeelight bulb detected. To improve performance and avoid errors, add '
                    'your device to the configuration.')
    else:
        raise ExecuteError('Yeelight Error: Unable to detect a Yeelight bulb. Maybe the device is turned '
                           'off or there is a problem with the network.')


@dataclass
class YeelightMessage(Message):
    """:class:`YeelightMessage` instance created by :class:`Yeelight` component. Create It using::

        from then.components import Yeelight

        message = Yeelight(...).message(packet="...")
        message.send()

    :arg state: ON|OFF|TOGGLE state. By default ON.
    :arg brightness: 0-100 brightness value.
    :arg color: hexadecimal or name color.
    :arg temperature: 1700-6500K temperature color.
    :arg effect: power on->off or off->on effect. Choices: "smooth" or "sudden".
    :arg effect_duration: smooth effect duration. Only available for smooth.
    :arg flow_transition: Transition availables: disco, temp, strobe, pulse, strobe_color, alarm,
                          police, police2, lsd, christmas, rgb, randomloop, slowdown
    :arg flow_count: Flow repeat counts
    """
    state: str = 'ON'
    brightness: int = None
    color: str = None
    temperature: int = None
    # Power ON/OFF effects
    effect: str = 'smooth'
    effect_duration: int = 300
    flow_transition: str = None
    flow_count: int = 1
    flow_duration: int = None
    flow_sleep: int = None
    component: 'Yeelight' = None

    def __post_init__(self):
        if self.state:
            self.state = self.state.upper()
        self._color = None
        if self.color:
            color = COLORS_NAMES.get(self.color, self.color).upper().lstrip('#')
            self._color = tuple(int(color[i:i+2], 16) for i in (0, 2 ,4))

    def get_bulb(self):
        from yeelight import Bulb, discover_bulbs
        ip = self.component.ip
        if not ip:
            devices = discover_bulbs()
            list_devices(devices)
            ip = devices[0]['ip']
        return Bulb(ip)

    def send(self):
        from yeelight import Flow
        from yeelight import transitions
        bulb = self.get_bulb()
        state = self.state
        if state == 'TOGGLE':
            state = {'off': 'ON', 'on': 'OFF'}[bulb.get_properties(['power'])['power']]
        if state == 'ON':
            bulb.turn_on(effect=self.effect, duration=self.effect_duration)
        elif state == 'OFF':
            bulb.turn_off(effect=self.effect, duration=self.effect_duration)
        if self.flow_transition:
            trans = getattr(transitions, self.flow_transition)
            if self.flow_transition == 'pulse':
                trans = trans(*self._color, self.flow_duration or 250, self.brightness or 100)
            else:
                kwargs = {'duration': self.flow_duration, 'brightness': self.brightness,
                          'sleep': self.flow_sleep}
                spec = inspect.getargspec(trans)
                kwargs = {key: value for key, value in kwargs.items() if key in spec.args and value is not None}
                trans = trans(**kwargs)
            bulb.start_flow(Flow(count=self.flow_count, transitions=trans))
        elif self._color:
            bulb.set_rgb(*self._color)
        elif self.brightness:
            bulb.set_brightness(self.brightness)
        elif self.temperature:
            bulb.set_color_temp(self.temperature)


@dataclass
class Yeelight(Component):
    """Create a Yeelight instance to control a Xiaomi Yeelight Bulb::

        from then.components import Yeelight

        Yeelight(ip='192.168.x.xx')\\
            .send(flow_transition='pulse', flow_count=1, color='blue')

    :param ip: Yeelight bulb IP.
    """
    ip: str = None
    _message_class = YeelightMessage

    def message(self, context=None, **kwargs) -> YeelightMessage:
        return super(Yeelight, self).message(context, **kwargs)
