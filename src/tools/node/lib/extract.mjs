import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { ZipReader } from "./zip.mjs";
import { readWad, wadStrings } from "./wad.mjs";
import { DEV, DEFAULT_IPK3 } from "./paths.mjs";

const TEXT_EXTENSIONS = new Set([".txt", ".zs", ".zc", ".zsc", ".acs", ".md", ".inf", ".csv"]);
const ROOT_LUMPS = new Set([
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
]);

function write(outRoot, relativePath, data) {
  const path = join(outRoot, relativePath);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, data);
  return path;
}

function extname(name) {
  const index = name.lastIndexOf(".");
  return index === -1 ? "" : name.slice(index).toLowerCase();
}

function basename(name) {
  return name.slice(name.lastIndexOf("/") + 1);
}

export function extractSources({ ipk3 = DEFAULT_IPK3, out = join(DEV, "source") } = {}) {
  const reader = new ZipReader(ipk3);
  const manifest = [];

  for (const name of reader.names) {
    const base = basename(name);
    const upper = name.toUpperCase();
    const take =
      base.startsWith("Language") ||
      (!name.includes("/") && ROOT_LUMPS.has(upper)) ||
      (upper.startsWith("ACS/") && name.toLowerCase().endsWith(".acs")) ||
      (upper.startsWith("ZSCRIPT/") && TEXT_EXTENSIONS.has(extname(name))) ||
      (upper.startsWith("MENU/") && name.toLowerCase().endsWith(".zs")) ||
      name.toLowerCase().endsWith("/font.inf");
    if (!take) {
      continue;
    }
    const data = reader.read(name);
    write(out, name, data);
    manifest.push({ path: name, out: name, bytes: data.length });
  }

  for (const name of reader.names) {
    if (!name.toLowerCase().endsWith(".wad") || !name.startsWith("Maps/")) {
      continue;
    }
    const data = reader.read(name);
    const map = basename(name);
    for (const lump of readWad(data)) {
      const upper = lump.name.toUpperCase();
      if ((upper === "DIALOGUE" || upper === "SCRIPTS") && lump.data.length) {
        write(out, `maps/${map}/${upper}`, lump.data);
        manifest.push({ path: `${name}:${lump.name}`, out: `maps/${map}/${upper}`, bytes: lump.data.length });
      } else if (upper === "BEHAVIOR" && lump.data.length) {
        const text = wadStrings(lump.data).join("\n") + "\n";
        write(out, `maps/${map}/BEHAVIOR.strings.txt`, Buffer.from(text, "utf8"));
        manifest.push({ path: `${name}:BEHAVIOR`, out: `maps/${map}/BEHAVIOR.strings.txt`, bytes: text.length });
      }
    }
  }

  const df = join(dirname(ipk3), "DF.pk3");
  if (existsSync(df)) {
    const engine = new ZipReader(df);
    for (const name of ["language.csv", "language.def", "ui/noto/noto-sans.ttf", "ui/noto/OFL.txt"]) {
      if (!engine.has(name)) {
        continue;
      }
      const data = engine.read(name);
      write(out, "engine/" + name, data);
      manifest.push({ path: "DF.pk3:" + name, out: "engine/" + name, bytes: data.length });
    }
  }

  write(out, "MANIFEST.json", Buffer.from(JSON.stringify(manifest, null, 2), "utf8"));
  const total = manifest.reduce((sum, entry) => sum + entry.bytes, 0);
  console.log(`Extracted ${manifest.length} entries, ${(total / 1024 / 1024).toFixed(2)} MB -> ${out}`);
}
