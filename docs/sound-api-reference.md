# `sound` Module API Reference

Condensed from the official Pythonista 3.4 documentation. Covers playing sound effects
(built-in and custom), music playback, microphone recording, and MIDI.

See `docs/builtin-sounds.md` for the catalog of built-in sound names (`arcade:Coin_1`,
etc.) usable with `play_effect()`.

## Functions

### `sound.play_effect(name[, volume, pitch=1.0, pan=0.0, looping=False])`

Play the sound effect with the given name. The asset picker (`[+]` button in the toolbar)
lists the built-in names, but `name` can also be a file path for custom sound effects.

- Playback is asynchronous: the function returns before the sound finishes playing.
- Returns a `sound.Effect` object for adjusting settings mid-playback or stopping early.
- May return `None` if too many effects are already playing (the limit is usually
  about 32).

### `sound.stop_all_effects()`

Stop all sound effects currently playing via `play_effect()`.

### `sound.stop_effect(effect)`

Stop playback of the given effect (`effect` must be a `play_effect()` return value).

### `sound.set_volume(vol)`

Set the default volume for all sound effects (0.0–1.0, default 0.5). Has no effect on
sounds already playing.

### `sound.set_honors_silent_switch(flag)`

Whether the silent (mute) switch is honored when playing sounds (`True` by default).

## `sound.Effect`

Represents a currently-playing sound effect. You cannot create `Effect` objects directly;
they are returned by `play_effect()`. For one-off effects the return value can be ignored.

| Member | Description |
|---|---|
| `stop()` | Stop playback. |
| `looping` | `True` loops indefinitely until `stop()` is called. |
| `pan` | Stereo position: -1 = left, +1 = right, 0 = center. |
| `pitch` | Playback speed; default 1.0. |
| `position` | Spatial (3D) position as an `(x, y, z)` tuple. Overrides stereo `pan`. |
| `volume` | Current volume. |

## `sound.Player(file_path)`

Easy audio-file playback from disk. Recommended for music and other audio that doesn't
need very low latency; `play_effect()` suits game sound effects better.

| Member | Description |
|---|---|
| `play()` | Start playing. |
| `stop()` | Stop and reset the playback position. |
| `pause()` | Stop but keep the current playback position. |
| `current_time` | Playback position in seconds. |
| `duration` | Track duration (read-only). |
| `finished_handler` | Callable invoked with no arguments when playback finishes. |
| `number_of_loops` | Repeat count; `-1` repeats forever. |
| `playing` | `True` while playing (read-only). |
| `pan` | Stereo position: -1 = left, +1 = right, 0 = center. |

## `sound.Recorder(file_path)`

Record audio from the device microphone. The output format follows the file extension:
`.m4a` (MPEG4 AAC, much smaller) or `.wav` (Linear PCM — prefer it if you plan to
process raw samples with the `wave` module).

| Member | Description |
|---|---|
| `record([duration])` | Start recording; stops automatically after `duration` seconds if given, otherwise call `stop()`. |
| `stop()` | Stop recording. |
| `pause()` | Pause recording; resume with `record()`. |
| `current_time` | Duration of the active recording. |
| `recording` | Whether currently recording (boolean). |
| `meters` | Read-only dict of current average/peak power: `{'average': (left, right), 'peak': (left, right)}`. Accessing it enables metering, which costs extra resources. |

## `sound.MIDIPlayer(file_path[, sound_bank_path])`

Simple playback of MIDI (`.mid`) files, using the built-in "Merlin Silver" sound bank or
a custom one (must be `.sf2` format).

| Member | Description |
|---|---|
| `play()` | Start playback. |
| `stop()` | Stop playback. |
| `current_time` | Playback position. |
| `duration` | Track duration (read-only). |
| `rate` | Playback rate; 1.0 is normal speed. |
