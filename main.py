#!/usr/bin/env python3
"""Entry point for the Meridia passport make.fun entry.

Reads the pre-rendered passport spread (entry.png, next to this file),
validates it, and writes it to the output directory as entry.png.

Standard library only. No network, no secrets, no writes outside the
output directory.
"""

import os
import struct
import sys

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1048576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py")

    with open(src, "rb") as fh:
        data = fh.read()

    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the %d byte limit"
                    % (len(data), MAX_BYTES))
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        return fail("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return fail("entry.png is %dx%d, expected %dx%d"
                    % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)

    print("wrote %s (%dx%d, %d bytes)" % (dst, width, height, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
