import ctypes as ct

from logHandler import log

from . import config
from .binds import Binds
from .cdll import BITS
from .context import Context, StripStrategy
from .kinds import KindId


class Controller:
    def __init__(self):
        self._binds = Binds()
        self.ctx = Context(StripStrategy(self, 0))
        self.bits = config.get('bits', BITS)

    def login(self):
        retval = self._binds.login()
        log.info('INFO - logged into Voicemeeter Remote API')
        return retval

    def logout(self):
        self._binds.logout()
        log.info('NFO - logged out of Voicemeeter Remote API')

    @property
    def kind_id(self):
        c_type = ct.c_long()
        self._binds.get_voicemeeter_type(c_type)
        return KindId(c_type.value).name.lower()

    @property
    def version(self):
        ver = ct.c_long()
        self._binds.get_voicemeeter_version(ver)
        return '{}.{}.{}.{}'.format(
            (ver.value & 0xFF000000) >> 24,
            (ver.value & 0x00FF0000) >> 16,
            (ver.value & 0x0000FF00) >> 8,
            ver.value & 0x000000FF,
        )

    def run_voicemeeter(self, kind_id):
        val = kind_id.value
        if self.bits == 64:
            val += 3
        self._binds.run_voicemeeter(val)

    def __clear(self):
        while self._binds.is_parameters_dirty() == 1:
            pass

    def get(self, param):
        self.__clear()
        buf = ct.c_float()
        self._binds.get_parameter_float(param.encode(), buf)
        return buf.value

    def set(self, param, val):
        self._binds.set_parameter_float(param.encode(), ct.c_float(float(val)))
