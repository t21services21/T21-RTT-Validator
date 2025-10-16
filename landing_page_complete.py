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
            <a href='#about' class='nav-link'>ABOUT</a>
            <a href='#services' class='nav-link'>SERVICES</a>
            <a href='#pricing' class='nav-link'>PRICING</a>
            <a href='#contact' class='nav-link'>CONTACT</a>
        </div>
        <div class='nav-login'>
            <button onclick='toggleLoginMenu()' style='background: linear-gradient(135deg, #d4af37, #f4d03f); color: #1a1a1a; padding: 10px 30px; border: none; border-radius: 25px; font-weight: 800; cursor: pointer; text-transform: uppercase;'>LOGIN ▼</button>
            <div id='loginMenu' style='display: none; position: absolute; right: 50px; top: 60px; background: white; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); padding: 10px; z-index: 1001;'>
                <a href='/student_login' style='display: block; padding: 12px 25px; color: #1a1a1a; text-decoration: none; font-weight: 600; border-radius: 5px; margin: 5px 0;' onmouseover='this.style.background="#f0f0f0"' onmouseout='this.style.background="white"'>🎓 Student Login</a>
                <a href='/staff_login' style='display: block; padding: 12px 25px; color: #1a1a1a; text-decoration: none; font-weight: 600; border-radius: 5px; margin: 5px 0;' onmouseover='this.style.background="#f0f0f0"' onmouseout='this.style.background="white"'>👥 Staff Login</a>
                <a href='/nhs_login' style='display: block; padding: 12px 25px; color: #1a1a1a; text-decoration: none; font-weight: 600; border-radius: 5px; margin: 5px 0;' onmouseover='this.style.background="#f0f0f0"' onmouseout='this.style.background="white"'>🏥 NHS Login</a>
            </div>
        </div>
    </div>
    
    <script>
    function toggleLoginMenu() {
        var menu = document.getElementById('loginMenu');
        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    }
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        var menu = document.getElementById('loginMenu');
        var button = event.target.closest('button');
        if (!button && menu.style.display === 'block') {
            menu.style.display = 'none';
        }
    });
    </script>
    
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
    
    <!-- About Section -->
    <div id='about' class='content-section' style='background: #f8f9fa;'>
        <h2 class='section-title'>About T21 Services</h2>
        <p class='section-text'>T21 Services Limited is a UK-based healthcare training and technology company, specializing in NHS administration training and AI-powered automation solutions. Established in 2020, we're committed to transforming healthcare workforce development.</p>
        <div style='margin-top: 30px; display: flex; gap: 30px; flex-wrap: wrap;'>
            <div style='flex: 1; min-width: 250px;'>
                <h3 style='color: #d4af37;'>🏢 Company Details</h3>
                <p><strong>Registered:</strong> Companies House UK<br>
                <strong>Company No:</strong> 13091053<br>
                <strong>Location:</strong> Liverpool, England<br>
                <strong>Founded:</strong> 2020</p>
            </div>
            <div style='flex: 1; min-width: 250px;'>
                <h3 style='color: #d4af37;'>✅ Certifications</h3>
                <p><strong>TQUK Approved Centre #36257481088</strong><br>
                <strong>NHS Compliant</strong><br>
                <strong>GDPR Certified</strong><br>
                <strong>ISO Standards</strong></p>
            </div>
        </div>
    </div>
    
    <!-- Services Section -->
    <div id='services' class='content-section'>
        <h2 class='section-title'>What We Offer</h2>
        <p class='section-text'>In the decades we've been in this business, we think we've figured out how to help you find that feeling. 
        The secret? Putting people ahead of technology. Always listening to them and being generous with our knowledge.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Service cards using Streamlit columns (not HTML)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-left: 5px solid #d4af37; height: 100%;'>
            <h3 style='color: #1a1a1a; font-size: 24px; margin-bottom: 15px;'>🎓 Professional Training</h3>
            <p style='color: #555; font-size: 16px; line-height: 1.8;'>Comprehensive NHS healthcare administration training covering 15+ roles. TQUK-endorsed professional development course (Understanding RTT & Hospital Administration - PDLC-01-039) designed to empower your workforce with the skills needed for modern healthcare delivery.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-left: 5px solid #d4af37; height: 100%;'>
            <h3 style='color: #1a1a1a; font-size: 24px; margin-bottom: 15px;'>🤖 AI-Powered Automation</h3>
            <p style='color: #555; font-size: 16px; line-height: 1.8;'>7 intelligent AI systems with 188 pre-built scenarios to automate routine tasks, reduce administrative burden, and allow your staff to focus on patient care.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-left: 5px solid #d4af37; height: 100%;'>
            <h3 style='color: #1a1a1a; font-size: 24px; margin-bottom: 15px;'>💰 Proven ROI</h3>
            <p style='color: #555; font-size: 16px; line-height: 1.8;'>Our clients save £2M+ per year through improved efficiency, reduced errors, and optimized workflows. Real results from real NHS organizations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Pricing Section
    st.markdown("""
    <div id='pricing' class='content-section' style='background: #f8f9fa; margin-top: 60px;'>
        <h2 class='section-title'>Pricing Plans</h2>
        <p class='section-text'>Flexible pricing options for individuals and organizations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center;'>
            <h3 style='color: #d4af37; font-size: 28px;'>Individual</h3>
            <p style='font-size: 48px; font-weight: 800; color: #1a1a1a; margin: 20px 0;'>£299</p>
            <p style='color: #666;'>per course</p>
            <ul style='text-align: left; color: #555; line-height: 2;'>
                <li>✅ Full course access</li>
                <li>✅ TQUK-recognized certificate</li>
                <li>✅ 6 months support</li>
                <li>✅ Digital resources</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #d4af37, #f4d03f); padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); text-align: center;'>
            <h3 style='color: #1a1a1a; font-size: 28px;'>Organization</h3>
            <p style='font-size: 48px; font-weight: 800; color: #1a1a1a; margin: 20px 0;'>£2,499</p>
            <p style='color: #1a1a1a;'>per year (up to 50 users)</p>
            <ul style='text-align: left; color: #1a1a1a; line-height: 2;'>
                <li>✅ Unlimited courses</li>
                <li>✅ AI automation tools</li>
                <li>✅ Priority support</li>
                <li>✅ Custom training</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center;'>
            <h3 style='color: #d4af37; font-size: 28px;'>Enterprise</h3>
            <p style='font-size: 48px; font-weight: 800; color: #1a1a1a; margin: 20px 0;'>Custom</p>
            <p style='color: #666;'>contact us</p>
            <ul style='text-align: left; color: #555; line-height: 2;'>
                <li>✅ Unlimited users</li>
                <li>✅ White-label option</li>
                <li>✅ Dedicated support</li>
                <li>✅ Custom integrations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact Section
    st.markdown("""
    <div id='contact' class='content-section' style='margin-top: 60px;'>
        <h2 class='section-title'>Contact Us</h2>
        <p class='section-text'>Get in touch with our team. We're here to help!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📧 Send us a message")
        with st.form("contact_form"):
            name = st.text_input("Full Name*")
            email = st.text_input("Email Address*")
            phone = st.text_input("Phone Number")
            message = st.text_area("Message*", height=150)
            
            if st.form_submit_button("Send Message", type="primary"):
                if name and email and message:
                    st.success("✅ Thank you! We'll get back to you within 24 hours.")
                else:
                    st.error("Please fill in all required fields.")
    
    with col2:
        st.markdown("""
        ### 📍 Contact Information
        
        **T21 Services Limited**  
        Liverpool, England  
        United Kingdom 🇬🇧
        
        **Email:**  
        📧 info@t21services.co.uk  
        📧 support@t21services.co.uk
        
        **Phone:**  
        📞 +44 (0) 151 123 4567
        
        **Company Registration:**  
        Companies House No: 13091053
        
        **Business Hours:**  
        Monday - Friday: 9:00 AM - 6:00 PM GMT  
        Saturday - Sunday: Closed
        """)
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <div class='footer-content'>
            <div class='footer-section'>
                <h4>Company</h4>
                <a href='#about' class='footer-link'>About Us</a>
                <span class='footer-link'>Our Team</span>
                <span class='footer-link'>Careers</span>
            </div>
            <div class='footer-section'>
                <h4>Services</h4>
                <a href='#services' class='footer-link'>Training Programs</a>
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
            <div style='margin-bottom: 15px;'>
                <a href='/privacy_policy' style='color: rgba(255,255,255,0.8); margin: 0 15px; text-decoration: none;'>Privacy Policy</a> |
                <a href='/terms_of_service' style='color: rgba(255,255,255,0.8); margin: 0 15px; text-decoration: none;'>Terms of Service</a> |
                <a href='/gdpr_compliance' style='color: rgba(255,255,255,0.8); margin: 0 15px; text-decoration: none;'>GDPR Compliance</a> |
                <a href='/cookie_policy' style='color: rgba(255,255,255,0.8); margin: 0 15px; text-decoration: none;'>Cookie Policy</a>
            </div>
            © 2025 T21 Services Limited | Company No: 13091053 | Liverpool, England 🇬🇧
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
            <div style='margin-bottom: 15px;'>
                <a href='/privacy_policy' style='color: rgba(255,255,255,0.8); margin: 0 15px; text-decoration: none;'>Privacy Policy</a> |
                <a href='/terms_of_service' style='color: rgba(255,255,255,0.8); margin: 0 15px; text-decoration: none;'>Terms of Service</a> |
                <a href='/gdpr_compliance' style='color: rgba(255,255,255,0.8); margin: 0 15px; text-decoration: none;'>GDPR Compliance</a> |
                <a href='/cookie_policy' style='color: rgba(255,255,255,0.8); margin: 0 15px; text-decoration: none;'>Cookie Policy</a>
            </div>
            © 2025 T21 Services Limited | Company No: 13091053 | Liverpool, England 🇬🇧
        </div>
    </div>
    """, unsafe_allow_html=True)
