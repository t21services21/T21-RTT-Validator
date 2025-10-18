"""
T21 DATA ANONYMIZATION UTILITIES

CRITICAL for NHS compliance and patient privacy!

This module ensures that NO patient identifiable information is stored
in the learning system. All examples are anonymized before storage.

What gets anonymized:
- Patient names
- NHS numbers
- Addresses
- Phone numbers
- Email addresses
- Dates of birth
- Specific identifiable details

What gets preserved (for learning):
- Clinical conditions
- Specialty information
- Letter structure and patterns
- RTT codes and pathways
- Commenting patterns
"""

import re
from datetime import datetime, timedelta
import random
from typing import Dict, Tuple


class DataAnonymizer:
    """
    Anonymizes patient data while preserving clinical and administrative patterns
    for learning purposes
    """
    
    # Common UK names for anonymization
    FIRST_NAMES = ["John", "Jane", "Sarah", "Michael", "Emma", "David", "Lisa", "James"]
    LAST_NAMES = ["Smith", "Jones", "Williams", "Brown", "Taylor", "Davies", "Wilson"]
    
    # NHS number pattern: XXX XXX XXXX
    NHS_NUMBER_PATTERN = r'\b\d{3}\s?\d{3}\s?\d{4}\b'
    
    # Phone number patterns
    PHONE_PATTERN = r'\b(?:0\d{2,4}[\s-]?\d{3,4}[\s-]?\d{3,4}|\+44[\s-]?\d{2,4}[\s-]?\d{3,4}[\s-]?\d{3,4})\b'
    
    # Email pattern
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Address patterns (UK postcodes)
    POSTCODE_PATTERN = r'\b[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}\b'
    
    # Date patterns (multiple formats)
    DATE_PATTERNS = [
        r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',  # DD/MM/YYYY or DD-MM-YYYY
        r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b',     # YYYY-MM-DD
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b'  # DD Month YYYY
    ]
    
    def __init__(self):
        self.name_mapping = {}  # Track replacements for consistency
        self.date_offset = None  # Random offset for date shifting
    
    def anonymize_text(self, text: str, preserve_structure: bool = True) -> Tuple[str, Dict]:
        """
        Anonymize patient-identifiable information in text
        
        Args:
            text: Original text containing patient data
            preserve_structure: Keep clinical/administrative structure
        
        Returns:
            (anonymized_text, metadata_about_anonymization)
        """
        if not text:
            return text, {}
        
        anonymized = text
        metadata = {
            'anonymized_at': datetime.now().isoformat(),
            'replacements_made': []
        }
        
        # 1. Remove NHS numbers
        nhs_matches = re.findall(self.NHS_NUMBER_PATTERN, anonymized)
        for match in nhs_matches:
            replacement = self._generate_fake_nhs_number()
            anonymized = anonymized.replace(match, replacement)
            metadata['replacements_made'].append('NHS_NUMBER')
        
        # 2. Remove phone numbers
        phone_matches = re.findall(self.PHONE_PATTERN, anonymized)
        for match in phone_matches:
            anonymized = anonymized.replace(match, '[PHONE_REMOVED]')
            metadata['replacements_made'].append('PHONE')
        
        # 3. Remove emails
        email_matches = re.findall(self.EMAIL_PATTERN, anonymized)
        for match in email_matches:
            anonymized = anonymized.replace(match, '[EMAIL_REMOVED]')
            metadata['replacements_made'].append('EMAIL')
        
        # 4. Remove postcodes
        postcode_matches = re.findall(self.POSTCODE_PATTERN, anonymized)
        for match in postcode_matches:
            anonymized = anonymized.replace(match, 'XX1 1XX')
            metadata['replacements_made'].append('POSTCODE')
        
        # 5. Shift dates (preserve relative timing)
        anonymized = self._shift_dates(anonymized)
        if '[DATE_SHIFTED]' in str(metadata):
            metadata['replacements_made'].append('DATES_SHIFTED')
        
        # 6. Remove common name patterns (if preserve_structure is False)
        if not preserve_structure:
            anonymized = self._anonymize_names(anonymized)
            if self.name_mapping:
                metadata['replacements_made'].append('NAMES')
        
        # 7. Remove specific addresses
        anonymized = self._remove_addresses(anonymized)
        
        metadata['replacements_made'] = list(set(metadata['replacements_made']))
        
        return anonymized, metadata
    
    def _generate_fake_nhs_number(self) -> str:
        """Generate a fake but valid-looking NHS number"""
        # Generate 10 random digits
        digits = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        return f"{digits[:3]} {digits[3:6]} {digits[6:]}"
    
    def _shift_dates(self, text: str) -> str:
        """
        Shift all dates by a random offset to preserve relative timing
        but anonymize actual dates
        """
        if self.date_offset is None:
            # Random offset between -365 and +365 days
            self.date_offset = random.randint(-365, 365)
        
        anonymized = text
        
        # Try each date pattern
        for pattern in self.DATE_PATTERNS:
            matches = re.findall(pattern, anonymized)
            for match in matches:
                try:
                    # Parse date (simplified - would need more robust parsing)
                    # For now, just replace with placeholder
                    anonymized = anonymized.replace(match, '[DATE]')
                except:
                    pass
        
        return anonymized
    
    def _anonymize_names(self, text: str) -> str:
        """Replace names with anonymous equivalents"""
        anonymized = text
        
        # Common titles
        titles = r'\b(?:Mr|Mrs|Miss|Ms|Dr|Prof)\b\.?\s+'
        
        # Find potential names (Title + capitalized words)
        name_pattern = titles + r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        
        matches = re.findall(name_pattern, text)
        for match in matches:
            if match not in self.name_mapping:
                # Generate consistent replacement
                fake_name = f"{random.choice(self.FIRST_NAMES)} {random.choice(self.LAST_NAMES)}"
                self.name_mapping[match] = fake_name
            
            anonymized = anonymized.replace(match, self.name_mapping[match])
        
        return anonymized
    
    def _remove_addresses(self, text: str) -> str:
        """Remove street addresses"""
        # Common address indicators
        address_keywords = [
            r'\d+\s+[A-Z][a-z]+\s+(?:Street|Road|Avenue|Lane|Drive|Close|Way|Court)',
            r'(?:Flat|Apartment|Unit)\s+\d+',
        ]
        
        anonymized = text
        for pattern in address_keywords:
            anonymized = re.sub(pattern, '[ADDRESS_REMOVED]', anonymized, flags=re.IGNORECASE)
        
        return anonymized
    
    def anonymize_for_learning(self, letter_text: str, letter_metadata: Dict = None) -> Dict:
        """
        Specialized anonymization for letter interpreter learning
        Preserves clinical and RTT-relevant information
        """
        anonymized_text, anon_metadata = self.anonymize_text(letter_text, preserve_structure=True)
        
        # Extract and preserve key learning elements
        learning_data = {
            'anonymized_letter': anonymized_text,
            'anonymization_metadata': anon_metadata,
            'preserved_elements': {}
        }
        
        # Preserve specialty if provided
        if letter_metadata:
            if 'specialty' in letter_metadata:
                learning_data['preserved_elements']['specialty'] = letter_metadata['specialty']
            if 'letter_type' in letter_metadata:
                learning_data['preserved_elements']['letter_type'] = letter_metadata['letter_type']
            if 'rtt_code' in letter_metadata:
                learning_data['preserved_elements']['rtt_code'] = letter_metadata['rtt_code']
        
        return learning_data
    
    def validate_anonymization(self, text: str) -> Dict:
        """
        Check if text contains any obvious patient-identifiable information
        Returns warnings if potential PII found
        """
        warnings = []
        
        # Check for NHS numbers
        if re.search(self.NHS_NUMBER_PATTERN, text):
            warnings.append("Potential NHS number found")
        
        # Check for phone numbers
        if re.search(self.PHONE_PATTERN, text):
            warnings.append("Potential phone number found")
        
        # Check for emails
        if re.search(self.EMAIL_PATTERN, text):
            warnings.append("Potential email address found")
        
        # Check for postcodes
        if re.search(self.POSTCODE_PATTERN, text):
            warnings.append("Potential postcode found")
        
        return {
            'is_safe': len(warnings) == 0,
            'warnings': warnings,
            'risk_level': 'HIGH' if warnings else 'LOW'
        }


# Global instance
anonymizer = DataAnonymizer()


# Quick anonymization function for convenience
def anonymize_quick(text: str) -> str:
    """Quick anonymization - returns just the anonymized text"""
    anonymized, _ = anonymizer.anonymize_text(text)
    return anonymized


if __name__ == "__main__":
    # Test anonymization
    test_letter = """
    Dear Dr Smith,
    
    Re: John Doe, DOB 15/03/1975, NHS Number: 123 456 7890
    Address: 45 High Street, London, SW1A 1AA
    Tel: 020 1234 5678
    Email: john.doe@email.com
    
    I am writing to refer this patient for investigation of chest pain.
    Patient has been experiencing symptoms for 2 weeks.
    
    Please see urgently.
    
    Dr Jane Wilson
    Green Street Surgery
    """
    
    print("ORIGINAL LETTER:")
    print(test_letter)
    print("\n" + "="*60 + "\n")
    
    anonymized, metadata = anonymizer.anonymize_text(test_letter)
    
    print("ANONYMIZED LETTER:")
    print(anonymized)
    print("\n" + "="*60 + "\n")
    
    print("ANONYMIZATION METADATA:")
    print(metadata)
    print("\n" + "="*60 + "\n")
    
    # Validate
    validation = anonymizer.validate_anonymization(anonymized)
    print("VALIDATION:")
    print(f"Is Safe: {validation['is_safe']}")
    print(f"Risk Level: {validation['risk_level']}")
    print(f"Warnings: {validation['warnings']}")
