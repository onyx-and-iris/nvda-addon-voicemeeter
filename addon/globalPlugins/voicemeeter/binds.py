import ctypes as ct
from ctypes.wintypes import CHAR, FLOAT, LONG

from .cdll import libc
from .error import VMAddonCAPIError


class Binds:
    bind_login = libc.VBVMR_Login
    bind_login.restype = LONG
    bind_login.argtypes = None

    bind_logout = libc.VBVMR_Logout
    bind_logout.restype = LONG
    bind_logout.argtypes = None

    bind_run_voicemeeter = libc.VBVMR_RunVoicemeeter
    bind_run_voicemeeter.restype = LONG
    bind_run_voicemeeter.argtypes = [LONG]

    bind_get_voicemeeter_type = libc.VBVMR_GetVoicemeeterType
    bind_get_voicemeeter_type.restype = LONG
    bind_get_voicemeeter_type.argtypes = [ct.POINTER(LONG)]

    bind_get_voicemeeter_version = libc.VBVMR_GetVoicemeeterVersion
    bind_get_voicemeeter_version.restype = LONG
    bind_get_voicemeeter_version.argtypes = [ct.POINTER(LONG)]

    bind_is_parameters_dirty = libc.VBVMR_IsParametersDirty
    bind_is_parameters_dirty.restype = LONG
    bind_is_parameters_dirty.argtypes = None

    bind_get_parameter_float = libc.VBVMR_GetParameterFloat
    bind_get_parameter_float.restype = LONG
    bind_get_parameter_float.argtypes = [ct.POINTER(CHAR), ct.POINTER(FLOAT)]

    bind_set_parameter_float = libc.VBVMR_SetParameterFloat
    bind_set_parameter_float.restype = LONG
    bind_set_parameter_float.argtypes = [ct.POINTER(CHAR), FLOAT]

    def _call(self, fn, *args, ok=(0,)):
        retval = fn(*args)
        if retval not in ok:
            raise VMAddonCAPIError(fn.__name__, retval)
        return retval

    def login(self):
        return self._call(self.bind_login, ok=(0, 1))

    def logout(self):
        return self._call(self.bind_logout)

    def run_voicemeeter(self, kind_val):
        return self._call(self.bind_run_voicemeeter, kind_val)

    def get_voicemeeter_type(self, c_type):
        return self._call(self.bind_get_voicemeeter_type, ct.byref(c_type))

    def get_voicemeeter_version(self, ver):
        return self._call(self.bind_get_voicemeeter_version, ct.byref(ver))

    def is_parameters_dirty(self):
        return self._call(self.bind_is_parameters_dirty, ok=(0, 1))

    def get_parameter_float(self, param, buf):
        return self._call(self.bind_get_parameter_float, param, ct.byref(buf))

    def set_parameter_float(self, param, val):
        return self._call(self.bind_set_parameter_float, param, val)
