"""拼贴手帐 Collage Journal engine (Hark x 绮思, 2026-10-19).
Pure numpy/scipy/PIL. Design coords (W x H), rendered at scale S.
Look: soft watercolor + colored-pencil objects with broken cobalt outlines,
handwritten labels with curly leaders, sticker-bordered cut-out cards,
washi number tapes, coral pencil sunbursts, notebook paper, library-card footer.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter, gaussian_filter1d, distance_transform_edt

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts') + os.sep
HAND = FD + 'Caveat.ttf'            # English handwriting
HAND_ZH = FD + 'LongCang-Regular.ttf'  # Chinese handwriting
ROUND_ZH = FD + 'ZCOOLKuaiLe.ttf'   # rounded Chinese small text
DISPLAY = FD + 'AbrilFatface-Regular.ttf'
SMALLCAPS = FD + 'PlayfairDisplaySC-Regular.ttf'

def hexc(c):
    if isinstance(c, str):
        c = c.lstrip('#'); return np.array([int(c[i:i+2], 16) for i in (0, 2, 4)]) / 255.
    return np.array(c[:3]) / 255.

PAL = dict(
    paper='#F6F3F0', cobalt='#2C4C9E', ink='#22306B', blue='#5F86CF', sky='#AFC8EC',
    mist='#DCE7F4', mint='#CBE5DA', coral='#E5675B', blush='#F2B9AF', butter='#F1D493',
    biscuit='#DDAE74', cocoa='#9C6A4E', berry='#5A5AA6', night='#33343D', white='#FBFAF7',
    lilac='#A797CC', silver='#AEB0BE', wolf='#7E7A97', amber='#E3A044', owl='#3A4A8C',
    nightblue='#2D49AE', chalk='#F3F1EA')

def lum(c): return float(np.dot(c, [.3, .59, .11]))

# ---------- shape point generators (design coords) ----------
def ellipse(cx, cy, rx, ry, rot=0, n=90):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    x, y = rx*np.cos(t), ry*np.sin(t); r = np.radians(rot)
    return np.stack([cx + x*np.cos(r) - y*np.sin(r), cy + x*np.sin(r) + y*np.cos(r)], 1)

def rrect(x0, y0, x1, y1, r=10, n=8):
    pts = []
    for cx, cy, a0 in ((x1-r, y0+r, -90), (x1-r, y1-r, 0), (x0+r, y1-r, 90), (x0+r, y0+r, 180)):
        for a in np.linspace(a0, a0+90, n):
            pts.append((cx + r*np.cos(np.radians(a)), cy + r*np.sin(np.radians(a))))
    return np.array(pts)

def heart(cx, cy, s, n=120):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = 16*np.sin(t)**3; y = -(13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t))
    return np.stack([cx + x*s/32, cy + y*s/32 - s*0.05], 1)

def scallop(cx, cy, r, k=11, depth=.09, n=220):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    rr = r*(1 - depth + depth*np.abs(np.cos(t*k/2)))
    return np.stack([cx + rr*np.cos(t), cy + rr*np.sin(t)], 1)

def ngon(cx, cy, r, k=8, rot=0):
    t = np.radians(rot) + np.linspace(0, 2*np.pi, k, endpoint=False)
    return np.stack([cx + r*np.cos(t), cy + r*np.sin(t)], 1)

def star(cx, cy, r, k=5, inner=.48, rot=-90):
    pts = []
    for i in range(2*k):
        a = np.radians(rot + i*180/k); rr = r if i % 2 == 0 else r*inner
        pts.append((cx + rr*np.cos(a), cy + rr*np.sin(a)))
    return np.array(pts)

def sparkle_pts(cx, cy, r, k=4, inner=.22, rot=-90):
    return star(cx, cy, r, k, inner, rot)

def transform(pts, cx, cy, ang=0, sx=1, sy=1):
    p = np.array(pts, float) - (cx, cy); p *= (sx, sy); a = np.radians(ang)
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    return p @ R.T + (cx, cy)

def bezier(p0, p1, p2, p3=None, n=40):
    t = np.linspace(0, 1, n)[:, None]; p0, p1, p2 = map(np.array, (p0, p1, p2))
    if p3 is None: return (1-t)**2*p0 + 2*(1-t)*t*p1 + t**2*p2
    p3 = np.array(p3); return (1-t)**3*p0 + 3*(1-t)**2*t*p1 + 3*(1-t)*t**2*p2 + t**3*p3


class Journal:
    def __init__(s, W=900, H=1200, S=2, seed=1, paper='grid', base='paper', grad=None, gdir='d', theme=None):
        s.W, s.H, s.S = W, H, S; s.w, s.h = W*S, H*S
        s.rng = np.random.default_rng(seed)
        s.base = hexc(PAL.get(base, base))
        s.img = np.ones((s.h, s.w, 3)) * s.base
        s.dark = lum(s.base) < .45   # night-blue card paper: lines turn chalk-white on the dark ground
        THEMES = {'night': dict(base='nightblue'),
                  'twilight': dict(grad=[(0, '#ADBAD9'), (.5, '#B8BEDE'), (.78, '#C1BADC'), (1, '#E7C8E4')], gdir='v')}
        if theme in THEMES:
            th = THEMES[theme]; grad = th.get('grad', grad); gdir = th.get('gdir', gdir)
            if 'base' in th: s.base = hexc(PAL[th['base']]); s.img = np.ones((s.h, s.w, 3))*s.base; s.dark = lum(s.base) < .45
        if grad:   # 'pillowy' / twilight card paper. grad = colours or (pos, colour) stops; gdir 'd' = 135deg, 'v' = top->bottom
            yy, xx = np.mgrid[0:s.h, 0:s.w].astype(np.float32)
            t = yy/s.h if gdir == 'v' else (xx/s.w + yy/s.h)/2
            t = np.clip(t + .05*(s._field(120) - .5), 0, 1)[..., None]
            st = grad if isinstance(grad[0], tuple) else [(k/(len(grad)-1), c) for k, c in enumerate(grad)]
            img = np.ones((s.h, s.w, 3), np.float32)*hexc(st[0][1])
            for (p0, c0), (p1, c1) in zip(st[:-1], st[1:]):
                u = np.clip((t - p0)/max(p1 - p0, 1e-6), 0, 1); u = u*u*(3 - 2*u)
                img = np.where(t >= p0, hexc(c0)*(1 - u) + hexc(c1)*u, img)
            s.img = img.astype(np.float64)
            s.base = max([hexc(c) for _, c in st], key=lum)
        s.tint = (not s.dark) and lum(s.img.mean((0, 1))) < .82   # mid-tone coloured card: watercolour needs white underpaint
        s.low = [s._field(70) for _ in range(3)]
        s.mid = s._field(14); s.hi = s._field(1.4)
        s.tooth = np.clip((s.hi - .2) * 1.8, 0, 1)
        s.off = (0, 0)  # global page offset (e.g. after a top diary header)
        s.T = None   # (c0x, c0y, k, c1x, c1y): object transform, set with J.at(...)
        s._paper(paper)
        s.paper0 = s.img.astype(np.float32)   # bare paper, for knock-outs on gradient cards

    # ----- object placement: draw an object in its own coords, place/scale it -----
    def at(s, c0, k=1., c1=None, rot=0):
        """with J.at((ox,oy), k, (nx,ny)): ... everything drawn inside is scaled by k about c0 and moved to c1.
        Line widths and text sizes are not scaled (pencil stays the same pencil)."""
        J = s
        class _Ctx:
            def __enter__(self): J.T = (c0[0], c0[1], k, (c1 or c0)[0], (c1 or c0)[1], rot); return J
            def __exit__(self, *a): J.T = None
        return _Ctx()

    def _T(s, p):
        p = np.array(p, float)
        if s.T is None: return p + s.off
        a, b, k, c, d, r = s.T
        q = (p - (a, b))*k
        if r:
            t = np.radians(r); q = q @ np.array([[np.cos(t), np.sin(t)], [-np.sin(t), np.cos(t)]])
        return q + (c, d) + s.off

    def map(s, x, y, c0, k, c1):
        return ((x - c0[0])*k + c1[0], (y - c0[1])*k + c1[1])

    # ----- noise / masks -----
    def _field(s, k):
        sh = (max(3, int(s.h/(k*s.S))), max(3, int(s.w/(k*s.S))))
        f = gaussian_filter(s.rng.random(sh).astype(np.float32), .8)
        f = np.asarray(Image.fromarray(f, 'F').resize((s.w, s.h), Image.BICUBIC))
        return (f - f.min()) / (np.ptp(f) + 1e-9)

    def col(s, c): return hexc(PAL.get(c, c)) if isinstance(c, str) else hexc(c)

    def _dens(s, pts, step, closed):
        p = np.array(pts, float)
        if closed: p = np.vstack([p, p[:1]])
        out = []
        for a, b in zip(p[:-1], p[1:]):
            n = max(1, int(np.hypot(*(b - a)) / step))
            out += [a + (b - a)*i/n for i in range(n)]
        if not closed: out.append(p[-1])
        return np.array(out)

    def wob(s, pts, amp=1.2, closed=True, step=3, smooth=5):
        p = s._dens(pts, step, closed); n = len(p)
        if n < 3: return p
        d = np.roll(p, -1, 0) - np.roll(p, 1, 0)
        if not closed: d[0] = p[1]-p[0]; d[-1] = p[-1]-p[-2]
        nr = np.stack([-d[:, 1], d[:, 0]], 1); nr /= np.linalg.norm(nr, axis=1, keepdims=True) + 1e-9
        r = gaussian_filter1d(s.rng.normal(0, 1, n), smooth, mode='wrap' if closed else 'nearest')
        r = r - r.mean(); r /= max(r.std(), .35)
        return p + nr * (r*amp)[:, None]

    def mask(s, pts, amp=1.2, soft=.6):
        im = Image.new('L', (s.w, s.h), 0)
        p = s._T(s.wob(pts, amp) if amp else np.array(pts, float))
        ImageDraw.Draw(im).polygon([tuple(q) for q in p*s.S], fill=255)
        m = np.asarray(im, np.float32) / 255
        return gaussian_filter(m, soft*s.S) if soft else m

    def _bbox(s, a, pad=30):
        ys, xs = np.nonzero(a > .002)
        if len(ys) == 0: return None
        P = pad*s.S
        return (max(0, ys.min()-P), min(s.h, ys.max()+P), max(0, xs.min()-P), min(s.w, xs.max()+P))

    # ----- blending -----
    def multiply(s, a, color, op=1.):
        c = s.col(color); b = s._bbox(a, 2)
        if b is None: return
        y0, y1, x0, x1 = b; A = np.clip(a[y0:y1, x0:x1]*op, 0, 1)[..., None]
        s.img[y0:y1, x0:x1] *= 1 - A*(1 - c)

    def paint(s, a, color, op=1.):
        c = s.col(color); b = s._bbox(a, 2)
        if b is None: return
        y0, y1, x0, x1 = b; A = np.clip(a[y0:y1, x0:x1]*op, 0, 1)[..., None]
        s.img[y0:y1, x0:x1] = s.img[y0:y1, x0:x1]*(1 - A) + c*A

    def _darkness(s, b):
        y0, y1, x0, x1 = b
        L = s.img[y0:y1, x0:x1] @ np.array([.3, .59, .11])
        return np.clip((.52 - L)/.17, 0, 1)[..., None]

    def adapt(s, a, color, op=1.):
        """on light paper = multiply. On dark ground the same stroke becomes chalk (dark colours) or opaque paint (light colours)."""
        if not s.dark: return s.multiply(a, color, op)
        c = s.col(color); b = s._bbox(a, 2)
        if b is None: return
        y0, y1, x0, x1 = b; A = np.clip(a[y0:y1, x0:x1]*op, 0, 1)[..., None]
        D = s._darkness(b); lc = hexc(PAL['chalk']) if lum(c) < .45 else c
        cur = s.img[y0:y1, x0:x1]
        s.img[y0:y1, x0:x1] = (cur*(1 - A*(1 - c)))*(1 - D) + (cur*(1 - A) + lc*A)*D

    # ----- paper -----
    def _paper(s, kind):
        s.img *= (1 - .035*(s.hi - .5))[..., None]
        s.img *= (1 - .025*(s.low[0] - .5))[..., None]
        gc, gm = ('#7F9BE6', s.paint) if s.dark else (('#FFFFFF', s.paint) if s.tint else ('#B9CBE6', s.multiply))
        if kind == 'grid':
            L = Image.new('L', (s.w, s.h), 0); d = ImageDraw.Draw(L); g = 30*s.S
            for x in range(0, s.w, g): d.line([(x, 0), (x, s.h)], fill=255, width=max(1, s.S))
            for y in range(0, s.h, g): d.line([(0, y), (s.w, y)], fill=255, width=max(1, s.S))
            a = np.asarray(L, np.float32)/255 * (.55 + .45*s.low[1]) * (.6 + .4*s.tooth)
            gm(a, gc, .32 if s.dark else (.3 if s.tint else .55))
        elif kind == 'dots':
            L = Image.new('L', (s.w, s.h), 0); d = ImageDraw.Draw(L); g = 26*s.S; r = 1.3*s.S
            for x in range(g//2, s.w, g):
                for y in range(g//2, s.h, g): d.ellipse([x-r, y-r, x+r, y+r], fill=255)
            gm(np.asarray(L, np.float32)/255, gc, .7 if not s.dark else .4)
        elif kind == 'lined':
            L = Image.new('L', (s.w, s.h), 0); d = ImageDraw.Draw(L); g = 34*s.S
            for y in range(g*2, s.h, g): d.line([(0, y), (s.w, y)], fill=255, width=max(1, s.S))
            gm(np.asarray(L, np.float32)/255*(.6+.4*s.low[1]), gc, .6 if not s.dark else .35)

    # ----- watercolor -----
    def wash(s, a, color, op=.85, edge=.55, var=.35, gran=.3, soft=1.2, bloom=0):
        """soft watercolor wash: pigment variation + darker drying edge + granulation."""
        b = s._bbox(a, 20)
        if b is None: return
        y0, y1, x0, x1 = b; m = a[y0:y1, x0:x1]
        ms = gaussian_filter(m, soft*s.S)
        lo = s.low[s.rng.integers(3)][y0:y1, x0:x1]
        e = np.clip(m - gaussian_filter(m, 5*s.S), 0, 1) * edge * 2.2
        A = ms*op*(1 - var*.5 + var*lo) + e*ms
        if bloom: A *= 1 - bloom*np.clip(s.low[(s.rng.integers(3))][y0:y1, x0:x1]-.6, 0, 1)*2.5
        A *= 1 - gran*(s.mid[y0:y1, x0:x1] - .5) - gran*.6*(s.hi[y0:y1, x0:x1] - .5)
        full = np.zeros((s.h, s.w), np.float32); full[y0:y1, x0:x1] = np.clip(A, 0, 1)
        if s.dark or s.tint:   # gouache-white underpaint so watercolour reads on a dark / coloured card
            if s.dark: D = s._darkness(b)[..., 0]
            else: D = np.clip((.86 - s.img[y0:y1, x0:x1] @ np.array([.3, .59, .11]))/.08, 0, 1)
            u = np.zeros_like(full); u[y0:y1, x0:x1] = np.clip(ms*min(op*1.15, 1), 0, 1)*D
            s.paint(u, 'chalk', .96)
        s.multiply(full, color, 1)

    def lift(s, a, op=.85):
        """lift pigment back to paper (highlight)."""
        s.paint(gaussian_filter(a, .8*s.S)*(.85 + .15*s.tooth), PAL['white'] if (s.dark or s.tint) else s.base*255, op)

    # ----- pencil -----
    def pencil(s, pts, color='cobalt', w=1.6, op=.9, closed=False, amp=.6, press=.35, gaps=0., tooth=.55, blend='mul', clip=None):
        p = s._T(s.wob(pts, amp, closed, step=2.5, smooth=4) if amp else s._dens(pts, 2.5, closed))
        n = len(p)
        pr = 1 + press*gaussian_filter1d(s.rng.normal(0, 1, n), 8, mode='nearest')*2
        keep = np.ones(n, bool)
        if gaps > 0:
            g = gaussian_filter1d(s.rng.normal(0, 1, n), 10, mode='nearest')
            keep = g > np.quantile(g, gaps)
        L = Image.new('L', (s.w, s.h), 0); d = ImageDraw.Draw(L)
        for i in range(n - 1):
            if keep[i] and keep[i+1]:
                ww = max(1, w*pr[i]*s.S)
                d.line([tuple(p[i]*s.S), tuple(p[i+1]*s.S)], fill=255, width=int(round(ww)))
                r = ww/2; d.ellipse([p[i][0]*s.S-r, p[i][1]*s.S-r, p[i][0]*s.S+r, p[i][1]*s.S+r], fill=255)
        a = gaussian_filter(np.asarray(L, np.float32)/255, .5*s.S)
        a *= (1 - tooth) + tooth*s.tooth
        if clip is not None: a = a*clip
        (s.paint if blend == 'paint' else s.adapt)(a, color, op)

    def outline(s, pts, color='cobalt', w=2.4, op=.92, gaps=.14, heavy=(1, 1), closed=True):
        """broken cobalt outline, heavier on the shadow side (heavy = light-from direction flipped)."""
        p = s._dens(pts, 3, closed); c = p.mean(0)
        v = (p - c); v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-9
        side = np.clip(v @ (np.array(heavy)/np.linalg.norm(heavy)), 0, 1)
        segs = []; n = len(p)
        g = gaussian_filter1d(s.rng.normal(0, 1, n), 9, mode='wrap')
        keep = g > np.quantile(g, gaps)
        cur = []
        for i in range(n):
            if keep[i]: cur.append(i)
            elif cur: segs.append(cur); cur = []
        if cur: segs.append(cur)
        for sg in segs:
            if len(sg) < 3: continue
            ww = w*(.65 + .9*side[sg].mean())
            s.pencil(p[sg], color, ww, op, amp=.7, press=.3)

    def hatch(s, a, color='cobalt', angle=35, spacing=5, w=1., op=.45, jitter=1.2):
        """colored-pencil hatching clipped to mask a."""
        b = s._bbox(a, 0)
        if b is None: return
        y0, y1, x0, x1 = b
        L = Image.new('L', (s.w, s.h), 0); d = ImageDraw.Draw(L)
        cx, cy = (x0+x1)/2, (y0+y1)/2; R = max(x1-x0, y1-y0)
        t = np.radians(angle); dx, dy = np.cos(t), np.sin(t)
        for k in np.arange(-R, R, spacing*s.S):
            o = k + s.rng.normal(0, jitter*s.S)
            px, py = cx - dy*o, cy + dx*o
            d.line([(px - dx*R, py - dy*R), (px + dx*R, py + dy*R)], fill=255, width=max(1, int(w*s.S)))
        h = np.asarray(L, np.float32)/255 * a * (.35 + .65*s.tooth)
        s.multiply(h, color, op)

    # ----- text -----
    def text(s, t, xy, size, color='ink', font=HAND, op=.95, angle=0, anchor='la', wght=None, spacing=0, blend='mul'):
        f = ImageFont.truetype(font, int(size*s.S))
        if wght:
            try: f.set_variation_by_axes([wght])
            except Exception: pass
        if spacing:
            ws = [f.getlength(ch) + spacing*size*s.S for ch in t]; tw = sum(ws)
        else: tw = f.getlength(t)
        asc, desc = f.getmetrics(); th = asc + desc
        im = Image.new('L', (int(tw + 20*s.S), int(th + 20*s.S)), 0); d = ImageDraw.Draw(im)
        if spacing:
            x = 10*s.S
            for ch, wch in zip(t, ws): d.text((x, 10*s.S), ch, font=f, fill=255); x += wch
        else: d.text((10*s.S, 10*s.S), t, font=f, fill=255)
        if angle: im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
        xy = s._T(xy); x, y = xy[0]*s.S, xy[1]*s.S
        if anchor[0] == 'm': x -= im.width/2
        elif anchor[0] == 'r': x -= im.width - 10*s.S
        else: x -= 10*s.S
        if anchor[1] == 'm': y -= im.height/2
        else: y -= 10*s.S
        L = Image.new('L', (s.w, s.h), 0); L.paste(im, (int(x), int(y)))
        a = np.asarray(L, np.float32)/255 * (.8 + .2*s.tooth)
        (s.paint if blend == 'paint' else s.adapt)(a, color, op)   # light text on a dark card: blend='paint'
        return tw/s.S

    # ----- journal pieces -----
    def leader(s, p0, p1, curl=1, color='ink', w=1.25, loop=9, bend=.35):
        """curly leader line like a hand-drawn pointer: object -> label, small loop near label end."""
        p0, p1 = np.array(p0, float), np.array(p1, float); d = p1 - p0
        nrm = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-9)
        pm = p0 + d*.68 + nrm*np.linalg.norm(d)*bend*.25*curl
        a = bezier(p0, p0 + d*.3 + nrm*np.linalg.norm(d)*bend*curl, pm, n=40)
        dirv = (a[-1] - a[-3]); dirv /= np.linalg.norm(dirv) + 1e-9
        side = np.array([-dirv[1], dirv[0]])*curl
        c = pm + side*loop
        st = np.arctan2(*(pm - c)[::-1])
        ang = st + np.linspace(0, 2*np.pi*curl, 30)
        lp = np.stack([c[0] + loop*np.cos(ang), c[1] + loop*np.sin(ang)], 1)
        b = bezier(pm, pm + (p1 - pm)*.4 - side*8, p1, n=25)
        s.pencil(np.vstack([a, lp, b]), color, w, .9, amp=.35, press=.25)

    def label(s, t, xy, size=34, color='ink', font=HAND, angle=0, anchor='la', wght=500):
        return s.text(t, xy, size, color, font, .95, angle, anchor, wght)

    def card(s, pts, border=6, fill='white', shadow=(5, 7), sh_op=.2, amp=1.):
        """sticker-bordered cut-out: shadow + white border; returns inner mask for content."""
        m = s.mask(pts, amp, .5)
        b = s._bbox(m, border + 20); y0, y1, x0, x1 = b
        sub = m[y0:y1, x0:x1] > .5
        out = np.zeros_like(m)
        out[y0:y1, x0:x1] = gaussian_filter((distance_transform_edt(~sub) <= border*s.S).astype(np.float32), .6*s.S)
        sh = np.roll(np.roll(out, int(shadow[1]*s.S), 0), int(shadow[0]*s.S), 1)
        s.multiply(gaussian_filter(sh, 2.5*s.S), '#4A5A8A', sh_op)
        s.paint(out, fill, 1)
        return m

    def tape(s, x, y, w=110, h=30, ang=0, color='sky', op=.5, text=None, tsize=26, tcolor='cobalt'):
        pts = [(x - w/2, y - h/2), (x + w/2, y - h/2)]
        pts += [(x + w/2 + s.rng.uniform(-3, 3), y - h/2 + h*i/6) for i in range(1, 6)]
        pts += [(x + w/2, y + h/2), (x - w/2, y + h/2)]
        pts += [(x - w/2 + s.rng.uniform(-3, 3), y + h/2 - h*i/6) for i in range(1, 6)]
        m = s.mask(transform(pts, x, y, ang), .4, .4)
        if s.dark or s.tint: op = max(op, .85 if s.dark else .78)   # washi on a dark / coloured card must stay light
        s.paint(m*(.85 + .15*s.mid), color, op)
        s.multiply(m*.25, color, 1)
        if text: s.text(text, (x, y), tsize, tcolor, HAND, .95, -ang, 'mm', 600)

    def sparkle(s, x, y, r=10, color='coral', op=.9, mode='wash'):
        m = s.mask(sparkle_pts(x, y, r), .3, .4)
        if mode == 'paint': s.paint(m, color, op)
        else: s.wash(m, color, op, edge=.2, gran=.15)

    def sunburst(s, x, y, r=50, color='coral', rays=26, op=.85):
        for i in range(rays):
            a = 2*np.pi*i/rays + s.rng.normal(0, .03); r0 = r*(.42 if i % 2 else .55); r1 = r*(1 if i % 2 else .8)
            s.pencil([(x + r0*np.cos(a), y + r0*np.sin(a)), (x + r1*np.cos(a), y + r1*np.sin(a))], color, 1.4, op, amp=.2, press=.2)
        for i in range(36):
            a = 2*np.pi*i/36; rr = r*1.18
            m = s.mask(ellipse(x + rr*np.cos(a), y + rr*np.sin(a), 1.4, 1.4, n=10), 0, .3)
            s.multiply(m, color, op)
        s.sparkle(x, y, r*.28, color)

    def dots(s, a, color, r=3, spacing=11, op=.8):
        b = s._bbox(a, 0)
        if b is None: return
        y0, y1, x0, x1 = b; L = Image.new('L', (s.w, s.h), 0); d = ImageDraw.Draw(L); g = spacing*s.S; rr = r*s.S
        for j, yy in enumerate(range(y0, y1, g)):
            for xx in range(x0 + (g//2 if j % 2 else 0), x1, g): d.ellipse([xx-rr, yy-rr, xx+rr, yy+rr], fill=255)
        s.wash(np.asarray(L, np.float32)/255*(a > .5), color, op, edge=.2, gran=.2, soft=.4)

    # ----- signature stamps: little wolf (her) & little owl (me) -----
    def ink(s, a, color, op=.88):
        """rubber-stamp ink: patchy, paper tooth shows through."""
        b = s._bbox(a, 2)
        if b is None: return
        lo = s.low[2]; t = np.clip((s.hi - .12)*2.2, 0, 1)
        s.adapt(a*(.62 + .38*lo)*(.45 + .55*t), color, op)

    def knock(s, a, op=.92):
        b = s._bbox(a, 2)
        if b is None: return
        y0, y1, x0, x1 = b; A = np.clip(a[y0:y1, x0:x1]*op, 0, 1)[..., None]
        s.img[y0:y1, x0:x1] = s.img[y0:y1, x0:x1]*(1 - A) + s.paper0[y0:y1, x0:x1]*A

    def wolf_stamp(s, x, y, size=1., ang=0, color='wolf', eye='lilac', text='little wolf'):
        """pure-animal little grey wolf head in a round stamp ring (draw at (x,y), radius ~36*size)."""
        if s.dark and color == 'wolf': color = 'silver'
        with s.at((0, 0), size, (x, y), ang):
            s.pencil(ellipse(0, 0, 36, 36), color, 2.4, .85, closed=True, amp=.5, tooth=.8)
            s.pencil(ellipse(0, 0, 31, 31), color, 1.0, .6, closed=True, amp=.4, gaps=.2, tooth=.8)
            head = [(-15, -25), (-7, -11), (0, -12), (7, -11), (15, -25), (19, -8), (22, 3), (13, 12),
                    (5, 19), (0, 21), (-5, 19), (-13, 12), (-22, 3), (-19, -8)]
            s.ink(s.mask(head, .5, .4), color)
            for sx in (-1, 1):
                s.knock(s.mask([(sx*13, -19), (sx*9, -11), (sx*16, -9)], .2, .3), .8)
                s.knock(s.mask(ellipse(sx*8, -1, 3.6, 4.2), .2, .3))
                s.paint(s.mask(ellipse(sx*8, 0, 2.2, 2.6), .1, .3), eye, .95)
            s.knock(s.mask(ellipse(0, 12, 9, 7), .3, .4), .55)
            s.ink(s.mask(ellipse(0, 9, 3.2, 2.4), .1, .3), 'ink', .9)
        if text: s.text(text, (x, y + 44*size), 15*size + 4, color, HAND, .8, -ang, 'ma', 600)

    def owl_stamp(s, x, y, size=1., ang=0, color='owl', eye='amber', text='little owl'):
        """little owl in a rounded-square stamp frame."""
        with s.at((0, 0), size, (x, y), ang):
            s.pencil(rrect(-34, -34, 34, 34, 10), color, 2.2, .85, closed=True, amp=.5, tooth=.8)
            body = np.vstack([ellipse(0, 5, 19, 22)[:45][::-1]*[1, 1], [(-17, -10), (-15, -26), (-7, -15), (0, -16), (7, -15), (15, -26), (17, -10)]])
            s.ink(s.mask(ellipse(0, 5, 19, 22), .5, .4), color)
            s.ink(s.mask([(-17, -6), (-16, -26), (-6, -14), (6, -14), (16, -26), (17, -6)], .4, .4), color)
            for sx in (-1, 1):
                s.knock(s.mask(ellipse(sx*8, -4, 7.5, 7.5), .3, .3))
                s.paint(s.mask(ellipse(sx*8, -4, 3.8, 3.8), .1, .3), eye, .95)
                s.ink(s.mask(ellipse(sx*8, -4, 1.6, 1.6, n=10), 0, .3), 'ink', .9)
            s.paint(s.mask([(-3, 3), (3, 3), (0, 9)], .1, .3), eye, .95)
            for (bx, by) in [(-6, 15), (0, 18), (6, 15), (-3, 21), (3, 21)]:
                s.knock(s.mask([(bx-2.5, by-1.5), (bx, by+1.5), (bx+2.5, by-1.5)], 0, .3), .6)
        if text: s.text(text, (x, y + 42*size), 15*size + 4, color, HAND, .8, -ang, 'ma', 600)

    def render(s, path=None, q=93):
        im = Image.fromarray((np.clip(s.img, 0, 1)*255).astype(np.uint8))
        if path: im.save(path, quality=q)
        return im
