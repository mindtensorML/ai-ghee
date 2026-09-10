# The mark

घ्यू, the Nepali word for ghee, with its shirorekha carried on past the word.
Somewhere in that run the line takes one reading, flat then a swell then the
break, which is the shape the rig watches for while it churns. A gold dot
marks the apex.

Everything here is generated. Run `python3 make_logo.py` from the repo root
to rebuild the lot. Do not edit these files by hand, they get overwritten.

The letterform is stored in that script as outline paths, not as text, so no
file here needs a font installed and no renderer can re-shape the conjunct
wrongly. The half form of घ, where it drops its vertical stem and joins य, is
baked into the artwork.


## Which file

**Screen, in colour.** `ai-ghee-mark-cream` on a light page, `ai-ghee-mark-ink`
reversed, `ai-ghee-mark-gold` where you want the ghee colour to carry it.
`ai-ghee-mark-clear` is the same drawing with no background, for putting on
something else.

**Anything cropped to a circle.** A YouTube avatar, a profile picture, a cap.
Use the `circle` files. The mark is inset so the rule ends do not run into
the crop.

**Small.** Below about forty pixels the rule is a hairline and the mark washes
out, so the `glyph` files drop the rule and set the word alone and heavier.
That is what the favicon and the header icon use.

**Print, one colour.** `print/mark-black` and `print/mark-white`, with `-clear`
versions that have no background. The gold dot is left off, because a dot in
the same ink as the line it sits on is not a dot, it is a lump.

**When the reading is too much.** `ai-ghee-quiet` is the same mark with a
straight rule and no swell. For contexts where the data nod would be noise,
or where it will be reproduced too small or too roughly for the swell to
survive.


## The colours

    ink     #1b1712
    gold    #c08a2e
    cream   #f4ead7
    paper   #fff8ec
    lit     #e9b657      the gold that holds up on a dark ground

Two inks at most anywhere. Nothing here uses a gradient.


## Clear space and minimum size

Leave at least the height of the word clear on every side.

The full mark stops working below about 40px wide on screen, or about 18mm
in print. Use a `glyph` file under that.
