import ctypes as ct
import winreg
from pathlib import Path

from .error import VMError


class Binds:
    VM_KEY = "VB:Voicemeeter {17359A74-1236-5467}"
    BITS = 64 if ct.sizeof(ct.c_voidp) == 8 else 32

    def __init__(self):
        dll_path = Path(self.__vmpath()).parent.joinpath(
            f'VoicemeeterRemote{"64" if self.BITS == 64 else ""}.dll'
        )
        if self.BITS == 64:
            self.libc = ct.CDLL(str(dll_path))
        else:
            self.libc = ct.WinDLL(str(dll_path))

    def __vmpath(self):
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"{}".format(
                "\\".join(
                    (
                        "\\".join(
                            filter(
                                None,
                                (
                                    "SOFTWARE",
                                    "WOW6432Node" if self.BITS == 64 else "",
                                    "Microsoft",
                                    "Windows",
                                    "CurrentVersion",
                                    "Uninstall",
                                ),
                            )
                        ),
                        self.VM_KEY,
                    )
                )
            ),
        ) as vm_key:
            return winreg.QueryValueEx(vm_key, r"UninstallString")[0]

    def call(self, fn, *args, ok=(0,)):
        retval = getattr(self.libc, fn)(*args)
        if retval not in ok:
            raise VMError(f"{fn} returned {retval}")
        return retval
