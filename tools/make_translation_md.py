import os
import re
import zipfile

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
    ("Title", "Титульный экран", "MapInfo → map TITLEMAP"),
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
    ("Accessibility", "Специальные возможности", "MenuDef → TabTest"),
]

display = [
    ("Resolution Width", "Ширина (пикс.)", "MenuDef → RU_DFDisplayOptions"),
    ("Resolution Height", "Высота (пикс.)", "MenuDef → RU_DFDisplayOptions"),
    ("VHS Intensity", "Интенсивность VHS-эффекта", "MenuDef → RU_DFDisplayOptions"),
    ("VHS Tearing", "Разрывы изображения (VHS)", "MenuDef → RU_DFDisplayOptions"),
    ("HUD Size", "Размер HUD", "MenuDef → RU_DFDisplayOptions"),
]

keybinds = [
    ("Keybinds", "Назначение клавиш", "MenuDef → RU_DFKeyBinds → Title"),
    ("Camera Horizontal Sensitivity", "Чувствительность камеры по горизонтали", "RU_DFKeyBinds"),
    ("Camera Vertical Sensitivity", "Чувствительность камеры по вертикали", "RU_DFKeyBinds"),
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
    ("Use Quick Item 1", "Использовать быстрый предмет 1", "RU_DFKeyBinds"),
    ("Use Quick Item 2", "Использовать быстрый предмет 2", "RU_DFKeyBinds"),
    ("Use Quick Item 3", "Использовать быстрый предмет 3", "RU_DFKeyBinds"),
    ("Use Quick Item 4", "Использовать быстрый предмет 4", "RU_DFKeyBinds"),
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
    ("Ammo Received", "Количество получаемых патронов", "RU_DFAdvancedOptions"),
    ("Consumable Healing Rate", "Эффективность лечебных предметов", "RU_DFAdvancedOptions"),
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
    ("Crosshair Color Match Health", "Цвет прицела по уровню здоровья", "RU_DFAdvancedOptions"),
]

joystick_brightness = [
    ("WARNING: Controller Support is not fully implemented!", "ВНИМАНИЕ: Поддержка контроллера реализована не полностью!", "MenuDef → RU_NewJoystickOptions → Title"),
    ("Adjust the slider until you can slightly spot the figure in the background.", "Передвигайте ползунок, пока фигура на фоне не станет едва различимой.", "MenuDef → BrightnessAdjust → Title"),
]

option_values = [
    ("Off", "Выкл.", "MenuDef → OptionValue (CrosshairHealthTypes, vhss, boboption, flashoption, painflashoption)"),
    ("On", "Вкл.", "MenuDef → OptionValue → CrosshairHealthTypes"),
    ("Minimal", "Минимум", "MenuDef → OptionValue (vhss, boboption, flashoption, painflashoption)"),
    ("Default", "По умолчанию", "MenuDef → OptionValue (vhss, boboption, painflashoption)"),
    ("Can't See Sh!t", "Ни хрена не видно", "MenuDef → OptionValue → vhss"),
    ("Unplayable", "Неиграбельно", "MenuDef → OptionValue → boboption"),
    ("Eye Damage", "Вред глазам", "MenuDef → OptionValue → flashoption"),
    ("Standard", "Стандарт", "MenuDef → OptionValue (skill_ammo, skill_damage, skill_heal, skill_stamina, skill_weapon)"),
    ("Doubled", "Вдвое больше", "MenuDef → OptionValue (skill_ammo, skill_heal)"),
    ("Halved", "Вдвое меньше", "MenuDef → OptionValue → skill_damage"),
    ("None", "Нет", "MenuDef → OptionValue (skill_stamina, skill_weapon)"),
    ("Disabled", "Отключено", "MenuDef → OptionValue → skill_parry"),
    ("Enabled", "Включено", "MenuDef → OptionValue → skill_parry"),
    ("Mouse1: Use Item | Mouse2: Options", "ЛКМ: использовать | ПКМ: действия", "MenuDef → OptionValue → InvClickSwap"),
    ("Mouse1: Options | Mouse2: Use Item", "ЛКМ: действия | ПКМ: использовать", "MenuDef → OptionValue → InvClickSwap"),
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

ui_pilot = [
    ("Consumables & Medications (%d/%d)", "Расходники и медикаменты (%d/%d)", "InventoryMenu.zc → conTitle"),
    ("Key Items", "Ключевые предметы", "InventoryMenu.zc → subHead2"),
    ("Abilities", "Способности", "InventoryMenu.zc → subHead3"),
    ("Attribute", "Характеристики", "InventoryMenu.zc → AtrTextHeader"),
    ("Condition", "Состояние", "InventoryMenu.zc → CStateTextHeader"),
    ("Current Objective", "Текущая цель", "InventoryMenu.zc → ObjHeader"),
    ("Description:", "Описание:", "InventoryMenu.zc → itemTextHeader"),
    ("Location: %s", "Локация: %s", "InventoryMenu.zc → LocationName"),
    ("Assign to Quick Use", "Назначить на быстрое использование", "InventoryMenu.zc → BindingLabel"),
    (r"\cD[Mouse1] \cJUse Item", r"\cD[ЛКМ] \cJИспользовать", "InventoryMenu.zc → m1Tip"),
    (r"\cD[Mouse2] \cJOptions", r"\cD[ПКМ] \cJДействия", "InventoryMenu.zc → m2Tip"),
    ("Inventory", "Инвентарь", "Верхние вкладки (5 файлов)"),
    ("Weapons", "Оружие", "Верхние вкладки (5 файлов)"),
    ("Bestiary", "Бестиарий", "Верхние вкладки (5 файлов)"),
    ("Map", "Карта", "Верхние вкладки (5 файлов)"),
    ("Help", "Помощь", "Верхние вкладки (5 файлов)"),
    ("Effect:", "Эффект:", "InventoryMenu.zc → itemEffectHeader"),
    (r"LEVEL %d Avatar:\n%s\n\nStrength: %d\nWits: %d\nPhysique: %d\n\n    Exaltation: %d\n    Mutation: %d\n    Psi. Attunement: %d/%d",
     r"УРОВЕНЬ %d Аватар:\n%s\n\nСила: %d\nРазум: %d\nТелосложение: %d\n\n    Экзальтация: %d\n    Мутация: %d\n    Пси-настройка: %d/%d",
     "InventoryMenu.zc → Attribute"),
    (r"Toxin (Lethal)\n\cR-Suffer Periodic Damage\n-Impaired Movement\n-Impaired Aim\n\n",
     r"Токсин (смертельный)\n\cR-Периодический урон\n-Нарушение движения\n-Нарушение прицеливания\n\n",
     "InventoryMenu.zc → Condition"),
    (r"Toxin (Moderate)\n\cR-Impaired Aim\n\n",
     r"Токсин (умеренный)\n\cR-Нарушение прицеливания\n\n",
     "InventoryMenu.zc → Condition"),
    (r"\cJRadiation (Lethal)\n\cR-Imminent Overload\n-Impaired Vision\n\n",
     r"\cJРадиация (смертельная)\n\cR-Неминуемая перегрузка\n-Нарушение зрения\n\n",
     "InventoryMenu.zc → Condition"),
    (r"\cJRadiation (Moderate)\n\cR-Impaired Vision\n\n",
     r"\cJРадиация (умеренная)\n\cR-Нарушение зрения\n\n",
     "InventoryMenu.zc → Condition"),
    ("Use Item", "Использовать", "InventoryMenu.zc → epUse"),
    ("Drop Item", "Выбросить", "InventoryMenu.zc → epDrop"),
    ("Keybind", "Привязать", "InventoryMenu.zc → epBind"),
    ("Handgun: %d", "Пистолет: %d", "InventoryMenu.zc → ремонт"),
    ("Trenchgun: %d", "Траншейка: %d", "InventoryMenu.zc → ремонт"),
    ("Spray Can: %d", "Баллончик: %d", "InventoryMenu.zc → ремонт"),
    ("Assault Rifle: %d", "Автомат: %d", "InventoryMenu.zc → ремонт"),
    ("Enhancements", "Улучшения", "Codex.txt → кнопка"),
    ("Information:", "Информация:", "Codex.txt → wInfoHeader"),
    ("Secondary Fire:", "Альтернативный огонь:", "Codex.txt → wAbilityHeader"),
    ("Additional Mechanics:", "Дополнительные механики:", "Codex.txt → wQuirkHeader"),
    ("Weapon Modifications:", "Модификации оружия:", "Codex.txt → Info_Upgrade"),
    ("Character Ascension:", "Возвышение персонажа:", "Codex.txt → Info_Upgrade"),
    ("Unique:", "Уникальное:", "Codex.txt → Info_Upgrade"),
    ("[W][A][S][D] - Movement / [E] - Interact", "[W][A][S][D] - Движение / [E] - Взаимодействие", "GenericScreenStuff.txt → tutorial"),
    ("Information:", "Информация:", "Bestiary.txt → bPhyHeader"),
    ("Additional Data:", "Дополнительные данные:", "Bestiary.txt → bPhyHeader2"),
    ("Snapshot:", "Снимок:", "Bestiary.txt → bImageHeader"),
    ("Archive:", "Архив:", "Bestiary.txt → bLoreHeader"),
    ("Hobo", "Бродяга", "Player.txt → title"),
    ("Mutation Lv.1", "Мутация ур.1", "Player.txt → phyLevel_nfo"),
]

ui_upgrades = [
    ("Enter Character Name:", "Введите имя персонажа:", "CreationMenu.zc"),
    ("Accept", "Принять", "CreationMenu.zc"),
    ("Barrel Mod", "Модификация ствола", "GunUpgrade.zc"),
    ("Extended Magazine", "Увеличенный магазин", "GunUpgrade.zc"),
    ("Exotic Powder Mixture", "Экзотическая пороховая смесь", "GunUpgrade.zc"),
    ("Current Exaltation: %d", "Текущая экзальтация: %d", "LevelUpMenu.zc"),
    ("Upgrade %s: %d -> %d", "Улучшение %s: %d -> %d", "LevelUpMenu.zc"),
    ("Cost: %d", "Стоимость: %d", "LevelUpMenu.zc"),
    ("Strength / Wits / Physique", "Сила / Разум / Телосложение", "LevelUpMenu.zc"),
    ("SECONDARY ATTRIBUTES", "ВТОРИЧНЫЕ АТРИБУТЫ", "LevelUpMenu.zc"),
    ("Exaltation / Mutation", "Экзальтация / Мутация", "LevelUpMenu.zc"),
    ("Confirm Selection:", "Подтвердить выбор:", "LevelUpMenu.zc / ShopMenu.zc"),
    ("Confirm / Cancel", "Подтвердить / Отмена", "UIUpgrades/*.zc"),
    ("[Esc] Leave", "[Esc] Выйти", "UIUpgrades/*.zc / NewItemMenu.zc"),
    ("Survival Response", "Реакция выживания", "ShopMenu.zc"),
    ("Third Mind", "Третий разум", "ShopMenu.zc"),
    ("Predatory Focus", "Хищный фокус", "ShopMenu.zc"),
    ("Even More Pockets!", "Ещё больше карманов!", "ShopMenu.zc"),
    ("Reflect Damage", "Отражение урона", "ShopMenu.zc"),
    ("Endless Hunger", "Бесконечный голод", "ShopMenu.zc"),
    ("Organic Caltrops", "Органические шипы", "ShopMenu.zc"),
    ("Psychic Blast", "Психический взрыв", "ShopMenu.zc"),
    ("Current Mutation Point: %d", "Текущие очки мутации: %d", "ShopMenu.zc"),
    ("Max", "Макс.", "Hud.txt"),
]

desc_en = lang_values(os.path.join(ROOT, "source", "Language.txt"))
desc_ru = lang_values(os.path.join(ROOT, "work", "Language.RU"))
descriptions = []
for key, value in desc_en.items():
    if key.startswith("DESC_"):
        descriptions.append((key, value, desc_ru.get(key, "—")))

weapon_en = lang_values(os.path.join(ROOT, "source", "Language.Weapon.txt"))
weapon_ru = lang_values(os.path.join(ROOT, "work", "Language.Weapon.txt"))
weapon_translations = []
for key, value in weapon_en.items():
    if key in weapon_ru:
        weapon_translations.append((key, value.replace("\n", "<br>"), weapon_ru[key].replace("\n", "<br>")))

npc_files = [
    ("Language.NPC", "Создание персонажа, UI диалогов, Spray/Vial, ODD_DEVICE"),
    ("Language.NPCBox", "Первый NPC «Подозрительная коробка»"),
    ("Language.NPCDisciples", "Холодильник/Ученик Рааха и ученик Сджинна"),
    ("Language.NPCLantern", "Говорящий фонарь"),
    ("Language.NPCMISC", "Инженер, врата, труп"),
    ("Language.NPCMonastery", "Алтарь и аномальный гриб"),
    ("Language.NPCPrism", "Таинственная призма: читаемые имена/выборы; шифрованный текст оставлен"),
    ("Language.NPCDreamer", "Сновидец и ученик Сармипадхвы (активные ключи)"),
    ("Language.NPCEgg", "Яйцо и броня"),
    ("Language.NPCADB", "Актор Чувак Братан, пси-способности; закомментированный блок не переводился"),
    ("Language.NPCAstronaut", "Астронавт: читаемые реплики и хроника; искажённый текст оставлен"),
    ("Language.Duel", "Дуэли и заметки"),
    ("Language.Weapon.txt", "Оружие; DB_* (молот) оставлены"),
]
npc_rows = []
for file, desc in npc_files:
    en = lang_values(os.path.join(ROOT, "source", file))
    ru = lang_values(os.path.join(ROOT, "work", file))
    npc_rows.append((file, f"{len(ru)}/{len(en)}", desc))

content_files = [
    ("Language.Items.txt", "Предметы, расходники, ключи"),
    ("Language.Upgrade.txt", "Улучшения, мутации, способности"),
    ("Language.Tutorial", "Подсказки и советы"),
    ("Language.Objective", "Цели"),
    ("Language.Bestiary.txt", "Бестиарий"),
    ("Language.Note.txt", "Заметки и записи"),
    ("Language.Artistical", "Лор и вступление"),
    ("Language.Map", "Карта: читаемые тексты; технические логи оставлены"),
]
content_rows = []
for file, desc in content_files:
    en = lang_values(os.path.join(ROOT, "source", file))
    ru = lang_values(os.path.join(ROOT, "work", file)) if os.path.isfile(os.path.join(ROOT, "work", file)) else {}
    content_rows.append((file, f"{len(ru)}/{len(en)}", desc))

ru_menus = [
    ("DFDisplayOptions (protected)", "RU_DFDisplayOptions", "TabTest → Графика"),
    ("DFKeyBinds (protected)", "RU_DFKeyBinds", "TabTest → Управление"),
    ("DFSoundOptions (protected)", "RU_DFSoundOptions", "TabTest → Звук"),
    ("DFAdvancedOptions (protected)", "RU_DFAdvancedOptions", "TabTest → Специальные возможности"),
    ("NewJoystickOptions (protected)", "RU_NewJoystickOptions", "RU_DFAdvancedOptions → Субменю джойстика"),
]

fonts = [
    ("bigfont: 256 латинских глифов", "Полный набор + 74 глифа: 33 заглавные, 33 строчные (включая Ё/ё) и 8 типографских знаков; используется в главном меню", "Fonts/bigfont/"),
    ("BigUpper: движковый английский шрифт настроек", "Полная копия bigfont + кириллица", "Fonts/BigUpper/"),
    ("ACS_FONT: 592 латинских глифа", "Полный набор + 74 глифа для описаний/HUD-сообщений", "Fonts/ACS_FONT/"),
    ("smallfont: 592 латинских глифа", "Полный набор + 74 глифа для сохранений/загрузок", "Fonts/smallfont/"),
    ("NewSmallFont: встроенный hex-шрифт", "Не используется после возврата к BIGFONT", "—"),
    ("dialoguefont: уже с кириллицей", "Не менялся; используется для реплик", "Fonts/dialoguefont/"),
    ("npcfont / DF_FONT / ChatBoxFont / CONVO_FONT", "Исходные шрифты не меняются; UI переключён на RU_-версии", "FontDefs.txt / HiRes/DF_FONT"),
]

ui_fonts = [
    ("RU_DF_FONT", "99 оригинальных глифов DVFFN + 76 сгенерированных (кириллица и типографика); SpaceWidth 9, Kerning -1", "HUD, инвентарь, кодекс, заметки, улучшения"),
    ("RU_ChatBoxFont", "Те же глифы; SpaceWidth 5, Kerning -1", "Чат и сообщения о подборе"),
    ("RU_CONVO_FONT", "Те же глифы; SpaceWidth 10, Kerning 0", "Реплики в диалогах"),
    ("RU_npcfont", "592 оригинальных глифа + 74 сгенерированных пары; золотой стиль, SpaceWidth 5, Kerning -3, Scale 1.2", "Имена NPC"),
]

layout = [
    ("Главное меню: NewSmallFont, золотой выбранный пункт", "BIGFONT (оригинальный шрифт); выбранный пункт белый + подсветка рамкой"),
    ("Позиции пунктов 128/136/127/127/138/147", "124/126/111/110/140/140 — под русские подписи BIGFONT, центр 160"),
    ("Вкладки настроек: BIGFONT через Menu/tabmenu.zs", "Оригинальный BigUpper; отдельный font override убран; подписи вкладок переведены"),
    ("Настройки: protected OptionMenu с английскими подписями", "Новые RU_-меню; вкладки ведут на них"),
    ("Настройки: описания из Language.txt на английском", "Language.RU с [ru]-секциями для всех DESC_*"),
    ("Загрузка/сохранение: английские заголовки и попапы", "Русские заголовки, попапы, кнопки, Время/Дата"),
    ("Карта/сложность/эпизод/выход: английские", "Переведены в MapInfo"),
    ("Титульный экран: [Press any button] по центру", "[Нажмите любую кнопку]; x считается по ширине строки (BIGFONT.StringWidth)"),
]

not_translated = [
    ("HUD, инвентарь, кодекс", "Шрифты RU_ готовы; текст ещё не переведён"),
    ("Имена NPC", "RU_npcfont готов; текст ещё не переведён"),
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
pk3_path = os.path.join(ROOT, "dist", "DF_RU.pk3")
if os.path.isfile(pk3_path):
    with zipfile.ZipFile(pk3_path) as z:
        pk3_entries = len(z.namelist())
    pk3_size = os.path.getsize(pk3_path)
    size_str = f"{pk3_size:,}".replace(",", " ")
    build_line = f"Сборка: `dist/DF_RU.pk3` — {pk3_entries} записей, {size_str} байт (~{pk3_size / 1024 / 1024:.1f} МБ)."
else:
    build_line = "Сборка: `dist/DF_RU.pk3` не найдена."
lines.append(build_line)
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
lines.append("## 6. Дополнительно / Специальные возможности")
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
lines.append("Название карты в слоте извлекается до перевода строки, поэтому локализованное «Время:» не попадает в подпись карты и не перекрывает дату/время.")
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
lines.append("Проверка сборки: PK3 пересобран, в игре не запускался. Визуальная проверка — за тобой.")
lines.append("")
lines.append("## 16. Открытые вопросы (для стилевой вычитки)")
lines.append("")
lines.append("- `Use Psykhus Injector` → «Использовать инъектор Психуса»: написание «Психус/Психхус» согласовать с будущим переводом предметов (`Language.Items`).")
lines.append("- `Nulled Landscape` оставлено без перевода в `RU_DFAdvancedOptions` и `DESC_DISTORTION`; согласовать с названием локации.")
lines.append("- `Can't See Sh!t` → «Ни хрена не видно»: сохранена грубоватая шутка оригинала; при желании смягчить.")
lines.append("- `Consumable Healing Rate` → «Эффективность лечебных предметов»: в коде `healAmount * modf_heal`, то есть количество лечения, а не скорость.")
lines.append("- `Mouse2: Options` → «ПКМ: действия»: в инвентаре открывает меню действий предмета (`ShowExtendedOption`).")
lines.append("- Названия актов оставлены как в оригинале («Чистые обнажённые умы» и т. п.).")
lines.append("- Игровые сокращения (`DMG`, `PT`, `HP`, `PSI` и т. п.) оставлять как в оригинале, не переводить на русские сокращения вроде «УРН».")
lines.append("")
lines.append("## 17. UI-шрифты (внутриигровой интерфейс)")
lines.append("")
lines.append(table(["Шрифт", "Что сделано", "Где используется"], ui_fonts))
lines.append("")
lines.append("В ZScript-оверрайдах ссылки заменены: `DF_FONT` → `RU_DF_FONT`, `ChatBoxFont` → `RU_ChatBoxFont`, `CONVO_FONT` → `RU_CONVO_FONT`, `npcfont` → `RU_npcfont`. Исходные шрифты не изменяются.")
lines.append("")
lines.append("## 18. UI: инвентарь и вкладки (первый блок)")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], ui_pilot))
lines.append("")
lines.append("Названия и описания предметов из `Language.Items` в этот блок ещё не входят — следующий этап.")
lines.append("")
lines.append("## 19. Оружие (`Language.Weapon`)")
lines.append("")
lines.append(table(["Ключ", "Что было (EN)", "Что стало (RU)"], weapon_translations))
lines.append("")
lines.append("`DB_Info`/`DB_Ability`/`DB_Quirk` (молот) оставлены без перевода: оригинальный текст намеренно искажён.")
lines.append("")
lines.append("## 20. UI: улучшения, магазин и создание персонажа")
lines.append("")
lines.append(table(["Что было (EN)", "Что стало (RU)", "Где"], ui_upgrades))
lines.append("")
lines.append("## 21. NPC: персонажи и диалоги")
lines.append("")
lines.append(table(["Файл", "Ключей переведено", "Что охвачено"], npc_rows))
lines.append("")
lines.append("Шрифт имён — `RU_npcfont`, реплики — `dialoguefont` (кириллица уже была в оригинале), ответы — `RU_CONVO_FONT`.")
lines.append("")
lines.append("Имена и короткие реплики, зашитые прямо в карты (`World's Anchor`, `TERMINAL`, `Door` и т. п.), переводятся в `ConversationMenuBase.TranslateInline`; в таблицу `Language.*` они не входят. В `Language.NPCPrism`, `Language.NPCAstronaut` и части `Language.NPCADB` оригинал намеренно искажён/зашифрован — переведены читаемые имена, выборы и реплики, остальное оставлено как в оригинале.")
lines.append("")
lines.append("## 22. Предметы, улучшения, кодекс, заметки")
lines.append("")
lines.append(table(["Файл", "Ключей переведено", "Что охвачено"], content_rows))
lines.append("")
lines.append("`Language.Map`: переведены читаемые тексты и UI; терминальные логи, шифры, ASCII-арт и часть технических ключей оставлены на английском. ACS-скрипты карт — следующий блок.")

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines))
print(f"Wrote {OUT}")
print(f"Text rows: {total}, descriptions: {len(descriptions)}")
