#!/usr/bin/env python3
# tools/slice_traits.py
# Usage: python tools/slice_traits.py path/to/master.png
from PIL import Image
import sys
import os

# ordered list extracted from your traits file (top-to-bottom, left-to-right)
traits = [
"incompetent_fool","cursed_ruler","plague_carrier","tyrant_despot","economically_ruined",
"chronic_gambler","paranoid_schemer","weak_willed","siege_incompetent",
"ambitious_but_weak","reckless_spender","lucky_merchant","battle_hardened","diplomatic_genius",
"strategic_mind","naval_supremacist","absolute_authority","economic_titan",
"conquerer_supreme","godlike_ruler"
]

TILE_W = 128
TILE_H = 128

def main():
    if len(sys.argv) < 2:
        print('Usage: python tools/slice_traits.py path/to/master.png [out_dir]')
        sys.exit(1)
    master = sys.argv[1].strip()
    # Robustly recover from concatenated paths like '...pngC:\other\path.png'
    if not os.path.exists(master):
        low = master.lower()
        png_indices = [i for i in range(len(low)) if low.startswith('.png', i)]
        recovered = None
        import re
        for i in png_indices:
            cand = master[:i+4]
            # try to locate the last drive-letter start within cand
            drives = list(re.finditer(r'[A-Za-z]:\\', cand))
            if drives:
                start = drives[-1].start()
                candidate_path = cand[start:]
            else:
                candidate_path = cand
            if os.path.exists(candidate_path):
                recovered = candidate_path
                break
        if recovered:
            master = recovered
        else:
            # fallback: if there are any .png substrings, take the last one as best-effort
            if png_indices:
                last_i = png_indices[-1]
                cand = master[:last_i+4]
                drives = list(re.finditer(r'[A-Za-z]:\\', cand))
                if drives:
                    master = cand[drives[-1].start():]
                else:
                    master = cand
    
    out_dir = sys.argv[2] if len(sys.argv) > 2 else 'source_icons'
    # Compatibility for older Python versions that don't support exist_ok
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    img = Image.open(master).convert('RGBA')
    W,H = img.size
    cols = W // TILE_W
    rows = H // TILE_H
    total = cols * rows
    if total < len(traits):
        print('Warning: image has fewer tiles (%d) than trait names (%d).' % (total, len(traits)))
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= len(traits):
                break
            left = c * TILE_W
            top = r * TILE_H
            box = (left, top, left + TILE_W, top + TILE_H)
            tile = img.crop(box)
            name = traits[idx]
            out_path = os.path.join(out_dir, name + '.png')
            tile.save(out_path)
            print('Wrote', out_path)
            idx += 1
        if idx >= len(traits):
            break
    print('Done: produced %d icons into %s' % (idx, out_dir))

if __name__ == '__main__':
    main()