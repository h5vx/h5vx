#!/usr/bin/env python3
"""Generates SVG project cards (dark + light) and README.md for the GitHub profile."""
from pathlib import Path
from textwrap import wrap
from html import escape

USER = "h5vx"
OUT = Path(__file__).parent

LANG_COLORS = {
    "Go": "#00ADD8", "Python": "#3572A5", "C++": "#f34b7d", "JavaScript": "#f1e05a",
    "Lua": "#5562e8", "Vue": "#41b883", "Qt/QML": "#44a51c", "Kotlin": "#A97BFF",
}

CATEGORIES = [
    ("observability", "Monitoring & Observability", "Prometheus exporters, dashboards, alerting", "#f97316", [
        ("samp-monitor", "SA-MP / open.mp server monitor: Prometheus exporter, REST API, web UI and a ready Grafana dashboard. Zero deps, ~10 MB RSS.", ["Go"], ["prometheus", "grafana"]),
        ("awg_exporter", "Prometheus exporter for AmneziaWG running in Docker: per-client traffic and handshakes labeled with client names.", ["Go"], ["prometheus", "vpn"]),
        ("xiaomi_exporter", "Prometheus exporter for Xiaomi Air Purifier Elite over local miIO protocol. No cloud, no Home Assistant.", ["Python"], ["prometheus", "iot"]),
        ("grafana-xmpp-webhook", "Webhook service that delivers Grafana alerts to XMPP (Jabber) chats.", ["Go"], ["grafana", "xmpp"]),
    ]),
    ("network", "VPN & Networking", "Privacy tools and protocol tinkering", "#22c55e", [
        ("amnezia-client-android-nougat", "Amnezia VPN client (AmneziaWG) built to run on old Android 7 Nougat devices.", ["C++", "Qt/QML", "Kotlin"], ["fork", "vpn", "android"]),
        ("proxychecker", "Simple asynchronous proxy checker.", ["Python"], ["asyncio", "proxy"]),
    ]),
    ("bots", "Bots", "Telegram, XMPP and streaming automation", "#38bdf8", [
        ("BandPlan_bot", "Telegram bot for band rehearsals: polls members' free time, finds overlaps, picks a slot and pins the schedule.", ["Python"], ["telegram"]),
        ("ugubot", "ChatGPT bot for XMPP (Jabber) with a web interface.", ["Python", "Vue"], ["xmpp", "llm"]),
        ("sampboombot", "Finds mp3 tracks on music services and streams them to an Icecast radio.", ["Python", "Lua"], ["icecast", "sa-mp"]),
    ]),
    ("tools", "Tools & Fun", "Small utilities and visual experiments", "#a78bfa", [
        ("pactop", "CLI tool that shows installed pacman packages sorted by size.", ["Go"], ["arch linux", "cli"]),
        ("MechanicalCounter3D", "3D mechanical counter that shows how positional numeral systems work.", ["JavaScript"], ["three.js", "demo"]),
    ]),
]

THEMES = {
    "dark":  dict(bg="#0d1117", card="#161b22", border="#30363d", title="#e6edf3", text="#9da7b3", muted="#7d8590", chip="#21262d"),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", title="#1f2328", text="#424a53", muted="#656d76", chip="#eaeef2"),
}
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
W, H = 440, 150


def chip_width(label, size=10.5):
    return len(label) * size * 0.6 + 14


def card(name, desc, langs, tags, accent, t):
    lines = wrap(desc, 62)[:3]
    desc_svg = "".join(
        f'<text x="24" y="{66 + i * 18}" class="d">{escape(l)}</text>' for i, l in enumerate(lines))

    # language dots
    x, langs_svg = 24, ""
    for lang in langs:
        c = LANG_COLORS.get(lang, t["muted"])
        langs_svg += f'<circle cx="{x + 5}" cy="{H - 21}" r="5" fill="{c}"/>' \
                     f'<text x="{x + 15}" y="{H - 17}" class="m">{escape(lang)}</text>'
        x += 15 + len(lang) * 7 + 14

    # tags, right-aligned
    x, tags_svg = W - 18, ""
    for tag in reversed(tags):
        w = chip_width(tag)
        x -= w
        fill = accent if tag == "fork" else t["chip"]
        color = "#fff" if tag == "fork" else t["muted"]
        tags_svg += f'<rect x="{x:.1f}" y="{H - 32}" width="{w:.1f}" height="19" rx="9.5" fill="{fill}"/>' \
                    f'<text x="{x + w / 2:.1f}" y="{H - 19}" text-anchor="middle" class="c" fill="{color}">{escape(tag)}</text>'
        x -= 6

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .n {{ font: 600 16px {MONO}; fill: {t["title"]}; }}
  .d {{ font: 400 12.5px {FONT}; fill: {t["text"]}; }}
  .m {{ font: 500 12px {FONT}; fill: {t["muted"]}; }}
  .c {{ font: 500 10.5px {MONO}; }}
  .r {{ animation: in .6s ease-out both; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
</style>
<g class="r">
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>
  <rect x="1" y="14" width="4" height="{H - 28}" rx="2" fill="{accent}"/>
  <svg x="24" y="21" width="16" height="16" viewBox="0 0 16 16"><path fill="{accent}" d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"/></svg>
  <text x="48" y="35" class="n">{escape(name)}</text>
  {desc_svg}
  {langs_svg}
  {tags_svg}
</g>
</svg>
'''


def header(title, subtitle, accent, count, t, width=880, height=80):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
  .h {{ font: 700 22px {FONT}; fill: {t["title"]}; }}
  .s {{ font: 400 13px {FONT}; fill: {t["muted"]}; }}
  .k {{ font: 600 12px {MONO}; fill: {accent}; }}
</style>
<rect x="0" y="16" width="6" height="46" rx="3" fill="{accent}"/>
<text x="20" y="36" class="h">{escape(title)}</text>
<text x="20" y="58" class="s">{escape(subtitle)}</text>
<rect x="{width - 74}" y="27" width="72" height="24" rx="12" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".5"/>
<text x="{width - 38}" y="43" text-anchor="middle" class="k">{count} repo{"s" if count != 1 else ""}</text>
<line x1="0" y1="{height - 1}" x2="{width}" y2="{height - 1}" stroke="{t["border"]}"/>
</svg>
'''


def banner(t, width=880, height=170):
    total = sum(len(c[4]) for c in CATEGORIES)
    pills, x = "", 40
    for _, title, _, accent, items in CATEGORIES:
        label = f"{title} · {len(items)}"
        w = len(label) * 7.1 + 26
        pills += f'<rect x="{x:.0f}" y="112" width="{w:.0f}" height="28" rx="14" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".55"/>' \
                 f'<circle cx="{x + 14:.0f}" cy="126" r="4" fill="{accent}"/>' \
                 f'<text x="{x + 24:.0f}" y="130.5" class="p">{escape(label)}</text>'
        x += w + 10
    grad = "".join(f'<stop offset="{i / (len(CATEGORIES) - 1):.2f}" stop-color="{c[3]}"/>' for i, c in enumerate(CATEGORIES))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="g" x1="0" x2="1">{grad}</linearGradient>
  <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t["border"]}"/></pattern>
</defs>
<style>
  .t {{ font: 800 34px {FONT}; fill: {t["title"]}; }}
  .u {{ font: 500 15px {MONO}; fill: {t["muted"]}; }}
  .p {{ font: 500 12.5px {FONT}; fill: {t["title"]}; }}
  .bar {{ animation: grow 1.2s cubic-bezier(.2,.8,.2,1) both; transform-origin: left; }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
</style>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="16" fill="url(#dots)" opacity=".6"/>
<rect class="bar" x="40" y="30" width="56" height="5" rx="2.5" fill="url(#g)"/>
<text x="40" y="78" class="t">Projects</text>
<text x="{width - 40}" y="78" text-anchor="end" class="u">github.com/{USER} · {total} repos</text>
{pills}
</svg>
'''


def picture(base, alt, href=None, width=None):
    w = f' width="{width}"' if width else ""
    pic = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{base}-dark.svg">'
           f'<img alt="{escape(alt)}" src="./assets/{base}-light.svg"{w}></picture>')
    return f'<a href="{href}">{pic}</a>' if href else pic


def main():
    assets = OUT / "assets"
    assets.mkdir(exist_ok=True)
    for f in assets.glob("*.svg"):
        f.unlink()

    md = ["<!-- generated by generate.py -->", '<div align="center">', "",
          picture("banner", "Projects", width="100%"), "", "</div>", ""]
    for key, title, subtitle, accent, items in CATEGORIES:
        for mode, t in THEMES.items():
            (assets / f"cat-{key}-{mode}.svg").write_text(header(title, subtitle, accent, len(items), t))
        md += ["", picture(f"cat-{key}", title, width="100%"), "", '<p align="center">']
        for name, desc, langs, tags, in items:
            for mode, t in THEMES.items():
                (assets / f"card-{name}-{mode}.svg").write_text(card(name, desc, langs, tags, accent, t))
            md.append(picture(f"card-{name}", name, f"https://github.com/{USER}/{name}", width="49%"))
        md.append("</p>")
    for mode, t in THEMES.items():
        (assets / f"banner-{mode}.svg").write_text(banner(t))
    (OUT / "README.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
