import { existsSync, mkdirSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { loadImage, createCanvas, GlobalFonts } from "@napi-rs/canvas";
import { ZipReader } from "./zip.mjs";
import { DEFAULT_IPK3, DEFAULT_WORK, DEV } from "./paths.mjs";

const BIG_PROFILES = {
  bigfont: { font: 32, height: 46, left: 1, right: 1, y: 0 },
  ACS_FONT: { font: 24, height: 32, left: 1, right: 0, y: 0 },
};

const UI_PROFILES = {
  RU_DF_FONT: { font: 18, height: 28, left: 1, right: 1, y: 1, space: 9, kerning: -1 },
  RU_ChatBoxFont: { font: 18, height: 28, left: 1, right: 1, y: 1, space: 5, kerning: -1 },
  RU_CONVO_FONT: { font: 18, height: 28, left: 1, right: 1, y: 1, space: 10, kerning: 0 },
};

const CHARS = [
  ...Array.from({ length: 32 }, (_, i) => String.fromCodePoint(0x0410 + i)),
  ...Array.from({ length: 32 }, (_, i) => String.fromCodePoint(0x0430 + i)),
  "Ё",
  "ё",
  ...[0x2013, 0x2014, 0x2026, 0x2116, 0x2018, 0x2019, 0x201c, 0x201d, 0x00ab, 0x00bb].map(
    (code) => String.fromCodePoint(code),
  ),
];

function glyphName(ch) {
  return `${ch.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")}.png`;
}

function fontPath() {
  const local = join(DEV, "source", "fonts", "noto-sans.ttf");
  if (existsSync(local)) {
    return local;
  }
  return join(DEV, "source", "engine", "ui", "noto", "noto-sans.ttf");
}

function clearPngs(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
    return;
  }
  for (const name of readdirSync(dir)) {
    if (name.toLowerCase().endsWith(".png")) {
      rmSync(join(dir, name));
    }
  }
}

function renderGlyph(fontSize, ch, profile) {
  const measureCanvas = createCanvas(8, 8);
  const measure = measureCanvas.getContext("2d");
  measure.font = `${fontSize}px NotoSans`;
  const metrics = measure.measureText(ch);
  const width = Math.max(
    1,
    Math.ceil(Math.max(metrics.width, metrics.actualBoundingBoxRight)) + profile.left + profile.right,
  );
  const canvas = createCanvas(width, profile.height);
  const ctx = canvas.getContext("2d");
  ctx.font = `${fontSize}px NotoSans`;
  ctx.fillStyle = "#fff";
  ctx.textBaseline = "alphabetic";
  ctx.fillText(ch, profile.left, Math.round(fontSize * 1.1) + profile.y);
  return canvas.toBuffer("image/png");
}

function readFontPngs(reader, prefix, hex) {
  const result = new Map();
  for (const name of reader.names) {
    if (!name.startsWith(prefix) || !name.toLowerCase().endsWith(".png")) {
      continue;
    }
    const base = name.slice(name.lastIndexOf("/") + 1).replace(/\.png$/i, "");
    const numeric = hex ? base : base.replace(/^DVFFN/i, "");
    const code = Number.parseInt(numeric, hex ? 16 : 10);
    if (!Number.isFinite(code)) {
      continue;
    }
    result.set(String.fromCodePoint(code), reader.read(name));
  }
  return result;
}

function writeInf(path, space, kerning, scale, translation) {
  const lines = [`SpaceWidth ${space}`, `Kerning ${kerning}`, `Scale ${scale}`];
  if (translation) {
    lines.push("TranslationType Standard");
  }
  writeFileSync(path, lines.join("\n") + "\n", "utf8");
}

async function npcGlyph(ch, gradient) {
  const size = 20;
  const source = createCanvas(64, 64);
  const context = source.getContext("2d");
  context.font = `${size}px NotoSans`;
  context.fillStyle = "#fff";
  context.textBaseline = "alphabetic";
  context.fillText(ch, 8, Math.round(size * 1.1));
  const pixels = context.getImageData(0, 0, 64, 64).data;
  let minX = 64;
  let minY = 64;
  let maxX = -1;
  let maxY = -1;
  for (let y = 0; y < 64; y++) {
    for (let x = 0; x < 64; x++) {
      if (pixels[(y * 64 + x) * 4 + 3] > 0) {
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
        maxX = Math.max(maxX, x);
        maxY = Math.max(maxY, y);
      }
    }
  }
  if (maxX < minX) {
    return createCanvas(23, 27).toBuffer("image/png");
  }
  const width = maxX - minX + 1;
  const height = maxY - minY + 1;
  const high = new Uint8Array(width * height);
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      high[y * width + x] = pixels[((y + minY) * 64 + (x + minX)) * 4 + 3] > 110 ? 1 : 0;
    }
  }
  const dilated = new Uint8Array(width * height);
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let value = 0;
      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          const nx = x + dx;
          const ny = y + dy;
          if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
            value = Math.max(value, high[ny * width + nx]);
          }
        }
      }
      dilated[y * width + x] = value;
    }
  }
  const mask = new Uint8Array(400);
  for (let y = 0; y < 20; y++) {
    const sy = Math.min(height - 1, Math.floor((y * height) / 20));
    for (let x = 0; x < 20; x++) {
      const sx = Math.min(width - 1, Math.floor((x * width) / 20));
      mask[y * 20 + x] = dilated[sy * width + sx];
    }
  }
  const alpha = new Uint8Array(23 * 27 * 4);
  const put = (x, y, r, g, b) => {
    if (x < 0 || x >= 23 || y < 0 || y >= 27) {
      return;
    }
    const index = (y * 23 + x) * 4;
    alpha[index] = r;
    alpha[index + 1] = g;
    alpha[index + 2] = b;
    alpha[index + 3] = 255;
  };
  for (let y = 0; y < 20; y++) {
    for (let x = 0; x < 20; x++) {
      if (mask[y * 20 + x]) {
        put(x + 2, y + 2, 11, 11, 11);
      }
    }
  }
  for (let y = 0; y < 20; y++) {
    for (let x = 0; x < 20; x++) {
      if (mask[y * 20 + x]) {
        put(x + 1, y + 3, 51, 30, 10);
      }
    }
  }
  for (let y = 0; y < 20; y++) {
    const color = gradient[Math.min(gradient.length - 1, y)] || [210, 155, 85, 255];
    for (let x = 0; x < 20; x++) {
      if (mask[y * 20 + x]) {
        put(x + 1, y + 3, color[0], color[1], color[2]);
      }
    }
  }
  const canvas = createCanvas(23, 27);
  const context2 = canvas.getContext("2d");
  const image = context2.createImageData(23, 27);
  image.data.set(alpha);
  context2.putImageData(image, 0, 0);
  return canvas.toBuffer("image/png");
}

async function npcGradient(original) {
  const fallback = Array.from({ length: 16 }, () => [210, 155, 85, 255]);
  const data = original.get("A");
  if (!data) {
    return fallback;
  }
  const image = await loadImage(data);
  const canvas = createCanvas(image.width, image.height);
  const context = canvas.getContext("2d");
  context.drawImage(image, 0, 0);
  const pixels = context.getImageData(0, 0, image.width, image.height).data;
  const rows = [];
  for (let y = 0; y < image.height; y++) {
    const counts = new Map();
    for (let x = 0; x < image.width; x++) {
      const index = (y * image.width + x) * 4;
      const r = pixels[index];
      const g = pixels[index + 1];
      const b = pixels[index + 2];
      const a = pixels[index + 3];
      if (a && r > 150 && g > 100) {
        const key = `${r},${g},${b},${a}`;
        counts.set(key, (counts.get(key) || 0) + 1);
      }
    }
    if (counts.size) {
      let best = null;
      let bestCount = -1;
      for (const [key, count] of counts) {
        if (count > bestCount) {
          best = key;
          bestCount = count;
        }
      }
      rows.push(best.split(",").map(Number));
    }
  }
  return rows.length ? rows : fallback;
}

export async function generateFonts({ ipk3 = DEFAULT_IPK3, work = DEFAULT_WORK, force = false } = {}) {
  const ttf = fontPath();
  if (!existsSync(ttf)) {
    throw new Error(`Font file not found: ${ttf}`);
  }
  if (!GlobalFonts.registerFromPath(ttf, "NotoSans")) {
    throw new Error(`Cannot register font: ${ttf}`);
  }
  const reader = new ZipReader(ipk3);
  const fontsRoot = join(work, "Fonts");

  for (const [name, profile] of Object.entries(BIG_PROFILES)) {
    const out = join(fontsRoot, name);
    if (force) {
      clearPngs(out);
    } else {
      mkdirSync(out, { recursive: true });
    }
    let generated = 0;
    for (const ch of CHARS) {
      const target = join(out, glyphName(ch));
      if (force || !existsSync(target)) {
        writeFileSync(target, renderGlyph(profile.font, ch, profile));
        generated++;
      }
    }
    console.log(`Big font ${name}: ${generated} generated`);
  }

  const dvffn = readFontPngs(reader, "HiRes/DF_FONT/DVFFN", false);
  for (const [name, profile] of Object.entries(UI_PROFILES)) {
    const out = join(fontsRoot, name);
    if (force) {
      clearPngs(out);
    } else {
      mkdirSync(out, { recursive: true });
    }
    for (const [ch, data] of dvffn) {
      const target = join(out, glyphName(ch));
      if (force || !existsSync(target)) {
        writeFileSync(target, data);
      }
    }
    let generated = 0;
    for (const ch of CHARS) {
      const target = join(out, glyphName(ch));
      if ((force || !existsSync(target)) && !dvffn.has(ch)) {
        writeFileSync(target, renderGlyph(profile.font, ch, profile));
        generated++;
      }
    }
    writeInf(join(out, "font.inf"), profile.space, profile.kerning, 1, true);
    console.log(`UI font ${name}: ${dvffn.size} original + ${generated} generated`);
  }

  const npcOriginal = readFontPngs(reader, "Fonts/npcfont/", true);
  const out = join(fontsRoot, "RU_npcfont");
  if (force) {
    clearPngs(out);
  } else {
    mkdirSync(out, { recursive: true });
  }
  for (const [ch, data] of npcOriginal) {
    const target = join(out, glyphName(ch));
    if (force || !existsSync(target)) {
      writeFileSync(target, data);
    }
  }
  const gradient = await npcGradient(npcOriginal);
  let generated = 0;
  for (const ch of CHARS) {
    if (ch !== ch.toUpperCase() || npcOriginal.has(ch)) {
      continue;
    }
    const target = join(out, glyphName(ch));
    if (!force && existsSync(target)) {
      continue;
    }
    const data = await npcGlyph(ch, gradient);
    writeFileSync(target, data);
    const lower = ch.toLowerCase();
    if (lower !== ch && !npcOriginal.has(lower)) {
      writeFileSync(join(out, glyphName(lower)), data);
    }
    generated++;
  }
  writeInf(join(out, "font.inf"), 5, -3, 1.2, false);
  console.log(`NPC font: ${npcOriginal.size} original + ${generated} generated pairs`);
}
