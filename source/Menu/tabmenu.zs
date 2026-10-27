class MenuTransition ui
{
    private MenuAnimation animator;
    private OptionMenu cur, next;
    private bool bNext;

    void TransitionTo(OptionMenu from, OptionMenu to, bool goNext, double time = 150.0)
    {
        if (!animator)
            animator = new("MenuAnimation");

        animator.Clear();
        cur = from;
        next = to;
        bNext = goNext;
		Menu.MenuSound("menu/clear");

        animator.StartAnimationIn(time);
    }

    bool UpdateTransition(double delta, int yOfs = 0)
    {
        if (!IsTransitioning())
            return true;

        animator.CheckAnimation(delta);
        if (animator.HasFinishedAnimating())
        {
            cur.Destroy();
            return true;
        }

        int width = Screen.GetWidth();
        int shift = int(width * animator.GetFraction());

        Vector2 ofs = Screen.SetOffset(bNext ? -shift : shift, 0.0);
        int curOfs = cur.mDesc.mPosition;
        cur.mDesc.mPosition = yOfs + abs(curOfs); // Make sure to get rid of the caption.
        cur.Drawer();
        cur.mDesc.mPosition = curOfs;

        Screen.SetOffset(bNext ? width - shift : -width + shift, 0.0);
        curOfs = next.mDesc.mPosition;
        next.mDesc.mPosition = yOfs + abs(curOfs); // Make sure to get rid of the caption.
        next.Drawer();
        next.mDesc.mPosition = curOfs;

        Screen.SetOffset(ofs.x, ofs.y);
        return false;
    }

    bool IsTransitioning() const
    {
        return animator && animator.IsAnimating();
    }
}

class TabMenu : OptionMenu
{
    enum ETabMenuMouse
    {
        MOUSE_InTabs = MOUSE_Release + 1,
        MOUSE_TabClicked
    }

    // Assumes a virtual width of 640.
    const DEF_MENU_WIDTH = 640;
    const DEF_PADDING = 4;

    const BUTTON_BOX_SIZE = 26;
    const BUTTON_PADDING = DEF_PADDING;
    const BUTTON_SIZE = BUTTON_BOX_SIZE - BUTTON_PADDING;

    const TAB_BAR_WIDTH = DEF_MENU_WIDTH - BUTTON_BOX_SIZE*2;
    const DEF_TAB_WIDTH = TAB_BAR_WIDTH / 5;
    const DEF_TAB_HEIGHT = 50;

    private int tabSize;
    private int prevButton, nextButton;
    private Array<int> tabs;
    private int selectedTab;
    private int hovering;

    private bool bController;
    private OptionMenu curMenu;
    private MenuTransition trans;

    protected double prevTime;

    void SetSubmenu(int tab)
    {
        if (tab < 0)
        {
            selectedTab = -1;
            if (curMenu)
                curMenu.Destroy();

            return;
        }

        let desc = OptionMenuDescriptor(MenuDescriptor.GetDescriptor(OptionMenuItemTab(mDesc.mItems[tabs[tab]]).GetAction()));
        class<Menu> cls = desc.mClass ? desc.mClass : (class<Menu>)("OptionMenu"); // TODO: Get default class?
        let newMenu = OptionMenu(new(cls));
        newMenu.Init(mParentMenu, desc);
        newMenu.mDesc.mSelectedItem = -1;
        newMenu.mDesc.mScrollPos = 0;
        
        if (curMenu && curMenu.mDesc.mAnimatedTransition && newMenu && newMenu.mDesc.mAnimatedTransition)
            trans.TransitionTo(curMenu, newMenu, tab > selectedTab);
        else if (curMenu)
            curMenu.Destroy();
        
        curMenu = newMenu;
        selectedTab = tab;
    }

    void CycleSubmenu(bool prev = false)
    {
        int nextTab;
        if (selectedTab < 0)
        {
            if (!tabs.Size())
                return;
        }
        else if (prev)
        {
            nextTab = selectedTab - 1;
            if (nextTab < 0)
                nextTab = tabs.Size()-1;
        }
        else
        {
            nextTab = selectedTab + 1;
            if (nextTab >= tabs.Size())
                nextTab = 0;
        }

        if (nextTab != selectedTab)
            SetSubmenu(nextTab);
    }

    int, int GetTabSize() const
    {
        int width, height;
        if (tabSize >= 0)
            [width, height] = OptionMenuItemTabSize(mDesc.mItems[tabSize]).GetSize();

        if (width <= 0)
            width = DEF_TAB_WIDTH;
        if (height <= 0)
            height = DEF_TAB_HEIGHT;

        return width * cleanXFac_1, height * cleanYFac_1;
    }

    int GetTabPadding() const
    {
        int p;
        if (tabSize >= 0)
            p = OptionMenuItemTabSize(mDesc.mItems[tabSize]).GetPadding();

        if (p <= 0)
            p = DEF_PADDING;

        return p * cleanYFac_1;
    }

    // Second return value is how many tabs are in each row.
    int, int GetRows() const
    {
        int width = GetTabSize();
        int tabs = tabs.Size();
        int tabBarW = TAB_BAR_WIDTH * cleanXFac_1;

        int rows = int(ceil(double(tabs * width) / tabBarW));
        if (rows > 1)
            tabs = max(1, tabBarW / width);

        return rows, tabs;
    }

    // Check if the mouse is within the tab bar's bounding box.
    bool InTabBar(int mouseX, int mouseY) const
    {
        let [temp, height] = GetTabSize();
        int rows = GetRows();

        int middle = Screen.GetWidth() / 2;
        int tabBarW = TAB_BAR_WIDTH*cleanXFac_1 / 2;
        return mouseY >= 0 && mouseY <= rows*height
                && mouseX >= middle-tabBarW && mouseX <= middle+tabBarW;
    }

    override void Init(Menu parent, OptionMenuDescriptor desc)
    {
        super.Init(parent, desc);

        trans = new("MenuTransition");
		DontBlur = true;
		DontDim = true;

        // Some properties are defined as menu items to give greater customizability.
        desc.mSelectedItem = tabSize = prevButton = nextButton = selectedTab = hovering = -1;
        for (int i = 0; i < desc.mItems.Size(); ++i)
        {
            let s = OptionMenuItemTabSize(desc.mItems[i]);
            if (s)
            {
                tabSize = i;
                continue;
            }

            let t = OptionMenuItemTab(desc.mItems[i]);
            if (t)
            {
                let optDesc = OptionMenuDescriptor(MenuDescriptor.GetDescriptor(t.GetAction()));
                if (optDesc)
                {
                    int end = tabs.Push(i);
                    t.header = self;
                    if (selectedTab < 0)
                        SetSubmenu(end);
                }

                continue;
            }

            let tb = OptionMenuItemTabButton(desc.mItems[i]);
            if (tb)
            {
                if (tb.IsNext())
                    nextButton = i;
                else
                    prevButton = i;

                continue;
            }
        }
    }

    override void Ticker()
    {
        super.Ticker();
        if (curMenu)
            curMenu.Ticker();
    }

    override void Drawer()
    {
		Screen.Dim(Color(0,0,0), 1.0, 0, 0, screen.GetWidth(), screen.GetHeight());
		
        double curTime = MSTimeF();
        if (prevTime <= 0.0)
            prevTime = curTime;

        double delta = curTime - prevTime;
        prevTime = curTime;

        int startY = DrawTabs();
        if (curMenu)
        {
            if (!trans.UpdateTransition(delta, startY))
                return;

            int curOfs = curMenu.mDesc.mPosition;
            curMenu.mDesc.mPosition = startY + abs(curOfs); // Make sure to get rid of the caption.
            if (!trans.IsTransitioning())
                curMenu.Drawer();
            curMenu.mDesc.mPosition = curOfs;
        }
        else
        {
            super.Drawer();
        }
    }

    override bool MenuEvent(int mKey, bool fromController)
    {
        // All controller inputs are converted into their corresponding keyboard keys before being passed.
        bController = fromController;
        if (mKey == MKEY_PageDown || mKey == MKEY_PageUp)
        {
            CycleSubmenu(fromController ? mKey == MKEY_PageUp : mKey == MKEY_PageDown);
            return true;
        }

        if (curMenu)
            return curMenu.MenuEvent(mKey, fromController);

        return super.MenuEvent(mKey, fromController);
    }

    override bool OnUIEvent(UIEvent ev)
    {
        // These events can only be triggered by the keyboard.
        if (ev.type > UIEvent.Type_None)
            bController = false;

        // Check if the mouse is within the tab section.
        if ((ev.type == UIEvent.Type_MouseMove && tabs.Size())
            || (ev.type == UIEvent.Type_LButtonDown && hovering >= 0))
        {
            int type = MOUSE_TabClicked;
            if (ev.type == UIEvent.Type_MouseMove)
            {
                type = MOUSE_InTabs;
                hovering = -1;
                if (curMenu)
                    curMenu.mDesc.mSelectedItem = -1;
            }

            int realY = ev.mouseY - abs(mDesc.mPosition)*cleanYFac_1;
            if (InTabBar(ev.mouseX, realY))
            {
                MouseEvent(type, ev.mouseX, realY);
                return true;
            }
        }

        if (curMenu)
            return curMenu.OnUIEvent(ev);

        return super.OnUIEvent(ev);
    }

    override bool OnInputEvent(InputEvent ev)
    {
        // Check if a controller button was pressed. If not, check if it was a keyboard press.
        if (ev.keyScan >= InputEvent.Key_Pad_LThumb_Right && ev.keyScan < InputEvent.Num_Keys)
            bController = true;
        else if (ev.type > InputEvent.Type_None && ev.type < InputEvent.Type_GUI)
            bController = false;

        if (curMenu)
            return curMenu.OnInputEvent(ev);

        return super.OnInputEvent(ev);
    }

    override bool MouseEvent(int type, int mx, int my)
    {
        if (type == MOUSE_InTabs)
        {
            let [width, height] = GetTabSize();
            let [rows, tabsPerRow] = GetRows();

            // Find out which row the mouse is in.
            int tabCount = tabsPerRow;
            int row = int(rows * double(my) / (rows*height));
            if (row >= rows-1)
            {
                row = rows-1;
                tabCount = tabs.Size() - tabsPerRow*(rows-1);
            }

            // Find the exact tab in the row.
            int totalWidth = tabCount * width;
            int relX = mx - (Screen.GetWidth()/2 - totalWidth/2);
            if (relX >= 0 && relX <= totalWidth)
            {
                int tab = min(int(tabCount * double(relX) / totalWidth), tabCount-1);
                hovering = row*tabsPerRow + tab;
                return true;
            }

            return super.MouseEvent(type, mx, my);
        }
        else if (type == MOUSE_TabClicked)
        {
            if (hovering != selectedTab)
                SetSubmenu(hovering);

            return true;
        }

        if (curMenu)
            return curMenu.MouseEvent(type, mx, my);

        return super.MouseEvent(type, mx, my);
    }

    override bool TranslateKeyboardEvents()
    {
        if (curMenu)
            return curMenu.TranslateKeyboardEvents();

        return super.TranslateKeyboardEvents();
    }

    virtual int DrawTabs()
    {
        // Get the vertical indent for the tab menu getting drawn.
        let [width, height] = GetTabSize();
        let [rows, tabsPerRow] = GetRows();

        int totalHeight = height * rows;
        int yOfs = abs(mDesc.mPosition) * cleanYFac_1;
        int startY = yOfs + totalHeight;

        // Draw the next and previous tab buttons, centered in the middle of the rows.
        int buttonY = yOfs + totalHeight/2 - BUTTON_BOX_SIZE*cleanYFac_1/2;
        if (prevButton >= 0)
            OptionMenuItemTabButton(mDesc.mItems[prevButton]).DrawButton(buttonY, bController);

        if (nextButton >= 0)
            OptionMenuItemTabButton(mDesc.mItems[nextButton]).DrawButton(buttonY, bController);

        int halfW = width / 2;
        int halfH = height / 2;

        int middle = Screen.GetWidth()/2;
        int curY = yOfs;
        int curX;
        int startTab;
        // Start by drawing filled out rows.
        if (rows > 1)
        {
            int startX = middle - (tabsPerRow*width)/2;
            curX = startX;
            startTab = tabsPerRow*(rows-1);
            for (int i, curTab; i < startTab; ++i, ++curTab, curX += width)
            {
                if (curTab >= tabsPerRow)
                {
                    curTab = 0;
                    curY += height;
                    curX = startX;
                }

                OptionMenuItemTab(mDesc.mItems[tabs[i]]).DrawLabel(curX, curY, mDesc.mFont,
                                    i == selectedTab || i == hovering ? optionMenuSettings.mFontColorSelection : -1);
            }

            curY += height;
        }

        // Draw the final row.
        curX = middle - ((tabs.Size()-startTab)*width)/2;
        for (int i = startTab; i < tabs.Size(); ++i, curX += width)
        {
            OptionMenuItemTab(mDesc.mItems[tabs[i]]).DrawLabel(curX, curY, mDesc.mFont,
                                i == selectedTab || i == hovering ? optionMenuSettings.mFontColorSelection : -1);
        }

        return startY;
    }

    OptionMenu GetSubmenu() const
    {
        return curMenu;
    }
}

class OptionMenuItemTab : OptionMenuItem
{
    TabMenu header;

    protected string tabLabel;

    void Init(Name submenu, string label)
    {
        mAction = submenu;
        tabLabel = label;
    }

    virtual void DrawLabel(int x, int y, Font fnt, int fontTranslation = Font.CR_NATIVEPAL)
    {
        if (!header || !tabLabel.Length())
            return;

        let [width, height] = header.GetTabSize();
        int padding = header.GetTabPadding();

        // Remove the padding from around the edges to get the real dimensions.
        width -= (padding<<1);
        height -= (padding<<1);

        // Break the label down to fit into the tab area.
        string label = StringTable.Localize(tabLabel);
        int realW = width / cleanXFac_1;
        BrokenLines lines = fnt.BreakLines(label, realW);

        int fh = fnt.GetHeight() * cleanYFac_1;
        double scale = min(1.0, height / double(fh * lines.Count()));
        if (scale < 1.0)
        {
            // Outside of the tab box, so rescale it.
            scale = 0.75;
            lines = fnt.BreakLines(label, int(realW / scale));
        }

        fh = int(fh*scale);
        int yPos = y + padding + height/2 - fh*lines.Count()/2;
        int centerX = x + padding + width/2;
        Vector2 scalars = (cleanXFac_1, cleanYFac_1) * scale;
        double strMod = scalars.x * 0.5;
        for (int i = 0; i < lines.Count(); ++i, yPos += fh)
        {
            int xPos = int(centerX - lines.StringWidth(i)*strMod);
            Screen.DrawText(fnt, fontTranslation, xPos, yPos, lines.StringAt(i),
                            DTA_ScaleX, scalars.x, DTA_ScaleY, scalars.y);
        }
    }
}

class OptionMenuItemTabButton : OptionMenuItem
{
    private TextureID keyboard, controller;
    private bool nextButton;

    void Init(TextureID kb, TextureID con, bool next = false)
    {
        keyboard = kb;
        controller = con;
        nextButton = next;
    }

    virtual void DrawButton(int y = 0, bool fromController = false)
    {
        TextureID tex = fromController ? controller : keyboard;
        if (!tex.IsValid())
            return;

        int halfTab = TabMenu.TAB_BAR_WIDTH*cleanXFac_1 / 2;
        int x = Screen.GetWidth() / 2;
        if (nextButton)
            x += halfTab;
        else
            x -= (halfTab + TabMenu.BUTTON_BOX_SIZE*cleanXFac_1);

        Screen.DrawTexture(tex, true,
                            x + TabMenu.BUTTON_PADDING*cleanXFac_1,
                            y + TabMenu.BUTTON_PADDING*cleanYFac_1,
                            DTA_TopLeft, true,
                            DTA_DestWidth, TabMenu.BUTTON_SIZE * cleanXFac_1,
                            DTA_DestHeight, TabMenu.BUTTON_SIZE * cleanYFac_1);
    }

    bool IsNext() const
    {
        return nextButton;
    }

    override bool Selectable()
    {
        return false;
    }
}

class OptionMenuItemTabSize : OptionMenuItem
{
    private int width, height;
    private int padding;

    void Init(int w, int h = 0, int p = 0)
    {
        width = w;
        height = h;
        padding = p;
    }

    int, int GetSize() const
    {
        return width, height;
    }

    int, int GetPadding() const
    {
        return padding, padding;
    }

    override bool Selectable()
    {
        return false;
    }
}
