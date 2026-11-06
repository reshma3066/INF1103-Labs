# Verification record - 6 November 2026

These results were observed during execution; this is a text record, not a screenshot.

| Check | Observed result |
| --- | --- |
| `python -m unittest discover -s L7 -v` | 9 tests passed, 0.073 seconds |
| `docker build -t inf1103-lab7 ./L7` | Built successfully using python:3.11-slim |
| `docker run --rm inf1103-lab7 python -m unittest -v` | 9 tests passed, 0.079 seconds |
| Container menu input: 1, then 6 | Both products displayed; inventory saved; exit code 0 |

The menu displayed these product details:

```text
ID: P001 | Name: Guitar | Price: $250.00 | Stock: 5
Weight: 3 kg
Requires physical shipping.
Shipping cost: $15.00
ID: D001 | Name: Music tutorial | Price: $19.90 | Stock: 100
Download size: 250 MB
Delivered digitally through a download.
```

An initial sandboxed Windows test run encountered permission errors accessing
temporary directories. Running with the required filesystem access passed all
tests; Docker tests also passed. This was an environment access issue.

Submission preparation reran the Docker build, tests and program successfully.
The latest test run passed all 9 tests in 0.075 seconds; see the raw logs in
`evidence`. JPG screenshots show the saved command output in Notepad.

Source commit `ad3c82e` was published to GitHub through the authenticated connector
after the command-line push required sign-in. `git fetch` verified the published
commit. The original local commit `c017ba2` is preserved on `lab7-local-backup`.
Submission evidence and updated documentation are included in a follow-up commit.
