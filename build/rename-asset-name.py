# Rename 4 — the asset name itself.
#
# Usage, from this directory:  python3 -I rename-asset-name.py --check   (dry run)
#                              python3 -I rename-asset-name.py           (apply)
#
# WHY. `AMnESTI` is the source publication's own compound name and it is in the
# paper's title: "AMnESTI reverses age-associated lung immune decline to drive
# heterosubtypic protection by inactivated influenza vaccines", Sci. Immunol. 11,
# eadz5242 (2026). It expands to "AEC-targeting MN Encapsulated STING agonist", and
# the data room carries AECI/ and AECII/ arm labels that spell out the first letter.
# One search on the asset name returns the paper and its PMC full text.
#
# It is present in build/pre-edit-workbook-backup.xlsx -- the publisher's original --
# at cells no rename has ever touched, which is the dispositive proof that it came in
# with the supplementary file rather than being authored here.
#
# This is HANDOFF section 7 Leak 2 again: a published compound name that survived every
# sweep. Rename 2 renamed NanoSTING and PS-GAMP and left the headline compound. The
# red-team that found Leak 2 classified AMnESTI as "INVENTED -- contrived backronym with
# Mn embedded", which is exactly wrong and for an instructive reason: it is a contrived
# backronym, because the authors contrived it. The red-team has no web access, so the
# enumeration it produces is parametric knowledge only. Never treat it as sufficient.
#
# BLAST RADIUS, wider than rename 3. The asset name reaches the prompt and the grader,
# which are GENERATED from the brief, so the rename must go into the brief rather than
# into the shipped copies. It also reaches make-artifacts.py, whose slice marker is the
# literal opening words of the prompt, and make-annotation-pdf.py, which writes the
# asset name into the /Subject metadata of both shipped PDFs.
#
# WHAT MUST NOT CHANGE. GUARD is counted in every target before and after and the
# script aborts if any count moves. It now includes the rename-3 outputs, since those
# are settled names and a rule firing inside one would be a regression.

import os, re, sys, zipfile, collections

CHECK = '--check' in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RULES = [('AMnESTI', 'PSLN-344')]

GUARD = [
    # rename 3's outputs -- settled names, must be untouched
    'PSLN-212', 'PSLN-R848', 'PSLN-SRB', 'CMP-204', 'PCL-26-0417',
    # the 13 that replacements.README.txt names as the minimum, after rename 1
    'H5N1', 'H1N1', 'H3N2', 'Ly6C', 'Ly6G', 'H-2Db', 'H-2Kd', 'CD11b', 'CD11c',
    'IFN-beta', 'Ccl2', 'Ccl3', 'Ccl5',
    # names standing decision 9 keeps
    # 'ADU-S100' was here as never-touch; rename 5 made it CDN-1807, on the grounds that
    # it names the asset's own composition rather than being commodity tooling.
    'CDN-1807', 'R848', 'SRB', 'FreeSRB', 'INCB3344', 'Clodrosome', 'carbenoxolone',
    'CBX', 'OT-I', 'Sftpa1-/-Sftpd-/-', 'NR-3177', 'NR-348', 'NR-41803', 'FR-201',
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
    'build/anton-brief-psql25c1.md',   # prompt and grader are generated FROM this
    'build/annotation-source.md',
    'build/audit-golden.py',
    'build/audit-registry.py',
    'build/make-artifacts.py',         # the prompt slice marker is a literal
    'build/make-annotation-pdf.py',    # writes the name into both PDFs' /Subject
    'task/golden-response.md',
    'fa/error_modes.md',
    'README.md',
]
XLSX_OLD = 'data-room/adjuvant_program_dataset.xlsx'
XLSX_NEW = 'data-room/adjuvant_program_dataset.xlsx'
BACKUP = 'build/pre-edit-workbook-backup.xlsx'

# NOT targets, by design:
#   HANDOFF.md                     section 7 carries the rename-2 and rename-3 mapping
#                                  tables; a blind substitution rewrites history.
#   fa/task-defects-and-fixes.md   records the original filename as a Leak 1 vector.
#   rename-assets.py               its GUARD lists AMnESTI as never-touch; that entry is
#   verify-rename.py               now false and both need hand edits, not substitution.
#   task/prompt.txt                generated. Let make-artifacts.py regenerate them, which
#   task/grader-guidelines.txt     is also a check: if the brief edit is right they come
#   task/golden-response.txt/.pdf  out carrying the new name with no further intervention.

fail = []
counts = lambda t: {g: t.count(g) for g in GUARD}


def apply_rules(t):
    for old, new in RULES:
        t = t.replace(old, new)
    return t


def check_guard(label, before, after):
    b, a = counts(before), counts(after)
    moved = {g: (b[g], a[g]) for g in GUARD if b[g] != a[g]}
    if moved:
        fail.append('%s: guard counts moved: %s' % (label, moved))


print('Text targets')
new_text = {}
for rel in TEXT_TARGETS:
    p = os.path.join(ROOT, rel)
    before = open(p, encoding='utf-8').read()
    after = apply_rules(before)
    n = {o: before.count(o) for o, _ in RULES if before.count(o)}
    print('  %-36s %s' % (rel, n or 'no occurrences'))
    for o, _ in RULES:
        if o in after:
            fail.append('%s: rule string survives: %s' % (rel, o))
    check_guard(rel, before, after)
    new_text[p] = after

print('\nWorkbook (zip-level, sheet entries only)')
src = os.path.join(ROOT, XLSX_OLD)
zin = zipfile.ZipFile(src)
entries = [(i, zin.read(i.filename)) for i in zin.infolist()]
comment = zin.comment
zin.close()
SHEET = re.compile(r'^xl/worksheets/sheet\d+\.xml$')
new_entries, touched, total = [], [], 0
for info, data in entries:
    blob = data.decode('utf-8', 'replace')
    hits = sum(blob.count(o) for o, _ in RULES)
    if SHEET.match(info.filename):
        after = apply_rules(blob)
        if hits:
            touched.append(info.filename); total += hits
            check_guard(info.filename, blob, after)
            for o, _ in RULES:
                if o in after:
                    fail.append('%s: rule string survives: %s' % (info.filename, o))
        new_entries.append((info, after.encode('utf-8')))
    else:
        if hits:
            fail.append('%s: NON-SHEET entry carries the asset name (%d)'
                        % (info.filename, hits))
        new_entries.append((info, data))
print('  %-36s %d sheet entries, %d occurrences' % (XLSX_OLD, len(touched), total))
print('  filename  %s  ->  %s' % (os.path.basename(XLSX_OLD), os.path.basename(XLSX_NEW)))

if fail:
    print('\nABORTED, nothing written:')
    [print('  ' + f) for f in fail]
    sys.exit(1)
if CHECK:
    print('\nDry run. Guard held on every target. Nothing written.')
    print('Rules: ' + ', '.join('%s -> %s' % r for r in RULES))
    sys.exit(0)

for p, body in new_text.items():
    open(p, 'w', encoding='utf-8').write(body)
    print('  wrote %s' % os.path.relpath(p, ROOT))

tmp = src + '.new'
with zipfile.ZipFile(tmp, 'w') as zout:
    if comment:
        zout.comment = comment
    for info, data in new_entries:
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        for a in ('compress_type', 'external_attr', 'internal_attr', 'create_system',
                  'create_version', 'extract_version', 'flag_bits', 'comment'):
            setattr(zi, a, getattr(info, a))
        zout.writestr(zi, data)
os.replace(tmp, src)
print('  wrote %s' % XLSX_OLD)

print('\nPost-write verification')
old_by_name = {i.filename: (i, d) for i, d in entries}
zv = zipfile.ZipFile(src)
assert [i.filename for i in zv.infolist()] == [i.filename for i, _ in entries], 'entry list changed'
print('  entry list and order           identical (%d entries)' % len(entries))
for i in zv.infolist():
    oi, od = old_by_name[i.filename]
    assert i.date_time == oi.date_time, 'mtime changed on ' + i.filename
    assert i.compress_type == oi.compress_type, 'compression changed on ' + i.filename
    if not SHEET.match(i.filename):
        assert zv.read(i.filename) == od, 'non-sheet entry changed: ' + i.filename
print('  entry mtimes and compression   identical')
print('  non-sheet entries              byte-identical')
zv.close()

import openpyxl
def numeric(p):
    w = openpyxl.load_workbook(p, data_only=True)
    return [c.value for s in w for r in s.iter_rows() for c in r
            if isinstance(c.value, (int, float)) and not isinstance(c.value, bool)]
a, b = numeric(src), numeric(os.path.join(ROOT, BACKUP))
assert a == b, 'numeric cells differ from the publisher original: %d vs %d' % (len(a), len(b))
print('  numeric cells vs backup        identical (%d cells)' % len(a))

w = openpyxl.load_workbook(src, data_only=True)
strings = collections.Counter(c.value for s in w for r in s.iter_rows() for c in r
                              if isinstance(c.value, str) and 'PSLN-344' in c.value)
print('\nRenamed cell strings now in the workbook')
for s, c in sorted(strings.items()):
    print('  %4dx  %r' % (c, s))
print('\nThe file itself still needs: git mv %s %s' % (XLSX_OLD, XLSX_NEW))
print('Then: python3 -I make-artifacts.py && python3 -I audit-golden.py')
