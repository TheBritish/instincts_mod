#!/usr/bin/env python3
"""
Find and remove duplicate consecutive monthly_prestige entries.
"""

import re

# Read file
file_path = r"c:\Users\Craig.CraigBates-PC\Documents\Paradox Interactive\Europa Universalis V\mod\instincts_mod\in_game\common\advances\instincts_country_advances.txt"

with open(file_path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Find duplicates
duplicates = []
for i in range(len(lines) - 1):
    if re.match(r'^\s*monthly_prestige\s*=', lines[i]) and re.match(r'^\s*monthly_prestige\s*=', lines[i+1]):
        duplicates.append(i + 1)  # Line number (1-indexed)
        print(f"Line {i+1}-{i+2}: Duplicate monthly_prestige found")

if duplicates:
    print(f"\nFound {len(duplicates)} duplicate monthly_prestige pairs")
    # Remove duplicates (keep first, remove second)
    new_lines = []
    skip_next = False
    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue
        new_lines.append(lines[i])
        if i < len(lines) - 1 and re.match(r'^\s*monthly_prestige\s*=', lines[i]) and re.match(r'^\s*monthly_prestige\s*=', lines[i+1]):
            skip_next = True
    
    # Write back
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.writelines(new_lines)
    
    print(f"✓ Removed {len(duplicates)} duplicate monthly_prestige entries")
else:
    print("No duplicate monthly_prestige entries found")
