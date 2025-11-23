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
