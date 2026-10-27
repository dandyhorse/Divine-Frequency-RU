using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Effects;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Win32;
using Forms = System.Windows.Forms;
using Path = System.IO.Path;

namespace DfRuPatcher
{
    public static class Program
    {
        [STAThread]
        public static void Main()
        {
            var app = new Application();
            app.ShutdownMode = ShutdownMode.OnMainWindowClose;
            app.Run(new PatcherWindow());
        }
    }

    public sealed class PatcherWindow : Window
    {
        private const string GameName = "Divine Frequency";
        private const string PatchResource = "DF_RU.wad";
        private const string MusicResource = "music.mp3";
        private const string MusicUrl = "https://www.youtube.com/watch?v=WOLUFWzSd4A";

        private readonly MediaPlayer music = new MediaPlayer();
        private readonly string musicFile = Path.Combine(Path.GetTempPath(), "df_ru_patcher_music.mp3");
        private TextBox pathBox;
        private TextBox logBox;
        private TextBlock badge;
        private TextBlock patchSize;
        private TextBlock volumeLabel;
        private Slider volumeSlider;
        private Button installButton;
        private Button uninstallButton;
        private Button launchButton;
        private Button musicButton;

        public PatcherWindow()
        {
            Title = "DF RU Patcher";
            Width = 720;
            Height = 720;
            ResizableMode();
            WindowStyle = WindowStyle.None;
            Background = ColorBrush("#008080");
            Foreground = ColorBrush("#E7E2D8");
            FontFamily = new FontFamily("Consolas");
            WindowStartupLocation = WindowStartupLocation.CenterScreen;
            Content = BuildUi();
            Loaded += OnLoaded;
            Closed += OnClosed;
        }

        private void ResizableMode()
        {
            ResizeMode = ResizeMode.NoResize;
        }

        private static SolidColorBrush ColorBrush(string value)
        {
            return (SolidColorBrush)new BrushConverter().ConvertFromString(value);
        }

        private static TextBlock Label(string text, double size, string color, bool bold = false)
        {
            return new TextBlock
            {
                Text = text,
                FontSize = size,
                Foreground = ColorBrush(color),
                FontWeight = bold ? FontWeights.Bold : FontWeights.Normal,
                TextWrapping = TextWrapping.Wrap,
            };
        }

        private static Border Panel()
        {
            return new Border
            {
                Background = ColorBrush("#080B10"),
                BorderBrush = ColorBrush("#505861"),
                BorderThickness = new Thickness(1),
                CornerRadius = new CornerRadius(0),
                Padding = new Thickness(12, 10, 12, 10),
                Margin = new Thickness(0, 0, 0, 9),
            };
        }

        private Button MakeButton(string text, string background, string foreground, RoutedEventHandler handler)
        {
            var button = new Button
            {
                Content = text,
                Background = ColorBrush(background),
                Foreground = ColorBrush(foreground),
                BorderBrush = ColorBrush("#3B4557"),
                BorderThickness = new Thickness(1),
                FontFamily = new FontFamily("Consolas"),
                FontSize = 15,
                FontWeight = FontWeights.Bold,
                Padding = new Thickness(12, 8, 12, 8),
                Margin = new Thickness(0, 0, 8, 0),
                Cursor = Cursors.Hand,
            };
            button.Click += handler;
            return button;
        }

        private FrameworkElement BuildUi()
        {
            var desktop = new Grid { Background = ColorBrush("#008080") };
            var frame = new Border
            {
                Background = ColorBrush("#05070A"),
                BorderBrush = ColorBrush("#6E747A"),
                BorderThickness = new Thickness(2),
                Margin = new Thickness(12),
            };
            var root = new StackPanel { Margin = new Thickness(10) };
            root.Children.Add(BuildTitleBar());
            root.Children.Add(BuildDisplay());

            var game = Panel();
            game.Child = BuildGamePanel();
            root.Children.Add(game);

            var patch = Panel();
            patch.Child = BuildPatchPanel();
            root.Children.Add(patch);

            var actions = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(0, 1, 0, 9) };
            installButton = MakeButton("УСТАНОВИТЬ / ОБНОВИТЬ", "#D58B2B", "#090B0E", InstallPatch);
            uninstallButton = MakeButton("УДАЛИТЬ", "#2A1717", "#F08A80", UninstallPatch);
            launchButton = MakeButton("ЗАПУСТИТЬ ИГРУ", "#1B222D", "#D6DCE8", LaunchGame);
            actions.Children.Add(installButton);
            actions.Children.Add(uninstallButton);
            actions.Children.Add(launchButton);
            root.Children.Add(actions);

            root.Children.Add(BuildTerminal());
            root.Children.Add(BuildFooter());
            frame.Child = root;
            desktop.Children.Add(frame);
            return desktop;
        }

        private FrameworkElement BuildTitleBar()
        {
            var bar = new Grid { Height = 31, Margin = new Thickness(0, 0, 0, 9) };
            bar.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            bar.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            var drag = new Border
            {
                Background = ColorBrush("#0B0F15"),
                BorderBrush = ColorBrush("#505861"),
                BorderThickness = new Thickness(1),
                Padding = new Thickness(9, 0, 9, 0),
            };
            drag.Child = Label("DF // RU PATCHER  ::  v1.0.7", 13, "#D8D2C4", true);
            drag.MouseLeftButtonDown += (sender, args) =>
            {
                if (args.ButtonState == MouseButtonState.Pressed)
                {
                    DragMove();
                }
            };
            bar.Children.Add(drag);

            var controls = new StackPanel { Orientation = Orientation.Horizontal };
            var minimize = MakeButton("_", "#B8B8B8", "#000000", (sender, args) => WindowState = WindowState.Minimized);
            minimize.Width = 30;
            minimize.Padding = new Thickness(0);
            minimize.Margin = new Thickness(4, 0, 0, 0);
            minimize.FontSize = 14;
            var close = MakeButton("X", "#B8B8B8", "#000000", (sender, args) => Close());
            close.Width = 30;
            close.Padding = new Thickness(0);
            close.Margin = new Thickness(3, 0, 0, 0);
            close.FontSize = 14;
            controls.Children.Add(minimize);
            controls.Children.Add(close);
            Grid.SetColumn(controls, 1);
            bar.Children.Add(controls);
            return bar;
        }

        private FrameworkElement BuildDisplay()
        {
            var border = new Border
            {
                Background = ColorBrush("#010203"),
                BorderBrush = ColorBrush("#8B939C"),
                BorderThickness = new Thickness(2),
                Height = 184,
                Margin = new Thickness(0, 0, 0, 9),
                ClipToBounds = true,
            };
            var canvas = new Canvas { Width = 664, Height = 180, ClipToBounds = true };
            var glow = new Ellipse
            {
                Width = 430,
                Height = 120,
                Fill = new RadialGradientBrush(ColorBrush("#5A0A10").Color, ColorBrush("#00000000").Color),
                Opacity = 0.65,
            };
            Canvas.SetLeft(glow, 117);
            Canvas.SetTop(glow, 28);
            canvas.Children.Add(glow);

            var random = new Random(1337);
            for (var i = 0; i < 70; i++)
            {
                var star = new Ellipse
                {
                    Width = random.Next(1, 3),
                    Height = random.Next(1, 3),
                    Fill = ColorBrush(random.Next(0, 3) == 0 ? "#B82931" : "#A8B0B8"),
                    Opacity = 0.2 + random.NextDouble() * 0.7,
                };
                Canvas.SetLeft(star, random.Next(8, 650));
                Canvas.SetTop(star, random.Next(5, 160));
                canvas.Children.Add(star);
                var blink = new DoubleAnimation(0.1, 1, TimeSpan.FromSeconds(1.4 + random.NextDouble() * 3.4))
                {
                    AutoReverse = true,
                    RepeatBehavior = RepeatBehavior.Forever,
                    BeginTime = TimeSpan.FromMilliseconds(random.Next(0, 1800)),
                    EasingFunction = new SineEase { EasingMode = EasingMode.EaseInOut },
                };
                star.BeginAnimation(OpacityProperty, blink);
            }

            AddBlood(canvas, 196, 108, 0.0);
            AddBlood(canvas, 252, 112, 0.7);
            AddBlood(canvas, 430, 110, 1.2);
            AddBlood(canvas, 520, 108, 0.35);

            var title = new StackPanel
            {
                Orientation = Orientation.Horizontal,
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center,
            };
            var text = "† DIVINE FREQUENCY †";
            for (var i = 0; i < text.Length; i++)
            {
                var ch = text[i];
                var block = new TextBlock
                {
                    Text = ch == ' ' ? " " : ch.ToString(),
                    FontFamily = new FontFamily("Impact, Arial Black"),
                    FontSize = ch == '†' ? 34 : 38,
                    FontWeight = FontWeights.Bold,
                    Foreground = TitleBrush(),
                    Effect = new DropShadowEffect
                    {
                        Color = ColorBrush("#9B1018").Color,
                        BlurRadius = 9,
                        ShadowDepth = 0,
                        Opacity = 0.9,
                    },
                };
                var transform = new TranslateTransform();
                block.RenderTransform = transform;
                var floatAnimation = new DoubleAnimation(0, -3, TimeSpan.FromSeconds(2.2))
                {
                    AutoReverse = true,
                    RepeatBehavior = RepeatBehavior.Forever,
                    BeginTime = TimeSpan.FromMilliseconds(i * 65),
                    EasingFunction = new SineEase { EasingMode = EasingMode.EaseInOut },
                };
                transform.BeginAnimation(TranslateTransform.YProperty, floatAnimation);
                title.Children.Add(block);
            }

            var titleGrid = new Grid { Width = 664, Height = 180 };
            titleGrid.Children.Add(canvas);
            titleGrid.Children.Add(title);
            border.Child = titleGrid;
            return border;
        }

        private static Brush TitleBrush()
        {
            var gradient = new LinearGradientBrush { StartPoint = new Point(0, 0), EndPoint = new Point(0, 1) };
            gradient.GradientStops.Add(new GradientStop(ColorBrush("#FFE0A0").Color, 0));
            gradient.GradientStops.Add(new GradientStop(ColorBrush("#D58B2B").Color, 0.42));
            gradient.GradientStops.Add(new GradientStop(ColorBrush("#A81720").Color, 0.72));
            gradient.GradientStops.Add(new GradientStop(ColorBrush("#6C0710").Color, 1));
            return gradient;
        }

        private static void AddBlood(Canvas canvas, double x, double y, double delay)
        {
            var drip = new Polygon
            {
                Points = new PointCollection
                {
                    new Point(0, 0),
                    new Point(5, 0),
                    new Point(4, 15),
                    new Point(2, 20),
                    new Point(0, 12),
                },
                Fill = ColorBrush("#9E1018"),
                Opacity = 0.8,
                Effect = new DropShadowEffect
                {
                    Color = ColorBrush("#E01420").Color,
                    BlurRadius = 8,
                    ShadowDepth = 0,
                    Opacity = 0.8,
                },
            };
            Canvas.SetLeft(drip, x);
            Canvas.SetTop(drip, y);
            var move = new TranslateTransform();
            drip.RenderTransform = move;
            var fall = new DoubleAnimation(0, 15, TimeSpan.FromSeconds(2.4))
            {
                AutoReverse = true,
                RepeatBehavior = RepeatBehavior.Forever,
                BeginTime = TimeSpan.FromSeconds(delay),
                EasingFunction = new SineEase { EasingMode = EasingMode.EaseInOut },
            };
            var fade = new DoubleAnimation(0.8, 0.25, TimeSpan.FromSeconds(2.4))
            {
                AutoReverse = true,
                RepeatBehavior = RepeatBehavior.Forever,
                BeginTime = TimeSpan.FromSeconds(delay),
            };
            move.BeginAnimation(TranslateTransform.YProperty, fall);
            drip.BeginAnimation(OpacityProperty, fade);
            canvas.Children.Add(drip);
        }

        private FrameworkElement BuildFooter()
        {
            var footer = new Grid { Margin = new Thickness(1, 2, 1, 0) };
            footer.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            footer.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            footer.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });

            var volume = new StackPanel { Orientation = Orientation.Horizontal, VerticalAlignment = VerticalAlignment.Center };
            volume.Children.Add(Label("VOL", 11, "#98A2B0", true));
            volumeSlider = new Slider
            {
                Width = 130,
                Minimum = 0,
                Maximum = 100,
                Value = 50,
                Margin = new Thickness(7, 0, 7, 0),
                VerticalAlignment = VerticalAlignment.Center,
            };
            volumeSlider.ValueChanged += VolumeChanged;
            volume.Children.Add(volumeSlider);
            volumeLabel = Label("50%", 11, "#D58B2B", true);
            volume.Children.Add(volumeLabel);
            footer.Children.Add(volume);

            var right = new StackPanel { Orientation = Orientation.Horizontal, HorizontalAlignment = HorizontalAlignment.Right, VerticalAlignment = VerticalAlignment.Center };
            musicButton = MakeButton("MUSIC: ON", "#1B222D", "#D6DCE8", ToggleMusic);
            musicButton.FontSize = 10;
            musicButton.Padding = new Thickness(7, 3, 7, 3);
            musicButton.Margin = new Thickness(12, 0, 0, 0);
            right.Children.Add(musicButton);
            var link = new TextBlock { FontSize = 10, VerticalAlignment = VerticalAlignment.Center, Margin = new Thickness(14, 0, 0, 0) };
            var hyperlink = new Hyperlink(new Run("MUSIC: Moonlight Equilibrium (8-bit)"))
            {
                Foreground = ColorBrush("#D58B2B"),
                TextDecorations = TextDecorations.Underline,
            };
            hyperlink.RequestNavigate += OpenMusicLink;
            link.Inlines.Add(hyperlink);
            right.Children.Add(link);
            Grid.SetColumn(right, 2);
            footer.Children.Add(right);
            return footer;
        }

        private void VolumeChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            var value = volumeSlider == null ? 50 : e.NewValue;
            if (volumeLabel != null)
            {
                volumeLabel.Text = ((int)value) + "%";
            }
            music.Volume = value / 100.0;
        }

        private FrameworkElement BuildGamePanel()
        {
            var panel = new StackPanel();
            panel.Children.Add(Label("GAME DIRECTORY", 13, "#7E8798", true));

            var row = new Grid { Margin = new Thickness(0, 7, 0, 7) };
            row.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            row.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            pathBox = new TextBox
            {
                IsReadOnly = true,
                Background = ColorBrush("#0B0F16"),
                Foreground = ColorBrush("#E7E2D8"),
                BorderBrush = ColorBrush("#293141"),
                BorderThickness = new Thickness(1),
                FontSize = 15,
                Padding = new Thickness(9, 8, 9, 8),
                Margin = new Thickness(0, 0, 8, 0),
                VerticalContentAlignment = VerticalAlignment.Center,
            };
            row.Children.Add(pathBox);
            var browse = MakeButton("ОБЗОР", "#1D2430", "#D6DCE8", BrowseGame);
            browse.Margin = new Thickness(0);
            Grid.SetColumn(browse, 1);
            row.Children.Add(browse);
            panel.Children.Add(row);

            var statusRow = new Grid();
            statusRow.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            statusRow.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            statusRow.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            badge = Label("ПОИСК", 13, "#7E8798", true);
            badge.Margin = new Thickness(0, 0, 10, 0);
            statusRow.Children.Add(badge);
            var detect = new Button
            {
                Content = "НАЙТИ АВТОМАТИЧЕСКИ",
                Background = Brushes.Transparent,
                BorderThickness = new Thickness(0),
                Foreground = ColorBrush("#F3B43F"),
                Cursor = Cursors.Hand,
                FontSize = 13,
                Padding = new Thickness(0),
            };
            detect.Click += DetectGame;
            Grid.SetColumn(detect, 2);
            statusRow.Children.Add(detect);
            panel.Children.Add(statusRow);
            return panel;
        }

        private FrameworkElement BuildPatchPanel()
        {
            var grid = new Grid();
            grid.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            grid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            var text = new StackPanel();
            text.Children.Add(Label("RUSSIAN PATCH", 13, "#7E8798", true));
            text.Children.Add(Label("DF_RU.wad", 20, "#E7E2D8", true));
            text.Children.Add(Label("Полная версия игры. Демо не поддерживается.", 13, "#7E8798"));
            grid.Children.Add(text);
            patchSize = Label("...", 15, "#F3B43F", true);
            patchSize.VerticalAlignment = VerticalAlignment.Center;
            Grid.SetColumn(patchSize, 1);
            grid.Children.Add(patchSize);
            return grid;
        }

        private FrameworkElement BuildTerminal()
        {
            var border = Panel();
            border.Margin = new Thickness(0);
            border.Padding = new Thickness(0);
            border.Height = 130;
            var grid = new Grid();
            grid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
            grid.RowDefinitions.Add(new RowDefinition { Height = new GridLength(1, GridUnitType.Star) });
            var head = new Grid { Margin = new Thickness(10, 7, 10, 5) };
            head.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            head.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            head.Children.Add(Label("STATUS.LOG", 11, "#657080", true));
            var state = Label("READY", 11, "#7DD49B", true);
            Grid.SetColumn(state, 1);
            head.Children.Add(state);
            grid.Children.Add(head);
            logBox = new TextBox
            {
                IsReadOnly = true,
                Background = Brushes.Transparent,
                Foreground = ColorBrush("#B8C1CF"),
                BorderThickness = new Thickness(0),
                FontSize = 13,
                Padding = new Thickness(10, 0, 10, 9),
                VerticalScrollBarVisibility = ScrollBarVisibility.Auto,
                HorizontalScrollBarVisibility = ScrollBarVisibility.Disabled,
                TextWrapping = TextWrapping.Wrap,
                Text = "Готов к установке.\r\n",
            };
            Grid.SetRow(logBox, 1);
            grid.Children.Add(logBox);
            border.Child = grid;
            return border;
        }

        private void OnLoaded(object sender, RoutedEventArgs e)
        {
            patchSize.Text = FormatSize(ResourceSize(PatchResource));
            Log("Патч: DF_RU.wad, " + patchSize.Text);
            DetectGame(null, null);
            StartMusic();
        }

        private void OnClosed(object sender, EventArgs e)
        {
            music.Stop();
            music.Close();
            try
            {
                if (File.Exists(musicFile))
                {
                    File.Delete(musicFile);
                }
            }
            catch
            {
            }
        }

        private void OpenMusicLink(object sender, RequestNavigateEventArgs e)
        {
            Process.Start(new ProcessStartInfo(e.Uri.AbsoluteUri) { UseShellExecute = true });
            e.Handled = true;
        }

        private void ToggleMusic(object sender, RoutedEventArgs e)
        {
            if (musicButton.Content.ToString() == "MUSIC: ON")
            {
                music.Pause();
                musicButton.Content = "MUSIC: OFF";
                return;
            }
            music.Play();
            musicButton.Content = "MUSIC: ON";
        }

        private void StartMusic()
        {
            try
            {
                using (var input = Assembly.GetExecutingAssembly().GetManifestResourceStream(MusicResource))
                {
                    if (input == null)
                    {
                        return;
                    }
                    using (var output = File.Create(musicFile))
                    {
                        input.CopyTo(output);
                    }
                }
                music.Open(new Uri(musicFile));
                music.Volume = 0.5;
                music.MediaEnded += (sender, args) =>
                {
                    music.Position = TimeSpan.Zero;
                    music.Play();
                };
                music.Play();
            }
            catch
            {
                musicButton.Content = "MUSIC: N/A";
            }
        }

        private void DetectGame(object sender, RoutedEventArgs e)
        {
            var found = FindGame(pathBox.Text);
            if (found == null)
            {
                SetBadge("НЕ НАЙДЕНА", "#F08A80");
                SetButtons(false);
                Log("Игра не найдена. Укажи папку вручную.");
                return;
            }
            pathBox.Text = found;
            SetBadge("НАЙДЕНА", "#7DD49B");
            SetButtons(true);
            Log("Игра: " + found);
        }

        private void BrowseGame(object sender, RoutedEventArgs e)
        {
            using (var dialog = new Forms.FolderBrowserDialog())
            {
                dialog.Description = "Выберите папку Divine Frequency";
                dialog.ShowNewFolderButton = false;
                if (dialog.ShowDialog() == Forms.DialogResult.OK)
                {
                    pathBox.Text = dialog.SelectedPath;
                    DetectGame(null, null);
                }
            }
        }

        private void SetButtons(bool enabled)
        {
            if (installButton != null)
            {
                installButton.IsEnabled = enabled;
                uninstallButton.IsEnabled = enabled;
                launchButton.IsEnabled = enabled;
            }
        }

        private void SetBadge(string text, string color)
        {
            badge.Text = text;
            badge.Foreground = ColorBrush(color);
        }

        private void InstallPatch(object sender, RoutedEventArgs e)
        {
            var game = pathBox.Text;
            if (!IsGameDir(game))
            {
                Log("Ошибка: папка игры не найдена или это Demo-версия.");
                return;
            }
            try
            {
                var skins = Path.Combine(game, "skins");
                Directory.CreateDirectory(skins);
                var target = Path.Combine(skins, PatchResource);
                using (var input = Assembly.GetExecutingAssembly().GetManifestResourceStream(PatchResource))
                {
                    if (input == null)
                    {
                        Log("Ошибка: встроенный патч не найден.");
                        return;
                    }
                    using (var output = File.Create(target))
                    {
                        input.CopyTo(output);
                    }
                }
                Log("Установлено: " + target);
                Log("Перезапусти игру, если она уже запущена.");
            }
            catch (Exception ex)
            {
                Log("Ошибка установки: " + ex.Message);
            }
        }

        private void UninstallPatch(object sender, RoutedEventArgs e)
        {
            var game = pathBox.Text;
            if (!IsGameDir(game))
            {
                Log("Ошибка: папка игры не найдена.");
                return;
            }
            var target = Path.Combine(game, "skins", PatchResource);
            try
            {
                if (File.Exists(target))
                {
                    File.Delete(target);
                }
                Log("Патч удалён. Оригинальная игра не изменена.");
            }
            catch (Exception ex)
            {
                Log("Ошибка удаления: " + ex.Message);
            }
        }

        private void LaunchGame(object sender, RoutedEventArgs e)
        {
            var game = pathBox.Text;
            if (!IsGameDir(game))
            {
                Log("Ошибка: папка игры не найдена.");
                return;
            }
            try
            {
                Process.Start(new ProcessStartInfo(Path.Combine(game, "DivineFrequency.exe"))
                {
                    WorkingDirectory = game,
                    UseShellExecute = true,
                });
                Log("Игра запущена.");
            }
            catch (Exception ex)
            {
                Log("Не удалось запустить игру: " + ex.Message);
            }
        }

        private void Log(string message)
        {
            logBox.AppendText("[" + DateTime.Now.ToString("HH:mm:ss") + "] " + message + "\r\n");
            logBox.ScrollToEnd();
        }

        private static long ResourceSize(string name)
        {
            using (var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(name))
            {
                return stream == null ? 0 : stream.Length;
            }
        }

        private static string FormatSize(long bytes)
        {
            return (bytes / 1024.0 / 1024.0).ToString("0.0") + " MB";
        }

        private static bool IsGameDir(string folder)
        {
            if (string.IsNullOrWhiteSpace(folder) || Regex.IsMatch(folder, "demo", RegexOptions.IgnoreCase))
            {
                return false;
            }
            try
            {
                var path = Path.GetFullPath(folder.Trim().Trim('"'));
                return File.Exists(Path.Combine(path, "DivineFrequency.exe")) &&
                       File.Exists(Path.Combine(path, "DFSDSA.ipk3"));
            }
            catch
            {
                return false;
            }
        }

        private static string NormalizePath(string folder)
        {
            try
            {
                return Path.GetFullPath(folder.Trim().Trim('"'));
            }
            catch
            {
                return null;
            }
        }

        private static string FindGame(string explicitPath)
        {
            if (IsGameDir(explicitPath))
            {
                return NormalizePath(explicitPath);
            }

            var roots = new List<string>();
            AddRegistryPath(roots, @"HKEY_CURRENT_USER\Software\Valve\Steam", "SteamPath");
            AddRegistryPath(roots, @"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath");
            AddRegistryPath(roots, @"HKEY_LOCAL_MACHINE\SOFTWARE\Valve\Steam", "InstallPath");

            var libraries = new List<string>(roots);
            foreach (var root in roots)
            {
                var vdf = Path.Combine(root, "steamapps", "libraryfolders.vdf");
                if (!File.Exists(vdf))
                {
                    continue;
                }
                var text = File.ReadAllText(vdf);
                foreach (Match match in Regex.Matches(text, "\"path\"\\s+\"([^\"]+)\""))
                {
                    libraries.Add(match.Groups[1].Value.Replace("\\\\", "\\"));
                }
            }

            foreach (var root in libraries)
            {
                var found = Check(path => Path.Combine(path, "steamapps", "common", GameName), root);
                if (found != null) return found;
            }

            foreach (var basePath in new[]
            {
                Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86),
                Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles),
                @"C:\Steam",
                @"D:\Steam",
                @"D:\SteamLibrary",
                @"E:\SteamLibrary",
            })
            {
                var found = Check(path => Path.Combine(path, "steamapps", "common", GameName), basePath);
                if (found != null) return found;
            }
            return null;
        }

        private static string Check(Func<string, string> make, string root)
        {
            if (string.IsNullOrWhiteSpace(root))
            {
                return null;
            }
            var candidate = make(root);
            return IsGameDir(candidate) ? NormalizePath(candidate) : null;
        }

        private static void AddRegistryPath(List<string> roots, string key, string name)
        {
            try
            {
                var value = Registry.GetValue(key, name, null) as string;
                if (!string.IsNullOrWhiteSpace(value))
                {
                    var path = NormalizePath(value);
                    if (path != null) roots.Add(path);
                }
            }
            catch
            {
            }
        }
    }
}
