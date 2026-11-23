# Design tokens

Source: the Pipenzo "Flow look" tokens, `extension/sidepanel/tokens.css` in jortega0033/clip-to-reel-studio at commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21). The copy is `retail_pos/static/tokens.css`. Do not edit it.

## Resync

Copy the file over `retail_pos/static/tokens.css`. Nothing else changes.

## Rule

New UI uses these tokens; no new colour literals (no `#hex`, `rgb()`, `hsl()` in CSS or JavaScript). Read a token in JavaScript with `getComputedStyle(document.documentElement).getPropertyValue('--token')`. Link `tokens.css` before any other stylesheet. The header comment in the file holds the contrast rules: yellow only on the primary action and the current-step marker, text never on a bare alpha layer, red only for danger. The `--glass*`, `--blur`, `--hero-shadow` and `--shadow-*` tokens exist in the file but [ui-quality.md](ui-quality.md) rule 4 forbids glass panels and shadow-on-every-card, so do not use them.

## Light and dark

Dark is the primary design: black page, alpha layers as opaque equivalents. The `:root` block is the matching light theme. The operating system picks one through `prefers-color-scheme`; `color-scheme: light dark` is set. There is no manual switch.

## Tokens by role

- Surfaces: `--bg`, `--bg-raised`, `--surface`, `--bg-sunken`, `--hero-bg`, `--ink`
- Text: `--fg`, `--muted`, `--faint`, `--on-hero`, `--on-hero-muted`, `--on-ink`, `--on-ink-muted`, `--on-media`
- Lines and focus: `--border`, `--control-border`, `--hairline`, `--input-border`, `--hero-border`, `--hero-chip-border`, `--ink-border`, `--focus`, `--ring-accent`
- Accent: `--primary`, `--primary-press`, `--primary-edge`, `--on-primary`
- Status: `--ok`, `--ok-bg`, `--warn-fg`, `--warn-bg`, `--danger`, `--danger-bg`, `--info`, `--success`
- Interaction layers: `--state-hover`, `--state-selected`, `--btn-secondary`, `--btn-secondary-border`, `--ink-hover`, `--scrim`
- Type: `--font`, `--font-display`, `--mono` (the source loads bundled fonts through a `fonts.css` that is not copied here, so the system fallbacks apply)
- Space and radius: `--space-1` to `--space-7`, `--radius-control`, `--radius-card`, `--radius-media`, `--radius-hero`, `--radius-chip`, `--radius-pill`
- Motion: `--dur-1` to `--dur-4`, `--ease-out`, `--ease-in-out`
- Not for use here: `--glass`, `--glass-strong`, `--glass-border`, `--glass-highlight`, `--glass-video`, `--glass-video-border`, `--blur`, `--shadow-*`, `--hero-shadow`, `--grad-*`
