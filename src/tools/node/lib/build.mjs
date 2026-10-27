import { existsSync, mkdirSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { ZipReader, writeZip } from "./zip.mjs";
import { replaceBehavior } from "./wad.mjs";
import { DEFAULT_IPK3, DEFAULT_PK3, DEFAULT_WORK } from "./paths.mjs";

const FONT_TARGETS = [
  ["Fonts/bigfont", "Fonts/bigfont", "bigfont"],
  ["Fonts/BigUpper", "Fonts/bigfont", "bigfont"],
  ["Fonts/ACS_FONT", "Fonts/ACS_FONT", "ACS_FONT"],
  ["Fonts/smallfont", "Fonts/smallfont", "ACS_FONT"],
];

const GENERATED_FONTS = ["RU_DF_FONT", "RU_ChatBoxFont", "RU_CONVO_FONT", "RU_npcfont"];

function walk(dir, base, add) {
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) {
      walk(path, base, add);
    } else {
      const relativePath = relative(base, path).replaceAll("\\", "/");
      add(relativePath, readFileSync(path));
    }
  }
}

export function buildPk3({
  ipk3 = DEFAULT_IPK3,
  work = DEFAULT_WORK,
  out = DEFAULT_PK3,
  withoutAcs = false,
  withoutMaps = false,
} = {}) {
  if (!existsSync(join(work, "MenuDef"))) {
    throw new Error(`MenuDef not found: ${join(work, "MenuDef")}`);
  }
  const reader = new ZipReader(ipk3);
  const entries = new Map();
  const add = (name, data) => entries.set(name, data);

  add("MenuDef", readFileSync(join(work, "MenuDef")));

  for (const [target, source, profile] of FONT_TARGETS) {
    for (const name of reader.names) {
      if (!name.startsWith(source + "/") || name.endsWith("/")) {
        continue;
      }
      add(target + "/" + name.slice(source.length + 1), reader.read(name));
    }
    const generated = join(work, "Fonts", profile);
    if (existsSync(generated)) {
      for (const name of readdirSync(generated)) {
        const path = join(generated, name);
        if (statSync(path).isFile()) {
          add(target + "/" + name, readFileSync(path));
        }
      }
    }
  }

  for (const fontName of GENERATED_FONTS) {
    const generated = join(work, "Fonts", fontName);
    if (!existsSync(generated)) {
      continue;
    }
    for (const name of readdirSync(generated)) {
      const path = join(generated, name);
      if (statSync(path).isFile()) {
        add("Fonts/" + fontName + "/" + name, readFileSync(path));
      }
    }
  }

  for (const name of readdirSync(work).sort()) {
    if (name !== "MapInfo" && !name.startsWith("Language.")) {
      continue;
    }
    const path = join(work, name);
    if (statSync(path).isFile()) {
      add(name, readFileSync(path));
    }
  }

  if (!withoutAcs) {
    for (const name of ["map_func", "Key_Message", "Upgrade_Message"]) {
      const path = join(work, "ACS", name + ".o");
      if (existsSync(path)) {
        add("ACS/" + name + ".o", readFileSync(path));
      }
    }
  }

  for (const folder of ["Menu", "ZScript"]) {
    const base = join(work, folder);
    if (!existsSync(base)) {
      continue;
    }
    walk(base, work, add);
  }

  if (!withoutMaps) {
    const mapsRoot = join(work, "maps");
    if (existsSync(mapsRoot)) {
      for (const mapName of readdirSync(mapsRoot).sort()) {
        const behavior = join(mapsRoot, mapName, "BEHAVIOR.o");
        if (!existsSync(behavior)) {
          continue;
        }
        const original = "Maps/" + mapName;
        if (!reader.has(original)) {
          throw new Error(`Map not found in IPK3: ${original}`);
        }
        add(original, replaceBehavior(reader.read(original), readFileSync(behavior)));
      }
    }
  }

  mkdirSync(dirname(out), { recursive: true });
  writeZip(out, entries, 6);
  const size = statSync(out).size;
  console.log(`Built ${out}`);
  console.log(`Entries: ${entries.size}`);
  console.log(`Size: ${(size / 1024).toFixed(1)} KB`);
  return { entries: entries.size, size };
}
