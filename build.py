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
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "template.html")

# The chart and the schematic are each drawn at two sizes so they stay readable
# on a phone, once per language. This used to be a hand written map of every
# pair, which is a line that gets forgotten the next time a language is added,
# and forgetting it does more than drop the phone image. A drawing that is not
# recognised here loses the card around it as well, so it would quietly render
# a shade different from the same drawing on every other page. The narrow twin
# is looked up on disk instead, so a language appears the moment it is drawn.

# A page can ask for its section numbers in Devanagari. Nothing else on the
# page is renumbered, because a milliamp reading is written the same way in
# both languages.
DEVANAGARI = str.maketrans("0123456789", "०१२३४५६७८९")

# What a screen reader says for the [*] that points at the footnote. It is set
# per page from the front matter, because it was English on the Nepali page.
NOTE_LABEL = "See note about this chart"


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
        f'<a href="#note" aria-label="{html.escape(NOTE_LABEL, quote=True)}">*</a>')
    return out


IMAGE_RE = re.compile(r'^!\[(?P<caption>.*?)\]\((?P<src>\S+?)(?:\s+"(?P<alt>[^"]*)")?\)\s*$')
ROW_RE = re.compile(r"^\|(?P<cells>.+)\|\s*$")


# -------------------------------------------------------------------- blocks

def responsive_variant(src):
    """The phone sized twin of a drawing, if one has been generated."""
    if not src.endswith(".svg"):
        return None
    stem, _, ext = src.rpartition(".")
    if stem.endswith("-narrow"):
        return None
    narrow = f"{stem}-narrow.{ext}"
    return narrow if os.path.exists(os.path.join(HERE, narrow)) else None


def figure(src, caption, alt, in_group):
    size = image_size(src)
    dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
    alt_attr = html.escape(alt or caption, quote=True)
    cap = f"\n      <figcaption>{inline(caption)}</figcaption>" if caption else ""

    narrow = responsive_variant(src)
    if narrow:
        # The chart carries no shadow of its own, the card around it does.
        img = (f'<img src="{src}"{dims} alt="{alt_attr}">')
        return (
            "    <figure>\n"
            '      <div class="chart">\n'
            "        <picture>\n"
            f'          <source media="(max-width: 620px)" srcset="{narrow}">\n'
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

# ------------------------------------------------------------------ languages

def languages(meta):
    """The site's languages, in the order they are declared in site.md.

    One entry per language, `code|label|locale`, separated by semicolons. The
    label is written in the language itself, because that is what a reader
    scanning the masthead for their own language is looking for.

        languages: en|English|en_GB ; ne|\u0928\u0947\u092a\u093e\u0932\u0940|ne_NP

    The file suffix is derived from the code, so `story.md` with `stem: index`
    becomes index.html in English and index-ne.html in Nepali. English carries
    no suffix because it was the first version of the site and its filenames
    are the ones already linked to from elsewhere.
    """
    out = []
    for part in meta.get("languages", "").split(";"):
        bits = [b.strip() for b in part.split("|")]
        if len(bits) == 3 and bits[0]:
            code, label, locale = bits
            out.append({"code": code, "label": label, "locale": locale,
                        "suffix": "" if code == "en" else "-" + code})
    return out


def page_file(stem, suffix):
    return f"{stem}{suffix}.html"


def page_url(base, stem, suffix):
    """The absolute URL of one page.

    The English story page is served as the bare directory rather than
    index.html, because that is the address the site is linked by, so the
    canonical URL has to collapse to it or two URLs serve one page.
    """
    name = page_file(stem, suffix)
    if name == "index.html":
        return base
    return base + name


def alternates(meta):
    """Every language version of this page except the one being written."""
    stem, base = meta.get("stem"), meta.get("site_url", "")
    if not stem:
        return []
    here = meta.get("lang", "en")
    return [{**lang,
             "href": page_file(stem, lang["suffix"]),
             "url": page_url(base, stem, lang["suffix"])}
            for lang in languages(meta) if lang["code"] != here]


def home_href(meta):
    """The story page in the language being read, or nothing from the story.

    The mark is what a reader clicks to get back, and it has to land them in
    the language they were already in rather than dropping them into English.
    On the story page itself it is a link to nowhere, so it is not made one.
    """
    here = meta.get("lang", "en")
    suffix = "" if here == "en" else "-" + here
    target = page_file("index", suffix)
    if meta.get("output") == target:
        return None
    return "./" if target == "index.html" else target


def here_label(meta):
    """What this page's own language calls itself, for the switcher button."""
    here = meta.get("lang", "en")
    for lang in languages(meta):
        if lang["code"] == here:
            return lang["label"]
    return here.upper()


def render_nav(meta):
    # the mark is decorative here, the name is right beside it, so alt is empty
    glyph = (f'<img src="logo.svg" alt="" width="24" height="24">'
             f'{meta.get("mark", "")}')
    home = home_href(meta)
    mark = (f'  <a class="mark" href="{home}">{glyph}</a>' if home
            else f'  <span class="mark">{glyph}</span>')

    links = []
    if meta.get("nav_text"):
        arrow = "&lsaquo; " if meta.get("nav_side") == "left" else ""
        tail = "" if arrow else " &rsaquo;"
        links.append(f'<a class="page" href="{meta["nav_href"]}">'
                     f'{arrow}{meta["nav_text"]}{tail}</a>')

    # The languages go behind a disclosure rather than sitting in the line.
    # Nine of them already wrapped to a second row inside the text column, and
    # the plan is more. `details` does this with no JavaScript at all, which
    # keeps the site at zero, and it is keyboard operable as it comes.
    #
    # One switcher link per other language, labelled in the language it leads
    # to and carrying that language so a screen reader says the word properly.
    others = alternates(meta)
    if others:
        items = "".join(
            f'<li><a class="lang" href="{a["href"]}" lang="{a["code"]}" '
            f'hreflang="{a["code"]}">{a["label"]}</a></li>' for a in others)
        label = here_label(meta)
        links.append(
            f'<details class="langs"><summary aria-label="Language, '
            f'{label}"><span class="here">{label}</span></summary>'
            f'<ul lang="">{items}</ul></details>')

    if not links:
        return mark

    group = '  <nav class="links">' + "".join(links) + "</nav>"
    return f"{group}\n{mark}" if meta.get("nav_side") == "left" else f"{mark}\n{group}"


def render_head_links(meta):
    """Canonical, og:locale and an hreflang line per language.

    Every version points at itself and at all the others, which is what tells
    a search engine they are one page in several languages rather than several
    pages. x-default goes to English, as the version to fall back to.
    """
    out = []
    if meta.get("locale"):
        out.append(f'<meta property="og:locale" content="{meta["locale"]}">')
    alts = alternates(meta)
    for alt in alts:
        out.append('<meta property="og:locale:alternate" '
                   f'content="{alt["locale"]}">')
    here = meta.get("og_url")
    if here:
        out.append(f'<link rel="canonical" href="{here}">')
    if here and alts:
        out.append(f'<link rel="alternate" hreflang="{meta.get("lang", "en")}" '
                   f'href="{here}">')
        for alt in alts:
            out.append(f'<link rel="alternate" hreflang="{alt["code"]}" '
                       f'href="{alt["url"]}">')
        english = here if meta.get("lang", "en") == "en" else next(
            (a["url"] for a in alts if a["code"] == "en"), here)
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
        f'      <iframe src="https://www.youtube-nocookie.com/embed/{vid}" '
        f'loading="lazy" '
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
    if meta.get("footer_links"):
        # the privacy and terms links, set once in site.md so every page carries
        # them. Google's OAuth review wants both reachable from the home page.
        lines.append(f'  <p class="legal">{inline(meta["footer_links"])}</p>')
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


def absolute(meta, img=None):
    """A full URL for an image, which link previews and schema both need.

    Defaults to og:image. The structured data passes its own, because the
    social card carries the title in big type and a search result wants a
    photograph of the thing instead.
    """
    img = img or meta.get("og_image", "")
    base = meta.get("og_url", "")
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


def render_schema(meta):
    """One block of JSON-LD per page, describing it as an article.

    Only what is already on the page goes in. There is no publication date in
    the front matter and one is not invented here, because a wrong date is
    worse to a search engine than no date. `inLanguage` plus the alternates
    already in the head are what tell it these are one article in nine
    languages rather than nine articles.
    """
    base = meta.get("site_url", "")
    if not base or not meta.get("headline"):
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta.get("og_title") or meta.get("headline", ""),
        "description": meta.get("og_description") or meta.get("description", ""),
        "image": absolute(meta, meta.get("schema_image")),
        "inLanguage": meta.get("lang", "en"),
        "mainEntityOfPage": {"@type": "WebPage", "@id": meta.get("og_url", base)},
        "isAccessibleForFree": True,
    }
    if meta.get("author"):
        data["author"] = {"@type": "Person", "name": meta["author"]}
    if meta.get("og_site_name"):
        data["isPartOf"] = {"@type": "WebSite", "name": meta["og_site_name"],
                            "url": base}
    body = json.dumps(data, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{body}\n</script>'


def build(md_path, template, site=None):
    meta, body = split_front_matter(open(md_path, encoding="utf-8").read())
    if meta is None or "output" not in meta:
        return None
    meta = {**(site or {}), **meta}
    meta.setdefault("lang", "en")
    globals()["NOTE_LABEL"] = meta.get("note_label", "See note about this chart")

    sections = render_sections(body, meta.get("numerals", "latin"))
    # The onward link belongs inside the final section, not adrift after it.
    tail = render_next(meta)
    if tail:
        sections = sections.rsplit("</section>", 1)
        sections = sections[0] + tail + "\n</section>" + sections[1]

    page = template
    for key in ("title", "description", "og_title", "og_description",
                "og_url", "kicker", "headline", "standfirst", "lang",
                "skip_text", "og_site_name", "og_image_alt"):
        page = page.replace("{{" + key + "}}", meta.get(key, ""))
    page = page.replace("{{schema}}", render_schema(meta))
    page = page.replace("{{og_image_absolute}}", absolute(meta))
    page = page.replace("{{head_links}}", render_head_links(meta))
    page = page.replace("{{nav}}", render_nav(meta))
    page = page.replace("{{video}}", render_video(meta))
    page = page.replace("{{sections}}", sections)
    page = page.replace("{{footer}}", render_footer(meta))

    out = os.path.join(HERE, meta["output"])
    open(out, "w", encoding="utf-8").write(page)
    return meta["output"]


def write_sitemap(site, pages):
    """One sitemap for every page the build just wrote.

    Written here rather than kept by hand because the page count is the
    language count times two plus the legal pages, and a list maintained by
    hand is a list that goes stale the first time a language is added.
    """
    base = site.get("site_url", "")
    if not base:
        return None
    urls = []
    for name in sorted(set(pages)):
        loc = base if name == "index.html" else base + name
        urls.append(f"  <url><loc>{loc}</loc></url>")
    doc = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8").write(doc)
    open(os.path.join(HERE, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n")
    return len(urls)


def main():
    template = open(TEMPLATE, encoding="utf-8").read()
    site = load_site()
    written, pages = [], []
    for name in sorted(os.listdir(HERE)):
        if name.endswith(".md"):
            result = build(os.path.join(HERE, name), template, site)
            if result:
                written.append(f"  {name} -> {result}")
                pages.append(result)
    if not written:
        print("no markdown pages found", file=sys.stderr)
        return 1
    print("\n".join(written))
    n = write_sitemap(site, pages)
    if n:
        print(f"  sitemap.xml -> {n} urls, robots.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
