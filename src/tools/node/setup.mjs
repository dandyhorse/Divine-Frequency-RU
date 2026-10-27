import { existsSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { ZipReader } from "./lib/zip.mjs";
import { ACC, ACC_INCLUDES } from "./lib/paths.mjs";

const URL = "https://github.com/ZDoom/acc/releases/download/1.60/acc-1.60-win32.zip";

if (existsSync(ACC) && !process.argv.includes("--force")) {
  console.log(`ACC already present: ${ACC}`);
  process.exit(0);
}

console.log(`Downloading ACC: ${URL}`);
const response = await fetch(URL);
if (!response.ok) {
  throw new Error(`Download failed: ${response.status} ${response.statusText}`);
}
const temp = mkdtempSync(join(tmpdir(), "df_ru_acc_"));
try {
  const zipPath = join(temp, "acc.zip");
  writeFileSync(zipPath, Buffer.from(await response.arrayBuffer()));
  const zip = new ZipReader(zipPath);
  const name = zip.names.find((entry) => entry.toLowerCase().endsWith("acc.exe"));
  if (!name) {
    throw new Error("acc.exe not found in downloaded archive");
  }
  writeFileSync(ACC, zip.read(name));
  console.log(`ACC installed: ${ACC}`);
  console.log(`ACC includes: ${ACC_INCLUDES}`);
} finally {
  rmSync(temp, { recursive: true, force: true });
}
