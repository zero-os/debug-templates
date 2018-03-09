from js9 import j
from zerorobot.template.base import TemplateBase
import gevent


class Benchmarker(TemplateBase):

    version = '0.0.1'
    template_name = 'benchmarker'

    def __init__(self, name, guid=None, data=None):
        super().__init__(name=name, guid=guid, data=data)

    @property
    def node_sal(self):
        return j.clients.zero_os.sal.node_get(self.data['node'])

    def load_generater_start(self, size='1M', period=1):
        self.gl_mgr.add('load_generater', self._load_generater, size=size, period=period)

    def load_generater_stop(self):
        self.gl_mgr.stop('load_generater')

    def _load_generater(self, size, period):
        while True:
            self.logger.info("load generater running...")
            ps = []
            for _ in range(5):
                ps.append(self.node_sal.client.system('dd if=/dev/urandom bs=%s count=1' % size))
            for p in ps:
                p.get()
            gevent.sleep(period)
