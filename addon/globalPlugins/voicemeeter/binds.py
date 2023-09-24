import ctypes as ct
from ctypes.wintypes import CHAR, FLOAT, LONG

from .cdll import libc
from .error import VMCAPIError


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

    bind_is_parameters_dirty = libc.VBVMR_IsParametersDirty
    bind_is_parameters_dirty.restype = LONG
    bind_is_parameters_dirty.argtypes = None

    bind_get_parameter_float = libc.VBVMR_GetParameterFloat
    bind_get_parameter_float.restype = LONG
    bind_get_parameter_float.argtypes = [ct.POINTER(CHAR), ct.POINTER(FLOAT)]

    bind_set_parameter_float = libc.VBVMR_SetParameterFloat
    bind_set_parameter_float.restype = LONG
    bind_set_parameter_float.argtypes = [ct.POINTER(CHAR), FLOAT]

    def call(self, fn, *args, ok=(0,)):
        retval = fn(*args)
        if retval not in ok:
            raise VMCAPIError(fn.bind_namebind_, retval)
        return retval
