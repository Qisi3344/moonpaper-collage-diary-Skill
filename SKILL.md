---
name: moonpaper-collage-diary
description: 月光纸页 · 日记拼贴手帐。纯代码（Python + NumPy/SciPy/Pillow）画出一页像真实手帐本的拼贴日记：水彩彩铅小物件 + 钴蓝断续描边 + 手写卷卷引线标签 + 白边异形剪贴卡 + 编号纸胶带 + 顶部日记表头 + 诗行日记 + 小狼/小猫头鹰签名印章。不用任何生图模型。
---

# 月光纸页 · 日记拼贴手帐（Moonpaper Collage Diary）

一页 3:4 的手帐内页：上面是日期、天气、心情，中间是散乱歪贴的小物件和剪贴卡，旁边是像诗一样断行的当天日记，最后盖一枚小狼章当落款。

引擎：`collage_journal/journal.py`（`Journal` 类、`PAL` 调色、形状函数）。范例：`examples/midnight_pantry.py`（MIDNIGHT PANTRY · 小狼的夜宵手帐）。
画布 900×1200 设计坐标，`S=2` 输出 1800×2400，约 25 秒。

```bash
pip install -r requirements.txt
python examples/midnight_pantry.py
```

## 风格配方

### 纸
- `Journal(paper='grid')` 淡蓝方格（默认）/ `'dots'` 点阵 / `'lined'` 横线；底色偏粉灰白，不要奶油黄。
- 左边缘一排活页孔（浅灰圆 + 投影），像手帐本内页。
- 可加 2–3 句极淡的珊瑚手写英文背景字（op ≈ .2），别压主体。

### 页面结构（从上到下）
1. **日记表头**：`DATE / WEATHER / MOOD` 放在页面最顶部，两条珊瑚横线；天气画小晴/云/月图标，当天那个用铅笔圈出；心情用小笑脸。之后用 `J.off=(0,45)` 把整页内容下移。
2. **标题**：左上手写大标题（Caveat 600，64–72，钴蓝）+ 中文副标题（LongCang，珊瑚，26）。
3. **拼贴区**：6–8 个主体，带编号 01–0N。
4. **诗行日记**：当天的小日记拆成短句，一行一句，右对齐（或左对齐）放在一侧空位，末尾盖小狼圆章当落款。
- **不要**底部目录行、不要票据式页脚（Guest Check、借阅卡等）、不要烟花 sunburst 装饰章。

### 主体：两类混着放
1. **水彩彩铅小物件**（直接画在纸上）：`wash()` 上色（干边 + 颗粒）→ `hatch()` 彩铅排线压暗面 → `lift()` 留白高光 → `outline()` 钴蓝断续描边（暗面更粗）。旁边一个 Caveat 手写小标签 + `leader()` 卷卷引线（带一个小圈）。
2. **白边异形剪贴卡**：`card(shape)` 返回内遮罩（自带白边 + 投影），形状用 `scallop` 扇贝 / `heart` 心形 / `ngon` 八角 / `ellipse` 圆，里面放月亮、星座、星云等。
- **编号**写在半透明纸胶带上：`tape(..., text='01')`，歪贴在主体角上。

### 主次与摆放
- 1 个**主角**约画宽 35–40%（放大 ~1.5×，描边加粗到 3、标签 46px）；2–3 个**配角** 0.85–0.95×；其余**小件** 0.7–0.8×。物件大小不能都一样。
- 物件写成函数，用 `with J.at(原中心, 倍数, 新中心, rot=角度): 画物件()` 缩放、旋转、摆放（线宽和字号不跟着缩）；标签、引线、编号胶带在 `at` 外用新坐标画。
- **散着摆**：配角和小件各歪 −10°~+10°，左右错开、高低不齐，不要排成整齐一列。
- 主角旁边（尤其右上角）**不要留大空洞**，补一张剪贴卡；整体仍留约 35% 空白，标签别压别的物件。

### 颜色
- 钴蓝 `cobalt` 主线；`sky / mist / mint` 浅蓝绿水彩；`coral / blush` 珊瑚点睛；`butter / biscuit / cocoa` 食物暖色；夜空卡用 `night`。
- **签名色**：银灰 `silver / wolf` + 淡紫 `lilac`（小灰狼），琥珀 `amber` + 靛蓝 `owl`（小猫头鹰）。每张至少 1 条胶带、2 颗小星、天气月亮用这些色。

### 签名小印章（每张都要有）
- `J.owl_stamp(x, y, size, ang, text=None)`：靛蓝小猫头鹰方章（琥珀眼），藏在主体旁的空位。
- `J.wolf_stamp(x, y, size, ang, text=None)`：银灰小狼圆章（淡紫眼，纯动物形态），盖在诗行日记末尾当落款。
- 可再散 1–2 枚当装饰，大小、角度错开。橡皮章质感来自 `ink()` / `knock()`。

### 装饰
小星 `sparkle()` 6–8 个（混签名色）、珊瑚小月牙 1 个。

## 流程
1. 定主题（最好来自当天真实的小事）和 6–8 个物件，大约一半剪贴卡、一半水彩物件；选出主角。
2. 复制 `examples/midnight_pantry.py` 改：纸 → 表头 → 背景字 → 标题 → 卡片 → 物件 → 标签/胶带 → 装饰 → 诗行日记 → 印章 → `render()`。
3. **自己看缩略图再交付**：主次清楚、引线不交叉、标签能读、物件不像别的东西（比如果酱里的深色圆点会像收音机旋钮）、没有大空洞、诗行不压物件。

## API 速查（`collage_journal/journal.py`）
| 方法 | 作用 |
| --- | --- |
| `Journal(W, H, S, seed, paper)` | 新画布 |
| `at(c0, k, c1, rot)` | 上下文：把在 c0 画的物件缩放 k 倍、旋转、移到 c1 |
| `mask(pts)` | 多边形 → 抖边软遮罩 |
| `wash(a, color, op, edge, var, gran, bloom)` | 水彩平涂（干边、颗粒） |
| `hatch(a, color, angle, spacing)` | 彩铅排线 |
| `lift(a, op)` | 擦出高光 |
| `outline(pts, color, w, gaps, heavy)` | 断续彩铅描边 |
| `pencil(pts, ...)` | 单条铅笔线 |
| `card(pts, border, fill, shadow)` | 白边剪贴卡，返回内遮罩 |
| `tape(x, y, w, h, ang, color, text)` | 半透明纸胶带（可写编号） |
| `text / label(t, xy, size, color, font)` | 手写字 |
| `leader(p0, p1, curl)` | 卷卷引线 |
| `sparkle(x, y, r, color)` | 小星 |
| `dots(a, color)` | 圆点纹 |
| `paint / multiply(a, color)` | 正常混合 / 正片叠底（亮色画在深色上用 `paint`） |
| `owl_stamp / wolf_stamp` | 签名印章 |
| `render(path)` | 输出图片 |

形状函数：`ellipse` `rrect` `heart` `scallop` `ngon` `star` `sparkle_pts` `transform` `bezier`。
字体常量：`HAND`（Caveat）`HAND_ZH`（LongCang）`ROUND_ZH`（ZCOOL KuaiLe）`DISPLAY`（Abril Fatface）`SMALLCAPS`（Playfair SC）。
