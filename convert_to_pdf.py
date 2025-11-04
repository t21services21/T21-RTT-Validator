"""
Convert all TQUK CDA markdown files to PDF
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
import os

def clean_text(text):
    """Clean markdown formatting for PDF"""
    # Remove markdown symbols
    text = text.replace('**', '')
    text = text.replace('`', '')
    text = text.replace('##', '')
    text = text.replace('#', '')
    text = text.replace('---', '')
    text = text.replace('✅', '✓')
    text = text.replace('❌', '✗')
    text = text.replace('🎯', '>')
    text = text.replace('📋', '')
    text = text.replace('📄', '')
    text = text.replace('📚', '')
    text = text.replace('🎓', '')
    text = text.replace('💡', '')
    text = text.replace('⚠️', 'WARNING:')
    return text

def markdown_to_pdf(input_file, output_file, title):
    """Convert markdown to professional PDF"""
    
    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=36
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=HexColor('#00008B'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=HexColor('#00008B'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#00008B'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=HexColor('#00008B'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        leftIndent=20,
        bulletIndent=10
    )
    
    # Build content
    elements = []
    
    # Title page
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("TQUK Level 3 Diploma in Adult Care (RQF)", heading2_style))
    elements.append(Paragraph("Qualification Number: 610/0103/6", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Centre: T21 Services UK", normal_style))
    elements.append(Paragraph("Centre Number: #36257481088", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("November 2025", normal_style))
    elements.append(PageBreak())
    
    # Process content
    lines = content.split('\n')
    in_table = False
    table_data = []
    
    for line in lines:
        line = line.strip()
        
        if not line or line == '---':
            elements.append(Spacer(1, 12))
            continue
        
        # Skip markdown metadata
        if line.startswith('**Qualification:**') or line.startswith('**Centre:**') or \
           line.startswith('**Unit Code:**') or line.startswith('**Level:**') or \
           line.startswith('**Credit Value:**') or line.startswith('**Guided Learning Hours:**'):
            continue
        
        # Headers
        if line.startswith('# '):
            elements.append(Paragraph(clean_text(line[2:]), heading1_style))
        elif line.startswith('## '):
            elements.append(Paragraph(clean_text(line[3:]), heading2_style))
        elif line.startswith('### '):
            elements.append(Paragraph(clean_text(line[4:]), heading3_style))
        elif line.startswith('#### '):
            elements.append(Paragraph(clean_text(line[5:]), heading3_style))
        
        # Tables
        elif line.startswith('|'):
            if not in_table:
                in_table = True
                table_data = []
            # Parse table row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if not all(c.startswith('-') for c in cells):  # Skip separator rows
                table_data.append(cells)
        else:
            # End of table
            if in_table and table_data:
                # Create table
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(t)
                elements.append(Spacer(1, 12))
                in_table = False
                table_data = []
            
            # Bullets
            if line.startswith('- ') or line.startswith('* ') or line.startswith('✅') or line.startswith('✓'):
                bullet_text = clean_text(line[2:] if line.startswith(('- ', '* ')) else line)
                elements.append(Paragraph(f"• {bullet_text}", bullet_style))
            # Normal text
            elif line:
                elements.append(Paragraph(clean_text(line), normal_style))
                elements.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(elements)
    print(f"Created: {output_file}")

# Files to convert
files_to_convert = [
    ("Unit_1_Assessment_Plan_Duty_of_Care.md", "Unit_1_Duty_of_Care_Assessment_Plan.pdf", "UNIT 1: DUTY OF CARE - Assessment Plan"),
    ("Unit_2_Assessment_Plan_Equality_Diversity_Inclusion.md", "Unit_2_Equality_Diversity_Inclusion_Assessment_Plan.pdf", "UNIT 2: EQUALITY, DIVERSITY & INCLUSION - Assessment Plan"),
    ("Unit_3_Assessment_Plan_Person_Centred_Practice.md", "Unit_3_Person_Centred_Practice_Assessment_Plan.pdf", "UNIT 3: PERSON-CENTRED PRACTICE - Assessment Plan"),
    ("Unit_4_Assessment_Plan_Safeguarding.md", "Unit_4_Safeguarding_Assessment_Plan.pdf", "UNIT 4: SAFEGUARDING - Assessment Plan"),
    ("Unit_5_Assessment_Plan_Communication.md", "Unit_5_Communication_Assessment_Plan.pdf", "UNIT 5: COMMUNICATION - Assessment Plan"),
    ("Unit_6_Assessment_Plan_Health_Safety.md", "Unit_6_Health_Safety_Assessment_Plan.pdf", "UNIT 6: HEALTH & SAFETY - Assessment Plan"),
    ("Unit_7_Assessment_Plan_CPD.md", "Unit_7_CPD_Assessment_Plan.pdf", "UNIT 7: CONTINUING PROFESSIONAL DEVELOPMENT - Assessment Plan"),
    ("CDA_SUBMISSION_SUMMARY.md", "CDA_Submission_Summary.pdf", "CENTRE-DEVISED ASSESSMENT SUBMISSION SUMMARY"),
    ("EMAIL_RESPONSE_TO_TQUK.md", "Email_Response_to_TQUK.pdf", "EMAIL RESPONSE TO TQUK")
]

print("Converting markdown files to PDF...")
print("=" * 60)

for input_file, output_file, title in files_to_convert:
    if os.path.exists(input_file):
        try:
            markdown_to_pdf(input_file, output_file, title)
        except Exception as e:
            print(f"ERROR converting {input_file}: {e}")
    else:
        print(f"WARNING: File not found: {input_file}")

print("=" * 60)
print("PDF conversion complete!")
print("\nPDF files created in current directory")
print("Ready for download and submission to TQUK!")
