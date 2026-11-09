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

if not CHECK:
    subprocess.run([sys.executable, '-I', 'make-annotation-pdf.py',
                    'annotation-source.md', '../data-room/trial_summary.pdf'], check=True)

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
