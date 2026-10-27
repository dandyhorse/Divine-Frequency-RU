import argparse
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_GAME = r"C:\Steam\steamapps\common\Divine Frequency"
DEFAULT_IPK3 = os.path.join(DEFAULT_GAME, "DFSDSA.ipk3")
DEFAULT_WORK = os.path.join(ROOT, "work")
DEFAULT_OUT = os.path.join(ROOT, "dist", "DF_RU.pk3")

FONT_TARGETS = (
    ("Fonts/bigfont", "Fonts/bigfont", "bigfont"),
    ("Fonts/BigUpper", "Fonts/bigfont", "bigfont"),
    ("Fonts/ACS_FONT", "Fonts/ACS_FONT", "ACS_FONT"),
    ("Fonts/smallfont", "Fonts/smallfont", "ACS_FONT"),
)

GENERATED_FONTS = (
    "RU_DF_FONT",
    "RU_ChatBoxFont",
    "RU_CONVO_FONT",
    "RU_npcfont",
)


def add_file(entries, name, path):
    with open(path, "rb") as f:
        entries[name] = f.read()


def main():
    ap = argparse.ArgumentParser(description="Build DF_RU.pk3 translation prototype")
    ap.add_argument("--ipk3", default=DEFAULT_IPK3)
    ap.add_argument("--work", default=DEFAULT_WORK)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    menu = os.path.join(args.work, "MenuDef")
    if not os.path.isfile(menu):
        raise SystemExit(f"MenuDef not found: {menu}")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    zin = zipfile.ZipFile(args.ipk3)
    zout = zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED, compresslevel=6)

    entries = {}
    add_file(entries, "MenuDef", menu)

    for target, source, profile in FONT_TARGETS:
        for e in zin.infolist():
            if e.is_dir() or not e.filename.startswith(source + "/"):
                continue
            entries[target + "/" + e.filename[len(source) + 1:]] = zin.read(e.filename)

        gen_dir = os.path.join(args.work, "Fonts", profile)
        if os.path.isdir(gen_dir):
            for name in sorted(os.listdir(gen_dir)):
                path = os.path.join(gen_dir, name)
                if os.path.isfile(path):
                    entries[target + "/" + name] = open(path, "rb").read()

    for font_name in GENERATED_FONTS:
        gen_dir = os.path.join(args.work, "Fonts", font_name)
        if not os.path.isdir(gen_dir):
            continue
        for name in sorted(os.listdir(gen_dir)):
            path = os.path.join(gen_dir, name)
            if os.path.isfile(path):
                entries["Fonts/" + font_name + "/" + name] = open(path, "rb").read()

    for name in sorted(os.listdir(args.work)):
        if name != "MapInfo" and not name.startswith("Language."):
            continue
        path = os.path.join(args.work, name)
        if os.path.isfile(path):
            add_file(entries, name, path)

    for folder in ("Menu", "ZScript"):
        base = os.path.join(args.work, folder)
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            for name in files:
                path = os.path.join(root, name)
                rel = os.path.relpath(path, args.work).replace(os.sep, "/")
                add_file(entries, rel, path)

    for name in sorted(entries):
        zout.writestr(name, entries[name])

    zout.close()
    zin.close()

    print(f"Built {args.out}")
    print(f"Entries: {len(entries)}")
    print(f"Size: {os.path.getsize(args.out) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
