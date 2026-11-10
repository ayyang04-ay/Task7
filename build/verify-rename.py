# Proves that the only edits between the reference branch and this one are the asset
# rename and the protocol identifier.
#
# Usage, from this directory:  python3 -I verify-rename.py [ref]
#   ref defaults to origin/claude/exciting-cray-mkihzd-v2
#
# The test is not "the diff looks superficial". It is: take every file as it stands on
# the reference branch, apply the declared substitutions, and require the result to be
# byte-identical to the working tree. Anything else -- a dropped line, a changed
# number, a mangled identifier, a stray edit -- fails. That is the check rename 1
# lacked, when 73 corrupted identifiers passed a drift check that only covered two
# files.

import os, re, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REF = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') \
    else 'origin/claude/exciting-cray-mkihzd-v2'

SUBS = [
    # rename 3
    ('AVB-R848', 'PSLN-R848'),
    ('AVB-SRB',  'PSLN-SRB'),
    ('AVB-101',  'PSLN-212'),
    ('AUP-0417', 'PCL-26-0417'),
    # rename 4 -- the asset name, which was the source publication's own compound name
    ('AMnESTI',  'PSLN-344'),
    ('amnesti_preclinical_dataset.xlsx', 'adjuvant_program_dataset.xlsx'),
]

# Files whose path changed. Key is the working-tree path, value the path on REF.
REF_PATHS = {
    'data-room/adjuvant_program_dataset.xlsx':
        'data-room/amnesti_preclinical_dataset.xlsx',
}

def expected(text):
    for old, new in SUBS:
        text = text.replace(old, new)
    return text

def at_ref(rel, binary=False):
    out = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (REF, REF_PATHS.get(rel, rel))],
                         capture_output=True, check=True).stdout
    return out if binary else out.decode('utf-8')

TEXT = [
    'build/annotation-source.md',
    'build/audit-golden.py',
    'build/audit-registry.py',
    'build/anton-brief-psql25c1.md',
    'build/label-mapping.tsv',
    'build/replacements.json',
    'build/replacements.README.txt',
    'build/make-artifacts.py',
    'build/make-annotation-pdf.py',
    'task/golden-response.md',
    'task/golden-response.txt',
    'task/prompt.txt',
    'task/grader-guidelines.txt',
    'fa/transcript-extract.py',
    'README.md',
]
# Files that carry a deliberate prose edit on top of the rename, so byte-identity with
# rename(ref) is the wrong test. They get the weaker but still mechanical pair of
# assertions: no superseded identifier survives anywhere, and no never-touch identifier
# changed count. Keep this list as short as it can be -- every entry is a file the
# strict test no longer covers.
ANNOTATED = {
    'fa/error_modes.md': 'rename note added recording that quoted trajectory text is '
                         'not verbatim at the compound name',
}
# Files deliberately left carrying superseded identifiers, because their job is to
# record the prior state. Asserted BYTE-IDENTICAL to the reference, with no
# substitutions applied -- a rename reaching one of these is itself the defect, since it
# would rewrite the incident record into a falsehood. HANDOFF.md belongs to this class
# in spirit but is hand-edited every pass, so it cannot be asserted mechanically.
# build/paste-checks.txt is deliberately NOT checked here. It holds statistics ABOUT the
# shipped text -- word count, character count, sha256 -- which do not transform under a
# substitution: PSLN-344 is one character longer than AMnESTI, so the prompt's character
# count legitimately moved 1185 -> 1187 while its word count stayed 201. It is generated,
# and `make-artifacts.py --check` is what verifies it.

# Files deliberately left carrying superseded identifiers, because their job is to
FROZEN = {
    'fa/task-defects-and-fixes.md': 'records the original filename as a Leak 1 vector '
                                    'and the pre-rename asset name',
}

GUARD_IN_ANNOTATED = ['PSLN-344', 'CMP-204', 'R848', 'SRB', 'Ly6C', 'CD11b',
                      'H5N1', 'H1N1', 'H3N2', 'Ifnb1', 'Ccl2', 'Tfr', 'GM-CSF']

fail = []

print('Text files: working tree == rename(%s)' % REF)
for rel in TEXT:
    want = expected(at_ref(rel))
    got = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    if want == got:
        n = sum(at_ref(rel).count(o) for o, _ in SUBS)
        print('  %-36s OK  (%d substitution%s)' % (rel, n, '' if n == 1 else 's'))
    else:
        fail.append(rel)
        print('  %-36s MISMATCH' % rel)
        a, b = want.split('\n'), got.split('\n')
        if len(a) != len(b):
            print('       line count %d vs %d' % (len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print('       first differing line %d' % (i + 1))
                print('       expected: %r' % x[:160])
                print('       actual  : %r' % y[:160])
                break

# ---------------------------------------------------------------- frozen files
print('\nFrozen files: must be byte-identical to the reference, no substitutions')
for rel, why in FROZEN.items():
    ref = at_ref(rel)
    got = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    if ref == got:
        print('  %-36s OK  (%s)' % (rel, why))
    else:
        fail.append(rel)
        print('  %-36s CHANGED -- a rename reached a historical record' % rel)

# ------------------------------------------------------------- annotated files
print('\nAnnotated files: prose edit allowed, rename still enforced')
for rel, why in ANNOTATED.items():
    ref = at_ref(rel)
    got = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    bad = []
    for old, _ in SUBS:
        # The old identifier may legitimately appear where the file is documenting the
        # mapping itself, so allow it only on a line that also names its replacement.
        for i, line in enumerate(got.split('\n'), 1):
            if old in line and not any(new in line for _, new in SUBS):
                bad.append('line %d still carries %s: %r' % (i, old, line.strip()[:90]))
    want_counts = {g: expected(ref).count(g) for g in GUARD_IN_ANNOTATED}
    got_counts = {g: got.count(g) for g in GUARD_IN_ANNOTATED}
    moved = {g: (want_counts[g], got_counts[g])
             for g in GUARD_IN_ANNOTATED if want_counts[g] != got_counts[g]}
    if moved:
        bad.append('never-touch counts moved: %s' % moved)
    if bad:
        fail.append(rel)
        print('  %-36s FAIL' % rel)
        for b in bad:
            print('       ' + b)
    else:
        print('  %-36s OK  (%s)' % (rel, why))

# ------------------------------------------------------------------ workbook
print('\nWorkbook: cell by cell')
XLSX = 'data-room/adjuvant_program_dataset.xlsx'
ref_bytes = at_ref(XLSX, binary=True)
tmp = os.path.join(HERE, '.ref-workbook.xlsx')
open(tmp, 'wb').write(ref_bytes)
try:
    import openpyxl
    wr = openpyxl.load_workbook(tmp, data_only=True)
    wn = openpyxl.load_workbook(os.path.join(ROOT, XLSX), data_only=True)
    if wr.sheetnames != wn.sheetnames:
        fail.append(XLSX + ' sheet names')
        print('  sheet names differ: %s vs %s' % (wr.sheetnames, wn.sheetnames))
    cells = renamed = numeric = 0
    for sr, sn in zip(wr, wn):
        for rr, rn in zip(sr.iter_rows(), sn.iter_rows()):
            for cr, cn in zip(rr, rn):
                cells += 1
                if isinstance(cr.value, str):
                    want = expected(cr.value)
                    if cn.value != want:
                        fail.append('%s!%s' % (sn.title, cn.coordinate))
                        print('  %s!%s  expected %r got %r'
                              % (sn.title, cn.coordinate, want, cn.value))
                    elif want != cr.value:
                        renamed += 1
                else:
                    if cr.value != cn.value:
                        fail.append('%s!%s' % (sn.title, cn.coordinate))
                        print('  %s!%s  NON-STRING CELL CHANGED %r -> %r'
                              % (sn.title, cn.coordinate, cr.value, cn.value))
                    elif cr.value is not None:
                        numeric += 1
    print('  %d cells compared' % cells)
    print('  %d string cells renamed, all exactly as declared' % renamed)
    print('  %d non-string cells, all identical' % numeric)

    # zip shape, which is what an openpyxl round-trip would have destroyed
    zr, zn = zipfile.ZipFile(tmp), zipfile.ZipFile(os.path.join(ROOT, XLSX))
    lr = [i.filename for i in zr.infolist()]
    ln = [i.filename for i in zn.infolist()]
    if lr != ln:
        fail.append('xlsx entry list')
        print('  entry list changed:\n    was %s\n    now %s' % (lr, ln))
    else:
        print('  %d zip entries, same names and order' % len(ln))
    mt = {i.filename: i.date_time for i in zr.infolist()}
    bad_mt = [i.filename for i in zn.infolist() if mt.get(i.filename) != i.date_time]
    if bad_mt:
        fail.append('xlsx mtimes')
        print('  entry mtime changed on: %s' % bad_mt)
    else:
        print('  entry mtimes unchanged')
    sheet = re.compile(r'^xl/worksheets/sheet\d+\.xml$')
    for i in zn.infolist():
        if not sheet.match(i.filename) and zn.read(i.filename) != zr.read(i.filename):
            fail.append('xlsx non-sheet ' + i.filename)
            print('  non-sheet entry changed: %s' % i.filename)
    print('  non-sheet entries byte-identical (metadata, theme, styles, rels)')
finally:
    os.path.exists(tmp) and os.remove(tmp)

# ------------------------------------------------------------------ PDFs
print('\nPDFs: extracted text == rename(reference text)')
try:
    from pdfminer.high_level import extract_text
    for rel in ('data-room/trial_summary.pdf', 'task/golden-response.pdf'):
        rb = at_ref(rel, binary=True)
        t = os.path.join(HERE, '.ref.pdf')
        open(t, 'wb').write(rb)
        try:
            norm = lambda s: re.sub(r'\s+', ' ', s).strip()
            want = norm(expected(extract_text(t)))
            got = norm(extract_text(os.path.join(ROOT, rel)))
            if want == got:
                print('  %-36s OK' % rel)
            else:
                fail.append(rel)
                print('  %-36s MISMATCH (%d vs %d chars)' % (rel, len(want), len(got)))
                for i, (x, y) in enumerate(zip(want, got)):
                    if x != y:
                        print('       diverges at char %d' % i)
                        print('       expected ...%r...' % want[max(0, i-60):i+60])
                        print('       actual   ...%r...' % got[max(0, i-60):i+60])
                        break
        finally:
            os.path.exists(t) and os.remove(t)
except ImportError:
    fail.append('pdfminer.six absent, PDFs not verified')
    print('  pdfminer.six absent, cannot verify')

print()
if fail:
    print('FAILED: %d item(s): %s' % (len(fail), ', '.join(map(str, fail[:12]))))
    sys.exit(1)
print('All targets reduce exactly to the declared substitutions.')
print('Substitutions: ' + ', '.join('%s -> %s' % s for s in SUBS))
