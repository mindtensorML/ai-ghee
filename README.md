# AI Ghee Making

A photo story about making traditional bilona ghee with a homemade rig that
senses the moment cream breaks into butter and stops itself.

Live at https://mindtensorml.github.io/ai-ghee/

## To change the words

Edit `story.md` for the main page or `beast.md` for the machine page. Commit.
That is the whole job. A GitHub Action rebuilds `index.html` and `beast.html`
about forty seconds later and pushes them back, and the site updates itself.

You can do this in the browser on github.com without cloning anything.

If you would rather see the result before you push, run the build yourself.

    python3 build.py

It needs nothing installed beyond Python.

## What the markdown can do

    ## Heading            starts a new section, numbered for you
    plain paragraphs      blank line between them
    > a quoted line       becomes a large pull quote
    | Key | Value |       two or more of these become a spec table

Images use ordinary markdown. The link text is the caption printed under the
picture. The quoted part is the alt text for screen readers.

    ![Caption here](images/thing.jpg "Description for screen readers.")

How an image group is laid out depends on how many images sit together with
no blank line between them.

    one image      full width
    two images     side by side
    three or more  a strip, five across on a desktop

Write `[*]` in a caption to link it to the note at the bottom of the page.

Everything above the first heading is the page settings. Titles, link
previews, the video at the top, the footer note. Keys are named plainly, so
`headline` is the headline and `video` is the YouTube id.

## Files

    story.md            the main page, edit this
    beast.md            the machine page, edit this
    build.py            markdown to html, no dependencies
    template.html       the page shell
    style.css           the design, both pages share it
    images/             photographs and the two signal charts
    make_signal.py      redraws the charts from the sensor log
    make_logo.py        redraws the mark, the favicon and the logo files
    logo/               the mark as square files, for a channel avatar
    index.html          generated, do not edit by hand
    beast.html          generated, do not edit by hand

Every path is relative, so the folder works at the repo root or in a
subdirectory.

## The chart

`images/signal.svg` and `images/signal-narrow.svg` are plotted from
`data/churn_20260816.csv`, the log written by the rig during the run in the
photographs. To redraw them, run

    python3 make_signal.py

A cordless drill spikes hard whenever the churn catches, so single readings
run from under a hundred milliamps to over seventeen thousand and a plot of
every point is unreadable. The line is a moving median and the shaded band
is the middle half of the readings in the same window. The page says so in
its footer.


## The mark

The logo is the churn signal used as the surface of the ghee. It sits flat
while nothing is happening, swells as the fat gathers, peaks, then drops away
when the butter lets go. To redraw it, run

    python3 make_logo.py

That writes `favicon.svg`, `logo.svg` for the page header, and square files
in `logo/` on cream and on dark for a channel avatar. The favicon is drawn
with a heavier ring than the rest, because at sixteen pixels the normal
weight breaks up. The PNGs need `rsvg-convert` on the path and are skipped
quietly without it.
