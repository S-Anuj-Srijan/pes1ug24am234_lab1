from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, Preformatted
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "LAB1_DELIVERABLE.md"
OUTDIR = ROOT / "deliverble"
OUTPUT = OUTDIR / "LAB1_DELIVERABLE.pdf"

PAGE = landscape(A4)
NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2367A2")
PALE = colors.HexColor("#EAF2F8")
GRID = colors.HexColor("#9FB3C8")
INK = colors.HexColor("#1E2933")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8*mm))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=NAVY, spaceBefore=5*mm, spaceAfter=3*mm, keepWithNext=True))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=BLUE, spaceBefore=4*mm, spaceAfter=2*mm, keepWithNext=True))
styles.add(ParagraphStyle(name="H3x", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=3*mm, spaceAfter=1.5*mm, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.8, leading=12, textColor=INK, spaceAfter=2*mm))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName="Helvetica", fontSize=6.7, leading=8.3, textColor=INK))
styles.add(ParagraphStyle(name="CellHead", parent=styles["Smallx"], fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_LEFT))

def inline(s):
    s = s.replace("Â«", "&laquo;").replace("Â»", "&raquo;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<font name='Courier'>\1</font>", s)
    return s

def cell(text, head=False):
    return Paragraph(inline(text.strip()), styles["CellHead" if head else "Smallx"])

def make_table(rows):
    cols = len(rows[0])
    avail = PAGE[0] - 28*mm
    if cols == 6:
        widths = [14*mm, 31*mm, 74*mm, 16*mm, 82*mm, 61*mm]
    elif cols == 4:
        widths = [18*mm, 58*mm, 50*mm, avail-126*mm]
    elif cols == 3:
        widths = [24*mm, 56*mm, avail-80*mm]
    elif cols == 2:
        widths = [40*mm, avail-40*mm]
    else:
        widths = [avail/cols]*cols
    data = [[cell(x, r == 0) for x in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("GRID", (0,0), (-1,-1), 0.35, GRID),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PALE]),
    ]))
    return t

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = PAGE
    canvas.setStrokeColor(GRID); canvas.setLineWidth(.5)
    canvas.line(14*mm, 12*mm, w-14*mm, 12*mm)
    canvas.setFont("Helvetica", 7.5); canvas.setFillColor(colors.HexColor("#526779"))
    canvas.drawString(14*mm, 7.5*mm, "Software Engineering Lab 1 | Problem Statement 46")
    canvas.drawRightString(w-14*mm, 7.5*mm, f"Page {doc.page}")
    canvas.restoreState()

def parse():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []; i = 0; first = True
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1; continue
        if line.startswith("```"):
            lang = line[3:].strip(); code=[]; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i].replace("Â«", "<<").replace("Â»", ">>")); i += 1
            story += [Paragraph("UML diagram source (Mermaid)", styles["H3x"]), Preformatted("\n".join(code), ParagraphStyle(name=f"Code{i}", fontName="Courier", fontSize=6.3, leading=7.6, backColor=colors.HexColor("#F4F7F9"), borderColor=GRID, borderWidth=.5, borderPadding=6, textColor=INK)), Spacer(1, 2*mm)]
            i += 1; continue
        if line.startswith("|"):
            rows=[]
            while i < len(lines) and lines[i].strip().startswith("|"):
                parts=[x.strip() for x in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", x) for x in parts): rows.append(parts)
                i += 1
            story += [make_table(rows), Spacer(1, 3*mm)]; continue
        if line.startswith("# "):
            if not first: story.append(PageBreak())
            story.append(Paragraph(inline(line[2:]), styles["DocTitle"])); first=False
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["H1x"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["H2x"]))
        elif line.startswith("#### "):
            story.append(Paragraph(inline(line[5:]), styles["H3x"]))
        elif re.match(r"^\d+\. ", line):
            story.append(Paragraph(inline(line), styles["Bodyx"], bulletText=None))
        else:
            story.append(Paragraph(inline(line), styles["Bodyx"]))
        i += 1
    return story

OUTDIR.mkdir(exist_ok=True)
doc = SimpleDocTemplate(str(OUTPUT), pagesize=PAGE, leftMargin=14*mm, rightMargin=14*mm, topMargin=13*mm, bottomMargin=17*mm, title="Software Engineering Lab 1 - Deliverable", author="PES University")
doc.build(parse(), onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
