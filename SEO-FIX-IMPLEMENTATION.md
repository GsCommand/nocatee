# Sitewide SEO Fix Implementation

Apply the following changes across the production site:

1. Replace every `mailto:outletdirect229@gmail.com...` Get Quote link with `https://hydrosealpavers.com/get-a-quote`.
2. Convert all internal navigation and contextual links from `.html` URLs to extensionless URLs.
3. Correct image preloads so each preload matches the rendered hero image. In particular, travertine must preload `/travertine-sealing-nocatee.webp`, not the old JPEG. Remove unused hero preloads.
4. Standardize all canonicals on the non-www extensionless host `https://nocateepaversealing.com/...`.
5. Rebuild `sitemap.xml` with non-www extensionless canonical URLs only.
6. Add a consistent contextual link to `https://hydrosealpavers.com/` from every non-homepage page.
7. Ensure `https://elfsightcdn.com/platform.js` loads no more than once per page.
8. Add visible breadcrumbs and matching `BreadcrumbList` schema to service pages and the calculator page.
9. Improve the roof-washing page by removing the phrase `Roof washing should never sound aggressive.`, replacing it with homeowner-focused service copy, and adding WebPage, Service, LocalBusiness and FAQ schema consistent with visible content.
10. Add WebPage, Service, LocalBusiness and FAQ schema to the house-washing page.
11. Deploy and internally link the joint-sand page if its source is production-ready; otherwise document the blocker rather than publishing a thin page.
12. Preserve existing FAQ placement directly above the social icon widget, the full footer, the homepage calculator, and current styling.

Validate all changed pages for one canonical, one H1, extensionless internal links, no personal Gmail CTA, one Elfsight platform script, matching visible/schema FAQs, responsive layout and valid JSON-LD.
