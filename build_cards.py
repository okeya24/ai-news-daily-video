#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日 AI 速递 · 铅笔素描风竖屏卡片生成模板（9:16, 1080x1920）"""
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
OUT = os.path.join(BASE, "output", "cards")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1920
PAPER = (244, 239, 228)
INK = (38, 36, 33)
GRAY = (96, 92, 84)
BROWN = (138, 109, 59)
LINE = (70, 66, 58)

SERIF_B = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SANS_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SANS_M = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"

def font(path, size, index=2):
    return ImageFont.truetype(path, size, index=index)

def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines

def cover_crop(img, tw, th):
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2; y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))

def base_canvas():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # 纸张轻微纹理边框
    d.rectangle((36, 36, W - 36, H - 36), outline=LINE, width=3)
    d.rectangle((48, 48, W - 48, H - 48), outline=(180, 170, 150), width=1)
    return img, d

def header(d, date_str):
    d.text((80, 86), "AI 新闻边角料", font=font(SERIF_B, 38), fill=INK)
    tw = d.textlength(date_str, font=font(SANS_R, 26))
    d.text((W - 80 - tw, 96), date_str, font=font(SANS_R, 26), fill=GRAY)
    d.line((80, 152, W - 80, 152), fill=LINE, width=2)

def news_card(idx, num, img_name, title, summary, date_str):
    img, d = base_canvas()
    header(d, date_str)

    # 插画区
    ix, iy, iw, ih = 80, 210, 920, 1000
    sketch = Image.open(os.path.join(ASSETS, img_name)).convert("RGB")
    sketch = cover_crop(sketch, iw, ih)
    img.paste(sketch, (ix, iy))
    d.rectangle((ix, iy, ix + iw, iy + ih), outline=LINE, width=3)

    # 编号
    d.text((80, 1280), num, font=font(SERIF_B, 100), fill=BROWN)
    # 标题
    tf = font(SERIF_B, 44)
    ty = 1410
    for line in wrap(d, title, tf, 920)[:2]:
        d.text((240, ty), line, font=tf, fill=INK)
        ty += 58
    # 摘要
    sf = font(SANS_R, 30)
    sy = max(ty + 30, 1560)
    for line in wrap(d, summary, sf, 920)[:4]:
        d.text((80, sy), line, font=sf, fill=GRAY)
        sy += 50
    # 底部
    d.line((80, 1830, W - 80, 1830), fill=(180, 170, 150), width=1)
    d.text((80, 1850), "全球 AI 热点 · 每日五条", font=font(SANS_R, 22), fill=GRAY)
    img.save(os.path.join(OUT, f"{idx:02d}_news{num}.png"), quality=95)

def intro_card(date_str):
    img, d = base_canvas()
    d.text((80, 86), "AI 新闻边角料", font=font(SERIF_B, 38), fill=INK)
    tw = d.textlength(date_str, font=font(SANS_R, 26))
    d.text((W - 80 - tw, 96), date_str, font=font(SANS_R, 26), fill=GRAY)
    d.line((80, 152, W - 80, 152), fill=LINE, width=2)

    eng = "DAILY AI BRIEFING"
    ef = font(SANS_M, 30)
    ew = d.textlength(eng, font=ef)
    d.text(((W - ew) / 2, 700), eng, font=ef, fill=BROWN)
    # 居中大标题
    big = "AI 新闻边角料"
    bf = font(SERIF_B, 84)
    bw = d.textlength(big, font=bf)
    d.text(((W - bw) / 2, 800), big, font=bf, fill=INK)
    # 装饰双线
    d.line((300, 960, W - 300, 960), fill=LINE, width=2)
    d.line((360, 980, W - 360, 980), fill=(180, 170, 150), width=1)
    sub = f"{date_str} · 全球 AI 热点五条"
    suf = font(SANS_R, 32)
    sw = d.textlength(sub, font=suf)
    d.text(((W - sw) / 2, 1060), sub, font=suf, fill=GRAY)
    note = "铅笔素描新闻版"
    nf = font(SANS_R, 24)
    nw = d.textlength(note, font=nf)
    d.text(((W - nw) / 2, 1700), note, font=nf, fill=GRAY)
    img.save(os.path.join(OUT, "00_intro.png"), quality=95)

def outro_card():
    img, d = base_canvas()
    t1 = "感谢观看"
    f1 = font(SERIF_B, 72)
    w1 = d.textlength(t1, font=f1)
    d.text(((W - w1) / 2, 720), t1, font=f1, fill=INK)
    t2 = "关注我，带你看全球 AI 边角料"
    f2 = font(SANS_R, 32)
    w2 = d.textlength(t2, font=f2)
    d.text(((W - w2) / 2, 880), t2, font=f2, fill=GRAY)
    t3 = "我们明天见"
    f3 = font(SERIF_B, 44)
    w3 = d.textlength(t3, font=f3)
    d.text(((W - w3) / 2, 1020), t3, font=f3, fill=BROWN)
    img.save(os.path.join(OUT, "06_outro.png"), quality=95)

if __name__ == "__main__":
    # 日期默认取当天；示例 news 列表为模板样例，每日由选题流程替换
    DATE = datetime.now().strftime("%Y.%m.%d")
    intro_card(DATE)
    news = [
        ("01", "news1.jpg", "Anthropic IPO 获六倍认购",
         "最高募资 904 亿美元、估值或冲 1.5 万亿；英伟达基石认购生变，估值泡沫争议四起"),
        ("02", "news2.jpg", "谷歌发布 Gemini 4 Hydrogen",
         "Orchestrator 可中途自动切换模型，官方称省 24% 配额、快 19%；数据尚待第三方复核"),
        ("03", "news3.jpg", "DeepSeek 开放应用能力 API",
         "搜索、文件、读取与语音能力上线；数据安全与语音滥用边界受关注"),
        ("04", "news4.jpg", "MiniMax 开源 4K 生图模型",
         "支持文生图、参考图与编辑，最高 4096×4096；部署门槛与图片版权仍有争议"),
        ("05", "news5.jpg", "开源 Agent 霸榜 GitHub 周榜",
         "agent-desktop 周增超 1.2 万星登顶；多数项目缺独立安全审计，越权风险需警惕"),
    ]
    for i, (num, im, title, summary) in enumerate(news, start=1):
        news_card(i, num, im, title, summary, DATE)
    outro_card()
    print("cards done:", sorted(os.listdir(OUT)))
