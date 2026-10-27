import argparse
import io
import math
import os
import zipfile

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_GAME = r"C:\Steam\steamapps\common\Divine Frequency"
DEFAULT_IPK3 = os.path.join(DEFAULT_GAME, "DFSDSA.ipk3")
DEFAULT_TTF = os.path.join(ROOT, "source", "fonts", "noto-sans.ttf")
if not os.path.isfile(DEFAULT_TTF):
    DEFAULT_TTF = os.path.join(ROOT, "source", "engine", "ui", "noto", "noto-sans.ttf")
DEFAULT_OUT_ROOT = os.path.join(ROOT, "work", "Fonts")
DEFAULT_PREVIEW = os.path.join(ROOT, "work", "preview_bigfont.png")

PROFILES = {
    "bigfont": {"canvas_h": 46, "font_size": 32, "left_pad": 1, "right_pad": 1, "y": 0},
    "ACS_FONT": {"canvas_h": 32, "font_size": 24, "left_pad": 1, "right_pad": 0, "y": 0},
}

CHARS = (
    [chr(c) for c in range(0x0410, 0x0430)]
    + [chr(c) for c in range(0x0430, 0x0450)]
    + ["Ё", "ё"]
    + [chr(c) for c in (0x2013, 0x2014, 0x2026, 0x2116, 0x2018, 0x2019, 0x201C, 0x201D)]
)


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


def load_bigfont(ipk3):
    z = zipfile.ZipFile(ipk3)
    glyphs = {}
    for e in z.infolist():
        if not e.filename.startswith("Fonts/bigfont/") or not e.filename.lower().endswith(".png"):
            continue
        base = os.path.splitext(os.path.basename(e.filename))[0]
        try:
            code = int(base, 16)
        except ValueError:
            continue
        glyphs[chr(code)] = Image.open(io.BytesIO(z.read(e.filename))).convert("RGBA")
    z.close()
    return glyphs


def draw_line(glyphs, text):
    widths = sum(glyphs[ch].width if ch in glyphs else 8 for ch in text)
    line = Image.new("RGBA", (max(1, widths), 46), (0, 0, 0, 0))
    x = 0
    for ch in text:
        img = glyphs.get(ch)
        if img is None:
            x += 8
            continue
        line.alpha_composite(img, (x, 0))
        x += img.width
    return line


def make_preview(glyphs, out_path):
    samples = [
        "New Game", "Новая игра",
        "Options", "Настройки",
        "Load Game", "Загрузить игру",
        "Save Game", "Сохранить игру",
        "Credits", "Титры",
        "Quit", "Выход",
    ]
    scale = 1 / 3
    rendered = []
    for s in samples:
        line = draw_line(glyphs, s)
        rendered.append(line.resize(
            (max(1, int(line.width * scale)), max(1, int(line.height * scale))),
            Image.Resampling.LANCZOS,
        ))
    w = max(i.width for i in rendered) + 12
    h = sum(i.height + 2 for i in rendered) + 12
    sheet = Image.new("RGBA", (w, h), (20, 20, 20, 255))
    y = 6
    for i in rendered:
        sheet.alpha_composite(i, (6, y))
        y += i.height + 2
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    sheet.save(out_path)
    print(f"Preview: {out_path} ({sheet.width}x{sheet.height})")


def main():
    ap = argparse.ArgumentParser(description="Generate Cyrillic glyphs for Divine Frequency fonts")
    ap.add_argument("--ttf", default=DEFAULT_TTF)
    ap.add_argument("--out-root", default=DEFAULT_OUT_ROOT)
    ap.add_argument("--ipk3", default=DEFAULT_IPK3)
    ap.add_argument("--preview", default=DEFAULT_PREVIEW)
    args = ap.parse_args()

    for name, profile in PROFILES.items():
        out = os.path.join(args.out_root, name)
        os.makedirs(out, exist_ok=True)
        font = ImageFont.truetype(args.ttf, profile["font_size"])
        for ch in CHARS:
            render_glyph(font, ch, profile).save(os.path.join(out, glyph_name(ch)))
        print(f"Generated {len(CHARS)} glyphs -> {out}")

    glyphs = load_bigfont(args.ipk3)
    for ch in CHARS:
        glyphs[ch] = Image.open(os.path.join(args.out_root, "bigfont", glyph_name(ch))).convert("RGBA")
    make_preview(glyphs, args.preview)


if __name__ == "__main__":
    main()
