# Orbit

A focus timer that walks you through a stretch break for laptop work.
Plain HTML, CSS and JavaScript in one file. No build step, no dependencies.

## What it does

- Focus / Break / Long break, adjustable from 1 to 180 minutes, long break every 4th round.
- Every break opens a guided set of seven stretches: walk in place, shoulder rolls,
  chest opener, neck turns, side bends, wrist stretch, eye rest. Roughly 2:45.
- Tap the question mark on any step for the full how-to. The step timer waits while you read.
- Works offline once installed, keeps the screen awake while counting, and picks the
  timer back up where it left off if the app is closed mid-session.
- Launch animation: the dot orbits the dial, which then settles into place as the timer
  itself. Tap to skip it; it is replaced by a plain fade when the system asks for reduced
  motion.

## Files

```
index.html             the whole app
manifest.webmanifest   install metadata
sw.js                  offline cache
icons/                 app icons
```

## Deploying

Everything is referenced with relative paths, so the app runs from any path:
a project page at `/orbit/`, a custom domain at the root, either way.

**GitHub Pages** — Settings → Pages → deploy from `main`, root folder.

**Cloudflare Workers** — connect this repository under Workers & Pages → Create → Import a
repository. No build command, output directory `/`.

A service worker needs HTTPS. Both hosts above provide it; `file://` does not, so the
install prompt and offline mode only appear on a deployed copy.

## Installing on a phone

- Android / Chrome: menu → Install app.
- iOS / Safari: Share → Add to Home Screen.
- Long-pressing the icon gives a **Stretch break** shortcut that opens straight into the
  exercises.

## Updating

Cached copies only pick up a new `index.html` after the cache name changes, so bump
`VERSION` at the top of `sw.js` with every release.

## Editing the routine

The exercises live in the `ROUTINE` array near the top of the script in `index.html`.
Each step is either timed (`s`, in seconds) or counted (`r`, free text), with a one-line
hint (`h`) and the long how-to (`d`). Add or remove steps freely; the screen follows the
list.

## URL options

`?work=25&short=5&long=15&cycles=4` set the lengths, `?theme=dark`, `?sound=0`,
`?bg=transparent` or `?bg=RRGGBB` for embedding, `?go=stretch` opens the stretches directly.
