#!/usr/bin/env python3
"""Render the make.fun news-image entry for 26 Nov 2026.

Magazine cover: "THANKSGIVING AT THE WORLD'S TABLE".
Layout: 1024x1024, cream page, date masthead in Playfair Display,
cover photo, 8 feature tiles with photos, ALSO ON TODAY strip (16 items),
red footer band. Deterministic: same input -> same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

CREAM = (246, 241, 231)
INK = (26, 26, 26)
MUTED = (90, 82, 72)
ORANGE = (196, 85, 45)
DEEPRED = (166, 58, 42)
GOLD = (217, 142, 31)
RULE = (196, 85, 45)
CAPTION_BG = (232, 222, 205)
TILE_BG = (255, 253, 247)

PLAYFAIR = os.path.join(HERE, "fonts", "PlayfairDisplay.ttf")
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def crop_fill(im, tw, th):
    """Center-crop image to fill tw x th exactly."""
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return im.crop((x, y, x + tw, y + th))


def main():
    page = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(page)

    # --- top accent bar -------------------------------------------------
    d.rectangle([0, 0, W, 8], fill=ORANGE)
    d.rectangle([0, 8, W, 10], fill=GOLD)

    # --- masthead: the date, big and centred ---------------------------
    f_date = font(PLAYFAIR, 48)
    date_txt = "THURSDAY 26 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=f_date)
    d.text(((W - dw) / 2, 16), date_txt, font=f_date, fill=INK)

    # hairline rule under the date
    d.rectangle([24, 78, W - 24, 80], fill=RULE)

    # --- title below the date -------------------------------------------
    f_title = font(PLAYFAIR, 33)
    title_txt = "THANKSGIVING AT THE WORLD'S TABLE"
    tw = d.textlength(title_txt, font=f_title)
    d.text(((W - tw) / 2, 88), title_txt, font=f_title, fill=DEEPRED)

    # --- subtitle --------------------------------------------------------
    f_sub = font(SERIF, 16)
    sub_txt = "The priciest feast in years \u2014 and the tariff storm behind the bill"
    sw = d.textlength(sub_txt, font=f_sub)
    d.text(((W - sw) / 2, 132), sub_txt, font=f_sub, fill=MUTED)

    # timing-honesty note
    f_note = font(SANS, 11)
    note_txt = "\u25c6 broke late Wednesday 25 November and leads today's coverage"
    nw = d.textlength(note_txt, font=f_note)
    d.text(((W - nw) / 2, 154), note_txt, font=f_note, fill=ORANGE)

    # --- cover photo ------------------------------------------------------
    cover = Image.open(os.path.join(HERE, "photos", "cover.jpg")).convert("RGB")
    cover = crop_fill(cover, W, 200)
    page.paste(cover, (0, 176))
    # thin gold rule under cover
    d.rectangle([0, 376, W, 379], fill=GOLD)

    # cover caption bar
    d.rectangle([0, 379, W, 413], fill=CAPTION_BG)
    f_cap = font(SANS, 12)
    cap_lines = [
        "Carving the turkey at a family Thanksgiving dinner. This year's feast costs 11% more",
        "than last year's \u2014 turkey +26%, macaroni +40.2%, green beans +36.7%. Photo: Wikimedia Commons, CC BY 2.0",
    ]
    cy = 383
    for line in cap_lines:
        d.text((24, cy), line, font=f_cap, fill=INK)
        cy += 15

    # --- features header --------------------------------------------------
    f_sect = font(SANS_B, 14)
    d.text((24, 424), "THE DAY IN EIGHT STORIES", font=f_sect, fill=DEEPRED)
    d.rectangle([24, 444, W - 24, 446], fill=RULE)

    # --- 8 feature tiles, 4 x 2 -------------------------------------------
    features = [
        ("photos/trump.jpg", "TARIFF SHOCKWAVE \u25c6",
         "Trump hits 14 partners with new tariffs",
         "China 20%, EU 15%, Indonesia 18% \u2014 proposed Wed; hearings 25 Jan."),
        ("photos/netanyahu.jpg", "NETANYAHU TRIAL \u25c6",
         "Judges urge: drop the bribery charge",
         "Jerusalem court says Case 4000 faces \u2018considerable difficulties\u2019."),
        ("photos/pyongyang.jpg", "PYONGYANG EXPELS ENVOY \u25c6",
         "North Korea kicks out Swiss diplomat",
         "Sylvain Astier persona non grata, 48 hours to leave; office shut."),
        ("photos/giza.jpg", "GIZA RING-ROAD FIRE \u25c6",
         "Fuel tanker fire kills at least 31",
         "Tanker overturns above Tunnel 10 in al-Warraq; 21 injured."),
        ("photos/macys.jpg", "PARADE IN THE RAIN \u25c6",
         "Macy's parade pushed to Saturday",
         "The 100th parade is postponed by storm \u2014 a first."),
        ("photos/nyse.jpg", "MARKETS IN FREEFALL \u25c6",
         "Nasdaq flirts with bear market",
         "Down 2% Wednesday, ~20% off its October record; VIX +60% in Nov."),
        ("photos/refinery.jpg", "OIL UNDER FIRE \u25c6",
         "Houthis hit Saudi Arabia's refinery",
         "Brent $94.71 as ships strike mines in Hormuz; OPEC+ meets 29 Nov."),
        ("photos/cessna.jpg", "PLANE DOWN IN MISSISSIPPI \u25c6",
         "Six dead in Gulf crash",
         "Cessna 210 down near Horn Island; two families lost, boys 10 and 12."),
    ]
    margin, gap = 24, 12
    tile_w = (W - 2 * margin - 3 * gap) // 4
    tile_h = 140
    photo_h = 64
    f_kick = font(SANS_B, 11)
    f_head = font(SANS_B, 13)
    f_desc = font(SANS, 11)
    ty0 = 454
    for i, (img, kicker, head, desc) in enumerate(features):
        col, row = i % 4, i // 4
        x0 = margin + col * (tile_w + gap)
        y0 = ty0 + row * (tile_h + 8)
        # tile background
        d.rectangle([x0, y0, x0 + tile_w, y0 + tile_h], fill=TILE_BG)
        d.rectangle([x0, y0, x0 + tile_w, y0 + tile_h], outline=(214, 204, 188), width=1)
        # photo
        ph = Image.open(os.path.join(HERE, img)).convert("RGB")
        ph = crop_fill(ph, tile_w, photo_h)
        page.paste(ph, (x0, y0))
        # kicker
        d.text((x0 + 6, y0 + photo_h + 3), kicker, font=f_kick, fill=ORANGE)
        # headline (max 2 lines)
        hl = wrap(d, head, f_head, tile_w - 12)
        hy = y0 + photo_h + 18
        for line in hl[:2]:
            d.text((x0 + 6, hy), line, font=f_head, fill=INK)
            hy += 15
        # description (max 2 lines)
        dl = wrap(d, desc, f_desc, tile_w - 12)
        dy = hy + 2
        for line in dl[:2]:
            d.text((x0 + 6, dy), line, font=f_desc, fill=MUTED)
            dy += 13

    # --- ALSO ON TODAY ----------------------------------------------------
    ay0 = ty0 + 2 * (tile_h + 8) + 6
    d.text((24, ay0), "ALSO ON TODAY", font=f_sect, fill=DEEPRED)
    d.rectangle([24, ay0 + 20, W - 24, ay0 + 22], fill=RULE)

    also = [
        ("CHINA 20%", "Beijing's rate is capped at 20% \u2014 or 40% if the tariff truce fails."),
        ("EUROPE 15%", "The EU faces 15% under the new Section 301 tariff plan."),
        ("INDONESIA 18%", "Jakarta is hit with 18% in the 14-partner sweep."),
        ("INDIA 17\u201325%", "New Delhi at 17%, or 25% if no deal is struck."),
        ("VIETNAM 20\u201335%", "Hanoi at 20%, rising to 35% without a deal."),
        ("CASE 2000", "Judges say reconsider the second Netanyahu case too."),
        ("CASE 1000", "The court seeks a deal in the gifts case."),
        ("AG TO REVIEW", "Attorney General Baharav-Miara will weigh the judges' advice."),
        ("SONGDOWON", "The expulsion is payback for Swiss sanctions on a children's camp."),
        ("LIBYA THREAT", "Libyan forces vow retaliation after the Merkury sinking."),
        ("GAZA STRAIN", "Two Hamas security chiefs killed in 24 hours; the truce wobbles."),
        ("DOLLAR STEADY", "Greenback flat at 103.7; the 10-year yield hits a 2\u00bd-month low."),
        ("OPEC+ MEETS", "Ministers gather 29 Nov to set 2027 output policy."),
        ("GROCERS FIGHT BACK", "Walmart's $35 feast for 10 undercuts last year; Lidl $33.56."),
        ("TURKEYS PARDONED", "Trump spares Freedom and Feathers from the table."),
        ("COAST STORM", "The East Coast braces for rain and strong winds on the holiday."),
    ]
    f_ak = font(SANS_B, 11)
    f_ad = font(SANS, 11)
    col_w = (W - 2 * margin - 16) // 2
    row_h = 25
    ay = ay0 + 26
    for i, (kick, desc) in enumerate(also):
        col, row = i % 2, i // 2
        x0 = margin + col * (col_w + 16)
        y0 = ay + row * row_h
        d.text((x0, y0), kick + " \u2014", font=f_ak, fill=DEEPRED)
        kw = d.textlength(kick + " \u2014 ", font=f_ak)
        dl = wrap(d, desc, f_ad, col_w - kw - 4)
        d.text((x0 + kw, y0), dl[0] if dl else "", font=f_ad, fill=INK)
        if len(dl) > 1:
            d.text((x0, y0 + 12), dl[1], font=f_ad, fill=INK)

    # --- footer band --------------------------------------------------------
    fy = H - 30
    d.rectangle([0, fy, W, H], fill=DEEPRED)
    f_foot = font(SANS_B, 12)
    foot = "THURSDAY 26 NOVEMBER 2026  \u2022  24 STORIES FROM AROUND THE WORLD  \u2022  THANKSGIVING AT THE WORLD'S TABLE"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, fy + 8), foot, font=f_foot, fill=(255, 253, 247))

    page.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
