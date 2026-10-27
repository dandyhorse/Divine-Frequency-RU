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
})
write("ZScript/UI/UIZForms/Load Menu/LoadMenu.zsc", loadmenu)

savemenu = read("ZScript/UI/UIZForms/Save Menu/SaveMenu.zsc")
savemenu = replace_all(savemenu, {
    r'"Cannot Save while on the title screen \n Please load or start a new game to save!"':
        r'"На титульном экране сохраняться нельзя.\nЗагрузите игру или начните новую, чтобы сохраниться!"',
    r'"Save Game"': r'"Сохранить игру"',
    r'"Time: "': r'"Время: "',
    r'"Date: "': r'"Дата: "',
})
write("ZScript/UI/UIZForms/Save Menu/SaveMenu.zsc", savemenu)

generic = read("ZScript/UI/GenericScreenStuff.txt")
generic = replace_all(generic, {
    r'"[Press any button]"': r'"[Нажмите любую кнопку]"',
})
write("ZScript/UI/GenericScreenStuff.txt", generic)

print("UI overrides written")
