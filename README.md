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
    index.html          generated, do not edit by hand
    beast.html          generated, do not edit by hand

Every path is relative, so the folder works at the repo root or in a
subdirectory.

## A note on the chart

`images/signal.svg` and `images/signal-narrow.svg` are stylised. They show
the shape of a churn rather than a raw sensor log, and the page says so in
its footer.
