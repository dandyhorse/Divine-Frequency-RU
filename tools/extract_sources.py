import argparse
import json
import os
import re
import struct
import zipfile


DEFAULT_GAME = r"C:\Steam\steamapps\common\Divine Frequency"
DEFAULT_IPK3 = os.path.join(DEFAULT_GAME, "DFSDSA.ipk3")
DEFAULT_OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source")

TEXT_EXTS = {".txt", ".zs", ".zc", ".zsc", ".acs", ".md", ".inf", ".csv"}
ROOT_LUMPS = {
    "MENUDEF",
    "MAPINFO",
    "MAPINFO.ENEMIES",
    "MAPINFO.ITEMS",
    "MAPINFO.MISC",
    "CVARINFO.TXT",
    "FONTDEFS.TXT",
    "KEYCONF.TXT",
    "ZSCRIPT.TXT",
    "LOADACS",
    "DEFBINDS.TXT",
    "DEFCVARS.TXT",
}


def read_wad(data):
    if data[:4] not in (b"IWAD", b"PWAD"):
        return []
    numlumps, diroffset = struct.unpack("<II", data[4:12])
    lumps = []
    for i in range(numlumps):
        off, size, name = struct.unpack("<II8s", data[diroffset + i * 16:diroffset + (i + 1) * 16])
        lumps.append((name.rstrip(b"\0").decode("latin1"), off, size))
    return lumps


def safe_write(out_root, relpath, data):
    path = os.path.join(out_root, relpath.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return path


def main():
    ap = argparse.ArgumentParser(description="Extract Divine Frequency text sources from DFSDSA.ipk3")
    ap.add_argument("--ipk3", default=DEFAULT_IPK3)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    out_root = args.out
    os.makedirs(out_root, exist_ok=True)

    manifest = []
    z = zipfile.ZipFile(args.ipk3)

    for e in z.infolist():
        if e.is_dir():
            continue
        name = e.filename
        base = name.split("/")[-1]
        upper = name.upper()
        take = False
        if base.startswith("Language"):
            take = True
        elif "/" not in name and upper in ROOT_LUMPS:
            take = True
        elif name.upper().startswith("ACS/") and name.lower().endswith(".acs"):
            take = True
        elif name.upper().startswith("ZSCRIPT/") and os.path.splitext(name.lower())[1] in TEXT_EXTS:
            take = True
        elif name.upper().startswith("MENU/") and name.lower().endswith(".zs"):
            take = True
        elif name.lower().endswith("/font.inf"):
            take = True
        if take:
            data = z.read(name)
            dest = safe_write(out_root, name, data)
            manifest.append({
                "path": name,
                "out": os.path.relpath(dest, out_root),
                "bytes": len(data),
            })

    for e in z.infolist():
        if e.is_dir() or not e.filename.lower().endswith(".wad"):
            continue
        data = z.read(e.filename)
        wad = os.path.basename(e.filename)
        for lump_name, off, size in read_wad(data):
            if lump_name.upper() in ("DIALOGUE", "SCRIPTS") and size:
                blob = data[off:off + size]
                rel = f"maps/{wad}/{lump_name.upper()}"
                dest = safe_write(out_root, rel, blob)
                manifest.append({
                    "path": e.filename + ":" + lump_name,
                    "out": os.path.relpath(dest, out_root),
                    "bytes": len(blob),
                })
            elif lump_name.upper() == "BEHAVIOR" and size:
                blob = data[off:off + size]
                strings = re.findall(rb"[\x20-\x7e]{4,}", blob)
                if strings:
                    text = "\n".join(s.decode("latin1") for s in strings) + "\n"
                    rel = f"maps/{wad}/BEHAVIOR.strings.txt"
                    dest = safe_write(out_root, rel, text.encode("utf-8"))
                    manifest.append({
                        "path": e.filename + ":BEHAVIOR",
                        "out": os.path.relpath(dest, out_root),
                        "bytes": len(text),
                    })

    # Engine-side reference files from DF.pk3
    df_pk3 = os.path.join(os.path.dirname(args.ipk3), "DF.pk3")
    if os.path.isfile(df_pk3):
        zz = zipfile.ZipFile(df_pk3)
        for name in ("language.csv", "language.def", "ui/noto/noto-sans.ttf", "ui/noto/OFL.txt"):
            try:
                data = zz.read(name)
            except KeyError:
                continue
            rel = "engine/" + name
            dest = safe_write(out_root, rel, data)
            manifest.append({"path": "DF.pk3:" + name, "out": os.path.relpath(dest, out_root), "bytes": len(data)})
        zz.close()

    z.close()

    with open(os.path.join(out_root, "MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    total = sum(x["bytes"] for x in manifest)
    print(f"Extracted {len(manifest)} entries, {total / 1024 / 1024:.2f} MB -> {out_root}")


if __name__ == "__main__":
    main()
