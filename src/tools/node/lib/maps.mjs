import { copyFileSync, existsSync, mkdtempSync, readdirSync, rmSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { ACC, ACC_INCLUDES, DEFAULT_WORK } from "./paths.mjs";

export function compileMaps({ acc = ACC, includes = ACC_INCLUDES, work = DEFAULT_WORK } = {}) {
  if (!existsSync(acc)) {
    throw new Error(`ACC not found: ${acc}`);
  }
  if (!existsSync(join(includes, "zcommon.acs"))) {
    throw new Error(`ACC includes not found: ${includes}`);
  }
  const mapsRoot = join(work, "maps");
  if (!existsSync(mapsRoot)) {
    throw new Error(`Maps directory not found: ${mapsRoot}`);
  }
  const mapDirs = readdirSync(mapsRoot)
    .sort()
    .filter((name) => {
      const path = join(mapsRoot, name);
      return statSync(path).isDirectory() && existsSync(join(path, "SCRIPTS"));
    });
  if (mapDirs.length === 0) {
    throw new Error(`No translated maps in ${mapsRoot}`);
  }
  for (const mapName of mapDirs) {
    const mapDir = join(mapsRoot, mapName);
    const temp = mkdtempSync(join(tmpdir(), "df_ru_map_"));
    try {
      copyFileSync(join(mapDir, "SCRIPTS"), join(temp, "SCRIPTS.acs"));
      for (const include of readdirSync(includes)) {
        const path = join(includes, include);
        if (statSync(path).isFile()) {
          copyFileSync(path, join(temp, include));
        }
      }
      const result = spawnSync(acc, ["SCRIPTS.acs", "BEHAVIOR.o"], {
        cwd: temp,
        stdio: "inherit",
      });
      if (result.status !== 0 || !existsSync(join(temp, "BEHAVIOR.o"))) {
        throw new Error(`ACC failed for ${mapName}`);
      }
      copyFileSync(join(temp, "BEHAVIOR.o"), join(mapDir, "BEHAVIOR.o"));
      console.log(`${mapName}: compiled`);
    } finally {
      rmSync(temp, { recursive: true, force: true });
    }
  }
  console.log(`Compiled ${mapDirs.length} maps`);
}
