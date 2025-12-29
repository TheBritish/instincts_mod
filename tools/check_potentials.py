import re, os, sys
ADV_PATH = os.path.join('in_game','common','advances','instincts_country_advances.txt')
if not os.path.exists(ADV_PATH):
    print('Advances file not found:', ADV_PATH)
    sys.exit(1)

with open(ADV_PATH, 'r') as f:
    lines = f.readlines()

header_re = re.compile(r'^([a-z]{3}_[^\s=]+)\s*=\s*{\s*$')
missing = []
for i,l in enumerate(lines):
    m = header_re.match(l)
    if m:
        name = m.group(1)
        # scan next up to 12 lines for a potential block
        found = False
        for j in range(i+1, min(i+13, len(lines))):
            if lines[j].strip().startswith('potential'):
                found = True
                break
            # if we hit a closing '}' for the block and didn't see potential, stop
            if lines[j].strip() == '}':
                break
        if not found:
            missing.append((i+1, name))

print('Total advances found:', sum(1 for l in lines if header_re.match(l)))
print('Advances missing potential:', len(missing))
if missing:
    print('\nFirst 30 missing examples (line, name):')
    for ln, nm in missing[:30]:
        print(ln, nm)

# exit code 0 if none missing, 2 otherwise
sys.exit(0 if len(missing)==0 else 2)
