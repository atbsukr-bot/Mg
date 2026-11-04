set -e
# cuts every piece from its own source file (raw.mov or an insert clip in raw/) -> aroll.mp4 (30 fps)
cd /home/claude/proj/raw; mkdir -p parts; rm -f parts/*
python3 -c "
import json;P=json.load(open('pieces.json'))['pieces']
for i,p in enumerate(P): print(i,p['s'],p['e']-p['s'],('raw.mov' if p.get('src','raw')=='raw' else p['src']),p['kind'])" > parts/list.txt
: > parts/v.txt; : > parts/a.txt
# colour correction for his own footage (scripts/grade.txt); inserts keep their own look
GRADE=$(cat /home/claude/proj/scripts/grade.txt 2>/dev/null || true)
while read i s d src kind; do
  n=$(printf %03d $i)
  VF="fps=30,"; [ "$kind" != "insert" ] && [ -n "$GRADE" ] && VF="fps=30,$GRADE,"
  ffmpeg -nostdin -y -v error -ss $s -i "$src" -t $d -map 0:v:0 -vf "${VF}scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -g 30 -an parts/v$n.mp4
  nf=$(ffprobe -v error -select_streams v -show_entries stream=nb_frames -of csv=p=0 parts/v$n.mp4 | tr -d ',\n')
  d=$(python3 -c "print($nf/30)")   # audio length = exact video length (no drift)
  f=$(python3 -c "print(min(0.02,$d/4))"); st=$(python3 -c "print($d-min(0.02,$d/4))")
  if [ "$kind" = "insert" ]; then
    # inserts keep their own (already mixed) sound; tag so cleanup filters are skipped
    ffmpeg -nostdin -y -v error -ss $s -i "$src" -t $d -map 0:a:0 -ac 1 -ar 48000 -af "apad,atrim=0:$d,afade=t=in:d=0.05,afade=t=out:st=$(python3 -c "print($d-0.08)"):d=0.08,loudnorm=I=-17:TP=-2" -ar 48000 parts/a$n.wav
  else
    ffmpeg -nostdin -y -v error -ss $s -i "$src" -t $d -map 0:a:0 -ac 1 -ar 48000 -af "apad,atrim=0:$d,highpass=f=75,afftdn=nf=-28,afade=t=in:d=$f,afade=t=out:st=$st:d=$f" parts/a$n.wav
  fi
  echo "file 'v$n.mp4'" >> parts/v.txt; echo "file 'a$n.wav'" >> parts/a.txt
  echo "part $i done"
done < parts/list.txt
ffmpeg -y -v error -f concat -safe 0 -i parts/v.txt -c copy parts/vcat.mp4
ffmpeg -y -v error -f concat -safe 0 -i parts/a.txt -af "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,loudnorm=I=-15:TP=-1.5:LRA=9,aresample=48000" -ar 48000 parts/acat.wav
ffmpeg -y -v error -i parts/vcat.mp4 -i parts/acat.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest /home/claude/proj/raw/aroll.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 /home/claude/proj/raw/aroll.mp4
echo ALLDONE
