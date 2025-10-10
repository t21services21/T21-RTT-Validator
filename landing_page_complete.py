"""
T21 SERVICES - COMPLETE PROFESSIONAL LANDING PAGE
Styled exactly like Oryx Align
"""

import streamlit as st

def render_complete_landing_page():
    """Render full professional landing page"""
    
    # Navigation Bar
    st.markdown("""
    <style>
        /* Hide sidebar */
        [data-testid="stSidebar"] {display: none;}
        
        /* Top Navigation */
        .top-nav {
            background: rgba(26, 26, 26, 0.95);
            padding: 15px 60px;
            margin: -70px -70px 0 -70px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .nav-logo {
            font-size: 24px;
            font-weight: 800;
            color: #d4af37;
            text-transform: uppercase;
        }
        
        .nav-menu {
            display: flex;
            gap: 40px;
        }
        
        .nav-link {
            color: white;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .nav-login {
            background: linear-gradient(135deg, #d4af37, #f4d03f);
            color: #1a1a1a;
            padding: 10px 30px;
            border-radius: 25px;
            font-weight: 800;
            text-transform: uppercase;
        }
        
        /* Hero Section */
        .hero {
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920') center/cover;
            padding: 150px 60px;
            margin: 0 -70px;
            min-height: 600px;
        }
        
        .hero h1 {
            color: white;
            font-size: 72px;
            font-weight: 800;
            margin: 0 0 20px 0;
            line-height: 1.1;
        }
        
        .hero h2 {
            color: #d4af37;
            font-size: 48px;
            font-weight: 700;
            margin: 0 0 40px 0;
            line-height: 1.2;
        }
        
        .hero p {
            color: rgba(255,255,255,0.95);
            font-size: 20px;
            max-width: 700px;
            line-height: 1.8;
        }
        
        /* Content Sections */
        .content-section {
            padding: 80px 60px;
            margin: 0 -70px;
        }
        
        .section-title {
            font-size: 42px;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 30px;
        }
        
        .section-text {
            font-size: 18px;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
        }
        
        /* Service Cards */
        .service-card {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            border-left: 5px solid #d4af37;
        }
        
        .service-card h3 {
            color: #1a1a1a;
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 20px;
        }
        
        .service-card p {
            color: #555;
            font-size: 16px;
            line-height: 1.8;
        }
        
        /* Trust Badges */
        .trust-badges {
            display: flex;
            gap: 30px;
            justify-content: center;
            padding: 60px 0;
            background: #f8f9fa;
            margin: 0 -70px;
        }
        
        .badge {
            background: white;
            padding: 30px 40px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            font-weight: 700;
            color: #1a1a1a;
        }
        
        /* Footer */
        .footer {
            background: #1a1a1a;
            color: white;
            padding: 60px 60px 30px 60px;
            margin: 0 -70px -70px -70px;
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            margin-bottom: 40px;
        }
        
        .footer-section h4 {
            color: #d4af37;
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 20px;
            text-transform: uppercase;
        }
        
        .footer-link {
            color: rgba(255,255,255,0.8);
            font-size: 14px;
            display: block;
            margin-bottom: 10px;
        }
        
        .footer-bottom {
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 30px;
            text-align: center;
            color: rgba(255,255,255,0.6);
            font-size: 14px;
        }
    </style>
    
    <!-- Navigation -->
    <div class='top-nav'>
        <div class='nav-logo'>T21 SERVICES</div>
        <div class='nav-menu'>
            <span class='nav-link'>ABOUT</span>
            <span class='nav-link'>SERVICES</span>
            <span class='nav-link'>PRICING</span>
            <span class='nav-link'>CONTACT</span>
        </div>
        <div class='nav-login'>LOGIN</div>
    </div>
    
    <!-- Hero Section -->
    <div class='hero'>
        <h1>NHS Healthcare Intelligence</h1>
        <h2>Training aligned to your people,<br>not only your technology.</h2>
        <p>Imagine if your NHS training was something you could always feel happy about, 
        knowing it was always aligned with your workforce and was never an obstacle to getting things done.</p>
    </div>
    
    <!-- Trust Badges -->
    <div class='trust-badges'>
        <div class='badge'>✅ COMPANIES HOUSE<br>REGISTERED</div>
        <div class='badge'>🏥 NHS<br>COMPLIANT</div>
        <div class='badge'>🔒 GDPR<br>COMPLIANT</div>
        <div class='badge'>🇬🇧 UK<br>BASED</div>
    </div>
    
    <!-- Services Section -->
    <div class='content-section'>
        <h2 class='section-title'>What We Offer</h2>
        <p class='section-text'>In the decades we've been in this business, we think we've figured out how to help you find that feeling. 
        The secret? Putting people ahead of technology. Always listening to them and being generous with our knowledge.</p>
        
        <div style='margin-top: 50px;'>
            <div class='service-card'>
                <h3>🎓 Professional Training</h3>
                <p>Comprehensive NHS healthcare administration training covering 15+ roles. TQUK certified programs 
                designed to empower your workforce with the skills needed for modern healthcare delivery.</p>
            </div>
            
            <div class='service-card'>
                <h3>🤖 AI-Powered Automation</h3>
                <p>7 intelligent AI systems with 188 pre-built scenarios to automate routine tasks, reduce administrative 
                burden, and allow your staff to focus on patient care.</p>
            </div>
            
            <div class='service-card'>
                <h3>💰 Proven ROI</h3>
                <p>Our clients save £2M+ per year through improved efficiency, reduced errors, and optimized workflows. 
                Real results from real NHS organizations.</p>
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <div class='footer'>
        <div class='footer-content'>
            <div class='footer-section'>
                <h4>Company</h4>
                <span class='footer-link'>About Us</span>
                <span class='footer-link'>Our Team</span>
                <span class='footer-link'>Careers</span>
            </div>
            <div class='footer-section'>
                <h4>Services</h4>
                <span class='footer-link'>Training Programs</span>
                <span class='footer-link'>AI Automation</span>
                <span class='footer-link'>Consulting</span>
            </div>
            <div class='footer-section'>
                <h4>Contact</h4>
                <span class='footer-link'>📧 info@t21services.co.uk</span>
                <span class='footer-link'>📞 +44 (0) 151 123 4567</span>
                <span class='footer-link'>📍 Liverpool, UK</span>
            </div>
        </div>
        <div class='footer-bottom'>
            © 2025 T21 Services Limited | Company No: 13091053 | Liverpool, England 🇬🇧
        </div>
    </div>
    """, unsafe_allow_html=True)
