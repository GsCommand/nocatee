from pathlib import Path
import json, re

path = Path('nocatee-driveway-paver-sealing.html')
html = path.read_text(encoding='utf-8')

def clean(value):
    value = re.sub(r'<[^>]+>', ' ', value)
    return re.sub(r'\s+', ' ', value).strip()

faqs = []
for details in re.findall(r'<details\b[^>]*>.*?</details>', html, re.I | re.S):
    q = re.search(r'<summary[^>]*>(.*?)</summary>', details, re.I | re.S)
    a = re.search(r'<p[^>]*>(.*?)</p>', details, re.I | re.S)
    if q and a:
        faqs.append({'@type':'Question','name':clean(q.group(1)),'acceptedAnswer':{'@type':'Answer','text':clean(a.group(1))}})

if len(faqs) != 8:
    raise SystemExit(f'Expected 8 visible driveway FAQs, found {len(faqs)}')

match = re.search(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>\s*(\{.*?\})\s*</script>', html, re.I | re.S)
if not match:
    raise SystemExit('No JSON-LD block found')
data = json.loads(match.group(1))
graph = data.get('@graph', [])
graph = [item for item in graph if item.get('@type') != 'FAQPage']
canonical = 'https://nocateepaversealing.com/nocatee-driveway-paver-sealing'
graph.append({'@type':'FAQPage','@id':canonical+'#faq','mainEntity':faqs})
data['@graph'] = graph
replacement = '<script type="application/ld+json">\n      ' + json.dumps(data, separators=(',', ':')) + '\n    </script>'
html = html[:match.start()] + replacement + html[match.end():]
path.write_text(html, encoding='utf-8')
