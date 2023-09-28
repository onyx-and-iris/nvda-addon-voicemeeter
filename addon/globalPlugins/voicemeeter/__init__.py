import time

import globalPluginHandler

from . import config, util
from .commands import CommandsMixin
from .controller import Controller
from .kinds import KindId, request_kind_map


class GlobalPlugin(CommandsMixin, globalPluginHandler.GlobalPlugin):
    __kind_id = config.get("voicemeeter", "potato")
    __gestures = util._make_gestures(__kind_id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = Controller()
        if self.controller.login() == 1:
            self.controller.run_voicemeeter(KindId[self.__kind_id.upper()])
            time.sleep(1)
        self.kind = request_kind_map(self.__kind_id)

    def terminate(self, *args, **kwargs):
        super().terminate(*args, **kwargs)
        self.controller.logout()
