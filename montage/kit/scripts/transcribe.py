"""python3 transcribe.py audio16k.wav transcript.json [model] [prompt]
model default: large-v3-turbo (int8). Do NOT use large-v3 (OOM)."""
import json, sys, time
from faster_whisper import WhisperModel
import soundfile as sf
t = time.time()
model = sys.argv[3] if len(sys.argv) > 3 else 'large-v3-turbo'
prompt = sys.argv[4] if len(sys.argv) > 4 else 'السلام عليكم، معكم ماجد في مقطع جديد. كلاود، مونتاج على طريقة ماجد، السكيل، الشورتات، الصورة المصغرة، القيتار.'
m = WhisperModel(model, device='cpu', compute_type='int8', cpu_threads=4)
audio, _ = sf.read(sys.argv[1], dtype='float32')
segs, info = m.transcribe(audio, language='ar', word_timestamps=True, beam_size=5,
                          condition_on_previous_text=False, initial_prompt=prompt)
out = []
for s in segs:
    out.append({'start': s.start, 'end': s.end, 'text': s.text,
                'words': [{'w': w.word, 's': w.start, 'e': w.end, 'p': w.probability} for w in s.words]})
    print(f'{s.start:7.2f}-{s.end:7.2f} {s.text}', flush=True)
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False)
print('DONE', time.time() - t)
