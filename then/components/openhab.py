from dataclasses import dataclass

from then.components.http import HttpMessageOwnApiBase, HttpBase


@dataclass
class OpenHabMessage(HttpMessageOwnApiBase):
    """:class:`OpenHabMessage` instance created by :class:`OpenHab` component. Create It using::

        from then.components import OpenHab

        message = OpenHab(...).message(item='otheritem', state='OFF')
        message.send()

    :arg item: OpenHab item to enable/disable
    :arg state: State to send. Options ``ON``/``OFF``. ``ON`` by default.
    """
    item: str
    state: str = 'ON'
    default_port: int = 8080
    component: 'OpenHab' = None

    def get_url(self):
        """Open Hab url

        :return: url
        :rtype: str
        """
        url = super().get_url()
        url += '/rest/items/{}'.format(self.item)
        return url

    def get_body(self):
        return self.state


@dataclass
class OpenHab(HttpBase):
    """Create a OpenHab instance to send a message to a user or channel::

        from then.components import OpenHab

        OpenHab(url="192.168.1.140")\\
            .send(item='myitem')

    :param url: Home Assistant address. Syntax: ``[<protocol>://]<server>[:<port>]``.
    :param timeout: Connection timeout to send message.
    """
    url: str
    timeout: int = 15
    method: str = 'post'
    content_type: str = 'text/plain'
