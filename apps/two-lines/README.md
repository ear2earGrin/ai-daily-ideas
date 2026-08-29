# Two Lines

A single-file novelty toy. Totally black screen, as if it were switched off, with
two long lines racked vertically down it.

Drag a finger (or the mouse) down a line and it goes wherever the finger passed,
at the speed the finger moves, and it stays gone — stop halfway and the rest of
the line is still sitting there. Specks lift off toward your fingertip, an intake
hiss rises with the sweep, the phone buzzes, and a smear stays behind on the
glass.

Nothing comes back on its own and no gesture brings it back. Two fresh lines only
if you press **Rack up**.

## Run it

Open `index.html` in a browser. No build, no dependencies, no network beyond the
Google Fonts stylesheet (it degrades to system faces offline).

Best on a phone: it uses pointer events, so it wants a finger.

## How it works

- **Powder** is drawn once into an offscreen canvas — a few thousand jittered
  specks with a density profile that tapers at both ends, plus clumps and stray
  dust — so the per-frame cost stays flat no matter how much is left.
- **Taking it** stamps a soft opaque `destination-out` brush along the pointer
  path, interpolated every 4px so fast swipes do not leave gaps. One pass clears
  everything under it — there is no speed threshold and nothing is left to come
  back for.
- **Progress** is tracked analytically, not by reading pixels: each line owns 96
  mass cells along its length, reduced by proximity to the stroke. Under 5%
  remaining counts as gone.
- **Sound** is synthesized in WebAudio (looping filtered noise for the intake, a
  bandpass sweep for the finishing sniff, a sine drop plus a lowpass swell for
  the rush). Nothing is loaded; the context starts on first touch.
- Honors `prefers-reduced-motion` and can be muted from the rail.
