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
            st.markdown(
                """These labs focus on building your first data pipelines.

- **Lab 1 – Extract and load**
  - Extract data from a CSV or API.
  - Load it into a local database or file.

- **Lab 2 – Add transformations**
  - Add cleaning and filtering steps to your pipeline.
  - Handle missing values and data types.

- **Mini project – End-to-end ETL script**
  - Build a Python script that extracts, transforms and loads data.
  - Add logging and error handling.
"""
            )
        elif selected_unit == 2:
            st.markdown(
                """These labs emphasise data warehouse design.

- **Lab 1 – Design a star schema**
  - Choose a business domain (e.g. retail, healthcare).
  - Identify facts and dimensions.
  - Sketch the schema on paper or in a tool.

- **Lab 2 – Implement the schema**
  - Create tables in a database.
  - Load sample data into fact and dimension tables.

- **Mini project – SCD Type 2 implementation**
  - Implement a slowly changing dimension pipeline.
  - Track historical changes to dimension records.
"""
            )
        elif selected_unit == 3:
            st.markdown(
                """These labs focus on batch processing at scale.

- **Lab 1 – Spark basics**
  - Load a dataset into a Spark DataFrame.
  - Perform filters, joins and aggregations.

- **Lab 2 – Optimise a Spark job**
  - Identify and fix performance issues (shuffles, skew).
  - Use partitioning and caching effectively.

- **Mini project – Batch pipeline with Spark**
  - Build a multi-stage batch pipeline.
  - Read from source, transform, write to target.
"""
            )
        elif selected_unit == 4:
            st.markdown(
                """These labs emphasise stream processing.

- **Lab 1 – Consume from a stream**
  - Set up a simple Kafka topic or cloud streaming service.
  - Write a consumer that reads and prints events.

- **Lab 2 – Windowed aggregations**
  - Compute aggregates over time windows (e.g. events per minute).

- **Mini project – Real-time alerting pipeline**
  - Build a pipeline that detects anomalies or thresholds.
  - Send alerts or write to a database.
"""
            )
        elif selected_unit == 5:
            st.markdown(
                """These labs bring cloud platforms into practice.

- **Lab 1 – Cloud storage and compute**
  - Upload data to cloud storage (S3, Blob, GCS).
  - Run a simple job using cloud compute.

- **Lab 2 – Infrastructure as code**
  - Define a simple cloud resource (bucket, database) using Terraform
    or CloudFormation.

- **Mini project – Cloud-native pipeline**
  - Build a pipeline using managed cloud services.
  - Document the architecture and cost considerations.
"""
            )
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
