import ctypes as ct

from logHandler import log

from .binds import Binds
from .cdll import BITS
from .context import Context, StripStrategy
from .kinds import KindId


class Controller(Binds):
    def __init__(self):
        self.ctx = Context(StripStrategy(self, 0))

    def login(self):
        retval = self.call(self.bind_login, ok=(0, 1))
        log.info("INFO - logged into Voicemeeter Remote API")
        return retval

    def logout(self):
        self.call(self.bind_logout)
        log.info("NFO - logged out of Voicemeeter Remote API")

    @property
    def kind_id(self):
        c_type = ct.c_long()
        self.call(self.bind_get_voicemeeter_type, ct.byref(c_type))
        return KindId(c_type.value).name.lower()

    def run_voicemeeter(self, kind_id):
        val = kind_id.value
        if val == 3 and BITS == 64:
            val = 6
        self.call(self.bind_run_voicemeeter, val)

    def __clear(self):
        while self.call(self.bind_is_parameters_dirty, ok=(0, 1)) == 1:
            pass

    def _get(self, param):
        self.__clear()
        buf = ct.c_float()
        self.call(self.bind_get_parameter_float, param.encode(), ct.byref(buf))
        return buf.value

    def _set(self, param, val):
        self.call(self.bind_set_parameter_float, param.encode(), ct.c_float(float(val)))
