from pathlib import Path
import json, re

ROOT = Path('.')
PAGES = {
    'nocatee-driveway-paver-sealing.html': ('Driveway Paver Sealing', 'Driveway paver cleaning, joint-sand replacement and sealing'),
    'nocatee-pool-deck-paver-sealing.html': ('Pool Deck Paver Sealing', 'Pool deck paver cleaning, joint-sand replacement and sealing'),
    'nocatee-travertine-sealing.html': ('Travertine Sealing', 'Travertine and natural-stone cleaning and sealing'),
    'nocatee-house-washing.html': ('House Washing', 'Soft-wash exterior house cleaning'),
    'nocatee-roof-washing.html': ('Roof Washing', 'Soft-wash roof cleaning'),
    'paver-sealing-cost-calculator.html': ('Paver Sealing Cost Calculator', 'Paver sealing cost estimation tool'),
}

def text_only(s: str) -> str:
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def extract(pattern, html, default=''):
    m = re.search(pattern, html, re.I | re.S)
    return text_only(m.group(1)) if m else default

def build_graph(html: str, label: str, service_type: str):
    canonical = extract(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', html)
    title = extract(r'<title>(.*?)</title>', html, label)
    description = extract(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', html)
    h1 = extract(r'<h1[^>]*>(.*?)</h1>', html, label)
    faq = []
    for q, a in re.findall(r'<details[^>]*class=["\'][^"\']*faq[^"\']*["\'][^>]*>\s*<summary[^>]*>(.*?)</summary>\s*<p[^>]*>(.*?)</p>', html, re.I | re.S):
        faq.append({'@type':'Question','name':text_only(q),'acceptedAnswer':{'@type':'Answer','text':text_only(a)}})
    graph = [
        {'@type':'WebPage','@id':canonical + '#webpage','url':canonical,'name':title,'description':description,'about':{'@id':'https://hydrosealpavers.com/#business'},'breadcrumb':{'@id':canonical + '#breadcrumb'}},
        {'@type':'Service','@id':canonical + '#service','name':h1 or label,'serviceType':service_type,'url':canonical,'provider':{'@id':'https://hydrosealpavers.com/#business'},'areaServed':[{'@type':'Place','name':'Nocatee, Florida'},{'@type':'Place','name':'Ponte Vedra, Florida'},{'@type':'AdministrativeArea','name':'St. Johns County, Florida'}]},
        {'@type':'BreadcrumbList','@id':canonical + '#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://nocateepaversealing.com/'},{'@type':'ListItem','position':2,'name':label,'item':canonical}]}
    ]
    if faq:
        graph.append({'@type':'FAQPage','@id':canonical + '#faq','mainEntity':faq})
    return json.dumps({'@context':'https://schema.org','@graph':graph}, separators=(',', ':'))

shared_css = '''
/* Shared utility styles used across service pages */
.breadcrumbs{width:min(100% - 36px,1180px);margin:18px auto 0;color:var(--muted);font-size:.92rem}.breadcrumbs a{color:var(--green-dark);font-weight:750}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.price-table-wrap{overflow-x:auto;margin:28px 0 18px;border:1px solid var(--line);border-radius:20px}.price-table{width:100%;min-width:580px;border-collapse:collapse;background:var(--panel)}.price-table th,.price-table td{padding:14px 18px;border-bottom:1px solid var(--line);text-align:left}.price-table th{color:#fff;background:var(--green-dark)}.price-table tr:last-child td{border-bottom:0}.pricing-note,.price-note{max-width:920px;font-size:.95rem}.hood-grid,.area-grid{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.hood-grid span,.area-grid span{padding:6px 13px;border:1px solid var(--line);border-radius:999px;font-size:.88rem}.callout{border-left:4px solid currentColor;padding:4px 0 4px 18px;margin:22px 0}.nap{font-size:.95rem;line-height:1.7}
'''
css = Path('styles.css').read_text(encoding='utf-8')
if 'Shared utility styles used across service pages' not in css:
    Path('styles.css').write_text(css.rstrip() + '\n' + shared_css, encoding='utf-8')

for filename, (label, service_type) in PAGES.items():
    path = Path(filename)
    if not path.exists():
        continue
    html = path.read_text(encoding='utf-8')
    html = re.sub(r'<h1([^>]*)>(.*?)</h1>', lambda m: '<h1'+m.group(1)+'>'+re.sub(r'\s*<br\s*/?>\s*',' ',m.group(2),flags=re.I).strip()+'</h1>', html, flags=re.I|re.S)
    graph = build_graph(html, label, service_type)
    block = '<script type="application/ld+json">\n      ' + graph + '\n    </script>'
    if re.search(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>', html, re.I|re.S):
        html = re.sub(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>', block, html, count=1, flags=re.I|re.S)
    else:
        html = html.replace('</head>', '    '+block+'\n  </head>', 1)
    path.write_text(html, encoding='utf-8')

# Replace the oversized pool-deck hero with a generated WebP when available.
pool = Path('nocatee-pool-deck-paver-sealing.html')
if pool.exists() and Path('resealed-pavers.webp').exists():
    html = pool.read_text(encoding='utf-8').replace('/resealed-pavers.jpg','/resealed-pavers.webp')
    pool.write_text(html, encoding='utf-8')

# Deploy the existing joint-sand page when present by adding it to sitemap and homepage/footer navigation.
if Path('nocatee-paver-joint-sand.html').exists():
    sitemap = Path('sitemap.xml')
    if sitemap.exists():
        s = sitemap.read_text(encoding='utf-8')
        url = 'https://nocateepaversealing.com/nocatee-paver-joint-sand'
        if url not in s:
            s = s.replace('</urlset>', f'  <url><loc>{url}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
            sitemap.write_text(s, encoding='utf-8')

# Remove confirmed-unused legacy image.
Path('nocatee-paver-sealing.png').unlink(missing_ok=True)
