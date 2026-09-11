#!/usr/bin/env python3
"""Even up the white space around the exported draw.io diagrams.

draw.io's PNG export scales the left border by the -s factor but not the right,
so every diagram lands with roughly 62px of white on the left and 22px on the
right. The image box is centred on the page, but the drawing inside it is not,
so the figure reads as pushed to the right. Cropping to the ink and re-padding
evenly fixes it at the source.

Run after re-exporting a diagram. Idempotent: a diagram that is already even is
left untouched.
"""

import sys
from pathlib import Path

from PIL import Image

PAD = 30            # px of white to leave on every side
TOLERANCE = 4       # px; ignore differences this small
WHITE = 244         # anything lighter than this counts as background
DIAGRAMS = [
    'activity_diagram', 'architecture_diagram', 'class', 'component_diagram',
    'dfd_level_0', 'dfd_level_1', 'dfd_level_2', 'erd', 'methodology',
    'sequence_diagram', 'state_machine', 'use_case_diagram',
]


def normalise(path):
    im = Image.open(path)
    rgb = im.convert('RGB')
    # bounding box of everything that is not background
    bbox = rgb.convert('L').point(lambda v: 0 if v > WHITE else 255).getbbox()
    if bbox is None:
        return None
    left, right = bbox[0], im.width - bbox[2]
    if abs(left - right) <= TOLERANCE:
        return None
    out = Image.new('RGB', (bbox[2] - bbox[0] + 2 * PAD,
                            bbox[3] - bbox[1] + 2 * PAD), 'white')
    out.paste(rgb.crop(bbox), (PAD, PAD))
    out.save(path)
    return left, right, out.size


def main():
    base = Path('src/images')
    changed = 0
    for name in DIAGRAMS:
        path = base / f'{name}.png'
        if not path.exists():
            continue
        result = normalise(path)
        if result:
            left, right, size = result
            print(f"  {name}: white {left}/{right} px -> even {PAD} px, now {size[0]}x{size[1]}")
            changed += 1
    print(f"Evened padding on {changed} diagram(s)")


if __name__ == '__main__':
    main()
