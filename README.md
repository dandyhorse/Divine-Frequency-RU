# RU Divine Frequency

Русский перевод Divine Frequency. Переведено меню: главное, сложность, все настройки, загрузка/сохранение и выход.

Полный анализ игры, объёма текста, шрифтов и плана работ: [ANALYSIS.md](ANALYSIS.md).

Таблица «что было → что стало»: [TRANSLATIONS.md](TRANSLATIONS.md).

## Текущий статус

- `DF_RU.pk3` собирается и загружается игрой через `-file`.
- Главное меню переведено и отцентровано.
- Шрифт главного меню — оригинальный `BIGFONT`; позиции пунктов пересчитаны под русские подписи. Вкладки настроек — оригинальный `BigUpper`.
- Для настроек добавлены полные шрифты `BigUpper` и `ACS_FONT` с кириллицей: русские подписи и описания больше не рассыпаются на отдельные буквы.
- Скриншоты для ориентира:
  - `test/screenshots/original_fullscreen_menu.png` — оригинальное меню;
  - `test/screenshots/quit_test.png` — диалог выхода и его шрифт.
- Актуальную сборку проверяй в игре: в этой итерации меню переведено целиком, включая настройки, загрузку/сохранение и выход.

Переведено в меню:

- Новая игра
- Настройки
- Загрузить игру
- Сохранить игру
- Титры
- Выход

Также переведены вкладки настроек (`Графика`, `Управление`, `Звук`, `Специальные возможности`) и заголовок `Выберите сложность:`.

## Запуск

Запустить игру с переводом:

```text
test\run_test.cmd
```

Запустить оригинал для сравнения:

```text
test\run_original.cmd
```

Оба скрипта используют отдельные копии конфига и не трогают основной профиль игры.

Вручную:

```text
cd /d "C:\Steam\steamapps\common\Divine Frequency"
DivineFrequency.exe -file "C:\projects\RU_DivineFrequency\dist\DF_RU.pk3" -config "C:\projects\RU_DivineFrequency\test\dfconfig-test.ini"
```

## Сравнение с оригиналом

Удобнее всего держать на рабочем столе два ярлыка:

- **Divine Frequency (RU)** — запускает игру с `DF_RU.pk3`, конфиг `test/dfconfig-test.ini`, язык `ru`;
- **Divine Frequency (Original)** — запускает игру без PK3, конфиг `test/dfconfig-original.ini`, язык `enu` (чистый английский оригинал).

Они уже созданы скриптом `test/create_shortcuts.ps1`. Оба запускаются в полноэкранном режиме (`vid_fullscreen=true`, разрешение 2560×1440), поэтому их можно открыть по очереди и сравнивать один к одному. Конфиги разные, настройки не перемешиваются; основной `Documents\My Games\Divine Frequency\dfconfig.ini` не затрагивается.

Разница в языке специально оставлена: оригинал идёт с `language=enu`, RU — с `language=ru`. Если хочется сравнить именно оригинальный русский движковый интерфейс (который рассыпается без кириллицы в `BigUpper`/`ACS_FONT`), в `test/dfconfig-original.ini` можно поставить `language=auto` или `language=ru`.

Готовое сравнение меню: `test/screenshots/compare_main_menu.png`. Пересобрать его можно так:

```text
python tools/make_comparison.py
```

## Сборка

Нужен Python 3 и Pillow:

```text
python -m pip install pillow
python tools/extract_sources.py
python tools/make_bigfont_cyr.py
python tools/make_menudef.py
python tools/make_mapinfo.py
python tools/make_ui_overrides.py
python tools/build_pk3.py
python tools/make_translation_md.py
```

`make_bigfont_cyr.py` генерирует кириллицу для `bigfont` и `ACS_FONT`. `build_pk3.py` добавляет в PK3:

- `MenuDef` — полный перевод меню, включая новые `RU_`-меню настроек (защищённые оригинальные меню нельзя заменить напрямую);
- `Language.RU` — описания настроек;
- `MapInfo` — название сложности, эпизода, карт и сообщение выхода;
- `ZScript/UI/...` — загрузка/сохранение и `[Нажмите любую кнопку]`;
- `Fonts/bigfont/` — оригинальные глифы + кириллица; главное меню;
- `Fonts/BigUpper/` — шрифт настроек;
- `Fonts/ACS_FONT/` — кириллица для описаний;
- `Fonts/smallfont/` — кириллица для мелких надписей сохранений/загрузок.

Вкладки настроек используют оригинальный `BigUpper`; отдельного `Menu/tabmenu.zs` в сборке нет.

Готовый файл: `dist/DF_RU.pk3`.

`tools/extract_sources.py` извлекает текстовые исходники из `DFSDSA.ipk3` в `source/`. Скрипт не копирует огромные `TEXTMAP`-файлы карт; для перевода нужны только `DIALOGUE`, `SCRIPTS`, `Language.*` и исходники ZScript/ACS.

## Что ещё не так

- HUD, инвентарь и кодекс используют `DF_FONT`/`ChatBoxFont`, куда кириллица ещё не добавлена.
- Имена NPC используют `npcfont` (золотой шрифт с обводкой), туда кириллицу тоже нужно добавлять отдельно.
- Основной текст игры (`Language.Items`, `Language.Weapon`, `Language.Upgrade`, `Language.Map`, NPC-диалоги) пока не переведён — это следующие большие этапы.
- Меню переведено целиком; визуальная проверка вкладок, загрузки/сохранения и выхода — за тобой.

## Что дальше

1. Проверить текущую сборку в игре: главное меню, вкладки настроек, загрузка/сохранение, выход.
2. Добавить кириллицу в `DF_FONT`/`ChatBoxFont` для HUD и инвентаря.
3. Добавить кириллицу в `npcfont` с сохранением золотого стиля.
4. Начать перевод `Language.Items`, `Language.Weapon`, `Language.Upgrade`.
5. Затем `Language.Map`, NPC-диалоги и, в конце, ACS/`DIALOGUE` внутри карт.

## Структура проекта

```text
ANALYSIS.md          полный анализ
TRANSLATIONS.md      таблица переводов «что было → что стало»
AGENTS.md            правила и текущее состояние для агентов
README.md            этот файл
source/              извлечённые текстовые исходники игры
work/                исходники перевода
  MenuDef            перевод главного меню
  Fonts/bigfont/     кириллица для bigfont
  Fonts/ACS_FONT/    кириллица для ACS_FONT
dist/                собранные PK3
tools/               извлечение, шрифты, сборка, сравнение
test/                конфиги RU/оригинала, запуск, ярлыки, скриншоты
```

## Лицензии и правовой статус

Движок UZDoom распространяется по GPL. Ассеты Divine Frequency принадлежат Abraxaes LLC. Перевод для личного использования — это одно; публикация патча с изменёнными игровыми ассетами требует разрешения правообладателя. Шрифт Noto Sans используется по лицензии OFL; текст лицензии лежит в `source/fonts/OFL.txt`.
