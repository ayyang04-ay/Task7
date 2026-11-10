# Rename 5 — the encapsulated payload.
#
# Usage, from this directory:  python3 -I rename-payload.py --check   (dry run)
#                              python3 -I rename-payload.py           (apply)
#
# WHY, and why this is not the same call as the other commodity reagents.
# ADU-S100 is a real named development-stage asset: the synthetic CDN STING agonist
# ML RR-S2 CDA, Aduro Biotech, licensed to Novartis as MIW815, Phase 1, dropped from the
# portfolio in 2019. Standing decision 9 originally classed it with the commodity tools
# and kept it on the grounds that real preclinical programmes name their published tool
# compounds, which is true but misses the discriminator.
#
# The discriminator is not "is it a company code" -- INCB3344 is one too, and it stays.
# It is whether the identifier names the ASSET'S OWN COMPOSITION. ADU-S100 is the
# payload both the candidate and the predecessor encapsulate, and the source paper's own
# abstract names it as what the asset encapsulates. That makes it constitutive of the
# thing the publication is about, which R848, carbenoxolone, INCB3344, Clodrosome, cGAMP
# and the lipid names are not: those are commodity tools that hundreds of papers use and
# that point at nothing in particular.
#
# WHAT THIS DOES NOT FIX. The exposure ADU-S100 carried was never only the string. The
# combination -- a cyclic dinucleotide payload, manganese coordination polymerisation, a
# pulmonary-surfactant-biomimetic liposome, aged mice, heterosubtypic influenza --
# narrows the literature to this programme with no compound name present at all. Renaming
# removes one named hook, not the fingerprint. See HANDOFF section 5, decision 9.
#
# FOOTPRINT. Five occurrences, all in annotation-source.md, which generates the shipped
# annotation PDF. ZERO in the workbook, which this script asserts rather than assumes.
# Nothing in the prompt, the grader or the golden refers to it.
#
# LEG 3 IS PRESERVED. Forcing-chain leg 3 is that the candidate and the comparator differ
# only by the Mn complex, and it rests on the annotation stating that both encapsulate the
# same cyclic dinucleotide. A full-string substitution keeps that sentence's force intact.

import os, re, sys, zipfile

CHECK = '--check' in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RULES = [('ADU-S100', 'CDN-1807')]

# Commodity tools that stay, plus the settled outputs of renames 3 and 4. Counted before
# and after; the script aborts if any count moves.
GUARD = [
    'PSLN-212', 'PSLN-344', 'PSLN-R848', 'PSLN-SRB', 'CMP-204', 'PCL-26-0417',
    'R848', 'cGAMP', 'INCB3344', 'Clodrosome', 'carbenoxolone', 'CBX', 'SRB',
    'DPPC', 'DPPG', 'DPPE-PEG2000', 'cholesterol', 'Mn2+', 'OT-I',
    'H5N1', 'H1N1', 'H3N2', 'Ly6C', 'Ly6G', 'H-2Db', 'H-2Kd', 'CD11b', 'CD11c',
    'NR-3177', 'NR-348', 'NR-41803', 'FR-201', 'NP366-374',
    'Ifnb1', 'Il6', 'Il10', 'Tnf', 'Isg15', 'Ccl2', 'Ccl3', 'Ccl5',
    'GM-CSF', 'CCR2', 'IFNAR', 'Ifnar', 'BALB/c', 'C57BL/6', 'AECI', 'AECII',
]

TEXT_TARGETS = ['build/annotation-source.md']
XLSX = 'data-room/adjuvant_program_dataset.xlsx'

# NOT targets: HANDOFF.md (section 5 and 7 record the decision and its reversal, so a
# substitution would rewrite the record), and rename-assets.py / rename-asset-name.py,
# whose GUARD lists name ADU-S100 as never-touch -- now false, and a hand edit.

fail = []
counts = lambda t: {g: t.count(g) for g in GUARD}

def apply_rules(t):
    for old, new in RULES:
        t = t.replace(old, new)
    return t

print('Text targets')
new_text = {}
for rel in TEXT_TARGETS:
    p = os.path.join(ROOT, rel)
    before = open(p, encoding='utf-8').read()
    after = apply_rules(before)
    print('  %-34s %s' % (rel, {o: before.count(o) for o, _ in RULES}))
    b, a = counts(before), counts(after)
    moved = {g: (b[g], a[g]) for g in GUARD if b[g] != a[g]}
    if moved:
        fail.append('%s: guard counts moved: %s' % (rel, moved))
    for o, _ in RULES:
        if o in after:
            fail.append('%s: rule string survives: %s' % (rel, o))
    new_text[p] = after

# Asserted, not assumed: the payload name must not be anywhere in the workbook, in any
# zip entry, metadata and theme included.
print('\nWorkbook')
z = zipfile.ZipFile(os.path.join(ROOT, XLSX))
hits = {i.filename: z.read(i.filename).decode('utf-8', 'replace').count(o)
        for i in z.infolist() for o, _ in RULES}
stray = {k: v for k, v in hits.items() if v}
print('  %-34s %s' % (XLSX, stray or 'no occurrences in any of the %d entries' % len(hits)))
if stray:
    fail.append('the workbook carries the payload name: %s' % stray)
z.close()

if fail:
    print('\nABORTED, nothing written:')
    [print('  ' + f) for f in fail]
    sys.exit(1)
if CHECK:
    print('\nDry run. Guard held. Nothing written.')
    print('Rules: ' + ', '.join('%s -> %s' % r for r in RULES))
    sys.exit(0)

for p, body in new_text.items():
    open(p, 'w', encoding='utf-8').write(body)
    print('  wrote %s' % os.path.relpath(p, ROOT))
print('\nNow run: python3 -I make-artifacts.py && python3 -I audit-golden.py')
