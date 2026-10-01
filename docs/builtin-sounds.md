# Built-in Sounds

Pythonista ships a library of built-in sounds, browsable from the `[+]` button at the top
of the editor. Play any of them by name:

```python
import sound
sound.play_effect('arcade:Coin_1')   # '<prefix>:<SoundName>'
```

`play_effect(name[, volume, pitch, pan, looping])` returns a `sound.Effect` object — it
can be stopped or looped, so it is not fire-and-forget. About 32 effects can play
simultaneously.

Physically, sounds ship as `.caf` files in `Media/Sounds/` inside the app bundle
(`Pythonista3.app/Media/Sounds/`). Each pack is a subfolder whose name **is** the
reference prefix, and the pack list comes from `Media/Collections.json`. All 10 packs
below were verified on-device (Pythonista 3.4).

## The 10 sound packs

| Prefix | Picker title | License | Example sounds |
|---|---|---|---|
| `8ve:` | 8ve (UI Sounds) | raisedbeaches.com/octave | `8ve:beep-attention` (unconfirmed, see note) |
| `arcade:` | Arcade | — | `arcade:Coin_1`, `arcade:Explosion_1` |
| `casino:` | Casino | Kenney, CC0 | `casino:CardFan1`, `casino:CardPlace1` |
| `digital:` | Digital | Kenney, CC0 | `digital:HighDown`, `digital:Laser1` |
| `drums:` | Drums | — | `drums:Drums_01` |
| `game:` | Game | — | `game:Beep`, `game:Boing_1` |
| `piano:` | Piano | — | `piano:A3`, `piano:C3` |
| `rpg:` | RPG | Kenney, CC0 | `rpg:BeltHandle1`, `rpg:BookFlip1`, `rpg:Footstep00` |
| `ui:` | UI | Kenney, CC0 | `ui:click1`, `ui:mouseclick1` |
| `voice:` | Voiceover | "Kenny", CC0 (spelled as in the app) | `voice:female_1` |

Notes:

- The reference name is the filename minus `.caf`.
- The `8ve` pack's on-disk names contain hyphens (e.g. `8ve-beep-attention.caf`). The
  direct mapping gives `8ve:beep-attention`, but the picker-inserted form is unconfirmed —
  verify in the `[+]` picker before using `8ve:` names in generated code.
