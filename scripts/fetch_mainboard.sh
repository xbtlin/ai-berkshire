#!/bin/bash
# 拉取 A股主板全量列表（沪60 + 深00，排除688/300/8xx/4xx）
cd "$(dirname "$0")"
mkdir -p /tmp/mb_pages
URL='https://push2.eastmoney.com/api/qt/clist/get'
FIELDS='f2,f3,f5,f6,f8,f9,f10,f12,f14,f20,f21,f22,f23,f24,f25,f26,f62,f100'
for pn in $(seq 1 19); do
  out="/tmp/mb_pages/page_${pn}.json"
  if [ -s "$out" ]; then continue; fi
  curl -s --retry 6 --retry-delay 2 --retry-all-errors \
    -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' \
    "${URL}?pn=${pn}&pz=200&po=1&np=1&fltt=2&invt=2&fid=f20&fs=m:1%2Bt:2,m:0%2Bt:6&fields=${FIELDS}" \
    -o "$out"
  sleep 0.4
done
# 统计成功页
ok=0; total=0
for f in /tmp/mb_pages/page_*.json; do
  if grep -q '"diff"' "$f" 2>/dev/null; then ok=$((ok+1)); fi
done
echo "OK pages: $ok / 19"
