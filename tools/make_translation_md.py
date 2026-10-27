import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "TRANSLATIONS.md")


def esc(s):
    return s.replace("|", r"\|")


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(esc(x) for x in row) + " |")
    return "\n".join(out)


def lang_values(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"//[^\n]*", "", text)
    values = {}
    for m in re.finditer(r'(?ms)^\s*([A-Za-z0-9_]+)\s*=\s*((?:"(?:[^"\\]|\\.)*"\s*)+);', text):
        values[m.group(1)] = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
    return values


main = [
    ("New Game", "Новая игра", "MenuDef → MainMenu"),
    ("Options", "Настройки", "MenuDef → MainMenu"),
    ("Load Game", "Загрузить игру", "MenuDef → MainMenu"),
    ("Save Game", "Сохранить игру", "MenuDef → MainMenu"),
    ("Credits", "Титры", "MenuDef → MainMenu"),
    ("Quit", "Выход", "MenuDef → MainMenu"),
]

skill_maps = [
    ("Select Difficulty:", "Выберите сложность:", "MenuDef → SkillMenu"),
    ("Standard", "Обычная", "MapInfo → Skill normal → Name"),
    ("Confirm starting a New Game?", "Начать новую игру?", "MapInfo → Skill normal → mustconfirm"),
    ("Main Story", "Основная история", "MapInfo → episode map01"),
    ("Title", "Заголовок", "MapInfo → map TITLEMAP"),
    ("ACT I - Metempsychosis", "АКТ I — Метемпсихоз", "MapInfo → карты MAP01–05, MAP30–31"),
    ("ACT II - Pure Naked Minds", "АКТ II — Чистые обнажённые умы", "MapInfo → карты MAP06–16"),
    ("ACT III - Without Center or Circumference", "АКТ III — Без центра и окружности", "MapInfo → карты MAP17–18"),
    ("To The Edge of Existence", "К краю бытия", "MapInfo → карта MAP19"),
    ("Do you want to quit?", "Вы действительно хотите выйти?", "MapInfo → GameInfo → quitmessages (движковый default)"),
]

tabs = [
    ("Graphics", "Графика", "MenuDef → TabTest"),
    ("Control", "Управление", "MenuDef → TabTest"),
    ("Audio", "Звук", "MenuDef → TabTest"),
    ("Accessibility", "Доступность", "MenuDef → TabTest"),
]

display = [
    ("Resolution Width", "Ширина разрешения", "MenuDef → RU_DFDisplayOptions"),
    ("Resolution Height", "Высота разрешения", "MenuDef → RU_DFDisplayOptions"),
    ("VHS Intensity", "Интенсивность VHS", "MenuDef → RU_DFDisplayOptions"),
    ("VHS Tearing", "Разрыв VHS", "MenuDef → RU_DFDisplayOptions"),
    ("HUD Size", "Размер HUD", "MenuDef → RU_DFDisplayOptions"),
]

keybinds = [
    ("Keybinds", "Управление", "MenuDef → RU_DFKeyBinds → Title"),
    ("Camera Horizontal Sensitivity", "Горизонтальная чувствительность камеры", "RU_DFKeyBinds"),
    ("Camera Vertical Sensitivity", "Вертикальная чувствительность камеры", "RU_DFKeyBinds"),
    ("--MOVEMENT--", "--ДВИЖЕНИЕ--", "RU_DFKeyBinds"),
    ("Move Forward", "Вперёд", "RU_DFKeyBinds"),
    ("Move Backward", "Назад", "RU_DFKeyBinds"),
    ("Strafe Left", "Влево", "RU_DFKeyBinds"),
    ("Strafe Right", "Вправо", "RU_DFKeyBinds"),
    ("Jump", "Прыжок", "RU_DFKeyBinds"),
    ("Crouch (Toggle)", "Присесть (переключение)", "RU_DFKeyBinds"),
    ("Crouch (Hold)", "Присесть (удержание)", "RU_DFKeyBinds"),
    ("Sprint (Hold)", "Бег (удержание)", "RU_DFKeyBinds"),
    ("Dash", "Рывок", "RU_DFKeyBinds"),
    ("--INTERACTION--", "--ВЗАИМОДЕЙСТВИЕ--", "RU_DFKeyBinds"),
    ("Primary Fire", "Основной огонь", "RU_DFKeyBinds"),
    ("Secondary Fire", "Альтернативный огонь", "RU_DFKeyBinds"),
    ("Reload", "Перезарядка", "RU_DFKeyBinds"),
    ("Primary Interact", "Основное взаимодействие", "RU_DFKeyBinds"),
    ("Secondary Interact", "Дополнительное взаимодействие", "RU_DFKeyBinds"),
    ("Change Firing Mode", "Сменить режим стрельбы", "RU_DFKeyBinds"),
    ("Next Weapon", "Следующее оружие", "RU_DFKeyBinds"),
    ("Previous Weapon", "Предыдущее оружие", "RU_DFKeyBinds"),
    ("--ADDITIONAL INTERACTION--", "--ДОПОЛНИТЕЛЬНОЕ ВЗАИМОДЕЙСТВИЕ--", "RU_DFKeyBinds"),
    ("Open Inventory", "Открыть инвентарь", "RU_DFKeyBinds"),
    ("Open Map", "Открыть карту", "RU_DFKeyBinds"),
    ("Use Psykhus Injector", "Использовать инъектор Психуса", "RU_DFKeyBinds"),
    ("Use Quick Item 1", "Быстрый предмет 1", "RU_DFKeyBinds"),
    ("Use Quick Item 2", "Быстрый предмет 2", "RU_DFKeyBinds"),
    ("Use Quick Item 3", "Быстрый предмет 3", "RU_DFKeyBinds"),
    ("Use Quick Item 4", "Быстрый предмет 4", "RU_DFKeyBinds"),
    ("Select Weapon Slot 1", "Слот оружия 1", "RU_DFKeyBinds"),
    ("Select Weapon Slot 2", "Слот оружия 2", "RU_DFKeyBinds"),
    ("Select Weapon Slot 3", "Слот оружия 3", "RU_DFKeyBinds"),
    ("Select Weapon Slot 4", "Слот оружия 4", "RU_DFKeyBinds"),
    ("--GAME STATE--", "--СОСТОЯНИЕ ИГРЫ--", "RU_DFKeyBinds"),
    ("Quicksave", "Быстрое сохранение", "RU_DFKeyBinds"),
    ("Quickload", "Быстрая загрузка", "RU_DFKeyBinds"),
    ("--INVENTORY UI--", "--ИНТЕРФЕЙС ИНВЕНТАРЯ--", "RU_DFKeyBinds"),
    ("Interaction Layout", "Раскладка взаимодействия", "RU_DFKeyBinds"),
]

advanced = [
    ("Advanced", "Дополнительно", "MenuDef → RU_DFAdvancedOptions → Title"),
    ("--DIFFICULTY--", "--СЛОЖНОСТЬ--", "RU_DFAdvancedOptions"),
    ("Player Damage Taken", "Получаемый урон", "RU_DFAdvancedOptions"),
    ("Ammo Received", "Получаемые патроны", "RU_DFAdvancedOptions"),
    ("Consumable Healing Rate", "Эффективность лечения расходниками", "RU_DFAdvancedOptions"),
    ("Stamina Consumption", "Расход выносливости", "RU_DFAdvancedOptions"),
    ("Weapon Degredation Rate", "Скорость износа оружия", "RU_DFAdvancedOptions"),
    ("Resonance Break: Extended Timing", "Разрыв резонанса: расширенное окно", "RU_DFAdvancedOptions"),
    ("--GAMEPLAY--", "--ИГРОВОЙ ПРОЦЕСС--", "RU_DFAdvancedOptions"),
    ("Damage Number", "Числа урона", "RU_DFAdvancedOptions"),
    ("HUD (Heads-Up Display)", "HUD (интерфейс)", "RU_DFAdvancedOptions"),
    ("Interaction Icon", "Значок взаимодействия", "RU_DFAdvancedOptions"),
    ("Item Tooltip", "Подсказка предмета", "RU_DFAdvancedOptions"),
    ("Melee Camera Movement", "Движение камеры в ближнем бою", "RU_DFAdvancedOptions"),
    ("Nulled Landscape Distortion", "Искажение Nulled Landscape", "RU_DFAdvancedOptions"),
    ("Trenchgun Crosshair", "Прицел траншейного ружья", "RU_DFAdvancedOptions"),
    ("Tutorials", "Обучение", "RU_DFAdvancedOptions"),
    ("--MISCELLANEOUS--", "--РАЗНОЕ--", "RU_DFAdvancedOptions"),
    ("Item Pickup Flash Intensity", "Яркость вспышки при подборе", "RU_DFAdvancedOptions"),
    ("Damage Taken Flash Intensity", "Яркость вспышки при получении урона", "RU_DFAdvancedOptions"),
    ("Crosshair Color Match Health", "Цвет прицела по здоровью", "RU_DFAdvancedOptions"),
]

joystick_brightness = [
    ("WARNING: Controller Support is not fully implemented!", "ВНИМАНИЕ: Поддержка контроллера реализована не полностью!", "MenuDef → RU_NewJoystickOptions → Title"),
    ("Adjust the slider until you can slightly spot the figure in the background.", "Настройте ползунок, пока едва не начнёте различать фигуру на фоне.", "MenuDef → BrightnessAdjust → Title"),
]

option_values = [
    ("Off", "Выкл.", "MenuDef → OptionValue (CrosshairHealthTypes, vhss, boboption, flashoption, painflashoption)"),
    ("On", "Вкл.", "MenuDef → OptionValue → CrosshairHealthTypes"),
    ("Minimal", "Минимум", "MenuDef → OptionValue (vhss, boboption, flashoption, painflashoption)"),
    ("Default", "По умолчанию", "MenuDef → OptionValue (vhss, boboption, painflashoption)"),
    ("Can't See Sh!t", "Ничего не видно", "MenuDef → OptionValue → vhss"),
    ("Unplayable", "Неиграбельно", "MenuDef → OptionValue → boboption"),
    ("Eye Damage", "Вред глазам", "MenuDef → OptionValue → flashoption"),
    ("Standard", "Стандарт", "MenuDef → OptionValue (skill_ammo, skill_damage, skill_heal, skill_stamina, skill_weapon)"),
    ("Doubled", "Удвоено", "MenuDef → OptionValue (skill_ammo, skill_heal)"),
    ("Halved", "Половинный", "MenuDef → OptionValue → skill_damage"),
    ("None", "Нет", "MenuDef → OptionValue (skill_stamina, skill_weapon)"),
    ("Disabled", "Отключено", "MenuDef → OptionValue → skill_parry"),
    ("Enabled", "Включено", "MenuDef → OptionValue → skill_parry"),
    ("Mouse1: Use Item | Mouse2: Options", "ЛКМ: использовать | ПКМ: настройки", "MenuDef → OptionValue → InvClickSwap"),
    ("Mouse1: Options | Mouse2: Use Item", "ЛКМ: настройки | ПКМ: использовать", "MenuDef → OptionValue → InvClickSwap"),
]

loadsave = [
    ("Load Game", "Загрузить игру", "ZScript/UI/UIZForms/Load Menu/LoadMenu.zsc"),
    ("Save Game", "Сохранить игру", "ZScript/UI/UIZForms/Save Menu/SaveMenu.zsc"),
    (r"Delete Save?\n", r"Удалить сохранение?\n", "LoadSaveBase.zsc → ConfirmDelete"),
    (r"DELETE \cU(Y)", r"УДАЛИТЬ \cU(Y)", "LoadSaveBase.zsc → ConfirmDelete"),
    (r"CANCEL \cU(N)", r"ОТМЕНА \cU(N)", "LoadSaveBase.zsc → ConfirmDelete"),
    ("Overwrite Save?", "Перезаписать сохранение?", "LoadSaveBase.zsc → ConfirmOverwrite"),
    (r"SAVE \cU(Y)", r"СОХРАНИТЬ \cU(Y)", "LoadSaveBase.zsc → ConfirmOverwrite"),
    (r"CANCEL \cU(N)", r"ОТМЕНА \cU(N)", "LoadSaveBase.zsc → ConfirmOverwrite"),
    ("Create New Save?", "Создать новое сохранение?", "LoadSaveBase.zsc → CreateNewSave"),
    ("Confirm", "Подтвердить", "LoadSaveBase.zsc → CreateNewSave"),
    ("Cancel", "Отмена", "LoadSaveBase.zsc → CreateNewSave"),
    (r"Cannot Save while on the title screen \n Please load or start a new game to save!",
     r"На титульном экране сохраняться нельзя.\nЗагрузите игру или начните новую, чтобы сохраниться!",
     "SaveMenu.zsc → MainMenuText"),
    ("Time: ", "Время: ", "LoadMenu.zsc / SaveMenu.zsc → SaveSlotSaveAge"),
    ("Date: ", "Дата: ", "LoadMenu.zsc / SaveMenu.zsc → SaveSlotTimeSaved"),
]

title_prompt = [
    ("[Press any button]", "[Нажмите любую кнопку]", "ZScript/UI/GenericScreenStuff.txt"),
]

desc_en = lang_values(os.path.join(ROOT, "source", "Language.txt"))
desc_ru = lang_values(os.path.join(ROOT, "work", "Language.RU"))
descriptions = []
for key, value in desc_en.items():
    if key.startswith("DESC_"):
        descriptions.append((key, value, desc_ru.get(key, "—")))

ru_menus = [
    ("DFDisplayOptions (protected)", "RU_DFDisplayOptions", "TabTest → Графика"),
    ("DFKeyBinds (protected)", "RU_DFKeyBinds", "TabTest → Управление"),
    ("DFSoundOptions (protected)", "RU_DFSoundOptions", "TabTest → Звук"),
    ("DFAdvancedOptions (protected)", "RU_DFAdvancedOptions", "TabTest → Доступность"),
    ("NewJoystickOptions (protected)", "RU_NewJoystickOptions", "RU_DFAdvancedOptions → Субменю джойстика"),
]

fonts = [
    ("bigfont: 256 латинских глифов", "Полный набор + 74 глифа: 33 заглавные, 33 строчные (включая Ё/ё) и 8 типографских знаков; используется в главном меню", "Fonts/bigfont/"),
    ("BigUpper: движковый английский шрифт настроек", "Полная копия bigfont + кириллица", "Fonts/BigUpper/"),
    ("ACS_FONT: 592 латинских глифа", "Полный набор + 74 глифа для описаний/HUD-сообщений", "Fonts/ACS_FONT/"),
    ("smallfont: 592 латинских глифа", "Полный набор + 74 глифа для сохранений/загрузок", "Fonts/smallfont/"),
    ("NewSmallFont: встроенный hex-шрифт", "Не используется после возврата к BIGFONT", "—"),
    ("dialoguefont: уже с кириллицей", "Не менялся", "Fonts/dialoguefont/"),
    ("npcfont, DF_FONT, CONVO_FONT, ChatBoxFont", "Не менялись; кириллицы пока нет", "Вне текущего объёма"),
]

layout = [
    ("Главное меню: NewSmallFont, золотой выбранный пункт", "BIGFONT (оригинальный шрифт); выбранный пункт белый + подсветка рамкой"),
    ("Позиции пунктов 128/136/127/127/138/147", "124/126/111/110/140/140 — под русские подписи BIGFONT, центр 160"),
    ("Вкладки настроек: BIGFONT через Menu/tabmenu.zs", "Оригинальный BigUpper; отдельный font override убран; подписи вкладок переведены"),
    ("Настройки: protected OptionMenu с английскими подписями", "Новые RU_-меню; вкладки ведут на них"),
    ("Настройки: описания из Language.txt на английском", "Language.RU с [ru]-секциями для всех DESC_*"),
    ("Загрузка/сохранение: английские заголовки и попапы", "Русские заголовки, попапы, кнопки, Время/Дата"),
    ("Карта/сложность/эпизод/выход: английские", "Переведены в MapInfo"),
    ("Титульный экран: [Press any button]", "[Нажмите любую кнопку]"),
]

not_translated = [
    ("HUD, инвентарь, кодекс", "DF_FONT / ChatBoxFont; кириллица не добавлена"),
    ("Имена NPC", "npcfont; кириллица не добавлена"),
    ("Сюжетный текст", "Language.Items, Language.Weapon, Language.Upgrade, Language.Map, Language.NPC*"),
    ("ACS и диалоги карт", "ACS/*.acs, SCRIPTS/BEHAVIOR, DIALOGUE"),
    ("Озвучка", "Остаётся английской; перевод текстовый"),
]

total = sum(len(x) for x in [main, skill_maps, tabs, display, keybinds, advanced, joystick_brightness, option_values, loadsave, title_prompt])
total += len(descriptions)

lines = []
lines.append("# Divine Frequency — таблица перевода меню")
lines.append("")
lines.append("Дата: 27.10.2026")
lines.append("")
lines.append("Сборка: `dist/DF_RU.pk3` — 2003 записи, ~940 КБ.")
lines.append("")
lines.append("Формат: каждая секция содержит таблицу **«что было → что стало»**. В колонке «Где» указан файл/блок, где применён перевод.")
lines.append("")
lines.append(f"Всего текстовых строк в таблицах: **{total}** (включая {len(descriptions)} описаний `DESC_*`).")
lines.append("")
lines.append("## 1. Главное меню")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], main))
lines.append("")
lines.append("## 2. Сложность, карты и выход")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], skill_maps))
lines.append("")
lines.append("## 3. Вкладки настроек")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], tabs))
lines.append("")
lines.append("## 4. Графика")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], display))
lines.append("")
lines.append("Остальные подписи вкладки «Графика» (`$VIDMNU_*`, `$DSPLYMNU_*`, `$GLPREFMNU_*`) берутся из `language.csv` и уже локализованы движком.")
lines.append("")
lines.append("## 5. Управление")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], keybinds))
lines.append("")
lines.append("## 6. Дополнительно / Доступность")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], advanced))
lines.append("")
lines.append("## 7. Джойстик и яркость")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], joystick_brightness))
lines.append("")
lines.append("## 8. Значения опций")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], option_values))
lines.append("")
lines.append("## 9. Описания настроек (`Language.RU`)")
lines.append("")
lines.append(table(["Ключ", "Что было (EN)", "Что стало (RU)"], descriptions))
lines.append("")
lines.append("## 10. Загрузка и сохранение")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], loadsave))
lines.append("")
lines.append("## 11. Титульный экран")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], title_prompt))
lines.append("")
lines.append("## 12. Шрифты")
lines.append("")
lines.append(table(["Что было", "Что стало", "Где"], fonts))
lines.append("")
lines.append("Папки шрифтов в UZDoom загружаются атомарно, поэтому в PK3 кладутся полные наборы: оригинальные PNG + `font.inf` + кириллица.")
lines.append("")
lines.append("## 13. Вёрстка и техническая часть")
lines.append("")
lines.append(table(["Что было", "Что стало"], layout))
lines.append("")
lines.append("### Новые меню настроек")
lines.append("")
lines.append(table(["Было", "Стало", "Где используется"], ru_menus))
lines.append("")
lines.append("## 14. Что не переведено в этой итерации")
lines.append("")
lines.append(table(["Раздел", "Статус"], not_translated))
lines.append("")
lines.append("## 15. Запуск")
lines.append("")
lines.append("- `test/run_test.cmd` или ярлык **Divine Frequency (RU)** — полный экран, `language=ru`.")
lines.append("- `test/run_original.cmd` или ярлык **Divine Frequency (Original)** — полный экран, `language=enu`.")
lines.append("- Конфиги: `test/dfconfig-test.ini` и `test/dfconfig-original.ini`; основной `dfconfig.ini` не изменяется.")
lines.append("")
lines.append("Проверка сборки: запуск с `-stdout` — ZScript компилируется, ошибок нет. Визуальная проверка — за тобой.")
lines.append("")

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines))
print(f"Wrote {OUT}")
print(f"Text rows: {total}, descriptions: {len(descriptions)}")
