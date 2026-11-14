#!/bin/bash
# Daily AI briefing: compose vertical video from cards + dubbed audio (9:16)
set -e
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CARDS="$BASE/output/cards"
AUD="$BASE/assets"
SEG="$BASE/output/seg"
mkdir -p "$SEG"

# 顺序：卡片 配音
PAIRS=(
  "00_intro.png:intro.wav"
  "01_news01.png:n1.wav"
  "02_news02.png:n2.wav"
  "03_news03.png:n3.wav"
  "04_news04.png:n4.wav"
  "05_news05.png:n5.wav"
  "06_outro.png:outro.wav"
)

CONCAT="$SEG/concat.txt"
: > "$CONCAT"

i=0
for pair in "${PAIRS[@]}"; do
  card="${pair%%:*}"; aud="${pair##*:}"
  seg="$SEG/seg_$i.mp4"
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUD/$aud")
  ffmpeg -y -loop 1 -i "$CARDS/$card" -i "$AUD/$aud" -t "$dur" \
    -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -tune stillimage -pix_fmt yuv420p -r 30 \
    -c:a aac -b:a 192k -ar 44100 -ac 2 \
    "$seg"
  echo "file '$seg'" >> "$CONCAT"
  i=$((i+1))
done

OUT="$BASE/output/ai-news-briefing_$(date +%Y-%m-%d).mp4"
ffmpeg -y -f concat -safe 0 -i "$CONCAT" -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 44100 -ac 2 "$OUT"

echo "=== done ==="
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT"
echo "$OUT"
