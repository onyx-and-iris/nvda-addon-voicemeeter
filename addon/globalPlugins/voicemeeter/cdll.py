import ctypes as ct
import platform
from pathlib import Path

from .error import VMAddonError

try:
    import winreg
except ImportError as e:
    ERR_MSG = 'winreg module not found, only Windows OS supported'
    raise VMAddonError(ERR_MSG) from e

# Defense against edge cases where winreg imports but we're not on Windows
if platform.system() != 'Windows':
    ERR_MSG = f'Unsupported OS: {platform.system()}, only Windows OS supported'
    raise VMAddonError(ERR_MSG)

BITS = 64 if ct.sizeof(ct.c_voidp) == 8 else 32

VM_KEY = 'VB:Voicemeeter {17359A74-1236-5467}'
REG_KEY = '\\'.join(
    filter(
        None,
        (
            'SOFTWARE',
            'WOW6432Node' if BITS == 64 else '',
            'Microsoft',
            'Windows',
            'CurrentVersion',
            'Uninstall',
        ),
    )
)


def get_vmpath():
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'{}'.format('\\'.join((REG_KEY, VM_KEY)))) as vm_key:
        return winreg.QueryValueEx(vm_key, r'UninstallString')[0]


try:
    vm_parent = Path(get_vmpath()).parent
except FileNotFoundError as e:
    ERR_MSG = 'Voicemeeter installation not found in registry'
    raise VMAddonError(ERR_MSG) from e

DLL_NAME = f'VoicemeeterRemote{"64" if BITS == 64 else ""}.dll'

dll_path = vm_parent.joinpath(DLL_NAME)
if not dll_path.is_file():
    ERR_MSG = f'Could not find {dll_path}'
    raise VMAddonError(ERR_MSG)

libc = ct.WinDLL(str(dll_path))
