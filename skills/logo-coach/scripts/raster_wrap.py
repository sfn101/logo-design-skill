#!/usr/bin/env python3
"""Wrap a PNG/JPEG (a phone photo of a sketch, or a raster export) in an SVG so the test tools accept it.

preview_sheet.py and concept_sheet.py read SVG. A designer's PNG export or a photo of a sketchbook page is not
SVG, so this writes a tiny SVG that embeds the image at its native aspect ratio. The result lets you run the
visual tests (16/32 px ladder, greyscale, squint blur, mirror, backgrounds, contexts, shelf test) on raster work.

It does NOT vectorise anything and it is not a master file — svg_audit.py will (correctly) flag the raster.
For critique of vector craft (anchors, angles, colour count), ask the designer for the SVG.

Usage:
  python3 scripts/raster_wrap.py sketch-photo.jpg                      # -> sketch-photo.svg next to it
  python3 scripts/raster_wrap.py export.png -o work/export-wrapped.svg
  python3 scripts/raster_wrap.py a.png b.jpg --out-dir wrapped          # batch
Standard library only.
"""
import argparse
import base64
import os
import struct
import sys

sys.dont_write_bytecode = True


def image_size(path):
    """(width, height, mime) for PNG / JPEG / GIF / WebP(VP8X, VP8, VP8L), else raise."""
    with open(path, "rb") as fh:
        head = fh.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24])
            return w, h, "image/png"
        if head[:6] in (b"GIF87a", b"GIF89a"):
            w, h = struct.unpack("<HH", head[6:10])
            return w, h, "image/gif"
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            kind = head[12:16]
            if kind == b"VP8X":
                w = int.from_bytes(head[24:27], "little") + 1
                h = int.from_bytes(head[27:30], "little") + 1
            elif kind == b"VP8 ":
                fh.seek(26)
                w, h = struct.unpack("<HH", fh.read(4))
                w, h = w & 0x3FFF, h & 0x3FFF
            else:  # VP8L
                fh.seek(21)
                b = fh.read(4)
                w = 1 + (((b[1] & 0x3F) << 8) | b[0])
                h = 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
            return w, h, "image/webp"
        if head[:2] == b"\xff\xd8":
            fh.seek(2)
            while True:
                marker = fh.read(2)
                if len(marker) < 2 or marker[0] != 0xFF:
                    break
                code = marker[1]
                if code in (0xD8, 0x01) or 0xD0 <= code <= 0xD7:
                    continue
                seg_len = struct.unpack(">H", fh.read(2))[0]
                if code in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    fh.read(1)
                    h, w = struct.unpack(">HH", fh.read(4))
                    return w, h, "image/jpeg"
                fh.seek(seg_len - 2, 1)
    raise ValueError(f"unsupported or unreadable image: {path} (PNG, JPEG, GIF, WebP)")


def wrap(path, out):
    w, h, mime = image_size(path)
    data = base64.b64encode(open(path, "rb").read()).decode("ascii")
    title = os.path.splitext(os.path.basename(path))[0]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'viewBox="0 0 {w} {h}" width="{w}" height="{h}"><title>{title} (raster, wrapped for testing)</title>'
           f'<image width="{w}" height="{h}" href="data:{mime};base64,{data}" xlink:href="data:{mime};base64,{data}"/></svg>\n')
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"wrote {out}  ({w}×{h} {mime.split('/')[1]}; raster wrapped — visual tests only, not a master)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--out", help="output .svg (single input only)")
    ap.add_argument("--out-dir", help="directory for batch output")
    a = ap.parse_args()
    if a.out and len(a.files) > 1:
        ap.error("-o works with one input; use --out-dir for several")
    if a.out_dir:
        os.makedirs(a.out_dir, exist_ok=True)
    status = 0
    for f in a.files:
        base = os.path.splitext(os.path.basename(f))[0] + ".svg"
        out = a.out or (os.path.join(a.out_dir, base) if a.out_dir else os.path.splitext(f)[0] + ".svg")
        try:
            wrap(f, out)
        except (OSError, ValueError) as e:
            print(f"✖ {e}")
            status = 1
    sys.exit(status)


if __name__ == "__main__":
    import svglib  # noqa: F401  (UTF-8 console on Windows)
    main()
