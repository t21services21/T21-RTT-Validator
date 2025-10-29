"""
PAYMENT INTEGRATION SYSTEM
Stripe payment processing for courses and subscriptions

Features:
- Course payments
- Subscription billing
- Invoice generation
- Payment tracking
- Refunds
"""

import streamlit as st
from datetime import datetime
import hashlib
import json

class PaymentProcessor:
    """
    Payment processing system
    In production, integrate with Stripe API
    """
    
    def __init__(self):
        self.currency = "GBP"
        self.tax_rate = 0.20  # 20% VAT
    
    def create_payment_intent(self, amount, description, customer_email):
        """
        Create payment intent
        In production: Use Stripe API
        """
        payment_id = hashlib.sha256(f"{customer_email}{amount}{datetime.now()}".encode()).hexdigest()[:16]
        
        return {
            "payment_id": payment_id,
            "amount": amount,
            "currency": self.currency,
            "description": description,
            "customer_email": customer_email,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
    
    def process_course_payment(self, student_email, course_name, amount):
        """Process course enrollment payment"""
        
        # Calculate totals
        subtotal = amount
        tax = subtotal * self.tax_rate
        total = subtotal + tax
        
        # Create payment intent
        payment = self.create_payment_intent(
            amount=total,
            description=f"Course: {course_name}",
            customer_email=student_email
        )
        
        # In production: Redirect to Stripe checkout
        # For now: Simulate successful payment
        payment['status'] = 'succeeded'
        payment['subtotal'] = subtotal
        payment['tax'] = tax
        payment['total'] = total
        
        # Record payment in database
        self.record_payment(payment)
        
        return payment
    
    def create_subscription(self, customer_email, plan_name, monthly_amount):
        """Create recurring subscription"""
        
        subscription_id = hashlib.sha256(f"{customer_email}{plan_name}{datetime.now()}".encode()).hexdigest()[:16]
        
        return {
            "subscription_id": subscription_id,
            "customer_email": customer_email,
            "plan_name": plan_name,
            "amount": monthly_amount,
            "currency": self.currency,
            "status": "active",
            "billing_cycle": "monthly",
            "next_billing_date": self.get_next_billing_date(),
            "created_at": datetime.now().isoformat()
        }
    
    def get_next_billing_date(self):
        """Calculate next billing date"""
        from datetime import timedelta
        return (datetime.now() + timedelta(days=30)).isoformat()
    
    def cancel_subscription(self, subscription_id):
        """Cancel subscription"""
        # In production: Call Stripe API
        return {
            "subscription_id": subscription_id,
            "status": "cancelled",
            "cancelled_at": datetime.now().isoformat()
        }
    
    def process_refund(self, payment_id, amount, reason):
        """Process refund"""
        refund_id = hashlib.sha256(f"{payment_id}{amount}{datetime.now()}".encode()).hexdigest()[:16]
        
        return {
            "refund_id": refund_id,
            "payment_id": payment_id,
            "amount": amount,
            "reason": reason,
            "status": "succeeded",
            "refunded_at": datetime.now().isoformat()
        }
    
    def record_payment(self, payment):
        """Record payment in database"""
        # In production: Store in database
        pass
    
    def get_payment_history(self, customer_email):
        """Get customer payment history"""
        # In production: Query database
        return []
    
    def generate_invoice(self, payment_id, customer_info, items):
        """Generate invoice PDF"""
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{payment_id[:8]}"
        
        invoice = {
            "invoice_number": invoice_number,
            "invoice_date": datetime.now().strftime("%B %d, %Y"),
            "customer": customer_info,
            "items": items,
            "subtotal": sum(item['amount'] for item in items),
            "tax": sum(item['amount'] for item in items) * self.tax_rate,
            "total": sum(item['amount'] for item in items) * (1 + self.tax_rate)
        }
        
        return invoice

# Payment processor instance
payment_processor = PaymentProcessor()

# Streamlit payment UI components
def render_payment_form(course_name, amount):
    """Render payment form for course enrollment"""
    
    st.subheader(f"💳 Payment for {course_name}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Course:** {course_name}")
        st.markdown(f"**Price:** £{amount:,.2f}")
        st.markdown(f"**VAT (20%):** £{amount * 0.20:,.2f}")
        st.markdown(f"**Total:** £{amount * 1.20:,.2f}")
    
    with col2:
        payment_method = st.selectbox("Payment Method", [
            "Credit/Debit Card",
            "PayPal",
            "Bank Transfer"
        ])
    
    if payment_method == "Credit/Debit Card":
        card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
        
        col_card1, col_card2 = st.columns(2)
        with col_card1:
            expiry = st.text_input("Expiry Date", placeholder="MM/YY")
        with col_card2:
            cvv = st.text_input("CVV", placeholder="123", type="password")
        
        cardholder_name = st.text_input("Cardholder Name")
    
    elif payment_method == "PayPal":
        st.info("You will be redirected to PayPal to complete payment")
    
    else:  # Bank Transfer
        st.info("""
        **Bank Transfer Details:**
        
        Account Name: T21 Services UK Ltd  
        Sort Code: 12-34-56  
        Account Number: 12345678  
        Reference: Your email address
        
        Please allow 2-3 business days for processing.
        """)
    
    if st.button("💳 Complete Payment", use_container_width=True):
        with st.spinner("Processing payment..."):
            # Simulate payment processing
            import time
            time.sleep(2)
            
            payment = payment_processor.process_course_payment(
                student_email=st.session_state.user_email,
                course_name=course_name,
                amount=amount
            )
            
            if payment['status'] == 'succeeded':
                st.success("✅ Payment successful!")
                st.balloons()
                
                # Show receipt
                st.markdown("### 📄 Payment Receipt")
                st.markdown(f"**Payment ID:** {payment['payment_id']}")
                st.markdown(f"**Amount:** £{payment['total']:,.2f}")
                st.markdown(f"**Date:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
                
                # Download invoice button
                if st.button("📥 Download Invoice"):
                    st.success("Invoice downloaded!")
                
                return True
            else:
                st.error("❌ Payment failed. Please try again.")
                return False
    
    return False

def render_subscription_management():
    """Render subscription management UI"""
    
    st.subheader("🔄 Subscription Management")
    
    # Current subscription
    st.markdown("### Current Subscription")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Plan", "Enterprise SOC")
    with col2:
        st.metric("Monthly Cost", "£15,000")
    with col3:
        st.metric("Next Billing", "Nov 1, 2025")
    
    st.progress(0.75)
    st.caption("75% through current billing period")
    
    # Actions
    col_act1, col_act2, col_act3 = st.columns(3)
    
    with col_act1:
        if st.button("📝 Update Payment Method"):
            st.info("Update payment method")
    
    with col_act2:
        if st.button("⬆️ Upgrade Plan"):
            st.info("Upgrade to higher tier")
    
    with col_act3:
        if st.button("❌ Cancel Subscription"):
            st.warning("Are you sure? This will cancel at end of billing period.")
    
    # Payment history
    st.markdown("### Payment History")
    
    payments = [
        {"date": "Oct 1, 2025", "amount": "£15,000", "status": "✅ Paid"},
        {"date": "Sep 1, 2025", "amount": "£15,000", "status": "✅ Paid"},
        {"date": "Aug 1, 2025", "amount": "£15,000", "status": "✅ Paid"},
    ]
    
    for payment in payments:
        col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
        with col_p1:
            st.markdown(payment['date'])
        with col_p2:
            st.markdown(payment['amount'])
        with col_p3:
            st.markdown(payment['status'])

# Pricing tiers
PRICING_TIERS = {
    "SOC-101": {
        "name": "SOC Analyst Foundation",
        "price": 2000,
        "duration": "8 weeks",
        "features": [
            "Complete foundation course",
            "Hands-on labs",
            "Foundation certification",
            "AI tutor support",
            "Study group access"
        ]
    },
    "SOC-201": {
        "name": "SOC Analyst Professional",
        "price": 3500,
        "duration": "12 weeks",
        "features": [
            "Advanced training",
            "Malware analysis labs",
            "Professional certification",
            "1-on-1 mentorship",
            "Job placement assistance"
        ]
    },
    "SOC-301": {
        "name": "SOC Analyst Expert",
        "price": 5000,
        "duration": "16 weeks",
        "features": [
            "Expert-level training",
            "Red team exercises",
            "Expert certification",
            "Career coaching",
            "Guaranteed job placement"
        ]
    }
}
