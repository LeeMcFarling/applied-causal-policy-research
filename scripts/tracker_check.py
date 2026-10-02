#!/usr/bin/env python3
"""Consistency check for the maturity trackers.

Checks, for every _MATURITY_TRACKER.md under guiding-principles/:
  1. Subdomain Status Matrix derives from brief frontmatter
     (phase = min over briefs, file count, word count).
  2. Every brief's `subdomain:` has a tracker row.
  3. The generated Dependency Map block is current (see --write-deps).
Checks across the corpus:
  4. Brief ids are unique.
  5. Every id named in dependencies / related_initiatives / accelerants /
     linked_policies is a live brief or a row in a "Planned Briefs" table.
  6. Planned Briefs rows: id not already written, cited by at least one live
     brief, reserved in only one table, and not "Parked" if any brief lists
     it under `dependencies:`. Ids named in the Blocks column must be live.
  7. Hard-dependency cap: every brief's `phase:` equals
     min(gate-met phase, phase of each live `dependencies:` entry). The
     gate-met phase is the `phase:` value, or, for a capped brief, the N in
     its "# capped by ...; gate-met phase without cap: N" comment.
  8. Consistency Issues rows (the Phase 2 gate): ids unique, briefs named in
     Open rows live, and no brief named in an Open row has a gate-met phase
     of 2+. Resolved rows may name briefs since moved to deprecated/.

Covers all four layers: Foundations, Operating-System, Infrastructure, and
each Policy_Domains/* folder (every _MATURITY_TRACKER.md under guiding-principles/).

Usage:
  python3 scripts/tracker_check.py               check only (exit 1 on any problem)
  python3 scripts/tracker_check.py --write-deps  regenerate each tracker's
                                                 Dependency Map block, then check
"""
import collections
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GP = os.path.join(ROOT, 'guiding-principles')
REF_FIELDS = ('dependencies', 'related_initiatives', 'accelerants', 'linked_policies')
GEN_BEGIN = '<!-- BEGIN GENERATED: scripts/tracker_check.py --write-deps — do not edit by hand -->'
GEN_END = '<!-- END GENERATED -->'
GATE_MET = re.compile(r'^phase:.*gate-met phase without cap:\s*(\d+)', re.M)


def rel(p):
    return os.path.relpath(p, ROOT)


class Brief:
    def __init__(self, path, y, words, gate_met):
        self.path, self.y, self.words = path, y, words
        self.id = str(y['id']) if y.get('id') else None
        self.phase = y.get('phase')
        self.gate_met = gate_met if gate_met is not None else self.phase
        self.deps = [str(d) for d in (y.get('dependencies') or [])]
        self.tracker = None  # directory of the tracker that counts this brief


def load_briefs(tracker_dirs):
    briefs = []
    for p in glob.glob(GP + '/**/*.md', recursive=True):
        if os.path.basename(p).startswith('_'):
            continue
        s = open(p, encoding='utf-8').read()
        if not s.startswith('---'):
            continue
        e = s.find('\n---', 3)
        y = yaml.safe_load(s[3:e]) or {}
        m = GATE_MET.search(s[:e])
        b = Brief(p, y, len(s[e + 4:].split()), int(m.group(1)) if m else None)
        owners = [d for d in tracker_dirs if p.startswith(d + os.sep)]
        b.tracker = max(owners, key=len) if owners else None
        briefs.append(b)
    return briefs


def table_after(lines, start):
    """Header and rows (as cell lists) of the first markdown table after line `start`."""
    k = next(i for i in range(start + 1, len(lines)) if lines[i].startswith('|'))
    hdr = [c.strip().lower() for c in lines[k].strip().strip('|').split('|')]
    rows = []
    for l in lines[k + 2:]:
        if not l.startswith('|'):
            break
        rows.append([c.strip() for c in l.strip().strip('|').split('|')])
    return hdr, rows


def section_rows(path, heading):
    L = open(path, encoding='utf-8').read().split('\n')
    out = []
    for i, l in enumerate(L):
        if re.match(r'^#+ ' + heading, l):
            out.extend(table_after(L, i)[1])
    return out


def check_matrix(tracker, briefs, probs):
    d = os.path.dirname(tracker)
    agg = collections.defaultdict(lambda: [[], 0, 0])
    for b in briefs:
        if b.path.startswith(d + os.sep):
            a = agg[b.y.get('subdomain')]
            a[0].append(b.phase)
            a[1] += 1
            a[2] += b.words
    L = open(tracker, encoding='utf-8').read().split('\n')
    i = next(k for k, l in enumerate(L) if l.startswith('## Subdomain Status'))
    hdr, raw = table_after(L, i)
    pi = hdr.index('phase')
    fi = next(x for x, c in enumerate(hdr) if 'file' in c)
    wi = next(x for x, c in enumerate(hdr) if 'word' in c)
    rows = {}
    for c in raw:
        if c[pi] in ('—', '-'):
            continue  # cross-reference row; not derived
        rows[c[0]] = (int(c[pi]), int(c[fi]), int(c[wi].strip('~').replace(',', '')))
    for sub, (ph, n, w) in agg.items():
        if sub not in rows:
            probs.append(f'{rel(tracker)}: brief subdomain {sub!r} has no tracker row')
        elif rows[sub] != (min(ph), n, w):
            probs.append(f'{rel(tracker)}: {sub} tracker {rows[sub]} vs derived {(min(ph), n, w)}')
    for sub, v in rows.items():
        if sub not in agg and v[1] != 0:
            probs.append(f'{rel(tracker)}: row {sub} claims {v[1]} files but no brief has that subdomain')


def dependency_block(tdir, by_id):
    """Brief-level Dependency Map for one tracker, derived from `dependencies:` frontmatter."""
    name = os.path.basename
    mine = sorted((b for b in by_id.values() if b.tracker == tdir), key=lambda b: b.id)
    requires, provides, caps = [], [], []
    for b in mine:
        for d in b.deps:
            dep = by_id.get(d)
            if dep and dep.tracker != tdir:
                requires.append(f'| `{b.id}` | `{d}` | {name(dep.tracker)} | {dep.phase} |')
        live = [by_id[d] for d in b.deps if d in by_id]
        low = [x for x in live if x.phase < b.gate_met]
        if low:
            floor = min(x.phase for x in low)
            who = ', '.join(f'`{x.id}`' for x in low if x.phase == floor)
            caps.append(f'| `{b.id}` | {b.gate_met} | {floor} | {who} |')
    for b in sorted(by_id.values(), key=lambda b: b.id):
        if b.tracker == tdir:
            continue
        for d in b.deps:
            if d in by_id and by_id[d].tracker == tdir:
                provides.append((d, b.id, name(b.tracker)))
    grouped = collections.defaultdict(lambda: collections.defaultdict(list))
    for d, i, t in provides:
        grouped[d][t].append(i)
    provides = [
        f'| `{d}` | {sum(len(v) for v in doms.values())} | '
        + '; '.join(f'{t}: ' + ', '.join(f'`{i}`' for i in sorted(doms[t])) for t in sorted(doms))
        + ' |'
        for d, doms in sorted(grouped.items(), key=lambda kv: (-sum(len(v) for v in kv[1].values()), kv[0]))
    ]

    def table(hdr, rows):
        sep = '|' + '|'.join('---' for _ in hdr.strip('|').split('|')) + '|'
        return '\n'.join([hdr, sep] + (rows or ['| _none_ |' + ' |' * (hdr.count('|') - 2)]))

    return '\n'.join([
        GEN_BEGIN,
        '',
        'Brief-level hard dependencies, derived from each brief\'s `dependencies:` frontmatter. '
        'Every live entry counts as hard: a brief cannot exceed the phase of any brief it depends on. '
        '`related_initiatives:` links are soft and not listed. Unwritten dependencies are in Planned Briefs above.',
        '',
        '### Requires (from other domains)',
        table('| Brief | Depends on | Their domain | Their phase |', requires),
        '',
        '### Required by (other domains)',
        table('| Our brief | Briefs requiring it | Required by (by domain) |', provides),
        '',
        '### Phase caps (briefs held below their gate-met phase)',
        table('| Brief | Gate-met phase | Capped to | Capped by |', caps),
        '',
        GEN_END,
    ])


def sync_dependency_block(tracker, block, write, probs):
    s = open(tracker, encoding='utf-8').read()
    if GEN_BEGIN in s:
        i, j = s.index(GEN_BEGIN), s.index(GEN_END) + len(GEN_END)
        new = s[:i] + block + s[j:]
    else:
        k = s.index('## Dependency Map')
        new = s[:k] + '## Dependency Map\n\n' + block + '\n\n' + s[k + len('## Dependency Map'):].lstrip('\n')
    if new == s:
        return
    if write:
        open(tracker, 'w', encoding='utf-8').write(new)
        print(f'  wrote Dependency Map: {rel(tracker)}')
    else:
        probs.append(f'{rel(tracker)}: Dependency Map is stale — run with --write-deps')


def main():
    write = '--write-deps' in sys.argv
    trackers = sorted(glob.glob(GP + '/**/_MATURITY_TRACKER.md', recursive=True))
    tdirs = [os.path.dirname(t) for t in trackers]
    briefs = load_briefs(tdirs)
    probs = []

    ids = collections.defaultdict(list)
    for b in briefs:
        if b.id:
            ids[b.id].append(b.path)
    for i, ps in ids.items():
        if len(ps) > 1:
            probs.append(f'duplicate id {i!r}: ' + ', '.join(rel(p) for p in ps))
    by_id = {b.id: b for b in briefs if b.id}

    for t in trackers:
        sync_dependency_block(t, dependency_block(os.path.dirname(t), by_id), write, probs)
        check_matrix(t, briefs, probs)

    # hard-dependency cap
    for b in by_id.values():
        live = [by_id[d].phase for d in b.deps if d in by_id]
        want = min([b.gate_met] + live)
        if b.phase != want:
            probs.append(f'{rel(b.path)}: phase {b.phase} but gate-met {b.gate_met} capped by '
                         f'dependencies gives {want}')

    planned = {}
    for src in trackers:
        for c in section_rows(src, 'Planned Briefs'):
            m = re.match(r'`([^`]+)`', c[0])
            if not m:
                continue
            pid = m.group(1)
            if pid in planned:
                probs.append(f'planned id {pid!r} reserved twice: {rel(planned[pid][0])}, {rel(src)}')
            planned[pid] = (src, c[2], c[3])

    cited = collections.defaultdict(lambda: collections.defaultdict(list))
    for b in briefs:
        for f in REF_FIELDS:
            for v in b.y.get(f) or []:
                cited[str(v)][f].append(b.path)
    for v, fields in sorted(cited.items()):
        if v not in ids and v not in planned:
            where = sorted({rel(p) for ps in fields.values() for p in ps})
            probs.append(f'unresolved reference {v!r} (not live, not planned) in: ' + ', '.join(where))

    for pid, (src, blocks, status) in sorted(planned.items()):
        if pid in ids:
            probs.append(f'{rel(src)}: planned {pid!r} is now written ({rel(ids[pid][0])}) — delete the row')
        if pid not in cited:
            probs.append(f'{rel(src)}: planned {pid!r} is cited by no live brief — delete the row')
        if 'dependencies' in cited.get(pid, {}) and 'parked' in (blocks + status).lower():
            probs.append(f'{rel(src)}: planned {pid!r} is a hard dependency but marked Parked')
        for b in re.findall(r'`([^`]+)`', blocks):
            if b not in ids:
                probs.append(f'{rel(src)}: planned {pid!r} blocks {b!r}, which is not a live brief')

    # consistency issues (Phase 2 gate)
    issues, n_open = {}, 0
    for src in trackers:
        for c in section_rows(src, 'Consistency Issues'):
            if not re.match(r'^[A-Z]{2,3}-\d+$', c[0]):
                continue
            if c[0] in issues:
                probs.append(f'consistency issue {c[0]} listed twice: {rel(issues[c[0]])}, {rel(src)}')
            issues[c[0]] = src
            is_open = c[3].lower().startswith('open')
            n_open += is_open
            for bid in re.findall(r'`([^`]+)`', c[1]):
                if bid not in by_id and is_open:
                    probs.append(f'{rel(src)}: {c[0]} names {bid!r}, which is not a live brief')
                elif is_open and bid in by_id and by_id[bid].gate_met >= 2:
                    probs.append(f'{rel(src)}: {c[0]} is open but `{bid}` claims gate-met phase '
                                 f'{by_id[bid].gate_met}; Phase 2 requires internal consistency')

    todo = sum(1 for _, _, s in planned.values() if not s.lower().startswith('parked'))
    print(f'{len(briefs)} briefs, {len(trackers)} trackers, {len(planned)} planned briefs '
          f'({todo} to write, {len(planned) - todo} parked), {len(issues)} consistency issues '
          f'({n_open} open)')
    for x in probs:
        print('✗', x)
    print('✓ no problems' if not probs else f'\n{len(probs)} problem(s)')
    sys.exit(1 if probs else 0)


if __name__ == '__main__':
    main()
