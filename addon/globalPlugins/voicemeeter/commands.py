import ui
from logHandler import log

from . import context, util


class CommandsMixin:
    ### ANNOUNCEMENTS ###

    def script_announce_voicemeeter_version(self, _):
        ui.message(f"Running Voicemeeter {self.kind}")

    def script_announce_controller(self, _):
        ui.message(f"Controller for {self.controller.ctx.strategy} {self.controller.ctx.index + 1}")

    ### ALTER THE CONTEXT ###

    def script_strip_mode(self, _):
        if self.controller.ctx.index >= self.kind.num_strip:
            ui.message(f"Controller strip {self.controller.ctx.index + 1} does not exist for Voicemeeter {self.kind}")
            return
        self.controller.ctx.strategy = context.StripStrategy(self.controller, self.controller.ctx.index)
        ui.message(f"Controller for strip {self.controller.ctx.index + 1}")
        log.info(f"INFO - strip {self.controller.ctx.index} mode")

    def script_bus_mode(self, _):
        if self.controller.ctx.index >= self.kind.num_bus:
            ui.message(f"Controller bus {self.controller.ctx.index + 1} does not exist for Voicemeeter {self.kind}")
            return
        self.controller.ctx.strategy = context.BusStrategy(self.controller, self.controller.ctx.index)
        ui.message(f"Controller for {self.controller.ctx.strategy} {self.controller.ctx.index + 1}")
        log.info(f"INFO - {self.controller.ctx.strategy} {self.controller.ctx.index} mode")

    def script_index(self, gesture):
        proposed = int(gesture.displayName[-1])
        self.controller.ctx.index = proposed - 1
        ui.message(f"Controller for {self.controller.ctx.strategy} {self.controller.ctx.index + 1}")
        log.info(f"INFO - {self.controller.ctx.strategy} {self.controller.ctx.index} mode")

    def script_slider_mode(self, gesture):
        if gesture.displayName.endswith("g"):
            self.controller.ctx.slider_mode = "gain"
        elif gesture.displayName.endswith("c"):
            self.controller.ctx.slider_mode = "comp"
        elif gesture.displayName.endswith("t"):
            self.controller.ctx.slider_mode = "gate"
        elif gesture.displayName.endswith("d"):
            self.controller.ctx.slider_mode = "denoiser"
        elif gesture.displayName.endswith("a"):
            self.controller.ctx.slider_mode = "audibility"
        ui.message(f"{self.controller.ctx.slider_mode} mode enabled")

    ### BOOLEAN PARAMETERS ###

    def script_toggle_mono(self, _):
        val = not self.controller.ctx.get_bool("mono")
        self.controller.ctx.set_bool("mono", val)
        ui.message("on" if val else "off")

    def script_toggle_solo(self, _):
        val = not self.controller.ctx.get_bool("solo")
        self.controller.ctx.set_bool("solo", val)
        ui.message("on" if val else "off")

    def script_toggle_mute(self, _):
        val = not self.controller.ctx.get_bool("mute")
        self.controller.ctx.set_bool("mute", val)
        ui.message("on" if val else "off")

    def script_toggle_mc(self, _):
        val = not self.controller.ctx.get_bool("mc")
        self.controller.ctx.set_bool("mc", val)
        ui.message("on" if val else "off")

    def script_karaoke(self, _):
        val = self.controller.ctx.get_int("karaoke") + 1
        if val == 5:
            val = 0
        self.controller.ctx.set_int("karaoke", val)
        ui.message(val)

    def script_bus_assignment(self, gesture):
        proposed = int(gesture.displayName[-1])
        if proposed - 1 < self.kind.phys_out:
            output = f"A{proposed}"
        else:
            output = f"B{proposed - self.kind.phys_out}"
        val = not self.controller.ctx.get_bool(output)
        self.controller.ctx.set_bool(output, val)
        ui.message("on" if val else "off")

    ### SLIDER MODES ###

    def script_slider_increase(self, gesture):
        op = util.remove_prefix(gesture.displayName, "kb:NVDA+shift+")
        if op.startswith("alt"):
            offset = 0.1
        elif op.startswith("ctrl"):
            offset = 3
        else:
            offset = 1
        val = self.controller.ctx.get_float(self.controller.ctx.slider_mode) + offset
        self.controller.ctx.set_float(self.controller.ctx.slider_mode, val)
        ui.message(str(round(val, 1)))

    def script_slider_decrease(self, gesture):
        op = util.remove_prefix(gesture.displayName, "kb:NVDA+shift+")
        if op.startswith("alt"):
            offset = 0.1
        elif op.startswith("ctrl"):
            offset = 3
        else:
            offset = 1
        val = self.controller.ctx.get_float(self.controller.ctx.slider_mode) - offset
        self.controller.ctx.set_float(self.controller.ctx.slider_mode, val)
        ui.message(str(round(val, 1)))
