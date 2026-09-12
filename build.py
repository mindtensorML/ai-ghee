#!/usr/bin/env python3
"""Turn the markdown story files into the site's HTML pages.

Run it with no arguments. It reads every .md file in this folder that has
front matter (so README.md is ignored), and writes the file named by each
one's `output:` key.

    python3 build.py

You should only ever need to edit the .md files. This script and
template.html hold the layout, style.css holds the design.


WHAT THE MARKDOWN SUPPORTS
--------------------------

Front matter at the top, between two lines of three dashes. One key per
line. See story.md for the full set.

In the body:

    ## Heading            starts a new section, numbered automatically
    plain paragraphs      normal text, blank line between them
    > quoted line         becomes a large pull quote
    | Key | Value |       two or more of these become a spec table

Images use ordinary markdown, where the link text is the caption shown on
the page and the quoted title is the alt text read by screen readers.

    ![Caption here](images/thing.jpg "Description for screen readers.")

The layout of an image group is decided by how many images sit together
with no blank line between them.

    one image      a full width figure
    two images     a side by side pair
    three or more  a strip, five across on desktop

Inline you can use **bold**, *italic*, [links](https://example.com) and
`code`. Nothing else is needed, so nothing else is supported.
"""

import html
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "template.html")

# The chart and the schematic are each drawn at two sizes so they stay readable
# on a phone. When one of these is used, the narrow version is offered to
# small screens.
RESPONSIVE = {"images/signal.svg": "images/signal-narrow.svg",
              "images/schematic.svg": "images/schematic-narrow.svg",
              "images/signal-ne.svg": "images/signal-ne-narrow.svg",
              "images/schematic-ne.svg": "images/schematic-ne-narrow.svg"}

# A page can ask for its section numbers in Devanagari. Nothing else on the
# page is renumbered, because a milliamp reading is written the same way in
# both languages.
DEVANAGARI = str.maketrans("0123456789", "०१२३४५६७८९")


# ---------------------------------------------------------------- image size

def image_size(path):
    """Return (width, height) for a jpg, png or svg, or None if unknown.

    Reading the headers directly keeps this script free of dependencies, so
    the GitHub Action does not have to install anything.
    """
    full = os.path.join(HERE, path)
    if not os.path.exists(full):
        print(f"  warning, missing image {path}", file=sys.stderr)
        return None
    if path.lower().endswith(".svg"):
        head = open(full, "r", encoding="utf-8", errors="replace").read(2000)
        m = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', head)
        return (int(float(m.group(1))), int(float(m.group(2)))) if m else None
    with open(full, "rb") as fh:
        data = fh.read(32)
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            fh.seek(16)
            return struct.unpack(">II", fh.read(8))
        if data[:2] != b"\xff\xd8":
            return None
        fh.seek(2)
        while True:
            b = fh.read(1)
            while b and b != b"\xff":
                b = fh.read(1)
            marker = fh.read(1)
            while marker == b"\xff":
                marker = fh.read(1)
            if not marker:
                return None
            # Start of frame markers carry the dimensions
            if marker[0] in set(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC}:
                fh.read(3)
                h, w = struct.unpack(">HH", fh.read(4))
                return (w, h)
            size = struct.unpack(">H", fh.read(2))[0]
            fh.seek(size - 2, os.SEEK_CUR)


# ------------------------------------------------------------------- inlines

def inline(text):
    """Apply the small set of inline markdown we use."""
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    # [*] in a caption points at the note in the footer
    out = out.replace(
        "[*]",
        '<a href="#note" aria-label="See note about this chart">*</a>')
    return out


IMAGE_RE = re.compile(r'^!\[(?P<caption>.*?)\]\((?P<src>\S+?)(?:\s+"(?P<alt>[^"]*)")?\)\s*$')
ROW_RE = re.compile(r"^\|(?P<cells>.+)\|\s*$")


# -------------------------------------------------------------------- blocks

def figure(src, caption, alt, in_group):
    size = image_size(src)
    dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
    alt_attr = html.escape(alt or caption, quote=True)
    cap = f"\n      <figcaption>{inline(caption)}</figcaption>" if caption else ""

    if src in RESPONSIVE:
        # The chart carries no shadow of its own, the card around it does.
        img = (f'<img src="{src}"{dims} alt="{alt_attr}">')
        return (
            "    <figure>\n"
            '      <div class="chart">\n'
            "        <picture>\n"
            f'          <source media="(max-width: 620px)" srcset="{RESPONSIVE[src]}">\n'
            f"          {img}\n"
            "        </picture>\n"
            "      </div>"
            f"{cap}\n    </figure>"
        )

    lazy = ' loading="lazy" decoding="async"'
    indent = "      " if in_group else "    "
    return (
        f"{indent}<figure>\n"
        f'{indent}  <img src="{src}"{dims} alt="{alt_attr}"{lazy}>\n'
        + (f"{indent}  <figcaption>{inline(caption)}</figcaption>\n" if caption else "")
        + f"{indent}</figure>"
    )


def image_group(images):
    """One image is a plain figure. Two make a pair. More make a strip."""
    if len(images) == 1:
        return figure(*images[0], in_group=False)
    cls = "pair" if len(images) == 2 else "ladder"
    inner = "\n".join(figure(*im, in_group=True) for im in images)
    return f'    <div class="{cls}">\n{inner}\n    </div>'


def spec_table(rows):
    items = "\n".join(
        f'      <li><span class="k">{inline(k)}</span>'
        f'<span class="v">{inline(v)}</span></li>'
        for k, v in rows
    )
    return f'    <ul class="spec">\n{items}\n    </ul>'


# -------------------------------------------------------------------- parsing

def split_front_matter(text):
    if not text.startswith("---"):
        return None, text
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body.strip()


def parse_section(body):
    """Turn one section's markdown into a list of rendered HTML blocks."""
    blocks, images, rows, para = [], [], [], []

    def flush_para():
        if para:
            blocks.append(f"    <p>{inline(' '.join(para))}</p>")
            para.clear()

    def flush_images():
        if images:
            blocks.append(image_group(list(images)))
            images.clear()

    def flush_rows():
        if rows:
            blocks.append(spec_table(list(rows)))
            rows.clear()

    def flush_all():
        flush_para()
        flush_images()
        flush_rows()

    for raw in body.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            flush_all()
            continue

        m = IMAGE_RE.match(line.strip())
        if m:
            flush_para()
            flush_rows()
            images.append((m.group("src"), m.group("caption"), m.group("alt")))
            continue

        m = ROW_RE.match(line.strip())
        if m:
            cells = [c.strip() for c in m.group("cells").split("|")]
            if len(cells) == 2 and not all(set(c) <= set("-: ") for c in cells):
                flush_para()
                flush_images()
                rows.append((cells[0], cells[1]))
                continue

        if line.strip().startswith(">"):
            flush_all()
            blocks.append(f'    <p class="pull">{inline(line.strip()[1:].strip())}</p>')
            continue

        flush_images()
        flush_rows()
        para.append(line.strip())

    flush_all()
    return blocks


def render_sections(body, numerals="latin"):
    parts = re.split(r"^## +", body, flags=re.M)
    out = []
    for n, chunk in enumerate([p for p in parts if p.strip()], 1):
        heading, _, rest = chunk.partition("\n")
        num = f"{n:02d}"
        if numerals == "devanagari":
            num = num.translate(DEVANAGARI)
        blocks = "\n".join(parse_section(rest))
        if n == 1:
            # the very first paragraph on a page carries the standfirst weight
            blocks = blocks.replace("    <p>", '    <p class="lead">', 1)
        out.append(
            '<section class="wrap">\n'
            f'  <p class="num">{num}</p>\n'
            f"  <h2>{inline(heading.strip())}</h2>\n"
            f"{blocks}\n"
            "</section>"
        )
    return "\n\n".join(out)


# --------------------------------------------------------------------- render

def render_nav(meta):
    # the mark is decorative here, the name is right beside it, so alt is empty
    mark = (f'  <span class="mark"><img src="logo.svg" alt="" width="24" height="24">'
            f'{meta.get("mark", "")}</span>')

    links = []
    if meta.get("nav_text"):
        arrow = "&lsaquo; " if meta.get("nav_side") == "left" else ""
        tail = "" if arrow else " &rsaquo;"
        links.append(f'<a href="{meta["nav_href"]}">'
                     f'{arrow}{meta["nav_text"]}{tail}</a>')
    if meta.get("alt_href"):
        # the switcher is labelled in the language it leads to, and carries
        # that language so a screen reader says the word properly
        code = meta.get("alt_lang", "en")
        links.append(f'<a class="lang" href="{meta["alt_href"]}" lang="{code}" '
                     f'hreflang="{code}">{meta.get("alt_label", code)}</a>')
    if not links:
        return mark

    group = '  <nav class="links">' + "".join(links) + "</nav>"
    return f"{group}\n{mark}" if meta.get("nav_side") == "left" else f"{mark}\n{group}"


def render_head_links(meta):
    """Canonical, og:locale and the hreflang pair, when a page has a twin.

    Each language version points at itself and at the other one, which is
    what tells a search engine they are the same page rather than two.
    """
    out = []
    if meta.get("locale"):
        out.append(f'<meta property="og:locale" content="{meta["locale"]}">')
    if meta.get("alt_locale"):
        out.append('<meta property="og:locale:alternate" '
                   f'content="{meta["alt_locale"]}">')
    here, other = meta.get("og_url"), meta.get("alt_url")
    if here:
        out.append(f'<link rel="canonical" href="{here}">')
    if here and other:
        out.append(f'<link rel="alternate" hreflang="{meta.get("lang", "en")}" '
                   f'href="{here}">')
        out.append(f'<link rel="alternate" hreflang="{meta.get("alt_lang", "")}" '
                   f'href="{other}">')
        english = here if meta.get("lang", "en") == "en" else other
        out.append(f'<link rel="alternate" hreflang="x-default" href="{english}">')
    return "\n".join(out)


def render_video(meta):
    vid = meta.get("video")
    if not vid:
        return ""
    caption = meta.get("video_caption", "")
    cap = f"\n    <figcaption>{inline(caption)}</figcaption>" if caption else ""
    return (
        '\n<div class="wrap">\n'
        '  <figure class="video-figure">\n'
        '    <div class="video">\n'
        f'      <iframe src="https://www.youtube.com/embed/{vid}" '
        f'title="{html.escape(meta.get("og_title", "Video"), quote=True)}" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
        'gyroscope; picture-in-picture; web-share" '
        'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n'
        "    </div>"
        f"{cap}\n  </figure>\n</div>\n"
    )


def render_footer(meta):
    lines = []
    if meta.get("footnote"):
        # the marker is added here, so strip one if it was typed in the markdown
        note = meta["footnote"].lstrip("*").strip()
        lines.append(f'  <p id="note">* {inline(note)}</p>')
    if meta.get("credit"):
        lines.append(f'  <p>{inline(meta["credit"])}</p>')
    if meta.get("contact_email"):
        label = meta.get("contact_text", "Questions, corrections, or you have made this yourself")
        addr = meta["contact_email"]
        lines.append(f'  <p class="contact">{inline(label)} '
                     f'<a href="mailto:{addr}">{addr}</a></p>')
    return "\n".join(lines)


def render_next(meta):
    if not meta.get("next_text"):
        return ""
    arrow = "&lsaquo; " if meta.get("nav_side") == "left" else " &rsaquo;"
    label = (f'{arrow}{meta["next_text"]}' if meta.get("nav_side") == "left"
             else f'{meta["next_text"]}{arrow}')
    blurb = meta.get("next_blurb", "")
    return (
        '\n  <div class="next">\n'
        f'    <a href="{meta["next_href"]}">{label}</a>\n'
        + (f"    <p>{inline(blurb)}</p>\n" if blurb else "")
        + "  </div>"
    )


def absolute(meta):
    """og:image has to be a full URL for link previews to work."""
    img, base = meta.get("og_image", ""), meta.get("og_url", "")
    if not img or img.startswith("http"):
        return img
    root = base.rsplit("/", 1)[0] + "/" if base.endswith(".html") else base
    return root.rstrip("/") + "/" + img.lstrip("/")


def load_site():
    """Settings shared by every page, from site.md.

    That file has no `output` key so it is never built as a page of its own.
    A page's own front matter wins over anything set there, which is what
    lets one line in site.md change the contact address everywhere.
    """
    path = os.path.join(HERE, "site.md")
    if not os.path.exists(path):
        return {}
    meta, _ = split_front_matter(open(path, encoding="utf-8").read())
    meta = dict(meta or {})
    meta.pop("output", None)
    return meta


def build(md_path, template, site=None):
    meta, body = split_front_matter(open(md_path, encoding="utf-8").read())
    if meta is None or "output" not in meta:
        return None
    meta = {**(site or {}), **meta}
    meta.setdefault("lang", "en")

    sections = render_sections(body, meta.get("numerals", "latin"))
    # The onward link belongs inside the final section, not adrift after it.
    tail = render_next(meta)
    if tail:
        sections = sections.rsplit("</section>", 1)
        sections = sections[0] + tail + "\n</section>" + sections[1]

    page = template
    for key in ("title", "description", "og_title", "og_description",
                "og_url", "kicker", "headline", "standfirst", "lang"):
        page = page.replace("{{" + key + "}}", meta.get(key, ""))
    page = page.replace("{{og_image_absolute}}", absolute(meta))
    page = page.replace("{{head_links}}", render_head_links(meta))
    page = page.replace("{{nav}}", render_nav(meta))
    page = page.replace("{{video}}", render_video(meta))
    page = page.replace("{{sections}}", sections)
    page = page.replace("{{footer}}", render_footer(meta))

    out = os.path.join(HERE, meta["output"])
    open(out, "w", encoding="utf-8").write(page)
    return meta["output"]


def main():
    template = open(TEMPLATE, encoding="utf-8").read()
    site = load_site()
    written = []
    for name in sorted(os.listdir(HERE)):
        if name.endswith(".md"):
            result = build(os.path.join(HERE, name), template, site)
            if result:
                written.append(f"  {name} -> {result}")
    if not written:
        print("no markdown pages found", file=sys.stderr)
        return 1
    print("\n".join(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
