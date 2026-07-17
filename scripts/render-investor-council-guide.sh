#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/assets/tutorial/investor-council-guide"
output_dir="$repo_root/public/media"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

mkdir -p "$output_dir"

render_svg() {
  local source_file="$1"
  local output_file="$2"

  if command -v rsvg-convert >/dev/null 2>&1; then
    rsvg-convert --width 720 --height 720 --output "$output_file" "$source_file"
  elif command -v qlmanage >/dev/null 2>&1; then
    qlmanage -t -s 720 -o "$work_dir" "$source_file" >/dev/null 2>&1
    mv "$work_dir/$(basename "$source_file").png" "$output_file"
  elif command -v magick >/dev/null 2>&1; then
    magick -background none "$source_file" -resize 720x720 "$output_file"
  else
    echo "SVG renderer required: install librsvg, ImageMagick, or run on macOS." >&2
    exit 1
  fi
}

for scene_number in 01 02 03 04 05; do
  render_svg \
    "$source_dir/scene-$scene_number.svg" \
    "$work_dir/scene-$scene_number.png"
done

ffmpeg -hide_banner -loglevel error -y \
  -loop 1 -framerate 30 -t 5 -i "$work_dir/scene-01.png" \
  -loop 1 -framerate 30 -t 5 -i "$work_dir/scene-02.png" \
  -loop 1 -framerate 30 -t 5 -i "$work_dir/scene-03.png" \
  -loop 1 -framerate 30 -t 5 -i "$work_dir/scene-04.png" \
  -loop 1 -framerate 30 -t 5 -i "$work_dir/scene-05.png" \
  -filter_complex \
    "[0:v][1:v]xfade=transition=fade:duration=0.4:offset=4.6[v1];\
     [v1][2:v]xfade=transition=fade:duration=0.4:offset=9.2[v2];\
     [v2][3:v]xfade=transition=fade:duration=0.4:offset=13.8[v3];\
     [v3][4:v]xfade=transition=fade:duration=0.4:offset=18.4,format=yuv420p[vout]" \
  -map "[vout]" -an -c:v libx264 -preset slow -crf 23 \
  -profile:v high -level 4.0 -movflags +faststart \
  "$output_dir/investor-council-guide.mp4"

ffmpeg -hide_banner -loglevel error -y \
  -i "$work_dir/scene-01.png" -frames:v 1 -q:v 3 \
  "$output_dir/investor-council-guide-poster.jpg"

printf 'Rendered %s\n' "$output_dir/investor-council-guide.mp4"
