import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")
WORK = os.path.join(ROOT, "work")


def read(rel):
    with open(os.path.join(SRC, rel), "r", encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    path = os.path.join(WORK, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def replace_all(text, mapping):
    for old, new in mapping.items():
        if old not in text:
            raise SystemExit(f"Not found: {old!r}")
        text = text.replace(old, new)
    return text


loadsave = read("ZScript/UI/UIZForms/LoadSaveBase.zsc")
loadsave = replace_all(loadsave, {
    r'"Delete Save?\n"': r'"Удалить сохранение?\n"',
    r'"DELETE \cU(Y)"': r'"УДАЛИТЬ \cU(Y)"',
    r'"CANCEL \cU(N)"': r'"ОТМЕНА \cU(N)"',
    r'"Overwrite Save?"': r'"Перезаписать сохранение?"',
    r'"SAVE \cU(Y)"': r'"СОХРАНИТЬ \cU(Y)"',
    r'"Create New Save?"': r'"Создать новое сохранение?"',
    r'"Confirm"': r'"Подтвердить"',
    r'"Cancel"': r'"Отмена"',
})
write("ZScript/UI/UIZForms/LoadSaveBase.zsc", loadsave)

loadmenu = read("ZScript/UI/UIZForms/Load Menu/LoadMenu.zsc")
loadmenu = replace_all(loadmenu, {
    r'"Load Game"': r'"Загрузить игру"',
    r'"Time: "': r'"Время: "',
    r'"Date: "': r'"Дата: "',
    r'SaveCommentString.indexof("Time")-(SaveCommentString.indexof("MAP")+8)':
        r'SaveCommentString.indexof("\n", SaveCommentString.indexof("MAP"))-(SaveCommentString.indexof("MAP")+8)',
})
write("ZScript/UI/UIZForms/Load Menu/LoadMenu.zsc", loadmenu)

savemenu = read("ZScript/UI/UIZForms/Save Menu/SaveMenu.zsc")
savemenu = replace_all(savemenu, {
    r'"Cannot Save while on the title screen \n Please load or start a new game to save!"':
        r'"На титульном экране сохраняться нельзя.\nЗагрузите игру или начните новую, чтобы сохраниться!"',
    r'"Save Game"': r'"Сохранить игру"',
    r'"Time: "': r'"Время: "',
    r'"Date: "': r'"Дата: "',
    r'SaveCommentString.indexof("Time")-(SaveCommentString.indexof("MAP")+8)':
        r'SaveCommentString.indexof("\n", SaveCommentString.indexof("MAP"))-(SaveCommentString.indexof("MAP")+8)',
})
write("ZScript/UI/UIZForms/Save Menu/SaveMenu.zsc", savemenu)

generic = read("ZScript/UI/GenericScreenStuff.txt")
generic = replace_all(generic, {
    "\tif(input_confirm)\n"
    "\t{\n"
    "\t  Screen.DrawText(BIGFONT, Font.CR_WHITE, 126, 180, String.Format(\"[Press any button]\"),\n"
    "\t  DTA_ScaleX, 0.7,\n"
    "\t  DTA_ScaleY, 0.6,\n"
    "\t  DTA_Spacing, -1,\n"
    "\t  DTA_Alpha, 0.2,\n"
    "\t  DTA_320x200, true\n"
    "\t  );\n"
    "\t}":
    "\tif(input_confirm)\n"
    "\t{\n"
    "\t  String prompt = \"[Нажмите любую кнопку]\";\n"
    "\t  Screen.DrawText(BIGFONT, Font.CR_WHITE, int(160 - (BIGFONT.StringWidth(prompt) - prompt.Length()) * 0.7 / 2), 180, prompt,\n"
    "\t  DTA_ScaleX, 0.7,\n"
    "\t  DTA_ScaleY, 0.6,\n"
    "\t  DTA_Spacing, -1,\n"
    "\t  DTA_Alpha, 0.2,\n"
    "\t  DTA_320x200, true\n"
    "\t  );\n"
    "\t}",
    r'"\cD[%s] [%s] [%s] [%s]\cJ - Movement\n\cD[%s]\cJ - Interact"':
        r'"\cD[%s] [%s] [%s] [%s]\cJ - Движение\n\cD[%s]\cJ - Взаимодействие"',
})
write("ZScript/UI/GenericScreenStuff.txt", generic)

INLINE_MAP = {
    "TERMINAL": "ТЕРМИНАЛ",
    "AN EGG": "ЯЙЦО",
    "BENCH": "ВЕРСТАК",
    "BURIED LEVELS ENTRANCE": "ВХОД В ПОГРЕБЁННЫЕ УРОВНИ",
    "Bed": "Кровать",
    "CABINET": "ШКАФ",
    "CONSOLE": "КОНСОЛЬ",
    "CONTROL PANEL": "ПАНЕЛЬ УПРАВЛЕНИЯ",
    "DAMAGED ELECTRONIC DEVICE": "ПОВРЕЖДЁННОЕ ЭЛЕКТРОННОЕ УСТРОЙСТВО",
    "DOOR": "ДВЕРЬ",
    "Door": "Дверь",
    "ELECTRONIC DEVICE": "ЭЛЕКТРОННОЕ УСТРОЙСТВО",
    "ELEVATOR CONTROL": "УПРАВЛЕНИЕ ЛИФТОМ",
    "ENIGMATIC FIGURE": "ЗАГАДОЧНАЯ ФИГУРА",
    "EXALTED DREAMER": "ВОЗВЫШЕННЫЙ СНОВИДЕЦ",
    "File Cabinet": "Картотека",
    "NOWHERE": "НИГДЕ",
    "THRESHOLD": "ПОРОГ",
    "TRAIN TICKET": "ЖЕЛЕЗНОДОРОЖНЫЙ БИЛЕТ",
    "Table": "Стол",
    "VENDING MACHINE": "ТОРГОВЫЙ АВТОМАТ",
    "World's Anchor": "Якорь Мира",
    r"\cD[Open Containment Unit]": r"\cD[Открыть блок содержания]",
    r"\cQ(Leave)": r"\cQ(Уйти)",
    r"\cQ[Instinct] \cDCall forth emissaries.": r"\cQ[Инстинкт] \cDПризвать эмиссаров.",
    r"\cQ[Strength] \cDTry brute forcing the doors open.": r"\cQ[Сила] \cDПопробовать выломать двери.",
}

def zs_quote(text):
    return text.replace('"', r'\"')

translate_lines = ["\tString TranslateInline(String text)", "\t{"]
for eng, rus in INLINE_MAP.items():
    translate_lines.append(f'\t\tif (text == "{zs_quote(eng)}") return "{zs_quote(rus)}";')
translate_lines.extend(["\t\treturn text;", "\t}"])
translate_func = "\n".join(translate_lines)

conversation_base = read("ZScript/ConversationMenu/ConversationMenuBase.txt")
conversation_base = replace_all(conversation_base, {
    "\tString ParseSpeakerMessage()": translate_func + "\n\n\tString ParseSpeakerMessage()",
    "toSay = ReplaceToken(toSay);": "toSay = TranslateInline(ReplaceToken(toSay));",
    "return Stringtable.Localize(mCurNode.SpeakerName);": "return TranslateInline(Stringtable.Localize(mCurNode.SpeakerName));",
    'return players[consoleplayer].ConversationNPC.GetTag("Person");': 'return TranslateInline(players[consoleplayer].ConversationNPC.GetTag("Person"));',
    "let ReplyText = Stringtable.Localize(reply.Reply);": "let ReplyText = TranslateInline(Stringtable.Localize(reply.Reply));",
    "goodbyestr = Stringtable.Localize(goodbyestr);": "goodbyestr = TranslateInline(Stringtable.Localize(goodbyestr));",
})
write("ZScript/ConversationMenu/ConversationMenuBase.txt", conversation_base)

FONT_FILES = [
    "ZScript/UI/Calibration.txt",
    "ZScript/UI/DamageNumber.txt",
    "ZScript/UI/Hud.txt",
    "ZScript/UI/Note.txt",
    "ZScript/UI/UIZForms/UICodex/Bestiary.txt",
    "ZScript/UI/UIZForms/UICodex/Codex.txt",
    "ZScript/UI/UIZForms/UICodex/HUDinfo.txt",
    "ZScript/UI/UIZForms/UICodex/Map.txt",
    "ZScript/UI/UIZForms/UIInventory/InventoryMenu.zc",
    "ZScript/UI/UIZForms/UIInventory/NewItemMenu.zc",
    "ZScript/UI/UIZForms/UIUpgrades/CreationMenu.zc",
    "ZScript/UI/UIZForms/UIUpgrades/GunUpgrade.zc",
    "ZScript/UI/UIZForms/UIUpgrades/LevelUpMenu.zc",
    "ZScript/UI/UIZForms/UIUpgrades/ShopMenu.zc",
    "ZScript/ConversationMenu/ConversationMenuComponents.txt",
    "ZScript/ConversationMenu/Sample.txt",
]

FONT_REPLACEMENTS = {
    r'"DF_FONT"': r'"RU_DF_FONT"',
    r'"ChatBoxFont"': r'"RU_ChatBoxFont"',
    r'"CONVO_FONT"': r'"RU_CONVO_FONT"',
    r'"npcfont"': r'"RU_npcfont"',
}

UI_TRANSLATIONS = {
    "ZScript/UI/UIZForms/UIInventory/InventoryMenu.zc": {
        r'"Consumables & Medications (%d/%d)"': r'"Расходники и медикаменты (%d/%d)"',
        r'"Location: %s"': r'"Локация: %s"',
        r'"Description:"': r'"Описание:"',
        r'"\cDEffect:"': r'"\cDЭффект:"',
        r'"Key Items"': r'"Ключевые предметы"',
        r'"Abilities"': r'"Способности"',
        r'"Attribute"': r'"Характеристики"',
        r'"Condition"': r'"Состояние"',
        r'"Current Objective"': r'"Текущая цель"',
        r'"Assign to Quick Use"': r'"Назначить на быстрое использование"',
        r'"LEVEL %d Avatar:\n%s\n\nStrength: %d\nWits: %d\nPhysique: %d\n\n    Exaltation: %d\n    Mutation: %d\n    Psi. Attunement: %d/%d"':
            r'"УРОВЕНЬ %d Аватар:\n%s\n\nСила: %d\nРазум: %d\nТелосложение: %d\n\n    Экзальтация: %d\n    Мутация: %d\n    Пси-настройка: %d/%d"',
        r'"Toxin (Lethal)\n\cR-Suffer Periodic Damage\n-Impaired Movement\n-Impaired Aim\n\n"':
            r'"Токсин (смертельный)\n\cR-Периодический урон\n-Нарушение движения\n-Нарушение прицеливания\n\n"',
        r'"Toxin (Moderate)\n\cR-Impaired Aim\n\n"':
            r'"Токсин (умеренный)\n\cR-Нарушение прицеливания\n\n"',
        r'"\cJRadiation (Lethal)\n\cR-Imminent Overload\n-Impaired Vision\n\n"':
            r'"\cJРадиация (смертельная)\n\cR-Неминуемая перегрузка\n-Нарушение зрения\n\n"',
        r'"\cJRadiation (Moderate)\n\cR-Impaired Vision\n\n"':
            r'"\cJРадиация (умеренная)\n\cR-Нарушение зрения\n\n"',
        r'"\cD[Mouse1] \cJUse Item"': r'"\cD[ЛКМ] \cJИспользовать"',
        r'"\cD[Mouse2] \cJOptions"': r'"\cD[ПКМ] \cJДействия"',
        r'"\cD[Mouse1] \cJOptions"': r'"\cD[ЛКМ] \cJДействия"',
        r'"\cD[Mouse2] \cJUse Item"': r'"\cD[ПКМ] \cJИспользовать"',
        r'"Use Item"': r'"Использовать"',
        r'"Drop Item"': r'"Выбросить"',
        r'"Keybind"': r'"Привязать"',
        r'"Handgun: %d"': r'"Пистолет: %d"',
        r'"Trenchgun: %d"': r'"Траншейка: %d"',
        r'"Spray Can: %d"': r'"Баллончик: %d"',
        r'"Assault Rifle: %d"': r'"Автомат: %d"',
    },
    "ZScript/UI/UIZForms/UICodex/Codex.txt": {
        r'"\cFEnhancements"': r'"\cFУлучшения"',
        r'"Information:"': r'"Информация:"',
        r'"Secondary Fire:"': r'"Альтернативный огонь:"',
        r'"Additional Mechanics:"': r'"Дополнительные механики:"',
        r'"\cFWeapon Modifications:"': r'"\cFМодификации оружия:"',
        r'"\cFCharacter Ascension:"': r'"\cFВозвышение персонажа:"',
        r'"\cFUnique:"': r'"\cFУникальное:"',
    },
    "ZScript/UI/UIZForms/UICodex/Bestiary.txt": {
        r'"Information:"': r'"Информация:"',
        r'"Additional Data:"': r'"Дополнительные данные:"',
        r'"Snapshot:"': r'"Снимок:"',
        r'"Archive:"': r'"Архив:"',
    },
    "ZScript/UI/UIZForms/UIUpgrades/CreationMenu.zc": {
        r'"Enter Character Name:"': r'"Введите имя персонажа:"',
        r'"Accept"': r'"Принять"',
    },
    "ZScript/UI/UIZForms/UIUpgrades/GunUpgrade.zc": {
        r'"Barrel Mod"': r'"Модификация ствола"',
        r'"Extended Magazine"': r'"Увеличенный магазин"',
        r'"Exotic Powder Mixture"': r'"Экзотическая пороховая смесь"',
        r'"Confirm"': r'"Подтвердить"',
        r'"Cancel"': r'"Отмена"',
        r'"\cD[Esc] \cJLeave "': r'"\cD[Esc] \cJВыйти "',
    },
    "ZScript/UI/UIZForms/UIUpgrades/LevelUpMenu.zc": {
        r'"Current Exaltation: \cF%d"': r'"Текущая экзальтация: \cF%d"',
        r'"Upgrade %s: %d -> %d"': r'"Улучшение %s: %d -> %d"',
        r'"Cost: %d"': r'"Стоимость: %d"',
        r'"Strength"': r'"Сила"',
        r'"Wits"': r'"Разум"',
        r'"Physique"': r'"Телосложение"',
        r'"Confirm"': r'"Подтвердить"',
        r'"Cancel"': r'"Отмена"',
        r'"SECONDARY ATTRIBUTES"': r'"ВТОРИЧНЫЕ АТРИБУТЫ"',
        r'"Exaltation"': r'"Экзальтация"',
        r'"Mutation"': r'"Мутация"',
        r'"Confirm Selection: \cF"': r'"Подтвердить выбор: \cF"',
        r'"Strength Upgrade\cJ?"': r'"Улучшение Силы\cJ?"',
        r'"Wits Upgrade\cJ?"': r'"Улучшение Разума\cJ?"',
        r'"Physique Upgrade\cJ?"': r'"Улучшение Телосложения\cJ?"',
        r'"\cD[Esc] \cJLeave "': r'"\cD[Esc] \cJВыйти "',
    },
    "ZScript/UI/UIZForms/UIUpgrades/ShopMenu.zc": {
        r'"Survival Response"': r'"Реакция выживания"',
        r'"Third Mind"': r'"Третий разум"',
        r'"Predatory Focus"': r'"Хищный фокус"',
        r'"Even More Pockets!"': r'"Ещё больше карманов!"',
        r'"Reflect Damage"': r'"Отражение урона"',
        r'"Endless Hunger"': r'"Бесконечный голод"',
        r'"Organic Caltrops"': r'"Органические шипы"',
        r'"Psychic Blast"': r'"Психический взрыв"',
        r'"Confirm"': r'"Подтвердить"',
        r'"Cancel"': r'"Отмена"',
        r'"Current Mutation Point: \cF%d"': r'"Текущие очки мутации: \cF%d"',
        r'"Confirm Selection: \cF"': r'"Подтвердить выбор: \cF"',
        r'"\cD[Esc] \cJLeave"': r'"\cD[Esc] \cJВыйти"',
    },
    "ZScript/UI/UIZForms/UIInventory/NewItemMenu.zc": {
        r'"\cD[Esc] \cJLeave"': r'"\cD[Esc] \cJВыйти"',
    },
    "ZScript/UI/Hud.txt": {
        r'"Max"': r'"Макс."',
    },
}

TAB_FILES = [
    "ZScript/UI/UIZForms/UIInventory/InventoryMenu.zc",
    "ZScript/UI/UIZForms/UICodex/Codex.txt",
    "ZScript/UI/UIZForms/UICodex/Bestiary.txt",
    "ZScript/UI/UIZForms/UICodex/Map.txt",
    "ZScript/UI/UIZForms/UICodex/HUDinfo.txt",
]

TAB_LABELS = {
    r'"Inventory"': r'"Инвентарь"',
    r'"Weapons"': r'"Оружие"',
    r'"Bestiary"': r'"Бестиарий"',
    r'"Map"': r'"Карта"',
    r'"Help"': r'"Помощь"',
}

for rel in TAB_FILES:
    UI_TRANSLATIONS.setdefault(rel, {}).update(TAB_LABELS)

for rel in FONT_FILES:
    text = read(rel)
    changed = 0
    for old, new in FONT_REPLACEMENTS.items():
        if old in text:
            text = text.replace(old, new)
            changed += 1
    for old, new in UI_TRANSLATIONS.get(rel, {}).items():
        if old not in text:
            raise SystemExit(f"UI translation string not found in {rel}: {old!r}")
        text = text.replace(old, new)
    if not changed:
        print(f"WARNING: no UI font names in {rel}")
    write(rel, text)

player = read("ZScript/Game/Player/Player.txt")
player = replace_all(player, {
    r'title = "Hobo";': r'title = "Бродяга";',
    r'phyLevel_nfo = "Mutation Lv.1";': r'phyLevel_nfo = "Мутация ур.1";',
    r'phyLevel_nfo = String.Format("Mutation Lv.%d", phyLevel);': r'phyLevel_nfo = String.Format("Мутация ур.%d", phyLevel);',
})
write("ZScript/Game/Player/Player.txt", player)

WEAPON_NAME_FILES = {
    "ZScript/Game/Weapons/Hands.txt": {
        r'wep_name = "Fists";': r'wep_name = "Кулаки";',
    },
    "ZScript/Game/Weapons/Pistol2.txt": {
        r'wep_name = "Handgun";': r'wep_name = "Пистолет";',
    },
    "ZScript/Game/Weapons/Shotgun2.txt": {
        r'wep_name = "Trench Gun";': r'wep_name = "Траншейное ружьё";',
    },
    "ZScript/Game/Weapons/SprayCan.txt": {
        r'wep_name = "Spray Can";': r'wep_name = "Баллончик";',
    },
    "ZScript/Game/Weapons/AR.txt": {
        r'wep_name = "Assault Rifle";': r'wep_name = "Автомат";',
    },
}

for rel, mapping in WEAPON_NAME_FILES.items():
    text = read(rel)
    text = replace_all(text, mapping)
    write(rel, text)

print("UI overrides written")
