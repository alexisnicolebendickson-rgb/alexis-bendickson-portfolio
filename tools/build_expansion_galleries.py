#!/usr/bin/env python3
"""Append expansion + portrait + birth/pin-up picks (154) to the live galleries.
Continues round-1 asset numbering per slug. Refuses to run twice.
"""
import os, re, sys, glob
from PIL import Image

REPO = os.path.expanduser('~/workspace/portfolio-rebuild')
ORG = os.path.expanduser('~/workspace/user/media_library/portfolio-business-best/facebook-picks-organized')
IMG = os.path.join(REPO, 'assets/img')
HTML = os.path.join(REPO, 'photography.html')

def find(folder, code):
    hits = sorted(glob.glob(os.path.join(ORG, folder, code + '_*.jpg')))
    assert hits, f'{folder}/{code}'
    return hits[0]

def process(src, dst):
    im = Image.open(src).convert('RGB')
    im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(dst, 'JPEG', quality=82, optimize=True, progressive=True)

# slug: (folder, label, start_no, last_existing_asset_no, [(code, alt)])
G = {}

G['weddings'] = ('Weddings', 'Weddings', 30, 29, [
 ('W32','groomsmen with the ring bearer on a lawn'),('W33','ring bearer in front of the groomsmen, close'),
 ('W34','young groomsman adjusting his bow tie'),('W35','full wedding party at a stone gate'),
 ('W36','bride alone with her bouquet beside a large tree'),('W37','bride holding a cream bouquet, close, smiling'),
 ('W38','bride and groom in a horse-drawn carriage'),('W39','black and white violinist at an outdoor ceremony'),
 ('W40','black and white couple nose-to-nose against a brick wall'),('W41','black and white flower girl walking down the aisle'),
 ('W42','bride alone outdoors at sunset by a lake'),('W43','black and white bride smiling beside a friend'),
 ('W44','bride with four bridesmaids in navy on a tree-lined path'),('W45','bride beside an older woman in navy lace'),
 ('W46','bride alone seated on a bridge at sunset, red bouquet'),('W47','black and white couple kissing, groom in a hat')])

G['maternity'] = ('Maternity', 'Maternity', 25, 24, [
 ('M26','white lace dress alone in a tall grass field'),('M27','couple by a lake holding an ultrasound photo'),
 ('M28','sunset couple with sunflowers'),('M29','black and white portrait reclining on sand with sunflowers'),
 ('M30','couple indoors at a gender reveal'),('M31','black and white seated portrait from a gender reveal session'),
 ('M32','family in superhero costumes on a lawn, wide'),('M33','couple in a field with a sign, playful'),
 ('M34','children in front, parents behind, superhero shirts')])

NB = [
 ('N12','black and white forehead-to-nose kiss in a hospital bed'),('N13','mother in a gown smiling with a supporter'),
 ('N14',"mother in bed holding 'It's a Girl' balloons"),('N15','mother holding a sleeping newborn'),
 ('N16','baby in a white patterned armchair'),('N17','black and white sleeping baby on a white blanket'),
 ('N18',"newborn on a father's tattooed back"),('N19','newborn on a white blanket, wide'),
 ('N20','sleeping newborn in a maroon wrap, close'),('N21','mother kissing a newborn, close'),
 ('N22','baby yawning'),('N23','newborn on a blue blanket with a giraffe toy'),
 ('N24','black and white newborn with a stuffed toy, close'),('N25','newborn in a blue wrap on white fur, eyes open'),
 ('N26','newborn feet detail with a hospital band'),('N27','newborn in a red wrap on white fur, eyes open'),
 ('N28','family portrait, parents holding their newborn'),('N29','black and white mother holding a newborn at her chest'),
 ('N30','newborn in a clear hospital bassinet'),('N31','newborn in a teal wrap in a woven basket'),
 ('N32','baby with sharp blue eyes, close'),('N33','baby in a Superman shirt among wooden blocks'),
 ('N34','baby looking up wide-eyed'),('N35','black and white detail, two adult hands over a sleeping baby'),
 ('N36','toddler in a mint dress seated, smiling'),('N37','black and white toddler in a mint dress, close'),
 ('N38','toddler walking in a navy cardigan'),('N39','baby in a pink dress in a purple armchair outdoors'),
 ('N40','father holding a baby in a floral outfit'),('N41','mother lifting a baby overhead outdoors'),
 ('N42','baby on her tummy on white fur'),('N43','baby in a white outfit among flowers'),
 ('N44','black and white baby with a Paris sign'),('N45','baby in a basket with bunny ears beside carrots'),
 ('N46','black and white baby smiling on white fur'),('N47','toddler beside a big number one, purple backdrop'),
 ('N48','toddler on white fur, purple backdrop'),('N49','toddler in a chair looking aside, close'),
 ('N50','baby in a plaid shirt smiling, balloons behind'),('N51','black and white profile, close'),
 ('N52','baby with angel wings, smiling'),('N53','outdoor family portrait, parents holding their baby'),
 ('N54','black and white baby portrait, close'),('N55','black and white baby from behind, looking at a Christmas tree'),
 ('N56','baby in a red elf outfit over gift boxes'),('N57','mother in white lace nursing her baby, seated'),
 ('N58','tender nursing portrait, close'),
 ('N59','black and white fetal monitor with a paper printout, detail'),('N60','labor moment, gripping the bed rail'),
 ('N61',"adult hand holding a newborn's tiny hand, close"),('N62',"black and white mother resting with her newborn on her chest"),
 ('N63',"newborn in a striped cap on her mother's chest"),('N64','mother in a hospital bed smiling at her newborn beside her'),
 ('N65','mother holding her newborn in a striped cap, smiling down'),('N66',"adult hand cradling a newborn's head, close"),
 ('N67','mother resting in a hospital bed, flowers in the foreground'),('N68','partner at the bedside holding her hand'),
 ('N69','mother in a hospital bed holding her wrapped newborn, close'),('N70','black and white going-home moment, mother leaning over the car seat'),
 ('N71','newborn in a teal wrap, eyes open, close'),('N72','black and white sleeping newborn in a round woven basket')]
G['newborn'] = ('Newborn', 'Newborn', 12, 11, NB)

FA = [
 ('P11','green hair and a blue off-shoulder top among foliage, close'),('P12','sitting on a log in the woods, wide'),
 ('P13','kneeling on a country road in a white dress'),('P14','blue hair and a patterned dress standing in a field'),
 ('P15','seated in a field in a white outfit'),('P16','floral dress against a brick wall, close'),
 ('P17','among sunflowers, smiling, close'),('P18','standing in a sunflower field at sunset, wide'),
 ('P19','crouching beside a trailer outdoors'),('P20','flower crown, smiling, close'),
 ('P21','hat, sitting among tulips'),('P22','black and white among tulips'),
 ('P23','black and white denim jacket portrait, close'),('P24','sitting in a field, wide'),
 ('P25','black and white portrait, direct gaze, close'),('P26','white dress in tall grass'),
 ('P27','dark top and patterned skirt crouching in golden light'),('P28','in red, holding a small dog on a brick sidewalk'),
 ('P29','in red, seated on an ornate bench'),('P30','hands playing an acoustic guitar, detail'),
 ('P31','black and white portrait smiling on a rope swing'),('P32','sailor hat and chevron top outdoors'),
 ('P33','black and white reclining portrait, close'),('P34','reclining portrait against a dark backdrop, wide'),
 ('P35','lying on a rock in front of a waterfall, green hair'),('P36','seated in the woods, navy top'),
 ('P37','seated on a log in the woods, hand in hair, wide'),('P38','black tank top, seated cross-legged on a rock'),
 ('P39','black and white one-shoulder dress against wooden doors'),('P40','burgundy cutout dress against wooden doors'),
 ('P41','floral dress seated on a bench, laughing, close'),('P42','floral dress leaning against a brick column'),
 ('P43','lying on a rock by a waterfall in overalls'),('P44','seated on a log in a creek, wide'),
 ('P45','striped top and denim shorts against a red brick wall'),('P46','striped bodysuit on metal stairs'),
 ('P47','black and white, striped top before a brick wall, from behind'),('P48','reclining on a city sidewalk'),
 ('P49','striped dress in a sunflower field at sunset, wide'),('P50','black and white, arms outstretched against wooden doors'),
 ('P51','black sleeveless top leaning on a railing by a brick wall'),('P52','reclining in an alley in studded boots'),
 ('P53','black and white over-shoulder portrait, close')]
G['fashion'] = ('Fashion', 'Fashion', 11, 10, FA)

EM = [
 ('B15','black and white, light chemise seated outdoors on grass'),('B16','light chemise seated on porch steps'),
 ('B17','black and white portrait in a red polka-dot top, close'),('B18','kneeling before a giant eye sculpture'),
 ('B19','standing at a giant eye sculpture, full-length'),('B20','blue polka-dot dress at a giant eye sculpture, wide'),
 ('B21','blue polka-dot dress leaning at a giant eye sculpture'),('B22','black and white over-shoulder portrait in a plaid shirt'),
 ('B23','plaid shirt, hands in hair, outdoors'),('B24','black and white full-length portrait in a plaid shirt'),
 ('B25','long green dress by an ivy-covered wall'),('B26','black and white hooded robe against a graffiti wall'),
 ('B27','crouching in a graphic tee and boots against a rusted wall'),('B28','standing in a field looking back over her shoulder, flower crown'),
 ('B29','pink top and white pants seated on rocks beside a lake'),('B30','black and white over-shoulder back view by the water'),
 ('B31','red polka-dot top and black skirt standing in the woods'),('B32','striped top seated on grass before a red disc sculpture'),
 ('B33','striped top reclining on grass before a red disc sculpture'),('B34','striped top leaning against a chain-link fence'),
 ('B35','striped top seated on yellow bleachers, red heels'),('B36','blue polka-dot dress seated before a giant eye sculpture, laughing'),
 ('B37','legs in black heels and a polka-dot skirt on a bench, detail'),('B38','blue polka-dot dress standing on a path, sun flare')]
G['empowerment'] = ('Empowerment', 'Empowerment', 15, 14, EM)

G['seniors'] = ('Seniors', 'Seniors', 28, 27, [
 ('S28','graduation cap with a raised-fist design and colorful stole, close')])

html = open(HTML).read()
if 'studio-newborn-72' in html:
    sys.exit('Expansion galleries already present — aborting.')

total = 0
for slug, (folder, label, start, last, items) in G.items():
    figs = []
    for j, (code, alt) in enumerate(items):
        no = start + j
        name = f'studio-{slug}-{no:02d}.jpg'
        process(find(folder, code), os.path.join(IMG, name))
        figs.append(f'          <figure><img src="assets/img/{name}" alt="{label}: {alt}" loading="lazy" /></figure>')
        total += 1
    anchor = f'          <figure><img src="assets/img/studio-{slug}-{last:02d}.jpg"'
    idx = html.find(anchor)
    assert idx >= 0, slug
    line_end = html.find('\n', idx)
    html = html[:line_end + 1] + '\n'.join(figs) + '\n' + html[line_end + 1:]

open(HTML, 'w').write(html)
print('appended photos:', total)
