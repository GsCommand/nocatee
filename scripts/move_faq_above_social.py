from pathlib import Path
import re

SOCIAL_WIDGET = '<div class="elfsight-app-f7229490-8c31-483c-aa82-d3a3b751a7c7" data-elfsight-app-lazy></div>'
SOCIAL_COMMENT = '<!-- Elfsight Social Media Icons | Untitled Social Media Icons 2 -->'
PLATFORM_SCRIPT = '<script src="https://elfsightcdn.com/platform.js" async></script>'


def find_section_bounds(text: str, marker_pos: int) -> tuple[int, int]:
    starts = [m.start() for m in re.finditer(r'<section\b', text[:marker_pos], flags=re.I)]
    if not starts:
        raise ValueError('No containing section start found')
    start = starts[-1]
    token_re = re.compile(r'<section\b|</section\s*>', flags=re.I)
    depth = 0
    for match in token_re.finditer(text, start):
        token = match.group(0).lower()
        if token.startswith('<section'):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return start, match.end()
    raise ValueError('No matching section end found')


def move_faq(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    social_start = re.search(r'<section\b[^>]*class=["\'][^"\']*social-icons[^"\']*["\'][^>]*>', text, flags=re.I)
    question_marker = re.search(r'<p\b[^>]*class=["\'][^"\']*eyebrow[^"\']*["\'][^>]*>\s*Questions\s*</p>', text, flags=re.I)
    if not social_start or not question_marker:
        return False

    faq_start, faq_end = find_section_bounds(text, question_marker.start())
    faq_block = text[faq_start:faq_end].strip()
    text = text[:faq_start] + text[faq_end:]

    social_start = re.search(r'<section\b[^>]*class=["\'][^"\']*social-icons[^"\']*["\'][^>]*>', text, flags=re.I)
    if not social_start:
        raise ValueError(f'{path}: social section disappeared')
    social_open_end = social_start.end()
    social_section_start, social_section_end = find_section_bounds(text, social_open_end - 1)
    social_block = text[social_section_start:social_section_end]

    widget_pos = social_block.find(SOCIAL_COMMENT)
    if widget_pos < 0:
        widget_pos = social_block.find(SOCIAL_WIDGET)
    if widget_pos < 0:
        closing_pos = social_block.rfind('</section>')
        insertion = f'\n      {faq_block}\n      {SOCIAL_COMMENT}\n      {SOCIAL_WIDGET}\n    '
        social_block = social_block[:closing_pos] + insertion + social_block[closing_pos:]
    else:
        insertion = f'{faq_block}\n      '
        social_block = social_block[:widget_pos] + insertion + social_block[widget_pos:]

    # Ensure the shared Elfsight loader exists once somewhere on the page.
    if PLATFORM_SCRIPT not in text:
        social_block = social_block.replace(SOCIAL_COMMENT, PLATFORM_SCRIPT + '\n      ' + SOCIAL_COMMENT, 1)

    text = text[:social_section_start] + social_block + text[social_section_end:]
    path.write_text(text, encoding='utf-8')
    return True


changed = []
for path in sorted(Path('.').glob('*.html')):
    if move_faq(path):
        changed.append(path.name)

print('Updated:', ', '.join(changed) if changed else 'none')
