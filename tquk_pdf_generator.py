"""
TQUK PDF Generator
Converts markdown documents to professional PDFs with T21 Services branding
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import re


def create_pdf_from_markdown(content, title="TQUK Document"):
    """
    Convert markdown content to PDF with professional formatting
    
    Args:
        content: Markdown content string
        title: Document title
    
    Returns:
        BytesIO object containing PDF
    """
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        title=title
    )
    
    # Container for PDF elements
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1f4788',
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#1f4788',
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2c5aa0',
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor='#2c5aa0',
        spaceAfter=6,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        leftIndent=20,
        spaceAfter=6
    )
    
    # Process content line by line
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Handle horizontal rules
        if line.startswith('===') or line.startswith('---'):
            story.append(Spacer(1, 0.2*inch))
            continue
        
        # Handle headings
        if line.startswith('# '):
            text = line[2:].strip()
            # Remove markdown formatting
            text = clean_markdown(text)
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 0.1*inch))
        
        elif line.startswith('## '):
            text = line[3:].strip()
            text = clean_markdown(text)
            story.append(Paragraph(text, heading1_style))
        
        elif line.startswith('### '):
            text = line[4:].strip()
            text = clean_markdown(text)
            story.append(Paragraph(text, heading2_style))
        
        elif line.startswith('#### '):
            text = line[5:].strip()
            text = clean_markdown(text)
            story.append(Paragraph(text, heading3_style))
        
        # Handle bullet points
        elif line.startswith('- ') or line.startswith('* '):
            text = '• ' + line[2:].strip()
            text = clean_markdown(text)
            story.append(Paragraph(text, body_style))
        
        # Handle numbered lists
        elif re.match(r'^\d+\.\s', line):
            text = clean_markdown(line)
            story.append(Paragraph(text, body_style))
        
        # Handle code blocks (simple detection)
        elif line.startswith('    ') or line.startswith('\t'):
            text = line.strip()
            story.append(Paragraph(text, code_style))
        
        # Regular paragraph
        else:
            text = clean_markdown(line)
            if text:  # Only add non-empty paragraphs
                story.append(Paragraph(text, body_style))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF data
    buffer.seek(0)
    return buffer


def clean_markdown(text):
    """Remove markdown formatting for PDF"""
    # First, escape special XML characters
    text = text.replace('&', '&amp;')
    
    # Remove all markdown formatting - keep text only
    # Remove bold/italic markers (don't convert to HTML, just remove)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)  # Bold+Italic
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)      # Bold
    text = re.sub(r'__(.+?)__', r'\1', text)          # Bold (underscore)
    text = re.sub(r'\*(.+?)\*', r'\1', text)          # Italic
    text = re.sub(r'_(.+?)_', r'\1', text)            # Italic (underscore)
    
    # Remove inline code markers
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    # Remove links but keep text
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # Remove remaining special characters that cause issues
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    
    # Remove underscores used for blanks (they cause issues)
    text = re.sub(r'_{2,}', '[blank]', text)
    
    return text


def generate_tquk_pdf(markdown_content, document_title="TQUK Document"):
    """
    Generate a PDF from markdown content
    
    Args:
        markdown_content: String containing markdown content
        document_title: Title for the PDF document
    
    Returns:
        BytesIO object containing the PDF
    """
    try:
        return create_pdf_from_markdown(markdown_content, document_title)
    except Exception as e:
        # If PDF generation fails, create a simple text-based PDF
        print(f"PDF generation error: {str(e)}")
        return create_simple_pdf(markdown_content, document_title)


def create_simple_pdf(content, title="TQUK Document"):
    """
    Create a simple PDF without complex formatting (fallback)
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        title=title
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Simple body style
    body_style = ParagraphStyle(
        'SimpleBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    # Split content into lines and add as simple paragraphs
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            # Remove ALL special characters
            line = line.replace('*', '').replace('_', '').replace('#', '')
            line = line.replace('&', 'and').replace('<', '').replace('>', '')
            
            try:
                story.append(Paragraph(line, body_style))
            except:
                # If even this fails, skip the line
                pass
    
    doc.build(story)
    buffer.seek(0)
    return buffer
