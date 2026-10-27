# DF RU Patcher

Небольшой Windows-установщик патча Divine Frequency. Написан на C#/WPF, собирается системным `csc.exe` из .NET Framework 4.8, без отдельного .NET SDK.

## Сборка

```bat
npm run build
npm run installer
```

Результат: `build/DF_RU_Patcher.exe`. Внутрь встроены `DF_RU.wad` и музыкальный файл.

## Запуск

`DF_RU_Patcher.exe` сам ищет полную версию игры через Steam, показывает найденный путь и позволяет установить, обновить или удалить `skins\DF_RU.wad`.

## Музыка

8-bit The Black Dahlia Murder — Moonlight Equilibrium:

https://www.youtube.com/watch?v=WOLUFWzSd4A
