from pathlib import Path
import re

path = Path('styles.css')
text = path.read_text(encoding='utf-8')

old = '''.site-footer {
  padding: 26px clamp(18px, 5vw, 72px);
  color: var(--muted);
  border-top: 1px solid var(--line);
}

.site-footer p {
  margin: 0;
}
'''

new = '''.site-footer {
  padding: 26px clamp(18px, 5vw, 72px);
  color: var(--green);
  border-top: 1px solid var(--line);
  text-align: center;
}

.site-footer nav {
  margin: 0 auto 8px;
  text-align: center;
}

.site-footer a,
.site-footer p {
  color: var(--green);
}

.site-footer p {
  margin: 0;
  text-align: center;
}
'''

if old not in text:
    raise SystemExit('Expected footer CSS block was not found')

text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
