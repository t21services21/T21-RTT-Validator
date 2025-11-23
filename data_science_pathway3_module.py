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


COURSE_ID = "data_science_pathway_3"
COURSE_NAME = "Data Science Pathway 3 (Advanced ML & MLOps)"


UNITS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Advanced Feature Engineering & Pipelines at Scale",
        "level": "Advanced",
        "glh": 24,
        "credits": 4,
    },
    2: {
        "name": "Experiment Tracking & Model Selection",
        "level": "Advanced",
        "glh": 24,
        "credits": 4,
    },
    3: {
        "name": "Advanced Supervised Models & Ensembles",
        "level": "Advanced",
        "glh": 24,
        "credits": 4,
    },
    4: {
        "name": "Time-series Forecasting for Operations",
        "level": "Advanced",
        "glh": 24,
        "credits": 4,
    },
    5: {
        "name": "Packaging, Environments & CI/CD for ML",
        "level": "Advanced",
        "glh": 18,
        "credits": 3,
    },
    6: {
        "name": "Monitoring, Drift & Responsible AI",
        "level": "Advanced",
        "glh": 18,
        "credits": 3,
    },
    7: {
        "name": "Advanced Production-style Capstone Project",
        "level": "Advanced",
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
        st.markdown("#### 📘 Why advanced feature engineering matters in production")
        st.markdown(
            """In this unit you take the feature engineering mindset from Pathway 2
and push it to **production-scale problems**:

- Features must be recomputed reliably on new data every day/hour.
- The same feature may be used by **many models** across teams.
- Mistakes in feature definitions can break dashboards, models and SLAs.

You move from "a notebook that works" to a **repeatable feature pipeline**
that could live in a feature store or data platform.
"""
        )

        st.markdown("#### 🧱 Designing feature tables for multiple models")
        st.markdown(
            """You will practise designing feature tables that can support several
use cases at once, for example:

- A patient/consumer table with stable identifiers and slowly changing
  attributes.
- Separate event-level tables (visits, transactions, sensor readings).
- Clear keys and timestamps that make joining safe.

The emphasis is on **clarity and re-use**: one well-designed table may
support churn models, upsell models and risk scores.
"""
        )

        st.markdown("#### ⏱ Late-arriving data, backfills and point-in-time correctness")
        st.markdown(
            """In production you rarely have "perfect" data at once:

- Some records arrive late (e.g. claims processed days after the event).
- Historical backfills are needed when you fix a bug or onboard new data.
- Features must respect **time travel** constraints so models never see
  information from the future.

You will discuss point-in-time correctness and why feature pipelines must
be careful about which rows are visible on any given prediction date.
"""
        )

        st.markdown("#### 🧩 Towards feature stores and shared definitions")
        st.markdown(
            """Rather than every team writing their own feature code from
scratch, many organisations move towards **feature stores** or shared
libraries of feature definitions.

At this level you will not build a full feature store, but you will:

- Write feature definitions as reusable functions or small pipelines.
- Think about naming, ownership and documentation of features.
- Understand how a feature store can reduce duplication and errors.
"""
        )
    elif unit_number == 2:
        st.markdown("#### 📘 Why experiment tracking matters")
        st.markdown(
            """As models and datasets grow, you can no longer rely on memory or
spreadsheet notes to track what you tried. This unit shows how systematic
**experiment tracking** helps you:

- Reproduce past results.
- Compare models fairly over time.
- Explain decisions to colleagues, auditors and regulators.
"""
        )

        st.markdown("#### 🗂 What to log for each run")
        st.markdown(
            """You will design a lightweight logging strategy that records:

- Parameters and hyperparameters.
- Data versions and feature sets.
- Metrics on validation and test sets.
- Pointers to artefacts (models, plots, configuration files).

This maps to tools like MLflow, Weights & Biases or custom internal
systems, but the ideas stay the same across platforms.
"""
        )

        st.markdown("#### ⚖️ Model selection strategies")
        st.markdown(
            """Instead of choosing a model based on one lucky validation split,
you will explore strategies such as:

- k-fold cross-validation with logged results.
- Comparing families of models (linear vs tree-based vs boosting).
- Using simple baselines as anchors so you know when a complex model is
  really better.
"""
        )

        st.markdown("#### 📜 Reproducibility and audit trails")
        st.markdown(
            """You will discuss how experiment tracking supports
**reproducibility** and governance:

- Being able to re-run a training job months later.
- Answering "which model version made this prediction?".
- Supporting compliance requirements in regulated environments.
"""
        )
    elif unit_number == 3:
        st.markdown("#### 📘 Why advanced supervised models?")
        st.markdown(
            """This unit deepens your supervised learning skills with
**gradient boosting, ensembles and calibration**. You will see when
these models genuinely add value beyond simpler baselines and what
trade-offs they introduce (complexity, interpretability, compute).
"""
        )

        st.markdown("#### 🌲 Ensembles and gradient boosting")
        st.markdown(
            """You will compare different ensemble approaches:

- Random forests as bagged decision trees.
- Gradient boosting frameworks (e.g. XGBoost/LightGBM style APIs).
- Simple stacking/ensembling ideas.

The focus is on **evaluation discipline** (validation folds, baselines)
rather than specific libraries.
"""
        )

        st.markdown("#### 🎯 Probability calibration and decision thresholds")
        st.markdown(
            """For many real problems you care about **probabilities**, not just
class labels. You will:

- Diagnose over- or under-confident models using calibration plots.
- Explore methods like Platt scaling / isotonic regression conceptually.
- Understand how calibration interacts with threshold choices and
  cost-sensitive decisions.
"""
        )

        st.markdown("#### 🔍 Interpretability and communication")
        st.markdown(
            """Complex models do not have to be black boxes. You will practise:

- Comparing global feature importance to simple baselines.
- Inspecting partial dependence-style effects conceptually.
- Writing clear explanations of what the model has learned and where it
  may fail.
"""
        )
    elif unit_number == 4:
        st.markdown("#### 📘 Why time-series forecasting?")
        st.markdown(
            """Many operational decisions depend on **future values**: demand,
admissions, call volumes, workloads. This unit focuses on building and
evaluating time-series forecasts that are realistic enough for
operational planning.
"""
        )

        st.markdown("#### 📈 Forecasting baselines and error metrics")
        st.markdown(
            """You will start with strong, simple baselines:

- Naïve forecasts (e.g. "tomorrow = today").
- Moving averages and seasonal naïve baselines.

You will evaluate them using metrics such as MAE, RMSE and MAPE and use
these as anchors before trying more complex models.
"""
        )

        st.markdown("#### 🔁 Seasonality, trend and covariates")
        st.markdown(
            """Real series often have:

- Long-term trends (upwards or downwards).
- Seasonality (daily/weekly/annual patterns).
- External drivers (holidays, campaigns, weather).

You will discuss how to represent these patterns via features or via
specialised forecasting models.
"""
        )

        st.markdown("#### 🧪 Rolling-window evaluation and leakage risks")
        st.markdown(
            """Random train/test splits often break the time structure and can
hide leakage. You will practise:

- Rolling-origin evaluation (train on past, validate on the next block).
- Comparing models across several forecast horizons.
- Checking for leakage from future information in features.
"""
        )
    elif unit_number == 5:
        st.markdown("#### 📘 Why packaging and environments matter")
        st.markdown(
            """Great models are useless if they cannot be run reliably on
another machine. This unit focuses on **environments, packaging and
deployment plumbing** so that:

- The right versions of libraries are available.
- Code runs the same way on laptops, servers and CI.
- Teams can iterate safely without "it works on my machine" bugs.
"""
        )

        st.markdown("#### 📦 Environments and dependency management")
        st.markdown(
            """You will explore practical patterns for managing dependencies:

- Environment files (e.g. `requirements.txt`, `pyproject.toml`).
- Pinning vs flexible version ranges.
- Using virtual environments or containers to isolate projects.

The emphasis is on **repeatability** and clear documentation.
"""
        )

        st.markdown("#### 🧰 Packaging models and pipelines")
        st.markdown(
            """You will think about how a trained pipeline becomes a
**deployable artefact**:

- Simple batch scripts that load a saved pipeline.
- Lightweight services/APIs for online scoring.
- Configuration-driven design so behaviour is not hard-coded.
"""
        )

        st.markdown("#### 🔄 CI/CD concepts for ML projects")
        st.markdown(
            """You will discuss how continuous integration and delivery look for
ML:

- Automated tests for data/feature assumptions.
- Re-running training or evaluation in CI.
- Controlled promotion of models between environments (dev/test/prod).
"""
        )
    elif unit_number == 6:
        st.markdown("#### 📘 Why monitoring and responsible AI?")
        st.markdown(
            """Models change behaviour over time as data, users and processes
change. This unit focuses on **catching problems early** and ensuring
models remain safe and ethical in production.
"""
        )

        st.markdown("#### 📡 Data and model performance monitoring")
        st.markdown(
            """You will explore what and how to monitor:

- Data ranges, missingness and distributions.
- Feature drift vs label drift.
- Performance metrics over time and across segments.

The goal is to design a minimal but effective monitoring dashboard.
"""
        )

        st.markdown("#### ⚖️ Fairness, bias and impact")
        st.markdown(
            """You will connect technical monitoring to real-world impact:

- Checking performance across key subgroups.
- Identifying potential unfairness or harm.
- Designing escalation paths when issues are detected.
"""
        )

        st.markdown("#### 🧭 Governance and incident response")
        st.markdown(
            """Monitoring is only useful if someone acts on it. You will discuss
simple governance patterns:

- Who owns a model in production.
- How incidents are logged, triaged and resolved.
- How learnings feed back into retraining and design.
"""
        )
    elif unit_number == 7:
        st.markdown("#### 📘 Production-style capstone goals")
        st.markdown(
            """The Pathway 3 capstone is your chance to demonstrate **end-to-end
ownership** of an ML system:

- A realistic problem and dataset.
- A robust training pipeline and chosen model.
- A clear deployment and monitoring sketch.
"""
        )

        st.markdown("#### 🧱 Suggested capstone structure")
        st.markdown(
            """A typical structure:

1. Problem & context (including risks and constraints).
2. Data understanding and feature pipeline.
3. Experiment tracking and model selection.
4. Packaging & deployment plan.
5. Monitoring, drift and responsible AI considerations.
6. Reflections and next steps.
"""
        )


def render_data_science_pathway3_module():
    learner_email = st.session_state.get("user_email", "")

    st.title("🚀 Data Science Pathway 3 (Advanced ML & MLOps)")
    st.success(
        "Take the final step: design, deploy and monitor advanced ML systems that work in the real world."
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
            """Pathway 3 is designed for learners who have already completed
Pathway 2 (Intermediate ML) or have equivalent experience building and
evaluating models.

By the end of this pathway you will be able to:

- Design robust feature pipelines for production.
- Track experiments and select models systematically.
- Use advanced supervised models and evaluate them fairly.
- Build and evaluate time-series forecasts for operations questions.
- Understand packaging, environments and CI/CD concepts for ML.
- Design monitoring, drift detection and responsible AI checks.
- Complete a production-style ML capstone project.
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
        st.info("High-level reading and concept reference for advanced topics.")

        selected_unit = st.selectbox(
            "Select a unit:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_p3_materials_unit",
        )

        _render_unit_learning_materials(selected_unit)

        st.markdown("---")
        if st.button("📥 Download unit theory summary as PDF", key="ds_p3_unit_pdf"):
            unit = UNITS[selected_unit]
            content_lines = [f"# Unit {selected_unit}: {unit['name']}", ""]
            content_lines.append("High-level notes for this advanced unit.")
            content_lines.append("Refer to the in-app learning materials, labs and notebooks for full details.")
            markdown_content = "\n".join(content_lines)
            pdf_buffer = create_unit_pdf(
                selected_unit,
                unit["name"],
                markdown_content,
            )
            st.download_button(
                label="📥 Download Unit Summary PDF",
                data=pdf_buffer,
                file_name=f"Data_Science_Pathway3_Unit_{selected_unit}.pdf",
                mime="application/pdf",
                key="ds_p3_unit_pdf_dl",
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

    # Labs & mini projects (placeholder – to be expanded like Pathway 2)
    with tabs[2]:
        st.subheader("🧪 Labs & Mini Projects")
        st.info(
            "Each unit in Pathway 3 will have advanced labs and production-style mini projects. "
            "Tutors can adapt these to local datasets and infrastructure."
        )

        selected_unit = st.selectbox(
            "Choose a unit to view high-level lab ideas:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_p3_labs_unit",
        )
        st.markdown(f"### Unit {selected_unit}: {UNITS[selected_unit]['name']}")

        if selected_unit == 1:
            st.markdown(
                """These labs focus on taking feature engineering skills to a
**production-ready** level.

- **Lab 1 – From ad-hoc notebook to reusable feature pipeline**
  - Start from a Pathway 2 feature notebook.
  - Refactor the code into clear functions or a small library.
  - Add basic tests or assertions for key assumptions (e.g. no future
    dates, valid ranges).

- **Lab 2 – Designing a shared feature table**
  - Sketch a feature table that could support multiple models (e.g.
    churn, readmission, upsell).
  - Write down clear column definitions, data types and refresh cadence.
  - Identify which upstream tables feed into this feature table.

- **Mini project – Point-in-time safe feature dataset**
  - Take a transactional dataset with timestamps.
  - Build a small feature pipeline that guarantees "no future leakage"
    when you simulate training vs scoring days.
  - Document your approach so another engineer could re-implement it.
"""
            )
            st.info(
                "Use notebook `U1_advanced_feature_pipelines.ipynb` in "
                "`data_science_pathway3/notebooks` as a starting point for these labs."
            )
        elif selected_unit == 2:
            st.markdown(
                """These labs emphasise **systematic experiment tracking** and
fair comparison of models.

- **Lab 1 – Designing a minimal experiment log schema**
  - Decide which fields you will log for each run (params, data version,
    metrics, notes).
  - Implement a simple logging helper (e.g. writing JSON or CSV rows).
  - Run a few experiments and confirm they are recorded consistently.

- **Lab 2 – Comparing several model families fairly**
  - Pick a problem from Pathway 2 (regression or classification).
  - Train and log at least three model types (e.g. linear, random forest,
    gradient boosting) using the same validation strategy.
  - Produce a small comparison table or plot from the logged results.

- **Mini project – Reproducible model report**
  - Choose a "best" model based on your experiments.
  - Write a short report that cites the experiment runs, metrics and
    configuration used.
"""
            )
            st.info(
                "Use notebook `U2_experiment_tracking_model_selection.ipynb` in "
                "`data_science_pathway3/notebooks` as a starting point for these labs."
            )
        elif selected_unit == 3:
            st.markdown(
                """These labs focus on **advanced supervised models** and how to
evaluate them responsibly.

- **Lab 1 – Baselines vs advanced models**
  - Start from a Pathway 2 classification or regression problem.
  - Train simple baselines (logistic/linear, small tree).
  - Train at least one boosting model and one random forest.
  - Compare performance across multiple validation folds.

- **Lab 2 – Exploring model behaviour**
  - Inspect feature importances or similar summaries.
  - For a handful of example records, compare predictions from baseline
    vs advanced models.
  - Document where the advanced model helps and where it might be
    risky.

- **Mini project – Calibrated risk model**
  - Take a binary classification task (e.g. risk score).
  - Train an advanced model and assess calibration (e.g. via a
    reliability curve or binned analysis).
  - Propose threshold(s) and a monitoring plan for probability drift.
"""
            )
            st.info(
                "Use notebook `U3_advanced_supervised_ensembles.ipynb` in "
                "`data_science_pathway3/notebooks` as a starting point for these labs."
            )
        elif selected_unit == 4:
            st.markdown(
                """These labs emphasise **practical forecasting** for operations
questions.

- **Lab 1 – Baseline vs simple model**
  - Take a univariate time series (e.g. daily demand or admissions).
  - Implement naïve and moving-average baselines.
  - Implement at least one simple forecasting model (e.g. ARIMA-style or
    boosted trees on lag features).
  - Compare performance across several forecast horizons.

- **Lab 2 – Rolling-window evaluation**
  - Set up a rolling-origin evaluation loop.
  - Record error metrics at each step and visualise how they change.
  - Identify periods where the model struggles (e.g. holidays, shocks).

- **Mini project – Forecasting for a capacity decision**
  - Frame an operations question (e.g. staffing a clinic or call centre).
  - Build a small forecasting experiment and summarise results for a
    non-technical stakeholder.
"""
            )
            st.info(
                "Use notebook `U4_time_series_forecasting_ops.ipynb` in "
                "`data_science_pathway3/notebooks` to run these forecasting labs."
            )
        elif selected_unit == 5:
            st.markdown(
                """These labs focus on turning code and models into **reliable
artefacts** that others can run.

- **Lab 1 – Defining a reproducible environment**
  - Take an existing project from Pathway 2.
  - Write a clear dependency specification (e.g. `requirements.txt`).
  - Create and test a fresh environment using only that spec.

- **Lab 2 – Packaging a batch scoring job**
  - Wrap a trained pipeline in a simple CLI script (conceptually) that
    reads input data and writes scored output.
  - Add basic configuration for input/output paths and model location.

- **Mini project – CI/CD sketch for a small ML project**
  - Draw or describe a minimal CI/CD workflow for retraining and
    deploying a model.
  - Identify which checks/tests you would run before promotion.
"""
            )
            st.info(
                "Use notebook `U5_packaging_and_cicd.ipynb` in "
                "`data_science_pathway3/notebooks` as a design space for these labs."
            )
        elif selected_unit == 6:
            st.markdown(
                """These labs emphasise **monitoring and responsible AI**.

- **Lab 1 – Designing monitoring signals**
  - For a chosen model, list key data and performance metrics to track.
  - Sketch simple charts or alerts you would configure.

- **Lab 2 – Segment analysis for fairness**
  - Simulate or use real subgroup labels (e.g. region, age band).
  - Compare performance metrics across segments.
  - Document any concerning gaps and potential mitigations.

- **Mini project – Incident playbook outline**
  - Write a short "incident response" checklist for when a model drifts
    or behaves unexpectedly.
"""
            )
            st.info(
                "Use notebook `U6_monitoring_drift_responsible_ai.ipynb` in "
                "`data_science_pathway3/notebooks` when working through these labs."
            )
        elif selected_unit == 7:
            st.markdown(
                """Use these milestones to structure your Pathway 3 capstone.

- **Milestone 1 – Problem & context**
  - Define a realistic problem, stakeholders and constraints.
  - Clarify what "good" looks like (metrics, business impact).

- **Milestone 2 – Data & features**
  - Design and implement your feature pipeline.
  - Document data sources and any assumptions.

- **Milestone 3 – Experiments & model choice**
  - Run and log experiments across several model families.
  - Justify your chosen model based on evidence.

- **Milestone 4 – Deployment & monitoring sketch**
  - Describe how the model would be packaged and deployed.
  - Outline monitoring, drift checks and responsible AI safeguards.
"""
            )
            st.info(
                "Use notebook `U7_production_capstone_template.ipynb` in "
                "`data_science_pathway3/notebooks` as the main workspace for your capstone."
            )
        else:
            st.markdown(
                "Detailed lab descriptions for this unit will be added in a later "
                "build, following the same style as Pathway 2 (clear, practical, "
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
                key="ds_p3_assessment_unit",
            )
            render_evidence_submission_form(learner_email, COURSE_ID, assessment_unit)

        st.markdown("---")
        st.markdown("### ✅ Quick-check quizzes (Units 1–7)")
        st.caption(
            "Short multiple-choice quizzes for each unit will be added here, mirroring the Pathway 2 style."
        )

        # Simple scaffold quiz for Unit 1 so learners have immediate checks.
        quiz_unit = st.selectbox(
            "Choose a unit for a quick-check quiz:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_p3_quiz_unit_select",
        )

        questions: Dict[int, list] = {
            1: [
                {
                    "text": "Why is point-in-time correctness important for production features?",
                    "options": [
                        "It makes queries faster",
                        "It prevents models from accidentally using information from the future",
                        "It reduces storage costs",
                        "It guarantees 100% accuracy",
                    ],
                    "answer": 1,
                    "explanation": "Point-in-time correctness avoids future leakage when training and scoring models.",
                },
                {
                    "text": "What is a key advantage of a shared feature table used by multiple models?",
                    "options": [
                        "Each team must write their own version",
                        "It increases duplication",
                        "It promotes consistency and reuse across models",
                        "It makes debugging impossible",
                    ],
                    "answer": 2,
                    "explanation": "Shared feature tables or stores reduce duplication and keep definitions consistent.",
                },
            ],
            2: [
                {
                    "text": "Which of the following is the main purpose of experiment tracking?",
                    "options": [
                        "Making models train faster",
                        "Keeping a structured record of runs, parameters and metrics",
                        "Encrypting data at rest",
                        "Reducing cloud costs",
                    ],
                    "answer": 1,
                    "explanation": "Experiment tracking lets you reproduce and compare runs reliably.",
                },
                {
                    "text": "Why is it useful to log data versions alongside metrics?",
                    "options": [
                        "Because metrics are meaningless without knowing which data they came from",
                        "To reduce the size of logs",
                        "To hide model performance",
                        "It is never necessary",
                    ],
                    "answer": 0,
                    "explanation": "Knowing data versions is essential when interpreting and reproducing results.",
                },
            ],
            3: [
                {
                    "text": "Why is it important to compare advanced models against strong baselines?",
                    "options": [
                        "To make experiments slower",
                        "To see whether extra complexity really delivers better performance",
                        "To avoid logging metrics",
                        "Baselines are never needed once you use boosting",
                    ],
                    "answer": 1,
                    "explanation": "Without baselines you cannot judge whether complex models are worth the added cost and risk.",
                },
                {
                    "text": "What does probability calibration aim to improve?",
                    "options": [
                        "The ranking of examples only",
                        "The match between predicted probabilities and observed frequencies",
                        "The size of the dataset",
                        "The speed of training",
                    ],
                    "answer": 1,
                    "explanation": "Calibration is about predicted probabilities reflecting true outcome frequencies.",
                },
            ],
            4: [
                {
                    "text": "Why are random train/test splits often a bad idea for time-series forecasting?",
                    "options": [
                        "They make models too slow",
                        "They can leak future information into the training set",
                        "They reduce the number of samples",
                        "They always improve accuracy",
                    ],
                    "answer": 1,
                    "explanation": "Random splits can mix past and future, leading to overly optimistic estimates.",
                },
                {
                    "text": "What is a key goal of rolling-origin evaluation?",
                    "options": [
                        "To shuffle the data",
                        "To test the model on future periods as they would appear in production",
                        "To reduce the need for metrics",
                        "To ignore seasonality",
                    ],
                    "answer": 1,
                    "explanation": "Rolling-origin evaluation mimics repeated training on the past and forecasting the next block.",
                },
            ],
            5: [
                {
                    "text": "What is the main purpose of using a dependency specification like requirements.txt?",
                    "options": [
                        "To make code run faster",
                        "To record which libraries and versions a project depends on",
                        "To encrypt model weights",
                        "To automatically tune hyperparameters",
                    ],
                    "answer": 1,
                    "explanation": "A clear dependency spec lets others recreate a compatible environment.",
                },
                {
                    "text": "Which of the following best describes CI/CD for ML projects?",
                    "options": [
                        "Running training only on local laptops",
                        "Automating tests and deployment steps so changes can be delivered safely and repeatedly",
                        "Storing all models in a single notebook",
                        "Avoiding any tests to move faster",
                    ],
                    "answer": 1,
                    "explanation": "CI/CD brings discipline to how models and code are tested and promoted across environments.",
                },
            ],
            6: [
                {
                    "text": "Which of the following is a key reason to monitor model performance over time?",
                    "options": [
                        "To increase training time",
                        "To detect degradation as data or behaviour changes",
                        "To avoid collecting metrics",
                        "To guarantee the model never needs retraining",
                    ],
                    "answer": 1,
                    "explanation": "Performance monitoring helps you see when the model no longer behaves as expected.",
                },
                {
                    "text": "Why is it important to look at metrics by subgroup (e.g. region, age band)?",
                    "options": [
                        "To make dashboards more complex",
                        "To understand whether the model is performing very differently for different groups",
                        "To reduce the number of charts",
                        "It is never useful",
                    ],
                    "answer": 1,
                    "explanation": "Segmented metrics can reveal fairness or quality issues that averages hide.",
                },
            ],
            7: [
                {
                    "text": "Which combination best describes a strong Pathway 3 capstone?",
                    "options": [
                        "Toy dataset and no documentation",
                        "Realistic problem, tracked experiments, deployment & monitoring sketch",
                        "Only a model file with no context",
                        "A slide with buzzwords only",
                    ],
                    "answer": 1,
                    "explanation": "A Pathway 3 capstone should show end-to-end thinking from problem to monitoring.",
                },
                {
                    "text": "Why should the capstone explicitly discuss risks and limitations?",
                    "options": [
                        "To make the report longer",
                        "To demonstrate mature judgement about where the model should and should not be used",
                        "To hide weaknesses",
                        "It is not needed at advanced level",
                    ],
                    "answer": 1,
                    "explanation": "Being clear about risks and limits is essential for responsible advanced practice.",
                },
            ],
        }

        qs = questions.get(quiz_unit, [])
        answers = []
        for idx, q in enumerate(qs, start=1):
            st.markdown(f"**Q{idx}. {q['text']}**")
            choice = st.radio(
                label=f"p3_u{quiz_unit}_q{idx}",
                options=list(range(len(q["options"]))),
                format_func=lambda i, opts=q["options"]: opts[i],
                key=f"ds_p3_u{quiz_unit}_q{idx}",
            )
            answers.append(choice)

        if qs and st.button("Mark Pathway 3 quiz", key="ds_p3_quiz_mark"):
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
            """This area will host advanced study plans, checklists and deployment
runbooks for Pathway 3.

Tutors/admins can also host additional documents in the main LMS materials
system (e.g. architecture diagrams, MLOps runbooks, responsible AI policies).
"""
        )

        st.markdown("---")
        st.markdown("### 📥 Download core documents as PDF")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("📥 Pathway 3 study plan PDF", key="dsp3_study_plan_pdf"):
                study_plan_md = """# Data Science Pathway 3 – 10–12 Week Study Plan

This plan assumes around **10–12 weeks** of part-time study for learners
who have already completed Pathway 2 or have equivalent experience.

---

## Weeks 1–2 – Unit 1: Advanced Feature Engineering & Pipelines at Scale

- Revisit Pathway 2 feature notebooks and identify limitations for
  production use.
- Design a multi-model feature table and document keys/timestamps.
- Work through Unit 1 labs and mini project.
- Capture open questions about feature stores and governance.

## Weeks 2–3 – Unit 2: Experiment Tracking & Model Selection

- Choose a project from Pathway 2 as a case study.
- Design an experiment logging schema (what to log and where).
- Log several runs across model families and compare results.
- Complete Unit 2 labs and quick-check quiz.

## Weeks 3–4 – Unit 3: Advanced Supervised Models & Ensembles

- Implement at least one boosting model and one random forest.
- Benchmark them carefully against strong baselines.
- Explore calibration and interpretability for your chosen problem.
- Complete Unit 3 labs and quick-check quiz.

## Weeks 4–5 – Unit 4: Time-series Forecasting for Operations

- Select a realistic time-series (demand, admissions, usage).
- Build baseline and simple forecasting models.
- Implement a rolling-origin evaluation loop.
- Complete Unit 4 labs and quick-check quiz.

## Weeks 5–6 – Unit 5: Packaging, Environments & CI/CD for ML

- Create or refine a dependency specification for one project.
- Sketch a batch scoring job and simple service-style deployment.
- Draft a minimal CI/CD pipeline design.
- Complete Unit 5 labs and quick-check quiz.

## Weeks 6–7 – Unit 6: Monitoring, Drift & Responsible AI

- Define monitoring signals for at least one model.
- Design simple dashboards or alert rules for key metrics.
- Run a subgroup/fairness analysis (even if with synthetic labels).
- Complete Unit 6 labs and quick-check quiz.

## Weeks 7–10+ – Unit 7: Advanced Production-style Capstone

- Choose a problem and dataset with real operational flavour.
- Build a robust training + evaluation workflow using Pathway 3 tools.
- Produce a deployment & monitoring sketch that could be handed to an
  engineering team.
- Prepare final notebook/script, report/slides, and optional demo.

Learners who want a **flagship portfolio project** are encouraged to
spend additional weeks polishing the Pathway 3 capstone.
"""
                pdf = create_unit_pdf(0, "Pathway 3 Study Plan", study_plan_md)
                st.download_button(
                    label="Download Study Plan PDF",
                    data=pdf,
                    file_name="Data_Science_Pathway3_Study_Plan.pdf",
                    mime="application/pdf",
                    key="dsp3_study_plan_pdf_dl",
                )

        with col_b:
            if st.button(
                "📥 Pathway 3 checklists PDF", key="dsp3_checklists_pdf"
            ):
                checklists_md = """# Data Science Pathway 3 – Unit Checklists

Use these checklists to track readiness for **advanced, production-style
work**. They are guidance, not formal assessment criteria.

---

## Unit 1 – Advanced Feature Engineering & Pipelines at Scale

- [ ] I can design feature tables that support multiple models.
- [ ] I understand point-in-time correctness and future leakage.
- [ ] I can explain how late-arriving data and backfills affect features.
- [ ] I can sketch how a feature store or shared feature library works.

## Unit 2 – Experiment Tracking & Model Selection

- [ ] I can describe what should be logged for each experiment run.
- [ ] I can design a simple experiment log schema.
- [ ] I can compare model families using consistent validation.
- [ ] I understand how tracking supports reproducibility and audit.

## Unit 3 – Advanced Supervised Models & Ensembles

- [ ] I can implement at least one boosting model and one random forest.
- [ ] I always compare advanced models against strong baselines.
- [ ] I understand the idea of probability calibration.
- [ ] I can communicate complex model behaviour in plain language.

## Unit 4 – Time-series Forecasting for Operations

- [ ] I can build and evaluate simple forecasting baselines.
- [ ] I understand trend, seasonality and external covariates.
- [ ] I can implement a rolling-origin evaluation.
- [ ] I can relate forecast quality to an operational decision.

## Unit 5 – Packaging, Environments & CI/CD for ML

- [ ] I can specify dependencies for a project in a reproducible way.
- [ ] I understand the role of virtual environments or containers.
- [ ] I can sketch how a model would be packaged for batch or service
      deployment.
- [ ] I can describe a minimal CI/CD workflow for ML.

## Unit 6 – Monitoring, Drift & Responsible AI

- [ ] I can list key data and performance signals to monitor over time.
- [ ] I understand the difference between feature drift and label drift.
- [ ] I can analyse metrics by subgroup to look for fairness issues.
- [ ] I can outline an incident response plan for a drifting model.

## Unit 7 – Advanced Production-style Capstone

- [ ] I have chosen a realistic, well-scoped problem and dataset.
- [ ] I have tracked experiments and justified my chosen model.
- [ ] I have outlined deployment, monitoring and responsible AI
      considerations.
- [ ] I have prepared a portfolio-ready notebook/script and report.
"""
                pdf = create_unit_pdf(0, "Pathway 3 Checklists", checklists_md)
                st.download_button(
                    label="Download Checklists PDF",
                    data=pdf,
                    file_name="Data_Science_Pathway3_Unit_Checklists.pdf",
                    mime="application/pdf",
                    key="dsp3_checklists_pdf_dl",
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
                    key=f"ds_pathway3_progress_unit_{unit_number}",
                )

    # Certificate
    with tabs[7]:
        st.subheader("🎓 Certificate")
        st.info(
            "On successful completion of all units and assessments, learners receive a "
            "T21 Data Science Pathway 3 (Advanced ML & MLOps) certificate, where offered by "
            "their training provider."
        )

        st.markdown(
            """### Requirements for completion

- Complete and submit evidence for all 7 units
- Demonstrate competence in advanced ML, evaluation and basic MLOps concepts
- Complete at least one production-style ML capstone project
- Meet internal quality standards set by tutors/assessors
"""
        )

        if enrollment and enrollment.get("progress", 0) >= 100:
            st.success(
                "All requirements appear to be complete. Your training provider can now "
                "issue your Data Science Pathway 3 certificate."
            )
        else:
            st.info(
                "Keep working through your units and projects. Once everything is complete, "
                "your tutor will confirm and issue your certificate."
            )
