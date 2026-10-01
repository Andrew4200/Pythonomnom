# Built-in Sounds

Pythonista ships a library of built-in sounds, browsable from the `[+]` button at the top
of the editor. Play any of them by name:

```python
import sound
sound.play_effect('arcade:Laser_1')   # '<pack-prefix>:<SoundName>'
```

`play_effect(name[, volume, pitch, pan, looping])` returns a `sound.Effect` object — it
can be stopped or looped, so it is not fire-and-forget. About 32 effects can play
simultaneously.

## Verified packs

These prefixes are confirmed by the official 3.4 sound docs or community tutorials:

| Prefix | Pack | Verified examples |
|---|---|---|
| `arcade:` | Arcade | `arcade:Laser_1` (official sound docs), `arcade:Coin_1`, `arcade:Coin_2`, `arcade:Explosion_2` |
| `rpg:` | RPG | `rpg:Footstep00` (Kenney, CC0) |

## Unverified packs — confirm in the in-app picker

These packs exist in the Sounds tab, but no public source confirms their code prefixes or
sound names. Candidate prefixes below are guesses, **not verified** — check the `[+]`
picker on-device before using any of them in generated code:

| Candidate prefix | Pack | License / attribution |
|---|---|---|
| `8ve:`? | 8ve (UI Sounds) | Octave UI sounds (raisedbeaches.com/octave) — attribution verified, prefix not |
| ? | Casino | Kenney, CC0 — prefix unknown |
| ? | Digital | Kenney, CC0 — prefix unknown |
| ? | Drums | — |
| ? | Game | — |
| ? | Piano | — |
| ? | UI | Kenney, CC0 — prefix unknown |
| ? | Voiceover | "Kenny — CC0" as shown in app — prefix unknown |
