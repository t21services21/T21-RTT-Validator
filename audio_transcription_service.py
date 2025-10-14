"""
T21 Audio Transcription Service
Convert doctor dictations to text using OpenAI Whisper

Features:
- Transcribe audio files (MP3, WAV, M4A)
- Recognize medical terminology
- Format as clinic letters
- Auto-populate patient details
- 10x faster than audio typist
"""

import os
from typing import Dict, Any, Optional
import json

class AudioTranscriptionService:
    """Transcribe doctor dictations using AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize transcription service
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("Warning: No OpenAI API key provided. Set OPENAI_API_KEY environment variable.")
        
        self.supported_formats = ['.mp3', '.wav', '.m4a', '.mp4', '.mpeg', '.mpga', '.webm']
        
    def transcribe_audio(self, audio_file_path: str, 
                        language: str = 'en',
                        prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (default: 'en')
            prompt: Optional prompt to guide transcription
            
        Returns:
            Dictionary with transcription and metadata
        """
        # Check file exists
        if not os.path.exists(audio_file_path):
            return {
                "success": False,
                "error": f"File not found: {audio_file_path}"
            }
        
        # Check file format
        file_ext = os.path.splitext(audio_file_path)[1].lower()
        if file_ext not in self.supported_formats:
            return {
                "success": False,
                "error": f"Unsupported format: {file_ext}. Supported: {self.supported_formats}"
            }
        
        try:
            # Import OpenAI (only when needed)
            try:
                import openai
            except ImportError:
                return {
                    "success": False,
                    "error": "OpenAI package not installed. Run: pip install openai"
                }
            
            # Set API key
            openai.api_key = self.api_key
            
            # Open audio file
            with open(audio_file_path, 'rb') as audio_file:
                # Use medical terminology prompt if none provided
                if prompt is None:
                    prompt = self._get_medical_prompt()
                
                # Transcribe using Whisper
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    prompt=prompt,
                    response_format="verbose_json"
                )
            
            return {
                "success": True,
                "text": transcript['text'],
                "language": transcript.get('language'),
                "duration": transcript.get('duration'),
                "segments": transcript.get('segments', [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def transcribe_and_format(self, audio_file_path: str,
                             patient_details: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Transcribe audio and format as clinic letter
        
        Args:
            audio_file_path: Path to audio file
            patient_details: Optional patient details to populate
            
        Returns:
            Dictionary with formatted letter
        """
        # Transcribe audio
        result = self.transcribe_audio(audio_file_path)
        
        if not result['success']:
            return result
        
        # Format as clinic letter
        formatted_letter = self._format_as_letter(
            result['text'],
            patient_details
        )
        
        return {
            "success": True,
            "transcription": result['text'],
            "formatted_letter": formatted_letter,
            "duration": result.get('duration'),
            "word_count": len(result['text'].split())
        }
    
    def _format_as_letter(self, transcription: str,
                         patient_details: Optional[Dict[str, str]] = None) -> str:
        """Format transcription as professional clinic letter"""
        letter_parts = []
        
        # Header
        letter_parts.append("=" * 80)
        letter_parts.append("CLINIC LETTER")
        letter_parts.append("=" * 80)
        letter_parts.append("")
        
        # Date
        from datetime import datetime
        letter_parts.append(f"Date: {datetime.now().strftime('%d/%m/%Y')}")
        letter_parts.append("")
        
        # Patient details
        if patient_details:
            letter_parts.append("PATIENT DETAILS:")
            if patient_details.get('name'):
                letter_parts.append(f"Name: {patient_details['name']}")
            if patient_details.get('nhs_number'):
                letter_parts.append(f"NHS Number: {patient_details['nhs_number']}")
            if patient_details.get('date_of_birth'):
                letter_parts.append(f"Date of Birth: {patient_details['date_of_birth']}")
            letter_parts.append("")
        
        # Transcription content
        letter_parts.append("CONSULTATION NOTES:")
        letter_parts.append("")
        letter_parts.append(transcription)
        letter_parts.append("")
        
        # Footer
        letter_parts.append("=" * 80)
        letter_parts.append("Transcribed using T21 AI Audio Transcription Service")
        letter_parts.append("=" * 80)
        
        return "\n".join(letter_parts)
    
    def _get_medical_prompt(self) -> str:
        """Get prompt with medical terminology"""
        return """This is a medical consultation dictation. 
        Please transcribe accurately including medical terminology such as:
        diagnoses, medications, procedures, anatomical terms, and clinical observations.
        Maintain professional medical language and formatting."""
    
    def batch_transcribe(self, audio_files: list) -> Dict[str, Any]:
        """
        Transcribe multiple audio files
        
        Args:
            audio_files: List of audio file paths
            
        Returns:
            Dictionary with all transcriptions
        """
        results = []
        
        for audio_file in audio_files:
            result = self.transcribe_audio(audio_file)
            results.append({
                "file": audio_file,
                "result": result
            })
        
        successful = sum(1 for r in results if r['result'].get('success'))
        failed = len(results) - successful
        
        return {
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "results": results
        }
    
    def estimate_cost(self, audio_duration_minutes: float) -> float:
        """
        Estimate transcription cost
        
        Args:
            audio_duration_minutes: Duration in minutes
            
        Returns:
            Estimated cost in USD
        """
        # OpenAI Whisper pricing: $0.006 per minute
        cost_per_minute = 0.006
        return audio_duration_minutes * cost_per_minute
    
    def get_audio_duration(self, audio_file_path: str) -> Optional[float]:
        """Get audio file duration in minutes"""
        try:
            import wave
            import contextlib
            
            with contextlib.closing(wave.open(audio_file_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration_seconds = frames / float(rate)
                return duration_seconds / 60.0
        except:
            return None


# Example usage
if __name__ == "__main__":
    service = AudioTranscriptionService()
    
    # Example: Transcribe single audio file
    result = service.transcribe_and_format(
        "doctor_dictation.mp3",
        patient_details={
            "name": "Mr. John Smith",
            "nhs_number": "1234567890",
            "date_of_birth": "01/01/1970"
        }
    )
    
    if result['success']:
        print("Transcription successful!")
        print(f"Duration: {result['duration']} seconds")
        print(f"Word count: {result['word_count']}")
        print("\nFormatted Letter:")
        print(result['formatted_letter'])
    else:
        print(f"Error: {result['error']}")
    
    # Example: Estimate cost
    duration_minutes = 5.0
    cost = service.estimate_cost(duration_minutes)
    print(f"\nEstimated cost for {duration_minutes} minutes: ${cost:.3f}")
