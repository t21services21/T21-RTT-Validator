import streamlit as st
from typing import Dict, Any

COURSE_ID = "data_science_pathway_2"
COURSE_NAME = "Data Science Pathway 2 (Intermediate ML)"

UNITS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Feature Engineering & Data Pipelines",
        "level": "Intermediate",
        "glh": 24,
        "credits": 4,
    },
    2: {
        "name": "Supervised Learning: Regression",
        "level": "Intermediate",
        "glh": 24,
        "credits": 4,
    },
    3: {
        "name": "Supervised Learning: Classification",
        "level": "Intermediate",
        "glh": 24,
        "credits": 4,
    },
    4: {
        "name": "Model Evaluation & Validation",
        "level": "Intermediate",
        "glh": 18,
        "credits": 3,
    },
    5: {
        "name": "Unsupervised Learning & Segmentation",
        "level": "Intermediate",
        "glh": 18,
        "credits": 3,
    },
    6: {
        "name": "Deploying & Operationalising Models",
        "level": "Intermediate",
        "glh": 18,
        "credits": 3,
    },
    7: {
        "name": "Pathway 2 Capstone Project",
        "level": "Intermediate",
        "glh": 36,
        "credits": 6,
    },
}


def _render_unit1_learning_materials():
    """Detailed theory content for Unit 1: Feature Engineering & Data Pipelines."""

    st.markdown("### Unit 1: Feature Engineering & Data Pipelines")
    st.caption("Level: Intermediate • Suggested hours: 24 • Suggested credits: 4")

    st.markdown("#### 📘 What is feature engineering?")
    st.markdown(
        """Most real-world datasets are **not** ready to plug straight into a
machine learning model. They contain:

- Missing values
- Free-text fields
- Categorical labels instead of numbers
- Timestamps and IDs

**Feature engineering** is the process of taking that messy, raw data and
turning it into a clean table of model-ready features that capture useful
signal for the problem you care about.

Good feature engineering often has **more impact** on performance and
robustness than trying many fancy algorithms.
"""
    )

    st.markdown("#### 🔁 The feature pipeline mindset")
    st.markdown(
        """In Pathway 1 you cleaned data mainly for analysis. In Pathway 2 you
need a **repeatable pipeline** that can run every time new data arrives.

A simple feature pipeline usually has steps such as:

1. **Select raw columns** you need from source tables.
2. **Handle missing values** (impute, flag, or drop carefully).
3. **Encode categoricals** (one-hot, target encoding, etc.).
4. **Scale numeric features** where needed.
5. **Create derived features** that capture business logic
   (ratios, rolling averages, days since event, etc.).

Modern libraries such as **scikit-learn** let you package these steps into a
`Pipeline` or `ColumnTransformer` so the exact same logic is applied during
training and when you score new data.
"""
    )

    st.markdown("#### 🧹 Handling missing values")
    st.markdown(
        """Missing data is normal in healthcare, finance and most other
domains. The key is to be **deliberate**:

- For numeric features you can use strategies like mean/median imputation
  and often add a **"was_missing" flag** as a separate feature.
- For categoricals you might create a special `"Unknown"` or `"Missing"`
  category instead of dropping rows.
- Sometimes missingness itself carries signal (e.g. not attending an
  appointment) – your features should allow the model to learn from that.

You should **never silently drop half your dataset** without thinking about
what those rows represent in the real process.
"""
    )

    st.markdown("#### 🔡 Encoding categorical variables")
    st.markdown(
        """Most models cannot work directly with strings, so we convert
categorical variables to numbers.

Common approaches:

- **One-hot encoding** – create binary columns such as
  `country_UK`, `country_US`, `country_NG`.
- **Ordinal encoding** – map categories to integers when the order has
  meaning (e.g. education level).
- **Target or mean encoding** – replace categories with a summary
  statistic from the target (used carefully to avoid leakage).

In scikit-learn you typically use `OneHotEncoder` inside a
`ColumnTransformer` so it becomes part of the overall pipeline.
"""
    )

    st.markdown("#### 📏 Scaling numeric features")
    st.markdown(
        """Some models (like linear models and neural networks) behave better
when numeric features are on similar scales.

You can use:

- **StandardScaler** – subtract mean, divide by standard deviation.
- **MinMaxScaler** – map values to a fixed range such as [0, 1].

Tree-based models (random forests, gradient boosting) are **less
sensitive** to scaling, but it is still good practice when mixing them with
other algorithms or distance-based methods.
"""
    )

    st.markdown("#### 🧱 Creating business-aware features")
    st.markdown(
        """Strong features often come from domain understanding, not
mathematics alone. Examples:

- Ratio features: `readmissions / total_admissions`,
  `claims_amount / income`.
- Time features: `days_since_last_visit`, `hour_of_day`, `is_weekend`.
- Aggregations: average lab values over the last 3 months, total spend in
  the last 90 days.

In this unit you will practice turning a messy transactional dataset into a
compact table of features that a model can learn from.
"""
    )

    st.markdown("#### 🧪 Train/validation/test splits and leakage")
    st.markdown(
        """When building pipelines it is critical to avoid **data leakage** –
using information from the future or from the validation set inside your
training transformations.

Good practice:

- Split into **train/validation/test** first.
- Fit all preprocessing steps using **only the training data**.
- Apply the fitted transformers to validation and test sets.

In scikit-learn, fitting a `Pipeline` on the training set automatically
ensures that the parameters of each step (like means for scaling) are
learned only from the training portion.
"""
    )


def _render_unit1_labs():
    """Labs and mini-project ideas for Unit 1."""

    st.markdown("### 🧪 Labs & Mini Projects – Unit 1")
    st.markdown(
        """These labs assume you already know basic Pandas and Python from
Pathway 1. The focus here is on **turning raw tables into reusable
pipelines**.

- **Lab 1 – From raw CSVs to a clean feature table**
  - Load a raw dataset with demographics and activity (e.g. customer or
    patient events).
  - Identify missing values, categorical columns and numeric columns.
  - Build a script or notebook that outputs a clean `features.csv` ready
    for modelling.

- **Lab 2 – Build a scikit-learn preprocessing pipeline**
  - Use `ColumnTransformer` and `Pipeline` to:
    - Impute missing numeric values.
    - One-hot encode categoricals.
    - Scale selected numeric features.
  - Save the fitted pipeline to disk for later reuse.

- **Mini project – Compare "hand-made" vs pipeline approach**
  - Train a simple model twice:
    - Once using ad-hoc cleaning code.
    - Once using a well-defined pipeline.
  - Compare maintainability and risk of leakage.
  - Write a short note explaining why the pipeline version is better for
    production.
"""
    )
    """Quick-check multiple-choice quiz for Unit 1."""

    st.markdown("### Quick-check quiz – Unit 1")
    st.caption("Use this short quiz to check your understanding of feature engineering and pipelines.")

    questions = [
        {
            "text": "What is the main goal of feature engineering?",
            "options": [
                "Collect as many raw columns as possible",
                "Turn raw data into informative, model-ready features",
                "Replace models with dashboards",
                "Avoid cleaning data",
            ],
            "answer": 1,
            "explanation": "Feature engineering creates useful inputs for models.",
        },
        {
            "text": "Which step should usually happen FIRST when building a pipeline?",
            "options": [
                "Train the model and then split the data",
                "Split into train/validation/test, then fit transformers on the training data",
                "Impute missing values on the full dataset before splitting",
                "Scale features using statistics from the test set",
            ],
            "answer": 1,
            "explanation": "Split first, then fit preprocessing on the training data.",
        },
        {
            "text": "Which is a good reason to use one-hot encoding?",
            "options": [
                "To convert free-text notes into a single number",
                "To represent categorical values as binary indicator columns",
                "To remove all categorical columns",
                "To scale numeric features",
            ],
            "answer": 1,
            "explanation": "One-hot encoding turns categories into binary features.",
        },
        {
            "text": "What is data leakage?",
            "options": [
                "Storing data without encryption",
                "Using information from validation/test sets inside training transformations or labels",
                "Making backups of the database",
                "Dropping missing values",
            ],
            "answer": 1,
            "explanation": "Leakage happens when future or validation information affects training.",
        },
        {
            "text": "Which of these is an example of a business-aware feature?",
            "options": [
                "A random number between 0 and 1",
                "Days since last appointment",
                "Row index",
                "The string representation of an ID",
            ],
            "answer": 1,
            "explanation": "Days since last appointment relates to engagement or risk.",
        },
    ]

    answers = []
    for idx, q in enumerate(questions, start=1):
        st.markdown(f"**Q{idx}. {q['text']}**")
        choice = st.radio(
            label=f"u1_q{idx}",
            options=list(range(len(q["options"]))),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"ds_p2_u1_q{idx}",
        )
        answers.append(choice)

    if st.button("Mark Unit 1 quiz", key="ds_p2_u1_quiz_mark"):
        score = sum(1 for ua, q in zip(answers, questions) if ua == q["answer"])
        total = len(questions)
        st.success(f"You scored {score} out of {total} on Unit 1 quick-check quiz.")

        if total:
            for idx, (ua, q) in enumerate(zip(answers, questions), start=1):
                if ua != q["answer"]:
                    correct = q["options"][q["answer"]]
                    explanation = q.get("explanation", "")
                    st.warning(f"Q{idx}: Correct answer is '{correct}'. {explanation}")

        if total > 0 and score == total:
            st.balloons()


def _render_unit5_learning_materials():
    """Detailed theory content for Unit 5: Unsupervised Learning & Segmentation."""

    st.markdown("### Unit 5: Unsupervised Learning & Segmentation")
    st.caption("Level: Intermediate • Suggested hours: 18 • Suggested credits: 3")

    st.markdown("#### 📘 What is unsupervised learning?")
    st.markdown(
        """In unsupervised learning you **do not have labels** like churn
or revenue. Instead, you look for structure in the features themselves.

Common goals:

- Group similar observations together (clustering).
- Reduce dimensionality to simpler representations.
- Discover patterns or segments that are useful for decisions.
"""
    )

    st.markdown("#### 👥 Clustering and segmentation")
    st.markdown(
        """Clustering algorithms group observations based on similarity.

Typical business use: **segmentation** – e.g. customer segments, patient
profiles, facility types.

Popular approaches:

- **k-means** – partitions data into k clusters, each with a centroid.
- **Hierarchical clustering** – builds a tree of clusters.
- **DBSCAN** – density-based, can find irregular-shaped clusters and
  identify noise.
"""
    )

    st.markdown("#### 📏 Distance, scaling and features")
    st.markdown(
        """Most clustering algorithms rely on some notion of **distance** or
similarity between points.

This makes feature engineering and scaling critical:

- Features with large scales can dominate distance calculations.
- Including irrelevant features can hide real structure.

You should usually reuse your pipelines (imputation, encoding, scaling)
from earlier units before clustering.
"""
    )

    st.markdown("#### 📊 Evaluating clusters")
    st.markdown(
        """Unsupervised models do not have labels, so evaluation is more
subjective.

You can use:

- **Internal metrics** like silhouette score.
- **Stability checks** – do clusters look similar across samples?
- **Business validation** – do segments make sense to domain experts?

The key is whether the segments support better decisions or insights, not
just high internal scores.
"""
    )


def _render_unit5_labs():
    """Labs and mini-project ideas for Unit 5."""

    st.markdown("### 🧪 Labs & Mini Projects – Unit 5")
    st.markdown(
        """These labs focus on using clustering for practical segmentation.

- **Lab 1 – Customer or patient segmentation with k-means**
  - Choose a dataset with entities (customers, patients, locations).
  - Build a preprocessing pipeline (handle missing values, encode
    categoricals, scale features).
  - Apply k-means for several values of k.
  - Inspect cluster centroids and basic metrics (e.g. silhouette score).

- **Lab 2 – Interpreting and labelling segments**
  - Profile each cluster: average values, distributions, key differences.
  - Give each cluster a descriptive business label (e.g. "high-usage
    digital", "low-engagement occasional").

- **Mini project – Segmentation for a decision**
  - Design a simple strategy that uses segments (e.g. tailored
    communication, targeted support).
  - Prepare a short slide or document explaining segments and how they
    should influence actions.
"""
    )


def _render_unit5_quiz():
    """Quick-check multiple-choice quiz for Unit 5."""

    st.markdown("### ✅ Quick-check quiz – Unit 5")
    st.caption(
        "Use this quiz to check your understanding of unsupervised learning and segmentation."
    )

    questions = [
        {
            "text": "What is a key difference between supervised and unsupervised learning?",
            "options": [
                "Supervised learning does not use features",
                "Unsupervised learning does not use labelled targets",
                "Unsupervised learning cannot be used for real problems",
                "There is no difference",
            ],
            "answer": 1,
            "explanation": "In unsupervised learning you typically do not have labels such as churn or revenue.",
        },
        {
            "text": "Which algorithm is commonly used for segmentation via clustering?",
            "options": ["Linear regression", "k-means", "Logistic regression", "Naive Bayes"],
            "answer": 1,
            "explanation": "k-means is a widely used clustering algorithm for segmentation tasks.",
        },
        {
            "text": "Why is feature scaling important before applying distance-based clustering?",
            "options": [
                "To increase the number of clusters",
                "To prevent features with large scales from dominating the distance calculation",
                "To remove all categorical variables",
                "To avoid needing a pipeline",
            ],
            "answer": 1,
            "explanation": "If features are on very different scales, those with larger values can dominate distance-based methods.",
        },
        {
            "text": "Which of the following is an example of business validation of clusters?",
            "options": [
                "Checking the Python version",
                "Asking domain experts whether the segments make sense and match their experience",
                "Counting the number of columns",
                "Using accuracy as the only metric",
            ],
            "answer": 1,
            "explanation": "Clusters are useful when they support real decisions; expert feedback is crucial.",
        },
        {
            "text": "What is a typical use case for segmentation?",
            "options": [
                "Encrypting a database",
                "Tailoring communication or interventions to different groups",
                "Replacing all supervised models",
                "Measuring code quality",
            ],
            "answer": 1,
            "explanation": "Segmentation is often used to target different actions or messages to different groups.",
        },
    ]

    answers = []
    for idx, q in enumerate(questions, start=1):
        st.markdown(f"**Q{idx}. {q['text']}**")
        choice = st.radio(
            label=f"u5_q{idx}",
            options=list(range(len(q["options"]))),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"ds_p2_u5_q{idx}",
        )
        answers.append(choice)

    if st.button("Mark Unit 5 quiz", key="ds_p2_u5_quiz_mark"):
        score = sum(1 for ua, q in zip(answers, questions) if ua == q["answer"])
        total = len(questions)
        st.success(f"You scored {score} out of {total} on Unit 5 quick-check quiz.")

        if total:
            for idx, (ua, q) in enumerate(zip(answers, questions), start=1):
                if ua != q["answer"]:
                    correct = q["options"][q["answer"]]
                    explanation = q.get("explanation", "")
                    st.warning(f"Q{idx}: Correct answer is '{correct}'. {explanation}")

        if total > 0 and score == total:
            st.balloons()


def _render_unit6_learning_materials():
    """Detailed theory content for Unit 6: Deploying & Operationalising Models."""

    st.markdown("### Unit 6: Deploying & Operationalising Models")
    st.caption("Level: Intermediate • Suggested hours: 18 • Suggested credits: 3")

    st.markdown("#### 📘 From notebook to real-world use")
    st.markdown(
        "So far you have focused on building and evaluating models. Deployment is about making a model **available to real users or systems** in a safe, reliable way.\n\n"
        "Common deployment targets include:\n\n"
        "- Batch scoring jobs (e.g. daily churn scores).\n"
        "- Real-time APIs (e.g. risk score when a form is submitted).\n"
        "- Embedded models in BI tools or internal apps (e.g. Streamlit dashboards)."
    )

    st.markdown("#### 🧱 Packaging models and pipelines")
    st.markdown(
        "Your feature engineering and model should be treated as a single **artifact**:\n\n"
        "- Use scikit-learn `Pipeline` so preprocessing + model stay together.\n"
        "- Save the trained pipeline using a format like `joblib` or `pickle`.\n"
        "- Track the exact data schema and versions used for training.\n\n"
        "This reduces the risk that production data is transformed differently from training data."
    )

    st.markdown("#### 🌐 Simple deployment patterns")
    st.markdown(
        "You will explore lightweight deployment patterns suitable for many organisations:\n\n"
        "- **Batch scoring scripts** scheduled via cron or enterprise schedulers.\n"
        "- **Simple web apps** (e.g. Streamlit) where users upload data or interact with forms.\n"
        "- **HTTP APIs** using frameworks like FastAPI or Flask (conceptual level only here).\n\n"
        "The emphasis in this unit is on **clarity, monitoring and safety**, not on building complex infrastructure."
    )

    st.markdown("#### 📡 Monitoring and feedback loops")
    st.markdown(
        "Once a model is in use you need to monitor:\n\n"
        "- Data quality – are incoming features still in expected ranges?\n"
        "- Performance – are key metrics stable over time?\n"
        "- Drift – has the relationship between inputs and outcomes changed?\n\n"
        "You also need feedback loops so that new labelled data can be used to **retrain** or update the model on a sensible schedule."
    )


def _render_unit6_labs():
    """Labs and mini-project ideas for Unit 6."""

    st.markdown("### 🧪 Labs & Mini Projects – Unit 6")
    st.markdown(
        "These labs focus on turning a working model into something that could be used by others.\n\n"
        "- **Lab 1 – Saving and loading a trained pipeline**\n"
        "  - Take a pipeline + model from an earlier unit.\n"
        "  - Save it to disk using `joblib` or `pickle`.\n"
        "  - Write a small script that loads the pipeline and scores new data from a CSV file.\n\n"
        "- **Lab 2 – Simple prediction app or script**\n"
        "  - Build a tiny CLI tool or Streamlit app where a user can input features (or upload a file) and receive predictions.\n"
        "  - Include basic validation and user guidance.\n\n"
        "- **Mini project – Deployment and monitoring plan**\n"
        "  - Choose one of your earlier models.\n"
        "  - Draft a short document describing how it would be deployed, who would use it, how it would be monitored and how often it would be retrained."
    )


def _render_unit6_quiz():
    """Quick-check multiple-choice quiz for Unit 6."""

    st.markdown("### ✅ Quick-check quiz – Unit 6")
    st.caption(
        "Use this quiz to check your understanding of deployment and operationalisation basics."
    )

    questions = [
        {
            "text": "What is the main purpose of packaging preprocessing and the model into a single Pipeline when deploying?",
            "options": [
                "To reduce training time",
                "To ensure the same transformations are applied in training and when scoring new data",
                "To avoid saving the model",
                "To automatically balance the classes",
            ],
            "answer": 1,
            "explanation": "Pipelines help guarantee that production data is processed in exactly the same way as training data.",
        },
        {
            "text": "Which of the following is an example of a simple deployment pattern?",
            "options": [
                "Re-training the model after every prediction",
                "A daily batch script that loads a saved pipeline and scores new data",
                "Editing the model weights manually in Excel",
                "Storing the model only in a notebook with no way to reuse it",
            ],
            "answer": 1,
            "explanation": "Batch scoring with a saved pipeline is a common and practical deployment pattern.",
        },
        {
            "text": "Why is monitoring important after deployment?",
            "options": [
                "To check that the Python version is correct",
                "To detect data quality issues, performance changes and possible drift over time",
                "To reduce the number of users",
                "To avoid having to retrain the model",
            ],
            "answer": 1,
            "explanation": "Monitoring helps you see whether the model is still reliable and whether the input data has changed.",
        },
        {
            "text": "Which of these is a reasonable artefact to save from a training run for later deployment?",
            "options": [
                "Only the raw training data",
                "The fitted preprocessing + model pipeline and metadata about data schema/versions",
                "Only the evaluation metrics",
                "Only the Python script without parameters",
            ],
            "answer": 1,
            "explanation": "You need the fitted pipeline plus metadata so you can reproduce and safely reuse the model.",
        },
        {
            "text": "What is a typical role of a simple Streamlit app in deployment?",
            "options": [
                "To replace all backend systems",
                "To provide an easy interface for users to send data to a model and see predictions",
                "To train models automatically without code",
                "To store raw databases",
            ],
            "answer": 1,
            "explanation": "Streamlit can host lightweight internal tools where users interact with models via forms or uploads.",
        },
    ]

    answers = []
    for idx, q in enumerate(questions, start=1):
        st.markdown(f"**Q{idx}. {q['text']}**")
        choice = st.radio(
            label=f"u6_q{idx}",
            options=list(range(len(q["options"]))),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"ds_p2_u6_q{idx}",
        )
        answers.append(choice)

    if st.button("Mark Unit 6 quiz", key="ds_p2_u6_quiz_mark"):
        score = sum(1 for ua, q in zip(answers, questions) if ua == q["answer"])
        total = len(questions)
        st.success(f"You scored {score} out of {total} on Unit 6 quick-check quiz.")

        if total:
            for idx, (ua, q) in enumerate(zip(answers, questions), start=1):
                if ua != q["answer"]:
                    correct = q["options"][q["answer"]]
                    explanation = q.get("explanation", "")
                    st.warning(f"Q{idx}: Correct answer is '{correct}'. {explanation}")

        if total > 0 and score == total:
            st.balloons()


def _render_unit7_learning_materials():
    """Capstone project brief and guidance for Unit 7."""

    st.markdown("### Unit 7: Pathway 2 Capstone Project")
    st.caption("Level: Intermediate • Suggested hours: 36 • Suggested credits: 6")

    st.markdown("#### 🎓 Capstone overview")
    st.markdown(
        """In this capstone you will complete an **end-to-end ML project**
using the skills from Units 1–6.

You will:

- Choose a realistic problem and dataset.
- Build a reproducible feature pipeline.
- Train and evaluate at least one regression or classification model.
- (Optionally) explore segmentation or unsupervised structure.
- Propose a simple deployment and monitoring plan.

Your goal is to produce something that could go into a **portfolio** or be
discussed with a hiring manager or stakeholder.
"""
    )

    st.markdown("#### 🧱 Suggested project structure")
    st.markdown(
        """A typical capstone structure:

1. **Problem definition & context**
   - Who is the decision-maker?
   - What question are you answering?
   - What would a good model change in the real world?

2. **Data understanding & EDA**
   - Describe the dataset(s) and key fields.
   - Explore distributions, missingness, and potential leakage.

3. **Feature engineering & pipelines (Unit 1)**
   - Design a feature table.
   - Implement a `Pipeline` / `ColumnTransformer` for preprocessing.

4. **Modelling (Units 2 & 3)**
   - Choose at least one baseline model.
   - Optionally compare a second model or variant.

5. **Evaluation & validation (Unit 4)**
   - Use appropriate metrics and validation strategy.
   - Justify metric choice based on business impact.

6. **Segmentation or unsupervised analysis (Unit 5, optional but encouraged)**
   - Explore clusters/segments if they add value.

7. **Deployment & monitoring sketch (Unit 6)**
   - Explain how this model could be deployed (batch, app, or API).
   - Outline monitoring and retraining.
"""
    )

    st.markdown("#### 📦 Capstone deliverables")
    st.markdown(
        """Your capstone should result in:

- A **notebook or script** showing the full workflow.
- A **short written report or slide deck** summarising:
  - Problem, data, features, models, metrics.
  - Limitations and ethical considerations.
  - Deployment and monitoring plan.
- (Optional) A **small demo** (e.g. Streamlit app) showing how a user
  would interact with the model.
"""
    )


def _render_unit7_labs():
    """Milestones for the capstone project (Unit 7)."""

    st.markdown("### 🧪 Capstone milestones – Unit 7")
    st.markdown(
        """Use these milestones to structure your capstone.

- **Milestone 1 – Problem & data selection**
  - Choose a problem domain (e.g. churn, readmission, demand, default).
  - Identify and document your dataset(s).
  - Write a short problem statement and success criteria.

  - Explore the data, missingness, and basic relationships.
  - Identify any potential sources of data leakage and document how you
    will avoid them.

- **Milestone 3 – Feature pipeline and baseline model**
  - Build a preprocessing pipeline.
  - Train at least one baseline model (regression or classification).
  - Record baseline metrics.

- **Milestone 4 – Improved model and evaluation**
  - Tune hyperparameters or try alternative models.
  - Use appropriate validation (e.g. cross-validation).
  - Compare models using metrics that match the business question.

- **Milestone 5 – Deployment & monitoring plan**
  - Sketch how the model would be deployed (script, app, or API).
  - Propose monitoring and retraining approach.
  - Prepare your final report or slides.
"""
    )


def _render_unit7_quiz():
    """Short readiness / planning quiz for the capstone (Unit 7)."""

    st.markdown("### ✅ Capstone readiness check – Unit 7")
    st.caption(
        "Use this quick quiz to check you have a solid plan before you invest many hours in the capstone."
    )

    questions = [
        {
            "text": "Which of the following is the BEST starting point for your capstone?",
            "options": [
                "Jump straight into modelling on a random dataset",
                "Define a clear problem, stakeholders, and success criteria",
                "Pick the most complex neural network available",
                "Start by writing a deployment script",
            ],
            "answer": 1,
            "explanation": "A clear problem definition and success criteria keep the capstone focused and relevant.",
        },
        {
            "text": "How should you decide which metrics to report for your capstone model?",
            "options": [
                "Use accuracy for everything",
                "Choose metrics that align with the decision and cost of errors for the stakeholders",
                "Only use the metric with the highest value",
                "Avoid reporting metrics to keep things simple",
            ],
            "answer": 1,
            "explanation": "Metrics should reflect the real-world trade-offs of the decision your model supports.",
        },
        {
            "text": "What is a good way to show that your capstone work is reproducible?",
            "options": [
                "Keep all work in an interactive notebook with no explanations",
                "Use a pipeline for preprocessing + model and clearly document data sources and steps",
                "Change the code every time you run it",
                "Only share screenshots of results",
            ],
            "answer": 1,
            "explanation": "Pipelines and clear documentation make it easier for others to rerun and trust your work.",
        },
        {
            "text": "Which of the following should be included in your capstone report?",
            "options": [
                "Only the final metric value",
                "Problem statement, data overview, methods, results, limitations, and next steps",
                "Only screenshots of code",
                "Only a description of the tools you used",
            ],
            "answer": 1,
            "explanation": "A good report tells the full story from problem to results and acknowledges limitations.",
        },
        {
            "text": "What is a realistic deployment outcome for this pathway's capstone?",
            "options": [
                "A fully productionised system with SLAs and full MLOps stack",
                "A simple but clear plan or demo (e.g. script or small app) that shows how the model could be used",
                "Deployment is not relevant",
                "Only a code snippet with no explanation",
            ],
            "answer": 1,
            "explanation": "At this level you aim for a realistic plan or lightweight demo rather than full production infrastructure.",
        },
    ]

    answers = []
    for idx, q in enumerate(questions, start=1):
        st.markdown(f"**Q{idx}. {q['text']}**")
        choice = st.radio(
            label=f"u7_q{idx}",
            options=list(range(len(q["options"]))),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"ds_p2_u7_q{idx}",
        )
        answers.append(choice)

    if st.button("Mark Unit 7 readiness quiz", key="ds_p2_u7_quiz_mark"):
        score = sum(1 for ua, q in zip(answers, questions) if ua == q["answer"])
        total = len(questions)
        st.success(f"You scored {score} out of {total} on the Unit 7 readiness quiz.")

        if total:
            for idx, (ua, q) in enumerate(zip(answers, questions), start=1):
                if ua != q["answer"]:
                    correct = q["options"][q["answer"]]
                    explanation = q.get("explanation", "")
                    st.warning(f"Q{idx}: Correct answer is '{correct}'. {explanation}")

        if total > 0 and score == total:
            st.balloons()


def render_data_science_pathway2_module():
    """Main UI for Data Science Pathway 2 (Intermediate ML).

    Mirrors the overall structure of Pathway 1, with detailed content
    currently implemented for Units 1–7.
    """

    st.title("📊 Data Science Pathway 2 (Intermediate ML)")
    st.success(
        "Take the next step after Foundations: build, evaluate and communicate machine learning models that solve real problems."
    )

    st.markdown("---")

    tabs = st.tabs(
        [
            "📚 Course Overview",
            "📖 Learning Materials",
            "🧪 Labs & Mini Projects",
            "📝 Assessments",
        ]
    )

    # Overview
    with tabs[0]:
        st.subheader("📚 Course Overview")
        st.markdown(
            """Pathway 2 is designed for learners who have already completed
Data Science Foundations (Pathway 1) or have equivalent experience in
Python, Pandas, SQL and basic statistics.

By the end of this pathway you will be able to:

- Build reproducible feature engineering pipelines.
- Train and compare regression and classification models.
- Evaluate models fairly using appropriate metrics and validation
  strategies.
- Use clustering and dimensionality reduction for segmentation.
- Deploy simple models as data products or demos.
- Complete an end-to-end ML capstone suitable for your portfolio.
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
                if unit_number == 1:
                    st.write(
                        "Focus: turning raw tables into clean, reusable feature pipelines and understanding leakage."
                    )
                elif unit_number == 6:
                    st.write(
                        "Focus: deploying and operationalising models, including packaging, monitoring, and feedback loops."
                    )
                elif unit_number == 7:
                    st.write(
                        "Focus: completing an end-to-end capstone project that demonstrates your ability to apply the whole pathway."
                    )
                else:
                    st.write("Detailed content will be added for this unit in a later build.")

    # Learning materials
    with tabs[1]:
        st.subheader("📖 Learning Materials")
        selected_unit = st.selectbox(
            "Select a unit:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_p2_materials_unit",
        )

        if selected_unit == 1:
            _render_unit1_learning_materials()
        elif selected_unit == 2:
            _render_unit2_learning_materials()
        elif selected_unit == 3:
            _render_unit3_learning_materials()
        elif selected_unit == 4:
            _render_unit4_learning_materials()
        elif selected_unit == 5:
            _render_unit5_learning_materials()
        elif selected_unit == 6:
            _render_unit6_learning_materials()
        elif selected_unit == 7:
            _render_unit7_learning_materials()
        else:
            st.info(
                "Detailed learning materials for this unit will be added in a future update."
            )

    # Labs & mini projects
    with tabs[2]:
        st.subheader("🧪 Labs & Mini Projects")
        selected_unit_labs = st.selectbox(
            "Choose a unit to view lab ideas:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_p2_labs_unit",
        )

        if selected_unit_labs == 1:
            _render_unit1_labs()
        elif selected_unit_labs == 2:
            _render_unit2_labs()
        elif selected_unit_labs == 3:
            _render_unit3_labs()
        elif selected_unit_labs == 4:
            _render_unit4_labs()
        elif selected_unit_labs == 5:
            _render_unit5_labs()
        elif selected_unit_labs == 6:
            _render_unit6_labs()
        elif selected_unit_labs == 7:
            _render_unit7_labs()
        else:
            st.info(
                "Lab outlines for this unit will be added in a future update."
            )

    # Assessments (lightweight for now – quick-check quiz only)
    with tabs[3]:
        st.subheader("📝 Assessments")
        st.info(
            "Formal evidence submission and documents will follow the same pattern as Pathway 1. For now, use the quick-check quiz to test your understanding."
        )

        unit_assessment = st.selectbox(
            "Select unit for quick-check quiz:",
            options=[1, 2, 3, 4, 5, 6, 7],
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="ds_p2_assessment_unit",
        )

        if unit_assessment == 1:
            _render_unit1_quiz()
        elif unit_assessment == 2:
            _render_unit2_quiz()
        elif unit_assessment == 3:
            _render_unit3_quiz()
        elif unit_assessment == 4:
            _render_unit4_quiz()
        elif unit_assessment == 5:
            _render_unit5_quiz()
        elif unit_assessment == 6:
            _render_unit6_quiz()
        elif unit_assessment == 7:
            _render_unit7_quiz()
