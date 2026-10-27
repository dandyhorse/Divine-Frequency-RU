export function readWad(data) {
  if (data.toString("latin1", 0, 4) !== "IWAD" && data.toString("latin1", 0, 4) !== "PWAD") {
    throw new Error("Not a WAD file");
  }
  const count = data.readUInt32LE(4);
  const directoryOffset = data.readUInt32LE(8);
  const lumps = [];
  for (let i = 0; i < count; i++) {
    const offset = directoryOffset + i * 16;
    const position = data.readUInt32LE(offset);
    const size = data.readUInt32LE(offset + 4);
    const rawName = data.subarray(offset + 8, offset + 16);
    const zero = rawName.indexOf(0);
    const name = rawName.toString("latin1", 0, zero === -1 ? 8 : zero);
    lumps.push({ name, data: data.subarray(position, position + size) });
  }
  return lumps;
}

export function writeWad(lumps) {
  const headerSize = 12;
  let dataSize = 0;
  for (const lump of lumps) {
    dataSize += lump.data.length;
  }
  const directoryOffset = headerSize + dataSize;
  const out = Buffer.alloc(directoryOffset + lumps.length * 16);
  out.write("PWAD", 0, "latin1");
  out.writeUInt32LE(lumps.length, 4);
  out.writeUInt32LE(directoryOffset, 8);

  let position = headerSize;
  for (let i = 0; i < lumps.length; i++) {
    const lump = lumps[i];
    lump.data.copy(out, position);
    const entry = directoryOffset + i * 16;
    out.writeUInt32LE(position, entry);
    out.writeUInt32LE(lump.data.length, entry + 4);
    const rawName = Buffer.alloc(8);
    rawName.write(lump.name, 0, "latin1");
    rawName.copy(out, entry + 8);
    position += lump.data.length;
  }
  return out;
}

export function replaceBehavior(wad, behavior) {
  const lumps = readWad(wad);
  let found = false;
  const result = lumps.map((lump) => {
    if (lump.name.toUpperCase() === "BEHAVIOR") {
      found = true;
      return { name: lump.name, data: behavior };
    }
    return lump;
  });
  if (!found) {
    throw new Error("BEHAVIOR lump not found");
  }
  return writeWad(result);
}

export function wadStrings(data) {
  const strings = [];
  const pattern = /[\x20-\x7e]{4,}/g;
  const text = data.toString("latin1");
  for (const match of text.matchAll(pattern)) {
    strings.push(match[0]);
  }
  return strings;
}
