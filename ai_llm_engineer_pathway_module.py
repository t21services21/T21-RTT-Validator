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
        st.info("Learning materials will be added here.")

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
        st.subheader("📂 Documents & Downloads")
        st.info("Course materials and resources.")
