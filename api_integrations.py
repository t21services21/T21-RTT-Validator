"""
REAL API INTEGRATIONS
Connect to Stripe, AWS, SendGrid, and other services

Setup Instructions:
1. Get API keys from each service
2. Add to Streamlit secrets
3. Test connections
"""

import os
import streamlit as st

# ============================================
# STRIPE PAYMENT INTEGRATION
# ============================================

def setup_stripe():
    """
    Setup Stripe for payment processing
    
    Steps to get Stripe API key:
    1. Go to https://stripe.com
    2. Create account (free)
    3. Go to Developers > API keys
    4. Copy Secret key
    5. Add to Streamlit secrets:
       - Go to https://share.streamlit.io
       - Select your app
       - Settings > Secrets
       - Add: STRIPE_SECRET_KEY = "sk_test_..."
    """
    
    try:
        import stripe
        
        # Get API key from secrets
        if 'STRIPE_SECRET_KEY' in st.secrets:
            stripe.api_key = st.secrets['STRIPE_SECRET_KEY']
            return True
        else:
            st.warning("""
            ⚠️ Stripe not configured yet!
            
            **To enable payments:**
            1. Sign up at https://stripe.com (free)
            2. Get your API key from Dashboard > Developers > API keys
            3. Add to Streamlit Secrets:
               ```
               STRIPE_SECRET_KEY = "sk_test_your_key_here"
               ```
            """)
            return False
    except ImportError:
        st.error("Stripe library not installed. Add 'stripe' to requirements.txt")
        return False

def create_stripe_payment(amount, description, customer_email):
    """Create Stripe payment intent"""
    
    try:
        import stripe
        
        if not setup_stripe():
            return None
        
        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency='gbp',
            description=description,
            receipt_email=customer_email,
            metadata={
                'customer_email': customer_email,
                'description': description
            }
        )
        
        return payment_intent
    
    except Exception as e:
        st.error(f"Stripe error: {e}")
        return None

def create_stripe_subscription(customer_email, price_id, plan_name):
    """Create Stripe subscription"""
    
    try:
        import stripe
        
        if not setup_stripe():
            return None
        
        # Create customer
        customer = stripe.Customer.create(
            email=customer_email,
            description=f"SOC Services - {plan_name}"
        )
        
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': price_id}],
            metadata={
                'plan_name': plan_name
            }
        )
        
        return subscription
    
    except Exception as e:
        st.error(f"Stripe subscription error: {e}")
        return None

# ============================================
# SENDGRID EMAIL INTEGRATION
# ============================================

def setup_sendgrid():
    """
    Setup SendGrid for email
    
    GOOD NEWS: Already configured!
    - Sender: admin@t21services.co.uk
    - API key already in secrets
    """
    
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        if 'SENDGRID_API_KEY' in st.secrets:
            return True
        else:
            st.warning("SendGrid not configured. Add SENDGRID_API_KEY to secrets.")
            return False
    except ImportError:
        st.error("SendGrid library not installed. Add 'sendgrid' to requirements.txt")
        return False

def send_email_via_sendgrid(to_email, subject, html_content):
    """Send email using SendGrid"""
    
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        if not setup_sendgrid():
            return False
        
        message = Mail(
            from_email='admin@t21services.co.uk',
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        sg = SendGridAPIClient(st.secrets['SENDGRID_API_KEY'])
        response = sg.send(message)
        
        return response.status_code == 202
    
    except Exception as e:
        st.error(f"SendGrid error: {e}")
        return False

# ============================================
# AWS INTEGRATION (for VMs)
# ============================================

def setup_aws():
    """
    Setup AWS for lab VMs
    
    Steps to get AWS credentials:
    1. Go to https://aws.amazon.com
    2. Create account
    3. Go to IAM > Users > Create User
    4. Attach policy: AmazonEC2FullAccess
    5. Create access key
    6. Add to Streamlit secrets:
       AWS_ACCESS_KEY_ID = "AKIA..."
       AWS_SECRET_ACCESS_KEY = "..."
       AWS_REGION = "eu-west-2"
    """
    
    try:
        import boto3
        
        if all(key in st.secrets for key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION']):
            return True
        else:
            st.warning("""
            ⚠️ AWS not configured yet!
            
            **To enable lab VMs:**
            1. Sign up at https://aws.amazon.com
            2. Create IAM user with EC2 access
            3. Get access keys
            4. Add to Streamlit Secrets:
               ```
               AWS_ACCESS_KEY_ID = "AKIA..."
               AWS_SECRET_ACCESS_KEY = "..."
               AWS_REGION = "eu-west-2"
               ```
            """)
            return False
    except ImportError:
        st.error("boto3 not installed. Add 'boto3' to requirements.txt")
        return False

def create_lab_vm_aws(lab_type):
    """Create EC2 instance for lab"""
    
    try:
        import boto3
        
        if not setup_aws():
            return None
        
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'],
            region_name=st.secrets['AWS_REGION']
        )
        
        # Launch instance
        response = ec2.run_instances(
            ImageId='ami-0c55b159cbfafe1f0',  # Ubuntu 22.04
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            KeyName='lab-key',
            SecurityGroupIds=['sg-lab-security'],
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': f'T21-Lab-{lab_type}'},
                    {'Key': 'Type', 'Value': 'CyberLab'}
                ]
            }]
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        
        # Wait for instance to start
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        
        # Get public IP
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
        
        return {
            'instance_id': instance_id,
            'public_ip': public_ip,
            'status': 'running'
        }
    
    except Exception as e:
        st.error(f"AWS error: {e}")
        return None

# ============================================
# OPENAI INTEGRATION (AI Tutor)
# ============================================

def setup_openai():
    """
    Setup OpenAI for AI tutor
    
    Steps:
    1. Go to https://platform.openai.com
    2. Create account
    3. Add payment method
    4. Get API key from API keys section
    5. Add to Streamlit secrets:
       OPENAI_API_KEY = "sk-..."
    """
    
    try:
        import openai
        
        if 'OPENAI_API_KEY' in st.secrets:
            openai.api_key = st.secrets['OPENAI_API_KEY']
            return True
        else:
            st.warning("""
            ⚠️ OpenAI not configured!
            
            **To enable AI Tutor:**
            1. Sign up at https://platform.openai.com
            2. Add payment method ($5-10/month typical)
            3. Get API key
            4. Add to Streamlit Secrets:
               ```
               OPENAI_API_KEY = "sk-..."
               ```
            """)
            return False
    except ImportError:
        st.error("openai not installed. Add 'openai' to requirements.txt")
        return False

def ask_ai_tutor(question, context=""):
    """Ask AI tutor a question"""
    
    try:
        import openai
        
        if not setup_openai():
            return "AI Tutor not configured yet. Please add OpenAI API key."
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert SOC analyst instructor. Provide clear, helpful explanations."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {e}"

# ============================================
# YOUTUBE/VIMEO VIDEO INTEGRATION
# ============================================

def setup_video_hosting():
    """
    Setup video hosting
    
    Options:
    1. YouTube (Free, public)
    2. Vimeo (Paid, private, better for courses)
    3. AWS S3 + CloudFront (Full control)
    
    For Vimeo:
    1. Sign up at https://vimeo.com
    2. Get Pro account ($20/month)
    3. Upload videos
    4. Get video IDs
    5. Add to course content
    """
    
    st.info("""
    **Video Hosting Options:**
    
    **Option 1: YouTube (Recommended for Start)**
    - ✅ Free
    - ✅ Easy to use
    - ✅ Good quality
    - ❌ Public (but can be unlisted)
    
    **Option 2: Vimeo Pro ($20/month)**
    - ✅ Private videos
    - ✅ No ads
    - ✅ Better player
    - ✅ Analytics
    
    **Option 3: AWS S3 ($5-20/month)**
    - ✅ Full control
    - ✅ Private
    - ✅ Fast delivery
    - ❌ More complex setup
    """)

# ============================================
# CONFIGURATION CHECKER
# ============================================

def check_all_integrations():
    """Check status of all integrations"""
    
    st.markdown("### 🔧 API Integration Status")
    
    integrations = {
        "Stripe (Payments)": setup_stripe(),
        "SendGrid (Email)": setup_sendgrid(),
        "AWS (Lab VMs)": setup_aws(),
        "OpenAI (AI Tutor)": setup_openai()
    }
    
    for name, status in integrations.items():
        if status:
            st.success(f"✅ {name} - Configured")
        else:
            st.warning(f"⚠️ {name} - Not configured")
    
    # Show what's needed
    st.markdown("---")
    st.markdown("### 📋 What You Need:")
    
    st.markdown("""
    **1. Stripe Account (Free)**
    - Sign up: https://stripe.com
    - Get API key: Dashboard > Developers > API keys
    - Cost: Free (2.9% + 30p per transaction)
    
    **2. SendGrid Account (Already have!)**
    - ✅ Already configured
    - ✅ Sender verified: admin@t21services.co.uk
    
    **3. AWS Account (Optional - for VMs)**
    - Sign up: https://aws.amazon.com
    - Free tier: 750 hours/month free for 12 months
    - Cost after: ~$10-50/month depending on usage
    
    **4. OpenAI Account (Optional - for AI)**
    - Sign up: https://platform.openai.com
    - Cost: ~$5-20/month for AI tutor
    
    **5. Video Hosting (Choose one)**
    - YouTube: Free
    - Vimeo Pro: $20/month
    - AWS S3: $5-20/month
    """)

# ============================================
# QUICK SETUP GUIDE
# ============================================

def render_setup_guide():
    """Render setup guide for integrations"""
    
    st.title("🔧 API Integration Setup Guide")
    
    st.markdown("""
    This guide will help you set up all the integrations needed for the platform.
    
    **Priority Order:**
    1. ✅ SendGrid (Already done!)
    2. 🔴 Stripe (Needed for payments)
    3. 🟡 Video Hosting (Needed for courses)
    4. 🟡 OpenAI (Nice to have)
    5. 🟢 AWS (Can wait until you have students)
    """)
    
    check_all_integrations()
    
    st.markdown("---")
    
    st.markdown("### 🚀 Next Steps:")
    
    st.markdown("""
    **This Week:**
    1. Set up Stripe account (30 minutes)
    2. Choose video hosting (YouTube to start)
    3. Upload first 5 videos
    
    **Next Week:**
    1. Set up OpenAI for AI tutor (optional)
    2. Test payment flow
    3. Launch beta program
    
    **When You Have Students:**
    1. Set up AWS for lab VMs
    2. Scale infrastructure
    3. Add more features
    """)

if __name__ == "__main__":
    render_setup_guide()
