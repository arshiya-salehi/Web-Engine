"""
Report Generator
Generates a PDF report with index analytics
"""

import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch


def generate_report(stats_file='index_stats.json', output_file='milestone1_report.pdf'):
    """
    Generate PDF report with index analytics
    
    Args:
        stats_file: Path to JSON file containing statistics
        output_file: Output PDF file path
    """
    # Load statistics
    if not os.path.exists(stats_file):
        print(f"Error: Statistics file '{stats_file}' not found. Please run build_index.py first.")
        return
    
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    
    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("Milestone 1: Index Construction Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Introduction
    intro_text = """
    This report presents the analytics for the inverted index constructed from the web page corpus.
    The index was built using the following specifications:
    <br/><br/>
    • Tokens: All alphanumeric sequences<br/>
    • Stop words: Not used (all words indexed)<br/>
    • Stemming: Porter stemming algorithm<br/>
    • Important words: Words in bold, headings (h1, h2, h3), and titles are marked as important<br/>
    • Term frequency: Calculated for each token in each document<br/>
    """
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(Spacer(1, 0.4*inch))
    
    # Analytics Table
    story.append(Paragraph("Index Analytics", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Create table data
    table_data = [
        ['Metric', 'Value'],
        ['Number of Indexed Documents', f"{stats['num_documents']:,}"],
        ['Number of Unique Tokens', f"{stats['num_unique_tokens']:,}"],
        ['Total Size of Index on Disk', f"{stats['index_size_kb']:.2f} KB"]
    ]
    
    # Create table
    table = Table(table_data, colWidths=[4*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Additional Information
    story.append(Paragraph("Implementation Details", heading_style))
    details_text = """
    <b>Index Structure:</b><br/>
    The inverted index is stored as a dictionary where each token maps to a dictionary of document IDs.
    Each posting contains the term frequency (tf) and a flag indicating if the token appears in important
    contexts (bold, headings, or title).<br/><br/>
    
    <b>File Organization:</b><br/>
    The index is saved in JSON format with two files:
    <br/>• inverted_index.json: Contains the main inverted index structure
    <br/>• doc_mapping.json: Contains mappings between URLs and document IDs<br/><br/>
    
    <b>Processing Pipeline:</b><br/>
    1. HTML content is parsed using BeautifulSoup to extract text and identify important elements
    <br/>2. Text is tokenized into alphanumeric sequences
    <br/>3. Tokens are stemmed using the Porter stemming algorithm
    <br/>4. Term frequencies are calculated and stored in the inverted index
    """
    story.append(Paragraph(details_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"Report generated successfully: {output_file}")


if __name__ == '__main__':
    generate_report()

