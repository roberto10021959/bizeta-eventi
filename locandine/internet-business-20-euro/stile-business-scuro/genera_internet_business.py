# -*- coding: utf-8 -*-
"""Locandina Vodafone Business: rete Internet a 20 euro/mese passando la SIM mobile,
15 euro/mese aggiungendo un'utenza luce.

Stile delle grafiche P.IVA di settembre 2026 ("Linea fissa P.IVA", "Luce Business"):
fondo nero con alone rosso, etichetta con barretta rossa, titolo Inter bianco, prezzo rosso
in un riquadro scuro, bottone WhatsApp verde, pillola Fastweb+Vodafone e Bizeta bianco.
Generazione come genera_flat.py: HTML -> Chromium (Playwright), tutti i formati.

    python genera_internet_business.py CARTELLA_LOGHI CARTELLA_USCITA
"""
import asyncio, base64, mimetypes, pathlib, sys

LOGHI = pathlib.Path(sys.argv[1])
USCITA = pathlib.Path(sys.argv[2])
CHROMIUM = "/opt/pw-browsers/chromium"


def incorpora(nome):
    p = LOGHI / nome
    tipo = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{tipo};base64," + base64.b64encode(p.read_bytes()).decode("ascii")


FW_VF = incorpora("Fastweb_+_Vodafone_logo orizzontale.png")
BIZETA = incorpora("_bizeta_bianco_trasparente.png")
WHATSAPP = incorpora("_whatsapp_icona.png")
MODEM = incorpora("modem_scontornato.png")
ROSSO = "#e60000"
VERDE = "#25d366"


def pagina(w, h):
    # misure pensate su 1080 di larghezza; nei formati meno slanciati comanda l'altezza
    s = min(w / 1080.0, h / 1640.0)
    alto = h / w                         # 1.25 post, 1.41 A4, 1.78 storia
    modem_h = (360 if alto < 1.3 else 440 if alto < 1.6 else 520) * s
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
html, body {{ width: {w}px; height: {h}px; overflow: hidden }}
body {{ font-family: "Inter", sans-serif; color: #fff; background: #0b0b0c;
  background-image: radial-gradient(ellipse {900*s}px {700*s}px at 100% 0%, rgba(160,0,0,.55), transparent 70%),
                    radial-gradient(ellipse {700*s}px {500*s}px at 0% 100%, rgba(120,0,0,.25), transparent 70%);
  display: flex; flex-direction: column; padding: {64*s}px {56*s}px {44*s}px; padding-left: {max(56*s, (w - 968*s) / 2)}px;
  padding-right: {max(56*s, (w - 968*s) / 2)}px }}
.etichetta {{ align-self: flex-start; background: rgba(255,255,255,.10); border-radius: {8*s}px;
  padding: {10*s}px {18*s}px; font-size: {24*s}px; font-weight: 700; letter-spacing: {2.4*s}px;
  color: #ddd; display: flex; align-items: center; gap: {12*s}px }}
.etichetta i {{ width: {5*s}px; height: {26*s}px; background: {ROSSO}; display: block }}
.alto {{ display: flex; align-items: flex-end; gap: {20*s}px; margin-top: {34*s}px }}
.titolo {{ flex: 1; font-family: "Inter Display", "Inter", sans-serif; font-weight: 800;
  font-size: {92*s}px; line-height: 1.0; letter-spacing: -{3*s}px }}
.titolo em {{ font-style: normal; color: {ROSSO} }}
.modem {{ height: {modem_h}px; filter: drop-shadow(0 {24*s}px {30*s}px rgba(0,0,0,.7)) }}
.sotto {{ font-size: {38*s}px; line-height: 1.3; color: #c9c9c9; margin-top: {26*s}px }}
.sotto b {{ color: #fff }}
.spazio {{ flex: 1 }}
.riquadro {{ background: #1f1f22; border-radius: {34*s}px; padding: {26*s}px {34*s}px {24*s}px;
  margin-top: {22*s}px; display: flex; align-items: center; gap: {26*s}px }}
.riquadro .testi {{ flex: 1 }}
.piccolo {{ font-size: {23*s}px; font-weight: 600; letter-spacing: {2*s}px; color: #cfcfcf;
  text-transform: uppercase; line-height: 1.3 }}
.prezzo {{ font-family: "Inter Display", "Inter", sans-serif; font-weight: 900; color: {ROSSO};
  font-size: {150*s}px; line-height: .9; letter-spacing: -{6*s}px; margin: {4*s}px 0 {6*s}px }}
.prezzo small {{ font-size: {72*s}px; letter-spacing: -{2*s}px }}
.luce .prezzo {{ color: #ffc900 }}
.icona {{ width: {120*s}px; height: {120*s}px; border-radius: 50%; flex: none;
  display: flex; align-items: center; justify-content: center; font-size: {64*s}px }}
.sim {{ background: rgba(230,0,0,.16) }}
.lampadina {{ background: rgba(255,201,0,.16) }}
.whatsapp {{ align-self: flex-start; background: {VERDE}; border-radius: {16*s}px; margin-top: {30*s}px;
  padding: {16*s}px {28*s}px; display: flex; align-items: center; gap: {16*s}px;
  font-size: {32*s}px; font-weight: 700 }}
.whatsapp img {{ height: {46*s}px }}
.indirizzo {{ font-size: {23*s}px; color: #a8a8a8; margin-top: {26*s}px; padding-bottom: {16*s}px;
  border-bottom: 1px solid rgba(255,255,255,.18) }}
.loghi {{ display: flex; justify-content: space-between; align-items: center; margin-top: {26*s}px }}
.pillola {{ background: #fff; border-radius: 999px; padding: {12*s}px {28*s}px; display: inline-flex }}
.pillola img {{ height: {36*s}px; display: block }}
.bz {{ height: {52*s}px; display: block }}
</style></head><body>
  <div class="etichetta"><i></i>PER CHI HA LA PARTITA IVA</div>
  <div class="alto">
    <div class="titolo">La tua rete Internet a soli <em>20€</em> al mese</div>
    <img class="modem" src="{MODEM}" alt="">
  </div>
  <div class="sotto">se passi a <b>Vodafone Business</b><br>la tua <b>SIM mobile!</b></div>
  <div class="spazio"></div>
  <div class="riquadro">
    <div class="testi">
      <div class="piccolo">Internet + SIM in Vodafone Business</div>
      <div class="prezzo">20 <small>euro</small></div>
      <div class="piccolo">al mese, oltre IVA</div>
    </div>
    <div class="icona sim">&#128241;</div>
  </div>
  <div class="riquadro luce">
    <div class="testi">
      <div class="piccolo">E se attivi anche un'utenza luce</div>
      <div class="prezzo">15 <small>euro</small></div>
      <div class="piccolo">al mese, oltre IVA</div>
    </div>
    <div class="icona lampadina">&#128161;</div>
  </div>
  <div class="whatsapp"><img src="{WHATSAPP}" alt="">Scrivici su WhatsApp&nbsp; 349 177 5024</div>
  <div class="indirizzo">Vodafone Store Cannizzaro &middot; Via T. Cannizzaro 74, Messina</div>
  <div class="loghi">
    <span class="pillola"><img src="{FW_VF}" alt="Fastweb + Vodafone"></span>
    <img class="bz" src="{BIZETA}" alt="Bi Zeta">
  </div>
</body></html>"""


FORMATI = [(" - A4 vetrina", 2480, 3508),
           (" - social 1080x1350", 1080, 1350),
           (" - storia 1080x1920", 1080, 1920)]


async def principale():
    from playwright.async_api import async_playwright
    USCITA.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROMIUM)
        for suffisso, w, h in FORMATI:
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            await pg.set_content(pagina(w, h), wait_until="load")
            await pg.wait_for_timeout(350)
            fuori = USCITA / f"INTERNET BUSINESS 20 EURO{suffisso} - ottobre 2026.png"
            await pg.screenshot(path=str(fuori))
            if "A4" in suffisso:
                await pg.pdf(path=str(fuori.with_suffix(".pdf")), width="210mm", height="297mm",
                             print_background=True,
                             margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            await pg.close()
            print(f" fatto {fuori.name} ({w}x{h})")
        await b.close()


if __name__ == "__main__":
    asyncio.run(principale())
