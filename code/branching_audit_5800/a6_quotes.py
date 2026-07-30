"""A6 -- X3's factual base: does arXiv:math/0612170 contain a SECOND tower
definition at §3.6?

X3 is entirely a claim about what the cited paper contains, so the cheapest
falsifier is any of the four strings being absent.  This is a FOURTH extractor
(after mg-af28's, mg-6ad0's and mg-41aa's), written here: FlateDecode streams
are inflated, Tj / TJ / ' / " operands are concatenated, both literal and hex
strings are decoded, and TJ kerning arrays are joined.  Ligature loss is
handled by searching the ligature-dropped spelling as well, which is mg-6ad0's
X6 finding and the reason a single-spelling search is not a search.

Network: downloads the PDF.  If the download fails, this prints NOT RUN and
exits 0 -- and the audit reports X3 as UNVERIFIED rather than as verified.
"""
import re, sys, zlib, urllib.request

URL = "https://arxiv.org/pdf/math/0612170"
LOCAL = sys.argv[1] if len(sys.argv) > 1 else None

print("=" * 78)
print("A6  X3 -- THE SECOND TOWER DEFINITION, ON A FOURTH EXTRACTOR")
print("=" * 78)

try:
    if LOCAL:
        raw = open(LOCAL, "rb").read()
        print("\nsource: %s (%d bytes)" % (LOCAL, len(raw)))
    else:
        raw = urllib.request.urlopen(URL, timeout=60).read()
        print("\nsource: %s (%d bytes)" % (URL, len(raw)))
except Exception as e:
    print("\nDOWNLOAD FAILED: %s" % e)
    print("\nSUMMARY a6_quotes: NOT RUN (no network); X3 UNVERIFIED by this audit")
    sys.exit(0)


def streams(data):
    out = []
    for m in re.finditer(rb"stream\r?\n", data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end < 0:
            continue
        blob = data[start:end]
        try:
            out.append(zlib.decompress(blob))
        except Exception:
            try:
                out.append(zlib.decompressobj().decompress(blob))
            except Exception:
                pass
    return out


def unescape(s):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == 0x5C and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt in b"nrtbf":
                out.append({0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12}[nxt])
                i += 2
                continue
            if 0x30 <= nxt <= 0x37:
                j = i + 1
                oct_ = b""
                while j < len(s) and len(oct_) < 3 and 0x30 <= s[j] <= 0x37:
                    oct_ += bytes([s[j]])
                    j += 1
                out.append(int(oct_, 8) & 0xFF)
                i = j
                continue
            out.append(nxt)
            i += 2
            continue
        out.append(c)
        i += 1
    return bytes(out)


TOKEN = re.compile(rb"\((?:\\.|[^\\()])*\)"          # literal string
                   rb"|<[0-9A-Fa-f\s]*>"              # hex string
                   rb"|-?\d+\.?\d*"                   # number (TJ kerning)
                   rb"|\bTJ\b|\bTj\b|\bTD\b|\bTd\b|\bT\*\b|'|\"")

# A TJ kerning value more negative than this is a word space, not a kern.
# TeX-set PDFs express inter-word gaps this way and nothing else; joining the
# fragments without it yields ALGEBRAICSTRUCTURES, and then every multi-word
# search reports ABSENT.  That is how this extractor failed on its first run.
SPACE_KERN = -100.0


def extract(content):
    parts = []
    for m in TOKEN.finditer(content):
        t = m.group(0)
        if t.startswith(b"("):
            parts.append(unescape(t[1:-1]))
        elif t.startswith(b"<"):
            h = re.sub(rb"\s", b"", t[1:-1])
            if len(h) % 2:
                h += b"0"
            try:
                parts.append(bytes.fromhex(h.decode("ascii")))
            except Exception:
                pass
        elif t[:1].isdigit() or t[:1] == b"-":
            try:
                if float(t) <= SPACE_KERN:
                    parts.append(b" ")
            except ValueError:
                pass
        elif t in (b"TD", b"Td", b"T*", b"'", b'"', b"TJ", b"Tj"):
            parts.append(b" ")
    return b"".join(parts)


text = b"".join(extract(s) for s in streams(raw))
txt = text.decode("latin-1")
flat = re.sub(r"\s+", " ", txt)
# TeX hyphenates across line breaks: the paper prints "injective homo- morphism".
# A search that does not undo that reports a present string as ABSENT -- which
# is what this extractor did on its first run, and is the same class of error as
# mg-6ad0's X6 ligature finding.  Both spellings are kept and both are searched.
dehyph = flat.replace("- ", "")
print("extracted characters: %d" % len(flat))


def drop_ligatures(s):
    """What a ligature-dropping reader produces: fi, ff, fl, ffi, ffl gone."""
    for lig in ("ffi", "ffl", "fi", "ff", "fl"):
        s = s.replace(lig, "")
    return s


flat_nl = drop_ligatures(flat)

TARGETS = [
    ("S3.1 title", "Tower of Algebras (Preserving unities)"),
    ("S3.6 title", "Tower of Algebras (not Preserving unities)"),
    ("S3.6 input clause", "algebra injection not necessarily preserving unities"),
    ("axiom (2) clause", "is an injective homomorphism of algebras"),
    ("axiom (2) unit clause", "for all m and n"),
    ("S3.6 defers to [10]", "the details can be found in [10]"),
]

print("\nsearched in BOTH spellings -- as printed, and ligature-dropped:")
missing = 0
for label, s in TARGETS:
    a = s in flat or s in dehyph
    b = drop_ligatures(s) in flat_nl or drop_ligatures(s) in drop_ligatures(dehyph)
    hit = a or b
    if not hit:
        missing += 1
    print("  %-22s printed:%-5s ligature-dropped:%-5s  %s"
          % (label, a, b, "FOUND" if hit else "*** ABSENT ***"))

# what does the paper actually say around the two section titles?
for key in ("Tower of Algebras (Preserving unities)",
            "Tower of Algebras (not Preserving unities)"):
    k = drop_ligatures(key)
    i = flat_nl.find(k)
    if i >= 0:
        print("\ncontext for %r:\n   ...%s..." % (key, flat_nl[i:i + 260]))

# what the section actually calls the object
i = drop_ligatures(flat).find("we consider a semi-tower of algebras")
print("\nWHAT S3.6 CALLS ITS OWN OBJECT (not quoted by mg-41aa):")
print("   %s" % (drop_ligatures(flat)[i:i + 150] if i >= 0 else "phrase not found"))

# the three conditions X3 says nobody has tested
print("\nDOES ANY INSTRUMENT IN THIS REPO TEST BERGERON-LI (3), (4), (5)?")
print("  (this is the claim 'untested by mg-af28, by mg-6ad0 and by mg-41aa')")
print("  grep is run by run_all.sh, not here -- see out_a6_grep.txt")

print("\nSUMMARY a6_quotes: %d of %d target strings ABSENT (0 = X3's factual "
      "base holds)" % (missing, len(TARGETS)))
