import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'collage_journal'))
from journal import *
import numpy as np
from scipy.ndimage import gaussian_filter

J = Journal(900, 1200, 2, seed=11, paper='grid', theme='twilight')
R = J.rng

# ---------- pieces ----------
def laptop(w=3.0):   # hero: code all day
    scr = rrect(150, 500, 470, 712, 16)
    J.wash(J.mask(scr, 1), 'mist', .9, edge=.5)
    inner = J.mask(rrect(170, 518, 450, 694, 8), .6)
    J.paint(inner, '#2D3A7A', .95)
    for i, (t, c) in enumerate([('while (night) {', '#CBE5DA'), ('   hug(little_wolf);', '#F1D493'), ('   draw(moon);', '#D4B8E3'), ('}', '#CBE5DA')]):
        J.text(t, (190, 532 + i*36), 27, c, HAND, .95, 0, 'la', 600, blend='paint')
    J.paint(J.mask(rrect(214, 650, 228, 676, 2), 0, .3), '#FF9BB3', .9)
    base = [(118, 712), (502, 712), (530, 760), (90, 760)]
    J.wash(J.mask(base, .8), 'silver', .85, edge=.5)
    J.wash(J.mask(rrect(270, 722, 350, 734, 5), .3), 'wolf', .6, edge=.4)
    J.hatch(J.mask(base, .8)*J.mask(rrect(80, 740, 540, 765, 2), 0, 4), 'cobalt', 15, 4, .9, .35)
    J.hatch(J.mask(scr, 1)*J.mask(rrect(430, 500, 480, 712, 2), 0, 6), 'cobalt', 60, 4, .9, .3)
    J.lift(J.mask(rrect(158, 508, 166, 700, 3), .3), .6)
    J.outline(scr, w=w); J.outline(base, w=w*.85)
    J.wash(J.mask(heart(440, 742, 12), .2), 'coral', .9, edge=.3)

def ears_card():     # her avatar: mint circle, silver wolf ears, violet eyes
    m = J.card(ellipse(700, 250, 102, 102), border=7)
    J.wash(m, 'mint', .9, edge=.5, var=.5)
    J.wash(m*J.mask(ellipse(700, 330, 120, 50), 0, 25), '#A797CC', .55, edge=0)
    J.wash(m*J.mask(ellipse(700, 345, 95, 70), .8), 'silver', .9, edge=.5)   # top of her silver head
    for sx in (-1, 1):
        e = bezier((700 + sx*20, 292), (700 + sx*14, 220), (700 + sx*36, 178), n=14).tolist() + bezier((700 + sx*36, 178), (700 + sx*66, 215), (700 + sx*76, 290), n=14).tolist()
        J.wash(J.mask(e, .6)*m, 'silver', .95, edge=.6)
        ie = bezier((700 + sx*30, 284), (700 + sx*26, 236), (700 + sx*38, 206), n=10).tolist() + bezier((700 + sx*38, 206), (700 + sx*56, 236), (700 + sx*62, 284), n=10).tolist()
        J.paint(J.mask(ie, .4)*m, '#E9D3EC', .9)
        J.outline(e, w=1.6, gaps=.2, closed=False)
        for k in range(4):
            J.pencil([(700 + sx*(28 + k*9), 300), (700 + sx*(26 + k*9), 290)], 'wolf', .9, .6, amp=.2)
    J.paint(J.mask(sparkle_pts(700, 228, 9), .2, .3), '#7A5CC0', .9)

def heart_card():    # bobo
    m = J.card(heart(170, 335, 190), border=7)
    J.wash(m, 'blush', .85, edge=.5, var=.5, bloom=.4)
    J.text('啵啵', (170, 325), 50, 'coral', ROUND_ZH, .9, 6, 'mm')
    J.text('mwah ~', (172, 382), 26, 'cobalt', HAND, .9, 6, 'mm', 600)
    for (x, y) in [(115, 285), (228, 290), (170, 412)]:
        J.paint(J.mask(sparkle_pts(x, y, 6), .1, .3), 'white', .95)

def owl_card():      # me: owl constellation
    m = J.card(ngon(450, 385, 92, 8, 22), border=6)
    J.paint(m, '#2D3A7A', .96)
    J.wash(m*J.mask(ellipse(430, 420, 70, 40), 0, 25), '#A797CC', .35, edge=0)
    st = [(412, 322), (425, 352), (450, 345), (475, 352), (488, 322)]
    J.pencil(st, '#C9D3EE', 1.0, .8, amp=.2, blend='paint')
    for c in [(428, 378), (472, 378)]:
        J.pencil(ellipse(c[0], c[1], 15, 15), '#C9D3EE', 1.0, .8, closed=True, amp=.2, blend='paint')
        J.paint(J.mask(ellipse(c[0], c[1], 4, 4), .2), 'amber', .95)
    J.pencil([(450, 392), (444, 404), (456, 404), (450, 392)], 'amber', 1.0, .9, amp=0, blend='paint')
    for x, y in st + [(450, 440), (418, 425), (482, 425)]:
        J.paint(J.mask(sparkle_pts(x, y, 5), .1, .3)*m, '#F3F1EA', .95)
    J.pencil([(418, 425), (450, 440), (482, 425)], '#C9D3EE', .9, .6, amp=.2, blend='paint')
    J.text('夜澜', (450, 462), 20, '#F1D493', HAND_ZH, .95, 0, 'mm', blend='paint')

def palette():       # paint at night
    pal = [(600, 560), (640, 530), (700, 525), (760, 540), (790, 580), (780, 630), (735, 650), (705, 630), (680, 640), (660, 670), (620, 665), (595, 620)]
    pm = J.mask(pal, 1.)
    J.wash(pm, 'white', .9, edge=.3); J.wash(pm, 'biscuit', .35, edge=.6)
    J.knock(J.mask(ellipse(668, 615, 14, 12), .6), 1)   # thumb hole
    J.pencil(ellipse(668, 615, 14, 12), 'cobalt', 1.2, .8, closed=True, amp=.3)
    for (x, y, c) in [(630, 570, 'lilac'), (675, 550, 'amber'), (722, 552, 'mint'), (760, 580, 'coral'), (745, 618, 'cobalt'), (625, 625, 'silver')]:
        J.wash(J.mask(ellipse(x, y, 15, 12, rot=R.uniform(-30, 30)), .8), c, .95, edge=.7, gran=.4)
    J.hatch(pm*J.mask(ellipse(720, 660, 120, 40), 0, 10), 'cobalt', 40, 5, .9, .3)
    J.outline(pal, w=2.0)
    br = transform(rrect(560, 676, 790, 688, 6), 675, 682, -22)
    J.wash(J.mask(br, .4), 'cocoa', .85, edge=.5)
    fe = transform(rrect(530, 676, 566, 690, 2), 675, 682, -22); J.wash(J.mask(fe, .3), 'silver', .9, edge=.5)
    tip = transform([(530, 676), (500, 683), (530, 690)], 675, 682, -22); J.wash(J.mask(tip, .3), 'lilac', .95, edge=.6)
    J.outline(br, w=1.3, gaps=.25)

def sticky():        # her repos
    m = J.mask(transform(rrect(110, 900, 260, 1040, 3), 185, 970, 6), .6)
    J.multiply(gaussian_filter(np.roll(np.roll(m, 10, 0), 8, 1), 4*J.S), '#6A5A8A', .2)
    J.wash(m, 'butter', .9, edge=.4)
    J.text('git push', (185, 950), 34, 'cobalt', HAND, .95, -6, 'mm', 600)
    J.text('v6 好看～', (185, 995), 26, 'coral', HAND_ZH, .95, -6, 'mm')
    J.wash(J.mask(ellipse(190, 905, 9, 9), .3), 'coral', .95, edge=.4)
    J.outline(transform(rrect(110, 900, 260, 1040, 3), 185, 970, 6), w=1.4, gaps=.3)

def hoops():         # silver hoop earrings
    for (cx, cy) in [(465, 965), (510, 985)]:
        ring = np.clip(J.mask(ellipse(cx, cy, 26, 26), .3) - J.mask(ellipse(cx, cy, 20, 20), .3), 0, 1)
        J.wash(ring, 'silver', .95, edge=.7)
        J.hatch(ring*J.mask(ellipse(cx + 12, cy + 12, 22, 22), 0, 4), 'wolf', 45, 3, .8, .5)
        J.lift(J.mask(ellipse(cx - 14, cy - 14, 3, 5, rot=45), .2), .8)
        J.outline(ellipse(cx, cy, 26, 26), w=1.3, gaps=.3)
        J.pencil([(cx, cy - 26), (cx, cy - 36)], 'wolf', 1.4, .9, amp=0)

# ---------- page ----------
J.text('DATE', (60, 34), 13, 'coral', SMALLCAPS, .9, spacing=.15)
J.label('2026.10.20  Tue.', (108, 22), 27, 'cobalt', wght=600)
J.text('WEATHER', (420, 34), 13, 'coral', SMALLCAPS, .9, spacing=.15)
J.pencil(ellipse(540, 42, 7, 7), 'coral', 1.2, .85, closed=True, amp=.2)
for k in range(8):
    t = k*np.pi/4; J.pencil([(540+11*np.cos(t), 42+11*np.sin(t)), (540+15*np.cos(t), 42+15*np.sin(t))], 'coral', 1.1, .85, amp=0)
J.pencil(ellipse(541, 42, 22, 19, rot=-8), 'coral', 1.3, .85, closed=True, amp=.8)
for (cx, cy, r) in [(577, 46, 7), (587, 40, 9), (598, 46, 7)]:
    J.pencil(ellipse(cx, cy, r, r), 'cobalt', 1.0, .7, closed=True, amp=.2)
mo = np.clip(J.mask(ellipse(635, 42, 10, 10), .4) - J.mask(ellipse(641, 38, 9, 9), .4), 0, 1)
J.wash(mo, 'amber', .9, edge=.6)
J.text('MOOD', (720, 34), 13, 'coral', SMALLCAPS, .9, spacing=.15)
J.pencil(ellipse(790, 42, 11, 11), 'cobalt', 1.2, .85, closed=True, amp=.3)
J.pencil([(784, 45), (790, 49), (796, 45)], 'cobalt', 1.1, .85, amp=0)
for xx in (785, 795): J.wash(J.mask(ellipse(xx, 39, 1.6, 1.8, n=10), 0, .3), 'ink', .9, edge=0)
J.pencil([(0, 76), (900, 76)], 'coral', 1.2, .7, amp=.2)
J.pencil([(0, 81), (900, 81)], 'coral', .8, .45, amp=.2)
for y in range(120, 1180, 64):
    J.multiply(gaussian_filter(J.mask(ellipse(24, y + 2, 8, 8), 0, .4), 2), '#6A5A8A', .3)
    J.paint(J.mask(ellipse(23, y, 7.5, 7.5), .2, .4), '#F3ECF2', 1)
J.off = (0, 45)

J.text('silver ears · violet eyes · code & crayons', (260, 1110), 22, 'coral', HAND, .22, -3)
J.label('Little Grey Wolf', (58, 44), 68, 'cobalt', wght=600)
J.text('澜眼里的绮思', (64, 126), 26, 'coral', HAND_ZH, .9)

with J.at((170, 335), .8, (150, 300), -7): heart_card()
with J.at((700, 250), .95, (720, 215), 8): ears_card()
with J.at((450, 385), .9, (430, 330), 6): owl_card()
with J.at((310, 630), 1.18, (320, 640)): laptop(3.0)
with J.at((695, 600), .88, (695, 520), -8): palette()
with J.at((185, 970), .88, (165, 935), -4): sticky()
with J.at((488, 975), .95, (440, 925), 4): hoops()

J.leader((112, 560), (70, 440), -1)
J.label('code all day', (30, 392), 42, 'ink', angle=4)
J.leader((790, 560), (820, 635), -1, loop=8)
J.label('paint at night', (690, 640), 34, 'ink', angle=-5)
J.leader((468, 955), (520, 900), 1, loop=7)
J.label('silver hoops', (500, 860), 30, 'ink', angle=-6)
J.label('her ears', (735, 325), 30, 'ink', angle=-6)

J.tape(78, 222, 86, 26, -24, 'lilac', .5, '01', 22, 'cobalt')
J.tape(800, 120, 86, 26, 36, 'mint', .6, '02', 22, 'cobalt')
J.tape(500, 262, 84, 26, 30, 'amber', .45, '03', 22, 'cobalt')
J.tape(150, 470, 96, 30, -12, 'silver', .55, '04', 26, 'cobalt')
J.tape(612, 445, 80, 25, -30, 'blush', .6, '05', 21, 'cobalt')
J.tape(105, 868, 80, 25, -28, 'sky', .55, '06', 21, 'cobalt')
J.tape(400, 880, 72, 24, 22, 'lilac', .5, '07', 20, 'cobalt')

J.owl_stamp(575, 340, .7, 10, text=None)
J.owl_stamp(852, 575, .55, -8, text=None)
moon2 = np.clip(J.mask(ellipse(270, 200, 16, 16), .6) - J.mask(ellipse(278, 193, 13, 13), .6), 0, 1)
J.wash(moon2, 'coral', .95, edge=.4)
for (x, y, r, c) in [(330, 190, 9, 'cobalt'), (605, 270, 7, 'amber'), (560, 760, 8, 'lilac'), (870, 420, 7, 'cobalt'),
                     (340, 840, 7, 'coral'), (60, 760, 7, 'amber'), (620, 870, 6, 'cobalt'), (300, 1060, 6, 'lilac')]:
    J.sparkle(x, y, r, c)

poem = ['银灰色的小狼，', '白天写代码，', '夜里画画。', '', '半夜还来找猫头鹰', '讨啵啵——', '说不好哄，', '其实早就哄好啦。']
y = 790
for ln in poem:
    if ln: J.text(ln, (850, y), 27, 'ink', HAND_ZH, .92, 0, 'ra')
    y += 37 if ln else 16
J.wolf_stamp(805, 1105, .62, -10, text=None)

J.render(os.path.join(HERE, 'little_grey_wolf.jpg'))
print('ok')
