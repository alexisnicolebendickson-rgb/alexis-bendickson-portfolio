#!/usr/bin/env python3
"""Build round-1 Studio Work galleries into photography.html.
Copies keeper images (resized to max 1600px, q82) into assets/img/ and
inserts gallery sections before the 'Personal work / Beginnings' section.
Also appends 10 iCloud Homecoming photos to the Homecoming grid.
Idempotent-ish: refuses to run if studio sections already present.
"""
import os, re, sys, glob
from PIL import Image

REPO = os.path.expanduser('~/workspace/portfolio-rebuild')
ORG = os.path.expanduser('~/workspace/user/media_library/portfolio-business-best/facebook-picks-organized')
ICLOUD = os.path.expanduser('~/workspace/user/media_library/portfolio-business-best')
IMG = os.path.join(REPO, 'assets/img')
HTML = os.path.join(REPO, 'photography.html')

def find(folder, code):
    hits = glob.glob(os.path.join(ORG, folder, code + '_*.jpg')) + \
           glob.glob(os.path.join(ORG, folder, code + '*.jpg'))
    hits = [h for h in hits if not os.path.basename(h).startswith(code + 'A_')]
    if code.endswith('A'):
        hits = glob.glob(os.path.join(ORG, folder, code + '_*.jpg'))
    assert len(hits) >= 1, f'{folder}/{code}: {hits}'
    # prefer exact code_ match
    exact = [h for h in hits if os.path.basename(h).startswith(code + '_')]
    return (exact or hits)[0]

def process(src, dst):
    im = Image.open(src).convert('RGB')
    im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(dst, 'JPEG', quality=82, optimize=True, progressive=True)
    return im.size

# gallery: (folder, slug, kicker, title, sub, [(code, alt), ...])
G = []
def gal(folder, slug, title, sub, items):
    G.append((folder, slug, title, sub, items))

gal('Weddings', 'weddings', 'Weddings',
    'Full wedding days — ceremonies, details, and the people in between.',
    [('W01','bride profile with updo detail'),('W02','bride and bridesmaids laughing with bouquets'),
     ('W03','couple kiss through purple flowers'),('W04','white bouquet detail on a table'),
     ('W05','black and white groomsmen group portrait'),('W06','bride laughing with coral bridesmaids, lakeside'),
     ('W07',"bridesmaids' feet and bouquets detail"),('W08','full wedding party by columns, wide'),
     ('W09','couple waterfall embrace'),('W10','pink lily bouquet and silver shoes detail'),
     ('W11','couple walking under a draped arch'),('W12','black and white ceremony vows, close'),
     ('W13','ring and pink-and-white bouquet detail'),('W14','couple at a stone arch'),
     ('W15','black and white couple at a stone arch'),('W17','tiered wedding cake with autumn leaves'),
     ('W18','hands and rings, close'),('W19','black and white couple silhouette'),
     ('W20','couple portrait in red and black'),('W21','flower girl and ring bearer'),
     ('W22','black and white wedding party on a bridge'),('W23','black and white ceremony in a field'),
     ('W24','couple exchanging vows, close'),('W25','bouquet detail'),
     ('W26','couple kiss with groomsmen'),('W27','black and white bride with a young boy'),
     ('W28',"couple's vows at the altar"),('W29','ceremony under stained glass'),
     ('W30','black and white first kiss')])

gal('Maternity', 'maternity', 'Maternity',
    'Expecting, in fields, water, and late light.',
    [('M01','couple lakeside picnic in golden light'),('M02','mother standing in water in a pink dress'),
     ('M03','couple close, partner kissing her head'),('M04','couple laughing on stone stairs'),
     ('M05','sunset silhouette with sunflowers'),('M06','black and white belly portrait with sunflowers'),
     ('M07','golden field, wide'),('M08','belly with dog tags detail'),
     ('M09','partner kissing her belly'),('M10','belly and hands, close'),
     ('M11','couple kiss'),('M12','partner belly kiss, close'),
     ('M13','couple seated in a field'),('M14','partner holding an ultrasound photo, close'),
     ('M15','belly with a teal ribbon, close'),('M16','mother among blossoms'),
     ('M17','black and white couple on a bridge'),('M18','mother and child, backlit'),
     ('M19','black and white family of three'),('M20','mother smiling by a tree'),
     ('M21','black and white belly, close'),('M23','black and white family at the falls'),
     ('M24','mother seated on a blanket in a field'),('M25','mother and child by a tree')])

gal('Newborn', 'newborn', 'Newborn & birth',
    'First days — birth stories, fresh-48 sessions, and first birthdays.',
    [('N01','patterned socks detail, close'),('N02','draped labor portrait, wide'),
     ('N03','partner supporting labor, wide'),('N04','newborn with a pink bow, wrapped, close'),
     ('N05','black and white bassinet, wide'),('N06','tiny feet detail, close'),
     ('N07','newborn with a headband, close'),('N08','black and white newborn, close'),
     ('N09','newborn with a floral headband, close'),('N10','mother and child by a tree, wide'),
     ('N11','child crawling in leaves, wide')])

gal('Engagement', 'engagement', 'Engagement & couples',
    'Engagements and couple sessions, mostly outdoors, mostly laughing.',
    [('E01','couple dip at a sunset lakeshore'),('E02','couple on a dock, wide'),
     ('E03','couple lying in grass, close'),('E04','couple close, laughing'),
     ('E05','family trio laughing'),('E06','black and white trio'),
     ('E07','sunlit family in a field'),('E08','couple close, smiling'),
     ('E09','boots with a 2014 date detail'),('E10','black and white couple walking away'),
     ('E11','couple under an autumn tree, wide'),('E12','couple kiss, close'),
     ('E13','black and white couple by a lake'),('E14','ring on stone, close'),
     ('E15','couple at sunset in a yellow wrap, wide'),('E16','hands and lace detail, close'),
     ('E17','black and white couple on a bridge'),('E18','couple laughing in a field, wide'),
     ('E19','couple reclining on rocks, wide'),('E20','black and white couple kiss, close'),
     ('E21','couple on a bridge, wide'),('E22','ring on wood detail'),
     ('E23','ring and flower detail'),('E24','couple by a cabin, wide'),
     ('E27','couple reclining on rocks, wide'),('E28','black and white couple on rocks'),
     ('E33','couple sharing a milkshake, close')])

gal('Seniors', 'seniors', 'Seniors',
    'Senior portraits — fields, waterfalls, brick walls, and guitars.',
    [('S01','graduation cap, close'),('S02','seated on stairs, wide'),
     ('S03','sunflower portrait, close'),('S04','colorful outfit against a brick wall, wide'),
     ('S05','sitting on a bridge, wide'),('S06','fountain, wide'),
     ('S07','black and white brick portrait, close'),('S08','sitting in a field, wide'),
     ('S09','portrait with crossed arms, close'),('S10','black and white back tattoo, close'),
     ('S11','train portrait, close'),('S12','field portrait in denim, wide'),
     ('S13','black and white portrait, close'),('S14','waterfall crouch, wide'),
     ('S15','black and white waterfall sitting'),('S16','waterfall sitting, wide'),
     ('S17','waterfall portrait, close'),('S18','field portrait with a friend, wide'),
     ('S19','wooded path, wide'),('S20','plaid by a red door, close'),
     ('S21','field portrait in a cardigan, wide'),('S22','sitting in a field, wide'),
     ('S23','black and white standing on a beach, wide'),('S24','guitar by a stone wall, wide'),
     ('S25','black and white guitar portrait'),('S26','sitting against a wall, wide'),
     ('S27','hoodie portrait, close')])

gal('Family', 'family', 'Family',
    'Families as they are — autumn light, tulips, and one very patient dog.',
    [('F01','couple kiss in autumn, wide'),('F02','girl reading under a tree, wide'),
     ('F03','black and white couple kiss, close'),('F04','sisters laughing, close'),
     ('F05','couple kiss, close'),('F06','mother, baby and dog, wide'),
     ('F07','large family portrait, wide'),('F08','mother with children, wide'),
     ('F09',"black and white boy's portrait, close"),
     ('E25','mother smiling among blossoms, close'),
     ('E26','mother and son on a blanket among tulips, wide'),
     ('E29','child in a Santa hat, close'),
     ('E30','child holding a "Happy Holidays" sign, wide'),
     ('E31','boy with an Olaf snowman, wide'),
     ('E32','black and white mother and son, close')])
# stowaway sources live in the Engagement folder
STOW = {'E25','E26','E29','E30','E31','E32'}

gal('Minis', 'minis', 'Mini sessions',
    'Fall and Valentine minis — short sessions, small people, big expressions.',
    [('MI01','girl with a pink flower crown, close'),('MI02','children kissing their dad, wide'),
     ('MI03','couple on an autumn path, wide'),('MI04','black and white mother and child, close'),
     ('MI05','toddler on hay, wide'),('MI06','toddler with a pumpkin, close'),
     ('MI07',"black and white girl's portrait, close"),('MI08','family on a blanket, wide'),
     ('MI09','dad lifting a boy, wide'),('MI10','boy in camo, close'),
     ('MI11','boy with a heart frame, close'),('MI12','two boys at an XO stand, wide'),
     ('MI13','boy at columns, wide'),('MI14','mother and boy on a bridge, wide')])

gal('Fashion', 'fashion', 'Fashion & portrait',
    'Styled portrait work — color, brick, graffiti, and red backdrops.',
    [('P01','black and white portrait, close'),('P02','navy dress, wide'),
     ('P03','red backdrop, wide'),('P04','color portrait, close'),
     ('P05','graffiti wall, wide'),('P06','brick portrait, close'),
     ('P07','field portrait, wide'),('P08','cap by a gate, wide'),
     ('P09','cap portrait, close'),('P10','sitting by shutters, wide')])

gal('Empowerment', 'empowerment', 'Empowerment',
    'Boudoir and pin-up, kept tasteful — robes, window light, shadow, and confidence.',
    [('B01','white robe by a window, wide'),('B02','black and white robe by a window, close'),
     ('B03','bed portrait, close'),('B04','burgundy dress, seated, wide'),
     ('B05','over-shoulder portrait with pearls, close'),('B06','black and white robe and window portrait, close'),
     ('B07','green dress on a rooftop, wide'),('B08','robe on a turquoise chair, wide'),
     ('B09','pink-hair portrait, close'),('B10','over-shoulder portrait in a white top, close'),
     ('B11','smiling portrait in a white top, close'),('B12','black and white smiling portrait, close'),
     ('B13','gold top standing in a field, wide'),('B14','black and white portrait in a white top by a creek, close')])

html = open(HTML).read()
if 'studio-weddings-01' in html:
    sys.exit('Studio galleries already present — aborting.')

sections = []
sections.append('''      <section class="block tight">
        <p class="kicker">Studio work</p>
        <h2 class="section-title">The studio years</h2>
        <p class="section-sub">From the studio years, 2014–2018 — weddings, maternity, newborns, seniors, families, and empowerment sessions for more than 200 clients across Missouri and Kansas.</p>
      </section>''')

total = 0
for folder, slug, title, sub, items in G:
    figs = []
    for i, (code, alt) in enumerate(items, 1):
        srcfolder = 'Engagement' if code in STOW else folder
        src = find(srcfolder, code)
        name = f'studio-{slug}-{i:02d}.jpg'
        process(src, os.path.join(IMG, name))
        label = title.split(' &')[0]
        figs.append(f'          <figure><img src="assets/img/{name}" alt="{label}: {alt}" loading="lazy" /></figure>')
        total += 1
    sections.append(f'''      <section class="block tight">
        <p class="kicker">Studio work</p>
        <h2 class="section-title">{title}</h2>
        <p class="section-sub">{sub}</p>
        <div class="photo-grid">
{chr(10).join(figs)}
        </div>
      </section>''')

block = '\n\n'.join(sections) + '\n\n'
anchor = '''      <section class="block tight">
        <p class="kicker">Personal work</p>'''
assert anchor in html
html = html.replace(anchor, block + anchor, 1)

# Homecoming additions (iCloud, Oct 2023 session) — friend-solo closeup held out
HC = [
    ('studio-2023-woods-fullbody.jpg', 'Lillia and a friend in the woods, full-length homecoming portrait'),
    ('studio-2023-woods-closeup.jpg', 'Lillia and a friend in the woods, close homecoming portrait'),
    ('studio-2023-dock-bw.jpg', 'Black and white homecoming portrait on a dock'),
    ('studio-2023-dock-profile.jpg', 'Homecoming profile portrait on a dock'),
    ('studio-2023-dock-bw-overshoulder.jpg', 'Black and white over-the-shoulder homecoming portrait on a dock'),
    ('studio-2023-dock-bw-eyes.jpg', 'Black and white close homecoming portrait, eyes to camera'),
    ('studio-2023-shore-fullbody.jpg', 'Full-length homecoming portrait on the shore'),
    ('studio-2023-cotton-crouch.jpg', 'Crouching in a cotton field, homecoming portrait'),
    ('studio-2023-cotton-wide.jpg', 'Wide homecoming portrait in a cotton field'),
    ('studio-2023-cotton-sitting.jpg', 'Sitting in a cotton field, homecoming portrait'),
]
hc_figs = []
for i, (fn, alt) in enumerate(HC, 20):
    name = f'lillia-homecoming-{i:02d}.jpg'
    process(os.path.join(ICLOUD, fn), os.path.join(IMG, name))
    hc_figs.append(f'          <figure><img src="assets/img/{name}" alt="{alt}" loading="lazy" /></figure>')
hc_anchor = '''          <figure><img src="assets/img/lillia-homecoming-19.jpg" alt="Lillia with a tall cup against a white brick wall" loading="lazy" /></figure>
        </div>'''
assert hc_anchor in html
html = html.replace(hc_anchor, hc_anchor.split('\n')[0] + '\n' + '\n'.join(hc_figs) + '\n        </div>', 1)

open(HTML, 'w').write(html)
print('studio photos:', total, '| homecoming added:', len(HC))
