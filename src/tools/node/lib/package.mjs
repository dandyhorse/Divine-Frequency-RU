import { existsSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { writeZip } from "./zip.mjs";
import { DEFAULT_PK3, DEFAULT_PORTABLE, PACKAGING } from "./paths.mjs";

const PACKAGE_FILES = ["install.cmd", "uninstall.cmd", "find_game.ps1", "README.txt"];

export function packagePortable({
  pk3 = DEFAULT_PK3,
  out = DEFAULT_PORTABLE,
  version = "1.0.7",
} = {}) {
  if (!existsSync(pk3)) {
    throw new Error(`PK3 not found: ${pk3}`);
  }
  const entries = new Map();
  const data = readFileSync(pk3);
  entries.set("DF_RU.wad", data);
  entries.set("DF_RU.pk3", data);
  for (const name of PACKAGE_FILES) {
    const path = join(PACKAGING, name);
    if (!existsSync(path)) {
      throw new Error(`Packaging file not found: ${path}`);
    }
    entries.set(name, readFileSync(path));
  }
  entries.set("VERSION.txt", Buffer.from(version + "\n"));
  writeZip(out, entries, 9);
  const size = statSync(out).size;
  console.log(`Built ${out}`);
  console.log(`Size: ${(size / 1024 / 1024).toFixed(2)} MB`);
  return { size };
}
