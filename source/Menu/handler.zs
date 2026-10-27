class MenuAnimation ui
{
    enum EAnimationState : uint8
    {
        ANIM_NONE,
        ANIM_IN,
        ANIM_DONE,
        ANIM_OUT
    }

    private EAnimationState animState;
    private double baseTime, timer;
    private double fraction;

    static MenuAnimation Create(double dur)
    {
        let ma = new("MenuAnimation");
        ma.StartAnimationIn(dur);

        return ma;
    }

    void StartAnimationIn(double dur)
    {
        if (timer >= dur)
            return;

        animState = ANIM_IN;
        baseTime = dur;
        if (timer < 0.0)
            timer = 0.0;
    }

    void StartAnimationOut(double dur)
    {
        if (timer <= 0.0)
            return;

        animState = ANIM_OUT;
        baseTime = dur;
        if (timer > baseTime)
            timer = baseTime;
    }

    void CheckAnimation(double delta)
    {
        if (animState == ANIM_IN)
        {
            timer += delta;
            fraction = clamp(timer / baseTime, 0.0, 1.0);
            if (fraction >= 1.0)
                animState = ANIM_DONE;
        }
        else if (animState == ANIM_OUT)
        {
            timer -= delta;
            fraction = clamp(timer / baseTime, 0.0, 1.0);
            if (fraction <= 0.0)
                animState = ANIM_NONE;
        }
    }

    void Clear()
    {
        animState = ANIM_NONE;
        fraction = 0.0;
        baseTime = timer = 0.0;
    }

    double GetFraction() const
    {
        return fraction;
    }

    bool IsAnimating() const
    {
        return animState == ANIM_IN || animState == ANIM_OUT;
    }

    bool HasNoAnimation() const
    {
        return animState == ANIM_NONE;
    }

    bool HasFinishedAnimating() const
    {
        return animState == ANIM_DONE;
    }
}

class MenuHandler : StaticEventHandler
{
    // Menu fading.
    private ui MenuAnimation backgroundFade;

    // For delta tracking.
    protected ui double prevTime;

    static ui MenuHandler Get()
    {
        return MenuHandler(StaticEventHandler.Find("MenuHandler"));
    }

    override void UITick()
    {
        if (menuActive == Menu.Off)
            ResetMenu();
    }

    protected ui void ResetMenu()
    {
        prevTime = 0.0;
        if (backgroundFade)
            backgroundFade.Clear();
    }

    // Background fading.

    override void RenderOverlay(RenderEvent e)
    {
        double curTime = MSTimeF();

        if (menuActive == Menu.Off)
            return;

        if (prevTime <= 0.0)
            prevTime = curTime;

        double delta = curTime - prevTime;
        prevTime = curTime;

        CheckFade(delta);
    }

    protected ui void CheckFade(double delta)
    {
        if (backgroundFade)
        {
            backgroundFade.CheckAnimation(delta);

            if (!backgroundFade.HasNoAnimation())
                Screen.Dim(0, backgroundFade.GetFraction(), 0, 0, Screen.GetWidth(), Screen.GetHeight());
        }
    }

    ui void StartFadeIn(double dur)
    {
        if (!backgroundFade)
            backgroundFade = new("MenuAnimation");

         backgroundFade.StartAnimationIn(dur);
    }

    ui void StartFadeOut(double dur)
    {
        if (backgroundFade)
            backgroundFade.StartAnimationOut(dur);
    }

    ui bool IsFadedIn() const
    {
        return backgroundFade && backgroundFade.HasFinishedAnimating();
    }

    ui bool IsFadedOut() const
    {
        return !backgroundFade || backgroundFade.HasNoAnimation();
    }
}
