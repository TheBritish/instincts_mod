import re
import os
import shutil

# Path relative to this repo root when run from repo
ADV_PATH = os.path.join('in_game', 'common', 'advances', 'instincts_country_advances.txt')

def make_backup(path):
    bak = path + '.bak'
    shutil.copy2(path, bak)
    print('Backup written to {}'.format(bak))

def insert_potentials(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    changed = 0
    i = 0
    # Pattern matches lines like: eng_traditions_longbow_mastery = {
    header_re = re.compile(r'^([a-z]{3})_[^\s=]*\s*=\s*{\s*$')

    while i < len(lines):
        m = header_re.match(lines[i])
        if m:
            prefix = m.group(1).upper()
            # Look ahead a few lines to see if potential already exists
            j = i+1
            has_potential = False
            # scan until the next non-empty line or up to 8 lines
            scan_end = min(len(lines), i+12)
            while j < scan_end:
                s = lines[j].strip()
                if s == '':
                    j += 1
                    continue
                if s.startswith('potential'):
                    has_potential = True
                break

            if not has_potential:
                insertion = []
                insertion.append('    potential = {\n')
                insertion.append('        has_or_had_tag = {}\n'.format(prefix))
                insertion.append('    }\n')
                lines[i+1:i+1] = insertion
                changed += 1
                i += len(insertion)  # skip over inserted lines
        i += 1

    if changed > 0:
        with open(path, 'w') as f:
            f.writelines(lines)
    return changed

if __name__ == '__main__':
    repo_root = os.getcwd()
    adv_full = os.path.join(repo_root, ADV_PATH)
    if not os.path.exists(adv_full):
        print('Advances file not found at', adv_full)
        exit(1)
    make_backup(adv_full)
    changed = insert_potentials(adv_full)
    print('Inserted potential into {} advance entries'.format(changed))
