# Two Lines

A single-file novelty toy. Totally black screen, as if it were switched off, with
two long lines racked vertically down it.

Drag a finger (or the mouse) down a line and it goes — and it goes at the speed
you take it: a fast sweep clears the whole line in one pass, a slow crawl only
thins it and leaves you to come back for the rest. Specks lift off toward your
fingertip, an intake hiss rises with the sweep, the phone buzzes, and a smear
stays behind on the glass.

Nothing racks up again on its own. **Double-tap** anywhere (or press Rack up)
for two more.

## Run it

Open `index.html` in a browser. No build, no dependencies, no network beyond the
Google Fonts stylesheet (it degrades to system faces offline).

Best on a phone: it uses pointer events, so it wants a finger.

## How it works

- **Powder** is drawn once into an offscreen canvas — a few thousand jittered
  specks with a density profile that tapers at both ends, plus clumps and stray
  dust — so the per-frame cost stays flat no matter how much is left.
- **Taking it** stamps a soft `destination-out` brush along the pointer path,
  interpolated every 4px so fast swipes do not leave gaps. Both the brush's
  opacity and the mass it removes scale with pointer speed, measured per move
  event, which is what makes a slow drag merely thin the line.
- **Progress** is tracked analytically, not by reading pixels: each line owns 96
  mass cells along its length, reduced by proximity to the stroke. Under 5%
  remaining counts as gone.
- **Sound** is synthesized in WebAudio (looping filtered noise for the intake, a
  bandpass sweep for the finishing sniff, a sine drop plus a lowpass swell for
  the rush). Nothing is loaded; the context starts on first touch.
- A **tap** is a press that neither travelled more than 14px nor lasted longer
  than 320ms; two inside 420ms rack up again, so a drag can never reset by
  accident.
- Honors `prefers-reduced-motion` and can be muted from the rail.
