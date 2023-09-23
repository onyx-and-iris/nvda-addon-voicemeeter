import ctypes as ct

from logHandler import log

from .binds import Binds
from .context import Context, StripStrategy
from .kinds import KindId


class Controller:
    def __init__(self):
        self.binds = Binds()
        self.ctx = Context(StripStrategy(self, 0))

    def login(self):
        retval = self.binds.call("VBVMR_Login", ok=(0, 1))
        log.info("INFO - logged into Voicemeeter Remote API")
        return retval

    def logout(self):
        self.binds.call("VBVMR_Logout")
        log.info("NFO - logged out of Voicemeeter Remote API")

    @property
    def kind_id(self):
        c_type = ct.c_long()
        self.binds.call("VBVMR_GetVoicemeeterType", ct.byref(c_type))
        return KindId(c_type.value).name.lower()

    def run_voicemeeter(self, kind_id):
        val = kind_id.value
        if val == 3 and Binds.BITS == 64:
            val = 6
        self.binds.call("VBVMR_RunVoicemeeter", val)

    def __clear(self):
        while self.binds.call("VBVMR_IsParametersDirty", ok=(0, 1)) == 1:
            pass

    def _get(self, param):
        self.__clear()
        buf = ct.c_float()
        self.binds.call("VBVMR_GetParameterFloat", param.encode(), ct.byref(buf))
        return buf.value

    def _set(self, param, val):
        self.binds.call("VBVMR_SetParameterFloat", param.encode(), ct.c_float(float(val)))
