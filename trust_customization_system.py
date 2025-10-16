"""
TRUST-SPECIFIC AI CUSTOMIZATION SYSTEM
Allows each NHS Trust to upload their policies and customize AI for their specific workflows

COMPETITIVE ADVANTAGE OVER SIGMA:
- Trust uploads their local RTT policies
- Trust uploads their SOPs and procedures
- AI learns Trust-specific workflows
- Personalized answers for each Trust
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import hashlib


# Trust configuration directory
TRUST_CONFIG_DIR = "trust_configs"
os.makedirs(TRUST_CONFIG_DIR, exist_ok=True)


def get_current_user_email():
    """Get current user email"""
    try:
        import streamlit as st
        return st.session_state.get('user_email', 'demo@t21services.co.uk')
    except:
        return 'demo@t21services.co.uk'


def get_trust_from_email(email: str) -> str:
    """Extract Trust name from email domain"""
    if '@' not in email:
        return 'default_trust'
    
    domain = email.split('@')[1].lower()
    
    # Map common NHS domains to Trust names
    if '.nhs.uk' in domain:
        # Extract Trust identifier from email
        trust_id = domain.replace('.nhs.uk', '').replace('.', '_')
        return trust_id
    else:
        return 'default_trust'


def upload_trust_document(
    trust_id: str,
    document_name: str,
    document_type: str,  # 'policy', 'sop', 'workflow', 'procedure'
    content: str,
    category: str = "RTT Validation",
    uploaded_by: str = ""
) -> Dict:
    """
    Upload Trust-specific document for AI training
    
    Returns: {success: bool, document_id: str, message: str}
    """
    
    try:
        # Generate document ID
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        doc_id = f"{trust_id}_{document_type}_{timestamp}"
        
        # Load or create Trust configuration
        trust_config_file = os.path.join(TRUST_CONFIG_DIR, f"{trust_id}.json")
        
        if os.path.exists(trust_config_file):
            with open(trust_config_file, 'r', encoding='utf-8') as f:
                trust_config = json.load(f)
        else:
            trust_config = {
                'trust_id': trust_id,
                'trust_name': trust_id.replace('_', ' ').title(),
                'documents': [],
                'created_date': datetime.now().isoformat(),
                'ai_training_status': 'pending'
            }
        
        # Add document
        document = {
            'document_id': doc_id,
            'document_name': document_name,
            'document_type': document_type,
            'category': category,
            'content': content,
            'upload_date': datetime.now().isoformat(),
            'uploaded_by': uploaded_by or get_current_user_email(),
            'word_count': len(content.split()),
            'status': 'active'
        }
        
        trust_config['documents'].append(document)
        trust_config['last_updated'] = datetime.now().isoformat()
        trust_config['ai_training_status'] = 'pending'  # Mark for retraining
        
        # Save Trust configuration
        with open(trust_config_file, 'w', encoding='utf-8') as f:
            json.dump(trust_config, f, indent=2)
        
        return {
            'success': True,
            'document_id': doc_id,
            'message': f'Document uploaded successfully. Trust AI will be retrained with this content.',
            'trust_id': trust_id
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Failed to upload document'
        }


def get_trust_documents(trust_id: str) -> List[Dict]:
    """Get all documents for a Trust"""
    
    trust_config_file = os.path.join(TRUST_CONFIG_DIR, f"{trust_id}.json")
    
    if not os.path.exists(trust_config_file):
        return []
    
    try:
        with open(trust_config_file, 'r', encoding='utf-8') as f:
            trust_config = json.load(f)
        
        return trust_config.get('documents', [])
    except:
        return []


def get_trust_config(trust_id: str) -> Dict:
    """Get Trust configuration"""
    
    trust_config_file = os.path.join(TRUST_CONFIG_DIR, f"{trust_id}.json")
    
    if not os.path.exists(trust_config_file):
        return {
            'trust_id': trust_id,
            'trust_name': trust_id.replace('_', ' ').title(),
            'documents': [],
            'ai_training_status': 'not_configured'
        }
    
    try:
        with open(trust_config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            'trust_id': trust_id,
            'trust_name': trust_id.replace('_', ' ').title(),
            'documents': [],
            'ai_training_status': 'error'
        }


def delete_trust_document(trust_id: str, document_id: str) -> Dict:
    """Delete a Trust document"""
    
    trust_config_file = os.path.join(TRUST_CONFIG_DIR, f"{trust_id}.json")
    
    if not os.path.exists(trust_config_file):
        return {'success': False, 'error': 'Trust configuration not found'}
    
    try:
        with open(trust_config_file, 'r', encoding='utf-8') as f:
            trust_config = json.load(f)
        
        # Remove document
        trust_config['documents'] = [
            doc for doc in trust_config['documents']
            if doc['document_id'] != document_id
        ]
        
        trust_config['last_updated'] = datetime.now().isoformat()
        trust_config['ai_training_status'] = 'pending'
        
        with open(trust_config_file, 'w', encoding='utf-8') as f:
            json.dump(trust_config, f, indent=2)
        
        return {
            'success': True,
            'message': 'Document deleted successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_trust_context_for_ai(trust_id: str) -> str:
    """
    Get Trust-specific context to inject into AI prompts
    This gives the AI knowledge of Trust-specific policies
    """
    
    documents = get_trust_documents(trust_id)
    
    if not documents:
        return ""
    
    context = f"\n\n=== TRUST-SPECIFIC CONTEXT FOR {trust_id.upper()} ===\n\n"
    context += "The following are this Trust's specific policies and procedures:\n\n"
    
    for doc in documents:
        if doc.get('status') == 'active':
            context += f"\n--- {doc['document_name']} ({doc['document_type']}) ---\n"
            context += doc['content'][:2000]  # Limit to prevent token overflow
            context += "\n\n"
    
    context += "\n=== END TRUST-SPECIFIC CONTEXT ===\n\n"
    context += "Please prioritize these Trust-specific policies when answering questions.\n\n"
    
    return context


def update_trust_settings(
    trust_id: str,
    trust_name: str = "",
    ai_model_preference: str = "default",
    response_style: str = "professional",
    custom_instructions: str = ""
) -> Dict:
    """Update Trust settings and preferences"""
    
    trust_config_file = os.path.join(TRUST_CONFIG_DIR, f"{trust_id}.json")
    
    try:
        if os.path.exists(trust_config_file):
            with open(trust_config_file, 'r', encoding='utf-8') as f:
                trust_config = json.load(f)
        else:
            trust_config = {
                'trust_id': trust_id,
                'documents': []
            }
        
        # Update settings
        if trust_name:
            trust_config['trust_name'] = trust_name
        
        trust_config['settings'] = {
            'ai_model_preference': ai_model_preference,
            'response_style': response_style,
            'custom_instructions': custom_instructions,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(trust_config_file, 'w', encoding='utf-8') as f:
            json.dump(trust_config, f, indent=2)
        
        return {
            'success': True,
            'message': 'Trust settings updated successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_all_trusts() -> List[Dict]:
    """Get list of all configured Trusts"""
    
    trusts = []
    
    if not os.path.exists(TRUST_CONFIG_DIR):
        return trusts
    
    for filename in os.listdir(TRUST_CONFIG_DIR):
        if filename.endswith('.json'):
            try:
                filepath = os.path.join(TRUST_CONFIG_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                trusts.append({
                    'trust_id': config.get('trust_id'),
                    'trust_name': config.get('trust_name'),
                    'document_count': len(config.get('documents', [])),
                    'ai_training_status': config.get('ai_training_status', 'unknown'),
                    'last_updated': config.get('last_updated', 'N/A')
                })
            except:
                continue
    
    return sorted(trusts, key=lambda x: x.get('trust_name', ''))


def get_trust_statistics(trust_id: str) -> Dict:
    """Get statistics for a Trust's AI customization"""
    
    documents = get_trust_documents(trust_id)
    
    stats = {
        'total_documents': len(documents),
        'by_type': {},
        'total_words': 0,
        'by_category': {},
        'recent_uploads': []
    }
    
    for doc in documents:
        if doc.get('status') == 'active':
            # Count by type
            doc_type = doc.get('document_type', 'unknown')
            stats['by_type'][doc_type] = stats['by_type'].get(doc_type, 0) + 1
            
            # Count by category
            category = doc.get('category', 'uncategorized')
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
            # Total words
            stats['total_words'] += doc.get('word_count', 0)
            
            # Recent uploads (last 5)
            if len(stats['recent_uploads']) < 5:
                stats['recent_uploads'].append({
                    'name': doc['document_name'],
                    'type': doc_type,
                    'date': doc['upload_date']
                })
    
    return stats
