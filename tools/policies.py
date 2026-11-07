"""Builds the per-game privacy pages from the policy text below. Run: python3 tools/policies.py"""
import html, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = """
@font-face{font-family:"Alegreya";font-weight:800;font-display:swap;src:url(../fonts/alegreya-latin-800-normal.woff2) format("woff2")}
@font-face{font-family:"Alegreya";font-weight:700;font-display:swap;src:url(../fonts/alegreya-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"Alegreya Sans";font-weight:400;font-display:swap;src:url(../fonts/alegreya-sans-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Alegreya Sans";font-weight:400;font-display:swap;src:url(../fonts/alegreya-sans-latin-ext-400-normal.woff2) format("woff2");unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1EFF}
@font-face{font-family:"Alegreya Sans";font-weight:700;font-display:swap;src:url(../fonts/alegreya-sans-latin-700-normal.woff2) format("woff2")}
:root{--paper:#EFE7D4;--surface:#F7F1E3;--ink:#2B1D14;--muted:#6B5A4A;--line:rgba(43,29,20,.16);--accent:#A4561E;--gold:#A87A1E;
  --display:"Alegreya",Georgia,"Times New Roman",serif;--body:"Alegreya Sans","Gill Sans","Trebuchet MS",sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#1A1411;--surface:#241C17;--ink:#EFE6D4;--muted:#B5A48E;--line:rgba(239,230,212,.15);--accent:#E0965A;--gold:#D9A94A;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#1A1411;--surface:#241C17;--ink:#EFE6D4;--muted:#B5A48E;--line:rgba(239,230,212,.15);--accent:#E0965A;--gold:#D9A94A;color-scheme:dark}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:1.06rem/1.6 var(--body);padding:28px max(16px,env(safe-area-inset-left,0px)) 64px}
main{max-width:680px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
a{color:var(--accent);text-underline-offset:3px}a:focus-visible{outline:3px solid var(--gold);outline-offset:2px;border-radius:4px}
.studio{display:flex;align-items:center;gap:10px;font:700 .95rem/1 var(--display);color:var(--muted);text-decoration:none}
.studio img{width:36px;height:36px;border-radius:9px}
header{display:flex;flex-direction:column;gap:6px;padding-bottom:18px;border-bottom:2px solid var(--line)}
.eyebrow{font:700 .8rem/1 var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
h1{font:800 clamp(1.8rem,6vw,2.4rem)/1.1 var(--display);margin:0;text-wrap:balance}
h2{font:700 1.3rem/1.2 var(--display);margin:8px 0 0}
p,ul{margin:0}ul{padding-left:20px;display:flex;flex-direction:column;gap:6px}
.dates{color:var(--muted);font-size:.95rem}
.short{font-size:1.15rem;padding:14px 16px;border-left:3px solid var(--gold);background:var(--surface);border-radius:0 10px 10px 0}
.lang{display:flex;gap:14px;font-weight:700}
section{display:flex;flex-direction:column;gap:10px}
footer{color:var(--muted);font-size:.92rem;border-top:1px solid var(--line);padding-top:16px}
"""
def md(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"([\w.+-]+@[\w.-]+\.\w+)", lambda m: f'<a href="mailto:{m.group(1).replace("+","%2B")}">{m.group(1)}</a>', s)
    return s
def body(blocks):
    out = []
    for b in blocks:
        if b.startswith("## "): out.append(f"<h2>{md(b[3:])}</h2>")
        elif b.startswith("> "): out.append(f'<p class="short">{md(b[2:])}</p>')
        elif b.startswith("- "): out.append("<ul>" + "".join(f"<li>{md(x[2:])}</li>" for x in b.split("\n")) + "</ul>")
        else: out.append(f"<p>{md(b)}</p>")
    return "\n    ".join(out)
def page(slug, title, updated, sections, lang_note=""):
    parts = []
    for sid, lang, blocks in sections:
        parts.append(f'<section id="{sid}" lang="{lang}">\n    {body(blocks)}\n  </section>')
    langs = ""
    if len(sections) > 1:
        langs = '<nav class="lang" aria-label="Language">' + "".join(f'<a href="#{s[0]}">{ {"en":"English","sr":"Srpski"}[s[1]] }</a>' for s in sections) + "</nav>"
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)} Privacy Policy</title>
<link rel="icon" href="../img/favicon.png">
<style>{CSS}</style>
</head>
<body>
<main>
  <a class="studio" href="../"><img src="../img/mark.webp" alt="" width="36" height="36">Duralek Games</a>
  <header>
    <span class="eyebrow">{html.escape(title)}</span>
    <h1>Privacy policy</h1>
    <p class="dates">Last updated: {updated}</p>
  </header>
  {langs}
  {chr(10).join(parts)}
  <footer>{html.escape(title)} is made by Duralek, an independent game studio in Hawaiʻi. <a href="../">More games</a></footer>
</main>
</body>
</html>
"""
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    with open(os.path.join(ROOT, slug, "privacy.html"), "w") as f: f.write(doc)

EMAIL = "dukaduka1@gmail.com"

# Up the Village: the policy from the game's own repo (docs/privacy.html), unchanged in substance.
page("up-the-village", "Up the Village", "November 2026", [("en", "en", [
"> The short version: the game does not collect, store or share any personal information about you.",
"## What the game stores",
"Your progress (your club, squad, money and so on) is saved on your own device so you can continue later. It never leaves your device and we cannot see it. Deleting the app deletes the save.",
"## What we do not do",
"- No accounts or sign-in\n- No advertising and no ad trackers\n- No analytics or usage tracking\n- No personal data sold, shared or collected\n- No payment data stored by us (in versions that offer the optional Supporter purchase, an anonymous purchase-checking id and, if you buy, your store receipt go to RevenueCat; see Purchases)",
"## Links you choose to open",
"The game itself sends nothing anywhere. In Settings, three buttons can hand something to your phone, and only when you tap them: “Rate the game” opens the game’s page in the app store; “Share the game” opens your phone’s own share sheet with a short message and the store link, and you pick where (if anywhere) it goes; “Send feedback” opens your own email app with a message already written that holds the app’s version, the kind of device and where your club is in the game. That message is shown to you in full before anything is sent, and it is only sent if you press send in your email app.",
"## Purchases",
"The whole game is free to play. Version 1.0 has no purchases at all and makes no network connections. A later version may add one optional, one-time in-app purchase, “Supporter”, which would add cosmetic extras (a badge, a kit and a bench plaque) and change nothing about how the game plays. The rest of this section applies only to versions that offer it. The purchase is made and paid for entirely through Google Play (or the Apple App Store on iPhone). We never see or store your card number, your name, your address or any other payment details, and we have no account system to attach them to.",
"To remember that you are a supporter, the game keeps a small flag on your own device, and checks on launch whether your store account owns the purchase (this is what “Restore purchase” does). To do this we use a service called RevenueCat, which receives your purchase receipt from the store and an anonymous app user id it generates for your install. The app contacts RevenueCat when it starts, so the id and basic technical data such as your IP address, device type and app version reach it even if you never buy. It receives no name, email or advertising id from us, and we do not use it for tracking or advertising. RevenueCat’s handling is covered by its privacy policy; the store’s part is covered by Google’s or Apple’s privacy policy. Refunds are handled by Google Play under its own rules. If you choose to write a short bench plaque, the text is saved on your device with your save and goes nowhere else.",
"## Children",
"The game is gentle comedy and collects no data from anyone, including children.",
"## Contact",
f"Questions about this policy: {EMAIL}",
])])

# From the Block: the policy from the game's own repo (PRIVACY.md), English and Serbian.
page("from-the-block", "From the Block", "October 2026", [
("en", "en", [
"From the Block is a single-player basketball career game made by an independent developer.",
"- **The app collects no personal data.** It has no accounts, no analytics, no advertising, no tracking and no in-app purchases.\n- **The app has no internet permission.** It cannot send anything off your phone. The game, its pictures and its fonts are all inside the app.\n- **Your career is saved only on your device**, in the app's local storage. If you uninstall the app or clear its data, the save is deleted. Use the backup code in the game's settings to keep a copy yourself.\n- **The backup code** is text that you copy yourself. The app never sends it anywhere.\n- **Children.** The game is meant for players aged 13 and over.\n- **Changes.** If this ever changes, this page will be updated before a new version is released.",
f"Contact: {EMAIL}"]),
("sr", "sr", [
"## Srpski",
"Iz bloka (From the Block) je košarkaška igra za jednog igrača koju pravi nezavisni developer.",
"- **Aplikacija ne prikuplja lične podatke.** Nema naloga, analitike, reklama, praćenja ni kupovine u aplikaciji.\n- **Aplikacija nema dozvolu za internet.** Ništa ne može da pošalje sa tvog telefona. Igra, slike i fontovi su u samoj aplikaciji.\n- **Tvoja karijera se čuva samo na tvom uređaju**, u lokalnoj memoriji aplikacije. Ako obrišeš aplikaciju ili njene podatke, sačuvana igra nestaje. Backup kod iz podešavanja igre služi da sam sačuvaš kopiju.\n- **Backup kod** je tekst koji sam kopiraš. Aplikacija ga nikad nigde ne šalje.\n- **Deca.** Igra je namenjena igračima od 13 godina.\n- **Izmene.** Ako se nešto promeni, ova stranica će biti ažurirana pre izlaska nove verzije.",
f"Kontakt: {EMAIL}"])])

# Od Sela do Vrha: the policy from the game's own repo (PRIVACY.md), English and Serbian.
page("od-sela-do-vrha", "Od Sela do Vrha", "28 October 2026", [
("en", "en", [
"Od Sela do Vrha is a single-player football club owner game. It is made by an independent developer.",
"**What the app collects: nothing.**",
"- The game itself sends nothing anywhere. There are no accounts, no ads, no analytics and no tracking.\n- **Supporting the developer.** The whole game is free. In the menu you can choose to support the developer with an optional purchase; it gives no advantage in the game. The purchase is handled entirely by Google Play through Google's Play Billing library, under Google's own privacy policy. The app only asks Google Play whether this Google account has supported the game. It never sees your payment details.\n- Your careers, settings and achievements are saved only on your own phone, in the app's private storage (and in your phone's own Android backup, if you have that turned on). Uninstalling the app or clearing its data deletes them.\n- The \"copy save code\" feature creates a text code that you can copy yourself. The app never sends it anywhere.\n- The app may use the phone's vibration for game feedback. You can turn it off in Options.",
"**Children.** The game is not directed at children under 13 and does not knowingly collect any information from anyone.",
"**Changes.** If this ever changes, this page will be updated before the new version is released.",
f"**Contact.** {EMAIL}"]),
("sr", "sr", [
"## Srpski",
"Od Sela do Vrha je igra za jednog igrača o vlasniku fudbalskog kluba. Pravi je nezavisni autor.",
"**Šta aplikacija prikuplja: ništa.**",
"- Igra sama nigde ništa ne šalje. Nema naloga, reklama, analitike ni praćenja.\n- **Podrška autoru.** Cela igra je besplatna. U meniju možeš, ako želiš, da podržiš autora kupovinom koja ne daje nikakvu prednost u igri. Kupovinu u celosti obavlja Google Play preko Google-ove biblioteke Play Billing, po Google-ovoj politici privatnosti. Aplikacija samo pita Google Play da li je ovaj Google nalog podržao igru. Podatke o plaćanju nikad ne vidi.\n- Karijere, podešavanja i dostignuća čuvaju se samo na tvom telefonu, u privatnom prostoru aplikacije (i u rezervnoj kopiji tvog telefona, ako ti je uključena). Brisanjem aplikacije ili njenih podataka sve se briše.\n- „Kopiraj kod\" pravi tekstualni kod koji sam kopiraš. Aplikacija ga nikad nikome ne šalje.\n- Aplikacija može da koristi vibraciju telefona tokom igre. Možeš je isključiti u Opcijama.",
"**Deca.** Igra nije namenjena deci mlađoj od 13 godina i ni od koga svesno ne prikuplja podatke.",
"**Izmene.** Ako se ovo ikada promeni, ova stranica biće izmenjena pre izlaska nove verzije.",
f"**Kontakt.** {EMAIL}"])])

# Huakaʻi: new. Facts from the Godot project: Android export asks for no permissions, no network code,
# saves only to the app's own storage (save.json, checkpoints, album.cfg, settings.cfg).
page("huakai", "Huakaʻi", "November 2026", [("en", "en", [
"> Huakaʻi does not collect, send or share any information about you. Your game stays on your device.",
"## What the game stores",
"To let you carry on where you left off, the game saves on your device:",
"- your journey (where you are, your village, your journal) and a few checkpoints to go back to\n- the keepsakes and places you have found\n- your settings, such as sound and controls",
"This stays inside the app's own storage. It is never sent to us or anyone else. Uninstalling the app or clearing its data deletes it.",
"## What the game does not do",
"- It has no accounts, no ads, no analytics and no tracking.\n- It does not connect to the internet, and the Android app asks for no special permissions.\n- It has no in-app purchases.\n- It does not use your location, contacts, camera, microphone or files.",
"## Children",
"The game is gentle and suitable for families. Because it collects nothing, it collects nothing from children either.",
"## Changes",
"If a future version changes any of this, this page will be updated first, with a new date.",
"## Contact",
f"Questions about this policy: {EMAIL}"])])
print("built")
