"""Render a team Markdown file (Arabic, RTL) to a clean PDF with Chromium.
Usage: python3 tools/md2pdf.py input.md output.pdf "عنوان الغلاف"
"""
import re, sys, html, subprocess, pathlib, json
src, out = sys.argv[1], sys.argv[2]
FONTS = pathlib.Path('/home/user/Mg/montage/ep001/public/fonts').resolve()
md = open(src, encoding='utf-8').read()

def inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    return t

out_html, lines, i = [], md.splitlines(), 0
while i < len(lines):
    l = lines[i]
    if not l.strip(): i += 1; continue
    if l.startswith('```'):
        j = i + 1; buf = []
        while j < len(lines) and not lines[j].startswith('```'): buf.append(html.escape(lines[j])); j += 1
        out_html.append('<pre>' + '\n'.join(buf) + '</pre>'); i = j + 1; continue
    if l.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells): rows.append(cells)
            i += 1
        t = '<table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in rows[0]) + '</tr></thead><tbody>'
        t += ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</tbody></table>'
        out_html.append(t); continue
    m = re.match(r'^(#{1,3})\s+(.*)', l)
    if m:
        lvl = len(m.group(1)); out_html.append(f'<h{lvl}>{inline(m.group(2))}</h{lvl}>'); i += 1; continue
    if l.strip() == '---': out_html.append('<hr>'); i += 1; continue
    if l.startswith('🎬'):
        out_html.append(f'<div class="cue"><span>تصوير</span>{inline(l[1:].strip())}</div>'); i += 1; continue
    if l.startswith('>'):
        buf = []
        while i < len(lines) and lines[i].startswith('>'): buf.append(inline(lines[i][1:].strip())); i += 1
        out_html.append('<blockquote>' + '<br>'.join(buf) + '</blockquote>'); continue
    if re.match(r'^\s*([-*]|\d+\.)\s', l):
        tag = 'ol' if re.match(r'^\s*\d+\.', l) else 'ul'; buf = []
        while i < len(lines) and re.match(r'^\s*([-*]|\d+\.)\s', lines[i]):
            buf.append('<li>' + inline(re.sub(r'^\s*([-*]|\d+\.)\s', '', lines[i])) + '</li>'); i += 1
        out_html.append(f'<{tag}>' + ''.join(buf) + f'</{tag}>'); continue
    out_html.append(f'<p>{inline(l)}</p>'); i += 1

css = f"""
@font-face {{ font-family: Cairo; src: url('file://{FONTS}/Cairo.ttf'); font-weight: 200 1000; }}
@font-face {{ font-family: Tajawal; src: url('file://{FONTS}/Tajawal-Black.ttf'); font-weight: 900; }}
@page {{ size: A4; margin: 18mm 16mm 20mm; }}
body {{ font-family: Cairo, 'Noto Color Emoji', sans-serif; direction: rtl; color: #15181d; font-size: 13.5pt; line-height: 1.95; }}
h1 {{ font-family: Tajawal; font-weight: 900; font-size: 24pt; color: #8f1d17; border-bottom: 4px solid #8f1d17; padding-bottom: 6px; margin: 0 0 14px; }}
h2 {{ font-family: Tajawal; font-weight: 900; font-size: 16pt; color: #15181d; background: #f2eadb; border-right: 6px solid #c8261e; padding: 4px 12px; margin: 26px 0 10px; page-break-after: avoid; }}
h3 {{ font-size: 13pt; margin: 18px 0 6px; }}
p {{ margin: 0 0 10px; text-align: justify; }}
.cue {{ font-size: 10.5pt; color: #5b6170; background: #f1f3f6; border-radius: 6px; padding: 4px 10px; margin: 6px 0 12px; line-height: 1.6; }}
.cue span {{ background: #5b6170; color: #fff; border-radius: 4px; padding: 0 6px; margin-left: 8px; font-weight: 700; }}
blockquote {{ margin: 8px 0 14px; padding: 8px 14px; background: #fff7e0; border-right: 5px solid #e3b21b; font-weight: 700; }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0 16px; font-size: 11pt; page-break-inside: avoid; }}
th, td {{ border: 1px solid #cfc7b5; padding: 5px 8px; text-align: right; vertical-align: top; }}
th {{ background: #f2eadb; }}
hr {{ border: 0; border-top: 1px dashed #bbb; margin: 18px 0; }}
code {{ font-family: monospace; font-size: 10pt; background: #f1f1f1; padding: 0 4px; }}
pre {{ background: #f6f6f6; padding: 10px; white-space: pre-wrap; font-family: Cairo; }}
ul, ol {{ margin: 0 0 10px; padding-right: 22px; }}
"""
doc = f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(out_html)}</body></html>"
tmp = pathlib.Path(out).with_suffix('.html'); tmp.write_text(doc, encoding='utf-8')
js = f"""
const {{chromium}} = require('playwright');
(async () => {{
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://{tmp.resolve()}'); await p.evaluate(() => document.fonts.ready);
  await p.pdf({{path: {json.dumps(str(pathlib.Path(out).resolve()))}, format: 'A4', printBackground: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;text-align:center;font-size:9px;color:#888">MN Cousins · Mg — <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: {{top: '18mm', bottom: '20mm', left: '16mm', right: '16mm'}} }});
  await b.close();
}})();
"""
subprocess.run(['node', '-e', js], check=True)
tmp.unlink()
print('ok', out)
