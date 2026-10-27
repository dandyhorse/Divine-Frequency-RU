import { existsSync, mkdirSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "../..");
const source = join(here, "Installer.cs");
const musicDir = join(here, "music");
const patch = join(root, "build", "DF_RU.pk3");
const output = join(root, "build", "DF_RU_Patcher.exe");

const cscCandidates = [
  "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe",
  "C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\csc.exe",
];
const csc = cscCandidates.find((path) => existsSync(path));
if (!csc) {
  throw new Error("C# compiler not found");
}
if (!existsSync(source)) {
  throw new Error(`Installer source not found: ${source}`);
}
if (!existsSync(patch)) {
  throw new Error(`Patch not found: ${patch}. Run npm run build first.`);
}
const music = readdirSync(musicDir).find((name) => name.toLowerCase().endsWith(".mp3"));
if (!music) {
  throw new Error(`MP3 not found in ${musicDir}`);
}

const framework = dirname(csc);
const wpf = join(framework, "WPF");
const references = [
  join(wpf, "PresentationFramework.dll"),
  join(wpf, "PresentationCore.dll"),
  join(wpf, "WindowsBase.dll"),
  join(framework, "System.Xaml.dll"),
  join(framework, "System.Windows.Forms.dll"),
  join(framework, "System.Drawing.dll"),
  join(framework, "System.Core.dll"),
].map((path) => `/reference:${path}`);

mkdirSync(dirname(output), { recursive: true });
const args = [
  "/nologo",
  "/target:winexe",
  `/out:${output}`,
  `/resource:${join(musicDir, music)},music.mp3`,
  `/resource:${patch},DF_RU.wad`,
  ...references,
  source,
];
const result = spawnSync(csc, args, { stdio: "inherit" });
if (result.status !== 0) {
  process.exitCode = result.status || 1;
} else {
  console.log(`Built ${output}`);
  console.log(`Size: ${(statSync(output).size / 1024 / 1024).toFixed(2)} MB`);
}
