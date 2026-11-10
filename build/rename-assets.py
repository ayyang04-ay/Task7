# Rename 3 — proprietary asset names only.
#
# Usage, from this directory:  python3 -I rename-assets.py --check   (dry run, writes nothing)
#                              python3 -I rename-assets.py           (apply)
#
# WHY THIS SCRIPT EXISTS IN THE REPO.
# Rename 2's script lived in a session scratchpad and was lost, so this pass had to
# rebuild the guard from nothing. That is avoidable waste on the one operation in this
# project with two prior incidents. See build/replacements.README.txt for rename 1,
# which corrupted 73 real identifiers because 125 of its rules were bare two-character
# panel tokens applied as plain substring replacements.
#
# WHAT CHANGES. Three proprietary asset names. Nothing else. The predecessor adjuvant
# and its two research variants carried a stem that collides with a real clinical-stage
# asset (AviadoBio's AVB-101, an AAV9-GRN gene therapy), which is a third-party
# collision rather than a source leak, but the room is meant to read as self-contained.
#
# WHAT MUST NOT CHANGE. Every reagent, strain, gene, allele, marker and catalogue
# identifier. GUARD below is counted in every target before and after the edit and the
# script aborts if any count moves. Standing decision 9 keeps commodity reagents as
# they are, so ADU-S100, R848, INCB3344, Clodrosome, carbenoxolone, the BEI catalogue
# numbers, the lipid names and every strain name are guard entries, not targets.
# CMP-204 is likewise a guard entry: it is already a replacement name and it does not
# collide with anything.
#
# RULE SAFETY. Every rule is a full name of 7+ characters, so none can match inside a
# gene, allele, strain or marker. Rules are applied longest-first so none can fire
# inside another. Suffixed and prefixed forms ride along as substring matches, which is
# how rename 2 preserved the deliberate quirks: the trailing space, the lowercase (y),
# the parenthesis-free Y, Imprinting+ and Naive+.

import os, re, sys, zipfile, collections

CHECK = '--check' in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Longest first. Order matters: AVB-R848 and AVB-SRB are resolved before AVB-101 so a
# shorter rule can never fire inside a longer name.
RULES = [
    ('AVB-R848', 'PSLN-R848'),
    ('AVB-SRB',  'PSLN-SRB'),
    ('AVB-101',  'PSLN-212'),
]

# Counts of each of these must be identical before and after, in every target.
GUARD = [
    # the 13 that replacements.README.txt names as the minimum, after rename 1
    'H5N1', 'H1N1', 'H3N2', 'Ly6C', 'Ly6G', 'H-2Db', 'H-2Kd', 'CD11b', 'CD11c',
    'IFN-beta', 'Ccl2', 'Ccl3', 'Ccl5',
    # the asset and the names standing decision 9 keeps
    # NOT 'AMnESTI'. It was a guard entry here until rename 4 established that it is
    # the source publication's own compound name, present in the publisher's original
    # workbook. It is now a renamed target; see rename-asset-name.py.
    'PSLN-344', 'CMP-204', 'ADU-S100', 'R848', 'SRB', 'FreeSRB', 'INCB3344',
    'Clodrosome', 'carbenoxolone', 'CBX', 'OT-I', 'Sftpa1-/-Sftpd-/-',
    'NR-3177', 'NR-348', 'NR-41803', 'FR-201',
    # formulation
    'DPPC', 'DPPG', 'DPPE-PEG2000', 'cholesterol', 'cGAMP', 'Mn2+',
    # strains and animals
    'BALB/c', 'C57BL/6', 'Swiss Webster', 'Ifnar', 'CD45.1', 'CD45.2',
    # markers, epitopes, analytes
    'NP366-374', 'CXCR5', 'PD1', 'ICOS', 'Ki-67', 'GZMB', 'IFN-gamma', 'GM-CSF',
    'CCR2', 'IFNAR', 'Ifnb1', 'Il6', 'Il10', 'Tnf', 'Isg15', 'Tfh', 'Tfr',
    'IgG1', 'IgG2a', 'HAI', 'mLD50', 'AECI', 'AECII', 'CFSE', 'SPA/D',
]

TEXT_TARGETS = [
    'build/annotation-source.md',
    'task/golden-response.md',
    'build/audit-golden.py',
    'build/audit-registry.py',
    'fa/error_modes.md',
]
XLSX = 'data-room/adjuvant_program_dataset.xlsx'
BACKUP = 'build/pre-edit-workbook-backup.xlsx'

# HANDOFF.md is deliberately NOT a target. Its section 7 carries the rename-2 mapping
# table ("NanoSTING -> AVB-101"). A blind substitution there would rewrite history into
# "NanoSTING -> PSLN-212" and erase the record of the previous rename. Edit it by hand.

fail = []


def counts(text):
    return {g: text.count(g) for g in GUARD}


def apply_rules(text):
    for old, new in RULES:
        text = text.replace(old, new)
    return text


def check_guard(label, before, after):
    b, a = counts(before), counts(after)
    moved = {g: (b[g], a[g]) for g in GUARD if b[g] != a[g]}
    if moved:
        fail.append('%s: guard counts moved: %s' % (label, moved))
        return False
    return True


def report(label, before, after):
    hits = {old: before.count(old) for old, _ in RULES if before.count(old)}
    left = {old: after.count(old) for old, _ in RULES if after.count(old)}
    print('  %-34s %s' % (label, hits or 'no occurrences'))
    if left:
        fail.append('%s: rule string survives the edit: %s' % (label, left))
    check_guard(label, before, after)


# ---------------------------------------------------------------- text targets
print('Text targets')
text_new = {}
for rel in TEXT_TARGETS:
    path = os.path.join(ROOT, rel)
    before = open(path, encoding='utf-8').read()
    after = apply_rules(before)
    report(rel, before, after)
    text_new[path] = after

# ---------------------------------------------------------------- workbook
# Zip-level substitution on the sheet entries only. The shipped workbook is a
# hand-built archive: 23 entries, no sharedStrings.xml (every label inline in the sheet
# XML), no calcChain, app.xml stripped to Application and AppVersion, a uniform entry
# mtime, core.xml carrying an internal creator with a created/modified spread, and a
# theme and styles deliberately not the Excel 2024 pair. An openpyxl load/save
# round-trip would rebuild the entry set, synthesise a shared-string table, rewrite
# app.xml and the theme and reset every mtime -- reintroducing the over-sanitisation
# tells that a red-team found and that HANDOFF section 7 records as fixed. So every
# entry is rewritten verbatim except the sheets, preserving name, order, date_time,
# compress_type and all flag/attr fields.
print('\nWorkbook (zip-level, sheet entries only)')
src = os.path.join(ROOT, XLSX)
zin = zipfile.ZipFile(src)
entries = [(i, zin.read(i.filename)) for i in zin.infolist()]
archive_comment = zin.comment
zin.close()

SHEET = re.compile(r'^xl/worksheets/sheet\d+\.xml$')
new_entries, touched = [], []
for info, data in entries:
    if SHEET.match(info.filename):
        before = data.decode('utf-8')
        after = apply_rules(before)
        if after != before:
            touched.append(info.filename)
            check_guard(info.filename, before, after)
            for old, _ in RULES:
                if old in after:
                    fail.append('%s: rule string survives: %s' % (info.filename, old))
        new_entries.append((info, after.encode('utf-8')))
    else:
        # A rule string outside the sheets would mean the identifier lives somewhere
        # this script does not edit -- metadata, theme, styles. Abort rather than
        # silently ship a half-renamed file.
        blob = data.decode('utf-8', 'replace')
        for old, _ in RULES:
            if old in blob:
                fail.append('%s: NON-SHEET entry carries %s' % (info.filename, old))
        new_entries.append((info, data))

total = sum(entries[i][1].decode('utf-8', 'replace').count(o)
            for i in range(len(entries)) for o, _ in RULES)
print('  %-34s %d sheet entries carry a rule string, %d occurrences'
      % (XLSX, len(touched), total))

if fail:
    print('\nABORTED, nothing written:')
    for f in fail:
        print('  ' + f)
    sys.exit(1)

if CHECK:
    print('\nDry run. Guard held on every target. Nothing written.')
    print('Rules: ' + ', '.join('%s -> %s' % r for r in RULES))
    sys.exit(0)

# ---------------------------------------------------------------- write
for path, body in text_new.items():
    open(path, 'w', encoding='utf-8').write(body)
    print('  wrote %s' % os.path.relpath(path, ROOT))

tmp = src + '.new'
with zipfile.ZipFile(tmp, 'w') as zout:
    if archive_comment:
        zout.comment = archive_comment
    for info, data in new_entries:
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.compress_type = info.compress_type
        zi.external_attr = info.external_attr
        zi.internal_attr = info.internal_attr
        zi.create_system = info.create_system
        zi.create_version = info.create_version
        zi.extract_version = info.extract_version
        zi.flag_bits = info.flag_bits
        zi.comment = info.comment
        zout.writestr(zi, data)
os.replace(tmp, src)
print('  wrote %s' % XLSX)

# ---------------------------------------------------------------- verify the write
print('\nPost-write verification')
old_by_name = {i.filename: (i, d) for i, d in entries}
zv = zipfile.ZipFile(src)
new_list = [i.filename for i in zv.infolist()]
old_list = [i.filename for i, _ in entries]
assert new_list == old_list, 'entry list or order changed'
print('  entry list and order           identical (%d entries)' % len(new_list))

for i in zv.infolist():
    oi, od = old_by_name[i.filename]
    assert i.date_time == oi.date_time, 'mtime changed on ' + i.filename
    assert i.compress_type == oi.compress_type, 'compression changed on ' + i.filename
    if not SHEET.match(i.filename):
        assert zv.read(i.filename) == od, 'non-sheet entry changed: ' + i.filename
print('  entry mtimes and compression   identical')
print('  non-sheet entries              byte-identical')

import openpyxl
def numeric_cells(p):
    w = openpyxl.load_workbook(p, data_only=True)
    return [c.value for s in w for r in s.iter_rows() for c in r
            if isinstance(c.value, (int, float)) and not isinstance(c.value, bool)]
a, b = numeric_cells(src), numeric_cells(os.path.join(ROOT, BACKUP))
assert a == b, 'numeric cells differ from the publisher original: %d vs %d' % (len(a), len(b))
print('  numeric cells vs backup        identical (%d cells)' % len(a))

w = openpyxl.load_workbook(src, data_only=True)
strings = collections.Counter(c.value for s in w for r in s.iter_rows() for c in r
                              if isinstance(c.value, str) and 'PSLN' in c.value)
print('\nRenamed cell strings now in the workbook')
for s, c in sorted(strings.items()):
    print('  %4dx  %r' % (c, s))
print('\nDone. Now run: python3 -I make-artifacts.py && python3 -I audit-golden.py')
