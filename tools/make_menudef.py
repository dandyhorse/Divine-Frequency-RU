import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "source", "MenuDef")
out = os.path.join(ROOT, "work", "MenuDef")

MAINMENU = '''ListMenu "MainMenu"
{
\tClass "FadeMenu"
\tAnimated
\tAnimatedTransition
\tDontDim
\tFont "BIGFONT", "White", "White"
\tPosition 124, 72
\tHighlightTextItem "Новая игра", "n", "PlayerclassMenu"
\tPosition 126, 92
\tHighlightTextItem "Настройки", "o", "TabTest", 0
\tPosition 111, 112
\tHighlightTextItem "Загрузить игру", "l", "DFLoadMenu", 0
\tPosition 110, 132
\tHighlightTextItem "Сохранить игру", "s", "DFSaveMenu", 0
\tPosition 140, 152
\tHighlightTextItem "Титры", "s", "CreditMenu", 0
\tPosition 140, 172
\tHighlightTextItem "Выход", "q", "QuitMenu", 0
}
'''

SKILLMENU = '''ListMenu "SkillMenu"
{
\tAnimated
\tAnimatedTransition
\tDontDim
\tFont "BIGFONT", "Gray", "White"
\tPosition 128, 72
\tForceList
\tStaticTextCentered 160, 30, "Выберите сложность:"
}
'''

TABTEST = '''OptionMenu "TabTest"
{
\tClass "TabMenu"
\tAnimated
\tAnimatedTransition
\tTab "RU_DFDisplayOptions", "Графика"
\tTab "RU_DFKeyBinds", "Управление"
\tTab "RU_DFSoundOptions", "Звук"
\tTab "RU_DFAdvancedOptions", "Доступность"
}
'''

REPLACEMENTS = {
    "Keybinds": "Управление",
    "Camera Horizontal Sensitivity": "Горизонтальная чувствительность камеры",
    "Camera Vertical Sensitivity": "Вертикальная чувствительность камеры",
    "--MOVEMENT--": "--ДВИЖЕНИЕ--",
    "Move Forward": "Вперёд",
    "Move Backward": "Назад",
    "Strafe Left": "Влево",
    "Strafe Right": "Вправо",
    "Jump": "Прыжок",
    "Crouch (Toggle)": "Присесть (переключение)",
    "Crouch (Hold)": "Присесть (удержание)",
    "Sprint (Hold)": "Бег (удержание)",
    "Dash": "Рывок",
    "--INTERACTION--": "--ВЗАИМОДЕЙСТВИЕ--",
    "Primary Fire": "Основной огонь",
    "Secondary Fire": "Альтернативный огонь",
    "Reload": "Перезарядка",
    "Primary Interact": "Основное взаимодействие",
    "Secondary Interact": "Дополнительное взаимодействие",
    "Change Firing Mode": "Сменить режим стрельбы",
    "Next Weapon": "Следующее оружие",
    "Previous Weapon": "Предыдущее оружие",
    "--ADDITIONAL INTERACTION--": "--ДОПОЛНИТЕЛЬНОЕ ВЗАИМОДЕЙСТВИЕ--",
    "Open Inventory": "Открыть инвентарь",
    "Open Map": "Открыть карту",
    "Use Psykhus Injector": "Использовать инъектор Психуса",
    "Use Quick Item 1": "Быстрый предмет 1",
    "Use Quick Item 2": "Быстрый предмет 2",
    "Use Quick Item 3": "Быстрый предмет 3",
    "Use Quick Item 4": "Быстрый предмет 4",
    "Select Weapon Slot 1": "Слот оружия 1",
    "Select Weapon Slot 2": "Слот оружия 2",
    "Select Weapon Slot 3": "Слот оружия 3",
    "Select Weapon Slot 4": "Слот оружия 4",
    "--GAME STATE--": "--СОСТОЯНИЕ ИГРЫ--",
    "Quicksave": "Быстрое сохранение",
    "Quickload": "Быстрая загрузка",
    "--INVENTORY UI--": "--ИНТЕРФЕЙС ИНВЕНТАРЯ--",
    "Interaction Layout": "Раскладка взаимодействия",
    "Advanced": "Дополнительно",
    "--DIFFICULTY--": "--СЛОЖНОСТЬ--",
    "Player Damage Taken": "Получаемый урон",
    "Ammo Received": "Получаемые патроны",
    "Consumable Healing Rate": "Эффективность лечения расходниками",
    "Stamina Consumption": "Расход выносливости",
    "Weapon Degredation Rate": "Скорость износа оружия",
    "Resonance Break: Extended Timing": "Разрыв резонанса: расширенное окно",
    "--GAMEPLAY--": "--ИГРОВОЙ ПРОЦЕСС--",
    "Damage Number": "Числа урона",
    "HUD (Heads-Up Display)": "HUD (интерфейс)",
    "Interaction Icon": "Значок взаимодействия",
    "Item Tooltip": "Подсказка предмета",
    "Melee Camera Movement": "Движение камеры в ближнем бою",
    "Nulled Landscape Distortion": "Искажение Nulled Landscape",
    "Trenchgun Crosshair": "Прицел траншейного ружья",
    "Tutorials": "Обучение",
    "--MISCELLANEOUS--": "--РАЗНОЕ--",
    "Item Pickup Flash Intensity": "Яркость вспышки при подборе",
    "Damage Taken Flash Intensity": "Яркость вспышки при получении урона",
    "Crosshair Color Match Health": "Цвет прицела по здоровью",
    "WARNING: Controller Support is not fully implemented!": "ВНИМАНИЕ: Поддержка контроллера реализована не полностью!",
    "Adjust the slider until you can slightly spot the figure in the background.": "Настройте ползунок, пока едва не начнёте различать фигуру на фоне.",
    "Resolution Width": "Ширина разрешения",
    "Resolution Height": "Высота разрешения",
    "VHS Intensity": "Интенсивность VHS",
    "VHS Tearing": "Разрыв VHS",
    "HUD Size": "Размер HUD",
    "Off": "Выкл.",
    "On": "Вкл.",
    "Minimal": "Минимум",
    "Default": "По умолчанию",
    "Can't See Sh!t": "Ничего не видно",
    "Unplayable": "Неиграбельно",
    "Eye Damage": "Вред глазам",
    "Standard": "Стандарт",
    "Doubled": "Удвоено",
    "Halved": "Половинный",
    "None": "Нет",
    "Disabled": "Отключено",
    "Enabled": "Включено",
    "Mouse1: Use Item | Mouse2: Options": "ЛКМ: использовать | ПКМ: настройки",
    "Mouse1: Options | Mouse2: Use Item": "ЛКМ: настройки | ПКМ: использовать",
}


def replace_block(text, pattern, replacement):
    new, n = re.subn(pattern, replacement, text, count=1, flags=re.M | re.S)
    if n != 1:
        raise SystemExit(f"Block not found: {pattern}")
    return new


with open(src, "r", encoding="utf-8") as f:
    text = f.read()

text = replace_block(text, r'^ListMenu "MainMenu"\s*\{.*?^\}\s*', MAINMENU)
text = replace_block(text, r'^ListMenu "SkillMenu"\s*\{.*?^\}\s*', SKILLMENU)
text = replace_block(text, r'^OptionMenu "TabTest"\s*\{.*?^\}\s*', TABTEST)

def extract_block(text, pattern):
    m = re.search(pattern, text, flags=re.M | re.S)
    if not m:
        raise SystemExit(f"Block not found: {pattern}")
    return m.group(0)

orig_display = extract_block(text, r'^OptionMenu "DFDisplayOptions" protected\s*\{.*?^\}\s*')
orig_keybinds = extract_block(text, r'^OptionMenu "DFKeyBinds" protected\s*\{.*?^\}\s*')
orig_sound = extract_block(text, r'^OptionMenu "DFSoundOptions" protected\s*\{.*?^\}\s*')
orig_advanced = extract_block(text, r'^OptionMenu "DFAdvancedOptions" protected\s*\{.*?^\}\s*')
orig_joystick = extract_block(text, r'^OptionMenu "NewJoystickOptions"(?: protected)?\s*\{.*?^\}\s*')

new_display = orig_display.replace('OptionMenu "DFDisplayOptions" protected', 'OptionMenu "RU_DFDisplayOptions"', 1)
new_keybinds = orig_keybinds.replace('OptionMenu "DFKeyBinds" protected', 'OptionMenu "RU_DFKeyBinds"', 1)
new_sound = orig_sound.replace('OptionMenu "DFSoundOptions" protected', 'OptionMenu "RU_DFSoundOptions"', 1)
new_advanced = orig_advanced.replace('OptionMenu "DFAdvancedOptions" protected', 'OptionMenu "RU_DFAdvancedOptions"', 1)
new_advanced = new_advanced.replace('"NewJoystickOptions"', '"RU_NewJoystickOptions"')
new_joystick = re.sub(r'^OptionMenu "NewJoystickOptions"(?: protected)?', 'OptionMenu "RU_NewJoystickOptions"', orig_joystick, count=1, flags=re.M)

text = text + "\n\n" + new_display + "\n" + new_keybinds + "\n" + new_sound + "\n" + new_advanced + "\n" + new_joystick + "\n"

for eng, rus in REPLACEMENTS.items():
    text = text.replace(f'"{eng}"', f'"{rus}"')

os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print(f"Wrote {out}")
