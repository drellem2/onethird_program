import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cells import split_row, split_passages

lines = open(sys.argv[1] if len(sys.argv) > 1 else 'STATE.md').read().split('\n')
for ln in sys.argv[2].split(','):
    n = int(ln)
    parts = split_row(lines[n-1])
    print("=" * 30, "LINE", n, "cols", [len(p) for p in parts])
    for ci, cell in enumerate(parts):
        if not cell.strip():
            continue
        ps = split_passages(cell)
        for i, p in enumerate(ps):
            print(f"  [{ci}.{i}] ({len(p)}) {p}")
