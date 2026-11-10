# Regenerates every shipped artifact from its single source and reports any drift.
#
# Usage, from this directory:  python3 -I make-artifacts.py
#        check without writing: python3 -I make-artifacts.py --check
#
# The brief is the source of truth for the prompt and the grader; annotation-source.md
# is the source for the annotation PDF. The shipped copies are generated, never edited
# by hand. Run this after any edit to the brief or the annotation source, and before
# uploading anything to Studio.

import hashlib, subprocess, sys, os

CHECK = '--check' in sys.argv
BRIEF = 'anton-brief-psql25c1.md'
drift = []

GRADER_FRAMING = (
    "You are grading a response to a portfolio-review request on AMnESTI, a "
    "manganese-complexed pulmonary-surfactant-biomimetic liposomal STING agonist "
    "developed as an adjuvant for influenza A vaccines in older adults. The solver had "
    "the study's per-animal data workbook and a per-block annotation, and was asked "
    "whether to advance the asset, what is driving the protection, whether a biomarker "
    "is worth carrying forward and could go into patients, what the next studies must "
    "establish, and what was ruled out. Grade content for presence and correctness "
    "only. Do not grade where in the answer anything sits or in what order it appears."
)

def slice_between(text, start, end):
    i = text.index(start); j = text.index(end, i)
    return text[i:j].strip()

def emit(path, body, label):
    body = body.rstrip() + '\n'
    old = open(path).read() if os.path.exists(path) else None
    if old == body:
        print('  %-28s unchanged' % label)
    elif CHECK:
        print('  %-28s DRIFT: shipped copy differs from the brief' % label)
        drift.append(label)
    else:
        open(path, 'w').write(body)
        print('  %-28s regenerated' % label)
    return body

brief = open(BRIEF).read()

print('Artifacts')
prompt = emit('../task/prompt.txt',
              slice_between(brief, 'AMnESTI is our manganese-complexed', '### Prompt audit'),
              'task/prompt.txt')
grader = emit('../task/grader-guidelines.txt',
              GRADER_FRAMING + '\n\n' + slice_between(brief, 'A. Must be present and correct:',
                                                      '\n\n---\n\n## 5. SUPPORTING'),
              'task/grader-guidelines.txt')

ANNOT_SRC = 'annotation-source.md'
ANNOT_PDF = '../data-room/trial_summary.pdf'

def annotation_drift():
    # The PDF is generated, so a text diff against the source is the only check that
    # catches a shipped data-room file carrying something the source does not. This
    # exists because 27 corrupted strings once passed a green drift check that only
    # covered prompt.txt and grader-guidelines.txt.
    try:
        from pdfminer.high_level import extract_text
    except ImportError:
        return ['task/trial_summary.pdf (pdfminer.six absent, cannot verify)']
    import re
    def norm(t):
        return re.sub(r'\s+', ' ', re.sub(r'[*_`#|>-]', ' ', t)).strip()
    from pdfminer.pdfpage import PDFPage
    with open(ANNOT_PDF, 'rb') as fh:
        npages = sum(1 for _ in PDFPage.get_pages(fh))
    pdf = norm(extract_text(ANNOT_PDF))
    src = norm(open(ANNOT_SRC).read())
    bad = []
    # Every identifier-shaped token in the PDF must also appear in the source. A bare
    # integer no greater than the page count is a rendered page number and is not in
    # the source by design, so it is exempt.
    def exempt(t):
        return t.isdigit() and int(t) <= npages
    toks = set(re.findall(r'\b[A-Za-z]*[0-9]+[A-Za-z0-9+-]*\b', pdf))
    orphan = sorted(t for t in toks if t not in src and not exempt(t))
    if orphan:
        bad.append('data-room/trial_summary.pdf carries %d token(s) absent from %s: %s'
                   % (len(orphan), ANNOT_SRC, ', '.join(orphan[:12])))
    for entry in re.findall(r'S\d\d-[A-Z]', src):
        if entry not in pdf:
            bad.append('data-room/trial_summary.pdf is missing block label %s' % entry)
            break
    return bad

if not CHECK:
    subprocess.run([sys.executable, '-I', 'make-annotation-pdf.py',
                    ANNOT_SRC, ANNOT_PDF], check=True)
else:
    for d in annotation_drift():
        print('  %-28s DRIFT: %s' % ('data-room/trial_summary.pdf', d))
        drift.append('data-room/trial_summary.pdf')

def stats(name, body, extra=''):
    lines = [l for l in body.split('\n') if l.strip()]
    return ("%s\n%s\nWord count      : %d\nCharacter count : %d\nsha256 prefix   : %s\n"
            "Paragraphs      : %d, each one unbroken line. Confirm no hard wraps survived "
            "the paste.\n%s\nRequired last line, in full:\n%s\n"
            % (name, '-' * len(name), len(body.split()), len(body),
               hashlib.sha256(body.encode()).hexdigest()[:12], len(lines),
               extra, lines[-1]))

checks = (
    "Verify each paste in the Studio form against these before launching.\n"
    "Regenerate with: python3 -I make-artifacts.py\n\n"
    + stats('prompt.txt', prompt)
    + '\n' + stats('grader-guidelines.txt', grader,
                   "\nScroll to the bottom of the form and confirm the C list is present. A\n"
                   "previous run uploaded 18,309 characters of a 24,504-character grader. It\n"
                   "stopped at the end of section A, leaving no penalty list and no neutral list.\n")
)
if CHECK:
    print('\n' + ('DRIFT in: ' + ', '.join(drift) if drift else 'No drift. Shipped copies match their sources.'))
    sys.exit(1 if drift else 0)
open('paste-checks.txt', 'w').write(checks)
print('  %-28s regenerated' % 'build/paste-checks.txt')
print('\n' + checks)
