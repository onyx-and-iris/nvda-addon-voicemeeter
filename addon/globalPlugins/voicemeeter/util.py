from . import config
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
        'kb:NVDA+alt+s': 'strip_mode',
        'kb:NVDA+alt+b': 'bus_mode',
        'kb:NVDA+alt+g': 'gain_mode',
        'kb:NVDA+alt+c': 'comp_mode',
        'kb:NVDA+alt+t': 'gate_mode',
        'kb:NVDA+alt+d': 'denoiser_mode',
        'kb:NVDA+alt+a': 'audibility_mode',
        'kb:NVDA+shift+q': 'announce_controller',
        'kb:NVDA+shift+v': 'announce_voicemeeter_version',
        'kb:NVDA+shift+o': 'rotate_mono',
        'kb:NVDA+shift+s': 'toggle_solo',
        'kb:NVDA+shift+m': 'toggle_mute',
        'kb:NVDA+shift+c': 'toggle_mc',
        'kb:NVDA+shift+k': 'rotate_karaoke',
        'kb:NVDA+shift+n': 'rotate_bus_mode_next',
        'kb:NVDA+shift+p': 'rotate_bus_mode_previous',
        'kb:NVDA+shift+upArrow': 'slider_increase_by_point_one',
        'kb:NVDA+shift+downArrow': 'slider_decrease_by_point_one',
        'kb:NVDA+shift+alt+upArrow': 'slider_increase_by_one',
        'kb:NVDA+shift+alt+downArrow': 'slider_decrease_by_one',
        'kb:NVDA+shift+control+upArrow': 'slider_increase_by_three',
        'kb:NVDA+shift+control+downArrow': 'slider_decrease_by_three',
    }
    for i in range(1, kind.num_strip + 1):
        defaults[f'kb:NVDA+alt+{i}'] = 'index'
    for i in range(1, kind.phys_out + kind.virt_out + 1):
        defaults[f'kb:NVDA+shift+{i}'] = 'bus_assignment'
    abc = config.get('keybinds')
    if abc:
        overrides = {f'kb:{remove_prefix(k, "kb:")}': v for k, v in abc.items()}
        matching_values = set(defaults.values()).intersection(set(overrides.values()))
        defaults = {k: v for k, v in defaults.items() if v not in matching_values}
        return {**defaults, **overrides}
    return defaults


_bus_mode_map = {
    'normal': 'Normal',
    'amix': 'Mix Down A',
    'bmix': 'Mix Down B',
    'repeat': 'Stereo Repeat',
    'composite': 'Composite',
    'tvmix': 'Up Mix TV',
    'upmix21': 'Up Mix 2.1',
    'upmix41': 'Up Mix 4.1',
    'upmix61': 'Up Mix 6.1',
    'centeronly': 'Center Only',
    'lfeonly': 'Low Frequency Effect Only',
    'rearonly': 'Rear Only',
}


def _get_bus_mode_opts(kind_id):
    if kind_id == 'basic':
        return [
            'normal',
            'amix',
            'repeat',
            'composite',
        ]
    return [
        'normal',
        'amix',
        'bmix',
        'repeat',
        'composite',
        'tvmix',
        'upmix21',
        'upmix41',
        'upmix61',
        'centeronly',
        'lfeonly',
        'rearonly',
    ]


def _get_bus_mode_readable_name(mode):
    return _bus_mode_map.get(mode, mode)
