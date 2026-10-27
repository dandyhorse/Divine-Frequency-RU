# Инструменты

## Node.js

Основной пайплайн: `src/tools/node`.

- `cli.mjs` — `check`, `apply`, `fonts`, `maps`, `build`, `package`, `extract`, `all`, `doctor`.
- `setup.mjs` — скачивает ACC 1.60 win32.
- `lib/zip.mjs` — чтение/запись ZIP/PK3 без зависимостей.
- `lib/wad.mjs` — замена `BEHAVIOR` в WAD карты.
- `lib/completed.mjs` — применение `DF_RU_TRANSLATION_completed.md`.
- `lib/maps.mjs` — компиляция `SCRIPTS` через ACC.
- `lib/build.mjs` — сборка `build/DF_RU.pk3`.
- `lib/package.mjs` — сборка `build/DF_RU_Portable.zip`.
- `lib/extract.mjs` — извлечение исходников из `DFSDSA.ipk3`.
- `lib/fonts.mjs` — генерация кириллических шрифтов через `@napi-rs/canvas`.

Запуск из корня проекта:

```bat
npm install
npm run doctor
npm run fonts
npm run maps
npm run build
npm run package
npm run all
```

## ACC

`src/tools/acc` содержит include-файлы ACC и `acc.exe` (включён; `npm run setup` скачивает при отсутствии).
ACC 1.60: https://github.com/ZDoom/acc. Компилятор используется только для `SCRIPTS` карт.
