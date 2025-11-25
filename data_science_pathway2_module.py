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

    st.markdown("---")
    st.markdown("#### 🔧 Detailed Feature Engineering Techniques")
    st.markdown(
        """**1. Missing Value Strategies with Code**

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# Sample data with missing values
data = {
    'age': [25, np.nan, 35, 28, np.nan, 45],
    'income': [50000, 60000, np.nan, 55000, 70000, np.nan],
    'country': ['UK', 'USA', np.nan, 'UK', 'France', 'USA']
}
df = pd.DataFrame(data)

# Strategy 1: Simple imputation
from sklearn.impute import SimpleImputer

# Numeric imputation (median)
num_imputer = SimpleImputer(strategy='median')
df[['age', 'income']] = num_imputer.fit_transform(df[['age', 'income']])

# Strategy 2: Add missing indicator
df['age_missing'] = df['age'].isna().astype(int)
df['income_missing'] = df['income'].isna().astype(int)

# Strategy 3: Categorical imputation (constant)
df['country'] = df['country'].fillna('Unknown')
```

---

**2. Categorical Encoding Examples**

```python
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Sample categorical data
countries = pd.DataFrame({'country': ['UK', 'USA', 'UK', 'France', 'USA']})

# One-Hot Encoding
encoder = OneHotEncoder(sparse=False, drop='first')  # drop first to avoid multicollinearity
encoded = encoder.fit_transform(countries[['country']])
encoded_df = pd.DataFrame(
    encoded, 
    columns=encoder.get_feature_names_out(['country'])
)
print(encoded_df)

# Output:
#    country_UK  country_USA
# 0         1.0          0.0
# 1         0.0          1.0
# 2         1.0          0.0
# 3         0.0          0.0  # France (baseline)
# 4         0.0          1.0
```

---

**3. Feature Scaling Comparison**

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Sample data with outliers
data = np.array([[1], [2], [3], [4], [100]])  # 100 is outlier

# StandardScaler (sensitive to outliers)
standard = StandardScaler().fit_transform(data)
print("Standard:", standard.flatten())

# MinMaxScaler (very sensitive to outliers)
minmax = MinMaxScaler().fit_transform(data)
print("MinMax:", minmax.flatten())

# RobustScaler (robust to outliers)
robust = RobustScaler().fit_transform(data)
print("Robust:", robust.flatten())

# Choose based on your data:
# - StandardScaler: Normal distribution
# - MinMaxScaler: Bounded range needed
# - RobustScaler: Outliers present
```

---

**4. Creating Derived Features**

```python
# E-commerce customer features
orders = pd.DataFrame({
    'customer_id': [1, 1, 2, 2, 2, 3],
    'order_date': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-01-15', 
                                    '2024-02-20', '2024-03-10', '2024-03-01']),
    'amount': [100, 150, 200, 50, 300, 75]
})

# Feature 1: Recency (days since last order)
analysis_date = pd.to_datetime('2024-04-01')
customer_features = orders.groupby('customer_id').agg({
    'order_date': lambda x: (analysis_date - x.max()).days,
    'amount': ['sum', 'mean', 'count']
}).reset_index()

customer_features.columns = ['customer_id', 'recency', 'total_spend', 
                               'avg_order_value', 'order_frequency']

# Feature 2: Spend velocity (£ per day)
first_order = orders.groupby('customer_id')['order_date'].min()
last_order = orders.groupby('customer_id')['order_date'].max()
days_active = (last_order - first_order).dt.days + 1
customer_features['spend_velocity'] = customer_features['total_spend'] / days_active.values

print(customer_features)
```

---

**5. Time-Based Features**

```python
# Extract temporal features
df = pd.DataFrame({
    'timestamp': pd.to_datetime(['2024-01-15 14:30', '2024-02-20 09:15', 
                                  '2024-03-10 22:45', '2024-04-05 17:00'])
})

# Extract components
df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day_of_week'] = df['timestamp'].dt.dayofweek  # 0=Monday
df['hour'] = df['timestamp'].dt.hour
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['is_business_hours'] = df['hour'].between(9, 17).astype(int)
df['quarter'] = df['timestamp'].dt.quarter

# Cyclical encoding (for hour, month)
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🔨 Building Production Pipelines")
    st.markdown(
        """**Complete Feature Pipeline Example**

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Define column types
numeric_features = ['age', 'income', 'credit_score']
categorical_features = ['country', 'education', 'employment_type']

# Numeric pipeline
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical pipeline
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

# Combine into preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Use in full ML pipeline
from sklearn.ensemble import RandomForestClassifier

ml_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# Train
ml_pipeline.fit(X_train, y_train)

# Predict (preprocessing happens automatically!)
predictions = ml_pipeline.predict(X_test)
```

**Why Pipelines?**
- ✅ Prevent data leakage
- ✅ Reproducible (same transforms for train/test)
- ✅ Production-ready (single object to save)
- ✅ Cleaner code
"""
    )

    st.markdown("---")
    st.markdown("#### ⚠️ Common Feature Engineering Mistakes")
    st.markdown(
        """**1. Data Leakage**

```python
# ❌ WRONG: Scale before split
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Leakage! Test data influenced scaling
X_train, X_test = train_test_split(X_scaled)

# ✅ RIGHT: Split first, then scale
X_train, X_test = train_test_split(X)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit on train only
X_test_scaled = scaler.transform(X_test)  # Transform test using train params
```

---

**2. Target Leakage**

```python
# ❌ WRONG: Feature contains future information
df['will_churn'] = df['days_until_churn'] < 30  # Leakage! You wouldn't know this

# ✅ RIGHT: Use only past information
df['recency'] = (pd.Timestamp.now() - df['last_purchase_date']).dt.days
```

---

**3. High Cardinality Categoricals**

```python
# ❌ WRONG: One-hot encode 1000 unique customer IDs
# Creates 1000 columns, causes overfitting

# ✅ RIGHT: Use target encoding or frequency encoding
from category_encoders import TargetEncoder

encoder = TargetEncoder()
X_train_encoded = encoder.fit_transform(X_train['customer_id'], y_train)
X_test_encoded = encoder.transform(X_test['customer_id'])
```

---

**4. Not Handling Unknown Categories**

```python
# ❌ WRONG: Encoder fails on new category
encoder = OneHotEncoder()
encoder.fit(train['country'])
test_encoded = encoder.transform(test['country'])  # Error if new country!

# ✅ RIGHT: Handle unknown
encoder = OneHotEncoder(handle_unknown='ignore')
encoder.fit(train[['country']])
test_encoded = encoder.transform(test[['country']])  # Unknown → all zeros
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎯 Feature Selection Techniques")
    st.markdown(
        """**Why Feature Selection Matters:**
- Reduces overfitting
- Improves model speed
- Enhances interpretability
- Removes noise

**1. Filter Methods (Fast, Pre-modeling)**

```python
from sklearn.feature_selection import SelectKBest, f_classif

# Select top 10 features by ANOVA F-value
selector = SelectKBest(f_classif, k=10)
X_selected = selector.fit_transform(X, y)

# Get selected feature names
selected_features = X.columns[selector.get_support()]
print(f"Selected: {selected_features.tolist()}")
```

---

**2. Wrapper Methods (Model-Based)**

```python
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

# Recursive Feature Elimination
model = RandomForestClassifier()
rfe = RFE(estimator=model, n_features_to_select=10)
X_selected = rfe.fit_transform(X, y)

print(f"Selected features: {X.columns[rfe.support_].tolist()}")
print(f"Feature ranking: {rfe.ranking_}")
```

---

**3. Embedded Methods (Built into model)**

```python
from sklearn.ensemble import RandomForestClassifier

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Get feature importances
importance_df = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

# Select top features
top_features = importance_df.head(10)['feature'].tolist()
X_train_selected = X_train[top_features]
```

---

**4. Variance Threshold (Remove Low-Variance)**

```python
from sklearn.feature_selection import VarianceThreshold

# Remove features with <1% variance
selector = VarianceThreshold(threshold=0.01)
X_high_variance = selector.fit_transform(X)

print(f"Removed {X.shape[1] - X_high_variance.shape[1]} low-variance features")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 📊 Real-World Feature Engineering Examples")
    st.markdown(
        """**E-Commerce Churn Prediction Features**

```python
# Input: Raw transaction data
# Output: Customer-level features for churn prediction

def create_customer_features(transactions, analysis_date='2024-04-01'):
    analysis_date = pd.to_datetime(analysis_date)
    
    features = transactions.groupby('customer_id').agg({
        # Recency
        'order_date': lambda x: (analysis_date - x.max()).days,
        
        # Frequency
        'order_id': 'count',
        
        # Monetary
        'amount': ['sum', 'mean', 'std'],
        
        # Additional behavioral features
        'product_category': lambda x: x.nunique(),  # Diversity
    }).reset_index()
    
    features.columns = ['customer_id', 'recency', 'frequency', 
                        'monetary', 'avg_order', 'order_std', 'category_diversity']
    
    # Derived features
    features['order_consistency'] = 1 / (features['order_std'] + 1)
    features['is_high_value'] = (features['monetary'] > features['monetary'].quantile(0.75)).astype(int)
    features['is_at_risk'] = (features['recency'] > 90).astype(int)
    
    return features
```

---

**Credit Scoring Features**

```python
def create_credit_features(applicant_data):
    features = applicant_data.copy()
    
    # Income ratios
    features['debt_to_income'] = features['total_debt'] / features['annual_income']
    features['credit_utilization'] = features['credit_used'] / features['credit_limit']
    
    # Age-based features
    features['years_employed'] = (pd.Timestamp.now() - features['employment_start_date']).dt.days / 365
    features['credit_age_years'] = (pd.Timestamp.now() - features['first_credit_date']).dt.days / 365
    
    # Risk indicators
    features['has_recent_delinquency'] = (features['months_since_delinquency'] < 6).astype(int)
    features['high_debt_ratio'] = (features['debt_to_income'] > 0.4).astype(int)
    
    # Stability score (custom)
    features['stability_score'] = (
        features['years_employed'] * 0.3 +
        features['credit_age_years'] * 0.3 +
        (1 - features['credit_utilization']) * 0.4
    )
    
    return features
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🚀 Interview Preparation")
    st.markdown(
        """**Common Feature Engineering Interview Questions**

**Q1: "What's the difference between one-hot encoding and label encoding?"**

**Answer:** 
- **Label encoding** assigns integers to categories (Red=0, Blue=1, Green=2). Use for ordinal data with natural order.
- **One-hot encoding** creates binary columns for each category. Use for nominal data without order. Prevents model from assuming false ordinal relationships.

---

**Q2: "How do you handle missing values in production?"**

**Answer:**
1. **Understand why data is missing** (MCAR, MAR, MNAR)
2. **Document the strategy** in pipeline
3. **Add missing indicators** as separate features
4. **Use robust imputation** (median for outliers, mode for categoricals)
5. **Monitor missing rates** in production (drift detection)

---

**Q3: "Explain data leakage and how to prevent it."**

**Answer:**
Data leakage = using information from test/future data during training.

**Prevention:**
- Split data FIRST, preprocess AFTER
- Fit transformers on train only, transform test
- Use Pipelines to automate proper workflow
- Cross-validation with proper folds
- Don't use target or future information in features

---

**Q4: "When would you NOT scale features?"**

**Answer:**
- Tree-based models (Random Forest, XGBoost) - invariant to scaling
- Already on same scale
- Interpreting coefficients in original units important
- Binary features (already 0/1)

---

**Q5: "How do you create features from timestamps?"**

**Answer:**
- **Extract:** hour, day_of_week, month, quarter, year
- **Cyclical encoding:** sin/cos for hour, month (preserves cyclical nature)
- **Relative:** days_since_event, time_to_deadline
- **Business logic:** is_business_hours, is_weekend, is_holiday
- **Interactions:** weekend AND night, holiday AND retail_sector
"""
    )

    st.markdown("---")
    st.markdown("#### 📚 Best Practices & Tips")
    st.markdown(
        """**Feature Engineering Workflow**

1. **Start Simple**
   - Load data, basic cleaning
   - Create obvious features first
   - Establish baseline model

2. **Iterative Improvement**
   - Analyze feature importances
   - Create features based on domain knowledge
   - Test impact on validation set

3. **Document Everything**
   - Why each feature was created
   - Transformation logic
   - Expected value ranges

4. **Version Control**
   - Save feature creation code
   - Track feature sets (v1, v2, v3)
   - Log performance by feature set

5. **Monitor in Production**
   - Feature drift (distributions change)
   - Missing value rates increase
   - New categories appear

---

**Tools & Resources:**

- **Libraries:** scikit-learn, category_encoders, feature-engine
- **Books:** "Feature Engineering for Machine Learning" (Alice Zheng)
- **Practice:** Kaggle competitions (study winning solutions)
- **Blog:** machinelearningmastery.com/feature-engineering

---

**What You Can Do Now:**
- ✅ Build production-ready feature pipelines
- ✅ Handle missing data strategically
- ✅ Encode categorical variables correctly
- ✅ Create meaningful derived features
- ✅ Prevent data leakage
- ✅ Select most important features
- ✅ Answer interview questions confidently

**Next:** Unit 2 (Regression) teaches you to build predictive models with these features!
"""
    )

def _render_unit1_labs():
    """Labs and mini-project ideas for Unit 1."""

    st.markdown("### 🧪 HANDS-ON LABS: Unit 1 Feature Engineering")
    st.markdown(
        """**Complete these 3 labs to master feature pipelines:**

---

## Lab 1: Build Complete Feature Pipeline (90 min)

**Objective:** Transform raw customer data into ML-ready features

**Setup: Create Raw Dataset**

```python
import pandas as pd
import numpy as np

# Simulate messy real-world data
np.random.seed(42)
n = 1000

raw_data = pd.DataFrame({
    'customer_id': range(1, n+1),
    'age': np.random.normal(35, 12, n),
    'income': np.random.lognormal(10.5, 0.5, n),
    'credit_score': np.random.normal(650, 100, n),
    'country': np.random.choice(['UK', 'USA', 'Germany', 'France', None], n, p=[0.4, 0.3, 0.15, 0.1, 0.05]),
    'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD', None], n, p=[0.2, 0.4, 0.25, 0.1, 0.05]),
    'employment_type': np.random.choice(['Full-time', 'Part-time', 'Self-employed', None], n, p=[0.6, 0.2, 0.15, 0.05]),
    'months_employed': np.random.exponential(36, n),
    'num_accounts': np.random.poisson(2, n),
    'total_balance': np.random.lognormal(8, 1.5, n),
    'churned': np.random.choice([0, 1], n, p=[0.85, 0.15])
})

# Introduce missing values
raw_data.loc[raw_data.sample(frac=0.1).index, 'income'] = np.nan
raw_data.loc[raw_data.sample(frac=0.08).index, 'credit_score'] = np.nan
raw_data.loc[raw_data.sample(frac=0.05).index, 'months_employed'] = np.nan

raw_data.to_csv('raw_customer_data.csv', index=False)
print("✅ Created raw_customer_data.csv")
print(f"Shape: {raw_data.shape}")
print(f"\\nMissing values:\\n{raw_data.isnull().sum()}")
```

---

**Part A: Explore and Understand (20 min)**

```python
import pandas as pd
import numpy as np

df = pd.read_csv('raw_customer_data.csv')

# 1. Basic exploration
print("Dataset shape:", df.shape)
print("\\nColumn types:")
print(df.dtypes)

# 2. Missing value analysis
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing': missing,
    'Percentage': missing_pct
}).sort_values('Missing', ascending=False)
print("\\nMissing values:")
print(missing_df[missing_df['Missing'] > 0])

# 3. Identify column types
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# Remove ID and target
numeric_cols.remove('customer_id')
numeric_cols.remove('churned')

print(f"\\nNumeric features: {numeric_cols}")
print(f"Categorical features: {categorical_cols}")

# 4. Check distributions
print("\\nNumeric distributions:")
print(df[numeric_cols].describe())

# 5. Check categorical cardinality
print("\\nCategorical value counts:")
for col in categorical_cols:
    print(f"\\n{col}:")
    print(df[col].value_counts(dropna=False))
```

---

**Part B: Build Feature Pipeline (40 min)**

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# Prepare data
X = df.drop(['customer_id', 'churned'], axis=1)
y = df['churned']

# Split FIRST (prevent leakage)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# Define transformers for numeric features
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Define transformers for categorical features
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

# Combine transformers
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols)
    ],
    remainder='drop'  # Drop any other columns
)

# Fit on training data
preprocessor.fit(X_train)

# Transform both sets
X_train_transformed = preprocessor.transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

print(f"\\nTransformed shape: {X_train_transformed.shape}")
print("Feature engineering complete!")

# Get feature names
cat_features = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_cols)
all_features = numeric_cols + list(cat_features)
print(f"\\nTotal features: {len(all_features)}")
```

---

**Part C: Create Derived Features (30 min)**

```python
from sklearn.preprocessing import FunctionTransformer

def create_business_features(X):
    \"\"\"Create custom business logic features\"\"\"
    X_new = X.copy()
    
    # Financial ratios
    X_new['balance_per_account'] = X_new['total_balance'] / (X_new['num_accounts'] + 1)
    X_new['income_to_balance_ratio'] = X_new['income'] / (X_new['total_balance'] + 1)
    
    # Employment stability
    X_new['is_stable_employment'] = (X_new['months_employed'] > 24).astype(int)
    X_new['employment_years'] = X_new['months_employed'] / 12
    
    # Credit risk indicators
    X_new['is_high_credit'] = (X_new['credit_score'] > 700).astype(int)
    X_new['is_low_credit'] = (X_new['credit_score'] < 600).astype(int)
    
    # Age groups
    X_new['is_young'] = (X_new['age'] < 30).astype(int)
    X_new['is_senior'] = (X_new['age'] > 60).astype(int)
    
    return X_new

# Create extended pipeline with custom features
custom_feature_transformer = FunctionTransformer(create_business_features)

extended_pipeline = Pipeline(steps=[
    ('custom_features', custom_feature_transformer),
    ('preprocessor', preprocessor)
])

# Fit and transform
extended_pipeline.fit(X_train, y_train)
X_train_extended = extended_pipeline.transform(X_train)
X_test_extended = extended_pipeline.transform(X_test)

print(f"Extended features shape: {X_train_extended.shape}")
```

---

## Lab 2: Handle Real-World Data Issues (75 min)

**Objective:** Master advanced preprocessing techniques

**Part A: Outlier Detection and Treatment (25 min)**

```python
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt

# Detect outliers using IQR
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

# Check income for outliers
outliers, lower, upper = detect_outliers_iqr(df, 'income')
print(f"Income outliers: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")
print(f"Range: [{lower:.0f}, {upper:.0f}]")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Before
axes[0].boxplot(df['income'].dropna())
axes[0].set_title('Income (with outliers)')
axes[0].set_ylabel('Income')

# After (cap outliers)
income_capped = df['income'].clip(lower=lower, upper=upper)
axes[1].boxplot(income_capped.dropna())
axes[1].set_title('Income (outliers capped)')
axes[1].set_ylabel('Income')

plt.tight_layout()
plt.show()

# Strategy: Use RobustScaler for features with outliers
outlier_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', RobustScaler())  # Robust to outliers
])
```

---

**Part B: High Cardinality Categoricals (25 min)**

```python
# Simulate high cardinality feature
df['zip_code'] = np.random.randint(10000, 99999, len(df))

print(f"Unique zip codes: {df['zip_code'].nunique()}")

# Strategy 1: Frequency encoding
zip_freq = df['zip_code'].value_counts(normalize=True)
df['zip_frequency'] = df['zip_code'].map(zip_freq)

# Strategy 2: Target encoding (use with caution - risk of leakage!)
from category_encoders import TargetEncoder

# Must fit on train, transform on test
encoder = TargetEncoder(cols=['zip_code'])
df['zip_encoded'] = encoder.fit_transform(
    df[['zip_code']], 
    df['churned']
)

print("\\nFrequency encoding:")
print(df[['zip_code', 'zip_frequency']].head())

print("\\nTarget encoding:")
print(df[['zip_code', 'zip_encoded', 'churned']].head())

# Strategy 3: Grouping rare categories
def group_rare_categories(series, threshold=0.05):
    \"\"\"Group categories appearing < threshold into 'Other'\"\"\"
    value_counts = series.value_counts(normalize=True)
    rare_categories = value_counts[value_counts < threshold].index
    return series.replace(rare_categories, 'Other')

# Apply to country
df['country_grouped'] = group_rare_categories(df['country'], threshold=0.05)
print("\\nBefore grouping:", df['country'].value_counts())
print("\\nAfter grouping:", df['country_grouped'].value_counts())
```

---

**Part C: Missing Value Strategies (25 min)**

```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer

# Strategy comparison
strategies = {
    'Mean': SimpleImputer(strategy='mean'),
    'Median': SimpleImputer(strategy='median'),
    'KNN': KNNImputer(n_neighbors=5),
    'Iterative': IterativeImputer(random_state=42)
}

# Test on income (has missing values)
income_data = df[['income']].copy()
original_missing = income_data['income'].isna()

results = {}
for name, imputer in strategies.items():
    imputed = imputer.fit_transform(income_data)
    # Calculate imputed values statistics
    imputed_values = imputed[original_missing.values, 0]
    results[name] = {
        'mean': imputed_values.mean(),
        'std': imputed_values.std(),
        'min': imputed_values.min(),
        'max': imputed_values.max()
    }

# Compare strategies
comparison_df = pd.DataFrame(results).T
print("Imputation strategy comparison:")
print(comparison_df)

# Add missing indicator
df['income_missing'] = df['income'].isna().astype(int)
print(f"\\nMissing indicator added: {df['income_missing'].sum()} customers")
```

---

## Lab 3: Production Pipeline (60 min)

**Objective:** Build, save, and deploy a complete ML pipeline

**Part A: Build Full ML Pipeline (20 min)**

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# Build complete pipeline
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    ))
])

# Train
full_pipeline.fit(X_train, y_train)

# Predict
y_pred = full_pipeline.predict(X_test)
y_pred_proba = full_pipeline.predict_proba(X_test)[:, 1]

# Evaluate
print("Classification Report:")
print(classification_report(y_test, y_pred))
print(f"\\nROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Feature importance
feature_importance = full_pipeline.named_steps['classifier'].feature_importances_
importance_df = pd.DataFrame({
    'feature': all_features,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

print("\\nTop 10 features:")
print(importance_df.head(10))
```

---

**Part B: Save and Load Pipeline (15 min)**

```python
import joblib
import json

# Save pipeline
joblib.dump(full_pipeline, 'customer_churn_pipeline.pkl')
print("✅ Pipeline saved to customer_churn_pipeline.pkl")

# Save feature names and metadata
metadata = {
    'numeric_features': numeric_cols,
    'categorical_features': categorical_cols,
    'all_features': all_features,
    'train_shape': X_train.shape,
    'model_type': 'RandomForestClassifier',
    'roc_auc': float(roc_auc_score(y_test, y_pred_proba))
}

with open('pipeline_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print("✅ Metadata saved to pipeline_metadata.json")

# Load pipeline
loaded_pipeline = joblib.load('customer_churn_pipeline.pkl')

# Test loaded pipeline
test_sample = X_test.head(1)
prediction = loaded_pipeline.predict(test_sample)
prediction_proba = loaded_pipeline.predict_proba(test_sample)

print(f"\\nTest prediction: {prediction[0]}")
print(f"Churn probability: {prediction_proba[0][1]:.2%}")
```

---

**Part C: Create Prediction Function (25 min)**

```python
def predict_churn(customer_data, pipeline_path='customer_churn_pipeline.pkl'):
    \"\"\"
    Predict customer churn using trained pipeline
    
    Args:
        customer_data: DataFrame with customer features
        pipeline_path: Path to saved pipeline
    
    Returns:
        DataFrame with predictions and probabilities
    \"\"\"
    # Load pipeline
    pipeline = joblib.load(pipeline_path)
    
    # Make predictions
    predictions = pipeline.predict(customer_data)
    probabilities = pipeline.predict_proba(customer_data)[:, 1]
    
    # Create results dataframe
    results = customer_data.copy()
    results['churn_prediction'] = predictions
    results['churn_probability'] = probabilities
    results['risk_level'] = pd.cut(
        probabilities,
        bins=[0, 0.3, 0.7, 1.0],
        labels=['Low', 'Medium', 'High']
    )
    
    return results[['customer_id', 'churn_prediction', 'churn_probability', 'risk_level']]

# Test prediction function
new_customers = X_test.head(10).copy()
new_customers['customer_id'] = range(1, 11)

predictions = predict_churn(new_customers)
print("Churn predictions for new customers:")
print(predictions)

# Identify high-risk customers
high_risk = predictions[predictions['risk_level'] == 'High']
print(f"\\nHigh-risk customers: {len(high_risk)}")
print(high_risk)
```

---

**Lab Completion Checklist:**
- ☐ Built complete feature pipeline with ColumnTransformer
- ☐ Handled missing values appropriately
- ☐ Encoded categorical variables
- ☐ Created derived business features
- ☐ Detected and handled outliers
- ☐ Managed high cardinality features
- ☐ Built and evaluated full ML pipeline
- ☐ Saved pipeline to disk
- ☐ Created production prediction function

**Next:** Unit 2 teaches regression algorithms to use with these features!
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

    st.markdown("---")
    st.markdown("#### 🔢 Mathematical Foundations")
    st.markdown(
        """**Linear Regression Equation:**

$$y = β_0 + β_1x_1 + β_2x_2 + ... + β_nx_n + ε$$

Where:
- **y** = target variable (what we're predicting)
- **β₀** = intercept (baseline value)
- **β₁, β₂, ..., βₙ** = coefficients (feature weights)
- **x₁, x₂, ..., xₙ** = features
- **ε** = error term

**Goal:** Find coefficients that minimize prediction error

---

**Loss Functions:**

1. **Mean Squared Error (MSE):**
   $$MSE = \\frac{1}{n} \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2$$

2. **Root Mean Squared Error (RMSE):**
   $$RMSE = \\sqrt{MSE}$$ 
   - Same units as target variable
   - Penalizes large errors heavily

3. **Mean Absolute Error (MAE):**
   $$MAE = \\frac{1}{n} \\sum_{i=1}^{n} |y_i - \\hat{y}_i|$$
   - Less sensitive to outliers
   - More robust

4. **R² Score (Coefficient of Determination):**
   $$R^2 = 1 - \\frac{SS_{res}}{SS_{tot}}$$
   - Range: 0 to 1 (can be negative if model is terrible)
   - 0.8 = explains 80% of variance
"""
    )

    st.markdown("---")
    st.markdown("#### 🎯 Regression Algorithms")
    st.markdown(
        """**1. Linear Regression (Ordinary Least Squares)**

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Sample data: House prices
X = np.array([[1200], [1500], [1800], [2000], [2400]])  # Square footage
y = np.array([200000, 250000, 280000, 320000, 380000])  # Price

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Coefficient (per sq ft): £{model.coef_[0]:.2f}")
print(f"Intercept: £{model.intercept_:.2f}")
print(f"RMSE: £{rmse:,.0f}")
print(f"R² Score: {r2:.3f}")

# Predict for new house (2200 sq ft)
new_house = np.array([[2200]])
predicted_price = model.predict(new_house)
print(f"\\nPredicted price for 2200 sq ft: £{predicted_price[0]:,.0f}")
```

**Output:**
```
Coefficient (per sq ft): £158.33
Intercept: £20,000.00
RMSE: £15,000
R² Score: 0.982

Predicted price for 2200 sq ft: £368,326
```

---

**2. Polynomial Regression**

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

# Create polynomial features (degree 2)
# x, x² 
poly_pipeline = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('linear', LinearRegression())
])

poly_pipeline.fit(X_train, y_train)
y_pred_poly = poly_pipeline.predict(X_test)

rmse_poly = np.sqrt(mean_squared_error(y_test, y_pred_poly))
print(f"Polynomial RMSE: £{rmse_poly:,.0f}")

# Visualize
import matplotlib.pyplot as plt

X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_pred_linear = model.predict(X_range)
y_pred_poly_viz = poly_pipeline.predict(X_range)

plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='black', label='Actual')
plt.plot(X_range, y_pred_linear, color='blue', label='Linear')
plt.plot(X_range, y_pred_poly_viz, color='red', label='Polynomial (degree 2)')
plt.xlabel('Square Footage')
plt.ylabel('Price (£)')
plt.legend()
plt.title('Linear vs Polynomial Regression')
plt.show()
```

---

**3. Ridge Regression (L2 Regularization)**

```python
from sklearn.linear_model import Ridge

# Ridge with regularization strength alpha
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)

print(f"Ridge coefficients: {ridge.coef_}")
print(f"Linear coefficients: {model.coef_}")
# Ridge coefficients are smaller (shrunk towards zero)
```

**When to use:** Many features, multicollinearity, prevent overfitting

---

**4. Lasso Regression (L1 Regularization)**

```python
from sklearn.linear_model import Lasso

# Lasso can set coefficients to exactly zero (feature selection)
lasso = Lasso(alpha=1.0)
lasso.fit(X_train, y_train)

print(f"Lasso coefficients: {lasso.coef_}")
print(f"Non-zero features: {np.sum(lasso.coef_ != 0)}")
```

**When to use:** Feature selection, sparse models, interpretability

---

**5. ElasticNet (L1 + L2)**

```python
from sklearn.linear_model import ElasticNet

# Combines Ridge and Lasso
elastic = ElasticNet(alpha=1.0, l1_ratio=0.5)  # 50% L1, 50% L2
elastic.fit(X_train, y_train)
```

**When to use:** Best of both worlds, many correlated features
"""
    )

    st.markdown("---")
    st.markdown("#### 🌲 Tree-Based Regression")
    st.markdown(
        """**Decision Trees for Regression**

```python
from sklearn.tree import DecisionTreeRegressor

tree = DecisionTreeRegressor(max_depth=5, random_state=42)
tree.fit(X_train, y_train)
y_pred_tree = tree.predict(X_test)

rmse_tree = np.sqrt(mean_squared_error(y_test, y_pred_tree))
print(f"Decision Tree RMSE: £{rmse_tree:,.0f}")

# Visualize tree
from sklearn.tree import plot_tree
plt.figure(figsize=(20, 10))
plot_tree(tree, filled=True, feature_names=['sqft'], rounded=True)
plt.show()
```

---

**Random Forest Regression**

```python
from sklearn.ensemble import RandomForestRegressor

# Ensemble of decision trees
rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest RMSE: £{rmse_rf:,.0f}")
print(f"Random Forest R²: {r2_rf:.3f}")

# Feature importance
importances = rf.feature_importances_
print(f"\\nFeature importances: {importances}")
```

**Advantages:**
- ✅ Handles non-linear relationships
- ✅ No feature scaling needed
- ✅ Robust to outliers
- ✅ Feature importance built-in

---

**Gradient Boosting Regression**

```python
from sklearn.ensemble import GradientBoostingRegressor
import xgboost as xgb

# Gradient Boosting
gb = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    random_state=42
)

gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)

# XGBoost (faster, better performance)
xgb_model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    random_state=42
)

xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)

print(f"Gradient Boosting RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred_gb)):,.0f}")
print(f"XGBoost RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred_xgb)):,.0f}")
```

**When to use:**
- Kaggle competitions
- Need best accuracy
- Have enough data
- Can afford training time
"""
    )

    st.markdown("---")
    st.markdown("#### 📊 Model Evaluation")
    st.markdown(
        """**Comprehensive Evaluation Example**

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

def evaluate_regression_model(y_true, y_pred, model_name="Model"):
    \"\"\"Comprehensive regression evaluation\"\"\"
    
    # Calculate metrics
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    # Print metrics
    print(f"\\n{model_name} Performance:")
    print(f"MAE:  £{mae:,.2f}")
    print(f"RMSE: £{rmse:,.2f}")
    print(f"R²:   {r2:.4f}")
    print(f"MAPE: {mape:.2f}%")
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Predicted vs Actual
    axes[0].scatter(y_true, y_pred, alpha=0.5)
    axes[0].plot([y_true.min(), y_true.max()], 
                 [y_true.min(), y_true.max()], 
                 'r--', lw=2)
    axes[0].set_xlabel('Actual')
    axes[0].set_ylabel('Predicted')
    axes[0].set_title(f'{model_name}: Predicted vs Actual')
    
    # Residuals
    residuals = y_true - y_pred
    axes[1].scatter(y_pred, residuals, alpha=0.5)
    axes[1].axhline(y=0, color='r', linestyle='--')
    axes[1].set_xlabel('Predicted')
    axes[1].set_ylabel('Residuals')
    axes[1].set_title(f'{model_name}: Residual Plot')
    
    plt.tight_layout()
    plt.show()
    
    return {'MAE': mae, 'RMSE': rmse, 'R2': r2, 'MAPE': mape}

# Evaluate model
metrics = evaluate_regression_model(y_test, y_pred, "Linear Regression")
```

---

**Cross-Validation for Regression**

```python
from sklearn.model_selection import cross_val_score

# 5-fold cross-validation
cv_scores = cross_val_score(
    model, 
    X, 
    y, 
    cv=5, 
    scoring='neg_mean_squared_error'
)

# Convert to RMSE
cv_rmse = np.sqrt(-cv_scores)

print(f"Cross-Validation RMSE: £{cv_rmse.mean():,.0f} (+/- £{cv_rmse.std():,.0f})")
```

---

**Learning Curves (Detect Overfitting)**

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, 
    cv=5, 
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='neg_mean_squared_error'
)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, -train_scores.mean(axis=1), label='Training')
plt.plot(train_sizes, -val_scores.mean(axis=1), label='Validation')
plt.xlabel('Training Set Size')
plt.ylabel('MSE')
plt.title('Learning Curves')
plt.legend()
plt.show()
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎨 Hyperparameter Tuning")
    st.markdown(
        """**Grid Search for Ridge Alpha**

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'alpha': [0.001, 0.01, 0.1, 1, 10, 100]
}

# Grid search
grid_search = GridSearchCV(
    Ridge(),
    param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print(f"Best alpha: {grid_search.best_params_['alpha']}")
print(f"Best RMSE: £{np.sqrt(-grid_search.best_score_):,.0f}")

# Use best model
best_model = grid_search.best_estimator_
```

---

**Randomized Search (Faster for Large Grids)**

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

# Random Forest hyperparameters
param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(3, 15),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10)
}

random_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=param_dist,
    n_iter=20,  # Try 20 random combinations
    cv=5,
    scoring='neg_mean_squared_error',
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train, y_train)
print(f"Best params: {random_search.best_params_}")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🚀 Real-World Example: House Price Prediction")
    st.markdown(
        """**Complete End-to-End Regression Project**

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load data (example)
df = pd.DataFrame({
    'sqft': [1200, 1500, 1800, 2000, 2400, 2800, 1400, 1600, 2200, 2600],
    'bedrooms': [2, 3, 3, 4, 4, 5, 2, 3, 4, 5],
    'bathrooms': [1, 2, 2, 2, 3, 3, 1, 2, 3, 3],
    'age_years': [10, 5, 15, 8, 3, 1, 20, 12, 6, 2],
    'garage': [0, 1, 1, 2, 2, 2, 0, 1, 2, 2],
    'price': [200000, 250000, 280000, 320000, 380000, 450000, 
              230000, 260000, 350000, 420000]
})

# Feature engineering
df['price_per_sqft'] = df['price'] / df['sqft']
df['room_total'] = df['bedrooms'] + df['bathrooms']
df['is_new'] = (df['age_years'] < 5).astype(int)

# Prepare features
features = ['sqft', 'bedrooms', 'bathrooms', 'age_years', 'garage', 'room_total', 'is_new']
X = df[features]
y = df['price']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate
print(f"RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred)):,.0f}")
print(f"R²: {r2_score(y_test, y_pred):.3f}")

# Feature importance
importance_df = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\\nFeature Importance:")
print(importance_df)

# Predict for new house
new_house = pd.DataFrame({
    'sqft': [2100],
    'bedrooms': [4],
    'bathrooms': [3],
    'age_years': [5],
    'garage': [2],
    'room_total': [7],
    'is_new': [0]
})

predicted_price = model.predict(new_house)
print(f"\\nPredicted price for new house: £{predicted_price[0]:,.0f}")
```
"""
    )

    st.markdown("---")
    st.markdown("#### ⚠️ Common Mistakes & Solutions")
    st.markdown(
        """**1. Not Splitting Data Properly**

```python
# ❌ WRONG: Scale before split
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled)

# ✅ RIGHT: Split first
X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

---

**2. Using R² on Training Data**

```python
# ❌ WRONG: Evaluate on training data
model.fit(X_train, y_train)
r2_train = model.score(X_train, y_train)  # Will be misleadingly high!

# ✅ RIGHT: Always evaluate on validation/test
r2_test = model.score(X_test, y_test)
```

---

**3. Ignoring Target Variable Distribution**

```python
# Check if target is skewed
print(f"Skewness: {y.skew():.2f}")  # > 1 = right-skewed

# If skewed, consider log transform
y_log = np.log1p(y)  # log(1 + y) to handle zeros

# Train on log-transformed target
model.fit(X_train, np.log1p(y_train))

# Predictions need to be transformed back
y_pred_log = model.predict(X_test)
y_pred = np.expm1(y_pred_log)  # exp(x) - 1
```

---

**4. Not Handling Outliers**

```python
# Detect outliers using IQR
Q1 = y.quantile(0.25)
Q3 = y.quantile(0.75)
IQR = Q3 - Q1
outliers = (y < Q1 - 1.5*IQR) | (y > Q3 + 1.5*IQR)

print(f"Outliers: {outliers.sum()} ({outliers.mean()*100:.1f}%)")

# Options:
# 1. Remove outliers
# 2. Cap outliers
# 3. Use robust metrics (MAE instead of MSE)
# 4. Use robust scalers
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎯 Interview Preparation")
    st.markdown(
        """**Q1: Explain the difference between MAE and RMSE.**

**Answer:** 
- **MAE** (Mean Absolute Error) averages the absolute differences. Less sensitive to outliers.
- **RMSE** (Root Mean Squared Error) squares errors before averaging, then takes square root. Penalizes large errors more heavily.
- **Use MAE** when outliers shouldn't dominate.
- **Use RMSE** when large errors are particularly bad for business.

---

**Q2: When would you use Ridge vs Lasso?**

**Answer:**
- **Ridge (L2):** When you want to keep all features but shrink coefficients. Good with multicollinearity.
- **Lasso (L1):** When you want automatic feature selection. Sets some coefficients to exactly zero.
- **ElasticNet:** When you want both (many correlated features + feature selection).

---

**Q3: What does R² = 0.75 mean?**

**Answer:**
The model explains 75% of the variance in the target variable. The remaining 25% is unexplained (could be noise, missing features, or non-linear relationships not captured).

⚠️ **Caution:** R² can be misleading:
- Always increasing as you add features (use adjusted R²)
- Doesn't tell you if predictions are good in absolute terms
- Can be negative on test set if model is terrible

---

**Q4: How do you detect overfitting in regression?**

**Answer:**
1. **Train vs Test performance:** Large gap indicates overfitting
2. **Learning curves:** Training error low, validation error high
3. **Cross-validation:** High variance in CV scores
4. **Coefficients:** Very large coefficients suggest overfitting

**Solutions:**
- Regularization (Ridge/Lasso)
- Reduce model complexity
- More training data
- Feature selection
- Simpler model (linear instead of polynomial)
"""
    )

    st.markdown("---")
    st.markdown("#### 📚 Key Takeaways")
    st.markdown(
        """**Regression Algorithms Comparison:**

| Algorithm | Pros | Cons | When to Use |
|-----------|------|------|-------------|
| **Linear Regression** | Fast, interpretable, baseline | Assumes linear relationship | Start here always |
| **Ridge** | Handles multicollinearity, prevents overfitting | Still assumes linearity | Many correlated features |
| **Lasso** | Feature selection, sparse models | Can be unstable | Want automatic feature selection |
| **Decision Tree** | Non-linear, no scaling needed | Overfits easily | Quick baseline for non-linear |
| **Random Forest** | Robust, handles non-linear well | Slower, less interpretable | General-purpose, good default |
| **Gradient Boosting** | Best accuracy, feature importance | Slow to train, hyperparameter-sensitive | Kaggle, maximum accuracy |

---

**Metrics Cheat Sheet:**

- **RMSE:** General accuracy (same units as target)
- **MAE:** Robust to outliers
- **MAPE:** When relative error matters (%), but watch for division by zero
- **R²:** Explains variance, but can be misleading
- **Custom:** Define based on business cost of errors

---

**What You Can Do Now:**
- ✅ Build linear regression models
- ✅ Apply regularization (Ridge, Lasso)
- ✅ Use tree-based methods (RF, XGBoost)
- ✅ Evaluate models with proper metrics
- ✅ Tune hyperparameters
- ✅ Detect and prevent overfitting
- ✅ Communicate results to stakeholders

**Next:** Unit 3 (Classification) applies similar principles to categorical targets!
"""
    )


def _render_unit2_labs():
    """Labs and mini-project ideas for Unit 2."""

    st.markdown("### 🧪 HANDS-ON LABS: Unit 2 Regression")
    st.markdown(
        """**Complete these 3 labs to master regression:**

---

## Lab 1: Linear Regression Fundamentals (75 min)

**Objective:** Build and evaluate a complete house price prediction model

**Setup: Create Dataset**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Create realistic house price dataset
np.random.seed(42)
n = 200

df = pd.DataFrame({
    'sqft': np.random.normal(2000, 500, n),
    'bedrooms': np.random.randint(1, 6, n),
    'bathrooms': np.random.randint(1, 4, n),
    'age_years': np.random.exponential(15, n),
    'garage_spaces': np.random.randint(0, 3, n),
    'distance_to_city_km': np.random.exponential(10, n)
})

# Generate prices with realistic relationships
df['price'] = (
    150 * df['sqft'] +
    25000 * df['bedrooms'] +
    15000 * df['bathrooms'] -
    2000 * df['age_years'] +
    20000 * df['garage_spaces'] -
    3000 * df['distance_to_city_km'] +
    100000 +  # Base price
    np.random.normal(0, 30000, n)  # Noise
)

df['price'] = df['price'].clip(lower=100000)  # Minimum price

df.to_csv('house_prices.csv', index=False)
print("✅ Created house_prices.csv")
print(f"Shape: {df.shape}")
print(f"\\nPrice range: £{df['price'].min():,.0f} - £{df['price'].max():,.0f}")
```

---

**Part A: Exploratory Data Analysis (20 min)**

```python
df = pd.read_csv('house_prices.csv')

# 1. Basic statistics
print("Dataset Overview:")
print(df.describe())

# 2. Check correlations with price
correlations = df.corr()['price'].sort_values(ascending=False)
print("\\nCorrelations with price:")
print(correlations)

# 3. Visualize relationships
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
features = ['sqft', 'bedrooms', 'bathrooms', 'age_years', 'garage_spaces', 'distance_to_city_km']

for idx, feature in enumerate(features):
    row, col = idx // 3, idx % 3
    axes[row, col].scatter(df[feature], df['price'], alpha=0.5)
    axes[row, col].set_xlabel(feature)
    axes[row, col].set_ylabel('Price (£)')
    axes[row, col].set_title(f'Price vs {feature}')

plt.tight_layout()
plt.show()

# 4. Check for outliers
print("\\nOutlier detection (price):")
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['price'] < Q1 - 1.5*IQR) | (df['price'] > Q3 + 1.5*IQR)]
print(f"Outliers: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")
```

---

**Part B: Build Linear Regression Model (25 min)**

```python
# Prepare data
features = ['sqft', 'bedrooms', 'bathrooms', 'age_years', 'garage_spaces', 'distance_to_city_km']
X = df[features]
y = df['price']

# Split data (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train linear regression
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Coefficients
print("\\nModel Coefficients:")
coef_df = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_
}).sort_values('Coefficient', ascending=False)
print(coef_df)
print(f"\\nIntercept: £{model.intercept_:,.0f}")

# Interpretation
print("\\nInterpretation:")
print(f"Each additional sq ft adds: £{model.coef_[0]:.2f}")
print(f"Each additional bedroom adds: £{model.coef_[1]:,.0f}")
print(f"Each year of age reduces price by: £{abs(model.coef_[3]):,.0f}")
```

---

**Part C: Model Evaluation (30 min)**

```python
# Calculate metrics
def evaluate_model(y_true, y_pred, set_name=""):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    print(f"\\n{set_name} Performance:")
    print(f"MAE:  £{mae:,.0f}")
    print(f"RMSE: £{rmse:,.0f}")
    print(f"R²:   {r2:.4f}")
    print(f"MAPE: {mape:.2f}%")
    
    return {'MAE': mae, 'RMSE': rmse, 'R2': r2, 'MAPE': mape}

# Evaluate on both sets
train_metrics = evaluate_model(y_train, y_train_pred, "Training")
test_metrics = evaluate_model(y_test, y_test_pred, "Test")

# Check for overfitting
print("\\nOverfitting Check:")
print(f"Train R²: {train_metrics['R2']:.4f}")
print(f"Test R²:  {test_metrics['R2']:.4f}")
print(f"Difference: {abs(train_metrics['R2'] - test_metrics['R2']):.4f}")

if abs(train_metrics['R2'] - test_metrics['R2']) < 0.05:
    print("✅ Model generalizes well!")
else:
    print("⚠️ Possible overfitting")

# Visualize predictions
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Predicted vs Actual
axes[0].scatter(y_test, y_test_pred, alpha=0.5)
axes[0].plot([y_test.min(), y_test.max()], 
             [y_test.min(), y_test.max()], 
             'r--', lw=2, label='Perfect Prediction')
axes[0].set_xlabel('Actual Price (£)')
axes[0].set_ylabel('Predicted Price (£)')
axes[0].set_title('Predicted vs Actual')
axes[0].legend()

# Residuals
residuals = y_test - y_test_pred
axes[1].scatter(y_test_pred, residuals, alpha=0.5)
axes[1].axhline(y=0, color='r', linestyle='--')
axes[1].set_xlabel('Predicted Price (£)')
axes[1].set_ylabel('Residuals (£)')
axes[1].set_title('Residual Plot')

plt.tight_layout()
plt.show()

# Predict for new house
new_house = pd.DataFrame({
    'sqft': [2200],
    'bedrooms': [4],
    'bathrooms': [3],
    'age_years': [5],
    'garage_spaces': [2],
    'distance_to_city_km': [8]
})

predicted_price = model.predict(new_house)[0]
print(f"\\nPredicted price for new house: £{predicted_price:,.0f}")
```

---

## Lab 2: Regularization Comparison (90 min)

**Objective:** Compare Ridge, Lasso, and ElasticNet regression

**Part A: Ridge Regression (30 min)**

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Standardize features for regularization
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Try different alpha values for Ridge
alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
ridge_results = []

for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train_scaled, y_train)
    
    y_pred = ridge.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    ridge_results.append({
        'alpha': alpha,
        'rmse': rmse,
        'r2': r2,
        'coefficients': ridge.coef_
    })
    
    print(f"Alpha: {alpha:>6.3f} | RMSE: £{rmse:>10,.0f} | R²: {r2:.4f}")

# Find best alpha
best_ridge = min(ridge_results, key=lambda x: x['rmse'])
print(f"\\nBest Ridge alpha: {best_ridge['alpha']}")

# Plot coefficient paths
plt.figure(figsize=(10, 6))
for i, feature in enumerate(features):
    coefs = [r['coefficients'][i] for r in ridge_results]
    plt.plot(alphas, coefs, label=feature, marker='o')

plt.xscale('log')
plt.xlabel('Alpha (regularization strength)')
plt.ylabel('Coefficient Value')
plt.title('Ridge Regression: Coefficient Paths')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

**Part B: Lasso Regression (30 min)**

```python
# Lasso with different alphas
lasso_results = []

for alpha in alphas:
    lasso = Lasso(alpha=alpha, max_iter=10000)
    lasso.fit(X_train_scaled, y_train)
    
    y_pred = lasso.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    non_zero = np.sum(lasso.coef_ != 0)
    
    lasso_results.append({
        'alpha': alpha,
        'rmse': rmse,
        'r2': r2,
        'coefficients': lasso.coef_,
        'non_zero_features': non_zero
    })
    
    print(f"Alpha: {alpha:>6.3f} | RMSE: £{rmse:>10,.0f} | R²: {r2:.4f} | Non-zero: {non_zero}")

# Feature selection effect
print("\\nLasso Feature Selection:")
for result in lasso_results:
    print(f"Alpha {result['alpha']:>6.3f}: {result['non_zero_features']} features selected")

# Compare Ridge vs Lasso
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# RMSE comparison
ridge_rmse = [r['rmse'] for r in ridge_results]
lasso_rmse = [r['rmse'] for r in lasso_results]

axes[0].plot(alphas, ridge_rmse, marker='o', label='Ridge')
axes[0].plot(alphas, lasso_rmse, marker='s', label='Lasso')
axes[0].set_xscale('log')
axes[0].set_xlabel('Alpha')
axes[0].set_ylabel('RMSE (£)')
axes[0].set_title('Ridge vs Lasso: RMSE')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Coefficient comparison at best alpha
best_alpha = 1.0
ridge_best = Ridge(alpha=best_alpha).fit(X_train_scaled, y_train)
lasso_best = Lasso(alpha=best_alpha).fit(X_train_scaled, y_train)

x_pos = np.arange(len(features))
axes[1].bar(x_pos - 0.2, ridge_best.coef_, 0.4, label='Ridge', alpha=0.7)
axes[1].bar(x_pos + 0.2, lasso_best.coef_, 0.4, label='Lasso', alpha=0.7)
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(features, rotation=45)
axes[1].set_ylabel('Coefficient Value')
axes[1].set_title(f'Coefficients Comparison (alpha={best_alpha})')
axes[1].legend()

plt.tight_layout()
plt.show()
```

---

**Part C: ElasticNet & Grid Search (30 min)**

```python
from sklearn.model_selection import GridSearchCV

# ElasticNet combines L1 and L2
param_grid = {
    'alpha': [0.001, 0.01, 0.1, 1, 10],
    'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]  # 0=Ridge, 1=Lasso
}

elastic = ElasticNet(max_iter=10000)

grid_search = GridSearchCV(
    elastic,
    param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    n_jobs=-1
)

grid_search.fit(X_train_scaled, y_train)

print("Best ElasticNet parameters:")
print(f"Alpha: {grid_search.best_params_['alpha']}")
print(f"L1 ratio: {grid_search.best_params_['l1_ratio']}")

# Evaluate best model
best_elastic = grid_search.best_estimator_
y_pred_elastic = best_elastic.predict(X_test_scaled)

print("\\nElasticNet Performance:")
print(f"RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred_elastic)):,.0f}")
print(f"R²: {r2_score(y_test, y_pred_elastic):.4f}")

# Final comparison
models = {
    'Linear Regression': LinearRegression().fit(X_train_scaled, y_train),
    'Ridge (best)': Ridge(alpha=best_ridge['alpha']).fit(X_train_scaled, y_train),
    'Lasso (best)': Lasso(alpha=1.0).fit(X_train_scaled, y_train),
    'ElasticNet (best)': best_elastic
}

comparison = []
for name, model in models.items():
    y_pred = model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    comparison.append({'Model': name, 'RMSE': rmse, 'R²': r2})

comparison_df = pd.DataFrame(comparison).sort_values('RMSE')
print("\\nModel Comparison:")
print(comparison_df)
```

---

## Lab 3: Tree-Based Regression & XGBoost (90 min)

**Objective:** Compare tree-based methods with linear models

**Part A: Decision Tree Regression (25 min)**

```python
from sklearn.tree import DecisionTreeRegressor, plot_tree

# Train decision tree
tree = DecisionTreeRegressor(max_depth=5, min_samples_split=10, random_state=42)
tree.fit(X_train, y_train)

# Predictions
y_pred_tree = tree.predict(X_test)

print("Decision Tree Performance:")
print(f"RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred_tree)):,.0f}")
print(f"R²: {r2_score(y_test, y_pred_tree):.4f}")

# Feature importance
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': tree.feature_importances_
}).sort_values('Importance', ascending=False)

print("\\nFeature Importances:")
print(importance_df)

# Visualize tree
plt.figure(figsize=(20, 10))
plot_tree(tree, feature_names=features, filled=True, rounded=True, fontsize=10)
plt.title('Decision Tree (max_depth=5)')
plt.show()

# Test different depths
depths = [2, 3, 5, 7, 10, 15, 20]
tree_results = []

for depth in depths:
    tree = DecisionTreeRegressor(max_depth=depth, random_state=42)
    tree.fit(X_train, y_train)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, tree.predict(X_train)))
    test_rmse = np.sqrt(mean_squared_error(y_test, tree.predict(X_test)))
    
    tree_results.append({
        'depth': depth,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse
    })

# Plot overfitting
results_df = pd.DataFrame(tree_results)
plt.figure(figsize=(10, 6))
plt.plot(results_df['depth'], results_df['train_rmse'], marker='o', label='Train RMSE')
plt.plot(results_df['depth'], results_df['test_rmse'], marker='s', label='Test RMSE')
plt.xlabel('Max Depth')
plt.ylabel('RMSE (£)')
plt.title('Decision Tree: Depth vs Performance')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

**Part B: Random Forest Regression (30 min)**

```python
from sklearn.ensemble import RandomForestRegressor

# Train Random Forest
rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("Random Forest Performance:")
print(f"RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred_rf)):,.0f}")
print(f"R²: {r2_score(y_test, y_pred_rf):.4f}")

# Feature importance
rf_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf.feature_importances_
}).sort_values('Importance', ascending=False)

print("\\nRandom Forest Feature Importances:")
print(rf_importance)

# Visualize importances
plt.figure(figsize=(10, 6))
plt.barh(rf_importance['Feature'], rf_importance['Importance'])
plt.xlabel('Importance')
plt.title('Random Forest Feature Importances')
plt.tight_layout()
plt.show()

# Hyperparameter tuning
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(3, 20),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10)
}

random_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=param_dist,
    n_iter=20,
    cv=5,
    scoring='neg_mean_squared_error',
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train, y_train)

print("\\nBest Random Forest parameters:")
print(random_search.best_params_)

best_rf = random_search.best_estimator_
y_pred_best_rf = best_rf.predict(X_test)
print(f"\\nTuned RF RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred_best_rf)):,.0f}")
```

---

**Part C: XGBoost (35 min)**

```python
import xgboost as xgb

# Train XGBoost
xgb_model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)

print("XGBoost Performance:")
print(f"RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred_xgb)):,.0f}")
print(f"R²: {r2_score(y_test, y_pred_xgb):.4f}")

# Feature importance
xgb_importance = pd.DataFrame({
    'Feature': features,
    'Importance': xgb_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\\nXGBoost Feature Importances:")
print(xgb_importance)

# Hyperparameter tuning for XGBoost
param_grid_xgb = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.3],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 1.0]
}

grid_xgb = GridSearchCV(
    xgb.XGBRegressor(random_state=42),
    param_grid_xgb,
    cv=5,
    scoring='neg_mean_squared_error',
    n_jobs=-1
)

grid_xgb.fit(X_train, y_train)

print("\\nBest XGBoost parameters:")
print(grid_xgb.best_params_)

best_xgb = grid_xgb.best_estimator_
y_pred_best_xgb = best_xgb.predict(X_test)
print(f"\\nTuned XGBoost RMSE: £{np.sqrt(mean_squared_error(y_test, y_pred_best_xgb)):,.0f}")

# Final comparison: All models
all_models = {
    'Linear Regression': model,
    'Ridge': Ridge(alpha=1.0).fit(X_train_scaled, y_train),
    'Lasso': Lasso(alpha=1.0).fit(X_train_scaled, y_train),
    'Decision Tree': DecisionTreeRegressor(max_depth=5).fit(X_train, y_train),
    'Random Forest': best_rf,
    'XGBoost': best_xgb
}

final_comparison = []
for name, mdl in all_models.items():
    if name in ['Ridge', 'Lasso']:
        y_pred = mdl.predict(X_test_scaled)
    else:
        y_pred = mdl.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    final_comparison.append({
        'Model': name,
        'RMSE': rmse,
        'MAE': mae,
        'R²': r2
    })

final_df = pd.DataFrame(final_comparison).sort_values('RMSE')
print("\\n" + "="*70)
print("FINAL MODEL COMPARISON")
print("="*70)
print(final_df.to_string(index=False))

# Visualize
fig, ax = plt.subplots(figsize=(12, 6))
x_pos = np.arange(len(final_df))
ax.barh(x_pos, final_df['RMSE'], color='skyblue')
ax.set_yticks(x_pos)
ax.set_yticklabels(final_df['Model'])
ax.set_xlabel('RMSE (£)')
ax.set_title('Model Performance Comparison')
plt.tight_layout()
plt.show()
```

---

**Lab Completion Checklist:**
- ☐ Built and evaluated linear regression
- ☐ Compared Ridge, Lasso, ElasticNet
- ☐ Performed grid search for hyperparameters
- ☐ Trained decision tree regressor
- ☐ Built random forest model
- ☐ Implemented XGBoost regression
- ☐ Compared all models systematically
- ☐ Interpreted feature importances
- ☐ Visualized results

**Next:** Unit 3 teaches classification for categorical targets!
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

    st.markdown("---")
    st.markdown("#### 🎯 Classification Algorithms Deep Dive")
    st.markdown(
        """**1. Logistic Regression**

Predicts probability that observation belongs to positive class.

**Mathematical Foundation:**
$$P(y=1|x) = \\frac{1}{1 + e^{-(β_0 + β_1x_1 + ... + β_nx_n)}}$$

**Code Example:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import pandas as pd

# Example: Customer churn prediction
np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'tenure_months': np.random.randint(1, 72, n),
    'monthly_charges': np.random.normal(50, 20, n),
    'total_charges': np.random.normal(1500, 800, n),
    'num_support_calls': np.random.poisson(2, n)
})

# Generate target with realistic relationships
churn_prob = 1 / (1 + np.exp(-(
    -2 +
    -0.05 * df['tenure_months'] +
    0.02 * df['monthly_charges'] +
    0.3 * df['num_support_calls']
)))
df['churned'] = (np.random.random(n) < churn_prob).astype(int)

# Train model
X = df.drop('churned', axis=1)
y = df['churned']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = LogisticRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print("Coefficients:")
for feature, coef in zip(X.columns, model.coef_[0]):
    print(f"{feature}: {coef:.4f}")

print(f"\\nAccuracy: {model.score(X_test, y_test):.3f}")
print("\\nClassification Report:")
print(classification_report(y_test, y_pred))
```

**Interpretation:**
- Negative coefficient = increases probability of class 0
- Positive coefficient = increases probability of class 1
- `exp(coefficient)` = odds ratio

---

**2. Decision Tree Classifier**

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

print(f"Train Accuracy: {tree.score(X_train, y_train):.3f}")
print(f"Test Accuracy: {tree.score(X_test, y_test):.3f}")

# Visualize
plt.figure(figsize=(20, 10))
plot_tree(tree, feature_names=X.columns, class_names=['No Churn', 'Churn'], filled=True)
plt.show()
```

**Advantages:**
- ✅ Interpretable (visual decision rules)
- ✅ Handles non-linear relationships
- ✅ No feature scaling needed

**Disadvantages:**
- ❌ Prone to overfitting
- ❌ Unstable (small changes → different tree)

---

**3. Random Forest Classifier**

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
y_pred_proba_rf = rf.predict_proba(X_test)[:, 1]

print(f"Random Forest Accuracy: {rf.score(X_test, y_test):.3f}")

# Feature importance
importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\\nFeature Importances:")
print(importance_df)
```

---

**4. Gradient Boosting (XGBoost)**

```python
import xgboost as xgb

xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)
y_pred_proba_xgb = xgb_model.predict_proba(X_test)[:, 1]

print(f"XGBoost Accuracy: {xgb_model.score(X_test, y_test):.3f}")
```

**When to use:** Maximum performance needed, Kaggle competitions

---

**5. Support Vector Machine (SVM)**

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# SVM requires scaled features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm = SVC(kernel='rbf', probability=True, random_state=42)
svm.fit(X_train_scaled, y_train)

print(f"SVM Accuracy: {svm.score(X_test_scaled, y_test):.3f}")
```

**When to use:** High-dimensional data, clear margin between classes

---

**6. Naive Bayes**

```python
from sklearn.naive_bayes import GaussianNB

nb = GaussianNB()
nb.fit(X_train, y_train)

print(f"Naive Bayes Accuracy: {nb.score(X_test, y_test):.3f}")
```

**When to use:** Fast baseline, text classification, real-time predictions
"""
    )

    st.markdown("---")
    st.markdown("#### 📊 Classification Metrics Explained")
    st.markdown(
        """**Confusion Matrix:**

```
                  Predicted
                Negative  Positive
Actual Negative    TN       FP
       Positive    FN       TP
```

- **True Positive (TP):** Correctly predicted positive
- **True Negative (TN):** Correctly predicted negative
- **False Positive (FP):** Incorrectly predicted positive (Type I error)
- **False Negative (FN):** Incorrectly predicted negative (Type II error)

---

**Key Metrics:**

1. **Accuracy:** `(TP + TN) / Total`
   - Good when classes balanced
   - Misleading with imbalance

2. **Precision:** `TP / (TP + FP)`
   - "Of all predicted positives, how many were correct?"
   - Important when false positives are costly

3. **Recall (Sensitivity):** `TP / (TP + FN)`
   - "Of all actual positives, how many did we catch?"
   - Important when false negatives are costly

4. **F1-Score:** `2 × (Precision × Recall) / (Precision + Recall)`
   - Harmonic mean of precision and recall
   - Good single metric for imbalanced data

5. **Specificity:** `TN / (TN + FP)`
   - "Of all actual negatives, how many did we correctly identify?"

---

**Code Example:**

```python
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, roc_curve
import seaborn as sns

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:")
print(classification_report(y_test, y_pred))

# ROC-AUC
roc_auc = roc_auc_score(y_test, y_pred_proba)
print(f"\\nROC-AUC Score: {roc_auc:.3f}")

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

---

**Real-World Example: Fraud Detection**

```python
# Scenario: 1% of transactions are fraudulent
# Cost of missing fraud: £1,000
# Cost of false alarm: £10

# At default threshold (0.5):
# Precision: 0.60 (40% false positives)
# Recall: 0.80 (20% of fraud missed)

# Expected cost per 1000 transactions:
fraud_transactions = 10
false_negatives = fraud_transactions * 0.20  # 2 missed frauds
cost_fn = false_negatives * 1000  # £2,000

non_fraud = 990
false_positives = (10 / 0.6) - 10  # ~7 false alarms
cost_fp = false_positives * 10  # £70

total_cost = cost_fn + cost_fp  # £2,070

print(f"Expected cost: £{total_cost:.0f} per 1000 transactions")

# Adjust threshold to 0.3 to catch more fraud:
# Precision: 0.40 (more false positives)
# Recall: 0.95 (only 5% missed)

# New expected cost:
false_negatives_new = fraud_transactions * 0.05  # 0.5 missed
cost_fn_new = false_negatives_new * 1000  # £500

false_positives_new = (10 / 0.4) - 10  # 15 false alarms
cost_fp_new = false_positives_new * 10  # £150

total_cost_new = cost_fn_new + cost_fp_new  # £650

print(f"New expected cost: £{total_cost_new:.0f} (saved £{total_cost - total_cost_new:.0f})")
```
"""
    )

    st.markdown("---")
    st.markdown("#### ⚖️ Handling Class Imbalance")
    st.markdown(
        """**Problem:** When one class is rare (e.g., 1% fraud, 5% churn)

**Strategy 1: Class Weights**

```python
from sklearn.linear_model import LogisticRegression
from sklearn.utils.class_weight import compute_class_weight

# Automatically balance classes
model_balanced = LogisticRegression(class_weight='balanced')
model_balanced.fit(X_train, y_train)

# Or compute custom weights
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
weight_dict = {0: class_weights[0], 1: class_weights[1]}
model_custom = LogisticRegression(class_weight=weight_dict)
model_custom.fit(X_train, y_train)
```

---

**Strategy 2: Resampling (SMOTE)**

```python
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline

# Oversample minority class
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

print(f"Original class distribution: {np.bincount(y_train)}")
print(f"Resampled class distribution: {np.bincount(y_resampled)}")

# Train on resampled data
model_smote = LogisticRegression()
model_smote.fit(X_resampled, y_resampled)
```

---

**Strategy 3: Adjust Decision Threshold**

```python
from sklearn.metrics import precision_recall_curve

# Get probabilities
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Find optimal threshold
precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)

# Find threshold that maximizes F1
f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[optimal_idx]

print(f"Optimal threshold: {optimal_threshold:.3f}")
print(f"F1 at optimal: {f1_scores[optimal_idx]:.3f}")

# Apply optimal threshold
y_pred_optimal = (y_pred_proba >= optimal_threshold).astype(int)

print("\\nWith optimal threshold:")
print(classification_report(y_test, y_pred_optimal))

# Visualize
plt.figure(figsize=(10, 6))
plt.plot(thresholds, precision[:-1], label='Precision')
plt.plot(thresholds, recall[:-1], label='Recall')
plt.plot(thresholds, f1_scores[:-1], label='F1 Score')
plt.axvline(optimal_threshold, color='r', linestyle='--', label=f'Optimal={optimal_threshold:.3f}')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.title('Precision-Recall-F1 vs Threshold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

**Strategy 4: Evaluation Metrics**

```python
# Use metrics appropriate for imbalanced data
from sklearn.metrics import balanced_accuracy_score, average_precision_score

balanced_acc = balanced_accuracy_score(y_test, y_pred)
pr_auc = average_precision_score(y_test, y_pred_proba)

print(f"Balanced Accuracy: {balanced_acc:.3f}")
print(f"PR-AUC: {pr_auc:.3f}")  # Better than ROC-AUC for imbalanced data
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎨 Model Comparison & Selection")
    st.markdown(
        """**Complete Comparison Example:**

```python
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, f1_score

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Logistic (Balanced)': LogisticRegression(class_weight='balanced', max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(probability=True, random_state=42)
}

results = []
for name, model in models.items():
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    
    # Train and test
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Calculate metrics
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    
    results.append({
        'Model': name,
        'CV F1 (mean)': cv_scores.mean(),
        'CV F1 (std)': cv_scores.std(),
        'Test Accuracy': accuracy_score(y_test, y_pred),
        'Test Precision': precision_score(y_test, y_pred),
        'Test Recall': recall_score(y_test, y_pred),
        'Test F1': f1_score(y_test, y_pred),
        'Test ROC-AUC': roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
    })

results_df = pd.DataFrame(results).sort_values('Test F1', ascending=False)
print(results_df.to_string(index=False))
```

---

**Visualize Comparison:**

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Accuracy
axes[0, 0].barh(results_df['Model'], results_df['Test Accuracy'])
axes[0, 0].set_xlabel('Accuracy')
axes[0, 0].set_title('Model Accuracy Comparison')

# F1 Score
axes[0, 1].barh(results_df['Model'], results_df['Test F1'])
axes[0, 1].set_xlabel('F1 Score')
axes[0, 1].set_title('Model F1 Comparison')

# Precision vs Recall
axes[1, 0].scatter(results_df['Test Recall'], results_df['Test Precision'], s=100)
for idx, model in enumerate(results_df['Model']):
    axes[1, 0].annotate(model, (results_df.iloc[idx]['Test Recall'], results_df.iloc[idx]['Test Precision']))
axes[1, 0].set_xlabel('Recall')
axes[1, 0].set_ylabel('Precision')
axes[1, 0].set_title('Precision vs Recall Trade-off')

# ROC-AUC
axes[1, 1].barh(results_df['Model'], results_df['Test ROC-AUC'].fillna(0))
axes[1, 1].set_xlabel('ROC-AUC')
axes[1, 1].set_title('ROC-AUC Comparison')

plt.tight_layout()
plt.show()
```
"""
    )

    st.markdown("---")
    st.markdown("#### ⚠️ Common Mistakes & Solutions")
    st.markdown(
        """**1. Using Accuracy on Imbalanced Data**

```python
# ❌ WRONG: 95% accuracy sounds good
# But if 95% of data is class 0, predicting all 0 gives 95% accuracy!

# ✅ RIGHT: Check class distribution first
print(f"Class distribution: {np.bincount(y_train)}")
print(f"Baseline (always predict majority): {max(np.bincount(y_train))/len(y_train):.3f}")

# Use F1, precision, recall for imbalanced data
```

---

**2. Not Using Stratified Splits**

```python
# ❌ WRONG: Random split may have different class ratios
X_train, X_test = train_test_split(X, y, test_size=0.2)

# ✅ RIGHT: Stratify maintains class proportions
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

---

**3. Ignoring Class Probabilities**

```python
# ❌ WRONG: Only look at binary predictions
y_pred = model.predict(X_test)

# ✅ RIGHT: Use probabilities for ranking and threshold tuning
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Rank by risk
risk_scores = pd.DataFrame({
    'actual': y_test,
    'probability': y_pred_proba
}).sort_values('probability', ascending=False)

print("Top 10 highest risk:")
print(risk_scores.head(10))
```

---

**4. Overfitting to Training Data**

```python
# Check train vs test performance
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)

print(f"Train Accuracy: {train_acc:.3f}")
print(f"Test Accuracy: {test_acc:.3f}")
print(f"Difference: {train_acc - test_acc:.3f}")

if train_acc - test_acc > 0.1:
    print("⚠️ Model is overfitting!")
    print("Solutions: Regularization, simpler model, more data")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎯 Interview Preparation")
    st.markdown(
        """**Q1: Explain precision vs recall with an example.**

**Answer:**
- **Precision:** Of all patients we flagged as high-risk, what % actually were high-risk?
- **Recall:** Of all actual high-risk patients, what % did we catch?

**Example:** Email spam filter
- High precision = few legitimate emails marked as spam (low FP)
- High recall = catch most spam emails (low FN)
- Trade-off: Aggressive filter (high recall) may block legitimate emails (low precision)

---

**Q2: When would you use ROC-AUC vs PR-AUC?**

**Answer:**
- **ROC-AUC:** Balanced classes, care about both FP and FN equally
- **PR-AUC:** Imbalanced classes (e.g., 1% fraud), focus on positive class performance

**Why:** With 1% positives, even a bad model can achieve 0.99 TNR (specificity), making ROC-AUC misleadingly high. PR-AUC focuses on precision/recall, which are more sensitive to positive class performance.

---

**Q3: How do you choose a decision threshold?**

**Answer:**
1. **Business cost analysis:** Calculate cost of FP vs FN
2. **Plot precision-recall curve:** See trade-offs
3. **Optimize metric:** Maximize F1, or custom cost function
4. **Stakeholder input:** What error rate is acceptable?

**Example:** Loan default prediction
- FN (miss a default) costs £10,000
- FP (reject good customer) costs £100
- Threshold should favor recall (catch defaults) over precision

---

**Q4: What is class imbalance and how do you handle it?**

**Answer:**
**Problem:** One class much rarer than others (e.g., 1% fraud, 99% legitimate)

**Solutions:**
1. **Class weights:** Penalize errors on minority class more
2. **Resampling:** SMOTE (oversample minority) or undersample majority
3. **Threshold adjustment:** Lower threshold to catch more positives
4. **Different metrics:** Use F1, PR-AUC instead of accuracy
5. **Ensemble methods:** Balanced random forest
6. **Collect more data:** Especially minority class

**Best approach:** Try multiple methods and compare on holdout set
"""
    )

    st.markdown("---")
    st.markdown("#### 📚 Key Takeaways")
    st.markdown(
        """**Classification Algorithm Comparison:**

| Algorithm | Pros | Cons | When to Use |
|-----------|------|------|-------------|
| **Logistic Regression** | Interpretable, fast, probabilistic | Linear decision boundary | Start here, need coefficients |
| **Decision Tree** | Interpretable, non-linear, no scaling | Overfits easily | Quick baseline, need rules |
| **Random Forest** | Robust, feature importance, non-linear | Slower, less interpretable | General purpose, good default |
| **XGBoost** | Best performance, handles imbalance | Slow to train, many hyperparameters | Kaggle, maximum accuracy |
| **SVM** | Good for high dimensions | Slow on large data, needs scaling | Text classification, few samples |
| **Naive Bayes** | Very fast, works with little data | Strong assumptions | Text, real-time, baseline |

---

**Metrics Cheat Sheet:**

**Balanced Classes:**
- Accuracy, F1, ROC-AUC

**Imbalanced Classes:**
- Precision, Recall, F1, PR-AUC
- Balanced Accuracy
- Confusion matrix

**Cost-Sensitive:**
- Custom cost function
- Adjusted threshold
- Business metrics (£ saved)

---

**What You Can Do Now:**
- ✅ Build classification models for binary outcomes
- ✅ Choose appropriate metrics for problem
- ✅ Handle class imbalance
- ✅ Tune decision thresholds
- ✅ Compare multiple classifiers
- ✅ Interpret and explain results
- ✅ Calculate business impact

**Next:** Unit 4 (Model Evaluation) covers validation strategies and deployment readiness!
"""
    )


def _render_unit3_labs():
    """Labs and mini-project ideas for Unit 3."""

    st.markdown("### 🧪 HANDS-ON LABS: Unit 3 Classification")
    st.markdown(
        """**Complete these 3 labs to master classification:**

---

## Lab 1: Binary Classification Fundamentals (80 min)

**Objective:** Build and evaluate customer churn prediction models

**Setup: Create Dataset**

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, classification_report, 
                             roc_auc_score, roc_curve, precision_recall_curve)
import matplotlib.pyplot as plt
import seaborn as sns

# Create realistic churn dataset
np.random.seed(42)
n = 2000

df = pd.DataFrame({
    'tenure_months': np.random.randint(1, 72, n),
    'monthly_charges': np.random.normal(50, 20, n),
    'total_charges': np.random.normal(1500, 800, n),
    'num_support_calls': np.random.poisson(2, n),
    'num_late_payments': np.random.poisson(1, n),
    'has_streaming': np.random.choice([0, 1], n, p=[0.6, 0.4]),
    'contract_type': np.random.choice([0, 1, 2], n, p=[0.5, 0.3, 0.2])  # 0=month, 1=1yr, 2=2yr
})

# Generate churn with realistic relationships
churn_logit = (
    -2 +
    -0.05 * df['tenure_months'] +
    0.02 * df['monthly_charges'] +
    0.4 * df['num_support_calls'] +
    0.3 * df['num_late_payments'] +
    -0.5 * df['has_streaming'] +
    -0.8 * df['contract_type']
)
churn_prob = 1 / (1 + np.exp(-churn_logit))
df['churned'] = (np.random.random(n) < churn_prob).astype(int)

# Save
df.to_csv('customer_churn.csv', index=False)
print(f"✅ Created customer_churn.csv")
print(f"Shape: {df.shape}")
print(f"\\nChurn rate: {df['churned'].mean():.1%}")
print(f"Churned: {df['churned'].sum()}, Not churned: {(1-df['churned']).sum()}")
```

---

**Part A: Baseline Logistic Regression (25 min)**

```python
df = pd.read_csv('customer_churn.csv')

# Prepare data
X = df.drop('churned', axis=1)
y = df['churned']

# Stratified split (maintain class proportions)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")
print(f"Train churn rate: {y_train.mean():.1%}")
print(f"Test churn rate: {y_test.mean():.1%}")

# Train logistic regression
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Coefficients
print("\\nModel Coefficients:")
coef_df = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_[0]
}).sort_values('Coefficient', key=abs, ascending=False)
print(coef_df)

print(f"\\nAccuracy: {model.score(X_test, y_test):.3f}")
```

---

**Part B: Confusion Matrix & Metrics (25 min)**

```python
# Confusion matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Not Churn', 'Churn'],
            yticklabels=['Not Churn', 'Churn'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Extract values
tn, fp, fn, tp = cm.ravel()
print(f"True Negatives: {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives: {tp}")

# Classification report
print("\\nClassification Report:")
print(classification_report(y_test, y_pred, 
                          target_names=['Not Churn', 'Churn']))

# Manual metric calculation
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * (precision * recall) / (precision + recall)

print(f"\\nManual Calculations:")
print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")

# Business interpretation
print("\\n📊 Business Interpretation:")
print(f"• Of {fp} customers flagged as churners, they didn't churn (wasted retention effort)")
print(f"• Of {fn} actual churners, we missed them (lost revenue)")
print(f"• We correctly identified {tp} out of {tp+fn} churners ({recall:.1%} recall)")
```

---

**Part C: ROC Curve & Threshold Analysis (30 min)**

```python
# ROC Curve
fpr, tpr, roc_thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = roc_auc_score(y_test, y_pred_proba)

plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.3f})', linewidth=2)
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate (Recall)')
plt.title('ROC Curve')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Precision-Recall Curve
precision, recall, pr_thresholds = precision_recall_curve(y_test, y_pred_proba)

plt.figure(figsize=(10, 6))
plt.plot(recall, precision, linewidth=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.grid(True, alpha=0.3)
plt.show()

# Find optimal threshold
f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
optimal_idx = np.argmax(f1_scores)
optimal_threshold = pr_thresholds[optimal_idx]

print(f"\\nDefault threshold (0.5):")
print(f"  Precision: {precision_score(y_test, y_pred):.3f}")
print(f"  Recall: {recall_score(y_test, y_pred):.3f}")
print(f"  F1: {f1_score(y_test, y_pred):.3f}")

y_pred_optimal = (y_pred_proba >= optimal_threshold).astype(int)
print(f"\\nOptimal threshold ({optimal_threshold:.3f}):")
print(f"  Precision: {precision_score(y_test, y_pred_optimal):.3f}")
print(f"  Recall: {recall_score(y_test, y_pred_optimal):.3f}")
print(f"  F1: {f1_score(y_test, y_pred_optimal):.3f}")

# Plot threshold impact
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Precision & Recall vs Threshold
axes[0].plot(pr_thresholds, precision[:-1], label='Precision')
axes[0].plot(pr_thresholds, recall[:-1], label='Recall')
axes[0].plot(pr_thresholds, f1_scores[:-1], label='F1 Score')
axes[0].axvline(optimal_threshold, color='r', linestyle='--', 
                label=f'Optimal={optimal_threshold:.3f}')
axes[0].set_xlabel('Threshold')
axes[0].set_ylabel('Score')
axes[0].set_title('Metrics vs Threshold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Prediction distribution
axes[1].hist(y_pred_proba[y_test==0], bins=30, alpha=0.5, label='Not Churn', density=True)
axes[1].hist(y_pred_proba[y_test==1], bins=30, alpha=0.5, label='Churn', density=True)
axes[1].axvline(0.5, color='r', linestyle='--', label='Default threshold')
axes[1].axvline(optimal_threshold, color='g', linestyle='--', label='Optimal threshold')
axes[1].set_xlabel('Predicted Probability')
axes[1].set_ylabel('Density')
axes[1].set_title('Prediction Distribution by Class')
axes[1].legend()

plt.tight_layout()
plt.show()
```

---

## Lab 2: Handling Class Imbalance (90 min)

**Objective:** Master techniques for imbalanced classification

**Part A: Create Imbalanced Dataset (15 min)**

```python
# Create highly imbalanced fraud detection dataset
np.random.seed(42)
n = 5000

df_imb = pd.DataFrame({
    'transaction_amount': np.random.lognormal(4, 1, n),
    'account_age_days': np.random.exponential(365, n),
    'num_transactions_today': np.random.poisson(3, n),
    'distance_from_home_km': np.random.exponential(20, n),
    'unusual_time': np.random.choice([0, 1], n, p=[0.9, 0.1])
})

# Generate fraud (1% rate)
fraud_logit = (
    -5 +
    0.001 * df_imb['transaction_amount'] +
    -0.005 * df_imb['account_age_days'] +
    0.3 * df_imb['num_transactions_today'] +
    0.05 * df_imb['distance_from_home_km'] +
    1.5 * df_imb['unusual_time']
)
fraud_prob = 1 / (1 + np.exp(-fraud_logit))
df_imb['is_fraud'] = (np.random.random(n) < fraud_prob).astype(int)

# Adjust to get ~1% fraud rate
fraud_rate = df_imb['is_fraud'].mean()
if fraud_rate > 0.02:  # If too high, randomly remove some frauds
    fraud_indices = df_imb[df_imb['is_fraud'] == 1].index
    keep_fraud = np.random.choice(fraud_indices, size=int(n * 0.01), replace=False)
    df_imb.loc[~df_imb.index.isin(keep_fraud), 'is_fraud'] = 0

print(f"Fraud rate: {df_imb['is_fraud'].mean():.2%}")
print(f"Fraudulent: {df_imb['is_fraud'].sum()}")
print(f"Legitimate: {(~df_imb['is_fraud'].astype(bool)).sum()}")

df_imb.to_csv('fraud_detection.csv', index=False)
```

---

**Part B: Baseline vs Class Weights (30 min)**

```python
from sklearn.metrics import balanced_accuracy_score, average_precision_score

df_imb = pd.read_csv('fraud_detection.csv')

X = df_imb.drop('is_fraud', axis=1)
y = df_imb['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train fraud rate: {y_train.mean():.2%}")
print(f"Test fraud rate: {y_test.mean():.2%}")

# Model 1: Standard logistic regression
model_std = LogisticRegression(max_iter=1000, random_state=42)
model_std.fit(X_train, y_train)
y_pred_std = model_std.predict(X_test)
y_pred_proba_std = model_std.predict_proba(X_test)[:, 1]

print("\\n" + "="*60)
print("STANDARD MODEL")
print("="*60)
print(classification_report(y_test, y_pred_std, target_names=['Legitimate', 'Fraud']))

# Model 2: Balanced class weights
model_balanced = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
model_balanced.fit(X_train, y_train)
y_pred_balanced = model_balanced.predict(X_test)
y_pred_proba_balanced = model_balanced.predict_proba(X_test)[:, 1]

print("\\n" + "="*60)
print("BALANCED CLASS WEIGHTS")
print("="*60)
print(classification_report(y_test, y_pred_balanced, target_names=['Legitimate', 'Fraud']))

# Compare
comparison = pd.DataFrame({
    'Model': ['Standard', 'Balanced'],
    'Accuracy': [
        accuracy_score(y_test, y_pred_std),
        accuracy_score(y_test, y_pred_balanced)
    ],
    'Balanced Accuracy': [
        balanced_accuracy_score(y_test, y_pred_std),
        balanced_accuracy_score(y_test, y_pred_balanced)
    ],
    'Precision': [
        precision_score(y_test, y_pred_std),
        precision_score(y_test, y_pred_balanced)
    ],
    'Recall': [
        recall_score(y_test, y_pred_std),
        recall_score(y_test, y_pred_balanced)
    ],
    'F1': [
        f1_score(y_test, y_pred_std),
        f1_score(y_test, y_pred_balanced)
    ],
    'ROC-AUC': [
        roc_auc_score(y_test, y_pred_proba_std),
        roc_auc_score(y_test, y_pred_proba_balanced)
    ],
    'PR-AUC': [
        average_precision_score(y_test, y_pred_proba_std),
        average_precision_score(y_test, y_pred_proba_balanced)
    ]
})

print("\\n" + "="*60)
print("COMPARISON")
print("="*60)
print(comparison.to_string(index=False))
```

---

**Part C: SMOTE Resampling (25 min)**

```python
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# SMOTE oversampling
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print(f"Original training set: {X_train.shape}")
print(f"Original class distribution: {np.bincount(y_train)}")
print(f"\\nAfter SMOTE: {X_train_smote.shape}")
print(f"SMOTE class distribution: {np.bincount(y_train_smote)}")

# Train on SMOTE data
model_smote = LogisticRegression(max_iter=1000, random_state=42)
model_smote.fit(X_train_smote, y_train_smote)
y_pred_smote = model_smote.predict(X_test)
y_pred_proba_smote = model_smote.predict_proba(X_test)[:, 1]

print("\\n" + "="*60)
print("SMOTE MODEL")
print("="*60)
print(classification_report(y_test, y_pred_smote, target_names=['Legitimate', 'Fraud']))

# Combined: SMOTE + Undersampling
from imblearn.pipeline import Pipeline as ImbPipeline

resampler = ImbPipeline([
    ('smote', SMOTE(random_state=42)),
    ('undersample', RandomUnderSampler(random_state=42))
])

X_train_combined, y_train_combined = resampler.fit_resample(X_train, y_train)

print(f"\\nCombined resampling: {X_train_combined.shape}")
print(f"Class distribution: {np.bincount(y_train_combined)}")
```

---

**Part D: Cost-Sensitive Threshold Tuning (20 min)**

```python
# Business costs
cost_fp = 10  # Cost of investigating false alarm
cost_fn = 1000  # Cost of missing fraud

print(f"Business Context:")
print(f"  Cost of False Positive (false alarm): £{cost_fp}")
print(f"  Cost of False Negative (missed fraud): £{cost_fn}")

# Test different thresholds
thresholds_to_test = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
results = []

for threshold in thresholds_to_test:
    y_pred_thresh = (y_pred_proba_balanced >= threshold).astype(int)
    cm = confusion_matrix(y_test, y_pred_thresh)
    tn, fp, fn, tp = cm.ravel()
    
    total_cost = (fp * cost_fp) + (fn * cost_fn)
    cost_per_transaction = total_cost / len(y_test)
    
    results.append({
        'Threshold': threshold,
        'TP': tp,
        'FP': fp,
        'FN': fn,
        'TN': tn,
        'Precision': tp / (tp + fp) if (tp + fp) > 0 else 0,
        'Recall': tp / (tp + fn) if (tp + fn) > 0 else 0,
        'Total Cost': total_cost,
        'Cost per Txn': cost_per_transaction
    })

results_df = pd.DataFrame(results)
best_idx = results_df['Total Cost'].idxmin()
best_threshold = results_df.loc[best_idx, 'Threshold']

print("\\n" + "="*80)
print("THRESHOLD ANALYSIS")
print("="*80)
print(results_df.to_string(index=False))
print(f"\\n✅ Best threshold: {best_threshold} (minimizes total cost)")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(results_df['Threshold'], results_df['Precision'], marker='o', label='Precision')
axes[0].plot(results_df['Threshold'], results_df['Recall'], marker='s', label='Recall')
axes[0].axvline(best_threshold, color='r', linestyle='--', label=f'Best={best_threshold}')
axes[0].set_xlabel('Threshold')
axes[0].set_ylabel('Score')
axes[0].set_title('Metrics vs Threshold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(results_df['Threshold'], results_df['Total Cost'], marker='o', color='red')
axes[1].axvline(best_threshold, color='g', linestyle='--', label=f'Optimal={best_threshold}')
axes[1].set_xlabel('Threshold')
axes[1].set_ylabel('Total Cost (£)')
axes[1].set_title('Business Cost vs Threshold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Lab 3: Multi-Model Comparison (75 min)

**Objective:** Compare 6 classification algorithms systematically

**Part A: Train Multiple Models (30 min)**

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb
from sklearn.model_selection import cross_val_score
import time

# Use churn dataset
df = pd.read_csv('customer_churn.csv')
X = df.drop('churned', axis=1)
y = df['churned']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Define models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss'),
    'Naive Bayes': GaussianNB()
}

# Train and evaluate
results = []
for name, model in models.items():
    print(f"\\nTraining {name}...")
    
    # Training time
    start_time = time.time()
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    
    # Train on full training set
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Calculate metrics
    results.append({
        'Model': name,
        'CV F1 (mean)': cv_scores.mean(),
        'CV F1 (std)': cv_scores.std(),
        'Train Time (s)': train_time,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1': f1_score(y_test, y_pred),
        'ROC-AUC': roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
    })

results_df = pd.DataFrame(results).sort_values('F1', ascending=False)
```

---

**Part B: Visualize Comparison (25 min)**

```python
print("\\n" + "="*100)
print("MODEL COMPARISON RESULTS")
print("="*100)
print(results_df.to_string(index=False))

# Visualizations
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1. F1 Score
axes[0, 0].barh(results_df['Model'], results_df['F1'])
axes[0, 0].set_xlabel('F1 Score')
axes[0, 0].set_title('F1 Score Comparison')
axes[0, 0].set_xlim(0, 1)

# 2. Accuracy
axes[0, 1].barh(results_df['Model'], results_df['Accuracy'])
axes[0, 1].set_xlabel('Accuracy')
axes[0, 1].set_title('Accuracy Comparison')
axes[0, 1].set_xlim(0, 1)

# 3. ROC-AUC
axes[0, 2].barh(results_df['Model'], results_df['ROC-AUC'].fillna(0))
axes[0, 2].set_xlabel('ROC-AUC')
axes[0, 2].set_title('ROC-AUC Comparison')
axes[0, 2].set_xlim(0, 1)

# 4. Precision vs Recall
axes[1, 0].scatter(results_df['Recall'], results_df['Precision'], s=100)
for idx, model in enumerate(results_df['Model']):
    axes[1, 0].annotate(model, 
                       (results_df.iloc[idx]['Recall'], results_df.iloc[idx]['Precision']),
                       fontsize=8)
axes[1, 0].set_xlabel('Recall')
axes[1, 0].set_ylabel('Precision')
axes[1, 0].set_title('Precision vs Recall Trade-off')
axes[1, 0].set_xlim(0, 1)
axes[1, 0].set_ylim(0, 1)

# 5. Training Time
axes[1, 1].barh(results_df['Model'], results_df['Train Time (s)'])
axes[1, 1].set_xlabel('Training Time (seconds)')
axes[1, 1].set_title('Training Time Comparison')

# 6. CV F1 with error bars
axes[1, 2].barh(results_df['Model'], results_df['CV F1 (mean)'])
axes[1, 2].errorbar(results_df['CV F1 (mean)'], range(len(results_df)), 
                    xerr=results_df['CV F1 (std)'], fmt='none', color='red')
axes[1, 2].set_xlabel('CV F1 Score')
axes[1, 2].set_title('Cross-Validation F1 (with std)')
axes[1, 2].set_xlim(0, 1)

plt.tight_layout()
plt.show()
```

---

**Part C: Feature Importance Analysis (20 min)**

```python
# For tree-based models, show feature importance
tree_models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
}

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for idx, (name, model) in enumerate(tree_models.items()):
    model.fit(X_train, y_train)
    
    importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    axes[idx].barh(importance_df['feature'], importance_df['importance'])
    axes[idx].set_xlabel('Importance')
    axes[idx].set_title(f'{name} Feature Importance')

plt.tight_layout()
plt.show()

# Summary recommendations
print("\\n" + "="*100)
print("RECOMMENDATIONS")
print("="*100)
best_model = results_df.iloc[0]
print(f"\\n🏆 Best Overall Model: {best_model['Model']}")
print(f"   F1 Score: {best_model['F1']:.3f}")
print(f"   ROC-AUC: {best_model['ROC-AUC']:.3f}")
print(f"   Training Time: {best_model['Train Time (s)']:.2f}s")

fastest_model = results_df.loc[results_df['Train Time (s)'].idxmin()]
print(f"\\n⚡ Fastest Model: {fastest_model['Model']}")
print(f"   F1 Score: {fastest_model['F1']:.3f}")
print(f"   Training Time: {fastest_model['Train Time (s)']:.2f}s")
```

---

**Lab Completion Checklist:**
- ☐ Built logistic regression classifier
- ☐ Analyzed confusion matrix
- ☐ Plotted ROC and PR curves
- ☐ Tuned decision threshold
- ☐ Handled class imbalance with weights and SMOTE
- ☐ Performed cost-sensitive analysis
- ☐ Compared 6 classification algorithms
- ☐ Interpreted feature importances
- ☐ Made model selection recommendations

**Next:** Unit 4 teaches cross-validation and model evaluation!
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

    st.markdown("---")
    st.markdown("#### 🎯 Train/Validation/Test Split Strategy")
    st.markdown(
        """**The Golden Rule: Never touch your test set until final evaluation**

**Standard Split (70/15/15):**
```python
from sklearn.model_selection import train_test_split

# First split: separate test set
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)

# Second split: training and validation
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.176, random_state=42, stratify=y_temp  # 0.176 of 0.85 ≈ 0.15
)

print(f"Train: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
print(f"Val:   {len(X_val)} ({len(X_val)/len(X)*100:.1f}%)")
print(f"Test:  {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")
```

**Purpose of each set:**
1. **Training Set:** Fit model parameters (weights, coefficients)
2. **Validation Set:** Tune hyperparameters, select features, choose models
3. **Test Set:** Final unbiased performance estimate (use once!)

---

**Why This Matters:**
```python
# ❌ WRONG: Tuning on test set
best_alpha = None
best_score = 0

for alpha in [0.1, 1, 10]:
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)  # Using test set!
    if score > best_score:
        best_score = score
        best_alpha = alpha

# This gives overly optimistic estimate

# ✅ RIGHT: Tuning on validation set
best_alpha = None
best_score = 0

for alpha in [0.1, 1, 10]:
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    score = model.score(X_val, y_val)  # Using validation set
    if score > best_score:
        best_score = score
        best_alpha = alpha

# Final evaluation on test set (once!)
final_model = Ridge(alpha=best_alpha)
final_model.fit(X_train, y_train)
test_score = final_model.score(X_test, y_test)
print(f"Unbiased test score: {test_score:.3f}")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🔁 Cross-Validation Deep Dive")
    st.markdown(
        """**K-Fold Cross-Validation:**

Splits data into k folds, trains on k-1 folds, validates on remaining fold. Repeats k times.

```python
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.linear_model import LogisticRegression
import numpy as np

model = LogisticRegression()

# Simple cross-validation (returns scores only)
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')

print(f"CV Scores: {cv_scores}")
print(f"Mean: {cv_scores.mean():.3f}")
print(f"Std:  {cv_scores.std():.3f}")
print(f"95% CI: [{cv_scores.mean() - 1.96*cv_scores.std():.3f}, "
      f"{cv_scores.mean() + 1.96*cv_scores.std():.3f}]")

# Advanced cross-validation (returns multiple metrics)
cv_results = cross_validate(
    model, X_train, y_train, 
    cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
    return_train_score=True
)

print("\\nDetailed Results:")
for metric in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']:
    test_scores = cv_results[f'test_{metric}']
    train_scores = cv_results[f'train_{metric}']
    print(f"{metric.capitalize():12} - Train: {train_scores.mean():.3f} | Test: {test_scores.mean():.3f}")
```

---

**Stratified K-Fold (for classification):**

Maintains class proportions in each fold.

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train), 1):
    X_fold_train, X_fold_val = X_train[train_idx], X_train[val_idx]
    y_fold_train, y_fold_val = y_train[train_idx], y_train[val_idx]
    
    print(f"Fold {fold}:")
    print(f"  Train class distribution: {np.bincount(y_fold_train)}")
    print(f"  Val class distribution:   {np.bincount(y_fold_val)}")
```

---

**Choosing K:**
- **k=5:** Good balance (faster, slightly higher bias)
- **k=10:** More stable estimates (slower, lower bias)
- **k=n (Leave-One-Out):** Maximum data usage (very slow, high variance)

**Rule of thumb:** Use k=5 for large datasets (>10K), k=10 for smaller datasets
"""
    )

    st.markdown("---")
    st.markdown("#### ⏱ Time-Series Cross-Validation")
    st.markdown(
        """**Why Standard CV Fails for Time Series:**

```python
# ❌ WRONG: Random shuffle leaks future into past
cv_scores = cross_val_score(model, X, y, cv=5)  # Shuffles data randomly!

# ✅ RIGHT: Time-based splits
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)

for fold, (train_idx, val_idx) in enumerate(tscv.split(X), 1):
    X_train_fold = X[train_idx]
    y_train_fold = y[train_idx]
    X_val_fold = X[val_idx]
    y_val_fold = y[val_idx]
    
    print(f"Fold {fold}:")
    print(f"  Train: {min(train_idx)} to {max(train_idx)}")
    print(f"  Val:   {min(val_idx)} to {max(val_idx)}")
```

**Visualization:**
```
Fold 1: [Train        ] [Val]
Fold 2: [Train             ] [Val]
Fold 3: [Train                  ] [Val]
Fold 4: [Train                       ] [Val]
Fold 5: [Train                            ] [Val]
```

Each fold trains on more historical data, validates on future data.

---

**Gap Between Train and Validation:**

```python
class TimeSeriesSplitWithGap:
    def __init__(self, n_splits=5, test_size=None, gap=0):
        self.n_splits = n_splits
        self.test_size = test_size
        self.gap = gap
    
    def split(self, X):
        n_samples = len(X)
        
        if self.test_size is None:
            test_size = n_samples // (self.n_splits + 1)
        else:
            test_size = self.test_size
        
        indices = np.arange(n_samples)
        
        for i in range(self.n_splits):
            start_test = (i + 1) * test_size
            end_test = start_test + test_size
            
            if end_test > n_samples:
                break
            
            train_end = start_test - self.gap
            
            yield (indices[:train_end], indices[start_test:end_test])

# Use with 7-day gap (e.g., for model deployment delay)
tscv_gap = TimeSeriesSplitWithGap(n_splits=5, gap=7)

for fold, (train_idx, val_idx) in enumerate(tscv_gap.split(X), 1):
    print(f"Fold {fold}: Train until day {train_idx[-1]}, validate from day {val_idx[0]}")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 📊 Bias-Variance Tradeoff")
    st.markdown(
        """**Understanding the Tradeoff:**

$$\\text{Total Error} = \\text{Bias}^2 + \\text{Variance} + \\text{Irreducible Error}$$

- **Bias:** Error from wrong assumptions (underfitting)
- **Variance:** Error from sensitivity to training data (overfitting)
- **Irreducible Error:** Noise in data

```python
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

# Generate learning curves
train_sizes, train_scores, val_scores = learning_curve(
    model, X, y,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5,
    scoring='neg_mean_squared_error',
    n_jobs=-1
)

# Convert to positive RMSE
train_scores_mean = np.sqrt(-train_scores.mean(axis=1))
train_scores_std = np.sqrt(-train_scores.std(axis=1))
val_scores_mean = np.sqrt(-val_scores.mean(axis=1))
val_scores_std = np.sqrt(-val_scores.std(axis=1))

# Plot
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_scores_mean, label='Training error', marker='o')
plt.fill_between(train_sizes, 
                 train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.1)
plt.plot(train_sizes, val_scores_mean, label='Validation error', marker='s')
plt.fill_between(train_sizes,
                 val_scores_mean - val_scores_std,
                 val_scores_mean + val_scores_std, alpha=0.1)
plt.xlabel('Training Set Size')
plt.ylabel('RMSE')
plt.title('Learning Curves')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Diagnose from curves
if train_scores_mean[-1] < val_scores_mean[-1] * 0.8:
    print("⚠️ High variance (overfitting) - Try:")
    print("  • More training data")
    print("  • Regularization")
    print("  • Simpler model")
elif train_scores_mean[-1] > val_scores_mean[-1] * 1.2:
    print("⚠️ High bias (underfitting) - Try:")
    print("  • More complex model")
    print("  • More features")
    print("  • Reduce regularization")
else:
    print("✅ Good balance")
```

---

**Validation Curves (Hyperparameter Impact):**

```python
from sklearn.model_selection import validation_curve

param_range = [0.001, 0.01, 0.1, 1, 10, 100]

train_scores, val_scores = validation_curve(
    Ridge(), X, y,
    param_name='alpha',
    param_range=param_range,
    cv=5,
    scoring='neg_mean_squared_error'
)

train_mean = np.sqrt(-train_scores.mean(axis=1))
val_mean = np.sqrt(-val_scores.mean(axis=1))

plt.figure(figsize=(10, 6))
plt.semilogx(param_range, train_mean, label='Training', marker='o')
plt.semilogx(param_range, val_mean, label='Validation', marker='s')
plt.xlabel('Alpha (regularization)')
plt.ylabel('RMSE')
plt.title('Validation Curve for Ridge Regression')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Optimal alpha
optimal_alpha = param_range[np.argmin(val_mean)]
print(f"Optimal alpha: {optimal_alpha}")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎨 Nested Cross-Validation")
    st.markdown(
        """**Problem:** Standard CV + grid search can overestimate performance

**Solution:** Nested CV

```python
from sklearn.model_selection import GridSearchCV, cross_val_score

# Inner loop: Hyperparameter tuning
param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10]}

inner_cv = GridSearchCV(
    Ridge(),
    param_grid,
    cv=5,  # Inner 5-fold CV
    scoring='neg_mean_squared_error'
)

# Outer loop: Unbiased performance estimate
outer_cv_scores = cross_val_score(
    inner_cv,
    X_train, y_train,
    cv=5,  # Outer 5-fold CV
    scoring='neg_mean_squared_error'
)

print(f"Nested CV RMSE: {np.sqrt(-outer_cv_scores.mean()):.3f} "
      f"(+/- {np.sqrt(-outer_cv_scores.std()):.3f})")

# Compare to non-nested (biased estimate)
grid_search = GridSearchCV(Ridge(), param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
print(f"Non-nested (biased) RMSE: {np.sqrt(-grid_search.best_score_):.3f}")
```

**When to Use:**
- Small datasets (<1000 samples)
- Many hyperparameters to tune
- Need publication-ready unbiased estimates

**When Not to Use:**
- Large datasets (computationally expensive)
- Simple models with few hyperparameters
"""
    )

    st.markdown("---")
    st.markdown("#### ⚠️ Common Evaluation Mistakes")
    st.markdown(
        """**Mistake 1: Data Leakage via Scaling**

```python
# ❌ WRONG: Scale before split
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Learns from ALL data
X_train, X_test = train_test_split(X_scaled)

# Test set information leaked into training!

# ✅ RIGHT: Scale after split
X_train, X_test, y_train, y_test = train_test_split(X, y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Learn from train only
X_test_scaled = scaler.transform(X_test)  # Apply to test
```

---

**Mistake 2: Using Test Set Multiple Times**

```python
# ❌ WRONG: Iterative test set usage
models = [...]
for model in models:
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"{model}: {score}")
    
# Each test gives you info, you adjust, test again
# Test set score becomes optimistically biased!

# ✅ RIGHT: Use validation set for comparison
models = [...]
for model in models:
    model.fit(X_train, y_train)
    score = model.score(X_val, y_val)
    print(f"{model}: {score}")

# Select best model
best_model = models[best_idx]
best_model.fit(X_train, y_train)

# Test ONCE at the very end
final_score = best_model.score(X_test, y_test)
```

---

**Mistake 3: Ignoring Class Imbalance in CV**

```python
# ❌ WRONG: Random CV on imbalanced data
cv_scores = cross_val_score(model, X, y, cv=5)  # Random folds

# Some folds may have no positive examples!

# ✅ RIGHT: Stratified CV
from sklearn.model_selection import StratifiedKFold

cv_scores = cross_val_score(
    model, X, y, 
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
)
```

---

**Mistake 4: Comparing Models on Different Random Seeds**

```python
# ❌ WRONG: Different random states
model1_score = cross_val_score(model1, X, y, cv=KFold(5, shuffle=True, random_state=1))
model2_score = cross_val_score(model2, X, y, cv=KFold(5, shuffle=True, random_state=2))

# Not comparable! Different data in folds.

# ✅ RIGHT: Same CV splitter
cv = KFold(5, shuffle=True, random_state=42)

model1_score = cross_val_score(model1, X, y, cv=cv)
model2_score = cross_val_score(model2, X, y, cv=cv)
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎯 Interview Preparation")
    st.markdown(
        """**Q1: Explain train/validation/test split.**

**Answer:**
- **Training:** Fit model parameters (70%)
- **Validation:** Tune hyperparameters, select models (15%)
- **Test:** Final unbiased performance (15%) - use once!

The test set simulates real-world deployment where model sees completely new data.

---

**Q2: Why use cross-validation instead of a single validation split?**

**Answer:**
- **More stable estimates:** Reduces variance from single random split
- **Better data utilization:** Every sample used for both training and validation
- **Confidence intervals:** Can compute std dev across folds

**Trade-off:** Computational cost (k times slower)

---

**Q3: What is the difference between bias and variance?**

**Answer:**
- **Bias:** Error from wrong model assumptions
  - High bias = underfitting (model too simple)
  - Symptoms: High training error, high validation error
  - Fix: More complex model, more features
  
- **Variance:** Error from sensitivity to training data
  - High variance = overfitting (model too complex)
  - Symptoms: Low training error, high validation error
  - Fix: More data, regularization, simpler model

---

**Q4: How do you detect data leakage?**

**Answer:**
1. **Suspiciously high performance:** Test accuracy >> train accuracy
2. **Check feature creation:** Are future features used?
3. **Review preprocessing:** Scaling/imputation before split?
4. **Temporal check:** Is future data used to predict past?

**Prevention:**
- Split data FIRST
- Use pipelines (sklearn.pipeline.Pipeline)
- Time-based splits for temporal data
- Document feature creation process
"""
    )

    st.markdown("---")
    st.markdown("#### 📚 Key Takeaways")
    st.markdown(
        """**Validation Strategy Decision Tree:**

```
Is data time-ordered?
├─ Yes → Use TimeSeriesSplit
│         • No random shuffle
│         • Include gap if needed
│         • Validate on future data only
│
└─ No → Is dataset small (<5K)?
    ├─ Yes → Use 10-fold CV
    │         • More stable estimates
    │         • Or nested CV for unbiased HP tuning
    │
    └─ No → Use train/val/test split
              • 70/15/15 or 80/10/10
              • Stratify for classification
              • CV optional (expensive)
```

---

**Critical Rules:**

1. **Never touch test set** until final evaluation
2. **Split before preprocessing** (scaling, imputation)
3. **Stratify classification** data
4. **Use same CV splitter** when comparing models
5. **Report mean ± std** from CV
6. **Check for data leakage** systematically

---

**What You Can Do Now:**
- ✅ Design proper validation strategies
- ✅ Implement k-fold and stratified CV
- ✅ Handle time-series validation
- ✅ Detect and prevent data leakage
- ✅ Diagnose bias vs variance
- ✅ Use nested CV for unbiased estimates
- ✅ Avoid common evaluation mistakes

**Next:** Unit 5 (Unsupervised Learning) explores clustering and dimensionality reduction!
"""
    )


def _render_unit4_labs():
    """Labs and mini-project ideas for Unit 4."""

    st.markdown("### 🧪 HANDS-ON LABS: Unit 4 Model Evaluation")
    st.markdown(
        """**Complete these 3 labs to master validation:**

---

## Lab 1: Cross-Validation Strategies (70 min)

**Objective:** Compare validation approaches and understand their trade-offs

**Setup: Create Dataset**

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import matplotlib.pyplot as plt

# Create customer churn dataset
np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'tenure_months': np.random.randint(1, 72, n),
    'monthly_charges': np.random.normal(50, 20, n),
    'total_charges': np.random.normal(1500, 800, n),
    'num_support_calls': np.random.poisson(2, n),
    'contract_type': np.random.choice([0, 1, 2], n)
})

churn_logit = (-2 - 0.05*df['tenure_months'] + 0.02*df['monthly_charges'] + 
               0.4*df['num_support_calls'] - 0.8*df['contract_type'])
churn_prob = 1 / (1 + np.exp(-churn_logit))
df['churned'] = (np.random.random(n) < churn_prob).astype(int)

X = df.drop('churned', axis=1)
y = df['churned']

print(f"Dataset shape: {X.shape}")
print(f"Churn rate: {y.mean():.1%}")
```

---

**Part A: Single Train/Test Split Variability (20 min)**

```python
# Run same model with different random states
results = []

for seed in range(10):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y
    )
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    results.append({'seed': seed, 'accuracy': accuracy, 'f1': f1})

results_df = pd.DataFrame(results)

print("Single Split Results (10 different random splits):")
print(results_df.describe())
print(f"\\nAccuracy range: {results_df['accuracy'].min():.3f} - {results_df['accuracy'].max():.3f}")
print(f"Std deviation: {results_df['accuracy'].std():.3f}")

# Visualize variability
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].hist(results_df['accuracy'], bins=10, edgecolor='black')
axes[0].axvline(results_df['accuracy'].mean(), color='r', linestyle='--', label='Mean')
axes[0].set_xlabel('Accuracy')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Single Split Accuracy Distribution')
axes[0].legend()

axes[1].scatter(results_df['seed'], results_df['accuracy'])
axes[1].axhline(results_df['accuracy'].mean(), color='r', linestyle='--', label='Mean')
axes[1].set_xlabel('Random Seed')
axes[1].set_ylabel('Accuracy')
axes[1].set_title('Accuracy vs Random Seed')
axes[1].legend()

plt.tight_layout()
plt.show()

print(f"\\n⚠️ Single split variance: Performance varies by up to "
      f"{(results_df['accuracy'].max() - results_df['accuracy'].min()):.1%}")
```

---

**Part B: K-Fold Cross-Validation (25 min)**

```python
from sklearn.model_selection import cross_validate

model = RandomForestClassifier(n_estimators=100, random_state=42)

# Compare different k values
k_values = [3, 5, 10, 20]
cv_results = {}

for k in k_values:
    print(f"\\nTesting {k}-fold CV...")
    
    cv_scores = cross_validate(
        model, X, y,
        cv=StratifiedKFold(n_splits=k, shuffle=True, random_state=42),
        scoring=['accuracy', 'f1'],
        return_train_score=True,
        n_jobs=-1
    )
    
    cv_results[k] = {
        'train_accuracy': cv_scores['train_accuracy'],
        'test_accuracy': cv_scores['test_accuracy'],
        'train_f1': cv_scores['train_f1'],
        'test_f1': cv_scores['test_f1']
    }
    
    print(f"  Train Accuracy: {cv_scores['train_accuracy'].mean():.3f} "
          f"(±{cv_scores['train_accuracy'].std():.3f})")
    print(f"  Test Accuracy:  {cv_scores['test_accuracy'].mean():.3f} "
          f"(±{cv_scores['test_accuracy'].std():.3f})")

# Compare stability
comparison = []
for k in k_values:
    comparison.append({
        'k': k,
        'mean_accuracy': cv_results[k]['test_accuracy'].mean(),
        'std_accuracy': cv_results[k]['test_accuracy'].std(),
        'mean_f1': cv_results[k]['test_f1'].mean(),
        'std_f1': cv_results[k]['test_f1'].std()
    })

comparison_df = pd.DataFrame(comparison)
print("\\nCross-Validation Comparison:")
print(comparison_df.to_string(index=False))

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for k in k_values:
    axes[0].scatter([k]*k, cv_results[k]['test_accuracy'], alpha=0.6, label=f'{k}-fold')
    axes[0].plot([k-0.2, k+0.2], 
                 [cv_results[k]['test_accuracy'].mean()]*2, 
                 'r-', linewidth=2)

axes[0].set_xlabel('Number of Folds (k)')
axes[0].set_ylabel('Accuracy')
axes[0].set_title('CV Score Distribution by k')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(comparison_df['k'], comparison_df['std_accuracy'], marker='o')
axes[1].set_xlabel('Number of Folds (k)')
axes[1].set_ylabel('Standard Deviation')
axes[1].set_title('CV Score Stability vs k')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"\\n✅ CV is more stable: {comparison_df['std_accuracy'].min():.4f} std "
      f"vs single split {results_df['accuracy'].std():.4f}")
```

---

**Part C: Learning Curves (25 min)**

```python
from sklearn.model_selection import learning_curve

# Generate learning curves with different training sizes
train_sizes = np.linspace(0.1, 1.0, 10)

train_sizes_abs, train_scores, val_scores = learning_curve(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X, y,
    train_sizes=train_sizes,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

# Calculate statistics
train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
val_mean = val_scores.mean(axis=1)
val_std = val_scores.std(axis=1)

print("Learning Curve Results:")
for i, size in enumerate(train_sizes_abs):
    print(f"Training size {size:4d}: "
          f"Train={train_mean[i]:.3f}(±{train_std[i]:.3f}) | "
          f"Val={val_mean[i]:.3f}(±{val_std[i]:.3f})")

# Plot learning curves
plt.figure(figsize=(10, 6))
plt.plot(train_sizes_abs, train_mean, 'o-', color='r', label='Training score')
plt.fill_between(train_sizes_abs, train_mean - train_std, 
                 train_mean + train_std, alpha=0.1, color='r')
plt.plot(train_sizes_abs, val_mean, 'o-', color='g', label='CV score')
plt.fill_between(train_sizes_abs, val_mean - val_std,
                 val_mean + val_std, alpha=0.1, color='g')
plt.xlabel('Training Set Size')
plt.ylabel('Accuracy')
plt.title('Learning Curves')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.show()

# Diagnose
gap = train_mean[-1] - val_mean[-1]
if gap > 0.1:
    print(f"\\n⚠️ High variance (overfitting): gap = {gap:.3f}")
    print("   Solutions: More data, regularization, simpler model")
elif val_mean[-1] < 0.7:
    print(f"\\n⚠️ High bias (underfitting): val score = {val_mean[-1]:.3f}")
    print("   Solutions: More complex model, more features")
else:
    print(f"\\n✅ Good fit: gap = {gap:.3f}, val score = {val_mean[-1]:.3f}")
```

---

## Lab 2: Detecting Data Leakage (60 min)

**Objective:** Identify and fix data leakage issues

**Part A: Scaling Leakage (20 min)**

```python
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Generate data
X_leakage = np.random.randn(200, 5)
y_leakage = (X_leakage[:, 0] + X_leakage[:, 1] > 0).astype(int)

print("Scenario: Predict binary outcome from 5 features")
print(f"True dependency: y = (X[0] + X[1] > 0)")
print(f"Class balance: {y_leakage.mean():.1%} positive\\n")

# ❌ WRONG: Scale before split
scaler_wrong = StandardScaler()
X_scaled_wrong = scaler_wrong.fit_transform(X_leakage)

X_train_wrong, X_test_wrong, y_train_wrong, y_test_wrong = train_test_split(
    X_scaled_wrong, y_leakage, test_size=0.2, random_state=42
)

model_wrong = LogisticRegression()
model_wrong.fit(X_train_wrong, y_train_wrong)
score_wrong = model_wrong.score(X_test_wrong, y_test_wrong)

print(f"❌ WRONG (scale before split): Test accuracy = {score_wrong:.3f}")

# ✅ RIGHT: Scale after split
X_train_right, X_test_right, y_train_right, y_test_right = train_test_split(
    X_leakage, y_leakage, test_size=0.2, random_state=42
)

scaler_right = StandardScaler()
X_train_scaled_right = scaler_right.fit_transform(X_train_right)
X_test_scaled_right = scaler_right.transform(X_test_right)

model_right = LogisticRegression()
model_right.fit(X_train_scaled_right, y_train_right)
score_right = model_right.score(X_test_scaled_right, y_test_right)

print(f"✅ RIGHT (scale after split): Test accuracy = {score_right:.3f}")

print(f"\\nDifference: {abs(score_wrong - score_right):.3f}")
print("With leakage, test set information contaminated training!")
```

---

**Part B: Target Leakage (20 min)**

```python
# Create dataset with target leakage
n = 1000
age = np.random.randint(18, 80, n)
income = np.random.normal(50000, 20000, n)
credit_score = np.random.normal(650, 100, n)

# Target: Loan default (binary)
default_prob = 1 / (1 + np.exp(-(
    -5 + 0.05*age + 0.00001*income - 0.01*credit_score
)))
loan_default = (np.random.random(n) < default_prob).astype(int)

# ❌ Create leaky feature: "days_since_default"
# This is ONLY known AFTER default happens!
days_since_default = np.where(
    loan_default == 1,
    np.random.randint(1, 100, n),  # Days for defaulters
    np.random.randint(300, 1000, n)  # Large number for non-defaulters
)

df_leaky = pd.DataFrame({
    'age': age,
    'income': income,
    'credit_score': credit_score,
    'days_since_default': days_since_default,  # LEAKY!
    'loan_default': loan_default
})

# Model WITH leaky feature
X_with_leak = df_leaky[['age', 'income', 'credit_score', 'days_since_default']]
y = df_leaky['loan_default']

X_train, X_test, y_train, y_test = train_test_split(X_with_leak, y, test_size=0.2, random_state=42)

model_leak = LogisticRegression()
model_leak.fit(X_train, y_train)
score_leak = model_leak.score(X_test, y_test)

print(f"❌ With leaky feature: Test accuracy = {score_leak:.3f}")
print(f"Feature importances: {model_leak.coef_[0]}")

# Model WITHOUT leaky feature
X_no_leak = df_leaky[['age', 'income', 'credit_score']]

X_train_clean, X_test_clean, y_train, y_test = train_test_split(
    X_no_leak, y, test_size=0.2, random_state=42
)

model_clean = LogisticRegression()
model_clean.fit(X_train_clean, y_train)
score_clean = model_clean.score(X_test_clean, y_test)

print(f"\\n✅ Without leaky feature: Test accuracy = {score_clean:.3f}")
print(f"Feature importances: {model_clean.coef_[0]}")

print(f"\\n⚠️ Suspicious accuracy drop: {score_leak - score_clean:.3f}")
print("This indicates 'days_since_default' was leaking target information!")
```

---

**Part C: Temporal Leakage (20 min)**

```python
from sklearn.model_selection import TimeSeriesSplit

# Create time-ordered sales data
dates = pd.date_range('2023-01-01', periods=365, freq='D')
sales = 100 + np.cumsum(np.random.randn(365) * 10)  # Trending sales
sales = sales.clip(min=50)

# Feature: Moving average (using future data - WRONG!)
window = 7
sales_ma_wrong = pd.Series(sales).rolling(window=window, center=True).mean().fillna(sales)

df_time = pd.DataFrame({
    'date': dates,
    'sales': sales,
    'sales_ma_wrong': sales_ma_wrong,  # Uses future data!
    'day_of_week': dates.dayofweek,
    'month': dates.month
})

# Predict tomorrow's sales
df_time['target'] = df_time['sales'].shift(-1)
df_time = df_time.dropna()

print("Temporal Data:")
print(df_time.head())

# ❌ WRONG: Random CV (shuffles time order!)
X_temporal = df_time[['sales_ma_wrong', 'day_of_week', 'month']]
y_temporal = df_time['target']

cv_random = cross_val_score(
    LinearRegression(), X_temporal, y_temporal, 
    cv=5, scoring='r2'
)

print(f"\\n❌ Random CV (shuffled): R² = {cv_random.mean():.3f} (±{cv_random.std():.3f})")

# ✅ RIGHT: Time series CV (preserves order)
tscv = TimeSeriesSplit(n_splits=5)

cv_time = cross_val_score(
    LinearRegression(), X_temporal, y_temporal,
    cv=tscv, scoring='r2'
)

print(f"✅ Time Series CV: R² = {cv_time.mean():.3f} (±{cv_time.std():.3f})")

print(f"\\nDifference: {cv_random.mean() - cv_time.mean():.3f}")
print("Random CV inflates performance by using future to predict past!")

# Visualize splits
fig, axes = plt.subplots(5, 1, figsize=(12, 10))

for i, (train_idx, val_idx) in enumerate(tscv.split(X_temporal)):
    axes[i].scatter(train_idx, [1]*len(train_idx), c='blue', marker='|', s=100, label='Train')
    axes[i].scatter(val_idx, [1]*len(val_idx), c='red', marker='|', s=100, label='Val')
    axes[i].set_xlim(0, len(X_temporal))
    axes[i].set_ylim(0.5, 1.5)
    axes[i].set_yticks([])
    axes[i].set_title(f'Fold {i+1}')
    axes[i].legend()

plt.tight_layout()
plt.show()
```

---

## Lab 3: Hyperparameter Tuning & Nested CV (80 min)

**Objective:** Properly tune hyperparameters without overfitting

**Part A: Grid Search with Validation Set (25 min)**

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Use churn data from Lab 1
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Further split train into train and validation
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.25, random_state=42, stratify=y_train_full
)

print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7, 10],
    'min_samples_split': [2, 5, 10]
}

print(f"\\nTesting {len(param_grid['n_estimators']) * len(param_grid['max_depth']) * len(param_grid['min_samples_split'])} combinations")

# Grid search
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,  # 5-fold CV on training data
    scoring='f1',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"\\nBest parameters: {grid_search.best_params_}")
print(f"Best CV F1: {grid_search.best_score_:.3f}")

# Evaluate on validation set
best_model = grid_search.best_estimator_
val_score = f1_score(y_val, best_model.predict(X_val))
print(f"Validation F1: {val_score:.3f}")

# Final test (use once!)
test_score = f1_score(y_test, best_model.predict(X_test))
print(f"Test F1 (final): {test_score:.3f}")

# Analyze results
results_df = pd.DataFrame(grid_search.cv_results_)
top_10 = results_df.nsmallest(10, 'rank_test_score')[
    ['params', 'mean_test_score', 'std_test_score', 'rank_test_score']
]

print("\\nTop 10 parameter combinations:")
print(top_10.to_string(index=False))
```

---

**Part B: Nested Cross-Validation (30 min)**

```python
from sklearn.model_selection import cross_val_score

# Nested CV: Inner CV for hyperparameter tuning, outer CV for unbiased estimate

# Define inner CV grid search
inner_cv = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid={
        'n_estimators': [50, 100],
        'max_depth': [3, 5, 7]
    },
    cv=3,  # Inner 3-fold CV
    scoring='f1',
    n_jobs=-1
)

# Outer CV for performance estimation
outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Run nested CV
nested_scores = cross_val_score(
    inner_cv,
    X_train_full, y_train_full,
    cv=outer_cv,
    scoring='f1',
    n_jobs=-1
)

print("Nested CV Results:")
print(f"F1 scores per outer fold: {nested_scores}")
print(f"Mean F1: {nested_scores.mean():.3f}")
print(f"Std F1:  {nested_scores.std():.3f}")
print(f"95% CI:  [{nested_scores.mean() - 1.96*nested_scores.std():.3f}, "
      f"{nested_scores.mean() + 1.96*nested_scores.std():.3f}]")

# Compare to non-nested (biased)
non_nested_grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid={'n_estimators': [50, 100], 'max_depth': [3, 5, 7]},
    cv=5,
    scoring='f1'
)

non_nested_grid.fit(X_train_full, y_train_full)
non_nested_score = non_nested_grid.best_score_

print(f"\\nNon-nested CV (biased): {non_nested_score:.3f}")
print(f"Nested CV (unbiased):    {nested_scores.mean():.3f}")
print(f"Optimism bias:           {non_nested_score - nested_scores.mean():.3f}")

print("\\n⚠️ Non-nested CV overestimates performance!")
print("   Use nested CV for publication-ready estimates.")
```

---

**Part C: Validation Curves (25 min)**

```python
from sklearn.model_selection import validation_curve

# Study effect of max_depth on performance
param_range = [1, 2, 3, 5, 7, 10, 15, 20]

train_scores, val_scores = validation_curve(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X_train_full, y_train_full,
    param_name='max_depth',
    param_range=param_range,
    cv=5,
    scoring='f1',
    n_jobs=-1
)

train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
val_mean = val_scores.mean(axis=1)
val_std = val_scores.std(axis=1)

# Plot validation curve
plt.figure(figsize=(10, 6))
plt.plot(param_range, train_mean, 'o-', color='r', label='Training F1')
plt.fill_between(param_range, train_mean - train_std, 
                 train_mean + train_std, alpha=0.1, color='r')
plt.plot(param_range, val_mean, 'o-', color='g', label='Validation F1')
plt.fill_between(param_range, val_mean - val_std,
                 val_mean + val_std, alpha=0.1, color='g')
plt.xlabel('max_depth')
plt.ylabel('F1 Score')
plt.title('Validation Curve: max_depth')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.show()

# Find optimal depth
optimal_depth = param_range[np.argmax(val_mean)]
print(f"Optimal max_depth: {optimal_depth}")
print(f"Best validation F1: {val_mean.max():.3f}")

# Diagnose overfitting
for i, depth in enumerate(param_range):
    gap = train_mean[i] - val_mean[i]
    print(f"Depth {depth:2d}: Train={train_mean[i]:.3f}, Val={val_mean[i]:.3f}, Gap={gap:.3f}")

print(f"\\n⚠️ Beyond depth {optimal_depth}, model starts overfitting")
```

---

**Lab Completion Checklist:**
- ☐ Compared single split vs cross-validation stability
- ☐ Implemented k-fold and stratified CV
- ☐ Generated learning curves
- ☐ Detected scaling leakage
- ☐ Identified target leakage
- ☐ Handled temporal leakage with TimeSeriesSplit
- ☐ Performed grid search with proper validation
- ☐ Implemented nested CV for unbiased estimates
- ☐ Created validation curves

**Next:** Unit 5 explores unsupervised learning and clustering!
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

    st.markdown("---")
    st.markdown("#### 🎯 K-Means Clustering")
    st.markdown(
        """**Algorithm:** Partitions data into k clusters by minimizing within-cluster variance

**How it works:**
1. Randomly initialize k centroids
2. Assign each point to nearest centroid
3. Recalculate centroids as mean of assigned points
4. Repeat steps 2-3 until convergence

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create customer data
np.random.seed(42)
n = 300

df = pd.DataFrame({
    'avg_purchase': np.concatenate([
        np.random.normal(50, 10, 100),   # Low spenders
        np.random.normal(150, 20, 100),  # Medium spenders
        np.random.normal(300, 30, 100)   # High spenders
    ]),
    'visit_frequency': np.concatenate([
        np.random.normal(2, 0.5, 100),   # Infrequent
        np.random.normal(8, 1, 100),     # Regular
        np.random.normal(20, 3, 100)     # Very frequent
    ]),
    'account_age_months': np.random.uniform(1, 60, n)
})

# Scale features (CRITICAL for k-means!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Fit k-means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

df['cluster'] = clusters

print(f"Cluster sizes: {np.bincount(clusters)}")
print(f"\\nInertia (within-cluster sum of squares): {kmeans.inertia_:.2f}")

# Cluster centroids (in original scale)
centroids = scaler.inverse_transform(kmeans.cluster_centers_)
centroids_df = pd.DataFrame(centroids, columns=df.columns[:-1])
print("\\nCluster Centroids:")
print(centroids_df)

# Visualize
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['avg_purchase'], df['visit_frequency'], 
                     c=df['cluster'], cmap='viridis', alpha=0.6)
plt.scatter(centroids[:, 0], centroids[:, 1], 
           c='red', marker='X', s=200, edgecolors='black', label='Centroids')
plt.xlabel('Average Purchase ($)')
plt.ylabel('Visit Frequency (per month)')
plt.title('Customer Segments (K-Means)')
plt.colorbar(scatter, label='Cluster')
plt.legend()
plt.show()
```

**Choosing k (Elbow Method):**

```python
inertias = []
silhouette_scores = []
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    
    from sklearn.metrics import silhouette_score
    score = silhouette_score(X_scaled, kmeans.labels_)
    silhouette_scores.append(score)

# Plot elbow curve
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(k_range, inertias, 'o-')
axes[0].set_xlabel('Number of clusters (k)')
axes[0].set_ylabel('Inertia')
axes[0].set_title('Elbow Method')
axes[0].grid(True, alpha=0.3)

axes[1].plot(k_range, silhouette_scores, 'o-', color='green')
axes[1].set_xlabel('Number of clusters (k)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Analysis')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

optimal_k = k_range[np.argmax(silhouette_scores)]
print(f"\\nOptimal k (by silhouette): {optimal_k}")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🌳 Hierarchical Clustering")
    st.markdown(
        """**Algorithm:** Builds tree of clusters (dendrogram)

**Types:**
- **Agglomerative (bottom-up):** Start with each point as cluster, merge similar ones
- **Divisive (top-down):** Start with one cluster, split recursively

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist

# Compute linkage matrix
linkage_matrix = linkage(X_scaled, method='ward')

# Plot dendrogram
plt.figure(figsize=(12, 6))
dendrogram(linkage_matrix, truncate_mode='lastp', p=20)
plt.xlabel('Sample Index or (Cluster Size)')
plt.ylabel('Distance')
plt.title('Hierarchical Clustering Dendrogram')
plt.axhline(y=10, color='r', linestyle='--', label='Cut height')
plt.legend()
plt.show()

# Fit hierarchical clustering
hc = AgglomerativeClustering(n_clusters=3, linkage='ward')
hc_clusters = hc.fit_predict(X_scaled)

df['hc_cluster'] = hc_clusters

print(f"Hierarchical cluster sizes: {np.bincount(hc_clusters)}")

# Compare with k-means
from sklearn.metrics import adjusted_rand_score

ari = adjusted_rand_score(clusters, hc_clusters)
print(f"\\nAgreement with k-means (ARI): {ari:.3f}")
```

**Linkage Methods:**
- **Ward:** Minimizes within-cluster variance (similar to k-means)
- **Complete:** Maximum distance between clusters
- **Average:** Average distance between all pairs
- **Single:** Minimum distance (can create chains)
"""
    )

    st.markdown("---")
    st.markdown("#### 🔍 DBSCAN (Density-Based Clustering)")
    st.markdown(
        """**Algorithm:** Finds clusters as dense regions, identifies outliers

**Parameters:**
- **eps:** Maximum distance between points in same cluster
- **min_samples:** Minimum points to form dense region

```python
from sklearn.cluster import DBSCAN

# DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan_clusters = dbscan.fit_predict(X_scaled)

df['dbscan_cluster'] = dbscan_clusters

# -1 = noise/outliers
n_clusters = len(set(dbscan_clusters)) - (1 if -1 in dbscan_clusters else 0)
n_noise = list(dbscan_clusters).count(-1)

print(f"Number of clusters: {n_clusters}")
print(f"Number of noise points: {n_noise}")
print(f"Cluster sizes: {np.bincount(dbscan_clusters[dbscan_clusters >= 0])}")

# Visualize with noise
plt.figure(figsize=(10, 6))
colors = ['red' if x == -1 else plt.cm.viridis(x / n_clusters) 
          for x in dbscan_clusters]
plt.scatter(df['avg_purchase'], df['visit_frequency'], c=colors, alpha=0.6)
plt.xlabel('Average Purchase ($)')
plt.ylabel('Visit Frequency')
plt.title('DBSCAN Clustering (red = noise)')
plt.show()
```

**When to use DBSCAN:**
- ✅ Non-spherical clusters
- ✅ Varying cluster sizes
- ✅ Need to identify outliers
- ❌ High-dimensional data (curse of dimensionality)
"""
    )

    st.markdown("---")
    st.markdown("#### 📊 Clustering Evaluation Metrics")
    st.markdown(
        """**1. Silhouette Score (-1 to 1)**

Measures how similar a point is to its own cluster vs other clusters.

```python
from sklearn.metrics import silhouette_score, silhouette_samples

# Overall silhouette score
sil_score = silhouette_score(X_scaled, clusters)
print(f"Silhouette Score: {sil_score:.3f}")

# Per-sample silhouette values
sil_samples = silhouette_samples(X_scaled, clusters)

# Silhouette plot
fig, ax = plt.subplots(figsize=(10, 6))

y_lower = 10
for i in range(3):
    cluster_sil_values = sil_samples[clusters == i]
    cluster_sil_values.sort()
    
    size_cluster_i = cluster_sil_values.shape[0]
    y_upper = y_lower + size_cluster_i
    
    color = plt.cm.viridis(i / 3)
    ax.fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_sil_values,
                     facecolor=color, edgecolor=color, alpha=0.7,
                     label=f'Cluster {i}')
    
    y_lower = y_upper + 10

ax.axvline(x=sil_score, color="red", linestyle="--", label=f'Average={sil_score:.2f}')
ax.set_xlabel("Silhouette Coefficient")
ax.set_ylabel("Cluster")
ax.set_title("Silhouette Plot")
ax.legend()
plt.show()

# Interpretation
if sil_score > 0.5:
    print("✅ Good clustering: Clusters are well-separated")
elif sil_score > 0.25:
    print("⚠️ Moderate clustering: Some overlap between clusters")
else:
    print("❌ Poor clustering: Clusters are not well-defined")
```

---

**2. Davies-Bouldin Index (lower is better)**

```python
from sklearn.metrics import davies_bouldin_score

db_score = davies_bouldin_score(X_scaled, clusters)
print(f"Davies-Bouldin Score: {db_score:.3f}")
print("Lower is better (well-separated, compact clusters)")
```

---

**3. Calinski-Harabasz Index (higher is better)**

```python
from sklearn.metrics import calinski_harabasz_score

ch_score = calinski_harabasz_score(X_scaled, clusters)
print(f"Calinski-Harabasz Score: {ch_score:.1f}")
print("Higher is better (dense, well-separated clusters)")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎨 Dimensionality Reduction")
    st.markdown(
        """**Why reduce dimensions?**
- Visualize high-dimensional data
- Remove noise
- Speed up algorithms
- Avoid curse of dimensionality

---

**PCA (Principal Component Analysis)**

Finds orthogonal axes that maximize variance.

```python
from sklearn.decomposition import PCA

# Fit PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total variance explained: {pca.explained_variance_ratio_.sum():.1%}")

# Visualize in 2D
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', alpha=0.6)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('PCA Projection with Clusters')
plt.colorbar(scatter, label='Cluster')
plt.show()

# Scree plot (choose number of components)
pca_full = PCA()
pca_full.fit(X_scaled)

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(pca_full.explained_variance_ratio_)+1),
         np.cumsum(pca_full.explained_variance_ratio_), 'o-')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Scree Plot')
plt.axhline(y=0.95, color='r', linestyle='--', label='95% threshold')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
```

---

**t-SNE (t-Distributed Stochastic Neighbor Embedding)**

Preserves local structure, great for visualization.

```python
from sklearn.manifold import TSNE

# Fit t-SNE (slower than PCA)
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
X_tsne = tsne.fit_transform(X_scaled)

# Visualize
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=clusters, cmap='viridis', alpha=0.6)
plt.xlabel('t-SNE 1')
plt.ylabel('t-SNE 2')
plt.title('t-SNE Projection with Clusters')
plt.colorbar(scatter, label='Cluster')
plt.show()
```

**PCA vs t-SNE:**
| Feature | PCA | t-SNE |
|---------|-----|-------|
| Speed | ✅ Fast | ❌ Slow |
| Interpretable | ✅ Yes (linear) | ❌ No (non-linear) |
| Preserves | Global structure | Local structure |
| Deterministic | ✅ Yes | ❌ No (random init) |
| Use for | Feature engineering | Visualization only |
"""
    )

    st.markdown("---")
    st.markdown("#### 💼 Business Segmentation Example")
    st.markdown(
        """**Customer Segmentation for Marketing**

```python
# Profile each cluster
cluster_profiles = df.groupby('cluster').agg({
    'avg_purchase': ['mean', 'std', 'count'],
    'visit_frequency': ['mean', 'std'],
    'account_age_months': ['mean', 'std']
}).round(2)

print("Cluster Profiles:")
print(cluster_profiles)

# Assign business labels
cluster_names = {
    0: "Budget Shoppers (Low spend, infrequent)",
    1: "Loyal Regulars (Medium spend, frequent)",
    2: "Premium VIPs (High spend, very frequent)"
}

df['segment_name'] = df['cluster'].map(cluster_names)

# Segment distribution
print("\\nSegment Distribution:")
print(df['segment_name'].value_counts())

# Business recommendations
recommendations = {
    "Budget Shoppers": "Focus on promotions and discounts to increase frequency",
    "Loyal Regulars": "Loyalty program with points and rewards",
    "Premium VIPs": "Exclusive early access and personalized service"
}

for segment, action in recommendations.items():
    count = (df['segment_name'] == segment).sum()
    print(f"\\n{segment} ({count} customers): {action}")
```

**Visualize Segments:**

```python
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for i, col in enumerate(['avg_purchase', 'visit_frequency', 'account_age_months']):
    df.boxplot(column=col, by='segment_name', ax=axes[i])
    axes[i].set_title(f'{col} by Segment')
    axes[i].set_xlabel('')

plt.suptitle('')
plt.tight_layout()
plt.show()
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎯 Interview Preparation")
    st.markdown(
        """**Q1: When would you use k-means vs hierarchical clustering?**

**Answer:**
- **K-means:** Large datasets (>10K), know approximate number of clusters, want speed
- **Hierarchical:** Small datasets, explore different numbers of clusters, need dendrogram

---

**Q2: Why is feature scaling critical for k-means?**

**Answer:**
K-means uses Euclidean distance. Features with larger scales dominate the distance calculation.

Example: Age (0-100) vs Income (£0-£200K) without scaling means income dominates.

---

**Q3: How do you choose the number of clusters (k)?**

**Answer:**
1. **Elbow method:** Plot inertia vs k, look for "elbow"
2. **Silhouette score:** Maximize average silhouette
3. **Business constraints:** Predefined segments (e.g., 3 pricing tiers)
4. **Domain knowledge:** What's actionable/interpretable?

No single "correct" answer - depends on business goals.

---

**Q4: What's the difference between PCA and t-SNE?**

**Answer:**
- **PCA:** Linear transformation, preserves global structure, deterministic, fast. Use for feature engineering.
- **t-SNE:** Non-linear, preserves local structure, stochastic, slow. Use for visualization only.

t-SNE is NOT for dimensionality reduction in pipelines (distances don't generalize to new data).
"""
    )

    st.markdown("---")
    st.markdown("#### 📚 Key Takeaways")
    st.markdown(
        """**Clustering Algorithm Comparison:**

| Algorithm | Pros | Cons | When to Use |
|-----------|------|------|-------------|
| **K-Means** | Fast, scalable, simple | Needs k, assumes spherical | Large datasets, clear segments |
| **Hierarchical** | No need to choose k, dendrogram | Slow (O(n³)), no new predictions | Small data, exploratory |
| **DBSCAN** | Finds outliers, arbitrary shapes | Needs eps/min_samples tuning | Non-spherical clusters, noise |

---

**Critical Steps:**
1. **Scale features** (StandardScaler)
2. **Choose algorithm** based on data size and structure
3. **Determine k** (elbow, silhouette, business)
4. **Evaluate** (silhouette, business validation)
5. **Profile clusters** (describe characteristics)
6. **Name segments** (business-friendly labels)
7. **Take action** (segment-specific strategies)

---

**What You Can Do Now:**
- ✅ Perform k-means clustering with optimal k
- ✅ Build hierarchical clustering dendrograms
- ✅ Identify outliers with DBSCAN
- ✅ Evaluate clusters with silhouette score
- ✅ Reduce dimensions with PCA and t-SNE
- ✅ Profile and name customer segments
- ✅ Create actionable business strategies

**Next:** Unit 6 (Model Deployment) covers productionizing ML models!
"""
    )


def _render_unit5_labs():
    """Labs and mini-project ideas for Unit 5."""

    st.markdown("### 🧪 HANDS-ON LABS: Unit 5 Unsupervised Learning")
    st.markdown(
        """**Complete these 3 labs to master clustering:**

---

## Lab 1: Customer Segmentation with K-Means (80 min)

**Objective:** Build actionable customer segments from behavioral data

**Setup: Create Customer Dataset**

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
import seaborn as sns

# Create realistic customer data
np.random.seed(42)
n = 500

# Generate 3 distinct customer segments
segments = np.random.choice([0, 1, 2], n, p=[0.4, 0.35, 0.25])

df = pd.DataFrame({
    'customer_id': range(1, n+1),
    'avg_monthly_spend': np.where(segments == 0, np.random.normal(30, 10, n),
                                  np.where(segments == 1, np.random.normal(150, 30, n),
                                          np.random.normal(400, 80, n))),
    'visits_per_month': np.where(segments == 0, np.random.poisson(1, n),
                                 np.where(segments == 1, np.random.poisson(6, n),
                                         np.random.poisson(15, n))),
    'account_age_months': np.random.uniform(1, 48, n),
    'support_tickets': np.where(segments == 0, np.random.poisson(0.5, n),
                               np.where(segments == 1, np.random.poisson(1.5, n),
                                       np.random.poisson(0.3, n))),
    'mobile_app_usage': np.where(segments == 0, np.random.choice([0, 1], n, p=[0.8, 0.2]),
                                 np.where(segments == 1, np.random.choice([0, 1], n, p=[0.3, 0.7]),
                                         np.random.choice([0, 1], n, p=[0.1, 0.9])))
})

# Clip to realistic ranges
df['avg_monthly_spend'] = df['avg_monthly_spend'].clip(lower=10)
df['visits_per_month'] = df['visits_per_month'].clip(lower=0)
df['support_tickets'] = df['support_tickets'].clip(lower=0)

print("Customer Dataset:")
print(df.describe())
df.to_csv('customer_data.csv', index=False)
```

---

**Part A: Determine Optimal K (25 min)**

```python
df = pd.read_csv('customer_data.csv')

# Features for clustering
features = ['avg_monthly_spend', 'visits_per_month', 'account_age_months', 
            'support_tickets', 'mobile_app_usage']
X = df[features]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Scaled data shape: {X_scaled.shape}")
print(f"Feature means (should be ~0): {X_scaled.mean(axis=0).round(3)}")
print(f"Feature stds (should be ~1): {X_scaled.std(axis=0).round(3)}")

# Test different k values
k_range = range(2, 11)
inertias = []
silhouette_scores = []

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    
    inertias.append(kmeans.inertia_)
    sil_score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(sil_score)
    
    print(f"k={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={sil_score:.3f}")

# Elbow method visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Elbow plot
axes[0].plot(k_range, inertias, 'o-', linewidth=2, markersize=8)
axes[0].set_xlabel('Number of Clusters (k)')
axes[0].set_ylabel('Inertia (Within-Cluster Sum of Squares)')
axes[0].set_title('Elbow Method for Optimal k')
axes[0].grid(True, alpha=0.3)

# Silhouette plot
axes[1].plot(k_range, silhouette_scores, 'o-', color='green', linewidth=2, markersize=8)
axes[1].set_xlabel('Number of Clusters (k)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Score vs k')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Optimal k
optimal_k = k_range[np.argmax(silhouette_scores)]
print(f"\\n✅ Recommended k: {optimal_k} (highest silhouette score)")
```

---

**Part B: Fit & Evaluate K-Means (30 min)**

```python
# Fit final k-means
k_final = 3
kmeans_final = KMeans(n_clusters=k_final, random_state=42, n_init=10)
clusters = kmeans_final.fit_predict(X_scaled)

df['cluster'] = clusters

print(f"Cluster distribution:\\n{df['cluster'].value_counts().sort_index()}")

# Silhouette analysis
sil_score = silhouette_score(X_scaled, clusters)
sil_samples = silhouette_samples(X_scaled, clusters)

print(f"\\nOverall Silhouette Score: {sil_score:.3f}")

# Silhouette plot
fig, ax = plt.subplots(figsize=(10, 6))

y_lower = 10
for i in range(k_final):
    cluster_sil_values = sil_samples[clusters == i]
    cluster_sil_values.sort()
    
    size_cluster_i = cluster_sil_values.shape[0]
    y_upper = y_lower + size_cluster_i
    
    color = plt.cm.viridis(i / k_final)
    ax.fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_sil_values,
                     facecolor=color, alpha=0.7, label=f'Cluster {i}')
    
    # Cluster mean
    ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    
    y_lower = y_upper + 10

ax.axvline(x=sil_score, color="red", linestyle="--", 
           linewidth=2, label=f'Average={sil_score:.2f}')
ax.set_xlabel("Silhouette Coefficient", fontsize=12)
ax.set_ylabel("Cluster", fontsize=12)
ax.set_title("Silhouette Plot for Customer Segments", fontsize=14)
ax.legend()
plt.tight_layout()
plt.show()

# Cluster centroids (original scale)
centroids = scaler.inverse_transform(kmeans_final.cluster_centers_)
centroids_df = pd.DataFrame(centroids, columns=features)
centroids_df.index = [f'Cluster {i}' for i in range(k_final)]

print("\\nCluster Centroids (Original Scale):")
print(centroids_df.round(2))
```

---

**Part C: Profile & Label Segments (25 min)**

```python
# Detailed cluster profiling
cluster_profiles = df.groupby('cluster').agg({
    'avg_monthly_spend': ['mean', 'std', 'min', 'max'],
    'visits_per_month': ['mean', 'std'],
    'account_age_months': ['mean', 'std'],
    'support_tickets': ['mean', 'sum'],
    'mobile_app_usage': ['mean', 'sum'],
    'customer_id': 'count'
}).round(2)

cluster_profiles.columns = ['_'.join(col).strip() for col in cluster_profiles.columns.values]
print("\\nDetailed Cluster Profiles:")
print(cluster_profiles)

# Assign business-friendly names
cluster_descriptions = {
    0: "💰 Premium VIP (High spend, frequent, engaged)",
    1: "🛒 Regular Shoppers (Medium spend, moderate frequency)",
    2: "💸 Budget Browsers (Low spend, infrequent)"
}

# Map based on average spend (sort clusters by spend)
cluster_spend = df.groupby('cluster')['avg_monthly_spend'].mean().sort_values(ascending=False)
cluster_mapping = {old: new for new, old in enumerate(cluster_spend.index)}
df['cluster_ordered'] = df['cluster'].map(cluster_mapping)
df['segment_name'] = df['cluster_ordered'].map(cluster_descriptions)

print("\\nSegment Distribution:")
print(df['segment_name'].value_counts())

# Visualization: Segment profiles
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

for idx, col in enumerate(features):
    row = idx // 3
    col_idx = idx % 3
    
    df.boxplot(column=col, by='segment_name', ax=axes[row, col_idx])
    axes[row, col_idx].set_title(f'{col}')
    axes[row, col_idx].set_xlabel('')

# Remove last subplot if odd number of features
if len(features) % 3 != 0:
    fig.delaxes(axes[1, 2])

plt.suptitle('Customer Segment Profiles', fontsize=16, y=1.00)
plt.tight_layout()
plt.show()

# Scatter plot: Key dimensions
plt.figure(figsize=(12, 6))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

for i, (name, group) in enumerate(df.groupby('segment_name')):
    plt.scatter(group['avg_monthly_spend'], group['visits_per_month'],
               label=name, alpha=0.6, s=100, c=colors[i])

# Plot centroids
for i, row in centroids_df.iterrows():
    plt.scatter(row['avg_monthly_spend'], row['visits_per_month'],
               marker='X', s=500, c='black', edgecolors='white', linewidths=2)

plt.xlabel('Average Monthly Spend ($)', fontsize=12)
plt.ylabel('Visits per Month', fontsize=12)
plt.title('Customer Segments: Spend vs Frequency', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Business recommendations
recommendations = {
    "💰 Premium VIP (High spend, frequent, engaged)": 
        "• VIP customer service\\n• Early product access\\n• Personalized recommendations",
    "🛒 Regular Shoppers (Medium spend, moderate frequency)": 
        "• Loyalty rewards program\\n• Bundle offers\\n• Email marketing campaigns",
    "💸 Budget Browsers (Low spend, infrequent)": 
        "• Discount promotions\\n• Re-engagement campaigns\\n• Free shipping offers"
}

print("\\n" + "="*80)
print("SEGMENT-SPECIFIC STRATEGIES")
print("="*80)

for segment, actions in recommendations.items():
    count = (df['segment_name'] == segment).sum()
    pct = count / len(df) * 100
    total_spend = df[df['segment_name'] == segment]['avg_monthly_spend'].sum()
    
    print(f"\\n{segment}")
    print(f"  Size: {count} customers ({pct:.1f}%)")
    print(f"  Total monthly revenue: ${total_spend:,.0f}")
    print(f"  Actions:\\n{actions}")
```

---

## Lab 2: Clustering Algorithm Comparison (70 min)

**Objective:** Compare k-means, hierarchical, and DBSCAN

**Part A: Hierarchical Clustering (25 min)**

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Hierarchical clustering with ward linkage
hc = AgglomerativeClustering(n_clusters=3, linkage='ward')
hc_labels = hc.fit_predict(X_scaled)

df['hc_cluster'] = hc_labels

print(f"Hierarchical cluster sizes: {np.bincount(hc_labels)}")

# Compute linkage matrix for dendrogram
linkage_matrix = linkage(X_scaled, method='ward')

# Plot dendrogram
plt.figure(figsize=(14, 6))
dendrogram(linkage_matrix, 
          truncate_mode='lastp',
          p=30,
          show_leaf_counts=True)
plt.xlabel('Sample Index or (Cluster Size)', fontsize=12)
plt.ylabel('Distance', fontsize=12)
plt.title('Hierarchical Clustering Dendrogram', fontsize=14)
plt.axhline(y=15, color='r', linestyle='--', linewidth=2, label='Cut at k=3')
plt.legend()
plt.tight_layout()
plt.show()

# Compare with k-means
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

ari = adjusted_rand_score(clusters, hc_labels)
nmi = normalized_mutual_info_score(clusters, hc_labels)

print(f"\\nK-Means vs Hierarchical Clustering:")
print(f"  Adjusted Rand Index: {ari:.3f}")
print(f"  Normalized Mutual Info: {nmi:.3f}")
print(f"  (1.0 = perfect agreement, 0 = random)")
```

---

**Part B: DBSCAN (25 min)**

```python
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

# Find optimal eps using k-distance plot
neighbors = NearestNeighbors(n_neighbors=5)
neighbors_fit = neighbors.fit(X_scaled)
distances, indices = neighbors_fit.kneighbors(X_scaled)

# Sort distances
distances = np.sort(distances[:, -1], axis=0)

plt.figure(figsize=(10, 6))
plt.plot(distances)
plt.xlabel('Data Points (sorted by distance)')
plt.ylabel('5-NN Distance')
plt.title('K-Distance Plot (Find Elbow for eps)')
plt.axhline(y=1.5, color='r', linestyle='--', label='Suggested eps=1.5')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Fit DBSCAN
dbscan = DBSCAN(eps=1.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_scaled)

df['dbscan_cluster'] = dbscan_labels

# Analyze results
n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_noise = list(dbscan_labels).count(-1)

print(f"\\nDBSCAN Results:")
print(f"  Number of clusters: {n_clusters}")
print(f"  Number of outliers: {n_noise} ({n_noise/len(df)*100:.1f}%)")

if n_clusters > 0:
    print(f"  Cluster sizes: {np.bincount(dbscan_labels[dbscan_labels >= 0])}")

# Visualize outliers
plt.figure(figsize=(12, 6))
outliers = df[df['dbscan_cluster'] == -1]
inliers = df[df['dbscan_cluster'] != -1]

plt.scatter(inliers['avg_monthly_spend'], inliers['visits_per_month'],
           c=inliers['dbscan_cluster'], cmap='viridis', alpha=0.6, s=100, label='Clusters')
plt.scatter(outliers['avg_monthly_spend'], outliers['visits_per_month'],
           c='red', marker='x', s=100, alpha=0.8, label=f'Outliers (n={n_noise})')

plt.xlabel('Average Monthly Spend ($)')
plt.ylabel('Visits per Month')
plt.title('DBSCAN: Clusters and Outliers')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

**Part C: Algorithm Comparison Summary (20 min)**

```python
# Compare all three algorithms
comparison = pd.DataFrame({
    'Algorithm': ['K-Means', 'Hierarchical', 'DBSCAN'],
    'N_Clusters': [
        len(set(clusters)),
        len(set(hc_labels)),
        n_clusters
    ],
    'Silhouette': [
        silhouette_score(X_scaled, clusters),
        silhouette_score(X_scaled, hc_labels),
        silhouette_score(X_scaled, dbscan_labels[dbscan_labels >= 0]) if n_clusters > 1 else np.nan
    ],
    'N_Outliers': [0, 0, n_noise],
    'Speed': ['Fast', 'Slow', 'Medium']
})

print("\\nAlgorithm Comparison:")
print(comparison.to_string(index=False))

# Visualize agreement matrix
from sklearn.metrics.cluster import contingency_matrix

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# K-Means vs Hierarchical
cm1 = contingency_matrix(clusters, hc_labels)
sns.heatmap(cm1, annot=True, fmt='d', cmap='Blues', ax=axes[0])
axes[0].set_title(f'K-Means vs Hierarchical\\n(ARI={ari:.3f})')
axes[0].set_xlabel('Hierarchical Cluster')
axes[0].set_ylabel('K-Means Cluster')

# K-Means vs DBSCAN (excluding noise)
mask = dbscan_labels != -1
if mask.sum() > 0:
    cm2 = contingency_matrix(clusters[mask], dbscan_labels[mask])
    sns.heatmap(cm2, annot=True, fmt='d', cmap='Greens', ax=axes[1])
    axes[1].set_title('K-Means vs DBSCAN (excl. outliers)')
    axes[1].set_xlabel('DBSCAN Cluster')
    axes[1].set_ylabel('K-Means Cluster')

plt.tight_layout()
plt.show()

print("\\n✅ Recommendation: K-means provides best balance of performance and interpretability")
```

---

## Lab 3: Dimensionality Reduction (60 min)

**Objective:** Visualize high-dimensional data with PCA and t-SNE

**Part A: PCA Analysis (25 min)**

```python
from sklearn.decomposition import PCA

# Fit PCA with all components
pca_full = PCA()
X_pca_full = pca_full.fit_transform(X_scaled)

# Explained variance
explained_var = pca_full.explained_variance_ratio_
cumulative_var = np.cumsum(explained_var)

print("Explained Variance by Component:")
for i, (ev, cv) in enumerate(zip(explained_var, cumulative_var)):
    print(f"  PC{i+1}: {ev:.3f} ({cv:.1%} cumulative)")

# Scree plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].bar(range(1, len(explained_var)+1), explained_var)
axes[0].set_xlabel('Principal Component')
axes[0].set_ylabel('Explained Variance Ratio')
axes[0].set_title('Scree Plot')
axes[0].grid(True, alpha=0.3)

axes[1].plot(range(1, len(cumulative_var)+1), cumulative_var, 'o-', linewidth=2)
axes[1].axhline(y=0.95, color='r', linestyle='--', label='95% threshold')
axes[1].set_xlabel('Number of Components')
axes[1].set_ylabel('Cumulative Explained Variance')
axes[1].set_title('Cumulative Variance Explained')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 2D PCA projection
pca_2d = PCA(n_components=2)
X_pca_2d = pca_2d.fit_transform(X_scaled)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], 
                     c=df['cluster_ordered'], cmap='viridis', alpha=0.6, s=100)
plt.xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]:.1%} variance)')
plt.title(f'PCA Projection ({pca_2d.explained_variance_ratio_.sum():.1%} variance explained)')
plt.colorbar(scatter, label='Cluster')
plt.grid(True, alpha=0.3)
plt.show()

# Feature loadings
loadings = pca_2d.components_.T * np.sqrt(pca_2d.explained_variance_)
loading_df = pd.DataFrame(
    loadings,
    columns=['PC1', 'PC2'],
    index=features
)

print("\\nFeature Loadings (Contribution to PCs):")
print(loading_df.round(3))
```

---

**Part B: t-SNE Visualization (20 min)**

```python
from sklearn.manifold import TSNE

# Fit t-SNE
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=1000)
X_tsne = tsne.fit_transform(X_scaled)

print("t-SNE completed (non-deterministic, for visualization only)")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# t-SNE colored by cluster
scatter1 = axes[0].scatter(X_tsne[:, 0], X_tsne[:, 1],
                          c=df['cluster_ordered'], cmap='viridis', alpha=0.6, s=100)
axes[0].set_xlabel('t-SNE 1')
axes[0].set_ylabel('t-SNE 2')
axes[0].set_title('t-SNE Projection (colored by K-Means cluster)')
plt.colorbar(scatter1, ax=axes[0], label='Cluster')

# t-SNE colored by spend
scatter2 = axes[1].scatter(X_tsne[:, 0], X_tsne[:, 1],
                          c=df['avg_monthly_spend'], cmap='YlOrRd', alpha=0.6, s=100)
axes[1].set_xlabel('t-SNE 1')
axes[1].set_ylabel('t-SNE 2')
axes[1].set_title('t-SNE Projection (colored by Spend)')
plt.colorbar(scatter2, ax=axes[1], label='Avg Monthly Spend ($)')

plt.tight_layout()
plt.show()
```

---

**Part C: PCA vs t-SNE Comparison (15 min)**

```python
# Side-by-side comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# PCA
scatter1 = axes[0].scatter(X_pca_2d[:, 0], X_pca_2d[:, 1],
                          c=df['cluster_ordered'], cmap='viridis', alpha=0.6, s=100)
axes[0].set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]:.1%})')
axes[0].set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]:.1%})')
axes[0].set_title('PCA: Linear, Deterministic, Fast')
axes[0].grid(True, alpha=0.3)

# t-SNE
scatter2 = axes[1].scatter(X_tsne[:, 0], X_tsne[:, 1],
                          c=df['cluster_ordered'], cmap='viridis', alpha=0.6, s=100)
axes[1].set_xlabel('t-SNE 1')
axes[1].set_ylabel('t-SNE 2')
axes[1].set_title('t-SNE: Non-linear, Stochastic, Slow')

plt.suptitle('Dimensionality Reduction Comparison', fontsize=16)
plt.tight_layout()
plt.show()

print("\\nKey Differences:")
print("PCA:")
print("  ✅ Use for: Feature engineering, variance analysis")
print("  ✅ Advantages: Fast, interpretable, deterministic")
print("  ❌ Limitations: Only captures linear relationships")

print("\\nt-SNE:")
print("  ✅ Use for: Visualization only")
print("  ✅ Advantages: Preserves local structure, reveals clusters")
print("  ❌ Limitations: Slow, non-deterministic, can't transform new data")
```

---

**Lab Completion Checklist:**
- ☐ Created customer segmentation with k-means
- ☐ Used elbow method and silhouette score to choose k
- ☐ Profiled and named segments with business labels
- ☐ Compared k-means, hierarchical, and DBSCAN
- ☐ Identified outliers with DBSCAN
- ☐ Performed PCA and interpreted components
- ☐ Visualized clusters with t-SNE
- ☐ Created actionable segment strategies

**Next:** Unit 6 covers deploying models to production!
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

    st.markdown("#### Monitoring and feedback loops")
    st.markdown(
        "Once a model is in use you need to monitor:\n\n"
        "- Data quality – are incoming features still in expected ranges?\n"
        "- Performance – are key metrics stable over time?\n"
        "- Drift – has the relationship between inputs and outcomes changed?\n\n"
        "You also need feedback loops so that new labelled data can be used to **retrain** or update the model on a sensible schedule."
    )

    st.markdown("---")
    st.markdown("#### Production Pipelines")
    st.markdown(
        """**Complete Pipeline saves preprocessing + model together:**

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib

# Create pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier())
])

# Train
pipeline.fit(X_train, y_train)

# Save entire pipeline
joblib.dump(pipeline, 'model_v1.pkl')

# Load and use
loaded = joblib.load('model_v1.pkl')
predictions = loaded.predict(X_new)
```

**Benefits:** Single artifact, no train/prod skew, version control
"""
    )

    st.markdown("---")
    st.markdown("#### 🚀 Deployment Patterns Deep Dive")
    st.markdown(
        """**Pattern 1: Batch Scoring (Offline)**

Best for: Daily reports, marketing campaigns, risk assessments

**Pattern 2: Real-Time API (Online)**  

Best for: Web/mobile apps, instant decisions, fraud detection

**Pattern 3: Interactive Dashboard**

Best for: Internal tools, stakeholder demos, manual reviews

**Pattern 4: Model Monitoring**

Track: Data quality, performance metrics, drift detection

---

**Detailed implementation covered in comprehensive labs below!**
"""
    )

    st.markdown("---")
    st.markdown("#### 📦 Model Versioning Strategy")
    st.markdown(
        """**Why Version Everything:**

Production ML requires tracking:
- Model binary files
- Training data snapshots
- Code/config versions
- Performance baselines

**Semantic Versioning for Models:**

`v<MAJOR>.<MINOR>.<PATCH>`

- **MAJOR:** Breaking changes (new features, different output)
- **MINOR:** Backward-compatible improvements (retraining, tuning)
- **PATCH:** Bug fixes (preprocessing bugs, code fixes)

Example: `churn_model_v2.1.3.pkl`

**Model Metadata Template:**

```python
metadata = {
    # Version info
    'model_version': 'v2.1.3',
    'created_at': '2024-01-15 14:23:00',
    'created_by': 'data-science-team',
    'git_commit': 'a3f2b9c',
    
    # Model architecture
    'model_type': 'RandomForestClassifier',
    'framework': 'scikit-learn',
    'sklearn_version': '1.3.0',
    
    # Training data
    'training_data_path': 's3://bucket/training_data_2024Q1.csv',
    'training_samples': 50000,
    'training_date_range': '2023-01-01 to 2023-12-31',
    'feature_count': 25,
    'target_distribution': {'0': 0.70, '1': 0.30},
    
    # Performance
    'metrics': {
        'train_f1': 0.85,
        'val_f1': 0.78,
        'test_f1': 0.76,
        'roc_auc': 0.83
    },
    
    # Production info
    'deployed_to': 'production',
    'deployment_date': '2024-01-20',
    'monitoring_dashboard': 'https://metrics.company.com/churn-model',
    'retrain_schedule': 'Monthly'
}
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🔍 Data Validation in Production")
    st.markdown(
        """**Input Validation is Critical:**

```python
class ProductionDataValidator:
    def __init__(self, schema_path):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
    
    def validate(self, df):
        errors = []
        warnings = []
        
        # 1. Check columns exist
        missing_cols = set(self.schema['features']) - set(df.columns)
        if missing_cols:
            errors.append(f"Missing columns: {missing_cols}")
        
        # 2. Check data types
        for col in self.schema['features']:
            if col not in df.columns:
                continue
                
            expected_type = self.schema['types'][col]
            actual_type = str(df[col].dtype)
            
            if 'int' in expected_type and 'int' not in actual_type:
                errors.append(f"{col}: expected int, got {actual_type}")
        
        # 3. Check value ranges
        for col, bounds in self.schema.get('bounds', {}).items():
            if col in df.columns:
                if df[col].min() < bounds['min']:
                    warnings.append(f"{col} has values below min ({bounds['min']})")
                if df[col].max() > bounds['max']:
                    warnings.append(f"{col} has values above max ({bounds['max']})")
        
        # 4. Check for excessive nulls
        null_rates = df.isnull().mean()
        high_null = null_rates[null_rates > self.schema.get('max_null_rate', 0.5)]
        if len(high_null) > 0:
            warnings.append(f"High null rates in: {list(high_null.index)}")
        
        # 5. Check for duplicates
        if df.duplicated().sum() > 0:
            warnings.append(f"{df.duplicated().sum()} duplicate rows found")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

# Usage
validator = ProductionDataValidator('schema.json')
result = validator.validate(new_data)

if not result['valid']:
    raise ValueError(f"Validation failed: {result['errors']}")

if result['warnings']:
    logging.warning(f"Validation warnings: {result['warnings']}")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 📈 Monitoring Dashboards")
    st.markdown(
        """**Key Metrics to Track:**

**1. Model Performance Over Time**
- F1, Precision, Recall, AUC (weekly)
- Threshold for alerts: <10% drop

**2. Prediction Volume**
- Predictions per day/hour
- Detect anomalies (>50% drop)

**3. Latency (for APIs)**
- p50, p95, p99 response times
- Target: <100ms for most requests

**4. Error Rates**
- % of requests that fail
- Target: <1% error rate

**5. Data Quality**
- Missing value rates
- Out-of-range features
- Suspicious patterns

**Example Monitoring Query (SQL):**

```sql
SELECT 
    DATE_TRUNC('day', scored_at) as date,
    COUNT(*) as predictions,
    AVG(CASE WHEN actual IS NOT NULL 
        THEN CASE WHEN prediction = actual THEN 1.0 ELSE 0.0 END 
        END) as accuracy,
    AVG(probability) as avg_probability,
    SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as predicted_churns
FROM predictions_log
WHERE scored_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1 DESC;
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🔄 Automated Retraining")
    st.markdown(
        """**Retraining Triggers:**

1. **Time-based:** Every 30/90 days
2. **Performance-based:** F1 < 0.70
3. **Data-based:** >5% feature drift
4. **Business-based:** New product launch

**Retraining Pipeline:**

```python
class AutomatedRetrainingPipeline:
    def __init__(self, config):
        self.config = config
        self.current_model = joblib.load(config['current_model_path'])
    
    def check_triggers(self):
        # Check performance trigger
        recent_perf = self.get_recent_performance()
        if recent_perf['f1'] < self.config['min_f1']:
            return True, "Performance degraded"
        
        # Check drift trigger  
        drift_score = self.calculate_drift()
        if drift_score > self.config['max_drift']:
            return True, "Significant drift detected"
        
        # Check time trigger
        days_since_train = (datetime.now() - self.get_last_train_date()).days
        if days_since_train > self.config['max_days']:
            return True, "Scheduled retrain"
        
        return False, None
    
    def retrain_and_evaluate(self, new_data):
        # Load new data
        X, y = self.load_data(new_data)
        
        # Split
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
        
        # Retrain
        new_model = self.create_pipeline()
        new_model.fit(X_train, y_train)
        
        # Evaluate
        new_f1 = f1_score(y_val, new_model.predict(X_val))
        current_f1 = f1_score(y_val, self.current_model.predict(X_val))
        
        # Only deploy if improved
        if new_f1 >= current_f1 * 0.95:
            self.deploy_model(new_model, new_f1)
            self.notify_team(f"✅ Model retrained: F1={new_f1:.3f}")
            return True
        else:
            self.notify_team(f"❌ Retrain unsuccessful: new F1={new_f1:.3f}, current F1={current_f1:.3f}")
            return False
```
"""
    )

    st.markdown("---")
    st.markdown("#### ⚡ A/B Testing Models")
    st.markdown(
        """**Gradual Rollout Strategy:**

```python
import random

def predict_with_ab_test(features, model_a, model_b, traffic_split=0.9):
    # 90% traffic to model A (current), 10% to model B (new)
    if random.random() < traffic_split:
        prediction = model_a.predict([features])[0]
        model_version = "v1.2.3"
    else:
        prediction = model_b.predict([features])[0]
        model_version = "v1.3.0"
    
    # Log for analysis
    log_prediction(features, prediction, model_version)
    
    return prediction

# After 1 week, analyze results
def analyze_ab_test():
    df = pd.read_sql(\"\"\"
        SELECT 
            model_version,
            COUNT(*) as predictions,
            AVG(CASE WHEN actual = prediction THEN 1.0 ELSE 0.0 END) as accuracy,
            AVG(response_time_ms) as avg_latency
        FROM prediction_log
        WHERE created_at >= NOW() - INTERVAL '7 days'
        GROUP BY 1
    \"\"\")
    
    print(df)
    
    # If B is better, increase traffic
    if df[df['model_version']=='v1.3.0']['accuracy'].values[0] > \\
       df[df['model_version']=='v1.2.3']['accuracy'].values[0]:
        print("✅ New model performing better - increasing traffic to 50%")
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🛡️ Production Best Practices")
    st.markdown(
        """**Checklist for Production Deployment:**

**Pre-Deployment:**
- ☐ Model validated on hold-out test set
- ☐ Pipeline saved with all preprocessing
- ☐ Metadata documented
- ☐ Input validation implemented
- ☐ Tested on production-like data
- ☐ Performance baseline established
- ☐ Monitoring dashboard created
- ☐ Alerting configured
- ☐ Rollback plan documented
- ☐ Stakeholders notified

**Deployment:**
- ☐ Deploy to staging first
- ☐ Run integration tests
- ☐ Start with 5-10% traffic
- ☐ Monitor for 24 hours
- ☐ Gradually increase to 100%
- ☐ Keep previous version ready

**Post-Deployment:**
- ☐ Monitor performance daily (week 1)
- ☐ Review data quality metrics
- ☐ Check for drift weekly
- ☐ Collect user feedback
- ☐ Schedule retraining
- ☐ Document lessons learned

**Error Handling:**

```python
def safe_predict(pipeline, features):
    try:
        # Validate input
        if not isinstance(features, pd.DataFrame):
            raise ValueError("Input must be DataFrame")
        
        # Check schema
        expected_cols = pipeline.feature_names_in_
        if not all(col in features.columns for col in expected_cols):
            raise ValueError("Missing required features")
        
        # Make prediction
        prediction = pipeline.predict(features)
        probability = pipeline.predict_proba(features)
        
        return {
            'success': True,
            'prediction': int(prediction[0]),
            'probability': float(probability[0, 1])
        }
    
    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        
        return {
            'success': False,
            'error': str(e),
            'fallback_prediction': 0  # Safe default
        }
```
"""
    )

    st.markdown("---")
    st.markdown("#### 🎯 Interview Questions")
    st.markdown(
        """**Q1: What's the difference between batch and online serving?**

**Answer:**
- **Batch:** Predictions generated offline, stored, retrieved later. Good for reports, emails. Latency: hours-days.
- **Online:** Predictions generated on-demand via API. Good for web apps. Latency: milliseconds.

---

**Q2: How do you handle model versioning?**

**Answer:**
Use semantic versioning (MAJOR.MINOR.PATCH). Save:
- Model binary with version in filename
- Metadata JSON with training date, metrics, features
- Git commit hash for reproducibility
- Keep last 3 versions for rollback

---

**Q3: What causes model performance to degrade over time?**

**Answer:**
- **Data drift:** Feature distributions change
- **Concept drift:** Relationship between X and y changes
- **Schema drift:** New features added/removed
- **Label drift:** Definition of target changes

---

**Q4: How do you monitor a production model?**

**Answer:**
Track:
1. **Performance:** F1, AUC (compare to baseline)
2. **Data quality:** Null rates, outliers
3. **Predictions:** Volume, distribution
4. **System:** Latency, errors, throughput

Alert when >10% degradation.
"""
    )

    st.markdown("---")
    st.markdown("#### 📚 Key Takeaways")
    st.markdown(
        """**Production ML is Different:**
- Models are long-lived (months/years)
- Data changes over time
- Performance must be monitored
- Automation is essential

**Critical Success Factors:**
1. **Pipelines:** Prevent train/serve skew
2. **Versioning:** Enable rollback
3. **Monitoring:** Detect issues early
4. **Automation:** Reduce manual work
5. **Validation:** Catch bad data
6. **Documentation:** Support handoffs

**Deployment Checklist:**
- ✅ Save pipeline (not just model)
- ✅ Version everything
- ✅ Validate inputs
- ✅ Monitor performance
- ✅ Log predictions
- ✅ Plan for retraining
- ✅ Enable rollback
- ✅ A/B test changes

**Next:** Complete hands-on deployment labs!
"""
    )


def _render_unit6_labs():
    """Labs and mini-project ideas for Unit 6."""

    st.markdown("### 🧪 HANDS-ON LABS: Unit 6 Model Deployment")
    st.markdown("**Complete these 3 labs to master deployment:**")
    
    st.markdown("---")
    st.markdown("## Lab 1: Production Pipeline & Batch Scoring (90 min)")
    st.markdown("**Objective:** Save models and create automated batch scoring")
    st.code('''# Example: Save a trained model
import joblib
joblib.dump(model, "model.pkl")

# Load and use it
model = joblib.load("model.pkl")
predictions = model.predict(new_data)
''', language='python')
    
    st.markdown("---")
    st.markdown("## Lab 2: Interactive Prediction App (80 min)")
    st.markdown("**Objective:** Build Streamlit app for model predictions")
    st.code('''import streamlit as st
import joblib

model = joblib.load("model.pkl")

st.title("Prediction App")
user_input = st.number_input("Enter value")

if st.button("Predict"):
    prediction = model.predict([[user_input]])
    st.write(f"Prediction: {prediction[0]}")
''', language='python')
    
    st.markdown("---")
    st.markdown("## Lab 3: API Deployment (75 min)")
    st.markdown("**Objective:** Deploy model as REST API")
    st.code('''from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load("model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    prediction = model.predict([data["features"]])
    return jsonify({"prediction": prediction[0]})

if __name__ == "__main__":
    app.run(debug=True)
''', language='python')


def _render_unit6_quiz():
    """Quick-check quiz for Unit 6."""
    
    st.markdown("### ✅ Quick-check quiz – Unit 6")
    st.markdown("Test your understanding of model deployment concepts.")
    
    q1 = st.radio(
        "1. What is the main purpose of model versioning?",
        [
            "A) To make models run faster",
            "B) To track changes and enable rollback",
            "C) To reduce model size",
            "D) To improve accuracy"
        ],
        key="pathway2_u6_q1"
    )
    
    q2 = st.radio(
        "2. What does A/B testing in ML deployment mean?",
        [
            "A) Testing two different datasets",
            "B) Comparing two model versions with live traffic",
            "C) Testing model accuracy twice",
            "D) Using two different algorithms"
        ],
        key="pathway2_u6_q2"
    )
    
    q3 = st.radio(
        "3) What should you monitor in production ML systems?",
        [
            "A) Only model accuracy",
            "B) Only system latency",
            "C) Model performance, data drift, and system metrics",
            "D) Only error rates"
        ],
        key="pathway2_u6_q3"
    )
    
    if st.button("Submit Quiz", key="pathway2_u6_submit"):
        score = 0
        if "B)" in q1:
            score += 1
        if "B)" in q2:
            score += 1
        if "C)" in q3:
            score += 1
        
        st.write(f"### Score: {score}/3")
        if score == 3:
            st.success("Perfect! You understand deployment concepts well.")
            st.balloons()
        elif score >= 2:
            st.info("Good job! Review the materials for the questions you missed.")
        else:
            st.warning("Keep studying! Deployment is crucial for production ML.")


def _render_unit7_learning_materials():
    """Content for Unit 7: Pathway 2 Capstone Project."""
    
    st.markdown("### Unit 7: Pathway 2 Capstone Project")
    st.markdown(
        """**Build an end-to-end ML project** demonstrating all skills from Pathway 2.

**Project Requirements:**

1. **Problem Definition**
   - Clear ML objective (regression or classification)
   - Success metrics defined
   - Dataset selected

2. **Feature Engineering**
   - Create meaningful features
   - Handle missing data
   - Feature selection

3. **Model Development**
   - Try multiple algorithms
   - Hyperparameter tuning
   - Cross-validation

4. **Evaluation**
   - Comprehensive metrics
   - Validation strategy
   - Model comparison

5. **Documentation**
   - Jupyter notebook with analysis
   - README with instructions
   - Results summary
"""
    )
    
    st.markdown("#### 🎯 Suggested Projects")
    st.markdown(
        """**Choose one:**

1. **House Price Prediction**
   - Regression problem
   - Feature engineering from property data
   - Compare linear, tree-based, and ensemble models

2. **Customer Churn Prediction**
   - Binary classification
   - Handle class imbalance
   - Feature importance analysis

3. **Credit Risk Assessment**
   - Classification with cost-sensitive learning
   - Interpretable models required
   - Regulatory considerations

4. **Sales Forecasting**
   - Time-series regression
   - Seasonal patterns
   - Multiple product categories

5. **Customer Segmentation**
   - Unsupervised learning
   - K-means and hierarchical clustering
   - Business insights from segments
"""
    )
    
    st.markdown("#### 📋 Deliverables")
    st.markdown(
        """**Submit:**

1. **Jupyter Notebook**
   - Complete analysis workflow
   - Well-documented code
   - Visualizations
   - Results interpretation

2. **README.md**
   - Problem description
   - Dataset information
   - How to run the code
   - Results summary

3. **requirements.txt**
   - All dependencies listed
   - Version numbers included

4. **Presentation (optional)**
   - 5-10 slides
   - Problem, approach, results
   - Business impact
"""
    )
    
    st.markdown("#### 🏆 Evaluation Criteria")
    st.markdown(
        """**Graded on:**

- **Technical Quality (40%)**
  - Model performance
  - Proper validation
  - Code quality

- **Feature Engineering (20%)**
  - Creative features
  - Proper handling of data
  - Feature selection

- **Analysis & Insights (20%)**
  - Clear interpretation
  - Business relevance
  - Actionable recommendations

- **Documentation (20%)**
  - Clear explanations
  - Reproducible code
  - Professional presentation
"""
    )
    
    st.success("✅ Ready to build your Pathway 2 capstone!")


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
