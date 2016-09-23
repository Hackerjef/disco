import logging
import gevent

from holster.emitter import Emitter

from disco.state import State
from disco.api.client import APIClient
from disco.gateway.client import GatewayClient

log = logging.getLogger(__name__)


class DiscoClient(object):
    def __init__(self, token, sharding=None):
        self.log = log
        self.token = token
        self.sharding = sharding or {'number': 0, 'total': 1}

        self.events = Emitter(gevent.spawn)

        self.state = State(self)
        self.api = APIClient(self)
        self.gw = GatewayClient(self)

    def run(self):
        return gevent.spawn(self.gw.run)

    def run_forever(self):
        return self.gw.run()
