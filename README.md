# RU Divine Frequency

Русский перевод **Divine Frequency** (UZDoom). Патч не изменяет файлы игры: перевод лежит во внешнем `DF_RU.pk3`.

- Репозиторий: https://github.com/dandyhorse/Divine-Frequency-RU
- Сборка: `dist/DF_RU.pk3`
- Языковой пакет для ревью/правок: `dist/DF_RU_language_pack.zip`
- Полные тексты на ревью: [review/DF_RU_text_review.md](review/DF_RU_text_review.md)
- Таблица «что было → что стало»: [TRANSLATIONS.md](TRANSLATIONS.md)
- Анализ и технические детали: [ANALYSIS.md](ANALYSIS.md)

## Что переведено

- Главное меню, сложность, настройки, загрузка/сохранение, выход.
- Шрифты с кириллицей: `bigfont`, `BigUpper`, `ACS_FONT`, `smallfont`, а также UI-шрифты `RU_DF_FONT`, `RU_ChatBoxFont`, `RU_CONVO_FONT`, `RU_npcfont`.
- HUD, инвентарь, кодекс, карта, типы предметов и улучшений.
- `Language.Weapon`, `Language.Items`, `Language.Upgrade`, `Language.Tutorial`, `Language.Objective`, `Language.Bestiary`, `Language.Note`, `Language.Artistical`, `Language.Map` (читаемые тексты), NPC-диалоги и инлайн-имена/реплики из `DIALOGUE`.

Остались только технические вещи: ACS-сообщения, скомпилированные в `BEHAVIOR` карт (`Key_Message`, `map_func`), и часть терминальных логов/шифров в `Language.Map`. Меню и остальной UI от этого не зависят.

## Запуск

```text
test\run_test.cmd
```

Оригинал для сравнения:

```text
test\run_original.cmd
```

Скрипты используют отдельные копии конфига и не трогают основной `dfconfig.ini`.

Вручную:

```text
DivineFrequency.exe -file "C:\projects\RU_DivineFrequency\dist\DF_RU.pk3" -config "C:\projects\RU_DivineFrequency\test\dfconfig-test.ini"
```

## Сборка

Нужен Python 3 и Pillow:

```text
python -m pip install pillow
python tools/extract_sources.py
python tools/make_bigfont_cyr.py
python tools/make_ui_fonts_cyr.py
python tools/make_menudef.py
python tools/make_mapinfo.py
python tools/make_ui_overrides.py
python tools/build_pk3.py
python tools/make_translation_md.py
python tools/make_review_md.py
```

`extract_sources.py` извлекает текстовые исходники из `DFSDSA.ipk3` в `source/`. `make_ui_fonts_cyr.py` генерирует `RU_DF_FONT`, `RU_ChatBoxFont`, `RU_CONVO_FONT` и `RU_npcfont`. `make_review_md.py` собирает `review/DF_RU_text_review.md` с парами EN/RU для ревьюера.

## Сохранения

Сейвы, созданные под RU-патчем, содержат в `info.json` русские названия карт и `Время:` в комментарии. Если открыть такой сейв в английской версии, в списке сохранений может появиться русский текст и fallback-шрифт. Для standalone-сборки планируется отдельная папка сейвов через `-savedir`; это исключит смешивание RU и оригинальных сохранений. Подробнее — в разделе Releases/README standalone-пакета.

## Структура

```text
ANALYSIS.md          анализ игры
TRANSLATIONS.md      таблица переводов
AGENTS.md            правила и текущее состояние для агентов
README.md            этот файл
review/              полные тексты EN/RU для ревью
source/              извлечённые исходники игры
work/                исходники перевода
dist/                собранные PK3/пакеты
tools/               извлечение, шрифты, меню, сборка, отчёты
test/                конфиги, запуск, ярлыки, скриншоты
```

## Лицензии и правовой статус

Движок UZDoom распространяется по GPL. Ассеты Divine Frequency принадлежат Abraxaes LLC. Перевод публикуется по согласованию с разработчиками; для распространения сторонних сборок игры нужна отдельная проверка прав. Шрифт Noto Sans используется по лицензии OFL, текст лицензии — в `source/fonts/OFL.txt`.
