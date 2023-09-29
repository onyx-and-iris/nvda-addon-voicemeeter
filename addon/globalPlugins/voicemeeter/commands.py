import ui
from logHandler import log

from . import context


class CommandsMixin:
    ### ANNOUNCEMENTS ###

    def script_announce_voicemeeter_version(self, _):
        ui.message(f"Running Voicemeeter {self.kind} {self.controller.version}")

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

    def __set_slider_mode(self, mode):
        self.controller.ctx.slider_mode = mode
        ui.message(f"{mode} mode enabled")

    def script_gain_mode(self, _):
        self.__set_slider_mode("gain")

    def script_comp_mode(self, _):
        self.__set_slider_mode("comp")

    def script_gate_mode(self, _):
        self.__set_slider_mode("gate")

    def script_denoiser_mode(self, _):
        self.__set_slider_mode("denoiser")

    def script_audibility_mode(self, _):
        self.__set_slider_mode("audibility")

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
        opts = ["off", "k m", "k 1", "k 2", "k v"]
        val = self.controller.ctx.get_int("karaoke") + 1
        if val == len(opts):
            val = 0
        self.controller.ctx.set_int("karaoke", val)
        ui.message(opts[val])

    def script_bus_assignment(self, gesture):
        proposed = int(gesture.displayName[-1])
        if proposed - 1 < self.kind.phys_out:
            output = f"A{proposed}"
        else:
            output = f"B{proposed - self.kind.phys_out}"
        val = not self.controller.ctx.get_bool(output)
        self.controller.ctx.set_bool(output, val)
        ui.message("on" if val else "off")

    ### CONTROL SLIDERS ###

    def script_slider_increase_by_point_one(self, gesture):
        val = self.controller.ctx.get_float(self.controller.ctx.slider_mode) + 0.1
        self.controller.ctx.set_float(self.controller.ctx.slider_mode, val)
        ui.message(str(round(val, 1)))

    def script_slider_decrease_by_point_one(self, gesture):
        val = self.controller.ctx.get_float(self.controller.ctx.slider_mode) - 0.1
        self.controller.ctx.set_float(self.controller.ctx.slider_mode, val)
        ui.message(str(round(val, 1)))

    def script_slider_increase_by_one(self, gesture):
        val = self.controller.ctx.get_float(self.controller.ctx.slider_mode) + 1
        self.controller.ctx.set_float(self.controller.ctx.slider_mode, val)
        ui.message(str(round(val, 1)))

    def script_slider_decrease_by_one(self, gesture):
        val = self.controller.ctx.get_float(self.controller.ctx.slider_mode) - 1
        self.controller.ctx.set_float(self.controller.ctx.slider_mode, val)
        ui.message(str(round(val, 1)))

    def script_slider_increase_by_three(self, gesture):
        val = self.controller.ctx.get_float(self.controller.ctx.slider_mode) + 3
        self.controller.ctx.set_float(self.controller.ctx.slider_mode, val)
        ui.message(str(round(val, 1)))

    def script_slider_decrease_by_three(self, gesture):
        val = self.controller.ctx.get_float(self.controller.ctx.slider_mode) - 3
        self.controller.ctx.set_float(self.controller.ctx.slider_mode, val)
        ui.message(str(round(val, 1)))
