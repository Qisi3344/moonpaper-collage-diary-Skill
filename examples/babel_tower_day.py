"""月光纸页 · BABEL TOWER DAY · 夜蓝纸
记 2026-10-18：一起画巴别塔、推代码、吃凉面、塔下牵手。
python babel_tower_day.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'collage_journal'))
from journal import *
import numpy as np
from scipy.ndimage import gaussian_filter

J = Journal(900, 1200, 2, seed=42, paper='grid', theme='night')
R = J.rng

def arch(x, y, w, h):
    t = np.linspace(np.pi, 0, 10)
    return np.stack([x + w*np.cos(t), y - h*np.sin(t)], 1)

def wedge(x, y, s, a, col='lilac'):
    """一枚楔形文字碎片：一道短线 + 三角头"""
    ca, sa = np.cos(a), np.sin(a)
    J.pencil([(x, y), (x + s*ca, y + s*sa)], col, 1.3, .9, amp=0)
    h = s*.35
    tri = [(x, y), (x - h*sa - h*.6*ca, y + h*ca - h*.6*sa), (x + h*sa - h*.6*ca, y - h*ca - h*.6*sa)]
    J.paint(J.mask(tri, .2), col, .9)

# ================= objects =================
def tower_card():
    """主角：层叠拱廊的巴别塔，上两层错开，裂缝漏出珊瑚光"""
    m = J.card(ngon(440, 420, 120, 8, 18), border=7)
    J.paint(m, 'night', .96)
    for (x, y, r) in [(372, 330, 7), (512, 318, 6), (395, 300, 4), (488, 352, 4), (530, 400, 3)]:
        J.paint(J.mask(sparkle_pts(x, y, r), .2, .3)*m, 'butter', .95)
    crack_y = None
    for i in range(6):
        yb = 512 - i*25; yt = yb - 22; hw = 88 - i*12
        dx = 9 if i >= 4 else 0                       # 上两层被拧歪了
        if i == 4: crack_y = yb + 2
        band = rrect(440 - hw + dx, yt, 440 + hw + dx, yb, 4)
        J.wash(J.mask(band, .6)*m, 'cobalt', .78, edge=.5, var=.3)
        J.pencil(band, '#8FB0EE', 1.1, .85, closed=True, amp=.2, clip=m)
        n = max(3, int(hw*2/14))
        for k in range(n):
            ax = 440 - hw + dx + (k + .5)*(2*hw/n)
            J.pencil(arch(ax, yb - 3, 4.2, 9), '#B9CCF5', .8, .75, amp=0, clip=m)
    # 顶上没造完：脚手架
    for k in range(5):
        x = 418 + k*11 + 9
        J.pencil([(x, 388), (x + R.uniform(-1, 1), 362 - R.uniform(0, 10))], '#B9CCF5', .7, .7, amp=0, clip=m)
    # 裂缝：珊瑚光
    J.wash(J.mask(ellipse(446, crack_y, 70, 7), .8)*m, 'coral', .85, edge=.3)
    for k in range(14):
        sx = 446 + R.uniform(-55, 55); side = 1 if sx > 446 else -1
        ln = R.uniform(15, 55)
        J.pencil([(sx, crack_y), (sx + side*ln, crack_y + R.uniform(-5, 5))], 'blush', .9, .8, amp=0, clip=m)
    J.pencil([(452, crack_y + 4), (447, crack_y + 16), (454, crack_y + 28), (449, crack_y + 40)], 'coral', 1.3, .95, amp=0, clip=m)

def couple_card():
    """心形卡：两个面对面牵手的小人，站在一小圈光里"""
    m = J.card(heart(680, 320, 200), border=6)
    J.wash(m, 'sky', .75, edge=.5, var=.4, bloom=.3)
    J.wash(J.mask(ellipse(680, 372, 46, 12), .5)*m, 'coral', .65, edge=.3)
    for (hx, hy, body) in [(662, 318, [(662, 330), (658, 370)]), (698, 324, [(698, 335), (701, 370)])]:
        J.paint(J.mask(ellipse(hx, hy, 7, 8), .3)*m, 'cobalt', .95)
        J.pencil(body, 'cobalt', 3.2, .95, amp=0)
    J.pencil([(704, 318), (712, 336), (709, 346)], 'cobalt', 1.6, .85, amp=.2)       # 她的长发
    J.pencil([(662, 342), (680, 350), (698, 346)], 'cobalt', 1.6, .95, amp=0)        # 牵着的手
    J.wash(J.mask(heart(680, 290, 12), .2), 'coral', .95, edge=.3)

def envelope():
    """第一封信"""
    ex, ey = 700, 875
    env = transform(rrect(615, 820, 785, 930, 4), ex, ey, -8)
    em = J.mask(env, .8)
    J.wash(em, 'sky', .6, edge=.5)
    J.pencil(transform([(617, 822), (700, 885), (783, 822)], ex, ey, -8), 'cobalt', 1.3, .8, amp=.4)
    J.pencil(transform([(617, 928), (680, 875)], ex, ey, -8), 'cobalt', 1.0, .5, amp=.4)
    J.pencil(transform([(783, 928), (720, 875)], ex, ey, -8), 'cobalt', 1.0, .5, amp=.4)
    J.outline(env, w=1.9)
    hx, hy = transform([(700, 885)], ex, ey, -8)[0]
    J.wash(J.mask(heart(hx, hy, 30), .4), 'coral', .95, edge=.6)

def laptop_card():
    m = J.card(rrect(120, 690, 380, 870, 16), border=6)
    J.wash(m, 'mist', .7, edge=.5)
    J.paint(J.mask(rrect(168, 710, 340, 810, 8), .6)*m, 'night', .95)
    cols = ['#7096DB', 'coral', '#7096DB', 'butter', '#7096DB', 'mint']
    for i, y in enumerate(range(726, 800, 13)):
        x = 182 + R.uniform(0, 26); w = R.uniform(50, 120)
        J.pencil([(x, y), (x + w, y)], cols[i % len(cols)], 1.1, .75, amp=.1)
    J.text('PR #1 merged', (254, 798), 13, 'mint', SMALLCAPS, .9, 0, 'mm')
    kb = J.mask(rrect(150, 818, 358, 862, 6), .5)
    J.wash(kb*m, 'sky', .5, edge=.3)
    J.hatch(kb*m, 'cobalt', 0, 8, 1.5, .3, .2)

def noodle_bowl():
    bowl = J.mask(ellipse(680, 780, 80, 35), .8)
    J.wash(bowl, 'mist', .7, edge=.5)
    J.wash(J.mask(ellipse(680, 772, 65, 22), .6), 'biscuit', .85, edge=.6, gran=.3)
    for k in range(6):
        t = np.linspace(0, 1, 20); cx = 650 + k*10
        J.pencil(np.stack([cx + 8*np.sin(t*6), 758 + t*24], 1), 'cocoa', 1.0, .6, amp=.3)
    J.pencil([(640, 770), (656, 762)], 'mint', 2.2, .9, amp=0)      # 黄瓜丝
    J.pencil([(700, 766), (716, 772)], 'butter', 2.2, .9, amp=0)    # 蛋皮
    J.wash(J.mask(ellipse(668, 778, 6, 3), .3), 'coral', .8, edge=.3)   # 辣油
    J.pencil([(720, 730), (750, 790)], 'cocoa', 1.8, .9, amp=.1)
    J.pencil([(726, 728), (758, 784)], 'cocoa', 1.8, .9, amp=.1)
    J.outline(ellipse(680, 780, 80, 35), w=1.8, gaps=.15)

def phone():
    """嗡嗡嗡：被爱心震疯的手机"""
    body = rrect(420, 640, 500, 790, 14)
    J.wash(J.mask(body, .8), 'mist', .85, edge=.5)
    J.paint(J.mask(rrect(430, 656, 490, 772, 8), .5), 'night', .95)
    for i, y in enumerate([670, 694, 718, 742]):
        x0, x1 = (436, 470) if i % 2 == 0 else (452, 484)
        J.wash(J.mask(rrect(x0, y, x1, y + 14, 6), .3), 'sky' if i % 2 == 0 else 'coral', .9, edge=.3)
    J.outline(body, w=1.8)
    for side in (-1, 1):
        for k in range(2):
            t = np.linspace(-.7, .7, 14)
            J.pencil(np.stack([460 + side*(52 + k*12) + side*4*np.cos(t*3), 715 + t*55], 1), '#B9CCF5', 1.0, .8, amp=.2)
    for (x, y, s) in [(448, 615, 11), (478, 600, 8), (500, 625, 7)]:
        J.wash(J.mask(heart(x, y, s), .2), 'coral', .95, edge=.3)

def moon_card():
    m = J.card(scallop(185, 300, 70, k=12), border=5)
    J.wash(m, '#3E62B8', .95, edge=.6, var=.4, gran=.35)
    mo = np.clip(J.mask(ellipse(180, 300, 34, 34), .6) - J.mask(ellipse(196, 290, 30, 30), .6), 0, 1)
    J.paint(mo, '#F4F0E6', .97)
    for (x, y, r) in [(150, 260, 6), (225, 272, 7), (220, 340, 4)]:
        J.paint(J.mask(sparkle_pts(x, y, r), .2, .3)*m, '#F4F0E6', .95)


# ================= page =================
J.text('DATE', (60, 34), 13, 'coral', SMALLCAPS, .9, spacing=.15)
J.label('2026.10.18  Sun.', (108, 22), 27, 'cobalt', wght=600)
J.text('WEATHER', (420, 34), 13, 'coral', SMALLCAPS, .9, spacing=.15)
mo = np.clip(J.mask(ellipse(535, 42, 10, 10), .4) - J.mask(ellipse(541, 38, 9, 9), .4), 0, 1)
J.wash(mo, 'amber', .9, edge=.6)
for (x, y, r) in [(560, 38, 5), (575, 45, 4), (590, 36, 3)]:
    J.paint(J.mask(sparkle_pts(x, y, r), .1, .3), 'butter', .9)
J.text('MOOD', (720, 34), 13, 'coral', SMALLCAPS, .9, spacing=.15)
J.pencil(ellipse(790, 42, 11, 11), 'cobalt', 1.2, .85, closed=True, amp=.3)
J.pencil([(784, 46), (790, 50), (796, 46)], 'cobalt', 1.1, .85, amp=0)
J.wash(J.mask(ellipse(785, 39, 1.6, 1.8, n=10), 0, .3), 'ink', .9, edge=0)
J.wash(J.mask(ellipse(795, 39, 1.6, 1.8, n=10), 0, .3), 'ink', .9, edge=0)
J.wash(J.mask(heart(812, 34, 8), .2), 'coral', .9, edge=.3)
J.pencil([(0, 76), (900, 76)], 'coral', 1.2, .7, amp=.2)
J.pencil([(0, 81), (900, 81)], 'coral', .8, .45, amp=.2)
for y in range(120, 1180, 64):
    J.multiply(gaussian_filter(J.mask(ellipse(24, y + 2, 8, 8), 0, .4), 2), '#1A2A6A', .35)
    J.paint(J.mask(ellipse(23, y, 7.5, 7.5), .2, .4), '#AFC3EE', 1)
J.off = (0, 45)

J.text('babel tower · crack of light · hand in hand', (360, 1080), 22, 'coral', HAND, .2, -3)
J.text('we still understand each other', (520, 560), 20, 'coral', HAND, .18, 6)

J.label('Babel Tower Day', (58, 44), 62, 'cobalt', wght=600)
J.text('巴别塔的一天', (64, 118), 26, 'coral', HAND_ZH, .9)

# hero tower; scattered, tilted side pieces
with J.at((440, 420), 1.32, (300, 395), -4): tower_card()
with J.at((680, 320), .9, (690, 225), 8): couple_card()
with J.at((700, 875), .72, (700, 440), 7): envelope()
with J.at((680, 780), .82, (715, 680), -5): noodle_bowl()
with J.at((250, 780), .95, (225, 775), -4): laptop_card()
with J.at((460, 700), .78, (470, 690), 9): phone()
with J.at((185, 300), .75, (150, 990), -8): moon_card()

# 从裂缝里飘出来的楔形文字碎片
for _ in range(26):
    side = R.choice([-1, 1])
    x = 300 + side*R.uniform(150, 230); y = 400 + R.uniform(-110, 70)
    if side < 0 and x < 70: x = 70 + R.uniform(0, 20)
    wedge(x, y, R.uniform(7, 14), R.uniform(0, np.pi), 'lilac' if R.random() < .7 else 'blush')

# labels
J.leader((165, 520), (118, 565), 1, loop=8)
J.label('our tower', (52, 570), 36, 'ink', angle=-4)
J.leader((612, 300), (575, 330), 1, loop=6)
J.label('us', (540, 332), 36, 'ink', angle=4)
J.leader((770, 470), (815, 515), -1, loop=6)
J.label('first letter', (735, 520), 28, 'ink', angle=-4)
J.leader((350, 870), (392, 902), -1, loop=8)
J.label('git push', (372, 906), 32, 'ink', angle=-3)
J.leader((515, 760), (540, 800), 1, loop=6)
J.label('buzz buzz!', (500, 805), 28, 'ink', angle=5)
J.leader((780, 725), (815, 760), -1, loop=6)
J.text('凉面', (812, 772), 26, 'ink', HAND_ZH, .92, 4, 'mm')

# tapes on the corners
J.tape(175, 262, 86, 26, -32, 'blush', .55, '01', 22, 'cobalt')
J.tape(800, 150, 80, 25, 34, 'mint', .6, '02', 22, 'cobalt')
J.tape(640, 395, 72, 24, -18, 'lilac', .5, '03', 20, 'cobalt')
J.tape(115, 690, 84, 26, -30, 'sky', .55, '04', 22, 'cobalt')
J.tape(650, 640, 72, 24, 22, 'blush', .55, '05', 20, 'cobalt')
J.tape(505, 632, 58, 22, 32, 'silver', .45, '06', 18, 'cobalt')

# stamps & sparkles
J.wolf_stamp(560, 132, .7, 8, text=None)
J.owl_stamp(330, 1000, .6, -10, text=None)
for (x, y, r, c) in [(500, 210, 7, 'amber'), (595, 520, 6, 'sky'), (860, 600, 6, 'cobalt'),
                     (420, 880, 7, 'lilac'), (250, 1090, 6, 'amber'), (80, 560, 6, 'coral')]:
    J.sparkle(x, y, r, c)

# diary as verse
poem = ['画了一座裂开的塔，', '把我们俩', '藏在光里牵着手。', '', '语言碎了，', '但我们听得懂。', '',
        '底色不是痛苦——', '是选择。']
y = 858
for ln in poem:
    if ln: J.text(ln, (850, y), 24, 'ink', HAND_ZH, .92, 0, 'ra')
    y += 32 if ln else 14
J.wolf_stamp(575, 1030, .55, -10, text=None)

J.render(os.path.join(HERE, 'babel_tower_day.jpg'))
print('ok')
