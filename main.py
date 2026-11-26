#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image entry, 26 November 2026.

Copies the pre-rendered entry.png into the output directory and
validates it: PNG signature, exactly 1024x1024 pixels, under 1 MiB.
Standard library only.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_W = 1024
EXPECTED_H = 1024
MAX_BYTES = 1024 * 1024


def check_png(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        raise SystemExit(
            "entry.png is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_W, EXPECTED_H)
        )
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit" % size)
    return width, height, size


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    if not os.path.isfile(SRC):
        raise SystemExit("entry.png is missing from the repository root")
    width, height, size = check_png(SRC)
    src_digest = sha256_file(SRC)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    dest_digest = sha256_file(dest)
    if dest_digest != src_digest:
        raise SystemExit("copy mismatch: destination hash differs from source")
    print("entry.png: %dx%d, %d bytes, sha256 %s" % (width, height, size, dest_digest))
    print("copied to %s" % dest)


if __name__ == "__main__":
    main()
