import argparse
import io
import math
import os
import zipfile
from collections import Counter
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_GAME = r"C:\Steam\steamapps\common\Divine Frequency"
DEFAULT_IPK3 = os.path.join(DEFAULT_GAME, "DFSDSA.ipk3")
DEFAULT_TTF = os.path.join(ROOT, "source", "fonts", "noto-sans.ttf")
DEFAULT_OUT_ROOT = os.path.join(ROOT, "work", "Fonts")

CHARS = (
    [chr(c) for c in range(0x0410, 0x0430)]
    + [chr(c) for c in range(0x0430, 0x0450)]
    + ["Ё", "ё"]
    + [chr(c) for c in (0x2013, 0x2014, 0x2026, 0x2116, 0x2018, 0x2019, 0x201C, 0x201D, 0x00AB, 0x00BB)]
)

UI_PROFILES = {
    "RU_DF_FONT": {"space": 9, "kerning": -1, "canvas_h": 28, "font_size": 18, "left_pad": 1, "right_pad": 1, "y": 1},
    "RU_ChatBoxFont": {"space": 5, "kerning": -1, "canvas_h": 28, "font_size": 18, "left_pad": 1, "right_pad": 1, "y": 1},
    "RU_CONVO_FONT": {"space": 10, "kerning": 0, "canvas_h": 28, "font_size": 18, "left_pad": 1, "right_pad": 1, "y": 1},
}

NPC_NAME = "RU_npcfont"


def glyph_name(ch):
    return f"{ord(ch):04X}.png"


def render_glyph(font, ch, profile):
    bbox = font.getbbox(ch)
    advance = font.getlength(ch)
    width = max(
        1,
        int(math.ceil(advance)) + profile["left_pad"] + profile["right_pad"],
        int(bbox[2]) + profile["left_pad"] + profile["right_pad"],
    )
    img = Image.new("RGBA", (width, profile["canvas_h"]), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((profile["left_pad"], profile["y"]), ch, font=font, fill=(255, 255, 255, 255))
    return img


def load_dvffn(ipk3):
    glyphs = {}
    z = zipfile.ZipFile(ipk3)
    for e in z.infolist():
        name = e.filename
        if not name.startswith("HiRes/DF_FONT/DVFFN") or not name.lower().endswith(".png"):
            continue
        base = os.path.splitext(os.path.basename(name))[0]
        try:
            code = int(base[5:], 10)
        except ValueError:
            continue
        glyphs[chr(code)] = Image.open(io.BytesIO(z.read(name))).convert("RGBA")
    z.close()
    return glyphs


def load_npc(ipk3):
    glyphs = {}
    z = zipfile.ZipFile(ipk3)
    for e in z.infolist():
        name = e.filename
        if not name.startswith("Fonts/npcfont/") or not name.lower().endswith(".png"):
            continue
        base = os.path.splitext(os.path.basename(name))[0]
        try:
            code = int(base, 16)
        except ValueError:
            continue
        glyphs[chr(code)] = Image.open(io.BytesIO(z.read(name))).convert("RGBA")
    z.close()
    return glyphs


def write_font_inf(path, space, kerning, scale=1.0, translation=True):
    lines = [f"SpaceWidth {space}", f"Kerning {kerning}", f"Scale {scale}"]
    if translation:
        lines.append("TranslationType Standard")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def make_ui_fonts(glyphs, ttf, out_root):
    for name, profile in UI_PROFILES.items():
        out = os.path.join(out_root, name)
        os.makedirs(out, exist_ok=True)
        for f in os.listdir(out):
            if f.lower().endswith(".png"):
                os.remove(os.path.join(out, f))

        for ch, img in glyphs.items():
            img.save(os.path.join(out, glyph_name(ch)))

        font = ImageFont.truetype(ttf, profile["font_size"])
        generated = 0
        for ch in CHARS:
            if ch in glyphs:
                continue
            render_glyph(font, ch, profile).save(os.path.join(out, glyph_name(ch)))
            generated += 1

        write_font_inf(os.path.join(out, "font.inf"), profile["space"], profile["kerning"])
        print(f"UI font {name}: {len(glyphs)} original + {generated} generated glyphs -> {out}")


def npc_gradient(glyphs):
    ref = glyphs.get("A")
    if ref is None:
        return [(210, 155, 85, 255)] * 16
    rows = []
    px = ref.load()
    for y in range(ref.height):
        c = Counter()
        for x in range(ref.width):
            r, g, b, a = px[x, y]
            if a and r > 150 and g > 100:
                c[(r, g, b, a)] += 1
        if c:
            rows.append(c.most_common(1)[0][0])
    return rows or [(210, 155, 85, 255)] * 16


def npc_glyph(ch, ttf, gradient):
    font = ImageFont.truetype(ttf, 20)
    bbox = font.getbbox(ch)
    w, h = max(1, bbox[2] - bbox[0]), max(1, bbox[3] - bbox[1])
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((-bbox[0], -bbox[1]), ch, font=font, fill=255)
    mask = mask.point(lambda v: 255 if v > 110 else 0)
    mask = mask.filter(ImageFilter.MaxFilter(3))
    mask = mask.resize((20, 20), Image.Resampling.NEAREST)

    canvas = Image.new("RGBA", (23, 27), (0, 0, 0, 0))
    outline = mask.filter(ImageFilter.MaxFilter(3))
    shadow = Image.new("L", (23, 27), 0)
    shadow.paste(outline, (2, 2))
    canvas.paste((11, 11, 11, 255), (0, 0), shadow)
    canvas.paste((51, 30, 10, 255), (1, 3), outline)

    fill = Image.new("RGBA", (23, 27), (0, 0, 0, 0))
    p = fill.load()
    for y in range(20):
        col = gradient[min(len(gradient) - 1, int(y * len(gradient) / 20))]
        for x in range(23):
            if 0 <= x - 1 < 20 and mask.getpixel((x - 1, y)):
                p[x, y + 3] = col
    canvas.alpha_composite(fill)
    return canvas


def make_npc_font(glyphs, ttf, out_root):
    out = os.path.join(out_root, NPC_NAME)
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.lower().endswith(".png"):
            os.remove(os.path.join(out, f))

    for ch, img in glyphs.items():
        img.save(os.path.join(out, glyph_name(ch)))

    gradient = npc_gradient(glyphs)
    generated = 0
    for ch in CHARS:
        if ch in glyphs:
            continue
        if ch.islower():
            continue
        img = npc_glyph(ch, ttf, gradient)
        img.save(os.path.join(out, glyph_name(ch)))
        generated += 1
        lower = ch.lower()
        if lower != ch and lower not in glyphs:
            img.save(os.path.join(out, glyph_name(lower)))

    write_font_inf(os.path.join(out, "font.inf"), 5, -3, scale=1.2, translation=False)
    print(f"NPC font {NPC_NAME}: {len(glyphs)} original + {generated} generated pairs -> {out}")


def draw_line(glyphs, text, space, kerning, canvas_h):
    widths = []
    for ch in text:
        img = glyphs.get(ch)
        widths.append((img.width if img else space) + kerning)
    line = Image.new("RGBA", (max(1, sum(widths)), canvas_h), (0, 0, 0, 0))
    x = 0
    for ch, w in zip(text, widths):
        img = glyphs.get(ch)
        if img is not None:
            line.alpha_composite(img, (x, 0))
        x += w
    return line


def make_preview(glyphs, out_path, samples, space, kerning, canvas_h, scale=1.0, background=(20, 20, 20, 255)):
    rendered = []
    for s in samples:
        line = draw_line(glyphs, s, space, kerning, canvas_h)
        if scale != 1.0:
            line = line.resize((max(1, int(line.width * scale)), max(1, int(line.height * scale))), Image.Resampling.LANCZOS)
        rendered.append(line)
    w = max(i.width for i in rendered) + 12
    h = sum(i.height + 3 for i in rendered) + 12
    sheet = Image.new("RGBA", (w, h), background)
    y = 6
    for i in rendered:
        sheet.alpha_composite(i, (6, y))
        y += i.height + 3
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    sheet.save(out_path)
    print(f"Preview: {out_path} ({sheet.width}x{sheet.height})")


def main():
    ap = argparse.ArgumentParser(description="Generate Cyrillic UI fonts for Divine Frequency")
    ap.add_argument("--ttf", default=DEFAULT_TTF)
    ap.add_argument("--out-root", default=DEFAULT_OUT_ROOT)
    ap.add_argument("--ipk3", default=DEFAULT_IPK3)
    ap.add_argument("--ui-only", action="store_true")
    ap.add_argument("--npc-only", action="store_true")
    args = ap.parse_args()

    dvffn = load_dvffn(args.ipk3)
    npc = load_npc(args.ipk3)

    if not args.npc_only:
        make_ui_fonts(dvffn, args.ttf, args.out_root)
        ui_preview = {}
        for name, profile in UI_PROFILES.items():
            generated = {}
            for ch in CHARS:
                p = os.path.join(args.out_root, name, glyph_name(ch))
                if os.path.isfile(p):
                    generated[ch] = Image.open(p).convert("RGBA")
            glyphs = dict(dvffn)
            glyphs.update(generated)
            ui_preview[name] = (glyphs, profile)
        glyphs, profile = ui_preview["RU_DF_FONT"]
        make_preview(
            glyphs,
            os.path.join(ROOT, "work", "preview_ui_font.png"),
            ["Inventory", "Инвентарь", "Health / Здоровье", "Armor / Броня", "Ammo / Патроны", "АКТ I — Метемпсихоз", "Ёжик, «кавычки», …"],
            profile["space"],
            profile["kerning"],
            profile["canvas_h"],
        )

    if not args.ui_only:
        make_npc_font(npc, args.ttf, args.out_root)
        preview = dict(npc)
        for ch in CHARS:
            if ch in preview:
                continue
            upper = ch.upper()
            p = os.path.join(args.out_root, NPC_NAME, glyph_name(upper))
            if os.path.isfile(p):
                preview[ch] = Image.open(p).convert("RGBA")
        make_preview(
            preview,
            os.path.join(ROOT, "work", "preview_npc_font.png"),
            ["АКТ I — Метемпсихоз", "ВАСЁК", "ПСИХУС", "ЗДОРОВЬЕ", "ЭНЕРГИЯ"],
            5,
            -3,
            27,
            scale=1.0,
            background=(20, 20, 20, 255),
        )


if __name__ == "__main__":
    main()
