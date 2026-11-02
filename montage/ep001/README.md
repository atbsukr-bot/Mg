# ep001 — «بلاغ بلا عنوان» (شورت تجريبي)

مشروع Remotion. المصدر هو IMG_0259.MOV من مجلد Mg-team على Drive، وما ينرفع للمستودع.

## خطوات البناء
1. `python3 scripts/build_aroll.py`: يعدّل اتجاه الفيديو، ويتتبع الوجه، ويقص الوقفات. الناتج `public/aroll.mp4`.
2. `python3 scripts/make_sfx.py`: يركّب كل المؤثرات الصوتية والخلفية من الصفر.
3. `python3 scripts/make_edl.py`: ينفّذ خطة المشاهد ويكتب `public/edl.json`.
4. `npx remotion render src/index.ts Short out/ep001-short.mp4 --codec=h264 --crf=18`

## الخطوط والتراخيص
- **الخطوط:** Tajawal و Cairo و Reem Kufi، وكلها بترخيص مفتوح (OFL). ملفات الترخيص في `public/fonts/`.
- **المؤثرات الصوتية:** مولّدة بالكود، فما عليها أي حقوق.
