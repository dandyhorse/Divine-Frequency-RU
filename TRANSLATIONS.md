# Divine Frequency — таблица перевода меню

Дата: 27.10.2026

Сборка: `dist/DF_RU.pk3` — 3241 записей, 1 554 078 байт (~1.5 МБ).

Формат: каждая секция содержит таблицу **«что было → что стало»**. В колонке «Где» указан файл/блок, где применён перевод.

Всего текстовых строк в таблицах: **153** (включая 36 описаний `DESC_*`).

## 1. Главное меню

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| New Game | Новая игра | MenuDef → MainMenu |
| Options | Настройки | MenuDef → MainMenu |
| Load Game | Загрузить игру | MenuDef → MainMenu |
| Save Game | Сохранить игру | MenuDef → MainMenu |
| Credits | Титры | MenuDef → MainMenu |
| Quit | Выход | MenuDef → MainMenu |

## 2. Сложность, карты и выход

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Select Difficulty: | Выберите сложность: | MenuDef → SkillMenu |
| Standard | Обычная | MapInfo → Skill normal → Name |
| Confirm starting a New Game? | Начать новую игру? | MapInfo → Skill normal → mustconfirm |
| Main Story | Основная история | MapInfo → episode map01 |
| Title | Титульный экран | MapInfo → map TITLEMAP |
| ACT I - Metempsychosis | АКТ I — Метемпсихоз | MapInfo → карты MAP01–05, MAP30–31 |
| ACT II - Pure Naked Minds | АКТ II — Чистые обнажённые умы | MapInfo → карты MAP06–16 |
| ACT III - Without Center or Circumference | АКТ III — Без центра и окружности | MapInfo → карты MAP17–18 |
| To The Edge of Existence | К краю бытия | MapInfo → карта MAP19 |
| Do you want to quit? | Вы действительно хотите выйти? | MapInfo → GameInfo → quitmessages (движковый default) |

## 3. Вкладки настроек

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Graphics | Графика | MenuDef → TabTest |
| Control | Управление | MenuDef → TabTest |
| Audio | Звук | MenuDef → TabTest |
| Accessibility | Специальные возможности | MenuDef → TabTest |

## 4. Графика

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Resolution Width | Ширина (пикс.) | MenuDef → RU_DFDisplayOptions |
| Resolution Height | Высота (пикс.) | MenuDef → RU_DFDisplayOptions |
| VHS Intensity | Интенсивность VHS-эффекта | MenuDef → RU_DFDisplayOptions |
| VHS Tearing | Разрывы изображения (VHS) | MenuDef → RU_DFDisplayOptions |
| HUD Size | Размер HUD | MenuDef → RU_DFDisplayOptions |

Остальные подписи вкладки «Графика» (`$VIDMNU_*`, `$DSPLYMNU_*`, `$GLPREFMNU_*`) берутся из `language.csv` и уже локализованы движком.

## 5. Управление

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Keybinds | Назначение клавиш | MenuDef → RU_DFKeyBinds → Title |
| Camera Horizontal Sensitivity | Чувствительность камеры по горизонтали | RU_DFKeyBinds |
| Camera Vertical Sensitivity | Чувствительность камеры по вертикали | RU_DFKeyBinds |
| --MOVEMENT-- | --ДВИЖЕНИЕ-- | RU_DFKeyBinds |
| Move Forward | Вперёд | RU_DFKeyBinds |
| Move Backward | Назад | RU_DFKeyBinds |
| Strafe Left | Влево | RU_DFKeyBinds |
| Strafe Right | Вправо | RU_DFKeyBinds |
| Jump | Прыжок | RU_DFKeyBinds |
| Crouch (Toggle) | Присесть (переключение) | RU_DFKeyBinds |
| Crouch (Hold) | Присесть (удержание) | RU_DFKeyBinds |
| Sprint (Hold) | Бег (удержание) | RU_DFKeyBinds |
| Dash | Рывок | RU_DFKeyBinds |
| --INTERACTION-- | --ВЗАИМОДЕЙСТВИЕ-- | RU_DFKeyBinds |
| Primary Fire | Основной огонь | RU_DFKeyBinds |
| Secondary Fire | Альтернативный огонь | RU_DFKeyBinds |
| Reload | Перезарядка | RU_DFKeyBinds |
| Primary Interact | Основное взаимодействие | RU_DFKeyBinds |
| Secondary Interact | Дополнительное взаимодействие | RU_DFKeyBinds |
| Change Firing Mode | Сменить режим стрельбы | RU_DFKeyBinds |
| Next Weapon | Следующее оружие | RU_DFKeyBinds |
| Previous Weapon | Предыдущее оружие | RU_DFKeyBinds |
| --ADDITIONAL INTERACTION-- | --ДОПОЛНИТЕЛЬНОЕ ВЗАИМОДЕЙСТВИЕ-- | RU_DFKeyBinds |
| Open Inventory | Открыть инвентарь | RU_DFKeyBinds |
| Open Map | Открыть карту | RU_DFKeyBinds |
| Use Psykhus Injector | Использовать инъектор Психуса | RU_DFKeyBinds |
| Use Quick Item 1 | Использовать быстрый предмет 1 | RU_DFKeyBinds |
| Use Quick Item 2 | Использовать быстрый предмет 2 | RU_DFKeyBinds |
| Use Quick Item 3 | Использовать быстрый предмет 3 | RU_DFKeyBinds |
| Use Quick Item 4 | Использовать быстрый предмет 4 | RU_DFKeyBinds |
| Select Weapon Slot 1 | Слот оружия 1 | RU_DFKeyBinds |
| Select Weapon Slot 2 | Слот оружия 2 | RU_DFKeyBinds |
| Select Weapon Slot 3 | Слот оружия 3 | RU_DFKeyBinds |
| Select Weapon Slot 4 | Слот оружия 4 | RU_DFKeyBinds |
| --GAME STATE-- | --СОСТОЯНИЕ ИГРЫ-- | RU_DFKeyBinds |
| Quicksave | Быстрое сохранение | RU_DFKeyBinds |
| Quickload | Быстрая загрузка | RU_DFKeyBinds |
| --INVENTORY UI-- | --ИНТЕРФЕЙС ИНВЕНТАРЯ-- | RU_DFKeyBinds |
| Interaction Layout | Раскладка взаимодействия | RU_DFKeyBinds |

## 6. Дополнительно / Специальные возможности

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Advanced | Дополнительно | MenuDef → RU_DFAdvancedOptions → Title |
| --DIFFICULTY-- | --СЛОЖНОСТЬ-- | RU_DFAdvancedOptions |
| Player Damage Taken | Получаемый урон | RU_DFAdvancedOptions |
| Ammo Received | Количество получаемых патронов | RU_DFAdvancedOptions |
| Consumable Healing Rate | Эффективность лечебных предметов | RU_DFAdvancedOptions |
| Stamina Consumption | Расход выносливости | RU_DFAdvancedOptions |
| Weapon Degredation Rate | Скорость износа оружия | RU_DFAdvancedOptions |
| Resonance Break: Extended Timing | Разрыв резонанса: расширенное окно | RU_DFAdvancedOptions |
| --GAMEPLAY-- | --ИГРОВОЙ ПРОЦЕСС-- | RU_DFAdvancedOptions |
| Damage Number | Числа урона | RU_DFAdvancedOptions |
| HUD (Heads-Up Display) | HUD (интерфейс) | RU_DFAdvancedOptions |
| Interaction Icon | Значок взаимодействия | RU_DFAdvancedOptions |
| Item Tooltip | Подсказка предмета | RU_DFAdvancedOptions |
| Melee Camera Movement | Движение камеры в ближнем бою | RU_DFAdvancedOptions |
| Nulled Landscape Distortion | Искажение Nulled Landscape | RU_DFAdvancedOptions |
| Trenchgun Crosshair | Прицел траншейного ружья | RU_DFAdvancedOptions |
| Tutorials | Обучение | RU_DFAdvancedOptions |
| --MISCELLANEOUS-- | --РАЗНОЕ-- | RU_DFAdvancedOptions |
| Item Pickup Flash Intensity | Яркость вспышки при подборе | RU_DFAdvancedOptions |
| Damage Taken Flash Intensity | Яркость вспышки при получении урона | RU_DFAdvancedOptions |
| Crosshair Color Match Health | Цвет прицела по уровню здоровья | RU_DFAdvancedOptions |

## 7. Джойстик и яркость

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| WARNING: Controller Support is not fully implemented! | ВНИМАНИЕ: Поддержка контроллера реализована не полностью! | MenuDef → RU_NewJoystickOptions → Title |
| Adjust the slider until you can slightly spot the figure in the background. | Передвигайте ползунок, пока фигура на фоне не станет едва различимой. | MenuDef → BrightnessAdjust → Title |

## 8. Значения опций

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Off | Выкл. | MenuDef → OptionValue (CrosshairHealthTypes, vhss, boboption, flashoption, painflashoption) |
| On | Вкл. | MenuDef → OptionValue → CrosshairHealthTypes |
| Minimal | Минимум | MenuDef → OptionValue (vhss, boboption, flashoption, painflashoption) |
| Default | По умолчанию | MenuDef → OptionValue (vhss, boboption, painflashoption) |
| Can't See Sh!t | Ни хрена не видно | MenuDef → OptionValue → vhss |
| Unplayable | Неиграбельно | MenuDef → OptionValue → boboption |
| Eye Damage | Вред глазам | MenuDef → OptionValue → flashoption |
| Standard | Стандарт | MenuDef → OptionValue (skill_ammo, skill_damage, skill_heal, skill_stamina, skill_weapon) |
| Doubled | Вдвое больше | MenuDef → OptionValue (skill_ammo, skill_heal) |
| Halved | Вдвое меньше | MenuDef → OptionValue → skill_damage |
| None | Нет | MenuDef → OptionValue (skill_stamina, skill_weapon) |
| Disabled | Отключено | MenuDef → OptionValue → skill_parry |
| Enabled | Включено | MenuDef → OptionValue → skill_parry |
| Mouse1: Use Item \| Mouse2: Options | ЛКМ: использовать \| ПКМ: действия | MenuDef → OptionValue → InvClickSwap |
| Mouse1: Options \| Mouse2: Use Item | ЛКМ: действия \| ПКМ: использовать | MenuDef → OptionValue → InvClickSwap |

## 9. Описания настроек (`Language.RU`)

| Ключ | Что было (EN) | Что стало (RU) |
|---|---|---|
| DESC_FULLSCREEN | Chooses between windowed and fullscreen mode. | Выбор между оконным и полноэкранным режимом. |
| DESC_RESPRESET | Chooses from a list of resolution presets. | Выбор из списка готовых разрешений. |
| DESC_CUSTOMX | Enter a custom width for the game's resolution. | Введите желаемую ширину разрешения. |
| DESC_CUSTOMY | Enter a custom height for the game's resolution. | Введите желаемую высоту разрешения. |
| DESC_VSYNC | Worsen performance, but does improve it in some very rare case. | Ухудшает производительность, но в редких случаях может улучшить. |
| DESC_MAXFPS | Controls the framerate cap. | Ограничение частоты кадров. |
| DESC_FORCEASPECT | Forces the chosen screen resolution to be considered as the selected aspect ratio, rather than the actual ratio. | Принудительно задаёт соотношение сторон независимо от фактического разрешения. |
| DESC_FORCERATIOSTYLE | Controls whether or not the screen should stretch to a chosen aspect ratio or be letterboxed. | Растягивать изображение под выбранное соотношение сторон или добавлять чёрные полосы. |
| DESC_SCALEFACTOR | Controls the size of the HUD | Размер HUD. |
| DESC_CROSSHAIRSCALE | Controls the size of the crosshair | Размер прицела. |
| DESC_PRECACHE | WARNING: Less suttering but longer loading time. (Slightly more likely to crash - maybe) | ВНИМАНИЕ: меньше подтормаживаний, но дольше загрузка. (Чуть выше шанс вылета — возможно) |
| DESC_VHS | Controls the intensity of the VHS shader. | Интенсивность VHS-шейдера. |
| DESC_VHSTear | Controls the screen tearing FX of the VHS shader. | Эффект разрыва изображения VHS. |
| DESC_BLOOM | Controls whether or not lights give off a powerful glow. | Включает мощное свечение источников света. |
| DESC_SSAO | Controls the quality of ambient occlusion | Качество фонового затенения (SSAO). |
| DESC_TEXFILTER | Controls which texture filtering mode to use. | Режим фильтрации текстур. |
| DESC_FOV | Controls how wide the player's peripheral vision extends. | Ширина поля зрения. |
| DESC_GAMMA | Controls the degree of gamma correction. | Степень гамма-коррекции. |
| DESC_BRIGHTNESS | Controls the brightness level. | Уровень яркости. |
| DESC_CONTRAST | Controls the contrast level. | Уровень контраста. |
| DESC_SATURATION | Controls the saturation level. | Уровень насыщенности. |
| DESC_MASTERVOLUME | Controls the overall volume. | Общая громкость. |
| DESC_SFXVOLUME | Controls the volume at which in-game sound effects are played. | Громкость звуковых эффектов. |
| DESC_MUSICVOLUME | Controls the volume at which the music is played. | Громкость музыки. |
| DESC_MENUVOLUME | Controls the volume at which menu-mode sound effects are played. | Громкость звуков меню. |
| DESC_BACKGROUND | Controls whether or not to let the sound and music to continue playing in the background if the program's window loses focus. | Продолжать воспроизведение звука и музыки, когда окно игры не в фокусе. |
| DESC_TUTORIAL | Controls whether or not tutorial prompts are displayed. | Показывать обучающие подсказки. |
| DESC_DAMNUM | Controls whether or not to display damage number when attacking enemies. | Показывать числа урона при атаке врагов. |
| DESC_ARMORSFX | Controls whether or not to play an audio cue when armor points are completely depleted. | Звуковой сигнал при полном истощении брони. |
| DESC_RESETBIND | Backspace = Reset binding | Backspace — сбросить привязку |
| DESC_SGCX | Enables crosshair for the Trench Gun to assist aiming. | Включает прицел для траншейного ружья. |
| DESC_DISTORTION | Disable the visual distortion in Nulled Landscape. | Отключает визуальные искажения в Nulled Landscape. |
| DESC_HUD | Disable the in-game HUD. | Отключает HUD в игре. |
| DESC_TOOLTIP | Controls information displayed when highlighting consumables. | Информация при наведении на расходники. |
| DESC_ICON | Controls whether or not to render interaction icons. | Показывать значки взаимодействия. |
| DESC_MELEECAM | Controls whether or not melee attacks move the camera. | Движение камеры при атаках ближнего боя. |

## 10. Загрузка и сохранение

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Load Game | Загрузить игру | ZScript/UI/UIZForms/Load Menu/LoadMenu.zsc |
| Save Game | Сохранить игру | ZScript/UI/UIZForms/Save Menu/SaveMenu.zsc |
| Delete Save?\n | Удалить сохранение?\n | LoadSaveBase.zsc → ConfirmDelete |
| DELETE \cU(Y) | УДАЛИТЬ \cU(Y) | LoadSaveBase.zsc → ConfirmDelete |
| CANCEL \cU(N) | ОТМЕНА \cU(N) | LoadSaveBase.zsc → ConfirmDelete |
| Overwrite Save? | Перезаписать сохранение? | LoadSaveBase.zsc → ConfirmOverwrite |
| SAVE \cU(Y) | СОХРАНИТЬ \cU(Y) | LoadSaveBase.zsc → ConfirmOverwrite |
| CANCEL \cU(N) | ОТМЕНА \cU(N) | LoadSaveBase.zsc → ConfirmOverwrite |
| Create New Save? | Создать новое сохранение? | LoadSaveBase.zsc → CreateNewSave |
| Confirm | Подтвердить | LoadSaveBase.zsc → CreateNewSave |
| Cancel | Отмена | LoadSaveBase.zsc → CreateNewSave |
| Cannot Save while on the title screen \n Please load or start a new game to save! | На титульном экране сохраняться нельзя.\nЗагрузите игру или начните новую, чтобы сохраниться! | SaveMenu.zsc → MainMenuText |
| Time:  | Время:  | LoadMenu.zsc / SaveMenu.zsc → SaveSlotSaveAge |
| Date:  | Дата:  | LoadMenu.zsc / SaveMenu.zsc → SaveSlotTimeSaved |

Название карты в слоте извлекается до перевода строки, поэтому локализованное «Время:» не попадает в подпись карты и не перекрывает дату/время.

## 11. Титульный экран

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| [Press any button] | [Нажмите любую кнопку] | ZScript/UI/GenericScreenStuff.txt |

## 12. Шрифты

| Что было | Что стало | Где |
|---|---|---|
| bigfont: 256 латинских глифов | Полный набор + 74 глифа: 33 заглавные, 33 строчные (включая Ё/ё) и 8 типографских знаков; используется в главном меню | Fonts/bigfont/ |
| BigUpper: движковый английский шрифт настроек | Полная копия bigfont + кириллица | Fonts/BigUpper/ |
| ACS_FONT: 592 латинских глифа | Полный набор + 74 глифа для описаний/HUD-сообщений | Fonts/ACS_FONT/ |
| smallfont: 592 латинских глифа | Полный набор + 74 глифа для сохранений/загрузок | Fonts/smallfont/ |
| NewSmallFont: встроенный hex-шрифт | Не используется после возврата к BIGFONT | — |
| dialoguefont: уже с кириллицей | Не менялся; используется для реплик | Fonts/dialoguefont/ |
| npcfont / DF_FONT / ChatBoxFont / CONVO_FONT | Исходные шрифты не меняются; UI переключён на RU_-версии | FontDefs.txt / HiRes/DF_FONT |

Папки шрифтов в UZDoom загружаются атомарно, поэтому в PK3 кладутся полные наборы: оригинальные PNG + `font.inf` + кириллица.

## 13. Вёрстка и техническая часть

| Что было | Что стало |
|---|---|
| Главное меню: NewSmallFont, золотой выбранный пункт | BIGFONT (оригинальный шрифт); выбранный пункт белый + подсветка рамкой |
| Позиции пунктов 128/136/127/127/138/147 | 124/126/111/110/140/140 — под русские подписи BIGFONT, центр 160 |
| Вкладки настроек: BIGFONT через Menu/tabmenu.zs | Оригинальный BigUpper; отдельный font override убран; подписи вкладок переведены |
| Настройки: protected OptionMenu с английскими подписями | Новые RU_-меню; вкладки ведут на них |
| Настройки: описания из Language.txt на английском | Language.RU с [ru]-секциями для всех DESC_* |
| Загрузка/сохранение: английские заголовки и попапы | Русские заголовки, попапы, кнопки, Время/Дата |
| Карта/сложность/эпизод/выход: английские | Переведены в MapInfo |
| Титульный экран: [Press any button] по центру | [Нажмите любую кнопку]; x считается по ширине строки (BIGFONT.StringWidth) |

### Новые меню настроек

| Было | Стало | Где используется |
|---|---|---|
| DFDisplayOptions (protected) | RU_DFDisplayOptions | TabTest → Графика |
| DFKeyBinds (protected) | RU_DFKeyBinds | TabTest → Управление |
| DFSoundOptions (protected) | RU_DFSoundOptions | TabTest → Звук |
| DFAdvancedOptions (protected) | RU_DFAdvancedOptions | TabTest → Специальные возможности |
| NewJoystickOptions (protected) | RU_NewJoystickOptions | RU_DFAdvancedOptions → Субменю джойстика |

## 14. Что не переведено в этой итерации

| Раздел | Статус |
|---|---|
| HUD, инвентарь, кодекс | Шрифты RU_ готовы; текст ещё не переведён |
| Имена NPC | RU_npcfont готов; текст ещё не переведён |
| Сюжетный текст | Language.Items, Language.Weapon, Language.Upgrade, Language.Map, Language.NPC* |
| ACS и диалоги карт | ACS/*.acs, SCRIPTS/BEHAVIOR, DIALOGUE |
| Озвучка | Остаётся английской; перевод текстовый |

## 15. Запуск

- `test/run_test.cmd` или ярлык **Divine Frequency (RU)** — полный экран, `language=ru`.
- `test/run_original.cmd` или ярлык **Divine Frequency (Original)** — полный экран, `language=enu`.
- Конфиги: `test/dfconfig-test.ini` и `test/dfconfig-original.ini`; основной `dfconfig.ini` не изменяется.

Проверка сборки: PK3 пересобран, в игре не запускался. Визуальная проверка — за тобой.

## 16. Открытые вопросы (для стилевой вычитки)

- `Use Psykhus Injector` → «Использовать инъектор Психуса»: написание «Психус/Психхус» согласовать с будущим переводом предметов (`Language.Items`).
- `Nulled Landscape` оставлено без перевода в `RU_DFAdvancedOptions` и `DESC_DISTORTION`; согласовать с названием локации.
- `Can't See Sh!t` → «Ни хрена не видно»: сохранена грубоватая шутка оригинала; при желании смягчить.
- `Consumable Healing Rate` → «Эффективность лечебных предметов»: в коде `healAmount * modf_heal`, то есть количество лечения, а не скорость.
- `Mouse2: Options` → «ПКМ: действия»: в инвентаре открывает меню действий предмета (`ShowExtendedOption`).
- Названия актов оставлены как в оригинале («Чистые обнажённые умы» и т. п.).
- Игровые сокращения (`DMG`, `PT`, `HP`, `PSI` и т. п.) оставлять как в оригинале, не переводить на русские сокращения вроде «УРН».

## 17. UI-шрифты (внутриигровой интерфейс)

| Шрифт | Что сделано | Где используется |
|---|---|---|
| RU_DF_FONT | 99 оригинальных глифов DVFFN + 76 сгенерированных (кириллица и типографика); SpaceWidth 9, Kerning -1 | HUD, инвентарь, кодекс, заметки, улучшения |
| RU_ChatBoxFont | Те же глифы; SpaceWidth 5, Kerning -1 | Чат и сообщения о подборе |
| RU_CONVO_FONT | Те же глифы; SpaceWidth 10, Kerning 0 | Реплики в диалогах |
| RU_npcfont | 592 оригинальных глифа + 74 сгенерированных пары; золотой стиль, SpaceWidth 5, Kerning -3, Scale 1.2 | Имена NPC |

В ZScript-оверрайдах ссылки заменены: `DF_FONT` → `RU_DF_FONT`, `ChatBoxFont` → `RU_ChatBoxFont`, `CONVO_FONT` → `RU_CONVO_FONT`, `npcfont` → `RU_npcfont`. Исходные шрифты не изменяются.

## 18. UI: инвентарь и вкладки (первый блок)

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Consumables & Medications (%d/%d) | Расходники и медикаменты (%d/%d) | InventoryMenu.zc → conTitle |
| Key Items | Ключевые предметы | InventoryMenu.zc → subHead2 |
| Abilities | Способности | InventoryMenu.zc → subHead3 |
| Attribute | Характеристики | InventoryMenu.zc → AtrTextHeader |
| Condition | Состояние | InventoryMenu.zc → CStateTextHeader |
| Current Objective | Текущая цель | InventoryMenu.zc → ObjHeader |
| Description: | Описание: | InventoryMenu.zc → itemTextHeader |
| Location: %s | Локация: %s | InventoryMenu.zc → LocationName |
| Assign to Quick Use | Назначить на быстрое использование | InventoryMenu.zc → BindingLabel |
| \cD[Mouse1] \cJUse Item | \cD[ЛКМ] \cJИспользовать | InventoryMenu.zc → m1Tip |
| \cD[Mouse2] \cJOptions | \cD[ПКМ] \cJДействия | InventoryMenu.zc → m2Tip |
| Inventory | Инвентарь | Верхние вкладки (5 файлов) |
| Weapons | Оружие | Верхние вкладки (5 файлов) |
| Bestiary | Бестиарий | Верхние вкладки (5 файлов) |
| Map | Карта | Верхние вкладки (5 файлов) |
| Help | Помощь | Верхние вкладки (5 файлов) |
| Effect: | Эффект: | InventoryMenu.zc → itemEffectHeader |
| LEVEL %d Avatar:\n%s\n\nStrength: %d\nWits: %d\nPhysique: %d\n\n    Exaltation: %d\n    Mutation: %d\n    Psi. Attunement: %d/%d | УРОВЕНЬ %d Аватар:\n%s\n\nСила: %d\nРазум: %d\nТелосложение: %d\n\n    Экзальтация: %d\n    Мутация: %d\n    Пси-настройка: %d/%d | InventoryMenu.zc → Attribute |
| Toxin (Lethal)\n\cR-Suffer Periodic Damage\n-Impaired Movement\n-Impaired Aim\n\n | Токсин (смертельный)\n\cR-Периодический урон\n-Нарушение движения\n-Нарушение прицеливания\n\n | InventoryMenu.zc → Condition |
| Toxin (Moderate)\n\cR-Impaired Aim\n\n | Токсин (умеренный)\n\cR-Нарушение прицеливания\n\n | InventoryMenu.zc → Condition |
| \cJRadiation (Lethal)\n\cR-Imminent Overload\n-Impaired Vision\n\n | \cJРадиация (смертельная)\n\cR-Неминуемая перегрузка\n-Нарушение зрения\n\n | InventoryMenu.zc → Condition |
| \cJRadiation (Moderate)\n\cR-Impaired Vision\n\n | \cJРадиация (умеренная)\n\cR-Нарушение зрения\n\n | InventoryMenu.zc → Condition |
| Use Item | Использовать | InventoryMenu.zc → epUse |
| Drop Item | Выбросить | InventoryMenu.zc → epDrop |
| Keybind | Привязать | InventoryMenu.zc → epBind |
| Handgun: %d | Пистолет: %d | InventoryMenu.zc → ремонт |
| Trenchgun: %d | Траншейка: %d | InventoryMenu.zc → ремонт |
| Spray Can: %d | Баллончик: %d | InventoryMenu.zc → ремонт |
| Assault Rifle: %d | Автомат: %d | InventoryMenu.zc → ремонт |
| Enhancements | Улучшения | Codex.txt → кнопка |
| Information: | Информация: | Codex.txt → wInfoHeader |
| Secondary Fire: | Альтернативный огонь: | Codex.txt → wAbilityHeader |
| Additional Mechanics: | Дополнительные механики: | Codex.txt → wQuirkHeader |
| Weapon Modifications: | Модификации оружия: | Codex.txt → Info_Upgrade |
| Character Ascension: | Возвышение персонажа: | Codex.txt → Info_Upgrade |
| Unique: | Уникальное: | Codex.txt → Info_Upgrade |
| [W][A][S][D] - Movement / [E] - Interact | [W][A][S][D] - Движение / [E] - Взаимодействие | GenericScreenStuff.txt → tutorial |
| Information: | Информация: | Bestiary.txt → bPhyHeader |
| Additional Data: | Дополнительные данные: | Bestiary.txt → bPhyHeader2 |
| Snapshot: | Снимок: | Bestiary.txt → bImageHeader |
| Archive: | Архив: | Bestiary.txt → bLoreHeader |
| Hobo | Бродяга | Player.txt → title |
| Mutation Lv.1 | Мутация ур.1 | Player.txt → phyLevel_nfo |

Названия и описания предметов из `Language.Items` в этот блок ещё не входят — следующий этап.

## 19. Оружие (`Language.Weapon`)

| Ключ | Что было (EN) | Что стало (RU) |
|---|---|---|
| Hand_Info | Base Damage: 20 + (20 * STR Level)\nDamage Type: Physical\nWeapon Slot: 1\nBase Draw Speed: Average\nBase Reload Speed: N/A\nBase Spread: N/A\n\n\cU(Requires Strength 1)\n-\cJAttack damage bypass most resistance. Most attacks can inflict \cIResonance Break\cJ. | Базовый урон: 20 + (20 * уровень Силы)\nТип урона: Физический\nСлот оружия: 1\nСкорость доставания: Средняя\nСкорость перезарядки: Н/Д\nРазброс: Н/Д\n\n\cU(Требуется Сила 1)\n-\cJУрон от атак игнорирует большую часть сопротивления. Большинство атак могут накладывать \cIРазрыв резонанса\cJ. |
| Hand_Ability | \cU(Requires Strength 1)\n-\cFBlocking\cJ: \cDHold [Secondary Fire] \cJto block. Blocking reduces 50% of incoming damage and consumes Stamina.\n\n\cU(Requires Strength 2)\n-\cFRiposte\cJ: \cJBlocking at the moment before an attack lands will automatically trigger a counter-attack. | \cU(Требуется Сила 1)\n-\cFБлок\cJ: \cDУдерживайте [Альтернативный огонь] \cJдля блока. Блок снижает 50% входящего урона и расходует выносливость.\n\n\cU(Требуется Сила 2)\n-\cFРипост\cJ: \cJБлок в момент перед ударом автоматически запускает контратаку. |
| Hand_Quirk | \cU(Requires Strength 1)\n-\cFHeadbutt\cJ: \cDPress [Primary Fire]\cJ while blocking to launch a powerful headbutt at the cost of inflicting self damage.\n\n\cU(Requires Strength 1)\n-\cFHeavy Attack\cJ: \cDHold [Reload]\cJ to build up power for a powerful strike. Release the button to unleash the attack.\n\n\cU(Requires Strength 1)\n-\cFRetaliation Power\cJ: Blocking damage and headbutting will build up the retaliation power meter. Once the retaliation power meter is full, \cDPress [Reload] \cJto trigger a massive area-of-effect blast.\n\n\cU(Requires Strength 4)\n-\cFTouch of Death\cJ: \cDPress [Swap Fire Mode]\cJ to trigger an instant-kill attack. Requires killing enemies to charge up. Does not work on bosses. | \cU(Требуется Сила 1)\n-\cFУдар головой\cJ: \cDНажмите [Основной огонь]\cJ во время блока, чтобы нанести мощный удар головой ценой собственного здоровья.\n\n\cU(Требуется Сила 1)\n-\cFТяжёлая атака\cJ: \cDУдерживайте [Перезарядка]\cJ, чтобы накопить силу для мощного удара. Отпустите кнопку, чтобы высвободить атаку.\n\n\cU(Требуется Сила 1)\n-\cFСила возмездия\cJ: Блок урона и удары головой заполняют шкалу силы возмездия. Когда шкала заполнена, \cDнажмите [Перезарядка]\cJ, чтобы вызвать мощный взрыв по площади.\n\n\cU(Требуется Сила 4)\n-\cFКасание смерти\cJ: \cDНажмите [Сменить режим огня]\cJ, чтобы запустить атаку с мгновенным убийством. Требует убийств врагов для зарядки. Не работает на боссах. |
| Handgun_Info | Base Damage: \cR50 \cJ\| \cI(300)\cJ\nDamage Type: \cRHypertrauma \cJ\| \cIExplosive\cJ\nWeapon Slot: 2\nBase Draw Speed: Average\nBase Reload Speed: Average\nBase Spread: Low\n\n\n**FIRE MODES**\n---------------------------------------------------\n-\cRHypertrauma Rounds\cJ: Homemade rounds cooked up in some random basement and overloaded with gunpowder. Designed primarily for maximum fragmentation and shredding. \cDEffective against organic targets. Deals extra damage on headshots. Punches through multiple targets.\cJ.\n\n-\cIHigh-Explosive Rounds\cJ: Experimental demolition rounds manufactured by the CCE. \cDEffective against all targets, \cRbut can kill you if you aren't careful. | Базовый урон: \cR50 \cJ\| \cI(300)\cJ\nТип урона: \cRГипертравма \cJ\| \cIВзрывной\cJ\nСлот оружия: 2\nСкорость доставания: Средняя\nСкорость перезарядки: Средняя\nРазброс: Низкий\n\n\n**РЕЖИМЫ ОГНЯ**\n---------------------------------------------------\n-\cRПатроны гипертравмы\cJ: Самодельные патроны, собранные в каком-то подвале и забитые порохом под завязку. Рассчитаны в первую очередь на максимальную фрагментацию и разрывание. \cDЭффективны против органических целей. Наносят дополнительный урон при попадании в голову. Пробивают несколько целей.\cJ.\n\n-\cIФугасные патроны\cJ: Экспериментальные подрывные патроны производства CCE. \cDЭффективны против любых целей, \cRно могут убить вас, если не проявить осторожность. |
| Handgun_Ability | Conjure a swarm of insects to inflict Brain Rot on a target. Victims under the Brain Rot status become \cIFriendly\cJ and take constant damage. If the target dies, it will explode and damage nearby enemies.\n\n\cFRequires\cJ: Psychoentomo Communion\n\cFPsi Cost\cJ: 5 | Призовите рой насекомых, чтобы наложить на цель Гниль мозга. Жертвы под эффектом Гнили мозга становятся \cIдружелюбными\cJ и получают постоянный урон. Если цель умирает, она взрывается и наносит урон врагам поблизости.\n\n\cFТребуется\cJ: Психоэнтомное единение\n\cFЗатраты пси\cJ: 5 |
| Handgun_Quirk | \cGDegradation:\cJ\nRepeated firing will wear down the weapon's barrel, reducing bullet pressure and muzzle velocity. Therefore, leading to \cRreduced damage\cJ. | \cGИзнос:\cJ\nЧастая стрельба изнашивает ствол оружия, снижая давление пуль и начальную скорость. Это приводит к \cRснижению урона\cJ. |
| Shotgun_Info | Base Damage: 24-256\nDamage Type: Physical\nWeapon Slot: 3\nBase Draw Speed: Slow\nBase Reload Speed: Slow\nBase Spread: High\n\n\n**FIRE MODES**\n---------------------------------------------------\n-\cFPump-action\cJ: Switch to a standard pump-action technique.\n\n-\cFSlamfire\cJ: Switch to a slamfiring technique, gaining exceptionally \cDhigher firing rate\cJ, but at the cost of \cRworse recoil control\cJ. | Базовый урон: 24-256\nТип урона: Физический\nСлот оружия: 3\nСкорость доставания: Медленная\nСкорость перезарядки: Медленная\nРазброс: Высокий\n\n\n**РЕЖИМЫ ОГНЯ**\n---------------------------------------------------\n-\cFПомповый режим\cJ: Переключиться на стандартную помповую технику.\n\n-\cFСлэмфайр\cJ: Переключиться на технику слэмфайра, получая исключительно \cDвысокую скорость стрельбы\cJ, но ценой \cRхудшего контроля отдачи\cJ. |
| Shotgun_Ability | Discharge an electric orb that will bounce from the primary target up to 2 additional targets, \cIStunning\cJ each victim hit.\n\nEach target struck by the electric orb will grant you 1 Armor Stack and voltaically charge the Trench Gun's next shot, doubling damage dealt.\n\n\cFRequires\cJ: Limited Aeromancy Conduction\n\cFPsi Cost\cJ: 3 | Высвободите электрическую сферу, которая отскочит от основной цели к ещё 2 целям, \cIоглушая\cJ каждую поражённую жертву.\n\nКаждая цель, поражённая электрической сферой, даёт вам 1 слой брони и электризует следующий выстрел траншейного ружья, удваивая наносимый урон.\n\n\cFТребуется\cJ: Ограниченная проводимость аэромантии\n\cFЗатраты пси\cJ: 3 |
| Shotgun_Quirk | \cFRandomized Velocity:\cJ\nEach shell contains 8 pellets. Each pellet deals 8 Damage with a multiplier of 3-4. \n\n\cFReliable:\cJ\nThis weapon will still function even at zero durability.\n\n\cFDueling Weapon:\cJ\nCapable of inflicting a \cIResonance Break\cJ.\n\n\cGDegradation:\cJ\nRepeated firing will wear down the weapon's barrel, creating uneven pressure and erratic flight paths for the pellets. Therefore, leading to \cRsub-optimal scattering \cJand \cRslower firing rate\cJ.\n\n\cGBalance:\cJ\nDoes not inflict bonus headshot damage. | \cFСлучайная скорость:\cJ\nКаждый патрон содержит 8 дробин. Каждая дробина наносит 8 урона с множителем 3-4.\n\n\cFНадёжность:\cJ\nОружие продолжает работать даже при нулевой прочности.\n\n\cFДуэльное оружие:\cJ\nСпособно накладывать \cIРазрыв резонанса\cJ.\n\n\cGИзнос:\cJ\nЧастая стрельба изнашивает ствол оружия, создавая неравномерное давление и хаотичные траектории дробин. Это приводит к \cRнеоптимальному разлёту\cJ и \cRснижению скорости стрельбы\cJ.\n\n\cGБаланс:\cJ\nНе наносит дополнительный урон при попадании в голову. |
| Spray_Info | Base Damage: 60-70\nDamage Type: \c[DarkGreen]Necrotic\cJ\nWeapon Slot: 4\nBase Draw Speed: Average\nBase Reload Speed: N/A\nBase Spread: Low\n\n\n**FIRE MODES**\n---------------------------------------------------\n-\cFSpray\cJ: Spray deadly nerve gas. \cDExtremely effective against organic targets\cJ.\n\n-\cFThrow\cJ: Throw the spray can. It explodes shortly after impact, \cDreleasing a healing gas cloud\cJ. | Базовый урон: 60-70\nТип урона: \c[DarkGreen]Некротический\cJ\nСлот оружия: 4\nСкорость доставания: Средняя\nСкорость перезарядки: Н/Д\nРазброс: Низкий\n\n\n**РЕЖИМЫ ОГНЯ**\n---------------------------------------------------\n-\cFРаспыление\cJ: Распылите смертельный нервно-паралитический газ. \cDЧрезвычайно эффективен против органических целей\cJ.\n\n-\cFБросок\cJ: Бросьте баллончик. Он взрывается вскоре после удара, \cDвысвобождая облако лечебного газа\cJ. |
| Spray_Ability | Forcibly tear apart the biomass of fallen enemies and fuse it with your own to replace damaged or missing parts. Grants 15 HP and 1 Armor Stack per corpse.\n\nThe enemy corpse has to be somewhat intact to qualify.\n\n\cFRequires\cJ: Meta-Bioinduction\n\cFPsi Cost\cJ: 2 | Насильно разорвите биомассу павших врагов и срастите её со своей, чтобы заменить повреждённые или недостающие части. Даёт 15 HP и 1 слой брони за каждый труп.\n\nТруп врага должен быть относительно целым.\n\n\cFТребуется\cJ: Мета-биоиндукция\n\cFЗатраты пси\cJ: 2 |
| Spray_Quirk | \cFMetaphysical Binding:\n\cJThe spray can and storage vial are ontologically tethered, bypassing the need to reload.\n\n\cGDegradation:\cJ\n\cJRepeated use corrodes the weapon's nozzle, disrupting optimal pressure and acceleration. Therefore, leading to \cRreduced range\cJ. | \cFМетафизическая связь:\n\cJБаллончик и накопитель онтологически связаны, что избавляет от необходимости перезаряжаться.\n\n\cGИзнос:\cJ\n\cJЧастое использование разъедает сопло оружия, нарушая оптимальное давление и ускорение. Это приводит к \cRснижению дальности\cJ. |
| AR_Info | Base Damage: 100\nDamage Type: \cF[\|\|\|\|\|\|\|\|\|]\cJ\nWeapon Slot: 4\nBase Draw Speed: Slow\nBase Reload Speed: Slow\nBase Spread: Low\n\n\n**FIRE MODES**\n---------------------------------------------------\n-\cFBurst Fire\cJ: Switch to a five rounds burst firing mode.\n\n-\cFFull Auto\cJ: Switch to a fully automatic firing mode. | Базовый урон: 100\nТип урона: \cF[\|\|\|\|\|\|\|\|\|]\cJ\nСлот оружия: 4\nСкорость доставания: Медленная\nСкорость перезарядки: Медленная\nРазброс: Низкий\n\n\n**РЕЖИМЫ ОГНЯ**\n---------------------------------------------------\n-\cFОчередь\cJ: Переключиться на режим стрельбы очередями по пять патронов.\n\n-\cFПолный автомат\cJ: Переключиться на полностью автоматический режим стрельбы. |
| AR_Ability | Manifest matter at a localized level. For 20 seconds, the Assault Rifle will not consume ammo when firing, nor will it require ammo to fire.\n\n\cFRequires\cJ: Empowered Resonance\n\cFPsi Cost\cJ: 7 | Материализуйте материю на локальном уровне. В течение 20 секунд штурмовая винтовка не расходует патроны при стрельбе и не требует патронов для выстрела.\n\n\cFТребуется\cJ: Усиленный резонанс\n\cFЗатраты пси\cJ: 7 |
| AR_Quirk | \cGDegredation:\n\cJRepeated firing will compromise the weapon's barrel and muzzle, causing unpredictable horizontal deviation and muzzle climb. Therefore, leading to \cRworse recoil control\cJ. | \cGИзнос:\n\cJЧастая стрельба повреждает ствол и дуло оружия, вызывая непредсказуемое горизонтальное отклонение и подброс ствола. Это приводит к \cRхудшему контролю отдачи\cJ. |

`DB_Info`/`DB_Ability`/`DB_Quirk` (молот) оставлены без перевода: оригинальный текст намеренно искажён.

## 20. UI: улучшения, магазин и создание персонажа

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Enter Character Name: | Введите имя персонажа: | CreationMenu.zc |
| Accept | Принять | CreationMenu.zc |
| Barrel Mod | Модификация ствола | GunUpgrade.zc |
| Extended Magazine | Увеличенный магазин | GunUpgrade.zc |
| Exotic Powder Mixture | Экзотическая пороховая смесь | GunUpgrade.zc |
| Current Exaltation: %d | Текущая экзальтация: %d | LevelUpMenu.zc |
| Upgrade %s: %d -> %d | Улучшение %s: %d -> %d | LevelUpMenu.zc |
| Cost: %d | Стоимость: %d | LevelUpMenu.zc |
| Strength / Wits / Physique | Сила / Разум / Телосложение | LevelUpMenu.zc |
| SECONDARY ATTRIBUTES | ВТОРИЧНЫЕ АТРИБУТЫ | LevelUpMenu.zc |
| Exaltation / Mutation | Экзальтация / Мутация | LevelUpMenu.zc |
| Confirm Selection: | Подтвердить выбор: | LevelUpMenu.zc / ShopMenu.zc |
| Confirm / Cancel | Подтвердить / Отмена | UIUpgrades/*.zc |
| [Esc] Leave | [Esc] Выйти | UIUpgrades/*.zc / NewItemMenu.zc |
| Survival Response | Реакция выживания | ShopMenu.zc |
| Third Mind | Третий разум | ShopMenu.zc |
| Predatory Focus | Хищный фокус | ShopMenu.zc |
| Even More Pockets! | Ещё больше карманов! | ShopMenu.zc |
| Reflect Damage | Отражение урона | ShopMenu.zc |
| Endless Hunger | Бесконечный голод | ShopMenu.zc |
| Organic Caltrops | Органические шипы | ShopMenu.zc |
| Psychic Blast | Психический взрыв | ShopMenu.zc |
| Current Mutation Point: %d | Текущие очки мутации: %d | ShopMenu.zc |
| Max | Макс. | Hud.txt |

## 21. NPC: персонажи и диалоги

| Файл | Ключей переведено | Что охвачено |
|---|---|---|
| Language.NPC | 48/48 | Создание персонажа, UI диалогов, Spray/Vial, ODD_DEVICE |
| Language.NPCBox | 57/57 | Первый NPC «Подозрительная коробка» |
| Language.NPCDisciples | 75/75 | Холодильник/Ученик Рааха и ученик Сджинна |
| Language.NPCLantern | 31/31 | Говорящий фонарь |
| Language.NPCMISC | 11/11 | Инженер, врата, труп |
| Language.NPCMonastery | 21/21 | Алтарь и аномальный гриб |
| Language.NPCPrism | 7/11 | Таинственная призма: читаемые имена/выборы; шифрованный текст оставлен |
| Language.NPCDreamer | 12/28 | Сновидец и ученик Сармипадхвы (активные ключи) |
| Language.NPCEgg | 27/27 | Яйцо и броня |
| Language.NPCADB | 96/115 | Актор Чувак Братан, пси-способности; закомментированный блок не переводился |
| Language.NPCAstronaut | 46/78 | Астронавт: читаемые реплики и хроника; искажённый текст оставлен |
| Language.Duel | 16/16 | Дуэли и заметки |
| Language.Weapon.txt | 15/17 | Оружие; DB_* (молот) оставлены |

Шрифт имён — `RU_npcfont`, реплики — `dialoguefont` (кириллица уже была в оригинале), ответы — `RU_CONVO_FONT`.

Имена и короткие реплики, зашитые прямо в карты (`World's Anchor`, `TERMINAL`, `Door` и т. п.), переводятся в `ConversationMenuBase.TranslateInline`; в таблицу `Language.*` они не входят. В `Language.NPCPrism`, `Language.NPCAstronaut` и части `Language.NPCADB` оригинал намеренно искажён/зашифрован — переведены читаемые имена, выборы и реплики, остальное оставлено как в оригинале.

## 22. Предметы, улучшения, кодекс, заметки

| Файл | Ключей переведено | Что охвачено |
|---|---|---|
| Language.Items.txt | 106/106 | Предметы, расходники, ключи |
| Language.Upgrade.txt | 116/116 | Улучшения, мутации, способности |
| Language.Tutorial | 13/13 | Подсказки и советы |
| Language.Objective | 7/7 | Цели |
| Language.Bestiary.txt | 31/31 | Бестиарий |
| Language.Note.txt | 35/35 | Заметки и записи |
| Language.Artistical | 15/15 | Лор и вступление |
| Language.Map | 0/311 | Карта: ещё не переведена |

`Language.Map` (около 320 ключей) пока не переведён; ACS-скрипты карт — следующий блок.