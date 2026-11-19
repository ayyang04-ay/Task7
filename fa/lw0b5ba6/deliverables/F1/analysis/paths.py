"""Locations used by every script. Override the workbook location with the environment variable PSLN_XLSX."""
import os
ROOT = os.path.dirname(os.path.abspath(__file__))          # .../analysis
OUT = os.path.dirname(ROOT) + os.sep                       # deliverables folder (one level up)
TABLES = os.path.join(ROOT, 'tables') + os.sep             # analysis tables T0-T18 (CSV)
FIGS = os.path.join(OUT, 'figures') + os.sep               # figures used in the proposal
BUILD = os.path.join(ROOT, 'build') + os.sep               # intermediates (Word reference document, rendered Markdown)
XLSX = os.environ.get('PSLN_XLSX', '/tmp/world/filesystem/psln_program_dataset.xlsx')
PANDOC = os.environ.get('PANDOC', '/opt/conda/envs/genomics/bin/pandoc')
for d in (TABLES, FIGS, BUILD):
    os.makedirs(d, exist_ok=True)
