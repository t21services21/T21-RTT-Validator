import streamlit as st
from typing import Dict, Any

try:
    from tquk_course_assignment import get_learner_enrollments
except Exception:  # pragma: no cover
    def get_learner_enrollments(email: str):
        return []

try:
    from tquk_pdf_converter import create_unit_pdf
except Exception:  # pragma: no cover
    def create_unit_pdf(unit_number: int, unit_name: str, content: str):
        return content.encode("utf-8")

try:
    from tquk_evidence_tracking import (
        render_evidence_submission_form,
        render_evidence_tracking,
    )
except Exception:  # pragma: no cover
    def render_evidence_submission_form(email: str, course_id: str, unit_number: int):
        st.info("Evidence submission system is not available in this environment.")

    def render_evidence_tracking(email: str, course_id: str):
        st.info("Evidence tracking system is not available in this environment.")

try:
    from video_library import get_all_videos
except Exception:  # pragma: no cover
    def get_all_videos(category: str = None, week: int = None, competency: str = None):
        return []


COURSE_ID = "data_engineer_pathway"
COURSE_NAME = "Data Engineer Pathway"


UNITS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Data Engineering Fundamentals & Pipelines",
        "level": "Intermediate",
        "glh": 24,
        "credits": 4,
    },
    2: {
        "name": "Data Warehousing & Modeling",
        "level": "Intermediate",
        "glh": 24,
        "credits": 4,
    },
    3: {
        "name": "Batch Processing at Scale",
        "level": "Intermediate/Advanced",
        "glh": 30,
        "credits": 5,
    },
    4: {
        "name": "Stream Processing & Real-time Data",
        "level": "Advanced",
        "glh": 30,
        "credits": 5,
    },
    5: {
        "name": "Cloud Data Platforms & Infrastructure",
        "level": "Intermediate/Advanced",
        "glh": 30,
        "credits": 5,
    },
    6: {
        "name": "Data Quality, Orchestration & Monitoring",
        "level": "Advanced",
        "glh": 24,
        "credits": 4,
    },
    7: {
        "name": "Data Engineering Capstone Project",
        "level": "Advanced",
        "glh": 48,
        "credits": 8,
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
        st.metric("Progress", f"{progress}%")
        st.progress(progress / 100 if progress else 0)
    with col2:
        st.metric("Units Completed", f"{units_completed}/{total_units}")
    with col3:
        st.metric("Status", enrollment.get("status", "in_progress").title())


def _render_unit_learning_materials(unit_number: int):
    unit = UNITS[unit_number]
    st.markdown(f"### Unit {unit_number}: {unit['name']}")
    st.caption(
        f"Level: {unit['level']} • Suggested hours: {unit['glh']} • Suggested credits: {unit['credits']}"
    )

    if unit_number == 1:
        st.markdown("#### 📘 What does a data engineer do?")
        st.markdown(
            """Data engineers build and maintain the infrastructure and pipelines
that make data accessible, reliable and ready for analysis and ML.

- Design and implement data pipelines (ETL/ELT).
- Ensure data quality, reliability and performance.
- Work with data warehouses, lakes and streaming systems.

You will see how data engineers enable analysts, scientists and business
users to work with data at scale.
"""
        )

        st.markdown("#### 🔄 ETL vs ELT")
        st.markdown(
            """You will learn:

- **ETL** (Extract, Transform, Load): transform data before loading into
  the warehouse.
- **ELT** (Extract, Load, Transform): load raw data first, transform
  inside the warehouse.
- When to use each pattern and trade-offs.
"""
        )

        st.markdown("#### 🛠️ Building your first pipeline")
        st.markdown(
            """You will build a simple pipeline that:

- Extracts data from a source (CSV, API, database).
- Applies basic transformations (cleaning, filtering).
- Loads results into a target system.
"""
        )
    elif unit_number == 2:
        st.markdown("#### 📘 Why data warehousing?")
        st.markdown(
            """Data warehouses centralise data from multiple sources for
analytics and reporting. This unit covers:

- Dimensional modeling (facts and dimensions).
- Star and snowflake schemas.
- Slowly changing dimensions (SCD).
"""
        )

        st.markdown("#### ⭐ Star schema design")
        st.markdown(
            """You will practise:

- Identifying fact tables (transactions, events).
- Designing dimension tables (customers, products, time).
- Building a simple star schema for a business domain.
"""
        )

        st.markdown("#### 🔄 Slowly changing dimensions")
        st.markdown(
            """You will understand:

- Type 1 (overwrite), Type 2 (add row), Type 3 (add column).
- When to use each SCD type.
- Implementing SCD Type 2 in a pipeline.
"""
        )
    elif unit_number == 3:
        st.markdown("#### 📘 Why batch processing at scale?")
        st.markdown(
            """When datasets are too large for single-machine tools, you need
distributed processing. This unit covers:

- Apache Spark fundamentals.
- Batch job patterns and optimisations.
- Partitioning and parallelism.
"""
        )

        st.markdown("#### ⚡ Spark basics for data engineers")
        st.markdown(
            """You will learn:

- DataFrames and transformations.
- Reading and writing data at scale.
- Common operations: filter, join, aggregate, window functions.
"""
        )

        st.markdown("#### 🗂️ Partitioning and performance")
        st.markdown(
            """You will understand:

- How partitioning affects performance.
- Choosing partition keys.
- Avoiding common performance pitfalls (shuffles, skew).
"""
        )
    elif unit_number == 4:
        st.markdown("#### 📘 Why stream processing?")
        st.markdown(
            """Real-time data needs different tools and patterns. This unit
covers:

- Event-driven architectures.
- Stream processing concepts (windows, watermarks, state).
- Tools like Kafka, Flink, or cloud streaming services.
"""
        )

        st.markdown("#### 🌊 Streaming fundamentals")
        st.markdown(
            """You will learn:

- Difference between batch and streaming.
- Event time vs processing time.
- Windowing strategies (tumbling, sliding, session).
"""
        )

        st.markdown("#### 🔗 Building a simple streaming pipeline")
        st.markdown(
            """You will build a pipeline that:

- Consumes events from a stream (e.g. Kafka topic).
- Applies transformations and aggregations.
- Writes results to a sink (database, file, another stream).
"""
        )
    elif unit_number == 5:
        st.markdown("#### 📘 Cloud data platforms")
        st.markdown(
            """Modern data engineering often happens in the cloud. This unit
covers:

- Cloud storage (S3, Azure Blob, GCS).
- Cloud data warehouses (Redshift, BigQuery, Synapse).
- Managed services for pipelines and orchestration.
"""
        )

        st.markdown("#### ☁️ Infrastructure as code")
        st.markdown(
            """You will learn:

- Defining infrastructure with code (Terraform, CloudFormation).
- Version control for infrastructure.
- Reproducible environments.
"""
        )

        st.markdown("#### 🔐 Security and access control")
        st.markdown(
            """You will understand:

- IAM roles and policies.
- Encryption at rest and in transit.
- Best practices for credentials and secrets management.
"""
        )
    elif unit_number == 6:
        st.markdown("#### 📘 Data quality and validation")
        st.markdown(
            """Pipelines must produce reliable data. This unit covers:

- Data quality checks and assertions.
- Schema validation and evolution.
- Handling bad data gracefully.
"""
        )

        st.markdown("#### 🎼 Workflow orchestration")
        st.markdown(
            """You will learn:

- Orchestration tools (Airflow, Prefect, Dagster).
- Defining DAGs (directed acyclic graphs).
- Scheduling, retries and dependencies.
"""
        )

        st.markdown("#### 📊 Monitoring and alerting")
        st.markdown(
            """You will understand:

- Metrics to monitor (latency, throughput, errors).
- Setting up alerts for pipeline failures.
- Incident response and debugging strategies.
"""
        )
    elif unit_number == 7:
        st.markdown("#### 📘 Capstone goals")
        st.markdown(
            """The Data Engineer capstone demonstrates end-to-end ownership of a
data pipeline project, from design to production-ready implementation.
"""
        )

        st.markdown("#### 🧱 Suggested capstone structure")
        st.markdown(
            """A typical structure:

1. Problem & requirements (what data, who needs it, SLAs).
2. Architecture design (sources, transformations, targets).
3. Implementation (code, tests, orchestration).
4. Data quality and monitoring.
5. Documentation and runbook.
"""
        )


def render_data_engineer_pathway_module():
    learner_email = st.session_state.get("user_email", "")

    st.title("🔧 Data Engineer Pathway")
    st.success(
        "Become a job-ready data engineer who can build and maintain production data pipelines."
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
            "📊 My Progress",
            "🎓 Certificate",
        ]
    )

    # Overview
    with tabs[0]:
        st.subheader("📚 Course Overview")
        st.markdown(
            """This pathway is designed for learners who want to become **practical
 data analysts**, even if they do not have an IT background.

By the end of this pathway you will be able to:

- Turn business questions into clear, measurable analysis tasks.
- Clean and explore data using spreadsheets and SQL.
- Build insightful BI-style dashboards and reports.
- Use Python as a power tool for heavier analysis.
- Design sensible metrics, run simple A/B tests and explain results.
- Complete an end-to-end analyst capstone suitable for your portfolio.
"""
        )

        st.markdown("---")
        st.markdown("### 📦 Units in this pathway")
        for unit_number, unit in UNITS.items():
            with st.expander(f"Unit {unit_number}: {unit['name']}"):
                st.write(f"Level: {unit['level']}")
                st.write(
                    f"Suggested hours: {unit['glh']} • Suggested credits: {unit['credits']}"
                )

    # Learning materials
    with tabs[1]:
        st.subheader("📖 Learning Materials")
        st.info("Use this tab as the main reading and concept reference for each unit.")

        selected_unit = st.selectbox(
            "Select a unit:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="da_materials_unit",
        )

        _render_unit_learning_materials(selected_unit)

        st.markdown("---")
        if st.button("📥 Download unit theory summary as PDF", key="da_unit_pdf"):
            unit = UNITS[selected_unit]
            content_lines = [f"# Unit {selected_unit}: {unit['name']}", ""]
            content_lines.append("High-level notes for this Data Analyst unit.")
            content_lines.append("Refer to the in-app materials, labs and notebooks for full details.")
            markdown_content = "\n".join(content_lines)
            pdf_buffer = create_unit_pdf(
                selected_unit,
                unit["name"],
                markdown_content,
            )
            st.download_button(
                label="📥 Download Unit Summary PDF",
                data=pdf_buffer,
                file_name=f"Data_Analyst_Pathway_Unit_{selected_unit}.pdf",
                mime="application/pdf",
                key="da_unit_pdf_dl",
            )

        st.markdown("---")
        st.markdown("### 📺 Session recordings for this unit")
        st.caption(
            "Videos added in the global Video Library for this unit will appear here. "
            "Tutors can upload or link recordings from the main Video Library tool."
        )

        try:
            videos = get_all_videos(week=selected_unit)
        except Exception:
            videos = []

        if not videos:
            st.info("No session recordings have been linked to this unit yet.")
        else:
            for video in videos:
                title = video.get("title", "Untitled video")
                desc = video.get("description", "")
                vimeo_id = video.get("vimeo_id")
                vimeo_url = video.get("vimeo_url")

                with st.expander(f"🎥 {title}"):
                    if desc:
                        st.write(desc)

                    if vimeo_id:
                        embed_url = f"https://player.vimeo.com/video/{vimeo_id}"
                        if vimeo_url and ("?h=" in vimeo_url or "&h=" in vimeo_url):
                            import re as _re

                            match = _re.search(r"[?&]h=([a-zA-Z0-9]+)", vimeo_url)
                            if match:
                                embed_url += f"?h={match.group(1)}"

                        st.markdown(
                            f"""
<iframe src="{embed_url}" width="640" height="360" frameborder="0" 
        allow="autoplay; fullscreen; picture-in-picture" allowfullscreen>
</iframe>
""",
                            unsafe_allow_html=True,
                        )
                    elif vimeo_url:
                        st.markdown(f"[Open video link]({vimeo_url})")
                    else:
                        st.warning(
                            "Video link not available. Please check the Video Library entry."
                        )

    # Labs & mini projects
    with tabs[2]:
        st.subheader("🧪 Labs & Mini Projects")
        st.info(
            "Each unit includes practical labs and mini projects. Tutors can adapt them to "
            "local datasets and sectors."
        )

        selected_unit = st.selectbox(
            "Choose a unit to view lab ideas:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="da_labs_unit",
        )

        st.markdown(f"### Unit {selected_unit}: {UNITS[selected_unit]['name']}")

        if selected_unit == 1:
            st.markdown("### 🔥 Unit 1: Data Engineering Fundamentals & Pipelines")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Production-Ready ETL Code!**")
            
            st.markdown("### LAB 1: Build Your First ETL Pipeline (120 min)")
            st.markdown("**Objective:** Extract data from API, transform it, load to database")
            lab1_code = '''import requests
import pandas as pd
import sqlite3
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleETLPipeline:
    def __init__(self, db_path='data_warehouse.db'):
        self.db_path = db_path
        self.conn = None
    
    def extract_from_api(self, api_url):
        """Extract data from REST API"""
        logger.info(f"Extracting data from {api_url}")
        
        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Extracted {len(data)} records")
            return pd.DataFrame(data)
        
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise
    
    def extract_from_csv(self, file_path):
        """Extract data from CSV file"""
        logger.info(f"Extracting data from {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Extracted {len(df)} records from CSV")
            return df
        
        except Exception as e:
            logger.error(f"CSV extraction failed: {e}")
            raise
    
    def transform(self, df):
        """Transform and clean data"""
        logger.info("Starting transformation")
        
        initial_count = len(df)
        
        # 1. Remove duplicates
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_count - len(df)} duplicates")
        
        # 2. Handle missing values
        df = df.dropna(subset=['id', 'name'])  # Critical fields
        df['email'].fillna('unknown@company.com', inplace=True)
        
        # 3. Data type conversions
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # 4. Add metadata
        df['etl_timestamp'] = datetime.now()
        df['etl_batch_id'] = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        logger.info(f"Transformation complete: {len(df)} records ready")
        return df
    
    def load_to_database(self, df, table_name):
        """Load data to SQLite database"""
        logger.info(f"Loading {len(df)} records to {table_name}")
        
        try:
            self.conn = sqlite3.connect(self.db_path)
            
            # Load data
            df.to_sql(table_name, self.conn, if_exists='append', index=False)
            
            # Verify
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            logger.info(f"Load complete: {count} total records in {table_name}")
            
        except Exception as e:
            logger.error(f"Load failed: {e}")
            raise
        
        finally:
            if self.conn:
                self.conn.close()
    
    def run_pipeline(self, source_type, source, table_name):
        """Run complete ETL pipeline"""
        logger.info("="*60)
        logger.info("STARTING ETL PIPELINE")
        logger.info("="*60)
        
        try:
            # Extract
            if source_type == 'api':
                df = self.extract_from_api(source)
            elif source_type == 'csv':
                df = self.extract_from_csv(source)
            else:
                raise ValueError(f"Unknown source type: {source_type}")
            
            # Transform
            df_clean = self.transform(df)
            
            # Load
            self.load_to_database(df_clean, table_name)
            
            logger.info("="*60)
            logger.info("✅ ETL PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("="*60)
            
            return True
        
        except Exception as e:
            logger.error(f"❌ ETL PIPELINE FAILED: {e}")
            return False

# Example usage
pipeline = SimpleETLPipeline()

# Run pipeline from CSV
success = pipeline.run_pipeline(
    source_type='csv',
    source='customers.csv',
    table_name='customers'
)

if success:
    print("✅ Pipeline executed successfully!")'''
            st.code(lab1_code, language='python')
            
            st.markdown("### LAB 2: Advanced ETL with Error Handling & Retry Logic (90 min)")
            st.markdown("**Objective:** Build production-grade ETL with comprehensive error handling")
            lab2_code = '''import pandas as pd
import sqlite3
import time
import logging
from functools import wraps

def retry_on_failure(max_retries=3, delay=5):
    """Decorator for retry logic"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        logging.error(f"All {max_retries} attempts failed")
                        raise
        return wrapper
    return decorator

class ProductionETL:
    def __init__(self, config):
        self.config = config
        self.stats = {
            'records_extracted': 0,
            'records_transformed': 0,
            'records_loaded': 0,
            'errors': []
        }
    
    @retry_on_failure(max_retries=3, delay=5)
    def extract(self, source):
        """Extract with retry logic"""
        logging.info(f"Extracting from {source}")
        
        df = pd.read_csv(source)
        self.stats['records_extracted'] = len(df)
        
        # Validate extraction
        if len(df) == 0:
            raise ValueError("No data extracted")
        
        return df
    
    def transform_with_validation(self, df):
        """Transform with data quality checks"""
        logging.info("Starting transformation with validation")
        
        # Quality checks
        quality_report = {
            'total_records': len(df),
            'duplicates': df.duplicated().sum(),
            'missing_critical': df[['id', 'name']].isnull().sum().sum(),
            'invalid_dates': 0,
            'invalid_amounts': 0
        }
        
        # Transform
        df = df.drop_duplicates()
        df = df.dropna(subset=['id', 'name'])
        
        # Validate dates
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            quality_report['invalid_dates'] = df['date'].isnull().sum()
            df = df[df['date'].notnull()]
        
        # Validate amounts
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            quality_report['invalid_amounts'] = df['amount'].isnull().sum()
            df = df[df['amount'].notnull()]
        
        self.stats['records_transformed'] = len(df)
        
        # Log quality report
        logging.info(f"Quality Report: {quality_report}")
        
        if len(df) < quality_report['total_records'] * 0.5:
            raise ValueError(f"Too many records dropped: {quality_report['total_records']} -> {len(df)}")
        
        return df, quality_report
    
    @retry_on_failure(max_retries=3, delay=5)
    def load(self, df, table_name):
        """Load with transaction support"""
        logging.info(f"Loading to {table_name}")
        
        conn = sqlite3.connect(self.config['db_path'])
        
        try:
            # Begin transaction
            conn.execute('BEGIN TRANSACTION')
            
            # Load data
            df.to_sql(table_name, conn, if_exists='append', index=False)
            
            # Commit
            conn.commit()
            
            self.stats['records_loaded'] = len(df)
            logging.info(f"✅ Loaded {len(df)} records")
            
        except Exception as e:
            conn.rollback()
            logging.error(f"Load failed, transaction rolled back: {e}")
            raise
        
        finally:
            conn.close()
    
    def run(self, source, table_name):
        """Run complete pipeline with error handling"""
        start_time = time.time()
        
        try:
            # Extract
            df = self.extract(source)
            
            # Transform
            df_clean, quality_report = self.transform_with_validation(df)
            
            # Load
            self.load(df_clean, table_name)
            
            # Success
            duration = time.time() - start_time
            logging.info(f"✅ Pipeline completed in {duration:.2f}s")
            logging.info(f"Stats: {self.stats}")
            
            return True, self.stats
        
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"❌ Pipeline failed after {duration:.2f}s: {e}")
            return False, self.stats

# Example
config = {'db_path': 'warehouse.db'}
etl = ProductionETL(config)

success, stats = etl.run('customers.csv', 'customers')
print(f"\nPipeline Status: {'SUCCESS' if success else 'FAILED'}")
print(f"Statistics: {stats}")'''
            st.code(lab2_code, language='python')
            
            st.success("✅ Unit 1 Labs Complete: Copy and run these production-ready ETL pipelines!")
        elif selected_unit == 2:
            st.markdown("### 🔥 Unit 2: Data Warehousing & Dimensional Modeling")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Production Data Warehouse Code!**")
            
            st.markdown("### LAB 1: Design & Build Star Schema (120 min)")
            st.markdown("**Objective:** Design and implement a complete star schema for retail analytics")
            lab2_1 = '''import sqlite3
import pandas as pd
from datetime import datetime

# Create star schema for retail analytics
conn = sqlite3.connect('retail_warehouse.db')
cursor = conn.cursor()

print("🏛️ BUILDING STAR SCHEMA FOR RETAIL ANALYTICS\n" + "="*60)

# 1. DIMENSION TABLES

print("\n1. Creating Dimension Tables...")

# Dimension: Date
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    day_of_month INTEGER,
    day_of_year INTEGER,
    week_of_year INTEGER,
    month INTEGER,
    month_name VARCHAR(10),
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
)""")
print("✅ dim_date created")

# Dimension: Product
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_product (
    product_key INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    is_active BOOLEAN DEFAULT 1,
    effective_date DATE,
    expiry_date DATE
)""")
print("✅ dim_product created")

# Dimension: Customer
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(200),
    email VARCHAR(200),
    customer_segment VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    signup_date DATE,
    is_active BOOLEAN DEFAULT 1
)""")
print("✅ dim_customer created")

# Dimension: Store
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_store (
    store_key INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id VARCHAR(50) UNIQUE NOT NULL,
    store_name VARCHAR(200),
    store_type VARCHAR(50),
    region VARCHAR(100),
    country VARCHAR(100),
    manager_name VARCHAR(200),
    opening_date DATE
)""")
print("✅ dim_store created")

# 2. FACT TABLE

print("\n2. Creating Fact Table...")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_key INTEGER PRIMARY KEY AUTOINCREMENT,
    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    
    -- Measures (additive)
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    cost_amount DECIMAL(10,2),
    profit_amount DECIMAL(10,2),
    
    -- Degenerate dimensions
    order_id VARCHAR(50),
    transaction_id VARCHAR(50),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign keys
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
)""")
print("✅ fact_sales created")

# 3. CREATE INDEXES

print("\n3. Creating Indexes for Performance...")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_sales(date_key)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_fact_product ON fact_sales(product_key)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_fact_customer ON fact_sales(customer_key)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_fact_store ON fact_sales(store_key)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_fact_order ON fact_sales(order_id)')

print("✅ All indexes created")

conn.commit()

print("\n" + "="*60)
print("✅ STAR SCHEMA CREATED SUCCESSFULLY")
print("="*60)
print("\nSchema Summary:")
print("  Dimensions: 4 (Date, Product, Customer, Store)")
print("  Facts: 1 (Sales)")
print("  Indexes: 5 (optimized for queries)")

conn.close()'''
            st.code(lab2_1, language='python')
            
            st.markdown("### LAB 2: Slowly Changing Dimensions (SCD Type 2) (90 min)")
            st.markdown("**Objective:** Implement SCD Type 2 to track historical changes")
            lab2_2 = '''import sqlite3
import pandas as pd
from datetime import datetime, date

class SCDType2Manager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def create_scd_table(self):
        """Create SCD Type 2 dimension table"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_customer_scd (
            customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id VARCHAR(50) NOT NULL,
            customer_name VARCHAR(200),
            email VARCHAR(200),
            customer_segment VARCHAR(50),
            country VARCHAR(100),
            
            -- SCD Type 2 columns
            effective_date DATE NOT NULL,
            expiry_date DATE,
            is_current BOOLEAN DEFAULT 1,
            version INTEGER DEFAULT 1
        )""")
        self.conn.commit()
        print("✅ SCD Type 2 table created")
    
    def insert_new_customer(self, customer_data):
        """Insert new customer record"""
        self.cursor.execute("""
        INSERT INTO dim_customer_scd 
        (customer_id, customer_name, email, customer_segment, country, effective_date, expiry_date, is_current, version)
        VALUES (?, ?, ?, ?, ?, ?, NULL, 1, 1)
        """, (
            customer_data['customer_id'],
            customer_data['name'],
            customer_data['email'],
            customer_data['segment'],
            customer_data['country'],
            date.today()
        ))
        self.conn.commit()
        print(f"✅ New customer inserted: {customer_data['customer_id']}")
    
    def update_customer_scd(self, customer_id, new_data):
        """Update customer with SCD Type 2 logic"""
        print(f"\nUpdating customer: {customer_id}")
        
        # 1. Get current record
        self.cursor.execute("""
        SELECT customer_key, customer_name, email, customer_segment, country
        FROM dim_customer_scd
        WHERE customer_id = ? AND is_current = 1
        """, (customer_id,))
        
        current = self.cursor.fetchone()
        
        if not current:
            print(f"❌ Customer {customer_id} not found")
            return
        
        # 2. Check if data actually changed
        current_data = {
            'name': current[1],
            'email': current[2],
            'segment': current[3],
            'country': current[4]
        }
        
        has_changes = any([
            current_data['name'] != new_data.get('name', current_data['name']),
            current_data['email'] != new_data.get('email', current_data['email']),
            current_data['segment'] != new_data.get('segment', current_data['segment']),
            current_data['country'] != new_data.get('country', current_data['country'])
        ])
        
        if not has_changes:
            print("ℹ️ No changes detected, skipping update")
            return
        
        # 3. Expire current record
        self.cursor.execute("""
        UPDATE dim_customer_scd
        SET expiry_date = ?, is_current = 0
        WHERE customer_id = ? AND is_current = 1
        """, (date.today(), customer_id))
        
        # 4. Get next version number
        self.cursor.execute("""
        SELECT MAX(version) FROM dim_customer_scd WHERE customer_id = ?
        """, (customer_id,))
        max_version = self.cursor.fetchone()[0] or 0
        
        # 5. Insert new version
        self.cursor.execute("""
        INSERT INTO dim_customer_scd
        (customer_id, customer_name, email, customer_segment, country, effective_date, expiry_date, is_current, version)
        VALUES (?, ?, ?, ?, ?, ?, NULL, 1, ?)
        """, (
            customer_id,
            new_data.get('name', current_data['name']),
            new_data.get('email', current_data['email']),
            new_data.get('segment', current_data['segment']),
            new_data.get('country', current_data['country']),
            date.today(),
            max_version + 1
        ))
        
        self.conn.commit()
        print(f"✅ Customer updated: Version {max_version + 1} created")
    
    def get_customer_history(self, customer_id):
        """Get full history of customer changes"""
        query = """
        SELECT customer_key, customer_name, email, customer_segment, country,
               effective_date, expiry_date, is_current, version
        FROM dim_customer_scd
        WHERE customer_id = ?
        ORDER BY version
        """
        
        df = pd.read_sql_query(query, self.conn, params=(customer_id,))
        return df

# Example usage
scd = SCDType2Manager('retail_warehouse.db')
scd.create_scd_table()

# Insert new customer
scd.insert_new_customer({
    'customer_id': 'CUST001',
    'name': 'John Smith',
    'email': 'john@email.com',
    'segment': 'Bronze',
    'country': 'UK'
})

# Update customer (segment changed)
scd.update_customer_scd('CUST001', {
    'segment': 'Gold'  # Customer upgraded!
})

# View history
history = scd.get_customer_history('CUST001')
print("\nCustomer History:")
print(history)
print("\n✅ SCD Type 2 implementation complete!")'''
            st.code(lab2_2, language='python')
            
            st.markdown("### LAB 3: Fact Table Loading & Aggregations (90 min)")
            st.markdown("**Objective:** Load fact table and create aggregate tables for performance")
            lab2_3 = '''import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

conn = sqlite3.connect('retail_warehouse.db')

print("📊 FACT TABLE LOADING & AGGREGATIONS\n" + "="*60)

# 1. Load sample fact data
print("\n1. Loading Fact Data...")

# Generate sample sales transactions
np.random.seed(42)
num_transactions = 10000

sales_data = []
for i in range(num_transactions):
    sales_data.append({
        'date_key': int((datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y%m%d')),
        'product_key': np.random.randint(1, 101),
        'customer_key': np.random.randint(1, 1001),
        'store_key': np.random.randint(1, 11),
        'quantity': np.random.randint(1, 10),
        'unit_price': round(np.random.uniform(10, 500), 2),
        'discount_amount': round(np.random.uniform(0, 50), 2),
        'tax_amount': 0,
        'order_id': f'ORD{i:06d}',
        'transaction_id': f'TXN{i:06d}'
    })

df_sales = pd.DataFrame(sales_data)

# Calculate derived measures
df_sales['tax_amount'] = (df_sales['unit_price'] * df_sales['quantity'] * 0.2).round(2)
df_sales['total_amount'] = (df_sales['unit_price'] * df_sales['quantity'] - df_sales['discount_amount'] + df_sales['tax_amount']).round(2)
df_sales['cost_amount'] = (df_sales['unit_price'] * df_sales['quantity'] * 0.6).round(2)
df_sales['profit_amount'] = (df_sales['total_amount'] - df_sales['cost_amount']).round(2)

# Load to fact table
df_sales.to_sql('fact_sales', conn, if_exists='append', index=False)
print(f"✅ Loaded {len(df_sales):,} transactions to fact_sales")

# 2. Create aggregate tables for performance
print("\n2. Creating Aggregate Tables...")

# Daily aggregates
cursor.execute("""
CREATE TABLE IF NOT EXISTS agg_daily_sales AS
SELECT 
    date_key,
    COUNT(*) as num_transactions,
    SUM(quantity) as total_quantity,
    SUM(total_amount) as total_revenue,
    SUM(profit_amount) as total_profit,
    AVG(total_amount) as avg_transaction_value
FROM fact_sales
GROUP BY date_key
""")
print("✅ agg_daily_sales created")

# Product aggregates
cursor.execute("""
CREATE TABLE IF NOT EXISTS agg_product_sales AS
SELECT 
    product_key,
    COUNT(*) as num_sales,
    SUM(quantity) as total_quantity_sold,
    SUM(total_amount) as total_revenue,
    SUM(profit_amount) as total_profit,
    AVG(total_amount) as avg_sale_value
FROM fact_sales
GROUP BY product_key
""")
print("✅ agg_product_sales created")

# Customer aggregates
cursor.execute("""
CREATE TABLE IF NOT EXISTS agg_customer_sales AS
SELECT 
    customer_key,
    COUNT(*) as num_purchases,
    SUM(total_amount) as lifetime_value,
    AVG(total_amount) as avg_purchase_value,
    MIN(date_key) as first_purchase_date,
    MAX(date_key) as last_purchase_date
FROM fact_sales
GROUP BY customer_key
""")
print("✅ agg_customer_sales created")

conn.commit()

# 3. Query performance comparison
print("\n3. Query Performance Test...")

import time

# Query fact table directly
start = time.time()
cursor.execute('SELECT SUM(total_amount) FROM fact_sales WHERE date_key >= 20240101')
result1 = cursor.fetchone()[0]
time1 = (time.time() - start) * 1000

# Query aggregate table
start = time.time()
cursor.execute('SELECT SUM(total_revenue) FROM agg_daily_sales WHERE date_key >= 20240101')
result2 = cursor.fetchone()[0]
time2 = (time.time() - start) * 1000

print(f"\nFact table query: {time1:.2f}ms")
print(f"Aggregate table query: {time2:.2f}ms")
print(f"Speedup: {time1/time2:.1f}x faster")

print("\n✅ Star schema and aggregates ready for analytics!")'''
            st.code(lab2_3, language='python')
            
            st.success("✅ Unit 2 Labs Complete: Production data warehouse patterns mastered!")
        elif selected_unit == 3:
            st.markdown("### 🔥 Unit 3: Batch Processing at Scale with Apache Spark")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Production PySpark Code!**")
            
            st.markdown("### LAB 1: PySpark Fundamentals (120 min)")
            st.markdown("**Objective:** Master Spark DataFrames for large-scale data processing")
            lab3_1 = '''from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Initialize Spark
spark = SparkSession.builder \\
    .appName("DataEngineeringLab") \\
    .config("spark.driver.memory", "4g") \\
    .getOrCreate()

print("⚡ PYSPARK FUNDAMENTALS\n" + "="*60)

# 1. Load data
print("\n1. Loading Data...")

# Define schema for better performance
schema = StructType([
    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("product_id", StringType(), False),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("order_date", StringType(), True)
])

df = spark.read.csv('sales_data.csv', header=True, schema=schema)

print(f"✅ Loaded {df.count():,} records")
df.printSchema()
df.show(5)

# 2. Basic transformations
print("\n2. Transformations...")

# Add calculated columns
df_transformed = df.withColumn(
    "total_amount",
    col("quantity") * col("unit_price")
).withColumn(
    "discount",
    when(col("quantity") > 10, col("total_amount") * 0.1).otherwise(0)
).withColumn(
    "final_amount",
    col("total_amount") - col("discount")
)

df_transformed.show(5)

# 3. Filtering
print("\n3. Filtering...")

high_value_orders = df_transformed.filter(col("final_amount") > 1000)
print(f"High-value orders: {high_value_orders.count():,}")

# 4. Aggregations
print("\n4. Aggregations...")

# Group by customer
customer_summary = df_transformed.groupBy("customer_id").agg(
    count("order_id").alias("num_orders"),
    sum("final_amount").alias("total_spent"),
    avg("final_amount").alias("avg_order_value")
).orderBy(col("total_spent").desc())

print("\nTop 10 customers:")
customer_summary.show(10)

# 5. Joins
print("\n5. Joins...")

# Load product data
products = spark.read.csv('products.csv', header=True, inferSchema=True)

# Join sales with products
sales_with_products = df_transformed.join(
    products,
    df_transformed.product_id == products.product_id,
    "left"
)

print("\nSales with product details:")
sales_with_products.select("order_id", "product_name", "category", "final_amount").show(5)

# 6. Write results
print("\n6. Writing Results...")

customer_summary.write.mode("overwrite").parquet("output/customer_summary")
print("✅ Results written to Parquet")

spark.stop()'''
            st.code(lab3_1, language='python')
            
            st.markdown("### LAB 2: Spark Performance Optimization (90 min)")
            st.markdown("**Objective:** Optimize Spark jobs for production performance")
            lab3_2 = '''from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast
import time

spark = SparkSession.builder \\
    .appName("SparkOptimization") \\
    .config("spark.sql.adaptive.enabled", "true") \\
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \\
    .getOrCreate()

print("⚡ SPARK PERFORMANCE OPTIMIZATION\n" + "="*60)

# Load large dataset
df_large = spark.read.parquet("large_sales_data.parquet")
df_small = spark.read.csv("product_catalog.csv", header=True, inferSchema=True)

print(f"\nLarge dataset: {df_large.count():,} records")
print(f"Small dataset: {df_small.count():,} records")

# OPTIMIZATION 1: Broadcast Join
print("\n1. BROADCAST JOIN OPTIMIZATION:")

# Bad: Regular join (causes shuffle)
start = time.time()
result_regular = df_large.join(df_small, "product_id")
count_regular = result_regular.count()
time_regular = time.time() - start

print(f"Regular join: {time_regular:.2f}s")

# Good: Broadcast join (no shuffle for small table)
start = time.time()
result_broadcast = df_large.join(broadcast(df_small), "product_id")
count_broadcast = result_broadcast.count()
time_broadcast = time.time() - start

print(f"Broadcast join: {time_broadcast:.2f}s")
print(f"Speedup: {time_regular/time_broadcast:.1f}x faster")

# OPTIMIZATION 2: Partitioning
print("\n2. PARTITIONING OPTIMIZATION:")

# Repartition for better parallelism
df_partitioned = df_large.repartition(200, "customer_id")

print(f"Original partitions: {df_large.rdd.getNumPartitions()}")
print(f"After repartition: {df_partitioned.rdd.getNumPartitions()}")

# OPTIMIZATION 3: Caching
print("\n3. CACHING OPTIMIZATION:")

# Cache frequently accessed data
df_cached = df_large.filter(col("order_date") >= "2024-01-01").cache()

# First access (loads into memory)
start = time.time()
count1 = df_cached.count()
time1 = time.time() - start

# Second access (from cache)
start = time.time()
count2 = df_cached.count()
time2 = time.time() - start

print(f"First access: {time1:.2f}s")
print(f"Cached access: {time2:.2f}s")
print(f"Speedup: {time1/time2:.1f}x faster")

# OPTIMIZATION 4: Avoid Shuffles
print("\n4. SHUFFLE OPTIMIZATION:")

# Bad: Multiple shuffles
result_bad = df_large \\
    .groupBy("customer_id").count() \\
    .filter(col("count") > 5) \\
    .orderBy(col("count").desc())

# Good: Minimize shuffles
result_good = df_large \\
    .groupBy("customer_id").count() \\
    .filter(col("count") > 5) \\
    .coalesce(1) \\
    .orderBy(col("count").desc())

print("✅ Optimizations applied!")

# OPTIMIZATION 5: Predicate Pushdown
print("\n5. PREDICATE PUSHDOWN:")

# Good: Filter early (pushed down to data source)
df_filtered = spark.read.parquet("sales.parquet") \\
    .filter(col("year") == 2024) \\
    .filter(col("country") == "UK")

print("Physical plan shows filter pushed to scan")
df_filtered.explain()

print("\n✅ Spark optimization complete!")

spark.stop()'''
            st.code(lab3_2, language='python')
            
            st.success("✅ Unit 3 Labs Complete: Production Spark pipelines mastered!")
        elif selected_unit == 4:
            st.markdown("### 🔥 Unit 4: Stream Processing & Real-time Data")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Production Kafka & Streaming Code!**")
            
            st.markdown("### LAB 1: Kafka Producer & Consumer (120 min)")
            st.markdown("**Objective:** Build real-time data streaming with Kafka")
            lab4_1 = '''from kafka import KafkaProducer, KafkaConsumer
import json
import time
from datetime import datetime
import random

print("📡 KAFKA STREAMING PIPELINE\n" + "="*60)

# 1. PRODUCER - Send events to Kafka
print("\n1. Setting up Kafka Producer...")

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_event():
    """Generate sample e-commerce event"""
    return {
        'event_id': f"evt_{int(time.time()*1000)}",
        'event_type': random.choice(['page_view', 'add_to_cart', 'purchase', 'search']),
        'user_id': f"user_{random.randint(1, 1000)}",
        'product_id': f"prod_{random.randint(1, 100)}",
        'timestamp': datetime.now().isoformat(),
        'value': round(random.uniform(10, 500), 2)
    }

# Send 100 events
print("\nSending events to Kafka topic 'user_events'...")

for i in range(100):
    event = generate_event()
    producer.send('user_events', value=event)
    
    if (i + 1) % 20 == 0:
        print(f"Sent {i + 1} events...")
    
    time.sleep(0.1)  # Simulate real-time flow

producer.flush()
print("✅ 100 events sent to Kafka")

# 2. CONSUMER - Read events from Kafka
print("\n2. Setting up Kafka Consumer...")

consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='analytics_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("\nConsuming events...")

event_count = 0
event_types = {}

for message in consumer:
    event = message.value
    event_count += 1
    
    # Track event types
    event_type = event['event_type']
    event_types[event_type] = event_types.get(event_type, 0) + 1
    
    # Print sample events
    if event_count <= 5:
        print(f"Event {event_count}: {event['event_type']} by {event['user_id']}")
    
    # Stop after 100 events
    if event_count >= 100:
        break

print(f"\n✅ Consumed {event_count} events")
print(f"\nEvent type distribution:")
for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {event_type}: {count}")

consumer.close()'''
            st.code(lab4_1, language='python')
            
            st.markdown("### LAB 2: Real-time Aggregations & Windowing (90 min)")
            st.markdown("**Objective:** Compute real-time metrics with time windows")
            lab4_2 = '''from kafka import KafkaConsumer
import json
from datetime import datetime, timedelta
from collections import defaultdict
import time

print("🕰️ REAL-TIME WINDOWED AGGREGATIONS\n" + "="*60)

class StreamingAggregator:
    def __init__(self, window_size_seconds=60):
        self.window_size = window_size_seconds
        self.windows = defaultdict(lambda: {
            'count': 0,
            'total_value': 0,
            'events': []
        })
    
    def get_window_key(self, timestamp):
        """Get window key for timestamp"""
        dt = datetime.fromisoformat(timestamp)
        window_start = dt.replace(second=0, microsecond=0)
        return window_start.isoformat()
    
    def add_event(self, event):
        """Add event to appropriate window"""
        window_key = self.get_window_key(event['timestamp'])
        
        self.windows[window_key]['count'] += 1
        self.windows[window_key]['total_value'] += event.get('value', 0)
        self.windows[window_key]['events'].append(event)
    
    def get_window_stats(self, window_key):
        """Get statistics for a window"""
        window = self.windows[window_key]
        
        return {
            'window': window_key,
            'event_count': window['count'],
            'total_value': round(window['total_value'], 2),
            'avg_value': round(window['total_value'] / window['count'], 2) if window['count'] > 0 else 0
        }
    
    def detect_anomaly(self, window_key, threshold=100):
        """Detect anomalies in window"""
        stats = self.get_window_stats(window_key)
        
        if stats['event_count'] > threshold:
            return True, f"High traffic: {stats['event_count']} events"
        
        if stats['total_value'] > threshold * 50:
            return True, f"High value: ${stats['total_value']}"
        
        return False, "Normal"

# Setup consumer
consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

aggregator = StreamingAggregator(window_size_seconds=60)

print("\nProcessing real-time events with 1-minute windows...\n")

event_count = 0

for message in consumer:
    event = message.value
    event_count += 1
    
    # Add to window
    aggregator.add_event(event)
    
    # Get current window
    window_key = aggregator.get_window_key(event['timestamp'])
    stats = aggregator.get_window_stats(window_key)
    
    # Check for anomalies
    is_anomaly, reason = aggregator.detect_anomaly(window_key)
    
    # Print every 10 events
    if event_count % 10 == 0:
        print(f"Window {window_key}: {stats['event_count']} events, ${stats['total_value']:.2f} total")
        
        if is_anomaly:
            print(f"  ⚠️ ALERT: {reason}")
    
    # Stop after 100 events
    if event_count >= 100:
        break

print(f"\n✅ Processed {event_count} events across {len(aggregator.windows)} windows")

# Print all window summaries
print("\nWindow Summaries:")
for window_key in sorted(aggregator.windows.keys()):
    stats = aggregator.get_window_stats(window_key)
    print(f"  {window_key}: {stats['event_count']} events, ${stats['total_value']:.2f}")

consumer.close()'''
            st.code(lab4_2, language='python')
            
            st.success("✅ Unit 4 Labs Complete: Real-time streaming pipelines mastered!")
        elif selected_unit == 5:
            st.markdown("### 🔥 Unit 5: Cloud Data Platforms")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - AWS, GCP, Azure Code!**")
            
            st.markdown("### LAB 1: AWS Data Pipeline (120 min)")
            st.markdown("**Objective:** Build end-to-end data pipeline on AWS")
            lab5_1 = '''import boto3
import pandas as pd
from io import StringIO

print("☁️ AWS DATA PIPELINE\n" + "="*60)

# 1. S3 Operations
print("\n1. S3 Data Upload...")

s3_client = boto3.client('s3')
bucket_name = 'my-data-lake'

# Upload CSV to S3
df = pd.read_csv('local_data.csv')
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

s3_client.put_object(
    Bucket=bucket_name,
    Key='raw/sales_data.csv',
    Body=csv_buffer.getvalue()
)

print("✅ Data uploaded to S3")

# 2. AWS Glue ETL Job (PySpark)
glue_job = '''
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from S3
df = spark.read.csv("s3://my-data-lake/raw/sales_data.csv", header=True)

# Transform
df_clean = df.dropna().drop_duplicates()

# Write to processed zone
df_clean.write.mode("overwrite").parquet("s3://my-data-lake/processed/sales/")

job.commit()
'''

print("\n2. AWS Glue Job Code:")
print(glue_job)

# 3. Lambda Function for Trigger
lambda_code = '''
import json
import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    
    # Trigger Glue job when new file arrives
    response = glue.start_job_run(
        JobName='sales-etl-job',
        Arguments={
            '--input_path': event['Records'][0]['s3']['object']['key']
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Job started: {response['JobRunId']}")
    }
'''

print("\n3. Lambda Trigger Function:")
print(lambda_code)

print("\n✅ AWS pipeline complete!")'''
            st.code(lab5_1, language='python')
            
            st.markdown("### LAB 2: Infrastructure as Code with Terraform (90 min)")
            st.markdown("**Objective:** Define cloud infrastructure as code")
            lab5_2 = '''# main.tf - Terraform configuration for data pipeline

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# S3 Bucket for Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "my-company-data-lake"
  
  tags = {
    Environment = "Production"
    Purpose     = "Data Lake"
  }
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Glue Database
resource "aws_glue_catalog_database" "analytics" {
  name = "analytics_db"
}

# Glue Crawler
resource "aws_glue_crawler" "sales_crawler" {
  name          = "sales-data-crawler"
  role          = aws_iam_role.glue_role.arn
  database_name = aws_glue_catalog_database.analytics.name
  
  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/processed/sales/"
  }
}

# IAM Role for Glue
resource "aws_iam_role" "glue_role" {
  name = "glue-etl-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "glue.amazonaws.com"
      }
    }]
  })
}

# Redshift Cluster
resource "aws_redshift_cluster" "analytics_warehouse" {
  cluster_identifier = "analytics-warehouse"
  database_name      = "analytics"
  master_username    = "admin"
  master_password    = var.db_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  
  skip_final_snapshot = true
}

# Deploy commands:
# terraform init
# terraform plan
# terraform apply
# terraform destroy  # Cleanup'''
            st.code(lab5_2, language='terraform')
            
            st.success("✅ Unit 5 Labs Complete: Cloud data engineering mastered!")
        elif selected_unit == 6:
            st.markdown(
                """These labs focus on quality, orchestration and monitoring.

- **Lab 1 – Data quality checks**
  - Add assertions to a pipeline (schema, nulls, ranges).
  - Fail the pipeline if checks don't pass.

- **Lab 2 – Orchestrate with Airflow (or similar)**
  - Define a simple DAG with dependencies.
  - Schedule and run it.

- **Mini project – Monitored production pipeline**
  - Add logging, metrics and alerts to a pipeline.
  - Simulate a failure and practise debugging.
"""
            )
        elif selected_unit == 7:
            st.markdown(
                """Use these milestones to structure your Data Engineer capstone.

- **Milestone 1 – Requirements & design**
  - Define the problem, data sources and SLAs.
  - Sketch the architecture.

- **Milestone 2 – Implementation**
  - Build the pipeline with tests and orchestration.

- **Milestone 3 – Operations & documentation**
  - Add monitoring, alerts and a runbook.
  - Document the project for handoff.
"""
            )
        else:
            st.markdown(
                "Detailed lab descriptions for this unit will be added in a later build, "
                "following the same style as the Data Science pathways (clear, practical, "
                "portfolio-ready)."
            )

    # Assessments
    with tabs[3]:
        st.subheader("📝 Assessments")
        st.info(
            "Use this tab to submit evidence for each unit and to access quick-check quizzes."
        )

        if not learner_email:
            st.warning("Log in as a learner to submit assessments.")
        else:
            assessment_unit = st.selectbox(
                "Select unit for assessment submission:",
                options=list(UNITS.keys()),
                format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
                key="da_assessment_unit",
            )
            render_evidence_submission_form(learner_email, COURSE_ID, assessment_unit)

        st.markdown("---")
        st.markdown("### ✅ Quick-check quizzes (Units 1–7)")
        st.caption(
            "Short multiple-choice quizzes for each unit, starting with Units 1 and 2."
        )

        quiz_unit = st.selectbox(
            "Choose a unit for a quick-check quiz:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="da_quiz_unit",
        )

        questions: Dict[int, list] = {
            1: [
                {
                    "text": "What is the main difference between ETL and ELT?",
                    "options": [
                        "ETL transforms before loading, ELT loads then transforms",
                        "ETL is faster than ELT",
                        "ELT cannot handle large data",
                        "They are the same thing",
                    ],
                    "answer": 0,
                    "explanation": "ETL transforms data before loading into the warehouse; ELT loads raw data first and transforms inside the warehouse.",
                },
                {
                    "text": "Which is a typical responsibility of a data engineer?",
                    "options": [
                        "Designing hospital buildings",
                        "Building and maintaining data pipelines",
                        "Writing marketing copy",
                        "Managing HR processes",
                    ],
                    "answer": 1,
                    "explanation": "Data engineers build and maintain the infrastructure and pipelines that make data accessible.",
                },
                {
                    "text": "What is a data pipeline?",
                    "options": [
                        "A physical pipe",
                        "A series of data processing steps that move and transform data",
                        "A type of database",
                        "A visualization tool",
                    ],
                    "answer": 1,
                    "explanation": "Data pipelines automate the flow of data from sources through transformations to destinations.",
                },
                {
                    "text": "What is data ingestion?",
                    "options": [
                        "Deleting data",
                        "The process of importing data from sources into a storage system",
                        "Creating visualizations",
                        "Writing reports",
                    ],
                    "answer": 1,
                    "explanation": "Ingestion is the first step of bringing data into your data platform.",
                },
                {
                    "text": "Why use orchestration tools like Airflow?",
                    "options": [
                        "To delete databases",
                        "To schedule and monitor complex workflows with dependencies",
                        "To create charts",
                        "Orchestration is not useful",
                    ],
                    "answer": 1,
                    "explanation": "Orchestration tools manage task dependencies, scheduling, and monitoring.",
                },
                {
                    "text": "What is idempotency in data pipelines?",
                    "options": [
                        "Running faster",
                        "Producing the same result when run multiple times with the same input",
                        "Using more memory",
                        "Deleting data",
                    ],
                    "answer": 1,
                    "explanation": "Idempotent pipelines can be safely re-run without creating duplicates or errors.",
                },
                {
                    "text": "What is the difference between structured and unstructured data?",
                    "options": [
                        "They are the same",
                        "Structured has a defined schema; unstructured does not",
                        "Structured is always larger",
                        "Unstructured is always faster",
                    ],
                    "answer": 1,
                    "explanation": "Structured data fits into tables with schemas; unstructured includes text, images, videos.",
                },
                {
                    "text": "What is a data lake?",
                    "options": [
                        "A physical lake",
                        "A centralized repository for storing raw data in native format",
                        "A type of database",
                        "A visualization platform",
                    ],
                    "answer": 1,
                    "explanation": "Data lakes store raw data at scale, allowing flexible processing later.",
                },
                {
                    "text": "Why partition data in storage?",
                    "options": [
                        "To make queries slower",
                        "To improve query performance by reducing data scanned",
                        "To increase costs",
                        "Partitioning is not useful",
                    ],
                    "answer": 1,
                    "explanation": "Partitioning organizes data so queries only scan relevant subsets.",
                },
            ],
            2: [
                {
                    "text": "In a star schema, what is a fact table?",
                    "options": [
                        "A table storing descriptive attributes",
                        "A table storing measurable events or transactions",
                        "A table with only one row",
                        "A temporary table",
                    ],
                    "answer": 1,
                    "explanation": "Fact tables store measurable events (e.g. sales, clicks) with foreign keys to dimensions.",
                },
                {
                    "text": "What is SCD Type 2 used for?",
                    "options": [
                        "Overwriting old dimension values",
                        "Tracking historical changes by adding new rows",
                        "Deleting old records",
                        "Ignoring changes",
                    ],
                    "answer": 1,
                    "explanation": "SCD Type 2 adds a new row for each change, preserving history.",
                },
                {
                    "text": "What is a dimension table?",
                    "options": [
                        "A table storing measurements",
                        "A table storing descriptive attributes like customer names or product categories",
                        "A temporary table",
                        "A log table",
                    ],
                    "answer": 1,
                    "explanation": "Dimension tables provide context and attributes for facts.",
                },
                {
                    "text": "What is the difference between star and snowflake schemas?",
                    "options": [
                        "They are identical",
                        "Snowflake normalizes dimensions into multiple tables; star keeps them denormalized",
                        "Star is always slower",
                        "Snowflake doesn't use fact tables",
                    ],
                    "answer": 1,
                    "explanation": "Snowflake schemas normalize dimensions; star schemas denormalize for simpler queries.",
                },
                {
                    "text": "What is a surrogate key?",
                    "options": [
                        "A natural business key",
                        "An artificial key generated by the warehouse",
                        "A foreign key",
                        "A primary key from source systems",
                    ],
                    "answer": 1,
                    "explanation": "Surrogate keys are system-generated identifiers independent of business logic.",
                },
                {
                    "text": "Why use a data warehouse instead of operational databases for analytics?",
                    "options": [
                        "Warehouses are always cheaper",
                        "Warehouses are optimized for analytical queries and historical data",
                        "Operational databases are obsolete",
                        "There is no difference",
                    ],
                    "answer": 1,
                    "explanation": "Warehouses are designed for complex queries and historical analysis, not transactions.",
                },
                {
                    "text": "What is denormalization?",
                    "options": [
                        "Removing all data",
                        "Combining tables to reduce joins and improve query performance",
                        "Creating more tables",
                        "Encrypting data",
                    ],
                    "answer": 1,
                    "explanation": "Denormalization trades some redundancy for faster queries.",
                },
                {
                    "text": "What is a slowly changing dimension (SCD)?",
                    "options": [
                        "A dimension that never changes",
                        "A dimension where attributes change over time",
                        "A fact table",
                        "A temporary table",
                    ],
                    "answer": 1,
                    "explanation": "SCDs handle dimensions whose attributes change, like customer addresses.",
                },
                {
                    "text": "What is a data mart?",
                    "options": [
                        "A physical store",
                        "A subset of a data warehouse focused on a specific business area",
                        "A type of database",
                        "A visualization tool",
                    ],
                    "answer": 1,
                    "explanation": "Data marts provide focused, department-specific views of warehouse data.",
                },
            ],
            3: [
                {
                    "text": "Why use Apache Spark for batch processing?",
                    "options": [
                        "It only works on small datasets",
                        "It enables distributed processing of large datasets",
                        "It replaces all databases",
                        "It is only for streaming",
                    ],
                    "answer": 1,
                    "explanation": "Spark distributes computation across a cluster, handling datasets too large for single machines.",
                },
                {
                    "text": "What is a common cause of poor Spark performance?",
                    "options": [
                        "Using too few partitions",
                        "Data skew and excessive shuffles",
                        "Writing to disk",
                        "Using DataFrames",
                    ],
                    "answer": 1,
                    "explanation": "Data skew and shuffles can cause bottlenecks; partitioning and caching help.",
                },
                {
                    "text": "What is a shuffle in Spark?",
                    "options": [
                        "Deleting data",
                        "Redistributing data across partitions, often expensive",
                        "Reading from disk",
                        "Creating new columns",
                    ],
                    "answer": 1,
                    "explanation": "Shuffles move data between nodes and can be performance bottlenecks.",
                },
                {
                    "text": "What is the purpose of caching in Spark?",
                    "options": [
                        "To delete data",
                        "To store intermediate results in memory for reuse",
                        "To slow down processing",
                        "To encrypt data",
                    ],
                    "answer": 1,
                    "explanation": "Caching keeps frequently accessed data in memory, avoiding recomputation.",
                },
                {
                    "text": "What is data skew?",
                    "options": [
                        "Evenly distributed data",
                        "Uneven distribution of data across partitions",
                        "Fast processing",
                        "Encrypted data",
                    ],
                    "answer": 1,
                    "explanation": "Skew causes some partitions to have much more data, creating bottlenecks.",
                },
                {
                    "text": "Why use columnar storage formats like Parquet?",
                    "options": [
                        "They are always slower",
                        "They enable efficient compression and column-based queries",
                        "They only work for small data",
                        "They are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Columnar formats compress well and allow reading only needed columns.",
                },
                {
                    "text": "What is lazy evaluation in Spark?",
                    "options": [
                        "Immediate execution",
                        "Delaying computation until an action is called",
                        "Slow processing",
                        "Deleting data",
                    ],
                    "answer": 1,
                    "explanation": "Lazy evaluation builds an execution plan and optimizes before running.",
                },
                {
                    "text": "What is the difference between map and flatMap?",
                    "options": [
                        "They are identical",
                        "flatMap can produce zero or more output elements per input",
                        "map is always faster",
                        "flatMap doesn't work",
                    ],
                    "answer": 1,
                    "explanation": "flatMap flattens nested structures; map produces one output per input.",
                },
                {
                    "text": "Why use broadcast variables?",
                    "options": [
                        "To delete data",
                        "To efficiently share read-only data across all nodes",
                        "To slow down processing",
                        "They are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Broadcast variables send small lookup tables to all nodes efficiently.",
                },
            ],
            4: [
                {
                    "text": "What is the key difference between batch and stream processing?",
                    "options": [
                        "Batch processes data in real-time, streaming processes in batches",
                        "Stream processes data continuously as it arrives, batch processes in scheduled intervals",
                        "They are the same",
                        "Streaming is always slower",
                    ],
                    "answer": 1,
                    "explanation": "Streaming processes data continuously; batch processes it in scheduled chunks.",
                },
                {
                    "text": "What is a tumbling window in stream processing?",
                    "options": [
                        "A window that overlaps",
                        "A fixed-size, non-overlapping time window",
                        "A window that never closes",
                        "A window based on event count only",
                    ],
                    "answer": 1,
                    "explanation": "Tumbling windows are fixed-size and non-overlapping (e.g. every 5 minutes).",
                },
                {
                    "text": "What is a sliding window?",
                    "options": [
                        "A window that never moves",
                        "A window that overlaps with previous windows",
                        "A window based only on count",
                        "A window that deletes data",
                    ],
                    "answer": 1,
                    "explanation": "Sliding windows overlap, useful for moving averages.",
                },
                {
                    "text": "What is event time vs processing time?",
                    "options": [
                        "They are the same",
                        "Event time is when the event occurred; processing time is when it's processed",
                        "Event time is always later",
                        "Processing time doesn't matter",
                    ],
                    "answer": 1,
                    "explanation": "Event time reflects reality; processing time can lag due to delays.",
                },
                {
                    "text": "What is watermarking in stream processing?",
                    "options": [
                        "Adding logos to data",
                        "A mechanism to handle late-arriving events",
                        "Deleting old data",
                        "Encrypting streams",
                    ],
                    "answer": 1,
                    "explanation": "Watermarks define how long to wait for late events before closing windows.",
                },
                {
                    "text": "Why use message queues like Kafka?",
                    "options": [
                        "To delete messages",
                        "To decouple producers and consumers and buffer data",
                        "To slow down systems",
                        "They are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Message queues enable asynchronous, scalable data streaming.",
                },
                {
                    "text": "What is exactly-once semantics?",
                    "options": [
                        "Processing each message at least once",
                        "Guaranteeing each message is processed exactly once",
                        "Processing messages multiple times",
                        "Ignoring duplicates",
                    ],
                    "answer": 1,
                    "explanation": "Exactly-once ensures no duplicates or lost messages.",
                },
                {
                    "text": "What is stateful stream processing?",
                    "options": [
                        "Processing without memory",
                        "Maintaining state across events (e.g., running totals)",
                        "Deleting all state",
                        "Only processing one event",
                    ],
                    "answer": 1,
                    "explanation": "Stateful processing remembers information across events.",
                },
                {
                    "text": "What is backpressure?",
                    "options": [
                        "Increasing speed",
                        "A mechanism to slow down producers when consumers can't keep up",
                        "Deleting data",
                        "Encrypting streams",
                    ],
                    "answer": 1,
                    "explanation": "Backpressure prevents overwhelming downstream systems.",
                },
            ],
            5: [
                {
                    "text": "What is infrastructure as code (IaC)?",
                    "options": [
                        "Writing code in the cloud",
                        "Defining infrastructure using code files that can be versioned and automated",
                        "Manually clicking in cloud consoles",
                        "A type of database",
                    ],
                    "answer": 1,
                    "explanation": "IaC defines infrastructure in code (e.g. Terraform), enabling version control and automation.",
                },
                {
                    "text": "Which is a best practice for managing cloud credentials?",
                    "options": [
                        "Hardcode them in scripts",
                        "Use IAM roles and secrets management services",
                        "Share them in public repositories",
                        "Store them in plain text files",
                    ],
                    "answer": 1,
                    "explanation": "Use IAM roles and secrets managers to avoid hardcoding credentials.",
                },
                {
                    "text": "What is object storage?",
                    "options": [
                        "A type of database",
                        "Storage for unstructured data accessed via APIs (e.g., S3)",
                        "A file system",
                        "A cache",
                    ],
                    "answer": 1,
                    "explanation": "Object storage (like S3) stores data as objects with metadata.",
                },
                {
                    "text": "What is serverless computing?",
                    "options": [
                        "Computing without any servers",
                        "Running code without managing servers, paying only for execution time",
                        "Always more expensive",
                        "Only for websites",
                    ],
                    "answer": 1,
                    "explanation": "Serverless abstracts infrastructure management and scales automatically.",
                },
                {
                    "text": "Why use managed services in the cloud?",
                    "options": [
                        "They are always more expensive",
                        "To reduce operational overhead and focus on business logic",
                        "To have less control",
                        "They are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Managed services handle maintenance, scaling, and backups.",
                },
                {
                    "text": "What is auto-scaling?",
                    "options": [
                        "Manual resource adjustment",
                        "Automatically adjusting resources based on demand",
                        "Deleting resources",
                        "Fixed capacity",
                    ],
                    "answer": 1,
                    "explanation": "Auto-scaling adjusts compute resources to match workload.",
                },
                {
                    "text": "What is the difference between vertical and horizontal scaling?",
                    "options": [
                        "They are the same",
                        "Vertical adds more power to one machine; horizontal adds more machines",
                        "Vertical is always better",
                        "Horizontal doesn't work",
                    ],
                    "answer": 1,
                    "explanation": "Vertical scaling increases machine size; horizontal adds more machines.",
                },
                {
                    "text": "What is a VPC (Virtual Private Cloud)?",
                    "options": [
                        "A physical data center",
                        "An isolated network in the cloud",
                        "A type of database",
                        "A storage service",
                    ],
                    "answer": 1,
                    "explanation": "VPCs provide network isolation and security in cloud environments.",
                },
                {
                    "text": "Why use cloud regions and availability zones?",
                    "options": [
                        "To increase costs",
                        "For high availability and disaster recovery",
                        "They are not useful",
                        "To slow down services",
                    ],
                    "answer": 1,
                    "explanation": "Multiple zones provide redundancy and fault tolerance.",
                },
            ],
            6: [
                {
                    "text": "Why add data quality checks to pipelines?",
                    "options": [
                        "To make pipelines slower",
                        "To catch bad data early and prevent downstream issues",
                        "To delete all data",
                        "They are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Quality checks catch issues early, preventing bad data from reaching users.",
                },
                {
                    "text": "What is a DAG in workflow orchestration?",
                    "options": [
                        "A type of database",
                        "A directed acyclic graph representing task dependencies",
                        "A cloud service",
                        "A programming language",
                    ],
                    "answer": 1,
                    "explanation": "DAGs define task dependencies and execution order in orchestration tools like Airflow.",
                },
                {
                    "text": "What is data lineage?",
                    "options": [
                        "Deleting old data",
                        "Tracking data flow from sources through transformations to destinations",
                        "Creating backups",
                        "Encrypting data",
                    ],
                    "answer": 1,
                    "explanation": "Lineage shows data provenance and helps with debugging and compliance.",
                },
                {
                    "text": "Why implement data quality tests?",
                    "options": [
                        "To slow down pipelines",
                        "To validate data meets expected standards and catch issues early",
                        "To delete data",
                        "They are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Quality tests prevent bad data from propagating downstream.",
                },
                {
                    "text": "What is a data catalog?",
                    "options": [
                        "A physical book",
                        "A metadata repository documenting available datasets",
                        "A type of database",
                        "A visualization tool",
                    ],
                    "answer": 1,
                    "explanation": "Data catalogs help users discover and understand available data.",
                },
                {
                    "text": "What is monitoring in data pipelines?",
                    "options": [
                        "Ignoring errors",
                        "Tracking pipeline health, performance, and data quality",
                        "Deleting logs",
                        "Slowing down processing",
                    ],
                    "answer": 1,
                    "explanation": "Monitoring detects issues and ensures pipelines run reliably.",
                },
                {
                    "text": "What is alerting?",
                    "options": [
                        "Ignoring problems",
                        "Notifying teams when issues or thresholds are detected",
                        "Deleting data",
                        "Creating reports",
                    ],
                    "answer": 1,
                    "explanation": "Alerts enable quick response to pipeline failures or anomalies.",
                },
                {
                    "text": "Why use schema validation?",
                    "options": [
                        "To slow down processing",
                        "To ensure data matches expected structure and types",
                        "To delete data",
                        "It is not useful",
                    ],
                    "answer": 1,
                    "explanation": "Schema validation catches structural issues before they cause downstream errors.",
                },
                {
                    "text": "What is SLA (Service Level Agreement) monitoring?",
                    "options": [
                        "Ignoring deadlines",
                        "Tracking whether pipelines meet agreed performance and reliability targets",
                        "Deleting old data",
                        "Creating charts",
                    ],
                    "answer": 1,
                    "explanation": "SLA monitoring ensures pipelines meet business commitments.",
                },
            ],
            7: [
                {
                    "text": "What should a data engineering capstone include?",
                    "options": [
                        "Only raw code with no documentation",
                        "Architecture design, implementation, tests, monitoring and documentation",
                        "A single SQL query",
                        "Only a README",
                    ],
                    "answer": 1,
                    "explanation": "A strong capstone demonstrates end-to-end ownership with design, code, tests and docs.",
                },
                {
                    "text": "Why document a runbook for your pipeline?",
                    "options": [
                        "To make the project longer",
                        "To help others (or future you) operate and debug the pipeline",
                        "It is not useful",
                        "To hide information",
                    ],
                    "answer": 1,
                    "explanation": "Runbooks guide operations, troubleshooting and handoff.",
                },
                {
                    "text": "What should an architecture diagram include?",
                    "options": [
                        "Only colors",
                        "Data sources, processing steps, storage, and data flow",
                        "Random shapes",
                        "Nothing",
                    ],
                    "answer": 1,
                    "explanation": "Architecture diagrams show the complete system design and data flow.",
                },
                {
                    "text": "Why include tests in your data engineering project?",
                    "options": [
                        "To slow down development",
                        "To validate logic, catch bugs, and enable confident changes",
                        "Tests are not useful",
                        "To delete code",
                    ],
                    "answer": 1,
                    "explanation": "Tests ensure reliability and make refactoring safer.",
                },
                {
                    "text": "What is CI/CD for data pipelines?",
                    "options": [
                        "Manual deployment",
                        "Automated testing and deployment of pipeline code",
                        "Deleting pipelines",
                        "Creating documentation",
                    ],
                    "answer": 1,
                    "explanation": "CI/CD automates testing and deployment, improving reliability.",
                },
                {
                    "text": "Why version control your pipeline code?",
                    "options": [
                        "To lose history",
                        "To track changes, enable collaboration, and allow rollbacks",
                        "It is not useful",
                        "To slow down work",
                    ],
                    "answer": 1,
                    "explanation": "Version control is essential for managing code changes and collaboration.",
                },
                {
                    "text": "What makes a strong data engineering capstone?",
                    "options": [
                        "Only code with no documentation",
                        "Complete system with architecture, implementation, tests, monitoring, and docs",
                        "A single query",
                        "Random files",
                    ],
                    "answer": 1,
                    "explanation": "Strong capstones demonstrate end-to-end engineering skills.",
                },
                {
                    "text": "Why include a cost analysis in your capstone?",
                    "options": [
                        "To make it longer",
                        "To show understanding of real-world operational considerations",
                        "It is not relevant",
                        "To hide information",
                    ],
                    "answer": 1,
                    "explanation": "Cost awareness demonstrates production-ready thinking.",
                },
                {
                    "text": "Where should you host your data engineering portfolio?",
                    "options": [
                        "Keep it secret",
                        "GitHub with clear documentation and architecture diagrams",
                        "Only on your laptop",
                        "Never share it",
                    ],
                    "answer": 1,
                    "explanation": "GitHub portfolios demonstrate skills and enable employer review.",
                },
            ],
        }

        qs = questions.get(quiz_unit, [])
        answers = []
        for idx, q in enumerate(qs, start=1):
            st.markdown(f"**Q{idx}. {q['text']}**")
            choice = st.radio(
                label=f"da_u{quiz_unit}_q{idx}",
                options=list(range(len(q["options"]))),
                format_func=lambda i, opts=q["options"]: opts[i],
                key=f"da_quiz_u{quiz_unit}_q{idx}",
            )
            answers.append(choice)

        if qs and st.button("Mark Data Analyst quiz", key="da_quiz_mark"):
            score = sum(1 for ua, q in zip(answers, qs) if ua == q["answer"])
            total = len(qs)
            st.success(
                f"You scored {score} out of {total} on Unit {quiz_unit} quick-check quiz."
            )

            if total:
                for idx, (ua, q) in enumerate(zip(answers, qs), start=1):
                    if ua != q["answer"]:
                        correct = q["options"][q["answer"]]
                        explanation = q.get("explanation", "")
                        st.warning(f"Q{idx}: Correct answer is '{correct}'. {explanation}")

            if total > 0 and score == total:
                st.balloons()

    # Evidence tracking
    with tabs[4]:
        st.subheader("📋 Evidence Tracking")
        if not learner_email:
            st.warning("Log in as a learner to view your evidence.")
        else:
            render_evidence_tracking(learner_email, COURSE_ID)

    # Documents & downloads
    with tabs[5]:
        st.subheader("📂 Documents & Downloads")
        st.markdown(
            """This area will host study plans, unit checklists and portfolio guides
for the Data Analyst Pathway.
"""
        )

        st.markdown("---")
        st.markdown("### 📥 Download core documents as PDF")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button("📥 Study plan PDF", key="da_study_plan_pdf"):
                study_plan_md = """# Data Engineer Pathway – 10–12 Week Study Plan

Suggested week-by-week guide covering Units 1–7 with reading, labs and
portfolio milestones.

---

## Weeks 1–2 – Unit 1: Data Engineering Fundamentals & Pipelines

- Understand the data engineer role.
- Learn ETL vs ELT patterns.
- Build a simple extract-transform-load script.

## Weeks 3–4 – Unit 2: Data Warehousing & Modeling

- Study dimensional modeling and star schemas.
- Design a star schema for a chosen domain.
- Implement SCD Type 2 for a dimension.

## Weeks 5–6 – Unit 3: Batch Processing at Scale

- Learn Spark basics and DataFrames.
- Practise joins, aggregations and window functions.
- Optimise a batch job for performance.

## Week 7 – Unit 4: Stream Processing & Real-time Data

- Understand streaming concepts (windows, watermarks).
- Build a simple streaming pipeline.
- Compute windowed aggregations.

## Week 8 – Unit 5: Cloud Data Platforms & Infrastructure

- Explore cloud storage and compute services.
- Define infrastructure as code.
- Build a cloud-native pipeline.

## Week 9 – Unit 6: Data Quality, Orchestration & Monitoring

- Add data quality checks to a pipeline.
- Orchestrate workflows with Airflow or similar.
- Set up monitoring and alerts.

## Weeks 10–12 – Unit 7: Data Engineering Capstone Project

- Design and implement an end-to-end pipeline.
- Add tests, monitoring and documentation.
- Prepare portfolio artifacts and runbook.
"""
                pdf = create_unit_pdf(0, "Data Engineer Study Plan", study_plan_md)
                st.download_button(
                    label="Download Study Plan PDF",
                    data=pdf,
                    file_name="Data_Engineer_Pathway_Study_Plan.pdf",
                    mime="application/pdf",
                    key="da_study_plan_pdf_dl",
                )

        with col_b:
            if st.button("📥 Unit checklists PDF", key="da_checklists_pdf"):
                checklists_md = """# Data Engineer Pathway – Unit Checklists

Use these checklists to track your progress. They are guidance, not
formal assessment criteria.

---

## Unit 1 – Data Engineering Fundamentals & Pipelines

- [ ] I can explain what a data engineer does.
- [ ] I understand ETL vs ELT patterns.
- [ ] I can build a simple data pipeline with error handling.

## Unit 2 – Data Warehousing & Modeling

- [ ] I can design a star schema for a business domain.
- [ ] I understand fact and dimension tables.
- [ ] I can implement SCD Type 2.

## Unit 3 – Batch Processing at Scale

- [ ] I can write Spark jobs using DataFrames.
- [ ] I understand partitioning and performance tuning.
- [ ] I can optimise a batch pipeline.

## Unit 4 – Stream Processing & Real-time Data

- [ ] I understand streaming vs batch processing.
- [ ] I can build a simple streaming pipeline.
- [ ] I can compute windowed aggregations.

## Unit 5 – Cloud Data Platforms & Infrastructure

- [ ] I can use cloud storage and compute services.
- [ ] I can define infrastructure as code.
- [ ] I understand cloud security best practices.

## Unit 6 – Data Quality, Orchestration & Monitoring

- [ ] I can add data quality checks to pipelines.
- [ ] I can orchestrate workflows with a DAG tool.
- [ ] I can set up monitoring and alerts.

## Unit 7 – Data Engineering Capstone Project

- [ ] I have completed an end-to-end pipeline project.
- [ ] I have tests, monitoring and documentation.
- [ ] I have a runbook and portfolio artifacts.
"""
                pdf = create_unit_pdf(0, "Data Engineer Unit Checklists", checklists_md)
                st.download_button(
                    label="Download Checklists PDF",
                    data=pdf,
                    file_name="Data_Engineer_Pathway_Unit_Checklists.pdf",
                    mime="application/pdf",
                    key="da_checklists_pdf_dl",
                )

        with col_c:
            if st.button("📥 Portfolio guide PDF", key="da_portfolio_pdf"):
                portfolio_md = """# Data Engineer Pathway – Portfolio Guide

This guide helps you turn labs and the capstone into a job-ready
engineering portfolio.

## 1. Core artefacts to include

- Pipeline code with clear structure and tests.
- Architecture diagrams and documentation.
- A strong capstone project with runbook.

## 2. Suggested GitHub structure

- `engineer_capstone/` with code/tests/docs/README.
- `unit_labs/` grouped by topic (ETL, warehousing, Spark, streaming, cloud).

## 3. Writing good READMEs and technical docs

- Problem, architecture, implementation, monitoring, limitations.
- Include setup instructions and sample data.

## 4. Linking portfolio to CV and LinkedIn

- Add a "Projects" section with links and technical summaries.
- Highlight scale, tools, and impact.
"""
                pdf = create_unit_pdf(0, "Data Engineer Portfolio Guide", portfolio_md)
                st.download_button(
                    label="Download Portfolio Guide PDF",
                    data=pdf,
                    file_name="Data_Engineer_Pathway_Portfolio_Guide.pdf",
                    mime="application/pdf",
                    key="da_portfolio_pdf_dl",
                )

        st.markdown("---")
        st.markdown("### 💼 Career Preparation Package")
        st.success(
            "**NEW!** Data Engineer job toolkit - Resume, interview questions, "
            "system design, LinkedIn guide, and career strategies!"
        )
        
        if st.button("📥 Career Prep - Data Engineer Edition", key="de_career_prep_pdf"):
            career_prep_md = """# Career Prep Package - Land Your Data Engineer Job

**Complete toolkit for Data Engineer career success**

---

## 📄 DATA ENGINEER RESUME TEMPLATE

```
[YOUR NAME]
Data Engineer
Email: your.email@example.com | LinkedIn: linkedin.com/in/yourname
GitHub: github.com/yourname

PROFESSIONAL SUMMARY
Data Engineer with expertise in building scalable data pipelines, ETL processes,
and data infrastructure. Proficient in Python, SQL, Spark, and cloud platforms.
Completed comprehensive training in batch/stream processing, data warehousing,
orchestration, and production data systems.

TECHNICAL SKILLS
• Languages: Python, SQL, Bash
• Big Data: Apache Spark, Kafka, Airflow
• Cloud: AWS (S3, EC2, Lambda, Glue, Redshift) / Azure / GCP
• Databases: PostgreSQL, MySQL, Redshift, data warehousing
• Tools: Docker, Git, CI/CD, Terraform
• Skills: ETL/ELT, Data Pipelines, Data Modeling, Orchestration, Monitoring,
  Data Quality, Stream Processing

KEY PROJECTS

Data Pipeline Capstone | [Date]
• Built end-to-end pipeline processing 100K+ daily records
• Implemented star schema data warehouse with 5 fact tables
• Orchestrated ETL workflows using Airflow with error handling
• Monitored data quality with automated checks (99.9% accuracy)
• Reduced processing time by 40% through Spark optimization
• GitHub: [link]

Real-Time Streaming Pipeline | [Date]
• Built stream processing pipeline using Kafka and Spark Streaming
• Implemented windowing and watermarking for late data
• Achieved <5 second latency for real-time dashboards
• Handled 10K events/second with auto-scaling

Batch Processing with Spark | [Date]
• Processed 50GB+ datasets using PySpark
• Optimized partitioning strategy reducing runtime by 60%
• Implemented data quality checks and handled data skew
• Output to data warehouse for BI team consumption

EDUCATION & CERTIFICATIONS
• Data Engineer Pathway Certification | [Date]
  - Pipelines, Warehousing, Spark, Kafka, Cloud, Monitoring
  - 500+ hours hands-on training with production scenarios

[Your Previous Education/Experience]
```

---

## 💼 TOP 70 DATA ENGINEER INTERVIEW QUESTIONS

### ETL & Data Pipelines (15 Questions)

**Q1: What is the difference between ETL and ELT?**
A: ETL transforms data before loading (traditional data warehouse).
ELT loads raw data first, transforms inside warehouse (modern cloud approach).
Use ETL for sensitive data needing transformation, ELT for flexibility and scale.

**Q2: What is idempotency in data pipelines?**
A: Running same pipeline multiple times produces same result.
Critical for pipeline reliability and safe retries.
Example: Use UPSERT instead of INSERT to handle reruns.

**Q3: How do you handle pipeline failures?**
- Automated retries with exponential backoff
- Dead letter queues for failed records
- Alerting and monitoring
- Transaction logs for recovery
- Clear rollback procedures

**Q4: Explain slowly changing dimensions (SCD).**
- Type 0: Never changes
- Type 1: Overwrite (no history)
- Type 2: Add new row with effective dates (full history)
- Type 3: Add new column (limited history)
Most common: Type 2 for full historical tracking

**Q5: What is data partitioning?**
A: Splitting data into smaller chunks for parallel processing.
Benefits: Faster queries, easier maintenance, better scalability
Partition by: date (most common), region, category
Example: `/data/year=2024/month=11/day=23/file.parquet`

**Q6: How do you ensure data quality?**
- Schema validation
- Null checks
- Range/format validation
- Uniqueness constraints
- Referential integrity
- Automated testing
- Monitoring and alerting

**Q7: What is data lineage?**
A: Tracking data flow from sources through transformations to destinations.
Benefits: Debugging, compliance, impact analysis, trust
Tools: Data catalogs, metadata stores

**Q8: Explain incremental vs full load.**
- Full: Load entire dataset (simple but slow)
- Incremental: Load only new/changed data (efficient)
Methods: Timestamp, change data capture (CDC), delta files

**Q9: What is backfilling?**
A: Re-processing historical data with new logic.
Challenges: Resource intensive, maintaining two pipelines
Strategy: Batch processing, incremental approach

**Q10: How to handle late-arriving data?**
- Define cutoff window
- Reprocess with new data
- Use watermarks (streaming)
- Business rules for acceptance

**Q11: What is data validation?**
- Pre-load: Check before processing
- In-process: Validate during transformation
- Post-load: Verify after loading
- Reconciliation: Compare source vs destination counts

**Q12: Explain error handling strategies.**
- Fail fast: Stop on first error (data quality critical)
- Continue: Log errors, process rest (high availability)
- Quarantine: Move bad records to separate location
- Retry: Automatic retry with backoff

**Q13: What is schema evolution?**
A: Handling schema changes over time.
Approaches: Schema-on-read, schema-on-write, Avro/Parquet with evolution support
Best practice: Backward/forward compatible changes

**Q14: How to optimize pipeline performance?**
- Parallel processing
- Efficient file formats (Parquet, Avro)
- Appropriate partitioning
- Predicate pushdown
- Caching frequently used data
- Resource tuning

**Q15: What is data orchestration?**
A: Scheduling and managing pipeline dependencies.
Tools: Airflow, Luigi, Prefect
Key concepts: DAGs, task dependencies, retries, SLAs

---

### SQL & Data Warehousing (10 Questions)

**Q16: Star schema vs snowflake schema?**
Star: Denormalized, faster queries, more storage
Snowflake: Normalized dimensions, less storage, more joins
Use star for most data warehouses (simpler, faster)

**Q17: Fact vs dimension tables?**
Fact: Measures/metrics (sales, clicks, transactions)
Dimension: Context (customers, products, time, location)
Fact tables larger, dimension tables wider

**Q18: What are window functions?**
A: Calculations across related rows without grouping.
```sql
ROW_NUMBER(), RANK(), DENSE_RANK()
SUM() OVER, AVG() OVER
PARTITION BY, ORDER BY
```

**Q19: How to optimize slow queries?**
- Add indexes on filter/join columns
- Partition large tables
- Use column statistics
- Avoid SELECT *
- Use EXPLAIN/EXPLAIN ANALYZE
- Materialize common aggregations

**Q20: What is a materialized view?**
A: Pre-computed query results stored as table.
Benefits: Faster queries, trade storage for speed
Refresh: On-demand or scheduled

**Q21: Explain data warehouse vs data lake.**
Warehouse: Structured, schema-on-write, SQL, BI tools
Lake: All data types, schema-on-read, flexible, cheaper storage
Modern: Lakehouse (combines both)

**Q22: What is columnar storage?**
A: Store data by column, not row (Parquet, ORC).
Benefits: Better compression, faster analytics, efficient for subsets
Use for: Analytics workloads, data warehouses

**Q23: How to handle duplicate records?**
```sql
-- Find duplicates
SELECT col, COUNT(*) FROM table GROUP BY col HAVING COUNT(*) > 1

-- Remove duplicates
WITH deduped AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) as rn
  FROM table
)
SELECT * FROM deduped WHERE rn = 1
```

**Q24: What is data modeling?**
A: Designing structure for storing data.
Types: Conceptual, logical, physical
Approaches: Dimensional (star/snowflake), Data Vault, normalized

**Q25: Explain ACID properties.**
- Atomicity: All or nothing
- Consistency: Valid state transitions
- Isolation: Concurrent transactions don't interfere
- Durability: Committed data persists
Critical for transactional systems

---

### Apache Spark & Big Data (15 Questions)

**Q26: Explain Spark architecture.**
- Driver: Orchestrates job
- Executors: Run tasks
- Cluster Manager: Resource allocation (YARN, K8s, Standalone)
- DAG: Execution plan

**Q27: What is lazy evaluation?**
A: Spark doesn't execute until action called.
Transformations: map, filter, groupBy (lazy)
Actions: count, collect, save (trigger execution)
Benefits: Optimization, efficient execution plan

**Q28: RDD vs DataFrame vs Dataset?**
- RDD: Low-level, flexible, slower
- DataFrame: Optimized, SQL-like, most common
- Dataset: Type-safe, Scala/Java only
Use DataFrame for most cases

**Q29: What is shuffling?**
A: Data redistribution across partitions.
Triggered by: groupBy, join, repartition
Expensive: Network I/O, disk spills
Minimize: Broadcast small tables, pre-partition data

**Q30: How to optimize Spark jobs?**
- Appropriate partitioning (200-1000 partitions)
- Avoid shuffles when possible
- Cache reused DataFrames
- Broadcast small lookup tables
- Use efficient file formats (Parquet)
- Tune executor memory/cores
- Filter early (predicate pushdown)

**Q31: What is data skew?**
A: Uneven data distribution across partitions.
Problem: Some tasks take much longer
Solutions: Salting keys, increase partitions, custom partitioner

**Q32: Explain partition vs bucketing.**
Partition: Physical file organization by column values
Bucketing: Hash-based distribution within partitions
Use partitioning for time-series, bucketing for joins

**Q33: What is broadcast join?**
A: Replicating small table to all executors.
Avoids shuffle, much faster for small tables (<100MB)
```python
df_large.join(broadcast(df_small), "key")
```

**Q34: cache() vs persist()?**
cache(): Store in memory (MEMORY_ONLY)
persist(): Choose storage level (memory, disk, both)
Use for DataFrames accessed multiple times

**Q35: What is the catalyst optimizer?**
A: Spark's query optimizer for DataFrames.
Optimizations: Predicate pushdown, projection pushdown, constant folding
Why DataFrames faster than RDDs

**Q36: How to read/write Parquet?**
```python
# Read
df = spark.read.parquet("path/to/data")

# Write with partitioning
df.write.partitionBy("date").parquet("output/path")
```

**Q37: What are accumulators and broadcast variables?**
Accumulator: Shared variable for aggregation across executors
Broadcast: Read-only variable shared to all executors
Use: Counters, lookup tables

**Q38: Explain Spark SQL.**
A: SQL interface to Spark DataFrames.
```python
df.createOrReplaceTempView("table")
spark.sql("SELECT * FROM table WHERE col > 100")
```

**Q39: What is dynamic partition pruning?**
A: Skipping irrelevant partitions during query execution.
Benefit: Faster queries on partitioned data
Automatic in Spark 3+

**Q40: How to handle small files problem?**
- Compact files before processing
- Use coalesce/repartition when writing
- Set appropriate file size (128MB-1GB)
- Use compaction jobs

---

### Stream Processing (10 Questions)

**Q41: Batch vs stream processing?**
Batch: Process all data periodically (hourly, daily)
Stream: Process data continuously as it arrives
Use streaming for: Real-time, low latency requirements

**Q42: What is Apache Kafka?**
A: Distributed event streaming platform.
Components: Producers, consumers, topics, partitions, brokers
Use for: Event logs, message queuing, stream processing

**Q43: Explain Kafka topics and partitions.**
Topic: Category of messages
Partition: Ordered sequence within topic
Benefits: Parallelism, ordering within partition, scalability

**Q44: What is a consumer group?**
A: Set of consumers sharing topic consumption.
Each partition consumed by one consumer in group
Enables: Load balancing, fault tolerance

**Q45: What is windowing in streaming?**
A: Grouping events by time periods.
Types:
- Tumbling: Fixed, non-overlapping (every 5 min)
- Sliding: Overlapping (last 5 min, updated every minute)
- Session: Based on inactivity gaps

**Q46: What is watermarking?**
A: Tracking event time progress in streams.
Handles: Late-arriving data
Allows: Closing windows, managing state

**Q47: Exactly-once vs at-least-once processing?**
At-least-once: May process duplicates (simpler, faster)
Exactly-once: No duplicates (complex, slower, more expensive)
Choose based on: Data criticality, cost, complexity

**Q48: What is stateful vs stateless processing?**
Stateless: Each event processed independently
Stateful: Maintains state across events (aggregations, joins)
Stateful more complex: State management, checkpointing

**Q49: How to handle late data?**
- Set watermark tolerance window
- Reprocess if within window
- Drop if too late
- Send to separate late-data stream

**Q50: What is stream-table join?**
A: Enriching stream with reference data.
Example: Join click stream with user dimension table
Implementation: Broadcast table or versioned lookups

---

### Cloud & Infrastructure (10 Questions)

**Q51: What is Infrastructure as Code (IaC)?**
A: Managing infrastructure through code files.
Tools: Terraform, CloudFormation, Pulumi
Benefits: Version control, reproducibility, automation

**Q52: S3 vs EBS vs EFS?**
- S3: Object storage, cheapest, unlimited, eventual consistency
- EBS: Block storage, attached to EC2, persistent
- EFS: File system, shared across instances
Use S3 for data lakes, EBS for databases, EFS for shared files

**Q53: What is auto-scaling?**
A: Automatically adjust compute resources based on load.
Benefits: Cost optimization, handle traffic spikes
For data: EMR, Dataproc auto-scaling clusters

**Q54: Explain data lake vs data warehouse in cloud.**
Data Lake (S3, ADLS): Raw data, all formats, cheap, flexible
Data Warehouse (Redshift, Snowflake, BigQuery): Structured, optimized for BI
Strategy: Lake for storage, warehouse for analytics

**Q55: What is serverless computing?**
A: Run code without managing servers.
Examples: AWS Lambda, Azure Functions, GCP Cloud Functions
For data: Event-driven ETL, light transformations, scheduling

**Q56: How to secure data in cloud?**
- Encryption at rest and in transit
- IAM roles and policies (least privilege)
- VPC and network isolation
- Data masking/tokenization
- Audit logging
- Access controls

**Q57: What is a VPC?**
A: Virtual Private Cloud - isolated network.
Components: Subnets, route tables, security groups, NAT gateway
Use for: Network isolation, security

**Q58: Explain  CI/CD for data pipelines.**
Continuous Integration: Automated testing of code
Continuous Deployment: Automated deployment to production
Tools: Jenkins, GitLab CI, GitHub Actions
Tests: Data validation, schema checks, integration tests

**Q59: What is container orchestration?**
A: Managing containerized applications.
Kubernetes: Most popular, complex, powerful
Docker Compose: Simple, single host
For data: Airflow on K8s, Spark on K8s

**Q60: How to estimate cloud costs?**
- Compute: Instance hours × price
- Storage: GB × price × time
- Data transfer: GB transferred
- Optimize: Reserved instances, spot instances, lifecycle policies, auto-scaling

---

### System Design & Architecture (10 Questions)

**Q61: Design a data pipeline for processing clickstream data.**
1. Ingestion: Kafka for real-time collection
2. Stream processing: Spark Streaming for enrichment
3. Storage: S3 data lake (raw), Redshift (aggregated)
4. Orchestration: Airflow for batch jobs
5. Monitoring: CloudWatch, custom dashboards
6. Data quality: Schema validation, null checks

**Q62: How to process 1TB of data daily?**
- Use distributed processing (Spark, Presto)
- Partition by date for incremental processing
- Optimize file formats (Parquet)
- Scale compute based on load
- Parallel processing (10-100 executors)
- Incremental updates, not full rewrites

**Q63: Design a real-time analytics system.**
- Kafka for event ingestion
- Spark Streaming / Flink for processing
- Redis / Druid for serving layer
- Monitoring: Prometheus, Grafana
- Auto-scaling for variable load
- <5 second latency target

**Q64: How to build a data warehouse from scratch?**
1. Requirements: Identify use cases, KPIs
2. Data modeling: Star schema, fact/dimension tables
3. ETL: Extract from sources, transform, load
4. Tools: Redshift/Snowflake/BigQuery
5. BI layer: Tableau/Looker
6. Governance: Access control, data quality

**Q65: Design CDC (Change Data Capture) system.**
- Source: Database transaction logs
- Capture: Debezium, AWS DMS
- Stream: Kafka
- Process: Spark/Flink for transformations
- Target: Data warehouse with SCD Type 2
- Monitoring: Lag, throughput, errors

**Q66: How to ensure high availability?**
- Redundancy: Multi-AZ deployment
- Failover: Automatic switching
- Load balancing
- Backups: Regular, tested restores
- Monitoring: Health checks, alerts
- Chaos engineering: Test failure scenarios

**Q67: Design event-driven architecture.**
- Events: Kafka topics
- Producers: Applications, IoT, logs
- Consumers: Microservices, Lambda
- Schema registry: Avro schemas
- Dead letter queue: Failed events
- Monitoring: Event lag, throughput

**Q68: How to handle schema changes?**
- Backward compatible: Add optional fields
- Forward compatible: Ignore unknown fields
- Schema registry: Avro, Protobuf
- Versioning: Track schema versions
- Testing: Validate before production
- Communication: Notify consumers

**Q69: Design disaster recovery strategy.**
- Backups: Automated, regular
- Replication: Cross-region
- RPO: Recovery Point Objective (acceptable data loss)
- RTO: Recovery Time Objective (downtime)
- Testing: Regular DR drills
- Documentation: Runbooks

**Q70: How to implement data governance?**
- Data catalog: Metadata management
- Access control: Role-based permissions
- Data quality: Automated checks
- Lineage: Track data flow
- Compliance: GDPR, CCPA
- Audit logs: Track access, changes

---

## 🎤 INTERVIEW TIPS

### Technical Interview Prep:
1. Practice system design on whiteboard
2. Know your projects deeply
3. Be ready to write SQL/Python live
4. Understand trade-offs (not just one solution)
5. Ask clarifying questions

### Behavioral Questions:
- Describe a complex pipeline you built
- How do you handle production issues?
- Tell me about a time you optimized performance
- How do you ensure data quality?
- Describe working with stakeholders

### Questions to Ask:
- What's the data infrastructure stack?
- How is data quality ensured?
- What's the biggest data challenge?
- How does the team prioritize work?
- Opportunities for learning new technologies?

---

## 💡 LINKEDIN OPTIMIZATION

### Headline:
"Data Engineer | Spark, Airflow, AWS | Building Scalable Data Pipelines"

### Skills to Highlight:
- Apache Spark
- Python
- SQL
- Apache Airflow
- AWS / Azure / GCP
- ETL/ELT
- Data Warehousing
- Apache Kafka
- Docker
- Data Modeling

---

**Complete career prep for Data Engineer roles!**

Practice technical questions, build strong portfolio, optimize LinkedIn,
and confidently ace your interviews.

**Good luck! 🚀**
"""
            pdf = create_unit_pdf(0, "Career Prep - Data Engineer", career_prep_md)
            st.download_button(
                label="Download Career Prep Package PDF",
                data=pdf,
                file_name="Career_Prep_Package_Data_Engineer.pdf",
                mime="application/pdf",
                key="de_career_prep_pdf_dl",
            )

    # My Progress
    with tabs[6]:
        st.subheader("📊 My Progress")
        if not enrollment:
            st.info(
                "Progress data is not available yet. Once enrolled, your progress will appear here."
            )
        else:
            _render_progress_header(enrollment)

            st.markdown("---")
            st.markdown("### ✅ Personal checklist (for learners)")
            for unit_number, unit in UNITS.items():
                st.checkbox(
                    f"Completed Unit {unit_number}: {unit['name']}",
                    key=f"da_pathway_progress_unit_{unit_number}",
                )

    # Certificate
    with tabs[7]:
        st.subheader("🎓 Certificate")
        st.info(
            "On successful completion of all units and assessments, learners receive a "
            "T21 Data Analyst Pathway certificate, where offered by their training provider."
        )

        st.markdown(
            """### Requirements for completion

- Complete and submit evidence for all 7 units
- Demonstrate competence in core analyst tools (spreadsheets, SQL, BI, Python)
- Complete at least one end-to-end analyst capstone project
- Meet internal quality standards set by tutors/assessors
"""
        )

        if enrollment and enrollment.get("progress", 0) >= 100:
            st.success(
                "All requirements appear to be complete. Your training provider can now "
                "issue your Data Analyst Pathway certificate."
            )
        else:
            st.info(
                "Keep working through your units and projects. Once everything is complete, "
                "your tutor will confirm and issue your certificate."
            )
