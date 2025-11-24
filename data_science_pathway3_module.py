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

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS")
        
        st.markdown("## Lab 1: Production Feature Pipeline (90 min)")
        st.markdown(
            """**Objective:** Build reusable feature pipeline that prevents train/serve skew

**Part A: Create Reusable Feature Transformer**
```python
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class RFMFeatureTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, as_of_date=None):
        self.as_of_date = as_of_date or pd.Timestamp.now()
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, customer_orders_df):
        valid_orders = customer_orders_df[
            customer_orders_df['order_date'] <= self.as_of_date
        ]
        
        rfm = valid_orders.groupby('customer_id').agg({
            'order_date': lambda x: (self.as_of_date - x.max()).days,
            'order_id': 'count',
            'order_amount': 'sum'
        }).reset_index()
        
        rfm.columns = ['customer_id', 'recency_days', 'frequency', 'monetary']
        return rfm
```

**Part B: Verify No Train/Serve Skew**
```python
# Training features (Jan 1)
train_date = pd.Timestamp('2024-01-01')
train_transformer = RFMFeatureTransformer(as_of_date=train_date)
train_features = train_transformer.fit_transform(orders)

# Serving features (March 15)  
serve_date = pd.Timestamp('2024-03-15')
serve_transformer = RFMFeatureTransformer(as_of_date=serve_date)
serve_features = serve_transformer.fit_transform(orders)

# ✅ Same code = No skew!
```

**Part C: Integration Tests**
```python
import unittest

class TestRFMFeatures(unittest.TestCase):
    def test_point_in_time_correctness(self):
        as_of = pd.Timestamp('2023-01-10')
        transformer = RFMFeatureTransformer(as_of_date=as_of)
        features = transformer.fit_transform(orders)
        # Assert no future orders included
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestRFMFeatures)
unittest.TextTestRunner(verbosity=2).run(suite)
```

**Completion Checklist:**
- ☐ Created reusable transformer
- ☐ Implemented point-in-time correctness
- ☐ Same code for train/serve
- ☐ Wrote unit tests
"""
        )

        st.markdown("---")
        st.markdown("## Lab 2: Late-Arriving Data Handling (75 min)")
        st.markdown(
            """**Objective:** Handle delayed data arrivals and backfills

**Part A: Simulate Late Confirmations (25 min)**
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simulate payment confirmations arriving late
np.random.seed(42)
n_txns = 500

transactions = pd.DataFrame({
    'txn_id': range(n_txns),
    'customer_id': np.random.randint(1, 100, n_txns),
    'txn_date': pd.date_range('2024-01-01', periods=n_txns, freq='H'),
    'amount': np.random.gamma(2, 50, n_txns),
    'status': 'pending'
})

# Add confirmation delays (0-72 hours)
transactions['delay_hours'] = np.random.choice(
    [0, 24, 48, 72], 
    size=n_txns,
    p=[0.6, 0.2, 0.15, 0.05]
)

transactions['confirmation_date'] = transactions['txn_date'] + pd.to_timedelta(
    transactions['delay_hours'], unit='h'
)

print("Late Data Distribution:")
print(transactions['delay_hours'].value_counts().sort_index())
print(f"\\nLate arrivals: {(transactions['delay_hours'] > 0).mean():.1%}")
```

**Part B: Time-Aware Feature Computation (25 min)**
```python
def compute_features_as_of(txns_df, as_of_date, lookback_days=7):
    \"\"\"
    Compute features using ONLY data confirmed by as_of_date.
    This prevents future data leakage.
    \"\"\"
    # Filter to confirmed transactions
    confirmed = txns_df[txns_df['confirmation_date'] <= as_of_date].copy()
    
    # Lookback window
    window_start = as_of_date - timedelta(days=lookback_days)
    windowed = confirmed[confirmed['txn_date'] >= window_start]
    
    # Aggregate by customer
    features = windowed.groupby('customer_id').agg({
        'txn_id': 'count',
        'amount': ['sum', 'mean', 'std']
    }).reset_index()
    
    features.columns = ['customer_id', 'txn_count_7d', 'txn_sum_7d', 
                        'txn_avg_7d', 'txn_std_7d']
    features = features.fillna(0)
    
    return features

# Compare features at different dates
dates = pd.date_range('2024-01-08', '2024-01-11', freq='D')

for date in dates:
    feats = compute_features_as_of(transactions, as_of_date=date)
    print(f"\\n{date.date()}: {len(feats)} customers, avg txn count: {feats['txn_count_7d'].mean():.1f}")
    
# Key insight: Features change as late data arrives!
```

**Part C: Backfill Strategy (25 min)**
```python
class SimpleFeatureStore:
    \"\"\"Feature store that handles backfills\"\"\"
    
    def __init__(self):
        self.features = []
        
    def write_features(self, features_df, as_of_date, version):
        features_df = features_df.copy()
        features_df['as_of_date'] = as_of_date
        features_df['version'] = version
        features_df['computed_at'] = datetime.now()
        self.features.append(features_df)
        
    def read_features(self, as_of_date):
        if not self.features:
            return pd.DataFrame()
        
        all_feats = pd.concat(self.features)
        relevant = all_feats[all_feats['as_of_date'] == as_of_date]
        
        # Get latest version for each customer
        latest = relevant.sort_values('version').groupby('customer_id').tail(1)
        return latest
    
    def backfill(self, txns_df, dates_to_backfill):
        print(f"Backfilling {len(dates_to_backfill)} dates...")
        for date in dates_to_backfill:
            feats = compute_features_as_of(txns_df, as_of_date=date)
            version = len([f for f in self.features 
                          if f['as_of_date'].iloc[0] == date]) + 1
            self.write_features(feats, as_of_date=date, version=version)
            print(f"  ✅ {date.date()} (v{version})")

# Usage
store = SimpleFeatureStore()

# Initial computation
initial_date = pd.Timestamp('2024-01-10')
feats = compute_features_as_of(transactions, as_of_date=initial_date)
store.write_features(feats, as_of_date=initial_date, version=1)

# Later: backfill when late data arrives
backfill_dates = pd.date_range('2024-01-08', '2024-01-09', freq='D')
store.backfill(transactions, backfill_dates)

print(f"\\n✅ Feature store now has {len(store.features)} snapshots")
```

**Lab 2 Completion Checklist:**
- ☐ Simulated late-arriving data
- ☐ Implemented point-in-time feature computation
- ☐ Built simple feature store
- ☐ Tested backfill strategy
- ☐ Verified no data leakage
"""
        )

        st.markdown("---")
        st.markdown("## Lab 3: Feature Store Implementation (90 min)")
        st.markdown(
            """**Objective:** Build simplified feature store with versioning

**Part A: Feature Registry (30 min)**
```python
import json
from datetime import datetime

class FeatureRegistry:
    \"\"\"Track feature definitions and lineage\"\"\"
    
    def __init__(self):
        self.features = {}
        
    def register_feature(self, name, definition, owner, source_tables, dependencies=None):
        self.features[name] = {
            'name': name,
            'definition': definition,
            'owner': owner,
            'source_tables': source_tables,
            'dependencies': dependencies or [],
            'created_at': datetime.now().isoformat(),
            'version': 1
        }
        
    def get_feature(self, name):
        return self.features.get(name)
    
    def list_features(self):
        return list(self.features.keys())
    
    def get_lineage(self, name):
        \"\"\"Get full dependency tree for a feature\"\"\"
        feature = self.features.get(name)
        if not feature:
            return None
            
        lineage = {
            'feature': name,
            'source_tables': feature['source_tables'],
            'dependencies': feature['dependencies']
        }
        return lineage

# Usage
registry = FeatureRegistry()

registry.register_feature(
    name='customer_rfm_score',
    definition='RFM (Recency, Frequency, Monetary) score for customer segmentation',
    owner='data-science-team',
    source_tables=['orders', 'customers'],
    dependencies=['recency_days', 'frequency_count', 'monetary_value']
)

registry.register_feature(
    name='recency_days',
    definition='Days since last order',
    owner='data-science-team',
    source_tables=['orders']
)

print("Registered features:", registry.list_features())
print("\\nLineage for customer_rfm_score:")
print(json.dumps(registry.get_lineage('customer_rfm_score'), indent=2))
```

**Part B: Offline + Online Stores (30 min)**
```python
import pandas as pd

class FeatureStore:
    \"\"\"Simplified feature store with offline/online storage\"\"\"
    
    def __init__(self):
        self.offline_store = {}  # In production: Parquet files on S3
        self.online_store = {}   # In production: Redis/DynamoDB
        self.registry = FeatureRegistry()
        
    def write_offline(self, feature_name, features_df, as_of_date):
        \"\"\"Write to offline store (training data)\"\"\"
        key = f"{feature_name}_{as_of_date.date()}"
        self.offline_store[key] = features_df.copy()
        print(f"✅ Wrote {len(features_df)} rows to offline store: {key}")
        
    def write_online(self, feature_name, features_df):
        \"\"\"Write to online store (serving, latest values only)\"\"\"
        self.online_store[feature_name] = features_df.set_index('customer_id').to_dict('index')
        print(f"✅ Wrote {len(features_df)} rows to online store: {feature_name}")
        
    def read_offline(self, feature_name, as_of_date):
        \"\"\"Read from offline store for training\"\"\"
        key = f"{feature_name}_{as_of_date.date()}"
        return self.offline_store.get(key, pd.DataFrame())
        
    def read_online(self, feature_name, customer_ids):
        \"\"\"Read from online store for real-time serving\"\"\"
        store_data = self.online_store.get(feature_name, {})
        results = []
        for cust_id in customer_ids:
            if cust_id in store_data:
                row = {'customer_id': cust_id}
                row.update(store_data[cust_id])
                results.append(row)
        return pd.DataFrame(results)

# Usage example
store = FeatureStore()

# Compute features
from sklearn.base import BaseEstimator, TransformerMixin

class RFMTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, as_of_date):
        self.as_of_date = as_of_date
    def fit(self, X, y=None):
        return self
    def transform(self, df):
        return df.groupby('customer_id').agg({
            'order_date': lambda x: (self.as_of_date - x.max()).days,
            'order_id': 'count',
            'amount': 'sum'
        }).reset_index()

# Sample data
orders = pd.DataFrame({
    'customer_id': [1,1,2,2,3],
    'order_id': [1,2,3,4,5],
    'order_date': pd.to_datetime(['2024-01-01', '2024-01-15', 
                                   '2024-01-10', '2024-01-20', '2024-01-05']),
    'amount': [100, 150, 200, 250, 75]
})

# Write offline (for training)
as_of = pd.Timestamp('2024-01-20')
transformer = RFMTransformer(as_of_date=as_of)
features = transformer.transform(orders)
features.columns = ['customer_id', 'recency', 'frequency', 'monetary']
store.write_offline('rfm_features', features, as_of_date=as_of)

# Write online (for serving)
store.write_online('rfm_features', features)

# Read online (low latency)
online_features = store.read_online('rfm_features', customer_ids=[1, 2])
print("\\nOnline features for customers 1 & 2:")
print(online_features)
```

**Part C: Feature Monitoring (30 min)**
```python
class FeatureMonitor:
    \"\"\"Monitor feature quality and drift\"\"\"
    
    def __init__(self):
        self.baselines = {}
        self.alerts = []
        
    def set_baseline(self, feature_name, features_df):
        \"\"\"Set baseline statistics for monitoring\"\"\"
        self.baselines[feature_name] = {
            'mean': features_df.select_dtypes(include='number').mean().to_dict(),
            'std': features_df.select_dtypes(include='number').std().to_dict(),
            'null_rate': features_df.isnull().mean().to_dict(),
            'row_count': len(features_df)
        }
        
    def check_drift(self, feature_name, current_df, threshold=2.0):
        \"\"\"Check if features have drifted beyond threshold std devs\"\"\"
        if feature_name not in self.baselines:
            return []
            
        baseline = self.baselines[feature_name]
        alerts = []
        
        # Check mean drift
        for col in current_df.select_dtypes(include='number').columns:
            if col in baseline['mean']:
                current_mean = current_df[col].mean()
                baseline_mean = baseline['mean'][col]
                baseline_std = baseline['std'][col]
                
                if baseline_std > 0:
                    z_score = abs(current_mean - baseline_mean) / baseline_std
                    if z_score > threshold:
                        alerts.append(f"⚠️ {col}: mean drift ({z_score:.1f} std devs)")
        
        # Check null rate increase
        current_nulls = current_df.isnull().mean()
        for col in current_nulls.index:
            if col in baseline['null_rate']:
                if current_nulls[col] > baseline['null_rate'][col] * 1.5:
                    alerts.append(f"⚠️ {col}: null rate increased")
        
        return alerts

# Usage
monitor = FeatureMonitor()

# Set baseline
monitor.set_baseline('rfm_features', features)

# Simulate drift
drifted_features = features.copy()
drifted_features['monetary'] = drifted_features['monetary'] * 2  # Artificial drift

# Check
alerts = monitor.check_drift('rfm_features', drifted_features, threshold=1.5)
for alert in alerts:
    print(alert)
    
if not alerts:
    print("✅ No drift detected")
else:
    print(f"\\n🚨 {len(alerts)} alerts triggered!")
```

**Lab 3 Completion Checklist:**
- ☐ Built feature registry with lineage tracking
- ☐ Implemented offline store (training)
- ☐ Implemented online store (serving)
- ☐ Created feature monitoring system
- ☐ Tested drift detection
- ☐ Portfolio-ready feature store mini-project
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

        st.markdown("####  Reproducibility and audit trails")
        st.markdown(
            """You will discuss how experiment tracking supports
**reproducibility** and governance:

- Being able to re-run a training job months later.
- Answering "which model version made this prediction?".
- Supporting compliance requirements in regulated environments.
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS")
        
        st.markdown("## Lab 1: MLflow Experiment Tracking (90 min)")
        st.markdown(
            """**Objective:** Track experiments systematically with MLflow

**Part A: Setup MLflow**
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("churn_prediction")

# Log experiment
with mlflow.start_run(run_name="rf_baseline"):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    mlflow.log_params({"n_estimators": 100, "max_depth": None})
    mlflow.log_metric("f1_score", 0.82)
    mlflow.sklearn.log_model(model, "model")
```

**Part B: Compare Multiple Runs**  
**Part C: Model Registry**

- ☐ Tracked 5+ experiments
- ☐ Logged params, metrics, artifacts
- ☐ Compared runs in UI
"""
        )

        st.markdown("---")
        st.markdown("## Lab 2: Cross-Validation with Logging (75 min)")
        st.markdown(
            """**Objective:** Fair model comparison using CV

**Part A: k-Fold CV with MLflow Logging (25 min)**
```python
import mlflow
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Generate sample data
X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, random_state=42)

mlflow.set_experiment("cross_validation_comparison")

models = {
    'rf_50': RandomForestClassifier(n_estimators=50, random_state=42),
    'rf_100': RandomForestClassifier(n_estimators=100, random_state=42),
    'rf_200': RandomForestClassifier(n_estimators=200, random_state=42)
}

kf = KFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    with mlflow.start_run(run_name=name):
        # Perform CV
        cv_scores = cross_val_score(model, X, y, cv=kf, scoring='f1')
        
        # Log each fold
        for fold, score in enumerate(cv_scores, 1):
            mlflow.log_metric(f"fold_{fold}_f1", score)
        
        # Log aggregated metrics
        mlflow.log_metric("mean_cv_f1", cv_scores.mean())
        mlflow.log_metric("std_cv_f1", cv_scores.std())
        mlflow.log_param("n_estimators", model.n_estimators)
        mlflow.log_param("cv_folds", 5)
        
        print(f"{name}: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
```

**Part B: Nested CV (25 min)**
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None]
}

# Outer CV for evaluation
outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)

# Inner CV for hyperparameter tuning
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)

outer_scores = []

for train_idx, test_idx in outer_cv.split(X):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    # Inner loop: find best hyperparameters
    grid = GridSearchCV(RandomForestClassifier(random_state=42),
                       param_grid, cv=inner_cv, scoring='f1')
    grid.fit(X_train, y_train)
    
    # Outer loop: evaluate with best params
    score = grid.score(X_test, y_test)
    outer_scores.append(score)

print(f"\nNested CV F1: {np.mean(outer_scores):.3f} ± {np.std(outer_scores):.3f}")
print("✅ Unbiased estimate (no data leakage)")
```

**Part C: Statistical Significance Testing (25 min)**
```python
from scipy.stats import ttest_rel

# Compare two models statistically
model_a_scores = cross_val_score(models['rf_50'], X, y, cv=kf, scoring='f1')
model_b_scores = cross_val_score(models['rf_200'], X, y, cv=kf, scoring='f1')

t_stat, p_value = ttest_rel(model_a_scores, model_b_scores)

print(f"Model A (RF-50): {model_a_scores.mean():.3f}")
print(f"Model B (RF-200): {model_b_scores.mean():.3f}")
print(f"\nt-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("\n✅ Statistically significant difference")
else:
    print("\n❌ No significant difference")

# Completion checklist
print("\n- ☐ Performed 5-fold CV with logging")
print("- ☐ Implemented nested CV")
print("- ☐ Statistical significance test")
```
"""
        )

        st.markdown("---")
        st.markdown("## Lab 3: Automated Model Selection Pipeline (90 min)")
        st.markdown(
            """**Objective:** Build automated model comparison system

**Part A: Define Model Zoo (30 min)**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

model_zoo = {
    'logistic': LogisticRegression(max_iter=1000, random_state=42),
    'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'svm': SVC(probability=True, random_state=42),
    'xgboost': XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss'),
    'lightgbm': LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
}

print(f"Model zoo contains {len(model_zoo)} models")
```

**Part B: Automated Training + Logging (30 min)**
```python
import mlflow
import time
from sklearn.model_selection import cross_val_score

mlflow.set_experiment("automated_model_selection")

results = []

for name, model in model_zoo.items():
    print(f"\nTraining {name}...")
    start_time = time.time()
    
    with mlflow.start_run(run_name=name):
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='f1')
        
        # Log metrics
        mean_f1 = cv_scores.mean()
        std_f1 = cv_scores.std()
        training_time = time.time() - start_time
        
        mlflow.log_metric("mean_f1", mean_f1)
        mlflow.log_metric("std_f1", std_f1)
        mlflow.log_metric("training_time_sec", training_time)
        mlflow.log_param("model_type", name)
        
        # Train on full data and save
        model.fit(X, y)
        mlflow.sklearn.log_model(model, "model")
        
        results.append({
            'model': name,
            'mean_f1': mean_f1,
            'std_f1': std_f1,
            'time': training_time
        })
        
        print(f"  F1: {mean_f1:.3f} ± {std_f1:.3f} ({training_time:.1f}s)")
```

**Part C: Select Best Model (30 min)**
```python
import pandas as pd

# Compare models
results_df = pd.DataFrame(results).sort_values('mean_f1', ascending=False)

print("\n" + "="*60)
print("MODEL COMPARISON RESULTS")
print("="*60)
print(results_df.to_string(index=False))

# Statistical selection with confidence intervals
best_model_name = results_df.iloc[0]['model']
best_f1 = results_df.iloc[0]['mean_f1']
std = results_df.iloc[0]['std_f1']

# 95% confidence interval
from scipy.stats import t
ci = t.interval(0.95, df=4, loc=best_f1, scale=std/np.sqrt(5))

print(f"\n" + "="*60)
print("SELECTED MODEL")
print("="*60)
print(f"Model: {best_model_name}")
print(f"F1 Score: {best_f1:.3f} ± {std:.3f}")
print(f"95% CI: [{ci[0]:.3f}, {ci[1]:.3f}]")

# Check if significantly better than second best
if len(results_df) > 1:
    second_f1 = results_df.iloc[1]['mean_f1']
    if best_f1 - std > second_f1:
        print("\n✅ Clear winner (statistically better)")
    else:
        print("\n⚠️ Close race - consider both models")

print("\n- ☐ Compared 6 models")
print("- ☐ Logged all experiments")
print("- ☐ Selected best with CI")
print("- ☐ Production model identified")
```
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

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS")
        
        st.markdown("## Lab 1: Gradient Boosting Mastery (90 min)")
        st.markdown(
            """**Objective:** Master XGBoost, LightGBM, CatBoost

**Part A: XGBoost vs LightGBM**
```python
import xgboost as xgb
import lightgbm as lgb

# XGBoost
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6
)
xgb_model.fit(X_train, y_train)

# LightGBM (faster on large datasets)
lgb_model = lgb.LGBMClassifier(
    n_estimators=100,
    learning_rate=0.1,
    num_leaves=31
)
lgb_model.fit(X_train, y_train)
```

**Part B:** Hyperparameter tuning with Optuna  
**Part C:** Feature importance analysis

- ☐ Compared 3 boosting libraries
- ☐ Tuned hyperparameters
- ☐ Analyzed SHAP values
"""
        )

        st.markdown("---")
        st.markdown("## Lab 2: Ensemble Methods (75 min)")
        st.markdown(
            """**Objective:** Build stacking and blending ensembles

**Part A: Voting Classifier (25 min)**
```python
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Base models
lr = LogisticRegression(random_state=42)
dt = DecisionTreeClassifier(random_state=42)
rf = RandomForestClassifier(n_estimators=50, random_state=42)

# Hard voting
voting_hard = VotingClassifier(
    estimators=[('lr', lr), ('dt', dt), ('rf', rf)],
    voting='hard'
)

# Soft voting (uses probabilities)
voting_soft = VotingClassifier(
    estimators=[('lr', lr), ('dt', dt), ('rf', rf)],
    voting='soft'
)

# Compare
print("Individual models:")
for name, model in [('Logistic', lr), ('Tree', dt), ('Forest', rf)]:
    score = cross_val_score(model, X, y, cv=5, scoring='f1').mean()
    print(f"  {name}: {score:.3f}")

print("\nEnsembles:")
hard_score = cross_val_score(voting_hard, X, y, cv=5, scoring='f1').mean()
soft_score = cross_val_score(voting_soft, X, y, cv=5, scoring='f1').mean()
print(f"  Hard Voting: {hard_score:.3f}")
print(f"  Soft Voting: {soft_score:.3f}")
```

**Part B: Stacking with Meta-Learner (25 min)**
```python
from sklearn.ensemble import StackingClassifier

# Base models (level 0)
base_models = [
    ('rf', RandomForestClassifier(n_estimators=50, random_state=42)),
    ('xgb', xgb.XGBClassifier(n_estimators=50, random_state=42)),
    ('lgb', lgb.LGBMClassifier(n_estimators=50, random_state=42, verbose=-1))
]

# Meta-model (level 1)
meta_model = LogisticRegression()

# Stacking ensemble
stacking = StackingClassifier(
    estimators=base_models,
    final_estimator=meta_model,
    cv=5
)

# Train and evaluate
stacking.fit(X_train, y_train)
stack_score = stacking.score(X_test, y_test)

print(f"Stacking F1: {stack_score:.3f}")
print("✅ Meta-learner combines base model predictions")
```

**Part C: Weighted Blending (25 min)**
```python
from sklearn.metrics import f1_score
import numpy as np

# Train base models
models = {
    'rf': RandomForestClassifier(n_estimators=100, random_state=42),
    'xgb': xgb.XGBClassifier(n_estimators=100, random_state=42),
    'lgb': lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
}

# Get predictions
predictions = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions[name] = model.predict_proba(X_test)[:, 1]

# Optimize weights
from scipy.optimize import minimize

def blend_objective(weights):
    weights = weights / weights.sum()  # Normalize
    blended = sum(w * pred for w, pred in zip(weights, predictions.values()))
    y_pred = (blended > 0.5).astype(int)
    return -f1_score(y_test, y_pred)  # Negative for minimization

x0 = np.ones(len(models)) / len(models)  # Initial equal weights
result = minimize(blend_objective, x0, bounds=[(0, 1)] * len(models))

optimal_weights = result.x / result.x.sum()

print("Optimal weights:")
for name, weight in zip(models.keys(), optimal_weights):
    print(f"  {name}: {weight:.3f}")

print(f"\nBlended F1: {-result.fun:.3f}")
```
"""
        )

        st.markdown("---")
        st.markdown("## Lab 3: Model Calibration & Uncertainty (90 min)")
        st.markdown(
            """**Objective:** Calibrate probabilities for better decisions

**Part A: Calibration Curves (30 min)**
```python
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

# Train uncalibrated model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_proba = rf.predict_proba(X_test)[:, 1]

# Calibration curve
fraction_of_positives, mean_predicted_value = calibration_curve(
    y_test, y_proba, n_bins=10
)

plt.figure(figsize=(10, 6))
plt.plot([0, 1], [0, 1], 'k--', label='Perfectly calibrated')
plt.plot(mean_predicted_value, fraction_of_positives, 's-', 
         label='Random Forest')
plt.xlabel('Mean Predicted Probability')
plt.ylabel('Fraction of Positives')
plt.title('Calibration Curve')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("Calibration analysis:")
print(f"  Predicted avg: {y_proba.mean():.3f}")
print(f"  Actual positive rate: {y_test.mean():.3f}")
if abs(y_proba.mean() - y_test.mean()) > 0.05:
    print("  ⚠️ Model is miscalibrated!")
```

**Part B: Platt Scaling & Isotonic Regression (30 min)**
```python
from sklearn.calibration import CalibratedClassifierCV

# Platt scaling (logistic regression)
rf_platt = CalibratedClassifierCV(rf, method='sigmoid', cv=5)
rf_platt.fit(X_train, y_train)
y_proba_platt = rf_platt.predict_proba(X_test)[:, 1]

# Isotonic regression (non-parametric)
rf_isotonic = CalibratedClassifierCV(rf, method='isotonic', cv=5)
rf_isotonic.fit(X_train, y_train)
y_proba_isotonic = rf_isotonic.predict_proba(X_test)[:, 1]

# Compare calibration
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for ax, proba, title in zip(axes, 
                             [y_proba, y_proba_platt, y_proba_isotonic],
                             ['Uncalibrated', 'Platt Scaling', 'Isotonic']):
    frac_pos, mean_pred = calibration_curve(y_test, proba, n_bins=10)
    ax.plot([0, 1], [0, 1], 'k--')
    ax.plot(mean_pred, frac_pos, 's-')
    ax.set_title(title)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✅ Calibrated models provide reliable probabilities")
```

**Part C: Conformal Prediction Intervals (30 min)**
```python
from sklearn.model_selection import train_test_split

# Split for conformal prediction
X_train_cal, X_cal, y_train_cal, y_cal = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_cal, y_train_cal)

# Calibration scores (non-conformity scores)
cal_proba = model.predict_proba(X_cal)[:, 1]
cal_scores = np.abs(y_cal - cal_proba)

# Compute prediction intervals
alpha = 0.1  # 90% confidence
quantile = np.quantile(cal_scores, 1 - alpha)

# Test predictions with intervals
test_proba = model.predict_proba(X_test)[:, 1]
test_lower = np.clip(test_proba - quantile, 0, 1)
test_upper = np.clip(test_proba + quantile, 0, 1)

# Evaluate coverage
coverage = ((y_test >= test_lower) & (y_test <= test_upper)).mean()

print(f"Conformal Prediction Results:")
print(f"  Target coverage: {1-alpha:.1%}")
print(f"  Actual coverage: {coverage:.1%}")
print(f"  Avg interval width: {(test_upper - test_lower).mean():.3f}")

if coverage >= 1 - alpha - 0.05:
    print("  ✅ Valid prediction intervals")

print("\n- ☐ Analyzed calibration curves")
print("- ☐ Applied Platt scaling & isotonic regression")
print("- ☐ Implemented conformal prediction")
print("- ☐ Portfolio-ready uncertainty quantification")
```
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

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS")
        
        st.markdown("## Lab 1: Time-Series Forecasting Basics (90 min)")
        st.markdown(
            """**Objective:** Build ARIMA, Prophet, and baseline forecasts

**Part A:** Naive, seasonal naive, moving average baselines  
**Part B:** ARIMA model selection (ACF/PACF analysis)  
**Part C:** Prophet for trend + seasonality

- ☐ Built 5 forecast models
- ☐ Evaluated MAE, RMSE, MAPE
- ☐ Selected best model
"""
        )

        st.markdown("---")
        st.markdown("## Lab 2: ML for Time-Series (75 min)")
        st.markdown(
            """**Objective:** Use XGBoost with lag features

**Part A:** Create lag/rolling window features  
**Part B:** Train XGBoost regressor  
**Part C:** Multi-step ahead forecasting

*Full code in notebooks*
"""
        )

        st.markdown("---")
        st.markdown("## Lab 3: Demand Forecasting Mini-Project (90 min)")
        st.markdown(
            """**Objective:** Production-ready demand forecast

**Part A:** Load retail sales data + EDA  
**Part B:** Compare ARIMA vs Prophet vs XGBoost  
**Part C:** Deploy forecast API

- ☐ Portfolio-ready forecasting project
- ☐ Business metrics (inventory optimization)
- ☐ Deployed as API
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
            """You will explore lightweight automation for ML workflows:

- Running tests automatically when code changes.
- Building and versioning docker images.
- Controlled promotion of models between environments (dev/test/prod).
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS")
        
        st.markdown("## Lab 1: Docker for ML (90 min)")
        st.markdown(
            """**Objective:** Containerize ML application

**Part A:** Create Dockerfile for model serving  
**Part B:** Docker Compose multi-container setup  
**Part C:** Push to registry

- ☐ Dockerized ML API
- ☐ Reproducible environment
- ☐ Production-ready container
"""
        )

        st.markdown("---")
        st.markdown("## Lab 2: GitHub Actions CI/CD (75 min)")
        st.markdown(
            """**Objective:** Automate testing and deployment

**Part A:** Setup pytest for ML code  
**Part B:** GitHub Actions workflow  
**Part C:** Auto-deploy on merge to main

*Full code in course repository*
"""
        )

        st.markdown("---")
        st.markdown("## Lab 3: Model Versioning & Registry (90 min)")
        st.markdown(
            """**Objective:** Manage model versions in production

**Part A:** MLflow Model Registry  
**Part B:** Stage transitions (dev/staging/prod)  
**Part C:** Rollback strategy

- ☐ Model versioning system
- ☐ Automated deployment pipeline
- ☐ Portfolio-ready MLOps project
"""
        )

    elif unit_number == 6:
        st.markdown("#### 📘 Why monitoring and responsible AI?")
        st.markdown(
            """Models change behaviour over time as data, users and processes
change. This unit focuses on **catching problems early** and ensuring
"""
        )

        st.markdown("#### � Explainability and fairness considerations")
        st.markdown(
            """Responsible AI also means addressing fairness and bias:

- Asking whether the model treats subgroups differently.
- Using fairness metrics and concepts to identify potential harms.
- How learnings feed back into retraining and design.
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS")
        
        st.markdown("## Lab 1: Data Drift Detection (90 min)")
        st.markdown(
            """**Objective:** Monitor and detect distribution shifts

**Part A:** Implement PSI, KS test, KL divergence  
**Part B:** Build monitoring dashboard  
**Part C:** Automated alerts

- ☐ Drift detection system
- ☐ Real-time monitoring
- ☐ Alert thresholds configured
"""
        )

        st.markdown("---")
        st.markdown("## Lab 2: Model Performance Monitoring (75 min)")
        st.markdown(
            """**Objective:** Track model performance over time

**Part A:** Log predictions + ground truth  
**Part B:** Calculate rolling metrics  
**Part C:** Automated retraining triggers

*Full code in notebooks*
"""
        )

        st.markdown("---")
        st.markdown("## Lab 3: Fairness & Bias Analysis (90 min)")
        st.markdown(
            """**Objective:** Assess and mitigate model bias

**Part A:** Fairness metrics (demographic parity, equalized odds)  
**Part B:** Bias detection in predictions  
**Part C:** Mitigation strategies

- ☐ Fairness audit complete
- ☐ Bias mitigation implemented
- ☐ Responsible AI portfolio piece
"""
        )

    elif unit_number == 7:
        st.markdown("#### 🎓 Portfolio and career impact")
        st.markdown(
            """A polished capstone demonstrates you can handle production-like
ML projects. This is a strong portfolio piece that shows you understand
the **whole lifecycle** of an ML system, not just training a model.
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
                {
                    "text": "What is a feature store?",
                    "options": [
                        "A physical storage location",
                        "A centralized repository for managing, storing, and serving features",
                        "A type of database",
                        "A visualization tool",
                    ],
                    "answer": 1,
                    "explanation": "Feature stores provide centralized feature management with versioning and serving capabilities.",
                },
                {
                    "text": "Why is feature documentation important in production?",
                    "options": [
                        "To make files larger",
                        "To help teams understand feature definitions, sources, and update frequency",
                        "It is not important",
                        "To slow down development",
                    ],
                    "answer": 1,
                    "explanation": "Documentation ensures teams use features correctly and understand their limitations.",
                },
                {
                    "text": "What is late-arriving data?",
                    "options": [
                        "Data that arrives after the prediction deadline",
                        "Old historical data",
                        "Data with missing values",
                        "Encrypted data",
                    ],
                    "answer": 0,
                    "explanation": "Late-arriving data comes in after you need to make a prediction, requiring careful handling.",
                },
                {
                    "text": "How do you handle features that update at different frequencies?",
                    "options": [
                        "Ignore the problem",
                        "Use point-in-time joins to get the most recent value available at prediction time",
                        "Delete all features",
                        "Only use daily features",
                    ],
                    "answer": 1,
                    "explanation": "Point-in-time joins ensure you only use information that would have been available.",
                },
                {
                    "text": "What is feature drift?",
                    "options": [
                        "When feature definitions change",
                        "When the statistical properties of features change over time",
                        "When features are deleted",
                        "When models train faster",
                    ],
                    "answer": 1,
                    "explanation": "Feature drift occurs when the distribution of input features changes over time.",
                },
                {
                    "text": "Why version features in production?",
                    "options": [
                        "To confuse data scientists",
                        "To track changes and enable reproducibility",
                        "Versioning is not needed",
                        "To increase storage costs",
                    ],
                    "answer": 1,
                    "explanation": "Versioning allows you to reproduce models and understand what changed over time.",
                },
                {
                    "text": "What is the main challenge with real-time feature computation?",
                    "options": [
                        "It is too easy",
                        "Balancing latency requirements with computation complexity",
                        "It never works",
                        "It requires no infrastructure",
                    ],
                    "answer": 1,
                    "explanation": "Real-time features must be computed quickly enough to meet prediction latency requirements.",
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
                {
                    "text": "What should you log in an ML experiment?",
                    "options": [
                        "Only the final accuracy",
                        "Parameters, metrics, data versions, code versions, and environment details",
                        "Nothing",
                        "Only the model file",
                    ],
                    "answer": 1,
                    "explanation": "Comprehensive logging enables reproducibility and comparison across experiments.",
                },
                {
                    "text": "What is MLflow commonly used for?",
                    "options": [
                        "Writing code",
                        "Tracking experiments, packaging models, and managing deployments",
                        "Creating databases",
                        "Designing UIs",
                    ],
                    "answer": 1,
                    "explanation": "MLflow is a popular platform for the ML lifecycle including tracking and deployment.",
                },
                {
                    "text": "Why compare multiple model families in experiments?",
                    "options": [
                        "To waste time",
                        "To find which approach works best for your specific problem and data",
                        "To confuse stakeholders",
                        "It is not useful",
                    ],
                    "answer": 1,
                    "explanation": "Different model families have different strengths; experimentation reveals what works best.",
                },
                {
                    "text": "What is model reproducibility?",
                    "options": [
                        "Training the same model twice",
                        "The ability to recreate the exact same model and results given the same inputs",
                        "Making models faster",
                        "Deleting old models",
                    ],
                    "answer": 1,
                    "explanation": "Reproducibility means others can recreate your results with the same data and code.",
                },
                {
                    "text": "Why is experiment organization important?",
                    "options": [
                        "To make dashboards pretty",
                        "To enable comparison, avoid duplication, and support collaboration",
                        "It is not important",
                        "To slow down development",
                    ],
                    "answer": 1,
                    "explanation": "Good organization helps teams learn from past experiments and avoid repeating work.",
                },
                {
                    "text": "What is a model registry?",
                    "options": [
                        "A list of data scientists",
                        "A centralized store for managing model versions and metadata",
                        "A type of algorithm",
                        "A visualization tool",
                    ],
                    "answer": 1,
                    "explanation": "Model registries track model versions, stages (staging/production), and lineage.",
                },
                {
                    "text": "Why track hyperparameters in experiments?",
                    "options": [
                        "To make logs larger",
                        "To understand which configurations led to which results",
                        "Hyperparameters don't matter",
                        "To delete models",
                    ],
                    "answer": 1,
                    "explanation": "Tracking hyperparameters lets you reproduce results and understand what drives performance.",
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
                {
                    "text": "What is gradient boosting?",
                    "options": [
                        "A type of neural network",
                        "An ensemble method that builds models sequentially to correct errors",
                        "A data cleaning technique",
                        "A visualization method",
                    ],
                    "answer": 1,
                    "explanation": "Gradient boosting builds trees sequentially, each correcting the previous one's errors.",
                },
                {
                    "text": "Why use ensemble methods?",
                    "options": [
                        "They are always slower",
                        "Combining multiple models often improves performance and robustness",
                        "They require no data",
                        "They are simpler than single models",
                    ],
                    "answer": 1,
                    "explanation": "Ensembles leverage diverse models to achieve better overall performance.",
                },
                {
                    "text": "What is the difference between bagging and boosting?",
                    "options": [
                        "They are the same",
                        "Bagging trains models in parallel; boosting trains sequentially",
                        "Bagging is always better",
                        "Boosting doesn't use trees",
                    ],
                    "answer": 1,
                    "explanation": "Bagging (e.g., Random Forest) trains independently; boosting trains sequentially.",
                },
                {
                    "text": "What is SHAP used for?",
                    "options": [
                        "Training models faster",
                        "Explaining individual predictions by attributing contributions to features",
                        "Cleaning data",
                        "Creating databases",
                    ],
                    "answer": 1,
                    "explanation": "SHAP values explain how much each feature contributed to a specific prediction.",
                },
                {
                    "text": "Why is model interpretability important?",
                    "options": [
                        "It makes models slower",
                        "To build trust, debug issues, and meet regulatory requirements",
                        "It is not important",
                        "To reduce accuracy",
                    ],
                    "answer": 1,
                    "explanation": "Interpretability helps stakeholders trust and understand model decisions.",
                },
                {
                    "text": "What is feature importance?",
                    "options": [
                        "The size of features",
                        "A measure of how much each feature contributes to model predictions",
                        "The number of features",
                        "A type of encoding",
                    ],
                    "answer": 1,
                    "explanation": "Feature importance quantifies which features most influence model outputs.",
                },
                {
                    "text": "When should you use XGBoost or LightGBM?",
                    "options": [
                        "Never",
                        "When you need high performance on structured data with many features",
                        "Only for images",
                        "Only for text",
                    ],
                    "answer": 1,
                    "explanation": "Gradient boosting libraries excel on tabular data with complex patterns.",
                },
                {
                    "text": "What is overfitting in ensemble models?",
                    "options": [
                        "It never happens",
                        "When the ensemble learns training data too well and generalizes poorly",
                        "When models train too fast",
                        "When you use too few models",
                    ],
                    "answer": 1,
                    "explanation": "Even ensembles can overfit if not properly regularized or validated.",
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
                {
                    "text": "What is seasonality in time series?",
                    "options": [
                        "Random noise",
                        "Regular patterns that repeat at fixed intervals (e.g., weekly, yearly)",
                        "A type of error",
                        "Missing data",
                    ],
                    "answer": 1,
                    "explanation": "Seasonality refers to predictable patterns that recur at regular intervals.",
                },
                {
                    "text": "What is a naive forecast baseline?",
                    "options": [
                        "A complex neural network",
                        "Using the last observed value as the prediction",
                        "Random predictions",
                        "Always predicting zero",
                    ],
                    "answer": 1,
                    "explanation": "Naive forecasts (e.g., last value, seasonal naive) are simple but important baselines.",
                },
                {
                    "text": "Why is autocorrelation important in time series?",
                    "options": [
                        "It is not important",
                        "It measures how current values relate to past values",
                        "It removes all patterns",
                        "It only applies to images",
                    ],
                    "answer": 1,
                    "explanation": "Autocorrelation reveals temporal dependencies that forecasting models can exploit.",
                },
                {
                    "text": "What is a forecast horizon?",
                    "options": [
                        "The time period you are predicting into the future",
                        "The past data window",
                        "The model accuracy",
                        "The dataset size",
                    ],
                    "answer": 0,
                    "explanation": "Forecast horizon is how far ahead you're predicting (e.g., next 7 days).",
                },
                {
                    "text": "What is trend in time series?",
                    "options": [
                        "Random variation",
                        "A long-term increase or decrease in the data",
                        "Short-term noise",
                        "Missing values",
                    ],
                    "answer": 1,
                    "explanation": "Trend represents the overall direction of the series over time.",
                },
                {
                    "text": "Why use external covariates in forecasting?",
                    "options": [
                        "To make models slower",
                        "To incorporate additional information that influences the target",
                        "They are never useful",
                        "To reduce accuracy",
                    ],
                    "answer": 1,
                    "explanation": "Covariates (e.g., holidays, weather) can improve forecast accuracy.",
                },
                {
                    "text": "What is stationarity in time series?",
                    "options": [
                        "When the series never changes",
                        "When statistical properties (mean, variance) are constant over time",
                        "When there is no data",
                        "When models are perfect",
                    ],
                    "answer": 1,
                    "explanation": "Stationary series have stable statistical properties, making them easier to model.",
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
                {
                    "text": "What is a Docker container?",
                    "options": [
                        "A physical box",
                        "A lightweight, portable package containing code and dependencies",
                        "A type of database",
                        "A visualization tool",
                    ],
                    "answer": 1,
                    "explanation": "Containers package applications with their dependencies for consistent deployment.",
                },
                {
                    "text": "Why use virtual environments for ML projects?",
                    "options": [
                        "To make code slower",
                        "To isolate dependencies and avoid conflicts between projects",
                        "They are not useful",
                        "To increase disk usage",
                    ],
                    "answer": 1,
                    "explanation": "Virtual environments prevent dependency conflicts and ensure reproducibility.",
                },
                {
                    "text": "What is continuous integration (CI)?",
                    "options": [
                        "Never testing code",
                        "Automatically testing code changes when they are committed",
                        "Manual deployment",
                        "Deleting old code",
                    ],
                    "answer": 1,
                    "explanation": "CI automatically runs tests on code changes to catch issues early.",
                },
                {
                    "text": "What should you test in an ML pipeline?",
                    "options": [
                        "Nothing",
                        "Data validation, model performance, and code correctness",
                        "Only the final accuracy",
                        "Only the UI",
                    ],
                    "answer": 1,
                    "explanation": "Comprehensive testing covers data quality, model behavior, and code functionality.",
                },
                {
                    "text": "What is infrastructure as code (IaC)?",
                    "options": [
                        "Writing code in the cloud",
                        "Defining infrastructure using code that can be versioned and automated",
                        "Manually configuring servers",
                        "A type of ML algorithm",
                    ],
                    "answer": 1,
                    "explanation": "IaC treats infrastructure configuration as code, enabling version control and automation.",
                },
                {
                    "text": "Why package ML models?",
                    "options": [
                        "To make them larger",
                        "To make them portable, reproducible, and easy to deploy",
                        "Packaging is not needed",
                        "To slow down predictions",
                    ],
                    "answer": 1,
                    "explanation": "Packaging bundles models with dependencies for consistent deployment across environments.",
                },
                {
                    "text": "What is a model artifact?",
                    "options": [
                        "A bug in the code",
                        "The saved model file and associated metadata",
                        "A type of feature",
                        "A visualization",
                    ],
                    "answer": 1,
                    "explanation": "Artifacts include the trained model, preprocessing pipelines, and metadata.",
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
                {
                    "text": "What is data drift?",
                    "options": [
                        "When data is deleted",
                        "When the distribution of input features changes over time",
                        "When models train faster",
                        "When accuracy improves",
                    ],
                    "answer": 1,
                    "explanation": "Data drift occurs when input distributions shift, potentially degrading model performance.",
                },
                {
                    "text": "What is concept drift?",
                    "options": [
                        "When features are renamed",
                        "When the relationship between features and target changes over time",
                        "When data is encrypted",
                        "When models are deleted",
                    ],
                    "answer": 1,
                    "explanation": "Concept drift means the underlying patterns the model learned no longer hold.",
                },
                {
                    "text": "Why monitor prediction latency?",
                    "options": [
                        "It doesn't matter",
                        "To ensure predictions are fast enough for the application's requirements",
                        "To reduce accuracy",
                        "To increase costs",
                    ],
                    "answer": 1,
                    "explanation": "Latency monitoring ensures the model meets real-time or batch performance SLAs.",
                },
                {
                    "text": "What is an ML observability platform?",
                    "options": [
                        "A type of model",
                        "A system for monitoring model performance, data quality, and system health",
                        "A database",
                        "A visualization library",
                    ],
                    "answer": 1,
                    "explanation": "Observability platforms provide comprehensive monitoring of ML systems in production.",
                },
                {
                    "text": "Why is fairness important in ML?",
                    "options": [
                        "It is not important",
                        "To ensure models don't systematically disadvantage certain groups",
                        "To make models slower",
                        "To reduce accuracy",
                    ],
                    "answer": 1,
                    "explanation": "Fairness ensures ML systems treat all groups equitably and avoid harmful bias.",
                },
                {
                    "text": "What is a model retraining trigger?",
                    "options": [
                        "A type of feature",
                        "A condition that indicates the model should be retrained (e.g., performance drop)",
                        "A visualization",
                        "A database query",
                    ],
                    "answer": 1,
                    "explanation": "Triggers automate retraining when performance degrades or data changes significantly.",
                },
                {
                    "text": "What is responsible AI?",
                    "options": [
                        "Ignoring ethical concerns",
                        "Developing AI systems that are fair, transparent, accountable, and beneficial",
                        "Making models as complex as possible",
                        "Avoiding documentation",
                    ],
                    "answer": 1,
                    "explanation": "Responsible AI emphasizes ethical development and deployment of AI systems.",
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
                {
                    "text": "What makes an advanced capstone project strong?",
                    "options": [
                        "Using every algorithm available",
                        "Clear problem, rigorous methods, production considerations, and honest evaluation",
                        "The longest possible report",
                        "Hiding negative results",
                    ],
                    "answer": 1,
                    "explanation": "Strong advanced capstones demonstrate production-ready thinking and professional judgment.",
                },
                {
                    "text": "Why include a deployment plan in your capstone?",
                    "options": [
                        "To make it longer",
                        "To show you understand how the model would be used in practice",
                        "Deployment is not relevant",
                        "To avoid testing",
                    ],
                    "answer": 1,
                    "explanation": "Deployment planning demonstrates practical understanding of production ML.",
                },
                {
                    "text": "What should a monitoring plan include?",
                    "options": [
                        "Nothing",
                        "Metrics to track, alert thresholds, and retraining criteria",
                        "Only accuracy",
                        "Random numbers",
                    ],
                    "answer": 1,
                    "explanation": "A good monitoring plan specifies what to track and when to take action.",
                },
                {
                    "text": "Why document ethical considerations?",
                    "options": [
                        "It is not important",
                        "To show awareness of potential harms and mitigation strategies",
                        "To make the report longer",
                        "To hide problems",
                    ],
                    "answer": 1,
                    "explanation": "Ethical documentation shows professional responsibility and risk awareness.",
                },
                {
                    "text": "What is the purpose of an advanced capstone?",
                    "options": [
                        "To memorize formulas",
                        "To demonstrate production-ready ML skills from problem to deployment",
                        "To avoid learning",
                        "To pass time",
                    ],
                    "answer": 1,
                    "explanation": "Advanced capstones showcase end-to-end ML engineering and operational thinking.",
                },
                {
                    "text": "How should you present your advanced capstone?",
                    "options": [
                        "Keep it secret",
                        "GitHub repo with code, docs, architecture diagrams, and runbook",
                        "Only screenshots",
                        "Verbal description only",
                    ],
                    "answer": 1,
                    "explanation": "Professional presentation includes comprehensive documentation and reproducible code.",
                },
                {
                    "text": "What distinguishes an advanced capstone from intermediate?",
                    "options": [
                        "More pages",
                        "Production considerations, monitoring plans, and operational thinking",
                        "Using more libraries",
                        "Longer training time",
                    ],
                    "answer": 1,
                    "explanation": "Advanced capstones demonstrate MLOps maturity and production-ready practices.",
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

        st.markdown("---")
        st.markdown("### 💼 Career Preparation Package")
        st.success(
            "**NEW!** Advanced ML & MLOps career toolkit - Resume, interview Q&A, "
            "deployment questions, and career strategies for senior DS roles!"
        )
        
        if st.button("📥 Career Prep - Senior Data Scientist", key="dsp3_career_prep_pdf"):
            # Reusing comprehensive DS career prep (same role, advanced level)
            career_prep_md = """# Career Prep Package - Senior Data Scientist / ML Engineer

**Advanced toolkit for senior Data Science and MLOps roles**

This package includes all the Data Scientist interview content PLUS advanced
MLOps, production ML, and system design questions relevant to Pathway 3 topics.

See Data Scientist Career Prep Package (Pathway 2) for:
- Complete ML interview questions (80 questions)
- Resume templates
- Python/Scikit-learn coding questions
- Model deployment basics

**ADDITIONAL CONTENT FOR ADVANCED/SENIOR ROLES:**

---

## 💼 SENIOR-LEVEL FOCUS AREAS

### MLOps & Production ML
- Model monitoring and drift detection
- Feature stores and serving infrastructure
- A/B testing frameworks
- Model versioning and registry
- CI/CD for ML pipelines
- Container orchestration (Kubernetes)

### System Design for ML
- Designing scalable ML systems
- Real-time vs batch prediction architecture
- Handling high-throughput serving
- Multi-model serving strategies
- Cost optimization in production

### Advanced Topics
- Deep learning architecture decisions
- Transfer learning strategies
- Model compression and optimization
- Explainability in production
- Fairness and bias mitigation
- Privacy-preserving ML

---

## 🎤 SENIOR DATA SCIENTIST INTERVIEW FOCUS

### System Design Questions:
1. Design a recommendation system for 1M users
2. Build real-time fraud detection system
3. Design ML platform for 100 data scientists
4. Implement A/B testing framework
5. Design model monitoring infrastructure

### Leadership & Strategy:
- Managing ML projects and teams
- Communicating with executives
- Balancing research vs production
- Setting ML strategy
- Evaluating build vs buy decisions

### Trade-off Discussions:
- Model complexity vs interpretability
- Accuracy vs latency
- Development speed vs robustness
- Cost vs performance
- Custom vs off-the-shelf solutions

---

## 💡 SENIOR ROLE POSITIONING

### Resume Highlights for Senior Roles:
- Focus on impact and scale (millions of users, $X saved)
- Show leadership (mentoring, strategy, architecture)
- Production experience emphasized
- Business outcomes, not just model metrics
- End-to-end ownership of systems

### LinkedIn for Senior Roles:
"Senior Data Scientist | ML Engineering | Production ML Systems at Scale"
"ML Lead | MLOps | Building AI Products | Team Leadership"

### Salary Expectations:
- Mid-level Data Scientist: £50K-£80K
- Senior Data Scientist: £80K-£120K+
- Principal/Staff: £120K-£180K+
- ML Engineering Manager: £100K-£150K+

---

**For complete interview prep, refer to Data Scientist Career Prep Package,
plus focus on the advanced topics above for senior/lead positions.**

**Good luck advancing your ML career! 🚀**
"""
            pdf = create_unit_pdf(0, "Career Prep - Senior DS/MLOps", career_prep_md)
            st.download_button(
                label="Download Career Prep Package PDF",
                data=pdf,
                file_name="Career_Prep_Package_Senior_DS_MLOps.pdf",
                mime="application/pdf",
                key="dsp3_career_prep_pdf_dl",
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
