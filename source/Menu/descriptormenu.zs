class DescriptorMenu : OptionMenu
{
    const V_WIDTH = 640;

    const DESC_PADDING = 10;
    const DESC_WIDTH = V_WIDTH - DESC_PADDING*2;
    const DESC_LINES = 2;
    const DESC_SCROLL_SPEED = 0.5; // Lines per second
    const DESC_SCROLL_TIME = 3000.0; // Milliseconds
    const MS_TO_SECONDS = 1.0 / 1000.0;

    private OptionMenuItemDescriptionFont descFont;
    private Array<OptionMenuItemDescription> descriptions;
    private double scrollTimer;
    private double scrollOfs;
    private int curSelected;
	TextureID menu_arrow, menu_arrow_bg;
	double arrow_alpha;

    protected double delta, prevTime;

    override void Init(Menu parent, OptionMenuDescriptor desc)
    {
        super.Init(parent, desc);
		
		DontBlur = true;
		DontDim = true;
		menu_arrow = TexMan.CheckForTexture("MenuArow");
		menu_arrow_bg = TexMan.CheckForTexture("MenuARBG");
		
        // To prevent improper handling, temporarily remove these elements from the item list.
        for (int i = desc.mItems.Size()-1; i >= 0; --i)
        {
            let d = OptionMenuItemDescription(desc.mItems[i]);
            if (d)
            {
                if (d.IsValid())
                    descriptions.Push(d);
            }
            else
            {
                let f = OptionMenuItemDescriptionFont(desc.mItems[i]);
                if (f)
                    descFont = f;
            }
        }
    }
	
	override void Ticker()
	{
		Super.Ticker();
		
		if(arrow_alpha <= 0.0)
			arrow_alpha = 1.0;
		else
			arrow_alpha -= 0.05;
	}

    override bool MouseEvent(int type, int x, int y)
	{
		y = (y / cleanYFac_1) - mDesc.mDrawTop;

		if (mFocusControl)
		{
			mFocusControl.MouseEvent(type, x, y);
			return true;
		}
		else
		{
			int yLine = (y / optionMenuSettings.mLinespacing);
			if (yLine >= mDesc.mScrollTop)
				yLine += mDesc.mScrollPos;

			if (yLine >= 0)
			{
                for (int i = 0; i <= yLine && i < mDesc.mItems.Size(); ++i)
                {
                    if (i == mDesc.mScrollTop)
                    {
                        i += mDesc.mScrollPos;
                        if (i >= mDesc.mItems.Size())
                            break;
                    }
                    
                    if (ShouldSkip(mDesc.mItems[i]))
                        ++yLine;
                }

                if (yLine < mDesc.mItems.Size() && mDesc.mItems[yLine].Selectable())
                {
                    if (yLine != mDesc.mSelectedItem)
                        mDesc.mSelectedItem = yLine;

                    mDesc.mItems[yLine].MouseEvent(type, x, y);
                    return true;
                }
			}
		}

		mDesc.mSelectedItem = -1;
		return Menu.MouseEvent(type, x, y);
	}

    Font, int GetDescriptionFont() const
    {
        Font fnt;
        int t;
        if (descFont)
        {
            [fnt, t] = descFont.GetFont();
        }
        else
        {
            fnt = OptionFont();
            t = Font.CR_NATIVEPAL;
        }

        return fnt, t;
    }

    override void Drawer()
    {
        double curTime = MSTimeF();
        if (!prevTime)
            prevTime = curTime;

        delta = curTime - prevTime;
        prevTime = curTime;

        int y = mDesc.mPosition;
		if (y <= 0)
			y = DrawCaption(mDesc.mTitle, -y, true);

		mDesc.mDrawTop = y / cleanYfac_1; // Mouse checks are done in clean space.

        DrawDescription();

		int fontHeight = optionMenuSettings.mLinespacing * cleanYfac_1;
		int indent = GetIndent();
		int yTop = y + -16*cleanYfac_1;
		int lastRow = Screen.GetHeight() - OptionHeight()*4*cleanYfac_1;

		int i;
		for (; i < mDesc.mItems.Size() && y <= lastRow; ++i, y += fontHeight)
		{
			// Don't scroll the uppermost items.
			if (i == mDesc.mScrollTop)
			{
				i += mDesc.mScrollPos;
				if (i >= mDesc.mItems.Size())
                    break;	// Skipped beyond end of menu.
			}

            if (ShouldSkip(mDesc.mItems[i]))
            {
                y -= fontHeight;
                continue;
            }

			bool isSelected = mDesc.mSelectedItem == i;
			int curIndent = mDesc.mItems[i].Draw(mDesc, y, indent, isSelected);
			if (curIndent >= 0 && isSelected && mDesc.mItems[i].Selectable()
                && ((MenuTime() % 8) < 6 || GetCurrentMenu() != self))
			{
				DrawOptionText(curIndent + 3*cleanXfac_1, y, optionMenuSettings.mFontColorSelection, "◄");
			}
		}

		canScrollUp = (mDesc.mScrollPos > 0);
		canScrollDown = (i < mDesc.mItems.Size());
		visBottom = i - 1;

		if (canScrollUp)
		{
			Screen.DrawTexture(menu_arrow_bg, false, Screen.GetWidth() * 0.5, yTop, DTA_FlipY, true);
			Screen.DrawTexture(menu_arrow, false, Screen.GetWidth() * 0.5, yTop, 
			DTA_Alpha, arrow_alpha,
			DTA_FlipY, true);
		}
		if (canScrollDown)
		{
			Screen.DrawTexture(menu_arrow_bg, false, Screen.GetWidth() * 0.5, Screen.GetHeight() - 20*cleanYFac_1);
			Screen.DrawTexture(menu_arrow, false, Screen.GetWidth() * 0.5, Screen.GetHeight() - 20*cleanYFac_1, 
			DTA_Alpha, arrow_alpha);
		}
        Menu.Drawer();
    }

    virtual void DrawDescription()
    {
        if (mDesc.mSelectedItem != curSelected)
            ResetScroll();

        if (mDesc.mSelectedItem < 0 || !descriptions.Size())
            return;

        OptionMenuItemDescription selected;
        foreach (d : descriptions)
        {
            if (d.IsSelected(mDesc.mItems[mDesc.mSelectedItem]))
            {
                selected = d;
                break;
            }
        }

        if (!selected)
            return;

        curSelected = mDesc.mSelectedItem;

        // Draw the description if it has one.
        string description = selected.GetDescription();
        if (description.Length())
        {
            let [fnt, translation] = GetDescriptionFont();
            int fh = fnt.GetHeight() * cleanYFac_1;
            BrokenLines lines = fnt.BreakLines(description, DESC_WIDTH);

            int bottom = Screen.GetHeight() - DESC_PADDING*cleanYFac_1;
            int top = bottom - fh*DESC_LINES;
            int middle = Screen.GetWidth() / 2;

            let [cXOfs, cYOfs, cw, ch] = Screen.GetClipRect();
            Screen.SetClipRect(middle - DESC_WIDTH/2*cleanXFac_1, top, DESC_WIDTH*cleanXFac_1, bottom - top);
            
            let [y, startLine] = CheckScrollPosition(bottom, top, fh, lines.Count());
            int endLine = min(startLine + DESC_LINES + (y < top ? 1 : 0), lines.Count());
            double strMod = 0.5 * cleanXFac_1;
            for (int i = startLine; i < endLine; ++i, y += fh)
            {
                int x = int(middle - lines.StringWidth(i)*strMod);
                Screen.DrawText(fnt, FONT.CR_GRAY, x, y, lines.StringAt(i), DTA_CleanNoMove_1, true);
            }

            Screen.SetClipRect(cXOfs, cYOfs, cw, ch);
        }
    }

    bool ShouldSkip(OptionMenuItem item)
    {
        return item is "OptionMenuItemDescription" || item is "OptionMenuItemDescriptionFont";
    }

    protected int, int CheckScrollPosition(int bottom, int top, int fontHeight, int lines)
    {
        if (lines <= DESC_LINES)
        {
            ResetScroll();
            return top, 0;
        }

        // Only offset the first visible line on the top
        double scrollTopOfs = scrollOfs - floor(scrollOfs);
        int newTop = top - int(scrollTopOfs * fontHeight);

        // If idling, don't scroll
        if (scrollTimer > 0.0)
        {
            int startLine = int(scrollOfs);

            scrollTimer -= delta;
            if (scrollTimer <= 0.0 && scrollOfs)
                ResetScroll();

            return newTop, startLine;
        }

        // Scroll up
        double totalLineOfs = lines - DESC_LINES;
        scrollOfs += DESC_SCROLL_SPEED * delta * MS_TO_SECONDS;
        if (scrollOfs >= totalLineOfs)
        {
            newTop = top;
            scrollOfs = totalLineOfs;
            scrollTimer = DESC_SCROLL_TIME;
        }
        else
        {
            scrollTopOfs = scrollOfs - floor(scrollOfs);
            newTop = top - int(scrollTopOfs * fontHeight);
        }
        
        return newTop, int(scrollOfs);
    }

    protected void ResetScroll()
    {
        scrollOfs = 0.0;
        scrollTimer = DESC_SCROLL_TIME;
    }
}

class OptionMenuItemDescription : OptionMenuItem
{
    private string description;
    private OptionMenuItem option;

    void Init(OptionMenuDescriptor desc, string d)
    {
        // Get the option menu item to tie it to (previous in the list).
        int i = desc.mItems.Size()-1;
        if (i >= 0)
            option = desc.mItems[i];

        if (option)
            description = d;
    }

    bool IsValid() const
    {
        return option != null;
    }

    bool IsSelected(OptionMenuItem selected) const
    {
        return selected == option;
    }

    string GetDescription() const
    {
        return option ? StringTable.Localize(description) : "";
    }

    override bool Selectable()
    {
        return false;
    }
}

class OptionMenuItemDescriptionFont : OptionMenuItem
{
    private Font fnt;
    private int translation;

    void Init(Font f, int t = Font.CR_NATIVEPAL)
    {
        fnt = f;
        translation = t;
    }

    Font, int GetFont() const
    {
        return fnt, translation;
    }

    override bool Selectable()
    {
        return false;
    }
}