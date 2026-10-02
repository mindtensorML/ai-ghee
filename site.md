---
site_url: https://mindtensorml.github.io/ai-ghee/
languages: en|English|en_GB ; ne|नेपाली|ne_NP ; fr|Français|fr_FR ; rw|Ikinyarwanda|rw_RW ; lg|Oluganda|lg_UG ; de|Deutsch|de_DE ; zh|中文|zh_CN ; ru|Русский|ru_RU ; es|Español|es_ES ; hi|हिन्दी|hi_IN ; tr|Türkçe|tr_TR ; eu|Euskara|eu_ES ; ka|ქართული|ka_GE ; new|नेपाल भाषा|new_NP ; bn|বাংলা|bn_BD ; ja|日本語|ja_JP ; fil|Filipino|fil_PH ; yue|廣東話|yue_HK ; ar|العربية|ar_AR ; uk|Українська|uk_UA
og_site_name: JD's AI Ghee
og_image_alt: A pot of finished ghee, deep clear amber with a little foam at one edge
author: JD
credit: Photographs are from a single run in August 2026. The churn, the finished jars and the second batch were photographed later.
contact_text: Questions, corrections, or you have built one of these yourself.
contact_email: aighee@proton.me
footer_links: [Privacy](privacy.html) · [Terms](terms.html)
---

# Shared settings

Values every page uses. There is no `output` key here, so this file is never
built into a page of its own. Anything a page sets in its own front matter
wins over what is set here.

The contact address lives here so it can be changed in one place. It is
published, so treat it as disposable. Use a forwarding alias, and if it ever
starts attracting rubbish, delete the alias, put a new one on this line and
commit. Nothing else needs touching.

The privacy and terms links in `footer_links` are set here for the same
reason, so every page carries them. Google's OAuth review checks that both
are reachable from the home page. The labels stay in English on every
translated page, because the two pages they lead to are English only.
Overriding `footer_links` in a language's own two markdown files is all it
would take to change that for that language.

The `languages:` line above is the only place a language is declared. A code,
the name written in the language itself, and a locale. Filenames and sibling
URLs are worked out from the code, and whether a page reads right to left is
worked out from it too, in `build.py`, rather than being set here where a typo
would be silent.
