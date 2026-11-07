from pathlib import Path
for name in ['deck-build.txt','rehearsal-process.txt','baseline-browser-process.txt']:
 p=Path('documentation/m11')/name
 print(name, p.read_text(encoding='utf-8-sig')[-4000:] if p.exists() else 'MISSING')
