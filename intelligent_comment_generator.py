"""
T21 Intelligent Comment Generator
Generate ultra-detailed validation comments

Features:
- Extract all information from letters and PAS
- Generate comprehensive comments
- Include specific diagnoses, treatments, tests
- Document booking status
- Document queries sent
- Document PAS updates
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class IntelligentCommentGenerator:
    """Generate detailed validation comments"""
    
    def __init__(self):
        """Initialize comment generator"""
        self.comment_templates = self._load_templates()
        
    def generate_comment(self, 
                        letter_data: Dict[str, Any],
                        pas_data: Dict[str, Any],
                        validation_result: Dict[str, Any],
                        fixes_applied: List[Dict[str, Any]]) -> str:
        """
        Generate comprehensive validation comment
        
        Args:
            letter_data: Data extracted from clinic letter
            pas_data: Data from PAS system
            validation_result: Validation errors/warnings
            fixes_applied: List of fixes that were applied
            
        Returns:
            Detailed validation comment string
        """
        # Determine comment type based on clock action
        clock_action = letter_data.get('clock_action', 'CONTINUE')
        
        if clock_action == 'STOP':
            return self._generate_clock_stop_comment(letter_data, pas_data, validation_result, fixes_applied)
        elif clock_action == 'RESTART':
            return self._generate_clock_restart_comment(letter_data, pas_data, validation_result, fixes_applied)
        elif letter_data.get('letter_date') is None:
            return self._generate_no_letter_comment(pas_data, validation_result, fixes_applied)
        else:
            return self._generate_clock_continue_comment(letter_data, pas_data, validation_result, fixes_applied)
    
    def _generate_clock_stop_comment(self,
                                     letter_data: Dict[str, Any],
                                     pas_data: Dict[str, Any],
                                     validation_result: Dict[str, Any],
                                     fixes_applied: List[Dict[str, Any]]) -> str:
        """Generate comment for clock stop scenarios"""
        parts = []
        
        # Header with clock stop
        rtt_code = letter_data.get('rtt_code', 30)
        stop_date = letter_data.get('clock_stop_date') or letter_data.get('appointment_date')
        letter_date = letter_data.get('letter_date')
        
        parts.append(f"CS ({stop_date})({rtt_code}) AI AS PER CL DATED {letter_date}")
        
        # Appointment details
        if letter_data.get('appointment_date'):
            appt_type = self._determine_appointment_type(letter_data)
            parts.append(f"PATIENT ATTENDED {appt_type} {letter_data['appointment_date']}.")
        
        # Diagnosis
        diagnosis = letter_data.get('diagnosis', {})
        if diagnosis.get('condition'):
            diag_text = diagnosis['condition'].upper()
            if diagnosis.get('location'):
                diag_text += f" {diagnosis['location'].upper()}"
            parts.append(f"DIAGNOSIS: {diag_text}.")
        
        # Treatment provided
        treatments = letter_data.get('treatment_provided', [])
        if treatments:
            treatment_text = self._format_treatments(treatments)
            parts.append(f"TREATMENT PROVIDED: {treatment_text}.")
        
        # Diagnostic tests
        tests = letter_data.get('diagnostic_tests', [])
        if tests:
            test_text = self._format_diagnostic_tests(tests)
            parts.append(test_text)
        
        # Clock status explanation
        parts.append(f"CLOCK STOPPED {stop_date} - {self._get_stop_reason(rtt_code)}.")
        
        # Follow-up status
        follow_up = letter_data.get('follow_up', {})
        if follow_up.get('required'):
            fu_text = self._format_follow_up(follow_up, pas_data)
            parts.append(fu_text)
        
        # Future plans
        future_plans = letter_data.get('future_plans', [])
        if future_plans:
            plans_text = self._format_future_plans(future_plans)
            parts.append(plans_text)
        
        # Queries sent
        queries = self._identify_queries(letter_data, pas_data)
        if queries:
            parts.append(self._format_queries(queries))
        
        # PAS updates
        if fixes_applied:
            updates_text = self._format_pas_updates(fixes_applied)
            parts.append(f"PAS UPDATED: {updates_text}.")
        
        return " ".join(parts)
    
    def _generate_clock_continue_comment(self,
                                        letter_data: Dict[str, Any],
                                        pas_data: Dict[str, Any],
                                        validation_result: Dict[str, Any],
                                        fixes_applied: List[Dict[str, Any]]) -> str:
        """Generate comment for clock continues scenarios"""
        parts = []
        
        # Header
        validation_date = datetime.now().strftime('%d/%m/%Y')
        letter_date = letter_data.get('letter_date')
        
        parts.append(f"{validation_date} AI AS PER CL DATED {letter_date}")
        
        # Appointment details
        if letter_data.get('appointment_date'):
            appt_type = self._determine_appointment_type(letter_data)
            parts.append(f"PATIENT ATTENDED {appt_type} {letter_data['appointment_date']}.")
        
        # Diagnosis
        diagnosis = letter_data.get('diagnosis', {})
        if diagnosis.get('condition'):
            diag_text = diagnosis['condition'].upper()
            if diagnosis.get('location'):
                diag_text += f" {diagnosis['location'].upper()}"
            parts.append(f"DIAGNOSIS: {diag_text}.")
        
        # Investigations requested
        booking_reqs = letter_data.get('booking_requirements', {})
        if booking_reqs.get('diagnostics'):
            inv_text = self._format_investigation_requests(booking_reqs['diagnostics'], pas_data)
            parts.append(inv_text)
        
        # Diagnostic tests completed
        tests = letter_data.get('diagnostic_tests', [])
        if tests:
            test_text = self._format_diagnostic_tests(tests)
            parts.append(test_text)
        
        # Clock status
        rtt_code = letter_data.get('rtt_code', 20)
        parts.append(f"CLOCK CONTINUES - CODE {rtt_code} RECORDED.")
        
        # Follow-up requirements
        follow_up = letter_data.get('follow_up', {})
        if follow_up.get('required'):
            fu_text = self._format_follow_up(follow_up, pas_data)
            parts.append(fu_text)
        
        # Surgery listing
        if booking_reqs.get('surgery'):
            surgery_text = self._format_surgery_listing(pas_data)
            parts.append(surgery_text)
        
        # Queries sent
        queries = self._identify_queries(letter_data, pas_data)
        if queries:
            parts.append(self._format_queries(queries))
        
        # PAS updates
        if fixes_applied:
            updates_text = self._format_pas_updates(fixes_applied)
            parts.append(f"PAS UPDATED: {updates_text}.")
        
        return " ".join(parts)
    
    def _generate_no_letter_comment(self,
                                    pas_data: Dict[str, Any],
                                    validation_result: Dict[str, Any],
                                    fixes_applied: List[Dict[str, Any]]) -> str:
        """Generate comment when no clinic letter available"""
        parts = []
        
        # Header
        validation_date = datetime.now().strftime('%d/%m/%Y')
        parts.append(f"{validation_date} AI NO CLINIC LETTER AVAILABLE.")
        
        # What PAS shows
        if pas_data.get('appointment_date'):
            parts.append(f"PAS SHOWS: PATIENT ATTENDED APPOINTMENT {pas_data['appointment_date']}.")
        
        if pas_data.get('outcome'):
            parts.append(f"OUTCOME: {pas_data['outcome'].upper()}.")
        else:
            parts.append("OUTCOME: NOT RECORDED IN PAS.")
        
        # Insufficient information
        parts.append("UNABLE TO DETERMINE TREATMENT PROVIDED OR DIAGNOSIS.")
        
        # Code recorded
        rtt_code = pas_data.get('rtt_code', 20)
        parts.append(f"CODE {rtt_code} RECORDED FOR ATTENDANCE.")
        
        # Clock status
        parts.append("CLOCK CONTINUES.")
        
        # Query sent
        parts.append(f"QUERY SENT TO CONSULTANT SECRETARY {validation_date} REQUESTING CLINIC LETTER OR CONSULTATION NOTES TO COMPLETE VALIDATION.")
        
        # Awaiting response
        parts.append("AWAITING RESPONSE TO DETERMINE IF TREATMENT GIVEN (CODE 30) OR FURTHER INVESTIGATION REQUIRED (CODE 20).")
        
        return " ".join(parts)
    
    def _generate_clock_restart_comment(self,
                                       letter_data: Dict[str, Any],
                                       pas_data: Dict[str, Any],
                                       validation_result: Dict[str, Any],
                                       fixes_applied: List[Dict[str, Any]]) -> str:
        """Generate comment for clock restart (Code 11)"""
        parts = []
        
        # Header
        restart_date = letter_data.get('appointment_date')
        letter_date = letter_data.get('letter_date')
        
        parts.append(f"{restart_date} AI AS PER CL DATED {letter_date}")
        parts.append("PATIENT RETURNED FROM ACTIVE MONITORING. CLOCK RESTARTED (CODE 11).")
        
        # Previous stop details
        prev_stop_code = pas_data.get('previous_clock_stop_code')
        prev_stop_date = pas_data.get('previous_clock_stop_date')
        
        if prev_stop_code and prev_stop_date:
            stop_reason = self._get_stop_reason(prev_stop_code)
            parts.append(f"PREVIOUS CLOCK STOPPED {prev_stop_date} - {stop_reason}.")
        
        # Current status
        parts.append("PATIENT NOW READY FOR TREATMENT. ACTIVE TREATMENT PATHWAY RESUMED.")
        
        # Waiting time calculation note
        parts.append("WAITING TIME = PERIOD 1 + PERIOD 2 (WATCHFUL WAIT PERIOD EXCLUDED).")
        
        # Next steps
        follow_up = letter_data.get('follow_up', {})
        if follow_up.get('required'):
            fu_text = self._format_follow_up(follow_up, pas_data)
            parts.append(fu_text)
        
        # PAS updates
        if fixes_applied:
            updates_text = self._format_pas_updates(fixes_applied)
            parts.append(f"PAS UPDATED: {updates_text}.")
        
        return " ".join(parts)
    
    def _determine_appointment_type(self, letter_data: Dict[str, Any]) -> str:
        """Determine appointment type"""
        # Check if first appointment
        if letter_data.get('is_first_appointment'):
            return "FIRST APPOINTMENT"
        else:
            return "REVIEW APPOINTMENT"
    
    def _format_treatments(self, treatments: List[Dict[str, Any]]) -> str:
        """Format treatment details"""
        treatment_parts = []
        
        for treatment in treatments:
            if treatment['treatment_type'] == 'medication':
                med_text = treatment['medication'].upper()
                if treatment.get('dose'):
                    med_text += f" {treatment['dose']}"
                if treatment.get('frequency'):
                    med_text += f" {treatment['frequency']}"
                if treatment.get('purpose'):
                    med_text += f" FOR {treatment['purpose'].upper()}"
                treatment_parts.append(med_text)
            
            elif treatment['treatment_type'] == 'referral':
                ref_text = f"{treatment['referral_to'].upper()} REFERRAL SENT"
                if treatment.get('referral_date'):
                    ref_text += f" {treatment['referral_date']}"
                if treatment.get('duration'):
                    ref_text += f" FOR {treatment['duration']}"
                treatment_parts.append(ref_text)
            
            elif treatment['treatment_type'] == 'surgery':
                treatment_parts.append(f"{treatment.get('procedure', 'SURGERY').upper()} PERFORMED")
        
        return ", ".join(treatment_parts)
    
    def _format_diagnostic_tests(self, tests: List[Dict[str, Any]]) -> str:
        """Format diagnostic test details"""
        test_parts = []
        
        for test in tests:
            test_text = f"{test['test_type'].upper()}"
            if test.get('test_date'):
                test_text += f" {test['test_date']}"
            if test.get('results'):
                test_text += f" - {test['results'].upper()}"
            test_parts.append(test_text)
        
        if test_parts:
            return " ".join(test_parts) + "."
        return ""
    
    def _format_follow_up(self, follow_up: Dict[str, Any], pas_data: Dict[str, Any]) -> str:
        """Format follow-up requirements"""
        fu_text = "F/U"
        
        if follow_up.get('timeframe'):
            fu_text += f" REQUIRED IN {follow_up['timeframe'].upper()}"
        
        if follow_up.get('target_date'):
            fu_text += f" (TARGET {follow_up['target_date']})"
        
        # Check booking status in PAS
        if pas_data.get('follow_up_booked'):
            fu_date = pas_data.get('follow_up_date')
            fu_text += f" - BOOKED FOR {fu_date}"
        else:
            fu_text += " - NOT YET BOOKED"
            fu_text += f" - QUERY SENT TO BOOKING TEAM {datetime.now().strftime('%d/%m/%Y')}"
        
        return fu_text + "."
    
    def _format_future_plans(self, plans: List[Dict[str, Any]]) -> str:
        """Format future treatment plans"""
        plan_parts = []
        
        for plan in plans:
            plan_text = f"CONDITIONAL PLAN: {plan['condition'].upper()}, {plan['action'].upper()}"
            plan_parts.append(plan_text)
        
        return " ".join(plan_parts) + "."
    
    def _format_investigation_requests(self, diagnostics: List[Dict[str, Any]], pas_data: Dict[str, Any]) -> str:
        """Format investigation requests"""
        inv_parts = []
        
        for diagnostic in diagnostics:
            test_type = diagnostic['test_type'].upper()
            
            # Check if ordered in PAS
            if pas_data.get(f'{test_type.lower()}_ordered'):
                if pas_data.get(f'{test_type.lower()}_booked'):
                    date = pas_data.get(f'{test_type.lower()}_date')
                    inv_parts.append(f"{test_type} ORDERED - BOOKED FOR {date}")
                else:
                    inv_parts.append(f"{test_type} ORDERED - AWAITING BOOKING")
            else:
                inv_parts.append(f"{test_type} REQUIRED - QUERY SENT TO RADIOLOGY {datetime.now().strftime('%d/%m/%Y')}")
        
        if inv_parts:
            return "INVESTIGATION REQUESTED: " + ", ".join(inv_parts) + "."
        return ""
    
    def _format_surgery_listing(self, pas_data: Dict[str, Any]) -> str:
        """Format surgery listing status"""
        if pas_data.get('on_waiting_list'):
            if pas_data.get('tci_date'):
                return f"ON SURGICAL WAITING LIST - TCI DATE {pas_data['tci_date']}."
            else:
                return "ON SURGICAL WAITING LIST - AWAITING TCI DATE."
        else:
            return f"AWAITING WAITING LIST ENTRY - QUERY SENT TO ADMIN TEAM {datetime.now().strftime('%d/%m/%Y')}."
    
    def _identify_queries(self, letter_data: Dict[str, Any], pas_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify what queries need to be sent"""
        queries = []
        
        # Check follow-up booking
        follow_up = letter_data.get('follow_up', {})
        if follow_up.get('required') and not pas_data.get('follow_up_booked'):
            queries.append({
                "to": "Booking Team",
                "regarding": "Follow-up appointment booking"
            })
        
        # Check diagnostic bookings
        booking_reqs = letter_data.get('booking_requirements', {})
        for diagnostic in booking_reqs.get('diagnostics', []):
            test_type = diagnostic['test_type']
            if not pas_data.get(f'{test_type.lower()}_ordered'):
                queries.append({
                    "to": "Radiology",
                    "regarding": f"{test_type} scan ordering"
                })
        
        # Check surgery listing
        if booking_reqs.get('surgery') and not pas_data.get('on_waiting_list'):
            queries.append({
                "to": "Admin Team",
                "regarding": "Waiting list entry"
            })
        
        return queries
    
    def _format_queries(self, queries: List[Dict[str, str]]) -> str:
        """Format queries sent"""
        query_date = datetime.now().strftime('%d/%m/%Y')
        query_parts = []
        
        for query in queries:
            query_parts.append(f"QUERY SENT TO {query['to'].upper()} {query_date} RE: {query['regarding'].upper()}")
        
        return ". ".join(query_parts) + "."
    
    def _format_pas_updates(self, fixes_applied: List[Dict[str, Any]]) -> str:
        """Format PAS updates made"""
        update_parts = []
        
        for fix in fixes_applied:
            if fix['rule'] == 'CLOCK_STOP_CODE_INVALID':
                update_parts.append(f"CODE {fix['fixed_value']} ADDED")
            elif fix['rule'] == 'CLOCK_STOP_DATE_MISSING':
                update_parts.append("CLOCK STOPPED")
            elif 'MEDICATION' in fix['action'].upper():
                update_parts.append("MEDICATION RECORDED")
            elif 'REFERRAL' in fix['action'].upper():
                update_parts.append("REFERRAL RECORDED")
            elif 'WAITING_TIME' in fix['rule']:
                update_parts.append("WAITING TIME CORRECTED")
            else:
                update_parts.append(fix['action'].upper())
        
        return ", ".join(update_parts)
    
    def _get_stop_reason(self, rtt_code: int) -> str:
        """Get reason for clock stop based on code"""
        reasons = {
            30: "FIRST DEFINITIVE TREATMENT GIVEN",
            31: "PATIENT WATCHFUL WAIT",
            32: "CLINICIAN WATCHFUL WAIT",
            33: "PATIENT DNA FIRST ACTIVITY",
            34: "DECISION NOT TO TREAT",
            35: "PATIENT DECLINED TREATMENT",
            36: "PATIENT DECEASED"
        }
        return reasons.get(rtt_code, "CLOCK STOPPED")
    
    def _load_templates(self) -> Dict[str, str]:
        """Load comment templates"""
        return {
            "clock_stop": "CS ({date})({code}) AI AS PER CL DATED {letter_date}",
            "clock_continue": "{validation_date} AI AS PER CL DATED {letter_date}",
            "no_letter": "{validation_date} AI NO CLINIC LETTER AVAILABLE",
            "clock_restart": "{date} AI AS PER CL DATED {letter_date} PATIENT RETURNED FROM ACTIVE MONITORING"
        }


# Example usage
if __name__ == "__main__":
    generator = IntelligentCommentGenerator()
    
    # Sample data
    letter_data = {
        "letter_date": "24/05/2025",
        "appointment_date": "23/04/2025",
        "diagnosis": {
            "condition": "Medial meniscus tear",
            "location": "right knee",
            "severity": "complex"
        },
        "treatment_provided": [
            {
                "treatment_type": "medication",
                "medication": "Ibuprofen",
                "dose": "400mg",
                "frequency": "TDS",
                "purpose": "pain relief"
            },
            {
                "treatment_type": "referral",
                "referral_to": "Physiotherapy",
                "referral_date": "24/05/2025",
                "duration": "6 weeks"
            }
        ],
        "diagnostic_tests": [
            {
                "test_type": "MRI",
                "test_date": "15/04/2025",
                "results": "complex tear confirmed"
            }
        ],
        "follow_up": {
            "required": True,
            "timeframe": "8 weeks",
            "target_date": "18/07/2025"
        },
        "future_plans": [
            {
                "condition": "if no improvement after physiotherapy",
                "action": "list for arthroscopic meniscectomy"
            }
        ],
        "rtt_code": 30,
        "clock_action": "STOP"
    }
    
    pas_data = {
        "follow_up_booked": False
    }
    
    validation_result = {}
    
    fixes_applied = [
        {"rule": "CLOCK_STOP_CODE_INVALID", "fixed_value": 30, "action": "Add Code 30"},
        {"action": "Record medication"},
        {"action": "Record physiotherapy referral"}
    ]
    
    # Generate comment
    comment = generator.generate_comment(letter_data, pas_data, validation_result, fixes_applied)
    print(comment)
