"""
T21 NLP Letter Reading Engine
AI-powered clinic letter analysis and information extraction

Features:
- Extract patient details
- Extract diagnoses
- Extract treatments
- Extract diagnostic tests
- Extract follow-up requirements
- Extract booking status
- Translate to RTT codes
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

class NLPLetterReader:
    """AI-powered clinic letter reader and analyzer"""
    
    def __init__(self):
        """Initialize NLP engine"""
        self.medical_terms = self._load_medical_terms()
        self.rtt_code_rules = self._load_rtt_rules()
        
    def read_letter(self, letter_text: str) -> Dict[str, Any]:
        """
        Read and extract all information from clinic letter
        
        Args:
            letter_text: Full text of clinic letter
            
        Returns:
            Dictionary with all extracted information
        """
        result = {
            "letter_date": self._extract_letter_date(letter_text),
            "appointment_date": self._extract_appointment_date(letter_text),
            "patient_details": self._extract_patient_details(letter_text),
            "consultant": self._extract_consultant(letter_text),
            "specialty": self._extract_specialty(letter_text),
            "diagnosis": self._extract_diagnosis(letter_text),
            "diagnostic_tests": self._extract_diagnostic_tests(letter_text),
            "treatment_provided": self._extract_treatment(letter_text),
            "follow_up": self._extract_follow_up(letter_text),
            "future_plans": self._extract_future_plans(letter_text),
            "rtt_code": self._determine_rtt_code(letter_text),
            "clock_action": self._determine_clock_action(letter_text),
            "booking_requirements": self._extract_booking_requirements(letter_text)
        }
        
        return result
    
    def _extract_letter_date(self, text: str) -> Optional[str]:
        """Extract letter date"""
        patterns = [
            r"Date:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"Dated:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return self._normalize_date(match.group(1))
        
        return None
    
    def _extract_appointment_date(self, text: str) -> Optional[str]:
        """Extract appointment date from letter"""
        patterns = [
            r"attending.*?appointment.*?(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"attended.*?(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"seen.*?(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return self._normalize_date(match.group(1))
        
        return None
    
    def _extract_patient_details(self, text: str) -> Dict[str, str]:
        """Extract patient name and details"""
        details = {}
        
        # Extract patient name
        name_match = re.search(r"Dear\s+(Mr|Mrs|Miss|Ms|Dr)\.?\s+([A-Za-z\s]+)", text, re.IGNORECASE)
        if name_match:
            details["title"] = name_match.group(1)
            details["name"] = name_match.group(2).strip()
        
        return details
    
    def _extract_consultant(self, text: str) -> Optional[str]:
        """Extract consultant name"""
        patterns = [
            r"Yours sincerely,\s*([A-Za-z\s\.]+),\s*Consultant",
            r"([A-Za-z\s\.]+),\s*Consultant"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_specialty(self, text: str) -> Optional[str]:
        """Extract medical specialty"""
        specialties = [
            "Orthopaedic", "Cardiology", "Neurology", "Oncology",
            "General Surgery", "Urology", "Gynaecology", "ENT",
            "Ophthalmology", "Dermatology", "Gastroenterology"
        ]
        
        for specialty in specialties:
            if specialty.lower() in text.lower():
                return specialty
        
        return None
    
    def _extract_diagnosis(self, text: str) -> Dict[str, Any]:
        """Extract diagnosis information"""
        diagnosis = {
            "condition": None,
            "location": None,
            "severity": None
        }
        
        # Look for diagnosis section
        diag_match = re.search(r"DIAGNOSIS:?\s*([^\n]+)", text, re.IGNORECASE)
        if diag_match:
            diagnosis["condition"] = diag_match.group(1).strip()
        
        # Extract body part/location
        body_parts = ["knee", "shoulder", "hip", "ankle", "wrist", "elbow", "back", "neck"]
        for part in body_parts:
            if part in text.lower():
                diagnosis["location"] = part
                break
        
        # Extract severity
        severity_terms = ["complex", "severe", "moderate", "mild", "simple"]
        for term in severity_terms:
            if term in text.lower():
                diagnosis["severity"] = term
                break
        
        return diagnosis
    
    def _extract_diagnostic_tests(self, text: str) -> List[Dict[str, Any]]:
        """Extract diagnostic tests mentioned"""
        tests = []
        
        test_types = {
            "MRI": r"MRI\s*(?:scan)?",
            "CT": r"CT\s*(?:scan)?",
            "X-ray": r"X-?ray",
            "Ultrasound": r"ultrasound",
            "Blood test": r"blood\s*test",
            "ECG": r"ECG|electrocardiogram",
            "Endoscopy": r"endoscopy"
        }
        
        for test_name, pattern in test_types.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Try to find date near the test mention
                context = text[max(0, match.start()-50):min(len(text), match.end()+50)]
                date_match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})", context)
                
                test_info = {
                    "test_type": test_name,
                    "test_date": self._normalize_date(date_match.group(1)) if date_match else None,
                    "results": self._extract_test_results(text, test_name)
                }
                tests.append(test_info)
        
        return tests
    
    def _extract_test_results(self, text: str, test_name: str) -> Optional[str]:
        """Extract results for a specific test"""
        # Look for results after test mention
        pattern = f"{test_name}.*?(?:show|reveal|demonstrate)(?:s|ed)?\\s*([^.]+)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        return None
    
    def _extract_treatment(self, text: str) -> List[Dict[str, Any]]:
        """Extract treatments provided"""
        treatments = []
        
        # Look for medication
        med_pattern = r"(?:prescribed|given)\s+([A-Za-z]+)\s*(\d+mg)?\s*(TDS|BD|OD|QDS)?"
        med_matches = re.finditer(med_pattern, text, re.IGNORECASE)
        
        for match in med_matches:
            treatment = {
                "treatment_type": "medication",
                "medication": match.group(1),
                "dose": match.group(2) if match.group(2) else None,
                "frequency": match.group(3) if match.group(3) else None
            }
            treatments.append(treatment)
        
        # Look for referrals
        ref_pattern = r"referr(?:ed|al)\s+(?:to|for)\s+([A-Za-z\s]+)"
        ref_matches = re.finditer(ref_pattern, text, re.IGNORECASE)
        
        for match in ref_matches:
            treatment = {
                "treatment_type": "referral",
                "referral_to": match.group(1).strip()
            }
            treatments.append(treatment)
        
        # Look for surgery
        if re.search(r"surgery|operation|procedure", text, re.IGNORECASE):
            treatments.append({
                "treatment_type": "surgery",
                "procedure": self._extract_procedure_name(text)
            })
        
        return treatments
    
    def _extract_procedure_name(self, text: str) -> Optional[str]:
        """Extract surgical procedure name"""
        procedures = [
            "arthroscopy", "meniscectomy", "arthroplasty", "replacement",
            "repair", "excision", "biopsy"
        ]
        
        for proc in procedures:
            if proc in text.lower():
                # Get context around procedure
                match = re.search(f"([\\w\\s]+{proc}[\\w\\s]*)", text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        return None
    
    def _extract_follow_up(self, text: str) -> Dict[str, Any]:
        """Extract follow-up requirements"""
        follow_up = {
            "required": False,
            "timeframe": None,
            "target_date": None,
            "booking_status": "unknown"
        }
        
        # Check if follow-up mentioned
        if re.search(r"follow.?up|review", text, re.IGNORECASE):
            follow_up["required"] = True
            
            # Extract timeframe
            time_match = re.search(r"(?:in|after)\s+(\d+)\s+(week|month|day)", text, re.IGNORECASE)
            if time_match:
                follow_up["timeframe"] = f"{time_match.group(1)} {time_match.group(2)}s"
                
                # Calculate target date if appointment date known
                # (would need appointment date from context)
            
            # Check booking status
            if re.search(r"follow.?up\s+(?:booked|arranged|scheduled)", text, re.IGNORECASE):
                follow_up["booking_status"] = "booked"
            elif re.search(r"(?:please|patient to)\s+(?:contact|book|arrange)", text, re.IGNORECASE):
                follow_up["booking_status"] = "to be booked"
        
        return follow_up
    
    def _extract_future_plans(self, text: str) -> List[str]:
        """Extract future treatment plans"""
        plans = []
        
        # Look for conditional plans
        if_match = re.search(r"if\s+([^.]+),\s*([^.]+)", text, re.IGNORECASE)
        if if_match:
            plans.append({
                "condition": if_match.group(1).strip(),
                "action": if_match.group(2).strip()
            })
        
        return plans
    
    def _determine_rtt_code(self, text: str) -> int:
        """Determine appropriate RTT code based on letter content"""
        text_lower = text.lower()
        
        # Code 30 - Treatment given
        if any(word in text_lower for word in ["treated", "prescribed", "surgery performed", "procedure completed"]):
            return 30
        
        # Code 33 - DNA
        if "did not attend" in text_lower or "dna" in text_lower:
            return 33
        
        # Code 34 - Discharge
        if "discharged" in text_lower and "no treatment required" in text_lower:
            return 34
        
        # Code 35 - Patient declined
        if "declined" in text_lower or "refused" in text_lower:
            return 35
        
        # Code 31/32 - Watchful wait
        if "watchful wait" in text_lower or "active monitoring" in text_lower:
            if "patient" in text_lower and "chose" in text_lower:
                return 31
            else:
                return 32
        
        # Code 20 - Subsequent activity (default for appointments/tests)
        return 20
    
    def _determine_clock_action(self, text: str) -> str:
        """Determine if clock should start, stop, or continue"""
        code = self._determine_rtt_code(text)
        
        if code in [30, 31, 32, 33, 34, 35, 36]:
            return "STOP"
        elif code == 11:
            return "RESTART"
        elif code in [10, 12]:
            return "START"
        else:
            return "CONTINUE"
    
    def _extract_booking_requirements(self, text: str) -> Dict[str, Any]:
        """Extract what needs to be booked"""
        requirements = {
            "appointments": [],
            "diagnostics": [],
            "surgery": False
        }
        
        # Check for appointment booking needs
        if re.search(r"(?:book|arrange|schedule).*?appointment", text, re.IGNORECASE):
            requirements["appointments"].append({
                "type": "follow-up",
                "status": "required"
            })
        
        # Check for diagnostic booking needs
        for test in ["MRI", "CT", "X-ray", "ultrasound"]:
            if re.search(f"{test}.*?(?:required|needed|requested)", text, re.IGNORECASE):
                requirements["diagnostics"].append({
                    "test_type": test,
                    "status": "required"
                })
        
        # Check for surgery listing
        if re.search(r"(?:list|add).*?(?:surgery|waiting list)", text, re.IGNORECASE):
            requirements["surgery"] = True
        
        return requirements
    
    def _normalize_date(self, date_str: str) -> str:
        """Normalize date to DD/MM/YYYY format"""
        # Handle different date formats
        date_str = date_str.replace("-", "/")
        parts = date_str.split("/")
        
        if len(parts) == 3:
            day, month, year = parts
            return f"{day.zfill(2)}/{month.zfill(2)}/{year}"
        
        return date_str
    
    def _load_medical_terms(self) -> Dict[str, List[str]]:
        """Load medical terminology dictionary"""
        return {
            "diagnoses": ["tear", "fracture", "sprain", "arthritis", "stenosis"],
            "treatments": ["surgery", "medication", "physiotherapy", "injection"],
            "body_parts": ["knee", "shoulder", "hip", "ankle", "back", "neck"]
        }
    
    def _load_rtt_rules(self) -> Dict[int, str]:
        """Load RTT code rules"""
        return {
            10: "First activity after referral",
            11: "First activity after watchful wait ends",
            12: "Consultant referral for new condition",
            20: "Subsequent activity",
            21: "Transfer to another provider",
            30: "First definitive treatment",
            31: "Watchful wait - patient initiated",
            32: "Watchful wait - clinician initiated",
            33: "DNA first activity",
            34: "Decision not to treat",
            35: "Patient declined treatment",
            36: "Patient deceased"
        }


# Example usage
if __name__ == "__main__":
    reader = NLPLetterReader()
    
    sample_letter = """
    Date: 24/05/2025
    Dear Mr. Smith,
    
    Thank you for attending your appointment on 23/04/2025.
    
    I have reviewed your MRI scan results from 15/04/2025 which show a 
    complex tear of the medial meniscus in your right knee.
    
    DIAGNOSIS: Medial meniscus tear, right knee
    
    TREATMENT PROVIDED: I have prescribed Ibuprofen 400mg TDS for pain relief
    and referred you for physiotherapy.
    
    PLAN: 
    - Physiotherapy for 6 weeks
    - Review appointment required in 8 weeks
    - If no improvement, will list for arthroscopic surgery
    
    Yours sincerely,
    Mr. Williams, Consultant Orthopaedic Surgeon
    """
    
    result = reader.read_letter(sample_letter)
    print(json.dumps(result, indent=2))
