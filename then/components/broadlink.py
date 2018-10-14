"""This component allows you to send a IR/RF packet using a BroadLink RM
device.
"""
from __future__ import absolute_import

import base64
import binascii
import time
from typing import List
from dataclasses import dataclass

from then.components.base import Component, Message
from then.exceptions import ValidationError, ExecuteError
from then.components.log import Log



logger = Log(logger_name='broadlink', console=True)


def encode_packet(packet):
    return base64.b64encode(packet).decode()


def decode_packet(packet):
    return base64.b64decode(packet)


def hexlify_mac(mac: bytes):
    mac: str = binascii.hexlify(mac).upper()
    blocks = [mac[x:x + 2] for x in range(0, len(mac), 2)]
    return ':'.join(blocks)


def list_devices(devices):
    from broadlink import device
    devices: List[device] = devices
    for dev in devices:
        logger.info('BroadLink Device detected. HOST: {} MAC: {}.'.format(dev.host, hexlify_mac(dev.mac)))
    if len(devices) > 1:
        logger.info('More than one BroadLink device detected It will try to use the first device. '
                    'To improve performance and avoid errors, add your device to the configuration.')
    elif devices:
        logger.info('One BroadLink device detected. To improve performance and avoid errors, add '
                    'your device to the configuration.')
    else:
        raise ExecuteError('BroadLink Error: Unable to detect a BroadLink device. Maybe the device is turned '
                           'off or there is a problem with the network.')


@dataclass
class BroadLinkMessage(Message):
    """:class:`BroadLinkMessage` instance created by :class:`BroadLink` component. Create It using::

        from then.components import BroadLink

        message = BroadLink(...).message(packet="...")
        message.send()

    :arg packet: IR/RF packet to send.
    """
    packet: str
    component: 'BroadLink' = None

    def get_device(self):
        import broadlink

        if self.component.ip and self.component._mac:
            device = broadlink.rm((self.component.ip, 80), self.component._mac, None)
        else:
            devices = broadlink.discover(timeout=5)
            list_devices(devices)
            device = devices[0]
        device.auth()
        return device

    def send(self):
        device = self.get_device()
        device.send_data(decode_packet(self.packet))

    def enter_learning(self):
        device = self.get_device()
        device.enter_learning()
        logger.info('The BroadLink device has entered learning mode. Point the remote control at '
                    'the broadlink and press the button to learn.')
        logger.info('Waiting 20 seconds to show results...')
        time.sleep(20)
        packet = device.check_data()
        if packet:
            logger.info('This is your packet:\n{}'.format(encode_packet(packet)))
        else:
            logger.error('The package could not be obtained.')


@dataclass
class BroadLink(Component):
    """Create a BroadLink instance to send a IR/RF packet to a BroadLink RM device::

        from then.components import BroadLink

        BroadLink(ip='192.168.x.xx',
                  mac='34:EA:34:E3:XX:XX')\\
            .send(packet='JgBQAAABKJEUEhQRFDUUERQSFBEUERQRFDYUNRQRFDYU'
                         'NhQ2FDUUNhQRFBEUERQ2FBEUERQRFBITNhQ2FDYUERQ2'
                         'FDUUNhQ2FAAFGQABKEgUAA0FAAAAAAAAAAA=')

    :param ip: BroadLink device IP.
    :param mac: BroadLink device IP.
    """
    ip: str = None
    mac: str = None
    _message_class = BroadLinkMessage

    def __post_init__(self):
        if (self.ip and not self.mac) or (not self.ip and self.mac):
            raise ValidationError('Error on {}: to set a broadlink target you must put both an ip and a '
                                  'mac'.format(self.name))
        if self.mac:
            self._mac = binascii.unhexlify(self.mac.encode().replace(b':', b''))

    def message(self, params=None, **kwargs) -> BroadLinkMessage:
        return super(BroadLink, self).message(params, **kwargs)


def learning(ip=None, mac=None, **kwargs):
    BroadLink(ip=ip, mac=mac).message(packet=None).enter_learning()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    subparser = parser.add_subparsers()
    learning_parser = subparser.add_parser('learning')
    learning_parser.set_defaults(fn=learning)
    learning_parser.add_argument('--ip')
    learning_parser.add_argument('--mac')
    args = parser.parse_args()
    if hasattr(args, 'fn'):
        args.fn(**vars(args))
