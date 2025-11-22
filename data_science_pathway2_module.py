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
    # Global video library helper (used to show per-unit recordings)
    from video_library import get_all_videos
except Exception:
    def get_all_videos(category: str = None, week: int = None, competency: str = None):
        return []


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

For a guided walkthrough, see the notebook `U1_feature_pipelines.ipynb` in the Pathway 2 notebooks folder.
"""
    )


def _render_unit1_quiz():
    """Quick-check multiple-choice quiz for Unit 1."""

    st.markdown("### ✅ Quick-check quiz – Unit 1")
    st.caption(
        "Use this short quiz to check your understanding of feature engineering and pipelines."
    )

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


def _render_unit2_learning_materials():
    """Theory content for Unit 2: Supervised Learning – Regression."""

    st.markdown("### Unit 2: Supervised Learning – Regression")
    st.caption("Level: Intermediate • Suggested hours: 24 • Suggested credits: 4")

    st.markdown("#### 📘 What is regression?")
    st.markdown(
        """In regression we predict a **continuous numeric value** such as
monthly spend, length of stay, or demand for a product.

Typical goals:

- Forecasting a quantity in the future.
- Explaining how features relate to an outcome.
- Supporting decisions that depend on an estimated value (e.g. risk or cost).
"""
    )

    st.markdown("#### 🧮 Linear models and loss functions")
    st.markdown(
        """You will work mainly with linear models such as `LinearRegression`
and regularised variants.

Key ideas:

- Predictions are a weighted sum of features.
- We compare predictions to true values using **loss functions** such as
  MSE, RMSE and MAE.
- We care not only about average error but also about whether large
  errors are acceptable for the business context.
"""
    )

    st.markdown("#### 🧱 Regularisation and overfitting")
    st.markdown(
        """To avoid overfitting you will explore **Ridge** and **Lasso**
regression:

- Ridge (L2) shrinks coefficients towards zero.
- Lasso (L1) can set some coefficients exactly to zero.
- Regularisation strength is chosen via validation, not the test set.

You will compare models with and without regularisation on the same
train/validation split so you can see how much variance in performance is
just noise.
"""
    )

    st.markdown("#### 🧹 Preparing data for regression")
    st.markdown(
        """Most of the feature-engineering ideas from Unit 1 still apply, but
for regression you will pay close attention to:

- Obvious outliers that can dominate squared-error metrics.
- Skewed targets (e.g. spend) where log-transforms might be helpful.
- Leakage from target-like features (e.g. future revenue).

You will practice building a **single pipeline** that handles
imputation/encoding/scaling and then feeds a regression model.
"""
    )

    st.markdown("#### 📊 Metrics and evaluation for regression")
    st.markdown(
        """You will practice selecting metrics that match the problem:

- RMSE / MAE for general accuracy.
- MAPE where relative error matters.
- R² for proportion of variance explained (with limitations).

You will also compare **train vs validation** performance to spot
overfitting and use simple plots of **predicted vs actual** to see where
the model is systematically wrong (e.g. under-predicting high spenders).
"""
    )

    st.markdown("#### 💬 Communicating regression results")
    st.markdown(
        """A key skill for this unit is turning numbers into a clear story:

- Explain what a 10-unit change in the target actually means in money or
  risk terms.
- Use examples and simple tables instead of raw coefficient dumps.
- Be explicit about **uncertainty** and where the model performs poorly.

You will practice writing short stakeholder summaries that connect
regression outputs to concrete decisions.
"""
    )


def _render_unit2_labs():
    """Labs and mini-project ideas for Unit 2."""

    st.markdown("### 🧪 Labs & Mini Projects – Unit 2")
    st.markdown(
        """Suggested activities:

- **Lab 1 – Baseline regression model**
  - Take a cleaned feature table from Unit 1.
  - Fit a baseline linear regression model.
  - Compute RMSE/MAE on a validation set.

- **Lab 2 – Regularised models**
  - Train Ridge and Lasso models with several regularisation strengths.
  - Use cross-validation to pick a good value.
  - Compare coefficients and metrics to the baseline.

- **Mini project – Explainable regression**
  - Choose a business question (e.g. drivers of spend).
  - Fit a model and interpret key coefficients / feature importances.
  - Write a short note for stakeholders explaining what drives the outcome.

You can use the notebook `U2_regression_models.ipynb` as a starting point for this unit's practical work.
"""
    )


def _render_unit2_quiz():
    """Quick-check quiz for Unit 2."""

    st.markdown("### ✅ Quick-check quiz – Unit 2")
    st.caption("Check your understanding of regression basics and metrics.")

    questions = [
        {
            "text": "Which problem is most suitable for regression?",
            "options": [
                "Predicting whether a user will churn (yes/no)",
                "Predicting monthly revenue in GBP",
                "Predicting a product category",
                "Classifying emails as spam or not",
            ],
            "answer": 1,
            "explanation": "Regression predicts continuous numeric values, such as revenue.",
        },
        {
            "text": "What does regularisation mainly help with?",
            "options": [
                "Reducing dataset size",
                "Preventing overfitting by shrinking coefficients",
                "Improving data quality",
                "Guaranteeing perfect accuracy",
            ],
            "answer": 1,
            "explanation": "Regularisation discourages very large coefficients and can reduce overfitting.",
        },
        {
            "text": "Why do we usually compare models on a validation set instead of the training set?",
            "options": [
                "Training performance is always lower",
                "Validation performance better reflects generalisation to new data",
                "It is faster to compute",
                "We do not need a validation set",
            ],
            "answer": 1,
            "explanation": "Validation data simulates unseen data, so it is better for model selection.",
        },
        {
            "text": "Which situation suggests that a log-transform of the target might be useful?",
            "options": [
                "Target values are tightly clustered around a small range",
                "Target values are highly skewed with a long right tail (e.g. spend)",
                "The target is binary",
                "The target is a category label",
            ],
            "answer": 1,
            "explanation": "Strong right-skewed numeric targets can benefit from log-transforms for stability.",
        },
        {
            "text": "In a stakeholder summary, which statement best explains RMSE of 50 on next-month spend?",
            "options": [
                "\"The model is 50% accurate.\"",
                "\"On average, our predictions are about \u00a350 away from the true monthly spend.\"",
                "\"The model never makes errors greater than \u00a350.\"",
                "\"The coefficients are small so the model is good.\"",
            ],
            "answer": 1,
            "explanation": "RMSE can be translated into an average error in the same units as the target.",
        },
    ]

    answers = []
    for idx, q in enumerate(questions, start=1):
        st.markdown(f"**Q{idx}. {q['text']}**")
        choice = st.radio(
            label=f"u2_q{idx}",
            options=list(range(len(q["options"]))),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"ds_p2_u2_q{idx}",
        )
        answers.append(choice)

    if st.button("Mark Unit 2 quiz", key="ds_p2_u2_quiz_mark"):
        score = sum(1 for ua, q in zip(answers, questions) if ua == q["answer"])
        total = len(questions)
        st.success(f"You scored {score} out of {total} on Unit 2 quick-check quiz.")

        if total:
            for idx, (ua, q) in enumerate(zip(answers, questions), start=1):
                if ua != q["answer"]:
                    correct = q["options"][q["answer"]]
                    explanation = q.get("explanation", "")
                    st.warning(f"Q{idx}: Correct answer is '{correct}'. {explanation}")

        if total > 0 and score == total:
            st.balloons()


def _render_unit3_learning_materials():
    """Theory content for Unit 3: Supervised Learning – Classification."""

    st.markdown("### Unit 3: Supervised Learning – Classification")
    st.caption("Level: Intermediate • Suggested hours: 24 • Suggested credits: 4")

    st.markdown("#### 📘 What is classification?")
    st.markdown(
        """In classification we predict a **categorical label** such as
churn vs no-churn, high vs low risk, or a diagnosis category.

You will revisit logistic regression and tree-based models as core tools.
"""
    )

    st.markdown("#### 🧱 Choosing and training classifiers")
    st.markdown(
        """You will focus on **interpretable baselines** first:

- Logistic regression for binary problems.
- Simple tree-based models (e.g. decision trees, random forests).

The emphasis is on:

- Starting with a transparent baseline before trying complex models.
- Making sure features from Unit 1 are suitable for both linear and
  tree-based methods.
"""
    )

    st.markdown("#### 📊 Classification metrics")
    st.markdown(
        """You will learn why accuracy is often not enough:

- **Precision / recall / F1** for imbalanced problems.
- **ROC-AUC** and **PR-AUC** for ranking quality.
- Confusion matrices to understand types of error.

You will build intuition with concrete examples (e.g. fraud detection,
readmission risk) where missing positives is much worse than flagging a
few extra negatives.
"""
    )

    st.markdown("#### ⚖️ Class imbalance and decision thresholds")
    st.markdown(
        """Many real problems have **rare positive cases** (e.g. high-risk
patients, fraudulent claims).

You will practice:

- Using **stratified splits** so each fold has similar class ratios.
- Adjusting **decision thresholds** and plotting precision/recall vs
  threshold.
- Explaining trade-offs between **false positives** and **false
  negatives** to stakeholders.
"""
    )

    st.markdown("#### 💬 Communicating classification results")
    st.markdown(
        """Stakeholders rarely ask for ROC-AUC; they ask questions like
"how many high-risk patients will we miss?".

You will practice:

- Turning metrics into **plain-language statements** about outcomes.
- Presenting **example cases** the model got right/wrong.
- Highlighting where the model should **not** be used on its own
  (e.g. as a decision support tool, not an automatic rejection).
"""
    )


def _render_unit3_labs():
    """Labs and mini-project ideas for Unit 3."""

    st.markdown("### 🧪 Labs & Mini Projects – Unit 3")
    st.markdown(
        """Suggested activities:

- **Lab 1 – Baseline classifier**
  - Build a logistic regression model for a binary outcome.
  - Plot the confusion matrix and compute precision/recall/F1.

- **Lab 2 – Handling class imbalance**
  - Try re-weighting classes or simple resampling.
  - Compare metrics at different thresholds.

- **Mini project – Risk scoring model**
  - Choose a realistic risk prediction task (e.g. churn, default).
  - Train at least two classifiers and compare them using appropriate metrics.
  - Write a short summary focusing on the business impact of errors.

The notebook `U3_classification_metrics.ipynb` provides a scaffold for these experiments.
"""
    )


def _render_unit3_quiz():
    """Quick-check quiz for Unit 3."""

    st.markdown("### ✅ Quick-check quiz – Unit 3")
    st.caption("Check your understanding of classification concepts and metrics.")

    questions = [
        {
            "text": "Which of the following is a classification problem?",
            "options": [
                "Predicting daily sales amount",
                "Predicting whether a transaction is fraudulent (yes/no)",
                "Predicting length of stay in days",
                "Predicting a temperature in °C",
            ],
            "answer": 1,
            "explanation": "Fraud vs non-fraud is a binary classification problem.",
        },
        {
            "text": "Why can accuracy be misleading on highly imbalanced data?",
            "options": [
                "It is hard to compute",
                "A model can be accurate by always predicting the majority class",
                "It always underestimates performance",
                "It only works for regression",
            ],
            "answer": 1,
            "explanation": "With rare positives, predicting the majority class can give high accuracy but zero recall.",
        },
        {
            "text": "Which metric focuses on 'of the predicted positives, how many were correct'?",
            "options": ["Recall", "Precision", "Accuracy", "F1-score"],
            "answer": 1,
            "explanation": "Precision is the proportion of predicted positives that are truly positive.",
        },
        {
            "text": "In a hospital readmission model, which statement best describes high recall for the positive class?",
            "options": [
                "We correctly flag a high proportion of patients who will be readmitted",
                "We rarely flag patients who will not be readmitted",
                "Overall accuracy is guaranteed to be high",
                "The model is not useful for rare events",
            ],
            "answer": 0,
            "explanation": "Recall for the positive class measures how many true positives we successfully catch.",
        },
        {
            "text": "What does moving the classification threshold from 0.5 down to 0.2 usually do?",
            "options": [
                "Decreases both precision and recall",
                "Increases recall but may reduce precision",
                "Increases precision but may reduce recall",
                "Leaves precision and recall unchanged",
            ],
            "answer": 1,
            "explanation": "Lowering the threshold marks more cases as positive, catching more true positives but also more false positives.",
        },
    ]

    answers = []
    for idx, q in enumerate(questions, start=1):
        st.markdown(f"**Q{idx}. {q['text']}**")
        choice = st.radio(
            label=f"u3_q{idx}",
            options=list(range(len(q["options"]))),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"ds_p2_u3_q{idx}",
        )
        answers.append(choice)

    if st.button("Mark Unit 3 quiz", key="ds_p2_u3_quiz_mark"):
        score = sum(1 for ua, q in zip(answers, questions) if ua == q["answer"])
        total = len(questions)
        st.success(f"You scored {score} out of {total} on Unit 3 quick-check quiz.")

        if total:
            for idx, (ua, q) in enumerate(zip(answers, questions), start=1):
                if ua != q["answer"]:
                    correct = q["options"][q["answer"]]
                    explanation = q.get("explanation", "")
                    st.warning(f"Q{idx}: Correct answer is '{correct}'. {explanation}")

        if total > 0 and score == total:
            st.balloons()


def _render_unit4_learning_materials():
    """Theory content for Unit 4: Model Evaluation & Validation."""

    st.markdown("### Unit 4: Model Evaluation & Validation")
    st.caption("Level: Intermediate • Suggested hours: 18 • Suggested credits: 3")

    st.markdown("#### 📘 Why evaluation and validation matter")
    st.markdown(
        """In this unit you focus on how well your models **generalise** to new data,
and how to choose models and hyperparameters without overfitting.

Key ideas include:

- Separating train, validation and test data.
- Using cross-validation for reliable estimates.
- Picking metrics that match the business problem.
"""
    )

    st.markdown("#### 📊 Validation strategies")
    st.markdown(
        """You will compare several strategies:

- Simple train/validation/test split.
- k-fold cross-validation.
- Time-aware validation for time-series style problems.

You will also revisit why you **must not** use the test set to make
modelling decisions.
"""
    )

    st.markdown("#### 🔁 Cross-validation in practice")
    st.markdown(
        """You will use **k-fold cross-validation** to get more stable
estimates of model performance:

- How to choose k (e.g. 5 vs 10 folds).
- How CV interacts with hyperparameter tuning.
- Why you still need a final test set even after doing CV.

You will run simple experiments comparing single validation splits to
cross-validation and see how much scores can vary.
"""
    )

    st.markdown("#### ⏱ Time-aware evaluation")
    st.markdown(
        """For problems with a natural time order (e.g. admissions over
time) you will explore **time-aware validation**:

- Splitting by time so the model is trained on the past and evaluated on
  the future.
- Why shuffling can leak future information into the past.
- How to adapt cross-validation ideas for time-series style data.
"""
    )

    st.markdown("#### ⚠️ Common pitfalls in evaluation")
    st.markdown(
        """This unit also focuses on what can go wrong:

- Tuning hyperparameters directly on the test set.
- Reporting only accuracy on highly imbalanced data.
- Comparing models on different validation splits.

You will work through small case studies where evaluation mistakes lead
to over-optimistic conclusions, and practice fixing them.
"""
    )


def _render_unit4_labs():
    """Labs and mini-project ideas for Unit 4."""

    st.markdown("### 🧪 Labs & Mini Projects – Unit 4")
    st.markdown(
        """Suggested activities:

- **Lab 1 – Comparing validation strategies**
  - Take a model from Units 2 or 3.
  - Evaluate it with a hold-out split and with k-fold cross-validation.
  - Compare the stability of the metrics.

- **Lab 2 – Metric selection for a real decision**
  - Choose a regression or classification problem.
  - Decide which metrics matter most for the stakeholders.
  - Justify your choice in a short note.

- **Mini project – Evaluation review for a healthcare model**
  - Take an existing model (e.g. readmission risk or clinic no-show).
  - Audit how it was originally validated and identify any weaknesses
    (e.g. test set reuse, wrong metric for class imbalance).
  - Propose an improved validation plan.

For practical guidance, see `U4_model_validation.ipynb` in the Pathway 2 notebooks folder.
"""
    )


def _render_unit4_quiz():
    """Quick-check quiz for Unit 4."""

    st.markdown("### ✅ Quick-check quiz – Unit 4")
    st.caption("Check your understanding of evaluation and validation.")

    questions = [
        {
            "text": "What is the main purpose of a validation set?",
            "options": [
                "To train the model",
                "To select models and hyperparameters without touching the test set",
                "To store raw data",
                "To replace the training set",
            ],
            "answer": 1,
            "explanation": "The validation set is used for model selection and tuning.",
        },
        {
            "text": "Why should you avoid using the test set to make modelling decisions?",
            "options": [
                "It is usually smaller",
                "You would leak information and overestimate real performance",
                "It is slower to compute",
                "It cannot be used with cross-validation",
            ],
            "answer": 1,
            "explanation": "The test set should simulate truly unseen data.",
        },
        {
            "text": "Which of the following is a reasonable use of k-fold cross-validation?",
            "options": [
                "To generate more training data by copying rows",
                "To estimate model performance more reliably by averaging over several splits",
                "To avoid needing a test set",
                "To guarantee perfect generalisation",
            ],
            "answer": 1,
            "explanation": "Cross-validation averages performance over multiple splits to give a more stable estimate.",
        },
        {
            "text": "For a time-ordered dataset, which validation strategy is usually safest?",
            "options": [
                "Randomly shuffle all rows, then split",
                "Train on future data and test on past data",
                "Train on past data and validate on more recent data",
                "Use no validation at all",
            ],
            "answer": 2,
            "explanation": "To mimic production, you train on the past and evaluate on the future.",
        },
        {
            "text": "A model shows 99% accuracy but recall of 5% for the positive class on imbalanced data. What is the main issue?",
            "options": [
                "The accuracy metric is incorrect",
                "The model is effectively ignoring most positive cases",
                "Recall is always low on test data",
                "Nothing is wrong; high accuracy means the model is good",
            ],
            "answer": 1,
            "explanation": "Very low recall on the minority class means the model is missing almost all of the cases we care about.",
        },
    ]

    answers = []
    for idx, q in enumerate(questions, start=1):
        st.markdown(f"**Q{idx}. {q['text']}**")
        choice = st.radio(
            label=f"u4_q{idx}",
            options=list(range(len(q["options"]))),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"ds_p2_u4_q{idx}",
        )
        answers.append(choice)

    if st.button("Mark Unit 4 quiz", key="ds_p2_u4_quiz_mark"):
        score = sum(1 for ua, q in zip(answers, questions) if ua == q["answer"])
        total = len(questions)
        st.success(f"You scored {score} out of {total} on Unit 4 quick-check quiz.")

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

- **Healthcare-flavoured extension**
  - Imagine the data represents patients or service users.
  - Describe how you would use segments to prioritise outreach,
    education or follow-up appointments.

Use `U5_clustering_segmentation.ipynb` for a worked example of these steps.
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
        """These labs focus on turning a working model into something that could be used by others.

- **Lab 1 – Saving and loading a trained pipeline**
  - Take a pipeline + model from an earlier unit.
  - Save it to disk using `joblib` or `pickle`.
  - Write a small script that loads the pipeline and scores new data from a CSV file.

- **Lab 2 – Simple prediction app or script**
  - Build a tiny CLI tool or Streamlit app where a user can input features (or upload a file) and receive predictions.
  - Include basic validation and user guidance.

- **Mini project – Deployment and monitoring plan**
  - Choose one of your earlier models.
  - Draft a short document describing how it would be deployed, who would use it, how it would be monitored and how often it would be retrained.
  - Include at least one example monitoring alert (e.g. sudden drop in recall for a safety-critical classifier).
  - Develop a plan for retraining the model based on new data, including how often to retrain and how to evaluate the updated model.

You can use `U6_deployment_basics.ipynb` as a sandbox for these ideas.
"""
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

The notebook `U7_capstone_template.ipynb` provides a full scaffold for
planning and documenting your capstone.
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
    implemented for Units 1–7 and hooks for evidence, documents and progress.
    """

    learner_email = st.session_state.get("user_email", "")

    st.title("📊 Data Science Pathway 2 (Intermediate ML)")
    st.success(
        "Take the next step after Foundations: build, evaluate and communicate machine learning models that solve real problems."
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
        st.info("Use this tab as the main reading and concept reference for each unit.")

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

        st.markdown("---")
        st.markdown("### 📺 Session recordings for this unit")
        st.caption(
            "Videos added in the global Video Library for this week/unit will appear here. "
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
                        st.warning("Video link not available. Please check the Video Library entry.")

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

    # Assessments
    with tabs[3]:
        st.subheader("📝 Assessments")
        st.info(
            "Use this tab to submit evidence for each unit (labs, mini projects, capstone) "
            "and to complete quick-check quizzes."
        )

        if not learner_email:
            st.warning("Log in as a learner to submit assessments.")
        else:
            assessment_unit = st.selectbox(
                "Select unit for assessment submission:",
                options=list(UNITS.keys()),
                format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
                key="ds_p2_assessment_submission_unit",
            )
            render_evidence_submission_form(learner_email, COURSE_ID, assessment_unit)

        st.markdown("---")
        st.markdown("### ✅ Quick-check quizzes (Units 1–7)")
        st.caption(
            "Answer a short multiple-choice quiz for the selected unit directly in the app. "
            "Tutors can still use separate assessment materials for formal evidence."
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
- Study timetable templates for Intermediate ML
- Checklists for each Pathway 2 unit
- Portfolio structure guide (with emphasis on ML projects)
- Example project reports and capstone write-ups
"""
        )

        st.markdown("---")
        st.markdown("### 📥 Download core documents as PDF")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("📥 Pathway 2 study plan PDF", key="dsp2_study_plan_pdf"):
                study_plan_md = """# Data Science Pathway 2 – Study Plan

This plan assumes **7–12 weeks** of part-time study. Tutors can adapt the
pace for different cohorts. Always refer to the in-app materials for
full details and latest updates.

---

## Week 1–2 – Unit 1: Feature Engineering & Data Pipelines

- Read Unit 1 learning materials in the platform.
- Work through `U1_feature_pipelines.ipynb`:
  - Explore the sample events dataset.
  - Build a basic feature table.
  - Implement a `ColumnTransformer` + `Pipeline`.
- Complete Unit 1 labs and quick-check quiz.

## Week 2–3 – Unit 2: Supervised Learning – Regression

- Read Unit 2 theory (linear models, loss functions, regularisation).
- Use `U2_regression_models.ipynb` to:
  - Train baseline and regularised models.
  - Compare RMSE/MAE/R² on train vs validation.
- Complete Unit 2 labs and quick-check quiz.

## Week 3–4 – Unit 3: Supervised Learning – Classification

- Study classification metrics and class imbalance guidance.
- In `U3_classification_metrics.ipynb`:
  - Fit at least one logistic regression model.
  - Plot confusion matrix, ROC and PR curves.
  - Experiment with different thresholds.
- Complete Unit 3 labs and quick-check quiz.

## Week 4–5 – Unit 4: Model Evaluation & Validation

- Read about validation strategies and cross-validation.
- In `U4_model_validation.ipynb`:
  - Implement explicit train/validation/test splits.
  - Run k-fold cross-validation.
  - Try at least one time-aware split if relevant.
- Complete Unit 4 labs and quick-check quiz.

## Week 5–6 – Unit 5: Unsupervised Learning & Segmentation

- Review Unit 5 theory on clustering and segmentation.
- Use `U5_clustering_segmentation.ipynb` to:
  - Build a clustering pipeline with scaling.
  - Compare several values of *k*.
  - Profile clusters and write short segment descriptions.
- Complete Unit 5 labs and quick-check quiz.

## Week 6–7 – Unit 6: Deploying & Operationalising Models

- Study Unit 6 materials on deployment patterns and monitoring.
- In `U6_deployment_basics.ipynb`:
  - Load a trained pipeline from Units 1–3.
  - Implement a batch scoring helper.
  - Sketch a simple CLI or Streamlit interface.
- Complete Unit 6 labs and quick-check quiz.

## Week 7+ – Unit 7: Capstone Project

- Read the capstone brief and milestones in the platform.
- Use `U7_capstone_template.ipynb` as your main project notebook.
- Schedule regular check-ins with tutors/mentors.
- Prepare final notebook/script, report/slides and optional demo app.

Learners who already have experience can progress faster; those new to
ML may spread Units 1–4 over extra weeks.
"""
                pdf = create_unit_pdf(0, "Pathway 2 Study Plan", study_plan_md)
                st.download_button(
                    label="Download Study Plan PDF",
                    data=pdf,
                    file_name="Data_Science_Pathway2_Study_Plan.pdf",
                    mime="application/pdf",
                    key="dsp2_study_plan_pdf_dl",
                )

        with col_b:
            if st.button("📥 Pathway 2 checklists PDF", key="dsp2_checklists_pdf"):
                checklists_md = """# Data Science Pathway 2 – Unit Checklists

Use these checklists to track your progress. They are **not** formal
assessment criteria but a practical guide for learners and tutors.

---

## Unit 1 – Feature Engineering & Data Pipelines

- [ ] I can explain what feature engineering is and why it matters.
- [ ] I can identify numeric, categorical, date/time and ID columns.
- [ ] I can handle missing values in a deliberate, documented way.
- [ ] I can build a scikit-learn `Pipeline` / `ColumnTransformer`.
- [ ] I understand data leakage and can give at least two examples.

## Unit 2 – Supervised Learning: Regression

- [ ] I can describe the difference between regression and classification.
- [ ] I can train and evaluate at least one regression model.
- [ ] I know when to use RMSE, MAE, MAPE and R².
- [ ] I can explain the idea of Ridge and Lasso regularisation.
- [ ] I can write a short, non-technical summary of regression results.

## Unit 3 – Supervised Learning: Classification

- [ ] I can explain accuracy, precision, recall and F1 in plain language.
- [ ] I can interpret a confusion matrix for a binary classifier.
- [ ] I understand why accuracy alone is risky on imbalanced data.
- [ ] I can adjust a classification threshold and explain the impact.

## Unit 4 – Model Evaluation & Validation

- [ ] I can set up separate train, validation and test sets.
- [ ] I can run and interpret k-fold cross-validation.
- [ ] I understand when and how to use time-aware validation.
- [ ] I know why the test set must not be used for tuning.

## Unit 5 – Unsupervised Learning & Segmentation

- [ ] I can explain the difference between supervised and unsupervised
      learning.
- [ ] I can run a basic clustering algorithm on tabular data.
- [ ] I can interpret clusters using simple profiles/aggregates.
- [ ] I can describe at least one realistic use of segmentation.

## Unit 6 – Deploying & Operationalising Models

- [ ] I can save and reload a trained model/pipeline.
- [ ] I understand the difference between batch scoring and real-time
      prediction.
- [ ] I can outline a simple deployment architecture for an internal
      tool.
- [ ] I can list at least three things that should be monitored after
      deployment.

## Unit 7 – Capstone Project

- [ ] I have a clear problem statement and defined stakeholders.
- [ ] I have documented data sources and key assumptions.
- [ ] I have built at least one end-to-end pipeline + model.
- [ ] I have evaluated the model with appropriate metrics.
- [ ] I have written a short report or slide deck summarising the work.
"""
                pdf = create_unit_pdf(0, "Pathway 2 Checklists", checklists_md)
                st.download_button(
                    label="Download Checklists PDF",
                    data=pdf,
                    file_name="Data_Science_Pathway2_Unit_Checklists.pdf",
                    mime="application/pdf",
                    key="dsp2_checklists_pdf_dl",
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
                    key=f"ds_pathway2_progress_unit_{unit_number}",
                )

    # Certificate
    with tabs[7]:
        st.subheader("🎓 Certificate")
        st.info(
            "On successful completion of all units and assessments, learners receive a "
            "T21 Data Science Pathway 2 (Intermediate ML) certificate, where offered by "
            "their training provider."
        )

        st.markdown(
            """### Requirements for completion

- Complete and submit evidence for all 7 units
- Demonstrate competence in feature engineering, supervised and unsupervised learning
- Complete at least one end-to-end ML capstone project
- Meet internal quality standards set by tutors/assessors
"""
        )

        if enrollment and enrollment.get("progress", 0) >= 100:
            st.success(
                "All requirements appear to be complete. Your training provider can now "
                "issue your Data Science Pathway 2 certificate."
            )
        else:
            st.info(
                "Keep working through your units and projects. Once everything is complete, "
                "your tutor will confirm and issue your certificate."
            )
