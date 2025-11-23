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


COURSE_ID = "data_analyst_pathway"
COURSE_NAME = "Data Analyst Pathway"


UNITS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Data & Business Questions for Analysts",
        "level": "Beginner",
        "glh": 12,
        "credits": 2,
    },
    2: {
        "name": "Spreadsheet Skills for Analysis",
        "level": "Beginner",
        "glh": 18,
        "credits": 3,
    },
    3: {
        "name": "SQL for Data Analysts",
        "level": "Beginner/Intermediate",
        "glh": 24,
        "credits": 4,
    },
    4: {
        "name": "BI Dashboards & Storytelling",
        "level": "Intermediate",
        "glh": 18,
        "credits": 3,
    },
    5: {
        "name": "Python for Analysts",
        "level": "Intermediate",
        "glh": 24,
        "credits": 4,
    },
    6: {
        "name": "Metrics, A/B Tests & KPI Design",
        "level": "Intermediate",
        "glh": 18,
        "credits": 3,
    },
    7: {
        "name": "Data Analyst Capstone Project",
        "level": "Intermediate",
        "glh": 36,
        "credits": 6,
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
        st.markdown("#### 📘 What does a data analyst do?")
        st.markdown(
            """This unit introduces the **day-to-day work** of data analysts in
healthcare, retail, finance and other sectors:

- Turning business questions into measurable metrics.
- Working with stakeholders to clarify what success looks like.
- Choosing the right data sources and tools for a question.

You will see how analysts act as a **bridge** between raw data and
decisions, not just "report builders".
"""
        )

        st.markdown("#### 🎯 From vague requests to clear questions")
        st.markdown(
            """Stakeholders rarely speak in perfect analytics language. You will
practise rewriting vague requests such as:

- "Why are we so busy?"
- "Marketing isn't working."

into concrete, measurable questions with clear definitions and time
frames.
"""
        )

        st.markdown("#### 🧩 Mapping questions to data sources")
        st.markdown(
            """You will think about where data actually lives:

- Transactional systems (bookings, EHR, sales).
- CRM / marketing tools.
- Spreadsheets and manual trackers.

The focus is on **practical reasoning**: what tables or files do we need
to answer this question reliably?
"""
        )
    elif unit_number == 2:
        st.markdown("#### 📘 Why spreadsheets still matter")
        st.markdown(
            """Most organisations still rely heavily on Excel/Sheets. This unit
focuses on **practical spreadsheet skills** for cleaning, exploring and
summarising data.

You will treat spreadsheets as a serious analysis tool, not just a place
to store lists.
"""
        )

        st.markdown("#### 🧹 Cleaning and structuring data")
        st.markdown(
            """You will practise:

- Removing duplicates and obvious errors.
- Handling blanks and inconsistent formats.
- Turning "report-style" sheets into clean tables suitable for
  analysis.
"""
        )

        st.markdown("#### 🔢 Formulas, lookups and pivot tables")
        st.markdown(
            """Key analyst skills include:

- Conditional aggregates (e.g. `SUMIFS`, `COUNTIFS`).
- Lookups/joins (`XLOOKUP`, `VLOOKUP`, `INDEX/MATCH`).
- Pivot tables for quick grouped summaries.

You will use these to answer realistic questions from small datasets.
"""
        )
    elif unit_number == 3:
        st.markdown("#### 📘 Why SQL matters for analysts")
        st.markdown(
            """Most organisational data lives in relational databases. SQL lets
you query, filter and aggregate data directly without waiting for
someone else to export it for you.
"""
        )

        st.markdown("#### 🔍 Core SELECT queries")
        st.markdown(
            """You will practise:

- SELECT, WHERE, ORDER BY for filtering and sorting.
- Basic aggregates (COUNT, SUM, AVG, MIN, MAX).
- GROUP BY for grouped summaries.
"""
        )

        st.markdown("#### 🔗 Joins and multi-table queries")
        st.markdown(
            """Real questions usually need data from multiple tables. You will:

- Use INNER JOIN, LEFT JOIN to combine tables.
- Understand keys and relationships.
- Write queries that answer realistic business questions.
"""
        )
    elif unit_number == 4:
        st.markdown("#### 📘 Why BI dashboards?")
        st.markdown(
            """Dashboards let decision-makers see key metrics at a glance and
drill down when needed. This unit focuses on designing dashboards that
are clear, actionable and not cluttered.
"""
        )

        st.markdown("#### 🎨 Dashboard design principles")
        st.markdown(
            """You will learn:

- How to choose the right chart type for each question.
- Layout and filtering strategies.
- Avoiding chart junk and misleading visuals.
"""
        )

        st.markdown("#### 📖 Storytelling with data")
        st.markdown(
            """Numbers alone do not drive action. You will practise writing
short narratives that explain what the data shows and what should happen
next.
"""
        )
    elif unit_number == 5:
        st.markdown("#### 📘 When to use Python as an analyst")
        st.markdown(
            """Python complements spreadsheets and SQL when:

- Datasets are too large for Excel.
- You need to automate repetitive reports.
- Transformations are complex or need version control.
"""
        )

        st.markdown("#### 🐼 Pandas for data wrangling")
        st.markdown(
            """You will use Pandas to:

- Load CSVs and SQL results.
- Clean, filter and reshape data.
- Compute grouped metrics similar to SQL or pivot tables.
"""
        )

        st.markdown("#### 📊 Basic visualisation in Python")
        st.markdown(
            """You will create charts using libraries like Matplotlib, Seaborn
or Plotly, and understand when Python visuals are better than
spreadsheet charts.
"""
        )
    elif unit_number == 6:
        st.markdown("#### 📘 Designing good metrics and KPIs")
        st.markdown(
            """Not all metrics are useful. You will learn to design KPIs that:

- Tie directly to business outcomes.
- Are measurable and actionable.
- Can be tracked over time.
"""
        )

        st.markdown("#### 🧪 A/B testing for analysts")
        st.markdown(
            """You will understand:

- What an A/B test is and when to use it.
- How to interpret conversion rates and statistical significance.
- How to communicate test results to non-technical stakeholders.
"""
        )

        st.markdown("#### 📐 Avoiding common metric pitfalls")
        st.markdown(
            """You will discuss:

- Vanity metrics vs actionable metrics.
- Simpson's paradox and segmentation issues.
- How to critique and improve existing KPI sets.
"""
        )
    elif unit_number == 7:
        st.markdown("#### 📘 Capstone goals")
        st.markdown(
            """The Data Analyst capstone lets you demonstrate end-to-end
ownership of a realistic analysis project, from question to dashboard and
story.
"""
        )

        st.markdown("#### 🧱 Suggested capstone structure")
        st.markdown(
            """A typical structure:

1. Problem & stakeholders (who needs this and why).
2. Data sources and cleaning approach.
3. Analysis and key findings.
4. Dashboard or report.
5. Recommendations and limitations.
"""
        )


def render_data_analyst_pathway_module():
    learner_email = st.session_state.get("user_email", "")

    st.title("📊 Data Analyst Pathway")
    st.success(
        "Become a job-ready data analyst who can work across sectors and countries."
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
                """These labs focus on understanding business questions and
translating them into concrete analysis tasks.

- **Lab 1 – Rewrite vague requests**
  - Take 5–10 example stakeholder questions (e.g. "Why are DNAs high?",
    "Which campaigns are working?").
  - Rewrite each as a clear, measurable question with timeframe and
    metric.

- **Lab 2 – Map questions to data**
  - For each refined question, list which tables/files/fields you would
    need.
  - Identify any data quality risks or gaps.

- **Mini project – Question-to-metric map**
  - Choose one domain (e.g. outpatient clinics, online shop, call
    centre).
  - Create a one-page "question-to-metric" map that a manager could
    sign off.
"""
            )
        elif selected_unit == 2:
            st.markdown(
                """These labs emphasise **hands-on spreadsheet skills**.

- **Lab 1 – Clean a messy sheet**
  - Start from a messy CSV/Excel file (mixed formats, blanks,
    duplicates).
  - Use basic cleaning steps to create a tidy table.

- **Lab 2 – Lookups and joins in Excel/Sheets**
  - Use lookups to join a fact table (e.g. orders) to a dimension table
    (e.g. customers) and compute per-customer metrics.

- **Mini project – Mini KPI dashboard in Excel/Sheets**
  - Build a small dashboard using pivot tables and charts for a chosen
    dataset (e.g. weekly appointments or sales).
  - Add short text explaining 2–3 key insights.
"""
            )
        elif selected_unit == 3:
            st.markdown(
                """These labs focus on **SQL for analysts**.

- **Lab 1 – Core SELECTs**
  - Practise SELECT/WHERE/ORDER BY on a small multi-table schema
    (e.g. orders, customers, products).

- **Lab 2 – Joins and aggregates**
  - Write queries that join tables and compute grouped metrics (e.g.
    revenue per region, DNAs per clinic).

- **Mini project – Weekly metrics query**
  - Design a query or small set of queries that produce a weekly
    performance table for a manager.
"""
            )
        elif selected_unit == 4:
            st.markdown(
                """These labs emphasise **BI dashboards and storytelling**.

- **Lab 1 – Wireframe a dashboard**
  - Sketch the layout for an executive dashboard answering 3–5
    questions.

- **Lab 2 – Build a simple dashboard**
  - In your chosen BI tool or spreadsheets, build a small interactive
    dashboard with filters and 3–4 charts.

- **Mini project – One-page story**
  - Write a short story (slides or report) explaining what the dashboard
    shows and what actions you recommend.
"""
            )
        elif selected_unit == 5:
            st.markdown(
                """These labs bring **Python into the analyst toolkit**.

- **Lab 1 – Recreate a spreadsheet report in Python**
  - Take a simple spreadsheet report and reproduce it using Pandas.

- **Lab 2 – Basic visualisation**
  - Create a few key charts using Matplotlib/Seaborn/Plotly to match or
    improve on spreadsheet visuals.

- **Mini project – Python audit of an existing report**
  - Use Python to double-check numbers from an existing report and
    document any discrepancies.
"""
            )
        elif selected_unit == 6:
            st.markdown(
                """These labs focus on **metrics, KPIs and simple experiments**.

- **Lab 1 – KPI design**
  - For a given process or product, define a small KPI set with clear
    definitions.

- **Lab 2 – A/B test analysis**
  - Analyse a small A/B test dataset (conversion or response rates) and
    interpret the result in plain language.

- **Mini project – Metrics review memo**
  - Write a short memo critiquing an existing set of metrics and
    proposing improvements.
"""
            )
        elif selected_unit == 7:
            st.markdown(
                """Use these milestones to structure your Data Analyst capstone.

- **Milestone 1 – Problem & data**
  - Choose a domain and dataset; clarify the decision-maker and
    questions.

- **Milestone 2 – Analysis & visuals**
  - Build tables/charts answering the key questions.

- **Milestone 3 – Dashboard & story**
  - Create a small dashboard and a short written or slide-based story.
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
                    "text": "What is the primary job of a data analyst?",
                    "options": [
                        "Writing code for production systems",
                        "Turning business questions into data-driven insights",
                        "Configuring servers",
                        "Designing hospital buildings",
                    ],
                    "answer": 1,
                    "explanation": "Analysts translate questions into metrics and insights that support decisions.",
                },
                {
                    "text": "Which of these is a good example of a clear analysis question?",
                    "options": [
                        "Why are we so busy?",
                        "Are outpatient DNAs higher this quarter than last quarter?",
                        "Fix the waiting list",
                        "Improve performance",
                    ],
                    "answer": 1,
                    "explanation": "It is specific, measurable and time-bound.",
                },
                {
                    "text": "What is the difference between a data analyst and a data scientist?",
                    "options": [
                        "They are the same",
                        "Analysts focus on descriptive analytics; scientists build predictive models",
                        "Scientists never use SQL",
                        "Analysts always earn more",
                    ],
                    "answer": 1,
                    "explanation": "Analysts typically focus on reporting and insights; scientists build predictive models.",
                },
                {
                    "text": "Which data source would you use to answer 'How many customers visited last month'?",
                    "options": [
                        "A marketing campaign plan",
                        "Transactional or web analytics data",
                        "An organizational chart",
                        "A budget spreadsheet",
                    ],
                    "answer": 1,
                    "explanation": "Customer visit data comes from transactional systems or web analytics.",
                },
                {
                    "text": "What makes a metric actionable?",
                    "options": [
                        "It is very large",
                        "It is tied to decisions and stakeholders can act on it",
                        "It changes every second",
                        "It is complex",
                    ],
                    "answer": 1,
                    "explanation": "Actionable metrics directly inform decisions and drive specific actions.",
                },
                {
                    "text": "Why is it important to understand stakeholder needs?",
                    "options": [
                        "To make reports longer",
                        "To ensure your analysis answers the right questions",
                        "It is not important",
                        "To avoid doing work",
                    ],
                    "answer": 1,
                    "explanation": "Understanding needs ensures your analysis is relevant and valuable.",
                },
                {
                    "text": "What is a business metric?",
                    "options": [
                        "Any random number",
                        "A quantifiable measure of business performance",
                        "A type of chart",
                        "A database table",
                    ],
                    "answer": 1,
                    "explanation": "Business metrics quantify performance against objectives (e.g., revenue, churn).",
                },
                {
                    "text": "Why map questions to data sources early?",
                    "options": [
                        "To waste time",
                        "To identify data gaps and feasibility before starting analysis",
                        "It is not useful",
                        "To confuse stakeholders",
                    ],
                    "answer": 1,
                    "explanation": "Early mapping reveals whether you have the data needed to answer the question.",
                },
                {
                    "text": "What is the analyst's role in decision-making?",
                    "options": [
                        "To make all decisions",
                        "To provide insights that inform stakeholder decisions",
                        "To avoid stakeholders",
                        "To only create charts",
                    ],
                    "answer": 1,
                    "explanation": "Analysts provide data-driven insights; stakeholders make the final decisions.",
                },
            ],
            2: [
                {
                    "text": "Which function is most suitable for summing values that meet a condition in Excel/Sheets?",
                    "options": ["SUM", "SUMIF/SUMIFS", "COUNT", "AVERAGE"],
                    "answer": 1,
                    "explanation": "SUMIF/SUMIFS let you sum values that meet criteria.",
                },
                {
                    "text": "What is a common use of VLOOKUP or XLOOKUP?",
                    "options": [
                        "Sort a table",
                        "Join information from another table based on a key",
                        "Delete duplicates",
                        "Create a chart",
                    ],
                    "answer": 1,
                    "explanation": "Lookups retrieve related data from another table.",
                },
                {
                    "text": "What is a pivot table used for?",
                    "options": [
                        "Deleting data",
                        "Summarizing and aggregating data by categories",
                        "Encrypting files",
                        "Creating databases",
                    ],
                    "answer": 1,
                    "explanation": "Pivot tables quickly summarize large datasets by grouping and aggregating.",
                },
                {
                    "text": "Which formula would you use to count non-empty cells?",
                    "options": ["SUM", "COUNTA", "AVERAGE", "MAX"],
                    "answer": 1,
                    "explanation": "COUNTA counts cells that contain any type of data.",
                },
                {
                    "text": "What is conditional formatting used for?",
                    "options": [
                        "Deleting rows",
                        "Highlighting cells based on their values",
                        "Creating new sheets",
                        "Printing documents",
                    ],
                    "answer": 1,
                    "explanation": "Conditional formatting visually highlights data based on rules.",
                },
                {
                    "text": "Why clean data before analysis?",
                    "options": [
                        "To make files larger",
                        "To ensure accuracy and reliability of results",
                        "It is not necessary",
                        "To slow down work",
                    ],
                    "answer": 1,
                    "explanation": "Clean data prevents errors and ensures trustworthy analysis.",
                },
                {
                    "text": "What does INDEX/MATCH do?",
                    "options": [
                        "Deletes data",
                        "Performs flexible lookups more powerful than VLOOKUP",
                        "Creates charts",
                        "Sorts tables",
                    ],
                    "answer": 1,
                    "explanation": "INDEX/MATCH offers more flexibility than VLOOKUP for lookups.",
                },
                {
                    "text": "How do you handle duplicate rows?",
                    "options": [
                        "Always keep them",
                        "Investigate and remove if they represent the same record",
                        "Delete every other row",
                        "Ignore them",
                    ],
                    "answer": 1,
                    "explanation": "Duplicates should be investigated and removed if they're genuine repeats.",
                },
                {
                    "text": "What is data validation in spreadsheets?",
                    "options": [
                        "Deleting all data",
                        "Setting rules to control what data can be entered in cells",
                        "Creating charts",
                        "Printing sheets",
                    ],
                    "answer": 1,
                    "explanation": "Data validation prevents incorrect data entry by enforcing rules.",
                },
            ],
            3: [
                {
                    "text": "Which SQL clause is used to combine rows from two tables based on a key?",
                    "options": ["GROUP BY", "JOIN", "ORDER BY", "WHERE"],
                    "answer": 1,
                    "explanation": "JOIN combines rows from different tables using key columns.",
                },
                {
                    "text": "Which query pattern is most suitable for computing revenue per region?",
                    "options": [
                        "SELECT * FROM table",
                        "SELECT region, SUM(revenue) FROM table GROUP BY region",
                        "DELETE FROM table",
                        "UPDATE table",
                    ],
                    "answer": 1,
                    "explanation": "GROUP BY with SUM aggregates revenue per region.",
                },
                {
                    "text": "What does the WHERE clause do?",
                    "options": [
                        "Sorts results",
                        "Filters rows based on conditions",
                        "Joins tables",
                        "Creates tables",
                    ],
                    "answer": 1,
                    "explanation": "WHERE filters rows that meet specified conditions.",
                },
                {
                    "text": "Which aggregate function calculates the average?",
                    "options": ["SUM", "AVG", "COUNT", "MAX"],
                    "answer": 1,
                    "explanation": "AVG calculates the arithmetic mean of a column.",
                },
                {
                    "text": "What is a primary key?",
                    "options": [
                        "A password",
                        "A unique identifier for each row in a table",
                        "A type of chart",
                        "A database name",
                    ],
                    "answer": 1,
                    "explanation": "Primary keys uniquely identify each record in a table.",
                },
                {
                    "text": "What does DISTINCT do in SQL?",
                    "options": [
                        "Sorts results",
                        "Returns only unique values, removing duplicates",
                        "Deletes rows",
                        "Creates indexes",
                    ],
                    "answer": 1,
                    "explanation": "DISTINCT eliminates duplicate rows from query results.",
                },
                {
                    "text": "Which JOIN type keeps all rows from the left table?",
                    "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"],
                    "answer": 1,
                    "explanation": "LEFT JOIN keeps all left table rows, matching or NULL from right.",
                },
                {
                    "text": "What is the ORDER BY clause used for?",
                    "options": [
                        "Filtering rows",
                        "Sorting query results",
                        "Joining tables",
                        "Aggregating data",
                    ],
                    "answer": 1,
                    "explanation": "ORDER BY sorts results in ascending or descending order.",
                },
                {
                    "text": "Why use aliases in SQL?",
                    "options": [
                        "To delete data",
                        "To give tables or columns temporary names for readability",
                        "To encrypt queries",
                        "To slow down queries",
                    ],
                    "answer": 1,
                    "explanation": "Aliases make queries more readable and concise.",
                },
            ],
            4: [
                {
                    "text": "What is the main purpose of a BI dashboard?",
                    "options": [
                        "To store raw data",
                        "To present key metrics and trends in a way decision-makers can act on",
                        "To replace all databases",
                        "To hide information",
                    ],
                    "answer": 1,
                    "explanation": "Dashboards summarise information for quick understanding and action.",
                },
                {
                    "text": "Which is usually better for a top-level KPI chart?",
                    "options": [
                        "A cluttered 3D chart with many colours",
                        "A simple, clearly labelled bar or line chart",
                        "A table with every raw row",
                        "A pie chart with 20 slices",
                    ],
                    "answer": 1,
                    "explanation": "Simple, clear charts support faster understanding.",
                },
                {
                    "text": "What is data storytelling?",
                    "options": [
                        "Making up data",
                        "Presenting data in a narrative that guides audience to insights",
                        "Only using text",
                        "Hiding negative results",
                    ],
                    "answer": 1,
                    "explanation": "Data storytelling combines data, visuals, and narrative effectively.",
                },
                {
                    "text": "Which chart type is best for showing parts of a whole?",
                    "options": ["Line chart", "Pie chart or stacked bar", "Scatter plot", "Histogram"],
                    "answer": 1,
                    "explanation": "Pie charts and stacked bars show proportions of a total.",
                },
                {
                    "text": "What is chart junk?",
                    "options": [
                        "Old charts",
                        "Unnecessary decorations that distract from the message",
                        "Accurate data",
                        "Multiple data series",
                    ],
                    "answer": 1,
                    "explanation": "Chart junk includes clutter like 3D effects that don't add value.",
                },
                {
                    "text": "Why use filters in dashboards?",
                    "options": [
                        "To delete data",
                        "To let users explore data by different dimensions",
                        "To slow down loading",
                        "Filters are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Filters enable interactive exploration of data.",
                },
                {
                    "text": "What makes a dashboard effective?",
                    "options": [
                        "As many charts as possible",
                        "Clear focus on key metrics with actionable insights",
                        "Complex visualizations",
                        "No labels",
                    ],
                    "answer": 1,
                    "explanation": "Effective dashboards focus on key metrics and support decisions.",
                },
                {
                    "text": "When should you use a line chart?",
                    "options": [
                        "For categorical comparisons",
                        "For showing trends over time",
                        "For parts of a whole",
                        "Never",
                    ],
                    "answer": 1,
                    "explanation": "Line charts excel at showing changes over time.",
                },
                {
                    "text": "What is the purpose of dashboard annotations?",
                    "options": [
                        "To make dashboards slower",
                        "To provide context and highlight important events",
                        "To hide data",
                        "Annotations are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Annotations add context like product launches or policy changes.",
                },
            ],
            5: [
                {
                    "text": "In Python/Pandas, which object represents a table of rows and columns?",
                    "options": ["Series", "DataFrame", "List", "Dict"],
                    "answer": 1,
                    "explanation": "A DataFrame is the core table structure for tabular data.",
                },
                {
                    "text": "Which is a good use of Python for analysts?",
                    "options": [
                        "Replacing all SQL and spreadsheets immediately",
                        "Automating repetitive reports and heavier data transforms",
                        "Configuring servers",
                        "Designing hospital buildings",
                    ],
                    "answer": 1,
                    "explanation": "Python is great for automation and more complex analysis.",
                },
                {
                    "text": "What is the pandas library used for?",
                    "options": [
                        "Creating websites",
                        "Data manipulation and analysis",
                        "3D graphics",
                        "Audio processing",
                    ],
                    "answer": 1,
                    "explanation": "Pandas is the primary Python library for data analysis.",
                },
                {
                    "text": "How do you read a CSV file in pandas?",
                    "options": [
                        "pd.open_csv()",
                        "pd.read_csv()",
                        "pd.load_csv()",
                        "pd.import_csv()",
                    ],
                    "answer": 1,
                    "explanation": "pd.read_csv() is the standard method to load CSV files.",
                },
                {
                    "text": "What does df.groupby() do?",
                    "options": [
                        "Deletes rows",
                        "Groups data by specified columns for aggregation",
                        "Sorts data",
                        "Creates new columns",
                    ],
                    "answer": 1,
                    "explanation": "groupby() groups data for aggregations like sum, mean, count.",
                },
                {
                    "text": "Which library is commonly used for visualization in Python?",
                    "options": ["pandas", "matplotlib or seaborn", "numpy", "requests"],
                    "answer": 1,
                    "explanation": "Matplotlib and seaborn are popular for creating charts.",
                },
                {
                    "text": "What is a Jupyter notebook?",
                    "options": [
                        "A physical notebook",
                        "An interactive environment for code, text, and visualizations",
                        "A database",
                        "A spreadsheet",
                    ],
                    "answer": 1,
                    "explanation": "Jupyter notebooks combine code, output, and documentation.",
                },
                {
                    "text": "How do you filter rows in pandas?",
                    "options": [
                        "df.delete()",
                        "df[df['column'] > value]",
                        "df.remove()",
                        "df.filter_all()",
                    ],
                    "answer": 1,
                    "explanation": "Boolean indexing filters rows based on conditions.",
                },
                {
                    "text": "What is the advantage of Python over spreadsheets?",
                    "options": [
                        "Python is always easier",
                        "Python handles larger datasets and enables automation",
                        "Spreadsheets are obsolete",
                        "There is no advantage",
                    ],
                    "answer": 1,
                    "explanation": "Python scales better and automates repetitive tasks.",
                },
            ],
            6: [
                {
                    "text": "Which of the following is a KPI?",
                    "options": [
                        "A random data column",
                        "Monthly conversion rate for a signup funnel",
                        "The file name of a report",
                        "The number of columns in a table",
                    ],
                    "answer": 1,
                    "explanation": "KPIs are metrics linked directly to important outcomes.",
                },
                {
                    "text": "In an A/B test, conversion rate is usually defined as:",
                    "options": [
                        "conversions / total_users",
                        "total_users / conversions",
                        "revenue / conversions",
                        "revenue / total_users",
                    ],
                    "answer": 0,
                    "explanation": "Conversion rate is conversions divided by total users or visits.",
                },
                {
                    "text": "What is a KPI?",
                    "options": [
                        "A type of chart",
                        "A Key Performance Indicator measuring business objectives",
                        "A database query",
                        "A spreadsheet formula",
                    ],
                    "answer": 1,
                    "explanation": "KPIs are metrics that track progress toward business goals.",
                },
                {
                    "text": "What is statistical significance in A/B testing?",
                    "options": [
                        "The size of the difference",
                        "Confidence that the difference is not due to random chance",
                        "The number of users",
                        "The test duration",
                    ],
                    "answer": 1,
                    "explanation": "Significance indicates the result is unlikely to be random.",
                },
                {
                    "text": "Why define success metrics before starting an A/B test?",
                    "options": [
                        "To waste time",
                        "To ensure you measure what matters and avoid bias",
                        "It is not necessary",
                        "To confuse stakeholders",
                    ],
                    "answer": 1,
                    "explanation": "Pre-defining metrics prevents cherry-picking results.",
                },
                {
                    "text": "What is a vanity metric?",
                    "options": [
                        "A useful business metric",
                        "A metric that looks good but doesn't drive decisions",
                        "A KPI",
                        "An accurate measurement",
                    ],
                    "answer": 1,
                    "explanation": "Vanity metrics (like total page views) don't inform actionable decisions.",
                },
                {
                    "text": "How long should you run an A/B test?",
                    "options": [
                        "One hour",
                        "Long enough to reach statistical significance and account for weekly patterns",
                        "Forever",
                        "It doesn't matter",
                    ],
                    "answer": 1,
                    "explanation": "Tests need sufficient data and should cover full business cycles.",
                },
                {
                    "text": "What is segmentation in metrics?",
                    "options": [
                        "Deleting data",
                        "Breaking down metrics by different groups (e.g., region, age)",
                        "Creating charts",
                        "Encrypting data",
                    ],
                    "answer": 1,
                    "explanation": "Segmentation reveals how metrics vary across different groups.",
                },
                {
                    "text": "What is the control group in an A/B test?",
                    "options": [
                        "The group that gets the new version",
                        "The group that gets the current/baseline version",
                        "A random sample",
                        "The largest group",
                    ],
                    "answer": 1,
                    "explanation": "The control group experiences the current version for comparison.",
                },
            ],
            7: [
                {
                    "text": "Which deliverable is most important for your analyst capstone?",
                    "options": [
                        "Only the raw data",
                        "A clear notebook/report + dashboard + README explaining the project",
                        "A screenshot of your IDE",
                        "Only a list of formulas",
                    ],
                    "answer": 1,
                    "explanation": "Employers want to see a complete, documented project they can understand.",
                },
                {
                    "text": "Why should you state limitations in your capstone report?",
                    "options": [
                        "To make the report longer",
                        "To show honest judgement about where the analysis is strong or weak",
                        "To hide problems",
                        "It is not useful",
                    ],
                    "answer": 1,
                    "explanation": "Being transparent about limits builds trust and shows maturity.",
                },
                {
                    "text": "What should a capstone README include?",
                    "options": [
                        "Only your name",
                        "Problem, data, methods, results, and how to reproduce",
                        "Random notes",
                        "Nothing",
                    ],
                    "answer": 1,
                    "explanation": "A good README tells the complete story and enables reproduction.",
                },
                {
                    "text": "Why create a portfolio of analyst projects?",
                    "options": [
                        "To waste time",
                        "To demonstrate skills to potential employers",
                        "Portfolios are not useful",
                        "To hide your work",
                    ],
                    "answer": 1,
                    "explanation": "Portfolios showcase your practical skills and problem-solving ability.",
                },
                {
                    "text": "What makes a dataset suitable for a capstone?",
                    "options": [
                        "It has only 5 rows",
                        "It is realistic, documented, and relevant to business problems",
                        "It has no challenges",
                        "It is completely random",
                    ],
                    "answer": 1,
                    "explanation": "Good capstone datasets are realistic and allow you to demonstrate skills.",
                },
                {
                    "text": "How should you present findings to non-technical stakeholders?",
                    "options": [
                        "Use maximum technical jargon",
                        "Use plain language with clear visuals and actionable insights",
                        "Only show code",
                        "Avoid explanations",
                    ],
                    "answer": 1,
                    "explanation": "Non-technical audiences need clear, jargon-free explanations.",
                },
                {
                    "text": "What is the purpose of an analyst capstone?",
                    "options": [
                        "To memorize formulas",
                        "To demonstrate end-to-end analysis skills on a realistic problem",
                        "To avoid learning",
                        "To pass time",
                    ],
                    "answer": 1,
                    "explanation": "Capstones showcase your ability to tackle real problems independently.",
                },
                {
                    "text": "Which is more valuable: breadth or depth in a capstone?",
                    "options": [
                        "Breadth - cover everything superficially",
                        "Depth - do one problem well with rigorous methods",
                        "Neither matters",
                        "Only breadth",
                    ],
                    "answer": 1,
                    "explanation": "Employers value depth and rigor over superficial coverage.",
                },
                {
                    "text": "Where should you host your analyst portfolio?",
                    "options": [
                        "Keep it only on your laptop",
                        "GitHub with clear READMEs and documentation",
                        "Never share it",
                        "Only on paper",
                    ],
                    "answer": 1,
                    "explanation": "GitHub makes your work accessible and demonstrates technical proficiency.",
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
                study_plan_md = """# Data Analyst Pathway – 8–10 Week Study Plan

Suggested week-by-week guide covering Units 1–7 with reading, labs and
portfolio milestones.

---

## Week 1 – Unit 1: Data & Business Questions for Analysts

- Explore analyst role examples across sectors.
- Practise rewriting vague stakeholder questions into clear, measurable
  questions.
- Map questions to potential data sources.

## Week 2 – Unit 2: Spreadsheet Skills for Analysis

- Clean a messy spreadsheet into a tidy table.
- Practise key formulas and lookups.
- Build a small KPI mini-dashboard.

## Weeks 3–4 – Unit 3: SQL for Data Analysts

- Learn core SELECT/WHERE/ORDER BY queries.
- Join tables to answer realistic questions.
- Create a simple "weekly metrics" SQL script.

## Week 5 – Unit 4: BI Dashboards & Storytelling

- Design a small interactive dashboard.
- Write short narratives for each key chart.

## Week 6 – Unit 5: Python for Analysts

- Recreate one report from spreadsheets/SQL using Python + Pandas.
- Practise basic plotting.

## Week 7 – Unit 6: Metrics, A/B Tests & KPI Design

- Define KPIs for a chosen service/product.
- Analyse a small A/B test and interpret results.

## Weeks 8–10 – Unit 7: Data Analyst Capstone Project

- Choose a realistic dataset and problem.
- Complete an end-to-end analysis and dashboard.
- Prepare a report/slide deck and portfolio artifacts.
"""
                pdf = create_unit_pdf(0, "Data Analyst Study Plan", study_plan_md)
                st.download_button(
                    label="Download Study Plan PDF",
                    data=pdf,
                    file_name="Data_Analyst_Pathway_Study_Plan.pdf",
                    mime="application/pdf",
                    key="da_study_plan_pdf_dl",
                )

        with col_b:
            if st.button("📥 Unit checklists PDF", key="da_checklists_pdf"):
                checklists_md = """# Data Analyst Pathway – Unit Checklists

Use these checklists to track your progress. They are guidance, not
formal assessment criteria.

---

## Unit 1 – Data & Business Questions for Analysts

- [ ] I can describe what a data analyst does in plain language.
- [ ] I can turn vague stakeholder requests into clear questions.
- [ ] I can map questions to likely data sources.

## Unit 2 – Spreadsheet Skills for Analysis

- [ ] I can clean a messy sheet into a tidy table.
- [ ] I can use SUMIFS/COUNTIFS and lookups for common tasks.
- [ ] I can build a small dashboard using pivots/charts.

## Unit 3 – SQL for Data Analysts

- [ ] I can write SELECT/WHERE/ORDER BY queries.
- [ ] I can join tables and compute grouped metrics.
\n+## Unit 4 – BI Dashboards & Storytelling

- [ ] I can design a dashboard layout that answers specific questions.
- [ ] I can write short narratives to go with key visuals.

## Unit 5 – Python for Analysts

- [ ] I can load data into Pandas and perform basic cleaning.
- [ ] I can recreate simple reports in Python.

## Unit 6 – Metrics, A/B Tests & KPI Design

- [ ] I can define sensible KPIs for a process or product.
- [ ] I can interpret a simple A/B test and communicate results.

## Unit 7 – Data Analyst Capstone Project

- [ ] I have completed an end-to-end analysis suitable for my portfolio.
- [ ] I have a notebook/script, dashboard and written summary.
"""
                pdf = create_unit_pdf(0, "Data Analyst Unit Checklists", checklists_md)
                st.download_button(
                    label="Download Checklists PDF",
                    data=pdf,
                    file_name="Data_Analyst_Pathway_Unit_Checklists.pdf",
                    mime="application/pdf",
                    key="da_checklists_pdf_dl",
                )

        with col_c:
            if st.button("📥 Portfolio guide PDF", key="da_portfolio_pdf"):
                portfolio_md = """# Data Analyst Pathway – Portfolio Guide

This guide helps you turn labs and the capstone into a job-ready
portfolio.

## 1. Core artefacts to include

- Selected lab notebooks/reports showcasing spreadsheets, SQL, BI and
  Python.
- A strong capstone project with README and clear structure.

## 2. Suggested GitHub structure

- `analyst_capstone/` with notebooks/data/README.
- `unit_labs/` grouped by topic (spreadsheets, SQL, BI, Python).

## 3. Writing good READMEs and case studies

- Problem, data, methods, key insights, limitations.

## 4. Linking portfolio to CV and LinkedIn

- Add a "Projects" section with links and short summaries.
"""
                pdf = create_unit_pdf(0, "Data Analyst Portfolio Guide", portfolio_md)
                st.download_button(
                    label="Download Portfolio Guide PDF",
                    data=pdf,
                    file_name="Data_Analyst_Pathway_Portfolio_Guide.pdf",
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
