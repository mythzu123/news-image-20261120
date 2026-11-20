from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
im = Image.new('RGB', (1024, 1024), '#f4eddb')
d = ImageDraw.Draw(im)
INK = '#171714'
RED = '#821f26'
FONT = Path('C:/Windows/Fonts')
adjustments = []

def font(size, bold=False):
    return ImageFont.truetype(str(FONT / ('arialbd.ttf' if bold else 'arial.ttf')), size)

def wrap(text, f, width):
    lines = []
    line = ''
    for word in text.split(' '):
        candidate = line + (' ' if line else '') + word
        if line and d.textlength(candidate, font=f) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    lines.append(line)
    return lines

def text(text, box, size, bold=False, center=False, label=''):
    x, y, w, h = box
    original = size
    while size > 1:
        f = font(size, bold)
        lines = wrap(text, f, w)
        step = size + 4
        if len(lines) * step <= h and all(d.textlength(s, font=f) <= w for s in lines):
            break
        size -= 1
    if size != original:
        adjustments.append(f'{label}: font {original} -> {size} px')
    if len(lines) > 1:
        adjustments.append(f'{label}: {len(lines)} lines')
    for line in lines:
        xx = x + (w - d.textlength(line, font=f)) / 2 if center else x
        d.text((xx, y), line, font=f, fill=INK, stroke_width=0)
        y += step

def header(title, x, y, w, size=17):
    d.rectangle((x, y, x+w, y+31), fill=RED)
    f = font(size, True)
    while d.textlength(title, font=f) > w-16:
        size -= 1
        f = font(size, True)
    d.text((x+8, y+5), title, font=f, fill='#fff8e8')

d.rectangle((18, 18, 1005, 1005), outline=INK, width=2)
text('FRIDAY, NOVEMBER 20, 2026', (32, 29, 960, 22), 16, True, True)
text('THE WORLD TODAY', (30, 51, 964, 91), 89, True, True, 'Masthead')
text('THE STREET EDITION — ALL THE NEWS THAT FIT IN ONE PAGE', (30, 146, 964, 23), 19, True, True)
d.line((30, 181, 994, 181), fill=RED, width=5)

left, right, lw, rw = 32, 651, 598, 341
header('THE LEAD', left, 198, lw)
text('EUROPE RISES, THE WORLD MARCHES', (left, 242, lw, 150), 49, True, label='Lead headline')
text("Coordinated protests swept seven European countries on Friday — over housing, wages, schools and military spending. In Spain, students struck nationwide as a doctors' walkout rolled on. In Tokyo, thousands marched on the Diet against Prime Minister Takaichi.", (left, 407, lw, 217), 25, label='Lead body')

header('WORLD IN BRIEF', right, 198, rw)
brief = [
'ODISHA — Cyclone Akvan made landfall near Gopalpur; 300,000 people were evacuated, with no deaths reported.',
'RIYADH — Houthi missiles damaged the sovereign wealth fund tower in the financial district.',
'GAZA — Israeli troops crossed the ceasefire line in central Gaza, a first since the truce.',
'KENYA — The last Ebola patient went home, 37 days after the first case.',
'SENEGAL — Dozens are missing after a migrant boat capsized off the coast.',
'HAITI — Police said 34 suspected gang members were killed.',
"BRUSSELS — The EU and Britain sealed a post-Brexit 'reset' deal.",
'EL SALVADOR — President Bukele registered to run for a third term.',
"MARKETS — AI doubts dragged world stocks down; Japan's Nikkei fell 4.8%.",
'LAS VEGAS — Russell was fastest as rain washed out practice at the Grand Prix.'
]
heights = [79, 75, 75, 57, 57, 57, 57, 57, 57, 62]
y = 241
for item, h in zip(brief, heights):
    text(item, (right+1, y, rw-2, h-8), 17, label=item.split(' — ')[0])
    y += h
    d.line((right, y-5, right+rw, y-5), fill=RED, width=1)

d.line((640, 198, 640, 878), fill=INK, width=1)
panels = [
('THE HAGUE RULES', 'The World Court found Myanmar committed genocide against the Rohingya — the first such ruling against a state.'),
("'PEACE,' THEY CALLED IT", 'Trump, Xi and Putin held their first three-way summit in Shenzhen and signed a peace declaration. That night, missiles fell on Kyiv, Ukraine hit the Crimean Bridge again, and in Berlin the allies said Europe is ready to talk.'),
('THE PHONES WENT DARK', 'After the Shenzhen summit, US security officials ordered Air Force One reporters to seal the phones they had used in China inside Faraday bags, pool reports said.')
]
for i, (title, body) in enumerate(panels):
    x = left + i*203
    header(title, x, 639, 192, 14)
    text(body, (x+1, 682, 190, 190), 19, label=title)

header('DELETED OVERNIGHT', 32, 888, 960)
text('At COP31 in Antalya, fossil fuels were cut from the draft climate deal amid outcry. In Washington, a new cyber chief was named after a week of outages.', (33, 925, 958, 43), 18, label='Deleted overnight')
d.line((32, 970, 992, 970), fill=RED, width=2)
text("MEANWHILE, IN SMALL PRINT — Anthropic's record IPO closed at $97.17, up 17% on debut. • Fiona, the Cincinnati Zoo's beloved hippo, died after swallowing a visitor's hat.", (33, 977, 958, 25), 16, label='Small print')

im.save(ROOT / 'entry.png', optimize=True)
with Image.open(ROOT / 'entry.png') as check:
    check.verify()
size = (ROOT / 'entry.png').stat().st_size
assert size < 1048576
assert im.size == (1024, 1024)
print(f'PNG: {size} bytes; {im.width} x {im.height}')
print('\n'.join(adjustments))
