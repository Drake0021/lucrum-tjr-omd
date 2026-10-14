"""Group downloaded, not-yet-noted, non-bootcamp transcripts into ~45k-word batches.
Appends to catalog/other_batches.tsv (batch, video_id, words, title); prints new batch ids."""
import csv, os, re
sel = {r['id']: r for r in csv.DictReader(open('catalog/selection.csv', encoding='utf-8'))}
done = set()
if os.path.exists('catalog/other_batches.tsv'):
    for l in open('catalog/other_batches.tsv'):
        done.add(l.split('\t')[1])
start = max([int(l.split('\t')[0]) for l in open('catalog/other_batches.tsv')] or [100]) + 1 if done else 101
todo = []
for f in sorted(os.listdir('transcripts')):
    vid = f[:-3]
    if vid not in sel or sel[vid]['tier'] == '0' or vid in done or os.path.exists(f'notes/{vid}.md'):
        continue
    words = int(re.search(r'words: (\d+)', open('transcripts/' + f).read(400)).group(1))
    todo.append((int(sel[vid]['tier']), int(sel[vid]['rank']), vid, words, sel[vid]['title']))
todo.sort()
b, cur, out = start, 0, []
for t in todo:
    if cur and cur + t[3] > 45000:
        b += 1; cur = 0
    out.append((b, t[2], t[3], t[4])); cur += t[3]
with open('catalog/other_batches.tsv', 'a') as f:
    for r in out:
        f.write('\t'.join(map(str, r)) + '\n')
print(sorted({r[0] for r in out}), len(out), 'videos')
