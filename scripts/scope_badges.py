from pathlib import Path
import re

# Exterior-cleaning pages: keep only the licensed/insured badge.
for filename, service in [
    ('nocatee-house-washing.html', 'house washing'),
    ('nocatee-roof-washing.html', 'roof washing'),
]:
    path = Path(filename)
    html = path.read_text(encoding='utf-8')

    # Remove paver-specific Trident certification and paver-warranty artwork.
    html = re.sub(
        r'\s*<img[^>]+src="/Trident-Master\.jpg"[^>]*>',
        '',
        html,
        flags=re.I,
    )
    html = re.sub(
        r'\s*<img[^>]+src="/hydroseal-2-year-warranty\.png"[^>]*>',
        '',
        html,
        flags=re.I,
    )

    scope = (
        f'<p class="cert-scope">Licensed and insured for {service}. '
        'Trident Master certification and the two-year warranty relate to qualifying '
        'paver sealing work and do not apply to exterior-cleaning services.</p>'
    )
    if 'do not apply to exterior-cleaning services' not in html:
        # Place the statement immediately after the certification badge container.
        html = re.sub(
            r'(</div>\s*</div>\s*</section>)',
            r'\1' + scope,
            html,
            count=1,
            flags=re.I,
        )

    path.write_text(html, encoding='utf-8')

# Homepage: visibly scope the warranty to paver sealing and clarify alt text.
path = Path('index.html')
html = path.read_text(encoding='utf-8')
html = html.replace('alt="HydroSeal 2-Year Warranty"', 'alt="HydroSeal 2-Year Paver Sealing Warranty"')
html = html.replace('alt="2-Year Warranty"', 'alt="2-Year Paver Sealing Warranty"')
if 'Two-year warranty applies to qualifying paver sealing projects.' not in html:
    marker = '<img src="/hydroseal-2-year-warranty.png"'
    pos = html.find(marker)
    if pos != -1:
        end = html.find('>', pos)
        html = html[:end+1] + '<p class="cert-scope">Two-year warranty applies to qualifying paver sealing projects.</p>' + html[end+1:]
path.write_text(html, encoding='utf-8')

# Warranty page: state what is outside the program in plain language.
path = Path('warranty.html')
html = path.read_text(encoding='utf-8')
scope_sentence = (
    '<p><strong>Scope:</strong> This warranty applies to qualifying paver sealing work only. '
    'House washing, roof washing and other exterior-cleaning services are not covered by this warranty.</p>'
)
if 'other exterior-cleaning services are not covered by this warranty' not in html:
    anchor = 'The signed proposal, invoice and project-specific warranty control if their terms differ from this summary.</p>'
    html = html.replace(anchor, anchor + scope_sentence)
path.write_text(html, encoding='utf-8')

# Add a small shared style for the visible scope statements.
path = Path('styles.css')
css = path.read_text(encoding='utf-8')
if '.cert-scope' not in css:
    css += '\n.cert-scope { max-width: 760px; margin: 12px auto 0; padding: 0 18px; text-align: center; font-size: 0.9rem; line-height: 1.5; opacity: 0.82; }\n'
path.write_text(css, encoding='utf-8')
