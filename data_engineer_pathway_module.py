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
        st.markdown("#### 📘 What Does a Data Engineer Do? The Complete Role")
        st.markdown(
            """Data engineers are the **architects and builders of data infrastructure**. 
While data analysts and scientists consume data, data engineers make that consumption 
possible by building the pipelines, warehouses, and systems that deliver clean, 
reliable, and performant data at scale.

**Your Core Responsibilities:**

1. **Build Data Pipelines (ETL/ELT)**
   - Extract data from multiple sources (databases, APIs, files, streams)
   - Transform data (clean, enrich, aggregate, join)
   - Load data into target systems (warehouses, lakes, databases)
   - Schedule and orchestrate pipeline execution

2. **Maintain Data Infrastructure**
   - Design and implement data warehouses
   - Build and optimize data lakes
   - Manage streaming platforms (Kafka, Kinesis)
   - Configure cloud data services (AWS, GCP, Azure)

3. **Ensure Data Quality & Reliability**
   - Implement data validation and quality checks
   - Monitor pipeline health and performance
   - Handle errors and implement retry logic
   - Maintain data lineage and documentation

4. **Optimize for Performance & Cost**
   - Tune queries and transformations
   - Optimize storage formats (Parquet, ORC)
   - Implement caching and partitioning strategies
   - Monitor and reduce cloud costs

**Real-World Example:**

Imagine you're a Data Engineer at an e-commerce company. Your stakeholders need:
- Analysts want daily sales reports
- Data scientists need clean data for ML models
- Executives want real-time dashboards

**Your Job:**
- Build ETL pipeline to extract sales data from 5 different databases
- Clean and standardize the data
- Load into a data warehouse (star schema)
- Create real-time stream for live dashboard
- Orchestrate with Airflow (runs at 2 AM daily)
- Monitor pipeline health and alert on failures
- Optimize queries to run in <5 minutes
- Keep costs under budget

**The Data Engineering Workflow:**

1. **Requirements Gathering** (10% of time)
   - Understand data needs
   - Define SLAs (latency, freshness, quality)
   - Identify data sources

2. **Design** (15% of time)
   - Architecture diagrams
   - Data models (schemas)
   - Technology selection
   - Cost estimation

3. **Implementation** (40% of time)
   - Write pipeline code
   - Build transformations
   - Set up infrastructure
   - Write tests

4. **Testing & Validation** (15% of time)
   - Unit tests
   - Integration tests
   - Data quality validation
   - Performance testing

5. **Deployment & Monitoring** (10% of time)
   - Deploy to production
   - Set up monitoring
   - Configure alerts
   - Document runbooks

6. **Maintenance & Optimization** (10% of time)
   - Fix bugs
   - Optimize performance
   - Add new features
   - Reduce costs
"""
        )

        st.markdown("#### 🔄 ETL vs ELT: When to Use Each Pattern")
        st.markdown(
            """Understanding the difference between ETL and ELT is fundamental to data engineering.

**ETL (Extract, Transform, Load) - Traditional Pattern:**

**Process:**
1. Extract data from source systems
2. Transform data BEFORE loading (clean, join, aggregate)
3. Load transformed data into warehouse

**When to Use:**
- ✅ Source systems are slow or expensive to query
- ✅ Need to mask sensitive data before loading
- ✅ Target warehouse has limited compute power
- ✅ Transformations are complex and reusable
- ✅ Working with legacy systems

**Example:**
```python
# ETL Pattern
df = extract_from_api()  # Get raw data
df = clean_data(df)      # Transform BEFORE loading
df = join_with_ref(df)
df = aggregate(df)
load_to_warehouse(df)    # Load clean data
```

**ELT (Extract, Load, Transform) - Modern Pattern:**

**Process:**
1. Extract data from source systems
2. Load RAW data into warehouse/lake
3. Transform data INSIDE the warehouse (using SQL/Spark)

**When to Use:**
- ✅ Modern cloud warehouses (Snowflake, BigQuery, Redshift)
- ✅ Need to keep raw data for auditing
- ✅ Warehouse has powerful compute (can handle transformations)
- ✅ Multiple teams need different views of same data
- ✅ Want flexibility to re-transform historical data

**Example:**
```python
# ELT Pattern
df = extract_from_api()  # Get raw data
load_to_lake(df)         # Load RAW immediately

# Transform INSIDE warehouse using SQL
warehouse.execute(''''
    CREATE TABLE clean_sales AS
    SELECT * FROM raw_sales
    WHERE amount > 0
    AND date >= '2024-01-01'
'''')
```

**Comparison:**

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Transform Location** | External tool | Inside warehouse |
| **Raw Data** | Not stored | Stored in lake |
| **Flexibility** | Lower | Higher |
| **Warehouse Load** | Lower | Higher |
| **Best For** | Legacy systems | Modern cloud |
| **Tools** | Python, Spark | SQL, dbt |

**Modern Trend:** Most companies are moving to ELT because:
- Cloud warehouses are powerful and cheap
- Keeping raw data provides audit trail
- SQL transformations are easier to maintain
- Tools like dbt make ELT elegant
"""
        )

        st.markdown("#### 🛠️ Building Your First Pipeline: Step-by-Step")
        st.markdown(
            """Let's build a complete ETL pipeline from scratch.

**Scenario:** Extract daily sales from a CSV, clean it, load to PostgreSQL

**Step 1: Extract**
```python
import pandas as pd

def extract_sales_data(file_path):
    '''Extract sales data from CSV'''
    df = pd.read_csv(file_path)
    print(f"Extracted {len(df)} records")
    return df
```

**Step 2: Transform**
```python
def transform_sales_data(df):
    '''Clean and transform sales data'''
    # Remove duplicates
    df = df.drop_duplicates(subset=['order_id'])
    
    # Handle missing values
    df = df.dropna(subset=['order_id', 'customer_id'])
    df['email'].fillna('unknown@company.com', inplace=True)
    
    # Data type conversions
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['amount'] = pd.to_numeric(df['amount'])
    
    # Add derived columns
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    
    print(f"Transformed to {len(df)} clean records")
    return df
```

**Step 3: Load**
```python
from sqlalchemy import create_engine

def load_to_warehouse(df, table_name):
    '''Load data to PostgreSQL'''
    engine = create_engine('postgresql://user:pass@localhost:5432/warehouse')
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} records to {table_name}")
```

**Step 4: Orchestrate**
```python
def run_pipeline():
    '''Run complete ETL pipeline'''
    try:
        # Extract
        df = extract_sales_data('sales.csv')
        
        # Transform
        df_clean = transform_sales_data(df)
        
        # Load
        load_to_warehouse(df_clean, 'sales')
        
        print("✅ Pipeline completed successfully")
        return True
    
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        return False
```

**Best Practices:**

1. **Logging**
   - Log every step
   - Include timestamps
   - Log record counts

2. **Error Handling**
   - Try/except blocks
   - Retry logic for transient failures
   - Alert on persistent failures

3. **Idempotency**
   - Pipeline should produce same result if run multiple times
   - Use upsert instead of insert
   - Check for existing data before loading

4. **Testing**
   - Unit tests for each function
   - Integration tests for full pipeline
   - Data quality tests

5. **Monitoring**
   - Track execution time
   - Monitor data volumes
   - Alert on anomalies
"""
        )
        
        st.markdown("#### 📊 Data Sources: Extracting from Everywhere")
        st.markdown("""
**Data engineers extract from diverse sources:**

**1. Relational Databases (PostgreSQL, MySQL, SQL Server)**

```python
import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="production",
    user="etl_user",
    password="secret"
)

# Extract with SQL
query = "SELECT * FROM orders WHERE order_date >= '2024-01-01'"
df = pd.read_sql(query, conn)

print(f"Extracted {len(df)} orders")
conn.close()
```

**Best Practices:**
- ✅ Use connection pooling
- ✅ Query only needed columns
- ✅ Filter at source (WHERE clause)
- ✅ Use indexes for performance
- ✅ Close connections properly

**2. REST APIs**

```python
import requests
import pandas as pd

def extract_from_api(endpoint, api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return pd.DataFrame(data['results'])

# Extract
df = extract_from_api('https://api.company.com/sales', 'YOUR_KEY')
print(f"Extracted {len(df)} records from API")
```

**Best Practices:**
- ✅ Handle pagination
- ✅ Implement rate limiting
- ✅ Retry on failures
- ✅ Cache responses when appropriate

**3. Cloud Storage (S3, GCS, Azure Blob)**

```python
import boto3
import pandas as pd
from io import StringIO

# Read from S3
s3 = boto3.client('s3')
obj = s3.get_object(Bucket='my-bucket', Key='data/sales.csv')
df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))

print(f"Extracted {len(df)} records from S3")
```

**4. Streaming Sources (Kafka)**

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    event = message.value
    process_event(event)
```
""")
        
        st.markdown("#### 🔧 Advanced Transformation Patterns")
        st.markdown("""
**Common transformation patterns you'll use daily:**

**1. Data Cleaning**

```python
def clean_customer_data(df):
    # Remove duplicates
    df = df.drop_duplicates(subset=['customer_id'], keep='last')
    
    # Handle missing values
    df['email'].fillna('unknown@company.com', inplace=True)
    df['phone'].fillna('000-000-0000', inplace=True)
    
    # Standardize text
    df['name'] = df['name'].str.strip().str.title()
    df['email'] = df['email'].str.lower()
    
    # Fix data types
    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    
    # Remove outliers
    Q1 = df['age'].quantile(0.25)
    Q3 = df['age'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df['age'] >= Q1 - 1.5*IQR) & (df['age'] <= Q3 + 1.5*IQR)]
    
    return df
```

**2. Data Enrichment**

```python
def enrich_orders(orders_df, customers_df, products_df):
    # Join with customer data
    enriched = orders_df.merge(
        customers_df[['customer_id', 'segment', 'country']],
        on='customer_id',
        how='left'
    )
    
    # Join with product data
    enriched = enriched.merge(
        products_df[['product_id', 'category', 'brand']],
        on='product_id',
        how='left'
    )
    
    # Add derived columns
    enriched['order_year'] = enriched['order_date'].dt.year
    enriched['order_month'] = enriched['order_date'].dt.month
    enriched['is_weekend'] = enriched['order_date'].dt.dayofweek >= 5
    
    return enriched
```

**3. Aggregations**

```python
def create_customer_features(orders_df):
    customer_agg = orders_df.groupby('customer_id').agg({
        'order_id': 'count',
        'total_amount': ['sum', 'mean', 'max'],
        'order_date': ['min', 'max']
    })
    
    customer_agg.columns = ['num_orders', 'total_spent', 'avg_order', 
                            'max_order', 'first_order', 'last_order']
    
    # Calculate recency
    customer_agg['days_since_last_order'] = \
        (datetime.now() - customer_agg['last_order']).dt.days
    
    return customer_agg
```
""")
        
        st.markdown("#### ⚙️ Error Handling & Retry Logic")
        st.markdown("""
**Production pipelines must handle failures gracefully:**

**1. Retry with Exponential Backoff**

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, base_delay=2)
def extract_from_api(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
```

**2. Circuit Breaker Pattern**

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            
            raise e
```

**3. Dead Letter Queue**

```python
def process_with_dlq(record):
    try:
        # Process record
        result = transform_record(record)
        load_to_warehouse(result)
    
    except Exception as e:
        # Send to dead letter queue for manual review
        send_to_dlq(record, error=str(e))
        log_error(f"Record failed: {record['id']}, Error: {e}")
```
""")
        
        st.markdown("#### 🧪 Testing ETL Pipelines")
        st.markdown("""
**Testing is critical for reliable pipelines:**

**1. Unit Tests**

```python
import pytest
import pandas as pd

def test_transform_sales_data():
    # Arrange
    input_df = pd.DataFrame({
        'order_id': ['A', 'B', 'A'],  # Has duplicate
        'amount': [100, 200, 100]
    })
    
    # Act
    result = transform_sales_data(input_df)
    
    # Assert
    assert len(result) == 2, "Should remove duplicates"
    assert result['order_id'].is_unique, "order_id should be unique"
```

**2. Integration Tests**

```python
def test_full_pipeline():
    # Setup test database
    test_db = create_test_database()
    
    # Run pipeline
    success = run_pipeline(
        source='test_data.csv',
        target=test_db
    )
    
    # Verify
    assert success, "Pipeline should succeed"
    
    result_count = test_db.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    assert result_count > 0, "Should load data"
    
    # Cleanup
    test_db.close()
```

**3. Data Quality Tests**

```python
def test_data_quality():
    df = pd.read_sql("SELECT * FROM sales", conn)
    
    # No nulls in critical columns
    assert df['order_id'].notnull().all()
    
    # No duplicates
    assert df['order_id'].is_unique
    
    # Valid ranges
    assert (df['amount'] >= 0).all()
    assert (df['quantity'] > 0).all()
    
    # Data freshness
    latest = df['order_date'].max()
    assert (datetime.now() - latest).days < 2
```
""")
    elif unit_number == 2:
        st.markdown("#### 📘 Data Warehousing & Dimensional Modeling: The Complete Guide")
        st.markdown(
            """Data warehouses are the **foundation of enterprise analytics**. They centralize 
data from multiple sources, optimize it for querying, and provide a single source of truth 
for business intelligence.

**Why Data Warehouses Matter:**

1. **Centralized Data**
   - Combine data from CRM, ERP, web analytics, databases
   - Single source of truth for the organization
   - Consistent definitions and metrics

2. **Optimized for Analytics**
   - Denormalized for fast queries
   - Pre-aggregated tables
   - Indexed for common query patterns

3. **Historical Data**
   - Track changes over time
   - Support trend analysis
   - Enable year-over-year comparisons

4. **Business Intelligence**
   - Power BI, Tableau, Looker connect here
   - Self-service analytics for business users
   - Consistent reporting across teams

**Data Warehouse vs Data Lake:**

| Aspect | Data Warehouse | Data Lake |
|--------|----------------|------------|
| **Data Type** | Structured | All types |
| **Schema** | Schema-on-write | Schema-on-read |
| **Users** | Business analysts | Data scientists |
| **Cost** | Higher | Lower |
| **Query Speed** | Fast | Variable |
| **Use Case** | BI & reporting | ML & exploration |

**Modern Approach:** Use BOTH!
- Data Lake for raw data storage
- Data Warehouse for curated analytics
"""
        )

        st.markdown("#### ⭐ Star Schema Design: The Foundation of Analytics")
        st.markdown(
            """The **star schema** is the most common data warehouse design pattern.

**Components:**

1. **Fact Table (Center of Star)**
   - Contains measurable events/transactions
   - Examples: sales, orders, clicks, appointments
   - Columns: foreign keys to dimensions + numeric measures
   - Large (millions to billions of rows)

2. **Dimension Tables (Points of Star)**
   - Descriptive attributes
   - Examples: customers, products, dates, stores
   - Columns: primary key + descriptive attributes
   - Smaller (thousands to millions of rows)

**Example: Retail Sales Star Schema**

**Fact Table: fact_sales**
```sql
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT,              -- FK to dim_date
    product_key INT,           -- FK to dim_product
    customer_key INT,          -- FK to dim_customer
    store_key INT,             -- FK to dim_store
    
    -- Measures (additive)
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    cost_amount DECIMAL(10,2),
    profit_amount DECIMAL(10,2)
);
```

**Dimension: dim_product**
```sql
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2)
);
```

**Benefits of Star Schema:**
- ✅ Simple to understand
- ✅ Fast query performance
- ✅ Easy to add new dimensions
- ✅ Works great with BI tools

**Design Process:**
1. Identify business process (e.g., sales)
2. Define grain (one row per order line)
3. Identify dimensions (who, what, where, when)
4. Identify facts (numeric measures)
5. Build tables and relationships
"""
        )

        st.markdown("#### 🔄 Slowly Changing Dimensions: Tracking History")
        st.markdown(
            """Dimension data changes over time. How do you handle it?

**The Problem:**
- Customer moves to new address
- Product price changes
- Employee gets promoted

**Do you:** Overwrite? Keep history? Both?

**SCD Type 1: Overwrite (No History)**

**Approach:** Simply update the record

```sql
UPDATE dim_customer
SET address = '123 New St', city = 'London'
WHERE customer_id = 'CUST001';
```

**Pros:** Simple, saves space
**Cons:** Lose history
**Use When:** History doesn't matter (e.g., fixing typos)

**SCD Type 2: Add New Row (Full History)**

**Approach:** Keep old row, add new row with version/dates

```sql
-- Expire old record
UPDATE dim_customer
SET is_current = 0, end_date = '2024-11-28'
WHERE customer_id = 'CUST001' AND is_current = 1;

-- Insert new record
INSERT INTO dim_customer (
    customer_id, name, address, city,
    start_date, end_date, is_current, version
) VALUES (
    'CUST001', 'John Smith', '123 New St', 'London',
    '2024-11-28', NULL, 1, 2
);
```

**Pros:** Complete history, can analyze trends
**Cons:** More storage, more complex queries
**Use When:** History matters (customer segments, pricing)

**SCD Type 3: Add New Column (Limited History)**

**Approach:** Add columns for previous values

```sql
ALTER TABLE dim_customer ADD COLUMN previous_address VARCHAR(200);

UPDATE dim_customer
SET previous_address = address,
    address = '123 New St'
WHERE customer_id = 'CUST001';
```

**Pros:** Simple, keeps one previous value
**Cons:** Limited history (only 1-2 previous values)
**Use When:** Need to compare current vs previous only

**Comparison:**

| Type | History | Storage | Complexity | Use Case |
|------|---------|---------|------------|----------|
| **Type 1** | None | Low | Simple | Corrections |
| **Type 2** | Full | High | Complex | Trend analysis |
| **Type 3** | Limited | Medium | Medium | Before/after |

**Best Practice:** Use Type 2 for most business dimensions!
"""
        )
        
        st.markdown("#### 🏛️ Advanced Dimensional Modeling Patterns")
        st.markdown("""
**Beyond basic star schema:**

**1. Snowflake Schema**

Normalize dimensions into sub-dimensions:

```sql
-- Instead of flat dim_product:
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(200),
    category_key INT  -- FK to dim_category
);

CREATE TABLE dim_category (
    category_key INT PRIMARY KEY,
    category_name VARCHAR(100),
    department_key INT  -- FK to dim_department
);
```

**Pros:** Saves storage, enforces consistency  
**Cons:** More joins, slower queries  
**Use when:** Storage is critical concern

**2. Junk Dimensions**

Combine low-cardinality flags:

```sql
CREATE TABLE dim_order_flags (
    flag_key INT PRIMARY KEY,
    is_express BOOLEAN,
    is_gift BOOLEAN,
    is_international BOOLEAN,
    requires_signature BOOLEAN
);

-- In fact table:
fact_orders.flag_key -> dim_order_flags
```

**3. Role-Playing Dimensions**

Same dimension used multiple times:

```sql
-- dim_date used 3 times in fact_orders:
fact_orders.order_date_key -> dim_date
fact_orders.ship_date_key -> dim_date
fact_orders.delivery_date_key -> dim_date
```

**4. Degenerate Dimensions**

Dimension attributes stored in fact table:

```sql
CREATE TABLE fact_sales (
    sale_key INT,
    date_key INT,
    product_key INT,
    
    -- Degenerate dimensions (no separate dim table)
    order_number VARCHAR(50),
    invoice_number VARCHAR(50),
    
    -- Measures
    quantity INT,
    amount DECIMAL(10,2)
);
```
""")
        
        st.markdown("#### 📊 Fact Table Design Patterns")
        st.markdown("""
**Different types of fact tables:**

**1. Transaction Facts (Most Common)**

One row per business event:

```sql
CREATE TABLE fact_sales (
    sale_key BIGINT PRIMARY KEY,
    date_key INT,
    product_key INT,
    customer_key INT,
    
    -- Additive measures (can sum across all dimensions)
    quantity INT,
    revenue DECIMAL(10,2),
    cost DECIMAL(10,2),
    profit DECIMAL(10,2)
);
```

**2. Periodic Snapshot Facts**

Regular snapshots (daily, monthly):

```sql
CREATE TABLE fact_inventory_snapshot (
    snapshot_date_key INT,
    product_key INT,
    warehouse_key INT,
    
    -- Semi-additive (can't sum across time)
    quantity_on_hand INT,
    quantity_reserved INT,
    reorder_point INT
);
```

**3. Accumulating Snapshot Facts**

Track process with multiple milestones:

```sql
CREATE TABLE fact_order_fulfillment (
    order_key INT PRIMARY KEY,
    
    -- Multiple date keys for each milestone
    order_date_key INT,
    payment_date_key INT,
    ship_date_key INT,
    delivery_date_key INT,
    
    -- Measures
    days_to_ship INT,
    days_to_deliver INT
);
```

**4. Factless Fact Tables**

Track events with no measures:

```sql
CREATE TABLE fact_student_attendance (
    date_key INT,
    student_key INT,
    class_key INT,
    -- No measures, just the fact that student attended
    PRIMARY KEY (date_key, student_key, class_key)
);
```
""")
        
        st.markdown("#### ⚡ Warehouse Performance Optimization")
        st.markdown("""
**Make your warehouse FAST:**

**1. Indexing Strategies**

```sql
-- Index foreign keys
CREATE INDEX idx_fact_date ON fact_sales(date_key);
CREATE INDEX idx_fact_product ON fact_sales(product_key);
CREATE INDEX idx_fact_customer ON fact_sales(customer_key);

-- Composite index for common queries
CREATE INDEX idx_date_product ON fact_sales(date_key, product_key);
```

**2. Partitioning**

```sql
-- Partition fact table by date
CREATE TABLE fact_sales (
    sale_key BIGINT,
    order_date DATE,
    ...
) PARTITION BY RANGE (order_date) (
    PARTITION p2024_01 VALUES LESS THAN ('2024-02-01'),
    PARTITION p2024_02 VALUES LESS THAN ('2024-03-01'),
    ...
);
```

**Benefits:**
- Query only relevant partitions
- Faster data loading
- Easier data archival

**3. Materialized Views**

```sql
-- Pre-aggregate for common queries
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT 
    d.full_date,
    p.category,
    SUM(f.quantity) as total_quantity,
    SUM(f.revenue) as total_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY d.full_date, p.category;

-- Refresh daily
REFRESH MATERIALIZED VIEW mv_daily_sales;
```

**4. Query Optimization**

```sql
-- Bad: SELECT *
SELECT * FROM fact_sales WHERE date_key = 20241128;

-- Good: Select only needed columns
SELECT product_key, SUM(revenue) as total_revenue
FROM fact_sales
WHERE date_key = 20241128
GROUP BY product_key;

-- Better: Use aggregate table
SELECT product_key, total_revenue
FROM agg_daily_product_sales
WHERE date_key = 20241128;
```
""")
        
        st.markdown("#### 💼 Real-World Warehouse Design Examples")
        st.markdown(
            """**Learn from production warehouse designs:**

**Example 1: Retail Sales Warehouse**

**Business Requirements:**
- Track sales across 500 stores
- Analyze by product, customer, time, location
- Support daily reporting and trend analysis

**Schema Design:**

```sql
-- Fact Table
CREATE TABLE fact_sales (
    sale_key BIGINT PRIMARY KEY,
    date_key INT,
    product_key INT,
    customer_key INT,
    store_key INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);

-- Dimensions
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    sku VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    brand VARCHAR(100)
);

CREATE TABLE dim_store (
    store_key INT PRIMARY KEY,
    store_id VARCHAR(50),
    store_name VARCHAR(200),
    city VARCHAR(100),
    region VARCHAR(100),
    country VARCHAR(50)
);
```

**Example 2: Healthcare Analytics Warehouse**

**Business Requirements:**
- Track patient visits and treatments
- Analyze outcomes and costs
- Support quality metrics and compliance

**Schema Design:**

```sql
CREATE TABLE fact_patient_visit (
    visit_key BIGINT PRIMARY KEY,
    patient_key INT,
    provider_key INT,
    facility_key INT,
    visit_date_key INT,
    diagnosis_code VARCHAR(20),
    procedure_code VARCHAR(20),
    visit_cost DECIMAL(10,2),
    duration_minutes INT
);
```
"""
        )
        
        st.markdown("#### ✅ Data Warehouse Best Practices")
        st.markdown(
            """**Follow these practices for production warehouses:**

**1. Naming Conventions**
- Facts: `fact_` prefix (fact_sales, fact_orders)
- Dimensions: `dim_` prefix (dim_customer, dim_product)
- Aggregates: `agg_` prefix (agg_daily_sales)
- Keys: `_key` suffix (customer_key, date_key)

**2. Data Types**
- Use INT for keys (faster joins)
- Use DECIMAL for money (avoid floating point errors)
- Use DATE/TIMESTAMP for dates (not strings)
- Use VARCHAR with appropriate lengths

**3. Indexing Strategy**
```sql
-- Always index foreign keys
CREATE INDEX idx_fact_date ON fact_sales(date_key);
CREATE INDEX idx_fact_product ON fact_sales(product_key);
CREATE INDEX idx_fact_customer ON fact_sales(customer_key);
```

**4. Partitioning Strategy**
```sql
-- Partition large fact tables by date
CREATE TABLE fact_sales (
    ...
) PARTITION BY RANGE (date_key);
```

**5. Documentation**
- Document all tables and columns
- Maintain data dictionary
- Track data lineage
- Document business rules

**6. Testing**
- Test referential integrity
- Validate data quality
- Test query performance
- Monitor data volumes
"""
        )
        
        st.markdown("#### 🏗️ Advanced Data Warehouse Optimization Techniques")
        st.markdown(
            """**Performance Tuning for Large-Scale Warehouses:**

**1. Materialized Views**

Precompute expensive aggregations for faster queries.

**When to Use:**
- Queries run repeatedly with same aggregation logic
- Source tables are large but change infrequently
- Query latency is critical (dashboards, reports)

**Example Use Case:**
Daily sales summary dashboard querying 5-year transaction history (billions of rows).

**Trade-offs:**
- Pro: 100X+ query speedup
- Con: Storage cost, refresh overhead, staleness

**Refresh Strategies:**
- Full Refresh: Rebuild entire view (simple but slow)
- Incremental Refresh: Update only changed data (complex but fast)
- On-Demand: Refresh when source data changes
- Scheduled: Nightly/hourly batch refresh

**2. Partition Pruning**

Only scan relevant partitions based on query predicates.

**Best Practices:**
- Partition by date/time (most common filter)
- Limit partitions to 1000-5000 per table
- Use YYYY-MM-DD format for dates
- Avoid over-partitioning (too many small files)

**Example:**
Query: SELECT * FROM sales WHERE date >= '2024-01-01'
- Without partitioning: Scans 5 years of data (10 TB)
- With daily partitions: Scans only 2024 data (2 TB)
- Cost savings: 80% reduction in compute

**3. Columnar Storage Optimization**

Store data by column rather than row for analytical queries.

**Formats:**
- Parquet: Industry standard, great compression
- ORC: Optimized for Hive, good for Hadoop
- Arrow: In-memory columnar, fast processing

**Compression:**
- Snappy: Fast compression, moderate ratio (5:1)
- Gzip: Slower but better compression (10:1)
- Zstd: Best balance of speed and ratio (7:1)

**Example:**
1 TB CSV file → 150 GB Parquet with Snappy
- 85% storage reduction
- 10X faster queries (column pruning)
- Lower cloud costs

**4. Query Result Caching**

Cache frequently accessed query results.

**Implementation:**
- Application-level: Redis, Memcached
- Database-level: Snowflake result cache, BigQuery cache
- CDN-level: CloudFront for API responses

**Cache Invalidation Strategies:**
- Time-based (TTL): Cache for 1 hour, 1 day, etc.
- Event-based: Invalidate when source data updates
- Manual: Explicit cache clear on deployments

**5. Indexing Strategies**

Create indexes on frequently filtered columns.

**Index Types:**
- B-Tree: General purpose, good for range queries
- Hash: Fast equality lookups, no range support
- Bitmap: Great for low-cardinality columns
- Full-text: Search on text fields

**Anti-patterns:**
- Too many indexes (slows down writes)
- Indexing high-cardinality columns in OLAP (often not worth it)
- Not updating statistics after bulk loads

---

**Data Warehouse Architecture Patterns:**

**Pattern 1: Hub-and-Spoke**

Central warehouse with department-specific data marts.

**Structure:**
- Enterprise Data Warehouse (EDW): Single source of truth
- Data Marts: Finance, Marketing, Sales, HR specific
- ETL: Source → EDW → Data Marts

**Pros:**
- Clear ownership
- Optimized for department needs
- Reduced query contention

**Cons:**
- Data duplication
- Sync complexity
- Higher storage costs

**Best for:** Large enterprises with distinct business units

**Pattern 2: Data Vault 2.0**

Highly normalized, audit-friendly warehouse design.

**Components:**
- Hubs: Business keys (Customer, Product)
- Links: Relationships (Order-Customer, Order-Product)
- Satellites: Descriptive attributes with history

**Pros:**
- Full data lineage
- Audit trail built-in
- Handles late-arriving data
- Parallelizable loads

**Cons:**
- Complex to understand
- Many joins for queries
- Requires dimensional mart layer

**Best for:** Regulated industries (finance, healthcare), audit requirements

**Pattern 3: Kimball Dimensional Modeling**

Star schema with fact tables and dimension tables.

**Design:**
- Fact Tables: Metrics, measurements (sales, clicks)
- Dimension Tables: Context, attributes (product, customer, date)
- Denormalized for query performance

**Pros:**
- Easy to understand
- Fast queries
- BI tool friendly

**Cons:**
- Data duplication
- Complex slowly changing dimensions
- Harder to add new sources

**Best for:** BI/reporting, business user queries

**Pattern 4: Lambda Architecture**

Separate batch and speed layers for real-time + historical.

**Layers:**
- Batch Layer: Complete, accurate historical data (Hive, Redshift)
- Speed Layer: Recent data with low latency (Druid, ClickHouse)
- Serving Layer: Merge views from both layers

**Pros:**
- Real-time and batch support
- Fault-tolerant
- Scalable

**Cons:**
- Complex (two processing paths)
- Potential inconsistency
- Higher operational cost

**Best for:** Real-time dashboards with historical context

**Pattern 5: Kappa Architecture**

Everything is a stream (simpler than Lambda).

**Design:**
- Single processing path using stream processing
- Reprocess historical data by replaying streams
- Store in stream-friendly storage (Kafka, Kinesis)

**Pros:**
- Simpler than Lambda
- One codebase
- Event-driven

**Cons:**
- Requires stream-first mindset
- Reprocessing can be slow
- Limited batch optimizations

**Best for:** Event-driven systems, microservices

---

**Real-World Data Warehouse Scaling Examples:**

**Example 1: E-Commerce Company (100M orders/year)**

**Challenge:**
- Holiday traffic spikes (10X normal load)
- Customer 360 queries timeout (20+ seconds)
- Analyst ad-hoc queries slow down production

**Solution:**
1. Partitioned fact_orders by order_date (daily partitions)
2. Created dim_customer_summary materialized view
3. Separated analyst workload to read replica
4. Implemented query result caching (Redis, 1-hour TTL)
5. Added bitmap indexes on status, category columns

**Results:**
- Query latency: 20s → 2s (90% improvement)
- Black Friday handled without downtime
- Analyst queries no longer impact production
- Infrastructure cost: +15% (caching, replicas)

**Example 2: SaaS Analytics Platform (1000 tenants)**

**Challenge:**
- Tenant isolation required (regulatory)
- Some tenants have 1000X more data than others
- Cross-tenant analytics for benchmarking

**Solution:**
1. Schema per tenant (PostgreSQL schemas)
2. Dedicated clusters for top 10 tenants
3. Shared cluster for long-tail tenants
4. Aggregate tables for cross-tenant queries
5. Query governor: 5-minute timeout, max 1GB scan

**Results:**
- Tenant isolation: 100% compliant
- Large tenants: No noisy neighbor issues
- Cross-tenant queries: <10 seconds
- Cost allocation: Per-tenant tracking

**Example 3: Financial Services Firm (Regulatory Compliance)**

**Challenge:**
- 7-year data retention required
- Audit trail for every change
- Sub-second query for fraud detection
- Zero data loss tolerance

**Solution:**
1. Data Vault 2.0 architecture
2. Time-travel queries (temporal tables)
3. Write-Ahead Logging (WAL) for durability
4. Hot tier (last 90 days): SSD, hourly refresh
5. Warm tier (91 days-2 years): Standard storage
6. Cold tier (2-7 years): Glacier, compliance archive

**Results:**
- Full audit history: Every change tracked
- Fraud queries: <500ms (hot tier)
- Compliance: Passed all audits
- Storage cost: 60% reduction (tiering)

---

**Data Warehouse Governance:**

**1. Data Quality Rules**
- No NULLs in dimension business keys
- Fact table foreign keys must exist in dimensions
- Date dimensions must be complete (no gaps)
- Numeric measures must be non-negative where applicable

**2. Naming Conventions**
- Tables: fact_xxx, dim_xxx, stg_xxx (staging), tmp_xxx (temporary)
- Columns: snake_case, consistent suffixes (_id, _key, _date, _amount)
- Views: vw_xxx or mv_xxx (materialized)

**3. Access Control**
- Principle of least privilege
- Role-based access (Analyst, Engineer, Admin)
- Column-level security for PII
- Row-level security for multi-tenant

**4. Change Management**
- Version control all DDL (Git)
- Code review for schema changes
- Testing in dev/staging before production
- Rollback plan for every migration

**5. Cost Management**
- Set query timeouts to prevent runaway queries
- Limit scan size (e.g., max 1 TB per query)
- Monitor top 10 most expensive queries
- Chargeback to business units
"""
        )
    elif unit_number == 3:
        st.markdown("#### 📘 Batch Processing at Scale: Apache Spark Mastery")
        st.markdown(
            """When your data exceeds what a single machine can handle (100GB+), you need 
**distributed computing**. Apache Spark is the industry standard for batch processing at scale.

**Why Spark?**

- ✅ Process terabytes to petabytes of data
- ✅ 100x faster than Hadoop MapReduce
- ✅ Unified API for batch and streaming
- ✅ Works with Python, Scala, Java, R
- ✅ Integrates with all major cloud platforms

**Spark Architecture:**

1. **Driver Program**
   - Your application code
   - Coordinates execution
   - Manages SparkContext

2. **Cluster Manager**
   - YARN, Mesos, Kubernetes, or Standalone
   - Allocates resources
   - Manages worker nodes

3. **Executors**
   - Run on worker nodes
   - Execute tasks
   - Store data in memory/disk

**Key Concepts:**

**RDD (Resilient Distributed Dataset):**
- Low-level API
- Immutable distributed collection
- Fault-tolerant

**DataFrame:**
- High-level API (like pandas)
- Optimized query execution
- Schema enforcement
- **Use this 95% of the time!**

**Dataset:**
- Type-safe DataFrames
- Compile-time type checking
- Scala/Java only
"""
        )

        st.markdown("#### ⚡ Spark Fundamentals: DataFrames & Transformations")
        st.markdown(
            """**Basic Spark Operations:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg

# Initialize Spark
spark = SparkSession.builder.appName("MyApp").getOrCreate()

# Read data
df = spark.read.parquet('s3://bucket/sales.parquet')

# Transformations (lazy - not executed yet)
df_filtered = df.filter(col('amount') > 100)
df_grouped = df.groupBy('customer_id').agg(sum('amount'))

# Action (triggers execution)
result = df_grouped.collect()  # Returns data to driver
df_grouped.write.parquet('output/')  # Writes to storage
```

**Lazy Evaluation:**
- Transformations are NOT executed immediately
- Spark builds an execution plan
- Only runs when you call an action (collect, write, count)
- Allows Spark to optimize the entire workflow

**Common Transformations:**
- `select()` - Choose columns
- `filter()` / `where()` - Filter rows
- `groupBy()` - Group for aggregation
- `join()` - Join DataFrames
- `withColumn()` - Add/modify column
- `orderBy()` - Sort data

**Common Actions:**
- `count()` - Count rows
- `collect()` - Return all data to driver
- `show()` - Display sample
- `write()` - Save to storage
"""
        )

        st.markdown("#### 🗂️ Partitioning & Performance Optimization")
        st.markdown(
            """**Partitioning is KEY to Spark performance!**

**What is Partitioning?**
- Data is split into chunks (partitions)
- Each partition processed independently
- More partitions = more parallelism

**Partition Size Guidelines:**
- ✅ Target: 128MB - 1GB per partition
- ❌ Too small (<10MB): Too much overhead
- ❌ Too large (>2GB): Memory issues

**Partitioning Strategies:**

1. **File-based Partitioning:**
```python
# Write with partitioning
df.write.partitionBy('year', 'month').parquet('output/')

# Creates structure:
# output/year=2024/month=01/part-00000.parquet
# output/year=2024/month=02/part-00000.parquet
```

2. **Repartition for Parallelism:**
```python
# Increase partitions for more parallelism
df_repartitioned = df.repartition(200)

# Repartition by column (for joins)
df_by_customer = df.repartition('customer_id')
```

3. **Coalesce to Reduce:**
```python
# Reduce partitions (no shuffle)
df_small = df.coalesce(10)
```

**Performance Killers:**

❌ **Shuffle:** Moving data between partitions
- Caused by: joins, groupBy, repartition
- Solution: Use broadcast joins for small tables

❌ **Data Skew:** Uneven partition sizes
- Caused by: Hot keys (one customer has 90% of orders)
- Solution: Salt keys, custom partitioning

❌ **Spill to Disk:** Not enough memory
- Caused by: Too much data per partition
- Solution: Increase partitions, add memory

**Optimization Checklist:**
- ✅ Use DataFrame API (not RDD)
- ✅ Filter early (predicate pushdown)
- ✅ Broadcast small tables (<200MB)
- ✅ Cache frequently used DataFrames
- ✅ Partition by commonly filtered columns
- ✅ Use Parquet format (columnar, compressed)
- ✅ Enable adaptive query execution
"""
        )
        
        st.markdown("#### 🔧 Advanced Spark Transformations")
        st.markdown("""
**Master these Spark operations:**

**1. Window Functions**

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, lag, lead

# Rank products by revenue within each category
window_spec = Window.partitionBy('category').orderBy(col('revenue').desc())

df_ranked = df.withColumn('rank', row_number().over(window_spec))

# Get previous month's sales
window_time = Window.partitionBy('product_id').orderBy('month')
df_with_prev = df.withColumn('prev_month_sales', lag('sales', 1).over(window_time))
```

**2. User-Defined Functions (UDFs)**

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Define UDF
@udf(returnType=StringType())
def categorize_amount(amount):
    if amount > 1000:
        return 'High'
    elif amount > 100:
        return 'Medium'
    else:
        return 'Low'

# Use UDF
df_categorized = df.withColumn('amount_category', categorize_amount(col('amount')))
```

**Warning:** UDFs are slow! Use built-in functions when possible.

**3. Complex Aggregations**

```python
from pyspark.sql.functions import collect_list, collect_set, percentile_approx

result = df.groupBy('customer_id').agg(
    count('order_id').alias('num_orders'),
    sum('amount').alias('total_spent'),
    avg('amount').alias('avg_order'),
    percentile_approx('amount', 0.5).alias('median_order'),
    collect_list('product_id').alias('products_purchased'),
    collect_set('category').alias('unique_categories')
)
```
""")
        
        st.markdown("#### 🔗 Spark Join Optimization")
        st.markdown("""
**Joins are expensive - optimize them!**

**1. Broadcast Join (Small Table)**

```python
from pyspark.sql.functions import broadcast

# Bad: Regular join (shuffle both tables)
result = large_df.join(small_df, 'key')

# Good: Broadcast join (no shuffle for small table)
result = large_df.join(broadcast(small_df), 'key')
```

**When to use:** Small table < 200MB

**2. Bucketed Join**

```python
# Pre-bucket tables by join key
large_df.write.bucketBy(100, 'customer_id').saveAsTable('sales_bucketed')
small_df.write.bucketBy(100, 'customer_id').saveAsTable('customers_bucketed')

# Join bucketed tables (no shuffle!)
sales = spark.table('sales_bucketed')
customers = spark.table('customers_bucketed')
result = sales.join(customers, 'customer_id')
```

**3. Handling Data Skew**

```python
# Problem: One customer has 90% of orders (hot key)
# Solution: Salt the key

from pyspark.sql.functions import rand, concat

# Add salt to skewed table
skewed_df = df.withColumn('salt', (rand() * 10).cast('int'))
skewed_df = skewed_df.withColumn('salted_key', concat(col('customer_id'), col('salt')))

# Replicate small table
replicated_df = small_df.crossJoin(spark.range(10).withColumnRenamed('id', 'salt'))
replicated_df = replicated_df.withColumn('salted_key', concat(col('customer_id'), col('salt')))

# Join on salted key
result = skewed_df.join(replicated_df, 'salted_key')
```
""")
        
        st.markdown("#### 💾 Delta Lake: ACID for Data Lakes")
        st.markdown("""
**Delta Lake adds reliability to data lakes:**

**Key Features:**

1. **ACID Transactions**
   - Atomic writes (all or nothing)
   - Isolation (concurrent reads/writes)
   - Consistency (data integrity)
   - Durability (committed data persists)

2. **Time Travel**
   - Query previous versions
   - Rollback bad writes
   - Audit changes

3. **Schema Evolution**
   - Add columns safely
   - Enforce schema
   - Merge schema on write

**Example:**

```python
from delta.tables import DeltaTable

# Write Delta table
df.write.format('delta').mode('overwrite').save('/data/delta/sales')

# Read Delta table
df_delta = spark.read.format('delta').load('/data/delta/sales')

# Time travel
df_v1 = spark.read.format('delta').option('versionAsOf', 1).load('/data/delta/sales')
df_yesterday = spark.read.format('delta').option('timestampAsOf', '2024-11-27').load('/data/delta/sales')

# Upsert (merge)
delta_table = DeltaTable.forPath(spark, '/data/delta/sales')

delta_table.alias('target').merge(
    new_data.alias('source'),
    'target.order_id = source.order_id'
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

# Optimize & vacuum
delta_table.optimize().executeCompaction()
delta_table.vacuum(168)  # Remove files older than 7 days
```
""")
        
        st.markdown("#### 🔧 Spark Troubleshooting Guide")
        st.markdown(
            """**Common Spark issues and solutions:**

**Problem 1: Out of Memory Errors**

**Symptoms:**
- `java.lang.OutOfMemoryError`
- Executors crashing
- Spill to disk warnings

**Solutions:**
```python
# Increase executor memory
spark = SparkSession.builder \\
    .config("spark.executor.memory", "8g") \\
    .config("spark.driver.memory", "4g") \\
    .getOrCreate()

# Increase partitions
df_repartitioned = df.repartition(500)

# Use iterative processing
for partition in df.rdd.mapPartitions(process_partition):
    save_to_db(partition)
```

**Problem 2: Slow Joins**

**Symptoms:**
- Join takes hours
- Excessive shuffle

**Solutions:**
```python
# Use broadcast for small tables
result = large_df.join(broadcast(small_df), 'key')

# Pre-partition both tables
large_df.write.bucketBy(100, 'key').saveAsTable('large_bucketed')
small_df.write.bucketBy(100, 'key').saveAsTable('small_bucketed')
```

**Problem 3: Data Skew**

**Symptoms:**
- One task takes 10x longer
- Uneven partition sizes

**Solutions:**
```python
# Salt the skewed key
from pyspark.sql.functions import rand, concat

skewed_df = df.withColumn('salt', (rand() * 10).cast('int'))
skewed_df = skewed_df.withColumn('salted_key', 
    concat(col('customer_id'), lit('_'), col('salt')))
```

**Problem 4: Task Not Serializable**

**Symptoms:**
- `org.apache.spark.SparkException: Task not serializable`

**Solutions:**
```python
# Bad: Using class instance in lambda
class Processor:
    def process(self, x):
        return x * 2

processor = Processor()
df.rdd.map(lambda x: processor.process(x))  # ERROR!

# Good: Use function or broadcast
def process_func(x):
    return x * 2

df.rdd.map(process_func)  # Works!
```
"""
        )
        
        st.markdown("#### 🎯 Spark Production Deployment Best Practices")
        st.markdown(
            """**Deploying Spark to Production:**

**1. Cluster Sizing & Resource Allocation**

**Executor Configuration:**
- Executor Memory: 4-8 GB per executor (sweet spot)
- Executor Cores: 4-5 cores per executor (avoid too many)
- Number of Executors: (Total Cores / Executor Cores) - 1 for driver

**Example Calculation for 100-node cluster:**
- Each node: 16 cores, 64 GB RAM
- Total: 1,600 cores, 6.4 TB RAM
- Executor config: 5 cores, 20 GB RAM (4 executors per node)
- Total executors: 400 (4 per node × 100 nodes)
- Driver: 1 node reserved

**Spark Config:**
- spark.executor.instances: 400
- spark.executor.cores: 5
- spark.executor.memory: 20g
- spark.executor.memoryOverhead: 4g
- spark.driver.memory: 16g
- spark.driver.cores: 8

**2. Monitoring & Observability**

**Key Metrics to Track:**
- Job Duration: Track P50, P95, P99 latencies
- Task Skew: Identify stragglers (tasks >2x median)
- Shuffle Size: Monitor shuffle read/write volumes
- GC Time: Keep GC overhead <10% of task time
- Memory Utilization: Track executor memory usage
- Data Skew: Partition size variance

**Monitoring Stack:**
- Spark UI: Built-in monitoring dashboard
- Ganglia/Grafana: Cluster-level metrics
- Prometheus: Time-series metrics collection
- CloudWatch/Datadog: Cloud-native monitoring
- Custom Metrics: Application-specific KPIs

**Sample Alert Rules:**
- Job failure rate >5% (critical)
- Average job duration >2x baseline (warning)
- Executor OOM errors >10/hour (critical)
- Shuffle data >1 TB per job (warning)
- GC time >10% of task time (warning)

**3. Error Handling & Retry Logic**

**Idempotent Jobs:**
All production Spark jobs should be idempotent (safe to retry).

**Techniques:**
- Write to temp location, then atomic rename
- Use unique job IDs for deduplication
- Implement checkpointing for streaming jobs
- Track watermarks for incremental processing

**Retry Strategy:**
- Transient failures: Retry 3x with exponential backoff
- Data quality failures: Write to error queue, alert on-call
- Resource exhaustion: Scale up, then retry
- Code bugs: Fail fast, alert engineers

**4. Performance Tuning Checklist**

**Data Ingestion:**
- Use optimal file formats (Parquet, ORC)
- Partition data by commonly filtered columns
- Compress data (Snappy for speed, Gzip for size)
- Coalesce small files (aim for 128-256 MB per file)

**Transformations:**
- Cache intermediate results if reused
- Broadcast small lookup tables (<10 GB)
- Use narrow transformations when possible
- Minimize shuffles (coalesce, repartition sparingly)

**Joins:**
- Broadcast hash join for small tables
- Sort-merge join for large tables
- Bucket both sides if possible
- Filter before joining to reduce data volume

**Writes:**
- Repartition before writing to control file count
- Use dynamic partitioning for partitioned tables
- Enable speculation for slow tasks
- Write to distributed file system (S3, HDFS, GCS)

**5. Cost Optimization**

**Spot Instances:**
Use spot/preemptible instances for non-critical workloads.

**Strategy:**
- Core nodes: On-demand (stability)
- Task nodes: Spot instances (cost savings)
- Savings: 60-80% reduction on compute costs

**Auto-scaling:**
- Scale up during peak hours (8 AM - 6 PM)
- Scale down during off-hours
- Use EMR/Dataproc auto-scaling policies
- Set min/max cluster size boundaries

**Data Lifecycle:**
- Hot data (last 30 days): Standard storage
- Warm data (31-90 days): Infrequent access
- Cold data (90+ days): Glacier/Archive
- Purge after retention period (e.g., 7 years)

**6. Security Best Practices**

**Authentication & Authorization:**
- Use Kerberos for authentication
- Implement RBAC for data access
- Encrypt data at rest (S3 SSE, HDFS encryption)
- Encrypt data in transit (TLS/SSL)

**Data Masking:**
- PII columns: Hash or tokenize
- Sensitive data: Column-level encryption
- Audit logs: Track all data access

**Network Security:**
- Private subnets for clusters
- Security groups: Restrict to minimal ports
- VPN/PrivateLink for cloud connectivity
- No public IPs on data nodes

**7. Disaster Recovery**

**Backup Strategy:**
- Daily snapshots of critical data
- Cross-region replication for DR
- Retain backups for 30 days minimum
- Test restore procedures quarterly

**Recovery Time Objectives:**
- Critical jobs: RTO <1 hour
- Standard jobs: RTO <4 hours
- Low-priority jobs: RTO <24 hours

**Runbook:**
- Document common failure scenarios
- Step-by-step recovery procedures
- Contact information for escalations
- Post-mortem template for incidents

---

**Real-World Production Scenarios:**

**Scenario 1: Black Friday Traffic Spike**

**Challenge:**
E-commerce analytics pipeline processing 10X normal data volume (1 TB → 10 TB).

**Solution:**
1. Pre-scale cluster 2 days before (50 → 200 nodes)
2. Enable auto-scaling (max 500 nodes)
3. Implement backpressure in streaming jobs
4. Cache hot data (top products, users)
5. Set up war room for monitoring

**Results:**
- Processed 10 TB in 6 hours (vs 60 hours without prep)
- Zero downtime during peak traffic
- Scaled down gracefully post-event
- Cost: 3X normal, but revenue justified

**Scenario 2: Data Quality Incident**

**Challenge:**
Upstream service sent malformed JSON, breaking downstream pipelines.

**Problem:**
- 50,000 records rejected
- Data loss detected 6 hours later
- Business reports showing incorrect metrics

**Solution:**
1. Immediate: Stop all downstream pipelines
2. Root cause: Added schema validation to ingestion
3. Recovery: Reprocess last 24 hours of data
4. Prevention: Implement Great Expectations checks
5. Alerting: Real-time data quality monitoring

**Results:**
- Recovered within 4 hours
- Zero data loss (replayed from source)
- Schema validation prevented future issues
- SLA maintained (99.9% uptime)

**Scenario 3: Cost Optimization Initiative**

**Challenge:**
Monthly Spark job costs reached $50K, need to reduce by 30%.

**Analysis:**
- 40% of jobs running on under-utilized clusters
- Many small files (overhead from file opens)
- Excessive data scanning (no partitioning)
- Jobs running during peak hours (expensive)

**Optimizations:**
1. Consolidated small jobs into batch workflows
2. Compacted small files (10M files → 100K files)
3. Implemented table partitioning by date
4. Shifted non-critical jobs to off-peak hours
5. Used spot instances for 60% of cluster

**Results:**
- Cost reduced from $50K → $30K/month (40% savings)
- Job performance improved (less overhead)
- No business impact (same SLAs maintained)
- ROI: $240K annual savings

---

**Production Deployment Checklist:**

Before deploying to production:

**Code Quality:**
- [ ] Unit tests pass (>80% coverage)
- [ ] Integration tests pass
- [ ] Code review completed
- [ ] No hardcoded credentials
- [ ] Proper error handling

**Performance:**
- [ ] Load tested with production-scale data
- [ ] Memory profiling completed
- [ ] No memory leaks detected
- [ ] Query plans reviewed
- [ ] Partitioning strategy validated

**Monitoring:**
- [ ] Metrics instrumentation added
- [ ] Alerts configured
- [ ] Dashboards created
- [ ] Runbook documented
- [ ] On-call rotation scheduled

**Security:**
- [ ] Data encryption enabled
- [ ] Access controls configured
- [ ] Secrets in vault (not code)
- [ ] Audit logging enabled
- [ ] Compliance requirements met

**Operations:**
- [ ] Deployment automation tested
- [ ] Rollback procedure documented
- [ ] Capacity planning completed
- [ ] DR plan validated
- [ ] Stakeholders notified
"""
        )
        
        st.markdown("#### 🚀 Production Spark Deployment")
        st.markdown(
            """**Deploy Spark jobs to production:**

**1. Cluster Modes**

**Client Mode:**
- Driver runs on client machine
- Good for interactive work
- Not for production

**Cluster Mode:**
- Driver runs on cluster
- Good for production
- Survives client disconnect

```bash
# Submit in cluster mode
spark-submit \\
  --master yarn \\
  --deploy-mode cluster \\
  --num-executors 10 \\
  --executor-memory 8g \\
  --executor-cores 4 \\
  my_job.py
```

**2. Resource Allocation**

```python
# Configure resources
spark = SparkSession.builder \\
    .config("spark.executor.instances", "10") \\
    .config("spark.executor.memory", "8g") \\
    .config("spark.executor.cores", "4") \\
    .config("spark.driver.memory", "4g") \\
    .config("spark.sql.shuffle.partitions", "200") \\
    .getOrCreate()
```

**3. Monitoring**

```python
# Enable metrics
spark.conf.set("spark.metrics.conf.*.sink.console.class", 
               "org.apache.spark.metrics.sink.ConsoleSink")

# Log progress
df.write.parquet('output/', mode='overwrite')
print(f"Job completed: {spark.sparkContext.statusTracker().getJobIdsForGroup()}")
```

**4. Best Practices**
- ✅ Use dynamic allocation
- ✅ Enable adaptive query execution
- ✅ Monitor Spark UI (port 4040)
- ✅ Set appropriate shuffle partitions
- ✅ Use Parquet format
- ✅ Compress output
"""
        )
    elif unit_number == 4:
        st.markdown("#### 📘 Stream Processing & Real-time Data: Complete Guide")
        st.markdown(
            """**Real-time data processing** is critical for modern applications that need 
immediate insights and actions.

**Why Stream Processing?**

**Use Cases:**
- ✅ Real-time fraud detection (banking)
- ✅ Live dashboards (e-commerce)
- ✅ IoT sensor monitoring (manufacturing)
- ✅ Social media analytics (trending topics)
- ✅ Recommendation engines (Netflix, Spotify)
- ✅ Anomaly detection (security)

**Batch vs Streaming:**

| Aspect | Batch | Streaming |
|--------|-------|----------|
| **Latency** | Hours/days | Seconds/milliseconds |
| **Data Volume** | Large chunks | Continuous flow |
| **Processing** | Scheduled | Continuous |
| **Complexity** | Lower | Higher |
| **Tools** | Spark, Hadoop | Kafka, Flink |
| **Use Case** | Reports, ML training | Alerts, live dashboards |

**Key Concepts:**

**1. Event Time vs Processing Time**
- **Event Time:** When event actually occurred
- **Processing Time:** When system processes it
- **Gap:** Network delays, system downtime
- **Solution:** Use event time + watermarks

**2. Windowing**
- **Tumbling:** Fixed, non-overlapping (every 5 minutes)
- **Sliding:** Overlapping (last 5 minutes, updated every minute)
- **Session:** Based on activity gaps

**3. State Management**
- Keep track of data across events
- Examples: running totals, user sessions
- Challenge: Fault tolerance
"""
        )

        st.markdown("#### 🌊 Apache Kafka: The Streaming Platform")
        st.markdown(
            """**Kafka** is the industry standard for event streaming.

**Architecture:**

1. **Producers:** Send events to Kafka
2. **Topics:** Categories of events
3. **Partitions:** Parallel processing
4. **Consumers:** Read events from Kafka
5. **Brokers:** Kafka servers

**Example:**
```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send event
event = {'user_id': '123', 'action': 'purchase', 'amount': 99.99}
producer.send('user_events', value=event)

# Consumer
consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    event = message.value
    print(f"Received: {event}")
```

**Kafka Guarantees:**
- At-least-once delivery (default)
- Exactly-once semantics (with configuration)
- Ordered within partition
- Durable (replicated across brokers)
"""
        )

        st.markdown("#### 🔗 Building Streaming Pipelines")
        st.markdown(
            """**Stream Processing Pattern:**

1. **Ingest:** Kafka receives events
2. **Process:** Flink/Spark Streaming transforms
3. **Store:** Write to database/data lake
4. **Serve:** Power real-time dashboards

**Windowing Example:**
```python
# Count events per minute
windowed_counts = stream \\
    .window(tumbling_window(minutes=1)) \\
    .groupBy('event_type') \\
    .count()
```

**Best Practices:**
- ✅ Use event time (not processing time)
- ✅ Handle late-arriving data
- ✅ Implement exactly-once semantics
- ✅ Monitor lag and throughput
- ✅ Plan for backpressure
"""
        )
        
        st.markdown("#### 🔧 Kafka Deep Dive: Production Patterns")
        st.markdown("""
**Advanced Kafka concepts:**

**1. Consumer Groups & Parallelism**

```python
# Multiple consumers in same group = parallel processing
consumer1 = KafkaConsumer(
    'events',
    group_id='analytics_group',  # Same group
    bootstrap_servers=['localhost:9092']
)

consumer2 = KafkaConsumer(
    'events',
    group_id='analytics_group',  # Same group
    bootstrap_servers=['localhost:9092']
)

# Kafka automatically distributes partitions between consumers
```

**2. Exactly-Once Semantics**

```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    enable_idempotence=True,  # Exactly-once
    acks='all',  # Wait for all replicas
    retries=3
)
```

**3. Schema Registry**

```python
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

value_schema = avro.loads('''{
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "user_id", "type": "string"},
        {"name": "action", "type": "string"},
        {"name": "timestamp", "type": "long"}
    ]
}''')

producer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}, default_value_schema=value_schema)
```

**4. Kafka Connect**

No-code data integration:

```json
{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.port": "5432",
    "database.user": "postgres",
    "database.dbname": "production",
    "table.include.list": "public.orders",
    "topic.prefix": "db"
  }
}
```
""")
        
        st.markdown("#### 🌊 Stream Processing with Flink")
        st.markdown("""
**Apache Flink for stateful stream processing:**

**Windowing Example:**

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
table_env = StreamTableEnvironment.create(env)

# Define source
table_env.execute_sql(''''
    CREATE TABLE user_events (
        user_id STRING,
        event_type STRING,
        amount DOUBLE,
        event_time TIMESTAMP(3),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'events'
    )
'''')

# Tumbling window aggregation
result = table_env.sql_query(''''
    SELECT 
        TUMBLE_START(event_time, INTERVAL '1' MINUTE) as window_start,
        event_type,
        COUNT(*) as event_count,
        SUM(amount) as total_amount
    FROM user_events
    GROUP BY 
        TUMBLE(event_time, INTERVAL '1' MINUTE),
        event_type
'''')
```

**State Management:**

```python
# Maintain running totals per user
class RunningTotalFunction(KeyedProcessFunction):
    def __init__(self):
        self.state = None
    
    def open(self, runtime_context):
        # Initialize state
        self.state = runtime_context.get_state(
            ValueStateDescriptor('total', Types.DOUBLE())
        )
    
    def process_element(self, value, ctx):
        current_total = self.state.value() or 0.0
        new_total = current_total + value['amount']
        self.state.update(new_total)
        
        yield (value['user_id'], new_total)
```
""")
        
        st.markdown("#### 🎯 Real-Time Use Cases & Implementations")
        st.markdown(
            """**Production streaming applications:**

**Use Case 1: Real-Time Fraud Detection**

```python
from kafka import KafkaConsumer
import json

class FraudDetector:
    def __init__(self):
        self.user_spending = {}  # Track spending per user
    
    def detect_fraud(self, transaction):
        user_id = transaction['user_id']
        amount = transaction['amount']
        
        # Rule 1: Amount > $10,000
        if amount > 10000:
            return True, "High amount"
        
        # Rule 2: 3+ transactions in 5 minutes
        recent_count = self.user_spending.get(user_id, 0)
        if recent_count >= 3:
            return True, "Rapid transactions"
        
        # Update counter
        self.user_spending[user_id] = recent_count + 1
        
        return False, "Normal"

consumer = KafkaConsumer('transactions', ...)
detector = FraudDetector()

for message in consumer:
    transaction = message.value
    is_fraud, reason = detector.detect_fraud(transaction)
    
    if is_fraud:
        alert_fraud_team(transaction, reason)
        block_transaction(transaction)
```

**Use Case 2: Live Dashboard Metrics**

```python
import redis
from kafka import KafkaConsumer

redis_client = redis.Redis()
consumer = KafkaConsumer('page_views', ...)

for message in consumer:
    event = message.value
    
    # Update real-time counters
    redis_client.incr(f"page_views:{event['page']}")
    redis_client.incr(f"user_sessions:{event['user_id']}")
    
    # Update dashboard (reads from Redis)
```

**Use Case 3: IoT Sensor Monitoring**

```python
class SensorMonitor:
    def __init__(self):
        self.thresholds = {'temperature': 80, 'pressure': 100}
    
    def check_sensor(self, reading):
        sensor_type = reading['type']
        value = reading['value']
        
        if value > self.thresholds.get(sensor_type, float('inf')):
            send_alert(f"{sensor_type} exceeded: {value}")
            trigger_shutdown(reading['device_id'])
```
"""
        )
        
        st.markdown("#### ✅ Stream Processing Best Practices")
        st.markdown(
            """**Production streaming guidelines:**

**1. Handle Late Data**
```python
# Use watermarks for late-arriving events
window_spec = window(
    col('event_time'),
    '5 minutes',
    watermark='10 minutes'  # Accept data up to 10 min late
)
```

**2. Exactly-Once Processing**
```python
# Kafka configuration
producer = KafkaProducer(
    enable_idempotence=True,
    acks='all',
    max_in_flight_requests_per_connection=1
)
```

**3. Backpressure Handling**
```python
# Limit processing rate
consumer = KafkaConsumer(
    max_poll_records=100,
    max_poll_interval_ms=300000
)
```

**4. State Management**
- Use external state store (Redis, RocksDB)
- Checkpoint state regularly
- Plan for state recovery

**5. Monitoring**
- Track consumer lag
- Monitor throughput (events/sec)
- Alert on processing delays
- Track error rates
"""
        )
    elif unit_number == 5:
        st.markdown("#### 📘 Cloud Data Platforms: AWS, GCP, Azure Mastery")
        st.markdown(
            """**Cloud platforms** have revolutionized data engineering with managed services, 
scalability, and pay-as-you-go pricing.

**Why Cloud for Data Engineering?**

**Benefits:**
- ✅ **Scalability:** Handle any data volume
- ✅ **Managed Services:** Less infrastructure management
- ✅ **Cost-Effective:** Pay only for what you use
- ✅ **Global:** Deploy worldwide
- ✅ **Integration:** Services work together seamlessly

**Cloud Data Stack:**

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Storage** | S3 | Cloud Storage | Blob Storage |
| **Warehouse** | Redshift | BigQuery | Synapse |
| **ETL** | Glue | Dataflow | Data Factory |
| **Streaming** | Kinesis | Pub/Sub | Event Hubs |
| **Orchestration** | Step Functions | Cloud Composer | Data Factory |
| **Compute** | EMR (Spark) | Dataproc | HDInsight |

**AWS Data Engineering Stack:**

```python
# S3 for storage
import boto3
s3 = boto3.client('s3')
s3.upload_file('data.csv', 'my-bucket', 'raw/data.csv')

# Glue for ETL
glue = boto3.client('glue')
glue.start_job_run(JobName='my-etl-job')

# Redshift for warehouse
import psycopg2
conn = psycopg2.connect(
    host='cluster.redshift.amazonaws.com',
    database='analytics',
    user='admin'
)
```

**Cost Optimization:**
- ✅ Use spot instances for Spark
- ✅ Compress data (Parquet, gzip)
- ✅ Partition data for query pruning
- ✅ Set lifecycle policies (delete old data)
- ✅ Monitor and set budgets
"""
        )

        st.markdown("#### ☁️ Infrastructure as Code: Terraform")
        st.markdown(
            """**Infrastructure as Code (IaC)** treats infrastructure like software.

**Why IaC?**
- ✅ Version control for infrastructure
- ✅ Reproducible environments
- ✅ Automated deployments
- ✅ Disaster recovery
- ✅ Documentation as code

**Terraform Example:**
```hcl
# Create S3 bucket
resource "aws_s3_bucket" "data_lake" {
  bucket = "my-data-lake"
  
  tags = {
    Environment = "Production"
    Team        = "Data Engineering"
  }
}

# Create Glue database
resource "aws_glue_catalog_database" "analytics" {
  name = "analytics_db"
}

# Deploy:
# terraform init
# terraform plan
# terraform apply
```

**Benefits:**
- Changes are reviewed (pull requests)
- Rollback is easy (git revert)
- Environments are identical (dev/prod)
- Team collaboration
"""
        )

        st.markdown("#### 🔐 Security & Access Control")
        st.markdown(
            """**Security is critical** in data engineering.

**Key Principles:**

1. **Least Privilege**
   - Grant minimum necessary permissions
   - Use IAM roles (not root credentials)
   - Rotate credentials regularly

2. **Encryption**
   - **At Rest:** Encrypt stored data (S3, databases)
   - **In Transit:** Use HTTPS, TLS
   - **Key Management:** AWS KMS, Azure Key Vault

3. **Network Security**
   - VPC/VNet isolation
   - Private subnets for databases
   - Security groups/firewalls

4. **Secrets Management**
   - Never hardcode credentials
   - Use AWS Secrets Manager, HashiCorp Vault
   - Environment variables for config

**Example:**
```python
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        raise e

# Use secret
db_password = get_secret('prod/db/password')
```
"""
        )
        
        st.markdown("#### ☁️ AWS Data Engineering Stack")
        st.markdown("""
**Complete AWS data pipeline:**

**1. S3 Data Lake Architecture**

```
s3://my-data-lake/
├── raw/              # Landing zone
│   ├── sales/
│   └── customers/
├── processed/       # Cleaned data
│   ├── sales/
│   └── customers/
└── curated/         # Analytics-ready
    ├── sales_summary/
    └── customer_360/
```

**2. AWS Glue ETL Job**

```python
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
df = spark.read.parquet('s3://my-bucket/raw/sales/')

# Transform
df_clean = df.filter(col('amount') > 0).dropDuplicates(['order_id'])

# Write to processed zone
df_clean.write.mode('overwrite').parquet('s3://my-bucket/processed/sales/')

job.commit()
```

**3. Lambda for Event-Driven ETL**

```python
import boto3
import json

def lambda_handler(event, context):
    # Triggered when file lands in S3
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Start Glue job
    glue = boto3.client('glue')
    response = glue.start_job_run(
        JobName='process-sales-data',
        Arguments={'--input_path': f's3://{bucket}/{key}'}
    )
    
    return {'statusCode': 200, 'body': json.dumps('Job started')}
```
""")
        
        st.markdown("#### 🔵 GCP Data Engineering Stack")
        st.markdown("""
**Complete GCP data pipeline:**

**1. BigQuery Data Warehouse**

```python
from google.cloud import bigquery

client = bigquery.Client()

# Load data from GCS
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True
)

uri = 'gs://my-bucket/sales.csv'
table_id = 'my_project.analytics.sales'

load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
load_job.result()  # Wait for completion

print(f'Loaded {load_job.output_rows} rows')
```

**2. Dataflow (Apache Beam)**

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions(
    project='my-project',
    runner='DataflowRunner',
    region='us-central1',
    temp_location='gs://my-bucket/temp'
)

with beam.Pipeline(options=options) as p:
    (
        p
        | 'Read' >> beam.io.ReadFromText('gs://my-bucket/input.csv')
        | 'Parse' >> beam.Map(parse_csv)
        | 'Filter' >> beam.Filter(lambda x: x['amount'] > 0)
        | 'Write' >> beam.io.WriteToBigQuery(
            'my_project:analytics.sales',
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
    )
```

**3. Cloud Composer (Managed Airflow)**

```python
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

dag = DAG('gcp_etl', schedule_interval='@daily')

query_task = BigQueryInsertJobOperator(
    task_id='run_query',
    configuration={
        'query': {
            'query': 'SELECT * FROM `project.dataset.table`',
            'useLegacySql': False
        }
    },
    dag=dag
)
```
""")
        
        st.markdown("#### 💰 Cloud Cost Optimization")
        st.markdown("""
**Reduce cloud costs without sacrificing performance:**

**1. Storage Optimization**

```python
# Use Parquet (10x compression vs CSV)
df.write.parquet('s3://bucket/data.parquet')  # Good
df.write.csv('s3://bucket/data.csv')  # Bad (expensive)

# Partition data for query pruning
df.write.partitionBy('year', 'month').parquet('s3://bucket/sales/')

# Lifecycle policies (delete old data)
# In Terraform:
resource "aws_s3_bucket_lifecycle_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  
  rule {
    id = "delete_old_raw"
    status = "Enabled"
    
    expiration {
      days = 90  # Delete raw data after 90 days
    }
    
    filter {
      prefix = "raw/"
    }
  }
}
```

**2. Compute Optimization**

```python
# Use Spot/Preemptible instances for Spark
# AWS EMR:
emr_config = {
    'InstanceGroups': [
        {
            'InstanceRole': 'MASTER',
            'InstanceType': 'm5.xlarge',
            'InstanceCount': 1
        },
        {
            'InstanceRole': 'CORE',
            'InstanceType': 'm5.xlarge',
            'InstanceCount': 2,
            'Market': 'SPOT',  # 70% cheaper!
            'BidPrice': '0.10'
        }
    ]
}
```

**3. Query Optimization**

```sql
-- BigQuery: Use partitioned tables
CREATE TABLE analytics.sales
PARTITION BY DATE(order_date)
AS SELECT * FROM raw.sales;

-- Query only needed partitions
SELECT * FROM analytics.sales
WHERE order_date >= '2024-11-01'  -- Scans only Nov partition
```

**4. Monitoring Costs**

```python
import boto3

# Get AWS cost
ce = boto3.client('ce')
response = ce.get_cost_and_usage(
    TimePeriod={'Start': '2024-11-01', 'End': '2024-11-30'},
    Granularity='DAILY',
    Metrics=['UnblendedCost'],
    GroupBy=[{'Type': 'SERVICE', 'Key': 'SERVICE'}]
)

for result in response['ResultsByTime']:
    print(f"Date: {result['TimePeriod']['Start']}")
    for group in result['Groups']:
        service = group['Keys'][0]
        cost = group['Metrics']['UnblendedCost']['Amount']
        print(f"  {service}: ${float(cost):.2f}")
```
""")
        
        st.markdown("#### 🏗️ Cloud Data Architecture Patterns")
        st.markdown(
            """**Production-grade cloud architectures:**

**Pattern 1: Lambda Architecture (AWS)**

```
Data Sources
    |
    +---> Kinesis Firehose --> S3 (Raw)
    |                            |
    |                            +---> Glue ETL --> S3 (Processed)
    |                            |                   |
    |                            |                   +---> Athena (Queries)
    |
    +---> Kinesis Streams --> Lambda --> DynamoDB (Real-time)
```

**Components:**
- **Ingestion:** Kinesis Firehose, Kinesis Streams
- **Storage:** S3 (data lake), DynamoDB (operational)
- **Processing:** Glue (batch), Lambda (stream)
- **Analytics:** Athena, QuickSight

**Pattern 2: Modern Data Stack (GCP)**

```
Data Sources --> Pub/Sub --> Dataflow --> BigQuery --> Looker
                                |
                                +---> Cloud Storage
```

**Pattern 3: Medallion Architecture (Multi-Cloud)**

```
Sources --> Bronze (Raw) --> Silver (Cleaned) --> Gold (Aggregated)
              S3/ADLS         Delta Lake           Star Schema
```
"""
        )
        
        st.markdown("#### 💰 Advanced Cost Optimization")
        st.markdown(
            """**Reduce cloud costs significantly:**

**1. Storage Cost Optimization**

```python
# AWS S3 Lifecycle Policy
import boto3

s3 = boto3.client('s3')

lifecycle_policy = {
    'Rules': [
        {
            'Id': 'archive-old-data',
            'Status': 'Enabled',
            'Transitions': [
                {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                {'Days': 90, 'StorageClass': 'GLACIER'}
            ]
        }
    ]
}

s3.put_bucket_lifecycle_configuration(
    Bucket='my-data-lake',
    LifecycleConfiguration=lifecycle_policy
)

print("Expected savings: 80% on archived data")
```

**2. Use Spot Instances**
- 70-90% cheaper than on-demand
- Perfect for fault-tolerant batch jobs
- AWS Spot, GCP Preemptible, Azure Spot

**3. Partition and Compress Data**
```sql
-- Bad: Full table scan - $50
SELECT * FROM sales WHERE order_date = '2024-01-01';

-- Good: Partition pruning - $0.50
SELECT * FROM sales 
WHERE year = 2024 AND month = 1 AND day = 1;
```

**Cost Checklist:**
- ✅ Use appropriate storage tiers
- ✅ Implement lifecycle policies
- ✅ Partition large tables
- ✅ Use columnar formats (Parquet)
- ✅ Compress data
- ✅ Use Spot instances
- ✅ Set budget alerts
"""
        )
        
        st.markdown("#### 🏢 Real-World Cloud Architecture Case Studies")
        st.markdown(
            """**Case Study 1: Netflix - Streaming Analytics at Massive Scale**

**Challenge:** Process 450+ billion events/day from 200M+ subscribers across 190 countries.

**Architecture:**
- **Ingestion:** Amazon Kinesis (500K events/second)
- **Processing:** Apache Flink on EMR
- **Storage:** S3 Data Lake (100+ PB)
- **Analytics:** Redshift + Presto
- **Real-time:** ElastiCache for user sessions

**Key Decisions:**
```
1. Event Streaming: Kinesis over Kafka
   - Reason: Fully managed, auto-scaling
   - Cost: $0.015 per million events

2. Storage: S3 + Parquet
   - Partitioning: /year/month/day/hour/
   - Compression: Snappy (5:1 ratio)
   - Lifecycle: Standard → IA → Glacier

3. Query Engine: Presto for ad-hoc
   - 10,000+ queries/day
   - Sub-second response times
   - Federation across S3, MySQL, Cassandra
```

**Results:**
- 99.99% uptime
- <5 minute data freshness
- $50M/year infrastructure cost
- 10X improvement in query performance

---

**Case Study 2: Spotify - Recommendation Engine Pipeline**

**Challenge:** Generate personalized playlists for 500M users using listening history.

**Architecture:**
```
User Listening → Kafka → Spark Streaming → BigQuery → ML Models → Recommendations
     ↓
Cloud Storage (Event Lake)
     ↓
Dataflow (Batch Processing)
     ↓
BigQuery (Analytics Warehouse)
```

**Implementation:**
```python
# Real-time listening events
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('spotify-prod', 'listening-events')

def publish_listening_event(user_id, track_id, timestamp):
    data = json.dumps({
        'user_id': user_id,
        'track_id': track_id,
        'timestamp': timestamp,
        'platform': 'mobile',
        'country': 'US'
    })
    
    publisher.publish(topic_path, data.encode('utf-8'))

# Dataflow processing (Apache Beam)
import apache_beam as beam

class ComputeListeningStats(beam.DoFn):
    def process(self, element):
        user_id, events = element
        
        total_time = sum(e['duration'] for e in events)
        top_genres = Counter(e['genre'] for e in events).most_common(5)
        
        yield {
            'user_id': user_id,
            'total_listening_minutes': total_time / 60,
            'top_genres': top_genres,
            'unique_artists': len(set(e['artist'] for e in events))
        }

pipeline = (
    beam.Pipeline()
    | 'Read from PubSub' >> beam.io.ReadFromPubSub(subscription=sub)
    | 'Window' >> beam.WindowInto(beam.window.FixedWindows(3600))  # 1 hour
    | 'Group by User' >> beam.GroupByKey()
    | 'Compute Stats' >> beam.ParDo(ComputeListeningStats())
    | 'Write to BigQuery' >> beam.io.WriteToBigQuery('user_listening_stats')
)
```

**Optimization Techniques:**
1. **Caching:** Redis for hot user data (10M most active users)
2. **Partitioning:** BigQuery tables by date for cost optimization
3. **Batch vs Stream:** Batch for historical, stream for real-time
4. **Cost Control:** $20M/year → $12M/year with optimizations

---

**Case Study 3: Uber - Trip Data Pipeline**

**Challenge:** Process 15M+ trips/day across real-time and batch workflows.

**Architecture:**
```
Mobile Apps → Kafka → Flink/Samza → Hadoop HDFS → Hive/Presto
                 ↓
           Redis (Caching)
                 ↓
        PostgreSQL (Transactional)
```

**Data Flow:**
```sql
-- Real-time aggregations (Flink SQL)
CREATE TABLE trip_stats AS
SELECT 
    driver_id,
    TUMBLE_START(event_time, INTERVAL '5' MINUTE) as window_start,
    COUNT(*) as trip_count,
    SUM(fare) as total_earnings,
    AVG(rating) as avg_rating
FROM trip_events
GROUP BY driver_id, TUMBLE(event_time, INTERVAL '5' MINUTE);
```

**Batch Processing (Hive):**
```sql
-- Daily aggregations for analytics
INSERT OVERWRITE TABLE daily_city_metrics
PARTITION (date='2024-01-01')
SELECT 
    city_id,
    COUNT(DISTINCT driver_id) as active_drivers,
    COUNT(*) as total_trips,
    SUM(distance_km) as total_distance,
    AVG(wait_time_minutes) as avg_wait_time,
    PERCENTILE(fare, 0.95) as p95_fare
FROM trips
WHERE date = '2024-01-01'
GROUP BY city_id;
```

**Scaling Strategy:**
- 3,000+ Kafka brokers
- 100,000+ CPU cores (Hadoop cluster)
- 100 PB of data storage
- Multi-region active-active setup

**Key Lessons:**
1. Separate hot/cold data paths
2. Use caching aggressively (Redis)
3. Partition everything by geography
4. Monitor at every layer
"""
        )
        
        st.markdown("#### 💼 Data Engineering Career Paths & Salary Guide")
        st.markdown(
            """**Career Progression in Data Engineering:**

**Level 1: Junior Data Engineer (0-2 years)**
- Salary Range: $70K - $95K USD
- Focus: Learning pipelines, SQL, basic Spark
- Responsibilities: Bug fixes, data quality checks, simple ETL jobs
- Key Skills: Python, SQL, Git, basic cloud services
- Common Tasks: Writing SQL queries, debugging failed jobs, data validation

**Level 2: Mid-Level Data Engineer (2-4 years)**
- Salary Range: $95K - $130K USD  
- Focus: Building robust pipelines, system design
- Responsibilities: Design ETL workflows, optimize queries, mentor juniors
- Key Skills: Spark, Kafka, Airflow, cloud platforms (AWS/GCP/Azure)
- Common Tasks: Architecting data pipelines, performance tuning, code reviews

**Level 3: Senior Data Engineer (4-7 years)**
- Salary Range: $130K - $180K USD
- Focus: Architecture, scaling, best practices
- Responsibilities: System architecture, technical leadership, cross-team collaboration
- Key Skills: Distributed systems, data modeling, stream processing, infrastructure as code
- Common Tasks: Designing data platforms, capacity planning, technical strategy

**Level 4: Staff/Principal Data Engineer (7-10+ years)**
- Salary Range: $180K - $250K+ USD
- Focus: Company-wide data strategy, innovation
- Responsibilities: Technical vision, influence across org, solve hardest problems
- Key Skills: Deep expertise across stack, thought leadership, strategic thinking
- Common Tasks: Define architectural standards, research new technologies, technical mentoring

**Level 5: Engineering Manager / Director**
- Salary Range: $200K - $350K+ USD
- Focus: Team building, org planning, business alignment
- Responsibilities: Build teams, roadmap planning, stakeholder management
- Key Skills: Leadership, communication, strategic planning, technical judgment
- Common Tasks: Hiring, performance reviews, resource allocation, cross-functional collaboration

---

**Geographic Salary Variations (Senior Data Engineer):**

**North America:**
- San Francisco Bay Area: $180K - $250K + equity
- New York City: $160K - $220K + equity
- Seattle: $150K - $200K + equity
- Austin: $130K - $180K + equity
- Toronto: $100K - $140K CAD + equity

**Europe:**
- London: £80K - £120K + equity
- Amsterdam: €70K - €100K + equity
- Berlin: €65K - €90K + equity
- Paris: €60K - €85K + equity
- Zurich: CHF 120K - 160K + equity

**Asia-Pacific:**
- Singapore: SGD 100K - 150K + equity
- Sydney: AUD 120K - 160K + equity
- Tokyo: ¥8M - ¥12M + equity
- Bangalore: ₹20L - ₹40L + equity

---

**Industry Sectors & Opportunities:**

**1. Technology/FAANG (Highest Comp)**
- Companies: Google, Meta, Amazon, Apple, Microsoft, Netflix
- Salary Premium: +30-50% above market
- Scale: Billions of events/day
- Technologies: Cutting-edge, proprietary systems
- Culture: Innovation-focused, fast-paced

**2. Finance & Fintech (High Comp + Stability)**
- Companies: Goldman Sachs, JPMorgan, Stripe, PayPal, Square
- Salary Premium: +20-40% above market
- Scale: High-frequency trading, fraud detection, risk analytics
- Technologies: Real-time processing, regulatory compliance
- Culture: High-stakes, quality-focused

**3. E-commerce & Marketplaces**
- Companies: Amazon, eBay, Shopify, Instacart, DoorDash
- Salary: Market average to +20%
- Scale: Product catalogs, inventory, recommendations
- Technologies: Event-driven, recommendation engines
- Culture: Customer-focused, data-driven

**4. Healthcare & Life Sciences**
- Companies: United Health, Pfizer, 23andMe, Oscar Health
- Salary: Market average
- Scale: Patient data, clinical trials, genomics
- Technologies: HIPAA compliance, data security
- Culture: Impact-focused, regulatory-aware

**5. Gaming & Entertainment**
- Companies: Riot Games, Epic, Unity, Spotify, Disney
- Salary: Slightly below market but fun work
- Scale: Real-time player data, content recommendations
- Technologies: Real-time analytics, A/B testing platforms
- Culture: Creative, user-experience focused

---

**Remote Work Landscape:**

**Fully Remote Friendly Companies:**
- GitLab, Automattic, Zapier, InVision, Buffer
- Typically offer: Location-based compensation or unified global pay
- Advantage: Work from anywhere, flexible hours
- Challenge: Async communication, self-motivation required

**Hybrid Models:**
- Most FAANG companies: 3 days in office
- Consulting firms: Client site + home
- Startups: Flexible, team-dependent

**Compensation Adjustment:**
- Moving from SF to remote: Often 10-25% salary reduction
- Remote-first companies: Usually uniform pay regardless of location
- Hybrid: Full on-site compensation

---

**Critical Soft Skills for Advancement:**

**1. Communication**
- Explain technical concepts to non-technical stakeholders
- Write clear documentation
- Present architectural decisions
- Lead design reviews

**2. Business Acumen**
- Understand how data drives business value
- Translate business requirements to technical solutions
- Calculate ROI of data initiatives
- Partner with product managers

**3. Project Management**
- Break down large projects into milestones
- Estimate effort accurately
- Manage dependencies
- Deliver on commitments

**4. Collaboration**
- Work with data scientists, analysts, software engineers
- Navigate organizational complexity
- Build consensus on technical decisions
- Mentor junior engineers

**5. Problem-Solving**
- Debug production issues under pressure
- Design scalable systems from requirements
- Make pragmatic trade-offs
- Learn new technologies quickly

---

**Certifications Worth Getting:**

**Cloud Platforms:**
1. AWS Certified Data Analytics - Specialty ($300, widely recognized)
2. Google Professional Data Engineer ($200, GCP-focused)
3. Azure Data Engineer Associate ($165, Azure ecosystem)

**Big Data:**
1. Databricks Certified Data Engineer ($200, Spark expertise)
2. Confluent Certified Developer for Apache Kafka ($150, streaming)
3. Cloudera CCA Data Analyst ($295, Hadoop ecosystem - less relevant now)

**ROI Analysis:**
- Direct salary impact: Typically $5K-$15K
- Credibility boost: Opens doors to interviews
- Knowledge gain: Structured learning path
- Worth it?: Yes for cloud certs, maybe for vendor-specific

**Note:** Experience > Certifications. Build real projects over collecting certificates.

---

**Building Your Portfolio:**

**Project Ideas to Showcase:**

1. **Real-Time Stock Market Dashboard**
   - Stream: Yahoo Finance API → Kafka → Spark Streaming
   - Storage: TimescaleDB for time-series
   - Viz: Grafana dashboard
   - Demonstrates: Streaming, real-time processing, visualization

2. **Multi-Source E-Commerce Data Warehouse**
   - Sources: Postgres (transactional), MongoDB (product catalog), S3 (logs)
   - Pipeline: Airflow orchestration
   - Warehouse: Snowflake or BigQuery
   - Demonstrates: ETL, dimensional modeling, orchestration

3. **Distributed Log Processing System**
   - Input: Application logs (GB/day)
   - Processing: Parse, deduplicate, aggregate
   - Storage: Elasticsearch for search
   - Demonstrates: Batch processing, text processing, search

4. **CDC Pipeline for Database Replication**
   - Source: MySQL or Postgres
   - CDC: Debezium or custom log parsing
   - Target: S3 Data Lake + Redshift
   - Demonstrates: Change data capture, data replication

5. **ML Feature Store**
   - Compute: Spark for feature engineering
   - Storage: Redis (online) + S3 (offline)
   - Serving: REST API for ML models
   - Demonstrates: Real-time + batch, ML infrastructure

**Portfolio Best Practices:**
- Host code on GitHub with clear README
- Include architecture diagrams (draw.io, Lucidchart)
- Write blog posts explaining design decisions
- Demo with screenshots/videos
- Highlight: Scale handled, technologies used, trade-offs made

---

**Networking & Community:**

**Conferences:**
- Data Council (SF, NYC, Austin)
- Strata Data Conference
- AWS re:Invent
- Google Cloud Next
- Kafka Summit

**Online Communities:**
- Reddit: r/dataengineering (150K+ members)
- Slack: Data Engineering community
- Discord: Various data eng servers
- LinkedIn: Follow thought leaders

**Contributing to Open Source:**
- Apache Spark, Kafka, Airflow
- Even small contributions (docs, bug fixes) stand out
- Shows: Initiative, collaboration skills, technical depth

**Content Creation:**
- Write blog posts on Medium, personal blog
- Create YouTube tutorials
- Speak at local meetups
- Answer questions on StackOverflow

**Impact:**
- Builds personal brand
- Demonstrates expertise
- Expands professional network
- Creates job opportunities
"""
        )
    elif unit_number == 6:
        st.markdown("#### 📘 Data Quality, Orchestration & Monitoring")
        st.markdown(
            """**Production data pipelines** require quality checks, orchestration, and monitoring.

**Data Quality Framework:**

**The 6 Dimensions of Data Quality:**

1. **Completeness:** No missing critical values
2. **Accuracy:** Data is correct
3. **Consistency:** Same data across systems
4. **Timeliness:** Data is fresh
5. **Validity:** Follows business rules
6. **Uniqueness:** No duplicates

**Quality Checks Example:**
```python
def validate_sales_data(df):
    # Completeness
    assert df['order_id'].notnull().all(), "Missing order_ids"
    
    # Uniqueness
    assert df['order_id'].is_unique, "Duplicate order_ids"
    
    # Validity
    assert (df['amount'] >= 0).all(), "Negative amounts"
    
    # Timeliness
    latest = df['order_date'].max()
    assert (datetime.now() - latest).days < 2, "Data too old"
    
    return True
```

**Great Expectations:**
- Industry-standard quality framework
- Define expectations as code
- Automatic documentation
- Integration with Airflow
"""
        )

        st.markdown("#### 🎼 Apache Airflow: Workflow Orchestration")
        st.markdown(
            """**Airflow** orchestrates complex data workflows.

**Why Airflow?**
- ✅ Define workflows as Python code
- ✅ Rich UI for monitoring
- ✅ Automatic retries
- ✅ Dependency management
- ✅ Scheduling (cron-like)
- ✅ Huge ecosystem of operators

**DAG (Directed Acyclic Graph):**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'daily_etl',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2024, 1, 1)
)

extract = PythonOperator(task_id='extract', python_callable=extract_data, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=transform_data, dag=dag)
load = PythonOperator(task_id='load', python_callable=load_data, dag=dag)

# Define dependencies
extract >> transform >> load
```

**Best Practices:**
- ✅ Idempotent tasks (can run multiple times)
- ✅ Atomic operations (all or nothing)
- ✅ Proper error handling
- ✅ Meaningful task names
- ✅ SLA monitoring
"""
        )

        st.markdown("#### 📊 Monitoring & Alerting")
        st.markdown(
            """**Monitor everything** to catch issues early.

**Key Metrics:**

1. **Pipeline Health**
   - Success/failure rate
   - Execution time
   - Data volume processed

2. **Data Quality**
   - Null rate
   - Duplicate rate
   - Schema changes

3. **Performance**
   - Query latency
   - Throughput (records/sec)
   - Resource utilization

4. **Cost**
   - Cloud spend by service
   - Cost per GB processed
   - Budget alerts

**Alerting Strategy:**
- ✅ Alert on failures (immediate)
- ✅ Alert on SLA violations
- ✅ Alert on anomalies (data volume spikes)
- ✅ Weekly summary reports

**Tools:**
- Prometheus + Grafana
- CloudWatch (AWS)
- Stackdriver (GCP)
- PagerDuty for on-call
"""
        )
        
        st.markdown("#### ✅ Great Expectations: Data Quality Framework")
        st.markdown("""
**Industry-standard data quality testing:**

**Setup:**

```python
import great_expectations as ge
from great_expectations.dataset import PandasDataset

# Create expectation suite
df = pd.read_csv('sales.csv')
ge_df = ge.from_pandas(df)

# Define expectations
ge_df.expect_column_values_to_not_be_null('order_id')
ge_df.expect_column_values_to_be_unique('order_id')
ge_df.expect_column_values_to_be_between('amount', min_value=0, max_value=100000)
ge_df.expect_column_values_to_be_in_set('status', ['pending', 'completed', 'cancelled'])
ge_df.expect_column_values_to_match_regex('email', r'^[\w\.-]+@[\w\.-]+\.\w+$')

# Validate
results = ge_df.validate()

if results['success']:
    print("✅ All quality checks passed")
else:
    failed = [r for r in results['results'] if not r['success']]
    print(f"❌ {len(failed)} checks failed")
    for failure in failed:
        print(f"  - {failure['expectation_config']['expectation_type']}")
```

**Integration with Airflow:**

```python
from airflow.operators.python import PythonOperator
import great_expectations as ge

def validate_data_quality(**context):
    df = pd.read_parquet('/data/processed/sales.parquet')
    ge_df = ge.from_pandas(df)
    
    # Run expectations
    ge_df.expect_column_values_to_not_be_null('order_id')
    ge_df.expect_column_values_to_be_unique('order_id')
    
    results = ge_df.validate()
    
    if not results['success']:
        raise ValueError("Data quality checks failed")
    
    return True

quality_task = PythonOperator(
    task_id='validate_quality',
    python_callable=validate_data_quality,
    dag=dag
)
```
""")
        
        st.markdown("#### 🎼 Advanced Airflow Patterns")
        st.markdown("""
**Production Airflow patterns:**

**1. Dynamic DAG Generation**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Generate DAGs for multiple data sources
data_sources = ['sales', 'customers', 'products', 'orders']

for source in data_sources:
    dag_id = f'etl_{source}'
    
    dag = DAG(
        dag_id,
        schedule_interval='@daily',
        start_date=datetime(2024, 1, 1)
    )
    
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        op_kwargs={'source': source},
        dag=dag
    )
    
    globals()[dag_id] = dag  # Register DAG
```

**2. Task Groups**

```python
from airflow.utils.task_group import TaskGroup

with TaskGroup('data_quality_checks', dag=dag) as quality_group:
    check_schema = PythonOperator(task_id='check_schema', ...)
    check_nulls = PythonOperator(task_id='check_nulls', ...)
    check_duplicates = PythonOperator(task_id='check_duplicates', ...)
    
    [check_schema, check_nulls, check_duplicates]

# Use in workflow
extract >> transform >> quality_group >> load
```

**3. XComs for Data Passing**

```python
def extract_data(**context):
    df = pd.read_csv('data.csv')
    record_count = len(df)
    
    # Push to XCom
    context['task_instance'].xcom_push(key='record_count', value=record_count)
    return record_count

def validate_count(**context):
    # Pull from XCom
    record_count = context['task_instance'].xcom_pull(
        task_ids='extract',
        key='record_count'
    )
    
    if record_count < 100:
        raise ValueError(f"Too few records: {record_count}")
```

**4. SLA Monitoring**

```python
from datetime import timedelta

default_args = {
    'sla': timedelta(hours=2),  # Task must complete in 2 hours
    'on_failure_callback': send_alert,
    'on_sla_miss_callback': send_sla_alert
}

def send_sla_alert(dag, task_list, blocking_task_list, slas, blocking_tis):
    message = f"SLA missed for tasks: {[t.task_id for t in task_list]}"
    send_slack_alert(message)
```
""")
        
        st.markdown("#### 🔍 Advanced Orchestration Patterns")
        st.markdown(
            """**Complex workflow patterns in production:**

**1. Dynamic DAGs**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Generate tasks dynamically
def create_processing_dag():
    dag = DAG('dynamic_processing', start_date=datetime(2024, 1, 1))
    
    # Read configuration
    sources = ['api1', 'api2', 'api3', 'database1', 'database2']
    
    tasks = []
    for source in sources:
        task = PythonOperator(
            task_id=f'extract_{source}',
            python_callable=extract_data,
            op_kwargs={'source': source},
            dag=dag
        )
        tasks.append(task)
    
    # Set dependencies
    for i in range(len(tasks)-1):
        tasks[i] >> tasks[i+1]
    
    return dag

dag = create_processing_dag()
```

**2. Sensor Pattern**

```python
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.external_task import ExternalTaskSensor

# Wait for file to arrive
file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/incoming/*.csv',
    poke_interval=60,  # Check every 60 seconds
    timeout=3600  # Wait max 1 hour
)

# Wait for another DAG
external_sensor = ExternalTaskSensor(
    task_id='wait_for_upstream',
    external_dag_id='upstream_pipeline',
    external_task_id='final_task',
    timeout=600
)

file_sensor >> process_data >> external_sensor
```

**3. Parallel Processing Pattern**

```python
from airflow.operators.python import PythonOperator
from airflow.models import Variable

def process_partition(partition_id):
    # Process one partition
    df = read_partition(partition_id)
    df_clean = clean_data(df)
    save_partition(df_clean, partition_id)

# Create 10 parallel tasks
num_partitions = 10
parallel_tasks = []

for i in range(num_partitions):
    task = PythonOperator(
        task_id=f'process_partition_{i}',
        python_callable=process_partition,
        op_kwargs={'partition_id': i}
    )
    parallel_tasks.append(task)

# All run in parallel
extract >> parallel_tasks >> combine_results
```
"""
        )
        
        st.markdown("#### 📊 Production Monitoring Dashboard")
        st.markdown(
            """**Monitor pipeline health in real-time:**

**Key Metrics to Track:**

**1. Pipeline Success Rate**
```python
import prometheus_client as prom

# Define metrics
pipeline_success = prom.Counter(
    'pipeline_success_total',
    'Total successful pipeline runs',
    ['pipeline_name']
)

pipeline_failures = prom.Counter(
    'pipeline_failures_total',
    'Total failed pipeline runs',
    ['pipeline_name', 'error_type']
)

# Track execution
def run_pipeline(pipeline_name):
    try:
        execute_pipeline()
        pipeline_success.labels(pipeline_name=pipeline_name).inc()
    except Exception as e:
        pipeline_failures.labels(
            pipeline_name=pipeline_name,
            error_type=type(e).__name__
        ).inc()
        raise
```

**2. Data Volume Metrics**
```python
data_volume = prom.Gauge(
    'data_volume_bytes',
    'Volume of data processed',
    ['pipeline', 'stage']
)

processing_time = prom.Histogram(
    'processing_duration_seconds',
    'Time to process data',
    ['pipeline']
)

# Track metrics
with processing_time.labels(pipeline='sales').time():
    df = process_data()
    volume = df.memory_usage(deep=True).sum()
    data_volume.labels(pipeline='sales', stage='processed').set(volume)
```

**3. Data Quality Metrics**
```python
quality_score = prom.Gauge(
    'data_quality_score',
    'Data quality score (0-100)',
    ['table', 'dimension']
)

# Calculate and track
def check_quality(table_name):
    completeness = check_completeness(table_name)
    accuracy = check_accuracy(table_name)
    timeliness = check_timeliness(table_name)
    
    quality_score.labels(table=table_name, dimension='completeness').set(completeness)
    quality_score.labels(table=table_name, dimension='accuracy').set(accuracy)
    quality_score.labels(table=table_name, dimension='timeliness').set(timeliness)
```

**4. Alert Configuration**
```python
# Prometheus alerting rules
alerts = '''
groups:
- name: data_pipeline_alerts
  interval: 1m
  rules:
  - alert: HighFailureRate
    expr: rate(pipeline_failures_total[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Pipeline failure rate exceeded 10%"
  
  - alert: DataFreshness
    expr: time() - data_freshness_timestamp > 7200
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Data is more than 2 hours old"
  
  - alert: LowDataQuality
    expr: data_quality_score < 80
    for: 15m
    labels:
      severity: warning
    annotations:
      summary: "Data quality below threshold"
'''
```
"""
        )
    elif unit_number == 7:
        st.markdown("#### 📘 Data Engineering Capstone: Building Production Systems")
        st.markdown(
            """Your capstone demonstrates **end-to-end data engineering expertise** by building 
a production-ready data pipeline system.

**What Makes a Great Capstone:**

1. **Solves Real Problem**
   - Addresses actual business need
   - Uses realistic data volumes
   - Meets production requirements

2. **Production Quality**
   - Error handling and retries
   - Logging and monitoring
   - Data quality checks
   - Documentation

3. **Technical Depth**
   - Multiple technologies integrated
   - Scalable architecture
   - Performance optimized
   - Cost-effective

4. **Business Value**
   - Clear ROI or impact
   - Measurable improvements
   - Stakeholder alignment

**Project Scope:**
- 4-6 weeks of work
- 2,000-5,000 lines of code
- Multiple components (ETL, warehouse, orchestration)
- Complete documentation
"""
        )

        st.markdown("#### 🧱 Capstone Structure & Milestones")
        st.markdown(
            """**Phase 1: Planning & Design (Week 1)**

**Deliverables:**
- Problem statement document
- Data source inventory
- Architecture diagram
- Technology selection justification
- SLA definitions (latency, freshness, quality)
- Cost estimate

**Example:**
```
Problem: E-commerce company needs real-time sales analytics
Sources: PostgreSQL (orders), MongoDB (products), Kafka (events)
Target: Redshift warehouse + real-time dashboard
SLA: Data fresh within 5 minutes, 99.9% uptime
Cost: <$500/month
```

---

**Phase 2: Implementation (Weeks 2-4)**

**Deliverables:**
- ETL pipeline code (Python/Spark)
- Data warehouse schema (SQL DDL)
- Orchestration DAGs (Airflow)
- Data quality tests
- Infrastructure as code (Terraform)
- CI/CD pipeline

**Code Structure:**
```
project/
├── pipelines/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── dags/
│   └── daily_etl.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── terraform/
│   └── main.tf
├── tests/
│   └── test_pipeline.py
└── README.md
```

---

**Phase 3: Testing & Optimization (Week 5)**

**Deliverables:**
- Unit test suite (80%+ coverage)
- Integration tests
- Performance benchmarks
- Load testing results
- Optimization report

**Metrics to Track:**
- Pipeline execution time
- Data volume processed
- Error rate
- Cost per GB
- Query performance

---

**Phase 4: Documentation & Presentation (Week 6)**

**Deliverables:**
- Architecture documentation
- API documentation
- Operational runbook
- Troubleshooting guide
- Final presentation (15 min)

**Runbook Should Include:**
- How to deploy
- How to monitor
- Common errors and fixes
- Rollback procedures
- On-call escalation

---

**Evaluation Criteria:**

1. **Architecture (25%)**
   - Well-designed data model
   - Scalable system
   - Technology choices justified

2. **Implementation (30%)**
   - Clean, maintainable code
   - Error handling
   - Performance optimized
   - Security best practices

3. **Data Quality (20%)**
   - Validation framework
   - Quality monitoring
   - Testing coverage

4. **Operations (15%)**
   - Orchestration
   - Monitoring & alerting
   - Documentation

5. **Business Impact (10%)**
   - Solves real problem
   - Measurable value
   - Cost-effective
"""
        )
        
        st.markdown("#### 💡 Capstone Project Examples")
        st.markdown(
            """**1. Real-Time E-Commerce Analytics Platform**

**Problem:** Retail company needs real-time insights into sales, inventory, and customer behavior.

**Architecture:**
```
Data Sources → Kafka → Spark Streaming → Delta Lake → Power BI
     ↓
PostgreSQL (Orders)
MongoDB (Products)  
Redis (Sessions)
API (Payments)
```

**Implementation Highlights:**
```python
# Stream processing with Spark
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, count, sum, avg

spark = SparkSession.builder.appName("RealtimeAnalytics").getOrCreate()

# Read from Kafka
events_df = spark.readStream.format("kafka") \\
    .option("kafka.bootstrap.servers", "localhost:9092") \\
    .option("subscribe", "user_events") \\
    .load()

# Parse JSON and aggregate
parsed = events_df.selectExpr("CAST(value AS STRING) as json") \\
    .select(from_json(col("json"), schema).alias("data")) \\
    .select("data.*")

# Real-time metrics
metrics = parsed.groupBy(
    window(col("timestamp"), "5 minutes"),
    col("product_id")
).agg(
    count("*").alias("event_count"),
    sum("revenue").alias("total_revenue"),
    avg("revenue").alias("avg_revenue")
)

# Write to Delta Lake
metrics.writeStream \\
    .format("delta") \\
    .outputMode("append") \\
    .option("checkpointLocation", "/checkpoints/metrics") \\
    .start("/delta/real_time_metrics")
```

**Key Features:**
- Sub-5-minute data freshness
- Handles 10,000+ events/second
- Automated quality checks
- Real-time dashboards

---

**2. Multi-Source Data Warehouse for Healthcare**

**Problem:** Hospital system needs unified analytics across patient records, billing, and operations.

**Architecture:**
```
Sources → Airflow ETL → Data Vault 2.0 → Presentation Layer → Tableau
    ↓                       ↓                    ↓
HL7 Feed            Hubs/Links/Sats      Star Schemas
EMR DB              (Snowflake)           (Marts)
Billing API
```

**Data Vault Implementation:**
```sql
-- Hub: Patient
CREATE TABLE hub_patient (
    patient_hash_key BINARY(16) PRIMARY KEY,
    patient_id VARCHAR(50) NOT NULL,
    load_datetime TIMESTAMP,
    record_source VARCHAR(50)
);

-- Satellite: Patient Details
CREATE TABLE sat_patient_details (
    patient_hash_key BINARY(16),
    load_datetime TIMESTAMP,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    hash_diff BINARY(16),
    PRIMARY KEY (patient_hash_key, load_datetime)
);

-- Link: Patient-Encounter
CREATE TABLE link_patient_encounter (
    link_hash_key BINARY(16) PRIMARY KEY,
    patient_hash_key BINARY(16),
    encounter_hash_key BINARY(16),
    load_datetime TIMESTAMP,
    record_source VARCHAR(50)
);
```

**ETL Pipeline:**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract_hl7_messages():
    # Connect to HL7 feed
    messages = fetch_hl7_messages()
    return parse_hl7(messages)

def load_to_data_vault(data):
    # Calculate hash keys
    for record in data:
        record['hash_key'] = calculate_hash(record['business_key'])
        record['hash_diff'] = calculate_hash(record['attributes'])
    
    # Load hubs (if new)
    load_hubs(data)
    
    # Load satellites (always, with versioning)
    load_satellites(data)
    
    # Load links
    load_links(data)

dag = DAG('healthcare_etl', schedule_interval='@hourly')

extract = PythonOperator(task_id='extract', python_callable=extract_hl7_messages)
load = PythonOperator(task_id='load', python_callable=load_to_data_vault)

extract >> load
```

**Compliance Features:**
- HIPAA-compliant encryption
- Audit trail for all data access
- Data lineage tracking
- PII masking in non-production

---

**3. Cloud Data Lake for IoT Telemetry**

**Problem:** Manufacturing company needs to analyze sensor data from 10,000+ devices.

**Architecture:**
```
IoT Devices → AWS IoT Core → Kinesis → Lambda → S3 (Parquet) → Athena/Glue
                                ↓
                           DynamoDB (Hot data)
```

**Implementation:**
```python
# Lambda function for processing
import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    for record in event['Records']:
        # Parse Kinesis record
        payload = json.loads(record['kinesis']['data'])
        
        device_id = payload['device_id']
        timestamp = payload['timestamp']
        metrics = payload['metrics']
        
        # Store hot data in DynamoDB
        table = dynamodb.Table('iot_hot_data')
        table.put_item(Item={
            'device_id': device_id,
            'timestamp': timestamp,
            'temperature': metrics['temperature'],
            'pressure': metrics['pressure'],
            'status': metrics['status']
        })
        
        # Batch cold data to S3
        s3_key = f"telemetry/year={timestamp[:4]}/month={timestamp[5:7]}/day={timestamp[8:10]}/{device_id}.parquet"
        
        # Convert to Parquet and upload
        df = pandas.DataFrame([payload])
        parquet_buffer = df.to_parquet()
        s3.put_object(Bucket='iot-data-lake', Key=s3_key, Body=parquet_buffer)
    
    return {'statusCode': 200}
```

**Query with Athena:**
```sql
-- Create external table
CREATE EXTERNAL TABLE iot_telemetry (
    device_id STRING,
    timestamp TIMESTAMP,
    temperature DOUBLE,
    pressure DOUBLE,
    status STRING
)
PARTITIONED BY (year INT, month INT, day INT)
STORED AS PARQUET
LOCATION 's3://iot-data-lake/telemetry/';

-- Analyze device performance
SELECT 
    device_id,
    DATE_TRUNC('hour', timestamp) as hour,
    AVG(temperature) as avg_temp,
    MAX(pressure) as max_pressure,
    COUNT(*) as reading_count
FROM iot_telemetry
WHERE year = 2024 AND month = 12
GROUP BY device_id, DATE_TRUNC('hour', timestamp)
HAVING avg_temp > 80  -- Alert threshold
ORDER BY hour DESC;
```

**Cost Optimization:**
- S3 lifecycle policies (Standard → IA → Glacier)
- Partition pruning
- Compression (Parquet with Snappy)
- Reserved capacity for predictable workloads

**Monitoring:**
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Track metrics
cloudwatch.put_metric_data(
    Namespace='IoTPipeline',
    MetricData=[
        {
            'MetricName': 'RecordsProcessed',
            'Value': record_count,
            'Unit': 'Count'
        },
        {
            'MetricName': 'ProcessingLatency',
            'Value': latency_ms,
            'Unit': 'Milliseconds'
        }
    ]
)
```
"""
        )
        
        st.markdown("#### 🎯 Capstone Success Checklist")
        st.markdown(
            """**Technical Requirements:**

✅ **Data Ingestion**
- [ ] Connects to 2+ data sources
- [ ] Handles incremental loads
- [ ] Error handling and retries
- [ ] Data validation on ingestion

✅ **Data Processing**
- [ ] Transformation logic is modular
- [ ] Handles data quality issues
- [ ] Performance optimized (< 1 hour for full load)
- [ ] Idempotent operations

✅ **Data Storage**
- [ ] Appropriate data model (star, vault, etc.)
- [ ] Partitioning strategy
- [ ] Indexing for query performance
- [ ] Data retention policies

✅ **Orchestration**
- [ ] Automated with Airflow/Prefect
- [ ] Dependency management
- [ ] SLA monitoring
- [ ] Failure alerting

✅ **Data Quality**
- [ ] Automated quality checks
- [ ] Data profiling
- [ ] Anomaly detection
- [ ] Quality metrics tracked

✅ **Monitoring**
- [ ] Pipeline metrics dashboard
- [ ] Alert configuration
- [ ] Log aggregation
- [ ] Performance tracking

✅ **Documentation**
- [ ] Architecture diagram
- [ ] Data dictionary
- [ ] API documentation
- [ ] Operational runbook
- [ ] README with setup instructions

✅ **Testing**
- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests
- [ ] Data quality tests
- [ ] Load/performance tests

✅ **Deployment**
- [ ] Infrastructure as Code
- [ ] CI/CD pipeline
- [ ] Environment configuration
- [ ] Rollback procedures

✅ **Security & Compliance**
- [ ] Secrets management
- [ ] Access controls
- [ ] Audit logging
- [ ] Data encryption
"""
        )
        
        st.markdown("#### 📈 Presentation Guidelines")
        st.markdown(
            """**15-Minute Capstone Presentation Structure:**

**Slide 1: Problem Statement (2 min)**
- Business context and pain points
- Current state vs. desired state
- Success criteria and KPIs

**Slide 2-3: Architecture (3 min)**
- System architecture diagram
- Technology stack justification
- Data flow and processing steps
- Scalability considerations

**Slide 4-5: Implementation Highlights (4 min)**
- Code walkthrough (key components)
- Interesting technical challenges solved
- Performance optimizations
- Data quality framework

**Slide 6: Demo (4 min)**
- Live pipeline execution
- Monitoring dashboard
- Sample queries/analytics
- Data quality reports

**Slide 7: Results & Metrics (1 min)**
- Performance benchmarks
- Cost analysis
- Data quality improvements
- Business impact

**Slide 8: Lessons Learned (1 min)**
- What worked well
- What would you do differently
- Future enhancements

**Demo Preparation:**
```bash
# Pre-load sample data
python scripts/load_test_data.py

# Start monitoring dashboard
docker-compose up -d grafana

# Trigger pipeline
airflow dags trigger my_pipeline

# Prepare sample queries
psql -f demo_queries.sql
```

**Common Questions to Prepare For:**
1. How does your solution handle data quality issues?
2. What happens if a source system is down?
3. How would you scale this to 10x the data volume?
4. What's your disaster recovery strategy?
5. How do you ensure data freshness SLAs?
6. What security measures are in place?
7. How would you optimize costs further?
8. How do you handle schema changes?
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
            
            st.markdown("### LAB 3: Incremental Data Loading (90 min)")
            st.markdown("**Objective:** Load only new/changed records efficiently")
            lab1_3 = '''import pandas as pd
import sqlite3
from datetime import datetime

class IncrementalLoader:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
    
    def get_last_loaded_timestamp(self, table_name):
        """Get timestamp of last loaded record"""
        query = f"SELECT MAX(updated_at) FROM {table_name}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result if result else '1900-01-01'
    
    def load_incremental(self, source_file, table_name, timestamp_column='updated_at'):
        """Load only new records since last load"""
        print(f"Loading incremental data to {table_name}...")
        
        # Get last timestamp
        last_timestamp = self.get_last_loaded_timestamp(table_name)
        print(f"Last loaded: {last_timestamp}")
        
        # Load source data
        df = pd.read_csv(source_file)
        df[timestamp_column] = pd.to_datetime(df[timestamp_column])
        
        # Filter to new records only
        df_new = df[df[timestamp_column] > last_timestamp]
        
        print(f"Total records in source: {len(df):,}")
        print(f"New records to load: {len(df_new):,}")
        
        if len(df_new) == 0:
            print("✅ No new records to load")
            return 0
        
        # Load new records
        df_new.to_sql(table_name, self.conn, if_exists='append', index=False)
        
        print(f"✅ Loaded {len(df_new):,} new records")
        return len(df_new)

# Example
loader = IncrementalLoader('warehouse.db')
records_loaded = loader.load_incremental('customers.csv', 'customers', 'updated_at')
print(f"\nIncremental load complete: {records_loaded} records")'''
            st.code(lab1_3, language='python')
            
            st.markdown("### LAB 4: Dockerize ETL Pipeline (60 min)")
            st.markdown("**Objective:** Containerize your data pipeline")
            lab1_4 = '''# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy pipeline code
COPY etl_pipeline.py .
COPY config.yaml .

# Run pipeline
CMD ["python", "etl_pipeline.py"]

# requirements.txt
# pandas==2.1.0
# sqlalchemy==2.0.0
# psycopg2-binary==2.9.0
# requests==2.31.0

# docker-compose.yml
version: '3.8'

services:
  etl_pipeline:
    build: .
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=warehouse
    depends_on:
      - postgres
    volumes:
      - ./data:/data
  
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=warehouse
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

# Build and run:
# docker-compose build
# docker-compose up
# docker-compose down'''
            st.code(lab1_4, language='dockerfile')
            
            st.success("✅ Unit 1 Labs Complete: Production ETL pipelines mastered!")
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
            
            st.markdown("### LAB 4: Data Quality Framework for Warehouses (75 min)")
            st.markdown("**Objective:** Implement comprehensive data quality checks")
            lab2_4 = '''import pandas as pd
import sqlite3
from datetime import datetime

class DataQualityChecker:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.results = []
    
    def check_completeness(self, table_name, required_columns):
        """Check for missing values in critical columns"""
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, self.conn)
        
        for col in required_columns:
            null_count = df[col].isnull().sum()
            null_pct = (null_count / len(df)) * 100
            
            status = "PASS" if null_pct == 0 else "FAIL"
            self.results.append({
                'check': 'Completeness',
                'table': table_name,
                'column': col,
                'status': status,
                'details': f"{null_count} nulls ({null_pct:.1f}%)"
            })
    
    def check_uniqueness(self, table_name, unique_columns):
        """Check for duplicate values"""
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, self.conn)
        
        for col in unique_columns:
            dup_count = df[col].duplicated().sum()
            status = "PASS" if dup_count == 0 else "FAIL"
            
            self.results.append({
                'check': 'Uniqueness',
                'table': table_name,
                'column': col,
                'status': status,
                'details': f"{dup_count} duplicates"
            })
    
    def check_referential_integrity(self, fact_table, dim_table, fk_column, pk_column):
        """Check foreign key relationships"""
        query = f"""
        SELECT COUNT(*) as orphans
        FROM {fact_table} f
        LEFT JOIN {dim_table} d ON f.{fk_column} = d.{pk_column}
        WHERE d.{pk_column} IS NULL
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        orphans = cursor.fetchone()[0]
        
        status = "PASS" if orphans == 0 else "FAIL"
        self.results.append({
            'check': 'Referential Integrity',
            'table': fact_table,
            'column': fk_column,
            'status': status,
            'details': f"{orphans} orphaned records"
        })
    
    def check_data_freshness(self, table_name, date_column, max_age_hours=24):
        """Check if data is recent"""
        query = f"SELECT MAX({date_column}) as latest FROM {table_name}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        latest = cursor.fetchone()[0]
        
        if latest:
            latest_dt = pd.to_datetime(latest)
            age_hours = (datetime.now() - latest_dt).total_seconds() / 3600
            status = "PASS" if age_hours <= max_age_hours else "FAIL"
            
            self.results.append({
                'check': 'Freshness',
                'table': table_name,
                'column': date_column,
                'status': status,
                'details': f"{age_hours:.1f} hours old"
            })
    
    def generate_report(self):
        """Generate quality report"""
        df_results = pd.DataFrame(self.results)
        
        print("\n" + "="*60)
        print("DATA QUALITY REPORT")
        print("="*60)
        
        print(f"\nTotal Checks: {len(df_results)}")
        print(f"Passed: {len(df_results[df_results['status']=='PASS'])}")
        print(f"Failed: {len(df_results[df_results['status']=='FAIL'])}")
        
        print("\nFailed Checks:")
        failed = df_results[df_results['status']=='FAIL']
        if len(failed) > 0:
            print(failed.to_string(index=False))
        else:
            print("✅ All checks passed!")
        
        return df_results

# Example
checker = DataQualityChecker('retail_warehouse.db')

# Run checks
checker.check_completeness('fact_sales', ['order_id', 'customer_key', 'product_key'])
checker.check_uniqueness('fact_sales', ['order_id'])
checker.check_referential_integrity('fact_sales', 'dim_customer', 'customer_key', 'customer_key')
checker.check_data_freshness('fact_sales', 'created_at', max_age_hours=24)

# Generate report
report = checker.generate_report()
print("\n✅ Quality checks complete!")'''
            st.code(lab2_4, language='python')
            
            st.success("✅ Unit 2 Labs Complete: Data warehousing mastered!")
        elif selected_unit == 3:
            st.markdown("### 🔥 Unit 3: Batch Processing with Apache Spark")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Production Spark Pipelines!**")
            
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
            
            st.markdown("### LAB 3: Delta Lake for Data Reliability (90 min)")
            st.markdown("**Objective:** Implement ACID transactions and time travel with Delta Lake")
            lab3_3 = '''from pyspark.sql import SparkSession
from delta import *
from pyspark.sql.functions import col, current_timestamp

# Initialize Spark with Delta Lake
builder = SparkSession.builder.appName("DeltaLake") \\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("▶️ DELTA LAKE - ACID TRANSACTIONS & TIME TRAVEL\n" + "="*60)

# 1. Create Delta Table
print("\n1. Creating Delta Table...")

df = spark.read.csv('sales_data.csv', header=True, inferSchema=True)
df = df.withColumn("load_timestamp", current_timestamp())

# Write as Delta table
df.write.format("delta").mode("overwrite").save("/data/delta/sales")
print("✅ Delta table created")

# 2. Read Delta Table
delta_df = spark.read.format("delta").load("/data/delta/sales")
print(f"\nRecords in Delta table: {delta_df.count():,}")

# 3. ACID Updates (Upsert/Merge)
print("\n2. Performing ACID Merge...")

from delta.tables import DeltaTable

# Load new data
new_data = spark.read.csv('new_sales.csv', header=True, inferSchema=True)
new_data = new_data.withColumn("load_timestamp", current_timestamp())

# Get Delta table
delta_table = DeltaTable.forPath(spark, "/data/delta/sales")

# Merge (upsert)
delta_table.alias("target").merge(
    new_data.alias("source"),
    "target.order_id = source.order_id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("✅ Merge complete - updates and inserts applied")

# 4. Time Travel
print("\n3. Time Travel Queries...")

# Query previous version
df_v0 = spark.read.format("delta").option("versionAsOf", 0).load("/data/delta/sales")
df_v1 = spark.read.format("delta").option("versionAsOf", 1).load("/data/delta/sales")

print(f"Version 0: {df_v0.count():,} records")
print(f"Version 1: {df_v1.count():,} records")

# Query by timestamp
from datetime import datetime, timedelta
timestamp = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
df_historical = spark.read.format("delta").option("timestampAsOf", timestamp).load("/data/delta/sales")

print(f"Data as of {timestamp}: {df_historical.count():,} records")

# 5. View History
print("\n4. Delta Table History...")

delta_table.history().select("version", "timestamp", "operation", "operationMetrics").show()

# 6. Optimize & Vacuum
print("\n5. Optimize & Vacuum...")

# Optimize (compaction)
delta_table.optimize().executeCompaction()
print("✅ Table optimized")

# Vacuum old files (keep 7 days)
delta_table.vacuum(168)  # hours
print("✅ Old files vacuumed")

print("\n✅ Delta Lake operations complete!")

spark.stop()'''
            st.code(lab3_3, language='python')
            
            st.markdown("### LAB 4: Spark SQL & Data Lakehouse (75 min)")
            st.markdown("**Objective:** Build data lakehouse with Spark SQL")
            lab3_4 = '''from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, sum, avg, count

spark = SparkSession.builder.appName("DataLakehouse").getOrCreate()

print("🏛️ DATA LAKEHOUSE WITH SPARK SQL\n" + "="*60)

# 1. Create database
print("\n1. Creating Database...")

spark.sql("CREATE DATABASE IF NOT EXISTS analytics")
spark.sql("USE analytics")

print("✅ Database created")

# 2. Create tables from Parquet
print("\n2. Creating Tables...")

df_sales = spark.read.parquet('/data/sales.parquet')
df_sales.createOrReplaceTempView('sales_temp')

spark.sql("""
    CREATE TABLE IF NOT EXISTS sales
    USING DELTA
    AS SELECT * FROM sales_temp
""")

print("✅ Sales table created")

# 3. Complex SQL queries
print("\n3. Running Analytics Queries...")

# Query 1: Monthly revenue
monthly_revenue = spark.sql("""
    SELECT 
        year(order_date) as year,
        month(order_date) as month,
        COUNT(*) as num_orders,
        SUM(total_amount) as total_revenue,
        AVG(total_amount) as avg_order_value
    FROM sales
    GROUP BY year(order_date), month(order_date)
    ORDER BY year DESC, month DESC
""")

print("\nMonthly Revenue:")
monthly_revenue.show()

# Query 2: Customer segmentation
customer_segments = spark.sql("""
    WITH customer_metrics AS (
        SELECT 
            customer_id,
            COUNT(*) as num_orders,
            SUM(total_amount) as lifetime_value
        FROM sales
        GROUP BY customer_id
    )
    SELECT 
        CASE 
            WHEN lifetime_value > 10000 THEN 'VIP'
            WHEN lifetime_value > 5000 THEN 'Gold'
            WHEN lifetime_value > 1000 THEN 'Silver'
            ELSE 'Bronze'
        END as segment,
        COUNT(*) as num_customers,
        AVG(lifetime_value) as avg_clv
    FROM customer_metrics
    GROUP BY segment
    ORDER BY avg_clv DESC
""")

print("\nCustomer Segments:")
customer_segments.show()

# 4. Create materialized views
print("\n4. Creating Materialized Views...")

spark.sql("""
    CREATE OR REPLACE TABLE daily_summary
    USING DELTA
    AS
    SELECT 
        order_date,
        COUNT(*) as num_orders,
        SUM(total_amount) as total_revenue,
        AVG(total_amount) as avg_order_value
    FROM sales
    GROUP BY order_date
""")

print("✅ Materialized view created")

# 5. Query optimization
print("\n5. Query Optimization...")

# Analyze table for statistics
spark.sql("ANALYZE TABLE sales COMPUTE STATISTICS")

# Show query plan
monthly_revenue.explain(extended=True)

print("\n✅ Data lakehouse ready!")

spark.stop()'''
            st.code(lab3_4, language='python')
            
            st.markdown("### LAB 5: Advanced Partitioning & Performance Tuning (75 min)")
            st.markdown("**Objective:** Master data partitioning for optimal query performance")
            lab3_5 = '''from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, day
import time

spark = SparkSession.builder \\
    .appName("PartitioningStrategies") \\
    .config("spark.sql.adaptive.enabled", "true") \\
    .getOrCreate()

print("⚡ PARTITIONING & PERFORMANCE TUNING\n" + "="*60)

# 1. Load data
df = spark.read.parquet('/data/large_sales.parquet')

print(f"\nTotal records: {df.count():,}")
print(f"Current partitions: {df.rdd.getNumPartitions()}")

# 2. Partition by date (common pattern)
print("\n1. DATE-BASED PARTITIONING:")

df_with_parts = df \\
    .withColumn('year', year(col('order_date'))) \\
    .withColumn('month', month(col('order_date'))) \\
    .withColumn('day', day(col('order_date')))

# Write with partitioning
df_with_parts.write \\
    .partitionBy('year', 'month') \\
    .mode('overwrite') \\
    .parquet('/data/partitioned/sales')

print("✅ Data partitioned by year/month")

# 3. Query performance comparison
print("\n2. QUERY PERFORMANCE TEST:")

# Non-partitioned query
start = time.time()
df_non_part = spark.read.parquet('/data/large_sales.parquet')
result1 = df_non_part.filter(col('order_date') >= '2024-01-01').count()
time_non_part = time.time() - start

print(f"Non-partitioned query: {time_non_part:.2f}s")

# Partitioned query (partition pruning)
start = time.time()
df_part = spark.read.parquet('/data/partitioned/sales')
result2 = df_part.filter((col('year') == 2024) & (col('month') >= 1)).count()
time_part = time.time() - start

print(f"Partitioned query: {time_part:.2f}s")
print(f"Speedup: {time_non_part/time_part:.1f}x faster")

# 4. Bucketing for joins
print("\n3. BUCKETING STRATEGY:")

df.write \\
    .bucketBy(100, 'customer_id') \\
    .sortBy('order_date') \\
    .mode('overwrite') \\
    .saveAsTable('sales_bucketed')

print("✅ Data bucketed by customer_id (100 buckets)")

# 5. Repartition strategies
print("\n4. REPARTITION STRATEGIES:")

# By column (for joins)
df_repart_col = df.repartition(200, 'customer_id')
print(f"Repartitioned by customer_id: {df_repart_col.rdd.getNumPartitions()} partitions")

# By number (for parallelism)
df_repart_num = df.repartition(500)
print(f"Repartitioned to 500 partitions for max parallelism")

# Coalesce (reduce partitions)
df_coalesce = df.coalesce(10)
print(f"Coalesced to 10 partitions for final output")

# 6. Best practices summary
print("\n5. PARTITIONING BEST PRACTICES:")
print("="*60)
print("✅ Partition by frequently filtered columns (date, region)")
print("✅ Aim for 128MB-1GB per partition")
print("✅ Use bucketing for large dimension tables")
print("✅ Repartition before expensive operations (joins, aggregations)")
print("✅ Coalesce before writing small outputs")
print("✅ Enable adaptive query execution")

print("\n✅ Partitioning strategies mastered!")

spark.stop()'''
            st.code(lab3_5, language='python')
            
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
            
            st.markdown("### LAB 3: Stream Processing with Flink (90 min)")
            st.markdown("**Objective:** Build stateful stream processing pipeline")
            lab4_3 = '''from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col
import json

print("🌊 APACHE FLINK STREAM PROCESSING\n" + "="*60)

# 1. Setup Flink environment
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(4)

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
table_env = StreamTableEnvironment.create(env, settings)

print("✅ Flink environment initialized")

# 2. Create source table (Kafka)
table_env.execute_sql("""
    CREATE TABLE user_events (
        event_id STRING,
        user_id STRING,
        event_type STRING,
        product_id STRING,
        value DOUBLE,
        event_time TIMESTAMP(3),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'user_events',
        'properties.bootstrap.servers' = 'localhost:9092',
        'properties.group.id' = 'flink_consumer',
        'format' = 'json',
        'scan.startup.mode' = 'latest-offset'
    )
""")

print("✅ Kafka source table created")

# 3. Windowed aggregations
result = table_env.sql_query("""
    SELECT 
        TUMBLE_START(event_time, INTERVAL '1' MINUTE) as window_start,
        event_type,
        COUNT(*) as event_count,
        SUM(value) as total_value,
        AVG(value) as avg_value
    FROM user_events
    GROUP BY 
        TUMBLE(event_time, INTERVAL '1' MINUTE),
        event_type
""")

print("✅ Windowed aggregation query created")

# 4. Create sink table
table_env.execute_sql("""
    CREATE TABLE event_metrics (
        window_start TIMESTAMP(3),
        event_type STRING,
        event_count BIGINT,
        total_value DOUBLE,
        avg_value DOUBLE
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://localhost:5432/analytics',
        'table-name' = 'event_metrics',
        'username' = 'admin',
        'password' = 'secret'
    )
""")

print("✅ Sink table created")

# 5. Execute streaming job
result.execute_insert('event_metrics')

print("\n✅ Flink streaming job running!")
print("Processing events in 1-minute windows...")'''
            st.code(lab4_3, language='python')
            
            st.markdown("### LAB 4: Stream Joins & Enrichment (90 min)")
            st.markdown("**Objective:** Join multiple streams for real-time enrichment")
            lab4_4 = '''from kafka import KafkaProducer, KafkaConsumer
import json
from datetime import datetime
from collections import defaultdict

print("🔀 STREAM JOINS & ENRICHMENT\n" + "="*60)

class StreamJoiner:
    def __init__(self):
        self.user_cache = {}  # Cache user data
        self.product_cache = {}  # Cache product data
        self.enriched_events = []
    
    def load_reference_data(self):
        """Load reference data for enrichment"""
        # Simulate loading user data
        self.user_cache = {
            'user_1': {'name': 'John Doe', 'segment': 'Premium', 'country': 'US'},
            'user_2': {'name': 'Jane Smith', 'segment': 'Standard', 'country': 'UK'}
        }
        
        # Simulate loading product data
        self.product_cache = {
            'prod_1': {'name': 'Laptop', 'category': 'Electronics', 'price': 999.99},
            'prod_2': {'name': 'Mouse', 'category': 'Accessories', 'price': 29.99}
        }
        
        print("✅ Reference data loaded")
    
    def enrich_event(self, event):
        """Enrich event with user and product data"""
        user_id = event.get('user_id')
        product_id = event.get('product_id')
        
        # Join with user data
        user_data = self.user_cache.get(user_id, {})
        
        # Join with product data
        product_data = self.product_cache.get(product_id, {})
        
        # Create enriched event
        enriched = {
            **event,
            'user_name': user_data.get('name', 'Unknown'),
            'user_segment': user_data.get('segment', 'Unknown'),
            'user_country': user_data.get('country', 'Unknown'),
            'product_name': product_data.get('name', 'Unknown'),
            'product_category': product_data.get('category', 'Unknown'),
            'product_price': product_data.get('price', 0),
            'enrichment_timestamp': datetime.now().isoformat()
        }
        
        return enriched
    
    def process_stream(self, consumer, producer, output_topic):
        """Process and enrich stream"""
        print("\nProcessing and enriching events...\n")
        
        event_count = 0
        
        for message in consumer:
            event = message.value
            event_count += 1
            
            # Enrich event
            enriched_event = self.enrich_event(event)
            
            # Send to output topic
            producer.send(output_topic, value=enriched_event)
            
            # Print sample
            if event_count <= 3:
                print(f"Event {event_count}:")
                print(f"  Original: {event['event_type']} by {event['user_id']}")
                print(f"  Enriched: {enriched_event['user_name']} ({enriched_event['user_segment']})")
                print(f"            {enriched_event['product_name']} - ${enriched_event['product_price']}")
                print()
            
            if event_count >= 50:
                break
        
        print(f"\n✅ Enriched {event_count} events")

# Setup
joiner = StreamJoiner()
joiner.load_reference_data()

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'raw_events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Process stream
joiner.process_stream(consumer, producer, 'enriched_events')

print("\n✅ Stream enrichment pipeline complete!")'''
            st.code(lab4_4, language='python')
            
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
glue_job = """
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
"""

print("\n2. AWS Glue Job Code:")
print(glue_job)

# 3. Lambda Function for Trigger
lambda_code = """
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
"""

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
            
            st.markdown("### LAB 3: GCP BigQuery & Dataflow (90 min)")
            st.markdown("**Objective:** Build data pipeline on Google Cloud Platform")
            lab5_3 = '''from google.cloud import bigquery, storage
import pandas as pd

print("☁️ GCP DATA PIPELINE\n" + "="*60)

# 1. Upload to Cloud Storage
print("\n1. Uploading to GCS...")

storage_client = storage.Client()
bucket = storage_client.bucket('my-data-lake')

df = pd.read_csv('sales_data.csv')
blob = bucket.blob('raw/sales_data.csv')
blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')

print("✅ Data uploaded to GCS")

# 2. Load to BigQuery
print("\n2. Loading to BigQuery...")

bq_client = bigquery.Client()

# Create dataset
dataset_id = 'analytics'
dataset = bigquery.Dataset(f"{bq_client.project}.{dataset_id}")
dataset.location = 'US'
bq_client.create_dataset(dataset, exists_ok=True)

print(f"✅ Dataset {dataset_id} ready")

# Create table schema
schema = [
    bigquery.SchemaField('order_id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('customer_id', 'STRING'),
    bigquery.SchemaField('product_id', 'STRING'),
    bigquery.SchemaField('quantity', 'INTEGER'),
    bigquery.SchemaField('unit_price', 'FLOAT'),
    bigquery.SchemaField('total_amount', 'FLOAT'),
    bigquery.SchemaField('order_date', 'DATE')
]

table_id = f"{bq_client.project}.{dataset_id}.sales"
table = bigquery.Table(table_id, schema=schema)
table = bq_client.create_table(table, exists_ok=True)

print(f"✅ Table {table_id} created")

# Load data from GCS
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=False,
    schema=schema
)

uri = 'gs://my-data-lake/raw/sales_data.csv'
load_job = bq_client.load_table_from_uri(uri, table_id, job_config=job_config)

load_job.result()  # Wait for job to complete

print(f"✅ Loaded {load_job.output_rows} rows to BigQuery")

# 3. Query BigQuery
print("\n3. Querying BigQuery...")

query = """
    SELECT 
        product_id,
        COUNT(*) as num_orders,
        SUM(total_amount) as total_revenue
    FROM `analytics.sales`
    GROUP BY product_id
    ORDER BY total_revenue DESC
    LIMIT 10
"""

query_job = bq_client.query(query)
results = query_job.result()

print("\nTop 10 products:")
for row in results:
    print(f"  {row.product_id}: ${row.total_revenue:,.2f}")

print("\n✅ GCP pipeline complete!")'''
            st.code(lab5_3, language='python')
            
            st.markdown("### LAB 4: Azure Synapse & Data Factory (75 min)")
            st.markdown("**Objective:** Build data pipeline on Microsoft Azure")
            lab5_4 = '''from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import pandas as pd

print("☁️ AZURE DATA PIPELINE\n" + "="*60)

# 1. Upload to Azure Blob Storage
print("\n1. Uploading to Azure Blob Storage...")

connection_string = "DefaultEndpointsProtocol=https;AccountName=mydatalake;..."
blob_service = BlobServiceClient.from_connection_string(connection_string)

container_name = 'raw-data'
container_client = blob_service.get_container_client(container_name)

df = pd.read_csv('sales_data.csv')
blob_client = container_client.get_blob_client('sales/sales_data.csv')
blob_client.upload_blob(df.to_csv(index=False), overwrite=True)

print("✅ Data uploaded to Azure Blob Storage")

# 2. Azure Data Factory Pipeline (JSON)
adf_pipeline = {
    "name": "SalesETLPipeline",
    "properties": {
        "activities": [
            {
                "name": "CopyFromBlobToSynapse",
                "type": "Copy",
                "inputs": [{
                    "referenceName": "BlobSalesData",
                    "type": "DatasetReference"
                }],
                "outputs": [{
                    "referenceName": "SynapseSalesTable",
                    "type": "DatasetReference"
                }],
                "typeProperties": {
                    "source": {"type": "DelimitedTextSource"},
                    "sink": {"type": "SqlDWSink"}
                }
            }
        ]
    }
}

print("\n2. Azure Data Factory Pipeline:")
import json
print(json.dumps(adf_pipeline, indent=2))

# 3. Query Azure Synapse
synapse_query = """
SELECT 
    product_id,
    COUNT(*) as num_orders,
    SUM(total_amount) as total_revenue
FROM sales
GROUP BY product_id
ORDER BY total_revenue DESC;
"""

print("\n3. Synapse Analytics Query:")
print(synapse_query)

print("\n✅ Azure pipeline complete!")'''
            st.code(lab5_4, language='python')
            
            st.success("✅ Unit 5 Labs Complete: Multi-cloud data engineering mastered!")
        elif selected_unit == 6:
            st.markdown("### 🔥 Unit 6: Orchestration & Monitoring")
            st.markdown("**COMPREHENSIVE HANDS-ON LABS - Apache Airflow Production Code!**")
            
            st.markdown("### LAB 1: Apache Airflow DAG (120 min)")
            lab6_code = '''from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'data_team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('daily_sales_etl', default_args=default_args, schedule_interval='0 2 * * *')

def extract_data():
    df = pd.read_csv('/data/raw/sales.csv')
    df.to_parquet('/data/staging/sales.parquet')
    return len(df)

extract_task = PythonOperator(task_id='extract', python_callable=extract_data, dag=dag)
print("✅ Airflow DAG created!")'''
            st.code(lab6_code, language='python')
            
            st.markdown("### LAB 2: Advanced Airflow with Sensors & Branching (90 min)")
            st.markdown("**Objective:** Build complex DAG with conditional logic")
            lab6_2 = '''from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'data_team',
    'retries': 2,
    'retry_delay': timedelta(minutes=3)
}

dag = DAG(
    'advanced_etl_pipeline',
    default_args=default_args,
    schedule_interval='0 3 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False
)

# Sensor - wait for file
wait_for_file = FileSensor(
    task_id='wait_for_data_file',
    filepath='/data/incoming/sales_*.csv',
    poke_interval=60,
    timeout=600,
    dag=dag
)

def check_data_size(**context):
    """Check if data meets threshold"""
    df = pd.read_csv('/data/incoming/sales_latest.csv')
    
    if len(df) > 10000:
        return 'process_large_dataset'
    else:
        return 'process_small_dataset'

branch_task = BranchPythonOperator(
    task_id='check_data_size',
    python_callable=check_data_size,
    dag=dag
)

def process_large():
    print("Processing large dataset with Spark...")
    # Spark processing logic
    return "large_processed"

def process_small():
    print("Processing small dataset with Pandas...")
    # Pandas processing logic
    return "small_processed"

large_task = PythonOperator(
    task_id='process_large_dataset',
    python_callable=process_large,
    dag=dag
)

small_task = PythonOperator(
    task_id='process_small_dataset',
    python_callable=process_small,
    dag=dag
)

join_task = DummyOperator(
    task_id='join_branches',
    trigger_rule='none_failed_min_one_success',
    dag=dag
)

def send_notification(**context):
    print(f"Pipeline completed at {datetime.now()}")
    # Send email/Slack notification

notify_task = PythonOperator(
    task_id='send_notification',
    python_callable=send_notification,
    dag=dag
)

# Define workflow
wait_for_file >> branch_task >> [large_task, small_task] >> join_task >> notify_task

print("✅ Advanced Airflow DAG with branching created!")'''
            st.code(lab6_2, language='python')
            
            st.markdown("### LAB 3: Data Quality Monitoring with Airflow (90 min)")
            st.markdown("**Objective:** Implement automated data quality checks in pipelines")
            lab6_3 = '''from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.email import send_email
from datetime import datetime, timedelta
import pandas as pd
import great_expectations as ge

default_args = {
    'owner': 'data_quality_team',
    'email': ['quality@company.com'],
    'email_on_failure': True,
    'retries': 1
}

dag = DAG(
    'data_quality_pipeline',
    default_args=default_args,
    schedule_interval='0 4 * * *',
    start_date=datetime(2024, 1, 1)
)

def validate_schema(**context):
    """Validate data schema"""
    df = pd.read_parquet('/data/processed/sales.parquet')
    
    required_columns = ['order_id', 'customer_id', 'product_id', 'total_amount', 'order_date']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    print("✅ Schema validation passed")

def validate_completeness(**context):
    """Check for missing values"""
    df = pd.read_parquet('/data/processed/sales.parquet')
    
    critical_columns = ['order_id', 'customer_id', 'total_amount']
    
    for col in critical_columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        
        if null_pct > 0:
            raise ValueError(f"{col} has {null_pct:.2f}% null values")
    
    print("✅ Completeness validation passed")

def validate_uniqueness(**context):
    """Check for duplicates"""
    df = pd.read_parquet('/data/processed/sales.parquet')
    
    dup_count = df['order_id'].duplicated().sum()
    
    if dup_count > 0:
        raise ValueError(f"Found {dup_count} duplicate order_ids")
    
    print("✅ Uniqueness validation passed")

def validate_ranges(**context):
    """Validate data ranges"""
    df = pd.read_parquet('/data/processed/sales.parquet')
    
    # Check for negative amounts
    if (df['total_amount'] < 0).any():
        raise ValueError("Negative amounts found")
    
    # Check for future dates
    df['order_date'] = pd.to_datetime(df['order_date'])
    if (df['order_date'] > datetime.now()).any():
        raise ValueError("Future dates found")
    
    print("✅ Range validation passed")

def validate_with_great_expectations(**context):
    """Advanced validation with Great Expectations"""
    df = pd.read_parquet('/data/processed/sales.parquet')
    ge_df = ge.from_pandas(df)
    
    # Define expectations
    ge_df.expect_column_values_to_not_be_null('order_id')
    ge_df.expect_column_values_to_be_unique('order_id')
    ge_df.expect_column_values_to_be_between('total_amount', min_value=0, max_value=100000)
    ge_df.expect_column_values_to_be_in_set('status', ['completed', 'pending', 'cancelled'])
    
    # Validate
    results = ge_df.validate()
    
    if not results['success']:
        failed = [r for r in results['results'] if not r['success']]
        raise ValueError(f"Quality checks failed: {len(failed)} expectations")
    
    print("✅ Great Expectations validation passed")

def send_quality_report(**context):
    """Send quality report"""
    report = f"""
    Data Quality Report - {datetime.now().strftime('%Y-%m-%d')}
    
    All quality checks passed:
    ✅ Schema validation
    ✅ Completeness check
    ✅ Uniqueness check
    ✅ Range validation
    ✅ Great Expectations suite
    
    Pipeline is healthy and ready for consumption.
    """
    
    print(report)
    # send_email(to=['team@company.com'], subject='Quality Report', html_content=report)

# Define tasks
schema_task = PythonOperator(task_id='validate_schema', python_callable=validate_schema, dag=dag)
completeness_task = PythonOperator(task_id='validate_completeness', python_callable=validate_completeness, dag=dag)
uniqueness_task = PythonOperator(task_id='validate_uniqueness', python_callable=validate_uniqueness, dag=dag)
ranges_task = PythonOperator(task_id='validate_ranges', python_callable=validate_ranges, dag=dag)
ge_task = PythonOperator(task_id='validate_great_expectations', python_callable=validate_with_great_expectations, dag=dag)
report_task = PythonOperator(task_id='send_quality_report', python_callable=send_quality_report, dag=dag)

# Workflow
[schema_task, completeness_task, uniqueness_task, ranges_task, ge_task] >> report_task

print("✅ Data quality monitoring DAG created!")'''
            st.code(lab6_3, language='python')
            
            st.success("✅ Unit 6 Complete: Airflow orchestration mastered!")
        elif selected_unit == 7:
            st.markdown("### 🎯 Unit 7: Data Engineering Capstone Projects")
            st.markdown("**Choose one comprehensive project to demonstrate your data engineering expertise**")
            
            st.markdown("## 📊 Capstone Project Options")
            
            st.markdown("### Option 1: Real-time E-Commerce Analytics Platform")
            st.markdown("""
**Objective:** Build end-to-end real-time analytics system

**Architecture:**
- Kafka for event streaming
- Spark Streaming for processing
- PostgreSQL for analytics storage
- Airflow for orchestration
- Grafana for monitoring

**Deliverables:**
1. **Event Producer:**
   - Kafka producer for user events
   - Schema registry integration
   - Event validation

2. **Stream Processing:**
   - Spark Streaming job
   - Real-time aggregations
   - Windowed metrics
   - State management

3. **Data Warehouse:**
   - Star schema design
   - Fact and dimension tables
   - Incremental loading

4. **Orchestration:**
   - Airflow DAGs
   - Dependency management
   - Error handling

5. **Monitoring:**
   - Grafana dashboards
   - Alerting rules
   - Performance metrics

6. **Documentation:**
   - Architecture diagram
   - Setup instructions
   - Operational runbook

**Skills Demonstrated:** Kafka, Spark, SQL, Airflow, monitoring""")
            
            st.markdown("### Option 2: Cloud Data Lake & Warehouse (AWS/GCP/Azure)")
            st.markdown("""
**Objective:** Build scalable cloud-native data platform

**Architecture:**
- S3/GCS/Blob (data lake)
- Glue/Dataflow/Data Factory (ETL)
- Redshift/BigQuery/Synapse (warehouse)
- Terraform (infrastructure)
- CloudWatch/Stackdriver (monitoring)

**Deliverables:**
1. **Data Lake:**
   - Multi-zone architecture (raw/processed/curated)
   - Partitioning strategy
   - Data catalog

2. **ETL Pipelines:**
   - Batch processing jobs
   - Incremental loading
   - Data quality checks

3. **Data Warehouse:**
   - Dimensional model
   - Aggregate tables
   - Query optimization

4. **Infrastructure as Code:**
   - Terraform modules
   - Environment configs
   - CI/CD pipeline

5. **Cost Optimization:**
   - Resource sizing
   - Storage lifecycle policies
   - Query optimization

6. **Documentation:**
   - Cloud architecture
   - Cost analysis
   - Security best practices

**Skills Demonstrated:** Cloud platforms, IaC, cost optimization, security""")
            
            st.markdown("### Option 3: Batch Processing Pipeline at Scale")
            st.markdown("""
**Objective:** Process billions of records efficiently

**Architecture:**
- Apache Spark (PySpark)
- Delta Lake (ACID transactions)
- Airflow (orchestration)
- Great Expectations (quality)
- Prometheus (monitoring)

**Deliverables:**
1. **Spark Jobs:**
   - Multi-stage transformations
   - Performance optimized
   - Broadcast joins
   - Partitioning strategy

2. **Delta Lake:**
   - ACID transactions
   - Time travel
   - Schema evolution
   - Optimize & vacuum

3. **Data Quality:**
   - Great Expectations suite
   - Validation checkpoints
   - Quality reports

4. **Orchestration:**
   - Airflow DAGs
   - Dynamic task generation
   - SLA monitoring

5. **Performance:**
   - Benchmark results
   - Optimization report
   - Scalability analysis

6. **Documentation:**
   - Performance tuning guide
   - Troubleshooting playbook

**Skills Demonstrated:** Spark optimization, Delta Lake, data quality, scale""")
            
            st.markdown("### Option 4: CDC & Change Data Capture Pipeline")
            st.markdown("""
**Objective:** Build real-time CDC pipeline for database replication

**Architecture:**
- Debezium (CDC)
- Kafka (event streaming)
- Kafka Connect (connectors)
- PostgreSQL (source & target)
- Airflow (orchestration)

**Deliverables:**
1. **CDC Setup:**
   - Debezium connector config
   - Schema registry
   - Topic management

2. **Stream Processing:**
   - Change event processing
   - Transformation logic
   - Deduplication

3. **Target Loading:**
   - Sink connectors
   - Upsert logic
   - Conflict resolution

4. **Monitoring:**
   - Lag monitoring
   - Error tracking
   - Data freshness

5. **Testing:**
   - End-to-end tests
   - Failure scenarios
   - Recovery procedures

6. **Documentation:**
   - CDC architecture
   - Troubleshooting guide

**Skills Demonstrated:** CDC, Debezium, Kafka Connect, real-time replication""")
            
            st.markdown("### Option 5: Data Quality & Observability Platform")
            st.markdown("""
**Objective:** Build comprehensive data quality monitoring system

**Architecture:**
- Great Expectations (quality)
- Airflow (orchestration)
- PostgreSQL (metadata)
- Grafana (dashboards)
- PagerDuty (alerting)

**Deliverables:**
1. **Quality Framework:**
   - Expectation suites
   - Validation checkpoints
   - Custom expectations

2. **Monitoring:**
   - Quality dashboards
   - Trend analysis
   - Anomaly detection

3. **Alerting:**
   - Alert rules
   - Escalation policies
   - Incident tracking

4. **Lineage:**
   - Data lineage tracking
   - Impact analysis
   - Dependency mapping

5. **Reporting:**
   - Quality scorecards
   - SLA tracking
   - Executive summaries

6. **Documentation:**
   - Quality standards
   - Runbook

**Skills Demonstrated:** Data quality, observability, monitoring, alerting""")
            
            st.markdown("## 💻 Complete Capstone Implementation Example")
            st.markdown("**Full End-to-End E-Commerce Analytics Platform Code**")
            
            st.markdown("### 1. Kafka Event Producer")
            capstone_producer = '''# kafka_producer.py
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

class EcommerceEventProducer:
    def __init__(self, bootstrap_servers=['localhost:9092']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas
            retries=3,
            compression_type='gzip'
        )
        
    def generate_event(self):
        """Generate realistic e-commerce event"""
        event_types = ['page_view', 'add_to_cart', 'purchase', 'search', 'remove_from_cart']
        
        event = {
            'event_id': f"evt_{int(time.time()*1000)}_{random.randint(1000,9999)}",
            'event_type': random.choice(event_types),
            'user_id': f"user_{random.randint(1, 10000)}",
            'session_id': f"sess_{random.randint(1, 5000)}",
            'product_id': f"prod_{random.randint(1, 500)}",
            'category': random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports']),
            'timestamp': datetime.now().isoformat(),
            'device': random.choice(['mobile', 'desktop', 'tablet']),
            'location': random.choice(['US', 'UK', 'CA', 'DE', 'FR'])
        }
        
        # Add event-specific data
        if event['event_type'] == 'purchase':
            event['amount'] = round(random.uniform(10, 500), 2)
            event['quantity'] = random.randint(1, 5)
        elif event['event_type'] == 'search':
            event['search_term'] = random.choice(['laptop', 'shoes', 'book', 'headphones'])
            
        return event
    
    def produce_events(self, num_events=1000, events_per_second=10):
        """Produce events at specified rate"""
        print(f"Starting event production: {num_events} events at {events_per_second}/sec")
        
        for i in range(num_events):
            event = self.generate_event()
            
            # Use user_id as partition key for consistent ordering per user
            self.producer.send(
                'ecommerce_events',
                key=event['user_id'],
                value=event
            )
            
            if (i + 1) % 100 == 0:
                print(f"Produced {i + 1} events")
            
            time.sleep(1.0 / events_per_second)
        
        self.producer.flush()
        print(f"✅ Completed: {num_events} events produced")
        
    def close(self):
        self.producer.close()

if __name__ == "__main__":
    producer = EcommerceEventProducer()
    try:
        producer.produce_events(num_events=10000, events_per_second=100)
    finally:
        producer.close()'''
            st.code(capstone_producer, language='python')
            
            st.markdown("### 2. Spark Streaming Consumer")
            capstone_spark = '''# spark_streaming_job.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, count, sum as _sum, avg, max as _max,
    current_timestamp, to_timestamp
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# Define schema for incoming events
event_schema = StructType([
    StructField("event_id", StringType()),
    StructField("event_type", StringType()),
    StructField("user_id", StringType()),
    StructField("session_id", StringType()),
    StructField("product_id", StringType()),
    StructField("category", StringType()),
    StructField("timestamp", StringType()),
    StructField("device", StringType()),
    StructField("location", StringType()),
    StructField("amount", DoubleType()),
    StructField("quantity", IntegerType())
])

# Initialize Spark Session
spark = SparkSession.builder \\
    .appName("EcommerceRealTimeAnalytics") \\
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \\
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read from Kafka
df = spark.readStream \\
    .format("kafka") \\
    .option("kafka.bootstrap.servers", "localhost:9092") \\
    .option("subscribe", "ecommerce_events") \\
    .option("startingOffsets", "latest") \\
    .load()

# Parse JSON and extract event data
events = df.selectExpr("CAST(value AS STRING) as json") \\
    .select(from_json(col("json"), event_schema).alias("data")) \\
    .select("data.*") \\
    .withColumn("timestamp", to_timestamp(col("timestamp")))

# Real-time metrics: Events per minute by type
events_per_minute = events \\
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("event_type")
    ) \\
    .agg(
        count("*").alias("event_count"),
        count(col("user_id").distinct()).alias("unique_users")
    )

# Sales metrics: Revenue per minute
sales_metrics = events \\
    .filter(col("event_type") == "purchase") \\
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("category")
    ) \\
    .agg(
        _sum("amount").alias("total_revenue"),
        avg("amount").alias("avg_order_value"),
        count("*").alias("num_orders"),
        _sum("quantity").alias("total_items")
    )

# Popular products: Most viewed in last 10 minutes
popular_products = events \\
    .filter(col("event_type") == "page_view") \\
    .groupBy(
        window(col("timestamp"), "10 minutes", "5 minutes"),
        col("product_id"),
        col("category")
    ) \\
    .agg(count("*").alias("view_count"))

# Write to console (for demo) and to Delta Lake
query1 = events_per_minute.writeStream \\
    .outputMode("update") \\
    .format("delta") \\
    .option("path", "/data/delta/events_per_minute") \\
    .start()

query2 = sales_metrics.writeStream \\
    .outputMode("update") \\
    .format("delta") \\
    .option("path", "/data/delta/sales_metrics") \\
    .start()

query3 = popular_products.writeStream \\
    .outputMode("update") \\
    .format("delta") \\
    .option("path", "/data/delta/popular_products") \\
    .start()

# Keep running
spark.streams.awaitAnyTermination()'''
            st.code(capstone_spark, language='python')
            
            st.markdown("### 3. Airflow Orchestration DAG")
            capstone_airflow = '''# airflow_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import great_expectations as ge

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ecommerce_analytics_pipeline',
    default_args=default_args,
    description='End-to-end e-commerce analytics',
    schedule_interval='@hourly',
    catchup=False,
    max_active_runs=1
)

# 1. Data Quality Checks
def run_data_quality_checks(**context):
    """Run Great Expectations validation"""
    context_ge = ge.data_context.DataContext()
    
    suite_name = "ecommerce_events_suite"
    checkpoint_name = "hourly_checkpoint"
    
    checkpoint_result = context_ge.run_checkpoint(
        checkpoint_name=checkpoint_name,
        batch_request={
            "datasource_name": "delta_datasource",
            "data_asset_name": "events_per_minute",
            "batch_spec_passthrough": {
                "reader_method": "read_delta",
                "reader_options": {"path": "/data/delta/events_per_minute"}
            }
        }
    )
    
    if not checkpoint_result.success:
        raise ValueError("Data quality checks failed!")
    
    print("✅ Data quality validation passed")

quality_check = PythonOperator(
    task_id='data_quality_check',
    python_callable=run_data_quality_checks,
    dag=dag
)

# 2. Aggregate to Hourly Metrics
aggregate_metrics = SparkSubmitOperator(
    task_id='aggregate_hourly_metrics',
    application='/opt/spark/jobs/hourly_aggregation.py',
    conn_id='spark_default',
    total_executor_cores=4,
    executor_memory='4G',
    dag=dag
)

# 3. Load to PostgreSQL Warehouse
load_warehouse = PostgresOperator(
    task_id='load_to_warehouse',
    postgres_conn_id='postgres_warehouse',
    sql="""
    INSERT INTO fact_hourly_metrics (
        hour, event_type, event_count, unique_users, load_timestamp
    )
    SELECT 
        DATE_TRUNC('hour', window.start) as hour,
        event_type,
        SUM(event_count) as event_count,
        SUM(unique_users) as unique_users,
        CURRENT_TIMESTAMP as load_timestamp
    FROM delta.`/data/delta/events_per_minute`
    WHERE window.start >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
    GROUP BY DATE_TRUNC('hour', window.start), event_type
    ON CONFLICT (hour, event_type) 
    DO UPDATE SET 
        event_count = EXCLUDED.event_count,
        unique_users = EXCLUDED.unique_users,
        load_timestamp = EXCLUDED.load_timestamp;
    """,
    dag=dag
)

# 4. Update Materialized Views
refresh_views = PostgresOperator(
    task_id='refresh_materialized_views',
    postgres_conn_id='postgres_warehouse',
    sql="""
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_revenue;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_product_performance;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_user_segments;
    """,
    dag=dag
)

# 5. Send Success Notification
def send_success_notification(**context):
    import requests
    
    execution_date = context['execution_date']
    message = f"✅ Pipeline completed successfully for {execution_date}"
    
    # Send to Slack
    requests.post(
        'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
        json={'text': message}
    )

notify = PythonOperator(
    task_id='send_notification',
    python_callable=send_success_notification,
    dag=dag
)

# Define task dependencies
quality_check >> aggregate_metrics >> load_warehouse >> refresh_views >> notify'''
            st.code(capstone_airflow, language='python')
            
            st.markdown("### 4. Monitoring & Alerting")
            capstone_monitoring = '''# prometheus_metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
events_processed = Counter(
    'events_processed_total',
    'Total events processed',
    ['event_type', 'status']
)

processing_duration = Histogram(
    'processing_duration_seconds',
    'Time spent processing events',
    ['stage']
)

pipeline_lag = Gauge(
    'pipeline_lag_seconds',
    'Lag between event time and processing time'
)

data_quality_score = Gauge(
    'data_quality_score',
    'Data quality score 0-100',
    ['dimension']
)

# Start Prometheus metrics server
start_http_server(8000)

# Track metrics in your pipeline
def process_batch(events):
    with processing_duration.labels(stage='transform').time():
        # Process events
        for event in events:
            try:
                # Processing logic
                events_processed.labels(
                    event_type=event['event_type'],
                    status='success'
                ).inc()
            except Exception as e:
                events_processed.labels(
                    event_type=event['event_type'],
                    status='error'
                ).inc()
        
        # Update lag metric
        current_lag = time.time() - event['timestamp']
        pipeline_lag.set(current_lag)

# Grafana dashboard JSON (import to Grafana)
grafana_dashboard = {
    "dashboard": {
        "title": "E-Commerce Analytics Pipeline",
        "panels": [
            {
                "title": "Events Processed",
                "targets": [{
                    "expr": "rate(events_processed_total[5m])"
                }]
            },
            {
                "title": "Pipeline Lag",
                "targets": [{
                    "expr": "pipeline_lag_seconds"
                }]
            },
            {
                "title": "Processing Duration p95",
                "targets": [{
                    "expr": "histogram_quantile(0.95, processing_duration_seconds_bucket)"
                }]
            },
            {
                "title": "Data Quality Score",
                "targets": [{
                    "expr": "data_quality_score"
                }]
            }
        ]
    }
}'''
            st.code(capstone_monitoring, language='python')
            
            st.markdown("### 5. Infrastructure as Code (Terraform)")
            capstone_terraform = '''# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "ecommerce-analytics/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC for data platform
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "ecommerce-analytics-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
}

# MSK (Kafka) Cluster
resource "aws_msk_cluster" "kafka" {
  cluster_name           = "ecommerce-events"
  kafka_version          = "3.5.1"
  number_of_broker_nodes = 3
  
  broker_node_group_info {
    instance_type   = "kafka.m5.large"
    client_subnets  = module.vpc.private_subnets
    security_groups = [aws_security_group.kafka.id]
    
    storage_info {
      ebs_storage_info {
        volume_size = 100
      }
    }
  }
}

# EMR Cluster for Spark
resource "aws_emr_cluster" "spark" {
  name          = "ecommerce-analytics-spark"
  release_label = "emr-6.15.0"
  applications  = ["Spark", "Hadoop"]
  
  ec2_attributes {
    subnet_id                         = module.vpc.private_subnets[0]
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_slave.id
    instance_profile                  = aws_iam_instance_profile.emr.arn
  }
  
  master_instance_group {
    instance_type = "m5.xlarge"
  }
  
  core_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 3
  }
}

# RDS PostgreSQL for Warehouse
resource "aws_db_instance" "warehouse" {
  identifier = "ecommerce-warehouse"
  
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = "db.r5.xlarge"
  allocated_storage = 100
  
  db_name  = "analytics"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.warehouse.name
  
  backup_retention_period = 7
  multi_az                = true
}

# S3 Bucket for Delta Lake
resource "aws_s3_bucket" "delta_lake" {
  bucket = "ecommerce-analytics-delta-lake"
}

resource "aws_s3_bucket_versioning" "delta_lake" {
  bucket = aws_s3_bucket.delta_lake.id
  
  versioning_configuration {
    status = "Enabled"
  }
}'''
            st.code(capstone_terraform, language='terraform')
            
            st.markdown("## 📝 Capstone Evaluation Rubric")
            st.markdown("""
**Your capstone will be evaluated on:**

### 1. Architecture & Design (25%)
- ✅ Well-designed data model
- ✅ Scalable architecture
- ✅ Clear data flow diagram
- ✅ Technology choices justified

### 2. Implementation Quality (30%)
- ✅ Production-quality code
- ✅ Error handling & logging
- ✅ Performance optimized
- ✅ Security best practices

### 3. Data Quality (20%)
- ✅ Validation framework
- ✅ Quality monitoring
- ✅ Data lineage tracking
- ✅ Testing coverage

### 4. Operations (15%)
- ✅ Orchestration (Airflow)
- ✅ Monitoring & alerting
- ✅ Documentation complete
- ✅ Runbook for incidents

### 5. Business Impact (10%)
- ✅ Solves real problem
- ✅ Measurable value
- ✅ Cost-effective solution
- ✅ Scalability demonstrated

**Grading Scale:**
- 90-100%: Exceptional - Production-ready
- 80-89%: Strong - Minor improvements
- 70-79%: Good - Meets requirements
- Below 70%: Needs revision

**Bonus Points:**
- Infrastructure as Code (Terraform)
- CI/CD pipeline
- Kubernetes deployment
- Multi-cloud implementation
- Advanced monitoring (Prometheus, Grafana)""")
            
            st.success("✅ Choose your capstone project and build a world-class data platform!")
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
