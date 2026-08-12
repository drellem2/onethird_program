# docs/imports — artifacts brought under version control from outside the repo

Files here are **verbatim copies** of artifacts that arrived from somewhere that is not a
repository. They are imported byte-for-byte and are **not** edited, reformatted, or corrected in
the importing commit. Any mathematical assessment, repair, or integration happens later, in its
own commit, and is recorded there — not here.

The point of this directory is availability, not endorsement: an unversioned file in a drop
directory has exactly one copy and no backup, and this project has lost work to that before.
Importing a file records nothing about whether its claims are correct.

## compression.tex

| | |
|---|---|
| Source path | `~/files/compression.tex` |
| Source is under version control | no — `~/files` is an import drop, not a repo (`git rev-parse` there: `fatal: not a git repository`) |
| Backed up | no — `tmutil destinationinfo` reports `No destinations configured.` |
| Size | 5,950 bytes, 270 lines |
| Source mtime at import | 2026-08-12T13:00:12+0100 |
| sha256 | `99242c8ebe56dece2e7051744cc504b297c44c8fc74cf8c8e8bff9845fbaf76b` |
| Imported by | mg-2ffd, 2026-08-12 |
| Attribution | Daniel, 2026-08-12T13:00Z: *"see ~/files/compression.tex for a new one-third approach"* |

Section headings, as they appear in the file (a transcription of its own structure, not a summary
of its content):

```
### 1. Compress by forgetting alternate prefixes          (line 10)
### 2. Linear statistics behave perfectly under this compression   (line 66)
### 3. Even better: it computes BK energy exactly          (line 104)
### 4. Operator formulation                                (line 177)
### 5. Why this seems highly relevant to (1/3)-(2/3)       (line 229)
```

### What this import does NOT establish

Recorded explicitly so that a later reader does not mistake the presence of the file for a
verdict on it:

- **No mathematical assessment was performed.** §3's "exactly" has not been checked, §5's
  relevance argument has not been evaluated, and the note has not been compared against the
  corpus. Those questions are open and belong to pm-onethird's scoping.
- **The author's own framing is exploratory** — "seems highly relevant", "may connect directly",
  and a closing section that names an inequality it would *try* to prove rather than one it
  proves. Daniel ranked the item's **priority** (2026-08-12: "higher than riemann, equal to
  pogo"); he did not rank its probability, and this file records the former only.
- **The extension is `.tex` but the contents are not LaTeX-compilable as they stand** — the file
  uses Markdown `###` headings and bare `[` … `]` display delimiters. This is an observation about
  the bytes, made because it will surprise the next person who runs `pdflatex` on it. It has
  deliberately **not** been fixed: the import is verbatim, and converting it is a separate change.
- **The repository location is provisional.** `onethird_program` was chosen because the note is
  about (1/3)-(2/3); `one_third` and `one_third_width_three` were the other candidates. Moving a
  committed file is one commit, which is why the import did not wait on that decision.
