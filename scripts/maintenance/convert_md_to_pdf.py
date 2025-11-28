import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors
import re

def markdown_to_pdf(markdown_file, pdf_file):
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # Create PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue
    )

    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        textColor=colors.darkblue
    )

    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        textColor=colors.darkgreen
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=10,
        backgroundColor=colors.lightgrey,
        borderPadding=5,
        borderWidth=1,
        borderColor=colors.grey
    )

    story = []

    # Split content by lines and process
    lines = html_content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith('<h1>') and line.endswith('</h1>'):
            # Title
            text = re.sub(r'<[^>]+>', '', line)
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 12))

        elif line.startswith('<h2>') and line.endswith('</h2>'):
            # Heading 2
            text = re.sub(r'<[^>]+>', '', line)
            story.append(Paragraph(text, heading1_style))
            story.append(Spacer(1, 8))

        elif line.startswith('<h3>') and line.endswith('</h3>'):
            # Heading 3
            text = re.sub(r'<[^>]+>', '', line)
            story.append(Paragraph(text, heading2_style))
            story.append(Spacer(1, 6))

        elif line.startswith('<p>') and line.endswith('</p>'):
            # Paragraph
            text = re.sub(r'<[^>]+>', '', line)
            if text.strip():
                story.append(Paragraph(text, styles['Normal']))
                story.append(Spacer(1, 6))

        elif line.startswith('<table>'):
            # Simple table handling - convert to text representation
            table_text = "Table content (simplified for PDF)"
            story.append(Paragraph(table_text, styles['Normal']))
            story.append(Spacer(1, 6))
            # Skip table rows
            while i < len(lines) and not lines[i].strip().endswith('</table>'):
                i += 1

        elif line.startswith('<pre><code>'):
            # Code block
            code_lines = []
            i += 1
            while i < len(lines) and not (lines[i].strip().endswith('</code></pre>')):
                code_lines.append(lines[i])
                i += 1
            code_text = '\n'.join(code_lines)
            story.append(Paragraph(code_text, code_style))
            story.append(Spacer(1, 6))

        elif line.startswith('<ul>'):
            # List handling
            i += 1
            while i < len(lines) and not lines[i].strip().endswith('</ul>'):
                if lines[i].strip().startswith('<li>'):
                    list_text = re.sub(r'<[^>]+>', '', lines[i].strip())
                    story.append(Paragraph(f"• {list_text}", styles['Normal']))
                    story.append(Spacer(1, 3))
                i += 1

        elif line.strip() == '---':
            # Horizontal rule - add space
            story.append(Spacer(1, 12))

        i += 1

    # Build PDF
    doc.build(story)
    print(f"PDF created: {pdf_file}")

if __name__ == "__main__":
    # Convert Technical Blueprint
    markdown_to_pdf("CAREERIQ_TECHNICAL_BLUEPRINT.md", "CAREERIQ_TECHNICAL_BLUEPRINT.pdf")

    # Convert Revenue Deck
    markdown_to_pdf("CAREERIQ_REVENUE_DECK.md", "CAREERIQ_REVENUE_DECK.pdf")

    print("Both PDFs created successfully!")