# Two Lines

A single-file novelty toy. Dark room, a mirror tray, two lines racked out on it.
Drag a finger (or the mouse) along a line and it goes: the powder is eaten away
under the stroke, specks get sucked into the rolled note at your fingertip, an
intake hiss rises with the sweep, and a smear stays behind on the glass. Clear
both and you get the rush — a flash, a low thump, and a fresh rack on request.

## Run it

Open `index.html` in a browser. No build, no dependencies, no network beyond the
Google Fonts stylesheet (it degrades to system faces offline).

Best on a phone: it uses pointer events, so it wants a finger, and it vibrates
on each sweep where the device supports it.

## How it works

- **Powder** is drawn once into an offscreen canvas — a few thousand jittered
  specks with a density profile that tapers at both ends, plus clumps and stray
  dust — so the per-frame cost stays flat no matter how much is left.
- **Taking it** stamps a soft `destination-out` brush along the pointer path,
  interpolated every 4px so fast swipes do not leave gaps.
- **Progress** is tracked analytically, not by reading pixels: each line owns 96
  mass cells along its length, reduced by proximity to the stroke. Under 5%
  remaining counts as gone.
- **Sound** is synthesized in WebAudio (looping filtered noise for the intake, a
  bandpass sweep for the finishing sniff, a sine drop plus a lowpass swell for
  the rush). Nothing is loaded; the context starts on first touch.
- Honors `prefers-reduced-motion` and can be muted from the rail.
