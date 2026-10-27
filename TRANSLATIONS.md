# Divine Frequency — таблица перевода меню

Дата: 27.10.2026

Сборка: `dist/DF_RU.pk3` — 2003 записи, ~940 КБ.

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
| Title | Заголовок | MapInfo → map TITLEMAP |
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
| Accessibility | Доступность | MenuDef → TabTest |

## 4. Графика

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Resolution Width | Ширина разрешения | MenuDef → RU_DFDisplayOptions |
| Resolution Height | Высота разрешения | MenuDef → RU_DFDisplayOptions |
| VHS Intensity | Интенсивность VHS | MenuDef → RU_DFDisplayOptions |
| VHS Tearing | Разрыв VHS | MenuDef → RU_DFDisplayOptions |
| HUD Size | Размер HUD | MenuDef → RU_DFDisplayOptions |

Остальные подписи вкладки «Графика» (`$VIDMNU_*`, `$DSPLYMNU_*`, `$GLPREFMNU_*`) берутся из `language.csv` и уже локализованы движком.

## 5. Управление

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Keybinds | Управление | MenuDef → RU_DFKeyBinds → Title |
| Camera Horizontal Sensitivity | Горизонтальная чувствительность камеры | RU_DFKeyBinds |
| Camera Vertical Sensitivity | Вертикальная чувствительность камеры | RU_DFKeyBinds |
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
| Use Quick Item 1 | Быстрый предмет 1 | RU_DFKeyBinds |
| Use Quick Item 2 | Быстрый предмет 2 | RU_DFKeyBinds |
| Use Quick Item 3 | Быстрый предмет 3 | RU_DFKeyBinds |
| Use Quick Item 4 | Быстрый предмет 4 | RU_DFKeyBinds |
| Select Weapon Slot 1 | Слот оружия 1 | RU_DFKeyBinds |
| Select Weapon Slot 2 | Слот оружия 2 | RU_DFKeyBinds |
| Select Weapon Slot 3 | Слот оружия 3 | RU_DFKeyBinds |
| Select Weapon Slot 4 | Слот оружия 4 | RU_DFKeyBinds |
| --GAME STATE-- | --СОСТОЯНИЕ ИГРЫ-- | RU_DFKeyBinds |
| Quicksave | Быстрое сохранение | RU_DFKeyBinds |
| Quickload | Быстрая загрузка | RU_DFKeyBinds |
| --INVENTORY UI-- | --ИНТЕРФЕЙС ИНВЕНТАРЯ-- | RU_DFKeyBinds |
| Interaction Layout | Раскладка взаимодействия | RU_DFKeyBinds |

## 6. Дополнительно / Доступность

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Advanced | Дополнительно | MenuDef → RU_DFAdvancedOptions → Title |
| --DIFFICULTY-- | --СЛОЖНОСТЬ-- | RU_DFAdvancedOptions |
| Player Damage Taken | Получаемый урон | RU_DFAdvancedOptions |
| Ammo Received | Получаемые патроны | RU_DFAdvancedOptions |
| Consumable Healing Rate | Эффективность лечения расходниками | RU_DFAdvancedOptions |
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
| Crosshair Color Match Health | Цвет прицела по здоровью | RU_DFAdvancedOptions |

## 7. Джойстик и яркость

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| WARNING: Controller Support is not fully implemented! | ВНИМАНИЕ: Поддержка контроллера реализована не полностью! | MenuDef → RU_NewJoystickOptions → Title |
| Adjust the slider until you can slightly spot the figure in the background. | Настройте ползунок, пока едва не начнёте различать фигуру на фоне. | MenuDef → BrightnessAdjust → Title |

## 8. Значения опций

| Что было (EN) | Что стало (RU) | Где |
|---|---|---|
| Off | Выкл. | MenuDef → OptionValue (CrosshairHealthTypes, vhss, boboption, flashoption, painflashoption) |
| On | Вкл. | MenuDef → OptionValue → CrosshairHealthTypes |
| Minimal | Минимум | MenuDef → OptionValue (vhss, boboption, flashoption, painflashoption) |
| Default | По умолчанию | MenuDef → OptionValue (vhss, boboption, painflashoption) |
| Can't See Sh!t | Ничего не видно | MenuDef → OptionValue → vhss |
| Unplayable | Неиграбельно | MenuDef → OptionValue → boboption |
| Eye Damage | Вред глазам | MenuDef → OptionValue → flashoption |
| Standard | Стандарт | MenuDef → OptionValue (skill_ammo, skill_damage, skill_heal, skill_stamina, skill_weapon) |
| Doubled | Удвоено | MenuDef → OptionValue (skill_ammo, skill_heal) |
| Halved | Половинный | MenuDef → OptionValue → skill_damage |
| None | Нет | MenuDef → OptionValue (skill_stamina, skill_weapon) |
| Disabled | Отключено | MenuDef → OptionValue → skill_parry |
| Enabled | Включено | MenuDef → OptionValue → skill_parry |
| Mouse1: Use Item \| Mouse2: Options | ЛКМ: использовать \| ПКМ: настройки | MenuDef → OptionValue → InvClickSwap |
| Mouse1: Options \| Mouse2: Use Item | ЛКМ: настройки \| ПКМ: использовать | MenuDef → OptionValue → InvClickSwap |

## 9. Описания настроек (`Language.RU`)

| Ключ | Что было (EN) | Что стало (RU) |
|---|---|---|
| DESC_FULLSCREEN | Chooses between windowed and fullscreen mode. | Выбор между оконным и полноэкранным режимом. |
| DESC_RESPRESET | Chooses from a list of resolution presets. | Выбор из списка готовых разрешений. |
| DESC_CUSTOMX | Enter a custom width for the game's resolution. | Введите желаемую ширину разрешения. |
| DESC_CUSTOMY | Enter a custom height for the game's resolution. | Введите желаемую высоту разрешения. |
| DESC_VSYNC | Worsen performance, but does improve it in some very rare case. | Ухудшает производительность, но в редких случаях может улучшить. |
| DESC_MAXFPS | Controls the framerate cap. | Ограничение частоты кадров. |
| DESC_FORCEASPECT | Forces the chosen screen resolution to be considered as the selected aspect ratio, rather than the actual ratio. | Считать выбранное разрешение заданным соотношением сторон, а не фактическим. |
| DESC_FORCERATIOSTYLE | Controls whether or not the screen should stretch to a chosen aspect ratio or be letterboxed. | Растягивать изображение под выбранное соотношение сторон или добавлять чёрные полосы. |
| DESC_SCALEFACTOR | Controls the size of the HUD | Размер HUD. |
| DESC_CROSSHAIRSCALE | Controls the size of the crosshair | Размер прицела. |
| DESC_PRECACHE | WARNING: Less suttering but longer loading time. (Slightly more likely to crash - maybe) | ВНИМАНИЕ: меньше подтормаживаний, но дольше загрузка. (Чуть выше шанс вылета — возможно) |
| DESC_VHS | Controls the intensity of the VHS shader. | Интенсивность VHS-шейдера. |
| DESC_VHSTear | Controls the screen tearing FX of the VHS shader. | Эффект разрыва изображения VHS. |
| DESC_BLOOM | Controls whether or not lights give off a powerful glow. | Включает мощное свечение источников света. |
| DESC_SSAO | Controls the quality of ambient occlusion | Качество ambient occlusion. |
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
| DESC_BACKGROUND | Controls whether or not to let the sound and music to continue playing in the background if the program's window loses focus. | Продолжать звук и музыку, когда окно игры не в фокусе. |
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
| dialoguefont: уже с кириллицей | Не менялся | Fonts/dialoguefont/ |
| npcfont, DF_FONT, CONVO_FONT, ChatBoxFont | Не менялись; кириллицы пока нет | Вне текущего объёма |

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
| Титульный экран: [Press any button] | [Нажмите любую кнопку] |

### Новые меню настроек

| Было | Стало | Где используется |
|---|---|---|
| DFDisplayOptions (protected) | RU_DFDisplayOptions | TabTest → Графика |
| DFKeyBinds (protected) | RU_DFKeyBinds | TabTest → Управление |
| DFSoundOptions (protected) | RU_DFSoundOptions | TabTest → Звук |
| DFAdvancedOptions (protected) | RU_DFAdvancedOptions | TabTest → Доступность |
| NewJoystickOptions (protected) | RU_NewJoystickOptions | RU_DFAdvancedOptions → Субменю джойстика |

## 14. Что не переведено в этой итерации

| Раздел | Статус |
|---|---|
| HUD, инвентарь, кодекс | DF_FONT / ChatBoxFont; кириллица не добавлена |
| Имена NPC | npcfont; кириллица не добавлена |
| Сюжетный текст | Language.Items, Language.Weapon, Language.Upgrade, Language.Map, Language.NPC* |
| ACS и диалоги карт | ACS/*.acs, SCRIPTS/BEHAVIOR, DIALOGUE |
| Озвучка | Остаётся английской; перевод текстовый |

## 15. Запуск

- `test/run_test.cmd` или ярлык **Divine Frequency (RU)** — полный экран, `language=ru`.
- `test/run_original.cmd` или ярлык **Divine Frequency (Original)** — полный экран, `language=enu`.
- Конфиги: `test/dfconfig-test.ini` и `test/dfconfig-original.ini`; основной `dfconfig.ini` не изменяется.

Проверка сборки: запуск с `-stdout` — ZScript компилируется, ошибок нет. Визуальная проверка — за тобой.
