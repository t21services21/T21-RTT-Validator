"""
TQUK PDF Converter
Converts markdown learning materials to professional PDF documents
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import markdown2
from bs4 import BeautifulSoup
import re


def markdown_to_pdf(markdown_content, title="TQUK Learning Materials", unit_name=""):
    """
    Convert markdown content to a professional PDF
    
    Args:
        markdown_content: Markdown text to convert
        title: Document title
        unit_name: Unit name for header
    
    Returns:
        BytesIO object containing PDF data
    """
    
    # Create PDF buffer
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    )
    
    # Add title page
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph(title, title_style))
    if unit_name:
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(unit_name, heading1_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # TQUK branding
    tquk_info = """
    <para align=center>
    <b>TQUK Approved Centre #36257481088</b><br/>
    Nationally Recognized Qualification<br/>
    T21 Services UK | NHS Training & Simulation
    </para>
    """
    elements.append(Paragraph(tquk_info, body_style))
    elements.append(PageBreak())
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        markdown_content,
        extras=['tables', 'fenced-code-blocks', 'header-ids']
    )
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Process each element
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'blockquote']):
        
        if element.name == 'h1':
            text = element.get_text()
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(text, heading1_style))
            
        elif element.name == 'h2':
            text = element.get_text()
            elements.append(Spacer(1, 0.15*inch))
            elements.append(Paragraph(text, heading2_style))
            
        elif element.name == 'h3':
            text = element.get_text()
            elements.append(Paragraph(f"<b>{text}</b>", body_style))
            
        elif element.name == 'p':
            text = element.get_text()
            # Clean up text
            text = text.replace('✅', '• ')
            text = text.replace('📚', '')
            text = text.replace('💡', '')
            text = text.replace('⚠️', 'WARNING: ')
            text = text.replace('🎯', '• ')
            
            if text.strip():
                elements.append(Paragraph(text, body_style))
                
        elif element.name in ['ul', 'ol']:
            for li in element.find_all('li'):
                text = li.get_text()
                text = text.replace('✅', '')
                text = text.replace('📚', '')
                elements.append(Paragraph(f"• {text}", body_style))
                
        elif element.name == 'blockquote':
            text = element.get_text()
            quote_style = ParagraphStyle(
                'Quote',
                parent=body_style,
                leftIndent=20,
                rightIndent=20,
                textColor=colors.HexColor('#4b5563'),
                borderColor=colors.HexColor('#2563eb'),
                borderWidth=2,
                borderPadding=10
            )
            elements.append(Paragraph(text, quote_style))
    
    # Add footer
    elements.append(Spacer(1, 0.5*inch))
    footer_text = """
    <para align=center fontSize=9 textColor=#666666>
    T21 Services UK | NHS Training & Simulation Environment<br/>
    No real patient data | For training purposes only
    </para>
    """
    elements.append(Paragraph(footer_text, body_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF data
    buffer.seek(0)
    return buffer


def create_unit_pdf(unit_number, unit_name, markdown_content):
    """
    Create a PDF for a specific unit
    
    Args:
        unit_number: Unit number (1-7)
        unit_name: Name of the unit
        markdown_content: Markdown content
    
    Returns:
        BytesIO object containing PDF
    """
    title = f"Level 3 Diploma in Adult Care"
    unit_title = f"Unit {unit_number}: {unit_name}"
    
    return markdown_to_pdf(markdown_content, title, unit_title)
