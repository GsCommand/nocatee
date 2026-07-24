from pathlib import Path
import re

pages = [
    'index.html',
    'nocatee-driveway-paver-sealing.html',
    'nocatee-pool-deck-paver-sealing.html',
    'nocatee-travertine-sealing.html',
    'nocatee-house-washing.html',
    'nocatee-roof-washing.html',
    'paver-sealing-cost-calculator.html',
]

for filename in pages:
    path = Path(filename)
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')

    # Replace personal Gmail quote CTAs with branded quote page.
    text = re.sub(r'href="mailto:outletdirect229@gmail\.com\?subject=[^"]*"', 'href="https://hydrosealpavers.com/get-a-quote"', text)

    # Normalize internal links to extensionless URLs.
    text = re.sub(r'href="(/[^"#?]+)\.html([#?][^"]*)?"', lambda m: f'href="{m.group(1)}{m.group(2) or ""}"', text)

    # Normalize canonical URLs to non-www, extensionless form.
    def canonical_fix(match):
        url = match.group(1).replace('https://www.nocateepaversealing.com', 'https://nocateepaversealing.com')
        url = re.sub(r'\.html(?=$|[?#])', '', url)
        return f'<link rel="canonical" href="{url}" />'
    text = re.sub(r'<link rel="canonical" href="([^"]+)"\s*/?>', canonical_fix, text)

    # Correct known hero preloads.
    if filename == 'nocatee-travertine-sealing.html':
        text = re.sub(r'<link rel="preload" as="image" href="[^"]*nocatee-travertine-sealing\.jpeg"[^>]*>', '<link rel="preload" as="image" href="/travertine-sealing-nocatee.webp" type="image/webp" />', text)
    if filename == 'nocatee-pool-deck-paver-sealing.html':
        # Remove oversized stale preload when it does not match the rendered hero.
        text = re.sub(r'\s*<link rel="preload" as="image" href="/resealed-pavers\.jpg"[^>]*>\s*', '\n', text)

    # Ensure Elfsight platform is loaded once per page.
    matches = list(re.finditer(r'<script src="https://elfsightcdn\.com/platform\.js"[^>]*></script>', text))
    if len(matches) > 1:
        first_end = matches[0].end()
        before = text[:first_end]
        after = text[first_end:]
        after = re.sub(r'\s*<script src="https://elfsightcdn\.com/platform\.js"[^>]*></script>', '', after)
        text = before + after

    # Add consistent main-domain attribution to non-homepage footers.
    if filename != 'index.html' and 'Visit HydroSeal Pavers' not in text:
        text = text.replace(
            '<p>&copy; 2026 HydroSeal',
            '<p><a href="https://hydrosealpavers.com/">Visit HydroSeal Pavers</a></p>\n      <p>&copy; 2026 HydroSeal',
            1,
        )

    # Add visible breadcrumb navigation to service/calculator pages.
    if filename != 'index.html' and 'class="breadcrumbs"' not in text:
        label_map = {
            'nocatee-driveway-paver-sealing.html': 'Driveway Paver Sealing',
            'nocatee-pool-deck-paver-sealing.html': 'Pool Deck Paver Sealing',
            'nocatee-travertine-sealing.html': 'Travertine Sealing',
            'nocatee-house-washing.html': 'House Washing',
            'nocatee-roof-washing.html': 'Roof Washing',
            'paver-sealing-cost-calculator.html': 'Paver Sealing Cost Calculator',
        }
        label = label_map.get(filename, 'Service')
        crumb = f'\n    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true"> / </span><span aria-current="page">{label}</span></nav>\n'
        text = text.replace('<main', crumb + '    <main', 1)

    # Replace weak roof-washing headline.
    if filename == 'nocatee-roof-washing.html':
        text = text.replace('Roof washing should never sound aggressive.', 'Safe soft-wash roof cleaning for Nocatee homes')

    path.write_text(text, encoding='utf-8')

# Rebuild sitemap with extensionless canonical URLs.
sitemap = Path('sitemap.xml')
if sitemap.exists():
    text = sitemap.read_text(encoding='utf-8')
    text = text.replace('https://www.nocateepaversealing.com', 'https://nocateepaversealing.com')
    text = re.sub(r'\.html(?=</loc>)', '', text)
    sitemap.write_text(text, encoding='utf-8')
