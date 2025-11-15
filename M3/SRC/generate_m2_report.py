"""
Generate M2 Report
Creates a PDF report with query results for Milestone 2
"""

import json
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_report(query_results_file='query_results.json', output_file='milestone2_report_developer.pdf'):
    """Generate PDF report from query results"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    query_results_path = os.path.join(script_dir, query_results_file)
    
    if not os.path.exists(query_results_path):
        print(f"Error: Query results file not found: {query_results_path}")
        print("Please run test_queries.py first to generate query results.")
        sys.exit(1)
    
    # Load query results
    with open(query_results_path, 'r', encoding='utf-8') as f:
        query_results = json.load(f)
    
    # Create PDF
    output_path = os.path.join(script_dir, output_file)
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20
    )
    
    normal_style = styles['Normal']
    
    # Title
    story.append(Paragraph("Milestone 2: Retrieval Component", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Introduction
    story.append(Paragraph("Search Engine Implementation Report", heading_style))
    story.append(Paragraph(
        "This report presents the results of testing the search engine retrieval component "
        "with the required test queries. The search engine implements boolean AND queries "
        "with tf-idf scoring for ranking results.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Query Results Section
    story.append(Paragraph("Query Results", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Process each query
    for query, results_data in query_results.items():
        story.append(Paragraph(f"<b>Query {list(query_results.keys()).index(query) + 1}: {query}</b>", 
                              styles['Heading3']))
        story.append(Spacer(1, 0.1*inch))
        
        num_results = results_data.get('num_results', 0)
        query_time = results_data.get('query_time_ms', 0)
        
        story.append(Paragraph(
            f"Found {num_results} results (Query time: {query_time:.2f} ms)",
            normal_style
        ))
        story.append(Spacer(1, 0.1*inch))
        
        # Create table for results
        results = results_data.get('results', [])
        if results:
            # Table data
            table_data = [['Rank', 'URL', 'Score']]
            for result in results[:5]:  # Top 5 results
                rank = result.get('rank', '')
                url = result.get('url', '')
                score = result.get('score', 0)
                # Truncate long URLs for display
                if len(url) > 80:
                    url = url[:77] + '...'
                table_data.append([str(rank), url, f"{score:.4f}"])
            
            # Create table
            table = Table(table_data, colWidths=[0.5*inch, 5*inch, 0.8*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph("No results found.", normal_style))
        
        story.append(Spacer(1, 0.3*inch))
    
    # Implementation Details
    story.append(PageBreak())
    story.append(Paragraph("Implementation Details", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    details = [
        ("Query Processing", 
         "Queries are tokenized and stemmed using the same tokenizer and Porter stemmer "
         "used during indexing. This ensures query terms match indexed terms."),
        
        ("Boolean AND", 
         "The search engine implements boolean AND queries, meaning all query terms must "
         "be present in a document for it to be included in the results. The intersection "
         "of posting lists for all query terms is computed."),
        
        ("TF-IDF Scoring", 
         "Results are ranked using tf-idf (term frequency-inverse document frequency) scoring. "
         "The formula used is: tf_idf = (1 + log(tf)) * log(N/df), where tf is term frequency, "
         "df is document frequency, and N is the total number of documents."),
        
        ("Important Words", 
         "Words that appear in bold, headings (h1, h2, h3), or titles receive a 1.5x boost "
         "in their tf-idf score to reflect their higher importance."),
        
        ("Index Access", 
         "The search engine loads the inverted index into memory for fast query processing. "
         "Document mappings are also cached to enable fast URL lookups."),
    ]
    
    for title, description in details:
        story.append(Paragraph(f"<b>{title}</b>", styles['Heading3']))
        story.append(Paragraph(description, normal_style))
        story.append(Spacer(1, 0.15*inch))
    
    # Build PDF
    doc.build(story)
    print(f"Report generated: {output_path}")


if __name__ == '__main__':
    generate_report()

