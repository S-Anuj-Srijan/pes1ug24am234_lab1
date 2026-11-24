"""Screenshot recorded tool output in a browser and assemble the Lab 7 PDF.

Requires playwright and reportlab, plus installed Microsoft Edge.
These are labelled report-view screenshots, not native terminal captures.
"""
from html import escape
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
)

ROOT = Path(__file__).resolve().parents[1]


def transcript(path):
    metadata = json.loads(path.with_suffix('.command.json').read_text())
    text = f"Working directory: {metadata['working_directory']}\n"
    if metadata['environment']:
        text += f"Environment: {metadata['environment']}\n"
    text += '> ' + ' '.join(metadata['command']) + '\n'
    if metadata['stdin'] is not None:
        text += 'Supplied stdin: ' + repr(metadata['stdin']) + '\n'
    text += path.read_text(encoding='utf-8')
    text += path.with_suffix('.stderr.txt').read_text(encoding='utf-8')
    text += f"\nExit code: {metadata['exit_code']}\n"
    return text


def main():
    shots = []
    for label, title in [('code', 'Lab 6 - Code coverage'),
                         ('branch', 'Lab 6 - Branch coverage')]:
        base = ROOT / 'lab6/reports' / label
        shots.append((ROOT / f'lab6/screenshots/{label}_coverage.png', title,
                      transcript(base / 'tests.txt') + '\n' +
                      transcript(base / 'coverage.txt')))
    stages = [
        ('before_demo', 'Lab 7 - Original application: empty input'),
        ('before_fuzz', 'Lab 7 - Original application: fuzz failures'),
        ('after_invalid_demo', 'Lab 7 - Fixed application: empty input'),
        ('after_valid_demo', 'Lab 7 - Fixed application: valid input'),
        ('after_fuzz', 'Lab 7 - Fixed application: all tests pass'),
    ]
    for label, title in stages:
        text = transcript(ROOT / f'lab7/reports/{label}.txt')
        if label == 'before_fuzz':
            lines = text.splitlines()
            # Explicit excerpt: retain the command, each shrunk input, and summary.
            keep = lines[:4]
            for index, line in enumerate(lines):
                if 'Failing test case:' in line:
                    keep.extend(lines[index:index + 3])
            keep += lines[-7:]
            text = '[EXCERPT - full traceback: reports/before_fuzz.txt]\n' + '\n'.join(keep)
        shots.append((ROOT / f'lab7/screenshots/{label}.png', title, text))
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 900},
                                device_scale_factor=1.5)
        for path, title, text in shots:
            path.parent.mkdir(parents=True, exist_ok=True)
            html = f'''<!doctype html><meta charset="utf-8"><style>
            *{{box-sizing:border-box}}body{{margin:0;padding:32px;background:#f1f5f9;
            color:#152338;font:18px Arial}}h1{{font-size:28px;margin:8px 0 12px}}
            p{{margin:8px 0 20px}}pre{{background:#111827;color:#f1f5f9;padding:24px;
            border-radius:8px;font:17px/1.5 Consolas,monospace;white-space:pre-wrap;
            overflow-wrap:anywhere}}footer{{font-size:14px;color:#475569}}</style>
            <h1>{escape(title)}</h1><p>S Anuj Srijan | PES1UG24AM234 | 24 November 2026</p>
            <pre>{escape(text)}</pre><footer>Recorded command output - browser report screenshot.
            Actual stdout/stderr preserved in reports/; not a native terminal capture.</footer>'''
            path.with_suffix('.html').write_text(html, encoding='utf-8')
            page.set_content(html)
            page.screenshot(path=str(path), full_page=True)
        browser.close()
    output = ROOT / 'lab7/SE_Lab7_FuzzTesting_Deliverables.pdf'
    styles = getSampleStyleSheet()
    story = [Paragraph('Lab 7: Fuzz Testing', styles['Title']),
             Paragraph('S Anuj Srijan | PES1UG24AM234', styles['Heading2']),
             Paragraph('Visa Application | 24 November 2026', styles['Normal']),
             Spacer(1, 18)]
    paragraphs = [
        'Reference: SETAPESU26/L6_L7_52_visa_application, Lab 7; upstream commit '
        '5fff7c811cbd03f4611e80cac0ca7624c9ae30b8. Original source is preserved in baseline/.',
        'Results: all three no-crash properties fail on the original implementation. '
        'After validation fixes, all 33 tests pass: six property-based tests and '
        '27 regression/size-limit cases. Each property allows up to 300 examples '
        'with deterministic generation; failing properties stop after shrinking.',
        'Findings: None and non-string inputs cause AttributeError or TypeError. '
        'Empty or malformed strings cause conversion/unpacking ValueError. '
        'Negative values, NaN, infinity and overflowing fee arithmetic also need validation.',
        'Contract: invalid input returns None. The CLI prints Invalid input and continues. '
        'Entries and processing days are nonnegative integers. Fees and discounts must be '
        'finite and nonnegative. Text is limited to 10,000 characters and integer tokens '
        'to 100 ASCII digits. The original floor mean, 18% uplift and zero fee floor remain.',
        'Valid example: tourist:2 gives (Tourist, 2); 5,10,21 gives 12; '
        '6000|500 gives 6580.0. Empty lines crash the original but are rejected safely by the fix.',
        'Evidence format: the following images are browser screenshots of saved command '
        'output, not native terminal captures. Full stdout, stderr, command and exit status '
        'are in reports/. Run scripts/show_evidence.ps1 for native-terminal reproduction.',
        'Reproduce from the repository root: python scripts/verify_labs.py --lab 7. '
        'Submitted application: lab7/visa_application.py. Tests: lab7/test_processor.py. '
        'The handout uses processor.py generically; the assigned application retains its upstream name.',
    ]
    for paragraph in paragraphs:
        story.extend([Paragraph(escape(paragraph), styles['BodyText']), Spacer(1, 10)])
    for path, title, _ in shots[2:]:
        story.extend([PageBreak(), Paragraph(title, styles['Heading1']), Spacer(1, 12)])
        from PIL import Image as PILImage
        with PILImage.open(path) as im:
            width, height = im.size
        scale = min(499 / width, 650 / height)
        story.append(Image(str(path), width=width * scale, height=height * scale))
    def footer(canvas, doc):
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#64748b'))
        canvas.drawString(48, 25, 'S Anuj Srijan | PES1UG24AM234 | Lab 7')
        canvas.drawRightString(A4[0] - 48, 25, str(doc.page))
    SimpleDocTemplate(str(output), pagesize=A4, rightMargin=48, leftMargin=48,
                      topMargin=42, bottomMargin=42).build(
        story, onFirstPage=footer, onLaterPages=footer)
    print(output)


if __name__ == '__main__':
    main()
