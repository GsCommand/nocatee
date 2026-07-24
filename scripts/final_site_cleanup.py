from pathlib import Path
import json, re

ROOT = Path('.')
PAGES = [
    'index.html',
    'nocatee-driveway-paver-sealing.html',
    'nocatee-pool-deck-paver-sealing.html',
    'nocatee-travertine-sealing.html',
    'nocatee-house-washing.html',
    'nocatee-roof-washing.html',
    'paver-sealing-cost-calculator.html',
]
INLINE_REDUNDANT = {
    'index.html',
    'nocatee-driveway-paver-sealing.html',
    'nocatee-pool-deck-paver-sealing.html',
    'nocatee-travertine-sealing.html',
    'nocatee-house-washing.html',
}

NAV_JOINT = '<a href="/nocatee-paver-joint-sand">Joint Sand</a>'
FOOTER_EXTRA = ' &middot;\n        <a href="/nocatee-paver-joint-sand">Joint Sand</a> &middot;\n        <a href="/warranty">Warranty</a> &middot;\n        <a href="/privacy-policy">Privacy</a>'

for name in PAGES:
    path = ROOT / name
    html = path.read_text(encoding='utf-8')
    if name in INLINE_REDUNDANT:
        html = re.sub(r'\n\s*<style>.*?</style>', '', html, count=1, flags=re.S | re.I)
    if NAV_JOINT not in html:
        html = html.replace('<a href="/paver-sealing-cost-calculator">Cost Calculator</a>', '<a href="/nocatee-paver-joint-sand">Joint Sand</a><a href="/paver-sealing-cost-calculator">Cost Calculator</a>')
    if '<a href="/privacy-policy">Privacy</a>' not in html:
        html = html.replace('<a href="/paver-sealing-cost-calculator">Cost Calculator</a>\n      </nav>', '<a href="/paver-sealing-cost-calculator">Cost Calculator</a>' + FOOTER_EXTRA + '\n      </nav>')
        html = html.replace('<a href="/paver-sealing-cost-calculator">Cost Calculator</a></nav>', '<a href="/paver-sealing-cost-calculator">Cost Calculator</a>' + FOOTER_EXTRA + '</nav>')
    path.write_text(html, encoding='utf-8')

# Remove address entirely from homepage LocalBusiness schema and drop homepage breadcrumb schema if present.
index = Path('index.html')
html = index.read_text(encoding='utf-8')
match = re.search(r'<script[^>]+type="application/ld\+json"[^>]*>\s*(\{.*?\})\s*</script>', html, re.S | re.I)
if match:
    data = json.loads(match.group(1))
    graph = data.get('@graph', [])
    cleaned = []
    for entity in graph:
        if entity.get('@type') == 'BreadcrumbList':
            continue
        if entity.get('@type') == 'LocalBusiness':
            entity.pop('address', None)
        if entity.get('@type') == 'WebPage':
            entity.pop('breadcrumb', None)
        cleaned.append(entity)
    data['@graph'] = cleaned
    replacement = '<script type="application/ld+json">\n    ' + json.dumps(data, separators=(',', ':')) + '\n    </script>'
    html = html[:match.start()] + replacement + html[match.end():]
index.write_text(html, encoding='utf-8')

# Expand roof-washing page with useful local content and remove the old editorial sentence.
roof = Path('nocatee-roof-washing.html')
html = roof.read_text(encoding='utf-8')
old = re.search(r'<section class="section split"><div><p class="eyebrow">Soft wash roof cleaning</p>.*?</section>', html, re.S)
roof_content = '''<section class="section">
        <p class="eyebrow">Soft wash roof cleaning</p>
        <h2>Safe soft-wash roof cleaning for Nocatee homes</h2>
        <p>Nocatee roof washing should remove organic staining without relying on aggressive pressure. Florida humidity, shade, tree cover and warm temperatures can support algae and mildew on asphalt shingles, tile and other roof surfaces. HydroSeal evaluates the roof material, visible condition, access, pitch, runoff paths and surrounding landscaping before recommending service.</p>
        <p>Black streaks are commonly associated with organic growth, but not every dark area is a cleaning problem. Worn shingles, granule loss, oxidation, damaged flashing, old repairs and permanent discoloration may remain after washing. A roof cleaning estimate should separate treatable buildup from conditions that require a roofer or other repair professional.</p>
      </section>
      <section class="section split">
        <div><p class="eyebrow">Method</p><h2>Why soft washing is used instead of high pressure</h2><p>HydroSeal uses a controlled treatment process designed for organic roof staining. The cleaning solution is applied at low pressure so it can work on the buildup without using a pressure-washer stream to cut across shingles or force water beneath roof components.</p><p>The exact application depends on the roofing material, roof age, staining, weather and access. Some organic discoloration changes quickly, while heavier staining may continue to lighten after treatment. Roof washing does not repair leaks, loose materials, failing coatings or structural problems.</p></div>
        <ol class="steps"><li><strong>Inspect:</strong> review the roof material, condition, pitch, access and visible staining.</li><li><strong>Plan:</strong> identify gutters, downspouts, runoff areas, landscaping and sensitive exterior surfaces.</li><li><strong>Protect:</strong> use reasonable site-specific precautions around plants and property.</li><li><strong>Treat:</strong> apply the soft-wash solution at controlled pressure.</li><li><strong>Monitor:</strong> manage application and runoff based on weather and roof layout.</li><li><strong>Review:</strong> inspect the completed work and explain what may continue to lighten.</li></ol>
      </section>
      <section class="section split">
        <div><p class="eyebrow">Nocatee conditions</p><h2>Humidity, shade and tree cover affect roof staining</h2><p>Homes near ponds, preserves and mature landscaping may experience different roof conditions than open, full-sun properties. North-facing roof planes and shaded sections often dry more slowly. Tree debris can also hold moisture against valleys, gutters and lower roof edges.</p><p>Because every roof drains differently, runoff planning matters. Downspouts may discharge into planting beds, onto pavers or near pool equipment. HydroSeal reviews these areas before work so the process can be adapted to the property rather than treated as a one-size-fits-all wash.</p></div>
        <div><p class="eyebrow">What to expect</p><h2>Roof cleaning improves appearance but has limits</h2><p>Soft washing targets current organic buildup and black streaking. It cannot prevent future growth, restore worn roofing materials or guarantee that every mark will disappear. Results and how long the roof remains cleaner depend on shade, moisture, surrounding vegetation, roof material, drainage and maintenance.</p><p>Homeowners should also understand that roof washing is not a substitute for repair. Active leaks, loose shingles, cracked tiles, damaged flashing or unsafe access conditions should be handled before cleaning when they affect the work area.</p></div>
      </section>
      <section class="section">
        <p class="eyebrow">Service area</p><h2>Roof washing throughout Nocatee and nearby communities</h2>
        <p>HydroSeal provides Nocatee roof washing in communities such as Twenty Mile, Crosswater, Coastal Oaks, Del Webb Nocatee, Greenleaf, Willowcove and nearby Ponte Vedra and St. Johns County neighborhoods, subject to roof condition, access and scheduling.</p>
        <p>Exterior cleaning can also be coordinated with <a href="/nocatee-house-washing">Nocatee house washing</a> when siding, stucco, soffits, fascia and gutter faces need attention. Paver projects should be scheduled separately when roof runoff or exterior cleaning could affect recently sealed surfaces.</p>
      </section>'''
if old:
    html = html[:old.start()] + roof_content + html[old.end():]
roof.write_text(html, encoding='utf-8')

# Make calculator page informational and intent-specific rather than duplicating the homepage pricing section.
calc = Path('paver-sealing-cost-calculator.html')
html = calc.read_text(encoding='utf-8')
insert = '''
      <section class="section">
        <p class="eyebrow">How to use the estimate</p>
        <h2>A planning tool, not a duplicate price list</h2>
        <p>This calculator is designed to turn basic project details into a preliminary range. It is most useful when you know the approximate square footage and can identify whether the surface is concrete pavers, brick pavers, travertine or another natural stone. The result is not a binding quote because preparation usually determines the final scope.</p>
        <div class="split"><div><h3>Information that improves the estimate</h3><ul><li>Approximate square footage</li><li>Paver or stone material</li><li>Existing sealer condition</li><li>Visible white haze or efflorescence</li><li>Rust, oil or organic staining</li><li>Sunken or rocking pavers</li><li>Joint-sand loss</li><li>Access around pools, screens or narrow side yards</li></ul></div><div><h3>Why the final price may change</h3><p>A clean, unsealed driveway is different from a pool deck with failed coating, persistent shade and repair needs. Stripping, specialty stain treatment, releveling, drainage concerns, moisture and difficult access can change labor, materials and scheduling.</p><p>After using the calculator, send photos and the approximate measurements through the quote form. HydroSeal can then confirm whether the estimate reflects the visible project conditions.</p></div></div>
      </section>
      <section class="section split">
        <div><p class="eyebrow">Measure correctly</p><h2>Estimating your paver square footage</h2><p>For a simple rectangle, multiply length by width. Break irregular driveways, patios and pool decks into smaller rectangles, calculate each area and add the totals. Exclude the pool water, planting beds and other areas that will not be cleaned or sealed.</p><p>Measurements from plans, property apps or pacing can be useful for planning, but final billing should rely on confirmed measurements and the actual work area.</p></div>
        <div><p class="eyebrow">Next step</p><h2>Use the right service page for detailed guidance</h2><p>The calculator explains estimated cost, while the service pages explain preparation and limitations. Review <a href="/nocatee-driveway-paver-sealing">driveway paver sealing</a>, <a href="/nocatee-pool-deck-paver-sealing">pool deck paver sealing</a>, <a href="/nocatee-travertine-sealing">travertine sealing</a> or <a href="/nocatee-paver-joint-sand">joint-sand replacement</a> before requesting the final quote.</p></div>
      </section>
'''
if 'A planning tool, not a duplicate price list' not in html:
    html = html.replace('    </main>', insert + '    </main>')
calc.write_text(html, encoding='utf-8')

HEADER = '''<header class="site-header"><a class="brand" href="/" aria-label="Nocatee Paver Sealing home"><img class="brand-logo" src="/nocatee-paver-sealing-logo.png" alt="Nocatee Paver Sealing by HydroSeal" width="400" height="267" /></a><nav class="nav" aria-label="Primary navigation"><div class="nav-dropdown"><button class="nav-dropbtn" type="button">Paver Sealing</button><div class="nav-menu"><a href="/nocatee-driveway-paver-sealing">Driveway Sealing</a><a href="/nocatee-pool-deck-paver-sealing">Pool Deck Sealing</a><a href="/nocatee-travertine-sealing">Travertine Sealing</a><a href="/nocatee-paver-joint-sand">Joint Sand</a><a href="/paver-sealing-cost-calculator">Cost Calculator</a></div></div><div class="nav-dropdown"><button class="nav-dropbtn" type="button">Pressure Washing</button><div class="nav-menu"><a href="/nocatee-house-washing">House Wash</a><a href="/nocatee-roof-washing">Roof Wash</a></div></div><a class="nav-cta nav-call-text" href="tel:+19045375000"><span class="nav-call-label">Call or Text</span><span class="nav-call-phone">904.537.5000</span></a><a class="nav-cta" href="https://hydrosealpavers.com/get-a-quote">Get Quote</a></nav></header>'''
FOOTER = '''<div class="mobile-contactbar" aria-label="HydroSeal mobile contact options"><a class="mobile-callbar-btn" href="tel:+19045375000">📞 Call</a><a class="mobile-callbar-btn" href="sms:+19045375000">💬 Text</a></div><footer class="site-footer"><nav aria-label="Footer navigation"><a href="/nocatee-driveway-paver-sealing">Driveway Paver Sealing</a> &middot; <a href="/nocatee-pool-deck-paver-sealing">Pool Deck Sealing</a> &middot; <a href="/nocatee-travertine-sealing">Travertine Sealing</a> &middot; <a href="/nocatee-paver-joint-sand">Joint Sand</a> &middot; <a href="/nocatee-house-washing">House Washing</a> &middot; <a href="/nocatee-roof-washing">Roof Washing</a> &middot; <a href="/paver-sealing-cost-calculator">Cost Calculator</a> &middot; <a href="/warranty">Warranty</a> &middot; <a href="/privacy-policy">Privacy</a></nav><p><a href="https://hydrosealpavers.com/">Visit HydroSeal Pavers</a></p><p>&copy; 2026 HydroSeal &middot; Nocatee Paver Sealing &middot; Serving Nocatee, Ponte Vedra &amp; St. Johns County, FL</p></footer>'''

def page(title, description, canonical, crumb, body, schema):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>{title}</title><meta name="description" content="{description}" /><link rel="canonical" href="{canonical}" /><link rel="stylesheet" href="/styles.css" /><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body>{HEADER}<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true"> / </span><span aria-current="page">{crumb}</span></nav><main>{body}</main>{FOOTER}</body></html>'''

joint_url = 'https://nocateepaversealing.com/nocatee-paver-joint-sand'
joint_faq = [
    ('What joint sand does HydroSeal use?', 'HydroSeal generally uses ASTM C144 kiln-dried joint sand with a compatible joint-stabilizing sealer. The appropriate material depends on the paver system, drainage, existing joint material and site conditions.'),
    ('Do you remove the old joint sand?', 'Failing, contaminated or excessively low joint material is removed as needed during preparation. The joints are cleaned before fresh sand is installed to the appropriate level.'),
    ('Why not use polymeric sand on every project?', 'Polymeric sand can be useful in some systems, but Florida moisture, drainage, existing materials and future maintenance must be considered. HydroSeal does not treat one joint material as correct for every property.'),
    ('Can new sand fix sunken pavers?', 'No. Re-sanding restores joint levels but does not repair a failed base, severe settlement or drainage problem. Rocking or sunken pavers should be evaluated and repaired before sealing.'),
]
joint_schema = {'@context':'https://schema.org','@graph':[
    {'@type':'WebPage','@id':joint_url+'#webpage','url':joint_url,'name':'Nocatee Paver Joint Sand Replacement | HydroSeal','description':'Joint-sand replacement for Nocatee driveways, pool decks and patios using ASTM C144 kiln-dried sand and compatible joint-stabilizing sealer.','about':{'@id':'https://hydrosealpavers.com/#business'},'breadcrumb':{'@id':joint_url+'#breadcrumb'}},
    {'@type':'Service','@id':joint_url+'#service','name':'Nocatee Paver Joint Sand Replacement','serviceType':'Paver joint-sand removal, replacement and stabilization','url':joint_url,'provider':{'@id':'https://hydrosealpavers.com/#business'},'areaServed':[{'@type':'Place','name':'Nocatee, Florida'},{'@type':'Place','name':'Ponte Vedra, Florida'},{'@type':'AdministrativeArea','name':'St. Johns County, Florida'}]},
    {'@type':'BreadcrumbList','@id':joint_url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://nocateepaversealing.com/'},{'@type':'ListItem','position':2,'name':'Paver Joint Sand','item':joint_url}]},
    {'@type':'FAQPage','@id':joint_url+'#faq','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in joint_faq]}
]}
joint_body = '''<section class="section"><p class="eyebrow">Joint restoration</p><h1>Nocatee Paver Joint Sand Replacement</h1><p>Joint sand supports the interlock between pavers and helps the finished surface look complete. Rain, irrigation, roof runoff, pressure cleaning and normal traffic can lower the joint level over time. HydroSeal evaluates the joints, paver movement, drainage and existing materials before re-sanding.</p></section><section class="section split"><div><h2>ASTM C144 sand for clean, prepared joints</h2><p>HydroSeal generally uses ASTM C144 kiln-dried joint sand on suitable paver projects. Failing joint material is removed as needed, the surface is cleaned, and fresh sand is installed into dry, prepared joints before compatible sealer is applied.</p><p>The goal is to restore the joint profile and support stabilization without pretending sand can correct every structural issue.</p></div><div><h2>When re-sanding is not enough</h2><p>Low joints are different from a failed base. Sunken, rocking or separated pavers may require releveling or repair before sand and sealer are installed. Drainage problems, erosion and repeated washout should also be addressed rather than hidden.</p><p>For complete restoration, review <a href="/nocatee-driveway-paver-sealing">driveway sealing</a> or <a href="/nocatee-pool-deck-paver-sealing">pool deck sealing</a>.</p></div></section><section class="section"><h2>Our joint-sand process</h2><ol class="steps"><li><strong>Inspect:</strong> identify low joints, movement, drainage and existing material.</li><li><strong>Clean:</strong> remove buildup and failing joint material as appropriate.</li><li><strong>Dry:</strong> allow the pavers and joints to reach suitable conditions.</li><li><strong>Re-sand:</strong> install ASTM C144 kiln-dried sand to the proper joint level.</li><li><strong>Stabilize:</strong> apply the compatible sealer selected for the project.</li><li><strong>Review:</strong> explain cure time and future maintenance.</li></ol></section><section class="section faq-section"><p class="eyebrow">Questions</p><h2>Nocatee paver joint-sand questions</h2>''' + ''.join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q,a in joint_faq) + '''</section><section class="section cta-panel"><p class="eyebrow">Free estimate</p><h2>Request a joint-sand and paver sealing review</h2><p>Send photos showing the joints, low areas, rocking pavers and drainage concerns.</p><a class="button primary" href="https://hydrosealpavers.com/get-a-quote">Request quote</a></section>'''
Path('nocatee-paver-joint-sand.html').write_text(page('Nocatee Paver Joint Sand Replacement | HydroSeal','Joint-sand replacement for Nocatee driveways, pool decks and patios using ASTM C144 kiln-dried sand and compatible joint-stabilizing sealer.',joint_url,'Paver Joint Sand',joint_body,joint_schema), encoding='utf-8')

privacy_url = 'https://nocateepaversealing.com/privacy-policy'
privacy_schema = {'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':privacy_url+'#webpage','url':privacy_url,'name':'Privacy Policy | HydroSeal Nocatee','about':{'@id':'https://hydrosealpavers.com/#business'},'breadcrumb':{'@id':privacy_url+'#breadcrumb'}},{'@type':'BreadcrumbList','@id':privacy_url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://nocateepaversealing.com/'},{'@type':'ListItem','position':2,'name':'Privacy Policy','item':privacy_url}]}]}
privacy_body = '''<section class="section"><p class="eyebrow">Last updated July 23, 2026</p><h1>Privacy Policy</h1><p>HydroSeal uses information submitted through this website to respond to quote requests, schedule service, communicate about projects and improve the customer experience.</p><h2>Information we may collect</h2><p>Information may include your name, phone number, email address, service address, project photos, property details and messages you choose to provide. Basic technical information may also be collected by hosting, analytics, security or embedded-service providers.</p><h2>How information is used</h2><p>Information is used to review projects, prepare estimates, communicate about scheduling and service, maintain business records, prevent misuse and improve website performance. HydroSeal does not sell personal information.</p><h2>Third-party services</h2><p>The website may use services provided by hosting, form, analytics, review, gallery, chatbot or communications vendors. Those providers may process information under their own policies when their tools are used.</p><h2>Retention and security</h2><p>Information is retained only as reasonably needed for business, legal, tax, safety and customer-service purposes. No online system can guarantee absolute security.</p><h2>Your choices</h2><p>You may request correction or deletion of information that HydroSeal controls, subject to legal and recordkeeping requirements. Contact HydroSeal at <a href="mailto:info@hydrosealpavers.com">info@hydrosealpavers.com</a> or <a href="tel:+19045375000">904-537-5000</a>.</p></section>'''
Path('privacy-policy.html').write_text(page('Privacy Policy | HydroSeal Nocatee','Privacy policy for Nocatee Paver Sealing by HydroSeal, including quote requests, project photos, communications and third-party website services.',privacy_url,'Privacy Policy',privacy_body,privacy_schema), encoding='utf-8')

warranty_url = 'https://nocateepaversealing.com/warranty'
warranty_schema = {'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':warranty_url+'#webpage','url':warranty_url,'name':'Paver Sealing Warranty | HydroSeal Nocatee','about':{'@id':'https://hydrosealpavers.com/#business'},'breadcrumb':{'@id':warranty_url+'#breadcrumb'}},{'@type':'BreadcrumbList','@id':warranty_url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://nocateepaversealing.com/'},{'@type':'ListItem','position':2,'name':'Warranty','item':warranty_url}]}]}
warranty_body = '''<section class="section"><p class="eyebrow">Written coverage</p><h1>HydroSeal Paver Sealing Warranty</h1><p>Qualifying paver sealing projects include a written two-year workmanship and adhesion warranty. The project proposal or invoice controls the exact coverage for your property.</p><h2>What the warranty is intended to cover</h2><p>The warranty addresses covered workmanship and sealer-adhesion issues attributable to HydroSeal's application on the agreed work area during the stated warranty period.</p><h2>What is not covered</h2><p>Normal wear, fading, loss of sheen, traffic patterns, tire marks, stains, weeds, ants, efflorescence, irrigation deposits, rust, standing water, drainage problems, moisture migration, paver movement, base failure, erosion, damage by others, pressure washing by others, chemical exposure, weather events and pre-existing conditions are not workmanship or adhesion defects.</p><p>Color variation, natural-stone characteristics and changes caused by the underlying material are also outside workmanship coverage. Repairs, stripping, stain treatment and specialty preparation are covered only when specifically included in writing.</p><h2>Homeowner responsibilities</h2><p>Follow the written cure-time and care instructions, keep vehicles and water off the surface for the stated period, prevent irrigation from contacting fresh work and avoid incompatible cleaners or pressure washing that could damage the system.</p><h2>How to request a review</h2><p>Contact HydroSeal promptly with the service address, project date, description and clear photos. HydroSeal must be given a reasonable opportunity to inspect the area before repairs or alterations are made by another party.</p><p>This page is a general summary and does not replace the written warranty issued for a specific project.</p></section>'''
Path('warranty.html').write_text(page('Paver Sealing Warranty | HydroSeal Nocatee','Read the general terms of HydroSeal’s two-year workmanship and adhesion warranty for qualifying Nocatee paver sealing projects.',warranty_url,'Warranty',warranty_body,warranty_schema), encoding='utf-8')

# Add new URLs to sitemap.
sitemap = Path('sitemap.xml')
text = sitemap.read_text(encoding='utf-8')
for url in [joint_url, warranty_url, privacy_url]:
    if url not in text:
        text = text.replace('</urlset>', f'  <url><loc>{url}</loc><lastmod>2026-07-23</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
sitemap.write_text(text, encoding='utf-8')
