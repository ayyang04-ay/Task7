# Anton Taiga QA export

Contents:
- qa_report.md         — the full human-readable QA report for this problem version
- qa_items.json        — every QA finding, verbatim from Taiga (normalized field names)
- qa_jobs.json         — the QA runs (check type, status, result summaries)
- qa_status.json       — the version's auto-QA gate state
- problem_version.json — problem-version provenance (problem id, version, author, tags)

Read the "QA freshness" row in qa_report.md before acting on anything here. QA on
this environment is thin and often out of date: findings marked STALE were produced
against an EARLIER version of the task and may describe wording that no longer exists.

QA runs are kicked off from RL Studio; this export is a read-only snapshot from
Taiga at the "Exported" timestamp in qa_report.md.
