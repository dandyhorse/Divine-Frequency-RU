import {
  existsSync,
  mkdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { dirname, resolve } from "node:path";
import { COMPLETED, SOURCE, DEFAULT_WORK } from "./paths.mjs";

function readText(path) {
  const data = readFileSync(path);
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(data);
  } catch {
    return data.toString("latin1");
  }
}

function normalize(text) {
  return text.replace(/\r\n?/g, "\n");
}

function writeText(path, text) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, text, "utf8");
}

export function parseCompleted() {
  const document = readFileSync(COMPLETED, "utf8");
  return {
    zscript: parseSection(document, "## 1. ZScript", "## 2. Language"),
    maps: parseSection(document, "## 4. Строки карт (SCRIPTS)", "## 5. Не переводить"),
    document,
  };
}

function sectionBetween(document, start, end) {
  const startIndex = document.indexOf(start);
  if (startIndex === -1) {
    throw new Error(`Section not found: ${start}`);
  }
  const from = startIndex + start.length;
  const endIndex = document.indexOf(end, from);
  if (endIndex === -1) {
    throw new Error(`Section end not found: ${end}`);
  }
  return document.slice(from, endIndex);
}

function parseSection(document, start, end) {
  const section = sectionBetween(document, start, end);
  const result = new Map();
  let current = null;
  const lines = section.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const heading = lines[i].match(/^### `([^`]+)`$/);
    if (heading) {
      current = heading[1];
      if (!result.has(current)) {
        result.set(current, []);
      }
    }
    const item = lines[i].match(/^- строка (\d+):$/);
    if (!item || !current) {
      continue;
    }
    const entry = { line: Number(item[1]), en: null, ru: null };
    const en = (lines[i + 1] || "").match(/^\s+- \*\*EN:\*\* `(.*)`$/);
    const ru = (lines[i + 2] || "").match(/^\s+- \*\*RU:\*\* `(.*)`$/);
    if (en) {
      entry.en = en[1];
    }
    if (ru) {
      entry.ru = ru[1];
    }
    result.get(current).push(entry);
  }
  return result;
}

function applyEntries(target, entries, source = null) {
  if (!existsSync(target) && source && existsSync(source)) {
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, readFileSync(source));
  }
  if (!existsSync(target)) {
    throw new Error(`File not found: ${target}`);
  }
  const original = normalize(readText(target));
  const lines = original.split("\n");
  let changed = 0;
  let skipped = 0;
  for (const entry of entries) {
    if (!entry.en || !entry.ru) {
      skipped++;
      continue;
    }
    const index = entry.line - 1;
    if (index >= lines.length) {
      throw new Error(`${target}:${entry.line}: line out of range`);
    }
    if (lines[index].includes(entry.en)) {
      lines[index] = lines[index].replace(entry.en, entry.ru);
      changed++;
    } else if (lines[index].includes(entry.ru)) {
      skipped++;
    } else {
      throw new Error(`${target}:${entry.line}: source string not found: ${entry.en}`);
    }
  }
  if (changed) {
    writeText(target, lines.join("\n"));
  }
  return { changed, skipped };
}

function checkEntries(base, entries) {
  if (!existsSync(base)) {
    throw new Error(`File not found: ${base}`);
  }
  const lines = normalize(readText(base)).split("\n");
  for (const entry of entries) {
    if (!entry.en || !entry.ru) {
      continue;
    }
    if (entry.line > lines.length) {
      throw new Error(`${base}:${entry.line}: line out of range`);
    }
    if (!lines[entry.line - 1].includes(entry.en) && !lines[entry.line - 1].includes(entry.ru)) {
      throw new Error(`${base}:${entry.line}: string not found: ${entry.en}`);
    }
  }
}

function applyLanguage(document, work) {
  const normalizedDocument = normalize(document);
  const section = sectionBetween(normalizedDocument, "### `Terminal_08a_1`", "### Уже переведены");
  const en = section.match(/\*\*EN\*\*\s*```text\n(.*?)```/s);
  const ru = section.match(/\*\*RU\*\*\s*```text\n(.*?)```/s);
  if (!en || !ru) {
    throw new Error("Terminal_08a_1 translation blocks not found");
  }
  const target = resolve(work, "Language.Map");
  const text = readText(target);
  if (text.includes("Terminal_08a_1")) {
    return { changed: 0, skipped: 1 };
  }
  if (text.includes(ru[1].trimEnd())) {
    return { changed: 0, skipped: 1 };
  }
  if (text.includes(en[1].trimEnd())) {
    writeText(target, text.replace(en[1].trimEnd(), ru[1].trimEnd()));
    return { changed: 1, skipped: 0 };
  }
  const lines = ru[1].trimEnd().split("\n");
  const block =
    "Terminal_08a_1 =\n" +
    lines.map((line) => `"${line}\n"`).join("\n") +
    ";\n";
  const anchor = "Terminal_09 =";
  if (!text.includes(anchor)) {
    throw new Error("Terminal_09 anchor not found in Language.Map");
  }
  writeText(target, text.replace(anchor, block + anchor));
  return { changed: 1, skipped: 0 };
}

export function applyCompleted({ check = false, work = DEFAULT_WORK, zscript = true, maps = true, language = true } = {}) {
  const { zscript: zEntries, maps: mapEntries, document } = parseCompleted();
  let changed = 0;
  let skipped = 0;

  if (zscript) {
    for (const [relative, entries] of zEntries) {
      const target = resolve(work, "ZScript", relative);
      const source = resolve(SOURCE, "ZScript", relative);
      if (check) {
        checkEntries(existsSync(target) ? target : source, entries);
        console.log(`OK ZScript ${relative}: ${entries.length} strings`);
      } else {
        const result = applyEntries(target, entries, source);
        changed += result.changed;
        skipped += result.skipped;
        console.log(`ZScript ${relative}: ${result.changed} changed, ${result.skipped} already done`);
      }
    }
  }

  if (maps) {
    for (const [relative, entries] of mapEntries) {
      const target = resolve(work, "maps", relative, "SCRIPTS");
      const source = resolve(SOURCE, "maps", relative, "SCRIPTS");
      if (check) {
        checkEntries(source, entries);
        console.log(`OK map ${relative}: ${entries.filter((entry) => entry.en).length} strings`);
      } else {
        const result = applyEntries(target, entries, source);
        changed += result.changed;
        skipped += result.skipped;
        console.log(`Map ${relative}: ${result.changed} changed, ${result.skipped} skipped`);
      }
    }
  }

  if (language) {
    if (check) {
      console.log("OK Language terminal");
    } else {
      const result = applyLanguage(document, work);
      changed += result.changed;
      skipped += result.skipped;
      console.log(`Language Terminal_08a_1: ${result.changed} changed, ${result.skipped} already done`);
    }
  }

  console.log(`Total: ${changed} changed, ${skipped} skipped`);
}
