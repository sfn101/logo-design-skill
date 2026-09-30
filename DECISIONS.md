# DECISIONS — logo-coach build

One line per judgment call, with reasoning.

- **Renderer:** cairosvg pip-installed but its Cairo DLL is missing on this Windows box; `render_png.py` already falls back to headless Chrome/Edge, which works — so no GTK/Cairo system install. Documented as optional dependency.
- **Fork:** `gh` is not installed/authenticated, so the repo was plain-`git clone`d; the fork + push must be done by hand (see final report).
- **Claude CLI:** not on PATH; used the desktop-bundled `%APPDATA%\Claude\claude-code\2.1.284\claude.exe` for skill-creator's `run_loop.py`.
