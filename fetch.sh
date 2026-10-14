#!/bin/bash
# Fetch English captions for every video in catalog/selection.csv (bootcamp first), throttled.
cd "$(dirname "$0")"
python3 -I -c "
import csv
rows=list(csv.DictReader(open('catalog/selection.csv',encoding='utf-8')))
rows.sort(key=lambda r:(int(r['tier']),int(r['rank'])))
for r in rows: print(r['id'], r['duration_s'], r['title'].replace('\t',' '), sep='\t')
" > catalog/fetch_queue.tsv
touch catalog/dates.tsv catalog/failed.tsv
while IFS=$'\t' read -r id dur title; do
  [ -f "transcripts/$id.md" ] && continue
  ok=0
  for attempt in 1 2 3 4; do
    out=$(yt-dlp --js-runtimes node --impersonate chrome --ignore-no-formats-error --skip-download \
      --write-subs --write-auto-subs --sub-langs "en-orig,en" --sub-format json3 \
      --extractor-args "youtube:player_client=web_embedded" --sleep-requests 1 \
      --no-simulate --print "%(upload_date)s" -o "subs/%(id)s.%(ext)s" -- "$id" 2>&1)
    date=$(echo "$out" | grep -E '^[0-9]{8}$' | head -1)
    f=$(ls subs/$id.en-orig.json3 subs/$id.en.json3 2>/dev/null | head -1)
    if [ -n "$f" ]; then
      echo -e "$id\t$date" >> catalog/dates.tsv
      python3 -I json3_to_md.py "$f" "transcripts/$id.md" "$id" "$title" "${date:-?}" "$dur" && ok=1
      break
    fi
    if echo "$out" | grep -q "429"; then sleep $((60 * attempt)); else
      echo "$out" | grep -q -i "no subtitles\|There are no" && break; sleep 10; fi
  done
  [ $ok = 0 ] && echo -e "$id\t$title\t$(echo "$out" | grep -i error | tail -1)" >> catalog/failed.tsv
  sleep $((4 + RANDOM % 6))
done < catalog/fetch_queue.tsv
echo "DONE: $(ls transcripts | wc -l) transcripts, $(wc -l < catalog/failed.tsv) failed"
