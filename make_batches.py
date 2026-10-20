#!/usr/bin/env python3
"""Write one markdown page per batch of ghee, which build.py then turns into
HTML like any other page.

    python3 make_batches.py            writes into this folder
    python3 make_batches.py <dir>      writes somewhere else, for testing

Add a batch by adding a line to BATCHES below and running it. Nothing else.
`build.py` picks the new markdown up on its next run with no changes of its
own, because a batch page needs nothing the markdown grammar does not already
have. A two cell table does the code, the date and the readings, and a plain
link does the review.

THE CODE IS THE DATE, as YYMMDD. So 20 October 2026 is `261020`.

Reasons, because the obvious alternative is a sequential number and it is
worse. A date assigns itself, so there is no register to keep and no way to
reuse a code by accident, which is the failure a counter invites. It sorts
chronologically for free in the answers spreadsheet, which is the whole point
of scoring batches at all. It is also the lot mark that prepacked food
labelling already asks for, FSSAI in India and the EU and UK rules alike, so
one number does both jobs. It is digits only, so nothing reads ambiguously off
a label and there is no 0 against O. And digits dodge a trap, which is that
GitHub Pages URLs are case sensitive, so `batch-b2-001.html` and
`batch-B2-001.html` are two different addresses and one of them is a 404.

A second batch on one day takes `-2`, and the first keeps its plain code
because its labels may already be printed.

`B1` is the odd one out and stays. Everything shipped before any of this
existed carries one shared QR code and no printed batch number at all, so B1
is an agreement between the review page and the form rather than a date. The
letter makes those jars visibly not a dated batch, which is useful.

QR density is not a reason to prefer any of this. Measured with `qrcode`, every
scheme considered came out at version 4, 33 by 33 modules, at error correction
level M. At an 18 mm printed symbol that is 0.55 mm a module, which any phone
reads. The code could have been twice as long for nothing.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SITE = "https://mindtensorml.github.io/ai-ghee/"

#: The review form, with the batch code left as a token. `usp=pp_url` is not
#: optional and removing it is a silent bug. Tested in a real browser, without
#: it the hidden field that gets submitted still carried the value while the
#: visible box rendered empty, so a reader met an empty required question with
#: a stale answer sitting behind it.
#:
#: `entry.1407966721` is the batch code field's id. Google assigned it when the
#: field was created, it cannot be derived from anything else, and it ends up
#: printed inside the QR code on every label. If the form's batch field is ever
#: deleted and remade it gets a new id and every label in the world breaks.
#: `Assets WIP/review-form/update-review-form.gs` exists so the form can be
#: changed without that happening.
FORM = ("https://docs.google.com/forms/d/e/"
        "1FAIpQLSdcgkIxBf4SphYhROrMSaR606ep_5Ee2nLSgbfvpMmV0YLC-Q/viewform"
        "?usp=pp_url&entry.1407966721={code}")


# ---------------------------------------------------------------- the batches
#
# code   YYMMDD, as above. Required.
# made   the date written out, because the code is not meant to be decoded by
#        a reader. Required.
# jars   how many came out of it. Optional.
# churn  minutes from the motor starting to the butter breaking. Optional.
# peak   the peak motor current in mA at the break. Optional.
# note   one line about anything that was different about this one. Optional.
#
# The three readings are the reason a batch page is worth having at all. A
# customer holding a jar can see the actual numbers the machine recorded while
# making the thing in their hand, which is the point of the whole project.
# Leave them out and the page is a date and a review link.

BATCHES = [
    # dict(code="261020", made="20 October 2026", jars=9,
    #      churn="24.6", peak="4704",
    #      note="First batch with the new clear labels."),
]


def rows(b):
    """The spec table, skipping anything this batch does not know."""
    out = [("Batch", b["code"]), ("Made", b["made"])]
    if b.get("jars"):
        out.append(("Jars", str(b["jars"])))
    if b.get("churn"):
        out.append(("Churned", f"{b['churn']} minutes to the break"))
    if b.get("peak"):
        out.append(("Peak load", f"{b['peak']} mA"))
    return out


def page(b):
    code = b["code"]
    table = "\n".join(f"| {k} | {v} |" for k, v in rows(b))
    note = f"\n{b['note']}\n" if b.get("note") else ""
    readings = (
        "The numbers above came off the rig while this batch was being made, "
        "not off a spec sheet. The load on the motor climbs as the fat gathers "
        "and then drops away when the butter lets go of the liquid, and the "
        "minute that happened is the minute the machine decided it was done."
        if b.get("churn") or b.get("peak") else
        "The readings for this batch are not up here yet."
    )
    return f"""---
output: batch-{code}.html
title: Batch {code} · AI Ghee Making
description: Batch {code} of JD's AI Ghee, made {b['made']}. What the machine recorded, and how to tell me how it was.
og_title: Batch {code}
og_description: Batch {code}, made {b['made']}. What the machine recorded while it was being made.
og_image: images/card-en.jpg
og_type: website
schema_type: WebPage
og_url: {SITE}batch-{code}.html
skip_text: Skip to the content
lang: en
locale: en_GB
mark: AI Ghee Making
nav_text: The story
nav_href: index.html
nav_side: right
kicker: Batch {code}
headline: Made {b['made']}
standfirst: What the machine recorded while this batch was being made, and a place to tell me how it turned out.
credit:
contact_text: Anything that will not fit in a form.
next_text: Tell me how this jar was
next_href: {FORM.format(code=code)}
next_blurb: Nothing to type. The code goes in for you.
---

## This batch

{table}
{note}
{readings}

Every jar from this batch carries the same code, so a review tells me about the batch rather than about one jar. The [review page](review.html) is the way in if you came here without scanning anything.
"""


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else HERE
    if not BATCHES:
        print("no batches declared yet, nothing written")
        print("add a dict to BATCHES in this file and run it again")
        return 0

    seen = set()
    for b in BATCHES:
        if b["code"] in seen:
            print(f"  two batches both called {b['code']}", file=sys.stderr)
            return 1
        seen.add(b["code"])

    for b in BATCHES:
        name = f"batch-{b['code']}.md"
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
            fh.write(page(b))
        print(f"  {name}")
    print(f"{len(BATCHES)} batch page(s). Run build.py next.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
