# Two Lines

A single-file novelty toy. Totally black screen, as if it were switched off, with
two long lines racked vertically down it.

The two lines are not twins: one is longer, fatter and coarsely chopped, the
other shorter, thinner, finer and racked a little lower.

Move a finger over a line and it goes wherever the finger passed, at the speed
the finger moves, and it stays gone. Nothing has to be pressed or held — on a
trackpad or mouse, simply moving the cursor across a line takes it — no ghost, no smear, no dust
left on the black. Stop halfway and the rest of the line is still sitting there.
Specks lift off toward your fingertip, an intake hiss rises with the sweep, and
the phone buzzes.

Nothing brings them back. No tap, no gesture, no button, and not a resize or a
rotation either — a resize carries the powder across exactly as it stands. Two
lines, once, until the page is reloaded.

There is no text, no button and no chrome of any kind on the screen — just black
and the two lines.

## Install it on a phone

It is a PWA, so it installs from the browser rather than a store, and once it is
on the home screen it launches fullscreen with its own icon and runs with the
phone in airplane mode.

1. Serve this folder over HTTPS (any static host — the service worker needs a
   real origin, `file://` will not do).
2. Open that URL on the phone.
3. **iPhone:** Share → *Add to Home Screen*. **Android:** the ⋮ menu →
   *Install app* / *Add to Home screen*.

Relaunching the app gives you two fresh lines; nothing refills them while it is
open.

## Run it locally

Open `index.html` in a browser, or serve the folder (`npx http-server`) if you
want the service worker and install prompt too. No build, no dependencies, and
nothing is fetched from the network — every asset ships with the app.

## How it works

- **Powder** is drawn once into an offscreen canvas — a few thousand jittered
  specks with a density profile that tapers at both ends, plus clumps and stray
  dust — so the per-frame cost stays flat no matter how much is left.
- **Taking it** stamps a `destination-out` brush along the pointer path,
  interpolated every 4px so fast swipes do not leave gaps. The brush is fully
  opaque out to 82% of its radius and wider than the powder is, so one pass
  wipes the whole channel back to black.
- **Movement is the whole input.** Every `pointermove` sweeps, whether or not a
  button or finger is down, and coalesced events are replayed so a fast flick
  is not sampled down to a few points. A jump of more than 220px is treated as
  the cursor arriving rather than a stroke, so it carves nothing.
- **Reach** is decoupled from the brush: a line answers to a finger anywhere
  within ~63px of it, far outside the powder itself, and the brush is then
  stamped on the line rather than under the finger. The reach is capped at 44%
  of the gap between the lines, so a stroke can never be near both at once.
- **Progress** is tracked analytically, not by reading pixels: each line owns 96
  mass cells along its length, reduced by proximity to the stroke. Under 5%
  remaining counts as gone.
- **Sound** is synthesized in WebAudio (looping filtered noise for the intake, a
  bandpass sweep for the finishing sniff, a sine drop plus a lowpass swell for
  the rush). Nothing is loaded; the context starts on first touch.
- **Resizing preserves state.** A phone hiding its address bar used to re-run
  layout and rack two fresh lines; now the powder bitmap and the line geometry
  are carried over, scaled evenly from the height and re-centred, so a rotation
  there and back lands exactly where it started.
- Honors `prefers-reduced-motion`.
