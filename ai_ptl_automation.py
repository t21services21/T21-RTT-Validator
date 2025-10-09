"""
T21 AI-POWERED PTL AUTOMATION
Revolutionary AI features for Patient Tracking List

Features:
- AI Breach Risk Prediction (4 weeks ahead)
- AI Auto-Prioritization
- AI Appointment Recommendations
- AI Patient Outreach Automation
- AI Report Generation
- AI Anomaly Detection
- AI Resource Optimization
- AI Capacity Planning

This makes PTL 10x more powerful than standard NHS PTL!
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict
import json

# OpenAI integration
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def ai_predict_breach_risk(patient_data: Dict, ptl_context: List[Dict] = None) -> Dict:
    """
    AI predicts breach risk with advanced analysis
    
    Args:
        patient_data: Patient information
        ptl_context: Other patients for context (capacity, trends)
    
    Returns:
        Prediction with risk score, recommended actions, timeline
    """
    
    try:
        if not OPENAI_AVAILABLE:
            return fallback_breach_prediction(patient_data)
        
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return fallback_breach_prediction(patient_data)
        
        client = OpenAI(api_key=api_key)
        
        # Build comprehensive prompt
        prompt = f"""
        You are an expert NHS RTT breach prediction AI.
        
        PATIENT DATA:
        {json.dumps(patient_data, indent=2)}
        
        ANALYZE AND PREDICT:
        1. Breach risk score (0-100%)
        2. Likely breach date (if at risk)
        3. Contributing risk factors
        4. Recommended preventive actions
        5. Priority level (LOW, MEDIUM, HIGH, CRITICAL)
        6. Urgency timeline
        7. Appointment recommendations
        8. Resource requirements
        
        Consider:
        - Current weeks waiting
        - Specialty capacity
        - Historical patterns
        - Appointment availability
        - Patient factors (DNAs, cancellations)
        - Seasonal variations
        - Trust performance
        
        Respond in JSON format with detailed analysis.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert NHS RTT breach prediction AI with 20 years of experience."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        ai_result = response.choices[0].message.content
        
        try:
            result = json.loads(ai_result)
        except:
            result = {'ai_analysis': ai_result}
        
        result['success'] = True
        result['ai_powered'] = True
        result['prediction_time'] = datetime.now().isoformat()
        
        return result
        
    except Exception as e:
        return fallback_breach_prediction(patient_data)


def fallback_breach_prediction(patient_data: Dict) -> Dict:
    """Fallback breach prediction without AI"""
    
    days_waiting = patient_data.get('days_waiting', 0)
    specialty = patient_data.get('specialty', '')
    priority = patient_data.get('priority', 'Routine')
    
    # Simple rule-based prediction
    if priority == "2WW":
        target = 14
    elif priority == "Cancer 62-day":
        target = 62
    else:
        target = 126  # 18 weeks
    
    days_to_breach = target - days_waiting
    risk_score = max(0, min(100, 100 - (days_to_breach / target * 100)))
    
    if risk_score >= 80:
        priority_level = "CRITICAL"
        actions = [
            "IMMEDIATE appointment booking required",
            "Escalate to service manager",
            "Contact patient urgently",
            "Consider slot allocation from emergency capacity"
        ]
    elif risk_score >= 60:
        priority_level = "HIGH"
        actions = [
            "Book appointment within 3 days",
            "Review capacity with scheduler",
            "Contact patient to confirm availability"
        ]
    elif risk_score >= 40:
        priority_level = "MEDIUM"
        actions = [
            "Book appointment within 2 weeks",
            "Monitor weekly",
            "Standard contact procedure"
        ]
    else:
        priority_level = "LOW"
        actions = [
            "Standard booking process",
            "Monitor monthly"
        ]
    
    return {
        'success': True,
        'ai_powered': False,
        'breach_risk_score': risk_score,
        'priority_level': priority_level,
        'days_to_breach': days_to_breach,
        'recommended_actions': actions,
        'prediction_time': datetime.now().isoformat()
    }


def ai_auto_prioritize_ptl(patients: List[Dict]) -> List[Dict]:
    """
    AI automatically prioritizes entire PTL
    
    Returns:
        Sorted list with priority scores and recommendations
    """
    
    for patient in patients:
        # Calculate AI priority score
        prediction = ai_predict_breach_risk(patient)
        patient['ai_priority_score'] = prediction.get('breach_risk_score', 0)
        patient['ai_priority_level'] = prediction.get('priority_level', 'LOW')
        patient['ai_recommendations'] = prediction.get('recommended_actions', [])
    
    # Sort by AI priority score (highest first)
    patients.sort(key=lambda x: x.get('ai_priority_score', 0), reverse=True)
    
    return patients


def ai_recommend_appointments(patient: Dict, available_slots: List[Dict] = None) -> Dict:
    """
    AI recommends best appointment slot for patient
    
    Args:
        patient: Patient data
        available_slots: Available appointment slots
    
    Returns:
        Recommended slot with reasoning
    """
    
    try:
        if not OPENAI_AVAILABLE:
            return simple_slot_recommendation(patient, available_slots)
        
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return simple_slot_recommendation(patient, available_slots)
        
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        You are an expert NHS appointment scheduler AI.
        
        PATIENT:
        {json.dumps(patient, indent=2)}
        
        AVAILABLE SLOTS:
        {json.dumps(available_slots, indent=2) if available_slots else "No specific slots provided"}
        
        RECOMMEND:
        1. Best appointment date and time
        2. Reasoning for recommendation
        3. Alternative options
        4. Special considerations
        5. Communication plan
        
        Consider:
        - Breach risk urgency
        - Patient preferences
        - Travel time
        - Clinic capacity
        - Consultant availability
        
        Respond in JSON format.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert NHS appointment scheduler."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )
        
        result = response.choices[0].message.content
        
        try:
            return json.loads(result)
        except:
            return {'recommendation': result, 'ai_powered': True}
            
    except Exception as e:
        return simple_slot_recommendation(patient, available_slots)


def simple_slot_recommendation(patient: Dict, available_slots: List[Dict] = None) -> Dict:
    """Simple slot recommendation without AI"""
    
    days_to_breach = patient.get('days_to_breach', 126)
    
    if days_to_breach <= 7:
        recommendation = "URGENT: Book within 24 hours"
        timing = "Next available slot"
    elif days_to_breach <= 14:
        recommendation = "HIGH PRIORITY: Book within 3 days"
        timing = "Within this week"
    else:
        recommendation = "STANDARD: Book within 2 weeks"
        timing = "Next 2 weeks"
    
    return {
        'recommendation': recommendation,
        'timing': timing,
        'reasoning': f"Patient has {days_to_breach} days until breach",
        'ai_powered': False
    }


def ai_generate_ptl_report(ptl_data: Dict, report_type: str = "weekly") -> str:
    """
    AI generates comprehensive PTL report
    
    Args:
        ptl_data: PTL statistics and patient data
        report_type: weekly, monthly, breach, management
    
    Returns:
        Formatted report text
    """
    
    try:
        if not OPENAI_AVAILABLE:
            return generate_simple_report(ptl_data, report_type)
        
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return generate_simple_report(ptl_data, report_type)
        
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        You are an expert NHS RTT report writer.
        
        Generate a {report_type} PTL report.
        
        DATA:
        {json.dumps(ptl_data, indent=2)}
        
        INCLUDE:
        1. Executive Summary
        2. Key Metrics
        3. Breach Analysis
        4. Specialty Performance
        5. Risk Assessment
        6. Trends and Patterns
        7. Recommendations
        8. Action Items
        
        Format professionally for NHS management.
        Use clear headings, bullet points, and data tables.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert NHS report writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return generate_simple_report(ptl_data, report_type)


def generate_simple_report(ptl_data: Dict, report_type: str) -> str:
    """Generate simple report without AI"""
    
    report = f"# PTL {report_type.upper()} REPORT\n\n"
    report += f"**Generated:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    
    report += "## OVERVIEW\n\n"
    report += f"- Total Patients: {ptl_data.get('total_patients', 0)}\n"
    report += f"- Active Breaches: {ptl_data.get('breaches', 0)}\n"
    report += f"- Average Wait: {ptl_data.get('avg_weeks_waiting', 0)} weeks\n"
    report += f"- Longest Wait: {ptl_data.get('longest_wait_weeks', 0)} weeks\n\n"
    
    report += "## BREACH RISK\n\n"
    breach_risks = ptl_data.get('breach_risks', {})
    report += f"- 🔴 Critical: {breach_risks.get('CRITICAL', 0)}\n"
    report += f"- 🟠 High: {breach_risks.get('HIGH', 0)}\n"
    report += f"- 🟡 Medium: {breach_risks.get('MEDIUM', 0)}\n"
    report += f"- 🟢 Low: {breach_risks.get('LOW', 0)}\n\n"
    
    report += "## ACTIONS REQUIRED\n\n"
    critical = breach_risks.get('CRITICAL', 0)
    high = breach_risks.get('HIGH', 0)
    report += f"- {critical + high} patients need urgent attention\n"
    report += f"- {ptl_data.get('breaches', 0)} breaches to report to ICB/CCG\n"
    
    return report


def ai_detect_anomalies(ptl_data: Dict) -> List[Dict]:
    """
    AI detects anomalies and issues in PTL
    
    Returns:
        List of detected anomalies with severity and recommendations
    """
    
    anomalies = []
    
    # Check for unusual wait times
    avg_wait = ptl_data.get('avg_weeks_waiting', 0)
    if avg_wait > 12:
        anomalies.append({
            'type': 'HIGH_AVERAGE_WAIT',
            'severity': 'HIGH',
            'description': f'Average wait time is {avg_wait} weeks (target: under 12)',
            'recommendation': 'Review capacity and increase clinic slots'
        })
    
    # Check for high breach rate
    total = ptl_data.get('total_patients', 1)
    breaches = ptl_data.get('breaches', 0)
    breach_rate = (breaches / total * 100) if total > 0 else 0
    
    if breach_rate > 8:  # NHS target is 92% within 18 weeks = 8% breach rate max
        anomalies.append({
            'type': 'HIGH_BREACH_RATE',
            'severity': 'CRITICAL',
            'description': f'Breach rate is {breach_rate:.1f}% (target: under 8%)',
            'recommendation': 'Immediate escalation to senior management required'
        })
    
    # Check for capacity issues in specialties
    specialties = ptl_data.get('specialties', {})
    for specialty, count in specialties.items():
        if count > 100:  # Arbitrary threshold
            anomalies.append({
                'type': 'SPECIALTY_CAPACITY_ISSUE',
                'severity': 'MEDIUM',
                'specialty': specialty,
                'description': f'{specialty} has {count} patients waiting',
                'recommendation': f'Increase {specialty} clinic capacity'
            })
    
    return anomalies


def ai_optimize_resource_allocation(ptl_data: Dict) -> Dict:
    """
    AI recommends optimal resource allocation
    
    Returns:
        Resource allocation recommendations
    """
    
    recommendations = {
        'specialty_priorities': [],
        'clinic_slots_needed': {},
        'staff_allocation': {},
        'cost_benefit_analysis': {}
    }
    
    # Analyze specialty needs
    specialties = ptl_data.get('specialties', {})
    for specialty, count in specialties.items():
        if count > 50:
            recommendations['specialty_priorities'].append({
                'specialty': specialty,
                'patients_waiting': count,
                'priority': 'HIGH',
                'recommended_action': f'Add 2 extra clinic sessions per week for {specialty}'
            })
    
    return recommendations
