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
using System.Windows.Navigation;
using Microsoft.Win32;
using Forms = System.Windows.Forms;

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
        private Button installButton;
        private Button uninstallButton;
        private Button launchButton;
        private Button musicButton;

        public PatcherWindow()
        {
            Title = "DF RU Patcher";
            Width = 640;
            Height = 520;
            ResizableMode();
            Background = ColorBrush("#0B0D12");
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
                Background = ColorBrush("#11151D"),
                BorderBrush = ColorBrush("#293141"),
                BorderThickness = new Thickness(1),
                CornerRadius = new CornerRadius(2),
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
                FontSize = 12,
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
            var root = new StackPanel { Margin = new Thickness(22, 16, 22, 10) };

            var header = new Grid { Margin = new Thickness(0, 0, 0, 14) };
            header.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            header.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            var brand = new StackPanel();
            brand.Children.Add(Label("DF // RU", 27, "#F3B43F", true));
            brand.Children.Add(Label("PATCHER  1.0.7", 10, "#7E8798"));
            header.Children.Add(brand);
            musicButton = MakeButton("MUSIC: ON", "#171D28", "#9EA8B8", ToggleMusic);
            musicButton.Margin = new Thickness(0);
            Grid.SetColumn(musicButton, 1);
            header.Children.Add(musicButton);
            root.Children.Add(header);

            var gamePanel = Panel();
            gamePanel.Child = BuildGamePanel();
            root.Children.Add(gamePanel);

            var patchPanel = Panel();
            patchPanel.Child = BuildPatchPanel();
            root.Children.Add(patchPanel);

            var actions = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(0, 1, 0, 9) };
            installButton = MakeButton("УСТАНОВИТЬ / ОБНОВИТЬ", "#F3B43F", "#11151D", InstallPatch);
            uninstallButton = MakeButton("УДАЛИТЬ", "#241A1A", "#F08A80", UninstallPatch);
            launchButton = MakeButton("ЗАПУСТИТЬ ИГРУ", "#171D28", "#D6DCE8", LaunchGame);
            actions.Children.Add(installButton);
            actions.Children.Add(uninstallButton);
            actions.Children.Add(launchButton);
            root.Children.Add(actions);

            root.Children.Add(BuildTerminal());

            var footer = new Grid { Margin = new Thickness(1, 2, 1, 0) };
            footer.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            footer.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            footer.Children.Add(Label("Оригинальные файлы игры не изменяются", 9, "#657080"));
            var link = new TextBlock { FontSize = 9, HorizontalAlignment = HorizontalAlignment.Right };
            var hyperlink = new Hyperlink(new Run("MUSIC: Moonlight Equilibrium (8-bit)"))
            {
                Foreground = ColorBrush("#F3B43F"),
                TextDecorations = TextDecorations.Underline,
            };
            hyperlink.RequestNavigate += OpenMusicLink;
            link.Inlines.Add(hyperlink);
            Grid.SetColumn(link, 1);
            footer.Children.Add(link);
            root.Children.Add(footer);

            return root;
        }

        private FrameworkElement BuildGamePanel()
        {
            var panel = new StackPanel();
            panel.Children.Add(Label("GAME DIRECTORY", 10, "#7E8798", true));

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
                FontSize = 12,
                Padding = new Thickness(8, 7, 8, 7),
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
            badge = Label("ПОИСК", 10, "#7E8798", true);
            badge.Margin = new Thickness(0, 0, 10, 0);
            statusRow.Children.Add(badge);
            var detect = new Button
            {
                Content = "НАЙТИ АВТОМАТИЧЕСКИ",
                Background = Brushes.Transparent,
                BorderThickness = new Thickness(0),
                Foreground = ColorBrush("#F3B43F"),
                Cursor = Cursors.Hand,
                FontSize = 10,
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
            text.Children.Add(Label("RUSSIAN PATCH", 10, "#7E8798", true));
            text.Children.Add(Label("DF_RU.wad", 16, "#E7E2D8", true));
            text.Children.Add(Label("Полная версия игры. Демо не поддерживается.", 10, "#7E8798"));
            grid.Children.Add(text);
            patchSize = Label("...", 12, "#F3B43F", true);
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
            var grid = new Grid();
            grid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
            grid.RowDefinitions.Add(new RowDefinition { Height = new GridLength(1, GridUnitType.Star) });
            var head = new Grid { Margin = new Thickness(10, 7, 10, 5) };
            head.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            head.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            head.Children.Add(Label("STATUS.LOG", 9, "#657080", true));
            var state = Label("READY", 9, "#7DD49B", true);
            Grid.SetColumn(state, 1);
            head.Children.Add(state);
            grid.Children.Add(head);
            logBox = new TextBox
            {
                IsReadOnly = true,
                Background = Brushes.Transparent,
                Foreground = ColorBrush("#B8C1CF"),
                BorderThickness = new Thickness(0),
                FontSize = 10,
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
                music.Volume = 0.32;
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
