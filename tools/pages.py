"""Builds support and press pages for the games. Run: python3 tools/pages.py (after policies.py; shares its CSS)."""
import html, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = re.search(r'CSS = """(.*?)"""', open(os.path.join(ROOT, "tools", "policies.py")).read(), re.S).group(1)
EMAIL = "hello@duralek.games"
GAMES = {
 "up-the-village": dict(title="Mud, Tea and Hope", genre="Football · village comedy", img="up-the-village", press=True,
   blurb="Take a muddy English village team up the leagues, and keep the village’s heart while the money and the strangers arrive. Formerly Up the Village.",
   links=[("Google Play","https://play.google.com/store/apps/details?id=com.leftym.upthevillage"),("App Store","https://apps.apple.com/app/id6832921996")],
   facts=["Single-player football club story","Free, no ads, no accounts, no tracking","Works offline","Android and iPhone"]),
 "od-sela-do-vrha": dict(title="Od Sela do Vrha", genre="Football · club owner", img="od-sela-do-vrha", press=True,
   blurb="From a village pitch to the top: build the squad, the stadium and the community around a small club in the Balkans. Played in Serbian and English.",
   links=[("Google Play","https://play.google.com/store/apps/details?id=com.leftym.odseladovrha")],
   facts=["Single-player football club owner game","Free, no ads, no accounts, no tracking, no purchases","Works offline","Serbian and English"]),
 "from-the-block": dict(title="From the Block", genre="Basketball · career story", img="from-the-block", press=False,
   blurb="A sixteen-year-old point guard from a small New Belgrade club, and the road from the neighborhood court to college ball.", links=[], facts=[]),
 "huakai": dict(title="Huakaʻi", genre="Story adventure · ancient Hawaiʻi", img="huakai", press=False,
   blurb="A child arrives on Oʻahu by voyaging canoe and, over twenty years, grows into the one four villages trust to speak for them.", links=[], facts=[]),
}
def page(slug, name, heading, body):
    g = GAMES[slug]
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(g['title'])} {name}</title>
<link rel="icon" href="../img/favicon.png">
<style>{CSS}</style>
</head>
<body>
<main>
  <a class="studio" href="../"><img src="../img/mark.webp" alt="" width="36" height="36">Duralek Games</a>
  <header>
    <span class="eyebrow">{html.escape(g['title'])}</span>
    <h1>{heading}</h1>
  </header>
  {body}
  <footer>{html.escape(g['title'])} is made by Duralek, an independent game studio in Hawaiʻi. <a href="../">More games</a> · <a href="privacy.html">Privacy</a> · <a href="support.html">Support</a></footer>
</main>
</body>
</html>
"""
    open(os.path.join(ROOT, slug, name.lower() + ".html" if name != "Press" else "index.html"), "w").write(doc)
for slug, g in GAMES.items():
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    page(slug, "Support", "Support", f"""<section><p>Questions, bug reports and ideas are welcome. Write to {mail} and say which game and phone you use. If something broke, tell us what you were doing when it happened.</p>
  <h2>Common questions</h2>
  <p><b>Where is my game saved?</b> On your phone, inside the app. There are no accounts and nothing is stored online. Deleting the app or clearing its data deletes the save.</p>
  <p><b>Does the game need the internet?</b> No. It works offline.</p>
  <p><b>Does it collect my data?</b> No. See the <a href="privacy.html">privacy policy</a>.</p></section>""")
    if g["press"]:
        links = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in g["links"])
        facts = "".join(f"<li>{html.escape(f)}</li>" for f in g["facts"])
        page(slug, "Press", "Press page", f"""<section><p class="short">{html.escape(g['blurb'])}</p>
  <h2>Facts</h2><ul><li>Genre: {html.escape(g['genre'])}</li><li>Developer and publisher: Duralek</li><li>Price: free</li>{facts}</ul>
  <h2>Download</h2><ul>{links}</ul>
  <h2>Assets</h2><p>Icon: <a href="../img/{g['img']}.webp">{g['img']}.webp</a>. Trailer: <a href="../trailers/{slug}.mp4">{slug}.mp4</a>. More art on request.</p>
  <h2>Contact</h2><p>{mail}</p></section>""")
