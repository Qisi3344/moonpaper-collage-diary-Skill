import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'collage_journal'))
from journal import *
import numpy as np
from scipy.ndimage import gaussian_filter

J = Journal(900, 1200, 2, seed=7, paper='grid', base='nightblue')
R = J.rng

# ================= objects, each drawn in its own coords =================
def moon_card():
    m = J.card(scallop(185, 300, 98, k=12), border=6)
    J.wash(m, '#3E62B8', .95, edge=.6, var=.4, gran=.35)
    J.paint(J.mask(ellipse(178, 300, 48, 48), .8), '#F4F0E6', .97)
    for (cx, cy, r) in [(165, 285, 9), (195, 312, 6), (172, 322, 5), (192, 282, 4)]:
        J.wash(J.mask(ellipse(cx, cy, r, r*.9), .5), 'sky', .7, edge=.6)
    J.wash(J.mask(ellipse(188, 296, 46, 46), .8)*np.clip(1-J.mask(ellipse(170, 292, 46, 46), .8), 0, 1), 'sky', .45)
    for (x, y, r) in [(118, 248, 8), (250, 262, 10), (236, 352, 6), (128, 356, 5)]:
        J.paint(J.mask(sparkle_pts(x, y, r), .2, .3), '#F4F0E6', .95)

def heart_card():
    m = J.card(heart(690, 255, 215), border=7)
    J.wash(m, 'sky', .85, edge=.5, var=.5, bloom=.4)
    J.wash(m*J.mask(ellipse(640, 300, 90, 70), 0, 30), 'mint', .7, edge=0)
    st = [(625, 205), (662, 240), (700, 228), (735, 262), (712, 310), (676, 330), (648, 290)]
    J.pencil(st, 'ink', 1.0, .75, amp=.2)
    for x, y in st: J.paint(J.mask(sparkle_pts(x, y, 6), .1, .3), 'ink', .9)
    J.wash(J.mask(star(752, 200, 11), .3), 'coral', .9, edge=.3)
    for (x, y) in [(610, 330), (760, 330), (690, 360), (640, 250)]:
        J.paint(J.mask(ellipse(x, y, 2, 2, n=12), 0, .3), 'white', .9)

def night_card():
    m = J.card(ngon(470, 505, 98, 8, 22), border=6)
    J.paint(m, 'night', .96)
    for k in range(5):
        t = np.linspace(.3, 2.4*np.pi, 80); rr = 14 + k*12 + t*4
        sw = np.stack([455 + rr*np.cos(t + k*.6), 525 + rr*.55*np.sin(t + k*.6)], 1)
        J.pencil(sw, '#7096DB', 1.6, .85, amp=.4, blend='paint', clip=m)
    for (x, y, r) in [(430, 455, 12), (505, 440, 7), (520, 560, 9), (420, 545, 5), (470, 500, 5), (540, 495, 4)]:
        J.paint(J.mask(sparkle_pts(x, y, r), .2, .3)*m, 'butter', .95)
    J.paint(J.mask(ellipse(530, 462, 9, 9), .3), 'coral', .95)

def mug(w=2.3):
    body = J.mask(rrect(118, 548, 268, 690, 24), 1.)
    handle = np.clip(J.mask(ellipse(276, 610, 36, 40), 1) - J.mask(ellipse(278, 610, 21, 26), 1), 0, 1)
    handle *= np.clip(1 - body, 0, 1)
    J.wash(body, 'mist', .9, edge=.5); J.wash(handle, 'mist', .9, edge=.5)
    J.dots(body*J.mask(rrect(118, 575, 268, 690, 20), 0), 'blue', 4.2, 26, .6)
    J.hatch(body*J.mask(rrect(215, 548, 270, 690, 4), 0, 6), 'cobalt', 60, 4, .9, .35)
    J.hatch(handle, 'cobalt', 60, 4, .9, .3)
    J.paint(J.mask(ellipse(193, 549, 75, 15), .6), 'white', .9)
    J.wash(J.mask(ellipse(193, 551, 64, 10), .5), 'cocoa', .9, edge=.7)
    for (x, y) in [(176, 546), (205, 549)]:
        J.paint(J.mask(transform(rrect(x-9, y-8, x+9, y+8, 4), x, y, R.uniform(-20, 20)), .5), '#FBF8F2', .97)
        J.pencil(rrect(x-9, y-8, x+9, y+8, 4), 'blue', .9, .5, closed=True, amp=.3)
    J.lift(J.mask(rrect(132, 585, 140, 670, 4), .4), .6)
    J.outline(rrect(118, 548, 268, 690, 24), w=w)
    e = ellipse(276, 610, 36, 40); J.outline(e[e[:, 0] > 266], w=w*.85, closed=False)
    J.outline(ellipse(193, 549, 75, 15), w=w*.7, gaps=.25)
    for dx in (-22, 4, 30):
        t = np.linspace(0, 1, 30)
        J.pencil(np.stack([168 + dx + 7*np.sin(t*9), 528 - t*55], 1), 'sky', 1.6, .8, amp=.3)

def jam():
    glass = J.mask(rrect(655, 572, 790, 712, 26), 1)
    J.wash(glass, 'mist', .55, edge=.4)
    J.wash(J.mask(rrect(663, 608, 782, 704, 20), 1), 'berry', .9, edge=.7, gran=.45, var=.45)
    for (x, y) in [(674, 618), (770, 622), (676, 694), (700, 688), (752, 692), (772, 680)]:
        J.paint(J.mask(ellipse(x, y, 1.8, 1.8, n=10), 0, .3), 'white', .7)
    J.paint(J.mask(transform(rrect(680, 626, 768, 676, 6), 724, 651, -3), .6), '#FBF7EE', .97)
    J.text('berry', (724, 643), 21, 'cobalt', HAND, .95, 3, 'mm', 600)
    J.wash(J.mask(heart(724, 665, 13), .2), 'coral', .9, edge=.3)
    J.lift(J.mask(rrect(667, 590, 676, 690, 4), .5), .7)
    cloth = [(640, 560), (660, 535), (690, 528), (725, 525), (760, 528), (790, 535), (808, 560),
             (795, 572), (780, 566), (765, 576), (748, 568), (730, 578), (712, 568), (695, 578), (678, 568), (662, 577), (650, 568)]
    cm = J.mask(cloth, 1)
    J.wash(cm, 'blush', .75, edge=.4)
    J.hatch(cm, 'coral', 0, 9, 2.2, .45, .3); J.hatch(cm, 'coral', 90, 9, 2.2, .45, .3)
    J.pencil([(652, 566), (700, 572), (750, 572), (800, 564)], 'cobalt', 1.6, .9, amp=.5)
    J.pencil([(800, 564), (815, 585), (808, 600)], 'cobalt', 1.3, .9, amp=.5)
    J.hatch(glass*J.mask(rrect(750, 572, 795, 712, 4), 0, 8), 'cobalt', 65, 5, .9, .3)
    J.outline(rrect(655, 572, 790, 712, 26), w=2.0)
    J.outline(cloth, w=1.5, gaps=.3)

def plate():
    pl = J.mask(ellipse(305, 845, 168, 56), 1)
    J.wash(pl, 'mist', .6, edge=.4)
    J.lift(J.mask(ellipse(305, 845, 140, 42), .8), .75)
    J.pencil(ellipse(305, 845, 152, 49), 'blue', 1.5, .7, closed=True, amp=.5, gaps=.15)
    J.hatch(pl*np.clip(1-J.mask(ellipse(300, 838, 165, 50), 0, 6), 0, 1), 'cobalt', 20, 4, .9, .35)
    J.outline(ellipse(305, 845, 168, 56), w=2.0, gaps=.18)
    cres = np.clip(J.mask(ellipse(240, 832, 48, 40), 1) - J.mask(ellipse(262, 818, 40, 36), 1), 0, 1)
    J.wash(cres, 'biscuit', .95, edge=.75, gran=.4)
    J.hatch(cres*J.mask(ellipse(232, 855, 40, 22), 0, 6), 'cocoa', 40, 4, .9, .35)
    for (x, y) in [(214, 840), (225, 855), (240, 864), (205, 826)]:
        J.paint(J.mask(ellipse(x, y, 1.8, 1.8, n=10), 0, .3), 'white', .9)
    for (x, y, r, a) in [(318, 838, 30, 8), (378, 852, 25, -14), (345, 812, 19, 30)]:
        J.wash(J.mask(transform(star(x, y, r, inner=.52), x, y, a), 1), 'butter', .95, edge=.7, gran=.35)
        J.wash(J.mask(ellipse(x, y, 4, 4), .3), 'coral', .85, edge=.2)
    J.outline(transform(star(318, 838, 30, inner=.52), 318, 838, 8), w=1.3, gaps=.3)

def envelope():
    ex, ey = 700, 875
    env = transform(rrect(615, 820, 785, 930, 4), ex, ey, -8)
    em = J.mask(env, .8)
    J.wash(em, 'sky', .55, edge=.5)
    J.wash(J.mask(transform([(615, 820), (700, 885), (785, 820)], ex, ey, -8), .6), 'sky', .35, edge=.5)
    J.pencil(transform([(617, 822), (700, 885), (783, 822)], ex, ey, -8), 'cobalt', 1.3, .8, amp=.4)
    J.pencil(transform([(617, 928), (680, 875)], ex, ey, -8), 'cobalt', 1.0, .5, amp=.4)
    J.pencil(transform([(783, 928), (720, 875)], ex, ey, -8), 'cobalt', 1.0, .5, amp=.4)
    J.hatch(em*J.mask(transform(rrect(700, 885, 790, 935, 2), ex, ey, -8), 0, 8), 'cobalt', 50, 5, .9, .28)
    J.outline(env, w=1.9)
    hx, hy = transform([(700, 885)], ex, ey, -8)[0]
    J.wash(J.mask(heart(hx, hy, 30), .4), 'coral', .95, edge=.6)

# ================= page =================
# ---- diary header (top, like a real diary page) ----
J.text('DATE', (60, 34), 13, 'blush', SMALLCAPS, .9, spacing=.15)
J.label('2026.10.19  Mon.', (108, 22), 27, 'cobalt', wght=600)
J.text('WEATHER', (420, 34), 13, 'blush', SMALLCAPS, .9, spacing=.15)
J.pencil(ellipse(540, 42, 7, 7), 'coral', 1.2, .85, closed=True, amp=.2)
for k in range(8):
    t = k*np.pi/4; J.pencil([(540+11*np.cos(t), 42+11*np.sin(t)), (540+15*np.cos(t), 42+15*np.sin(t))], 'coral', 1.1, .85, amp=0)
for (cx, cy, r) in [(577, 46, 7), (587, 40, 9), (598, 46, 7)]:
    J.pencil(ellipse(cx, cy, r, r), 'cobalt', 1.0, .7, closed=True, amp=.2)
mo = np.clip(J.mask(ellipse(635, 42, 10, 10), .4) - J.mask(ellipse(641, 38, 9, 9), .4), 0, 1)
J.wash(mo, 'amber', .9, edge=.6)
J.pencil(ellipse(636, 42, 19, 16, rot=-8), 'coral', 1.3, .85, closed=True, amp=.8)
J.text('MOOD', (720, 34), 13, 'blush', SMALLCAPS, .9, spacing=.15)
J.pencil(ellipse(790, 42, 11, 11), 'cobalt', 1.2, .85, closed=True, amp=.3)
J.pencil([(784, 45), (790, 49), (796, 45)], 'cobalt', 1.1, .85, amp=0)
J.wash(J.mask(ellipse(785, 39, 1.6, 1.8, n=10), 0, .3), 'ink', .9, edge=0)
J.wash(J.mask(ellipse(795, 39, 1.6, 1.8, n=10), 0, .3), 'ink', .9, edge=0)
J.pencil([(0, 76), (900, 76)], 'coral', 1.2, .7, amp=.2)
J.pencil([(0, 81), (900, 81)], 'coral', .8, .45, amp=.2)
for y in range(120, 1180, 64):
    J.multiply(gaussian_filter(J.mask(ellipse(24, y + 2, 8, 8), 0, .4), 2), '#1C2E78', .35)
    J.paint(J.mask(ellipse(23, y, 7.5, 7.5), .2, .4), '#AFC3EE', 1)
J.off = (0, 45)

J.text('warm milk · two stars · one wish', (300, 1110), 22, 'coral', HAND, .2, -3)

J.label('Midnight Pantry', (58, 44), 70, 'cobalt', wght=600)
J.text('小狼的夜宵手帐', (64, 128), 26, 'blush', HAND_ZH, .9)

# hierarchy: hero mug; scattered, tilted side pieces
with J.at((185, 300), .78, (150, 272), -7): moon_card()
with J.at((690, 255), .84, (728, 232), 9): heart_card()
with J.at((470, 505), .86, (418, 372), -6): night_card()
with J.at((215, 585), 1.55, (300, 650)): mug(3.0)
with J.at((725, 620), .92, (650, 622), -6): jam()
with J.at((305, 845), .9, (300, 952), 2): plate()
with J.at((700, 875), .7, (772, 445), -9): envelope()

J.leader((152, 600), (92, 470), -1)
J.label('hot cocoa', (36, 414), 46, 'ink', angle=4)
J.leader((728, 650), (772, 700), -1, loop=8)
J.label('berry jam', (728, 706), 34, 'ink', angle=-5)
J.leader((160, 975), (110, 1012), 1, loop=8)
J.label('moon cookies', (48, 1016), 34, 'ink', angle=-2)
J.leader((838, 470), (852, 505), -1, loop=6)
J.label('a letter', (790, 510), 30, 'ink', angle=-4)

J.tape(82, 196, 86, 26, -24, 'blush', .55, '01', 22, 'cobalt')
J.tape(812, 150, 86, 26, 36, 'mint', .6, '02', 22, 'cobalt')
J.tape(352, 296, 84, 26, -34, 'lilac', .45, '03', 22, 'cobalt')
J.tape(415, 556, 92, 30, 16, 'blush', .55, '04', 26, 'cobalt')
J.tape(728, 548, 80, 25, 30, 'silver', .45, '05', 21, 'cobalt')
J.tape(452, 912, 80, 25, 20, 'sky', .55, '06', 21, 'cobalt')
J.tape(700, 412, 72, 24, -26, 'blush', .55, '07', 20, 'cobalt')

# our stamps instead of the decorative bursts
J.wolf_stamp(548, 120, .72, 8, text=None)
J.owl_stamp(585, 470, .9, 8, text=None)
J.owl_stamp(80, 775, .62, -10, text=None)
moon2 = np.clip(J.mask(ellipse(560, 300, 18, 18), .6) - J.mask(ellipse(569, 293, 15, 15), .6), 0, 1)
J.wash(moon2, 'coral', .95, edge=.4)
for (x, y, r, c) in [(300, 190, 9, 'cobalt'), (630, 390, 7, 'amber'), (262, 440, 7, 'sky'), (470, 200, 7, 'amber'),
                     (530, 560, 8, 'cobalt'), (500, 820, 7, 'coral'), (870, 790, 7, 'cobalt'), (860, 380, 6, 'lilac'), (505, 1060, 6, 'cobalt')]:
    J.sparkle(x, y, r, c)

# ---- diary as a poem, right-aligned like verse ----
poem = ['今晚月亮好圆，', '小狼偷偷', '吃掉了三块星星饼干。', '', '猫头鹰说：', '明天也要一起熬夜写手帐，', '不许先睡哦。']
y = 840
for ln in poem:
    if ln: J.text(ln, (848, y), 27, 'ink', HAND_ZH, .92, 0, 'ra')
    y += 38 if ln else 18
J.wolf_stamp(800, 1112, .62, -10, text=None)

J.render(os.path.join(HERE, 'midnight_pantry_night.jpg'))
print('ok')
