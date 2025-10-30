"""
CERTIFICATE GENERATOR
Generate professional certificates for course completion
"""

from datetime import datetime
import streamlit as st

def generate_certificate_html(student_name, course_name, completion_date, certificate_id):
    """Generate HTML certificate"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {{
                size: A4 landscape;
                margin: 0;
            }}
            body {{
                font-family: 'Georgia', serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .certificate {{
                width: 297mm;
                height: 210mm;
                padding: 40px;
                background: white;
                border: 20px solid #667eea;
                box-sizing: border-box;
                position: relative;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .logo {{
                font-size: 48px;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 10px;
            }}
            .title {{
                font-size: 42px;
                font-weight: bold;
                color: #333;
                margin: 20px 0;
                text-transform: uppercase;
                letter-spacing: 3px;
            }}
            .subtitle {{
                font-size: 24px;
                color: #666;
                margin: 10px 0;
            }}
            .student-name {{
                font-size: 56px;
                font-weight: bold;
                color: #667eea;
                margin: 30px 0;
                text-align: center;
                font-style: italic;
            }}
            .course-name {{
                font-size: 32px;
                color: #333;
                margin: 20px 0;
                text-align: center;
            }}
            .completion-text {{
                font-size: 20px;
                color: #666;
                text-align: center;
                margin: 20px 0;
            }}
            .footer {{
                position: absolute;
                bottom: 40px;
                left: 40px;
                right: 40px;
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
            }}
            .signature {{
                text-align: center;
            }}
            .signature-line {{
                width: 200px;
                border-top: 2px solid #333;
                margin: 10px auto;
            }}
            .certificate-id {{
                font-size: 12px;
                color: #999;
                text-align: center;
                margin-top: 20px;
            }}
            .seal {{
                width: 100px;
                height: 100px;
                border: 5px solid #667eea;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                font-weight: bold;
                color: #667eea;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="certificate">
            <div class="header">
                <div class="logo">T21 SERVICES</div>
                <div class="title">Certificate of Completion</div>
                <div class="subtitle">This is to certify that</div>
            </div>
            
            <div class="student-name">{student_name}</div>
            
            <div class="completion-text">has successfully completed</div>
            
            <div class="course-name">{course_name}</div>
            
            <div class="completion-text">
                on {completion_date}
            </div>
            
            <div class="footer">
                <div class="signature">
                    <div class="signature-line"></div>
                    <div>Director of Training</div>
                    <div style="font-size: 14px; color: #999;">T21 Services UK</div>
                </div>
                
                <div class="seal">
                    VERIFIED<br>CERTIFICATE
                </div>
                
                <div class="signature">
                    <div class="signature-line"></div>
                    <div>Head of Cybersecurity</div>
                    <div style="font-size: 14px; color: #999;">T21 Services UK</div>
                </div>
            </div>
            
            <div class="certificate-id">
                Certificate ID: {certificate_id}<br>
                Verify at: https://t21services.co.uk/verify/{certificate_id}
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def display_certificate(student_name, course_name):
    """Display certificate in Streamlit"""
    
    completion_date = datetime.now().strftime("%B %d, %Y")
    certificate_id = f"T21-{datetime.now().strftime('%Y%m%d')}-{hash(student_name) % 10000:04d}"
    
    html = generate_certificate_html(student_name, course_name, completion_date, certificate_id)
    
    st.components.v1.html(html, height=800, scrolling=True)
    
    # Download button
    st.download_button(
        label="📥 Download Certificate (HTML)",
        data=html,
        file_name=f"T21_Certificate_{student_name.replace(' ', '_')}.html",
        mime="text/html"
    )
    
    st.success("✅ Certificate generated successfully!")
    st.info("💡 Open the downloaded HTML file in your browser and print to PDF")
    
    return certificate_id
