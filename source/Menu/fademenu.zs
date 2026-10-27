class FadeMenu : ListMenu
{
    const FADE_TIME = 250.0; // ms

    protected MenuAnimation fade;
    protected bool bClosing, bFading;
    protected double prevTime;

    override bool MenuEvent(int mKey, bool fromController)
	{
        if (bClosing || bFading)
            return true;
		
        if (gameState == GS_LEVEL && mKey == MKEY_Back)
        {
			if(Screen.GetWidth() >= 3840)
		    {
				let uis = CVar.FindCVar("vid_scalefactor");
				if(uis)
					uis.SetFloat(0.5);
			}
	  
            bClosing = true;
            mDesc.mSelectedItem = -1;
            MenuSound("menu/clear");
			EventHandler.SendNetworkEvent("UpdateKeys");
            return true;
        }

		return super.MenuEvent(mKey, fromController);
	}

    override bool OnUIEvent(UIEvent ev)
    {
        if (bClosing || bFading)
            return true;

        return super.OnUIEvent(ev);
    }

    override bool OnInputEvent(InputEvent ev)
    {
        if (bClosing || bFading)
            return true;

        return super.OnInputEvent(ev);
    }

    override void Drawer()
    {
        double curTime = MSTimeF();
        if (prevTime <= 0.0)
            prevTime = curTime;

        double delta = curTime - prevTime;
        prevTime = curTime;

        // Only fade when actually in game.
        if (gameState != GS_LEVEL)
        {
            super.Drawer();
            return;
        }

        let handler = MenuHandler.Get();
        if (bClosing)
        {
            if (handler.IsFadedOut())
            {
                Close();
                if (!GetCurrentMenu())
                    menuDelegate.MenuDismissed();
            }
            else if (handler.IsFadedIn())
            {
                if (fade)
                {
                    if (fade.HasFinishedAnimating())
                        fade.StartAnimationOut(FADE_TIME);

                    fade.CheckAnimation(delta);
                }

                if (!fade || fade.HasNoAnimation())
                    handler.StartFadeOut(FADE_TIME);
                else
                    super.Drawer();
            }
        }
        else
        {
            if (handler.IsFadedOut())
            {
                bFading = true;
                handler.StartFadeIn(FADE_TIME);
            }
            else if (handler.IsFadedIn())
            {
                if (!fade)
                    fade = new("MenuAnimation");

                super.Drawer();

                if (fade.HasNoAnimation())
                    fade.StartAnimationIn(FADE_TIME);
                else if (fade.HasFinishedAnimating())
                    bFading = false;

                fade.CheckAnimation(delta);
            }
        }

        if (fade && !fade.HasNoAnimation())
            Screen.Dim(0, 1.0 - fade.GetFraction(), 0, 0, Screen.GetWidth(), Screen.GetHeight());
    }
}
