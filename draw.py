#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

One-page newspaper, drawn flat with Pillow. No photographs, no network.
48 stories: 3 illustrated leads, 1 navy band, 44 numbered briefs.
Region counts are computed from the data below, so the strip always
adds up to the story total. Saturday events are named as Saturday;
everything else happened, or was first reported, on Sunday 22 Nov 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (249, 245, 237)
INK = (22, 22, 22)
MUTED = (96, 92, 84)
NAVY = (26, 40, 72)
NAVY2 = (44, 62, 102)
RED = (178, 34, 22)
RULE = (182, 174, 158)
TEAL = (16, 118, 108)
GOLD = (214, 162, 42)
SKY = (214, 228, 240)
SEA = (52, 96, 140)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, max_w, leading, color=INK):
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def kicker(d, x, y, text, color, size=18):
    d.text((x, y), text, font=F(SANS_B, size), fill=color)
    return y + size + 6


# (number, region, brief) — region codes: EU ME AS AF NA LA GL
ITEMS = [
    (5, "EU", "Sparta II towed out of Finnish waters on Sunday"),
    (6, "ME", "Bahrain: Iranian strike wounds 2 at industrial site"),
    (7, "ME", "Houthis claim Rabigh refinery, Riyadh radar strikes"),
    (8, "ME", "Two tankers hit mines, ablaze near Strait of Hormuz"),
    (9, "AF", "Khartoum drones hit homes and a UN building; 4 dead"),
    (10, "ME", "Settlers torch cars, homes in West Bank villages"),
    (11, "AF", "Nigeria boat capsizes on way to funeral; 24 drown"),
    (12, "AS", "Java factory search: 3 dead, 36 missing after fire"),
    (13, "AS", "South Korea education minister quits in exam scandal"),
    (14, "AS", "China cuts margin ratio to 80% from 30 November"),
    (15, "AS", "NYT: China spy drive chased AI chips for 2+ years"),
    (16, "NA", "Bessent: US still seeks answers on Nvidia chip sales"),
    (17, "AS", "Taiwan warns Canada over deepening China trade ties"),
    (18, "AS", "Lowy index: US lead over China in Asia narrows"),
    (19, "AS", "Nepal PM Shah heads to India for a 2-day visit"),
    (20, "ME", "Lewis Pugh swims the war-hit Strait of Hormuz"),
    (21, "AF", "Second ship hit off Benghazi on Sunday evening"),
    (22, "EU", "Germany tests kamikaze drones in Lithuania"),
    (23, "EU", "France: 6th weekend of cost-of-living protests"),
    (24, "EU", "Belgium: flights to halt Monday in ATC strike"),
    (25, "EU", "Lisbon march over living costs and wages"),
    (26, "EU", "May 'aghast' at Burnham's EU plans; Tories object"),
    (27, "EU", "UK and EU clinch food and youth-mobility deals"),
    (28, "EU", "Zelensky: Crimea Bridge strikes a 'fair response'"),
    (29, "EU", "Poland: 3 objects in its airspace were Kh-101 missiles"),
    (30, "EU", "Russia welcomes US security offer, revives old demands"),
    (31, "AF", "Insecurity hinders DR Congo Ebola response"),
    (32, "LA", "Brazil storm kills 3, injures 162"),
    (33, "LA", "Burnt vehicles line Sinaloa roads after cartel capture"),
    (34, "NA", "California on alert as biggest waves in years arrive"),
    (35, "NA", "Masked ICE officers detain 2 at Seattle airport"),
    (36, "NA", "FBI probes apparent hack of its crime database"),
    (37, "EU", "Paolo Bulgari, jeweller, dies aged 89"),
    (38, "EU", "Catherine speaks of cancer in new documentary"),
    (39, "EU", "BBC apologises over Strictly noise disruption"),
    (40, "EU", "Liverpool thrash Manchester United 4-0 at Anfield"),
    (41, "NA", "NFL: Lions and Bears both reach 8-2"),
    (42, "NA", "NFL: Bills, Cowboys and Chiefs all win big"),
    (43, "LA", "49ers beat Vikings 35-10 in Mexico City return"),
    (44, "NA", "Skubal agrees record $450m, 9-year Mets deal"),
    (45, "GL", "Global CO2 emissions likely to fall this year"),
    (46, "EU", "Spain: Sanchez ups ante as 29 Nov snap poll nears"),
    (47, "EU", "Dutch FM Berendsen arrives in Delhi for 2-day visit"),
    (48, "AS", "China memory chipmakers gain ground amid US curbs"),
]

REGIONS = [
    ("EU", "EUROPE"),
    ("AS", "ASIA"),
    ("NA", "N. AMERICA"),
    ("ME", "MIDDLE EAST"),
    ("AF", "AFRICA"),
    ("LA", "LATIN AMERICA"),
    ("GL", "GLOBAL"),
]
counts = {code: 0 for code, _ in REGIONS}
for _, code, _ in ITEMS:
    counts[code] += 1
counts["GL"] += 2  # leads 1 (COP31) and 3 (BepiColombo) are global
counts["AF"] += 1  # lead 2 (Merkury, Libya) is Africa
counts["EU"] += 1  # band 4 (Dymer, Ukraine) is Europe
TOTAL = 3 + 1 + len(ITEMS)
assert sum(counts.values()) == TOTAL == 48, (counts, TOTAL)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 40
R = W - M

# --- Masthead ---
d.text((M, 20), "THE WORLD IN ONE PAGE", font=F(SERIF_B, 44), fill=NAVY)
d.text((R, 26), "SUNDAY", font=F(SANS_B, 24), fill=RED, anchor="ra")
d.text((R, 58), "22 NOVEMBER 2026", font=F(SANS_B, 24), fill=INK, anchor="ra")
d.line([M, 98, R, 98], fill=INK, width=4)
d.line([M, 106, R, 106], fill=RULE, width=2)

# --- Stat strip: number above label, so nothing is clipped ---
y = 114
strip = [("48", "STORIES"), ("7", "REGIONS"), ("3", "LEADS"), ("1", "DAY")]
sw = (R - M - 3 * 10) // 4
for i, (num, lab) in enumerate(strip):
    x0 = M + i * (sw + 10)
    d.rectangle([x0, y, x0 + sw, y + 48], outline=RULE, width=2)
    d.text((x0 + sw // 2, y + 2), num, font=F(SERIF_B, 26), fill=RED, anchor="ma")
    d.text((x0 + sw // 2, y + 28), lab, font=F(SANS_B, 14), fill=NAVY, anchor="ma")
y += 56

# --- Lead 1: COP31, text left, flat hall illustration right ---
y = kicker(d, M, y, "1  •  CLIMATE  —  LEAD STORY", RED)
lead_top = y
y = para(d, M, y, "COP31 ends with no deal", F(SERIF_B, 30), 560, 36)
y = para(d, M, y + 2,
         "Antalya talks collapse over fossil fuels: the EU and about "
         "130 parties refuse a draft that never mentions coal, oil or "
         "gas. Guterres is \u201cdeeply disappointed\u201d \u2014 the first "
         "summit with no headline deal since Copenhagen 2009.",
         F(SANS, 18), 560, 23, color=(58, 56, 50))
lead_bot = y
ix0, iy0, ix1, iy1 = 636, lead_top - 2, R, lead_bot
d.rectangle([ix0, iy0, ix1, iy1], fill=SKY, outline=RULE, width=2)
d.rectangle([ix0, iy0, ix1, iy0 + 26], fill=NAVY)
d.text((ix0 + 12, iy0 + 4), "COP31  •  ANTALYA", font=F(SANS_B, 14), fill=(255, 255, 255))
# draft sheet with the missing line
px0, py0, px1, py1 = ix0 + 34, iy0 + 38, ix1 - 34, iy1 - 10
d.rectangle([px0, py0, px1, py1], fill=(255, 255, 255), outline=RULE, width=2)
for j in range(3):
    d.line([px0 + 12, py0 + 16 + j * 14, px1 - 12, py0 + 16 + j * 14], fill=MUTED, width=2)
d.line([px0 + 12, py0 + 58, px1 - 12, py0 + 58], fill=RED, width=3)
d.text((px0 + 12, py0 + 64), "FOSSIL FUELS: —", font=F(SANS_B, 13), fill=RED)
d.rectangle([px1 - 118, py0 + 52, px1 - 10, py0 + 76], outline=RED, width=3)
d.text((px1 - 108, py0 + 57), "NO DEAL", font=F(SANS_B, 15), fill=RED)
y = lead_bot + 6
d.line([M, y, R, y], fill=RULE, width=2)
y += 7

# --- Row B: two illustrated leads ---
by, bh = y, 140
bw = (R - M - 18) // 2
# Lead 2: Merkury
x0 = M
d.rectangle([x0, by, x0 + bw, by + bh], outline=RULE, width=2)
yy = kicker(d, x0 + 12, by + 7, "2  •  LIBYA  —  WAR AT SEA", RED, 15)
yy = para(d, x0 + 12, yy, "Russian warship sunk off Libya",
         F(SANS_B, 19), bw - 148, 24)
para(d, x0 + 12, yy + 1,
     "Corvette Merkury capsizes at Benghazi after a suspected "
     "Ukrainian sea-drone strike; a second ship is hit that "
     "evening.",
     F(SANS, 15), bw - 148, 19, color=(58, 56, 50))
gx0, gy0 = x0 + bw - 132, by + 8
d.rectangle([gx0, gy0, gx0 + 120, gy0 + 122], fill=SEA, outline=RULE, width=1)
for wx in range(gx0 + 6, gx0 + 118, 22):
    d.line([wx, gy0 + 96, wx + 12, gy0 + 96], fill=(255, 255, 255), width=2)
    d.line([wx + 6, gy0 + 108, wx + 18, gy0 + 108], fill=(255, 255, 255), width=2)
d.polygon([(gx0 + 18, gy0 + 78), (gx0 + 102, gy0 + 62),
           (gx0 + 102, gy0 + 76), (gx0 + 18, gy0 + 92)], fill=(70, 70, 70))
d.rectangle([gx0 + 52, gy0 + 40, gx0 + 60, gy0 + 64], fill=(70, 70, 70))
for cx, cy, cr in ((gx0 + 34, gy0 + 26, 9), (gx0 + 48, gy0 + 16, 12), (gx0 + 66, gy0 + 10, 8)):
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(120, 120, 120))
d.rectangle([gx0 + 88, gy0 + 84, gx0 + 104, gy0 + 92], fill=(30, 30, 30))
d.text((gx0 + 8, gy0 + 4), "MERKURY", font=F(SANS_B, 11), fill=(255, 255, 255))
# Lead 3: BepiColombo
x0 = M + bw + 18
d.rectangle([x0, by, x0 + bw, by + bh], outline=RULE, width=2)
yy = kicker(d, x0 + 12, by + 7, "3  •  SPACE  —  MERCURY", TEAL, 15)
yy = para(d, x0 + 12, yy, "Into Mercury orbit — with a glitch",
         F(SANS_B, 19), bw - 148, 24)
para(d, x0 + 12, yy + 1,
     "BepiColombo reaches Mercury after 8 years; ESA reports a "
     "shorter thruster burn. Spacecraft safe.",
     F(SANS, 15), bw - 148, 19, color=(58, 56, 50))
cx0, cy0 = x0 + bw - 132, by + 8
d.rectangle([cx0, cy0, cx0 + 120, cy0 + 122], fill=(16, 20, 38), outline=RULE, width=1)
for sx, sy in ((cx0 + 10, cy0 + 12), (cx0 + 96, cy0 + 18), (cx0 + 22, cy0 + 100), (cx0 + 104, cy0 + 96), (cx0 + 58, cy0 + 8)):
    d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
d.ellipse([cx0 + 62, cy0 + 58, cx0 + 108, cy0 + 104], fill=(226, 140, 60))
for ox, oy, orr in ((cx0 + 74, cy0 + 70, 5), (cx0 + 92, cy0 + 88, 4), (cx0 + 84, cy0 + 66, 3)):
    d.ellipse([ox - orr, oy - orr, ox + orr, oy + orr], fill=(190, 108, 44))
d.rectangle([cx0 + 18, cy0 + 42, cx0 + 30, cy0 + 54], fill=(200, 210, 225))
d.rectangle([cx0 + 6, cy0 + 45, cx0 + 18, cy0 + 51], fill=(70, 120, 200))
d.rectangle([cx0 + 30, cy0 + 45, cx0 + 42, cy0 + 51], fill=(70, 120, 200))
d.text((cx0 + 8, cy0 + 4), "BEPICOLOMBO", font=F(SANS_B, 11), fill=(255, 255, 255))
y = by + bh + 6

# --- Band 4: Dymer ---
d.rectangle([M, y, R, y + 44], fill=NAVY)
d.text((M + 14, y + 3), "4  •  DYMER, UKRAINE: DRONE COLLAPSES 5-STOREY BLOCK",
       font=F(SANS_B, 20), fill=(255, 255, 255))
d.text((M + 14, y + 24),
       "4 killed in the Kyiv region, about 10 feared trapped, 9 evacuated.",
       font=F(SANS, 16), fill=(218, 222, 234))
y += 44 + 5

# --- Region strip (counts computed from the data; no drawn map) ---
d.rectangle([M, y, R, y + 48], fill=NAVY2)
d.text((M + 14, y + 5), "WHERE IT HAPPENED  —  48 STORIES, 7 REGIONS",
       font=F(SANS_B, 16), fill=(255, 255, 255))
count_line = "  •  ".join(
    "%s %d" % (name, counts[code]) for code, name in REGIONS)
d.text((M + 14, y + 27), count_line, font=F(SANS_B, 15), fill=(255, 235, 170))
y += 48 + 5

# --- Timeline ---
d.text((M, y), "THE DAY IN UTC  —  SUNDAY 22 NOVEMBER",
       font=F(SANS_B, 16), fill=RED)
y += 18
tl = [
    ("PRE-DAWN", "Merkury struck at Benghazi"),
    ("03:45 UTC", "BepiColombo orbit confirmed"),
    ("13:35 GMT", "Dymer rescue paused"),
    ("EVENING", "COP31 ends with no deal"),
]
tw = (R - M - 3 * 10) // 4
for i, (when, what) in enumerate(tl):
    x0 = M + i * (tw + 10)
    d.rectangle([x0, y, x0 + tw, y + 40], outline=RULE, width=2)
    d.text((x0 + 10, y + 3), when, font=F(SANS_B, 14), fill=RED)
    d.text((x0 + 10, y + 20), what, font=F(SANS, 13), fill=INK)
y += 40 + 6

# --- Numbered list: items 5-48, two columns ---
d.text((M, y), "THE DAY IN 48  —  CONTINUED",
       font=F(SANS_B, 16), fill=RED)
y += 15
fnum = F(SANS_B, 12)
fitem = F(SANS, 12)
colw = (R - M - 24) // 2
rows = (len(ITEMS) + 1) // 2
for idx, (n, _code, txt) in enumerate(ITEMS):
    col = idx // rows
    row = idx % rows
    x = M + col * (colw + 24)
    yy = y + row * 14
    d.text((x, yy), str(n), font=fnum, fill=RED)
    d.text((x + 26, yy), txt, font=fitem, fill=INK)
y = y + rows * 14 + 5

# --- Footer: DATE CHECK ---
d.rectangle([M, y, R, y + 32], fill=RED)
d.text((M + 14, y + 7),
       "DATE CHECK \u2014 Every story happened, or was first reported, "
       "on Sunday 22 November 2026.",
       font=F(SANS_B, 15), fill=(255, 255, 255))
y = y + 32 + 4
print("layout bottom y =", y, "of", H)
print("region counts:", counts, "total:", TOTAL)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
