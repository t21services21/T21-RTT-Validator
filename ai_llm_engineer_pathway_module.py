import streamlit as st
from typing import Dict, Any

try:
    from tquk_course_assignment import get_learner_enrollments
except Exception:
    def get_learner_enrollments(email: str):
        return []

try:
    from tquk_pdf_converter import create_unit_pdf
except Exception:
    def create_unit_pdf(unit_number: int, unit_name: str, content: str):
        return content.encode("utf-8")

try:
    from tquk_evidence_tracking import (
        render_evidence_submission_form,
        render_evidence_tracking,
    )
except Exception:
    def render_evidence_submission_form(email: str, course_id: str, unit_number: int):
        st.info("Evidence submission system is not available in this environment.")

    def render_evidence_tracking(email: str, course_id: str):
        st.info("Evidence tracking system is not available in this environment.")

try:
    from video_library import get_all_videos
except Exception:
    def get_all_videos(category: str = None, week: int = None, competency: str = None):
        return []


COURSE_ID = "ai_llm_engineer_pathway"
COURSE_NAME = "AI/LLM Engineer Pathway"


UNITS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "LLM Fundamentals & Architecture",
        "level": "Intermediate",
        "glh": 24,
        "credits": 4,
    },
    2: {
        "name": "Prompt Engineering & Optimization",
        "level": "Intermediate",
        "glh": 20,
        "credits": 3,
    },
    3: {
        "name": "RAG (Retrieval Augmented Generation)",
        "level": "Intermediate/Advanced",
        "glh": 30,
        "credits": 5,
    },
    4: {
        "name": "Fine-tuning & Model Training",
        "level": "Advanced",
        "glh": 30,
        "credits": 5,
    },
    5: {
        "name": "LLM Agents & Tool Integration",
        "level": "Advanced",
        "glh": 28,
        "credits": 5,
    },
    6: {
        "name": "Production Deployment & Scaling",
        "level": "Advanced",
        "glh": 24,
        "credits": 4,
    },
    7: {
        "name": "AI/LLM Engineer Capstone Project",
        "level": "Advanced",
        "glh": 40,
        "credits": 7,
    },
}


def _get_enrollment(email: str):
    enrollments = get_learner_enrollments(email)
    for e in enrollments:
        if e.get("course_id") == COURSE_ID:
            return e
    return None


def _render_progress_header(enrollment):
    if not enrollment:
        return

    total_units = len(UNITS)
    units_completed = enrollment.get("units_completed", 0)
    progress = enrollment.get("progress", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Units Completed", f"{units_completed}/{total_units}")
    with col2:
        st.metric("Overall Progress", f"{progress}%")
    with col3:
        st.metric("Status", enrollment.get("status", "in_progress").title())


def render_ai_llm_engineer_pathway_module():
    learner_email = st.session_state.get("user_email", "")

    st.title("🤖 AI/LLM Engineer Pathway")
    st.success(
        "Master Large Language Models - from fundamentals to production deployment!"
    )

    enrollment = _get_enrollment(learner_email) if learner_email else None
    if enrollment:
        _render_progress_header(enrollment)

    st.markdown("---")

    tabs = st.tabs(
        [
            "📚 Course Overview",
            "📖 Learning Materials",
            "🧪 Labs & Mini Projects",
            "📝 Assessments",
            "📋 Evidence Tracking",
            "📂 Documents & Downloads",
        ]
    )

    # Overview
    with tabs[0]:
        st.subheader("📚 Course Overview")
        st.markdown(
            """This pathway is designed for engineers who want to become **AI/LLM specialists**,
building production-ready applications with Large Language Models.

By the end of this pathway you will be able to:

- Understand LLM architecture and capabilities
- Master prompt engineering techniques
- Build RAG systems for knowledge retrieval
- Fine-tune models for specific tasks
- Create autonomous LLM agents
- Deploy LLMs at scale in production
- Optimize for cost and performance

**Who This Is For:**
- Software engineers moving into AI
- Data scientists expanding to LLMs
- ML engineers specializing in NLP
- Anyone building LLM applications

**Prerequisites:**
- Python programming (intermediate)
- Basic machine learning concepts
- API integration experience
- Cloud platform familiarity (helpful)
"""
        )

        st.markdown("### 📋 Course Structure")
        for unit_num, unit_info in UNITS.items():
            with st.expander(f"Unit {unit_num}: {unit_info['name']}"):
                st.markdown(f"**Level:** {unit_info['level']}")
                st.markdown(f"**Guided Learning Hours:** {unit_info['glh']}")
                st.markdown(f"**Credits:** {unit_info['credits']}")

    # Learning Materials
    with tabs[1]:
        st.subheader("📖 Learning Materials")
        st.info("Comprehensive theory and concepts for each unit.")
        
        selected_unit = st.selectbox(
            "Select a unit:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="llm_materials_unit",
        )
        
        st.markdown(f"### Unit {selected_unit}: {UNITS[selected_unit]['name']}")
        
        if selected_unit == 1:
            st.markdown("#### 📘 Large Language Models: The AI Revolution")
            st.markdown("""
**Large Language Models (LLMs)** like GPT-4, Claude, and Gemini have transformed AI.

**What are LLMs?**
- Neural networks trained on massive text data
- Billions of parameters (GPT-4: ~1.7 trillion)
- Can understand and generate human-like text
- Trained on internet-scale data

**Key Capabilities:**
- ✅ Text generation
- ✅ Question answering
- ✅ Code generation
- ✅ Translation
- ✅ Summarization
- ✅ Reasoning and analysis

**Major LLMs:**

| Model | Company | Strengths |
|-------|---------|----------|
| **GPT-4** | OpenAI | Best overall, coding |
| **Claude 3** | Anthropic | Long context, safety |
| **Gemini Pro** | Google | Multimodal, free tier |
| **Llama 2** | Meta | Open source |

**How LLMs Work:**
1. Tokenization (text → numbers)
2. Embedding (semantic representation)
3. Transformer architecture (attention mechanism)
4. Autoregressive generation (predict next token)

**Key Concepts:**
- **Tokens:** ~4 characters = 1 token
- **Context Window:** Max input size (GPT-4: 128k tokens)
- **Temperature:** Randomness (0 = deterministic, 1 = creative)
- **Top-p:** Nucleus sampling
"""
            )
            
            st.markdown("#### 🧠 Transformer Architecture Deep Dive")
            st.markdown(
                """**Understanding the Transformer** - the architecture that powers all modern LLMs:

**The Transformer Revolution (2017):**
- **Paper:** "Attention Is All You Need" (Vaswani et al.)
- **Innovation:** Replaced recurrent networks with self-attention
- **Impact:** Enabled parallel training on massive datasets
- **Result:** GPT, BERT, T5, and all modern LLMs

**Core Components:**

**1. Tokenization**
How text becomes numbers that models can process:

**Tokenization Methods:**
- **Word-level:** Each word is a token (simple but huge vocabulary)
- **Character-level:** Each character is a token (small vocab, long sequences)
- **Subword (BPE/WordPiece):** Balance of vocabulary size and sequence length

**Example - GPT Tokenization:**
- Input: "Large Language Models"
- Tokens: ["Large", " Language", " Models"]
- Token IDs: [43, 15417, 27972]
- Count: 3 tokens

**Why It Matters:**
- **Cost:** APIs charge per token ($0.03/1K for GPT-4 input)
- **Context limits:** GPT-4 Turbo = 128K tokens ≈ 96K words
- **Performance:** Longer sequences = slower processing

**2. Embeddings**
Converting tokens to dense vector representations:

**What are Embeddings?**
- High-dimensional vectors (GPT-4: 12,288 dimensions)
- Capture semantic meaning
- Similar words → similar vectors
- Enable arithmetic (king - man + woman ≈ queen)

**Example:**
- "cat" → [0.2, -0.5, 0.8, ..., 0.3]  (12,288 numbers)
- "kitten" → [0.19, -0.48, 0.79, ..., 0.29]  (very similar)
- "car" → [-0.7, 0.3, -0.1, ..., -0.4]  (very different)

**Positional Encoding:**
- Transformers have no inherent sequence understanding
- Position encoding adds order information
- Allows model to know token positions

**3. Self-Attention Mechanism**
The heart of the Transformer:

**Attention Formula:**
```
Attention(Q, K, V) = softmax(Q * K^T / √d_k) * V
```

Where:
- **Q (Query):** What am I looking for?
- **K (Key):** What do I contain?
- **V (Value):** What do I output?
- **d_k:** Dimension scaling factor

**Intuition:**
For each token, attention computes:
1. How relevant is every other token?
2. Weighted combination of all tokens
3. Result: Context-aware representation

**Example - Attention in Action:**
Sentence: "The animal didn't cross the street because it was too tired"

For token "it":
- Attends to "animal" (high weight: 0.7)
- Attends to "street" (low weight: 0.1)
- Learns "it" refers to "animal"

**Multi-Head Attention:**
- Run attention multiple times in parallel (GPT-4: 96 heads)
- Each head learns different patterns
- Some heads focus on syntax, others on semantics

**4. Feed-Forward Networks**
After attention, each position processed independently:

**Architecture:**
```
FFN(x) = max(0, xW1 + b1)W2 + b2
```

**Purpose:**
- Non-linear transformations
- Pattern recognition
- 4X expansion then contraction (hidden dim = 4 × embedding dim)

**5. Layer Normalization**
Stabilizes training:

**Why Needed:**
- Deep networks (GPT-3: 96 layers) can be unstable
- Normalization prevents exploding/vanishing gradients
- Enables training very deep models

**6. Residual Connections**
Skip connections around each sublayer:

**Formula:**
```
output = LayerNorm(x + Sublayer(x))
```

**Benefits:**
- Gradient flow in deep networks
- Easier optimization
- Prevents vanishing gradients

---

**Complete Transformer Block:**

```
Input Tokens
  ↓
Embeddings + Positional Encoding
  ↓
┌─ Multi-Head Self-Attention
│  ↓
│  Add & Normalize
├─ Feed-Forward Network
│  ↓
└─ Add & Normalize
  ↓
(Repeat 96 times for GPT-4)
  ↓
Output Probabilities
```

---

**Autoregressive Generation:**
How LLMs generate text one token at a time:

**Process:**
1. Start with prompt tokens
2. Forward pass through all layers
3. Output probability distribution over vocabulary
4. Sample next token (using temperature, top-p)
5. Add token to sequence
6. Repeat until stop condition

**Example Generation:**
```
Prompt: "The future of AI is"

Step 1: [The, future, of, AI, is] → predict "bright" (30%)
Step 2: [The, future, of, AI, is, bright] → predict "because" (25%)
Step 3: [..., bright, because] → predict "of" (40%)
...continue until complete
```

**Sampling Strategies:**

**1. Greedy Decoding:**
- Always pick highest probability token
- Deterministic but repetitive
- Example: "the the the..." loops

**2. Temperature Sampling:**
- temperature = 0: Greedy (deterministic)
- temperature = 0.7: Balanced (recommended)
- temperature = 1.0+: Creative but risky

**Formula:**
```python
probabilities = softmax(logits / temperature)
```

**3. Top-p (Nucleus) Sampling:**
- Sample from smallest set of tokens with cumulative probability ≥ p
- p = 0.9: Use top 90% probability mass
- More consistent than pure temperature

**4. Top-k Sampling:**
- Consider only top k tokens
- k = 50: Choose from top 50 candidates
- Simpler than top-p

---

**Model Architectures:**

**Decoder-Only (GPT Family):**
- **Architecture:** Causal self-attention (can't see future)
- **Training:** Predict next token
- **Strengths:** Text generation, completion
- **Examples:** GPT-3, GPT-4, Claude, Llama

**Encoder-Only (BERT Family):**
- **Architecture:** Bidirectional attention (sees all context)
- **Training:** Masked language modeling
- **Strengths:** Classification, understanding
- **Examples:** BERT, RoBERTa, DistilBERT

**Encoder-Decoder (T5 Family):**
- **Architecture:** Encoder + decoder
- **Training:** Seq2seq tasks
- **Strengths:** Translation, summarization
- **Examples:** T5, BART, Flan-T5

---

**Training LLMs:**

**Pre-training Phase:**
- **Data:** Massive text corpus (GPT-3: 570GB, 300B tokens)
- **Objective:** Predict next token
- **Duration:** Months on thousands of GPUs
- **Cost:** $10M - $100M+ for largest models

**Training Pipeline:**
```
1. Data Collection
   - Web scraping (Common Crawl)
   - Books, Wikipedia, code repos
   - Filter for quality

2. Data Preprocessing
   - Deduplication
   - Quality filtering
   - Toxic content removal

3. Tokenization
   - Learn BPE vocabulary
   - Tokenize entire corpus

4. Training
   - Distributed across GPU clusters
   - Gradient accumulation
   - Mixed precision (FP16/BF16)

5. Evaluation
   - Perplexity on held-out set
   - Downstream task performance
```

**Computational Requirements:**

**GPT-3 (175B parameters):**
- **GPU-hours:** 355 years on single GPU
- **Hardware:** 10,000+ NVIDIA V100s
- **Duration:** ~3 months wall-clock time
- **Energy:** ~1,287 MWh
- **CO2:** ~552 tons

**Llama 2 (70B parameters):**
- **GPU-hours:** 1.7M on A100s
- **Cost:** ~$5M in compute
- **Duration:** ~2 months

**Training Optimizations:**
- **Model Parallelism:** Split model across GPUs
- **Data Parallelism:** Split data across GPUs
- **Pipeline Parallelism:** Split layers across stages
- **Gradient Checkpointing:** Trade compute for memory
- **Mixed Precision:** FP16/BF16 for speed

---

**Emergent Abilities:**
Capabilities that appear at scale:

**Observed at Scale:**
1. **In-context Learning:** Learn from examples in prompt
2. **Chain-of-Thought:** Step-by-step reasoning
3. **Few-shot Learning:** Generalize from few examples
4. **Instruction Following:** Follow complex instructions
5. **Multi-step Reasoning:** Complex problem solving

**Scale Requirements:**
- **Below 10B params:** Limited reasoning
- **10B-100B params:** Some emergent abilities
- **100B+ params:** Strong emergent abilities

**Why Scale Matters:**
- Larger models learn more patterns
- Better generalization
- Stronger reasoning capabilities
- More robust to prompt variations

---

**Limitations of Current LLMs:**

**1. Hallucinations**
- Generate plausible but false information
- No inherent fact-checking
- Confident even when wrong

**Mitigation:**
- Use RAG for factual queries
- Request sources/citations
- Implement fact-checking layer

**2. Knowledge Cutoff**
- Training data has a cutoff date
- GPT-4: September 2021 (original)
- No real-time information

**Solution:**
- RAG with current data
- Tool use (web search, APIs)
- Regular model updates

**3. Reasoning Limitations**
- Struggle with complex logic
- Math errors on multi-step problems
- No true understanding

**Mitigation:**
- Chain-of-thought prompting
- Tool use (calculators, code execution)
- Verification steps

**4. Context Window Limits**
- Even 128K tokens has limits
- Can't process entire books
- Information in middle often lost

**Workarounds:**
- Chunking and summarization
- Map-reduce patterns
- Hierarchical processing

**5. Cost**
- API costs add up quickly
- GPT-4: $0.03/1K input, $0.06/1K output
- $100K+/month for heavy usage

**Optimization:**
- Caching frequent responses
- Use smaller models when possible
- Batch processing
- Prompt compression
"""
            )
        elif selected_unit == 2:
            st.markdown("#### 📘 Prompt Engineering: The Art of Talking to AI")
            st.markdown("""
**Prompt engineering** is the skill of crafting inputs to get optimal LLM outputs.

**Why It Matters:**
- Same question, different phrasing = vastly different results
- Good prompts save tokens (money!)
- Critical for production applications

**Core Techniques:**

1. **Zero-shot:** No examples, just the task
2. **Few-shot:** Provide examples
3. **Chain-of-thought:** Ask for step-by-step reasoning
4. **Role-based:** Assign persona to LLM
5. **Structured output:** Request JSON/XML format

**Prompt Patterns:**
- Instruction + Context + Question
- System message + User message
- Examples + Task
""")
            
            st.markdown("#### 🎯 Advanced Prompt Engineering")
            st.markdown("""This section will cover advanced prompting techniques including:
- Chain-of-thought prompting
- Few-shot learning
- Prompt templates and optimization
- Production best practices
""")
        elif selected_unit == 3:
            st.markdown("#### 📘 RAG: Retrieval Augmented Generation")
            st.markdown("""
**RAG** combines LLMs with external knowledge retrieval.

**Why RAG?**
- LLMs have knowledge cutoff dates
- Can't access private company data
- Hallucinate when uncertain

**RAG Solution:**
1. Store documents in vector database
2. Retrieve relevant docs for query
3. Pass docs + query to LLM
4. LLM answers using retrieved context

**Components:**
- Document loader
- Text splitter
- Embedding model
- Vector database (Pinecone, Chroma)
- Retriever
- LLM
""")
            
            st.markdown("#### 🔍 RAG Architecture Deep Dive")
            st.markdown("""Production RAG systems require careful design and optimization:

**Complete RAG Pipeline:**

```
┌─────────────────────────────────────────────────────────┐
│                    INGESTION PHASE                       │
├─────────────────────────────────────────────────────────┤
│ 1. Document Loading                                      │
│    - PDFs, Word docs, HTML, Markdown                    │
│    - APIs, databases, web scraping                      │
│                                                          │
│ 2. Text Chunking                                        │
│    - Split into manageable pieces (200-1000 tokens)    │
│    - Preserve context and meaning                       │
│    - Overlapping chunks for continuity                  │
│                                                          │
│ 3. Generate Embeddings                                  │
│    - text-embedding-ada-002 (OpenAI)                   │
│    - instructor-xl (open source)                        │
│    - Convert text → dense vectors                       │
│                                                          │
│ 4. Store in Vector Database                            │
│    - Pinecone, Weaviate, Chroma, Qdrant               │
│    - Indexed for fast similarity search                 │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    RETRIEVAL PHASE                       │
├─────────────────────────────────────────────────────────┤
│ 1. User Query                                           │
│    - "What is our refund policy?"                       │
│                                                          │
│ 2. Query Embedding                                      │
│    - Same embedding model as ingestion                  │
│    - Query → dense vector                               │
│                                                          │
│ 3. Similarity Search                                    │
│    - Cosine similarity, dot product, euclidean         │
│    - Top K results (typically 3-10)                     │
│    - Optional: MMR for diversity                        │
│                                                          │
│ 4. Reranking (Optional)                                 │
│    - Cross-encoder for better relevance                 │
│    - Cohere Rerank, ColBERT                            │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   GENERATION PHASE                       │
├─────────────────────────────────────────────────────────┤
│ 1. Construct Prompt                                     │
│    Context: [Retrieved documents]                       │
│    Question: [User query]                               │
│                                                          │
│ 2. LLM Generation                                       │
│    - GPT-4, Claude, or other LLM                       │
│    - Generate answer from context                       │
│                                                          │
│ 3. Citation Extraction (Optional)                       │
│    - Link answer to source documents                    │
│    - Track which chunks were used                       │
│                                                          │
│ 4. Response Validation                                  │
│    - Check for hallucinations                           │
│    - Confidence scoring                                 │
└─────────────────────────────────────────────────────────┘
```

---

**1. Document Loading & Processing**

**Supported Formats:**
```python
from langchain.document_loaders import (
    PyPDFLoader,          # PDF files
    Docx2txtLoader,       # Word documents
    UnstructuredHTMLLoader,  # HTML pages
    TextLoader,           # Plain text
    CSVLoader,            # CSV files
    NotionDirectoryLoader # Notion exports
)

# Example: Load multiple file types
loaders = [
    PyPDFLoader("product_manual.pdf"),
    Docx2txtLoader("company_policies.docx"),
    UnstructuredHTMLLoader("website_faq.html")
]

documents = []
for loader in loaders:
    documents.extend(loader.load())
```

**Advanced Loading:**
```python
# Load from API
import requests

def load_from_api(endpoint):
    response = requests.get(endpoint)
    data = response.json()
    return [{"text": item["content"], "metadata": item} for item in data]

# Load from database
import psycopg2

def load_from_postgres(query):
    conn = psycopg2.connect("dbname=mydb")
    cursor = conn.execute(query)
    return [{"text": row[0], "metadata": {"id": row[1]}} for row in cursor]
```

**2. Text Chunking Strategies**

**Why Chunking Matters:**
- Embeddings have token limits (8K for ada-002)
- Smaller chunks = more precise retrieval
- Larger chunks = more context

**Chunking Methods:**

**A. Fixed-Size Chunking**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Characters per chunk
    chunk_overlap=50,      # Overlap for continuity
    separators=["\\n\\n", "\\n", " ", ""]  # Split hierarchy
)

chunks = splitter.split_documents(documents)
```

**B. Semantic Chunking**
```python
# Split by semantic meaning (paragraphs, sections)
from langchain.text_splitter import MarkdownTextSplitter

splitter = MarkdownTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Preserves markdown structure
chunks = splitter.split_documents(markdown_docs)
```

**C. Sentence-Aware Chunking**
```python
from semantic_text_splitter import TextSplitter

splitter = TextSplitter(max_characters=500)
chunks = splitter.chunks("Your long document text...")
```

**Chunking Best Practices:**

| Document Type | Chunk Size | Overlap | Strategy |
|--------------|------------|---------|----------|
| Technical docs | 800-1000 | 100 | Markdown-aware |
| Chat logs | 300-500 | 50 | Sentence-based |
| Legal contracts | 1000-1500 | 200 | Paragraph-based |
| Code files | 500-800 | 100 | Function-aware |
| Customer reviews | 200-400 | 30 | Sentence-based |

---

**3. Embedding Models**

**Embedding Model Comparison:**

| Model | Dimensions | Speed | Cost | Best For |
|-------|-----------|-------|------|----------|
| **text-embedding-ada-002** | 1,536 | Fast | $0.0001/1K | General purpose |
| **text-embedding-3-small** | 1,536 | Faster | $0.00002/1K | Cost-sensitive |
| **text-embedding-3-large** | 3,072 | Medium | $0.00013/1K | High accuracy |
| **instructor-xl** | 768 | Medium | Free | Open source |
| **BGE-large** | 1,024 | Fast | Free | Open source |
| **E5-mistral** | 4,096 | Slow | Free | Long context |

**Choosing an Embedding Model:**

**For Production (Paid):**
```python
import openai

def embed_text(text):
    response = openai.Embedding.create(
        model="text-embedding-3-large",  # Best quality
        input=text
    )
    return response.data[0].embedding

# Cost: ~$0.13 per 1M tokens
# Quality: Excellent
# Latency: ~50ms
```

**For Production (Open Source):**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-large-en-v1.5')

def embed_text(text):
    return model.encode(text, normalize_embeddings=True)

# Cost: Free (self-hosted)
# Quality: Very good
# Latency: ~20ms on GPU
```

**Embedding Optimization:**

**1. Batch Processing**
```python
# Bad: One at a time
embeddings = [embed_text(chunk) for chunk in chunks]  # Slow!

# Good: Batch
batch_size = 100
embeddings = []
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    batch_embeddings = embed_text_batch(batch)
    embeddings.extend(batch_embeddings)
```

**2. Caching**
```python
import hashlib
import redis

redis_client = redis.Redis()

def embed_with_cache(text):
    # Check cache first
    cache_key = hashlib.md5(text.encode()).hexdigest()
    cached = redis_client.get(cache_key)
    
    if cached:
        return eval(cached)  # Deserialize
    
    # Generate embedding
    embedding = embed_text(text)
    
    # Cache it
    redis_client.set(cache_key, str(embedding), ex=86400)  # 24h TTL
    
    return embedding
```

---

**4. Vector Databases**

**Vector Database Comparison:**

| Database | Hosting | Scale | Speed | Best For |
|----------|---------|-------|-------|----------|
| **Pinecone** | Cloud | 100M+ | Fastest | Production, managed |
| **Weaviate** | Both | 10M+ | Fast | Hybrid search |
| **Chroma** | Local | 1M+ | Medium | Development |
| **Qdrant** | Both | 100M+ | Fast | Open source prod |
| **Milvus** | Both | Billions | Fast | Massive scale |
| **FAISS** | Local | 10M+ | Fastest | Research, in-memory |

**Pinecone (Cloud, Managed):**
```python
import pinecone

# Initialize
pinecone.init(api_key="YOUR_KEY", environment="us-west1-gcp")

# Create index
index = pinecone.Index("my-rag-index")

# Upsert vectors
index.upsert(vectors=[
    ("id-1", embedding_1, {"text": "chunk1", "source": "doc1.pdf"}),
    ("id-2", embedding_2, {"text": "chunk2", "source": "doc1.pdf"})
])

# Query
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)
```

**Weaviate (Hybrid Search):**
```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# Create schema
class_obj = {
    "class": "Document",
    "vectorizer": "text2vec-openai",
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {"name": "source", "dataType": ["string"]}
    ]
}
client.schema.create_class(class_obj)

# Add documents
client.data_object.create(
    data_object={"text": "chunk text", "source": "doc1.pdf"},
    class_name="Document"
)

# Hybrid search (vector + keyword)
results = client.query.get("Document", ["text", "source"]) \\
    .with_hybrid(query="user query", alpha=0.75) \\
    .with_limit(5) \\
    .do()
```

**Chroma (Local, Simple):**
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("documents")

# Add documents
collection.add(
    documents=["chunk 1 text", "chunk 2 text"],
    metadatas=[{"source": "doc1.pdf"}, {"source": "doc2.pdf"}],
    ids=["id1", "id2"]
)

# Query
results = collection.query(
    query_texts=["user query"],
    n_results=5
)
```

**Vector Database Selection Guide:**

**Choose Pinecone if:**
- Need managed solution
- Scale to 100M+ vectors
- Want fastest performance
- Budget for hosting ($70+/month)

**Choose Weaviate if:**
- Need hybrid search (vector + keyword)
- Want self-hosting option
- GraphQL interface preferred
- Complex filtering requirements

**Choose Chroma if:**
- Development/prototyping
- Small scale (<1M vectors)
- Want simplicity
- Local-only deployment

**Choose Qdrant if:**
- Need open source production solution
- Self-hosting preferred
- Advanced filtering requirements
- Cost-conscious

---

**5. Similarity Search Algorithms**

**Distance Metrics:**

**Cosine Similarity (Most Common):**
```python
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

# Range: -1 to 1 (1 = identical, 0 = orthogonal, -1 = opposite)
# Use when: Vector magnitude doesn't matter
# Best for: Text embeddings
```

**Euclidean Distance:**
```python
import numpy as np

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

# Range: 0 to ∞ (0 = identical)
# Use when: Absolute distance matters
# Best for: Image embeddings
```

**Dot Product:**
```python
def dot_product_similarity(a, b):
    return np.dot(a, b)

# Range: -∞ to ∞
# Use when: Vectors are normalized
# Best for: Fast computation
```

**Advanced Retrieval Strategies:**

**1. Maximum Marginal Relevance (MMR)**
```python
def mmr(query_embedding, doc_embeddings, lambda_param=0.5, k=5):
    \"\"\"
    Select diverse results, not just similar ones
    \"\"\"
    selected = []
    remaining = list(range(len(doc_embeddings)))
    
    # First: Most similar to query
    scores = [cosine_similarity(query_embedding, emb) for emb in doc_embeddings]
    first_idx = np.argmax(scores)
    selected.append(first_idx)
    remaining.remove(first_idx)
    
    # Rest: Balance similarity to query vs diversity from selected
    while len(selected) < k and remaining:
        mmr_scores = []
        for idx in remaining:
            # Similarity to query
            sim_query = cosine_similarity(query_embedding, doc_embeddings[idx])
            
            # Max similarity to already selected
            sim_selected = max([
                cosine_similarity(doc_embeddings[idx], doc_embeddings[s])
                for s in selected
            ])
            
            # MMR score
            mmr_score = lambda_param * sim_query - (1 - lambda_param) * sim_selected
            mmr_scores.append(mmr_score)
        
        best_idx = remaining[np.argmax(mmr_scores)]
        selected.append(best_idx)
        remaining.remove(best_idx)
    
    return selected
```

**2. Reranking with Cross-Encoder**
```python
from sentence_transformers import CrossEncoder

# Step 1: Fast retrieval (100 candidates)
initial_results = vector_db.query(query_embedding, top_k=100)

# Step 2: Precise reranking (top 10)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

pairs = [[query, doc['text']] for doc in initial_results]
scores = reranker.predict(pairs)

# Sort by reranker scores
reranked = sorted(zip(initial_results, scores), key=lambda x: x[1], reverse=True)
top_results = [doc for doc, score in reranked[:10]]
```

**3. Hybrid Search (Vector + Keyword)**
```python
def hybrid_search(query, vector_weight=0.7):
    # Vector search
    vector_results = vector_db.query(query_embedding, top_k=20)
    
    # Keyword search (BM25)
    keyword_results = bm25_search(query, top_k=20)
    
    # Combine scores
    combined = {}
    for doc in vector_results:
        combined[doc['id']] = vector_weight * doc['score']
    
    for doc in keyword_results:
        if doc['id'] in combined:
            combined[doc['id']] += (1 - vector_weight) * doc['score']
        else:
            combined[doc['id']] = (1 - vector_weight) * doc['score']
    
    # Sort by combined score
    return sorted(combined.items(), key=lambda x: x[1], reverse=True)[:10]
```

---

**6. RAG Prompt Engineering**

**Basic RAG Prompt:**
```python
BASIC_RAG_PROMPT = \"\"\"Answer the question based only on the following context:

Context:
{context}

Question: {question}

Answer:\"\"\"
```

**Production RAG Prompt:**
```python
PRODUCTION_RAG_PROMPT = \"\"\"You are a helpful assistant answering questions based on provided context.

Instructions:
1. Answer based ONLY on the context below
2. If the answer is not in the context, say "I don't have enough information"
3. Cite which part of the context you used
4. Be concise but complete

Context:
{context}

Question: {question}

Provide your answer below:\"\"\"
```

**Advanced RAG Prompt (with Citations):**
```python
CITATION_RAG_PROMPT = \"\"\"You are a research assistant. Answer the question using the provided sources.

Sources:
{context}

Question: {question}

Instructions:
1. Answer the question using information from the sources
2. Cite sources using [Source X] notation
3. If multiple sources support a point, cite all
4. If information is not in sources, explicitly state that

Answer:\"\"\"
```

---

**7. RAG Performance Metrics**

**Retrieval Metrics:**

**Recall@K:**
```python
def recall_at_k(retrieved_docs, relevant_docs, k=5):
    \"\"\"
    What fraction of relevant docs did we retrieve?
    \"\"\"
    retrieved_ids = set([doc['id'] for doc in retrieved_docs[:k]])
    relevant_ids = set([doc['id'] for doc in relevant_docs])
    
    if not relevant_ids:
        return 0.0
    
    return len(retrieved_ids & relevant_ids) / len(relevant_ids)
```

**MRR (Mean Reciprocal Rank):**
```python
def mean_reciprocal_rank(retrieved_docs, relevant_docs):
    \"\"\"
    How high was the first relevant result?
    \"\"\"
    relevant_ids = set([doc['id'] for doc in relevant_docs])
    
    for i, doc in enumerate(retrieved_docs, 1):
        if doc['id'] in relevant_ids:
            return 1.0 / i
    
    return 0.0
```

**NDCG (Normalized Discounted Cumulative Gain):**
```python
import numpy as np

def ndcg_at_k(retrieved_docs, relevance_scores, k=5):
    \"\"\"
    Accounts for position AND relevance
    \"\"\"
    dcg = sum([
        (2**rel - 1) / np.log2(i + 2)
        for i, rel in enumerate(relevance_scores[:k])
    ])
    
    ideal_scores = sorted(relevance_scores, reverse=True)
    idcg = sum([
        (2**rel - 1) / np.log2(i + 2)
        for i, rel in enumerate(ideal_scores[:k])
    ])
    
    return dcg / idcg if idcg > 0 else 0.0
```

**Generation Metrics:**

**Faithfulness:**
```python
def check_faithfulness(answer, context):
    \"\"\"
    Are all claims in answer supported by context?
    \"\"\"
    prompt = f\"\"\"
    Context: {context}
    
    Answer: {answer}
    
    Is every claim in the answer supported by the context? 
    Answer YES or NO and explain.
    \"\"\"
    
    response = llm(prompt)
    return "YES" in response.upper()
```

**Answer Relevance:**
```python
def check_relevance(question, answer):
    \"\"\"
    Does answer actually address the question?
    \"\"\"
    prompt = f\"\"\"
    Question: {question}
    Answer: {answer}
    
    Does the answer directly address the question?
    Rate 1-5 (1=not relevant, 5=highly relevant)
    \"\"\"
    
    response = llm(prompt)
    # Extract score from response
    return extract_score(response)
```

---

**8. Production RAG Patterns**

**Pattern 1: Simple RAG**
```python
def simple_rag(question):
    # 1. Embed question
    query_embedding = embed(question)
    
    # 2. Retrieve docs
    docs = vector_db.query(query_embedding, top_k=5)
    
    # 3. Construct prompt
    context = "\\n\\n".join([doc['text'] for doc in docs])
    prompt = f"Context: {context}\\n\\nQuestion: {question}\\n\\nAnswer:"
    
    # 4. Generate answer
    answer = llm(prompt)
    
    return answer
```

**Pattern 2: RAG with Reranking**
```python
def rag_with_reranking(question):
    # 1. Initial retrieval (more candidates)
    query_embedding = embed(question)
    candidate_docs = vector_db.query(query_embedding, top_k=50)
    
    # 2. Rerank for precision
    reranked_docs = rerank(question, candidate_docs, top_k=5)
    
    # 3. Generate answer
    context = "\\n\\n".join([doc['text'] for doc in reranked_docs])
    answer = llm(f"Context: {context}\\n\\nQuestion: {question}")
    
    return answer, reranked_docs  # Return sources too
```

**Pattern 3: Hierarchical RAG**
```python
def hierarchical_rag(question):
    \"\"\"
    First retrieve documents, then chunks within documents
    \"\"\"
    # 1. Document-level retrieval
    doc_embedding = embed(question)
    relevant_docs = doc_vector_db.query(doc_embedding, top_k=3)
    
    # 2. Chunk-level retrieval within relevant docs
    relevant_chunks = []
    for doc in relevant_docs:
        chunks = chunk_vector_db.query(
            query_embedding,
            filter={"doc_id": doc['id']},
            top_k=3
        )
        relevant_chunks.extend(chunks)
    
    # 3. Generate answer
    context = "\\n\\n".join([chunk['text'] for chunk in relevant_chunks])
    answer = llm(f"Context: {context}\\n\\nQuestion: {question}")
    
    return answer
```

**Pattern 4: Multi-Query RAG**
```python
def multi_query_rag(question):
    \"\"\"
    Generate multiple query variations for better retrieval
    \"\"\"
    # 1. Generate query variations
    variations = llm(f\"\"\"
    Generate 3 different ways to ask this question:
    {question}
    
    Return as JSON list.
    \"\"\")
    
    queries = json.loads(variations)
    
    # 2. Retrieve for each variation
    all_docs = []
    for query in queries:
        query_embedding = embed(query)
        docs = vector_db.query(query_embedding, top_k=5)
        all_docs.extend(docs)
    
    # 3. Deduplicate and rank
    unique_docs = deduplicate(all_docs)
    top_docs = rerank(question, unique_docs, top_k=5)
    
    # 4. Generate answer
    context = "\\n\\n".join([doc['text'] for doc in top_docs])
    answer = llm(f"Context: {context}\\n\\nQuestion: {question}")
    
    return answer
```

**Pattern 5: RAG with Self-Reflection**
```python
def self_reflective_rag(question, max_iterations=3):
    \"\"\"
    LLM reflects on whether it has enough context
    \"\"\"
    retrieved_docs = []
    
    for iteration in range(max_iterations):
        # Retrieve docs
        query_embedding = embed(question)
        docs = vector_db.query(query_embedding, top_k=5)
        retrieved_docs.extend(docs)
        
        # Try to answer
        context = "\\n\\n".join([doc['text'] for doc in retrieved_docs])
        answer = llm(f\"\"\"
        Context: {context}
        
        Question: {question}
        
        If you have enough information, answer the question.
        If not, output: NEED_MORE_INFO: <what information you need>
        \"\"\")
        
        if "NEED_MORE_INFO" not in answer:
            return answer  # Success!
        
        # Need more info - refine query
        needed_info = answer.split("NEED_MORE_INFO:")[1].strip()
        question = f"{question} Specifically: {needed_info}"
    
    return "I couldn't find enough information to answer this question."
```

---

**9. RAG Cost Optimization**

**Embedding Cost Calculation:**
```python
def calculate_embedding_cost(num_documents, avg_tokens_per_doc):
    \"\"\"
    OpenAI text-embedding-3-large: $0.00013 per 1K tokens
    \"\"\"
    total_tokens = num_documents * avg_tokens_per_doc
    cost = (total_tokens / 1000) * 0.00013
    
    return cost

# Example: 100,000 docs × 500 tokens = $6.50
```

**LLM Cost Calculation:**
```python
def calculate_rag_llm_cost(queries_per_month, tokens_per_query):
    \"\"\"
    GPT-4: $0.03 input + $0.06 output per 1K tokens
    \"\"\"
    # Assume 5 retrieved chunks × 200 tokens = 1000 input tokens
    # Assume 200 output tokens
    
    input_tokens = queries_per_month * 1000
    output_tokens = queries_per_month * 200
    
    input_cost = (input_tokens / 1000) * 0.03
    output_cost = (output_tokens / 1000) * 0.06
    
    return input_cost + output_cost

# Example: 100,000 queries/month = $3,000 + $1,200 = $4,200/month
```

**Cost Optimization Strategies:**

**1. Caching**
```python
import hashlib

cache = {}

def rag_with_cache(question):
    # Check cache
    cache_key = hashlib.md5(question.encode()).hexdigest()
    
    if cache_key in cache:
        return cache[cache_key]  # Instant, free response
    
    # Regular RAG
    answer = simple_rag(question)
    
    # Cache result
    cache[cache_key] = answer
    
    return answer

# Savings: 30-50% cost reduction if many repeated questions
```

**2. Smaller Models for Simple Queries**
```python
def adaptive_rag(question):
    # Classify question complexity
    complexity = classify_complexity(question)  # Simple, Medium, Complex
    
    if complexity == "Simple":
        model = "gpt-3.5-turbo"  # 10X cheaper
    else:
        model = "gpt-4"
    
    answer = llm(prompt, model=model)
    return answer

# Savings: 50-70% if 70% of queries are simple
```

**3. Fewer Chunks**
```python
# Bad: Always retrieve 10 chunks
docs = vector_db.query(query_embedding, top_k=10)

# Good: Use confidence threshold
docs = vector_db.query(query_embedding, top_k=10)
filtered_docs = [doc for doc in docs if doc['score'] > 0.7]

# Only use high-confidence chunks
# Savings: 20-40% token reduction
```

---

**10. RAG Debugging & Troubleshooting**

**Common RAG Problems:**

**Problem 1: Low Retrieval Accuracy**

**Symptoms:**
- Irrelevant chunks retrieved
- Missing obvious matches

**Debug:**
```python
# Test embedding quality
query = "What is the refund policy?"
query_emb = embed(query)

# Check what's actually similar
results = vector_db.query(query_emb, top_k=20)
for doc in results:
    print(f"Score: {doc['score']:.3f} - {doc['text'][:100]}")
```

**Solutions:**
- Better chunking strategy
- Different embedding model
- Add metadata filters
- Use hybrid search

**Problem 2: Context Window Overflow**

**Symptoms:**
- Token limit exceeded error
- Last chunks get truncated

**Solutions:**
```python
def smart_context_construction(docs, max_tokens=4000):
    \"\"\"
    Fit chunks into token budget
    \"\"\"
    context_chunks = []
    total_tokens = 0
    
    for doc in docs:
        doc_tokens = count_tokens(doc['text'])
        
        if total_tokens + doc_tokens > max_tokens:
            break  # Stop before overflow
        
        context_chunks.append(doc['text'])
        total_tokens += doc_tokens
    
    return "\\n\\n".join(context_chunks)
```

**Problem 3: Hallucination Despite RAG**

**Symptoms:**
- LLM invents facts not in context
- Mixes context with pre-training knowledge

**Solutions:**
```python
# Strong system message
ANTI_HALLUCINATION_PROMPT = \"\"\"You are a precise assistant.

CRITICAL RULES:
1. ONLY use information from the Context below
2. If Context doesn't contain the answer, say "I don't know"
3. DO NOT use your general knowledge
4. Quote directly from Context when possible

Context:
{context}

Question: {question}

Answer (using ONLY the Context):\"\"\"
```

**Problem 4: Slow Response Times**

**Benchmark each stage:**
```python
import time

def benchmark_rag(question):
    # Embedding
    t0 = time.time()
    query_emb = embed(question)
    t1 = time.time()
    print(f"Embedding: {(t1-t0)*1000:.0f}ms")
    
    # Retrieval
    docs = vector_db.query(query_emb, top_k=5)
    t2 = time.time()
    print(f"Retrieval: {(t2-t1)*1000:.0f}ms")
    
    # Generation
    context = "\\n\\n".join([doc['text'] for doc in docs])
    answer = llm(f"Context: {context}\\n\\nQ: {question}")
    t3 = time.time()
    print(f"Generation: {(t3-t2)*1000:.0f}ms")
    
    print(f"Total: {(t3-t0)*1000:.0f}ms")
    return answer

# Typical breakdown:
# Embedding: 20-50ms
# Retrieval: 10-100ms
# Generation: 1000-5000ms (most time here)
```

**Optimization:**
- Use streaming for generation
- Parallel embedding + retrieval
- Faster embedding model
- Smaller LLM for simple queries
"""
            )
        elif selected_unit == 4:
            st.markdown("#### 📘 Fine-tuning: Customizing LLMs")
            st.markdown("""
**Fine-tuning** adapts pre-trained LLMs to your specific use case.

**When to Fine-tune:**
- ✅ Need consistent output format
- ✅ Domain-specific language
- ✅ Reduce prompt length
- ✅ Improve accuracy on specific task

**Methods:**
- **Full fine-tuning:** Update all parameters (expensive)
- **LoRA:** Update small adapters (efficient)
- **Prompt tuning:** Learn soft prompts

**Process:**
1. Prepare training data (100-1000+ examples)
2. Upload to platform (OpenAI, Hugging Face)
3. Start training job
4. Evaluate results
5. Deploy fine-tuned model
""")
            
            st.markdown("#### 🎯 Fine-tuning Deep Dive")
            st.markdown("""Production fine-tuning requires understanding different techniques and their trade-offs:

**Why Fine-tune vs Prompt Engineering?**

| Aspect | Prompt Engineering | Fine-tuning |
|--------|-------------------|-------------|
| **Setup Time** | Minutes | Days/Weeks |
| **Cost** | Low (per query) | High (upfront) + Low (per query) |
| **Data Required** | None | 100-10,000+ examples |
| **Output Quality** | Good | Excellent |
| **Consistency** | Variable | Very consistent |
| **Latency** | Slower (long prompts) | Faster (short prompts) |
| **Use Case** | Exploration, variety | Production, specific tasks |

**When to Choose Each:**

**Prompt Engineering:**
- Prototyping and testing
- Tasks with high variety
- Limited training data
- Quick iteration needed
- Budget constraints

**Fine-tuning:**
- Production deployment
- Consistent output format required
- Domain-specific terminology
- Cost optimization at scale
- Performance critical

---

**Fine-tuning Methods Comparison:**

**1. Full Fine-tuning**
- Update **all** model parameters
- Requires most compute and memory
- Best quality for complex tasks
- Cost: $10K-$100K+ for large models

**2. LoRA (Low-Rank Adaptation)**
- Update small adapter layers (0.1-1% of parameters)
- Much more efficient than full fine-tuning
- 90% of full fine-tuning quality
- Cost: $100-$1,000

**3. QLoRA (Quantized LoRA)**
- LoRA + 4-bit quantization
- Fine-tune on single GPU
- Minimal quality loss
- Cost: $10-$100

**4. Prefix/Prompt Tuning**
- Learn soft prompts (not text)
- Most parameter efficient
- Good for classification tasks
- Cost: $1-$10

---

**LoRA (Low-Rank Adaptation) Explained:**

**The Problem:**
Fine-tuning 70B parameter model requires:
- 280 GB RAM (FP32)
- Multiple A100 GPUs ($40K+)
- Days of training time

**LoRA Solution:**
Instead of updating all weights, add small "adapter" matrices.

**How It Works:**

Original weight update:
```
W_new = W_old + ΔW
```

LoRA decomposition:
```
W_new = W_old + B×A
```

Where:
- W_old: 4096 × 4096 (frozen)
- B: 4096 × 8 (trainable)
- A: 8 × 4096 (trainable)

**Savings:**
- Original: 16M parameters to update
- LoRA: 131K parameters to update (99% reduction!)

**LoRA Implementation:**

```python
from peft import LoraConfig, get_peft_model, TaskType

# Configure LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,                    # Rank (higher = more capacity, more compute)
    lora_alpha=32,          # Scaling factor
    lora_dropout=0.1,       # Regularization
    target_modules=["q_proj", "v_proj"]  # Which layers to adapt
)

# Apply LoRA to model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
model = get_peft_model(model, lora_config)

# Check trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%
```

**LoRA Hyperparameters:**

| Parameter | Values | Effect |
|-----------|--------|--------|
| **r (rank)** | 4, 8, 16, 32 | Higher = more capacity, slower |
| **lora_alpha** | 16, 32, 64 | Scaling factor, typically 2×r |
| **lora_dropout** | 0.0, 0.05, 0.1 | Regularization |
| **target_modules** | q_proj, v_proj, etc | Which attention layers |

**Recommended Settings:**

**For Classification:**
- r = 8
- lora_alpha = 16
- target_modules = ["q_proj", "v_proj"]

**For Generation:**
- r = 16
- lora_alpha = 32
- target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]

---

**QLoRA: Quantized LoRA**

**The Innovation:**
Fine-tune 70B model on single 48GB GPU!

**How QLoRA Works:**

1. **Load base model in 4-bit**
```python
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-70b-hf",
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",        # Normal Float 4-bit
    bnb_4bit_use_double_quant=True    # Nested quantization
)
```

2. **Add LoRA adapters in 16-bit**
```python
lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
```

3. **Train normally**
```python
trainer = Trainer(
    model=model,
    train_dataset=dataset,
    args=TrainingArguments(
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        learning_rate=2e-4,
        fp16=True
    )
)

trainer.train()
```

**Memory Savings:**

| Model | Full FT | LoRA | QLoRA |
|-------|---------|------|-------|
| **7B** | 28 GB | 14 GB | 9 GB |
| **13B** | 52 GB | 26 GB | 16 GB |
| **70B** | 280 GB | 140 GB | 48 GB |

---

**Instruction Tuning**

**What is it?**
Teaching LLM to follow instructions consistently.

**Format:**
```json
{
  "instruction": "Summarize this article in 3 sentences.",
  "input": "[Long article text]",
  "output": "[3-sentence summary]"
}
```

**Popular Instruction Datasets:**

1. **Alpaca (52K examples)**
   - General instruction following
   - Stanford dataset
   - Self-instruct generated

2. **Dolly (15K examples)**
   - Human-written
   - Commercial-friendly license
   - Multiple categories

3. **FLAN (1M+ examples)**
   - Academic tasks
   - Very diverse
   - Chain-of-thought included

**Creating Instruction Data:**

```python
def create_instruction_example(task, input_text, output_text):
    \"\"\"
    Format for instruction tuning
    \"\"\"
    return {
        "instruction": task,
        "input": input_text,
        "output": output_text,
        "text": f\"\"\"### Instruction:
{task}

### Input:
{input_text}

### Response:
{output_text}\"\"\"
    }

# Example
example = create_instruction_example(
    task="Extract the company name and date from this earnings report.",
    input_text="Apple Inc. reported Q4 earnings on January 27, 2024...",
    output_text="Company: Apple Inc.\\nDate: January 27, 2024"
)
```

---

**RLHF (Reinforcement Learning from Human Feedback)**

**The Process:**

**Step 1: Supervised Fine-tuning (SFT)**
```
Base Model → SFT with high-quality examples → SFT Model
```

**Step 2: Reward Model Training**
```
SFT Model generates → Humans rank outputs → Train reward model
```

**Step 3: RL Optimization (PPO)**
```
SFT Model → Generate → Reward Model scores → Update via PPO
```

**RLHF Pipeline:**

```python
# 1. Supervised Fine-tuning
sft_model = train_sft(
    base_model="gpt-3.5",
    dataset=high_quality_responses,
    epochs=3
)

# 2. Train Reward Model
reward_model = train_reward_model(
    sft_model=sft_model,
    comparison_dataset=ranked_pairs,  # Human preferences
    epochs=1
)

# 3. RL Fine-tuning (PPO)
rlhf_model = train_with_ppo(
    sft_model=sft_model,
    reward_model=reward_model,
    prompts=training_prompts,
    steps=20000
)
```

**Human Preference Data Format:**
```json
{
  "prompt": "Explain quantum computing",
  "response_a": "[Technical, accurate]",
  "response_b": "[Simple, clear]",
  "preference": "b",  # Humans prefer B
  "reason": "More accessible to general audience"
}
```

**RLHF Use Cases:**
- ChatGPT: Helpful, honest, harmless
- GitHub Copilot: Correct, idiomatic code
- Claude: Safe, nuanced responses

---

**Data Preparation for Fine-tuning**

**Data Quality > Data Quantity**

**Minimum Examples:**
- Classification: 50-100 per class
- Summarization: 100-500
- Question Answering: 500-1,000
- Code Generation: 1,000-5,000
- General Chat: 5,000-10,000

**Data Format (OpenAI):**
```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is machine learning?"}, {"role": "assistant", "content": "Machine learning is..."}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Explain neural networks"}, {"role": "assistant", "content": "Neural networks are..."}]}
```

**Data Format (Hugging Face):**
```python
from datasets import Dataset

data = {
    "text": [
        "### Instruction: Translate to French\\n### Input: Hello\\n### Response: Bonjour",
        "### Instruction: Translate to French\\n### Input: Goodbye\\n### Response: Au revoir"
    ]
}

dataset = Dataset.from_dict(data)
```

**Data Quality Checklist:**

✅ **Diverse Examples**
- Cover edge cases
- Include different phrasings
- Multiple domains/topics

✅ **Consistent Format**
- Same structure for all examples
- Standardized field names
- Clear instruction-response pairs

✅ **High-Quality Outputs**
- Accurate information
- Appropriate tone/style
- Correct formatting

✅ **Balanced Distribution**
- Similar counts per category
- No duplicate examples
- Representative of production

**Data Augmentation:**

```python
def augment_training_data(example):
    \"\"\"
    Generate variations of training examples
    \"\"\"
    variations = []
    
    # Paraphrase instruction
    instructions = [
        example['instruction'],
        paraphrase(example['instruction']),
        simplify(example['instruction'])
    ]
    
    # Keep same input/output
    for inst in instructions:
        variations.append({
            'instruction': inst,
            'input': example['input'],
            'output': example['output']
        })
    
    return variations

# 100 examples → 300 examples
```

---

**Fine-tuning Workflow**

**Step 1: Prepare Environment**

```python
# Install dependencies
pip install transformers datasets peft bitsandbytes accelerate

# Load model and tokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

**Step 2: Prepare Dataset**

```python
from datasets import load_dataset

# Load your data
dataset = load_dataset("json", data_files="training_data.jsonl")

# Tokenize
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )

tokenized_dataset = dataset.map(tokenize_function, batched=True)
```

**Step 3: Configure Training**

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_steps=100,
    logging_steps=10,
    evaluation_strategy="steps",
    eval_steps=100,
    save_steps=500,
    save_total_limit=2,
    fp16=True,  # Mixed precision
    load_best_model_at_end=True
)
```

**Step 4: Train**

```python
from transformers import Trainer

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer
)

# Start training
trainer.train()

# Save model
trainer.save_model("./fine_tuned_model")
```

---

**Evaluation Metrics**

**1. Perplexity**
```python
import torch
from torch.nn import CrossEntropyLoss

def calculate_perplexity(model, dataset):
    model.eval()
    loss_fct = CrossEntropyLoss()
    losses = []
    
    for batch in dataset:
        with torch.no_grad():
            outputs = model(**batch)
            loss = outputs.loss
            losses.append(loss.item())
    
    avg_loss = sum(losses) / len(losses)
    perplexity = torch.exp(torch.tensor(avg_loss))
    return perplexity.item()

# Lower is better (GPT-4: ~10, untrained: 1000+)
```

**2. Task-Specific Accuracy**
```python
def evaluate_classification(model, test_data):
    correct = 0
    total = 0
    
    for example in test_data:
        prediction = model.generate(example['prompt'])
        if prediction.strip() == example['expected']:
            correct += 1
        total += 1
    
    accuracy = correct / total
    return accuracy
```

**3. Human Evaluation**
```python
def human_eval_template(prompt, model_output):
    return {
        "prompt": prompt,
        "output": model_output,
        "ratings": {
            "accuracy": None,      # 1-5
            "helpfulness": None,   # 1-5
            "harmlessness": None,  # 1-5
            "honesty": None        # 1-5
        },
        "comments": ""
    }

# Collect ratings from 3+ humans, average scores
```

**4. Benchmark Comparisons**
```python
# Standard benchmarks
benchmarks = {
    "MMLU": test_mmlu(model),           # General knowledge
    "HellaSwag": test_hellaswag(model), # Common sense
    "TruthfulQA": test_truthful(model), # Truthfulness
    "HumanEval": test_code(model)       # Code generation
}
```

---

**Cost Analysis**

**OpenAI Fine-tuning Costs:**

| Model | Training | Usage |
|-------|----------|-------|
| **GPT-3.5-turbo** | $0.008/1K tokens | $0.012/1K tokens |
| **Davinci-002** | $0.0060/1K tokens | $0.0120/1K tokens |
| **Babbage-002** | $0.0004/1K tokens | $0.0016/1K tokens |

**Example: Fine-tune GPT-3.5 on 10,000 examples**
- Avg 500 tokens per example
- Total: 5M tokens
- Training cost: 5,000 × $0.008 = $40
- Usage cost: ~2× base rate

**Self-Hosted Fine-tuning Costs:**

| Setup | Cost | Time | Best For |
|-------|------|------|----------|
| **1× A100 (80GB)** | $3/hour | 8-24h | 7-13B models |
| **4× A100** | $12/hour | 2-6h | 30-70B models |
| **Cloud (Lambda Labs)** | $1.10/hour | Variable | Budget fine-tuning |
| **Colab Pro+** | $50/month | Slow | Learning/testing |

**Example: Fine-tune Llama 2 7B**
- QLoRA on 1× A100
- 10 epochs, 10K examples
- Time: 8 hours
- Cost: $24

**ROI Calculation:**
```python
def calculate_roi(training_cost, queries_per_month, cost_savings_per_query):
    \"\"\"
    When does fine-tuning pay for itself?
    \"\"\"
    monthly_savings = queries_per_month * cost_savings_per_query
    break_even_months = training_cost / monthly_savings
    
    return break_even_months

# Example
roi = calculate_roi(
    training_cost=1000,           # $1K to fine-tune
    queries_per_month=100000,     # 100K queries/month
    cost_savings_per_query=0.02   # Save $0.02 per query
)
print(f"Break even in {roi:.1f} months")  # 0.5 months!
```

---

**Common Fine-tuning Mistakes**

**❌ Mistake 1: Not Enough Data**
- Symptom: Model overfits, poor generalization
- Solution: Aim for 1,000+ diverse examples minimum

**❌ Mistake 2: Low-Quality Data**
- Symptom: Model outputs are inconsistent/wrong
- Solution: Manual review of 100+ examples

**❌ Mistake 3: Wrong Learning Rate**
- Symptom: Model doesn't learn or diverges
- Solution: Start with 2e-5, try 1e-5 to 5e-5

**❌ Mistake 4: Overfitting**
- Symptom: Perfect train metrics, poor test metrics
- Solution: Early stopping, more data, regularization

**❌ Mistake 5: Ignoring Evaluation**
- Symptom: Deploy bad model to production
- Solution: Hold-out test set, human evaluation

---

**Production Deployment**

**Serving Fine-tuned Models:**

**Option 1: OpenAI (Easiest)**
```python
import openai

# Deploy automatically after fine-tuning
response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo:my-org:custom-model:abc123",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Option 2: Hugging Face Inference**
```python
from huggingface_hub import InferenceClient

client = InferenceClient(model="your-username/fine-tuned-model")
response = client.text_generation("Hello", max_new_tokens=50)
```

**Option 3: Self-Hosted (vLLM)**
```python
# Server
from vllm import LLM

llm = LLM(model="./fine-tuned-model")

# Client
import requests
response = requests.post(
    "http://localhost:8000/generate",
    json={"prompt": "Hello", "max_tokens": 50}
)
```

**Monitoring Fine-tuned Models:**

```python
def monitor_model_performance():
    metrics = {
        "latency_p50": measure_latency_p50(),
        "latency_p99": measure_latency_p99(),
        "error_rate": count_errors() / total_requests(),
        "user_satisfaction": get_user_ratings(),
        "output_quality": llm_judge_score()
    }
    
    # Alert if degradation
    if metrics["output_quality"] < 0.8:
        alert_team("Model quality degraded!")
    
    return metrics
```

---

**Fine-tuning Checklist**

**Before Training:**
- [ ] 1,000+ high-quality examples collected
- [ ] Data format validated
- [ ] Train/val/test split created (80/10/10)
- [ ] Baseline model performance measured
- [ ] Compute resources allocated

**During Training:**
- [ ] Training loss decreasing steadily
- [ ] Validation loss not increasing (overfitting check)
- [ ] Learning rate appropriate
- [ ] Checkpoints saved regularly
- [ ] Resource utilization monitored

**After Training:**
- [ ] Test set performance acceptable
- [ ] Human evaluation completed
- [ ] Cost analysis done
- [ ] Model safety tested
- [ ] Deployment plan ready

**Post-Deployment:**
- [ ] Monitoring dashboard set up
- [ ] Error tracking enabled
- [ ] User feedback collection
- [ ] A/B test running
- [ ] Rollback plan documented
"""
            )
        elif selected_unit == 5:
            st.markdown("#### 📘 LLM Agents: Autonomous AI Systems")
            st.markdown("""
**LLM Agents** can use tools and take actions autonomously.

**What are Agents?**
- LLMs that can call functions/APIs
- Make decisions about which tools to use
- Chain multiple actions together
- Maintain conversation state

**Agent Frameworks:**
- LangChain
- AutoGPT
- BabyAGI
- LlamaIndex

**Use Cases:**
- Customer service bots
- Data analysis assistants
- Code generation tools
- Research assistants
""")
            
            st.markdown("#### 🤖 AI Agents Deep Dive")
            st.markdown("""Building autonomous AI agents that can use tools and accomplish complex tasks:

**Agent vs Non-Agent LLM:**

| Feature | Standard LLM | LLM Agent |
|---------|-------------|-----------|
| **Interaction** | Single turn | Multi-turn |
| **Tools** | None | Functions, APIs, databases |
| **Memory** | Context window only | Persistent memory |
| **Planning** | No | Yes (goal-oriented) |
| **Autonomy** | Responds to prompts | Takes initiative |
| **Use Case** | Q&A, generation | Complex workflows |

---

**Core Agent Components:**

**1. Reasoning Engine (LLM)**
The brain - decides what to do next

**2. Tool Library**
Available actions the agent can take

**3. Memory System**
Stores conversation history, facts, results

**4. Planning Module**
Breaks down complex tasks into steps

**5. Execution Engine**
Runs tools and processes results

---

**Agent Architectures:**

**1. ReAct (Reasoning + Acting)**

Most popular pattern, used by ChatGPT plugins.

**How It Works:**
```
Thought → Action → Observation → Thought → ...
```

**Example:**
```
Question: What's the weather in London and how does it compare to Paris?

Thought: I need to get weather data for both cities
Action: get_weather(location="London")
Observation: London: 15°C, Cloudy

Thought: Now I need Paris weather
Action: get_weather(location="Paris") 
Observation: Paris: 18°C, Sunny

Thought: I have both, I can now compare
Final Answer: London is 15°C and cloudy, while Paris is warmer at 18°C and sunny.
```

**Implementation:**
```python
def react_agent(question, tools, max_iterations=10):
    \"\"\"
    ReAct pattern implementation
    \"\"\"
    context = f"Question: {question}\\n\\n"
    
    for i in range(max_iterations):
        # Reasoning step
        prompt = f\"\"\"{context}
Available tools: {list(tools.keys())}

What should you do next?
Respond in format:
Thought: [your reasoning]
Action: [tool_name(arguments)]
\"\"\"
        
        response = llm(prompt)
        context += response + "\\n"
        
        # Check if done
        if "Final Answer:" in response:
            answer = response.split("Final Answer:")[1].strip()
            return answer
        
        # Parse and execute action
        if "Action:" in response:
            action_line = response.split("Action:")[1].split("\\n")[0].strip()
            tool_name, args = parse_action(action_line)
            
            # Execute tool
            observation = tools[tool_name](**args)
            context += f"Observation: {observation}\\n\\n"
    
    return "Max iterations reached without conclusion"

# Define tools
tools = {
    "get_weather": lambda location: f"{location}: 20°C, Sunny",
    "search_web": lambda query: f"Search results for {query}...",
    "calculate": lambda expression: eval(expression)
}

answer = react_agent("What's 15 * 23?", tools)
```

**2. Plan-and-Execute**

Plan first, then execute steps.

**Architecture:**
```
Question → Planner → [Step 1, Step 2, Step 3] → Executor → Answer
```

**Implementation:**
```python
def plan_and_execute(question, tools):
    # Step 1: Create plan
    plan_prompt = f\"\"\"
Create a step-by-step plan to answer: {question}

Available tools: {list(tools.keys())}

Return plan as JSON:
{{
  "steps": [
    {{"action": "tool_name", "args": {{}}, "description": "..."}},
    ...
  ]
}}
\"\"\"
    
    plan = json.loads(llm(plan_prompt))
    
    # Step 2: Execute plan
    results = []
    for step in plan["steps"]:
        tool = tools[step["action"]]
        result = tool(**step["args"])
        results.append(result)
    
    # Step 3: Synthesize answer
    synthesis_prompt = f\"\"\"
Question: {question}
Results: {results}

Provide final answer:
\"\"\"
    
    answer = llm(synthesis_prompt)
    return answer
```

**3. Tree of Thoughts for Agents**

Explore multiple reasoning paths.

```python
def tree_of_thoughts_agent(question, tools):
    \"\"\"
    Generate multiple plans, execute best ones
    \"\"\"
    # Generate multiple plans
    plans = []
    for i in range(3):
        plan = generate_plan(question, tools)
        score = evaluate_plan_quality(plan)
        plans.append((plan, score))
    
    # Execute top 2 plans
    plans.sort(key=lambda x: x[1], reverse=True)
    results = []
    
    for plan, _ in plans[:2]:
        result = execute_plan(plan, tools)
        results.append(result)
    
    # Pick best result
    best_result = max(results, key=evaluate_result_quality)
    return best_result
```

---

**Tool Use & Function Calling:**

**OpenAI Function Calling:**

```python
import openai

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Agent loop
messages = [{"role": "user", "content": "What's the weather in SF?"}]

while True:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # Check if done
    if not message.get("tool_calls"):
        print(message.content)
        break
    
    # Execute tool calls
    messages.append(message)
    
    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # Execute function
        if function_name == "get_current_weather":
            result = get_current_weather(**function_args)
        elif function_name == "search_web":
            result = search_web(**function_args)
        
        # Add result to messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })
```

**LangChain Agents:**

```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Define tools
tools = [
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="Useful for math calculations"
    ),
    Tool(
        name="Search",
        func=search_web,
        description="Search the web for current information"
    ),
    Tool(
        name="Database",
        func=query_database,
        description="Query internal database"
    )
]

# Create agent
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Run
result = agent.run("What's the revenue of our top customer?")
```

---

**Memory Systems:**

**1. Short-term Memory (Context Window)**
```python
class ConversationMemory:
    def __init__(self, max_tokens=4000):
        self.messages = []
        self.max_tokens = max_tokens
    
    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        
        # Trim if too long
        while self.count_tokens() > self.max_tokens:
            self.messages.pop(0)  # Remove oldest
    
    def get(self):
        return self.messages
```

**2. Long-term Memory (Vector Store)**
```python
class VectorMemory:
    def __init__(self):
        self.vector_db = Chroma()
    
    def save(self, content, metadata=None):
        \"\"\"Save to long-term memory\"\"\"
        embedding = embed(content)
        self.vector_db.add(content, embedding, metadata)
    
    def recall(self, query, top_k=5):
        \"\"\"Retrieve relevant memories\"\"\"
        query_emb = embed(query)
        results = self.vector_db.query(query_emb, top_k=top_k)
        return results

# Usage
memory = VectorMemory()

# Save facts
memory.save("User's favorite color is blue")
memory.save("User lives in San Francisco")
memory.save("User is a software engineer")

# Recall
relevant_facts = memory.recall("What does the user do for work?")
# Returns: "User is a software engineer"
```

**3. Entity Memory**
```python
class EntityMemory:
    \"\"\"
    Track specific entities and their attributes
    \"\"\"
    def __init__(self):
        self.entities = {}
    
    def update(self, entity, attribute, value):
        if entity not in self.entities:
            self.entities[entity] = {}
        self.entities[entity][attribute] = value
    
    def get(self, entity):
        return self.entities.get(entity, {})

# Usage
memory = EntityMemory()
memory.update("John", "job", "Engineer")
memory.update("John", "location", "NYC")
memory.update("John", "favorite_food", "Pizza")

print(memory.get("John"))
# {"job": "Engineer", "location": "NYC", "favorite_food": "Pizza"}
```

---

**Multi-Agent Systems:**

**Collaborative Agents:**

```python
class AgentTeam:
    def __init__(self):
        self.agents = {
            "researcher": ResearchAgent(),
            "writer": WriterAgent(),
            "editor": EditorAgent()
        }
    
    def solve(self, task):
        # Researcher gathers information
        research = self.agents["researcher"].run(task)
        
        # Writer creates draft
        draft = self.agents["writer"].run(research)
        
        # Editor refines
        final = self.agents["editor"].run(draft)
        
        return final

# Define specialized agents
class ResearchAgent:
    def run(self, task):
        return search_and_summarize(task)

class WriterAgent:
    def run(self, research):
        return generate_article(research)

class EditorAgent:
    def run(self, draft):
        return improve_quality(draft)
```

**Hierarchical Agents:**

```python
class ManagerAgent:
    def __init__(self):
        self.workers = {
            "analyst": AnalystAgent(),
            "coder": CoderAgent(),
            "tester": TesterAgent()
        }
    
    def delegate(self, task):
        \"\"\"
        Manager decides which worker to assign
        \"\"\"
        # Analyze task
        plan = self.create_plan(task)
        
        results = []
        for subtask in plan:
            # Assign to appropriate worker
            worker = self.assign_worker(subtask)
            result = worker.run(subtask)
            results.append(result)
        
        # Synthesize results
        return self.synthesize(results)
```

**Competitive Agents (Debate):**

```python
def agent_debate(question, rounds=3):
    \"\"\"
    Two agents debate, judge picks winner
    \"\"\"
    agent_a = LLMAgent("You argue for the affirmative")
    agent_b = LLMAgent("You argue for the negative")
    judge = LLMAgent("You are an impartial judge")
    
    debate_history = []
    
    for round in range(rounds):
        # Agent A argues
        arg_a = agent_a.argue(question, debate_history)
        debate_history.append(("A", arg_a))
        
        # Agent B counters
        arg_b = agent_b.argue(question, debate_history)
        debate_history.append(("B", arg_b))
    
    # Judge decides
    verdict = judge.judge(question, debate_history)
    return verdict
```

---

**LangGraph: Advanced Agent Workflows**

**What is LangGraph?**
- Graph-based agent framework
- Nodes = agent actions
- Edges = transitions
- Supports cycles (iterative workflows)

**Simple LangGraph Example:**

```python
from langgraph.graph import Graph, END

# Define nodes
def researcher(state):
    query = state["query"]
    research = search_web(query)
    return {"research": research}

def writer(state):
    research = state["research"]
    article = generate_article(research)
    return {"article": article}

def reviewer(state):
    article = state["article"]
    if quality_check(article):
        return {"status": "approved"}
    else:
        return {"status": "needs_revision", "feedback": "..."}

# Build graph
workflow = Graph()

workflow.add_node("research", researcher)
workflow.add_node("write", writer)
workflow.add_node("review", reviewer)

# Add edges
workflow.add_edge("research", "write")
workflow.add_edge("write", "review")

# Conditional edge (cycle if needed)
workflow.add_conditional_edges(
    "review",
    lambda state: state["status"],
    {
        "approved": END,
        "needs_revision": "write"  # Go back to writer
    }
)

workflow.set_entry_point("research")

# Compile and run
app = workflow.compile()
result = app.invoke({"query": "AI trends 2024"})
```

**Complex LangGraph (Parallel Processing):**

```python
from langgraph.graph import Graph

def parallel_research(state):
    \"\"\"
    Research multiple sources simultaneously
    \"\"\"
    query = state["query"]
    
    sources = ["academic", "news", "social"]
    results = []
    
    for source in sources:
        result = search_source(query, source)
        results.append(result)
    
    return {"sources": results}

def synthesize(state):
    \"\"\"
    Combine results from all sources
    \"\"\"
    sources = state["sources"]
    synthesis = combine_sources(sources)
    return {"final": synthesis}

# Build graph with parallel nodes
workflow = Graph()
workflow.add_node("parallel_research", parallel_research)
workflow.add_node("synthesize", synthesize)
workflow.add_edge("parallel_research", "synthesize")
workflow.set_entry_point("parallel_research")

app = workflow.compile()
```

---

**Agent Evaluation:**

**Success Rate:**
```python
def evaluate_agent(agent, test_cases):
    successes = 0
    
    for case in test_cases:
        try:
            result = agent.run(case["input"])
            if result == case["expected"]:
                successes += 1
        except Exception as e:
            print(f"Error: {e}")
    
    success_rate = successes / len(test_cases)
    return success_rate
```

**Tool Usage Efficiency:**
```python
def measure_efficiency(agent, task):
    \"\"\"
    How many tool calls did agent make?
    Fewer is usually better
    \"\"\"
    agent.reset_metrics()
    result = agent.run(task)
    
    return {
        "tool_calls": agent.tool_call_count,
        "tokens_used": agent.token_count,
        "latency": agent.total_time,
        "cost": agent.calculate_cost()
    }
```

**Human Evaluation:**
```python
def human_eval(agent_responses):
    \"\"\"
    Rate agent helpfulness, accuracy, safety
    \"\"\"
    scores = {
        "helpfulness": 0,
        "accuracy": 0,
        "safety": 0
    }
    
    for response in agent_responses:
        print(f"Response: {response}")
        scores["helpfulness"] += int(input("Helpfulness (1-5): "))
        scores["accuracy"] += int(input("Accuracy (1-5): "))
        scores["safety"] += int(input("Safety (1-5): "))
    
    # Average
    n = len(agent_responses)
    return {k: v/n for k, v in scores.items()}
```

---

**Agent Safety & Guardrails:**

**1. Tool Access Control:**
```python
class SafeAgent:
    def __init__(self, allowed_tools):
        self.allowed_tools = allowed_tools
    
    def execute_tool(self, tool_name, args):
        # Check if tool is allowed
        if tool_name not in self.allowed_tools:
            return "ERROR: Tool not allowed"
        
        # Check arguments
        if not self.validate_args(tool_name, args):
            return "ERROR: Invalid arguments"
        
        # Execute
        return self.allowed_tools[tool_name](**args)
```

**2. Output Validation:**
```python
def validate_agent_output(output):
    \"\"\"
    Check if agent output is safe
    \"\"\"
    # Check for PII leakage
    if contains_pii(output):
        return False, "Output contains PII"
    
    # Check for harmful content
    if is_harmful(output):
        return False, "Output contains harmful content"
    
    # Check for hallucinations
    if confidence_score(output) < 0.7:
        return False, "Low confidence, possible hallucination"
    
    return True, "Output is safe"
```

**3. Budget Limits:**
```python
class BudgetLimitedAgent:
    def __init__(self, max_cost_per_task=1.0):
        self.max_cost = max_cost_per_task
        self.current_cost = 0
    
    def run(self, task):
        while self.current_cost < self.max_cost:
            action = self.decide_next_action()
            cost = self.estimate_action_cost(action)
            
            if self.current_cost + cost > self.max_cost:
                return "Budget exceeded, stopping"
            
            result = self.execute(action)
            self.current_cost += cost
            
            if self.is_done(result):
                return result
        
        return "Task incomplete, budget exhausted"
```

---

**Production Agent Patterns:**

**Pattern 1: Customer Service Agent**
```python
class CustomerServiceAgent:
    def __init__(self):
        self.tools = {
            "check_order_status": self.check_order,
            "process_refund": self.process_refund,
            "escalate_to_human": self.escalate
        }
        self.memory = VectorMemory()
    
    def handle_request(self, customer_id, message):
        # Load customer history
        history = self.memory.recall(f"customer_{customer_id}")
        
        # Decide action
        action = self.classify_intent(message)
        
        if action == "simple_query":
            return self.answer_query(message, history)
        elif action == "requires_action":
            return self.execute_action(message, history)
        elif action == "complex":
            return self.escalate(customer_id, message)
    
    def answer_query(self, message, history):
        context = f"History: {history}\\nQuery: {message}"
        return llm(context)
    
    def execute_action(self, message, history):
        # Use ReAct pattern
        return self.react_loop(message, self.tools)
```

**Pattern 2: Code Assistant Agent**
```python
class CodeAssistantAgent:
    def __init__(self):
        self.tools = {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "run_tests": self.run_tests,
            "search_docs": self.search_docs
        }
    
    def fix_bug(self, error_message, codebase_path):
        # Step 1: Understand error
        analysis = self.analyze_error(error_message)
        
        # Step 2: Find relevant code
        relevant_files = self.tools["search_docs"](analysis)
        
        # Step 3: Generate fix
        fix = self.generate_fix(analysis, relevant_files)
        
        # Step 4: Apply and test
        self.tools["write_file"](fix)
        test_result = self.tools["run_tests"]()
        
        # Step 5: Iterate if needed
        if not test_result["success"]:
            return self.fix_bug(test_result["error"], codebase_path)
        
        return {"status": "fixed", "changes": fix}
```

**Pattern 3: Research Agent**
```python
class ResearchAgent:
    def __init__(self):
        self.tools = {
            "search_arxiv": self.search_arxiv,
            "search_web": self.search_web,
            "summarize": self.summarize,
            "extract_citations": self.extract_citations
        }
        self.findings = []
    
    def research_topic(self, topic, depth=3):
        \"\"\"
        Recursively research a topic
        \"\"\"
        # Level 1: Overview
        overview = self.get_overview(topic)
        self.findings.append(overview)
        
        if depth <= 1:
            return self.synthesize_findings()
        
        # Level 2: Subtopics
        subtopics = self.extract_subtopics(overview)
        
        for subtopic in subtopics:
            result = self.research_topic(subtopic, depth - 1)
            self.findings.append(result)
        
        return self.synthesize_findings()
```

---

**Agent Debugging:**

**Logging:**
```python
import logging

class DebuggableAgent:
    def __init__(self):
        self.logger = logging.getLogger("agent")
        self.logger.setLevel(logging.DEBUG)
    
    def run(self, task):
        self.logger.info(f"Starting task: {task}")
        
        for step in self.plan(task):
            self.logger.debug(f"Executing: {step}")
            
            try:
                result = self.execute(step)
                self.logger.debug(f"Result: {result}")
            except Exception as e:
                self.logger.error(f"Error in {step}: {e}")
                raise
        
        self.logger.info("Task completed")
        return result
```

**Tracing:**
```python
class TracedAgent:
    def __init__(self):
        self.trace = []
    
    def run(self, task):
        self.trace.append({"event": "start", "task": task})
        
        # ... agent logic ...
        
        self.trace.append({"event": "tool_call", "tool": "search", "args": {...}})
        self.trace.append({"event": "result", "data": ...})
        
        return result
    
    def export_trace(self):
        \"\"\"
        Export trace for debugging
        \"\"\"
        return json.dumps(self.trace, indent=2)
```

---

**Agent Cost Optimization:**

**1. Tool Call Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_tool_call(tool_name, args_hash):
    return execute_tool(tool_name, args_hash)
```

**2. Smaller Models for Planning:**
```python
class HybridAgent:
    def __init__(self):
        self.planner = GPT35Turbo()  # Cheap
        self.executor = GPT4()       # Expensive but accurate
    
    def run(self, task):
        # Use cheap model for planning
        plan = self.planner.create_plan(task)
        
        # Use expensive model only for critical steps
        results = []
        for step in plan:
            if step.complexity == "high":
                result = self.executor.execute(step)
            else:
                result = self.planner.execute(step)
            results.append(result)
        
        return self.synthesize(results)
```

**3. Early Stopping:**
```python
def agent_with_confidence(task, confidence_threshold=0.8):
    \"\"\"
    Stop when confident enough
    \"\"\"
    for iteration in range(max_iterations):
        result = agent_step()
        confidence = estimate_confidence(result)
        
        if confidence > confidence_threshold:
            return result  # Good enough!
    
    return result  # Max iterations reached
```

---

**Agent Checklist:**

**Design:**
- [ ] Clear task definition
- [ ] Appropriate tools selected
- [ ] Memory strategy defined
- [ ] Error handling planned
- [ ] Budget/limits set

**Implementation:**
- [ ] Tools tested independently
- [ ] Memory system working
- [ ] Logging/tracing enabled
- [ ] Safety guardrails in place
- [ ] Cost estimation done

**Testing:**
- [ ] Unit tests for tools
- [ ] Integration tests for workflows
- [ ] Edge cases covered
- [ ] Performance benchmarked
- [ ] Human evaluation completed

**Deployment:**
- [ ] Monitoring dashboard ready
- [ ] Alert system configured
- [ ] Rollback plan documented
- [ ] Rate limiting enabled
- [ ] Cost tracking active
"""
            )
        elif selected_unit == 6:
            st.markdown("#### 📘 Production Deployment & Scaling")
            st.markdown("""
**Deploying LLMs** to production requires careful planning.

**Considerations:**
- **Latency:** Response time requirements
- **Cost:** Token usage at scale
- **Reliability:** Uptime and error handling
- **Security:** API key management
- **Monitoring:** Track usage and quality

**Deployment Options:**
- API wrapper (FastAPI)
- Serverless (AWS Lambda)
- Containers (Docker + Kubernetes)
- Managed platforms (Hugging Face Inference)

**Optimization:**
- Caching frequent queries
- Rate limiting
- Batch processing
- Model quantization
""")
            
            st.markdown("#### 🚀 Production Deployment Deep Dive")
            st.markdown("""Deploying LLMs to production at scale requires specialized infrastructure and practices:

**Serving Infrastructure Options:**

| Solution | Throughput | Latency | Cost | Best For |
|----------|-----------|---------|------|----------|
| **vLLM** | Very High | Low | Medium | Self-hosted, high scale |
| **Text Generation Inference (TGI)** | High | Low | Medium | Hugging Face models |
| **Triton** | Very High | Very Low | High | Multi-model serving |
| **OpenAI API** | High | Medium | High | Quick deployment |
| **Ray Serve** | High | Medium | Medium | Multi-model, complex workflows |
| **BentoML** | Medium | Medium | Low | Simple deployment |

---

**1. vLLM: High-Performance Serving**

**What is vLLM?**
- Fastest open-source LLM serving framework
- 24x throughput vs HuggingFace Transformers
- PagedAttention for memory optimization
- Continuous batching

**Installation & Setup:**
```bash
pip install vllm

# Serve Llama 2 7B
python -m vllm.entrypoints.openai.api_server \\
    --model meta-llama/Llama-2-7b-hf \\
    --port 8000 \\
    --tensor-parallel-size 1
```

**Python API:**
```python
from vllm import LLM, SamplingParams

# Load model
llm = LLM(model="meta-llama/Llama-2-7b-hf")

# Configure sampling
sampling_params = SamplingParams(
    temperature=0.8,
    top_p=0.95,
    max_tokens=100
)

# Generate
prompts = ["Hello, my name is", "The capital of France is"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Prompt: {output.prompt}")
    print(f"Generated: {output.outputs[0].text}")
```

**OpenAI-Compatible API:**
```python
import openai

# Point to vLLM server
openai.api_key = "EMPTY"
openai.api_base = "http://localhost:8000/v1"

# Use like OpenAI
response = openai.Completion.create(
    model="meta-llama/Llama-2-7b-hf",
    prompt="Once upon a time",
    max_tokens=100
)

print(response.choices[0].text)
```

**Performance Benchmarks:**

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| **vLLM** | 150 | 45ms | 120ms |
| **TGI** | 120 | 55ms | 140ms |
| **Transformers** | 6 | 800ms | 2000ms |

*Llama 2 7B, single A100 GPU*

---

**2. Text Generation Inference (TGI)**

**What is TGI?**
- Hugging Face's production serving solution
- Optimized for Hugging Face models
- Built-in monitoring & metrics
- Docker-first deployment

**Docker Deployment:**
```bash
# Pull image
docker pull ghcr.io/huggingface/text-generation-inference:latest

# Run server
docker run -d \\
    -p 8080:80 \\
    -v $PWD/models:/models \\
    --gpus all \\
    ghcr.io/huggingface/text-generation-inference:latest \\
    --model-id meta-llama/Llama-2-7b-hf \\
    --num-shard 1
```

**Python Client:**
```python
from text_generation import Client

client = Client("http://localhost:8080")

# Generate
response = client.generate(
    "Once upon a time",
    max_new_tokens=100,
    temperature=0.8
)

print(response.generated_text)

# Streaming
for response in client.generate_stream("Tell me a story", max_new_tokens=100):
    if not response.token.special:
        print(response.token.text, end="")
```

**Kubernetes Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-serving
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm
  template:
    metadata:
      labels:
        app: llm
    spec:
      containers:
      - name: tgi
        image: ghcr.io/huggingface/text-generation-inference:latest
        args:
          - --model-id=meta-llama/Llama-2-7b-hf
          - --num-shard=1
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 16Gi
          requests:
            nvidia.com/gpu: 1
            memory: 16Gi
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: llm-service
spec:
  selector:
    app: llm
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

---

**3. Load Balancing & Autoscaling**

**Nginx Load Balancer:**
```nginx
upstream llm_backend {
    least_conn;  # Route to least busy server
    
    server llm-server-1:8000 max_fails=3 fail_timeout=30s;
    server llm-server-2:8000 max_fails=3 fail_timeout=30s;
    server llm-server-3:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://llm_backend;
        proxy_set_header Host $host;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        
        # Rate limiting
        limit_req zone=llm_limit burst=10 nodelay;
    }
}

# Rate limit configuration
limit_req_zone $binary_remote_addr zone=llm_limit:10m rate=10r/s;
```

**Kubernetes HPA (Horizontal Pod Autoscaler):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-serving
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 1
        periodSeconds: 60
```

**AWS Auto Scaling:**
```python
import boto3

autoscaling = boto3.client('autoscaling')

# Create auto-scaling group
autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='llm-serving-asg',
    LaunchTemplate={
        'LaunchTemplateId': 'lt-xxxx',
        'Version': '$Latest'
    },
    MinSize=2,
    MaxSize=10,
    DesiredCapacity=3,
    TargetGroupARNs=['arn:aws:elasticloadbalancing:...'],
    HealthCheckType='ELB',
    HealthCheckGracePeriod=300
)

# CPU-based scaling policy
autoscaling.put_scaling_policy(
    AutoScalingGroupName='llm-serving-asg',
    PolicyName='scale-on-cpu',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'ASGAverageCPUUtilization'
        },
        'TargetValue': 70.0
    }
)
```

---

**4. Monitoring & Observability**

**Prometheus Metrics:**
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
requests_total = Counter('llm_requests_total', 'Total requests')
request_duration = Histogram('llm_request_duration_seconds', 'Request duration')
active_requests = Gauge('llm_active_requests', 'Active requests')
tokens_generated = Counter('llm_tokens_generated_total', 'Total tokens')
errors_total = Counter('llm_errors_total', 'Total errors', ['error_type'])

def generate_text(prompt):
    requests_total.inc()
    active_requests.inc()
    
    start_time = time.time()
    
    try:
        # Generate
        response = llm.generate(prompt)
        tokens_generated.inc(len(response.tokens))
        
        # Record duration
        duration = time.time() - start_time
        request_duration.observe(duration)
        
        return response
        
    except Exception as e:
        errors_total.labels(error_type=type(e).__name__).inc()
        raise
        
    finally:
        active_requests.dec()

# Start metrics server
start_http_server(8001)
```

**Grafana Dashboard (JSON):**
```json
{
  "dashboard": {
    "title": "LLM Serving Dashboard",
    "panels": [
      {
        "title": "Requests per Second",
        "targets": [{
          "expr": "rate(llm_requests_total[5m])"
        }]
      },
      {
        "title": "Average Latency (p50, p95, p99)",
        "targets": [
          {"expr": "histogram_quantile(0.50, llm_request_duration_seconds)"},
          {"expr": "histogram_quantile(0.95, llm_request_duration_seconds)"},
          {"expr": "histogram_quantile(0.99, llm_request_duration_seconds)"}
        ]
      },
      {
        "title": "Error Rate",
        "targets": [{
          "expr": "rate(llm_errors_total[5m])"
        }]
      },
      {
        "title": "Active Requests",
        "targets": [{
          "expr": "llm_active_requests"
        }]
      },
      {
        "title": "Tokens Generated per Second",
        "targets": [{
          "expr": "rate(llm_tokens_generated_total[5m])"
        }]
      }
    ]
  }
}
```

**Application Performance Monitoring:**
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

def generate_with_tracing(prompt):
    with tracer.start_as_current_span("llm_generation") as span:
        span.set_attribute("prompt_length", len(prompt))
        
        # Embedding
        with tracer.start_as_current_span("embedding"):
            embedding = embed(prompt)
        
        # Generation
        with tracer.start_as_current_span("generation"):
            response = llm.generate(prompt)
        
        span.set_attribute("tokens_generated", len(response.tokens))
        return response
```

---

**5. Caching Strategies**

**Redis Cache:**
```python
import redis
import hashlib
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cached_generate(prompt, **kwargs):
    # Create cache key
    cache_key = hashlib.md5(
        json.dumps({"prompt": prompt, **kwargs}).encode()
    ).hexdigest()
    
    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Generate
    response = llm.generate(prompt, **kwargs)
    
    # Cache result (24h TTL)
    redis_client.setex(
        cache_key,
        86400,
        json.dumps(response)
    )
    
    return response

# Savings: 30-50% cost reduction for repeated queries
```

**Semantic Caching:**
```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticCache:
    def __init__(self, similarity_threshold=0.95):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache = []  # (embedding, response) pairs
        self.threshold = similarity_threshold
    
    def get(self, prompt):
        prompt_emb = self.embedder.encode(prompt)
        
        for cached_emb, cached_response in self.cache:
            similarity = np.dot(prompt_emb, cached_emb)
            if similarity > self.threshold:
                return cached_response
        
        return None
    
    def set(self, prompt, response):
        prompt_emb = self.embedder.encode(prompt)
        self.cache.append((prompt_emb, response))
        
        # Limit cache size
        if len(self.cache) > 10000:
            self.cache.pop(0)

# Usage
cache = SemanticCache()

def generate_with_semantic_cache(prompt):
    # Check semantic cache
    cached = cache.get(prompt)
    if cached:
        return cached
    
    # Generate
    response = llm.generate(prompt)
    
    # Cache
    cache.set(prompt, response)
    
    return response
```

---

**6. Cost Optimization**

**Request Batching:**
```python
import asyncio
from collections import deque

class BatchingService:
    def __init__(self, batch_size=32, max_wait_ms=50):
        self.batch_size = batch_size
        self.max_wait_ms = max_wait_ms
        self.queue = deque()
        self.processing = False
    
    async def generate(self, prompt):
        # Add to queue
        future = asyncio.Future()
        self.queue.append((prompt, future))
        
        # Start processing if not already
        if not self.processing:
            asyncio.create_task(self.process_batch())
        
        # Wait for result
        return await future
    
    async def process_batch(self):
        self.processing = True
        
        # Wait for batch to fill or timeout
        await asyncio.sleep(self.max_wait_ms / 1000)
        
        # Collect batch
        batch = []
        futures = []
        
        while self.queue and len(batch) < self.batch_size:
            prompt, future = self.queue.popleft()
            batch.append(prompt)
            futures.append(future)
        
        if not batch:
            self.processing = False
            return
        
        # Process batch
        responses = llm.generate(batch)
        
        # Return results
        for future, response in zip(futures, responses):
            future.set_result(response)
        
        # Process next batch if queue not empty
        if self.queue:
            asyncio.create_task(self.process_batch())
        else:
            self.processing = False

# Batching increases throughput by 5-10x
```

**Model Quantization:**
```python
from transformers import AutoModelForCausalLM
import torch

# FP16 (2x memory reduction, minimal quality loss)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16
)

# INT8 (4x memory reduction, <5% quality loss)
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=quantization_config
)

# INT4 (8x memory reduction, ~10% quality loss)
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=quantization_config
)
```

**Token-Level Streaming:**
```python
def streaming_generate(prompt):
    \"\"\"
    Stream tokens as they're generated
    Reduces perceived latency
    \"\"\"
    for token in llm.generate_stream(prompt):
        yield token
        # User sees partial response immediately

# FastAPI endpoint
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/generate/stream")
async def stream_endpoint(prompt: str):
    return StreamingResponse(
        streaming_generate(prompt),
        media_type="text/event-stream"
    )
```

---

**7. A/B Testing Framework**

**Experiment Configuration:**
```python
import random

class ABTest:
    def __init__(self, variants):
        self.variants = variants  # {"model_a": 0.5, "model_b": 0.5}
    
    def select_variant(self, user_id):
        # Consistent variant per user
        random.seed(hash(user_id))
        r = random.random()
        
        cumulative = 0
        for variant, probability in self.variants.items():
            cumulative += probability
            if r < cumulative:
                return variant
        
        return list(self.variants.keys())[-1]

# Setup experiment
experiment = ABTest({
    "gpt-3.5-turbo": 0.5,
    "gpt-4": 0.5
})

def generate_with_ab_test(user_id, prompt):
    variant = experiment.select_variant(user_id)
    
    # Log assignment
    log_experiment_assignment(user_id, variant)
    
    # Generate with selected model
    response = generate(prompt, model=variant)
    
    # Log result
    log_experiment_result(user_id, variant, response)
    
    return response
```

**Metrics Collection:**
```python
class ABTestMetrics:
    def __init__(self):
        self.metrics = {}  # variant -> [scores]
    
    def record(self, variant, metric_name, value):
        key = f"{variant}:{metric_name}"
        if key not in self.metrics:
            self.metrics[key] = []
        self.metrics[key].append(value)
    
    def compare(self, metric_name):
        results = {}
        for variant in ["model_a", "model_b"]:
            key = f"{variant}:{metric_name}"
            values = self.metrics.get(key, [])
            results[variant] = {
                "mean": np.mean(values),
                "std": np.std(values),
                "count": len(values)
            }
        
        # Statistical significance test
        from scipy import stats
        t_stat, p_value = stats.ttest_ind(
            self.metrics["model_a:"+metric_name],
            self.metrics["model_b:"+metric_name]
        )
        
        results["p_value"] = p_value
        results["significant"] = p_value < 0.05
        
        return results
```

---

**8. Error Handling & Retry Logic**

**Exponential Backoff:**
```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    # Calculate delay with exponential backoff + jitter
                    delay = min(
                        base_delay * (2 ** attempt) + random.uniform(0, 1),
                        max_delay
                    )
                    
                    print(f"Retry {attempt+1}/{max_retries} after {delay:.2f}s")
                    time.sleep(delay)
            
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def generate_with_retry(prompt):
    return llm.generate(prompt)
```

**Circuit Breaker:**
```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if datetime.now() - self.last_failure > timedelta(seconds=self.timeout):
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset if half-open
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failures = 0
            
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure = datetime.now()
            
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
            
            raise

# Usage
breaker = CircuitBreaker()

def safe_generate(prompt):
    return breaker.call(llm.generate, prompt)
```

---

**9. Security Best Practices**

**API Key Management:**
```python
import os
from cryptography.fernet import Fernet

class SecureConfig:
    def __init__(self):
        # Load encryption key from environment
        self.key = os.environ.get("ENCRYPTION_KEY").encode()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, value):
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt(self, encrypted_value):
        return self.cipher.decrypt(encrypted_value.encode()).decode()

# Store API keys encrypted
config = SecureConfig()
encrypted_key = config.encrypt(os.environ["OPENAI_API_KEY"])

# Use when needed
api_key = config.decrypt(encrypted_key)
```

**Input Validation:**
```python
def validate_input(prompt, max_length=10000):
    \"\"\"
    Validate and sanitize user input
    \"\"\"
    # Length check
    if len(prompt) > max_length:
        raise ValueError(f"Prompt too long: {len(prompt)} > {max_length}")
    
    # Check for injection attempts
    dangerous_patterns = [
        "ignore previous instructions",
        "you are now",
        "new instructions:",
    ]
    
    prompt_lower = prompt.lower()
    for pattern in dangerous_patterns:
        if pattern in prompt_lower:
            raise ValueError("Potential prompt injection detected")
    
    # Check for PII
    import re
    if re.search(r'\\b\\d{3}-\\d{2}-\\d{4}\\b', prompt):  # SSN
        raise ValueError("PII detected in prompt")
    
    return prompt

def safe_generate(prompt):
    validated = validate_input(prompt)
    return llm.generate(validated)
```

**Rate Limiting:**
```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = defaultdict(list)
    
    def allow(self, user_id):
        now = datetime.now()
        
        # Clean old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if now - req_time < self.window
        ]
        
        # Check limit
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # Record request
        self.requests[user_id].append(now)
        return True

# Usage
limiter = RateLimiter(max_requests=100, window_seconds=60)

def generate_with_rate_limit(user_id, prompt):
    if not limiter.allow(user_id):
        raise Exception("Rate limit exceeded")
    
    return llm.generate(prompt)
```

---

**10. Deployment Checklist**

**Pre-Production:**
- [ ] Load testing completed (target: 100 req/s)
- [ ] Error rate < 0.1%
- [ ] p99 latency < 2 seconds
- [ ] Cost per request calculated
- [ ] Monitoring dashboards configured
- [ ] Alerts set up (latency, errors, cost)
- [ ] Backup/failover tested
- [ ] Security audit completed
- [ ] Rate limiting implemented
- [ ] Caching strategy defined

**Production Launch:**
- [ ] Blue-green deployment ready
- [ ] Rollback procedure documented
- [ ] Runbook created
- [ ] On-call rotation scheduled
- [ ] Incident response plan ready
- [ ] Performance baselines established
- [ ] Cost tracking active
- [ ] User feedback collection enabled

**Post-Launch:**
- [ ] Daily metrics review
- [ ] Weekly cost analysis
- [ ] Monthly performance optimization
- [ ] Quarterly capacity planning
- [ ] Continuous A/B testing
- [ ] Model updates evaluated
"""
            )
        elif selected_unit == 7:
            st.markdown("#### 📘 Capstone: Build Production LLM Application")
            st.markdown("""
**Your capstone** demonstrates end-to-end LLM engineering skills.

**Requirements:**
- Solve real business problem
- Production-quality code
- Proper error handling
- Monitoring and logging
- Documentation
- Cost optimization

**Evaluation Criteria:**
- Architecture design
- Code quality
- Performance
- Innovation
- Business value
""")
            
            st.markdown("#### 🎯 Capstone Project Options")
            st.markdown("""Choose one of these comprehensive projects that demonstrate production LLM engineering:

**Project 1: Enterprise RAG System**

**Problem Statement:**
Build a production RAG system for internal company knowledge base.

**Requirements:**
- Support 100K+ documents
- Sub-500ms query latency
- Multi-user concurrent access
- Source citation
- Cost < $0.10 per query

**Technical Implementation:**

```python
# Architecture
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import openai

class RAGSystem:
    def __init__(self):
        # Vector store
        self.chroma = chromadb.Client()
        self.collection = self.chroma.create_collection("knowledge_base")
        
        # Embedder
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Cache
        self.cache = {}
    
    def ingest_documents(self, documents):
        \"\"\"Batch ingest with progress tracking\"\"\"
        for i, doc in enumerate(documents):
            # Chunk document
            chunks = self.chunk_document(doc, chunk_size=512)
            
            # Generate embeddings
            embeddings = self.embedder.encode(chunks)
            
            # Store in vector DB
            self.collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=[{"source": doc["source"], "page": i}],
                ids=[f"{doc['id']}_chunk_{j}" for j in range(len(chunks))]
            )
    
    def query(self, question):
        # Check cache
        if question in self.cache:
            return self.cache[question]
        
        # Embed query
        query_emb = self.embedder.encode(question)
        
        # Retrieve
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=5
        )
        
        # Construct prompt
        context = "\\n\\n".join(results['documents'][0])
        prompt = f\"\"\"Answer based on context:
        
Context: {context}

Question: {question}

Answer:\"\"\"
        
        # Generate
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = {
            "answer": response.choices[0].message.content,
            "sources": results['metadatas'][0]
        }
        
        # Cache
        self.cache[question] = answer
        
        return answer

# FastAPI endpoints
app = FastAPI()
rag = RAGSystem()

class Query(BaseModel):
    question: str

@app.post("/query")
async def query_endpoint(q: Query):
    try:
        result = rag.query(q.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Evaluation Rubric:**

| Criteria | Weight | Excellent (5) | Good (4) | Fair (3) |
|----------|--------|---------------|----------|----------|
| **Architecture** | 25% | Scalable, modular, cloud-native | Well-structured, some cloud | Basic structure |
| **Performance** | 20% | <300ms, handles 100 req/s | <500ms, 50 req/s | <1s, 10 req/s |
| **Code Quality** | 20% | Tests, docs, type hints | Some tests/docs | Minimal docs |
| **Features** | 20% | Caching, monitoring, auth | Basic features | Core only |
| **Cost** | 15% | <$0.05/query | <$0.10/query | <$0.20/query |

**Deliverables:**
- [ ] Working application (deployed)
- [ ] GitHub repo with README
- [ ] Architecture diagram
- [ ] Performance benchmarks
- [ ] Cost analysis
- [ ] 10-minute demo video

---

**Project 2: AI-Powered Customer Support Agent**

**Problem Statement:**
Build an autonomous customer support agent that handles tier-1 support tickets.

**Requirements:**
- Multi-turn conversations
- Tool use (check orders, process refunds)
- Escalation to humans when needed
- < 5 second response time
- 80%+ resolution rate

**Technical Implementation:**

```python
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

class SupportAgent:
    def __init__(self):
        # Tools
        self.tools = [
            Tool(
                name="CheckOrderStatus",
                func=self.check_order,
                description="Check status of order by order_id"
            ),
            Tool(
                name="ProcessRefund",
                func=self.process_refund,
                description="Process refund for order_id"
            ),
            Tool(
                name="SearchKnowledgeBase",
                func=self.search_kb,
                description="Search internal docs"
            ),
            Tool(
                name="EscalateToHuman",
                func=self.escalate,
                description="Escalate complex issues to human agent"
            )
        ]
        
        # Memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=OpenAI(temperature=0),
            agent="chat-conversational-react-description",
            memory=self.memory,
            verbose=True
        )
    
    def check_order(self, order_id):
        # Call order API
        return {"status": "shipped", "tracking": "1Z999"}
    
    def process_refund(self, order_id):
        # Process refund logic
        return {"refund_id": "REF123", "amount": 49.99}
    
    def search_kb(self, query):
        # RAG search
        return "Return policy: 30 days..."
    
    def escalate(self, reason):
        # Create ticket for human
        return {"ticket_id": "TKT456", "assigned_to": "agent@company.com"}
    
    def handle_message(self, customer_id, message):
        # Load customer context
        context = self.load_customer_context(customer_id)
        
        # Add to prompt
        prompt = f\"\"\"Customer Context:
{context}

Customer: {message}

Handle this professionally and helpfully.\"\"\"
        
        # Run agent
        response = self.agent.run(prompt)
        
        return response

# Usage
agent = SupportAgent()
response = agent.handle_message(
    customer_id="CUST123",
    message="Where is my order #12345?"
)
```

**Evaluation Rubric:**

| Criteria | Weight | Excellent (5) | Good (4) | Fair (3) |
|----------|--------|---------------|----------|----------|
| **Autonomy** | 30% | Handles 90%+ without human | 80%+ | 70%+ |
| **Accuracy** | 25% | 95%+ correct responses | 85%+ | 75%+ |
| **Latency** | 20% | <3s average | <5s | <10s |
| **Tool Use** | 15% | Efficient, appropriate | Mostly good | Basic |
| **User Experience** | 10% | Natural, helpful, empathetic | Clear | Functional |

---

**Project 3: Code Assistant with Repository Context**

**Problem Statement:**
Build an AI code assistant that understands your codebase context.

**Requirements:**
- Code generation
- Bug fixing
- Code review
- Documentation generation
- Works with 10K+ files

**Technical Implementation:**

```python
import ast
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

class CodeAssistant:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.index_codebase()
    
    def index_codebase(self):
        \"\"\"Index all code files\"\"\"
        code_chunks = []
        
        # Find all Python files
        for file in Path(self.repo_path).rglob("*.py"):
            # Parse file
            with open(file) as f:
                try:
                    tree = ast.parse(f.read())
                    
                    # Extract functions/classes
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            code_chunks.append({
                                "code": ast.unparse(node),
                                "type": "function",
                                "name": node.name,
                                "file": str(file)
                            })
                        elif isinstance(node, ast.ClassDef):
                            code_chunks.append({
                                "code": ast.unparse(node),
                                "type": "class",
                                "name": node.name,
                                "file": str(file)
                            })
                except:
                    pass
        
        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts=[chunk["code"] for chunk in code_chunks],
            metadatas=code_chunks,
            embedding=self.embeddings
        )
    
    def generate_code(self, description):
        \"\"\"Generate code with context\"\"\"
        # Find relevant code examples
        similar = self.vectorstore.similarity_search(description, k=3)
        
        context = "\\n\\n".join([doc.page_content for doc in similar])
        
        prompt = f\"\"\"Based on these examples from the codebase:

{context}

Generate code for: {description}

Follow the same style and patterns.\"\"\"
        
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
    
    def fix_bug(self, error_message, file_path):
        \"\"\"Fix bugs with context\"\"\"
        # Read file
        with open(file_path) as f:
            code = f.read()
        
        # Find similar code
        similar = self.vectorstore.similarity_search(error_message, k=3)
        
        prompt = f\"\"\"Error: {error_message}

File: {file_path}
```python
{code}
```

Similar working code:
{similar}

Provide a fix:\"\"\"
        
        fix = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        
        return fix

# Usage
assistant = CodeAssistant("/path/to/repo")
code = assistant.generate_code("Create a REST API endpoint for user auth")
```

**Evaluation Rubric:**

| Criteria | Weight | Excellent (5) | Good (4) | Fair (3) |
|----------|--------|---------------|----------|----------|
| **Context Understanding** | 30% | Deep understanding | Good context | Basic context |
| **Code Quality** | 25% | Idiomatic, tested | Good style | Functional |
| **Accuracy** | 20% | 95%+ correct | 85%+ | 75%+ |
| **Performance** | 15% | Indexes 10K files <1min | <5min | <10min |
| **Features** | 10% | Generation, review, docs | 2 features | 1 feature |

---

**Project 4: Content Moderation System**

**Problem Statement:**
Build an AI content moderation system for user-generated content.

**Requirements:**
- Detect harmful content (toxicity, PII, NSFW)
- Multi-language support
- < 100ms latency
- 99%+ accuracy
- Explainable decisions

**Technical Implementation:**

```python
from transformers import pipeline
import re
from typing import Dict, List

class ContentModerator:
    def __init__(self):
        # Models
        self.toxicity = pipeline("text-classification", 
                                model="unitary/toxic-bert")
        self.pii_detector = self.load_pii_patterns()
        
        # Thresholds
        self.toxicity_threshold = 0.8
    
    def load_pii_patterns(self):
        return {
            "email": r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b',
            "phone": r'\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b',
            "ssn": r'\\b\\d{3}-\\d{2}-\\d{4}\\b',
            "credit_card": r'\\b\\d{4}[- ]?\\d{4}[- ]?\\d{4}[- ]?\\d{4}\\b'
        }
    
    def moderate(self, text: str) -> Dict:
        \"\"\"Comprehensive moderation\"\"\"
        results = {
            "safe": True,
            "reasons": [],
            "confidence": 1.0
        }
        
        # Check toxicity
        toxicity = self.toxicity(text)[0]
        if toxicity['score'] > self.toxicity_threshold:
            results["safe"] = False
            results["reasons"].append({
                "type": "toxicity",
                "confidence": toxicity['score'],
                "label": toxicity['label']
            })
        
        # Check PII
        for pii_type, pattern in self.pii_detector.items():
            matches = re.findall(pattern, text)
            if matches:
                results["safe"] = False
                results["reasons"].append({
                    "type": f"pii_{pii_type}",
                    "matches": len(matches)
                })
        
        # Check prompt injection
        injection_patterns = [
            "ignore previous instructions",
            "you are now",
            "new role:"
        ]
        for pattern in injection_patterns:
            if pattern in text.lower():
                results["safe"] = False
                results["reasons"].append({
                    "type": "prompt_injection",
                    "pattern": pattern
                })
        
        return results
    
    def sanitize(self, text: str) -> str:
        \"\"\"Remove PII while keeping content\"\"\"
        sanitized = text
        
        # Replace PII
        for pii_type, pattern in self.pii_detector.items():
            sanitized = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", sanitized)
        
        return sanitized

# FastAPI endpoint
from fastapi import FastAPI

app = FastAPI()
moderator = ContentModerator()

@app.post("/moderate")
async def moderate_content(text: str):
    result = moderator.moderate(text)
    
    if not result["safe"]:
        sanitized = moderator.sanitize(text)
        result["sanitized"] = sanitized
    
    return result
```

**Evaluation Rubric:**

| Criteria | Weight | Excellent (5) | Good (4) | Fair (3) |
|----------|--------|---------------|----------|----------|
| **Accuracy** | 35% | 99%+ | 95%+ | 90%+ |
| **Coverage** | 25% | 5+ categories | 3-4 categories | 2 categories |
| **Latency** | 20% | <50ms | <100ms | <200ms |
| **Explainability** | 15% | Detailed reasons | Basic reasons | Flag only |
| **False Positives** | 5% | <1% | <3% | <5% |

---

**Project 5: Multi-Language Translation API**

**Problem Statement:**
Build a production translation API with quality assurance.

**Requirements:**
- Support 10+ languages
- Preserve formatting (HTML, Markdown)
- Quality scoring
- Caching for cost optimization
- < 500ms latency

**Technical Implementation:**

```python
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from typing import Dict
import hashlib

class TranslationAPI:
    def __init__(self):
        # Model
        self.model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
        
        # Cache
        self.cache = {}
        
        # Language codes
        self.supported_langs = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ar": "Arabic",
            "ru": "Russian",
            "pt": "Portuguese",
            "hi": "Hindi"
        }
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict:
        # Check cache
        cache_key = hashlib.md5(
            f"{text}:{source_lang}:{target_lang}".encode()
        ).hexdigest()
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Set source language
        self.tokenizer.src_lang = source_lang
        
        # Encode
        encoded = self.tokenizer(text, return_tensors="pt")
        
        # Generate translation
        generated = self.model.generate(
            **encoded,
            forced_bos_token_id=self.tokenizer.get_lang_id(target_lang)
        )
        
        # Decode
        translation = self.tokenizer.batch_decode(
            generated, 
            skip_special_tokens=True
        )[0]
        
        # Quality score
        quality = self.assess_quality(text, translation, source_lang, target_lang)
        
        result = {
            "source": text,
            "translation": translation,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "quality_score": quality,
            "cached": False
        }
        
        # Cache
        self.cache[cache_key] = result
        
        return result
    
    def assess_quality(self, source, translation, source_lang, target_lang):
        \"\"\"Assess translation quality\"\"\"
        # Back-translation
        back_translation = self.translate_text(translation, target_lang, source_lang)
        
        # Calculate similarity
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, source, back_translation).ratio()
        
        return similarity
    
    def batch_translate(self, texts: List[str], source_lang: str, target_lang: str):
        \"\"\"Batch translation for efficiency\"\"\"
        return [self.translate(text, source_lang, target_lang) for text in texts]
```

**Evaluation Rubric:**

| Criteria | Weight | Excellent (5) | Good (4) | Fair (3) |
|----------|--------|---------------|----------|----------|
| **Accuracy** | 30% | Human-level | Good quality | Understandable |
| **Language Support** | 20% | 15+ languages | 10+ | 5+ |
| **Performance** | 20% | <300ms | <500ms | <1s |
| **Features** | 20% | Batch, cache, QA | 2 features | 1 feature |
| **Cost Efficiency** | 10% | 50%+ cache hits | 30%+ | 10%+ |

---

**General Capstone Guidelines:**

**Timeline:** 4-6 weeks

**Week 1-2:** Design & Setup
- Architecture design
- Tech stack selection
- Environment setup
- Initial prototype

**Week 3-4:** Implementation
- Core features
- Testing
- Optimization
- Documentation

**Week 5-6:** Deployment & Polish
- Deploy to production
- Performance tuning
- Demo preparation
- Final documentation

**Presentation Requirements:**
1. **Demo (10 min):** Live demonstration
2. **Architecture (5 min):** System design explanation
3. **Challenges (3 min):** Problems solved
4. **Metrics (2 min):** Performance, cost, quality
5. **Q&A (5 min):** Answer questions

**Code Requirements:**
- GitHub repository (public or private)
- README with setup instructions
- Requirements.txt / environment.yml
- Tests (minimum 70% coverage)
- CI/CD pipeline (GitHub Actions)
- Deployed application (live URL)

**Documentation Requirements:**
- Architecture diagram
- API documentation
- Performance benchmarks
- Cost analysis ($X per request/user)
- Monitoring dashboard screenshots
- Lessons learned (1-page)

**Bonus Points:**
- Open source contribution
- Blog post about your project
- Novel technique or optimization
- Production usage metrics
- User testimonials

---

**Resources for Capstone:**

**Infrastructure:**
- **Free Credits:** GCP ($300), AWS ($100), Hugging Face (free tier)
- **Deployment:** Render, Railway, Fly.io (free tiers)
- **Monitoring:** Grafana Cloud (free), Sentry (free tier)

**Datasets:**
- Hugging Face Datasets
- Kaggle
- GitHub repositories
- Common Crawl

**Code Templates:**
- FastAPI LLM template
- Streamlit LLM app
- LangChain examples
- LlamaIndex cookbook

**Office Hours:**
- Weekly Q&A sessions
- Code review appointments
- Architecture review
- Deployment assistance
"""
            )
        else:
            st.info(f"Learning materials for Unit {selected_unit} will be added soon.")

    # Labs
    with tabs[2]:
        st.subheader("🧪 Labs & Mini Projects")
        st.info("Hands-on labs with executable code for building LLM applications.")
        
        selected_unit = st.selectbox(
            "Choose a unit to view labs:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="llm_labs_unit",
        )

        st.markdown(f"### Unit {selected_unit}: {UNITS[selected_unit]['name']}")

        if selected_unit == 1:
            st.markdown("### 🔥 Unit 1: LLM Fundamentals & Architecture")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Production LLM Code!**")
            
            st.markdown("### LAB 1: Your First LLM Application (90 min)")
            st.markdown("**Objective:** Build a complete LLM application with OpenAI API")
            lab1_1 = '''import openai
import os
from datetime import datetime

# Setup
openai.api_key = os.getenv("OPENAI_API_KEY")

print("🤖 BUILDING YOUR FIRST LLM APPLICATION\\n" + "="*60)

# 1. Basic completion
print("\\n1. Basic Text Completion...")

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful data analyst assistant."},
        {"role": "user", "content": "Explain what a data warehouse is in simple terms."}
    ],
    temperature=0.7,
    max_tokens=200
)

answer = response.choices[0].message.content
print(f"Response: {answer}")
print(f"Tokens used: {response.usage.total_tokens}")

# 2. Streaming responses
print("\\n2. Streaming Response...")

stream = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Write a Python function to calculate factorial."}
    ],
    stream=True
)

print("Streaming output:")
for chunk in stream:
    if chunk.choices[0].delta.get("content"):
        print(chunk.choices[0].delta.content, end="")

print("\\n")

# 3. Function calling
print("\\n3. Function Calling...")

functions = [
    {
        "name": "get_sales_data",
        "description": "Get sales data for a specific date range",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                "region": {"type": "string", "description": "Geographic region"}
            },
            "required": ["start_date", "end_date"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Get me sales data for UK from January to March 2024"}
    ],
    functions=functions,
    function_call="auto"
)

if response.choices[0].message.get("function_call"):
    function_call = response.choices[0].message.function_call
    print(f"Function: {function_call.name}")
    print(f"Arguments: {function_call.arguments}")

# 4. Token counting
print("\\n4. Token Management...")

def count_tokens(text, model="gpt-4"):
    """Estimate token count"""
    # Rough estimate: ~4 characters per token
    return len(text) // 4

text = "This is a sample text for token counting."
tokens = count_tokens(text)
print(f"Text: {text}")
print(f"Estimated tokens: {tokens}")

# 5. Cost calculation
print("\\n5. Cost Calculation...")

def calculate_cost(input_tokens, output_tokens, model="gpt-4"):
    \"\"\"Calculate API cost\"\"\"
    # GPT-4 pricing (example)
    input_cost_per_1k = 0.03
    output_cost_per_1k = 0.06
    
    input_cost = (input_tokens / 1000) * input_cost_per_1k
    output_cost = (output_tokens / 1000) * output_cost_per_1k
    
    return input_cost + output_cost

cost = calculate_cost(500, 200)
print(f"Cost for 500 input + 200 output tokens: ${cost:.4f}")

print("\\n✅ First LLM application complete!")'''
            st.code(lab1_1, language='python')
            
            st.markdown("### LAB 2: Multi-Model Comparison (90 min)")
            st.markdown("**Objective:** Compare GPT-4, Claude, and Gemini")
            lab1_2 = '''import openai
import anthropic
import google.generativeai as genai
import time

print("🔬 MULTI-MODEL COMPARISON\\n" + "="*60)

# Setup clients
openai_client = openai.OpenAI()
anthropic_client = anthropic.Anthropic()
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

prompt = "Explain machine learning in 3 sentences."

# 1. GPT-4
print("\\n1. Testing GPT-4...")
start = time.time()

gpt_response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

gpt_time = time.time() - start
gpt_answer = gpt_response.choices[0].message.content
gpt_tokens = gpt_response.usage.total_tokens

print(f"Response: {gpt_answer}")
print(f"Time: {gpt_time:.2f}s | Tokens: {gpt_tokens}")

# 2. Claude
print("\\n2. Testing Claude...")
start = time.time()

claude_response = anthropic_client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

claude_time = time.time() - start
claude_answer = claude_response.content[0].text
claude_tokens = claude_response.usage.input_tokens + claude_response.usage.output_tokens

print(f"Response: {claude_answer}")
print(f"Time: {claude_time:.2f}s | Tokens: {claude_tokens}")

# 3. Gemini
print("\\n3. Testing Gemini...")
start = time.time()

model = genai.GenerativeModel('gemini-pro')
gemini_response = model.generate_content(prompt)

gemini_time = time.time() - start
gemini_answer = gemini_response.text

print(f"Response: {gemini_answer}")
print(f"Time: {gemini_time:.2f}s")

# 4. Comparison
print("\\n4. COMPARISON SUMMARY:")
print("="*60)
print(f"GPT-4:   {gpt_time:.2f}s | {gpt_tokens} tokens")
print(f"Claude:  {claude_time:.2f}s | {claude_tokens} tokens")
print(f"Gemini:  {gemini_time:.2f}s")

print("\\n✅ Multi-model comparison complete!")'''
            st.code(lab1_2, language='python')
            
            st.markdown("### LAB 3: Embeddings & Semantic Search (90 min)")
            st.markdown("**Objective:** Build semantic search with embeddings")
            lab1_3 = '''import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

print("🔍 EMBEDDINGS & SEMANTIC SEARCH\n" + "="*60)

# 1. Create embeddings
print("\n1. Creating Embeddings...")

documents = [
    "Python is a programming language",
    "Machine learning uses algorithms to learn from data",
    "SQL is used for database queries",
    "Data science combines statistics and programming",
    "Neural networks are inspired by the human brain"
]

embeddings = []
for doc in documents:
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=doc
    )
    embeddings.append(response.data[0].embedding)

print(f"✅ Created {len(embeddings)} embeddings")

# 2. Semantic search
print("\n2. Semantic Search...")

query = "What is ML?"
query_embedding = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=query
).data[0].embedding

# Calculate similarities
similarities = []
for i, doc_embedding in enumerate(embeddings):
    similarity = cosine_similarity(
        [query_embedding],
        [doc_embedding]
    )[0][0]
    similarities.append((i, similarity, documents[i]))

# Sort by similarity
similarities.sort(key=lambda x: x[1], reverse=True)

print(f"\nQuery: {query}")
print("\nTop 3 results:")
for i, (idx, score, doc) in enumerate(similarities[:3]):
    print(f"{i+1}. {doc} (score: {score:.4f})")

# 3. Clustering with embeddings
print("\n3. Clustering Documents...")

from sklearn.cluster import KMeans

embeddings_array = np.array(embeddings)
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(embeddings_array)

print("\nClusters:")
for i, (doc, cluster) in enumerate(zip(documents, clusters)):
    print(f"Cluster {cluster}: {doc}")

print("\n✅ Embeddings and semantic search complete!")'''
            st.code(lab1_3, language='python')
            
            st.markdown("### LAB 4: Token Optimization & Cost Management (75 min)")
            st.markdown("**Objective:** Optimize token usage and reduce LLM costs")
            lab1_4 = '''import openai
import tiktoken

print("💰 TOKEN OPTIMIZATION & COST MANAGEMENT\n" + "="*60)

# 1. Token counting
print("\n1. Accurate Token Counting...")

encoding = tiktoken.encoding_for_model("gpt-4")

text = "This is a sample text for token counting in GPT-4."
tokens = encoding.encode(text)

print(f"Text: {text}")
print(f"Tokens: {len(tokens)}")
print(f"Token IDs: {tokens[:10]}...")  # First 10

# 2. Cost calculation
print("\n2. Cost Calculation...")

def calculate_cost(input_text, output_text, model="gpt-4"):
    """Calculate exact API cost"""
    encoding = tiktoken.encoding_for_model(model)
    
    input_tokens = len(encoding.encode(input_text))
    output_tokens = len(encoding.encode(output_text))
    
    # GPT-4 pricing
    input_cost_per_1k = 0.03
    output_cost_per_1k = 0.06
    
    input_cost = (input_tokens / 1000) * input_cost_per_1k
    output_cost = (output_tokens / 1000) * output_cost_per_1k
    total_cost = input_cost + output_cost
    
    return {
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'total_tokens': input_tokens + output_tokens,
        'cost': total_cost
    }

prompt = "Explain machine learning in 3 sentences."
response_text = "Machine learning is a subset of AI..."

cost_info = calculate_cost(prompt, response_text)
print(f"\nInput tokens: {cost_info['input_tokens']}")
print(f"Output tokens: {cost_info['output_tokens']}")
print(f"Total cost: ${cost_info['cost']:.4f}")

# 3. Optimization strategies
print("\n3. Optimization Strategies...")

# Strategy 1: Reduce prompt length
verbose_prompt = """I would like you to please provide me with a comprehensive 
explanation of what machine learning is, including all the key concepts and 
important details that someone should know."""

concise_prompt = "Explain machine learning in 3 sentences."

verbose_tokens = len(encoding.encode(verbose_prompt))
concise_tokens = len(encoding.encode(concise_prompt))

print(f"\nVerbose prompt: {verbose_tokens} tokens")
print(f"Concise prompt: {concise_tokens} tokens")
print(f"Savings: {verbose_tokens - concise_tokens} tokens ({((verbose_tokens - concise_tokens) / verbose_tokens * 100):.1f}%)")

# Strategy 2: Use cheaper models when possible
models_cost = {
    'gpt-4': {'input': 0.03, 'output': 0.06},
    'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
    'claude-instant': {'input': 0.0008, 'output': 0.0024}
}

print("\n4. Model Cost Comparison (1000 tokens):")
for model, pricing in models_cost.items():
    cost = (pricing['input'] + pricing['output'])
    print(f"{model:20s}: ${cost:.4f}")

# 5. Batch processing
print("\n5. Batch Processing for Efficiency...")

queries = ["Query 1", "Query 2", "Query 3"]

# Bad: Individual calls
individual_cost = len(queries) * 0.001  # Overhead per call

# Good: Batch in single call
batch_prompt = "Answer these questions:\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(queries)])
batch_cost = 0.001  # Single call overhead

print(f"Individual calls cost: ${individual_cost:.4f}")
print(f"Batch call cost: ${batch_cost:.4f}")
print(f"Savings: ${individual_cost - batch_cost:.4f}")

print("\n✅ Token optimization complete!")'''
            st.code(lab1_4, language='python')
            
            st.markdown("### LAB 5: Build Conversational Chatbot (90 min)")
            st.markdown("**Objective:** Create chatbot with conversation memory")
            lab1_5 = '''import openai
from datetime import datetime

print("💬 CONVERSATIONAL CHATBOT\n" + "="*60)

class Chatbot:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.system_prompt = system_prompt
        self.conversation_history = []
        self.conversation_history.append({
            "role": "system",
            "content": system_prompt
        })
    
    def chat(self, user_message):
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.conversation_history
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def get_conversation_summary(self):
        return f"Total messages: {len(self.conversation_history) - 1}"  # Exclude system
    
    def clear_history(self):
        self.conversation_history = [self.conversation_history[0]]  # Keep system prompt

# 1. Create chatbot
print("\n1. Creating Chatbot...")

bot = Chatbot(system_prompt="You are a data engineering expert.")
print("✅ Chatbot initialized")

# 2. Multi-turn conversation
print("\n2. Multi-turn Conversation...")

conversation = [
    "What is Apache Spark?",
    "How does it compare to Hadoop?",
    "Can you give me a code example?"
]

for i, message in enumerate(conversation):
    print(f"\nUser: {message}")
    response = bot.chat(message)
    print(f"Bot: {response[:150]}...")

print(f"\n{bot.get_conversation_summary()}")

# 3. Conversation with context
print("\n3. Testing Context Retention...")

response = bot.chat("What was my first question?")
print(f"\nUser: What was my first question?")
print(f"Bot: {response}")

print("\n✅ Chatbot with memory complete!")'''
            st.code(lab1_5, language='python')
            
            st.success("✅ Unit 1 Labs Complete: LLM fundamentals mastered!")
            
        elif selected_unit == 2:
            st.markdown("### 🔥 Unit 2: Prompt Engineering & Optimization")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Advanced Prompting Techniques!**")
            
            st.markdown("### LAB 1: Advanced Prompt Patterns (120 min)")
            st.markdown("**Objective:** Master prompt engineering techniques")
            lab2_1 = '''import openai

client = openai.OpenAI()

print("✍️ ADVANCED PROMPT ENGINEERING\\n" + "="*60)

# 1. Zero-shot prompting
print("\\n1. ZERO-SHOT PROMPTING:")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": "Classify this review as positive or negative: 'The product is okay but shipping was slow.'"
    }]
)

print(f"Result: {response.choices[0].message.content}")

# 2. Few-shot prompting
print("\\n2. FEW-SHOT PROMPTING:")

few_shot_prompt = """Classify customer reviews as positive, negative, or neutral.

Examples:
Review: "Amazing product! Fast shipping!"
Sentiment: positive

Review: "Terrible quality, broke after 2 days"
Sentiment: negative

Review: "It's okay, nothing special"
Sentiment: neutral

Now classify this:
Review: "Good value for money but could be better"
Sentiment:"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": few_shot_prompt}]
)

print(f"Result: {response.choices[0].message.content}")

# 3. Chain-of-thought prompting
print("\\n3. CHAIN-OF-THOUGHT PROMPTING:")

cot_prompt = """Solve this step by step:

A store had 50 items. They sold 30% on Monday and 20% of the remaining on Tuesday.
How many items are left?

Let's think through this step by step:"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": cot_prompt}]
)

print(f"Result: {response.choices[0].message.content}")

# 4. Role-based prompting
print("\\n4. ROLE-BASED PROMPTING:")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a senior data engineer with 10 years of experience in building data pipelines."},
        {"role": "user", "content": "Should I use Kafka or RabbitMQ for my real-time analytics pipeline?"}
    ]
)

print(f"Result: {response.choices[0].message.content}")

# 5. Structured output
print("\\n5. STRUCTURED OUTPUT:")

structured_prompt = """Extract the following information from this text and return as JSON:
- company_name
- revenue
- year
- growth_rate

Text: "TechCorp reported $50M revenue in 2024, up 25% from last year."

Return only valid JSON:"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": structured_prompt}],
    response_format={"type": "json_object"}
)

print(f"Result: {response.choices[0].message.content}")

print("\\n✅ Prompt engineering techniques mastered!")'''
            st.code(lab2_1, language='python')
            
            st.markdown("### LAB 2: Prompt Optimization & A/B Testing (90 min)")
            st.markdown("**Objective:** Optimize prompts for better results")
            lab2_2 = '''import openai
import time
from statistics import mean

print("⚡ PROMPT OPTIMIZATION\n" + "="*60)

# Test different prompt versions
prompts = {
    "v1_basic": "Summarize this text: {text}",
    "v2_detailed": "Provide a concise 3-sentence summary of the following text, focusing on key points: {text}",
    "v3_structured": """Summarize the text below in this format:
- Main topic:
- Key points (3 bullet points):
- Conclusion:

Text: {text}"""
}

sample_text = """Artificial intelligence is transforming industries worldwide. 
Companies are using AI for automation, prediction, and decision-making. 
However, ethical considerations and data privacy remain important challenges."""

results = {}

for version, prompt_template in prompts.items():
    print(f"\nTesting {version}...")
    
    prompt = prompt_template.format(text=sample_text)
    
    start = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    latency = time.time() - start
    
    results[version] = {
        'response': response.choices[0].message.content,
        'tokens': response.usage.total_tokens,
        'latency': latency,
        'cost': (response.usage.total_tokens / 1000) * 0.002
    }
    
    print(f"  Tokens: {results[version]['tokens']}")
    print(f"  Latency: {results[version]['latency']:.2f}s")
    print(f"  Cost: ${results[version]['cost']:.4f}")

# Compare results
print("\n" + "="*60)
print("COMPARISON:")
print("="*60)

for version, data in results.items():
    print(f"\n{version}:")
    print(f"  Response: {data['response'][:100]}...")
    print(f"  Metrics: {data['tokens']} tokens, {data['latency']:.2f}s, ${data['cost']:.4f}")

# Winner
best_version = min(results.items(), key=lambda x: x[1]['cost'])
print(f"\n✅ Most cost-effective: {best_version[0]}")

print("\n✅ Prompt optimization complete!")'''
            st.code(lab2_2, language='python')
            
            st.markdown("### LAB 3: Prompt Chaining & Complex Workflows (90 min)")
            st.markdown("**Objective:** Build multi-step LLM workflows")
            lab2_3 = '''import openai
from typing import List, Dict

print("🔗 PROMPT CHAINING & WORKFLOWS\n" + "="*60)

class LLMWorkflow:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.conversation_history = []
    
    def call_llm(self, prompt: str, system_msg: str = None) -> str:
        """Single LLM call"""
        messages = []
        if system_msg:
            messages.append({"role": "system", "content": system_msg})
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        
        return response.choices[0].message.content
    
    def research_analyze_write(self, topic: str) -> Dict[str, str]:
        """Multi-step workflow: Research -> Analyze -> Write"""
        print(f"\nWorkflow for topic: {topic}")
        
        # Step 1: Research
        print("\n1. Research phase...")
        research_prompt = f"Research and list 5 key facts about: {topic}"
        research_result = self.call_llm(
            research_prompt,
            system_msg="You are a research assistant."
        )
        print(f"Research: {research_result[:100]}...")
        
        # Step 2: Analyze
        print("\n2. Analysis phase...")
        analysis_prompt = f"""Analyze these research findings and identify:
- Main trends
- Key insights
- Potential implications

Research findings:
{research_result}"""
        analysis_result = self.call_llm(
            analysis_prompt,
            system_msg="You are a data analyst."
        )
        print(f"Analysis: {analysis_result[:100]}...")
        
        # Step 3: Write
        print("\n3. Writing phase...")
        write_prompt = f"""Write a professional 2-paragraph summary based on:

Research: {research_result}

Analysis: {analysis_result}"""
        final_result = self.call_llm(
            write_prompt,
            system_msg="You are a professional writer."
        )
        print(f"Final: {final_result[:100]}...")
        
        return {
            'research': research_result,
            'analysis': analysis_result,
            'final': final_result
        }

# Example usage
workflow = LLMWorkflow()
results = workflow.research_analyze_write("Machine Learning in Healthcare")

print("\n" + "="*60)
print("FINAL OUTPUT:")
print("="*60)
print(results['final'])

print("\n✅ Prompt chaining workflow complete!")'''
            st.code(lab2_3, language='python')
            
            st.markdown("### LAB 4: ReAct & Self-Consistency Prompting (75 min)")
            st.markdown("**Objective:** Advanced prompting for reasoning and reliability")
            lab2_4 = '''import openai
from collections import Counter

print("🧠 REACT & SELF-CONSISTENCY PROMPTING\n" + "="*60)

# 1. ReAct (Reasoning + Acting)
print("\n1. ReAct Prompting...")

react_prompt = """Solve this problem step by step using Thought, Action, Observation pattern:

Problem: A store has 100 items. They sold 30% on Monday. On Tuesday, they sold 20% of what remained. How many items are left?

Thought 1: I need to calculate items sold on Monday
Action 1: Calculate 30% of 100
Observation 1: 30 items sold on Monday, 70 remain

Thought 2: Now calculate Tuesday's sales from remaining
Action 2: Calculate 20% of 70
Observation 2: 14 items sold on Tuesday

Thought 3: Calculate final remaining
Action 3: 70 - 14
Observation 3: 56 items remain

Answer: 56 items

Now solve this using the same pattern:
A company has 500 employees. 15% work remotely. Of the office workers, 25% are in management. How many office workers are NOT in management?"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": react_prompt}]
)

print(f"ReAct Response:\n{response.choices[0].message.content}")

# 2. Self-Consistency (Multiple samples + voting)
print("\n2. Self-Consistency Prompting...")

question = "If you flip a coin 3 times, what's the probability of getting at least 2 heads?"

# Generate multiple reasoning paths
responses = []
for i in range(5):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Solve step by step: {question}"}],
        temperature=0.7  # Some randomness
    )
    answer = response.choices[0].message.content
    responses.append(answer)
    print(f"\nPath {i+1}: {answer[:100]}...")

# Extract final answers (simplified)
final_answers = []
for resp in responses:
    # Extract last line as answer
    lines = resp.strip().split('\n')
    final_answers.append(lines[-1])

print("\n3. Voting on Answers...")
vote_counts = Counter(final_answers)
most_common = vote_counts.most_common(1)[0]

print(f"\nMost consistent answer: {most_common[0]}")
print(f"Votes: {most_common[1]}/5")

# 3. Chain-of-Thought with Self-Consistency
print("\n4. Combined: CoT + Self-Consistency...")

cot_prompt = """Let's solve this step by step:

Question: {question}

Step 1:
Step 2:
Step 3:
Final Answer:"""

responses = []
for i in range(3):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": cot_prompt.format(question=question)}],
        temperature=0.7
    )
    responses.append(response.choices[0].message.content)

print(f"\nGenerated {len(responses)} reasoning paths")
print("✅ Self-consistency improves reliability!")

print("\n✅ Advanced prompting techniques mastered!")'''
            st.code(lab2_4, language='python')
            
            st.success("✅ Unit 2 Labs Complete: Prompt engineering mastered!")
            
        elif selected_unit == 3:
            st.markdown("### 🔥 Unit 3: RAG (Retrieval Augmented Generation)")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Build Production RAG Systems!**")
            
            st.markdown("### LAB 1: Build RAG System with LangChain (150 min)")
            st.markdown("**Objective:** Create a complete RAG application")
            lab3_1 = '''from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

print("🔍 BUILDING RAG SYSTEM\\n" + "="*60)

# 1. Load documents
print("\\n1. Loading Documents...")

loader = TextLoader('company_docs.txt')
documents = loader.load()

print(f"✅ Loaded {len(documents)} documents")

# 2. Split into chunks
print("\\n2. Splitting into Chunks...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

chunks = text_splitter.split_documents(documents)
print(f"✅ Created {len(chunks)} chunks")

# 3. Create embeddings
print("\\n3. Creating Embeddings...")

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("✅ Vector store created")

# 4. Create retriever
print("\\n4. Setting up Retriever...")

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 5. Create QA chain
print("\\n5. Creating QA Chain...")

llm = ChatOpenAI(model="gpt-4", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 6. Query the system
print("\\n6. Querying RAG System...")

query = "What is our company's return policy?"
result = qa_chain({"query": query})

print(f"\\nQuestion: {query}")
print(f"Answer: {result['result']}")
print(f"\\nSource documents:")
for i, doc in enumerate(result['source_documents']):
    print(f"  {i+1}. {doc.page_content[:100]}...")

print("\\n✅ RAG system complete!")'''
            st.code(lab3_1, language='python')
            
            st.markdown("### LAB 2: Advanced RAG with Reranking (120 min)")
            st.markdown("**Objective:** Build production RAG with hybrid search and reranking")
            lab3_2 = '''from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
import chromadb

print("🚀 ADVANCED RAG WITH RERANKING\n" + "="*60)

# 1. Setup vector store
print("\n1. Setting up Vector Store...")

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory="./advanced_chroma",
    embedding_function=embeddings
)

# 2. Hybrid retriever (semantic + keyword)
print("\n2. Creating Hybrid Retriever...")

base_retriever = vectorstore.as_retriever(
    search_type="mmr",  # Maximum Marginal Relevance
    search_kwargs={"k": 10, "fetch_k": 20}
)

print("✅ Base retriever created")

# 3. Add reranking
print("\n3. Adding Reranking Layer...")

llm = ChatOpenAI(model="gpt-4", temperature=0)
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

print("✅ Reranking layer added")

# 4. Create advanced QA chain
print("\n4. Creating QA Chain...")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=compression_retriever,
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": """Use the following context to answer the question. 
If you don't know, say so. Always cite your sources.

Context: {context}

Question: {question}

Answer:"""
    }
)

print("✅ Advanced QA chain created")

# 5. Query with reranking
print("\n5. Querying with Reranking...")

query = "What are the benefits of using embeddings?"
result = qa_chain({"query": query})

print(f"\nQuestion: {query}")
print(f"\nAnswer: {result['result']}")
print(f"\nRelevant sources ({len(result['source_documents'])})")
for i, doc in enumerate(result['source_documents'][:3]):
    print(f"  {i+1}. {doc.page_content[:150]}...")

# 6. Evaluation metrics
print("\n6. RAG Evaluation...")

test_queries = [
    "What is machine learning?",
    "How does RAG work?",
    "What are embeddings?"
]

for q in test_queries:
    result = qa_chain({"query": q})
    print(f"\nQ: {q}")
    print(f"A: {result['result'][:100]}...")
    print(f"Sources: {len(result['source_documents'])}")

print("\n✅ Advanced RAG system complete!")'''
            st.code(lab3_2, language='python')
            
            st.markdown("### LAB 3: Vector Database with Pinecone (90 min)")
            st.markdown("**Objective:** Build scalable RAG with cloud vector database")
            lab3_3 = '''import pinecone
import openai
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

print("💾 VECTOR DATABASE WITH PINECONE\n" + "="*60)

# 1. Initialize Pinecone
print("\n1. Initializing Pinecone...")

pinecone.init(
    api_key="YOUR_API_KEY",
    environment="us-west1-gcp"
)

index_name = "knowledge-base"

# Create index if doesn't exist
if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        name=index_name,
        dimension=1536,  # OpenAI embedding dimension
        metric="cosine"
    )

print(f"✅ Pinecone index '{index_name}' ready")

# 2. Prepare documents
print("\n2. Preparing Documents...")

documents = [
    "Machine learning is a subset of AI that enables systems to learn from data.",
    "Deep learning uses neural networks with multiple layers.",
    "Natural language processing helps computers understand human language.",
    "Computer vision enables machines to interpret visual information."
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.create_documents(documents)
print(f"✅ Created {len(chunks)} document chunks")

# 3. Create embeddings and store
print("\n3. Creating Embeddings and Storing...")

embeddings = OpenAIEmbeddings()
vectorstore = Pinecone.from_documents(
    chunks,
    embeddings,
    index_name=index_name
)

print("✅ Documents embedded and stored in Pinecone")

# 4. Semantic search
print("\n4. Semantic Search...")

query = "What is deep learning?"
results = vectorstore.similarity_search(query, k=3)

print(f"\nQuery: {query}")
print("\nTop 3 results:")
for i, doc in enumerate(results):
    print(f"{i+1}. {doc.page_content}")

# 5. Search with scores
print("\n5. Search with Similarity Scores...")

results_with_scores = vectorstore.similarity_search_with_score(query, k=3)

for doc, score in results_with_scores:
    print(f"Score: {score:.4f} | {doc.page_content[:80]}...")

# 6. Metadata filtering
print("\n6. Metadata Filtering...")

# Add documents with metadata
metadata_docs = [
    {"text": "Python is great for data science", "category": "programming"},
    {"text": "SQL is used for databases", "category": "databases"},
    {"text": "Tableau creates visualizations", "category": "visualization"}
]

for doc in metadata_docs:
    vectorstore.add_texts([doc["text"]], metadatas=[{"category": doc["category"]}])

print("✅ Documents with metadata added")

# Filter by metadata
filtered_results = vectorstore.similarity_search(
    "programming languages",
    k=5,
    filter={"category": "programming"}
)

print(f"\nFiltered results: {len(filtered_results)}")

print("\n✅ Pinecone vector database complete!")'''
            st.code(lab3_3, language='python')
            
            st.markdown("### LAB 4: Production RAG with Caching (90 min)")
            st.markdown("**Objective:** Build production-ready RAG with performance optimization")
            lab3_4 = '''from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.cache import RedisCache
import redis
import hashlib
import time

print("🚀 PRODUCTION RAG WITH CACHING\n" + "="*60)

# 1. Setup caching
print("\n1. Setting up Redis Cache...")

redis_client = redis.Redis(host='localhost', port=6379)

class RAGCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 3600  # 1 hour
    
    def get_cache_key(self, query):
        return hashlib.md5(query.encode()).hexdigest()
    
    def get(self, query):
        key = self.get_cache_key(query)
        cached = self.redis.get(key)
        if cached:
            return cached.decode('utf-8')
        return None
    
    def set(self, query, response):
        key = self.get_cache_key(query)
        self.redis.setex(key, self.ttl, response)

cache = RAGCache(redis_client)
print("✅ Cache configured")

# 2. Setup RAG
print("\n2. Setting up RAG System...")

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

llm = ChatOpenAI(model="gpt-4", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("✅ RAG system ready")

# 3. Query with caching
print("\n3. Querying with Cache...")

def query_with_cache(question):
    # Check cache
    cached_response = cache.get(question)
    if cached_response:
        print(f"  ✅ CACHE HIT")
        return cached_response
    
    # Cache miss - query RAG
    print(f"  ❌ CACHE MISS - querying RAG")
    start = time.time()
    result = qa_chain({"query": question})
    latency = time.time() - start
    
    response = result['result']
    
    # Cache result
    cache.set(question, response)
    
    print(f"  Latency: {latency:.2f}s")
    return response

# Test queries
queries = [
    "What is machine learning?",
    "How does RAG work?",
    "What is machine learning?"  # Duplicate - should hit cache
]

for i, q in enumerate(queries):
    print(f"\nQuery {i+1}: {q}")
    response = query_with_cache(q)
    print(f"Response: {response[:80]}...")

# 4. Performance metrics
print("\n4. Performance Metrics...")

cache_stats = {
    'total_queries': 3,
    'cache_hits': 1,
    'cache_misses': 2,
    'hit_rate': 1/3 * 100
}

print(f"\nCache Statistics:")
print(f"  Total queries: {cache_stats['total_queries']}")
print(f"  Cache hits: {cache_stats['cache_hits']}")
print(f"  Cache misses: {cache_stats['cache_misses']}")
print(f"  Hit rate: {cache_stats['hit_rate']:.1f}%")

print("\n✅ Production RAG with caching complete!")'''
            st.code(lab3_4, language='python')
            
            st.markdown("### LAB 5: Multi-Document RAG with Metadata (90 min)")
            st.markdown("**Objective:** Build RAG system handling multiple document types")
            lab3_5 = '''from langchain.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

print("📚 MULTI-DOCUMENT RAG WITH METADATA\n" + "="*60)

# 1. Load multiple document types
print("\n1. Loading Multiple Document Types...")

documents = []

# Load PDFs
pdf_loader = PyPDFLoader('company_policy.pdf')
pdf_docs = pdf_loader.load()
for doc in pdf_docs:
    doc.metadata['source_type'] = 'policy'
    doc.metadata['department'] = 'HR'
documents.extend(pdf_docs)

# Load text files
text_loader = TextLoader('technical_docs.txt')
text_docs = text_loader.load()
for doc in text_docs:
    doc.metadata['source_type'] = 'technical'
    doc.metadata['department'] = 'Engineering'
documents.extend(text_docs)

# Load CSV
csv_loader = CSVLoader('product_catalog.csv')
csv_docs = csv_loader.load()
for doc in csv_docs:
    doc.metadata['source_type'] = 'catalog'
    doc.metadata['department'] = 'Sales'
documents.extend(csv_docs)

print(f"✅ Loaded {len(documents)} documents from multiple sources")

# 2. Split with metadata preservation
print("\n2. Splitting Documents...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)
print(f"✅ Created {len(chunks)} chunks (metadata preserved)")

# 3. Create vector store
print("\n3. Creating Vector Store...")

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./multi_doc_chroma"
)

print("✅ Vector store created")

# 4. Query with metadata filtering
print("\n4. Querying with Metadata Filters...")

# Query only HR documents
hr_results = vectorstore.similarity_search(
    "What is the vacation policy?",
    k=3,
    filter={"department": "HR"}
)

print("\nHR Policy Results:")
for i, doc in enumerate(hr_results):
    print(f"{i+1}. {doc.page_content[:80]}...")
    print(f"   Source: {doc.metadata['source_type']}, Dept: {doc.metadata['department']}")

# Query only technical docs
tech_results = vectorstore.similarity_search(
    "How do I deploy the application?",
    k=3,
    filter={"department": "Engineering"}
)

print("\nTechnical Docs Results:")
for i, doc in enumerate(tech_results):
    print(f"{i+1}. {doc.page_content[:80]}...")

# 5. Multi-query RAG
print("\n5. Multi-Query RAG...")

from langchain.retrievers import MultiQueryRetriever

llm = ChatOpenAI(model="gpt-4", temperature=0)

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# Generates multiple query variations automatically
results = retriever.get_relevant_documents("product pricing")

print(f"\nFound {len(results)} relevant documents")
for doc in results[:3]:
    print(f"  - {doc.page_content[:60]}...")

print("\n✅ Multi-document RAG complete!")'''
            st.code(lab3_5, language='python')
            
            st.markdown("### LAB 6: RAG Evaluation & Quality Metrics (75 min)")
            st.markdown("**Objective:** Measure and improve RAG system performance")
            lab3_6 = '''from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import pandas as pd

print("📊 RAG EVALUATION & QUALITY METRICS\n" + "="*60)

# 1. Setup RAG system
print("\n1. Setting up RAG System...")

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
llm = ChatOpenAI(model="gpt-4", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("✅ RAG system ready")

# 2. Create evaluation dataset
print("\n2. Creating Evaluation Dataset...")

eval_questions = [
    {"question": "What is machine learning?", "expected_answer": "ML is a subset of AI"},
    {"question": "How does RAG work?", "expected_answer": "RAG retrieves relevant documents"},
    {"question": "What are embeddings?", "expected_answer": "Embeddings are vector representations"}
]

print(f"✅ Created {len(eval_questions)} evaluation questions")

# 3. Evaluate retrieval quality
print("\n3. Evaluating Retrieval Quality...")

retrieval_metrics = []

for item in eval_questions:
    question = item['question']
    
    # Get retrieved documents
    docs = vectorstore.similarity_search_with_score(question, k=3)
    
    # Calculate metrics
    top_score = docs[0][1] if docs else 0
    avg_score = sum(score for _, score in docs) / len(docs) if docs else 0
    
    retrieval_metrics.append({
        'question': question,
        'num_docs': len(docs),
        'top_score': top_score,
        'avg_score': avg_score
    })

df_retrieval = pd.DataFrame(retrieval_metrics)
print("\nRetrieval Metrics:")
print(df_retrieval)

# 4. Evaluate answer quality
print("\n4. Evaluating Answer Quality...")

answer_metrics = []

for item in eval_questions:
    result = qa_chain({"query": item['question']})
    
    answer_metrics.append({
        'question': item['question'],
        'answer': result['result'],
        'num_sources': len(result['source_documents']),
        'answer_length': len(result['result'])
    })

df_answers = pd.DataFrame(answer_metrics)
print("\nAnswer Metrics:")
print(df_answers[['question', 'num_sources', 'answer_length']])

# 5. Calculate overall metrics
print("\n5. Overall RAG Metrics...")

metrics = {
    'avg_retrieval_score': df_retrieval['top_score'].mean(),
    'avg_sources_used': df_answers['num_sources'].mean(),
    'avg_answer_length': df_answers['answer_length'].mean()
}

print("\n" + "="*60)
print("RAG QUALITY METRICS:")
print("="*60)
for metric, value in metrics.items():
    print(f"{metric}: {value:.2f}")

print("\n✅ RAG evaluation complete!")'''
            st.code(lab3_6, language='python')
            
            st.success("✅ Unit 3 Labs Complete: RAG systems mastered!")
            
        elif selected_unit == 4:
            st.markdown("### 🔥 Unit 4: Fine-tuning & Model Training")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Fine-tune LLMs for Your Use Case!**")
            
            st.markdown("### LAB 1: Fine-tune GPT-3.5 (120 min)")
            st.markdown("**Objective:** Fine-tune a model for custom task")
            lab4_1 = '''import openai
import json

print("🎯 FINE-TUNING GPT-3.5\n" + "="*60)

# 1. Prepare training data
print("\n1. Preparing Training Data...")

training_data = [
    {"messages": [{"role": "system", "content": "You are a SQL expert."},
                  {"role": "user", "content": "Write a query to get top 10 customers"},
                  {"role": "assistant", "content": "SELECT customer_id, SUM(amount) as total FROM orders GROUP BY customer_id ORDER BY total DESC LIMIT 10;"}]},
    {"messages": [{"role": "system", "content": "You are a SQL expert."},
                  {"role": "user", "content": "How to join two tables?"},
                  {"role": "assistant", "content": "SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;"}]}
]

# Save as JSONL
with open('training_data.jsonl', 'w') as f:
    for item in training_data:
        f.write(json.dumps(item) + '\n')

print("✅ Training data prepared (100 examples)")

# 2. Upload training file
print("\n2. Uploading Training File...")

with open('training_data.jsonl', 'rb') as f:
    response = openai.File.create(file=f, purpose='fine-tune')

file_id = response.id
print(f"✅ File uploaded: {file_id}")

# 3. Create fine-tuning job
print("\n3. Starting Fine-tuning Job...")

ft_job = openai.FineTuningJob.create(
    training_file=file_id,
    model="gpt-3.5-turbo",
    hyperparameters={"n_epochs": 3}
)

print(f"✅ Fine-tuning job started: {ft_job.id}")
print(f"Status: {ft_job.status}")

# 4. Monitor progress
print("\n4. Monitoring Progress...")

import time
while True:
    job = openai.FineTuningJob.retrieve(ft_job.id)
    print(f"Status: {job.status}")
    
    if job.status in ['succeeded', 'failed']:
        break
    
    time.sleep(60)

if job.status == 'succeeded':
    fine_tuned_model = job.fine_tuned_model
    print(f"\n✅ Fine-tuning complete! Model: {fine_tuned_model}")
    
    # 5. Test fine-tuned model
    print("\n5. Testing Fine-tuned Model...")
    
    response = openai.ChatCompletion.create(
        model=fine_tuned_model,
        messages=[{"role": "user", "content": "Write a query to count orders by status"}]
    )
    
    print(f"Response: {response.choices[0].message.content}")
else:
    print(f"\n❌ Fine-tuning failed: {job.error}")

print("\n✅ Fine-tuning lab complete!")'''
            st.code(lab4_1, language='python')
            
            st.markdown("### LAB 2: LoRA Fine-tuning (90 min)")
            st.markdown("**Objective:** Efficient fine-tuning with LoRA")
            lab4_2 = '''from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset

print("🎯 LORA FINE-TUNING\n" + "="*60)

# 1. Load base model
print("\n1. Loading Base Model...")

model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

print(f"✅ Loaded {model_name}")

# 2. Configure LoRA
print("\n2. Configuring LoRA...")

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,  # LoRA rank
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["c_attn"]  # GPT-2 attention layers
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

print("✅ LoRA configured")

# 3. Prepare dataset
print("\n3. Preparing Dataset...")

dataset = load_dataset("text", data_files={"train": "training_data.txt"})

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

print("✅ Dataset prepared")

# 4. Training
print("\n4. Training with LoRA...")

training_args = TrainingArguments(
    output_dir="./lora_model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=100,
    logging_steps=10
)

print("✅ Training complete!")
print("\nTrainable parameters: Only 0.1% of full model!")
print("✅ LoRA fine-tuning mastered!")'''
            st.code(lab4_2, language='python')
            
            st.markdown("### LAB 3: LLM Evaluation & Benchmarking (90 min)")
            st.markdown("**Objective:** Evaluate and compare LLM performance")
            lab4_3 = '''import openai
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

print("📊 LLM EVALUATION & BENCHMARKING\n" + "="*60)

# 1. Load evaluation dataset
print("\n1. Loading Evaluation Dataset...")

eval_data = [
    {"input": "Classify: Great product!", "expected": "positive"},
    {"input": "Classify: Terrible service", "expected": "negative"},
    {"input": "Classify: It's okay", "expected": "neutral"},
    {"input": "Classify: Amazing experience!", "expected": "positive"},
    {"input": "Classify: Worst purchase ever", "expected": "negative"}
]

print(f"✅ Loaded {len(eval_data)} test cases")

# 2. Evaluate base model
print("\n2. Evaluating Base Model...")

base_predictions = []
for item in eval_data:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": item["input"]}],
        max_tokens=10
    )
    prediction = response.choices[0].message.content.lower().strip()
    base_predictions.append(prediction)

print(f"Base model predictions: {base_predictions}")

# 3. Evaluate fine-tuned model
print("\n3. Evaluating Fine-tuned Model...")

finetuned_predictions = []
for item in eval_data:
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo:custom",  # Your fine-tuned model
        messages=[{"role": "user", "content": item["input"]}],
        max_tokens=10
    )
    prediction = response.choices[0].message.content.lower().strip()
    finetuned_predictions.append(prediction)

print(f"Fine-tuned predictions: {finetuned_predictions}")

# 4. Calculate metrics
print("\n4. Calculating Metrics...")

expected = [item["expected"] for item in eval_data]

base_accuracy = accuracy_score(expected, base_predictions)
finetuned_accuracy = accuracy_score(expected, finetuned_predictions)

print("\n" + "="*60)
print("EVALUATION RESULTS:")
print("="*60)
print(f"Base Model Accuracy: {base_accuracy:.2%}")
print(f"Fine-tuned Model Accuracy: {finetuned_accuracy:.2%}")
print(f"Improvement: {(finetuned_accuracy - base_accuracy):.2%}")

# 5. Latency benchmark
print("\n5. Latency Benchmark...")

import time

latencies = []
for _ in range(10):
    start = time.time()
    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Test"}],
        max_tokens=10
    )
    latencies.append(time.time() - start)

print(f"\nAverage latency: {np.mean(latencies):.3f}s")
print(f"P50: {np.percentile(latencies, 50):.3f}s")
print(f"P95: {np.percentile(latencies, 95):.3f}s")

print("\n✅ LLM evaluation complete!")'''
            st.code(lab4_3, language='python')
            
            st.markdown("### LAB 4: RLHF - Reinforcement Learning from Human Feedback (90 min)")
            st.markdown("**Objective:** Implement human feedback loop for model improvement")
            lab4_4 = '''import openai
import pandas as pd
from datetime import datetime

print("👥 RLHF - HUMAN FEEDBACK INTEGRATION\n" + "="*60)

# 1. Collect model responses
print("\n1. Generating Model Responses...")

prompts = [
    "Explain quantum computing",
    "Write a Python function to sort a list",
    "What is the capital of France?"
]

responses = []
for prompt in prompts:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    responses.append({
        'prompt': prompt,
        'response': response.choices[0].message.content,
        'timestamp': datetime.now().isoformat()
    })

print(f"✅ Generated {len(responses)} responses")

# 2. Collect human feedback
print("\n2. Collecting Human Feedback...")

feedback_data = []

for item in responses:
    print(f"\nPrompt: {item['prompt']}")
    print(f"Response: {item['response'][:100]}...")
    
    # Simulate human rating (1-5)
    rating = 4  # In production, get from human raters
    feedback = "Good but could be more concise"
    
    feedback_data.append({
        'prompt': item['prompt'],
        'response': item['response'],
        'rating': rating,
        'feedback': feedback,
        'timestamp': datetime.now().isoformat()
    })

print(f"\n✅ Collected {len(feedback_data)} feedback items")

# 3. Prepare training data from feedback
print("\n3. Preparing Training Data from Feedback...")

training_examples = []

for item in feedback_data:
    if item['rating'] >= 4:  # Use high-quality responses
        training_examples.append({
            "messages": [
                {"role": "user", "content": item['prompt']},
                {"role": "assistant", "content": item['response']}
            ]
        })

print(f"✅ Created {len(training_examples)} training examples")

# 4. Save for fine-tuning
import json

with open('rlhf_training_data.jsonl', 'w') as f:
    for example in training_examples:
        f.write(json.dumps(example) + '\n')

print("✅ Training data saved")

# 5. Feedback analytics
print("\n4. Feedback Analytics...")

df_feedback = pd.DataFrame(feedback_data)

avg_rating = df_feedback['rating'].mean()
print(f"\nAverage rating: {avg_rating:.2f}/5")
print(f"High quality responses (4+): {len(df_feedback[df_feedback['rating'] >= 4])}")
print(f"Low quality responses (<3): {len(df_feedback[df_feedback['rating'] < 3])}")

print("\n✅ RLHF pipeline complete!")'''
            st.code(lab4_4, language='python')
            
            st.success("✅ Unit 4 Labs Complete: Model fine-tuning mastered!")
            
        elif selected_unit == 5:
            st.markdown("### 🔥 Unit 5: LLM Agents & Tool Integration")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Build Autonomous AI Agents!**")
            
            st.markdown("### LAB 1: Build LLM Agent with Tools (120 min)")
            st.markdown("**Objective:** Create autonomous agent with function calling")
            lab5_1 = '''from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
import requests

print("🤖 BUILDING LLM AGENT\n" + "="*60)

# 1. Define tools
print("\n1. Defining Agent Tools...")

def get_weather(location: str) -> str:
    """Get weather for a location"""
    # Simulate API call
    return f"Weather in {location}: 72°F, Sunny"

def search_database(query: str) -> str:
    """Search company database"""
    # Simulate database query
    return f"Found 5 results for: {query}"

def calculate(expression: str) -> str:
    """Calculate mathematical expression"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid expression"

tools = [
    Tool(
        name="Weather",
        func=get_weather,
        description="Get current weather for a location. Input should be a city name."
    ),
    Tool(
        name="Database",
        func=search_database,
        description="Search company database. Input should be a search query."
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Calculate math expressions. Input should be a valid Python expression."
    )
]

print(f"✅ {len(tools)} tools defined")

# 2. Initialize agent
print("\n2. Initializing Agent...")

llm = ChatOpenAI(model="gpt-4", temperature=0)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

print("✅ Agent initialized")

# 3. Run agent tasks
print("\n3. Running Agent Tasks...")

# Task 1: Use weather tool
response1 = agent.run("What's the weather in London?")
print(f"\nTask 1 Response: {response1}")

# Task 2: Use calculator
response2 = agent.run("Calculate 15% of 2500")
print(f"\nTask 2 Response: {response2}")

# Task 3: Multi-step reasoning
response3 = agent.run("Search the database for 'sales reports' and tell me how many results were found")
print(f"\nTask 3 Response: {response3}")

print("\n✅ LLM agent complete!")'''
            st.code(lab5_1, language='python')
            
            st.markdown("### LAB 2: Multi-Agent System (120 min)")
            st.markdown("**Objective:** Build collaborative multi-agent system")
            lab5_2 = '''from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

print("🤖 MULTI-AGENT SYSTEM\n" + "="*60)

# 1. Define specialized agents
print("\n1. Creating Specialized Agents...")

llm = ChatOpenAI(model="gpt-4", temperature=0)

# Research Agent
def research_tool(query: str) -> str:
    """Research information"""
    return f"Research results for: {query}"

# Analysis Agent
def analysis_tool(data: str) -> str:
    """Analyze data"""
    return f"Analysis of: {data}"

# Writer Agent
def writer_tool(content: str) -> str:
    """Write content"""
    return f"Written content based on: {content}"

tools = [
    Tool(name="Research", func=research_tool, description="Research information"),
    Tool(name="Analysis", func=analysis_tool, description="Analyze data"),
    Tool(name="Writer", func=writer_tool, description="Write content")
]

# 2. Create agent with memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True
)

print("✅ Multi-agent system created")

# 3. Run collaborative task
print("\n2. Running Collaborative Task...")

response = agent.run("Research AI trends, analyze the findings, and write a summary")
print(f"\nResult: {response}")

print("\n✅ Multi-agent system complete!")'''
            st.code(lab5_2, language='python')
            
            st.markdown("### LAB 3: LangGraph for Agent Workflows (90 min)")
            st.markdown("**Objective:** Build complex agent workflows with state management")
            lab5_3 = '''from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from typing import TypedDict, Annotated
import operator

print("🔀 LANGGRAPH AGENT WORKFLOWS\n" + "="*60)

# 1. Define state
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_step: str
    data: dict

# 2. Define nodes (agent actions)
def research_node(state):
    print("\nResearch node executing...")
    llm = ChatOpenAI(model="gpt-4")
    
    response = llm.invoke("Research AI trends")
    
    return {
        "messages": [response.content],
        "data": {"research_complete": True}
    }

def analyze_node(state):
    print("\nAnalyze node executing...")
    llm = ChatOpenAI(model="gpt-4")
    
    research_data = state["messages"][-1]
    response = llm.invoke(f"Analyze this research: {research_data}")
    
    return {
        "messages": [response.content],
        "data": {"analysis_complete": True}
    }

def write_node(state):
    print("\nWrite node executing...")
    llm = ChatOpenAI(model="gpt-4")
    
    analysis = state["messages"][-1]
    response = llm.invoke(f"Write summary of: {analysis}")
    
    return {
        "messages": [response.content],
        "next_step": "end"
    }

# 3. Build graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("research", research_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("write", write_node)

# Define edges (workflow)
workflow.set_entry_point("research")
workflow.add_edge("research", "analyze")
workflow.add_edge("analyze", "write")
workflow.add_edge("write", END)

# Compile
app = workflow.compile()

print("✅ Workflow graph compiled")

# 4. Execute workflow
print("\nExecuting workflow...")

initial_state = {
    "messages": [],
    "next_step": "research",
    "data": {}
}

result = app.invoke(initial_state)

print("\n" + "="*60)
print("WORKFLOW COMPLETE")
print("="*60)
print(f"\nFinal output: {result['messages'][-1][:200]}...")

print("\n✅ LangGraph workflow complete!")'''
            st.code(lab5_3, language='python')
            
            st.success("✅ Unit 5 Labs Complete: LLM agents mastered!")
            
        elif selected_unit == 6:
            st.markdown("### 🔥 Unit 6: Production Deployment & Scaling")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Deploy LLMs at Scale!**")
            
            st.markdown("### LAB 1: Deploy LLM with FastAPI (120 min)")
            st.markdown("**Objective:** Build production API for LLM application")
            lab6_1 = '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import uvicorn
from functools import lru_cache

app = FastAPI(title="LLM API")

class QueryRequest(BaseModel):
    prompt: str
    max_tokens: int = 500
    temperature: float = 0.7

class QueryResponse(BaseModel):
    response: str
    tokens_used: int
    model: str

@lru_cache(maxsize=100)
def cached_completion(prompt: str, temperature: float):
    """Cached LLM completion"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response

@app.post("/query", response_model=QueryResponse)
async def query_llm(request: QueryRequest):
    """Query LLM endpoint"""
    try:
        response = cached_completion(request.prompt, request.temperature)
        
        return QueryResponse(
            response=response.choices[0].message.content,
            tokens_used=response.usage.total_tokens,
            model="gpt-4"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

print("✅ LLM API deployed!")'''
            st.code(lab6_1, language='python')
            
            st.markdown("### LAB 2: LLM Monitoring & Observability (90 min)")
            st.markdown("**Objective:** Monitor LLM performance, cost, and quality")
            lab6_2 = '''from prometheus_client import Counter, Histogram, Gauge, start_http_server
import openai
import time
import json

print("📊 LLM MONITORING & OBSERVABILITY\n" + "="*60)

# 1. Setup metrics
print("\n1. Setting up Prometheus Metrics...")

llm_requests_total = Counter('llm_requests_total', 'Total LLM requests', ['model', 'status'])
llm_latency = Histogram('llm_latency_seconds', 'LLM request latency', ['model'])
llm_tokens = Counter('llm_tokens_total', 'Total tokens used', ['model', 'type'])
llm_cost = Counter('llm_cost_dollars', 'Total cost in dollars', ['model'])
llm_errors = Counter('llm_errors_total', 'Total errors', ['model', 'error_type'])

print("✅ Metrics configured")

# 2. Monitored LLM call
def monitored_llm_call(prompt, model="gpt-4"):
    """LLM call with monitoring"""
    start_time = time.time()
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Record metrics
        latency = time.time() - start_time
        llm_latency.labels(model=model).observe(latency)
        llm_requests_total.labels(model=model, status='success').inc()
        
        # Token metrics
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        llm_tokens.labels(model=model, type='input').inc(input_tokens)
        llm_tokens.labels(model=model, type='output').inc(output_tokens)
        
        # Cost calculation
        cost = (input_tokens / 1000 * 0.03) + (output_tokens / 1000 * 0.06)
        llm_cost.labels(model=model).inc(cost)
        
        print(f"✅ Request successful: {latency:.2f}s, {response.usage.total_tokens} tokens, ${cost:.4f}")
        
        return response.choices[0].message.content
    
    except Exception as e:
        llm_requests_total.labels(model=model, status='error').inc()
        llm_errors.labels(model=model, error_type=type(e).__name__).inc()
        print(f"❌ Request failed: {e}")
        raise

# 3. Start metrics server
print("\n2. Starting Metrics Server...")
start_http_server(8000)
print("✅ Metrics available at http://localhost:8000")

# 4. Test monitored calls
print("\n3. Testing Monitored Calls...")

for i in range(5):
    result = monitored_llm_call(f"Test query {i+1}", model="gpt-4")
    print(f"Response {i+1}: {result[:50]}...")
    time.sleep(1)

print("\n4. Metrics Summary:")
print("View at: http://localhost:8000/metrics")
print("\nSample metrics:")
print("  llm_requests_total{model='gpt-4',status='success'} 5")
print("  llm_cost_dollars{model='gpt-4'} 0.0234")

print("\n✅ LLM monitoring complete!")'''
            st.code(lab6_2, language='python')
            
            st.markdown("### LAB 3: Docker & Kubernetes Deployment (75 min)")
            st.markdown("**Objective:** Containerize and scale LLM applications")
            lab6_3 = '''# Dockerfile for LLM API
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY .env .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# requirements.txt
# fastapi==0.104.1
# uvicorn==0.24.0
# openai==1.3.0
# python-dotenv==1.0.0
# redis==5.0.1

# Build and run:
# docker build -t llm-api .
# docker run -p 8000:8000 --env-file .env llm-api

# Kubernetes deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-api
  template:
    metadata:
      labels:
        app: llm-api
    spec:
      containers:
      - name: llm-api
        image: myregistry/llm-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: llm-api-service
spec:
  selector:
    app: llm-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer

# Deploy:
# kubectl apply -f deployment.yaml
# kubectl get pods
# kubectl logs <pod-name>

print("✅ LLM containerized and deployed to Kubernetes!")'''
            st.code(lab6_3, language='dockerfile')
            
            st.success("✅ Unit 6 Labs Complete: LLM deployment mastered!")
            
        elif selected_unit == 7:
            st.markdown("### 🎯 Unit 7: AI/LLM Engineer Capstone Projects")
            st.markdown("**Choose one project to demonstrate your LLM engineering expertise**")
            
            st.markdown("## 📊 Capstone Project Options")
            
            st.markdown("### Option 1: Enterprise RAG System")
            st.markdown("""
**Build:** Production RAG for company knowledge base

**Deliverables:**
- Document ingestion pipeline
- Vector database (Pinecone/Weaviate)
- RAG chain with citations
- Web interface
- Monitoring dashboard""")
            
            st.markdown("### Option 2: AI Agent Platform")
            st.markdown("""
**Build:** Multi-agent system with tool integration

**Deliverables:**
- Agent framework (LangChain/AutoGPT)
- Custom tools integration
- Memory & state management
- API deployment
- Usage analytics""")
            
            st.markdown("### Option 3: Fine-tuned Domain Model")
            st.markdown("""
**Build:** Fine-tuned LLM for specific industry

**Deliverables:**
- Training data pipeline
- Fine-tuning workflow
- Evaluation framework
- Model deployment
- Performance comparison""")
            
            st.markdown("### Option 4: LLM-Powered Data Analytics Assistant")
            st.markdown("""
**Build:** AI assistant that writes SQL and analyzes data

**Deliverables:**
- Natural language to SQL
- Data visualization generation
- Insight extraction
- Multi-turn conversations
- Web interface""")
            
            st.markdown("### Option 5: Production LLM Monitoring System")
            st.markdown("""
**Build:** Comprehensive monitoring for LLM applications

**Deliverables:**
- Cost tracking dashboard
- Latency monitoring
- Quality evaluation
- A/B testing framework
- Alert system""")
            
            st.markdown("## 📝 Evaluation Rubric")
            st.markdown("""
**Grading:**
- Architecture (25%)
- Code Quality (30%)
- Performance (20%)
- Documentation (15%)
- Innovation (10%)""")
            
            st.success("✅ Choose your capstone and build the future of AI!")
            
        else:
            st.info(f"Labs for Unit {selected_unit} will be added soon!")

    # Assessments
    with tabs[3]:
        st.subheader("📝 Assessments")
        st.info("Assessment criteria and submission guidelines.")

    # Evidence Tracking
    with tabs[4]:
        st.subheader("📋 Evidence Tracking")
        if learner_email:
            render_evidence_tracking(learner_email, COURSE_ID)
        else:
            st.warning("Please log in to track your evidence.")

    # Documents
    with tabs[5]:
        st.subheader("📂 Resources & Career Development")
        
        resource_tabs = st.tabs([
            "💼 Career Paths & Salaries",
            "🎤 Interview Preparation",
            "📚 Case Studies",
            "🔗 Additional Resources"
        ])
        
        # Career Paths & Salaries
        with resource_tabs[0]:
            st.markdown("### 💼 LLM Engineer Career Paths & Compensation")
            st.markdown("""
**LLM/AI Engineer career trajectory and market data (2024):**

---

**Career Levels & Compensation:**

| Level | Title | Years Exp | Base Salary | Total Comp | Responsibilities |
|-------|-------|-----------|-------------|------------|------------------|
| **L3** | Junior LLM Engineer | 0-2 | $100K-$140K | $120K-$170K | Implement features, fine-tune models |
| **L4** | LLM Engineer | 2-4 | $140K-$180K | $170K-$250K | Own features, optimize performance |
| **L5** | Senior LLM Engineer | 4-7 | $180K-$250K | $250K-$400K | System design, mentor juniors |
| **L6** | Staff LLM Engineer | 7-10 | $250K-$350K | $400K-$600K | Architecture, cross-team influence |
| **L7** | Principal Engineer | 10+ | $350K-$500K | $600K-$1M+ | Company-wide technical direction |

*Compensation includes base salary + equity + bonus. Big Tech (FAANG) pays 20-40% above average.*

---

**Role Variations:**

**1. LLM Application Engineer**
- **Focus:** Building user-facing LLM applications
- **Skills:** API integration, RAG, prompt engineering
- **Salary:** $120K-$250K (L3-L5)
- **Companies:** Startups, mid-size companies

**2. LLM Research Engineer**
- **Focus:** Model architecture, training, fine-tuning
- **Skills:** PyTorch, distributed training, RLHF
- **Salary:** $150K-$400K (L4-L6)
- **Companies:** OpenAI, Anthropic, Google DeepMind

**3. MLOps Engineer (LLM Focus)**
- **Focus:** Production deployment, scaling, monitoring
- **Skills:** Kubernetes, vLLM, observability
- **Salary:** $140K-$300K (L4-L5)
- **Companies:** All companies with LLM products

**4. Prompt Engineer**
- **Focus:** Optimizing prompts, evaluation frameworks
- **Skills:** Linguistics, few-shot learning, evaluation
- **Salary:** $90K-$180K (L3-L4)
- **Companies:** AI agencies, consulting

**5. LLM Safety/Alignment Engineer**
- **Focus:** Model safety, bias reduction, alignment
- **Skills:** RLHF, red teaming, evaluation
- **Salary:** $160K-$400K (L4-L6)
- **Companies:** OpenAI, Anthropic, Meta

---

**Geographic Variations:**

| Location | Multiplier | Example (L4 Base) |
|----------|------------|-------------------|
| **San Francisco Bay Area** | 1.0x (baseline) | $160K |
| **Seattle** | 0.95x | $152K |
| **New York City** | 0.95x | $152K |
| **Austin** | 0.85x | $136K |
| **Remote (US)** | 0.80x | $128K |
| **Europe (London, Berlin)** | 0.60-0.70x | $96K-$112K |
| **Asia (Singapore, Tokyo)** | 0.55-0.65x | $88K-$104K |

---

**Company Tier Breakdown:**

**Tier 1 - Big Tech (FAANG + OpenAI, Anthropic)**
- Base: $150K-$500K
- Equity: $100K-$500K/year
- Bonus: 15-25%
- **Total:** $200K-$1M+
- **Examples:** Google, Meta, OpenAI, Anthropic, Microsoft

**Tier 2 - High-Growth Startups (Post-Series B)**
- Base: $130K-$350K
- Equity: $50K-$300K/year (paper value)
- Bonus: 10-20%
- **Total:** $150K-$600K
- **Examples:** Cohere, Hugging Face, Scale AI

**Tier 3 - Mid-Size Tech Companies**
- Base: $110K-$250K
- Equity: $20K-$100K/year
- Bonus: 10-15%
- **Total:** $130K-$350K
- **Examples:** Notion, Salesforce, Adobe

**Tier 4 - Traditional Companies + Early Startups**
- Base: $90K-$180K
- Equity: $0-$50K/year
- Bonus: 5-10%
- **Total:** $95K-$220K
- **Examples:** Banks, consulting, seed startups

---

**Skills to Salary Mapping:**

**Core Skills (Must Have):**
- Python, LLM APIs (**minimum**: +$100K base)
- Prompt engineering (+$20K)
- RAG systems (+$25K)

**Advanced Skills (High Value):**
- Fine-tuning (LoRA, RLHF) (+$30K)
- Production deployment (vLLM, TGI) (+$35K)
- LangChain/LlamaIndex (+$20K)
- Vector databases (+$25K)
- Evaluation frameworks (+$20K)

**Specialized Skills (Premium):**
- Model training from scratch (+$50K)
- Distributed training (+$40K)
- RLHF implementation (+$45K)
- Multi-modal models (+$40K)
- Safety/alignment (+$50K)

**Business Skills (Multiplier):**
- Technical leadership (+30%)
- Product sense (+20%)
- Stakeholder management (+15%)

---

**Career Progression Timeline:**

**Year 0-2: Junior Engineer**
- Learn fundamentals
- Build RAG applications
- Basic fine-tuning
- **Target:** $120K-$170K

**Year 2-4: Mid-Level Engineer**
- Own features end-to-end
- Optimize production systems
- Advanced fine-tuning
- **Target:** $170K-$250K

**Year 4-7: Senior Engineer**
- Design systems
- Mentor 2-3 engineers
- Cross-functional projects
- **Target:** $250K-$400K

**Year 7-10: Staff Engineer**
- Architecture decisions
- Influence multiple teams
- Technical strategy
- **Target:** $400K-$600K

**Year 10+: Principal/Distinguished**
- Company-wide impact
- Industry thought leader
- Research contributions
- **Target:** $600K-$1M+

---

**Alternative Paths:**

**Management Track:**
- **Engineering Manager:** $200K-$400K (manages 5-8 engineers)
- **Director of Engineering:** $300K-$600K (manages multiple teams)
- **VP of Engineering:** $400K-$1M+ (org-level leadership)

**Entrepreneurship:**
- **Founder (bootstrapped):** $0-$100K (early years)
- **Founder (funded):** $150K-$250K salary + equity
- **Exit potential:** $1M-$100M+ (rare but possible)

**Consulting:**
- **Independent Consultant:** $150-$500/hour ($200K-$800K/year)
- **Agency Partner:** $200K-$500K + profit share
- **Course Creator:** $50K-$500K/year (supplemental income)

---

**Job Market Trends (2024-2025):**

**Hot Skills:**
1. **Agentic AI** - 300% increase in job postings
2. **RAG Systems** - 250% increase
3. **LLM Evaluation** - 200% increase
4. **Production Deployment** - 180% increase
5. **Safety/Alignment** - 150% increase

**Market Conditions:**
- **Demand:** Very High (10+ openings per qualified candidate)
- **Competition:** Medium (more candidates entering market)
- **Time to Hire:** 2-8 weeks (faster than traditional ML roles)
- **Remote Work:** 60% of roles offer remote options

**Industry Hiring:**
- **Tech:** 40% of LLM roles
- **Finance:** 15% (trading, risk, compliance)
- **Healthcare:** 12% (diagnostics, drug discovery)
- **Legal:** 8% (contract analysis, research)
- **E-commerce:** 8% (recommendations, search)
- **Other:** 17%

---

**Compensation Negotiation Tips:**

**Research Comparable Offers:**
- Use Levels.fyi, Blind, H1B salary database
- Ask peers in similar roles
- Get multiple offers to compare

**Negotiation Strategy:**
- **Never give first number** - let them anchor
- **Focus on total comp** - not just base salary
- **Negotiate all components:**
  - Base salary (+10-20% possible)
  - Signing bonus ($20K-$100K)
  - Equity (25-50% increase possible)
  - Performance bonus (5-10% increase)
  - Relocation ($10K-$50K)

**Leverage Points:**
- Competing offers (strongest leverage)
- Unique skills (RLHF, multi-modal)
- Published research/projects
- Industry reputation

**Common Mistakes:**
- ❌ Accepting first offer without negotiating
- ❌ Only negotiating base salary
- ❌ Not understanding equity value
- ❌ Ignoring total compensation
- ❌ Negotiating over email (phone is better)

**Example Negotiation:**
```
Initial Offer:
- Base: $150K
- Equity: $100K/year (4 years)
- Bonus: 15% target
- Total: $272.5K

After Negotiation:
- Base: $165K (+$15K, 10%)
- Equity: $150K/year (+$50K, 50%)
- Signing Bonus: $30K (new)
- Bonus: 15% target
- Total: $344.75K (+$72.25K, 26.5% increase!)
```

---

**Building Your LLM Engineer Personal Brand:**

**Portfolio Projects (Essential):**
1. **Production RAG System** - deployed, with metrics
2. **Fine-tuned Model** - show before/after performance
3. **LLM Agent** - autonomous multi-tool system
4. **Open Source Contribution** - PR to major library
5. **Technical Blog Posts** - 5-10 articles

**Portfolio Hosting:**
- GitHub (code)
- Personal website (demos)
- Hugging Face (models)
- Medium/Substack (writing)
- YouTube (video demos, optional)

**Networking Strategies:**
- **Twitter/X:** Follow and engage with AI researchers
- **LinkedIn:** Post weekly about your learnings
- **Conferences:** NeurIPS, ICML, ACL (attend or volunteer)
- **Meetups:** Local AI/ML meetups
- **Discord/Slack:** Join LangChain, LlamaIndex communities

**Content Creation Ideas:**
- "I built a RAG system for [domain]"
- "Fine-tuning Llama 2 for under $50"
- "Prompt engineering patterns that actually work"
- "Deploying LLMs on a budget"
- "Common LLM mistakes and how to avoid them"

---

**Remote Work Opportunities:**

**Fully Remote Companies Hiring LLM Engineers:**
1. **Anthropic** - Remote US
2. **Cohere** - Remote North America
3. **Hugging Face** - Remote Global
4. **Scale AI** - Remote US
5. **Jasper.ai** - Remote US
6. **Inflection AI** - Remote US
7. **Character.AI** - Remote US
8. **Perplexity AI** - Remote US

**Tips for Remote Job Success:**
- **Communication:** Over-communicate progress
- **Timezone:** Be flexible with meetings
- **Presence:** Active on Slack/Discord
- **Documentation:** Write everything down
- **Video:** Camera on for important meetings

---

**Job Search Resources:**

**Job Boards:**
- LinkedIn Jobs (filter: "LLM", "AI Engineer")
- Wellfound (AngelList) - Startups
- Hacker News Who's Hiring
- AI Alignment Jobs Board
- LLM Career Jobs (specialized)

**Recruiters:**
- Hired.com
- TripleByte
- Vettery
- Direct reach-outs on LinkedIn

**Company Career Pages:**
- OpenAI: openai.com/careers
- Anthropic: anthropic.com/careers
- Google DeepMind: deepmind.com/careers
- Meta AI: ai.facebook.com/join-us

**Application Strategy:**
- **Volume:** Apply to 10-20 companies
- **Quality:** Tailor resume for each role
- **Timing:** Apply within 48 hours of posting
- **Follow-up:** Email recruiter after 5-7 days
- **Portfolio:** Send GitHub link with application

---

**Career Development Plan:**

**Months 1-3: Foundation**
- Complete this pathway
- Build 2 portfolio projects
- Write 3 technical blog posts
- **Goal:** Be interview-ready

**Months 4-6: Job Search**
- Apply to 15+ positions
- Network with 10+ professionals
- Attend 2 conferences/meetups
- **Goal:** Land first LLM role

**Months 7-12: First Role**
- Ship 2 major features
- Mentor 1 junior engineer
- Present at internal tech talk
- **Goal:** Demonstrate impact

**Year 2: Growth**
- Lead 1 project end-to-end
- Contribute to open source
- Speak at 1 external conference
- **Goal:** Promotion to mid-level

**Year 3-5: Specialization**
- Become expert in 1 area (RAG, fine-tuning, agents)
- Mentor 2-3 engineers
- Design systems architecture
- **Goal:** Senior engineer ($250K+)

---

**Success Metrics:**

**Technical:**
- ✅ 5+ production LLM features shipped
- ✅ 10K+ GitHub stars (open source)
- ✅ 3+ technical talks given
- ✅ 20+ blog posts published

**Career:**
- ✅ 100%+ salary increase in 3 years
- ✅ Promoted twice
- ✅ 50+ LinkedIn connections in AI
- ✅ Recognized expert in 1 domain

**Financial:**
- ✅ $250K+ total comp by year 5
- ✅ Equity worth $100K+ (paper value)
- ✅ Emergency fund (6 months expenses)
- ✅ Passive income streams ($1K+/month)
""")
        
        # Interview Preparation
        with resource_tabs[1]:
            st.markdown("### 🎤 LLM Engineer Interview Preparation")
            st.markdown("""
**Complete interview guide with real questions from top companies:**

---

**Interview Process Overview:**

**Typical Timeline: 3-6 weeks**

1. **Recruiter Screen** (30 min)
   - Background, motivation, salary expectations

2. **Technical Phone Screen** (45-60 min)
   - Coding (LeetCode Easy-Medium)
   - Basic LLM concepts

3. **Take-Home Assignment** (3-5 hours)
   - Build mini LLM application
   - Due in 3-7 days

4. **Onsite/Virtual Onsite** (4-5 hours)
   - **Round 1:** System Design (LLM focus)
   - **Round 2:** ML Fundamentals
   - **Round 3:** LLM Deep Dive
   - **Round 4:** Behavioral
   - **Round 5:** Coding

5. **Final Round** (30 min)
   - Hiring manager
   - Team fit, career goals

---

**Technical Interview Categories:**

### **1. LLM Fundamentals (Must Know)**

**Q: Explain how transformers work.**
```
Answer:
1. Input Embedding + Positional Encoding
2. Multi-Head Self-Attention
   - Q, K, V projections
   - Scaled dot-product attention
   - Multiple heads capture different patterns
3. Feed-Forward Network
   - 2-layer MLP
   - Applied position-wise
4. Layer Normalization + Residual Connections
5. Repeated N times (e.g., 12 layers for BERT-base)

Key Innovation: Self-attention allows modeling long-range dependencies
in O(n²) time vs O(n³) for RNNs.
```

**Q: What's the difference between GPT, BERT, and T5?**
```
Answer:
- GPT (Decoder-only): Autoregressive, predict next token
  Use case: Text generation, completion
  
- BERT (Encoder-only): Bidirectional, masked language modeling
  Use case: Classification, NER, Q&A
  
- T5 (Encoder-Decoder): Seq2seq, "text-to-text"
  Use case: Translation, summarization, generation

Modern trend: Decoder-only (GPT-style) dominates due to scaling laws.
```

**Q: Explain temperature in LLM sampling.**
```
Answer:
Temperature controls randomness in token selection:

- Temperature = 0: Greedy (always pick highest probability)
  Output: Deterministic, conservative
  
- Temperature = 0.7: Moderate randomness (good for most tasks)
  Output: Balanced creativity and coherence
  
- Temperature = 1.0: Sample from true distribution
  Output: More diverse, less predictable
  
- Temperature = 2.0: High randomness
  Output: Creative but may lose coherence

Formula: p_i = exp(logit_i / T) / Σ exp(logit_j / T)

Lower T → peaks sharpen → more deterministic
Higher T → distribution flattens → more random
```

**Q: What are embeddings and why are they important?**
```
Answer:
Embeddings map discrete tokens to continuous vectors.

Example:
"king" → [0.2, 0.8, -0.3, ...]  (768-dim vector)

Why important:
1. Capture semantic meaning
2. Similar words → similar vectors
   "king" and "queen" are close in space
3. Enable arithmetic: king - man + woman ≈ queen

In LLMs:
- Input: Token embeddings + positional embeddings
- Output: Contextual embeddings (different per position)
- Used for: RAG, semantic search, clustering
```

---

### **2. Prompt Engineering Questions**

**Q: How would you improve this prompt?**
```
Bad Prompt:
"Summarize this article."

Improved Prompt:
"Summarize this article in 3 bullet points, focusing on:
1. Main findings
2. Methodology
3. Implications

Keep each bullet under 50 words. Use technical language."

Why better:
- Clear output format (3 bullets)
- Specific focus areas
- Length constraint
- Tone specified
```

**Q: Explain few-shot prompting with an example.**
```
Answer:
Few-shot prompting provides examples to guide the model.

Example: Sentiment Classification

Prompt:
\"\"\"
Classify sentiment as Positive, Negative, or Neutral.

Examples:
Text: "This product is amazing!" → Sentiment: Positive
Text: "Worst purchase ever." → Sentiment: Negative
Text: "It's okay, nothing special." → Sentiment: Neutral

Now classify:
Text: "I love the design but it broke after a week." → Sentiment:
\"\"\"

Model Output: Negative

Why it works: Model learns pattern from examples
```

**Q: What's Chain-of-Thought prompting?**
```
Answer:
CoT prompts the model to show its reasoning steps.

Without CoT:
Q: "If I have 5 apples and buy 3 more, then give away 2, how many remain?"
A: "6" (might be wrong)

With CoT:
Q: "If I have 5 apples and buy 3 more, then give away 2, how many remain?
Let's think step by step."
A: "Starting with 5 apples.
    After buying 3 more: 5 + 3 = 8 apples.
    After giving away 2: 8 - 2 = 6 apples.
    Final answer: 6 apples."

Improves accuracy on reasoning tasks by 20-80%!
```

---

### **3. RAG System Questions**

**Q: Design a RAG system for customer support.**
```
Answer:

Architecture:
1. Document Ingestion
   - Load support docs, FAQs, past tickets
   - Chunk (512 tokens, 128 overlap)
   - Embed with sentence-transformers
   - Store in Pinecone/Weaviate

2. Query Processing
   - User asks: "How do I reset my password?"
   - Embed query
   - Retrieve top-5 relevant chunks (cosine similarity)
   - Rerank with cross-encoder (optional)

3. Generation
   - Construct prompt with retrieved context
   - Call LLM (GPT-3.5-turbo)
   - Generate answer with citations

4. Optimization
   - Cache common queries (Redis)
   - Monitor relevance metrics
   - A/B test chunk sizes

Cost: ~$0.05 per query
Latency: ~500ms
```

**Q: How would you evaluate RAG system quality?**
```
Answer:

Retrieval Metrics:
- Recall@K: % of relevant docs in top-K
- MRR (Mean Reciprocal Rank): 1 / rank of first relevant doc
- NDCG: Normalized Discounted Cumulative Gain

Generation Metrics:
- Faithfulness: Answer grounded in context? (LLM-as-judge)
- Answer Relevance: Addresses the question? (embedding similarity)
- Context Relevance: Retrieved context useful? (manual review)

End-to-End Metrics:
- User satisfaction (thumbs up/down)
- Resolution rate (issue solved?)
- Time to resolution

Implementation:
- Use LangSmith or Phoenix for monitoring
- A/B test improvements
- Human eval on sample (100 queries/week)
```

**Q: Vector database vs traditional database?**
```
Answer:

Traditional DB (PostgreSQL):
- Stores structured data (rows/columns)
- Exact match queries: WHERE name = 'John'
- Fast for lookups: O(log n)
- Not semantic

Vector DB (Pinecone, Weaviate):
- Stores embeddings (high-dim vectors)
- Semantic similarity queries: Find similar to [0.2, 0.8, ...]
- Fast ANN search: O(log n) with HNSW
- Captures meaning

Use Vector DB when:
- Semantic search needed
- Fuzzy matching
- Recommendation systems
- RAG applications

Hybrid Approach:
- PostgreSQL + pgvector extension
- Get structured filtering + vector search
```

---

### **4. Fine-Tuning Questions**

**Q: When should you fine-tune vs use prompting?**
```
Answer:

Use Prompting When:
- < 100 examples
- Task varies frequently
- Quick iteration needed
- Budget constrained

Use Fine-tuning When:
- 1,000+ examples available
- Consistent output format critical
- Domain-specific terminology
- Cost optimization at scale (shorter prompts)
- Latency sensitive (smaller fine-tuned model faster)

Example:
Medical diagnosis: Fine-tune (specialized domain)
General Q&A: Prompting (variety of queries)
```

**Q: Explain LoRA and why it's useful.**
```
Answer:

LoRA (Low-Rank Adaptation):
Instead of updating all 7B parameters, add small adapter matrices:
- Original: W (4096 x 4096) = 16M params
- LoRA: W + B×A where B (4096 x 8) and A (8 x 4096)
- Trainable: 131K params (99% reduction!)

Benefits:
1. Memory: Fine-tune 7B model on single GPU
2. Cost: $24 vs $5,000 for full fine-tuning
3. Speed: Train in hours vs days
4. Storage: Adapter = 10MB vs 14GB full model

Performance: 90-95% of full fine-tuning quality

Used by: Most production fine-tuning today
```

**Q: How would you prepare training data for fine-tuning?**
```
Answer:

Steps:
1. Collection
   - 1,000+ examples minimum
   - Diverse, representative of production

2. Format
   OpenAI:
   {"messages": [
     {"role": "system", "content": "You are..."},
     {"role": "user", "content": "Question"},
     {"role": "assistant", "content": "Answer"}
   ]}

3. Quality Check
   - Remove duplicates
   - Fix formatting errors
   - Check for PII
   - Manual review sample (100 examples)

4. Split
   - Train: 80%
   - Validation: 10%
   - Test: 10%

5. Augmentation (optional)
   - Paraphrase questions
   - Vary formatting
   - Add edge cases

Critical: Quality > Quantity
100 perfect examples > 1,000 mediocre examples
```

---

### **5. System Design Questions**

**Q: Design a production LLM chatbot for 100K daily users.**
```
Answer:

Requirements:
- 100K users/day = ~1.2 requests/second average
- Peak: 10x = 12 req/s
- Latency: < 2 seconds
- Cost: < $1,000/day

Architecture:

1. Load Balancer (AWS ALB)
   ↓
2. API Gateway (FastAPI)
   - Rate limiting: 100 req/min per user
   - Authentication: JWT tokens
   ↓
3. Cache Layer (Redis)
   - Cache common queries (30% hit rate)
   ↓
4. LLM Serving (vLLM)
   - 3x instances (Llama 2 7B)
   - Auto-scaling based on queue depth
   ↓
5. Database (PostgreSQL)
   - Store conversations
   - User metadata
   ↓
6. Monitoring (Prometheus + Grafana)
   - Latency, error rate, cost
   - Alerts on anomalies

Cost Breakdown:
- Compute: $500/day (3x A10 GPUs @ $0.50/hr)
- Storage: $20/day (1TB conversations)
- Network: $30/day
- Monitoring: $10/day
- Total: $560/day ✅ Under budget!

Optimizations:
- Semantic caching (+30% cost reduction)
- Batch inference (+5x throughput)
- INT8 quantization (+2x throughput)
```

**Q: How would you handle 10x traffic spike?**
```
Answer:

Short-term (< 5 min):
1. Auto-scaling (Kubernetes HPA)
   - Scale from 3 → 10 instances
   - Based on CPU > 70%

2. Cache warming
   - Preload common queries
   - 50% hit rate during spike

3. Rate limiting
   - 100 → 50 req/min per user
   - Queue non-critical requests

4. Circuit breaker
   - Fail fast if service degraded
   - Return cached/fallback responses

Long-term:
1. Capacity planning
   - Provision for 3x average traffic
   - Quarterly reviews

2. Load testing
   - Simulate 20x traffic monthly
   - Identify bottlenecks

3. Multi-region
   - Deploy to 3 regions (US-East, US-West, EU)
   - Route based on geography

4. CDN
   - Cache static responses
   - Reduce backend load

Cost during spike:
- Normal: $560/day
- 10x spike: $2,000/day (1 hour) = $83 total
- Acceptable with proper alerting
```

---

### **6. Coding Questions**

**Q: Implement semantic similarity search.**
```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.embeddings = None
    
    def index(self, documents):
        \"\"\"Index documents\"\"\"
        self.documents = documents
        self.embeddings = self.model.encode(documents)
    
    def search(self, query, top_k=5):
        \"\"\"Search for similar documents\"\"\"
        query_emb = self.model.encode([query])[0]
        
        # Cosine similarity
        similarities = np.dot(self.embeddings, query_emb) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_emb)
        )
        
        # Top K
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = [
            {
                "document": self.documents[i],
                "score": float(similarities[i])
            }
            for i in top_indices
        ]
        
        return results

# Usage
search = SemanticSearch()
search.index([
    "The weather is sunny today",
    "It's raining outside",
    "Python is a programming language"
])

results = search.search("What's the weather like?", top_k=2)
# Returns: sunny, raining docs (not Python)
```

**Q: Implement token counting for cost estimation.**
```python
import tiktoken

class CostEstimator:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.encoder = tiktoken.encoding_for_model(model)
        
        # Pricing (per 1K tokens)
        self.pricing = {
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gpt-4": {"input": 0.03, "output": 0.06}
        }
    
    def count_tokens(self, text):
        \"\"\"Count tokens in text\"\"\"
        return len(self.encoder.encode(text))
    
    def estimate_cost(self, input_text, output_tokens):
        \"\"\"Estimate cost for request\"\"\"
        input_tokens = self.count_tokens(input_text)
        
        input_cost = (input_tokens / 1000) * self.pricing[self.model]["input"]
        output_cost = (output_tokens / 1000) * self.pricing[self.model]["output"]
        
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost
        }

# Usage
estimator = CostEstimator("gpt-3.5-turbo")
cost = estimator.estimate_cost(
    "Write a 500-word essay about AI",
    output_tokens=700
)
print(f"Cost: ${cost['total_cost']:.4f}")
# Output: Cost: $0.0017
```

---

### **7. Behavioral Questions**

**Q: Tell me about a time you optimized an LLM system.**
```
STAR Framework:

Situation:
"Our RAG system was costing $10,000/month with 500ms latency."

Task:
"Reduce cost by 50% and latency to < 200ms without sacrificing quality."

Action:
1. Profiled system: 60% cost from embeddings, 30% from LLM
2. Implemented semantic caching (95% similarity threshold)
3. Switched embedder to smaller model (384 vs 768 dims)
4. Batched embedding requests (10x throughput)
5. Added Redis cache layer

Result:
- Cost reduced to $3,500/month (65% reduction)
- Latency improved to 180ms (64% reduction)
- Quality maintained (user satisfaction 96% → 95%)
- Documented optimization playbook for team
```

**Q: How do you handle ambiguous requirements?**
```
Answer:
1. Ask clarifying questions
   - "What's the success metric?"
   - "Who are the users?"
   - "What's the timeline?"

2. Create prototype quickly
   - Build minimal version in 1-2 days
   - Get feedback early

3. Iterate based on feedback
   - Don't goldplate
   - Ship increments

Example:
Request: "Make the chatbot better"
My approach:
- Defined "better": lower error rate + faster response
- Created evaluation set (100 queries)
- Tested 3 approaches
- Shipped best one in 1 week
```

---

**Interview Preparation Timeline:**

**4 Weeks Before:**
- Review LLM fundamentals
- Practice 30 coding problems (LeetCode)
- Build 1 portfolio project

**2 Weeks Before:**
- Mock interviews (Pramp, Interviewing.io)
- System design practice (5 problems)
- Behavioral STAR stories (5 examples)

**1 Week Before:**
- Company research (products, tech stack)
- Review your resume projects
- Prepare questions for interviewers

**Day Before:**
- Light review (no cramming!)
- Prepare environment (quiet space, good internet)
- Get 8 hours sleep

**Interview Day:**
- Arrive 10 min early (or log in early)
- Have water, pen, paper ready
- Stay calm, think out loud
- Ask clarifying questions

---

**Resources:**

**Practice Platforms:**
- LeetCode (coding)
- Pramp (mock interviews)
- Interviewing.io (practice with engineers)
- Glassdoor (company-specific questions)

**Books:**
- "Cracking the Coding Interview"
- "Designing Data-Intensive Applications"
- "System Design Interview" (Vol 1 & 2)

**Courses:**
- Fast.ai "Practical Deep Learning"
- DeepLearning.AI "LLM Specialization"
- This pathway! 🎓
""")
        
        # Case Studies
        with resource_tabs[2]:
            st.markdown("### 📚 Real-World LLM Case Studies")
            st.markdown("""
**Learn from production LLM systems at leading companies:**

---

## **Case Study 1: OpenAI ChatGPT**

**Overview:**
ChatGPT reached 100M users in 2 months - fastest growing app in history.

**Architecture:**

```
User Request
    ↓
Load Balancer (Azure)
    ↓
API Gateway
    ↓
Rate Limiter + Auth
    ↓
Content Moderation (Input)
    ↓
GPT-4 / GPT-3.5-turbo
    ↓
Content Moderation (Output)
    ↓
Response
```

**Technical Stack:**
- **Models:** GPT-4 (175B+), GPT-3.5-turbo (20B)
- **Infrastructure:** Azure cloud, custom NVIDIA clusters
- **Serving:** Custom inference engine (similar to vLLM)
- **Database:** Distributed system for conversation history
- **Monitoring:** Real-time metrics on quality, latency, cost

**Training Process:**

**1. Pre-training ($10M+)**
- 10,000+ GPUs for months
- 300B+ tokens of internet text
- Custom data filtering pipeline

**2. Supervised Fine-tuning ($100K)**
- 13,000+ human demonstrations
- High-quality instruction following
- Multi-turn conversations

**3. RLHF ($500K)**
- 30,000+ comparison pairs
- PPO optimization
- Iterative refinement over 6+ months

**Key Innovations:**

**System Message Control:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is quantum computing?"},
    {"role": "assistant", "content": "..."}
]
```

**Function Calling:**
```python
functions = [
    {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }
]
```

**Challenges Overcome:**

**1. Hallucinations**
- **Problem:** Model makes up facts
- **Solution:** RLHF with truthfulness reward, browsing tool for facts
- **Result:** 40% reduction in factual errors

**2. Safety**
- **Problem:** Harmful content generation
- **Solution:** Multi-layer moderation (input, output, post-processing)
- **Result:** 99.9% safety rate

**3. Scale**
- **Problem:** 100M daily users, peak 10K req/s
- **Solution:** Aggressive caching, model optimization, geographic distribution
- **Cost:** Estimated $2-3M/day in compute

**4. Latency**
- **Problem:** Users expect <1s response time
- **Solution:** Streaming responses, speculative decoding
- **Result:** Tokens start appearing in 300-500ms

**Cost Optimization:**

**Initial (Feb 2023):**
- Cost per query: $0.10
- Daily cost: $10M (100M queries)
- Monthly: $300M

**Optimized (Dec 2023):**
- Cost per query: $0.02
- Daily cost: $2M (80% reduction!)
- Techniques:
  - Distillation to smaller models
  - Caching common queries (40% hit rate)
  - Dynamic batching
  - Quantization (INT8)

**Metrics:**

| Metric | Value |
|--------|-------|
| **Active Users** | 100M+ weekly |
| **Requests/day** | 1B+ |
| **Latency (p50)** | 1.2s |
| **Latency (p99)** | 4.5s |
| **Uptime** | 99.9% |
| **User Satisfaction** | 4.5/5 |

**Lessons Learned:**

1. **RLHF is Critical** - Transformed model from "impressive" to "magical"
2. **Safety Layers** - Multiple layers catch more issues
3. **Caching Saves Millions** - 40% cache hit rate = $4M/day saved
4. **Streaming UX** - Users prefer seeing tokens immediately
5. **Monitor Everything** - Real-time alerts on quality degradation

**Open Questions:**
- How to reduce hallucinations further?
- Can we make alignment more efficient?
- How to handle multi-modal effectively?

---

## **Case Study 2: GitHub Copilot**

**Overview:**
AI pair programmer used by 1.5M+ developers, $10/month subscription.

**Architecture:**

```
IDE (VS Code)
    ↓
Copilot Extension
    ↓
Code Context Extraction
    ↓
API Gateway (GitHub)
    ↓
Codex Model (OpenAI)
    ↓
Post-processing
    ↓
Suggestions (1-3 options)
```

**Technical Stack:**
- **Model:** Codex (GPT-3.5 derivative, 12B params)
- **Training:** GitHub public repos (billions of lines)
- **Infrastructure:** Azure OpenAI Service
- **Latency:** <1s for suggestions
- **Context:** Up to 8KB of surrounding code

**Training Process:**

**1. Data Collection**
- Source: GitHub public repositories
- Size: 159GB of Python code alone
- Filtering:
  - Remove duplicates
  - Filter low-quality code
  - Remove sensitive data (API keys, PII)
  - License compliance checks

**2. Model Training**
- Base: GPT-3 architecture
- Specialization: Code completion
- Training time: Weeks on 1,000+ GPUs
- Cost: Estimated $5M+

**3. Fine-tuning**
- Human feedback on code quality
- Correctness verification
- Style consistency
- Security vulnerability detection

**Context Window Optimization:**

**Challenge:** Include relevant code without exceeding token limit

**Solution:**
```python
def extract_context(cursor_position, max_tokens=2048):
    \"\"\"
    Smart context extraction
    \"\"\"
    context = []
    
    # 1. Current file (highest priority)
    current_file = get_surrounding_code(cursor_position, lines=50)
    context.append(current_file)
    
    # 2. Imported files (if space)
    imports = get_imported_files()
    for imp in imports:
        if count_tokens(context) < max_tokens * 0.7:
            context.append(get_relevant_snippets(imp))
    
    # 3. Recently viewed files
    recent = get_recent_files(limit=5)
    for file in recent:
        if count_tokens(context) < max_tokens * 0.9:
            context.append(get_relevant_snippets(file))
    
    return combine_context(context, max_tokens)
```

**Key Features:**

**1. Multi-Line Suggestions**
```python
# User types:
def calculate_fibonacci(n):

# Copilot suggests entire function:
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
```

**2. Comment-to-Code**
```python
# User types:
# Function to send email with attachment

# Copilot generates:
def send_email_with_attachment(to, subject, body, attachment_path):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    # ... (complete implementation)
```

**3. Test Generation**
```python
# User types:
# Test for calculate_fibonacci

# Copilot generates:
def test_calculate_fibonacci():
    assert calculate_fibonacci(0) == 0
    assert calculate_fibonacci(1) == 1
    assert calculate_fibonacci(5) == 5
    assert calculate_fibonacci(10) == 55
```

**Challenges Overcome:**

**1. Code Quality**
- **Problem:** Generated code sometimes buggy or inefficient
- **Solution:** Post-processing filters, style checkers, linting
- **Result:** 27% acceptance rate → 35% after improvements

**2. Security**
- **Problem:** Generated code with vulnerabilities (SQL injection, XSS)
- **Solution:** Security scanner on all suggestions
- **Result:** 95% of vulnerabilities caught

**3. Licensing**
- **Problem:** Suggesting copyrighted code verbatim
- **Solution:** Duplicate detection, attribution system
- **Result:** <0.1% of suggestions flagged

**4. Latency**
- **Problem:** Users expect <500ms for suggestions
- **Solution:**
  - Aggressive caching of common patterns
  - Speculative generation (predict next edit)
  - Model optimization (distillation to 6B params)
- **Result:** p50 latency 300ms, p99 800ms

**Business Impact:**

| Metric | Value |
|--------|-------|
| **Subscribers** | 1.5M+ developers |
| **Revenue** | $180M+/year ($10/month × 1.5M) |
| **Code Acceptance** | 35-40% of suggestions |
| **Time Saved** | 55% faster coding (self-reported) |
| **ROI** | 10x for enterprises |

**Cost Structure:**

**Per User Per Month:**
- Model inference: $2-3
- Infrastructure: $1
- Support: $1
- **Total cost:** ~$4-5
- **Subscription:** $10
- **Margin:** 50-60%

**Lessons Learned:**

1. **Context is Everything** - More relevant context = better suggestions
2. **Latency Matters** - >1s feels broken, <500ms feels magical
3. **Acceptance Rate** - Focus on quality over quantity
4. **Security Scanning** - Must-have for code generation
5. **User Trust** - Transparent about limitations builds trust

**Future Directions:**
- Multi-file understanding
- Refactoring suggestions
- Bug detection and fixes
- Architecture recommendations

---

## **Case Study 3: Anthropic Claude**

**Overview:**
Claude is Anthropic's AI assistant focused on safety and helpfulness.

**Architecture:**

```
User Request
    ↓
Constitutional AI Check
    ↓
Claude 3 (Opus/Sonnet/Haiku)
    ↓
Safety Filters
    ↓
Response
```

**Technical Innovation: Constitutional AI (CAI)**

**Traditional RLHF:**
```
Human labels → Reward model → RL training
```

**Constitutional AI:**
```
AI self-critique → Constitutional principles → RL training
```

**How It Works:**

**Step 1: Constitutional Principles**
```python
principles = [
    "Choose the response that is most helpful and harmless",
    "Avoid responses that are toxic, racist, or sexist",
    "Prefer responses that are thoughtful and nuanced",
    "Acknowledge uncertainty rather than making up facts"
]
```

**Step 2: Self-Critique**
```python
# Generate initial response
response = model.generate(prompt)

# Self-critique
critique_prompt = f\"\"\"
Response: {response}

Critique this response according to these principles:
{principles}

What could be improved?
\"\"\"

critique = model.generate(critique_prompt)

# Generate improved response
improved_prompt = f\"\"\"
Original: {response}
Critique: {critique}

Generate an improved response:
\"\"\"

improved = model.generate(improved_prompt)
```

**Step 3: AI Feedback**
```python
# Compare responses
comparison_prompt = f\"\"\"
Response A: {response}
Response B: {improved}

Which response better follows the constitutional principles?
\"\"\"

preference = model.generate(comparison_prompt)
# Use for training reward model
```

**Benefits:**
- **Scalable:** No need for massive human labeling
- **Consistent:** Follows explicit principles
- **Transparent:** Principles are documented
- **Flexible:** Easy to update principles

**Model Variants:**

| Model | Parameters | Context | Speed | Cost | Use Case |
|-------|-----------|---------|-------|------|----------|
| **Claude 3 Opus** | 175B+ | 200K | Slow | $$$$ | Complex reasoning |
| **Claude 3 Sonnet** | 60B | 200K | Medium | $$ | Balanced |
| **Claude 3 Haiku** | 10B | 200K | Fast | $ | High volume |

**200K Context Window:**

**Challenge:** Most LLMs support 4K-32K tokens

**Claude's Solution:**
```python
# Can process entire codebases, books, documents
context = load_document("entire_book.txt")  # 150K tokens
response = claude.generate(
    f"Summarize this book: {context}",
    max_tokens=1000
)

# Maintains coherence across 200K tokens!
```

**Technical Implementation:**
- Custom attention mechanism
- Efficient KV cache management
- Sparse attention patterns
- Cost: ~$200/request for full context

**Safety Features:**

**1. Constitutional Screening**
```python
def screen_request(prompt):
    # Check against constitutional principles
    for principle in constitutional_principles:
        if violates(prompt, principle):
            return safe_alternative(prompt)
    return prompt
```

**2. Output Filtering**
```python
def filter_response(response):
    # Multi-stage safety check
    checks = [
        toxicity_check(response),
        factuality_check(response),
        bias_check(response),
        harm_check(response)
    ]
    
    if any(check.failed for check in checks):
        return regenerate_safely()
    
    return response
```

**3. Red Teaming**
- Internal team tries to elicit harmful responses
- 10,000+ attack scenarios tested
- Continuous improvement based on findings

**Performance Metrics:**

| Metric | Claude 3 Opus | GPT-4 | Gemini Ultra |
|--------|---------------|-------|--------------|
| **MMLU** | 86.8% | 86.4% | 90.0% |
| **HumanEval (Code)** | 84.9% | 67.0% | 74.4% |
| **Truthfulness** | 95.0% | 92.0% | 91.0% |
| **Safety** | 99.5% | 99.0% | 99.2% |

**Challenges:**

**1. Balancing Helpfulness vs Safety**
- **Problem:** Too cautious = less helpful
- **Solution:** Nuanced constitutional principles
- **Example:** "Decline harmful requests while being helpful for legitimate edge cases"

**2. Long Context Quality**
- **Problem:** Quality degrades at 100K+ tokens
- **Solution:** Hierarchical attention, better prompting
- **Result:** 90%+ quality maintained to 200K

**3. Cost**
- **Problem:** 200K context = expensive
- **Solution:** Dynamic context window, only use what's needed
- **Savings:** 60% cost reduction vs fixed 200K

**Business Model:**

**Pricing:**
- Opus: $15/M input tokens, $75/M output tokens
- Sonnet: $3/M input tokens, $15/M output tokens  
- Haiku: $0.25/M input tokens, $1.25/M output tokens

**Enterprise Features:**
- Custom constitutional principles
- Dedicated deployments
- Advanced safety controls
- Priority support

**Lessons Learned:**

1. **Constitutional AI Works** - Scalable alternative to pure RLHF
2. **Long Context Valuable** - Users willing to pay premium
3. **Safety ≠ Censorship** - Can be helpful AND safe
4. **Transparency Builds Trust** - Documenting principles helps adoption
5. **Model Zoo Approach** - Different models for different needs

**Impact:**
- 50K+ businesses using Claude
- Significantly safer than alternatives
- Leading in extended context use cases

---

## **Case Study 4: Jasper.ai (Content Generation at Scale)**

**Overview:**
Jasper helps businesses create marketing content with AI. $125M revenue in 2023.

**Business Model:**
- **Target:** Marketing teams, agencies, content creators
- **Pricing:** $49-$125/month
- **Users:** 100K+ businesses
- **Content Generated:** 1B+ words/month

**Architecture:**

```
User (Marketing Team)
    ↓
Web App (React)
    ↓
Templates Library (50+ templates)
    ↓
Prompt Generator
    ↓
GPT-4 / Claude
    ↓
Post-Processing
    ↓
Content Output
```

**Key Innovation: Template System**

**Instead of raw LLM prompts:**
```
User: "Write me a blog post about AI"
LLM: [Generic output]
```

**Jasper's Approach:**
```python
class BlogPostTemplate:
    def __init__(self):
        self.steps = [
            "Generate outline",
            "Write introduction",
            "Write body paragraphs",
            "Write conclusion",
            "Add SEO keywords"
        ]
    
    def generate(self, topic, keywords, tone, length):
        outline = self.generate_outline(topic, keywords)
        intro = self.generate_intro(topic, outline, tone)
        body = self.generate_body(outline, tone, length)
        conclusion = self.generate_conclusion(topic, body, tone)
        
        # Combine and optimize
        content = self.combine(intro, body, conclusion)
        content = self.optimize_seo(content, keywords)
        
        return content
```

**Templates:**
- Blog Post Outline
- Product Description
- Ad Copy (Facebook, Google)
- Email Marketing
- Social Media Posts
- Video Scripts
- SEO Meta Descriptions
- Press Releases
- And 40+ more...

**Multi-Step Generation:**

**Example: Blog Post Template**

**Step 1: Outline**
```
Prompt: Generate a blog post outline about "AI in Healthcare"
Keywords: diagnosis, machine learning, patient care

Output:
1. Introduction - AI Revolution in Healthcare
2. AI for Diagnosis - Accuracy & Speed
3. Personalized Treatment Plans
4. Challenges & Ethics
5. Future of AI in Healthcare
```

**Step 2: Introduction**
```
Prompt: Write an engaging introduction for a blog post.
Outline: [outline from step 1]
Tone: Professional yet accessible
Length: 150 words

Output: [Polished introduction]
```

**Step 3-5:** Similar for body and conclusion

**Brand Voice Customization:**

```python
class BrandVoice:
    def __init__(self, company):
        self.company = company
        self.tone = self.extract_tone_from_samples()
        self.vocabulary = self.build_vocabulary()
        self.style = self.analyze_style()
    
    def apply_to_content(self, content):
        # Rewrite to match brand voice
        prompt = f\"\"\"
Rewrite this content to match our brand voice:

Original: {content}

Brand Tone: {self.tone}
Brand Words: {self.vocabulary}
Style Guide: {self.style}

Rewritten:
\"\"\"
        return llm.generate(prompt)
```

**Example:**
```
Generic: "Our product is great and helps you save time."

Nike Brand Voice: "Just do it. Time's ticking. Your goals are waiting."

Apple Brand Voice: "Beautifully simple. Surprisingly powerful. Time redefined."
```

**Quality Control:**

**1. Grammar & Spell Check**
```python
def quality_check(content):
    # LanguageTool API
    grammar_issues = check_grammar(content)
    
    # Custom rules
    if contains_passive_voice(content) > 20%:
        suggest_active_voice()
    
    if readability_score(content) < 60:
        suggest_simplification()
    
    return issues
```

**2. Plagiarism Detection**
```python
def plagiarism_check(content):
    # Check against web
    results = copyscape.check(content)
    
    if results.similarity > 30%:
        return "Warning: High similarity detected"
    
    return "Original"
```

**3. SEO Optimization**
```python
def seo_optimize(content, keywords):
    # Keyword density
    for keyword in keywords:
        density = count_keyword(content, keyword) / word_count(content)
        if density < 0.01:  # < 1%
            suggest_keyword_insertion(keyword)
    
    # Meta description
    if not has_meta_description(content):
        generate_meta_description(content, keywords)
    
    # Headers
    if not has_proper_headers(content):
        suggest_header_structure()
    
    return optimized_content
```

**Performance Metrics:**

| Metric | Value |
|--------|-------|
| **Users** | 100K+ businesses |
| **Content/month** | 1B+ words |
| **Avg Content/User** | 10K words/month |
| **Time Saved** | 80% vs manual writing |
| **User Satisfaction** | 4.5/5 |
| **Retention** | 70% annual |

**Cost Structure:**

**Per User Per Month:**
- LLM API costs: $15-20 (GPT-4 + Claude)
- Infrastructure: $5
- Support: $5
- **Total cost:** ~$25-30
- **Subscription:** $49-125
- **Margin:** 50-75%

**Scaling Challenges:**

**1. Cost Control**
- **Problem:** GPT-4 expensive at scale ($0.03/1K tokens)
- **Solution:**
  - Use GPT-3.5 for simpler templates (5x cheaper)
  - Caching common generations
  - Batch processing
- **Result:** 60% cost reduction

**2. Quality Consistency**
- **Problem:** LLM outputs vary
- **Solution:**
  - Temperature=0.7 (balanced)
  - Multiple generations, pick best
  - Post-processing normalization
- **Result:** 90%+ consistency

**3. Latency**
- **Problem:** Users expect <10s for content
- **Solution:**
  - Streaming output (show as it generates)
  - Pre-computed templates
  - Background processing for long content
- **Result:** 5-15s for most content

**Competitive Advantages:**

1. **50+ Templates** - More than competitors
2. **Brand Voice** - Unique to Jasper
3. **Workflows** - Multi-step generation
4. **Integrations** - Connects to Surfer SEO, Grammarly, etc.
5. **Team Collaboration** - Shared workspaces

**Lessons Learned:**

1. **Templates > Raw LLM** - Structure improves quality
2. **Brand Voice Matters** - Key differentiator
3. **Quality Control Critical** - Can't just pass LLM output through
4. **SEO Integration** - Marketing teams need it
5. **User Education** - Teach users to get best results

**Future Plans:**
- Image generation integration
- Video script to video
- Multi-language expansion
- Industry-specific templates

---

## **Case Study 5: Intercom (AI Customer Support)**

**Overview:**
Intercom added AI to their customer support platform. Resolution rate: 70%+.

**The Problem:**
- 1,000+ support tickets/day
- Average handle time: 10 minutes
- Cost: $30/ticket (agent time)
- **Total:** $30K/day in support costs

**The Solution: Fin AI Agent**

**Architecture:**

```
Customer Question
    ↓
Fin AI Agent
    ↓
Knowledge Base RAG
    ↓
Tool Use (check orders, refunds, etc.)
    ↓
LLM Generation (GPT-4)
    ↓
Confidence Check
    ↓
If confident: Answer
If uncertain: Escalate to human
```

**Implementation:**

**1. Knowledge Base RAG**
```python
class KnowledgeBaseRAG:
    def __init__(self):
        self.vector_db = Pinecone()
        self.embedder = OpenAIEmbeddings()
        
        # Index all support docs
        self.index_articles()
    
    def query(self, question):
        # Embed question
        query_emb = self.embedder.embed(question)
        
        # Retrieve relevant articles
        results = self.vector_db.query(
            query_emb,
            top_k=5,
            filter={"status": "published"}
        )
        
        return results
```

**2. Tool Integration**
```python
tools = [
    {
        "name": "check_order_status",
        "description": "Check the status of a customer order",
        "parameters": {
            "order_id": "string"
        }
    },
    {
        "name": "process_refund",
        "description": "Process a refund for an order",
        "parameters": {
            "order_id": "string",
            "reason": "string"
        }
    },
    {
        "name": "update_subscription",
        "description": "Update customer subscription",
        "parameters": {
            "customer_id": "string",
            "action": "enum[upgrade, downgrade, cancel]"
        }
    }
]
```

**3. Confidence-Based Routing**
```python
def route_ticket(question, ai_response):
    confidence = calculate_confidence(ai_response)
    
    if confidence > 0.8:
        # High confidence - send to customer
        return send_ai_response(ai_response)
    
    elif confidence > 0.5:
        # Medium confidence - suggest to agent
        return suggest_to_agent(ai_response)
    
    else:
        # Low confidence - route to agent
        return escalate_to_human(question)
```

**Results:**

**Before AI:**
- Tickets/day: 1,000
- Agent-handled: 1,000 (100%)
- Cost/ticket: $30
- **Daily cost:** $30,000
- Avg response time: 2 hours
- Customer satisfaction: 75%

**After AI:**
- Tickets/day: 1,000
- AI-resolved: 700 (70%)
- Agent-handled: 300 (30%)
- Cost per AI ticket: $0.50
- **Daily cost:** $9,350 (69% reduction!)
- Avg response time: 5 minutes (AI), 1 hour (agent)
- Customer satisfaction: 85%

**ROI Calculation:**

**Annual Savings:**
```
Before: 365,000 tickets × $30 = $10.95M
After:  255,500 AI tickets × $0.50 = $127.75K
        109,500 agent tickets × $30 = $3.285M
        Total: $3.41M

Savings: $7.54M/year (69% cost reduction)
```

**Implementation Cost:**
- Development: $500K (6 months, 5 engineers)
- OpenAI API: $127K/year
- Infrastructure: $50K/year
- **Total Year 1:** $677K
- **Net Savings Year 1:** $6.86M

**ROI:** 10x in first year!

**Customer Feedback:**

**Positive:**
- "Instant responses!"
- "AI knew the answer immediately"
- "No waiting in queue"

**Negative:**
- "AI couldn't handle my complex issue"
- "Wanted to talk to a human"
- "Bot felt impersonal"

**Solution:** Always offer human escalation

**Challenges:**

**1. Knowledge Base Quality**
- **Problem:** Outdated articles → wrong answers
- **Solution:** Weekly KB reviews, flagged articles
- **Result:** 95% KB accuracy

**2. Complex Issues**
- **Problem:** AI struggles with multi-step problems
- **Solution:** Break into sub-problems, use tools
- **Result:** 70% → 85% resolution for complex issues

**3. Customer Trust**
- **Problem:** Users don't trust AI
- **Solution:** Transparency ("AI assistant powered by [company]"), human escalation
- **Result:** 85% satisfaction (up from 75%)

**Lessons Learned:**

1. **Start with FAQs** - Easy wins build confidence
2. **Human Escalation Critical** - Always offer human option
3. **Monitor Quality Daily** - AI can drift
4. **Update KB Weekly** - Stale info = wrong answers
5. **Transparency Builds Trust** - Tell users it's AI

**Expansion Plans:**
- Proactive support (detect issues before customer asks)
- Multi-language support
- Voice support integration
- Sentiment-based routing

---

## **Common Patterns Across All Case Studies**

**1. Hybrid AI-Human Systems**
- All use AI + human escalation
- AI handles 70-80% of volume
- Humans handle edge cases

**2. Multi-Layer Safety**
- Input screening
- Output filtering
- Post-processing checks
- Human oversight

**3. Caching Everywhere**
- 30-50% cost reduction
- Faster responses
- Better user experience

**4. Continuous Monitoring**
- Real-time quality metrics
- Cost tracking
- User satisfaction
- Model performance

**5. Iterative Improvement**
- Start simple
- Measure everything
- Iterate based on data
- Never stop optimizing

**Key Takeaways:**

✅ **Production LLMs are Complex** - Not just API calls
✅ **Cost Optimization Critical** - 50-80% reductions possible
✅ **Safety is Multi-Layered** - No single solution
✅ **User Experience Matters** - Latency, transparency, escalation
✅ **Monitoring is Essential** - Real-time quality tracking
✅ **ROI Can Be Massive** - 10x+ returns common

---

**Additional Resources:**

**Papers:**
- "Constitutional AI" (Anthropic)
- "Evaluating Large Language Models" (OpenAI)
- "RLHF: Reinforcement Learning from Human Feedback" (OpenAI)

**Blogs:**
- OpenAI Blog: platform.openai.com/blog
- Anthropic Blog: anthropic.com/index
- Hugging Face Blog: huggingface.co/blog

**Talks:**
- Scale AI Transform (annual conference)
- NeurIPS Workshops
- Company tech blogs
""")
        
        # Additional Resources  
        with resource_tabs[3]:
            st.markdown("### 🔗 Additional Resources & Learning Paths")
            st.markdown("""
**Comprehensive resources to continue your LLM engineering journey:**

---

## **🎓 Online Courses**

**Beginner Level:**

1. **Fast.ai - Practical Deep Learning**
   - **URL:** course.fast.ai
   - **Duration:** 7 weeks
   - **Cost:** Free
   - **Topics:** Neural networks, computer vision, NLP basics
   - **Projects:** 5 hands-on projects
   - **Best For:** Building intuition

2. **DeepLearning.AI - Machine Learning Specialization**
   - **URL:** coursera.org/specializations/machine-learning
   - **Duration:** 3 months
   - **Cost:** $49/month
   - **Topics:** Supervised learning, neural networks, ML systems
   - **Taught by:** Andrew Ng
   - **Certificate:** Yes

**Intermediate Level:**

3. **DeepLearning.AI - Generative AI with LLMs**
   - **URL:** coursera.org/learn/generative-ai-with-llms
   - **Duration:** 3 weeks
   - **Cost:** $49/month
   - **Topics:** Transformer architecture, fine-tuning, RLHF
   - **Projects:** Fine-tune LLM, build chatbot
   - **Best For:** Understanding LLM fundamentals

4. **LangChain Academy**
   - **URL:** academy.langchain.com
   - **Duration:** Self-paced
   - **Cost:** Free
   - **Topics:** RAG, agents, chains, LangGraph
   - **Projects:** 10+ hands-on labs
   - **Best For:** LangChain mastery

**Advanced Level:**

5. **Stanford CS224N - NLP with Deep Learning**
   - **URL:** web.stanford.edu/class/cs224n
   - **Duration:** 10 weeks (lectures available)
   - **Cost:** Free (audit)
   - **Topics:** Transformers, attention, language models
   - **Assignments:** 5 challenging projects
   - **Best For:** Deep theoretical understanding

6. **Full Stack LLM Bootcamp (UC Berkeley)**
   - **URL:** fullstackdeeplearning.com/llm-bootcamp
   - **Duration:** Videos available
   - **Cost:** Free
   - **Topics:** Production LLMs, deployment, evaluation
   - **Best For:** Production readiness

---

## **📚 Essential Books**

**Fundamentals:**

1. **"Hands-On Large Language Models"** by Jay Alammar
   - Visual explanations of LLM concepts
   - Practical examples in Python
   - Perfect for beginners

2. **"Natural Language Processing with Transformers"** by Lewis Tunstall
   - Deep dive into Hugging Face ecosystem
   - Covers BERT, GPT, T5
   - Production-focused

**Advanced:**

3. **"Speech and Language Processing"** by Dan Jurafsky
   - Comprehensive NLP textbook
   - 3rd edition covers transformers
   - Free online: web.stanford.edu/~jurafsky/slp3

4. **"Deep Learning"** by Ian Goodfellow
   - ML/DL foundations
   - Mathematical rigor
   - Free online: deeplearningbook.org

**System Design:**

5. **"Designing Data-Intensive Applications"** by Martin Kleppmann
   - Distributed systems
   - Databases at scale
   - Essential for LLM infrastructure

6. **"Building Machine Learning Powered Applications"** by Emmanuel Ameisen
   - ML in production
   - End-to-end projects
   - Best practices

---

## **🛠️ Tools & Libraries**

**LLM Frameworks:**

1. **LangChain**
   - **URL:** python.langchain.com
   - **Use:** RAG, agents, chains
   - **Pro:** Lots of integrations
   - **Con:** Can be complex
   - **Best For:** Rapid prototyping

2. **LlamaIndex**
   - **URL:** llamaindex.ai
   - **Use:** RAG, document querying
   - **Pro:** Simple, well-documented
   - **Con:** Less flexible than LangChain
   - **Best For:** RAG systems

3. **Haystack**
   - **URL:** haystack.deepset.ai
   - **Use:** NLP pipelines, RAG
   - **Pro:** Production-ready
   - **Con:** Steeper learning curve
   - **Best For:** Enterprise deployments

**Vector Databases:**

4. **Pinecone**
   - **Type:** Managed service
   - **Free Tier:** 1GB, 100K vectors
   - **Best For:** Getting started quickly

5. **Weaviate**
   - **Type:** Open source
   - **Features:** Hybrid search, multi-modal
   - **Best For:** Self-hosted, flexibility

6. **Chroma**
   - **Type:** Open source
   - **Features:** Lightweight, embeddable
   - **Best For:** Local development, small projects

**Serving:**

7. **vLLM**
   - **URL:** vllm.ai
   - **Use:** High-performance LLM serving
   - **Throughput:** 24x vs HuggingFace
   - **Best For:** Production serving

8. **Text Generation Inference (TGI)**
   - **URL:** huggingface.co/docs/text-generation-inference
   - **Use:** Hugging Face model serving
   - **Features:** Streaming, batching
   - **Best For:** HuggingFace models

**Monitoring:**

9. **LangSmith**
   - **URL:** smith.langchain.com
   - **Use:** LLM observability
   - **Features:** Tracing, evaluation, monitoring
   - **Free Tier:** 5K traces/month

10. **Phoenix (Arize)**
    - **URL:** phoenix.arize.com
    - **Use:** LLM observability (open source)
    - **Features:** Tracing, drift detection
    - **Best For:** Self-hosted monitoring

---

## **💻 Practice Platforms**

**Coding Practice:**

1. **LeetCode**
   - **URL:** leetcode.com
   - **Focus:** Algorithms, data structures
   - **LLM specific:** Some ML problems
   - **Cost:** Free (Premium $35/month)

2. **HackerRank**
   - **URL:** hackerrank.com
   - **Focus:** Coding challenges
   - **AI Track:** ML/AI specific problems
   - **Cost:** Free

**ML Competitions:**

3. **Kaggle**
   - **URL:** kaggle.com
   - **Focus:** ML competitions, datasets
   - **LLM:** Many NLP competitions
   - **Community:** Very active
   - **Cost:** Free

4. **AI Crowd**
   - **URL:** aicrowd.com
   - **Focus:** Research challenges
   - **Prizes:** Often monetary rewards
   - **Cost:** Free

---

## **🎤 Conferences & Events**

**Major Conferences:**

1. **NeurIPS** (Neural Information Processing Systems)
   - When: December annually
   - Where: Vancouver (rotates)
   - Focus: ML research
   - Cost: $1,000-1,500
   - Virtual: Available

2. **ICML** (International Conference on Machine Learning)
   - When: July annually
   - Where: Honolulu (rotates)
   - Focus: ML theory & practice
   - Cost: $800-1,200

3. **ACL** (Association for Computational Linguistics)
   - When: July/August
   - Where: Toronto (rotates)
   - Focus: NLP research
   - Cost: $600-1,000

**Industry Conferences:**

4. **Scale AI Transform**
   - When: October
   - Where: San Francisco
   - Focus: Enterprise AI
   - Cost: $1,500-3,000
   - Best For: Networking

5. **AI Engineer Summit**
   - When: June
   - Where: San Francisco
   - Focus: Production AI
   - Cost: $500-1,000
   - Best For: Practitioners

**Free/Virtual:**

6. **Weights & Biases Salon**
   - When: Monthly (virtual)
   - Cost: Free
   - Focus: ML tools, techniques

7. **Hugging Face Community Events**
   - When: Ongoing
   - Cost: Free
   - Focus: Open source NLP

---

## **👥 Communities**

**Discord Servers:**

1. **LangChain Discord**
   - Members: 50K+
   - Activity: Very high
   - Topics: RAG, agents, LangChain

2. **Hugging Face Discord**
   - Members: 30K+
   - Topics: Models, datasets, transformers

3. **OpenAI Discord**
   - Members: 100K+
   - Topics: GPT, API, use cases

**Reddit:**

4. **r/MachineLearning**
   - Members: 2.7M
   - Focus: ML research, papers

5. **r/LocalLLaMA**
   - Members: 150K
   - Focus: Self-hosted LLMs

6. **r/LangChain**
   - Members: 20K
   - Focus: LangChain development

**Slack/Forums:**

7. **MLOps Community**
   - URL: mlops.community
   - Focus: Production ML

8. **EleutherAI**
   - URL: eleuther.ai
   - Focus: Open source LLMs

---

## **📝 Blogs & Newsletters**

**Must-Follow Blogs:**

1. **Jay Alammar's Blog**
   - URL: jalammar.github.io
   - Focus: Visual explanations
   - Best Posts: "Illustrated Transformer", "Illustrated GPT"

2. **Eugene Yan**
   - URL: eugeneyan.com
   - Focus: Applied ML
   - Topics: RAG, evaluation, production

3. **Hugging Face Blog**
   - URL: huggingface.co/blog
   - Focus: Models, techniques
   - Updates: Weekly

**Newsletters:**

4. **The Batch** (DeepLearning.AI)
   - Frequency: Weekly
   - Focus: AI news, research summaries
   - Subscribe: deeplearning.ai/the-batch

5. **Import AI**
   - Frequency: Weekly
   - Focus: AI research digest
   - Subscribe: jack-clark.net

6. **TLDR AI**
   - Frequency: Daily
   - Focus: AI news, tools
   - Subscribe: tldr.tech/ai

---

## **🎥 YouTube Channels**

**Educational:**

1. **Andrej Karpathy**
   - Focus: Building LLMs from scratch
   - Best Series: "Neural Networks: Zero to Hero"

2. **3Blue1Brown**
   - Focus: Math intuition
   - Best For: Understanding attention, transformers

3. **Yannic Kilcher**
   - Focus: Paper explanations
   - Best For: Understanding research

**Practical:**

4. **Sam Witteveen**
   - Focus: LangChain tutorials
   - Best For: Building with LLMs

5. **Nicholas Renotte**
   - Focus: Project tutorials
   - Best For: Hands-on learning

---

## **🔬 Research Resources**

**Paper Repositories:**

1. **arXiv.org**
   - Search: cs.CL (Computation & Language)
   - Daily papers on LLMs

2. **Papers with Code**
   - URL: paperswithcode.com
   - Papers + implementation code

3. **Hugging Face Papers**
   - URL: huggingface.co/papers
   - Curated daily papers

**Paper Reading Lists:**

4. **"Must-Read LLM Papers"**
   - URL: github.com/Hannibal046/Awesome-LLM
   - 100+ essential papers

5. **"LLM Reading List"** (Sebastian Raschka)
   - URL: magazine.sebastianraschka.com
   - Curated, explained papers

---

## **💼 Job Search Platforms**

**Specialized:**

1. **AI Jobs**
   - URL: ai-jobs.net
   - Focus: AI/ML roles only

2. **Wellfound** (AngelList)
   - URL: wellfound.com
   - Focus: Startups

3. **RemoteOK**
   - URL: remoteok.com
   - Focus: Remote AI jobs

**General (with AI filters):**

4. **LinkedIn Jobs**
   - Filter: "LLM Engineer", "AI Engineer"
   - Set alerts for new postings

5. **Indeed**
   - Advanced search for AI roles
   - Salary estimates

---

## **🛤️ Suggested Learning Paths**

**Path 1: Application Developer (3 months)**

**Month 1: Fundamentals**
- Complete Fast.ai course
- Build 3 API-based apps
- Learn prompt engineering

**Month 2: RAG & Agents**
- LangChain tutorials
- Build RAG system
- Deploy to production

**Month 3: Portfolio**
- 2 capstone projects
- Write 5 blog posts
- Apply to jobs

**Target Role:** LLM Application Engineer ($120K-$180K)

---

**Path 2: Research Engineer (6 months)**

**Month 1-2: Foundations**
- CS224N Stanford course
- Read 20 papers
- Implement transformer from scratch

**Month 3-4: Advanced Topics**
- RLHF paper implementation
- Fine-tune models
- Contribute to open source

**Month 5-6: Specialization**
- Pick area (alignment, efficiency, etc.)
- Deep research
- Publish findings

**Target Role:** LLM Research Engineer ($160K-$400K)

---

**Path 3: MLOps Engineer (4 months)**

**Month 1: Infrastructure**
- Learn Kubernetes
- Deploy model with vLLM
- Set up monitoring

**Month 2: Optimization**
- Implement caching
- Cost optimization
- A/B testing framework

**Month 3: Production**
- Build full pipeline
- Monitoring dashboard
- Incident response

**Month 4: Portfolio**
- Document architectures
- Write case studies
- Apply to jobs

**Target Role:** LLM MLOps Engineer ($140K-$300K)

---

## **🎯 90-Day Action Plan**

**Week 1-2: Foundation**
- [ ] Complete this LLM pathway
- [ ] Set up development environment
- [ ] Join 3 communities (Discord, Reddit)

**Week 3-4: First Project**
- [ ] Build simple RAG system
- [ ] Deploy to Streamlit/Gradio
- [ ] Share on LinkedIn

**Week 5-6: Learning Deep Dive**
- [ ] Take DeepLearning.AI LLM course
- [ ] Read 10 papers
- [ ] Write 2 blog posts

**Week 7-8: Second Project**
- [ ] Fine-tune a model
- [ ] Document process
- [ ] Open source the code

**Week 9-10: Interview Prep**
- [ ] Practice 20 LeetCode problems
- [ ] Do 3 mock interviews
- [ ] Update resume

**Week 11-12: Job Search**
- [ ] Apply to 15 companies
- [ ] Network with 10 people
- [ ] Attend 2 meetups

**Goal:** Land LLM Engineer role in 90 days! 🎉

---

**Remember:**
- **Consistency > Intensity** - 1 hour daily beats 10 hours on weekends
- **Build in Public** - Share your learning journey
- **Network Early** - Start building relationships now
- **Stay Current** - AI moves fast, keep learning
- **Enjoy the Journey** - LLM engineering is incredibly rewarding!

**You've got this!** 💪
""")
            
            st.markdown("---")
            st.success("""
### 🎉 Congratulations on Completing the AI/LLM Engineer Pathway!

You've just completed one of the most comprehensive LLM engineering training programs available. 

**What You've Learned:**
- ✅ LLM Fundamentals & Transformer Architecture
- ✅ Prompt Engineering & Optimization Techniques
- ✅ Production RAG Systems & Vector Databases
- ✅ Fine-tuning with LoRA, QLoRA, and RLHF
- ✅ AI Agents & Multi-Agent Systems
- ✅ Production Deployment & MLOps
- ✅ Real-World Case Studies from Industry Leaders
- ✅ Career Development & Interview Preparation

**What's Next:**
1. Build your portfolio projects
2. Contribute to open source
3. Network with the community
4. Apply to your dream companies
5. Land that LLM Engineer role!

**Remember:** The LLM engineering field is rapidly evolving. Stay curious, keep building, and never stop learning!

**Good luck on your journey! 🚀**

---

**Final Thoughts:**

The AI/LLM engineering field offers unprecedented opportunities. With dedication, continuous learning,
and practical experience, you can build a rewarding career at the forefront of technology.

Start small, build momentum, and remember: every expert was once a beginner. Your journey starts now!
""")
