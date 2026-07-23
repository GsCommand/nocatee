from pathlib import Path
import re

FOOTER = '''<footer class="site-footer">
      <nav aria-label="Footer navigation">
        <a href="/nocatee-driveway-paver-sealing">Driveway Paver Sealing</a> &middot;
        <a href="/nocatee-pool-deck-paver-sealing">Pool Deck Sealing</a> &middot;
        <a href="/nocatee-travertine-sealing">Travertine Sealing</a> &middot;
        <a href="/nocatee-house-washing">House Washing</a> &middot;
        <a href="/nocatee-roof-washing">Roof Washing</a> &middot;
        <a href="/paver-sealing-cost-calculator">Cost Calculator</a>
      </nav>
      <p>&copy; 2026 HydroSeal &middot; Nocatee Paver Sealing &middot; Serving Nocatee, Ponte Vedra &amp; St. Johns County, FL</p>
    </footer>'''

pattern = re.compile(r'<footer\s+class=["\']site-footer["\'][^>]*>.*?</footer>', re.IGNORECASE | re.DOTALL)
changed = []

for path in sorted(Path('.').glob('*.html')):
    text = path.read_text(encoding='utf-8')
    if not pattern.search(text):
        continue
    updated, count = pattern.subn(FOOTER, text, count=1)
    if count != 1:
        raise SystemExit(f'Expected one footer in {path}, found {count}')
    if updated != text:
        path.write_text(updated, encoding='utf-8')
        changed.append(path.name)

if not changed:
    raise SystemExit('No footer markup needed restoration')

print('Updated:', ', '.join(changed))
