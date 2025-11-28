import markdown
import weasyprint

def convert_md_to_pdf(md_file, pdf_file):
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # Add basic CSS styling for better PDF appearance
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                font-size: 28px;
            }}
            h2 {{
                color: #34495e;
                font-size: 24px;
                margin-top: 30px;
            }}
            h3 {{
                color: #7f8c8d;
                font-size: 18px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            ul, ol {{
                margin-left: 20px;
            }}
            .emoji {{
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Convert HTML to PDF
    weasyprint.HTML(string=styled_html).write_pdf(pdf_file)
    print(f"PDF created: {pdf_file}")

if __name__ == "__main__":
    # Convert Technical Blueprint
    convert_md_to_pdf("CAREERIQ_TECHNICAL_BLUEPRINT.md", "CAREERIQ_TECHNICAL_BLUEPRINT.pdf")

    # Convert Revenue Deck
    convert_md_to_pdf("CAREERIQ_REVENUE_DECK.md", "CAREERIQ_REVENUE_DECK.pdf")

    print("Both PDFs created successfully!")