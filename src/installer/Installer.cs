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
using System.Windows.Media.Imaging;
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
        private const string BackgroundResource = "background.png";
        private const string FontResource = "Creepster-Regular.ttf";
        private const string MusicUrl = "https://www.youtube.com/watch?v=WOLUFWzSd4A";

        private readonly MediaPlayer music = new MediaPlayer();
        private readonly string musicFile = Path.Combine(Path.GetTempPath(), "df_ru_patcher_music.mp3");
        private FontFamily displayFont;
        private bool musicOn = true;
        private TextBlock pathText;
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
            Width = 340;
            Height = 680;
            ResizableMode();
            WindowStyle = WindowStyle.None;
            Background = new ImageBrush(LoadImageResource(BackgroundResource))
            {
                Stretch = Stretch.UniformToFill,
                Opacity = 0.55,
            };
            Foreground = ColorBrush("#F0F0F0");
            FontFamily = new FontFamily("Consolas");
            WindowStartupLocation = WindowStartupLocation.CenterScreen;
            Content = BuildUi();
            PreviewMouseLeftButtonDown += StartWindowDrag;
            Loaded += OnLoaded;
            Closed += OnClosed;
        }

        private void ResizableMode()
        {
            ResizeMode = ResizeMode.NoResize;
        }

        private void StartWindowDrag(object sender, MouseButtonEventArgs args)
        {
            if (!IsInteractive(args.OriginalSource as DependencyObject))
            {
                try
                {
                    DragMove();
                }
                catch
                {
                }
            }
        }

        private static bool IsInteractive(DependencyObject source)
        {
            while (source != null)
            {
                if (source is Button || source is Slider || source is TextBox || source is Hyperlink)
                {
                    return true;
                }
                source = VisualTreeHelper.GetParent(source);
            }
            return false;
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
                Background = ColorBrush("#D9050505"),
                BorderBrush = ColorBrush("#777777"),
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
                BorderBrush = ColorBrush("#777777"),
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
            var root = new StackPanel { Margin = new Thickness(9, 9, 9, 7) };
            root.Children.Add(BuildTitleBar());
            root.Children.Add(BuildDisplay());

            var game = Panel();
            game.Child = BuildGamePanel();
            root.Children.Add(game);

            var patch = Panel();
            patch.Child = BuildPatchPanel();
            root.Children.Add(patch);

            var actions = new Grid { Margin = new Thickness(0, 1, 0, 9) };
            actions.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            actions.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            actions.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            installButton = MakeButton("УСТАНОВИТЬ", "#F0F0F0", "#000000", InstallPatch);
            uninstallButton = MakeButton("УДАЛИТЬ", "#0A0A0A", "#C8C8C8", UninstallPatch);
            launchButton = MakeButton("ЗАПУСТИТЬ", "#101010", "#E0E0E0", LaunchGame);
            foreach (var button in new[] { installButton, uninstallButton, launchButton })
            {
                button.FontSize = 14;
                button.Padding = new Thickness(4, 8, 4, 8);
                button.HorizontalAlignment = HorizontalAlignment.Stretch;
            }
            installButton.Margin = new Thickness(0, 0, 4, 0);
            uninstallButton.Margin = new Thickness(0, 0, 4, 0);
            launchButton.Margin = new Thickness(0);
            Grid.SetColumn(installButton, 0);
            Grid.SetColumn(uninstallButton, 1);
            Grid.SetColumn(launchButton, 2);
            actions.Children.Add(installButton);
            actions.Children.Add(uninstallButton);
            actions.Children.Add(launchButton);
            root.Children.Add(actions);

            root.Children.Add(BuildTerminal());
            root.Children.Add(BuildFooter());
            return root;
        }

        private FrameworkElement BuildTitleBar()
        {
            var bar = new Grid { Height = 44, Margin = new Thickness(0, 0, 0, 9) };
            bar.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            bar.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            bar.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            bar.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            bar.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });

            var drag = new Border { Background = ColorBrush("#D9050505"), Padding = new Thickness(7, 0, 2, 0) };
            drag.Child = Label("DF", 15, "#F0F0F0", true);
            drag.MouseLeftButtonDown += (sender, args) =>
            {
                if (args.ButtonState == MouseButtonState.Pressed)
                {
                    DragMove();
                }
            };
            bar.Children.Add(drag);

            var volume = new StackPanel
            {
                Orientation = Orientation.Horizontal,
                VerticalAlignment = VerticalAlignment.Center,
                Width = 184,
                Margin = new Thickness(0, 0, 3, 0),
            };
            volume.Children.Add(Label("VOL", 10, "#A8A8A8", true));
            volumeSlider = new Slider
            {
                Width = 120,
                Minimum = 0,
                Maximum = 100,
                Value = 50,
                IsMoveToPointEnabled = true,
                Margin = new Thickness(5, 0, 5, 0),
                VerticalAlignment = VerticalAlignment.Center,
            };
            volumeSlider.ValueChanged += VolumeChanged;
            volume.Children.Add(volumeSlider);
            volumeLabel = Label("50%", 10, "#F0F0F0", true);
            volumeLabel.Width = 30;
            volumeLabel.TextAlignment = TextAlignment.Right;
            volume.Children.Add(volumeLabel);
            Grid.SetColumn(volume, 1);
            bar.Children.Add(volume);

            musicButton = new Button
            {
                Content = "\uD83D\uDD0A",
                Width = 34,
                Height = 30,
                FontFamily = new FontFamily("Segoe UI Symbol"),
                FontSize = 17,
                Background = ColorBrush("#101010"),
                Foreground = ColorBrush("#E0E0E0"),
                BorderBrush = ColorBrush("#777777"),
                BorderThickness = new Thickness(1),
                Cursor = Cursors.Hand,
                Margin = new Thickness(3, 0, 0, 0),
            };
            musicButton.Click += ToggleMusic;
            Grid.SetColumn(musicButton, 2);
            bar.Children.Add(musicButton);

            var minimize = MakeButton("_", "#E0E0E0", "#000000", (sender, args) => WindowState = WindowState.Minimized);
            minimize.Width = 28;
            minimize.Height = 30;
            minimize.Padding = new Thickness(0);
            minimize.Margin = new Thickness(4, 0, 0, 0);
            minimize.FontSize = 14;
            Grid.SetColumn(minimize, 3);
            bar.Children.Add(minimize);

            var close = MakeButton("X", "#E0E0E0", "#000000", (sender, args) => Close());
            close.Width = 28;
            close.Height = 30;
            close.Padding = new Thickness(0);
            close.Margin = new Thickness(3, 0, 0, 0);
            close.FontSize = 14;
            Grid.SetColumn(close, 4);
            bar.Children.Add(close);
            return bar;
        }

        private FrameworkElement BuildDisplay()
        {
            var border = new Border
            {
                Background = Brushes.Transparent,
                BorderThickness = new Thickness(0),
                Height = 166,
                Margin = new Thickness(0, 0, 0, 9),
                ClipToBounds = true,
            };
            var titleGrid = new Grid { Width = 322, Height = 162 };

            var title = new StackPanel
            {
                Orientation = Orientation.Vertical,
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center,
            };
            var displayFont = DisplayFont();
            var letterIndex = 0;
            foreach (var word in new[] { "DIVINE", "FREQUENCY" })
            {
                var row = new StackPanel { Orientation = Orientation.Horizontal, HorizontalAlignment = HorizontalAlignment.Center };
                foreach (var ch in word)
                {
                    if (ch == ' ')
                    {
                        row.Children.Add(new Border { Width = 8 });
                        continue;
                    }
                    var letter = new TextBlock
                    {
                        Text = ch.ToString(),
                        FontFamily = displayFont,
                        FontSize = 36,
                        FontWeight = FontWeights.Bold,
                        Foreground = ColorBrush("#F0F0F0"),
                        TextAlignment = TextAlignment.Center,
                        VerticalAlignment = VerticalAlignment.Bottom,
                        Effect = new DropShadowEffect
                        {
                            Color = Colors.Black,
                            BlurRadius = 3,
                            ShadowDepth = 2,
                            Opacity = 0.9,
                        },
                    };
                    var transform = new TranslateTransform();
                    letter.RenderTransform = transform;
                    var wave = new DoubleAnimation(0, -5, TimeSpan.FromSeconds(1.8))
                    {
                        AutoReverse = true,
                        RepeatBehavior = RepeatBehavior.Forever,
                        BeginTime = TimeSpan.FromMilliseconds(letterIndex * 80),
                        EasingFunction = new SineEase { EasingMode = EasingMode.EaseInOut },
                    };
                    var sway = new DoubleAnimation(-0.8, 0.8, TimeSpan.FromSeconds(2.3))
                    {
                        AutoReverse = true,
                        RepeatBehavior = RepeatBehavior.Forever,
                        BeginTime = TimeSpan.FromMilliseconds(letterIndex * 80),
                        EasingFunction = new SineEase { EasingMode = EasingMode.EaseInOut },
                    };
                    transform.BeginAnimation(TranslateTransform.YProperty, wave);
                    transform.BeginAnimation(TranslateTransform.XProperty, sway);
                    row.Children.Add(letter);
                    letterIndex++;
                }
                title.Children.Add(row);
            }

            var viewbox = new Viewbox
            {
                Width = 300,
                Height = 124,
                Stretch = Stretch.Uniform,
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center,
                Child = title,
            };
            titleGrid.Children.Add(viewbox);
            var subtitle = new TextBlock
            {
                Text = "RUSSIAN PATCH  //  1.0.9",
                FontFamily = new FontFamily("Consolas"),
                FontSize = 10,
                Foreground = ColorBrush("#D0D0D0"),
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Bottom,
                Margin = new Thickness(0, 0, 0, 8),
            };
            titleGrid.Children.Add(subtitle);
            border.Child = titleGrid;
            return border;
        }

        private static BitmapImage LoadImageResource(string name)
        {
            try
            {
                using (var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(name))
                {
                    if (stream == null)
                    {
                        return null;
                    }
                    var image = new BitmapImage();
                    image.BeginInit();
                    image.CacheOption = BitmapCacheOption.OnLoad;
                    image.StreamSource = stream;
                    image.EndInit();
                    image.Freeze();
                    return image;
                }
            }
            catch
            {
                return null;
            }
        }

        private FontFamily DisplayFont()
        {
            if (displayFont != null)
            {
                return displayFont;
            }
            try
            {
                var fontFile = Path.Combine(Path.GetTempPath(), "df_ru_creepster.ttf");
                using (var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(FontResource))
                {
                    if (stream == null)
                    {
                        return displayFont = new FontFamily("Impact");
                    }
                    using (var output = File.Create(fontFile))
                    {
                        stream.CopyTo(output);
                    }
                }
                var folder = new Uri(Path.GetDirectoryName(fontFile) + Path.DirectorySeparatorChar);
                displayFont = new FontFamily(folder, "./Creepster-Regular.ttf#Creepster");
                return displayFont;
            }
            catch
            {
                displayFont = new FontFamily("Impact");
                return displayFont;
            }
        }

        private FrameworkElement BuildFooter()
        {
            var footer = new Grid { Margin = new Thickness(1, 2, 1, 0) };
            footer.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            footer.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            footer.Children.Add(Label("Файлы игры не изменяются", 9, "#888888"));
            var link = new TextBlock { FontSize = 10, HorizontalAlignment = HorizontalAlignment.Right };
            var hyperlink = new Hyperlink(new Run("Music"))
            {
                Foreground = ColorBrush("#F0F0F0"),
                TextDecorations = TextDecorations.Underline,
            };
            hyperlink.RequestNavigate += OpenMusicLink;
            link.Inlines.Add(hyperlink);
            Grid.SetColumn(link, 1);
            footer.Children.Add(link);
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
            panel.Children.Add(Label("GAME DIRECTORY", 13, "#A8A8A8", true));

            var row = new Grid { Margin = new Thickness(0, 7, 0, 7) };
            row.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            row.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            pathText = new TextBlock
            {
                TextTrimming = TextTrimming.CharacterEllipsis,
                TextWrapping = TextWrapping.NoWrap,
                Foreground = ColorBrush("#F0F0F0"),
                FontSize = 15,
                Padding = new Thickness(9, 8, 9, 8),
                VerticalAlignment = VerticalAlignment.Center,
            };
            var pathBox = new Border
            {
                Background = ColorBrush("#E6080808"),
                BorderBrush = ColorBrush("#4A4A4A"),
                BorderThickness = new Thickness(1),
                Margin = new Thickness(0, 0, 8, 0),
                Child = pathText,
            };
            row.Children.Add(pathBox);
            var browse = MakeButton("ОБЗОР", "#101010", "#E0E0E0", BrowseGame);
            browse.Margin = new Thickness(0);
            Grid.SetColumn(browse, 1);
            row.Children.Add(browse);
            panel.Children.Add(row);

            var statusRow = new Grid();
            statusRow.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            statusRow.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            statusRow.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            badge = Label("ПОИСК", 13, "#A8A8A8", true);
            badge.Margin = new Thickness(0, 0, 10, 0);
            statusRow.Children.Add(badge);
            var detect = new Button
            {
                Content = "НАЙТИ АВТОМАТИЧЕСКИ",
                Background = Brushes.Transparent,
                BorderThickness = new Thickness(0),
                Foreground = ColorBrush("#FFFFFF"),
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
            text.Children.Add(Label("RUSSIAN PATCH", 13, "#A8A8A8", true));
            text.Children.Add(Label("DF_RU.wad", 20, "#F0F0F0", true));
            text.Children.Add(Label("Полная версия игры. Демо не поддерживается.", 13, "#A8A8A8"));
            grid.Children.Add(text);
            patchSize = Label("...", 15, "#FFFFFF", true);
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
            head.Children.Add(Label("STATUS.LOG", 11, "#888888", true));
            var state = Label("READY", 11, "#FFFFFF", true);
            Grid.SetColumn(state, 1);
            head.Children.Add(state);
            grid.Children.Add(head);
            logBox = new TextBox
            {
                IsReadOnly = true,
                Background = Brushes.Transparent,
                Foreground = ColorBrush("#D0D0D0"),
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
            volumeSlider.Value = 50;
            volumeLabel.Text = "50%";
            music.Volume = 0.5;
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
            musicOn = !musicOn;
            if (musicOn)
            {
                music.Play();
                musicButton.Content = "\uD83D\uDD0A";
            }
            else
            {
                music.Pause();
                musicButton.Content = "\uD83D\uDD07";
            }
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
                    if (musicOn)
                    {
                        music.Position = TimeSpan.Zero;
                        music.Play();
                    }
                };
                music.Play();
            }
            catch
            {
                musicButton.Content = "N/A";
            }
        }

        private void DetectGame(object sender, RoutedEventArgs e)
        {
            var found = FindGame(pathText.Text);
            if (found == null)
            {
                SetBadge("НЕ НАЙДЕНА", "#C8C8C8");
                SetButtons(false);
                Log("Игра не найдена. Укажи папку вручную.");
                return;
            }
            pathText.Text = found;
            pathText.ToolTip = found;
            SetBadge("НАЙДЕНА", "#FFFFFF");
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
                    pathText.Text = dialog.SelectedPath;
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
            var game = pathText.Text;
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
            var game = pathText.Text;
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
            var game = pathText.Text;
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
