import ast
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "review", "DF_RU_text_review.md")

CATEGORIES = [
    ("Диалоги и NPC", [
        "Language.NPC",
        "Language.NPCBox",
        "Language.NPCDisciples",
        "Language.NPCLantern",
        "Language.NPCMISC",
        "Language.NPCMonastery",
        "Language.NPCDreamer",
        "Language.NPCEgg",
        "Language.NPCADB",
        "Language.NPCAstronaut",
        "Language.NPCPrism",
        "Language.Duel",
    ]),
    ("Заметки, бестиарий и лор", [
        "Language.Note.txt",
        "Language.Bestiary.txt",
        "Language.Artistical",
    ]),
    ("Предметы, оружие и улучшения", [
        "Language.Items.txt",
        "Language.Weapon.txt",
        "Language.Upgrade.txt",
    ]),
    ("UI, цели и карта", [
        "Language.Tutorial",
        "Language.Objective",
        "Language.Map",
    ]),
]


def lang_values(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"//[^\n]*", "", text)
    values = {}
    for m in re.finditer(r'(?ms)^\s*([A-Za-z0-9_]+)\s*=\s*((?:"(?:[^"\\]|\\.)*"\s*)+);', text):
        values[m.group(1)] = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
    return values


def render_value(value):
    return value.replace("\\n", "\n")


def inline_map():
    path = os.path.join(ROOT, "tools", "make_ui_overrides.py")
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "INLINE_MAP":
                return ast.literal_eval(node.value)
    return {}


def main():
    lines = []
    lines.append("# Divine Frequency — тексты перевода на ревью")
    lines.append("")
    lines.append("Этот файл содержит сами строки: **EN** и **RU**. Сводка по покрытию — в `TRANSLATIONS.md`.")
    lines.append("")
    lines.append("Обозначения: `\\c…` и `\\c[Цвет]` — цветовые коды игры; `|` — разделитель строк эффекта; `%d`, `%s` — подстановки; `$Ключ` — ссылка на языковой ключ; `\\n` — перенос строки.")
    lines.append("")
    lines.append("")

    total = 0
    for title, files in CATEGORIES:
        lines.append(f"## {title}")
        lines.append("")
        for name in files:
            en_path = os.path.join(ROOT, "source", name)
            ru_path = os.path.join(ROOT, "work", name)
            if not os.path.isfile(en_path) or not os.path.isfile(ru_path):
                continue
            en = lang_values(en_path)
            ru = lang_values(ru_path)
            translated = [(k, en[k], ru[k]) for k in en if k in ru]
            if not translated:
                continue
            lines.append(f"### {name}")
            lines.append("")
            lines.append(f"Переведено: **{len(translated)}** из **{len(en)}** ключей.")
            lines.append("")
            for key, eng, rus in translated:
                lines.append(f"#### `{key}`")
                lines.append("")
                lines.append("**EN**")
                lines.append("~~~text")
                lines.append(render_value(eng))
                lines.append("~~~")
                lines.append("")
                lines.append("**RU**")
                lines.append("~~~text")
                lines.append(render_value(rus))
                lines.append("~~~")
                lines.append("")
                total += 1

    inline = inline_map()
    if inline:
        lines.append("## Инлайн-имена и реплики из `DIALOGUE`")
        lines.append("")
        lines.append("Переводятся в `ConversationMenuBase.TranslateInline`.")
        lines.append("")
        for eng, rus in inline.items():
            lines.append(f"### `{eng}`")
            lines.append("")
            lines.append("**EN**")
            lines.append("~~~text")
            lines.append(eng)
            lines.append("~~~")
            lines.append("")
            lines.append("**RU**")
            lines.append("~~~text")
            lines.append(rus)
            lines.append("~~~")
            lines.append("")
            total += 1

    lines.append("## Примечания")
    lines.append("")
    lines.append("- `Language.Map`: переведены читаемые тексты и UI; технические терминальные логи, шифры и ASCII-арт оставлены в оригинале.")
    lines.append("- В `Language.NPCAstronaut`, `Language.NPCADB` и `Language.NPCPrism` часть оригинала намеренно искажена/зашифрована; переведены читаемые фрагменты.")
    lines.append(f"- Всего строк в этом файле: **{total}**.")
    lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"Strings: {total}")


if __name__ == "__main__":
    main()
