# AI Ghee Making

A photo story about making traditional bilona ghee with a homemade rig that
senses the moment cream breaks into butter and stops itself. It is published
in English and in Nepali.

Live at https://mindtensorml.github.io/ai-ghee/

## To change the words

Edit `story.md` for the main page or `beast.md` for the machine page. The
Nepali versions of the same two pages are `story-ne.md` and `beast-ne.md`.
Commit. That is the whole job. A GitHub Action rebuilds the HTML about forty
seconds later and pushes it back, and the site updates itself.

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


## The two languages

Each page exists twice, and the two halves are joined by six keys in the
front matter.

    lang            goes on the html element, en unless you say otherwise
    locale          og:locale, so a shared link says which language it is
    alt_locale      the same for the other version
    alt_href        the link the switcher in the masthead follows
    alt_lang        the other version's language code
    alt_label       the word on the switcher, written in the language it
                    leads to, so the English page says नेपाली
    alt_url         the other version's full address, for the hreflang tags

`alt_url` is spelled out rather than worked out from `alt_href`, because the
English story lives at the bare directory address and the Nepali one at a
file name, and guessing between the two would be a trap waiting to spring.

One more key, `numerals: devanagari`, sets the section numbers in Devanagari.
It changes nothing else, because a milliamp reading is written the same way
in both languages.

No font is loaded for the Nepali pages. `style.css` keeps the Latin faces at
the front of the stack and puts the Devanagari ones behind them, so a
Devanagari face is only reached for the characters the Latin ones do not
carry. Between them they cover macOS, iOS, Windows, Android and the desktop
Linux distributions.

The design tracks its small uppercase type wide apart. Devanagari hangs from
one unbroken bar along the top of a word and that tracking snaps the bar into
pieces, so every tracked rule is reset for Nepali, and the type is set a
little larger, because Devanagari fills less of its em than a Latin capital
and at a matched size it reads as the smaller of the two.

## Shared settings

`site.md` holds the things both pages use, the photo credit and the contact
line. It has no `output` key so it is never built into a page. A page's own
front matter still wins, so either page can override any of it.

The contact address lives there for one reason. It is published on a public
site whose markdown is also public, so it will be harvested eventually and no
amount of hiding changes that. What matters is that replacing it is one line
in one file rather than a hunt. Use a forwarding alias, and when it starts
attracting rubbish, delete the alias and put a new one on that line.


## Files

    story.md            the main page, edit this
    beast.md            the machine page, edit this
    story-ne.md         the main page in Nepali, edit this
    beast-ne.md         the machine page in Nepali, edit this
    site.md             settings shared by every page, including the address
    build.py            markdown to html, no dependencies
    template.html       the page shell
    style.css           the design, every page shares it
    images/             photographs, the charts and the schematics
    make_signal.py      redraws the charts from the sensor log
    make_schematic.py   redraws the wiring diagrams
    make_logo.py        redraws the mark, the favicon and the logo files
    logo/               the mark as square files, for a channel avatar
    index.html          generated, do not edit by hand
    beast.html          generated, do not edit by hand
    index-ne.html       generated, do not edit by hand
    beast-ne.html       generated, do not edit by hand

Every path is relative, so the folder works at the repo root or in a
subdirectory.

## The chart

`images/signal.svg` and `images/signal-narrow.svg` are plotted from
`data/churn_20260816.csv`, the log written by the rig during the run in the
photographs. `signal-ne.svg` and `signal-ne-narrow.svg` are the same chart
with its words in Nepali. To redraw all four, run

    python3 make_signal.py

The log is read once and every version is drawn from it, so the four can
never disagree about what the run did.

A cordless drill spikes hard whenever the churn catches, so single readings
run from under a hundred milliamps to over seventeen thousand and a plot of
every point is unreadable. The line is a moving median and the shaded band
is the middle half of the readings in the same window. The page says so in
its footer.


## The schematic

`images/schematic.svg` and `images/schematic-narrow.svg` are drawn by

    python3 make_schematic.py

which writes the Nepali pair beside them. Only the words that describe
something are translated, and they are listed in `WORDS` near the top of that
script. Pin names, part numbers and the rig's own name are the same in any
language, so they are left where they are.

Everything in them was read off the rig rather than remembered. The pin
numbers, the PWM frequency, the sample rate and the trip currents come from
`bilona_ramped.py` on the Pi. The sensor address and its scaling come from
`current_test.py`. The supply is what is in the photographs.

Two line weights, and they mean something. Thin is signal, where nothing
carries more than a few milliamps. Thick is the motor loop. The Pi only ever
touches the thin lines, and the emergency stop is not among them.


## The mark

The logo is घ्यू, the Nepali word for ghee, with its shirorekha carried on past
the word. Somewhere in that run the line takes one reading, flat then a swell
then the break, which is the shape the rig watches for while it churns. To
redraw it, run

    python3 make_logo.py

That writes `favicon.svg`, `logo.svg` for the page header, `logo-mark.svg`,
the apple touch icon, and the whole brand family in `logo/`, which has its own
README saying which file to use when. The letterform is stored in the script
as outline paths rather than as text, so nothing depends on a font being
installed anywhere and no renderer can re-shape the conjunct wrongly.

One number governs the lot. `MASTER` in that script holds the type size, the
rule length and where the reading sits, and every file is built from it, so
the family cannot drift apart. The icons are the exception and are set larger
on purpose, because at sixteen pixels every unit of the box matters.
