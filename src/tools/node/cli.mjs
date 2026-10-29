#!/usr/bin/env node
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { applyCompleted } from "./lib/completed.mjs";
import { buildPk3 } from "./lib/build.mjs";
import { compileMaps } from "./lib/maps.mjs";
import { packagePortable } from "./lib/package.mjs";
import { extractSources } from "./lib/extract.mjs";
import { generateFonts } from "./lib/fonts.mjs";
import {
  ACC,
  ACC_INCLUDES,
  DEFAULT_IPK3,
  DEFAULT_PK3,
  DEFAULT_PORTABLE,
  DEFAULT_WORK,
  DEV,
} from "./lib/paths.mjs";

const args = process.argv.slice(2);
const command = args[0] || "help";

function value(name, fallback = undefined) {
  const index = args.indexOf(name);
  if (index === -1) {
    return fallback;
  }
  return args[index + 1];
}

function flag(name) {
  return args.includes(name);
}

function printHelp() {
  console.log(`Divine Frequency RU build tools

Commands:
  npm run check                  verify completed translations against source/work
  npm run apply                  apply completed translations to work/
  npm run fonts                  generate Cyrillic font PNGs with canvas
  npm run maps                   compile translated SCRIPTS with ACC
  npm run build                  build dist/DF_RU.pk3
  npm run package                build dist/DF_RU_Portable.zip
  npm run extract                extract source files from DFSDSA.ipk3
  npm run all                    apply + maps + build + package

Options:
  --ipk3 <path>                  path to DFSDSA.ipk3
  --work <path>                  path to dev/work
  --out <path>                   output PK3 or portable ZIP
  --acc <path>                   path to acc.exe
  --includes <path>              path to ACC include files
  --without-acs                  do not include translated ACS libraries
  --without-maps                 do not include translated map WADs
  --version <value>              portable package version (default 1.0.6)

Default game: ${DEFAULT_IPK3}
Default work: ${DEFAULT_WORK}
ACC: ${ACC}
`);
}

function applyOptions() {
  return {
    check: flag("--check"),
    work: resolve(value("--work", DEFAULT_WORK)),
    zscript: !flag("--maps-only") && !flag("--language-only"),
    maps: !flag("--zscript-only") && !flag("--language-only"),
    language: !flag("--zscript-only") && !flag("--maps-only"),
  };
}

function buildOptions() {
  return {
    ipk3: resolve(value("--ipk3", DEFAULT_IPK3)),
    work: resolve(value("--work", DEFAULT_WORK)),
    out: resolve(value("--out", DEFAULT_PK3)),
    withoutAcs: flag("--without-acs"),
    withoutMaps: flag("--without-maps"),
  };
}

try {
  switch (command) {
    case "check":
      applyCompleted({ ...applyOptions(), check: true });
      break;
    case "apply":
      applyCompleted(applyOptions());
      break;
    case "fonts":
      await generateFonts({
        ipk3: resolve(value("--ipk3", DEFAULT_IPK3)),
        work: resolve(value("--work", DEFAULT_WORK)),
        force: flag("--force"),
      });
      break;
    case "maps":
      compileMaps({
        acc: resolve(value("--acc", ACC)),
        includes: resolve(value("--includes", ACC_INCLUDES)),
        work: resolve(value("--work", DEFAULT_WORK)),
      });
      break;
    case "build":
      buildPk3(buildOptions());
      break;
    case "package":
      packagePortable({
        pk3: resolve(value("--pk3", DEFAULT_PK3)),
        out: resolve(value("--out", DEFAULT_PORTABLE)),
        version: value("--version", "1.0.10"),
      });
      break;
    case "extract":
      extractSources({
        ipk3: resolve(value("--ipk3", DEFAULT_IPK3)),
        out: resolve(value("--out", resolve(DEV, "source"))),
      });
      break;
    case "all":
      applyCompleted(applyOptions());
      await generateFonts({
        ipk3: resolve(value("--ipk3", DEFAULT_IPK3)),
        work: resolve(value("--work", DEFAULT_WORK)),
        force: flag("--force"),
      });
      compileMaps({
        acc: resolve(value("--acc", ACC)),
        includes: resolve(value("--includes", ACC_INCLUDES)),
        work: resolve(value("--work", DEFAULT_WORK)),
      });
      buildPk3(buildOptions());
      packagePortable({
        pk3: resolve(value("--out", DEFAULT_PK3)),
        out: resolve(value("--portable", DEFAULT_PORTABLE)),
        version: value("--version", "1.0.10"),
      });
      break;
    case "doctor":
      console.log(`Node: ${process.version}`);
      console.log(`Project: ${DEV}`);
      console.log(`Game: ${DEFAULT_IPK3} ${existsSync(DEFAULT_IPK3) ? "OK" : "MISSING"}`);
      console.log(`ACC: ${ACC} ${existsSync(ACC) ? "OK" : "MISSING"}`);
      break;
    case "help":
    case "--help":
    case "-h":
      printHelp();
      break;
    default:
      console.error(`Unknown command: ${command}`);
      printHelp();
      process.exitCode = 1;
  }
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exitCode = 1;
}
