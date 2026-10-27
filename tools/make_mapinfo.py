import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "source", "MapInfo")
out = os.path.join(ROOT, "work", "MapInfo")

with open(src, "r", encoding="utf-8") as f:
    text = f.read()

replacements = {
    'Name = "Standard"': 'Name = "Обычная"',
    'mustconfirm = "Confirm starting a New Game?"': 'mustconfirm = "Начать новую игру?"',
    'name = "Main Story"': 'name = "Основная история"',
    'map TITLEMAP "Title"': 'map TITLEMAP "Титульный экран"',
    '"ACT I - Metempsychosis"': '"АКТ I — Метемпсихоз"',
    '"ACT II - Pure Naked Minds"': '"АКТ II — Чистые обнажённые умы"',
    '"ACT III - Without Center or Circumference"': '"АКТ III — Без центра и окружности"',
    '"To The Edge of Existence"': '"К краю бытия"',
}
for eng, rus in replacements.items():
    if eng not in text:
        raise SystemExit(f"Not found in MapInfo: {eng}")
    text = text.replace(eng, rus)

anchor = 'TitlePage = "graphics/titlepic.png"'
if anchor not in text:
    raise SystemExit("TitlePage anchor not found")
text = text.replace(anchor, anchor + '\n\tquitmessages = "Вы действительно хотите выйти?"', 1)

os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print(f"Wrote {out}")
