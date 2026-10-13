# -*- coding: utf-8 -*-
"""
Locandina A4 Vodafone Business: rete Internet a 20 euro/mese passando la SIM mobile,
15 euro/mese aggiungendo un'utenza luce.

Stile ripreso da locandina_honor600.py e dalle grafiche "Promo Fibra" / "Offerte P.IVA":
titolone giallo Montserrat Black con contorno nero, pill Fastweb+Vodafone, cartellino giallo
inclinato col prezzo, fondo rosso Vodafone col modem, piede con WhatsApp / Bizeta / indirizzo.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REF = sys.argv[1]
OUT = sys.argv[2]

W, H = 2480, 3508                     # A4 a 300 dpi
GIALLO = (255, 198, 0)
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)
ROSSO = (230, 0, 0)
ROSSO_SCURO = (150, 0, 0)


def montserrat(dim, peso=900, corsivo=False):
    nome = "Montserrat-Italic-Variable.ttf" if corsivo else "Montserrat-Variable.ttf"
    f = ImageFont.truetype(os.path.join(REF, nome), dim)
    f.set_variation_by_axes([peso])
    return f


def ombra_sotto(base, img, xy, sfoc=18, opacita=0.45, spost=(0, 18)):
    a = img.getchannel("A").filter(ImageFilter.GaussianBlur(sfoc))
    o = Image.new("RGBA", img.size, (0, 0, 0, 0))
    o.putalpha(a.point(lambda v: int(v * opacita)))
    base.alpha_composite(o, (xy[0] + spost[0], xy[1] + spost[1]))


def sfondo():
    """Rosso Vodafone con luce radiale e bolle sfocate (come le grafiche P.IVA)."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W * 0.62) / W) ** 2 + ((y - H * 0.40) / H) ** 2)
    t = np.clip(d / 0.75, 0, 1)[..., None]
    c1, c2 = np.array([238, 18, 18], np.float32), np.array([128, 0, 0], np.float32)
    img = Image.fromarray((c1 * (1 - t) + c2 * t).astype(np.uint8), "RGB").convert("RGBA")
    bolle = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bolle)
    for cx, cy, r, a in ((180, 1350, 260, 40), (2350, 900, 340, 32), (2150, 2350, 200, 36),
                         (420, 2450, 140, 30), (1250, 1020, 90, 26), (2380, 1650, 110, 28)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 120, a))
    img.alpha_composite(bolle.filter(ImageFilter.GaussianBlur(14)))
    return img


def modem():
    """Modem Vodafone scontornato dal fondo rosso della grafica 'Internet Unlimited'."""
    src = Image.open(os.path.join(REF, "InternetUnlimitedVodafone.webp")).convert("RGB")
    a = np.asarray(src.crop((1650, 330, 2160, 1350))).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    rossezza = r - np.maximum(g, b)                 # alto sul fondo rosso, ~0 sul modem grigio
    alpha = np.clip((55 - rossezza) * 7, 0, 255).astype(np.uint8)
    m = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
    img = Image.fromarray(a.astype(np.uint8), "RGB").convert("RGBA")
    # despill: toglie l'alone rosso sui bordi
    arr = np.asarray(img).copy()
    grigio = arr[..., 1:3].max(axis=2)
    arr[..., 0] = np.minimum(arr[..., 0], grigio + 12)
    img = Image.fromarray(arr, "RGBA")
    img.putalpha(m)
    return img.crop(m.point(lambda v: 255 if v > 40 else 0).getbbox())


def sim(larg):
    """SIM stilizzata bianca con chip dorato e logo Vodafone."""
    h = int(larg * 1.32)
    s = 4
    im = Image.new("RGBA", (larg * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    L, Hh, ang = larg * s, h * s, int(larg * s * 0.24)
    d.polygon([(0, 0), (L - ang, 0), (L, ang), (L, Hh), (0, Hh)], fill=BIANCO)
    cw, ch = int(L * 0.46), int(L * 0.38)
    cx, cy = int(L * 0.27), int(Hh * 0.52)
    d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=int(L * 0.05), fill=(214, 175, 70))
    for i in (1, 2):
        d.line([(cx, cy + ch * i // 3), (cx + cw, cy + ch * i // 3)], fill=(160, 120, 30), width=s * 3)
    d.line([(cx + cw // 2, cy), (cx + cw // 2, cy + ch)], fill=(160, 120, 30), width=s * 3)
    # logo Vodafone vero, ritagliato dalla pill Fastweb+Vodafone
    src = Image.open(os.path.join(REF, "logo fastweb + vodafone chiaro.webp")).convert("RGBA")
    vf = src.crop((684, 452, 756, 524))
    m = Image.new("L", vf.size, 0)
    ImageDraw.Draw(m).ellipse([1, 1, vf.width - 2, vf.height - 2], fill=255)
    vf.putalpha(m)
    r = int(L * 0.40)
    vf = vf.resize((r, r), Image.LANCZOS)
    im.alpha_composite(vf, (int(L * 0.10), int(Hh * 0.10)))
    return im.resize((larg, h), Image.LANCZOS)


def lampadina(dim):
    s = 4
    D = dim * s
    im = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([D * 0.18, D * 0.04, D * 0.82, D * 0.66], fill=GIALLO, outline=NERO, width=6 * s)
    d.polygon([(D * 0.32, D * 0.56), (D * 0.68, D * 0.56), (D * 0.62, D * 0.74), (D * 0.38, D * 0.74)],
              fill=GIALLO)
    d.line([(D * 0.30, D * 0.58), (D * 0.38, D * 0.74)], fill=NERO, width=6 * s)
    d.line([(D * 0.70, D * 0.58), (D * 0.62, D * 0.74)], fill=NERO, width=6 * s)
    for i, y in enumerate((0.76, 0.83, 0.90)):
        w = 0.25 - i * 0.03
        d.rounded_rectangle([D * (0.5 - w), D * y, D * (0.5 + w), D * (y + 0.05)], radius=D * 0.02,
                            fill=(90, 90, 90))
    return im.resize((dim, dim), Image.LANCZOS)


def cartellino(base, cx, cy):
    """Cartellino giallo inclinato stile 'Saldi Vodafone' con il prezzo grande."""
    lw, lh = 1500, 700
    tag = Image.new("RGBA", (lw + 260, lh + 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(tag)
    ox, oy, sk = 130, 130, 110
    d.polygon([(ox + sk, oy), (ox + lw, oy), (ox + lw - sk, oy + lh), (ox, oy + lh)], fill=GIALLO)
    d.text((ox + 150, oy + 120), "a soli", font=montserrat(110, 800, True), fill=NERO, anchor="lm")
    d.text((ox + lw / 2 - 10, oy + 375), "20€", font=montserrat(470, 900, True),
           fill=NERO, anchor="mm", stroke_width=12, stroke_fill=BIANCO)
    d.text((ox + lw - 200, oy + lh - 85), "al mese", font=montserrat(105, 800, True), fill=NERO, anchor="rm")
    tag = tag.rotate(5, resample=Image.BICUBIC)
    xy = (int(cx - tag.width / 2), int(cy - tag.height / 2))
    ombra_sotto(base, tag, xy, 18, 0.45, (12, 18))
    base.alpha_composite(tag, xy)


def pill_fastweb_vodafone(larg):
    src = Image.open(os.path.join(REF, "logo fastweb + vodafone chiaro.webp")).convert("RGBA")
    pill = src.crop((262, 414, 1014, 566))
    m = Image.new("L", pill.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([2, 2, pill.width - 3, pill.height - 3], pill.height // 2, fill=255)
    pill.putalpha(m)
    return pill.resize((larg, int(pill.height * larg / pill.width)), Image.LANCZOS)


def bizeta(larg):
    src = Image.open(os.path.join(REF, "Logo bi Zeta.jpg")).convert("RGB")
    a = np.asarray(src)
    minimo = Image.fromarray(a.min(axis=2))
    alpha = Image.eval(minimo, lambda v: min(255, int((255 - v) * 1.2)))
    logo = src.convert("RGBA")
    logo.putalpha(alpha)
    logo = logo.crop(alpha.point(lambda v: 255 if v > 40 else 0).getbbox())
    return logo.resize((larg, int(logo.height * larg / logo.width)), Image.LANCZOS)


def testo_centrato_contornato(d, xy, testo, font, fill, stroke, ombra=14):
    d.text((xy[0] + ombra, xy[1] + ombra), testo, font=font, fill=NERO, anchor="mm",
           stroke_width=stroke, stroke_fill=NERO)
    d.text(xy, testo, font=font, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=NERO)


def main():
    img = sfondo()
    d = ImageDraw.Draw(img)

    # --- pill + titolo -----------------------------------------------------------------
    pill = pill_fastweb_vodafone(1150)
    ombra_sotto(img, pill, ((W - pill.width) // 2, 120), 14, 0.35, (0, 12))
    img.alpha_composite(pill, ((W - pill.width) // 2, 120))

    ft = montserrat(205, 900)
    for y, riga in ((470, "LA TUA RETE"), (690, "INTERNET")):
        testo_centrato_contornato(d, (W / 2, y), riga, ft, GIALLO, 16)

    # --- modem + SIM + cartellino ------------------------------------------------------
    mo = modem()
    mo = mo.resize((int(mo.width * 1150 / mo.height), 1150), Image.LANCZOS)
    mxy = (W - mo.width - 150, 820)
    terra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gy = mxy[1] + mo.height
    ImageDraw.Draw(terra).ellipse([mxy[0] - 60, gy - 45, mxy[0] + mo.width + 60, gy + 45], fill=(60, 0, 0, 170))
    img.alpha_composite(terra.filter(ImageFilter.GaussianBlur(25)))
    ombra_sotto(img, mo, mxy, 30, 0.40, (-20, 20))
    img.alpha_composite(mo, mxy)

    sm = sim(300).rotate(-12, resample=Image.BICUBIC, expand=True)
    sxy = (mxy[0] - 250, 1540)
    ombra_sotto(img, sm, sxy, 20, 0.45, (10, 20))
    img.alpha_composite(sm, sxy)

    cartellino(img, 800, 1260)

    # --- condizione ---------------------------------------------------------------------
    d = ImageDraw.Draw(img)
    fs = montserrat(118, 800)
    for y, riga in ((2080, "se passi a Vodafone Business"), (2225, "la tua SIM mobile!")):
        d.text((W / 2 + 6, y + 8), riga, font=fs, fill=(90, 0, 0), anchor="mm")
        d.text((W / 2, y), riga, font=fs, fill=BIANCO, anchor="mm")

    # --- nota luce: box bianco con lampadina -----------------------------------------
    bx0, by0, bx1, by1 = 170, 2370, W - 170, 2910
    box = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle([bx0, by0, bx1, by1], radius=60, fill=BIANCO)
    ombra = box.getchannel("A").filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.4))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(ombra)
    img.alpha_composite(sh, (0, 18))
    img.alpha_composite(box)
    lb = lampadina(380)
    img.alpha_composite(lb, (bx0 + 40, (by0 + by1) // 2 - 200))
    d = ImageDraw.Draw(img)
    tx = bx0 + 450
    d.text((tx, by0 + 120), "E se attivi anche", font=montserrat(92, 700), fill=NERO, anchor="lm")
    d.text((tx, by0 + 225), "un'utenza LUCE", font=montserrat(92, 900), fill=ROSSO, anchor="lm")
    d.text((tx, by0 + 330), "il prezzo scende a soli", font=montserrat(92, 700), fill=NERO, anchor="lm")
    d.text((tx, by0 + 445), "15€ al mese", font=montserrat(160, 900, True), fill=ROSSO, anchor="lm")

    # --- piede bianco (stile 'Saldi Estate') -------------------------------------------
    fy0 = 3020
    d.rectangle([0, fy0, W, H], fill=BIANCO)
    d.rectangle([0, fy0, W, fy0 + 16], fill=GIALLO)
    fy = 3250
    wa = Image.open(os.path.join(REF, "_whatsapp_icona.png")).convert("RGBA").resize((170, 170), Image.LANCZOS)
    img.alpha_composite(wa, (80, fy - 50))
    fp = montserrat(64, 800)
    d.text((280, fy - 40), "Contattaci su", font=fp, fill=NERO, anchor="lm")
    d.text((280, fy + 40), "WhatsApp:", font=fp, fill=NERO, anchor="lm")
    d.text((280, fy + 125), "349/1775024", font=montserrat(70, 900), fill=NERO, anchor="lm")

    biz = bizeta(640)
    img.alpha_composite(biz, ((W - biz.width) // 2, fy - 70))
    d.text((W / 2, fy + 150), "Vodafone Store Cannizzaro", font=montserrat(54, 700), fill=NERO, anchor="mm")

    pin = Image.open(os.path.join(REF, "icona luogo.png")).convert("RGBA")
    pin = pin.resize((130, 130), Image.LANCZOS)
    img.alpha_composite(pin, (1610, fy - 25))
    fi = montserrat(56, 800)
    for i, riga in enumerate(("Vieni a trovarci:", "Via T. Cannizzaro 74", "Messina")):
        d.text((1765, fy - 40 + i * 80), riga, font=fi, fill=NERO, anchor="lm")

    os.makedirs(OUT, exist_ok=True)
    rgb = img.convert("RGB")
    base = os.path.join(OUT, "Locandina A4 Internet Business 20 euro")
    rgb.save(base + ".png")
    rgb.save(base + ".pdf", resolution=300)
    rgb.resize((1240, 1754), Image.LANCZOS).save(base + " per WhatsApp.jpg", quality=90)
    print(base)


if __name__ == "__main__":
    main()
