import ui
from logHandler import log

from . import context


class CommandsMixin:
    ### ANNOUNCEMENTS ###

    def script_announce_voicemeeter_version(self, _):
        ui.message(f'Running Voicemeeter {self.kind} {self.controller.version} {self.controller.bits} bit')

    def script_announce_controller(self, _):
        ui.message(f'Controller for {self.controller.ctx.strategy} {self.controller.ctx.index + 1}')

    ### ALTER THE CONTEXT ###

    def script_strip_mode(self, _):
        if self.controller.ctx.index >= self.kind.num_strip:
            ui.message(f'Controller strip {self.controller.ctx.index + 1} does not exist for Voicemeeter {self.kind}')
            return
        self.controller.ctx.strategy = context.StripStrategy(self.controller, self.controller.ctx.index)
        ui.message(f'Controller for strip {self.controller.ctx.index + 1}')
        log.info(f'INFO - strip {self.controller.ctx.index} mode')

    def script_bus_mode(self, _):
        if self.controller.ctx.index >= self.kind.num_bus:
            ui.message(f'Controller bus {self.controller.ctx.index + 1} does not exist for Voicemeeter {self.kind}')
            return
        self.controller.ctx.strategy = context.BusStrategy(self.controller, self.controller.ctx.index)
        ui.message(f'Controller for {self.controller.ctx.strategy} {self.controller.ctx.index + 1}')
        log.info(f'INFO - {self.controller.ctx.strategy} {self.controller.ctx.index} mode')

    def script_index(self, gesture):
        proposed = int(gesture.displayName[-1])
        self.controller.ctx.index = proposed - 1
        ui.message(f'Controller for {self.controller.ctx.strategy} {self.controller.ctx.index + 1}')
        log.info(f'INFO - {self.controller.ctx.strategy} {self.controller.ctx.index} mode')

    def __set_slider_mode(self, mode):
        self.controller.ctx.slider_mode = mode
        ui.message(f'{mode} mode enabled')

    def script_gain_mode(self, _):
        self.__set_slider_mode('gain')

    def script_comp_mode(self, _):
        self.__set_slider_mode('comp')

    def script_gate_mode(self, _):
        self.__set_slider_mode('gate')

    def script_denoiser_mode(self, _):
        self.__set_slider_mode('denoiser')

    def script_audibility_mode(self, _):
        self.__set_slider_mode('audibility')

    # Mono is a special case because the parameter is a boolean for strips and an int for buses

    def script_rotate_mono(self, _):
        if isinstance(self.controller.ctx.strategy, context.StripStrategy):
            val = not self.controller.ctx.get_bool('mono')
            self.controller.ctx.set_bool('mono', val)
            ui.message('on' if val else 'off')
        else:
            opts = ['off', 'on', 'stereo reverse']
            val = self.controller.ctx.get_int('mono')
            new_val = (val + 1) % len(opts)
            self.controller.ctx.set_int('mono', new_val)
            ui.message(opts[new_val])

    ### BOOLEAN PARAMETERS ###

    def script_toggle_solo(self, _):
        if not isinstance(self.controller.ctx.strategy, context.StripStrategy):
            ui.message('Solo only available for strips')
            return

        val = not self.controller.ctx.get_bool('solo')
        self.controller.ctx.set_bool('solo', val)
        ui.message('on' if val else 'off')

    def script_toggle_mute(self, _):
        val = not self.controller.ctx.get_bool('mute')
        self.controller.ctx.set_bool('mute', val)
        ui.message('on' if val else 'off')

    def script_toggle_mc(self, _):
        if not isinstance(self.controller.ctx.strategy, context.StripStrategy):
            ui.message('MC only available for strips')
            return

        valid_indices_zero_based = [self.kind.phys_in]
        match self.kind.name:
            case 'potato':
                valid_indices_zero_based.append(self.kind.phys_in + self.kind.virt_in - 1)

        if self.controller.ctx.index not in valid_indices_zero_based:
            valid_indices_display = [i + 1 for i in valid_indices_zero_based]
            if len(valid_indices_display) == 1:
                ui.message(f'MC only available for strip {valid_indices_display[0]} for Voicemeeter {self.kind}')
            else:
                ui.message(
                    f'MC only available for strips {valid_indices_display[0]} and {valid_indices_display[1]} for Voicemeeter {self.kind}'
                )
            return

        val = not self.controller.ctx.get_bool('mc')
        self.controller.ctx.set_bool('mc', val)
        ui.message('on' if val else 'off')

    def script_karaoke(self, _):
        if not isinstance(self.controller.ctx.strategy, context.StripStrategy):
            ui.message('Karaoke mode only available for strips')
            return

        if self.kind.name not in ['banana', 'potato']:
            ui.message(f'Karaoke mode not available for Voicemeeter {self.kind}')
            return

        valid_index_zero_based = None
        match self.kind.name:
            case 'banana':
                valid_index_zero_based = self.kind.phys_in + self.kind.virt_in - 1
            case 'potato':
                valid_index_zero_based = self.kind.phys_in + self.kind.virt_in - 2

        if self.controller.ctx.index != valid_index_zero_based:
            ui.message(
                f'Karaoke mode only available for strip {valid_index_zero_based + 1} for Voicemeeter {self.kind}'
            )
            return

        opts = ['off', 'k m', 'k 1', 'k 2', 'k v']
        val = self.controller.ctx.get_int('karaoke')
        new_val = (val + 1) % len(opts)
        self.controller.ctx.set_int('karaoke', new_val)
        ui.message(opts[new_val])

    def script_bus_assignment(self, gesture):
        if not isinstance(self.controller.ctx.strategy, context.StripStrategy):
            ui.message('Bus assignment only available for strips')
            return

        proposed = int(gesture.displayName[-1])
        if proposed - 1 < self.kind.phys_out:
            output = f'A{proposed}'
        else:
            output = f'B{proposed - self.kind.phys_out}'
        val = not self.controller.ctx.get_bool(output)
        self.controller.ctx.set_bool(output, val)
        ui.message('on' if val else 'off')

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
