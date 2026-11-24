# -*- coding: utf-8 -*-
"""Erzeugt die Anki-Pakete (.apkg) im Ordner dist/.   Aufruf: python3 build_decks.py"""
import os, genanki
from content import VOCAB, FACTS

HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(HERE, "media")
DIST = os.path.join(HERE, "dist")
os.makedirs(DIST, exist_ok=True)

CREDITS = {  # Bild-Schlüssel -> Quellenangabe (Wikimedia Commons)
    "cathedrale": "Foto: Benh LIEU SON, CC BY-SA 3.0, Wikimedia Commons („Notre Dame Paris front facade lower.jpg“)",
    "gare": "Foto: Wikimedia Commons, CC BY-SA 3.0 („Gare du Nord Paris Hall RER.jpg“)",
    "boulangerie": "Foto: Fabien le libre, CC BY-SA 3.0, Wikimedia Commons („Boulangerie de la rue Montgallet à Paris.jpg“)",
    "magasin": "Foto: John75002, CC BY-SA 3.0, Wikimedia Commons („Magasin stern.jpg“)",
    "centre_commercial": "Foto: Seble, CC BY-SA 4.0, Wikimedia Commons („Centre commercial de la Part-Dieu - Affluence Noël 2017.jpg“)",
    "science": "Foto: axv, CC BY 4.0, Wikimedia Commons („Researcher at work in her laboratory.jpg“)",
    "fan": "Foto: NamiiCho, CC BY 3.0, Wikimedia Commons (BTS-Fans, Hamilton 2018)",
    "question": "Foto: Carlosar, gemeinfrei, Wikimedia Commons („Question mark.jpg“)",
    "entre": "Eigene Illustration (CC0)", "reponse": "Eigene Illustration (CC0)",
    "un_une": "Eigene Illustration (CC0)", "des": "Eigene Illustration (CC0)",
}

CSS = """
.card { font-family: 'Segoe UI', Arial, sans-serif; font-size: 22px; text-align: center; color: #222; background: #fdf6e3; }
.fr { font-size: 36px; font-weight: bold; color: #1f4e9c; }
.ipa { font-size: 20px; color: #777; margin-top: 4px; }
.de { font-size: 30px; font-weight: bold; color: #1b7a3a; }
.genus { display:inline-block; font-size: 14px; background:#e8dfc6; border-radius: 10px; padding: 2px 10px; margin-top: 8px; color:#555; }
.ex { margin-top: 16px; font-size: 20px; } .ex-de { color:#666; font-style: italic; font-size: 18px; }
.tip { margin: 14px auto 0; max-width: 520px; font-size: 16px; background:#fff3cd; border-radius: 8px; padding: 8px 12px; text-align:left; }
.pic img { max-width: 360px; max-height: 240px; border-radius: 10px; margin-top: 10px; }
.src { font-size: 10px; color:#999; margin-top: 4px; }
.fact-q { font-size: 24px; font-weight: bold; color:#1f4e9c; } .fact-a { font-size: 21px; margin-top: 10px; }
"""

PIC = '{{#Bild}}<div class="pic">{{Bild}}<div class="src">{{Quelle}}</div></div>{{/Bild}}'
BACK_INFO = ('<div class="ex">{{BeispielFr}}<div class="ex-de">{{BeispielDe}}</div></div>'
             '{{#Merkhilfe}}<div class="tip">💡 {{Merkhilfe}}</div>{{/Merkhilfe}}')

vocab_model = genanki.Model(
    1607392319, "Französisch Vokabel (DE/FR + Bild)",
    fields=[{"name": n} for n in ["Fr", "IPA", "De", "Genus", "BeispielFr", "BeispielDe", "Merkhilfe", "Bild", "Quelle"]],
    templates=[
        {"name": "FR → DE",
         "qfmt": '<div class="fr">{{Fr}}</div><div class="ipa">[{{IPA}}]</div>' + PIC,
         "afmt": '{{FrontSide}}<hr id="answer"><div class="de">{{De}}</div>'
                 '{{#Genus}}<div class="genus">{{Genus}}</div>{{/Genus}}' + BACK_INFO},
        {"name": "DE → FR",
         "qfmt": '<div class="de">{{De}}</div>{{#Genus}}<div class="genus">{{Genus}}</div>{{/Genus}}',
         "afmt": '{{FrontSide}}<hr id="answer"><div class="fr">{{Fr}}</div><div class="ipa">[{{IPA}}]</div>' + PIC + BACK_INFO},
        {"name": "Bild → Wort",
         "qfmt": '{{#Bild}}<div class="ipa">Wie heißt das auf Französisch?</div><div class="pic">{{Bild}}</div>{{/Bild}}',
         "afmt": '{{FrontSide}}<hr id="answer"><div class="fr">{{Fr}}</div><div class="ipa">[{{IPA}}]</div>'
                 '<div class="de">{{De}}</div><div class="src">{{Quelle}}</div>'},
    ],
    css=CSS)

fact_model = genanki.Model(
    1607392320, "Französisch Wissen (Frage/Antwort + Bild)",
    fields=[{"name": n} for n in ["Frage", "Antwort", "Bild", "Quelle"]],
    templates=[{"name": "Frage → Antwort",
                "qfmt": '<div class="fact-q">{{Frage}}</div>',
                "afmt": '{{FrontSide}}<hr id="answer"><div class="fact-a">{{Antwort}}</div>' + PIC}],
    css=CSS)

def img(key):
    if not key: return "", ""
    path = os.path.join(MEDIA, f"fr_{key}.jpg")
    assert os.path.exists(path), path
    return f'<img src="fr_{key}.jpg">', CREDITS[key]

def build(deck_id, name, notes, media, fname):
    deck = genanki.Deck(deck_id, name)
    for n in notes: deck.add_note(n)
    pkg = genanki.Package(deck); pkg.media_files = sorted(set(media))
    out = os.path.join(DIST, fname); pkg.write_to_file(out); print("geschrieben:", out, len(notes), "Notizen")

# Paket 1: Vokabeln
notes, media = [], []
for v in VOCAB:
    bild, quelle = img(v["image"])
    if v["image"]: media.append(os.path.join(MEDIA, f"fr_{v['image']}.jpg"))
    notes.append(genanki.Note(model=vocab_model,
        guid=genanki.guid_for("vokabel", v["key"]),
        fields=[v["fr"], v["ipa"], v["de"], v["gender"], v["example_fr"], v["example_de"], v["tip"], bild, quelle],
        tags=["Franzoesisch", "Unite1", "Volet3", v["group"]]))
build(1607392321, "Französisch::Unité 1 – Volet 3 (Vokabeln)", notes, media, "Franzoesisch_Unite1_Volet3_Vokabeln.apkg")

# Paket 2: Wissen / Landeskunde / Grammatik
notes, media = [], []
for i, f in enumerate(FACTS):
    bild, quelle = img(f["image"])
    if f["image"]: media.append(os.path.join(MEDIA, f"fr_{f['image']}.jpg"))
    notes.append(genanki.Note(model=fact_model, guid=genanki.guid_for("wissen", i, f["q"]),
        fields=[f["q"], f["a"], bild, quelle], tags=["Franzoesisch", "Unite1", "Volet3", f["tag"]]))
build(1607392322, "Französisch::Unité 1 – Volet 3 (Wissen & Landeskunde)", notes, media, "Franzoesisch_Unite1_Volet3_Wissen.apkg")
