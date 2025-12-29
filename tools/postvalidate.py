#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple post-validation for the mod.

Checks performed:
- Finds advance keys in in_game/common/advances/*.txt and ensures each has a `potential` block
- Verifies localisation `key` and `key_desc` exist in instincts_country_advances_l_english.yml
- Ensures localisation file is UTF-8 with BOM
- Reports unbalanced braces in advances files
- Finds deprecated tokens occurrences

This is a lightweight checker — it does not replace the game's PostValidate.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ADV_DIR = os.path.join(ROOT, 'in_game', 'common', 'advances')
LOC_FILE = os.path.join(ROOT, 'in_game', 'localization', 'english', 'instincts_country_advances_l_english.yml')

DEPRECATED = [
    'naval_movement',
    'global_manpower_modifier',
    'global_production_efficiency',
    'loyalty',
    'global_sailors_modifier',
]

def find_advances_in_file(path):
    advances = []
    # read in a Python2/3 compatible way and decode as utf-8 with replacement
    with open(path, 'rb') as f:
        data = f.read()
    try:
        text = data.decode('utf-8')
    except Exception:
        try:
            text = data.decode('utf-8', 'replace')
        except Exception:
            text = data.decode('latin1', 'replace')
    lines = text.splitlines(True)

    i = 0
    while i < len(lines):
        m = re.match(r'^([a-z0-9_]+)\s*=\s*\{', lines[i])
        if m:
            name = m.group(1)
            # parse block
            depth = lines[i].count('{') - lines[i].count('}')
            j = i + 1
            block = lines[i]
            while j < len(lines) and depth > 0:
                block += lines[j]
                depth += lines[j].count('{') - lines[j].count('}')
                j += 1
            advances.append((name, block, i+1))
            i = j
        else:
            i += 1
    return advances

def check_advances():
    missing_potential = []
    advances_found = 0
    files = []
    if not os.path.isdir(ADV_DIR):
        print('Advances dir not found:', ADV_DIR)
        return 0, []
    for fname in os.listdir(ADV_DIR):
        if not fname.endswith('.txt'):
            continue
        path = os.path.join(ADV_DIR, fname)
        files.append(path)
        advs = find_advances_in_file(path)
        advances_found += len(advs)
        for name, block, lineno in advs:
            if 'potential' not in block:
                missing_potential.append((name, path, lineno))
    return advances_found, missing_potential

def load_localisation_keys():
    if not os.path.isfile(LOC_FILE):
        return set()
    with open(LOC_FILE, 'rb') as f:
        data = f.read()
    try:
        text = data.decode('utf-8')
    except Exception:
        try:
            text = data.decode('utf-8', 'replace')
        except Exception:
            text = data.decode('latin1', 'replace')
    keys = set(re.findall(r'^\s*([a-z0-9_]+):', text, flags=re.M))
    return keys

def check_localisation_for_advances(adv_names, loc_keys):
    missing = []
    for name in adv_names:
        key = name
        key_desc = name + '_desc'
        if key not in loc_keys or key_desc not in loc_keys:
            missing.append(name)
    return missing

def check_bom():
    if not os.path.isfile(LOC_FILE):
        return False
    with open(LOC_FILE, 'rb') as f:
        start = f.read(3)
    return start == b'\xef\xbb\xbf'

def check_brace_balance():
    problems = []
    for root, _, files in os.walk(os.path.join(ROOT, 'in_game')):
        for fn in files:
            if not fn.endswith('.txt') and not fn.endswith('.yml'):
                continue
            path = os.path.join(root, fn)
            with open(path, 'rb') as f:
                data = f.read()
            try:
                txt = data.decode('utf-8')
            except Exception:
                try:
                    txt = data.decode('utf-8', 'replace')
                except Exception:
                    txt = data.decode('latin1', 'replace')
            open_count = txt.count('{')
            close_count = txt.count('}')
            if open_count != close_count:
                problems.append((path, open_count, close_count))
    return problems

def find_deprecated_tokens():
    hits = []
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.txt') and not fn.endswith('.yml'):
                continue
            path = os.path.join(root, fn)
            with open(path, 'rb') as f:
                data = f.read()
            try:
                text = data.decode('utf-8')
            except Exception:
                try:
                    text = data.decode('utf-8', 'replace')
                except Exception:
                    text = data.decode('latin1', 'replace')
            for i, line in enumerate(text.splitlines(), start=1):
                for token in DEPRECATED:
                    if token in line:
                        hits.append((token, path, i, line.strip()))
    return hits

def main():
    print('Running lightweight post-validate checks...')
    adv_count, missing_pot = check_advances()
    print('Advances found:', adv_count)
    if missing_pot:
        print('Advances missing potential:')
        for name, path, lineno in missing_pot:
            print(' -', name, 'in', path + ':' + str(lineno))
    else:
        print('All advances have potential blocks.')

    # localisation
    loc_keys = load_localisation_keys()
    adv_names = []
    # gather names from advances dir
    for fname in os.listdir(ADV_DIR):
        if not fname.endswith('.txt'):
            continue
        path = os.path.join(ADV_DIR, fname)
        advs = find_advances_in_file(path)
        adv_names.extend([n for n,_,_ in advs])

    missing_loc = check_localisation_for_advances(adv_names, loc_keys)
    print('Localisation entries total keys:', len(loc_keys))
    if missing_loc:
        print('Advances missing localisation (name or _desc):', len(missing_loc))
        for m in missing_loc[:30]:
            print(' -', m)
    else:
        print('All advances have localisation name + desc present (basic check).')

    # BOM check
    has_bom = check_bom()
    print('Localization file has UTF-8 BOM:', has_bom)

    # brace balance
    brace_issues = check_brace_balance()
    if brace_issues:
        print('Brace count mismatches found in files:')
        for p, o, c in brace_issues:
            print(' -', p, '{%d} vs }%d' % (o, c))
    else:
        print('All checked files have balanced braces (count-wise).')

    # deprecated tokens
    dep_hits = find_deprecated_tokens()
    if dep_hits:
        print('Deprecated token occurrences:')
        for token, path, lineno, line in dep_hits[:200]:
            print(' - {} in {}:{} -> {}'.format(token, path, lineno, line))
    else:
        print('No deprecated tokens found.')

    print('\nPost-validate checks complete.')

if __name__ == '__main__':
    main()
