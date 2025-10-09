"""
T21 SERVICES - HL7 FHIR PAS INTEGRATION
Connect to NHS Trust PAS systems via FHIR API
"""

import requests
from datetime import datetime
import json


# FHIR Server Configuration
FHIR_CONFIGS = {
    "nhs_test": {
        "name": "NHS FHIR Test Server",
        "base_url": "https://vonk.fire.ly",  # Public FHIR test server
        "auth_required": False,
        "description": "Public test server for demonstrations"
    },
    "hapi_test": {
        "name": "HAPI FHIR Test Server",
        "base_url": "http://hapi.fhir.org/baseR4",
        "auth_required": False,
        "description": "Public HL7 FHIR test server"
    }
}


class FHIRClient:
    """FHIR API Client for NHS PAS Integration"""
    
    def __init__(self, server="hapi_test"):
        """Initialize FHIR client with server config"""
        if server not in FHIR_CONFIGS:
            raise ValueError(f"Unknown server: {server}")
        
        self.config = FHIR_CONFIGS[server]
        self.base_url = self.config["base_url"]
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json"
        })
    
    def get_patients(self, limit=10):
        """
        Get list of patients from PAS
        
        Returns:
            list: List of patient resources
        """
        try:
            url = f"{self.base_url}/Patient"
            params = {"_count": limit}
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                bundle = response.json()
                
                if bundle.get("resourceType") == "Bundle":
                    patients = []
                    for entry in bundle.get("entry", []):
                        resource = entry.get("resource", {})
                        if resource.get("resourceType") == "Patient":
                            patients.append(self._parse_patient(resource))
                    
                    return patients
            
            return []
        
        except Exception as e:
            print(f"Error fetching patients: {e}")
            return []
    
    def get_patient(self, patient_id):
        """
        Get single patient by ID
        
        Args:
            patient_id: FHIR Patient ID
        
        Returns:
            dict: Patient data
        """
        try:
            url = f"{self.base_url}/Patient/{patient_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                resource = response.json()
                return self._parse_patient(resource)
            
            return None
        
        except Exception as e:
            print(f"Error fetching patient: {e}")
            return None
    
    def _parse_patient(self, resource):
        """Parse FHIR Patient resource into simple dict"""
        try:
            # Extract name
            name_obj = resource.get("name", [{}])[0]
            given_names = name_obj.get("given", [])
            family_name = name_obj.get("family", "")
            full_name = f"{' '.join(given_names)} {family_name}".strip()
            
            # Extract NHS number (identifier)
            nhs_number = "Unknown"
            for identifier in resource.get("identifier", []):
                system = identifier.get("system", "")
                if "nhs" in system.lower():
                    nhs_number = identifier.get("value", "Unknown")
                    break
            
            # If no NHS number found, use first identifier
            if nhs_number == "Unknown" and resource.get("identifier"):
                nhs_number = resource.get("identifier", [{}])[0].get("value", "Unknown")
            
            # Extract other data
            birth_date = resource.get("birthDate", "Unknown")
            gender = resource.get("gender", "Unknown").capitalize()
            
            # Extract address
            address_obj = resource.get("address", [{}])[0]
            city = address_obj.get("city", "")
            postal_code = address_obj.get("postalCode", "")
            address = f"{city}, {postal_code}".strip(", ")
            if not address:
                address = "Unknown"
            
            # Extract phone
            phone = "Unknown"
            for telecom in resource.get("telecom", []):
                if telecom.get("system") == "phone":
                    phone = telecom.get("value", "Unknown")
                    break
            
            return {
                "id": resource.get("id", "Unknown"),
                "nhs_number": nhs_number,
                "full_name": full_name or "Unknown Patient",
                "birth_date": birth_date,
                "gender": gender,
                "address": address,
                "phone": phone,
                "active": resource.get("active", True),
                "resource": resource  # Keep full resource for advanced use
            }
        
        except Exception as e:
            print(f"Error parsing patient: {e}")
            return {
                "id": resource.get("id", "Unknown"),
                "nhs_number": "Unknown",
                "full_name": "Parse Error",
                "birth_date": "Unknown",
                "gender": "Unknown",
                "address": "Unknown",
                "phone": "Unknown",
                "active": True,
                "resource": resource
            }
    
    def get_appointments(self, patient_id=None, limit=10):
        """
        Get appointments from PAS
        
        Args:
            patient_id: Optional patient ID to filter
            limit: Max results
        
        Returns:
            list: List of appointments
        """
        try:
            url = f"{self.base_url}/Appointment"
            params = {"_count": limit}
            
            if patient_id:
                params["patient"] = patient_id
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                bundle = response.json()
                
                if bundle.get("resourceType") == "Bundle":
                    appointments = []
                    for entry in bundle.get("entry", []):
                        resource = entry.get("resource", {})
                        if resource.get("resourceType") == "Appointment":
                            appointments.append(self._parse_appointment(resource))
                    
                    return appointments
            
            return []
        
        except Exception as e:
            print(f"Error fetching appointments: {e}")
            return []
    
    def _parse_appointment(self, resource):
        """Parse FHIR Appointment resource"""
        try:
            return {
                "id": resource.get("id", "Unknown"),
                "status": resource.get("status", "Unknown").capitalize(),
                "start": resource.get("start", "Unknown"),
                "end": resource.get("end", "Unknown"),
                "description": resource.get("description", "No description"),
                "patient_id": self._extract_patient_id(resource),
                "resource": resource
            }
        except Exception as e:
            print(f"Error parsing appointment: {e}")
            return {
                "id": resource.get("id", "Unknown"),
                "status": "Unknown",
                "start": "Unknown",
                "end": "Unknown",
                "description": "Parse Error",
                "patient_id": None,
                "resource": resource
            }
    
    def _extract_patient_id(self, appointment_resource):
        """Extract patient ID from appointment"""
        try:
            for participant in appointment_resource.get("participant", []):
                actor = participant.get("actor", {})
                reference = actor.get("reference", "")
                if "Patient/" in reference:
                    return reference.split("Patient/")[1]
            return None
        except:
            return None
    
    def test_connection(self):
        """Test FHIR server connection"""
        try:
            url = f"{self.base_url}/metadata"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                return True, f"✅ Connected to {self.config['name']}"
            else:
                return False, f"❌ Connection failed: {response.status_code}"
        
        except Exception as e:
            return False, f"❌ Connection error: {str(e)}"


# Quick test function
if __name__ == "__main__":
    print("Testing FHIR Connection...")
    
    client = FHIRClient("hapi_test")
    success, message = client.test_connection()
    print(message)
    
    if success:
        print("\nFetching patients...")
        patients = client.get_patients(limit=5)
        
        print(f"\nFound {len(patients)} patients:")
        for patient in patients:
            print(f"  - {patient['full_name']} (NHS: {patient['nhs_number']})")
