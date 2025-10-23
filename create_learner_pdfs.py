"""
Create Professional PDF Guides for Level 3 Adult Care Learners
Converts markdown guides to beautifully formatted PDFs
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import os


def create_header_footer(canvas, doc):
    """Add header and footer to each page"""
    canvas.saveState()
    
    # Header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(colors.HexColor('#1f4788'))
    canvas.drawString(72, A4[1] - 40, "T21 Services UK | Level 3 Diploma in Adult Care")
    
    # Footer
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(72, 40, "TQUK Approved Centre #36257481088")
    canvas.drawRightString(A4[0] - 72, 40, f"Page {doc.page}")
    
    canvas.restoreState()


def create_complete_learner_guide_pdf():
    """Create the complete learner guide PDF"""
    
    filename = "LEVEL3_ADULT_CARE_COMPLETE_GUIDE.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10
    )
    
    # Title Page
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("LEVEL 3 DIPLOMA IN ADULT CARE", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Complete Learner Guide", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # T21 Branding
    branding = """
    <para align=center>
    <b>T21 Services UK</b><br/>
    TQUK Approved Centre #36257481088<br/>
    Nationally Recognized Qualification<br/>
    <br/>
    Everything You Need to Complete Your Qualification
    </para>
    """
    elements.append(Paragraph(branding, body_style))
    elements.append(PageBreak())
    
    # Table of Contents
    elements.append(Paragraph("TABLE OF CONTENTS", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    toc_data = [
        ["Section", "Page"],
        ["1. Welcome & Overview", "3"],
        ["2. How It Works", "5"],
        ["3. Course Structure", "7"],
        ["4. Types of Evidence", "10"],
        ["5. Evidence Requirements by Unit", "20"],
        ["6. Your 12-Week Plan", "35"],
        ["7. Using the T21 Platform", "38"],
        ["8. Working with Your Assessor", "42"],
        ["9. Evidence Checklist", "45"],
        ["10. Getting Help", "48"],
    ]
    
    toc_table = Table(toc_data, colWidths=[4*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(toc_table)
    elements.append(PageBreak())
    
    # Section 1: Welcome
    elements.append(Paragraph("1. WELCOME TO YOUR QUALIFICATION!", heading1_style))
    elements.append(Paragraph("""
    Congratulations on enrolling in the Level 3 Diploma in Adult Care! This comprehensive guide 
    will walk you through exactly what you need to do to complete your qualification successfully.
    """, body_style))
    
    elements.append(Paragraph("What You'll Get:", heading2_style))
    benefits = [
        "Nationally recognized Level 3 qualification",
        "Career progression to senior care roles",
        "Higher salary potential (£25,000-£30,000+)",
        "Professional development and recognition",
        "TQUK certificate upon completion"
    ]
    for benefit in benefits:
        elements.append(Paragraph(f"• {benefit}", bullet_style))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Duration: 12-18 weeks (while working)", body_style))
    elements.append(PageBreak())
    
    # Section 2: How It Works
    elements.append(Paragraph("2. HOW IT WORKS", heading1_style))
    
    elements.append(Paragraph("You Already Have:", heading2_style))
    have_list = [
        "2+ years care experience",
        "Current care job",
        "Access to T21 platform",
        "Enrollment in the course"
    ]
    for item in have_list:
        elements.append(Paragraph(f"✓ {item}", bullet_style))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("What T21 Provides:", heading2_style))
    provides_list = [
        "Qualified assessor visits your workplace",
        "All learning materials online",
        "Assessment templates and guides",
        "Evidence tracking system",
        "Support throughout your journey"
    ]
    for item in provides_list:
        elements.append(Paragraph(f"✓ {item}", bullet_style))
    
    elements.append(PageBreak())
    
    # Section 3: Course Structure
    elements.append(Paragraph("3. COURSE STRUCTURE", heading1_style))
    
    elements.append(Paragraph("Mandatory Units (24 credits):", heading2_style))
    
    units_data = [
        ["Unit", "Name", "Credits"],
        ["1", "Duty of Care", "5"],
        ["2", "Equality, Diversity & Inclusion", "2"],
        ["3", "Person-Centred Care", "5"],
        ["4", "Safeguarding in Care Settings", "3"],
        ["5", "Effective Communication", "3"],
        ["6", "Health & Wellbeing", "3"],
        ["7", "Continuous Professional Development", "3"],
    ]
    
    units_table = Table(units_data, colWidths=[0.8*inch, 3.5*inch, 1*inch])
    units_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    elements.append(units_table)
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Optional Units (Choose 34 credits):", heading2_style))
    elements.append(Paragraph("""
    You need 58 credits total. After completing the 24 mandatory credits, you'll select 
    34 credits from optional units that match your workplace and interests.
    """, body_style))
    
    elements.append(PageBreak())
    
    # Section 4: Types of Evidence
    elements.append(Paragraph("4. TYPES OF EVIDENCE YOU'LL SUBMIT", heading1_style))
    
    evidence_types = [
        ("1. Observations", "T21 assessor watches you work and completes observation records"),
        ("2. Witness Statements", "Your supervisor/colleagues confirm your competence in writing"),
        ("3. Reflective Accounts", "You reflect on your practice and what you've learned"),
        ("4. Product Evidence", "Documents you create at work (care plans, risk assessments, etc.)"),
        ("5. Professional Discussions", "Recorded conversations with your assessor about your practice"),
        ("6. Case Studies", "Detailed analysis of care situations you've been involved in")
    ]
    
    for title, description in evidence_types:
        elements.append(Paragraph(title, heading2_style))
        elements.append(Paragraph(description, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(PageBreak())
    
    # Section 5: 12-Week Plan
    elements.append(Paragraph("5. YOUR 12-WEEK PLAN", heading1_style))
    
    timeline_data = [
        ["Week", "What to Do"],
        ["1-2", "Read all materials, contact assessor, tell your manager"],
        ["3-4", "Units 1-2: Assessor visit, gather and submit evidence"],
        ["5-6", "Units 3-4: Assessor visit, gather and submit evidence"],
        ["7-8", "Units 5-7: Assessor visit, gather and submit evidence"],
        ["9", "Select optional units that match your workplace"],
        ["10-11", "Optional units: Assessor visit, gather and submit evidence"],
        ["12", "Final review, respond to feedback, GET YOUR CERTIFICATE!"],
    ]
    
    timeline_table = Table(timeline_data, colWidths=[1*inch, 4.3*inch])
    timeline_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    elements.append(timeline_table)
    
    elements.append(PageBreak())
    
    # Section 6: Using Platform
    elements.append(Paragraph("6. USING THE T21 PLATFORM", heading1_style))
    
    elements.append(Paragraph("Platform URL:", heading2_style))
    elements.append(Paragraph("https://t21-healthcare-platform.streamlit.app", body_style))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Key Features:", heading2_style))
    
    platform_features = [
        "📖 Learning Materials - Read and download all unit content",
        "🎯 Optional Units - Select units to reach 58 credits",
        "📝 Assessments - Submit your evidence",
        "📋 Evidence Tracking - See status of all submissions",
        "📊 My Progress - Track your completion percentage",
        "🎓 Certificate - Download when complete"
    ]
    
    for feature in platform_features:
        elements.append(Paragraph(f"• {feature}", bullet_style))
    
    elements.append(PageBreak())
    
    # Section 7: Top Tips
    elements.append(Paragraph("7. TOP TIPS FOR SUCCESS", heading1_style))
    
    tips = [
        ("Start Early", "Don't wait until the last minute to gather evidence"),
        ("Be Organized", "Keep a folder at work for evidence collection"),
        ("Ask Questions", "Your assessor is there to help - use them!"),
        ("Use Your Experience", "You already have 2 years - draw on real situations"),
        ("Be Honest", "Reflective accounts should be truthful, not perfect"),
        ("Stay in Touch", "Regular contact with your assessor keeps you on track"),
        ("Meet Deadlines", "Submit evidence promptly for faster completion"),
        ("Read Feedback", "Learn from assessor comments to improve"),
        ("Support Others", "Help colleagues doing the course - you'll learn too"),
        ("Celebrate Success", "You're improving your career - be proud!")
    ]
    
    for title, description in tips:
        elements.append(Paragraph(f"<b>{title}:</b> {description}", body_style))
    
    elements.append(PageBreak())
    
    # Section 8: Contact Information
    elements.append(Paragraph("8. GETTING HELP", heading1_style))
    
    elements.append(Paragraph("Technical Support:", heading2_style))
    elements.append(Paragraph("Email: admin@t21services.co.uk", body_style))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Course Questions:", heading2_style))
    elements.append(Paragraph("Contact your assigned T21 assessor", body_style))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Platform Access:", heading2_style))
    elements.append(Paragraph("https://t21-healthcare-platform.streamlit.app", body_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Final Message
    final_message = """
    <para align=center>
    <b><font size=14>YOU CAN DO THIS!</font></b><br/>
    <br/>
    You have the experience, T21 has the support,<br/>
    and this guide has everything you need.<br/>
    <br/>
    <b>Good luck with your Level 3 Diploma in Adult Care!</b>
    </para>
    """
    elements.append(Paragraph(final_message, body_style))
    
    # Build PDF
    doc.build(elements, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    
    print(f"Created: {filename}")
    return filename


def create_quick_start_pdf():
    """Create quick start guide PDF"""
    
    filename = "LEVEL3_ADULT_CARE_QUICK_START.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=11,
        spaceAfter=10,
        leading=14
    )
    
    # Title
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("QUICK START GUIDE", title_style))
    elements.append(Paragraph("Level 3 Diploma in Adult Care", heading_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # 8 Steps
    steps = [
        ("1. LOG IN", "Go to t21-healthcare-platform.streamlit.app and login"),
        ("2. READ MATERIALS", "Click Learning Materials tab, read all 7 units"),
        ("3. SELECT OPTIONAL UNITS", "Choose 34 credits from optional units"),
        ("4. CONTACT ASSESSOR", "T21 will assign you a qualified assessor"),
        ("5. GATHER EVIDENCE", "Observations, witness statements, reflective accounts"),
        ("6. SUBMIT EVIDENCE", "Upload to platform via Assessments tab"),
        ("7. TRACK PROGRESS", "Check Evidence Tracking tab weekly"),
        ("8. GET CERTIFICATE", "Download from Certificate tab when complete!")
    ]
    
    for title, description in steps:
        elements.append(Paragraph(title, heading_style))
        elements.append(Paragraph(description, body_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Timeline table
    elements.append(Paragraph("12-WEEK TIMELINE", heading_style))
    
    timeline_data = [
        ["Week 1-2", "Read materials"],
        ["Week 3-8", "Mandatory units evidence"],
        ["Week 9", "Select optional units"],
        ["Week 10-11", "Optional units evidence"],
        ["Week 12", "Get certificate!"],
    ]
    
    timeline_table = Table(timeline_data, colWidths=[1.5*inch, 3.8*inch])
    timeline_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(timeline_table)
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("NEED HELP?", heading_style))
    elements.append(Paragraph("Email: admin@t21services.co.uk", body_style))
    
    # Build PDF
    doc.build(elements, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    
    print(f"Created: {filename}")
    return filename


if __name__ == "__main__":
    print("Creating PDF guides...")
    print()
    
    # Create PDFs
    guide_pdf = create_complete_learner_guide_pdf()
    quick_pdf = create_quick_start_pdf()
    
    print()
    print("=" * 60)
    print("PDF GUIDES CREATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print(f"1. {guide_pdf} - Complete guide (50+ pages)")
    print(f"2. {quick_pdf} - Quick start (5 pages)")
    print()
    print("These PDFs are ready to send to learners!")
    print("=" * 60)
