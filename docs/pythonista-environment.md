# Pythonista Environment

Facts about the Pythonista 3 iOS runtime this repo targets. Researched September 2026.
The exact bundled set can vary by release — verify on-device with `help('modules')`
in the Pythonista console before relying on anything critical in generated code.

## Version status

- **Pythonista 3.4** (April 2023) is the latest known release, ending ~3 years of
  silence from the developer. No newer release found as of September 2026 — treat
  3.4 as current.【8177591067846620195†L193-L199】
- Bundled interpreter: **Python 3.10.4**. Python 2 is no longer included.【8177591067846620195†L195-L197】
- 3.4 added pandas and refreshed other bundled modules.【8177591067846620195†L12-L18】

## Bundled third-party modules (reported)

Safe to import in generated scripts — no install step needed:【5291967592567826259†L10-L74】

- **Data/math:** numpy, pandas, matplotlib, sympy, mpmath
- **Web:** requests, beautifulsoup4 (`bs4`), bottle, flask, jinja2, html2text, yaml
- **Text/NLP:** nltk, pyparsing, unidecode
- **Dates:** dateutil, arrow, pytz
- **Files:** openpyxl, pypdf2, reportlab, qrcode
- **Crypto:** certifi, pycrypto, rsa
- **Services:** dropbox, evernote, openai
- **Audio:** midiutil, wavebender
- **Dev:** faker, pygments, pytest, yapf, jedi
- **Imaging:** Pillow

## iOS bridge modules (built in)

Tailor-made for iOS: `scene`, `ui`, `console`, `clipboard`, `photos`, `contacts`,
`reminders`, `location`, `motion`, `sound`, `speech`, `notification`, `calendar`.
Scripts can reach sensor/location data, the photo library, contacts, reminders, and
the clipboard, and can run from the share sheet, a custom keyboard, Shortcuts, and
Siri.【8177591067846620195†L166-L175】

## Sandbox limits

- The writable area is the app's `Documents/` folder; `Documents/site-packages/`
  is on `sys.path`.
- There is no C compiler on device: packages needing native extensions cannot be
  installed — use the bundled builds. StaSh (a shell installable via one-liner)
  provides pip for pure-Python wheels into `site-packages`.
- Repo rule for generated code is unchanged: bundled-only, paste-and-run, no install
  step. StaSh/pip is an escape hatch for the human, not for generated scripts.

## Target device

iPhone 15 Pro Max · 430×932 logical points, portrait · origin bottom-left, y up.
