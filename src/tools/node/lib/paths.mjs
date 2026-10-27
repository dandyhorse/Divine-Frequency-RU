import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
export const SRC = resolve(here, "../../..");
export const ROOT = resolve(SRC, "..");
export const DEV = resolve(ROOT, "dev");
export const DEFAULT_GAME = "C:\\Steam\\steamapps\\common\\Divine Frequency";
export const DEFAULT_IPK3 = resolve(DEFAULT_GAME, "DFSDSA.ipk3");
export const DEFAULT_WORK = resolve(DEV, "work");
export const DEFAULT_PK3 = resolve(ROOT, "build", "DF_RU.pk3");
export const DEFAULT_PORTABLE = resolve(ROOT, "build", "DF_RU_Portable.zip");
export const PACKAGING = resolve(SRC, "packaging");
export const ACC = resolve(SRC, "tools", "acc", "acc.exe");
export const ACC_INCLUDES = resolve(SRC, "tools", "acc");
export const COMPLETED = resolve(DEV, "DF_RU_TRANSLATION_completed.md");
export const SOURCE = resolve(DEV, "source");
