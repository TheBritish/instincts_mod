#!/usr/bin/env python3
"""
Remove invalid naval modifiers from EU5 advances file.
These are EU4 modifiers that don't exist in EU5:
- naval_forcelimit_modifier
- global_naval_forcelimit_modifier
- global_ship_build_speed
Replace with monthly_prestige = 0.05
"""

import re

# Read file
file_path = r"c:\Users\Craig.CraigBates-PC\Documents\Paradox Interactive\Europa Universalis V\mod\instincts_mod\in_game\common\advances\instincts_country_advances.txt"

with open(file_path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Count before
forcelimit_count = len(re.findall(r'^\s*naval_forcelimit_modifier\s*=', content, re.MULTILINE))
global_forcelimit_count = len(re.findall(r'^\s*global_naval_forcelimit_modifier\s*=', content, re.MULTILINE))
ship_build_count = len(re.findall(r'^\s*global_ship_build_speed\s*=', content, re.MULTILINE))

print(f"Found {forcelimit_count} naval_forcelimit_modifier entries")
print(f"Found {global_forcelimit_count} global_naval_forcelimit_modifier entries")
print(f"Found {ship_build_count} global_ship_build_speed entries")

# Replace all three invalid modifiers
content = re.sub(r'^\s*naval_forcelimit_modifier\s*=\s*[\d.]+', '    monthly_prestige = 0.05', content, flags=re.MULTILINE)
content = re.sub(r'^\s*global_naval_forcelimit_modifier\s*=\s*[\d.]+', '    monthly_prestige = 0.05', content, flags=re.MULTILINE)
content = re.sub(r'^\s*global_ship_build_speed\s*=\s*[\d.]+', '    monthly_prestige = 0.05', content, flags=re.MULTILINE)

# Write back
with open(file_path, 'w', encoding='utf-8-sig') as f:
    f.write(content)

print(f"✓ Replaced {forcelimit_count + global_forcelimit_count + ship_build_count} invalid naval modifiers with monthly_prestige")
