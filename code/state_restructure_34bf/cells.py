"""Shared helpers: split STATE.md table rows into cells, and cells into verbatim passages.

Everything here is loss-free by construction: split_row(join) and split_passages(join)
both round-trip exactly, and the callers assert that.
"""
import re

ABBREV = ("Cor.", "Thm.", "Prop.", "Rem.", "Ex.", "Obs.", "sec.", "Sec.", "e.g.", "i.e.",
          "cf.", "vs.", "Fig.", "St.", "Dr.", "resp.", "etc.")


def split_row(line):
    """Split a markdown table row into ['', c1, c2, ..., ''] on UNESCAPED pipes.

    ''.join with '|' between the parts reproduces the line exactly.
    """
    parts, buf, i = [], [], 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            buf.append(line[i:i + 2])
            i += 2
            continue
        if ch == "|":
            parts.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    parts.append("".join(buf))
    return parts


def join_row(parts):
    return "|".join(parts)


def split_passages(text):
    """Split a cell into sentence-ish passages. ''.join(result) == text, exactly."""
    idx = [0]
    for m in re.finditer(r"[.!?]", text):
        end = m.end()
        # absorb trailing closing markup that belongs to the sentence
        while end < len(text) and text[end] in "*)\"'”’`»":
            end += 1
        if end >= len(text) or not text[end].isspace():
            continue
        head = text[idx[-1]:end]
        if any(head.rstrip("*)\"'”’`»").endswith(a) for a in ABBREV):
            continue
        # swallow the whitespace run so the join is exact
        j = end
        while j < len(text) and text[j].isspace():
            j += 1
        idx.append(j)
    idx.append(len(text))
    out, seen = [], 0
    for a, b in zip(idx, idx[1:]):
        if b <= a:
            continue
        out.append(text[a:b])
        seen = b
    assert "".join(out) == text, "passage split is lossy"
    return out
