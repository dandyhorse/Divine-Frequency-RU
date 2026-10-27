import os
from PIL import Image, ImageDraw, ImageFont

root = r"C:\projects\RU_DivineFrequency"
shots = os.path.join(root, "test", "screenshots")
orig = Image.open(os.path.join(shots, "original_fullscreen_menu.png")).convert("RGB")
ru = Image.open(os.path.join(shots, "ru_fullscreen_menu.png")).convert("RGB")

# Crop the menu area (same region for both fullscreen screenshots).
crop = (640, 420, 1920, 1280)
orig = orig.crop(crop)
ru = ru.crop(crop)

cell_w, cell_h = 760, 510
orig = orig.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
ru = ru.resize((cell_w, cell_h), Image.Resampling.LANCZOS)

pad = 24
header = 56
width = pad + cell_w + pad + cell_w + pad
height = header + cell_h + pad
sheet = Image.new("RGB", (width, height), (18, 18, 20))
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(os.path.join(root, "source", "fonts", "noto-sans.ttf"), 28)

draw.text((pad, 14), "Оригинал (BIGFONT, English)", font=font, fill=(235, 235, 235))
draw.text((pad + cell_w + pad, 14), "RU (NewSmallFont, русский)", font=font, fill=(235, 235, 235))
sheet.paste(orig, (pad, header))
sheet.paste(ru, (pad + cell_w + pad, header))

out = os.path.join(shots, "compare_main_menu.png")
sheet.save(out)
print(out, sheet.size)
