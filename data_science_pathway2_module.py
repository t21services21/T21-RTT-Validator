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
        {
            "text": "What is the purpose of a ColumnTransformer in scikit-learn?",
            "options": [
                "To drop columns",
                "To apply different transformations to different columns",
                "To rename columns",
                "To sort columns",
            ],
            "answer": 1,
            "explanation": "ColumnTransformer lets you apply different preprocessing steps to different column groups.",
        },
        {
            "text": "Why should you fit transformers only on training data?",
            "options": [
                "To make the code run faster",
                "To prevent data leakage from validation/test sets",
                "It doesn't matter",
                "To use less memory",
            ],
            "answer": 1,
            "explanation": "Fitting on training data only prevents information from validation/test sets leaking into your model.",
        },
        {
            "text": "Which technique handles missing numeric values by replacing them with the column mean?",
            "options": ["One-hot encoding", "Mean imputation", "Scaling", "Dropping rows"],
            "answer": 1,
            "explanation": "Mean imputation fills missing values with the average of non-missing values.",
        },
        {
            "text": "What does StandardScaler do?",
            "options": [
                "Removes outliers",
                "Transforms features to have mean 0 and standard deviation 1",
                "Encodes categorical variables",
                "Drops missing values",
            ],
            "answer": 1,
            "explanation": "StandardScaler standardizes features by removing the mean and scaling to unit variance.",
        },
        {
            "text": "Which is a sign of feature leakage?",
            "options": [
                "Using last year's data to predict this year",
                "Using future information or target-derived features in training",
                "Using too many features",
                "Using cross-validation",
            ],
            "answer": 1,
            "explanation": "Leakage occurs when information that wouldn't be available at prediction time is used during training.",
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
                "\"On average, our predictions are about £50 away from the true monthly spend.\"",
                "\"The model never makes errors greater than £50.\"",
                "\"The coefficients are small so the model is good.\"",
            ],
            "answer": 1,
            "explanation": "RMSE can be translated into an average error in the same units as the target.",
        },
        {
            "text": "What is the main difference between Lasso and Ridge regression?",
            "options": [
                "Lasso can shrink coefficients to exactly zero; Ridge cannot",
                "Ridge is always better",
                "Lasso cannot handle categorical features",
                "They are the same",
            ],
            "answer": 0,
            "explanation": "Lasso (L1) can eliminate features by setting coefficients to zero; Ridge (L2) only shrinks them.",
        },
        {
            "text": "Which metric is most sensitive to outliers?",
            "options": ["MAE", "MSE", "Median Absolute Error", "R-squared"],
            "answer": 1,
            "explanation": "MSE squares errors, making it very sensitive to large outliers.",
        },
        {
            "text": "What does R-squared measure?",
            "options": [
                "The number of features",
                "The proportion of variance in the target explained by the model",
                "The training time",
                "The number of outliers",
            ],
            "answer": 1,
            "explanation": "R-squared indicates how much of the target's variance is captured by the model.",
        },
        {
            "text": "When should you use cross-validation instead of a single train/test split?",
            "options": [
                "Never",
                "When you want a more robust estimate of model performance",
                "Only for classification",
                "Only when you have millions of rows",
            ],
            "answer": 1,
            "explanation": "Cross-validation gives a more reliable performance estimate by testing on multiple folds.",
        },
        {
            "text": "What is the purpose of a residual plot in regression?",
            "options": [
                "To show the training time",
                "To diagnose patterns in prediction errors and check model assumptions",
                "To count the number of features",
                "To display the dataset",
            ],
            "answer": 1,
            "explanation": "Residual plots help identify non-linearity, heteroscedasticity, and other issues.",
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
        {
            "text": "What does ROC-AUC measure?",
            "options": [
                "The training time",
                "The model's ability to rank positive cases higher than negative cases",
                "The number of features",
                "The dataset size",
            ],
            "answer": 1,
            "explanation": "ROC-AUC measures how well the model separates classes across all thresholds.",
        },
        {
            "text": "In a confusion matrix, what are false positives?",
            "options": [
                "Cases predicted positive that are actually positive",
                "Cases predicted positive that are actually negative",
                "Cases predicted negative that are actually positive",
                "Cases predicted negative that are actually negative",
            ],
            "answer": 1,
            "explanation": "False positives are incorrectly predicted as positive when they are actually negative.",
        },
        {
            "text": "Why use stratified splitting for classification?",
            "options": [
                "To make the code run faster",
                "To ensure each split has similar class proportions",
                "To remove outliers",
                "It is only for regression",
            ],
            "answer": 1,
            "explanation": "Stratified splitting maintains class balance across train/validation/test sets.",
        },
        {
            "text": "What is the F1-score?",
            "options": [
                "The average of precision and recall",
                "The harmonic mean of precision and recall",
                "The product of precision and recall",
                "The difference between precision and recall",
            ],
            "answer": 1,
            "explanation": "F1-score is the harmonic mean, giving equal weight to precision and recall.",
        },
        {
            "text": "When would you prioritize recall over precision?",
            "options": [
                "When false negatives are very costly (e.g., missing a disease diagnosis)",
                "When false positives are very costly",
                "When the classes are balanced",
                "Never",
            ],
            "answer": 0,
            "explanation": "High recall is crucial when missing positive cases has serious consequences.",
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
        {
            "text": "What is overfitting?",
            "options": [
                "When a model performs poorly on both training and test data",
                "When a model performs well on training data but poorly on test data",
                "When a model is too simple",
                "When the dataset is too large",
            ],
            "answer": 1,
            "explanation": "Overfitting means the model has learned the training data too well, including noise.",
        },
        {
            "text": "What is the purpose of hyperparameter tuning?",
            "options": [
                "To find the best model configuration for validation performance",
                "To increase the training set size",
                "To remove features",
                "To guarantee perfect accuracy",
            ],
            "answer": 0,
            "explanation": "Hyperparameter tuning searches for the configuration that performs best on validation data.",
        },
        {
            "text": "Why use stratified k-fold cross-validation for classification?",
            "options": [
                "To make training faster",
                "To ensure each fold has similar class proportions",
                "To remove outliers",
                "It is only for regression",
            ],
            "answer": 1,
            "explanation": "Stratified CV maintains class balance in each fold, giving more reliable estimates.",
        },
        {
            "text": "What is a learning curve?",
            "options": [
                "A plot showing model performance vs training set size",
                "A plot of feature importance",
                "A confusion matrix",
                "A scatter plot of predictions",
            ],
            "answer": 0,
            "explanation": "Learning curves show how performance changes as you add more training data.",
        },
        {
            "text": "When should you use the test set?",
            "options": [
                "Throughout model development to check progress",
                "Only once at the very end to report final performance",
                "Never",
                "To tune hyperparameters",
            ],
            "answer": 1,
            "explanation": "The test set should be used only once at the end to avoid overfitting to it.",
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
        {
            "text": "What does the 'k' in k-means represent?",
            "options": [
                "The number of features",
                "The number of clusters",
                "The number of iterations",
                "The dataset size",
            ],
            "answer": 1,
            "explanation": "k is the number of clusters you want to create.",
        },
        {
            "text": "How do you typically choose the number of clusters?",
            "options": [
                "Always use k=2",
                "Use domain knowledge and validation metrics like silhouette score or elbow method",
                "Use as many clusters as there are rows",
                "It doesn't matter",
            ],
            "answer": 1,
            "explanation": "The number of clusters should be informed by business context and validation metrics.",
        },
        {
            "text": "What is dimensionality reduction used for?",
            "options": [
                "To increase the number of features",
                "To reduce the number of features while preserving important information",
                "To delete all data",
                "To encrypt data",
            ],
            "answer": 1,
            "explanation": "Dimensionality reduction techniques like PCA compress high-dimensional data.",
        },
        {
            "text": "Why might you use PCA before clustering?",
            "options": [
                "To make the code slower",
                "To reduce noise and computational cost while preserving variance",
                "To guarantee perfect clusters",
                "PCA should never be used with clustering",
            ],
            "answer": 1,
            "explanation": "PCA can help by reducing dimensions and noise before clustering.",
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
        {
            "text": "What is model drift?",
            "options": [
                "When the model file gets corrupted",
                "When model performance degrades over time due to changes in data patterns",
                "When the model trains too slowly",
                "When you use the wrong algorithm",
            ],
            "answer": 1,
            "explanation": "Drift occurs when the relationship between features and target changes over time.",
        },
        {
            "text": "Why save model metadata (e.g., feature names, data schema)?",
            "options": [
                "To make the file larger",
                "To ensure production data matches the expected format and features",
                "It is not necessary",
                "To slow down predictions",
            ],
            "answer": 1,
            "explanation": "Metadata helps validate that production data is compatible with the trained model.",
        },
        {
            "text": "What is A/B testing in the context of model deployment?",
            "options": [
                "Testing two different Python versions",
                "Comparing a new model against the current model with real users",
                "Testing on the training set twice",
                "Using two different databases",
            ],
            "answer": 1,
            "explanation": "A/B testing compares model versions in production to see which performs better.",
        },
        {
            "text": "Which is a sign that a model needs retraining?",
            "options": [
                "The code runs without errors",
                "Performance metrics degrade significantly on recent data",
                "The model was trained last week",
                "Users like the predictions",
            ],
            "answer": 1,
            "explanation": "Declining performance on new data suggests the model may be outdated.",
        },
        {
            "text": "What is the purpose of versioning models?",
            "options": [
                "To confuse users",
                "To track which model version is deployed and enable rollback if needed",
                "To delete old models immediately",
                "Versioning is not useful",
            ],
            "answer": 1,
            "explanation": "Versioning allows you to manage, compare, and roll back model deployments.",
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
        {
            "text": "Why document limitations in your capstone?",
            "options": [
                "To make the report longer",
                "To show honest judgment about where the analysis is strong or weak",
                "To hide problems",
                "Limitations are not important",
            ],
            "answer": 1,
            "explanation": "Acknowledging limitations builds trust and shows professional maturity.",
        },
        {
            "text": "What makes a capstone dataset suitable?",
            "options": [
                "It has only 10 rows",
                "It is realistic, well-documented, and relevant to a business problem",
                "It has no missing values or challenges",
                "It is completely random",
            ],
            "answer": 1,
            "explanation": "Good capstone datasets are realistic and allow you to demonstrate practical skills.",
        },
        {
            "text": "How should you present your capstone to potential employers?",
            "options": [
                "Keep it only on your laptop",
                "Upload to GitHub with a clear README, notebook, and report",
                "Only describe it verbally",
                "Print screenshots only",
            ],
            "answer": 1,
            "explanation": "A well-documented GitHub repository is easy to share and review.",
        },
        {
            "text": "What is the purpose of a capstone project?",
            "options": [
                "To memorize formulas",
                "To demonstrate end-to-end data science skills on a realistic problem",
                "To avoid learning theory",
                "To pass time",
            ],
            "answer": 1,
            "explanation": "Capstones showcase your ability to tackle real problems independently from start to finish.",
        },
        {
            "text": "Which is more valuable in a capstone: breadth or depth?",
            "options": [
                "Breadth - try everything superficially",
                "Depth - do one problem well with rigorous methods",
                "Neither matters",
                "Only breadth",
            ],
            "answer": 1,
            "explanation": "Employers value depth and rigor over superficial coverage of many topics.",
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
        if st.button("📥 Download unit theory summary as PDF", key="ds_p2_unit_pdf"):
            unit = UNITS[selected_unit]
            content_lines = [f"# Unit {selected_unit}: {unit['name']}", ""]
            content_lines.append("This PDF summarises the high-level theory for this unit.")
            content_lines.append("Refer to the in-app materials, labs and notebooks for full detail.")
            markdown_content = "\n".join(content_lines)
            pdf_buffer = create_unit_pdf(
                selected_unit,
                unit["name"],
                markdown_content,
            )
            st.download_button(
                label="📥 Download Unit Summary PDF",
                data=pdf_buffer,
                file_name=f"Data_Science_Pathway2_Unit_{selected_unit}.pdf",
                mime="application/pdf",
                key="ds_p2_unit_pdf_dl",
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

        st.markdown("---")
        st.markdown("### 💼 Career Preparation Package")
        st.success(
            "**NEW!** Complete job toolkit for Data Science roles - Resume, "
            "200+ ML interview questions, portfolio guide, and career strategies!"
        )
        
        if st.button("📥 Career Prep - Data Scientist Edition", key="dsp2_career_prep_pdf"):
            career_prep_md = """# Career Prep Package - Land Your Data Scientist Job

**Complete toolkit for Data Scientist career success**

---

## 📄 DATA SCIENTIST RESUME TEMPLATE

```
[YOUR NAME]
Data Scientist
Email: your.email@example.com | LinkedIn: linkedin.com/in/yourname
GitHub: github.com/yourname | Portfolio: yourportfolio.com

PROFESSIONAL SUMMARY
Data Scientist with expertise in machine learning, statistical modeling, and
Python programming. Completed rigorous training in feature engineering, model
development, validation, deployment, and MLOps. Strong ability to translate
business problems into ML solutions and communicate results to stakeholders.

TECHNICAL SKILLS
• Languages: Python (Scikit-learn, Pandas, NumPy, Matplotlib), SQL, R (basic)
• ML/AI: Regression, Classification, Clustering, Ensemble Methods, Deep Learning
• Tools: Jupyter, Git, Docker, MLflow, TensorFlow/PyTorch
• Deployment: Flask/FastAPI, AWS SageMaker, Docker containers
• Skills: Feature Engineering, Model Validation, Hyperparameter Tuning,
  A/B Testing, Experiment Tracking, Model Deployment

KEY PROJECTS

ML Production Capstone | [Date]
• Developed predictive model achieving 87% accuracy on customer churn
• Engineered 25+ features from raw data, improving baseline by 18%
• Implemented full ML pipeline with preprocessing, training, and validation
• Deployed model using Flask API with 50ms response time
• Set up MLflow experiment tracking and model registry
• GitHub: [link]

Classification Model - Healthcare | [Date]
• Built model predicting patient readmission with 82% precision
• Handled imbalanced dataset using SMOTE and class weights
• Performed feature importance analysis identifying top 10 drivers
• Validated using stratified 5-fold cross-validation
• Delivered insights to medical team with business recommendations

Time-Series Forecasting | [Date]
• Created ARIMA/Prophet models forecasting sales with 8% MAPE
• Implemented rolling-origin validation for robust evaluation
• Handled seasonality, trend components, and holiday effects
• Deployed automated retraining pipeline

EDUCATION & CERTIFICATIONS
• Data Science Pathway 2 & 3 Certifications | [Date]
  - Advanced ML, Deep Learning, MLOps, Model Deployment
  - 700+ hours hands-on training with real-world projects
  - Portfolio of production-ready models

[Your Previous Education/Experience]
```

---

## 💼 TOP 80 DATA SCIENCE INTERVIEW QUESTIONS

### Machine Learning Fundamentals (20 Questions)

**Q1: Explain bias-variance tradeoff.**
A: Bias = error from oversimplifying (underfitting)
Variance = error from too much complexity (overfitting)
Goal: Find balance that minimizes total error
Trade-off: Reducing one often increases the other

**Q2: What is overfitting? How do you prevent it?**
Overfitting: Model learns training data too well, poor generalization
Prevention:
- Cross-validation
- Regularization (L1/L2)
- More training data
- Feature selection
- Early stopping
- Ensemble methods

**Q3: Supervised vs unsupervised learning?**
Supervised: Has labeled data (y), predict output (classification, regression)
Unsupervised: No labels, find patterns (clustering, dimensionality reduction)

**Q4: Explain cross-validation.**
A: Splitting data into multiple folds for robust evaluation
K-fold: Split into k parts, train on k-1, validate on 1, repeat k times
Benefits: Better estimate of performance, reduces overfitting

**Q5: What is regularization? L1 vs L2?**
Regularization: Penalty for model complexity
L1 (Lasso): Sum of absolute weights, creates sparse models
L2 (Ridge): Sum of squared weights, shrinks all weights
ElasticNet: Combination of both

**Q6: How to handle imbalanced datasets?**
- Resampling: SMOTE, undersample majority class
- Class weights: Penalize minority class errors more
- Different metrics: Precision, recall, F1, not just accuracy
- Ensemble methods: Balanced Random Forest
- Generate synthetic samples

**Q7: Precision vs Recall vs F1-score?**
Precision: Of predicted positives, how many correct? (TP / (TP + FP))
Recall: Of actual positives, how many found? (TP / (TP + FN))
F1: Harmonic mean of precision and recall
Use case dependent: Spam (precision), Disease (recall)

**Q8: What is ROC-AUC?**
ROC: Receiver Operating Characteristic curve (TPR vs FPR)
AUC: Area Under Curve (0.5 = random, 1.0 = perfect)
Use for: Comparing classifiers, threshold selection
Good when: Classes balanced

**Q9: Classification vs Regression?**
Classification: Predicting categories (fraud yes/no, species)
Regression: Predicting continuous values (price, temperature)
Metrics differ: Accuracy vs RMSE

**Q10: Explain gradient descent.**
A: Iterative optimization algorithm
Steps:
1. Start with random weights
2. Calculate loss
3. Compute gradient (direction of steepest increase)
4. Update weights in opposite direction
5. Repeat until convergence

Variants: Batch, Stochastic (SGD), Mini-batch

**Q11: What are decision trees? Pros/cons?**
Tree-based model splitting data by features
Pros: Interpretable, handles non-linear, no scaling needed
Cons: Overfits easily, unstable, biased to dominant classes
Solutions: Pruning, Random Forest, Gradient Boosting

**Q12: Random Forest vs Gradient Boosting?**
Random Forest (Bagging):
- Parallel independent trees
- Reduces variance
- Less prone to overfitting
- Faster training

Gradient Boosting:
- Sequential trees correcting errors
- Reduces bias
- Often better accuracy
- Slower, more prone to overfitting
- Needs tuning

**Q13: What is feature engineering?**
Creating new features from existing data
Examples:
- Combining features: total_price = quantity × unit_price
- Binning: age groups from age
- Encoding: one-hot, target encoding
- Date features: day_of_week, month, is_weekend
- Aggregations: customer_avg_purchase

**Q14: How to handle missing values in ML?**
- Drop: If small percentage (<5%)
- Mean/median imputation: For numerical
- Mode/frequent: For categorical
- Predictive imputation: Model to predict missing
- Flag missing: Add "is_missing" indicator
- Forward/backward fill: For time-series

**Q15: Feature scaling - why important?**
Algorithms affected: KNN, SVM, Neural Networks, Gradient Descent
Not affected: Tree-based models
Methods:
- StandardScaler: Mean=0, Std=1
- MinMaxScaler: Scale to [0,1]
- RobustScaler: Handles outliers

**Q16: What is one-hot encoding?**
Converting categorical to binary columns
Example: Color (Red, Blue, Green) → Color_Red, Color_Blue, Color_Green
Use when: No ordinal relationship
Alternative: Label encoding (when ordinal)

**Q17: Feature selection methods?**
- Filter: Statistical tests (correlation, chi-square)
- Wrapper: Try subsets (forward/backward selection)
- Embedded: Built into model (Lasso, tree importance)
- Dimensionality reduction: PCA

**Q18: Train/validation/test split?**
Training: Fit model (60-70%)
Validation: Tune hyperparameters (15-20%)
Test: Final evaluation (15-20%)
Why separate test: Unbiased performance estimate

**Q19: What is data leakage?**
Training data contains information about target not available at prediction time
Examples:
- Using future data to predict past
- Target encoding without proper splitting
- Including duplicate test samples in training
Prevention: Careful feature engineering, proper CV

**Q20: Bagging vs Boosting?**
Bagging: Parallel models, reduce variance (Random Forest)
Boosting: Sequential models, reduce bias (XGBoost, AdaBoost)
Use bagging: High variance models
Use boosting: Better accuracy needed

---

### Advanced ML (15 Questions)

**Q21: Explain ensemble methods.**
Combining multiple models for better predictions
Types:
- Voting: Majority vote or average
- Bagging: Bootstrap + aggregate
- Boosting: Sequential error correction
- Stacking: Meta-model on predictions

**Q22: What is clustering? Name algorithms.**
Unsupervised learning to group similar data
Algorithms:
- K-means: Partition into k clusters
- Hierarchical: Build tree of clusters
- DBSCAN: Density-based, finds arbitrary shapes
- Gaussian Mixture: Probabilistic clustering

**Q23: Explain K-means.**
1. Initialize k centroids randomly
2. Assign each point to nearest centroid
3. Recalculate centroids as mean of assigned points
4. Repeat until convergence

Choosing k: Elbow method, silhouette score

**Q24: What is dimensionality reduction?**
Reducing number of features while preserving information
Why: Visualization, reduce overfitting, faster training
Methods: PCA, t-SNE, UMAP, feature selection

**Q25: Explain PCA.**
Principal Component Analysis: Linear transformation to uncorrelated components
Finds directions of maximum variance
Use for: Visualization (2D/3D), noise reduction, feature extraction

**Q26: Curse of dimensionality?**
As dimensions increase:
- Distance metrics become less meaningful
- Data becomes sparse
- More data needed
- Models overfit easier
Solutions: Feature selection, dimensionality reduction, regularization

**Q27: Regression model evaluation metrics?**
- MSE: Mean Squared Error (penalizes large errors)
- RMSE: Root MSE (same units as target)
- MAE: Mean Absolute Error (robust to outliers)
- R²: Explained variance (0=bad, 1=perfect)
- MAPE: Mean Absolute Percentage Error (relative)

**Q28: Classification metrics?**
- Accuracy: Overall correct (misleading for imbalanced)
- Precision: TP / (TP + FP)
- Recall: TP / (TP + FN)
- F1-Score: Harmonic mean
- ROC-AUC: Threshold-independent
- Confusion Matrix: Full picture

**Q29: Hyperparameter tuning methods?**
- Grid Search: Try all combinations (exhaustive, slow)
- Random Search: Random samples (faster, good enough)
- Bayesian Optimization: Smart search (efficient)
- Hyperband: Resource-aware early stopping

**Q30: What is cross-validation?**
K-Fold: Split data into k parts, rotate validation
Stratified: Maintain class distribution
Time-series: Use past to predict future
Leave-one-out: Each sample as validation
Purpose: Robust performance estimate, prevent overfitting

**Q31: Explain neural networks basics.**
Layers of connected neurons:
- Input layer: Features
- Hidden layers: Learn representations
- Output layer: Predictions
- Activation functions: Non-linearity (ReLU, Sigmoid, Tanh)
- Backpropagation: Update weights using gradients

**Q32: Activation functions - when to use?**
- ReLU: Default for hidden layers (fast, avoids vanishing gradient)
- Sigmoid: Binary classification output (0-1)
- Softmax: Multi-class output (probabilities sum to 1)
- Tanh: Alternative to ReLU (-1 to 1)
- Leaky ReLU: Solves dying ReLU problem

**Q33: What is batch normalization?**
Normalizes layer inputs during training
Benefits: Faster training, allows higher learning rates, regularization effect

**Q34: Dropout - what and why?**
Randomly drops neurons during training
Prevents overfitting by reducing co-adaptation
Typical rate: 0.2-0.5

**Q35: Transfer learning?**
Using pre-trained model as starting point
Common in: Computer vision (ImageNet), NLP (BERT)
Benefits: Less data needed, faster training, better performance

---

### Python/Scikit-Learn (15 Questions)

**Q36: Train/test split in sklearn?**
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**Q37: Implement k-fold cross-validation?**
```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
scores = cross_val_score(model, X, y, cv=5, scoring='f1')
print(f"Mean F1: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

**Q38: Create ML pipeline?**
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
pipeline.fit(X_train, y_train)
```

**Q39: Handle categorical variables?**
```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(), categorical_features)
])
```

**Q40: Grid search hyperparameters?**
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10]
}
grid = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
grid.fit(X_train, y_train)
print(f"Best params: {grid.best_params_}")
```

**Q41: Save and load model?**
```python
import joblib

# Save
joblib.dump(model, 'model.pkl')

# Load
model = joblib.load('model.pkl')
```

**Q42: Calculate feature importance?**
```python
# Tree-based models
importances = model.feature_importances_
feature_imp = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=False)

# Permutation importance (works for any model)
from sklearn.inspection import permutation_importance
perm_imp = permutation_importance(model, X_test, y_test)
```

**Q43: Handle imbalanced classes in code?**
```python
from sklearn.utils import class_weight
from imblearn.over_sampling import SMOTE

# Class weights
weights = class_weight.compute_class_weight(
    'balanced', classes=np.unique(y), y=y
)
model = RandomForestClassifier(class_weight='balanced')

# SMOTE
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X, y)
```

**Q44: Plot ROC curve?**
```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

y_pred_proba = model.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label=f'ROC (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()
```

**Q45: Implement early stopping?**
```python
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(
    n_estimators=1000,
    validation_fraction=0.1,
    n_iter_no_change=10,  # Stop if no improvement for 10 iterations
    tol=0.001
)
```

**Q46: Custom scorer?**
```python
from sklearn.metrics import make_scorer

def custom_metric(y_true, y_pred):
    # Your custom logic
    return score

scorer = make_scorer(custom_metric, greater_is_better=True)
cross_val_score(model, X, y, scoring=scorer)
```

**Q47: Stratified sampling?**
```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(X, y):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
```

**Q48: Pipeline with feature selection?**
```python
from sklearn.feature_selection import SelectKBest, f_classif

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('feature_selection', SelectKBest(f_classif, k=10)),
    ('model', LogisticRegression())
])
```

**Q49: Ensemble voting classifier?**
```python
from sklearn.ensemble import VotingClassifier

estimators = [
    ('rf', RandomForestClassifier()),
    ('lr', LogisticRegression()),
    ('svm', SVC(probability=True))
]
voting = VotingClassifier(estimators, voting='soft')
voting.fit(X_train, y_train)
```

**Q50: Handle outliers?**
```python
from sklearn.preprocessing import RobustScaler

# Robust to outliers
scaler = RobustScaler()

# Or remove outliers
from scipy import stats
z_scores = np.abs(stats.zscore(X))
X_clean = X[(z_scores < 3).all(axis=1)]
```

---

### Model Deployment & MLOps (15 Questions)

**Q51: How to deploy ML model to production?**
Options:
1. REST API (Flask/FastAPI)
2. Batch predictions (scheduled jobs)
3. Cloud services (SageMaker, Vertex AI)
4. Edge deployment (mobile, IoT)

**Q52: Create Flask API for model?**
```python
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict([data['features']])
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run()
```

**Q53: What is model monitoring?**
Tracking model performance in production
Monitor:
- Prediction distribution
- Feature distribution (drift)
- Performance metrics
- Latency, errors
- Business metrics

**Q54: What is data drift?**
When input data distribution changes over time
Example: COVID changed shopping patterns
Detection: Statistical tests, model performance decline
Solution: Retrain with new data

**Q55: What is concept drift?**
Relationship between features and target changes
Example: New fraud patterns emerge
Detection: Performance degradation
Solution: Regular retraining

**Q56: A/B testing for models?**
Compare new model vs current in production
Process:
1. Split traffic (e.g., 95% old, 5% new)
2. Measure metrics (accuracy, latency, business KPIs)
3. Statistical significance test
4. Gradual rollout if better

**Q57: Model versioning?**
Track different model versions
Tools: MLflow, DVC, Git LFS
Track: Code, data version, hyperparameters, metrics
Why: Reproducibility, rollback capability, experimentation

**Q58: What is MLflow?**
Open-source MLOps platform
Features:
- Experiment tracking
- Model registry
- Model deployment
- Project packaging

**Q59: CI/CD for ML?**
Automated testing and deployment
Tests:
- Unit tests (functions)
- Integration tests (pipeline)
- Model tests (performance thresholds)
- Data validation
Tools: Jenkins, GitHub Actions, GitLab CI

**Q60: Containerize ML model?**
```dockerfile
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY model.pkl app.py .
CMD ["python", "app.py"]
```

**Q61: Model explainability?**
Understanding model predictions
Methods:
- SHAP: Feature contribution per prediction
- LIME: Local interpretable explanations
- Feature importance: Global explanations
- Partial dependence plots

**Q62: Online vs offline learning?**
Offline: Batch training on historical data (most common)
Online: Incremental learning from streaming data
Use online for: High-velocity data, concept drift

**Q63: Model retraining strategy?**
- Time-based: Weekly, monthly
- Performance-based: When metrics degrade
- Data-based: When significant new data available
- Hybrid: Combine triggers

**Q64: Feature store?**
Centralized repository for features
Benefits:
- Feature reuse across models
- Consistency train/serve
- Faster experimentation
- Feature versioning
Tools: Feast, Tecton, AWS Feature Store

**Q65: Batch vs real-time prediction?**
Batch: Pre-compute predictions (daily recommendations)
Real-time: On-demand predictions (fraud detection)
Choose based on: Latency requirements, volume, cost

---

### Business & Scenarios (15 Questions)

**Q66: How would you approach a new ML problem?**
1. Understand business problem and success metrics
2. Explore and understand data
3. Define ML problem (classification, regression, etc.)
4. Establish baseline
5. Feature engineering
6. Model selection and training
7. Evaluation and iteration
8. Deployment and monitoring

**Q67: Model performance degrading - what to do?**
1. Check for data drift
2. Verify data pipeline integrity
3. Review recent changes
4. Analyze error cases
5. Retrain if needed
6. Monitor closely

**Q68: Explain model to non-technical stakeholder.**
- Avoid jargon
- Use analogies
- Focus on business impact
- Show visualizations
- Provide confidence metrics
- Discuss limitations

**Q69: How to measure model business impact?**
Connect to business metrics:
- Revenue increase
- Cost reduction
- Customer satisfaction
- Time saved
- Risk reduced
A/B test in production to measure true impact

**Q70: Handle missing labels in semi-supervised learning?**
- Pseudo-labeling: Model labels unlabeled data
- Self-training: Iteratively add confident predictions
- Co-training: Multiple views of data
- Active learning: Selectively label most informative

**Q71: Model says 90% accuracy - is it good?**
Depends on:
- Baseline (random, simple model)
- Class balance (90% accuracy with 90% majority class = useless)
- Business cost of errors
- Comparison to alternatives
- Domain standards

**Q72: Choose between multiple models?**
Consider:
- Performance metrics (on validation set)
- Inference latency
- Training time and cost
- Interpretability needs
- Maintenance complexity
- Stakeholder requirements

**Q73: Prevent overfitting in practice?**
- Use cross-validation
- More training data
- Regularization
- Simpler model
- Feature selection
- Early stopping
- Ensemble methods

**Q74: When to use deep learning vs traditional ML?**
Deep Learning: Large data, complex patterns, images/text/audio, computation available
Traditional ML: Small data, interpretability needed, tabular data, limited resources

**Q75: Handling class imbalance in business scenario?**
Example: Fraud (0.1% fraud)
- Don't use accuracy
- Use precision/recall, F1
- Class weights or SMOTE
- Consider business cost (missing fraud vs false alarms)
- Maybe predict probability and set threshold

**Q76: Feature engineering for time-series?**
- Lag features (previous values)
- Rolling statistics (7-day average)
- Time features (hour, day_of_week, month)
- Seasonality indicators
- Rate of change
- Domain-specific features

**Q77: Cold start problem in recommendations?**
New users/items with no history
Solutions:
- Content-based features
- Use demographics
- Popular items as default
- Hybrid approach
- Active learning (ask preferences)

**Q78: Ethical considerations in ML?**
- Bias in training data
- Fairness across groups
- Privacy and data protection
- Transparency and explainability
- Accountability for decisions
- Unintended consequences

**Q79: What makes a good feature?**
- Correlation with target
- Low correlation with other features
- Available at prediction time
- Stable over time
- Interpretable
- Computationally feasible

**Q80: Debugging poor model performance?**
1. Check data quality and labels
2. Verify preprocessing
3. Analyze error cases
4. Try simpler model (can it learn?)
5. More data or better features?
6. Hyperparameter tuning
7. Ensemble methods

---

## 🎤 INTERVIEW TIPS FOR DATA SCIENTISTS

### Technical Round Prep:
- Practice coding ML algorithms from scratch
- Understand math behind models
- Be ready for live coding
- Explain trade-offs clearly
- Know when to use each algorithm

### Take-Home Projects:
- Read requirements carefully
- Show complete workflow
- Document assumptions
- Provide clean, readable code
- Include visualizations
- Explain business impact

### Behavioral Round:
- STAR method for stories
- Prepare examples of:
  - Complex project you built
  - Dealing with ambiguity
  - Model failure and learning
  - Stakeholder communication
  - Team collaboration

### Questions to Ask:
- What ML problems is the team solving?
- What's the data infrastructure?
- How are models deployed?
- What tools and frameworks used?
- How is success measured?
- Opportunities for growth?

---

## 💡 LINKEDIN FOR DATA SCIENTISTS

### Headline:
"Data Scientist | ML, Python, Deep Learning | Building Predictive Models"

### Skills to Highlight:
1. Machine Learning
2. Python
3. Deep Learning
4. TensorFlow / PyTorch
5. Scikit-learn
6. Statistical Modeling
7. Feature Engineering
8. Model Deployment
9. Data Analysis
10. SQL

---

**Complete career prep for Data Scientist roles!**

Practice these questions, build strong ML portfolio, and ace your interviews.

**Good luck! 🚀**
"""
            pdf = create_unit_pdf(0, "Career Prep - Data Scientist", career_prep_md)
            st.download_button(
                label="Download Career Prep Package PDF",
                data=pdf,
                file_name="Career_Prep_Package_Data_Scientist.pdf",
                mime="application/pdf",
                key="dsp2_career_prep_pdf_dl",
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
