mixin class Highlight
{
    const HIGHLIGHT_TIME = 100.0; // ms

    private MenuAnimation highlight;
    private double prevTime;
    private bool bSelected;

    int, int, int, int ScaleBox(int xPos, int yPos, int xSize, int ySize, int vWidth, int vHeight)
    {
        int x, y, xs, ys;
        if (vWidth == ListMenuDescriptor.CleanScale)
        {
            x = (xPos - 160) * cleanXFac + Screen.GetWidth()/2;
            y = (yPos - 100) * cleanYFac + Screen.GetHeight()/2;
            xs = xSize * cleanXFac;
            ys = ySize * cleanYFac;
        }
        else
        {
            Vector2 pos, size;
            [pos.x, pos.y, size.x, size.y] = Screen.GetFullscreenRect(vWidth, vHeight, FSMode_ScaletoFit43);

            x = int(pos.x + xPos * size.x/vWidth);
            y = int(pos.y + yPos * size.y/vHeight);
            xs = int(xSize * size.x/vWidth);
            ys = int(ySize * size.y/vHeight);
        }

        return x, y, xs, ys;
    }

    protected void PlaySelectSound(bool selected)
    {
        if (!bSelected && selected)
            Menu.MenuSound("menu/clear");

        bSelected = selected;
    }

    protected void DrawHighlight(int x, int y, int vw, int vh, string text, int fntHeight, Font fnt, bool fadeIn, bool list = true)
    {
        double curTime = MSTimeF();
        if (prevTime <= 0.0)
            prevTime = curTime;

        double delta = curTime - prevTime;
        prevTime = curTime;

        if (!fadeIn && (!highlight || highlight.HasNoAnimation()))
            return;

        if (!highlight)
            highlight = new("MenuAnimation");

        if (fadeIn)
            highlight.StartAnimationIn(HIGHLIGHT_TIME);
        else
            highlight.StartAnimationOut(HIGHLIGHT_TIME);

        highlight.CheckAnimation(delta);

        int xPos, yPos, xSize, ySize;
        if (list)
        {
            [xPos, yPos, xSize, ySize] = ScaleBox(x, y, fnt.StringWidth(text), fntHeight, vw, vh);
            //size.x += double(vw) / Screen.GetWidth() * 0.5 * highlight.GetFraction();
        }
        else
        {
            xPos = x;
            yPos = y;
            xSize = (fnt.StringWidth(text) + 14) * cleanXFac_1;
            ySize = fntHeight * cleanYFac_1;
        }
        
        Screen.Dim(Color(48, 50, 60), 0.5, xPos, yPos, xSize, ySize);
    }
}

class ListMenuItemHighlightTextItem : ListMenuItemTextItem
{
    mixin Highlight;

    override void Draw(bool selected, ListMenuDescriptor desc)
	{
		let font = menuDelegate.PickFont(mFont);

        PlaySelectSound(selected);
        DrawHighlight(int(mXPos), int(mYPos), desc.DisplayWidth(), desc.DisplayHeight(), mText, desc.mLineSpacing, font, selected);
		DrawText(desc, font, selected ? mColorSelected : mColor, mXpos, mYpos, mText);
	}
}

class OptionMenuItemHighlightOption : OptionMenuItemOption
{
    mixin Highlight;

    override int Draw(OptionMenuDescriptor desc, int y, int indent, bool selected)
	{
		if (mCenter)
			indent = (Screen.GetWidth() / 2);

		DrawLabel(indent, y, selected ? OptionMenuSettings.mFontColorSelection : OptionMenuSettings.mFontColor, IsGrayed());

		int selection = GetSelection();
		String text = StringTable.Localize(OptionValues.GetText(mValues, Selection));
		if (!text.Length())
            text = StringTable.Localize("$TXT_UNKNOWN");

        PlaySelectSound(selected);
        DrawHighlight(indent, y, -1, -1, text, Menu.OptionHeight(), Menu.OptionFont(), selected, false);
		DrawValue(indent, y, OptionMenuSettings.mFontColorValue, text, IsGrayed());
		return indent;
	}
}
