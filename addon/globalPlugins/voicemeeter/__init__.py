import json
import time
from pathlib import Path

import globalPluginHandler
from logHandler import log

from .commands import CommandsMixin
from .controller import Controller
from .kinds import KindId, request_kind_map


def _make_gestures():
    defaults = {
        "kb:NVDA+alt+s": "strip_mode",
        "kb:NVDA+alt+b": "bus_mode",
        "kb:NVDA+shift+q": "announce_controller",
        "kb:NVDA+shift+a": "announce_voicemeeter_version",
        "kb:NVDA+shift+o": "toggle_mono",
        "kb:NVDA+shift+s": "toggle_solo",
        "kb:NVDA+shift+m": "toggle_mute",
        "kb:NVDA+shift+upArrow": "increase_gain",
        "kb:NVDA+shift+downArrow": "decrease_gain",
        "kb:NVDA+shift+alt+upArrow": "increase_gain",
        "kb:NVDA+shift+alt+downArrow": "decrease_gain",
        "kb:NVDA+shift+control+upArrow": "increase_gain",
        "kb:NVDA+shift+control+downArrow": "decrease_gain",
    }

    overrides = None
    pn = Path.home() / "Documents" / "Voicemeeter" / "keybinds.json"
    if pn.exists():
        with open(pn, "r") as f:
            data = json.load(f)
        overrides = {f"kb:{v}": k for k, v in data.items()}
        log.info("INFO - loading settings from keybinds.json")
    if overrides:
        return {**defaults, **overrides}
    return defaults


def _get_kind_id():
    pn = Path.home() / "Documents" / "Voicemeeter" / "settings.json"
    if pn.exists():
        with open(pn, "r") as f:
            data = json.load(f)
        return data["voicemeeter"]
    return "potato"


class GlobalPlugin(globalPluginHandler.GlobalPlugin, CommandsMixin):
    __gestures = _make_gestures()
    __kind_id = _get_kind_id()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = Controller()
        if self.controller.login() == 1:
            self.controller.run_voicemeeter(KindId[self.__kind_id.upper()])
            time.sleep(1)
        self.kind = request_kind_map(self.controller.kind_id)

        for i in range(1, self.kind.num_strip + 1):
            self.bindGesture(f"kb:NVDA+alt+{i}", "index")
        for i in range(1, self.kind.phys_out + self.kind.virt_out + 1):
            self.bindGesture(f"kb:NVDA+shift+{i}", "bus_assignment")

    def terminate(self, *args, **kwargs):
        super().terminate(*args, **kwargs)
        self.controller.logout()
