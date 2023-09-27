# NVDA Addon Voicemeeter

Control Voicemeeter with global hotkeys.

## Install

This addon can be installed through the Add-on store, `Install from external source`. Simply download the [latest Release](https://github.com/onyx-and-iris/nvda-addon-voicemeeter/releases) and load it with NVDA.

## Default Keybinds

### Controllers

- `NVDA+alt+s`: Enable strip mode
- `NVDA+alt+b`: Enable bus mode.

- `NVDA+alt+1`: Enable controller for channel 1 (strip|bus)
- `NVDA+alt+2`: Enable controller for channel 2 (strip|bus)
- `NVDA+alt+3`: Enable controller for channel 3 (strip|bus)
- `NVDA+alt+4`: Enable controller for channel 4 (strip|bus)
- `NVDA+alt+5`: Enable controller for channel 5 (strip|bus)
- `NVDA+alt+6`: Enable controller for channel 6 (strip|bus)
- `NVDA+alt+7`: Enable controller for channel 7 (strip|bus)
- `NVDA+alt+8`: Enable controller for channel 8 (strip|bus)

### Slider Modes

- `NVDA+alt+g`: Enable gain slider mode.
- `NVDA+alt+c`: Enable comp slider mode.
- `NVDA+alt+t`: Enable gate slider mode.
- `NVDA+alt+d`: Enable denoiser slider mode.
- `NVDA+alt+a`: Enable audibility slider mode.

### Sliders

- `NVDA+shift+upArrow`: Move slider up by 1 step
- `NVDA+shift+downArrow`: Move slider down by 1 step
- `NVDA+shift+alt+upArrow`: Move slider up by 0.1 step
- `NVDA+shift+alt+downArrow`: Move slider down by 0.1 step
- `NVDA+shift+control+upArrow`: Move slider up by 3 steps
- `NVDA+shift+control+downArrow`: Move slider down by 3 steps

### Channel Parameters

- `NVDA+shift+o`: Mono
- `NVDA+shift+s`: Solo
- `NVDA+shift+m`: Mute
- `NVDA+shift+c`: MC
- `NVDA+shift+k`: Karaoke

### Announcements

- `NVDA+shift+q`: Announce current controller.
- `NVDA+shift+a`: Announce Voicemeeter kind.

## Configuration

By placing a file named `nvda_settings.json` in `User Home Directory / Documents / Voicemeeter` (the same place as your Voicemeeter xml profiles) you can change most of the default keybinds.

The `voicemeeter` key can take one of three values:

- `basic`
- `banana`
- `potato`

example:

```json
{
  "voicemeeter": "banana",
  "keybinds": {
    "NVDA+alt+k": "strip_mode",
    "NVDA+alt+l": "bus_mode",
    "NVDA+alt+g": "gain_mode",
    "NVDA+alt+c": "comp_mode",
    "NVDA+alt+t": "gate_mode",
    "NVDA+alt+d": "denoiser_mode",
    "NVDA+alt+a": "audibility_mode",
    "NVDA+shift+q": "announce_controller",
    "NVDA+shift+z": "announce_voicemeeter_version",
    "NVDA+shift+s": "toggle_solo",
    "NVDA+shift+m": "toggle_mute",
    "NVDA+shift+c": "toggle_mc",
    "NVDA+shift+k": "karaoke",
    "NVDA+shift+upArrow": "slider_increase_by_point_one",
    "NVDA+shift+downArrow": "slider_decrease_by_point_one",
    "NVDA+shift+alt+upArrow": "slider_increase_by_one",
    "NVDA+shift+alt+downArrow": "slider_decrease_by_one",
    "NVDA+shift+control+upArrow": "slider_increase_by_three",
    "NVDA+shift+control+downArrow": "slider_decrease_by_three"
  }
}
```

Would make the following changes:

- load the plugin in `banana` mode (default is potato).
- change the `strip_mode` and `bus_mode` binds to k and l respectively.
- change the `announce_voicemeeter_version` bind to z.

All other binds would then be defaults.
