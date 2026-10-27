import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { DEV, SRC } from "./lib/paths.mjs";

const basePath = join(DEV, "DF_RU_TRANSLATIONS_ALL.md");
const completedPath = join(DEV, "DF_RU_TRANSLATION_completed.md");
const outputPath = join(SRC, "TRANSLATIONS.md");

if (!existsSync(basePath) || !existsSync(completedPath)) {
  throw new Error("Missing translation base/completed files in dev/");
}

const base = readFileSync(basePath, "utf8").replace(/\r\n?/g, "\n");
const completed = readFileSync(completedPath, "utf8").replace(/\r\n?/g, "\n");
const cut = base.indexOf("## 6. Приложение");
if (cut === -1) {
  throw new Error("Appendix marker not found in DF_RU_TRANSLATIONS_ALL.md");
}

const languageStart = base.indexOf("## 1. Language.*");
if (languageStart === -1) {
  throw new Error("Language section not found in translation base");
}
const body = base.slice(languageStart, cut).trimEnd();

const zscriptStart = completed.indexOf("## 1. ZScript");
const zscriptEnd = completed.indexOf("## 2. Language");
const zscript = completed
  .slice(zscriptStart, zscriptEnd)
  .trim()
  .split("\n")
  .slice(1)
  .join("\n")
  .trim();

const mapsStart = completed.indexOf("## 4. Строки карт (SCRIPTS)");
const mapsEnd = completed.indexOf("## 5. Не переводить");
const maps = completed
  .slice(mapsStart, mapsEnd)
  .trim()
  .split("\n")
  .slice(1)
  .join("\n")
  .trim();

const terminalStart = completed.indexOf("### `Terminal_08a_1`");
const terminalEnd = completed.indexOf("### Уже переведены");
const terminal = completed
  .slice(terminalStart, terminalEnd)
  .trim()
  .replace(
    "**ПЕРЕВОДИТЬ.** Файл: `source/Language.Map:227`.",
    "Добавлено в v1.0.6. Файл: `Language.Map`, ключ `Terminal_08a_1`.",
  );

const header = `# Divine Frequency — полная карта перевода

Дата: 27.10.2026 · версия перевода: **1.0.6**

Здесь собраны фактические переводы: **EN → RU** и место, где строка находится. Файл сгенерирован из рабочей сборки: \`Language.*\`, ZScript, ACS, MenuDef, MapInfo, runtime-словарей и \`SCRIPTS\` карт.

## Как читать

- **EN** — строка в оригинальной игре.
- **RU** — строка в патче.
- **Где** — файл, карта или ключ; для карт указана строка исходного \`SCRIPTS\`.
- Строки с намеренно повреждённым оригиналом и технические шифры помечены отдельно.

## Содержание

1. [Language.*](#1-language)
2. [ZScript: изменения строк](#2-zscript-изменения-строк)
3. [Runtime-словари](#3-runtime-словари)
4. [ACS-библиотеки](#4-acs-библиотеки)
5. [MenuDef и MapInfo](#5-menudef-и-mapinfo)
6. [v1.0.6: ZScript](#6-v106-zscript)
7. [v1.0.6: SCRIPTS карт](#7-v106-scripts-карт)
8. [v1.0.6: Language.Map — Terminal_08a_1](#8-v106-languagemap--terminal_08a_1)
9. [Что осталось без перевода](#9-что-осталось-без-перевода)

`;

const extra = `

## 6. v1.0.6: ZScript

Дополнительный проход: 77 строк в исходных ZScript-файлах. Номера строк относятся к исходникам игры.

${zscript}

## 7. v1.0.6: SCRIPTS карт

194 переводимые строки в 17 картах. Четыре намеренно повреждённые строки оставлены как в оригинале.

${maps}

## 8. v1.0.6: Language.Map — Terminal_08a_1

${terminal}

## 9. Что осталось без перевода

### Намеренно повреждённые строки карт

- \`MAP30.wad\`: строки 788, 792, 796.
- \`MAP31.wad\`: строка 317.

### Нет английского оригинала

- \`AnThit_2\` — в исходнике неэкранированные кавычки; полного текста нет.
- \`Elock_1\`, \`M01_DREAM_01a_1\`, \`M01_DREAM_01a_1a\`, \`M01_DREAM_01a_2\`, \`M01_DREAM_01a_2a\`, \`M01_Mail\`, \`M01_MailBox03\`, \`STUDENTGROUP\`, \`STUDENT_04\`, \`Terminal_12\` — 10 ключей DIALOGUE без записи в \`Language.*\`.

### Техническое

- Шифры, ASCII-арт, технические команды и намеренно испорченные логи.
- Имена классов, state-метки и пути ассетов.
- Озвучка остаётся английской.
`;

const output = header + body + extra + "\n";
writeFileSync(outputPath, output, "utf8");
console.log(`Wrote ${outputPath}`);
console.log(`Lines: ${output.split("\n").length}`);
console.log(`Size: ${(Buffer.byteLength(output) / 1024).toFixed(1)} KB`);
