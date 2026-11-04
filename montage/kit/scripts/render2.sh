cd /home/claude/proj/app
N=$(python3 -c "import json;print(json.load(open('public/edl.json'))['duration'])"); STEP=400; i=0; k=0
: > out/chunks.txt
while [ $i -lt $N ]; do
  e=$((i+STEP-1)); [ $e -ge $N ] && e=$((N-1))
  n=$(printf %02d $k)
  for try in 1 2 3; do
    npx remotion render build Main out/k$n.mp4 --frames=$i-$e --muted --codec=h264 --crf=17 --props='{"edlFile":"edl.json","noAudio":true}' --timeout=120000 --log=error > out/k$n.log 2>&1 && break
    echo "retry $n"
  done
  [ -f out/k$n.mp4 ] && echo "chunk $n ok ($i-$e)" || echo "chunk $n FAILED"
  echo "file 'k$n.mp4'" >> out/chunks.txt
  i=$((e+1)); k=$((k+1))
done

echo FINISHED
