from . import config, util
from .kinds import request_kind_map


def remove_prefix(input_string, prefix):
    if prefix and input_string.startswith(prefix):
        return input_string[len(prefix) :]
    return input_string


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[: -len(suffix)]
    return input_string


def _make_gestures(kind_id):
    kind = request_kind_map(kind_id)
    defaults = {
        "kb:NVDA+alt+s": "strip_mode",
        "kb:NVDA+alt+b": "bus_mode",
        "kb:NVDA+alt+g": "gain_mode",
        "kb:NVDA+alt+c": "comp_mode",
        "kb:NVDA+alt+t": "gate_mode",
        "kb:NVDA+alt+d": "denoiser_mode",
        "kb:NVDA+alt+a": "audibility_mode",
        "kb:NVDA+shift+q": "announce_controller",
        "kb:NVDA+shift+v": "announce_voicemeeter_version",
        "kb:NVDA+shift+o": "toggle_mono",
        "kb:NVDA+shift+s": "toggle_solo",
        "kb:NVDA+shift+m": "toggle_mute",
        "kb:NVDA+shift+c": "toggle_mc",
        "kb:NVDA+shift+k": "karaoke",
        "kb:NVDA+shift+upArrow": "slider_increase_by_point_one",
        "kb:NVDA+shift+downArrow": "slider_decrease_by_point_one",
        "kb:NVDA+shift+alt+upArrow": "slider_increase_by_one",
        "kb:NVDA+shift+alt+downArrow": "slider_decrease_by_one",
        "kb:NVDA+shift+control+upArrow": "slider_increase_by_three",
        "kb:NVDA+shift+control+downArrow": "slider_decrease_by_three",
    }
    for i in range(1, kind.num_strip + 1):
        defaults[f"kb:NVDA+alt+{i}"] = "index"
    for i in range(1, kind.phys_out + kind.virt_out + 1):
        defaults[f"kb:NVDA+shift+{i}"] = "bus_assignment"
    abc = config.get("keybinds")
    if abc:
        overrides = {f"kb:{util.remove_prefix(k, 'kb:')}": v for k, v in abc.items()}
        matching_values = set(defaults.values()).intersection(set(overrides.values()))
        defaults = {k: v for k, v in defaults.items() if v not in matching_values}
        return {**defaults, **overrides}
    return defaults
