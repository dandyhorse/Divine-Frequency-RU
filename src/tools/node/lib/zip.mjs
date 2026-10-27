import { readFileSync, writeFileSync } from "node:fs";
import { deflateRawSync, inflateRawSync } from "node:zlib";

const CRC_TABLE = new Uint32Array(256);
for (let i = 0; i < 256; i++) {
  let c = i;
  for (let j = 0; j < 8; j++) {
    c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  }
  CRC_TABLE[i] = c >>> 0;
}

export function crc32(buffer) {
  let c = 0xffffffff;
  for (const byte of buffer) {
    c = CRC_TABLE[(c ^ byte) & 0xff] ^ (c >>> 8);
  }
  return (c ^ 0xffffffff) >>> 0;
}

function findEocd(buffer) {
  const start = Math.max(0, buffer.length - 65557);
  for (let i = buffer.length - 22; i >= start; i--) {
    if (buffer.readUInt32LE(i) === 0x06054b50) {
      return i;
    }
  }
  throw new Error("ZIP end of central directory not found");
}

export class ZipReader {
  constructor(path) {
    this.path = path;
    this.buffer = readFileSync(path);
    this.entries = new Map();
    this.names = [];
    this.#readDirectory();
  }

  #readDirectory() {
    const eocd = findEocd(this.buffer);
    const count = this.buffer.readUInt16LE(eocd + 10);
    const directoryOffset = this.buffer.readUInt32LE(eocd + 16);
    let offset = directoryOffset;
    for (let i = 0; i < count; i++) {
      if (this.buffer.readUInt32LE(offset) !== 0x02014b50) {
        throw new Error(`Bad ZIP central directory entry at ${offset}`);
      }
      const method = this.buffer.readUInt16LE(offset + 10);
      const compressedSize = this.buffer.readUInt32LE(offset + 20);
      const uncompressedSize = this.buffer.readUInt32LE(offset + 24);
      const nameLength = this.buffer.readUInt16LE(offset + 28);
      const extraLength = this.buffer.readUInt16LE(offset + 30);
      const commentLength = this.buffer.readUInt16LE(offset + 32);
      const localOffset = this.buffer.readUInt32LE(offset + 42);
      const name = this.buffer.toString("utf8", offset + 46, offset + 46 + nameLength);
      this.entries.set(name, {
        name,
        method,
        compressedSize,
        uncompressedSize,
        localOffset,
      });
      this.names.push(name);
      offset += 46 + nameLength + extraLength + commentLength;
    }
  }

  has(name) {
    return this.entries.has(name);
  }

  read(name) {
    const entry = this.entries.get(name);
    if (!entry) {
      throw new Error(`Not found in ZIP: ${name}`);
    }
    const local = entry.localOffset;
    if (this.buffer.readUInt32LE(local) !== 0x04034b50) {
      throw new Error(`Bad ZIP local header for ${name}`);
    }
    const nameLength = this.buffer.readUInt16LE(local + 26);
    const extraLength = this.buffer.readUInt16LE(local + 28);
    const start = local + 30 + nameLength + extraLength;
    const compressed = this.buffer.subarray(start, start + entry.compressedSize);
    if (entry.method === 0) {
      return Buffer.from(compressed);
    }
    if (entry.method === 8) {
      return inflateRawSync(compressed);
    }
    throw new Error(`Unsupported ZIP compression method ${entry.method} for ${name}`);
  }
}

function dosDateTime(date) {
  const year = Math.max(1980, date.getFullYear());
  const time =
    (date.getHours() << 11) | (date.getMinutes() << 5) | Math.floor(date.getSeconds() / 2);
  const day = ((year - 1980) << 9) | ((date.getMonth() + 1) << 5) | date.getDate();
  return { time, day };
}

export function writeZip(path, entries, level = 6) {
  const names = [...entries.keys()].sort();
  const localParts = [];
  const centralParts = [];
  let offset = 0;
  const { time, day } = dosDateTime(new Date());

  for (const name of names) {
    const data = Buffer.isBuffer(entries.get(name))
      ? entries.get(name)
      : Buffer.from(entries.get(name));
    const compressed = deflateRawSync(data, { level });
    const nameBuffer = Buffer.from(name, "utf8");
    const checksum = crc32(data);

    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6);
    local.writeUInt16LE(8, 8);
    local.writeUInt16LE(time, 10);
    local.writeUInt16LE(day, 12);
    local.writeUInt32LE(checksum, 14);
    local.writeUInt32LE(compressed.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBuffer.length, 26);
    local.writeUInt16LE(0, 28);
    localParts.push(local, nameBuffer, compressed);

    const central = Buffer.alloc(46);
    central.writeUInt32LE(0x02014b50, 0);
    central.writeUInt16LE(20, 4);
    central.writeUInt16LE(20, 6);
    central.writeUInt16LE(0x0800, 8);
    central.writeUInt16LE(8, 10);
    central.writeUInt16LE(time, 12);
    central.writeUInt16LE(day, 14);
    central.writeUInt32LE(checksum, 16);
    central.writeUInt32LE(compressed.length, 20);
    central.writeUInt32LE(data.length, 24);
    central.writeUInt16LE(nameBuffer.length, 28);
    central.writeUInt16LE(0, 30);
    central.writeUInt16LE(0, 32);
    central.writeUInt16LE(0, 34);
    central.writeUInt16LE(0, 36);
    central.writeUInt32LE(0, 38);
    central.writeUInt32LE(offset, 42);
    centralParts.push(central, nameBuffer);

    offset += local.length + nameBuffer.length + compressed.length;
  }

  const centralBuffer = Buffer.concat(centralParts);
  const eocd = Buffer.alloc(22);
  eocd.writeUInt32LE(0x06054b50, 0);
  eocd.writeUInt16LE(0, 4);
  eocd.writeUInt16LE(0, 6);
  eocd.writeUInt16LE(names.length, 8);
  eocd.writeUInt16LE(names.length, 10);
  eocd.writeUInt32LE(centralBuffer.length, 12);
  eocd.writeUInt32LE(offset, 16);
  eocd.writeUInt16LE(0, 20);

  writeFileSync(path, Buffer.concat([...localParts, centralBuffer, eocd]));
}
