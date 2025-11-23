"""
Data Science Foundations (Pathway 1)
Global, sector-agnostic beginner-to-junior data science programme.

This module follows the same overall structure as the TQUK modules:
- Course overview
- Learning materials
- Labs & projects
- Assessments
- Evidence tracking
- Documents
- Progress
- Certificate

NOTE: This file is designed to integrate with existing T21 infrastructure
(tquk_course_assignment, tquk_evidence_tracking, tquk_pdf_converter) but
is NOT a TQUK qualification. It is a professional pathway course.
"""

import streamlit as st
from typing import Dict, Any

try:
    from tquk_course_assignment import get_learner_enrollments, update_learner_progress
except Exception:
    def get_learner_enrollments(email: str):
        return []

    def update_learner_progress(email: str, course_id: str, progress: int, units_completed: int):
        return None

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
    # Global video library helper (used to show per-unit recordings)
    from video_library import get_all_videos
except Exception:
    def get_all_videos(category: str = None, week: int = None, competency: str = None):
        return []


COURSE_ID = "data_science_foundations_pathway_1"
COURSE_NAME = "Data Science Foundations (Pathway 1)"


# Core unit definitions. These are intentionally global and sector-agnostic.
UNITS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Introduction to Data & the Role of the Data Scientist",
        "credits": 2,
        "glh": 12,
        "level": "Beginner",
        "file": None,
        "theory_topics": [
            "What is data science?",
            "Data roles: analyst, scientist, engineer, ML engineer",
            "Data lifecycle & CRISP-DM",
            "Ethics, privacy, bias, and responsible AI",
        ],
        "practicals": [
            "Explore multiple public datasets and identify basic patterns",
            "Formulate business questions for different sectors (retail, finance, healthcare, logistics)",
        ],
    },
    2: {
        "name": "Python Programming for Data",
        "credits": 3,
        "glh": 18,
        "level": "Beginner",
        "file": None,
        "theory_topics": [
            "Python syntax and data types",
            "Control flow, functions, modules",
            "Working in notebooks and VS Code",
            "Best practices: readable, reusable code",
        ],
        "practicals": [
            "Write scripts to load and summarise CSV files",
            "Build small reusable helper functions for data cleaning",
        ],
    },
    3: {
        "name": "Working with Data using Pandas & NumPy",
        "credits": 4,
        "glh": 24,
        "level": "Beginner/Intermediate",
        "file": None,
        "theory_topics": [
            "Series, DataFrames, indexes",
            "Filtering, joining, grouping, aggregation",
            "Handling missing values and outliers",
            "Vectorisation and performance basics",
        ],
        "practicals": [
            "Clean and join multiple datasets (sales, marketing, operations)",
            "Create a reusable data cleaning notebook template",
        ],
    },
    4: {
        "name": "SQL & Relational Databases for Analysis",
        "credits": 3,
        "glh": 18,
        "level": "Beginner/Intermediate",
        "file": None,
        "theory_topics": [
            "Relational model and schemas",
            "SELECT, WHERE, ORDER BY",
            "JOINs, GROUP BY, HAVING",
            "Intro to window functions",
        ],
        "practicals": [
            "Query a multi-table schema (orders, customers, products)",
            "Design queries to answer common business questions",
        ],
    },
    5: {
        "name": "Statistics & Probability for Data Science",
        "credits": 4,
        "glh": 24,
        "level": "Intermediate",
        "file": None,
        "theory_topics": [
            "Distributions and summary statistics",
            "Correlation vs causation",
            "Sampling, confidence intervals",
            "Hypothesis testing & A/B testing basics",
        ],
        "practicals": [
            "Run a simple A/B test analysis in Python",
            "Analyse correlations in a real dataset and discuss limitations",
        ],
    },
    6: {
        "name": "Data Visualisation & Storytelling",
        "credits": 3,
        "glh": 18,
        "level": "Intermediate",
        "file": None,
        "theory_topics": [
            "Chart types and when to use them",
            "Design principles and avoiding misleading charts",
            "Storytelling with data and audience focus",
        ],
        "practicals": [
            "Build a set of key charts for a chosen dataset",
            "Write a short narrative explaining insights to a non-technical audience",
        ],
    },
    7: {
        "name": "Foundations Capstone Project",
        "credits": 6,
        "glh": 36,
        "level": "Intermediate",
        "file": None,
        "theory_topics": [
            "End-to-end project structure",
            "Problem framing and success criteria",
            "Documentation and communication",
        ],
        "practicals": [
            "Choose a dataset in any sector and complete an end-to-end analysis",
            "Deliver a notebook, visual report, and short written summary that could go into a portfolio",
        ],
    },
}


def _get_enrollment(email: str):
    """Helper to fetch a learner's enrollment record for this course."""
    enrollments = get_learner_enrollments(email)
    for e in enrollments:
        if e.get("course_id") == COURSE_ID:
            return e
    return None


def _render_progress_header(enrollment):
    """Show top-of-page progress metrics if enrollment data exists."""
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


def _render_unit_content(unit_number: int, unit: Dict[str, Any]):
    """Shared renderer for unit details in materials/labs tabs."""
    st.markdown(f"### Unit {unit_number}: {unit['name']}")
    st.caption(
        f"Level: {unit['level']} • Suggested hours: {unit['glh']} • Suggested credits: {unit['credits']}"
    )

    st.markdown("#### 📘 Core Theory Topics")
    for topic in unit.get("theory_topics", []):
        st.write(f"- {topic}")

    st.markdown("#### 🧪 Practical Labs / Exercises")
    for task in unit.get("practicals", []):
        st.write(f"- {task}")

    # Extra detailed reading content for units so learners can read like a chapter
    if unit_number == 1:
        st.markdown("---")
        st.markdown("#### 📚 What is data science?")
        st.markdown(
            """Data science is about using **data + statistics + computing** to answer
            real-world questions and help people make better decisions.

Think of it as a **bridge** between raw data and useful action. A data scientist:

- Collects and organises data from different places (files, databases, APIs)
- Cleans it so it is accurate and reliable
- Explores it to find patterns and problems
- Builds models to **predict** or **classify** things
- Explains the results in simple language so managers can act on it

You can use data science in **any sector**: healthcare, finance, marketing,
e‑commerce, government, education, logistics, energy, sports and many more.
The tools and ways of thinking stay the same – only the data and business
questions change.
"""
        )

        st.markdown("#### 🧑‍💻 Key data roles")
        st.markdown(
            """In a modern team there are usually several different roles:

- **Data Analyst** – focuses on reporting and insight.
  - Cleans data, builds dashboards and reports.
  - Answers questions like *“Which campaign worked best?”* or
    *“Where are we losing customers?”*

- **Data Scientist** – focuses on experiments and prediction.
  - Builds models to predict the future or classify things.
  - Answers questions like *“Who is likely to churn?”* or
    *“What will demand look like next month?”*

- **Data Engineer** – focuses on data pipelines and infrastructure.
  - Moves data from source systems into clean, reliable tables.
  - Builds the foundations that analysts and scientists rely on.

- **Machine Learning Engineer** – focuses on deploying models.
  - Takes models and turns them into services and products.
  - Makes sure they are fast, reliable and can be monitored in production.

In a small company, one person may do several of these jobs. In a bigger
organisation, each role is usually separate.
"""
        )

        st.markdown("#### 🔁 Data lifecycle & CRISP‑DM")
        st.markdown(
            """Most serious projects follow a structured lifecycle so that work is
traceable and repeatable. One common framework is **CRISP‑DM**:

1. **Business Understanding** – What problem are we trying to solve?
2. **Data Understanding** – What data do we have? What is missing?
3. **Data Preparation** – Clean, join and transform the data.
4. **Modelling** – Build and compare different models.
5. **Evaluation** – Check if the model really solves the business problem.
6. **Deployment** – Put the model or analysis into real use.

You will use this pattern again and again, whatever country or sector you
work in. This course will train you to think in this structured way from the
very beginning.
"""
        )

        st.markdown("#### ⚖️ Ethics, privacy, bias & responsible AI")
        st.markdown(
            """Working with data is powerful, so it must be done **responsibly**:

- **Privacy** – respect laws and local rules (for example GDPR in Europe).
  Only collect the data you really need and protect it properly.

- **Bias** – data often reflects unfair patterns from the real world.
  If we are not careful, models can repeat or even amplify that unfairness.

- **Transparency** – people should understand, at least in simple language,
  how decisions that affect them are being made.

- **Accountability** – humans stay responsible for important decisions,
  especially in areas like healthcare, justice, employment, finance and
  immigration.

As a data professional you are not just a technician. You are also a
guardian of how data and AI are used. This mindset will give you a strong,
trusted profile in any global job market.
"""
        )

    elif unit_number == 2:
        st.markdown("---")
        st.markdown("#### 🐍 Why Python is the main language for data science")
        st.markdown(
            """Python is the main language used in modern data science teams because it is:

- **Easy to read** – the syntax is close to English.
- **Widely used worldwide** – many tutorials, examples and jobs.
- **Rich in libraries** – Pandas, NumPy, scikit-learn, Plotly and more.

For most junior roles you do not need to be a computer science expert. You
need **solid, reliable Python** that lets you load data, clean it and
answer questions.
"""
        )

        st.markdown("#### 🧱 Core building blocks: types, lists and dictionaries")
        st.markdown(
            """In almost every data script you write you will use:

- **Numbers and strings** – for quantities and labels.
- **Lists** – ordered collections such as monthly revenues.
- **Dictionaries** – key–value pairs such as `customer_id -> country`.

Understanding these types makes it much easier to control how data flows
through your code and into tools like Pandas and SQL.
"""
        )

        st.markdown("#### 🔁 Control flow, loops and functions")
        st.markdown(
            """Control flow lets your code make decisions instead of running the
same steps for every situation:

- `if` / `elif` / `else` to branch based on conditions.
- `for` loops to repeat actions over a list of items.
- **Functions** to group logic into reusable blocks with names and
  parameters.

Good functions make data projects easier to test, debug and reuse when you
move from one sector or country to another.
"""
        )

        st.markdown("#### 🧪 Working in notebooks and scripts")
        st.markdown(
            """In real teams you will often:

- Explore ideas quickly in **notebooks** (Jupyter, VS Code, Colab).
- Turn successful code into **scripts** (`.py` files) that can be run on a
  schedule or shared with colleagues.

This unit trains you to be comfortable in both worlds so that you can move
from experiment to small production-style code when needed.
"""
        )

        st.markdown("#### ✅ Professional habits from day one")
        st.markdown(
            """Employers in the UK, US and globally look for entry-level people who:

- Use clear, descriptive variable and function names.
- Keep notebooks tidy and remove unused code.
- Add short comments only where needed to explain intent.

These habits make your work easier to read in interviews and in real teams,
and they carry through into Pathway 2 and 3.
"""
        )

    elif unit_number == 3:
        st.markdown("---")
        st.markdown("#### 📊 Why Pandas & NumPy matter")
        st.markdown(
            """Pure Python lists and loops are too slow and awkward for serious data
work. **NumPy** gives you fast numerical arrays and **Pandas** adds
labelled tables (DataFrames) on top of that.

Together they let you:

- Load CSV/Excel/SQL data quickly.
- Filter and transform millions of rows.
- Group and summarise results for business questions.
"""
        )

        st.markdown("#### 🧮 Thinking in columns, not row-by-row loops")
        st.markdown(
            """In Pandas you usually avoid writing `for` loops over rows. Instead you:

- Express operations on **whole columns** at once (vectorisation).
- Use `groupby` and aggregations for business metrics.
- Apply functions only when needed.

This style is faster and creates shorter, clearer code that colleagues can
read more easily.
"""
        )

        st.markdown("#### 🧹 Handling messy real-world data")
        st.markdown(
            """Real data from hospitals, retailers, banks or government systems is
rarely clean. You will see missing values, duplicates and inconsistent
formats.

This unit trains you to use tools such as `.isna()`, `.fillna()`,
`.drop_duplicates()`, string methods and joins so that you can turn messy
inputs into reliable tables ready for analysis or modelling.
"""
        )

        st.markdown("#### 🧱 Reusable cleaning pipelines")
        st.markdown(
            """A powerful habit is to treat cleaning as a **repeatable pipeline**:

1. Load raw data.
2. Apply a standard sequence of cleaning steps.
3. Save a clean version for other notebooks, dashboards or team members.

Employers value people who can build these pipelines because it shows you
can handle **real, messy datasets**, not just perfect classroom examples.
"""
        )

    elif unit_number == 4:
        st.markdown("---")
        st.markdown("#### 🗄️ Why SQL is still critical")
        st.markdown(
            """Most serious organisations store their key data in **relational
databases**. Even if you love Python, you will often need SQL to:

- Pull data from production systems into Pandas.
- Build tables that BI tools (like Power BI or Tableau) can read.
- Answer ad-hoc questions directly in a database.
"""
        )

        st.markdown("#### 🧱 Core SQL skills for data roles")
        st.markdown(
            """For junior analyst and scientist roles, you should be confident with:

- `SELECT`, `FROM`, `WHERE` – choosing columns and filtering rows.
- `ORDER BY` – sorting results.
- `JOIN` – combining tables on keys.
- `GROUP BY` and aggregates such as `SUM`, `COUNT`, `AVG`.

These are exactly the topics that appear in many SQL interview tests across
the UK, US and globally.
"""
        )

        st.markdown("#### 🧠 Thinking in tables and keys")
        st.markdown(
            """Good SQL comes from understanding the **data model**:

- What does one row represent in each table (the grain)?
- Which columns are primary keys and which are foreign keys?
- Are relationships one-to-many or many-to-many?

Once this is clear, writing joins and aggregates without double-counting
becomes much easier.
"""
        )

    elif unit_number == 5:
        st.markdown("---")
        st.markdown("#### 📈 Why statistics matters for data science")
        st.markdown(
            """Statistics is the language of **uncertainty**. Even when you build
machine learning models you still rely on basic statistical ideas to

- Understand distributions and variability.
- Judge whether differences are real or just noise.
- Communicate results honestly to stakeholders.
"""
        )

        st.markdown("#### 🔍 Distributions, summaries and relationships")
        st.markdown(
            """In this unit you work with:

- Measures of centre (mean, median) and spread (variance, IQR).
- Common distribution shapes (normal, skewed, heavy-tailed).
- **Correlation** to see how two variables move together.

You will use these ideas in almost every serious project, whatever
country or sector you work in.
"""
        )

        st.markdown("#### 🧪 A/B testing and confidence")
        st.markdown(
            """A/B tests are everywhere: websites, apps, email campaigns, call
centres. This unit introduces conversion rate, lift and p-values so you
can judge whether a variant really performs better than control or if the
observed difference might just be random noise.
"""
        )

    elif unit_number == 6:
        st.markdown("---")
        st.markdown("#### 📊 Telling clear stories with charts")
        st.markdown(
            """Many decision-makers will only ever see your **charts and written
summary**, not your code. Clear visualisation turns analysis into
actionable insight.

You learn how to pick chart types that match the question:

- Bar charts for comparing categories.
- Line charts for trends over time.
- Scatter plots for relationships between two numeric variables.
"""
        )

        st.markdown("#### 🎨 Design principles and avoiding misleading charts")
        st.markdown(
            """Good charts remove clutter and focus attention on the main message.
This unit covers topics such as:

- Labelling axes and units clearly.
- Avoiding unnecessary 3D effects and heavy backgrounds.
- Choosing sensible scales so differences are not exaggerated.
"""
        )

        st.markdown("#### 🗣️ Writing the narrative")
        st.markdown(
            """Each important visual should come with a short narrative answering:

1. What does this chart show?
2. Why does it matter for the business or organisation?
3. What action or next step should we consider?

Being able to write this clearly is one of the strongest skills you can
develop as an early-career data professional.
"""
        )

    elif unit_number == 7:
        st.markdown("---")
        st.markdown("#### 🧱 What makes a strong capstone project")
        st.markdown(
            """Your capstone is often the first thing recruiters or hiring managers
look at in your portfolio. A strong project usually has:

- A clear problem statement in plain language.
- A realistic dataset in a recognisable sector.
- A transparent cleaning and analysis process.
- Charts and tables that support the key message.
- A concise written summary.
"""
        )

        st.markdown("#### 🧭 Suggested project flow")
        st.markdown(
            """You can structure your project as:

1. Choose a sector and dataset (e.g. retail, healthcare, finance,
   logistics, public sector).
2. Define clear questions and success criteria.
3. Clean and explore the data.
4. Answer the questions with tables, charts and, if appropriate,
   simple models.
5. Write up conclusions and recommendations.
"""
        )

        st.markdown("#### 🚀 Using the capstone in your career")
        st.markdown(
            """Once finished, your capstone can be uploaded to GitHub, linked on
your CV and mentioned in interviews as evidence that you can take a
realistic problem from start to finish.
"""
        )


def render_data_science_foundations_module():
    """Main entry point for the Data Science Foundations (Pathway 1) module."""

    learner_email = st.session_state.get("user_email", "")

    st.title("📊 Data Science Foundations (Pathway 1)")
    st.success(
        "Build a rock-solid foundation in data science with global, sector-agnostic skills.\n\n"
        "Designed so learners can work in any country and any industry after completion."
    )

    # Very lightweight role/enrollment check (not as strict as TQUK quals)
    user_role = st.session_state.get("user_role", st.session_state.get("user_type", "student"))
    if learner_email and "admin@t21services" in learner_email.lower():
        user_role = "super_admin"

    admin_roles = [
        "super_admin",
        "admin",
        "teacher",
        "tester",
        "staff",
        "instructor",
        "trainer",
    ]

    enrollment = _get_enrollment(learner_email) if learner_email else None
    is_enrolled = enrollment is not None

    if not is_enrolled and user_role not in admin_roles:
        st.warning("You are not formally enrolled on this pathway yet.")
        st.info("Ask your tutor or training provider to enroll you on Data Science Foundations.")
    elif not is_enrolled and user_role in admin_roles:
        st.info("Admin/Staff view: full preview access. Students must be enrolled to track progress.")

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
        st.success(
            "This pathway takes a complete beginner to a strong junior-level data analyst/"
            "scientist with globally transferable skills."
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """### 🎯 By the end of this pathway you will be able to:

- Work confidently with Python for data tasks
- Clean, join and analyse datasets using Pandas & NumPy
- Query relational databases using SQL
- Apply core statistics for data decisions
- Build clear visual reports and tell data stories
- Complete an end-to-end data project suitable for your portfolio
"""
            )
        with col2:
            st.markdown(
                """### 🧰 Tools & technologies used:

- Python 3 (notebooks + scripts)
- Pandas, NumPy, Matplotlib/Seaborn/Plotly
- SQL (any standards-compliant engine)
- Jupyter / VS Code (or similar)
- Git/GitHub (recommended for portfolio)
"""
            )

        st.markdown("---")
        st.markdown("### 📦 Units in this pathway")
        for unit_number, unit in UNITS.items():
            with st.expander(f"Unit {unit_number}: {unit['name']}"):
                _render_unit_content(unit_number, unit)

    # Learning materials
    with tabs[1]:
        st.subheader("📖 Learning Materials")
        st.info(
            "Use this tab as the main reading and concept reference for each unit."
        )

        selected_unit = st.selectbox(
            "Select a unit:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_foundations_materials_unit",
        )

        unit = UNITS[selected_unit]
        _render_unit_content(selected_unit, unit)

        st.markdown("---")
        if st.button("📥 Download theory summary as PDF", key="download_ds_foundations_unit_pdf"):
            content_lines = ["# " + unit["name"], "", "## Core Theory Topics"]
            for topic in unit.get("theory_topics", []):
                content_lines.append(f"- {topic}")
            content_lines.append("")
            content_lines.append("## Practical Focus")
            for task in unit.get("practicals", []):
                content_lines.append(f"- {task}")

            markdown_content = "\n".join(content_lines)
            pdf_buffer = create_unit_pdf(
                selected_unit,
                unit["name"],
                markdown_content,
            )
            st.download_button(
                label="📥 Download Unit Summary PDF",
                data=pdf_buffer,
                file_name=f"Data_Science_Foundations_Unit_{selected_unit}.pdf",
                mime="application/pdf",
            )

        st.markdown("---")
        st.markdown("### 📺 Session recordings for this unit")
        st.caption(
            "Videos added in the global Video Library for this week/unit will appear here. "
            "Tutors can upload or link Vimeo/Zoom/YouTube recordings from the main Video Library tool."
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

                    # Prefer embedded Vimeo player if we have an ID
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
                        st.warning("Video link not available. Please check the Video Library entry.")

    # Labs & mini projects
    with tabs[2]:
        st.subheader("🧪 Labs & Mini Projects")
        st.success(
            "Every unit includes suggested labs and mini projects. Tutors can adapt these "
            "to local datasets and sectors (UK, Europe, US, Africa, Asia, etc.)."
        )

        selected_unit = st.selectbox(
            "Choose a unit to view lab ideas:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_foundations_labs_unit",
        )
        unit = UNITS[selected_unit]

        _render_unit_content(selected_unit, unit)

        # Suggest the corresponding notebook for hands-on work, where available.
        notebook_map = {
            1: "U1_intro_exploration.ipynb",
            2: "U2_python_basics.ipynb",
            3: "U3_pandas_cleaning_uk_retail.ipynb",
            4: "U4_sql_queries_foundations_db.ipynb",
            5: "U5_ab_testing_web.ipynb",
            6: "U6_basic_charts.ipynb",
            7: "U7_capstone_template.ipynb",
        }

        nb_name = notebook_map.get(selected_unit)
        if nb_name:
            st.info(
                f"For hands-on practice, use the notebook `{nb_name}` in the "
                "`data_science_pathway1/notebooks` folder as a starting point."
            )

        st.markdown("---")
        st.markdown("### 🧪 Suggested lab structure")
        st.markdown(
            """1. **Setup** – load data, inspect columns, understand the question.
2. **Transform** – clean data, create any required features.
3. **Analyse** – compute metrics or build simple models.
4. **Visualise** – build charts that answer the question.
5. **Communicate** – write a short summary for a non-technical audience.
"""
        )

        st.info(
            "Tutors can attach specific example notebooks and datasets using the main LMS "
            "learning materials system or local teaching resources."
        )

    # Assessments
    with tabs[3]:
        st.subheader("📝 Assessments")
        st.info(
            "Use this tab to submit evidence for each unit (labs, mini projects, capstone)."
        )

        if not learner_email:
            st.warning("Log in as a learner to submit assessments.")
        else:
            selected_unit = st.selectbox(
                "Select unit for assessment submission:",
                options=list(UNITS.keys()),
                format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
                key="ds_foundations_assessment_unit",
            )
            render_evidence_submission_form(learner_email, COURSE_ID, selected_unit)

        st.markdown("---")
        st.markdown("### ✅ Quick-check quizzes (Units 1–7)")
        st.caption(
            "Answer a short multiple-choice quiz for the selected unit directly in the app. "
            "Tutors can still use the full markdown quizzes and final exam for formal "
            "assessment and evidence."
        )

        quiz_bank = {
            1: [
                {
                    "text": "Which option best describes data science?",
                    "options": [
                        "Designing websites only",
                        "Using data, statistics and computing to answer real questions",
                        "Fixing network hardware",
                        "Writing reports without data",
                    ],
                    "answer": 1,
                    "explanation": "Data science combines data, statistics and computing to answer real questions and support decisions.",
                },
                {
                    "text": "Which CRISP-DM phase comes first?",
                    "options": [
                        "Modelling",
                        "Business Understanding",
                        "Deployment",
                        "Data Preparation",
                    ],
                    "answer": 1,
                    "explanation": "You always start with Business Understanding – being clear on the problem before touching data.",
                },
                {
                    "text": "Which role mainly focuses on deploying models into production systems?",
                    "options": [
                        "Data Analyst",
                        "Data Engineer",
                        "Machine Learning Engineer",
                        "Database Administrator",
                    ],
                    "answer": 2,
                    "explanation": "Machine Learning Engineers take models and turn them into reliable services and products.",
                },
                {
                    "text": "Which of the following is an example of data ethics?",
                    "options": [
                        "Collecting as much data as possible without telling users",
                        "Only collecting data that is needed and protecting it properly",
                        "Selling user data to anyone who pays",
                        "Ignoring local privacy laws if the model is accurate",
                    ],
                    "answer": 1,
                    "explanation": "Good data ethics means collecting only what you need and protecting it in line with laws like GDPR.",
                },
                {
                    "text": "In CRISP-DM, which phase checks whether the model really solves the business problem?",
                    "options": ["Data Preparation", "Evaluation", "Deployment", "Data Understanding"],
                    "answer": 1,
                    "explanation": "Evaluation checks performance against the business goals before deployment.",
                },
                {
                    "text": "Which of the following is an example of algorithmic bias?",
                    "options": [
                        "A model that performs equally well for all demographic groups",
                        "A model that systematically underperforms for certain demographic groups",
                        "A model with high accuracy",
                        "A model trained on balanced data",
                    ],
                    "answer": 1,
                    "explanation": "Algorithmic bias occurs when a model systematically treats certain groups unfairly, often due to biased training data.",
                },
                {
                    "text": "What is the difference between a Data Analyst and a Data Scientist?",
                    "options": [
                        "They are exactly the same role",
                        "Analysts focus on reporting and dashboards; Scientists build predictive models",
                        "Scientists never use SQL",
                        "Analysts always earn more",
                    ],
                    "answer": 1,
                    "explanation": "Data Analysts typically focus on descriptive analytics and reporting, while Data Scientists build predictive and prescriptive models.",
                },
                {
                    "text": "Which law requires organizations in the EU to protect personal data?",
                    "options": ["HIPAA", "GDPR", "SOX", "FERPA"],
                    "answer": 1,
                    "explanation": "GDPR (General Data Protection Regulation) is the EU law governing data privacy and protection.",
                },
                {
                    "text": "In the data lifecycle, which comes first?",
                    "options": ["Data Collection", "Problem Definition", "Model Deployment", "Data Cleaning"],
                    "answer": 1,
                    "explanation": "You must define the problem and understand business needs before collecting or analyzing data.",
                },
                {
                    "text": "Which is a key principle of responsible AI?",
                    "options": [
                        "Maximize profit at any cost",
                        "Ensure fairness, transparency, and accountability",
                        "Hide model decisions from users",
                        "Ignore ethical considerations if accuracy is high",
                    ],
                    "answer": 1,
                    "explanation": "Responsible AI emphasizes fairness, transparency, accountability, and consideration of societal impact.",
                },
            ],
            2: [
                {
                    "text": "Which keyword is used to define a function in Python?",
                    "options": ["func", "def", "define", "lambda"],
                    "answer": 1,
                    "explanation": "Python functions are defined with the def keyword, for example: def my_function(): ...",
                },
                {
                    "text": "Which structure is best for key–value pairs such as customer_id -> country?",
                    "options": ["list", "tuple", "dict", "set"],
                    "answer": 2,
                    "explanation": "A dict stores key–value mappings efficiently, e.g. {customer_id: country}.",
                },
                {
                    "text": "What is the result of len([1, 2, 3, 4])?",
                    "options": ["3", "4", "5", "Error"],
                    "answer": 1,
                    "explanation": "The list has four elements, so len(...) returns 4.",
                },
                {
                    "text": "Which control structure lets you run some code only when a condition is true?",
                    "options": ["for loop", "while loop", "if statement", "function"],
                    "answer": 2,
                    "explanation": "An if statement chooses whether to run a block of code based on a condition.",
                },
                {
                    "text": "In a notebook, which is generally better practice?",
                    "options": [
                        "Keep all experiments, even broken ones, in the final version",
                        "Remove dead code and keep the notebook tidy and readable",
                        "Never use comments",
                        "Use one very long cell for the whole project",
                    ],
                    "answer": 1,
                    "explanation": "A clean, readable notebook with dead code removed is easier for others (and you) to understand.",
                },
                {
                    "text": "What does the following code do? x = [i**2 for i in range(5)]",
                    "options": [
                        "Creates a list of numbers 0 to 4",
                        "Creates a list of squares: [0, 1, 4, 9, 16]",
                        "Raises an error",
                        "Creates a dictionary",
                    ],
                    "answer": 1,
                    "explanation": "This is a list comprehension that squares each number from 0 to 4.",
                },
                {
                    "text": "Which is the correct way to import pandas?",
                    "options": ["import pandas", "import pandas as pd", "from pandas import *", "include pandas"],
                    "answer": 1,
                    "explanation": "The standard convention is 'import pandas as pd' for brevity and clarity.",
                },
                {
                    "text": "What is the output of: print(type([1, 2, 3]))?",
                    "options": ["<class 'tuple'>", "<class 'list'>", "<class 'dict'>", "<class 'set'>"],
                    "answer": 1,
                    "explanation": "Square brackets [] define a list in Python.",
                },
                {
                    "text": "Which statement about Python functions is true?",
                    "options": [
                        "Functions can only return one value",
                        "Functions can return multiple values as a tuple",
                        "Functions cannot have default parameters",
                        "Functions must always have a return statement",
                    ],
                    "answer": 1,
                    "explanation": "Python functions can return multiple values, which are automatically packed into a tuple.",
                },
                {
                    "text": "What is the purpose of the 'with' statement when opening files?",
                    "options": [
                        "It makes the code run faster",
                        "It automatically closes the file after the block executes",
                        "It encrypts the file",
                        "It is only for writing files",
                    ],
                    "answer": 1,
                    "explanation": "The 'with' statement ensures proper resource management by automatically closing the file.",
                },
            ],
            3: [
                {
                    "text": "In Pandas, which object represents a table of rows and columns?",
                    "options": ["Series", "DataFrame", "Array", "List"],
                    "answer": 1,
                    "explanation": "A DataFrame is a 2D table of rows and columns with labels.",
                },
                {
                    "text": "Which method shows column types and non-null counts?",
                    "options": ["df.head()", "df.info()", "df.describe()", "df.columns"],
                    "answer": 1,
                    "explanation": "df.info() gives an overview of columns, dtypes and non-null counts.",
                },
                {
                    "text": "Which operation is best for computing total revenue per country?",
                    "options": [
                        "df.sort_values()",
                        "df.groupby('country')['revenue'].sum()",
                        "df.dropna()",
                        "df.merge()",
                    ],
                    "answer": 1,
                    "explanation": "groupby with sum aggregates revenue per country.",
                },
                {
                    "text": "Which method would you use first to quickly inspect the top few rows of a DataFrame?",
                    "options": ["df.tail()", "df.head()", "df.count()", "df.sort_values()"],
                    "answer": 1,
                    "explanation": "df.head() shows the first 5 rows by default, useful for a quick glance.",
                },
                {
                    "text": "Which is a good way to handle obvious duplicate rows in a dataset?",
                    "options": [
                        "Ignore them always",
                        "Use df.drop_duplicates() when duplicates truly represent the same record",
                        "Delete every second row",
                        "You can never remove duplicates",
                    ],
                    "answer": 1,
                    "explanation": "df.drop_duplicates() is appropriate when duplicates are genuine repeats of the same record.",
                },
                {
                    "text": "What does df.isnull().sum() return?",
                    "options": [
                        "The total number of rows",
                        "The count of missing values per column",
                        "The sum of all numeric columns",
                        "A boolean array",
                    ],
                    "answer": 1,
                    "explanation": "df.isnull().sum() counts missing values in each column.",
                },
                {
                    "text": "Which method would you use to combine two DataFrames side-by-side based on a common key?",
                    "options": ["df.concat()", "df.merge()", "df.append()", "df.join()"],
                    "answer": 1,
                    "explanation": "df.merge() performs SQL-style joins based on common columns.",
                },
                {
                    "text": "What is the result of df['price'].mean()?",
                    "options": [
                        "The median price",
                        "The average price across all rows",
                        "The most common price",
                        "The total sum of prices",
                    ],
                    "answer": 1,
                    "explanation": "The .mean() method calculates the arithmetic average.",
                },
                {
                    "text": "How do you select rows where age > 30 in a DataFrame?",
                    "options": [
                        "df[age > 30]",
                        "df[df['age'] > 30]",
                        "df.select(age > 30)",
                        "df.filter(age > 30)",
                    ],
                    "answer": 1,
                    "explanation": "Boolean indexing with df[df['age'] > 30] filters rows based on conditions.",
                },
                {
                    "text": "What does df.describe() provide?",
                    "options": [
                        "Column names only",
                        "Summary statistics for numeric columns",
                        "The first 5 rows",
                        "Data types of columns",
                    ],
                    "answer": 1,
                    "explanation": "df.describe() shows count, mean, std, min, quartiles, and max for numeric columns.",
                },
            ],
            4: [
                {
                    "text": "Which SQL clause filters rows before aggregation?",
                    "options": ["GROUP BY", "WHERE", "HAVING", "ORDER BY"],
                    "answer": 1,
                    "explanation": "WHERE filters rows before grouping; HAVING filters groups after aggregation.",
                },
                {
                    "text": "Which JOIN keeps all rows from the left table and matches from the right?",
                    "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
                    "answer": 1,
                    "explanation": "LEFT JOIN keeps all rows from the left table and matches or NULLs from the right.",
                },
                {
                    "text": "Which keyword is used to sort query results?",
                    "options": ["GROUP BY", "ORDER BY", "SORT BY", "RANK BY"],
                    "answer": 1,
                    "explanation": "ORDER BY sorts the result set.",
                },
                {
                    "text": "In a typical orders schema, which column is most likely a foreign key in the orders table?",
                    "options": ["order_id", "order_date", "customer_id", "total_amount"],
                    "answer": 2,
                    "explanation": "customer_id in the orders table usually refers to the primary key of the customers table.",
                },
                {
                    "text": "What does SELECT * FROM customers WHERE country = 'UK'; do?",
                    "options": [
                        "Updates all UK customers",
                        "Deletes all UK customers",
                        "Returns all columns for customers where country is UK",
                        "Returns only the country column",
                    ],
                    "answer": 2,
                    "explanation": "SELECT with WHERE filters rows and returns matching records; it does not change the data.",
                },
                {
                    "text": "Which aggregate function counts non-NULL values?",
                    "options": ["SUM()", "COUNT()", "AVG()", "MAX()"],
                    "answer": 1,
                    "explanation": "COUNT() counts the number of non-NULL values in a column.",
                },
                {
                    "text": "What is the difference between WHERE and HAVING?",
                    "options": [
                        "They are the same",
                        "WHERE filters rows before grouping; HAVING filters groups after aggregation",
                        "HAVING is faster",
                        "WHERE only works with numbers",
                    ],
                    "answer": 1,
                    "explanation": "WHERE filters individual rows; HAVING filters aggregated groups.",
                },
                {
                    "text": "Which SQL statement would you use to add a new row to a table?",
                    "options": ["UPDATE", "INSERT", "ALTER", "SELECT"],
                    "answer": 1,
                    "explanation": "INSERT adds new rows to a table.",
                },
                {
                    "text": "What does DISTINCT do in a SELECT statement?",
                    "options": [
                        "Sorts the results",
                        "Removes duplicate rows from the result set",
                        "Counts the rows",
                        "Joins tables",
                    ],
                    "answer": 1,
                    "explanation": "DISTINCT eliminates duplicate rows, returning only unique combinations.",
                },
            ],
            5: [
                {
                    "text": "Which measure describes spread: mean, median or standard deviation?",
                    "options": ["Mean", "Median", "Standard deviation", "Mode"],
                    "answer": 2,
                    "explanation": "Standard deviation is a common measure of spread around the mean.",
                },
                {
                    "text": "In an A/B test, conversion rate is usually defined as:",
                    "options": [
                        "conversions / total_users",
                        "total_users / conversions",
                        "revenue / total_users",
                        "revenue / conversions",
                    ],
                    "answer": 0,
                    "explanation": "Conversion rate is number of conversions divided by total users or visits.",
                },
                {
                    "text": "Which statement about correlation is true?",
                    "options": [
                        "Correlation proves causation",
                        "Correlation measures a linear relationship between two variables",
                        "Correlation is always between -2 and 2",
                        "Correlation is the same as p-value",
                    ],
                    "answer": 1,
                    "explanation": "Correlation measures linear association but does not by itself prove causation.",
                },
                {
                    "text": "A p-value of 0.03 in an A/B test typically means:",
                    "options": [
                        "There is a 3% chance the result is due to random variation under the null hypothesis",
                        "The new variant is 3% better",
                        "The result is definitely true",
                        "The test was run on 3% of users",
                    ],
                    "answer": 0,
                    "explanation": "A low p-value suggests the observed difference would be unlikely if there were actually no effect.",
                },
                {
                    "text": "Which of these is an example of a hypothesis test question?",
                    "options": [
                        "What is the average age of users?",
                        "Is the conversion rate higher for variant B than variant A?",
                        "How many users signed up this month?",
                        "What is the maximum revenue?",
                    ],
                    "answer": 1,
                    "explanation": "Hypothesis tests compare groups or conditions, such as A vs B conversion rates.",
                },
                {
                    "text": "What is the median of the dataset [1, 3, 5, 7, 9]?",
                    "options": ["3", "5", "7", "4"],
                    "answer": 1,
                    "explanation": "The median is the middle value when data is sorted: 5 is in the middle position.",
                },
                {
                    "text": "Which statistical test would you use to compare means of two groups?",
                    "options": ["Chi-square test", "T-test", "Correlation", "ANOVA"],
                    "answer": 1,
                    "explanation": "A t-test compares the means of two groups to see if they differ significantly.",
                },
                {
                    "text": "What does a confidence interval tell you?",
                    "options": [
                        "The exact true value",
                        "A range where the true value likely falls",
                        "The sample size",
                        "The p-value",
                    ],
                    "answer": 1,
                    "explanation": "A confidence interval gives a range of plausible values for a population parameter.",
                },
                {
                    "text": "Which measure is most affected by outliers?",
                    "options": ["Median", "Mean", "Mode", "Range"],
                    "answer": 1,
                    "explanation": "The mean is sensitive to extreme values; median is more robust to outliers.",
                },
                {
                    "text": "What is statistical power in hypothesis testing?",
                    "options": [
                        "The probability of correctly rejecting a false null hypothesis",
                        "The sample size",
                        "The p-value threshold",
                        "The confidence level",
                    ],
                    "answer": 0,
                    "explanation": "Statistical power is the probability of detecting an effect when it truly exists.",
                },
            ],
            6: [
                {
                    "text": "Which chart is best for a trend over time?",
                    "options": ["Bar chart", "Line chart", "Pie chart", "Scatter plot"],
                    "answer": 1,
                    "explanation": "Line charts are usually best for showing changes over time.",
                },
                {
                    "text": "What is chart junk?",
                    "options": [
                        "Old charts on disk",
                        "Unnecessary decorations that do not help understanding",
                        "Charts with bugs",
                        "Charts with more than one series",
                    ],
                    "answer": 1,
                    "explanation": "Chart junk is clutter that distracts from the message, such as heavy 3D effects or random icons.",
                },
                {
                    "text": "Which visual would best show the relationship between price and quantity sold?",
                    "options": ["Bar chart", "Line chart", "Pie chart", "Scatter plot"],
                    "answer": 3,
                    "explanation": "Scatter plots are ideal for showing relationships between two numeric variables.",
                },
                {
                    "text": "When creating a dashboard for senior managers, what is usually most important?",
                    "options": [
                        "As many charts as possible",
                        "Clear key metrics and a short narrative they can act on",
                        "Fancy animations",
                        "Showing all raw data tables",
                    ],
                    "answer": 1,
                    "explanation": "Decision-makers need a clear story with key metrics and recommended actions, not noise.",
                },
                {
                    "text": "Which of these is a good practice for chart titles?",
                    "options": [
                        "Use generic titles like 'Chart 1'",
                        "Write a short takeaway, e.g. 'UK revenue grew 10% year-on-year'",
                        "Leave the title blank",
                        "Use only acronyms",
                    ],
                    "answer": 1,
                    "explanation": "Titles that state the main message help non-technical audiences understand quickly.",
                },
                {
                    "text": "What is the purpose of using color in data visualization?",
                    "options": [
                        "To make charts look pretty",
                        "To highlight important patterns and guide attention",
                        "To confuse the audience",
                        "Color should never be used",
                    ],
                    "answer": 1,
                    "explanation": "Color should be used purposefully to draw attention to key insights and patterns.",
                },
                {
                    "text": "Which chart type is generally NOT recommended for showing proportions?",
                    "options": ["Pie chart", "Stacked bar chart", "Line chart", "Treemap"],
                    "answer": 2,
                    "explanation": "Line charts show trends over time, not proportions of a whole.",
                },
                {
                    "text": "What is the main advantage of interactive dashboards over static reports?",
                    "options": [
                        "They look more modern",
                        "Users can explore data and drill down into details",
                        "They are always faster to create",
                        "They never need updates",
                    ],
                    "answer": 1,
                    "explanation": "Interactive dashboards allow users to filter, drill down, and explore data dynamically.",
                },
                {
                    "text": "When presenting to non-technical stakeholders, which is most important?",
                    "options": [
                        "Show all the code you wrote",
                        "Focus on insights and recommendations in plain language",
                        "Use as much technical jargon as possible",
                        "Only show raw data tables",
                    ],
                    "answer": 1,
                    "explanation": "Non-technical audiences need clear insights and actionable recommendations, not technical details.",
                },
                {
                    "text": "What does 'data storytelling' mean?",
                    "options": [
                        "Making up data",
                        "Presenting data in a narrative that guides the audience to insights and actions",
                        "Only using text, no charts",
                        "Hiding negative results",
                    ],
                    "answer": 1,
                    "explanation": "Data storytelling combines data, visuals, and narrative to communicate insights effectively.",
                },
            ],
            7: [
                {
                    "text": "Which is the best description of a capstone project?",
                    "options": [
                        "A single SQL query",
                        "An end-to-end analysis on a realistic dataset with clear narrative",
                        "A screenshot of your IDE",
                        "A random collection of charts",
                    ],
                    "answer": 1,
                    "explanation": "A capstone is an end-to-end project that tells a clear story using realistic data.",
                },
                {
                    "text": "Why should you describe limitations of your project?",
                    "options": [
                        "To show the work is useless",
                        "To be honest about what the analysis can and cannot support",
                        "To make the report longer",
                        "It is not important",
                    ],
                    "answer": 1,
                    "explanation": "Being open about limitations builds trust and shows you understand your methods.",
                },
                {
                    "text": "Which of the following is usually NOT a good choice for a capstone dataset?",
                    "options": [
                        "A realistic open dataset relevant to an industry",
                        "A tiny toy dataset with 10 rows and no real context",
                        "A public healthcare dataset with clear documentation",
                        "Retail sales data from an online shop",
                    ],
                    "answer": 1,
                    "explanation": "Capstones should use realistic data; very small toy datasets are not impressive to employers.",
                },
                {
                    "text": "What is one good way to present your capstone to employers?",
                    "options": [
                        "Keep it only on your local laptop",
                        "Upload the notebook and report to GitHub with a clear README",
                        "Print screenshots only",
                        "Describe it verbally without any artefacts",
                    ],
                    "answer": 1,
                    "explanation": "A well-documented GitHub repo with code, notebook and README is easy to share and review.",
                },
                {
                    "text": "Which document is most important to include alongside your capstone code?",
                    "options": [
                        "A README explaining the problem, data, methods and results",
                        "Your full employment history",
                        "A list of all Python packages ever installed",
                        "Nothing, code speaks for itself",
                    ],
                    "answer": 0,
                    "explanation": "A clear README helps others understand your project quickly and shows communication skills.",
                },
                {
                    "text": "What should be the first section of your capstone report?",
                    "options": [
                        "The code",
                        "Problem definition and business context",
                        "The conclusion",
                        "Your CV",
                    ],
                    "answer": 1,
                    "explanation": "Start with the problem and context so readers understand why the work matters.",
                },
                {
                    "text": "Which is a sign of a strong capstone project?",
                    "options": [
                        "Using every machine learning algorithm you know",
                        "Clear problem, appropriate methods, honest results and limitations",
                        "The longest possible report",
                        "Hiding any negative findings",
                    ],
                    "answer": 1,
                    "explanation": "Strong capstones are focused, honest, and demonstrate good judgment in method selection.",
                },
                {
                    "text": "Why include visualizations in your capstone?",
                    "options": [
                        "To make it look colorful",
                        "To communicate patterns and insights more effectively than tables alone",
                        "Because all projects must have exactly 10 charts",
                        "Visualizations are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Good visualizations help communicate findings clearly and make reports more accessible.",
                },
                {
                    "text": "What is the purpose of a capstone project in your learning journey?",
                    "options": [
                        "To pass time",
                        "To demonstrate end-to-end data science skills to potential employers",
                        "To memorize formulas",
                        "To avoid learning theory",
                    ],
                    "answer": 1,
                    "explanation": "Capstones showcase your ability to tackle real problems independently from start to finish.",
                },
                {
                    "text": "Which is better for a capstone: depth or breadth?",
                    "options": [
                        "Breadth - try to cover everything superficially",
                        "Depth - do one problem well with clear methods and honest evaluation",
                        "Neither matters",
                        "Only breadth matters",
                    ],
                    "answer": 1,
                    "explanation": "Employers value depth and rigor over superficial coverage of many topics.",
                },
            ],
        }

        selected_quiz_unit = st.selectbox(
            "Choose a unit:",
            options=list(quiz_bank.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_foundations_quiz_unit",
        )

        questions = quiz_bank.get(selected_quiz_unit, [])
        if not questions:
            st.info("No quiz available for this unit yet.")
            return

        answers = []
        for idx, q in enumerate(questions, start=1):
            st.markdown(f"**Q{idx}. {q['text']}**")
            choice = st.radio(
                label=f"q{idx}",
                options=list(range(len(q["options"]))),
                format_func=lambda i, opts=q["options"]: opts[i],
                key=f"ds_foundations_q{selected_quiz_unit}_{idx}",
            )
            answers.append(choice)

        if st.button("Mark quiz", key="ds_foundations_quiz_mark"):
            score = sum(1 for ua, q in zip(answers, questions) if ua == q["answer"])
            total = len(questions)
            st.success(f"You scored {score} out of {total} on Unit {selected_quiz_unit}.")

            if total:
                for idx, (ua, q) in enumerate(zip(answers, questions), start=1):
                    if ua != q["answer"]:
                        correct = q["options"][q["answer"]]
                        explanation = q.get("explanation", "")
                        st.warning(f"Q{idx}: Correct answer is '{correct}'. {explanation}")

            if total > 0 and score == total:
                st.balloons()
                        "A list of all Python errors you saw",
                        "Random notes with no structure",
                    ],
                    "answer": 0,
                    "explanation": "A clear README helps others understand your project quickly and is standard practice on GitHub.",
                },
            ],
        }

        quiz_unit = st.selectbox(
            "Choose a unit for a quick-check quiz:",
            options=sorted(quiz_bank.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="dsf_quiz_unit_select",
        )

        qs = quiz_bank.get(quiz_unit, [])
        user_answers = []
        for idx, q in enumerate(qs):
            st.markdown(f"**Q{idx + 1}. {q['text']}**")
            choice = st.radio(
                label=f"q{quiz_unit}_{idx+1}",
                options=list(range(len(q["options"]))),
                format_func=lambda i, opts=q["options"]: opts[i],
                key=f"dsf_quiz_u{quiz_unit}_q{idx+1}",
            )
            user_answers.append(choice)

        if st.button("Mark quiz", key="dsf_quiz_mark"):
            score = sum(1 for ua, q in zip(user_answers, qs) if ua == q["answer"])
            total = len(qs)
            st.success(f"You scored {score} out of {total} on Unit {quiz_unit} quick-check quiz.")

            # Show brief feedback for any questions that were answered incorrectly
            if total:
                for idx, (ua, q) in enumerate(zip(user_answers, qs), start=1):
                    if ua != q["answer"]:
                        correct_option = q["options"][q["answer"]]
                        explanation = q.get("explanation", "")
                        st.warning(f"Q{idx}: Correct answer is '{correct_option}'. {explanation}")

            if total > 0 and score == total:
                st.balloons()

        st.markdown("---")
        st.markdown("### 📚 Quizzes and final exam for this pathway")
        st.markdown(
            """This pathway includes structured quizzes for each unit plus a final
theory & application exam. Quizzes are authored as markdown files in the
project so they can be imported into your chosen quiz/assessment system or
shared as PDFs.

**Quiz files for Pathway 1 (relative to project root):**

- `data_science_pathway1/assessments/unit1_quiz.md`
- `data_science_pathway1/assessments/unit2_quiz.md`
- `data_science_pathway1/assessments/unit3_quiz.md`
 - `data_science_pathway1/assessments/unit4_quiz.md`
 - `data_science_pathway1/assessments/unit5_quiz.md`
 - `data_science_pathway1/assessments/unit6_quiz.md`
 - `data_science_pathway1/assessments/unit7_quiz.md`
 - `data_science_pathway1/assessments/final_exam_pathway1.md`
"""
        )

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
            """Use this area for supporting documents, study plans and checklists.

Suggested documents (which tutors/admins can host in the main LMS materials system):
- Study timetable templates (8–12 week plans)
- Checklists for each unit
- Portfolio structure guide
- Example project reports and CV snippets

For this pathway, the following template documents already exist in the
project under `data_science_pathway1/docs` and can be converted to PDF or
uploaded into the central LMS document library:

- `study_plan_8_weeks.md` – suggested 8-week teaching plan
- `unit_checklists_pathway1.md` – tutor/learner unit checklists
- `portfolio_guide.md` – guidance for building a job-ready portfolio
"""
        )

        st.markdown("---")
        st.markdown("### 📥 Download core documents as PDF")

        # These documents are generated from inline markdown templates so that
        # learners can download PDFs directly from the app.
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button("📥 Study plan (8 weeks) PDF", key="dsf_study_plan_pdf"):
                study_plan_md = """# Data Science Foundations (Pathway 1) – 8 Week Study Plan

This plan assumes **8 weeks** of part-time study. Tutors can stretch or
compress it depending on learner background.

---

## Week 1 – Unit 1: Intro to Data & the Role of the Data Scientist

- Read Unit 1 learning materials in the app.
- Explore at least one public dataset (e.g. open government, NHS, World Bank).
- Map CRISP-DM phases to a simple project idea.
- Complete Unit 1 quick-check quiz.

## Week 2 – Unit 2: Python Programming for Data

- Work through the Python basics notebook(s) provided by your tutor.
- Practise loading CSVs and computing simple summaries.
- Implement a few small helper functions for data cleaning.
- Complete Unit 2 quick-check quiz.

## Week 3 – Unit 3: Working with Data using Pandas & NumPy

- Read the Pandas & NumPy theory sections.
- In notebooks, practise:
  - Loading multiple CSVs.
  - Joining tables and handling missing values.
  - Building a reusable cleaning pipeline.
- Complete Unit 3 quick-check quiz.

## Week 4 – Unit 4: SQL & Relational Databases for Analysis

- Review SQL theory topics (SELECT, WHERE, JOIN, GROUP BY, HAVING).
- Practise queries on a sample multi-table schema.
- Write at least 5 queries that answer realistic business questions.
- Complete Unit 4 quick-check quiz.

## Week 5 – Unit 5: Statistics & Probability for Data Science

- Study distributions, summary statistics and correlation.
- Run a small A/B test analysis in Python or a notebook.
- Interpret p-values in plain language.
- Complete Unit 5 quick-check quiz.

## Week 6 – Unit 6: Data Visualisation & Storytelling

- Read the visualisation and storytelling guidance.
- Build a small dashboard or report (at least 4 charts) for a chosen dataset.
- Write short narratives for each key chart.
- Complete Unit 6 quick-check quiz.

## Weeks 7–8 – Unit 7: Foundations Capstone Project

- Select a realistic dataset and define clear questions.
- Complete an end-to-end analysis using the CRISP-DM mindset.
- Prepare a notebook/script plus a short report or slide deck.
- Share a draft portfolio/GitHub repo with peers or tutors for feedback.

Learners may also choose to spend **extra time** on the capstone if they
want a standout portfolio project.
"""
                pdf = create_unit_pdf(0, "Study Plan (8 Weeks)", study_plan_md)
                st.download_button(
                    label="Download Study Plan PDF",
                    data=pdf,
                    file_name="Data_Science_Foundations_Study_Plan_8_Weeks.pdf",
                    mime="application/pdf",
                    key="dsf_study_plan_pdf_dl",
                )

        with col_b:
            if st.button("📥 Unit checklists PDF", key="dsf_checklists_pdf"):
                checklists_md = """# Data Science Foundations (Pathway 1) – Unit Checklists

Use these checklists to track progress. They are **not** formal assessment
criteria but a practical guide.

---

## Unit 1 – Intro to Data & the Role of the Data Scientist

- [ ] I can explain what data science is in one or two sentences.
- [ ] I can name the main data roles (analyst, scientist, engineer, ML engineer).
- [ ] I understand the CRISP-DM lifecycle at a high level.
- [ ] I can give at least one example of data ethics/privacy concern.

## Unit 2 – Python Programming for Data

- [ ] I can write simple Python scripts and functions.
- [ ] I can load CSV files and print basic summaries.
- [ ] I understand lists, dictionaries and control flow.
- [ ] I can keep a notebook tidy and readable.

## Unit 3 – Working with Data using Pandas & NumPy

- [ ] I can create and manipulate Pandas DataFrames.
- [ ] I can handle missing values and duplicates sensibly.
- [ ] I can join multiple tables and compute grouped metrics.
- [ ] I can build a small, reusable cleaning notebook or script.

## Unit 4 – SQL & Relational Databases for Analysis

- [ ] I can explain what a relational database and schema are.
- [ ] I can write SELECT, WHERE, ORDER BY, GROUP BY and simple JOIN queries.
- [ ] I understand the idea of primary keys and foreign keys.
- [ ] I can answer realistic questions using SQL queries.

## Unit 5 – Statistics & Probability for Data Science

- [ ] I can describe mean, median, standard deviation and distributions.
- [ ] I know that correlation does not imply causation.
- [ ] I can interpret a simple A/B test result and p-value.
- [ ] I can explain what a confidence interval means in plain language.

## Unit 6 – Data Visualisation & Storytelling

- [ ] I can pick appropriate chart types for different questions.
- [ ] I avoid common chart junk and misleading visual choices.
- [ ] I can write short narrative summaries to go with charts.
- [ ] I can build a small, coherent visual story or dashboard.

## Unit 7 – Foundations Capstone Project

- [ ] I have chosen a realistic dataset and clear problem statement.
- [ ] I have documented my data sources and basic cleaning steps.
- [ ] I have built an end-to-end analysis answering the key questions.
- [ ] I have written a short report or slide deck with conclusions and next steps.
"""
                pdf = create_unit_pdf(0, "Unit Checklists", checklists_md)
                st.download_button(
                    label="Download Checklists PDF",
                    data=pdf,
                    file_name="Data_Science_Foundations_Unit_Checklists.pdf",
                    mime="application/pdf",
                    key="dsf_checklists_pdf_dl",
                )

        with col_c:
            if st.button("📥 Portfolio guide PDF", key="dsf_portfolio_pdf"):
                portfolio_md = """# Data Science Foundations (Pathway 1) – Portfolio Guide

This guide explains how to turn your Pathway 1 work into a **job-ready
portfolio** that stands out in the UK, US and global markets.

---

## 1. Core artefacts to include

- At least one **clean, well-documented notebook** per major unit (Python,
  Pandas, SQL, statistics, visualisation).
- A strong **capstone project** notebook and report.
- A short `README.md` in each project folder explaining:
  - Problem and context.
  - Data sources.
  - Methods and key results.
  - How to run the code.

## 2. Structuring your GitHub repository

Suggested structure:

- `foundations_capstone/`
  - `notebooks/`
  - `data/` (small sample or synthetic data only)
  - `README.md`
- `unit_labs/`
  - `python_basics/`
  - `pandas_cleaning/`
  - `sql_exercises/`
  - `visualisation_story/`

Make sure you remove credentials and do **not** publish sensitive data.

## 3. Writing a strong README

Every portfolio project should have a README that answers:

1. What problem are you solving and why does it matter?
2. What data did you use and how did you clean it?
3. What methods and tools did you apply?
4. What are the main findings or recommendations?
5. How can someone run or reproduce your work?

## 4. Connecting portfolio to CV and LinkedIn

- Add a short "Projects" section to your CV with 2–3 bullet points per
  project and a link to GitHub.
- On LinkedIn, add links to key repositories in your About section and
  Experience/Projects entries.

Your goal is that a recruiter or hiring manager can open **one link** and
quickly see that you can take a realistic dataset from question to insight.
"""
                pdf = create_unit_pdf(0, "Portfolio Guide", portfolio_md)
                st.download_button(
                    label="Download Portfolio Guide PDF",
                    data=pdf,
                    file_name="Data_Science_Foundations_Portfolio_Guide.pdf",
                    mime="application/pdf",
                    key="dsf_portfolio_pdf_dl",
                )

        st.markdown("---")
        st.markdown("### 💼 Career Preparation Package")
        st.success(
            "**NEW!** Comprehensive job search toolkit with resume templates, "
            "200 interview questions, LinkedIn optimization, and more!"
        )
        
        if st.button("📥 Career Prep Package (Resume + Interview Guide)", key="dsf_career_prep_pdf"):
            career_prep_md = """# Career Prep Package - Land Your Data Job

**For:** Data Analyst, Data Scientist, Data Engineer roles

---

## 📄 RESUME TEMPLATES

### Data Analyst Resume Template

```
[YOUR NAME]
Data Analyst
Email: your.email@example.com | Phone: +44 7XXX XXX XXX
LinkedIn: linkedin.com/in/yourname | GitHub: github.com/yourname

PROFESSIONAL SUMMARY
Results-driven Data Analyst with expertise in SQL, Python, and data visualization.
Completed comprehensive training covering data cleaning, statistical analysis,
dashboard creation, and business intelligence. Proven ability to translate complex
data into actionable business insights.

TECHNICAL SKILLS
• Languages: SQL, Python (Pandas, NumPy, Matplotlib, Seaborn)
• Tools: Excel (Advanced), Tableau/Power BI, Jupyter Notebooks
• Databases: MySQL, PostgreSQL
• Skills: Data Cleaning, EDA, A/B Testing, Statistical Analysis, Dashboards

KEY PROJECTS

Data Analysis Capstone | [Date]
• Analyzed [domain] dataset with 50,000+ records to identify [business insight]
• Cleaned and transformed data using Python Pandas, handling 15% missing values
• Created interactive dashboard showing key metrics and trends
• Presented findings to stakeholders with actionable recommendations
• GitHub: [link]

EDUCATION & CERTIFICATIONS
• Data Science Foundations Certification | [Date]
  - 350+ hours of hands-on training
  - Validated through comprehensive assessments
```

---

## 💼 TOP 50 INTERVIEW QUESTIONS

### SQL Questions (10)
1. What is the difference between WHERE and HAVING?
   ANSWER: WHERE filters rows before grouping, HAVING filters after aggregation

2. Write a query to find the top 5 customers by total spend
   ANSWER:
   ```sql
   SELECT customer_id, SUM(order_amount) as total
   FROM orders
   GROUP BY customer_id
   ORDER BY total DESC
   LIMIT 5;
   ```

3. Explain INNER JOIN vs LEFT JOIN
   ANSWER: INNER returns only matches from both tables,
   LEFT returns all from left table + matches from right

4. How do you find duplicate rows?
   ANSWER:
   ```sql
   SELECT column, COUNT(*) as count
   FROM table
   GROUP BY column
   HAVING COUNT(*) > 1;
   ```

5. What is a window function? Give an example
   ANSWER: Performs calculations across table rows related to current row
   ```sql
   SELECT name, salary,
          RANK() OVER (ORDER BY salary DESC) as rank
   FROM employees;
   ```

6. Write query for running total
   ```sql
   SELECT date, sales,
          SUM(sales) OVER (ORDER BY date) as running_total
   FROM daily_sales;
   ```

7. How to optimize slow queries?
   - Add indexes on columns in WHERE/JOIN
   - Avoid SELECT *, choose specific columns
   - Use EXPLAIN to analyze query plan

8. Explain GROUP BY
   - Groups rows with same values
   - Used with aggregation functions (SUM, COUNT, AVG)

9. What is a subquery?
   - Query within a query
   - Used for filtering or calculating intermediate results

10. How to handle NULL in SQL?
   - Use IS NULL / IS NOT NULL
   - Use COALESCE(column, default_value)
   - Use IFNULL or NULLIF functions

### Python/Pandas Questions (10)
11. Read CSV in Pandas: pd.read_csv('file.csv')

12. DataFrame vs Series: DataFrame is 2D table, Series is 1D column

13. Handle missing values:
    - df.dropna() - remove rows
    - df.fillna(value) - fill with value
    - df.interpolate() - fill with interpolation

14. .loc vs .iloc:
    - .loc[row_label, col_label] - by label
    - .iloc[row_index, col_index] - by integer position

15. Merge DataFrames:
    pd.merge(df1, df2, on='key', how='inner')

16. groupby() example:
    df.groupby('category')['sales'].sum()

17. Remove duplicates:
    df.drop_duplicates(subset=['column'])

18. Vectorization:
    - Apply operations to entire arrays at once
    - Much faster than loops
    - Example: df['total'] = df['price'] * df['quantity']

19. Create pivot table:
    df.pivot_table(values='sales', index='product', columns='month', aggfunc='sum')

20. Filter rows:
    df[df['sales'] > 1000]
    df.query('sales > 1000 and region == "UK"')

### Statistics Questions (10)
21. Mean vs Median vs Mode:
    - Mean: average
    - Median: middle value
    - Mode: most common value

22. Standard deviation: measures spread of data around mean

23. Correlation vs Causation:
    - Correlation: two variables move together
    - Causation: one causes the other
    - Correlation does NOT imply causation!

24. P-value: probability of seeing results if null hypothesis is true
    - p < 0.05 usually considered significant

25. A/B test steps:
    - Define metric and hypothesis
    - Randomly split users
    - Run experiment
    - Calculate statistical significance
    - Make decision

26. Sampling bias: when sample doesn't represent population

27. Confidence interval: range where true value likely falls
    - 95% CI means 95% confident true value is in range

28. Hypothesis testing:
    - Null hypothesis: no effect
    - Alternative: there is an effect
    - Use statistical test to accept/reject

29. Type I error: False positive (reject true null hypothesis)
    Type II error: False negative (fail to reject false null hypothesis)

30. Outliers:
    - Values far from others
    - Handle by: removal, capping, transformation, or keeping with justification

### Machine Learning Questions (10)
31. Supervised vs Unsupervised:
    - Supervised: has labels (classification, regression)
    - Unsupervised: no labels (clustering)

32. Overfitting:
    - Model learns training data too well
    - Prevent: cross-validation, regularization, more data

33. Train/test split: divide data for training and evaluation

34. Cross-validation: multiple train/test splits to robust evaluation

35. Precision vs Recall:
    - Precision: of predicted positives, how many correct?
    - Recall: of actual positives, how many found?

36. Feature engineering: creating new features from existing data

37. Bias-variance tradeoff:
    - High bias: underfitting
    - High variance: overfitting
    - Need balance

38. Regularization (L1/L2): prevents overfitting by penalizing complexity

39. Imbalanced datasets:
    - Use SMOTE, class weights, or different metrics
    - Don't use accuracy alone

40. Model evaluation:
    - Regression: MSE, RMSE, MAE, R²
    - Classification: Accuracy, Precision, Recall, F1, ROC-AUC

### Behavioral Questions (10)
41. Tell me about yourself:
    - Brief career history
    - Why data role
    - Key skills and achievements

42. Why data analyst/scientist?
    - Passion for data and insights
    - Problem-solving
    - Impact on business decisions

43. Describe a challenging project:
    - Situation, Task, Action, Result (STAR method)
    - Focus on how you overcame challenges

44. How do you prioritize tasks?
    - Understand business impact
    - Consider urgency and importance
    - Communicate with stakeholders

45. Explain technical results to non-technical audience:
    - Avoid jargon
    - Use visualizations
    - Focus on business impact

46. How do you ensure analysis is correct?
    - Validate data sources
    - Check edge cases
    - Peer review
    - Document assumptions

47. Handle conflicting data:
    - Investigate root cause
    - Check data quality
    - Consult with data owners
    - Document decision

48. Data quality issues:
    - Document the issue
    - Assess impact
    - Fix if possible or flag limitations
    - Communicate to stakeholders

49. How do you stay current?
    - Online courses
    - Blog posts and papers
    - Communities (Kaggle, GitHub)
    - Practice projects

50. Questions for interviewer:
    - What does success look like in this role?
    - What tools and technologies does the team use?
    - What are the biggest data challenges?
    - What is the team structure?

---

## 🎤 INTERVIEW TIPS

### Before Interview:
- Research company and role
- Prepare STAR stories
- Practice technical questions
- Prepare questions to ask

### During Interview:
- Listen carefully
- Clarify before answering
- Use examples from experience
- Show enthusiasm

### After Interview:
- Send thank you email within 24h
- Reiterate interest
- Reference specific discussion points

---

## 💡 LINKEDIN OPTIMIZATION

### Headline Example:
"Data Analyst | SQL, Python, Tableau | Turning Data into Insights"

### About Section:
I'm a Data Analyst passionate about [specific area]. I recently completed
intensive training in [pathway topics], where I:
✓ Built [X] end-to-end projects
✓ Mastered [key skills]
✓ Worked with datasets from [domains]

I'm particularly interested in [industry] and solving [types of problems].

Currently seeking opportunities to apply my skills in [type of role].

### Skills to Add:
- SQL
- Python
- Data Analysis
- Data Visualization
- Pandas
- Statistical Analysis
- Excel
- Tableau/Power BI
- Problem Solving
- Communication

---

## 📧 EMAIL TEMPLATE - Networking

Subject: Data Analyst interested in [Company]

Hi [Name],

I'm [Your Name], a data analyst with foundation in SQL, Python, and visualization.
I recently completed comprehensive training and I'm impressed by [Company]'s
work in [specific area].

I noticed [Company] is [doing X / hiring / working on Y], and I believe my
skills in [relevant skills] could contribute to [specific value].

Would you be open to a brief conversation about opportunities at [Company]?

Best regards,
[Your Name]

---

This Career Prep Package is designed to help you land your first data role.
Practice the interview questions, customize the resume template, and optimize
your LinkedIn profile.

Good luck with your job search!
"""
            pdf = create_unit_pdf(0, "Career Prep Package", career_prep_md)
            st.download_button(
                label="Download Career Prep Package PDF",
                data=pdf,
                file_name="Career_Prep_Package_Data_Jobs.pdf",
                mime="application/pdf",
                key="dsf_career_prep_pdf_dl",
            )

    # My Progress
    with tabs[6]:
        st.subheader("📊 My Progress")
        if not enrollment:
            st.info("Progress data is not available yet. Once enrolled, your progress will appear here.")
        else:
            _render_progress_header(enrollment)

            st.markdown("---")
            st.markdown("### ✅ Personal checklist (for learners)")
            for unit_number, unit in UNITS.items():
                st.checkbox(
                    f"Completed Unit {unit_number}: {unit['name']}",
                    key=f"ds_foundations_progress_unit_{unit_number}",
                )

    # Certificate
    with tabs[7]:
        st.subheader("🎓 Certificate")
        st.info(
            "On successful completion of all units and assessments, learners receive a "
            "T21 Data Science Foundations certificate. Training providers can also link "
            "this to external awards if desired."
        )

        st.markdown(
            """### Requirements for completion

- Complete and submit evidence for all 7 units
- Demonstrate competence in Python, SQL, statistics and visualisation
- Complete at least one end-to-end capstone project
- Meet internal quality standards set by tutors/assessors
"""
        )

        if enrollment and enrollment.get("progress", 0) >= 100:
            st.success(
                "All requirements appear to be complete. Your training provider can now "
                "issue your Data Science Foundations certificate."
            )
        else:
            st.info(
                "Keep working through your units and projects. Once everything is complete, "
                "your tutor will confirm and issue your certificate."
            )
