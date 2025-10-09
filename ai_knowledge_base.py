"""
T21 AI KNOWLEDGE BASE SYSTEM
Upload and manage training materials for AI to learn from

Features:
- Upload training documents (PDF, DOCX, TXT)
- Extract and store knowledge
- Vector embeddings for semantic search
- AI can reference your materials
- Fine-tuning preparation
- Material versioning
"""

import json
import os
from datetime import datetime
from typing import List, Dict


# Database for knowledge base
KNOWLEDGE_BASE_DB = "ai_knowledge_base.json"
MATERIALS_DB = "training_materials.json"


def load_knowledge_base():
    """Load the knowledge base"""
    if os.path.exists(KNOWLEDGE_BASE_DB):
        with open(KNOWLEDGE_BASE_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'materials': [], 'chunks': []}


def save_knowledge_base(data):
    """Save the knowledge base"""
    with open(KNOWLEDGE_BASE_DB, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_materials():
    """Load training materials metadata"""
    if os.path.exists(MATERIALS_DB):
        with open(MATERIALS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_materials(materials):
    """Save training materials metadata"""
    with open(MATERIALS_DB, 'w', encoding='utf-8') as f:
        json.dump(materials, f, indent=2)


def generate_material_id():
    """Generate unique material ID"""
    return f"MAT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(3).hex()}"


def add_training_material(
    title: str,
    content: str,
    material_type: str,
    category: str,
    description: str = "",
    tags: List[str] = None,
    file_name: str = ""
):
    """
    Add training material to knowledge base
    
    Args:
        title: Material title
        content: Full text content
        material_type: Type (PDF, Document, Video Transcript, etc.)
        category: Category (RTT Rules, Case Studies, Guidelines, etc.)
        description: Description
        tags: List of tags
        file_name: Original file name
    """
    
    material_id = generate_material_id()
    
    # Create material metadata
    material = {
        'material_id': material_id,
        'title': title,
        'description': description,
        'material_type': material_type,
        'category': category,
        'tags': tags or [],
        'file_name': file_name,
        'upload_date': datetime.now().isoformat(),
        'status': 'active',
        'word_count': len(content.split()),
        'character_count': len(content)
    }
    
    # Save material metadata
    materials = load_materials()
    materials.append(material)
    save_materials(materials)
    
    # Process content into chunks for AI
    chunks = chunk_content(content, material_id, title)
    
    # Add to knowledge base
    kb = load_knowledge_base()
    kb['materials'].append(material)
    kb['chunks'].extend(chunks)
    save_knowledge_base(kb)
    
    return material_id


def chunk_content(content: str, material_id: str, title: str, chunk_size: int = 1000):
    """
    Split content into chunks for AI processing
    
    Args:
        content: Full text content
        material_id: Material ID
        title: Material title
        chunk_size: Characters per chunk
    """
    
    chunks = []
    words = content.split()
    current_chunk = []
    current_size = 0
    chunk_num = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1
        
        if current_size >= chunk_size:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'chunk_id': f"{material_id}_CHUNK_{chunk_num}",
                'material_id': material_id,
                'material_title': title,
                'chunk_number': chunk_num,
                'content': chunk_text,
                'word_count': len(current_chunk)
            })
            
            current_chunk = []
            current_size = 0
            chunk_num += 1
    
    # Add remaining words
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        chunks.append({
            'chunk_id': f"{material_id}_CHUNK_{chunk_num}",
            'material_id': material_id,
            'material_title': title,
            'chunk_number': chunk_num,
            'content': chunk_text,
            'word_count': len(current_chunk)
        })
    
    return chunks


def search_knowledge_base(query: str, category: str = None, limit: int = 5):
    """
    Search knowledge base for relevant information
    
    Args:
        query: Search query
        category: Filter by category (optional)
        limit: Max results
    """
    
    kb = load_knowledge_base()
    chunks = kb['chunks']
    
    # Filter by category if specified
    if category:
        chunks = [c for c in chunks if any(
            m['material_id'] == c['material_id'] and m['category'] == category
            for m in kb['materials']
        )]
    
    # Simple keyword search (can be enhanced with vector embeddings)
    query_words = query.lower().split()
    results = []
    
    for chunk in chunks:
        content_lower = chunk['content'].lower()
        score = sum(1 for word in query_words if word in content_lower)
        
        if score > 0:
            results.append({
                'chunk': chunk,
                'score': score
            })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return [r['chunk'] for r in results[:limit]]


def get_all_materials():
    """Get all training materials"""
    return load_materials()


def get_material_by_id(material_id: str):
    """Get specific material"""
    materials = load_materials()
    for material in materials:
        if material['material_id'] == material_id:
            return material
    return None


def get_materials_by_category(category: str):
    """Get materials by category"""
    materials = load_materials()
    return [m for m in materials if m['category'] == category]


def delete_material(material_id: str):
    """Delete a material and its chunks"""
    
    # Remove from materials
    materials = load_materials()
    materials = [m for m in materials if m['material_id'] != material_id]
    save_materials(materials)
    
    # Remove from knowledge base
    kb = load_knowledge_base()
    kb['materials'] = [m for m in kb['materials'] if m['material_id'] != material_id]
    kb['chunks'] = [c for c in kb['chunks'] if c['material_id'] != material_id]
    save_knowledge_base(kb)
    
    return True


def get_knowledge_base_stats():
    """Get statistics about knowledge base"""
    
    materials = load_materials()
    kb = load_knowledge_base()
    
    stats = {
        'total_materials': len(materials),
        'total_chunks': len(kb['chunks']),
        'total_words': sum(m['word_count'] for m in materials),
        'categories': {},
        'material_types': {},
        'recent_uploads': []
    }
    
    # Count by category
    for material in materials:
        category = material['category']
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        material_type = material['material_type']
        stats['material_types'][material_type] = stats['material_types'].get(material_type, 0) + 1
    
    # Get recent uploads
    sorted_materials = sorted(materials, key=lambda x: x['upload_date'], reverse=True)
    stats['recent_uploads'] = sorted_materials[:5]
    
    return stats


def prepare_fine_tuning_data():
    """
    Prepare data for fine-tuning OpenAI model
    
    Returns JSONL format for fine-tuning
    """
    
    kb = load_knowledge_base()
    fine_tune_data = []
    
    for chunk in kb['chunks']:
        # Create training example
        example = {
            "messages": [
                {"role": "system", "content": "You are an expert NHS RTT (Referral to Treatment) pathway validator and coordinator."},
                {"role": "user", "content": f"What do you know about: {chunk['material_title']}?"},
                {"role": "assistant", "content": chunk['content']}
            ]
        }
        fine_tune_data.append(example)
    
    return fine_tune_data


def export_knowledge_for_ai():
    """
    Export all knowledge in format for AI to consume
    Returns concatenated content for AI context
    """
    
    kb = load_knowledge_base()
    materials = kb['materials']
    chunks = kb['chunks']
    
    # Group chunks by material
    content_by_material = {}
    for chunk in chunks:
        material_id = chunk['material_id']
        if material_id not in content_by_material:
            content_by_material[material_id] = []
        content_by_material[material_id].append(chunk)
    
    # Build full knowledge base text
    full_content = "# T21 RTT TRAINING KNOWLEDGE BASE\n\n"
    
    for material in materials:
        material_id = material['material_id']
        full_content += f"## {material['title']}\n"
        full_content += f"**Category:** {material['category']}\n"
        full_content += f"**Type:** {material['material_type']}\n\n"
        
        # Add all chunks for this material
        if material_id in content_by_material:
            material_chunks = sorted(content_by_material[material_id], 
                                   key=lambda x: x['chunk_number'])
            for chunk in material_chunks:
                full_content += chunk['content'] + "\n\n"
        
        full_content += "---\n\n"
    
    return full_content


def save_knowledge_export(filename: str = "ai_knowledge_export.txt"):
    """Save exported knowledge to file"""
    content = export_knowledge_for_ai()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename
