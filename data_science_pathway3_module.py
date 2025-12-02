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


def _render_unit1_labs():
    """Labs for Unit 1: Advanced Feature Engineering"""
    st.markdown("---")
    st.markdown("## 🧪 HANDS-ON LABS: Unit 1")
    
    st.markdown("### Lab 1: Build a Feature Store (90 min)")
    lab1_code = '''import pandas as pd
import sqlite3
from datetime import datetime
import hashlib

class SimpleFeatureStore:
    def __init__(self, db_path="features.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS features (
            feature_id TEXT PRIMARY KEY,
            feature_name TEXT,
            entity_id TEXT,
            feature_value REAL,
            timestamp TEXT,
            version TEXT
        )""")
        self.conn.commit()
    
    def write_features(self, entity_id, features, version="v1"):
        timestamp = datetime.now().isoformat()
        for feature_name, value in features.items():
            feature_id = hashlib.md5(
                f"{entity_id}_{feature_name}_{timestamp}".encode()
            ).hexdigest()
            self.conn.execute(
                "INSERT INTO features VALUES (?, ?, ?, ?, ?, ?)",
                (feature_id, feature_name, entity_id, value, timestamp, version)
            )
        self.conn.commit()
    
    def read_features(self, entity_id, feature_names, version="v1"):
        placeholders = ",".join(["?"] * len(feature_names))
        query = f"""SELECT feature_name, feature_value FROM features
                    WHERE entity_id = ? AND feature_name IN ({placeholders})
                    AND version = ? ORDER BY timestamp DESC"""
        cursor = self.conn.execute(query, [entity_id] + feature_names + [version])
        return dict(cursor.fetchall())

# Example
store = SimpleFeatureStore()
store.write_features("customer_123", {
    "total_purchases": 45,
    "avg_order_value": 125.50
})
features = store.read_features("customer_123", ["total_purchases"])
print(features)'''
    st.code(lab1_code, language='python')
    
    st.markdown("#### Part B: Feature Versioning (30 min)")
    lab1b_code = '''import json
from datetime import datetime

class FeatureRegistry:
    def __init__(self):
        self.features = {}
    
    def register(self, name, description, dtype, source, owner, version="v1.0"):
        self.features[name] = {
            "description": description,
            "dtype": dtype,
            "source": source,
            "owner": owner,
            "version": version,
            "created_at": datetime.now().isoformat()
        }
        print(f"✅ Registered {name} v{version}")
    
    def get_metadata(self, name):
        return self.features.get(name, {})
    
    def save(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.features, f, indent=2)
        print(f"✅ Saved registry to {filepath}")

# Example
registry = FeatureRegistry()

registry.register(
    name="customer_lifetime_value",
    description="Predicted CLV based on purchase history",
    dtype="float",
    source="transactions + ml_model",
    owner="data-science-team",
    version="v2.1"
)

registry.register(
    name="churn_risk_score",
    description="Probability of churn in next 30 days",
    dtype="float",
    source="churn_model_v3",
    owner="ml-ops-team",
    version="v3.0"
)

metadata = registry.get_metadata("customer_lifetime_value")
print(f"\nMetadata: {json.dumps(metadata, indent=2)}")

registry.save("feature_registry.json")'''
    st.code(lab1b_code, language='python')
    
    st.markdown("#### Part C: Point-in-Time Correctness (30 min)")
    lab1c_code = '''import pandas as pd
from datetime import datetime, timedelta

def compute_features_point_in_time(transactions_df, customer_id, as_of_date, lookback_days=90):
    """Compute features using only data available before as_of_date"""
    cutoff = pd.to_datetime(as_of_date)
    start = cutoff - timedelta(days=lookback_days)
    
    # Filter: only transactions BEFORE as_of_date
    valid_txns = transactions_df[
        (transactions_df['customer_id'] == customer_id) &
        (transactions_df['date'] < cutoff) &
        (transactions_df['date'] >= start)
    ]
    
    features = {
        'as_of_date': as_of_date,
        'total_transactions': len(valid_txns),
        'total_spent': valid_txns['amount'].sum() if len(valid_txns) > 0 else 0,
        'avg_transaction': valid_txns['amount'].mean() if len(valid_txns) > 0 else 0,
        'days_since_last': (
            (cutoff - valid_txns['date'].max()).days 
            if len(valid_txns) > 0 else lookback_days
        )
    }
    
    return features

# Example: Simulate time-travel
import numpy as np
np.random.seed(42)

# Generate transactions over 1 year
txns = []
for day in range(365):
    if np.random.random() < 0.3:  # 30% chance of transaction
        txns.append({
            'customer_id': 'C001',
            'date': datetime(2023, 1, 1) + timedelta(days=day),
            'amount': np.random.uniform(20, 200)
        })

txns_df = pd.DataFrame(txns)

# Compute features as of different dates
for month in [3, 6, 9, 12]:
    as_of = datetime(2023, month, 1)
    features = compute_features_point_in_time(txns_df, 'C001', as_of)
    print(f"\nAs of {as_of.date()}:")
    print(f"  Transactions: {features['total_transactions']}")
    print(f"  Total spent: ${features['total_spent']:.2f}")
    print(f"  Days since last: {features['days_since_last']}")

print("\n✅ Point-in-time correctness prevents data leakage!")'''
    st.code(lab1c_code, language='python')
    
    st.markdown("### Lab 2: Feature Monitoring (60 min)")
    lab2_code = '''import pandas as pd
from scipy import stats

def detect_feature_drift(train_features, prod_features, threshold=0.05):
    drift_report = {}
    for col in train_features.columns:
        if train_features[col].dtype in ['float64', 'int64']:
            stat, p_value = stats.ks_2samp(
                train_features[col].dropna(),
                prod_features[col].dropna()
            )
            drift_report[col] = {
                'p_value': p_value,
                'drift': p_value < threshold
            }
    return drift_report

# Example
train = pd.DataFrame({'feature1': [1, 2, 3, 4, 5]})
prod = pd.DataFrame({'feature1': [10, 20, 30, 40, 50]})  # Drifted

report = detect_feature_drift(train, prod)
for feature, result in report.items():
    status = "⚠️ DRIFT" if result['drift'] else "✅ OK"
    print(f"{feature}: {status} (p={result['p_value']:.4f})")'''
    st.code(lab2_code, language='python')
    
    st.markdown("#### Part B: Automated Monitoring Dashboard (30 min)")
    lab2b_code = '''import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

class FeatureMonitoringDashboard:
    def __init__(self):
        self.baselines = {}
        self.alerts = []
    
    def set_baseline(self, feature_name, data):
        self.baselines[feature_name] = {
            'mean': data.mean(),
            'std': data.std(),
            'min': data.min(),
            'max': data.max(),
            'q25': data.quantile(0.25),
            'q50': data.quantile(0.50),
            'q75': data.quantile(0.75),
            'data': data.values
        }
    
    def check_feature(self, feature_name, current_data, threshold=0.05):
        if feature_name not in self.baselines:
            return {'error': 'No baseline set'}
        
        baseline = self.baselines[feature_name]
        
        # Statistical tests
        ks_stat, ks_pval = stats.ks_2samp(baseline['data'], current_data.values)
        
        # Mean shift detection
        current_mean = current_data.mean()
        mean_shift_sigma = abs(current_mean - baseline['mean']) / baseline['std']
        
        # Variance change
        variance_ratio = current_data.std() / baseline['std']
        
        # Determine alert level
        drift_detected = ks_pval < threshold
        if ks_pval < 0.01 or mean_shift_sigma > 3:
            alert_level = '🔴 CRITICAL'
        elif drift_detected or mean_shift_sigma > 2:
            alert_level = '🟡 WARNING'
        else:
            alert_level = '🟢 OK'
        
        result = {
            'feature': feature_name,
            'alert_level': alert_level,
            'drift_detected': drift_detected,
            'ks_pvalue': ks_pval,
            'mean_shift_sigma': mean_shift_sigma,
            'variance_ratio': variance_ratio,
            'baseline_mean': baseline['mean'],
            'current_mean': current_mean
        }
        
        if drift_detected:
            self.alerts.append(result)
        
        return result
    
    def get_alerts(self):
        return pd.DataFrame(self.alerts)

# Example
monitor = FeatureMonitoringDashboard()

# Set baselines
np.random.seed(42)
for feature in ['age', 'income', 'credit_score']:
    baseline_data = pd.Series(np.random.normal(50, 10, 1000))
    monitor.set_baseline(feature, baseline_data)

# Check current data (simulating drift)
current_age = pd.Series(np.random.normal(55, 12, 500))  # Shifted
current_income = pd.Series(np.random.normal(50, 10, 500))  # Normal
current_credit = pd.Series(np.random.normal(60, 15, 500))  # Shifted + variance

print("📊 Feature Monitoring Results:\n")
for fname, data in [('age', current_age), ('income', current_income), ('credit_score', current_credit)]:
    result = monitor.check_feature(fname, data)
    print(f"{result['alert_level']} {result['feature']}")
    print(f"  Drift: {result['drift_detected']}")
    print(f"  p-value: {result['ks_pvalue']:.6f}")
    print(f"  Mean shift: {result['mean_shift_sigma']:.2f} sigma")
    print()

alerts_df = monitor.get_alerts()
if len(alerts_df) > 0:
    print(f"⚠️ {len(alerts_df)} features with drift detected!")
else:
    print("✅ All features within normal range")'''
    st.code(lab2b_code, language='python')
    
    st.markdown("### Lab 3: Feature Selection & Importance (90 min)")
    st.markdown("**Identify and select the most important features for your model**")
    
    lab3_code = '''import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif, RFE, mutual_info_classif
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

class FeatureSelector:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.results = {}
    
    def univariate_selection(self, k=10):
        """Select features using univariate statistical tests"""
        selector = SelectKBest(f_classif, k=k)
        selector.fit(self.X, self.y)
        
        scores = pd.DataFrame({
            'feature': self.X.columns,
            'score': selector.scores_
        }).sort_values('score', ascending=False)
        
        self.results['univariate'] = scores
        return scores
    
    def tree_importance(self):
        """Get feature importance from tree-based model"""
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(self.X, self.y)
        
        importance = pd.DataFrame({
            'feature': self.X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.results['tree_importance'] = importance
        return importance
    
    def permutation_importance_analysis(self, n_repeats=10):
        """Calculate permutation importance"""
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(self.X, self.y)
        
        perm_importance = permutation_importance(
            model, self.X, self.y,
            n_repeats=n_repeats,
            random_state=42
        )
        
        importance = pd.DataFrame({
            'feature': self.X.columns,
            'importance_mean': perm_importance.importances_mean,
            'importance_std': perm_importance.importances_std
        }).sort_values('importance_mean', ascending=False)
        
        self.results['permutation'] = importance
        return importance
    
    def recursive_feature_elimination(self, n_features=10):
        """Use RFE to select features"""
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        rfe = RFE(model, n_features_to_select=n_features)
        rfe.fit(self.X, self.y)
        
        selected = pd.DataFrame({
            'feature': self.X.columns,
            'selected': rfe.support_,
            'ranking': rfe.ranking_
        }).sort_values('ranking')
        
        self.results['rfe'] = selected
        return selected
    
    def mutual_information(self):
        """Calculate mutual information"""
        mi_scores = mutual_info_classif(self.X, self.y, random_state=42)
        
        mi = pd.DataFrame({
            'feature': self.X.columns,
            'mi_score': mi_scores
        }).sort_values('mi_score', ascending=False)
        
        self.results['mutual_info'] = mi
        return mi
    
    def get_consensus_features(self, top_n=10):
        """Get features that rank high across multiple methods"""
        # Normalize rankings
        rankings = {}
        
        for method, df in self.results.items():
            if method == 'rfe':
                # For RFE, selected features get rank 1
                rankings[method] = df[df['selected']]['feature'].tolist()
            else:
                # For others, take top N
                rankings[method] = df.head(top_n)['feature'].tolist()
        
        # Count appearances
        feature_counts = {}
        for features in rankings.values():
            for feature in features:
                feature_counts[feature] = feature_counts.get(feature, 0) + 1
        
        # Sort by count
        consensus = pd.DataFrame([
            {'feature': f, 'method_count': c}
            for f, c in feature_counts.items()
        ]).sort_values('method_count', ascending=False)
        
        return consensus

# Example
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=1000,
    n_features=30,
    n_informative=15,
    n_redundant=10,
    random_state=42
)

X_df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(30)])

# Create selector
selector = FeatureSelector(X_df, y)

print("🔍 Running Feature Selection Methods...\n")

# Run all methods
print("1. Univariate Selection:")
univariate = selector.univariate_selection(k=10)
print(univariate.head())

print("\n2. Tree-based Importance:")
tree_imp = selector.tree_importance()
print(tree_imp.head())

print("\n3. Permutation Importance:")
perm_imp = selector.permutation_importance_analysis()
print(perm_imp.head())

print("\n4. Recursive Feature Elimination:")
rfe = selector.recursive_feature_elimination(n_features=10)
print(rfe[rfe['selected']])

print("\n5. Mutual Information:")
mi = selector.mutual_information()
print(mi.head())

# Get consensus
print("\n🏆 Consensus Features (appear in multiple methods):")
consensus = selector.get_consensus_features(top_n=10)
print(consensus.head(15))

print(f"\n✅ Top features: {consensus.head(10)['feature'].tolist()}")'''
    st.code(lab3_code, language='python')
    
    st.success("✅ Unit 1 Labs Complete: Production feature engineering mastered!")


def _render_unit2_labs():
    """Labs for Unit 2: Experiment Tracking"""
    st.markdown("---")
    st.markdown("## 🧪 HANDS-ON LABS: Unit 2")
    
    st.markdown("### Lab 1: MLflow Experiment Tracking (90 min)")
    lab1_code = '''import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Setup MLflow
mlflow.set_experiment("my_experiment")

# Run experiment
with mlflow.start_run(run_name="rf_baseline"):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", None)
    
    # Log metrics
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    mlflow.log_metric("train_accuracy", train_score)
    mlflow.log_metric("test_accuracy", test_score)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    print(f"Train: {train_score:.3f}, Test: {test_score:.3f}")

# View results: mlflow ui'''
    st.code(lab1_code, language='python')
    
    st.markdown("#### Part B: Hyperparameter Tracking (30 min)")
    lab1b_code = '''import mlflow
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5]
}

mlflow.set_experiment("hyperparameter_search")

with mlflow.start_run(run_name="grid_search_rf"):
    grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )
    grid.fit(X_train, y_train)
    
    # Log all parameter combinations
    for i, params in enumerate(grid.cv_results_['params']):
        with mlflow.start_run(run_name=f"config_{i}", nested=True):
            for param, value in params.items():
                mlflow.log_param(param, value)
            mlflow.log_metric("mean_cv_score", grid.cv_results_['mean_test_score'][i])
            mlflow.log_metric("std_cv_score", grid.cv_results_['std_test_score'][i])
    
    # Log best configuration
    mlflow.log_params(grid.best_params_)
    mlflow.log_metric("best_cv_score", grid.best_score_)
    mlflow.log_metric("test_score", grid.score(X_test, y_test))
    mlflow.sklearn.log_model(grid.best_estimator_, "best_model")
    
    print(f"Best params: {grid.best_params_}")
    print(f"Best CV score: {grid.best_score_:.3f}")
    print(f"Test score: {grid.score(X_test, y_test):.3f}")'''
    st.code(lab1b_code, language='python')
    
    st.markdown("#### Part C: Model Comparison Dashboard (30 min)")
    lab1c_code = '''import mlflow
import pandas as pd

# Search for all runs in experiment
experiment = mlflow.get_experiment_by_name("my_experiment")
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

# Create comparison dataframe
comparison = runs[[
    'run_id',
    'params.n_estimators',
    'params.max_depth',
    'metrics.train_accuracy',
    'metrics.test_accuracy',
    'start_time'
]].copy()

comparison['start_time'] = pd.to_datetime(comparison['start_time'])
comparison = comparison.sort_values('metrics.test_accuracy', ascending=False)

print("\n🏆 Top 5 Models:")
print(comparison.head().to_string(index=False))

# Find best model
best_run = comparison.iloc[0]
print(f"\n✅ Best Model:")
print(f"  Run ID: {best_run['run_id']}")
print(f"  Test Accuracy: {best_run['metrics.test_accuracy']:.3f}")
print(f"  n_estimators: {best_run['params.n_estimators']}")
print(f"  max_depth: {best_run['params.max_depth']}")'''
    st.code(lab1c_code, language='python')
    
    st.markdown("### Lab 2: Cross-Validation Comparison (75 min)")
    lab2_code = '''from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np

models = {
    'Logistic': LogisticRegression(max_iter=1000),
    'RF': RandomForestClassifier(n_estimators=100, random_state=42),
    'GBM': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

kf = KFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')
    print(f"{name}: {scores.mean():.3f} ± {scores.std():.3f}")
    
# Statistical comparison
from scipy.stats import ttest_rel
rf_scores = cross_val_score(models['RF'], X, y, cv=kf)
gbm_scores = cross_val_score(models['GBM'], X, y, cv=kf)
t_stat, p_value = ttest_rel(rf_scores, gbm_scores)
print(f"\\nRF vs GBM: p-value = {p_value:.4f}")
if p_value < 0.05:
    print("✅ Statistically significant difference")
else:
    print("❌ No significant difference")'''
    st.code(lab2_code, language='python')
    
    st.markdown("#### Part B: Nested Cross-Validation (40 min)")
    lab2b_code = '''from sklearn.model_selection import GridSearchCV, cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Outer CV for unbiased evaluation
outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)

# Inner CV for hyperparameter tuning
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None]
}

outer_scores = []

for fold, (train_idx, test_idx) in enumerate(outer_cv.split(X), 1):
    X_train_fold, X_test_fold = X[train_idx], X[test_idx]
    y_train_fold, y_test_fold = y[train_idx], y[test_idx]
    
    # Inner loop: hyperparameter tuning
    grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        cv=inner_cv,
        scoring='accuracy'
    )
    grid.fit(X_train_fold, y_train_fold)
    
    # Outer loop: evaluate with best params
    test_score = grid.score(X_test_fold, y_test_fold)
    outer_scores.append(test_score)
    
    print(f"Fold {fold}: {test_score:.3f} (best params: {grid.best_params_})")

print(f"\nNested CV Score: {np.mean(outer_scores):.3f} ± {np.std(outer_scores):.3f}")
print("✅ Unbiased estimate (no data leakage)")'''
    st.code(lab2b_code, language='python')
    
    st.markdown("### Lab 3: Automated Model Selection (90 min)")
    st.markdown("**Build a system that automatically selects the best model**")
    
    lab3_code = '''import mlflow
import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import numpy as np

class AutoMLSelector:
    def __init__(self, experiment_name="auto_ml"):
        mlflow.set_experiment(experiment_name)
        self.results = []
    
    def evaluate_model(self, model, model_name, X, y, cv=5):
        """Evaluate a single model with cross-validation"""
        with mlflow.start_run(run_name=model_name):
            kf = KFold(n_splits=cv, shuffle=True, random_state=42)
            scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')
            
            mean_score = scores.mean()
            std_score = scores.std()
            
            # Log to MLflow
            mlflow.log_param("model_type", model_name)
            mlflow.log_metric("mean_cv_accuracy", mean_score)
            mlflow.log_metric("std_cv_accuracy", std_score)
            mlflow.log_metric("min_cv_accuracy", scores.min())
            mlflow.log_metric("max_cv_accuracy", scores.max())
            
            # Store results
            self.results.append({
                'model': model_name,
                'mean_accuracy': mean_score,
                'std_accuracy': std_score,
                'scores': scores
            })
            
            print(f"{model_name}: {mean_score:.3f} ± {std_score:.3f}")
            
            return mean_score, std_score
    
    def run_model_zoo(self, X, y):
        """Evaluate multiple models"""
        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(kernel='rbf', random_state=42),
            'Naive Bayes': GaussianNB()
        }
        
        print("🚀 Running AutoML Model Selection...\n")
        
        for name, model in models.items():
            self.evaluate_model(model, name, X, y)
        
        return self.get_best_model()
    
    def get_best_model(self):
        """Get the best performing model"""
        results_df = pd.DataFrame(self.results)
        results_df = results_df.sort_values('mean_accuracy', ascending=False)
        
        best = results_df.iloc[0]
        
        print(f"\n🏆 Best Model: {best['model']}")
        print(f"   Accuracy: {best['mean_accuracy']:.3f} ± {best['std_accuracy']:.3f}")
        
        return best
    
    def get_leaderboard(self):
        """Get full leaderboard"""
        results_df = pd.DataFrame(self.results)
        results_df = results_df.sort_values('mean_accuracy', ascending=False)
        results_df['rank'] = range(1, len(results_df) + 1)
        return results_df[['rank', 'model', 'mean_accuracy', 'std_accuracy']]

# Example usage
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, random_state=42)

selector = AutoMLSelector()
best_model = selector.run_model_zoo(X, y)

print("\n📊 Full Leaderboard:")
print(selector.get_leaderboard().to_string(index=False))'''
    st.code(lab3_code, language='python')
    
    st.markdown("#### Part B: Statistical Model Comparison (30 min)")
    lab3b_code = '''from scipy.stats import ttest_rel, wilcoxon
import numpy as np

def compare_models_statistically(model1_scores, model2_scores, model1_name, model2_name):
    """Compare two models using statistical tests"""
    
    # Paired t-test
    t_stat, t_pval = ttest_rel(model1_scores, model2_scores)
    
    # Wilcoxon signed-rank test (non-parametric)
    w_stat, w_pval = wilcoxon(model1_scores, model2_scores)
    
    print(f"\n📊 Statistical Comparison: {model1_name} vs {model2_name}")
    print(f"\n{model1_name}: {model1_scores.mean():.3f} ± {model1_scores.std():.3f}")
    print(f"{model2_name}: {model2_scores.mean():.3f} ± {model2_scores.std():.3f}")
    
    print(f"\nPaired t-test:")
    print(f"  t-statistic: {t_stat:.3f}")
    print(f"  p-value: {t_pval:.4f}")
    
    print(f"\nWilcoxon test:")
    print(f"  statistic: {w_stat:.3f}")
    print(f"  p-value: {w_pval:.4f}")
    
    # Interpretation
    alpha = 0.05
    if t_pval < alpha:
        diff = model1_scores.mean() - model2_scores.mean()
        winner = model1_name if diff > 0 else model2_name
        print(f"\n✅ Statistically significant difference (p < {alpha})")
        print(f"   Winner: {winner}")
    else:
        print(f"\n❌ No significant difference (p >= {alpha})")
        print(f"   Both models perform similarly")

# Example
rf_scores = selector.results[1]['scores']  # Random Forest
gb_scores = selector.results[2]['scores']  # Gradient Boosting

compare_models_statistically(rf_scores, gb_scores, 'Random Forest', 'Gradient Boosting')'''
    st.code(lab3b_code, language='python')
    
    st.markdown("### Lab 4: Experiment Reproducibility (60 min)")
    lab4_code = '''import mlflow
import hashlib
import json
from datetime import datetime
import numpy as np

class ReproducibleExperiment:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)
        self.config = {}
    
    def set_seeds(self, seed=42):
        """Set all random seeds for reproducibility"""
        np.random.seed(seed)
        import random
        random.seed(seed)
        
        try:
            import torch
            torch.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
        except ImportError:
            pass
        
        self.config['seed'] = seed
        print(f"✅ Set random seed: {seed}")
    
    def log_environment(self):
        """Log complete environment information"""
        import sys
        import platform
        import sklearn
        
        env_info = {
            'python_version': sys.version,
            'platform': platform.platform(),
            'sklearn_version': sklearn.__version__,
            'timestamp': datetime.now().isoformat()
        }
        
        self.config['environment'] = env_info
        return env_info
    
    def compute_data_hash(self, X, y):
        """Compute hash of data for verification"""
        data_str = f"{X.tobytes()}{y.tobytes()}"
        data_hash = hashlib.md5(data_str.encode()).hexdigest()
        self.config['data_hash'] = data_hash
        return data_hash
    
    def run_experiment(self, model, X_train, y_train, X_test, y_test, params):
        """Run fully reproducible experiment"""
        with mlflow.start_run(run_name=f"reproducible_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log all configuration
            mlflow.log_params(params)
            mlflow.log_param('seed', self.config.get('seed', 'not_set'))
            mlflow.log_param('data_hash', self.config.get('data_hash', 'not_computed'))
            
            # Log environment
            env_info = self.log_environment()
            for key, value in env_info.items():
                mlflow.log_param(f'env_{key}', str(value)[:250])  # MLflow param limit
            
            # Train
            model.fit(X_train, y_train)
            
            # Evaluate
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            mlflow.log_metric('train_accuracy', train_score)
            mlflow.log_metric('test_accuracy', test_score)
            
            # Save model
            mlflow.sklearn.log_model(model, 'model')
            
            # Save complete config
            config_path = 'experiment_config.json'
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            mlflow.log_artifact(config_path)
            
            print(f"\n✅ Experiment logged with full reproducibility")
            print(f"   Train: {train_score:.3f}")
            print(f"   Test: {test_score:.3f}")
            print(f"   Data hash: {self.config.get('data_hash', 'N/A')[:8]}...")
            
            return {
                'train_score': train_score,
                'test_score': test_score,
                'run_id': mlflow.active_run().info.run_id
            }

# Example
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Create reproducible experiment
exp = ReproducibleExperiment('reproducibility_demo')

# Set seeds
exp.set_seeds(42)

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Compute data hash
data_hash = exp.compute_data_hash(X, y)
print(f"\nData hash: {data_hash}")

# Run experiment
model = RandomForestClassifier(n_estimators=100, random_state=42)
params = {'n_estimators': 100, 'random_state': 42}

results = exp.run_experiment(model, X_train, y_train, X_test, y_test, params)

print(f"\n✅ Run ID: {results['run_id']}")
print("Anyone can reproduce this exact result using the logged configuration!")'''
    st.code(lab4_code, language='python')
    
    st.markdown("### Lab 5: Model Lineage Tracking (75 min)")
    lab5_code = '''import mlflow
import json
from datetime import datetime
import hashlib

class ModelLineageTracker:
    def __init__(self):
        self.lineage = {}
    
    def track_data_lineage(self, data_source, data_version, transformations):
        """Track data lineage"""
        data_hash = hashlib.md5(str(data_source).encode()).hexdigest()
        
        return {
            'data_source': data_source,
            'data_version': data_version,
            'data_hash': data_hash,
            'transformations': transformations,
            'timestamp': datetime.now().isoformat()
        }
    
    def track_model_lineage(self, model_name, model_version, parent_models=None):
        """Track model lineage and dependencies"""
        lineage_id = f"{model_name}_v{model_version}"
        
        self.lineage[lineage_id] = {
            'model_name': model_name,
            'version': model_version,
            'parent_models': parent_models or [],
            'created_at': datetime.now().isoformat(),
            'children': []
        }
        
        # Update parent models
        if parent_models:
            for parent_id in parent_models:
                if parent_id in self.lineage:
                    self.lineage[parent_id]['children'].append(lineage_id)
        
        return lineage_id
    
    def log_full_lineage(self, model, model_name, model_version, 
                        data_lineage, hyperparams, metrics):
        """Log complete model lineage to MLflow"""
        with mlflow.start_run(run_name=f"{model_name}_v{model_version}"):
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Log hyperparameters
            mlflow.log_params(hyperparams)
            
            # Log metrics
            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)
            
            # Log data lineage
            mlflow.log_dict(data_lineage, "data_lineage.json")
            
            # Log model lineage
            model_lineage_id = self.track_model_lineage(model_name, model_version)
            mlflow.log_param("lineage_id", model_lineage_id)
            
            # Save complete lineage graph
            mlflow.log_dict(self.lineage, "model_lineage_graph.json")
            
            run_id = mlflow.active_run().info.run_id
            
            print(f"✅ Logged complete lineage for {model_name} v{model_version}")
            print(f"   Run ID: {run_id}")
            print(f"   Lineage ID: {model_lineage_id}")
            
            return run_id
    
    def visualize_lineage(self, model_id):
        """Visualize model lineage graph"""
        if model_id not in self.lineage:
            print(f"❌ Model {model_id} not found")
            return
        
        def print_tree(node_id, indent=0):
            if node_id not in self.lineage:
                return
            
            node = self.lineage[node_id]
            print("  " * indent + f"├─ {node['model_name']} v{node['version']}")
            
            for child_id in node['children']:
                print_tree(child_id, indent + 1)
        
        print("\n🌳 Model Lineage Tree:")
        print_tree(model_id)

# Example
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

mlflow.set_experiment("lineage_tracking_demo")

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Track lineage
tracker = ModelLineageTracker()

# Track data lineage
data_lineage = tracker.track_data_lineage(
    data_source="synthetic_classification_dataset",
    data_version="v1.0",
    transformations=[
        "train_test_split(test_size=0.2)",
        "StandardScaler()"
    ]
)

# Train and log model v1
model_v1 = RandomForestClassifier(n_estimators=50, random_state=42)
model_v1.fit(X_train, y_train)

run_id_v1 = tracker.log_full_lineage(
    model=model_v1,
    model_name="churn_predictor",
    model_version="1.0",
    data_lineage=data_lineage,
    hyperparams={'n_estimators': 50, 'random_state': 42},
    metrics={'accuracy': model_v1.score(X_test, y_test)}
)

# Train improved model v2 (child of v1)
model_v2 = RandomForestClassifier(n_estimators=100, random_state=42)
model_v2.fit(X_train, y_train)

run_id_v2 = tracker.log_full_lineage(
    model=model_v2,
    model_name="churn_predictor",
    model_version="2.0",
    data_lineage=data_lineage,
    hyperparams={'n_estimators': 100, 'random_state': 42},
    metrics={'accuracy': model_v2.score(X_test, y_test)}
)

# Visualize lineage
tracker.visualize_lineage("churn_predictor_v1.0")

print("\n✅ Complete lineage tracked and logged to MLflow!")'''
    st.code(lab5_code, language='python')
    
    st.success("✅ Unit 2 Labs Complete: Experiment tracking and model selection mastered!")


def _render_unit3_labs():
    """Labs for Unit 3: Hyperparameter Optimization"""
    st.markdown("---")
    st.markdown("## 🧪 HANDS-ON LABS: Unit 3")
    
    st.markdown("### Lab 1: Grid Search with MLflow (90 min)")
    lab1_code = '''from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import mlflow

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5, 10]
}

mlflow.set_experiment("hyperparameter_tuning")

with mlflow.start_run(run_name="grid_search"):
    grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )
    grid.fit(X_train, y_train)
    
    # Log best parameters
    for param, value in grid.best_params_.items():
        mlflow.log_param(f"best_{param}", value)
    
    # Log best score
    mlflow.log_metric("best_cv_score", grid.best_score_)
    mlflow.log_metric("test_score", grid.score(X_test, y_test))
    
    # Log model
    mlflow.sklearn.log_model(grid.best_estimator_, "model")
    
    print(f"Best params: {grid.best_params_}")
    print(f"Best CV score: {grid.best_score_:.3f}")'''
    st.code(lab1_code, language='python')
    
    st.markdown("### Lab 2: Bayesian Optimization with Optuna (90 min)")
    lab2_code = '''import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    # Define hyperparameter search space
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    max_depth = trial.suggest_int('max_depth', 3, 20)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42
    )
    
    # Evaluate with cross-validation
    score = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy').mean()
    return score

# Run optimization
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)

print(f"Best params: {study.best_params}")
print(f"Best score: {study.best_value:.3f}")

# Train final model
best_model = RandomForestClassifier(**study.best_params, random_state=42)
best_model.fit(X_train, y_train)
print(f"Test score: {best_model.score(X_test, y_test):.3f}")'''
    st.code(lab2_code, language='python')
    
    st.markdown("#### Part B: Pruning and Early Stopping (30 min)")
    lab2b_code = '''import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def objective_with_pruning(trial):
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    max_depth = trial.suggest_int('max_depth', 3, 20)
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    
    # Incremental evaluation for pruning
    scores = []
    for fold in range(3):
        score = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy')[fold]
        scores.append(score)
        
        # Report intermediate value
        trial.report(score, fold)
        
        # Prune if not promising
        if trial.should_prune():
            raise optuna.TrialPruned()
    
    return sum(scores) / len(scores)

# Run with pruning
study = optuna.create_study(
    direction='maximize',
    pruner=optuna.pruners.MedianPruner(n_startup_trials=5)
)

study.optimize(objective_with_pruning, n_trials=50, timeout=300)

print(f"\nBest trial:")
print(f"  Value: {study.best_value:.3f}")
print(f"  Params: {study.best_params}")
print(f"\nPruned trials: {len([t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED])}")
print(f"Completed trials: {len([t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE])}")'''
    st.code(lab2b_code, language='python')
    
    st.markdown("#### Part C: Multi-Objective Optimization (30 min)")
    lab2c_code = '''import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import time

def multi_objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    max_depth = trial.suggest_int('max_depth', 3, 20)
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    
    # Objective 1: Maximize accuracy
    start = time.time()
    accuracy = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy').mean()
    training_time = time.time() - start
    
    # Objective 2: Minimize training time
    return accuracy, training_time

# Multi-objective study
study = optuna.create_study(
    directions=['maximize', 'minimize']  # Max accuracy, min time
)

study.optimize(multi_objective, n_trials=30)

print("\n🎯 Pareto Front (best trade-offs):")
for trial in study.best_trials:
    print(f"  Accuracy: {trial.values[0]:.3f}, Time: {trial.values[1]:.2f}s")
    print(f"    Params: {trial.params}")
    print()'''
    st.code(lab2c_code, language='python')
    
    st.markdown("### Lab 3: Random Search vs Grid Search (60 min)")
    lab3_code = '''from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint, uniform
import time
import numpy as np

# Define search spaces
param_grid = {
    'n_estimators': [50, 100, 150, 200],
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

param_distributions = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(5, 20),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 4)
}

# Grid Search
print("🔍 Running Grid Search...")
start = time.time()
grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    n_jobs=-1
)
grid.fit(X_train, y_train)
grid_time = time.time() - start

print(f"  Time: {grid_time:.1f}s")
print(f"  Best score: {grid.best_score_:.3f}")
print(f"  Combinations tried: {len(grid.cv_results_['params'])}")

# Random Search
print("\n🎲 Running Random Search...")
start = time.time()
random = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions,
    n_iter=50,  # Try 50 random combinations
    cv=3,
    random_state=42,
    n_jobs=-1
)
random.fit(X_train, y_train)
random_time = time.time() - start

print(f"  Time: {random_time:.1f}s")
print(f"  Best score: {random.best_score_:.3f}")
print(f"  Combinations tried: 50")

# Comparison
print("\n🏆 Comparison:")
print(f"  Grid Search: {grid.best_score_:.3f} in {grid_time:.1f}s")
print(f"  Random Search: {random.best_score_:.3f} in {random_time:.1f}s")
print(f"  Speedup: {grid_time/random_time:.1f}x faster")

if random.best_score_ >= grid.best_score_ * 0.99:  # Within 1%
    print("\n✅ Random Search found comparable solution much faster!")'''
    st.code(lab3_code, language='python')
    
    st.markdown("### Lab 4: Hyperband Optimization (45 min)")
    lab4_code = '''import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

def objective_with_budget(trial):
    # Suggest hyperparameters
    n_estimators = trial.suggest_int('n_estimators', 10, 200)
    max_depth = trial.suggest_int('max_depth', 3, 20)
    
    # Use pruning for early stopping
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    
    # Incremental evaluation
    scores = []
    for i in range(3):  # 3-fold CV
        score = cross_val_score(model, X_train, y_train, cv=3)[i]
        scores.append(score)
        
        # Report intermediate value
        trial.report(score, i)
        
        # Prune unpromising trials
        if trial.should_prune():
            raise optuna.TrialPruned()
    
    return np.mean(scores)

# Run Hyperband-style optimization
study = optuna.create_study(
    direction='maximize',
    pruner=optuna.pruners.HyperbandPruner(
        min_resource=1,
        max_resource=10,
        reduction_factor=3
    )
)

print("🚀 Running Hyperband Optimization...\n")
study.optimize(objective_with_budget, n_trials=100, timeout=300)

print(f"\nBest trial:")
print(f"  Value: {study.best_value:.3f}")
print(f"  Params: {study.best_params}")

print(f"\nOptimization stats:")
print(f"  Total trials: {len(study.trials)}")
print(f"  Pruned: {len([t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED])}")
print(f"  Completed: {len([t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE])}")
print(f"  Speedup from pruning: {len(study.trials) / len([t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]):.1f}x")'''
    st.code(lab4_code, language='python')
    
    st.markdown("### Lab 5: Bayesian Optimization (60 min)")
    lab5_code = '''from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
import numpy as np

class BayesianOptimizer:
    def __init__(self, bounds, n_init=5):
        self.bounds = bounds  # [(min, max), ...]
        self.n_init = n_init
        self.X_observed = []
        self.y_observed = []
        self.gp = GaussianProcessRegressor(
            kernel=Matern(nu=2.5),
            alpha=1e-6,
            normalize_y=True,
            n_restarts_optimizer=5
        )
    
    def suggest_next(self):
        """Suggest next point to evaluate using acquisition function"""
        if len(self.X_observed) < self.n_init:
            # Random exploration
            return [np.random.uniform(low, high) for low, high in self.bounds]
        
        # Fit GP
        self.gp.fit(self.X_observed, self.y_observed)
        
        # Expected Improvement acquisition
        best_y = max(self.y_observed)
        
        # Sample candidates
        n_candidates = 1000
        candidates = np.array([
            [np.random.uniform(low, high) for low, high in self.bounds]
            for _ in range(n_candidates)
        ])
        
        # Predict
        mu, sigma = self.gp.predict(candidates, return_std=True)
        
        # Expected Improvement
        with np.errstate(divide='ignore'):
            Z = (mu - best_y) / sigma
            ei = (mu - best_y) * stats.norm.cdf(Z) + sigma * stats.norm.pdf(Z)
            ei[sigma == 0.0] = 0.0
        
        # Return best candidate
        best_idx = np.argmax(ei)
        return candidates[best_idx].tolist()
    
    def observe(self, x, y):
        """Record observation"""
        self.X_observed.append(x)
        self.y_observed.append(y)
    
    def get_best(self):
        """Get best observed point"""
        best_idx = np.argmax(self.y_observed)
        return self.X_observed[best_idx], self.y_observed[best_idx]

# Example: Optimize hyperparameters
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
from scipy import stats

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

def objective(params):
    """Objective function to maximize"""
    n_estimators = int(params[0])
    max_depth = int(params[1])
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    
    score = cross_val_score(model, X, y, cv=3, scoring='accuracy').mean()
    return score

# Run Bayesian Optimization
optimizer = BayesianOptimizer(
    bounds=[(50, 200), (5, 20)],  # n_estimators, max_depth
    n_init=5
)

print("🧪 Running Bayesian Optimization...\n")

for i in range(20):
    # Get next point to try
    params = optimizer.suggest_next()
    
    # Evaluate
    score = objective(params)
    
    # Record
    optimizer.observe(params, score)
    
    print(f"Trial {i+1}: n_est={int(params[0])}, depth={int(params[1])} -> {score:.3f}")

# Get best
best_params, best_score = optimizer.get_best()
print(f"\n🏆 Best: n_est={int(best_params[0])}, depth={int(best_params[1])} -> {best_score:.3f}")'''
    st.code(lab5_code, language='python')
    
    st.markdown("### Lab 6: Genetic Algorithm Optimization (75 min)")
    lab6_code = '''import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

class GeneticOptimizer:
    def __init__(self, param_bounds, population_size=20, generations=10):
        self.param_bounds = param_bounds
        self.population_size = population_size
        self.generations = generations
        self.best_individual = None
        self.best_score = -np.inf
    
    def create_individual(self):
        """Create random parameter set"""
        return [np.random.uniform(low, high) for low, high in self.param_bounds]
    
    def create_population(self):
        """Create initial population"""
        return [self.create_individual() for _ in range(self.population_size)]
    
    def evaluate(self, individual, X, y):
        """Evaluate fitness of individual"""
        n_estimators = int(individual[0])
        max_depth = int(individual[1])
        min_samples_split = int(individual[2])
        
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=42
        )
        
        score = cross_val_score(model, X, y, cv=3, scoring='accuracy').mean()
        return score
    
    def select_parents(self, population, scores):
        """Tournament selection"""
        tournament_size = 3
        selected = []
        
        for _ in range(2):  # Select 2 parents
            tournament_idx = np.random.choice(len(population), tournament_size)
            tournament_scores = [scores[i] for i in tournament_idx]
            winner_idx = tournament_idx[np.argmax(tournament_scores)]
            selected.append(population[winner_idx])
        
        return selected
    
    def crossover(self, parent1, parent2):
        """Single-point crossover"""
        crossover_point = np.random.randint(1, len(parent1))
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child
    
    def mutate(self, individual, mutation_rate=0.1):
        """Mutate individual"""
        mutated = individual.copy()
        for i in range(len(mutated)):
            if np.random.random() < mutation_rate:
                mutated[i] = np.random.uniform(*self.param_bounds[i])
        return mutated
    
    def optimize(self, X, y):
        """Run genetic algorithm"""
        population = self.create_population()
        
        for gen in range(self.generations):
            # Evaluate
            scores = [self.evaluate(ind, X, y) for ind in population]
            
            # Track best
            gen_best_idx = np.argmax(scores)
            if scores[gen_best_idx] > self.best_score:
                self.best_score = scores[gen_best_idx]
                self.best_individual = population[gen_best_idx]
            
            print(f"Gen {gen+1}: Best={self.best_score:.3f}, Avg={np.mean(scores):.3f}")
            
            # Create new population
            new_population = []
            
            # Elitism: keep best individual
            new_population.append(self.best_individual)
            
            # Generate rest through selection, crossover, mutation
            while len(new_population) < self.population_size:
                parents = self.select_parents(population, scores)
                child = self.crossover(parents[0], parents[1])
                child = self.mutate(child)
                new_population.append(child)
            
            population = new_population
        
        return self.best_individual, self.best_score

# Example
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

optimizer = GeneticOptimizer(
    param_bounds=[(50, 200), (5, 20), (2, 10)],  # n_estimators, max_depth, min_samples_split
    population_size=15,
    generations=8
)

print("🧬 Running Genetic Algorithm...\n")
best_params, best_score = optimizer.optimize(X, y)

print(f"\n🏆 Best Parameters:")
print(f"  n_estimators: {int(best_params[0])}")
print(f"  max_depth: {int(best_params[1])}")
print(f"  min_samples_split: {int(best_params[2])}")
print(f"  Score: {best_score:.3f}")'''
    st.code(lab6_code, language='python')
    
    st.markdown("### Lab 7: AutoML Pipeline (60 min)")
    lab7_code = '''from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np

class SimpleAutoML:
    def __init__(self, time_budget_minutes=5):
        self.time_budget = time_budget_minutes * 60
        self.models = self._get_model_space()
        self.best_pipeline = None
        self.best_score = -np.inf
        self.leaderboard = []
    
    def _get_model_space(self):
        """Define model search space"""
        return {
            'LogisticRegression': [
                {'C': 0.1}, {'C': 1.0}, {'C': 10.0}
            ],
            'RandomForest': [
                {'n_estimators': 50, 'max_depth': 5},
                {'n_estimators': 100, 'max_depth': 10},
                {'n_estimators': 200, 'max_depth': None}
            ],
            'GradientBoosting': [
                {'n_estimators': 50, 'learning_rate': 0.1},
                {'n_estimators': 100, 'learning_rate': 0.05},
                {'n_estimators': 200, 'learning_rate': 0.01}
            ]
        }
    
    def fit(self, X, y):
        """Run AutoML search"""
        import time
        start_time = time.time()
        
        print("🤖 Running AutoML...\n")
        
        for model_name, configs in self.models.items():
            for config in configs:
                if time.time() - start_time > self.time_budget:
                    print("\n⏰ Time budget exceeded")
                    break
                
                # Create pipeline
                if model_name == 'LogisticRegression':
                    model = LogisticRegression(**config, random_state=42, max_iter=1000)
                elif model_name == 'RandomForest':
                    model = RandomForestClassifier(**config, random_state=42)
                elif model_name == 'GradientBoosting':
                    model = GradientBoostingClassifier(**config, random_state=42)
                
                pipeline = Pipeline([
                    ('scaler', StandardScaler()),
                    ('model', model)
                ])
                
                # Evaluate
                try:
                    scores = cross_val_score(pipeline, X, y, cv=3, scoring='accuracy')
                    mean_score = scores.mean()
                    std_score = scores.std()
                    
                    # Track
                    self.leaderboard.append({
                        'model': model_name,
                        'config': config,
                        'score': mean_score,
                        'std': std_score
                    })
                    
                    # Update best
                    if mean_score > self.best_score:
                        self.best_score = mean_score
                        self.best_pipeline = pipeline
                        print(f"⭐ New best: {model_name} - {mean_score:.3f}")
                    else:
                        print(f"   {model_name} - {mean_score:.3f}")
                
                except Exception as e:
                    print(f"❌ {model_name} failed: {str(e)[:50]}")
        
        # Fit best pipeline
        self.best_pipeline.fit(X, y)
        
        return self
    
    def predict(self, X):
        return self.best_pipeline.predict(X)
    
    def get_leaderboard(self):
        import pandas as pd
        df = pd.DataFrame(self.leaderboard)
        return df.sort_values('score', ascending=False)

# Example
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Run AutoML
automl = SimpleAutoML(time_budget_minutes=2)
automl.fit(X_train, y_train)

# Results
print(f"\n🏆 Best Model Score: {automl.best_score:.3f}")
print(f"Test Score: {automl.best_pipeline.score(X_test, y_test):.3f}")

print("\n📊 Leaderboard:")
print(automl.get_leaderboard().head(10).to_string(index=False))'''
    st.code(lab7_code, language='python')
    
    st.success("✅ Unit 3 Labs Complete: Advanced hyperparameter optimization mastered!")


def _render_unit4_labs():
    """Labs for Unit 4: Time-Series Forecasting"""
    st.markdown("---")
    st.markdown("## 🧪 HANDS-ON LABS: Unit 4")
    
    st.markdown("### Lab 1: ARIMA Forecasting (60 min)")
    lab1_code = '''import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Generate sample time series
np.random.seed(42)
dates = pd.date_range('2022-01-01', periods=365, freq='D')
trend = np.linspace(100, 150, 365)
seasonality = 20 * np.sin(2 * np.pi * np.arange(365) / 7)
noise = np.random.normal(0, 5, 365)
data = trend + seasonality + noise

ts = pd.Series(data, index=dates)

# Split train/test
train = ts[:'2022-10-31']
test = ts['2022-11-01':]

# Fit ARIMA
model = ARIMA(train, order=(7, 1, 7))
model_fit = model.fit()

# Forecast
forecast = model_fit.forecast(steps=len(test))

# Evaluate
from sklearn.metrics import mean_absolute_error, mean_squared_error
mae = mean_absolute_error(test, forecast)
rmse = np.sqrt(mean_squared_error(test, forecast))

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

# Plot
plt.figure(figsize=(12, 6))
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, label='Actual', color='green')
plt.plot(test.index, forecast, label='Forecast', color='red', linestyle='--')
plt.legend()
plt.title('ARIMA Forecast')
plt.show()'''
    st.code(lab1_code, language='python')
    
    st.markdown("### Lab 2: Prophet for Seasonal Data (60 min)")
    lab2_code = '''from prophet import Prophet
import pandas as pd
import numpy as np

# Prepare data for Prophet
df = pd.DataFrame({
    'ds': dates,
    'y': data
})

train_df = df[df['ds'] <= '2022-10-31']
test_df = df[df['ds'] > '2022-10-31']

# Fit Prophet
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)
model.fit(train_df)

# Make forecast
future = model.make_future_dataframe(periods=len(test_df))
forecast = model.predict(future)

# Extract test predictions
test_forecast = forecast[forecast['ds'] > '2022-10-31']['yhat']

# Evaluate
mae = mean_absolute_error(test_df['y'], test_forecast)
rmse = np.sqrt(mean_squared_error(test_df['y'], test_forecast))

print(f"Prophet MAE: {mae:.2f}")
print(f"Prophet RMSE: {rmse:.2f}")

# Plot components
model.plot_components(forecast)
plt.show()'''
    st.code(lab2_code, language='python')
    
    st.markdown("### Lab 3: XGBoost Time-Series (60 min)")
    lab3_code = '''import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Create lag features
def create_features(series, n_lags=7):
    df = pd.DataFrame({'value': series.values})
    for i in range(1, n_lags + 1):
        df[f'lag_{i}'] = df['value'].shift(i)
    df['rolling_mean_7'] = df['value'].shift(1).rolling(7).mean()
    df['rolling_std_7'] = df['value'].shift(1).rolling(7).std()
    return df.dropna()

df_features = create_features(ts)

# Split
train_size = int(len(df_features) * 0.8)
X_train = df_features.iloc[:train_size].drop('value', axis=1)
y_train = df_features.iloc[:train_size]['value']
X_test = df_features.iloc[train_size:].drop('value', axis=1)
y_test = df_features.iloc[train_size:]['value']

# Train
model = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Predict
preds = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))

print(f"XGBoost MAE: {mae:.2f}")
print(f"XGBoost RMSE: {rmse:.2f}")

# Feature importance
importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nTop Features:")
print(importance.head())'''
    st.code(lab3_code, language='python')
    
    st.markdown("### Lab 4: Forecast Evaluation (45 min)")
    lab4_code = '''import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_forecast(actual, predicted, model_name):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    
    # Bias
    bias = np.mean(predicted - actual)
    
    print(f"\n{model_name} Metrics:")
    print(f"  MAE: {mae:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  MAPE: {mape:.1f}%")
    print(f"  Bias: {bias:.2f}")
    
    if abs(bias) < mae * 0.1:
        print("  ✅ Unbiased")
    else:
        print(f"  ⚠️ {'Over' if bias > 0 else 'Under'}-predicting")
    
    return {'mae': mae, 'rmse': rmse, 'mape': mape, 'bias': bias}

# Compare models
results = []
for name, preds in [('ARIMA', arima_pred), ('Prophet', prophet_pred), ('XGBoost', xgb_pred)]:
    metrics = evaluate_forecast(actual, preds, name)
    metrics['model'] = name
    results.append(metrics)

import pandas as pd
df = pd.DataFrame(results).sort_values('mae')
print(f"\n🏆 Best Model: {df.iloc[0]['model']}")'''
    st.code(lab4_code, language='python')
    
    st.markdown("### Lab 5: Seasonal Decomposition & Analysis (60 min)")
    lab5_code = '''import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

# Generate time series with trend, seasonality, and noise
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=365*3, freq='D')
trend = np.linspace(100, 200, len(dates))
seasonality = 30 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)  # Yearly
weekly = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)  # Weekly
noise = np.random.normal(0, 5, len(dates))

ts = pd.Series(trend + seasonality + weekly + noise, index=dates)

# Decompose
decomposition = seasonal_decompose(ts, model='additive', period=365)

# Extract components
trend_component = decomposition.trend
seasonal_component = decomposition.seasonal
residual_component = decomposition.resid

# Analyze
print("📊 Time Series Decomposition Analysis:")
print(f"\nTrend:")
print(f"  Start: {trend_component.dropna().iloc[0]:.2f}")
print(f"  End: {trend_component.dropna().iloc[-1]:.2f}")
print(f"  Change: {trend_component.dropna().iloc[-1] - trend_component.dropna().iloc[0]:.2f}")

print(f"\nSeasonality:")
print(f"  Amplitude: {seasonal_component.max() - seasonal_component.min():.2f}")
print(f"  Peak month: {seasonal_component.groupby(seasonal_component.index.month).mean().idxmax()}")

print(f"\nResiduals:")
print(f"  Mean: {residual_component.mean():.2f}")
print(f"  Std: {residual_component.std():.2f}")

# Plot
fig, axes = plt.subplots(4, 1, figsize=(12, 10))
ts.plot(ax=axes[0], title='Original')
trend_component.plot(ax=axes[1], title='Trend')
seasonal_component.plot(ax=axes[2], title='Seasonality')
residual_component.plot(ax=axes[3], title='Residuals')
plt.tight_layout()
plt.show()

print("\n✅ Decomposition helps identify patterns for better forecasting!")'''
    st.code(lab5_code, language='python')
    
    st.markdown("### Lab 6: Walk-Forward Validation (45 min)")
    lab6_code = '''import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

def walk_forward_validation(data, model_func, train_size=100, step=10):
    """Walk-forward validation for time series"""
    errors = []
    predictions = []
    actuals = []
    
    for i in range(train_size, len(data) - step, step):
        # Split
        train = data[:i]
        test = data[i:i+step]
        
        # Train and predict
        model = model_func(train)
        pred = model.predict(len(test))
        
        # Store results
        predictions.extend(pred)
        actuals.extend(test.values)
        
        # Calculate error for this window
        mae = mean_absolute_error(test, pred)
        errors.append(mae)
        
        print(f"Window {len(errors)}: Train size={len(train)}, Test size={len(test)}, MAE={mae:.2f}")
    
    overall_mae = mean_absolute_error(actuals, predictions)
    print(f"\n🎯 Overall MAE: {overall_mae:.2f}")
    print(f"Average window MAE: {np.mean(errors):.2f} ± {np.std(errors):.2f}")
    
    return predictions, actuals, errors

# Example model function
def simple_model(train_data):
    class SimpleModel:
        def __init__(self, data):
            self.mean = data.mean()
        
        def predict(self, steps):
            return [self.mean] * steps
    
    return SimpleModel(train_data)

# Run validation
preds, acts, errs = walk_forward_validation(ts, simple_model, train_size=365, step=30)

print("\n✅ Walk-forward validation provides realistic performance estimates!")'''
    st.code(lab6_code, language='python')
    
    st.markdown("### Lab 7: Anomaly Detection (60 min)")
    lab7_code = '''import pandas as pd
import numpy as np
from scipy import stats

class TimeSeriesAnomalyDetector:
    def __init__(self, window_size=30, threshold=3):
        self.window_size = window_size
        self.threshold = threshold
    
    def detect_statistical(self, series):
        """Detect anomalies using statistical methods"""
        anomalies = []
        
        for i in range(self.window_size, len(series)):
            window = series[i-self.window_size:i]
            
            mean = window.mean()
            std = window.std()
            
            # Z-score
            z_score = abs((series.iloc[i] - mean) / std) if std > 0 else 0
            
            if z_score > self.threshold:
                anomalies.append({
                    'index': i,
                    'value': series.iloc[i],
                    'z_score': z_score,
                    'expected_range': (mean - self.threshold*std, mean + self.threshold*std)
                })
        
        return anomalies
    
    def detect_isolation_forest(self, series):
        """Detect anomalies using Isolation Forest"""
        from sklearn.ensemble import IsolationForest
        
        # Prepare features
        X = series.values.reshape(-1, 1)
        
        # Fit model
        iso_forest = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        predictions = iso_forest.fit_predict(X)
        
        # Get anomalies
        anomaly_indices = np.where(predictions == -1)[0]
        
        anomalies = []
        for idx in anomaly_indices:
            anomalies.append({
                'index': idx,
                'value': series.iloc[idx],
                'method': 'isolation_forest'
            })
        
        return anomalies
    
    def detect_all(self, series):
        """Run all detection methods"""
        print("🔍 Running Anomaly Detection...\n")
        
        # Statistical
        stat_anomalies = self.detect_statistical(series)
        print(f"Statistical method: {len(stat_anomalies)} anomalies")
        
        # Isolation Forest
        iso_anomalies = self.detect_isolation_forest(series)
        print(f"Isolation Forest: {len(iso_anomalies)} anomalies")
        
        # Combine (intersection for high confidence)
        stat_indices = {a['index'] for a in stat_anomalies}
        iso_indices = {a['index'] for a in iso_anomalies}
        
        high_confidence = stat_indices & iso_indices
        
        print(f"\n✅ High confidence anomalies: {len(high_confidence)}")
        
        return {
            'statistical': stat_anomalies,
            'isolation_forest': iso_anomalies,
            'high_confidence': list(high_confidence)
        }

# Example
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=365, freq='D')

# Normal pattern
trend = np.linspace(100, 150, 365)
seasonality = 20 * np.sin(2 * np.pi * np.arange(365) / 7)
noise = np.random.normal(0, 3, 365)

ts = pd.Series(trend + seasonality + noise, index=dates)

# Inject anomalies
ts.iloc[50] = 200  # Spike
ts.iloc[100] = 50  # Drop
ts.iloc[200] = 180  # Spike

# Detect
detector = TimeSeriesAnomalyDetector(window_size=30, threshold=3)
results = detector.detect_all(ts)

print("\n⚠️ Detected Anomalies:")
for idx in results['high_confidence']:
    print(f"  Date: {ts.index[idx].date()}, Value: {ts.iloc[idx]:.2f}")

# Visualize
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))
plt.plot(ts.index, ts, label='Time Series', alpha=0.7)

for idx in results['high_confidence']:
    plt.scatter(ts.index[idx], ts.iloc[idx], color='red', s=100, zorder=5, label='Anomaly' if idx == results['high_confidence'][0] else '')

plt.legend()
plt.title('Time Series with Detected Anomalies')
plt.xlabel('Date')
plt.ylabel('Value')
plt.grid(True, alpha=0.3)
plt.show()'''
    st.code(lab7_code, language='python')
    
    st.markdown("### Lab 8: Multi-Step Forecasting (75 min)")
    lab8_code = '''import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

class MultiStepForecaster:
    def __init__(self, model, horizon=7):
        self.model = model
        self.horizon = horizon
    
    def create_sequences(self, data, n_lags=14):
        """Create sequences for multi-step forecasting"""
        X, y = [], []
        
        for i in range(len(data) - n_lags - self.horizon + 1):
            # Features: past n_lags values
            X.append(data[i:i+n_lags])
            # Target: next horizon values
            y.append(data[i+n_lags:i+n_lags+self.horizon])
        
        return np.array(X), np.array(y)
    
    def fit(self, train_data, n_lags=14):
        """Train multi-output model"""
        X_train, y_train = self.create_sequences(train_data, n_lags)
        self.model.fit(X_train, y_train)
        return self
    
    def predict(self, last_values):
        """Predict next horizon steps"""
        return self.model.predict([last_values])[0]
    
    def recursive_forecast(self, initial_values, n_steps):
        """Recursive multi-step forecasting"""
        forecasts = []
        current = list(initial_values)
        
        for _ in range(n_steps // self.horizon):
            # Predict next horizon
            pred = self.predict(current[-len(initial_values):])
            forecasts.extend(pred)
            
            # Update current with predictions
            current.extend(pred)
        
        return np.array(forecasts[:n_steps])

# Example
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=365, freq='D')
trend = np.linspace(100, 150, 365)
seasonality = 20 * np.sin(2 * np.pi * np.arange(365) / 7)
noise = np.random.normal(0, 3, 365)
ts = trend + seasonality + noise

# Split
train_size = 300
train = ts[:train_size]
test = ts[train_size:]

# Train multi-step forecaster
forecaster = MultiStepForecaster(
    model=RandomForestRegressor(n_estimators=100, random_state=42),
    horizon=7  # Forecast 7 days ahead
)

forecaster.fit(train, n_lags=14)

# Forecast
initial = train[-14:]
forecast = forecaster.recursive_forecast(initial, len(test))

# Evaluate
mae = mean_absolute_error(test, forecast)
print(f"\n🎯 Multi-Step Forecast MAE: {mae:.2f}")

# Compare with naive
naive_forecast = np.full(len(test), train[-1])
naive_mae = mean_absolute_error(test, naive_forecast)

print(f"Naive MAE: {naive_mae:.2f}")
print(f"Improvement: {(naive_mae - mae) / naive_mae * 100:.1f}%")

# Plot
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))
plt.plot(range(len(train)), train, label='Train', alpha=0.7)
plt.plot(range(len(train), len(train) + len(test)), test, label='Actual', color='green')
plt.plot(range(len(train), len(train) + len(test)), forecast, label='Forecast', color='red', linestyle='--')
plt.axvline(len(train), color='black', linestyle=':', alpha=0.5)
plt.legend()
plt.title('Multi-Step Forecasting')
plt.show()'''
    st.code(lab8_code, language='python')
    
    st.markdown("### Lab 9: Production Time-Series Pipeline (60 min)")
    lab9_code = '''import pandas as pd
import numpy as np
import joblib
from datetime import datetime

class ProductionTimeSeriesForecaster:
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = None
        self.feature_config = {}
        if model_path:
            self.load(model_path)
    
    def create_features(self, ts_data, n_lags=7):
        """Create features for production"""
        features = {}
        
        # Lag features
        for i in range(1, n_lags + 1):
            features[f'lag_{i}'] = ts_data[-i] if len(ts_data) >= i else 0
        
        # Rolling statistics
        if len(ts_data) >= 7:
            features['rolling_mean_7'] = np.mean(ts_data[-7:])
            features['rolling_std_7'] = np.std(ts_data[-7:])
        else:
            features['rolling_mean_7'] = np.mean(ts_data)
            features['rolling_std_7'] = 0
        
        # Time features
        now = datetime.now()
        features['day_of_week'] = now.weekday()
        features['day_of_month'] = now.day
        features['month'] = now.month
        
        return features
    
    def train(self, historical_data, target, n_lags=7):
        """Train the forecaster"""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        
        # Create training data
        X_train = []
        y_train = []
        
        for i in range(n_lags, len(historical_data)):
            features = self.create_features(historical_data[:i], n_lags)
            X_train.append(list(features.values()))
            y_train.append(target[i])
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        self.feature_config = {'n_lags': n_lags}
        
        print("✅ Model trained successfully")
    
    def predict(self, recent_data):
        """Make a prediction"""
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Create features
        features = self.create_features(
            recent_data, 
            self.feature_config['n_lags']
        )
        
        # Convert to array
        X = np.array([list(features.values())])
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.model.predict(X_scaled)[0]
        
        return prediction
    
    def save(self, path):
        """Save model to disk"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_config': self.feature_config
        }, path)
        print(f"✅ Model saved to {path}")
    
    def load(self, path):
        """Load model from disk"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_config = data['feature_config']
        print(f"✅ Model loaded from {path}")

# Example: Train and deploy
np.random.seed(42)
historical = np.cumsum(np.random.randn(365)) + 100

# Train
forecaster = ProductionTimeSeriesForecaster()
forecaster.train(historical, historical, n_lags=7)

# Save
forecaster.save('forecaster_model.pkl')

# Load and predict (simulating production)
production_forecaster = ProductionTimeSeriesForecaster('forecaster_model.pkl')
recent_data = historical[-14:]
prediction = production_forecaster.predict(recent_data)

print(f"\n🔮 Next forecast: {prediction:.2f}")
print("✅ Production pipeline ready!")'''
    st.code(lab9_code, language='python')
    
    st.markdown("### 🎯 Summary: Time-Series Best Practices")
    st.markdown("""**Key Takeaways:**
- Always check for stationarity before modeling
- Use multiple evaluation metrics (MAE, RMSE, MAPE)
- Implement walk-forward validation for realistic estimates
- Combine multiple models for better forecasts
- Monitor for anomalies and distribution shifts
- Document seasonal patterns and trends
- Use appropriate lag features for ML models
- Consider business context when selecting forecast horizon

**Production Checklist:**
✅ Baseline model established
✅ Multiple models compared
✅ Cross-validation implemented
✅ Anomaly detection in place
✅ Monitoring dashboard created
✅ Documentation complete""")
    
    st.success("✅ Unit 4 Labs Complete: Time-series forecasting mastered!")


def _render_unit5_labs():
    """Labs for Unit 5: Packaging & Deployment"""
    st.markdown("---")
    st.markdown("## 🧪 HANDS-ON LABS: Unit 5")
    
    st.markdown("### Lab 1: Create requirements.txt (30 min)")
    lab1_code = '''# Create virtual environment
python -m venv ml_env

# Activate (Windows)
ml_env\\Scripts\\activate

# Activate (Mac/Linux)
source ml_env/bin/activate

# Install packages
pip install pandas scikit-learn matplotlib joblib

# Generate requirements
pip freeze > requirements.txt

# Share with team
cat requirements.txt'''
    st.code(lab1_code, language='bash')
    
    st.markdown("### Lab 2: Package as Python Module (60 min)")
    lab2_code = '''# setup.py
from setuptools import setup, find_packages

setup(
    name="ml_predictor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "joblib>=1.0.0"
    ],
    author="Your Name",
    description="ML prediction package"
)

# predictor.py
import joblib
import pandas as pd

class Predictor:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)
    
    def predict(self, features):
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        return self.model.predict(features)

# Install package
# pip install -e .'''
    st.code(lab2_code, language='python')
    
    st.markdown("### Lab 3: Dockerize (45 min)")
    lab3_code = '''# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

# Build and run
docker build -t ml-app .
docker run -p 8000:8000 ml-app'''
    st.code(lab3_code, language='dockerfile')
    
    st.markdown("### Lab 4: CI/CD Pipeline (45 min)")
    lab4_code = '''# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/
      
      - name: Train model
        run: python src/train.py
      
      - name: Validate model
        run: python src/validate.py
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t ml-app:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push ml-app:${{ github.sha }}'''
    st.code(lab4_code, language='yaml')
    
    st.markdown("### Lab 5: Testing ML Models (60 min)")
    lab5_code = '''import pytest
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

class TestMLModel:
    @pytest.fixture
    def model(self):
        """Load trained model"""
        return joblib.load('model.pkl')
    
    @pytest.fixture
    def sample_data(self):
        """Create sample test data"""
        return np.random.randn(10, 20)
    
    def test_model_loads(self, model):
        """Test model can be loaded"""
        assert model is not None
        assert isinstance(model, RandomForestClassifier)
    
    def test_prediction_shape(self, model, sample_data):
        """Test prediction output shape"""
        predictions = model.predict(sample_data)
        assert len(predictions) == len(sample_data)
    
    def test_prediction_range(self, model, sample_data):
        """Test predictions are in valid range"""
        predictions = model.predict(sample_data)
        assert all(p in [0, 1] for p in predictions)
    
    def test_probability_sum(self, model, sample_data):
        """Test probabilities sum to 1"""
        probs = model.predict_proba(sample_data)
        assert np.allclose(probs.sum(axis=1), 1.0)
    
    def test_feature_count(self, model, sample_data):
        """Test model expects correct number of features"""
        assert model.n_features_in_ == sample_data.shape[1]
    
    def test_deterministic(self, model, sample_data):
        """Test predictions are deterministic"""
        pred1 = model.predict(sample_data)
        pred2 = model.predict(sample_data)
        assert np.array_equal(pred1, pred2)

# Run tests
# pytest test_model.py -v'''
    st.code(lab5_code, language='python')
    
    st.markdown("### Lab 6: Model Versioning & Rollback (60 min)")
    lab6_code = '''import joblib
import json
from datetime import datetime
import shutil
import os

class ModelRegistry:
    def __init__(self, registry_path="model_registry"):
        self.registry_path = registry_path
        os.makedirs(registry_path, exist_ok=True)
        self.metadata_file = os.path.join(registry_path, "registry.json")
        self.load_registry()
    
    def load_registry(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {'models': [], 'current': None}
    
    def save_registry(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def register_model(self, model, version, metrics, description=""):
        """Register a new model version"""
        model_path = os.path.join(self.registry_path, f"model_v{version}.pkl")
        joblib.dump(model, model_path)
        
        model_info = {
            'version': version,
            'path': model_path,
            'metrics': metrics,
            'description': description,
            'registered_at': datetime.now().isoformat(),
            'status': 'registered'
        }
        
        self.registry['models'].append(model_info)
        self.save_registry()
        
        print(f"✅ Registered model v{version}")
        print(f"   Metrics: {metrics}")
    
    def promote_to_production(self, version):
        """Promote a model version to production"""
        model_info = next((m for m in self.registry['models'] if m['version'] == version), None)
        
        if not model_info:
            print(f"❌ Model v{version} not found")
            return
        
        # Backup current production model
        if self.registry['current']:
            old_version = self.registry['current']
            print(f"📦 Backing up current production model (v{old_version})")
        
        # Promote new model
        self.registry['current'] = version
        model_info['status'] = 'production'
        
        # Copy to production path
        prod_path = os.path.join(self.registry_path, "production_model.pkl")
        shutil.copy(model_info['path'], prod_path)
        
        self.save_registry()
        print(f"✅ Promoted v{version} to production")
    
    def rollback(self):
        """Rollback to previous production model"""
        if not self.registry['current']:
            print("❌ No production model to rollback from")
            return
        
        current_version = self.registry['current']
        
        # Find previous production model
        prod_models = [m for m in self.registry['models'] if m['status'] == 'production']
        if len(prod_models) < 2:
            print("❌ No previous production model available")
            return
        
        # Get second-to-last production model
        previous = prod_models[-2]
        
        print(f"⚠️ Rolling back from v{current_version} to v{previous['version']}")
        self.promote_to_production(previous['version'])
    
    def list_models(self):
        """List all registered models"""
        print("\n📊 Registered Models:")
        for model in self.registry['models']:
            status = "🟢 PROD" if model['version'] == self.registry['current'] else "⚪️"
            print(f"  {status} v{model['version']}: {model['metrics']} - {model['description']}")

# Example usage
registry = ModelRegistry()

# Register multiple versions
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, random_state=42)

# Version 1
model_v1 = RandomForestClassifier(n_estimators=50, random_state=42)
model_v1.fit(X, y)
registry.register_model(model_v1, "1.0.0", {"accuracy": 0.82}, "Initial model")

# Version 2
model_v2 = RandomForestClassifier(n_estimators=100, random_state=42)
model_v2.fit(X, y)
registry.register_model(model_v2, "2.0.0", {"accuracy": 0.85}, "Improved model")

# Promote v2 to production
registry.promote_to_production("2.0.0")

# List all models
registry.list_models()

# Rollback if needed
# registry.rollback()'''
    st.code(lab6_code, language='python')
    
    st.markdown("### Lab 7: Blue-Green Deployment (45 min)")
    lab7_code = '''class BlueGreenDeployment:
    def __init__(self):
        self.blue_model = None
        self.green_model = None
        self.active = 'blue'  # Which environment is serving traffic
    
    def deploy_to_green(self, new_model):
        """Deploy new model to green environment"""
        print("🟢 Deploying to GREEN environment...")
        self.green_model = new_model
        print("✅ GREEN deployment complete")
    
    def run_smoke_tests(self, environment='green'):
        """Run smoke tests on specified environment"""
        model = self.green_model if environment == 'green' else self.blue_model
        
        print(f"\n🧪 Running smoke tests on {environment.upper()}...")
        
        # Test 1: Model loads
        assert model is not None, "Model not loaded"
        print("✅ Model loads successfully")
        
        # Test 2: Predictions work
        import numpy as np
        test_data = np.random.randn(10, 20)
        predictions = model.predict(test_data)
        assert len(predictions) == 10, "Prediction count mismatch"
        print("✅ Predictions working")
        
        # Test 3: Response time
        import time
        start = time.time()
        _ = model.predict(test_data)
        latency = (time.time() - start) * 1000
        assert latency < 100, f"Latency too high: {latency:.0f}ms"
        print(f"✅ Latency acceptable: {latency:.0f}ms")
        
        print(f"\n✅ All smoke tests passed for {environment.upper()}")
        return True
    
    def switch_traffic(self):
        """Switch traffic from blue to green"""
        if self.active == 'blue':
            print("\n🔄 Switching traffic: BLUE → GREEN")
            self.active = 'green'
            self.blue_model = self.green_model  # Update blue to match green
        else:
            print("\n🔄 Switching traffic: GREEN → BLUE")
            self.active = 'blue'
        
        print(f"✅ Traffic now on {self.active.upper()}")
    
    def rollback(self):
        """Instant rollback to previous version"""
        print("\n⚠️ ROLLBACK initiated!")
        self.switch_traffic()
        print("✅ Rollback complete - serving previous version")

# Example deployment
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, random_state=42)

# Initial deployment (blue)
deployment = BlueGreenDeployment()
blue_model = RandomForestClassifier(n_estimators=50, random_state=42)
blue_model.fit(X, y)
deployment.blue_model = blue_model
print("🔵 BLUE environment serving traffic")

# Deploy new version to green
green_model = RandomForestClassifier(n_estimators=100, random_state=42)
green_model.fit(X, y)
deployment.deploy_to_green(green_model)

# Test green environment
if deployment.run_smoke_tests('green'):
    # Switch traffic
    deployment.switch_traffic()
    print("\n✅ Deployment successful!")
else:
    print("\n❌ Tests failed - keeping BLUE active")'''
    st.code(lab7_code, language='python')
    
    st.markdown("### Lab 8: Kubernetes Deployment (90 min)")
    lab8_code = '''# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-deployment
  labels:
    app: ml-model
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
      - name: ml-model
        image: myregistry/ml-model:v1.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: MODEL_PATH
          value: "/app/models/model.pkl"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-model
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

# Deploy commands:
# kubectl apply -f deployment.yaml
# kubectl get pods
# kubectl get services
# kubectl logs -f deployment/ml-model-deployment
# kubectl scale deployment ml-model-deployment --replicas=5
# kubectl rollout status deployment/ml-model-deployment
# kubectl rollout undo deployment/ml-model-deployment  # Rollback'''
    st.code(lab8_code, language='yaml')
    
    st.markdown("### Lab 9: API Gateway & Load Balancing (60 min)")
    lab9_code = '''from flask import Flask, request, jsonify
import joblib
import numpy as np
import time
from functools import wraps

app = Flask(__name__)

# Load model
model = joblib.load('model.pkl')

# Rate limiting
request_counts = {}
RATE_LIMIT = 100  # requests per minute

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        current_minute = int(time.time() / 60)
        key = f"{client_ip}_{current_minute}"
        
        request_counts[key] = request_counts.get(key, 0) + 1
        
        if request_counts[key] > RATE_LIMIT:
            return jsonify({
                'error': 'Rate limit exceeded',
                'limit': RATE_LIMIT,
                'retry_after': 60
            }), 429
        
        return f(*args, **kwargs)
    return decorated_function

# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

# Readiness check
@app.route('/ready', methods=['GET'])
def ready():
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({'ready': False, 'reason': 'Model not loaded'}), 503
        return jsonify({'ready': True})
    except Exception as e:
        return jsonify({'ready': False, 'reason': str(e)}), 503

# Prediction endpoint with rate limiting
@app.route('/predict', methods=['POST'])
@rate_limit
def predict():
    try:
        # Validate request
        if not request.json:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Extract features
        features = request.json.get('features')
        if features is None:
            return jsonify({'error': 'Missing features field'}), 400
        
        # Convert to numpy array
        X = np.array(features).reshape(1, -1)
        
        # Predict
        start_time = time.time()
        prediction = model.predict(X)[0]
        prediction_proba = model.predict_proba(X)[0].tolist()
        latency = (time.time() - start_time) * 1000
        
        return jsonify({
            'prediction': int(prediction),
            'probabilities': prediction_proba,
            'latency_ms': round(latency, 2),
            'model_version': '1.0'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Batch prediction
@app.route('/predict/batch', methods=['POST'])
@rate_limit
def predict_batch():
    try:
        data = request.json.get('batch')
        if not data:
            return jsonify({'error': 'No batch data provided'}), 400
        
        X = np.array(data)
        predictions = model.predict(X).tolist()
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({
        'total_requests': sum(request_counts.values()),
        'active_clients': len(request_counts)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

# nginx.conf for load balancing
# upstream ml_backend {
#     least_conn;
#     server ml-api-1:8000 weight=3;
#     server ml-api-2:8000 weight=2;
#     server ml-api-3:8000 weight=1;
# }
# 
# server {
#     listen 80;
#     location / {
#         proxy_pass http://ml_backend;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#     }
# }'''
    st.code(lab9_code, language='python')
    
    st.markdown("### 🎯 Deployment Best Practices")
    st.markdown("""**Production Deployment Checklist:**
✅ Requirements.txt with pinned versions
✅ Comprehensive unit tests
✅ Docker containerization
✅ CI/CD pipeline configured
✅ Model versioning system
✅ Blue-green deployment strategy
✅ Kubernetes orchestration
✅ Health checks implemented
✅ Auto-scaling configured
✅ Rollback procedures documented""")
    
    st.success("✅ Unit 5 Labs Complete: ML deployment pipeline mastered!")


def _render_unit6_labs():
    """Labs for Unit 6: MLOps & Monitoring"""
    st.markdown("---")
    st.markdown("## 🧪 HANDS-ON LABS: Unit 6")
    
    st.markdown("### Lab 1: MLflow Tracking (60 min)")
    lab1_code = '''import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

mlflow.set_experiment("my_experiment")

with mlflow.start_run(run_name="rf_model"):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", model.score(X_test, y_test))
    mlflow.sklearn.log_model(model, "model")
    
print("Run: mlflow ui to view results")'''
    st.code(lab1_code, language='python')
    
    st.markdown("### Lab 2: Data Drift Detection (60 min)")
    lab2_code = '''from scipy.stats import ks_2samp
import pandas as pd
import numpy as np

def detect_drift(train_data, prod_data, threshold=0.05):
    drift_report = {}
    for col in train_data.columns:
        if train_data[col].dtype in ['float64', 'int64']:
            stat, p_value = ks_2samp(train_data[col], prod_data[col])
            drift_report[col] = {
                'p_value': p_value,
                'drift': p_value < threshold
            }
    return drift_report

# Example
train = pd.DataFrame(np.random.randn(1000, 5))
prod = pd.DataFrame(np.random.randn(1000, 5) + 0.5)  # Shifted

report = detect_drift(train, prod)
for col, result in report.items():
    status = "⚠️ DRIFT" if result['drift'] else "✅ OK"
    print(f"{col}: {status}")'''
    st.code(lab2_code, language='python')
    
    st.markdown("### Lab 3: Production Monitoring Dashboard (60 min)")
    lab3_code = '''import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.title("📊 ML Model Monitoring Dashboard")

# Simulate metrics
np.random.seed(42)
dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
metrics_df = pd.DataFrame({
    'date': dates,
    'accuracy': np.random.normal(0.85, 0.02, 30),
    'latency_ms': np.random.normal(50, 10, 30),
    'throughput': np.random.normal(1000, 100, 30),
    'error_rate': np.random.normal(0.02, 0.01, 30)
})

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    current_acc = metrics_df['accuracy'].iloc[-1]
    st.metric(
        "Accuracy",
        f"{current_acc:.1%}",
        f"{(current_acc - 0.85)*100:.1f}%"
    )

with col2:
    current_latency = metrics_df['latency_ms'].iloc[-1]
    st.metric(
        "Latency",
        f"{current_latency:.0f}ms",
        f"{current_latency - 50:.0f}ms"
    )

with col3:
    current_throughput = metrics_df['throughput'].iloc[-1]
    st.metric(
        "Throughput",
        f"{current_throughput:.0f}/s",
        f"{current_throughput - 1000:.0f}"
    )

with col4:
    current_error = metrics_df['error_rate'].iloc[-1]
    st.metric(
        "Error Rate",
        f"{current_error:.1%}",
        f"{(current_error - 0.02)*100:.1f}%",
        delta_color="inverse"
    )

# Charts
st.markdown("### Performance Trends")

fig1 = px.line(metrics_df, x='date', y='accuracy', title='Model Accuracy Over Time')
fig1.add_hline(y=0.80, line_dash="dash", line_color="red", annotation_text="Threshold")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(metrics_df, x='date', y='latency_ms', title='Response Latency')
fig2.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="SLA")
st.plotly_chart(fig2, use_container_width=True)

# Alerts
st.markdown("### ⚠️ Active Alerts")
if current_acc < 0.80:
    st.error("🔴 CRITICAL: Accuracy below threshold")
if current_latency > 100:
    st.warning("🟡 WARNING: High latency detected")
if current_error > 0.05:
    st.error("🔴 CRITICAL: Error rate too high")

if current_acc >= 0.80 and current_latency <= 100 and current_error <= 0.05:
    st.success("✅ All systems operational")'''
    st.code(lab3_code, language='python')
    
    st.markdown("### Lab 4: A/B Testing for Models (60 min)")
    lab4_code = '''import numpy as np
from scipy import stats
import pandas as pd

class ModelABTest:
    def __init__(self, model_a, model_b, name_a="Model A", name_b="Model B"):
        self.model_a = model_a
        self.model_b = model_b
        self.name_a = name_a
        self.name_b = name_b
        self.results_a = []
        self.results_b = []
    
    def assign_traffic(self, user_id, split=0.5):
        """Randomly assign user to model A or B"""
        # Use hash for consistent assignment
        hash_val = hash(str(user_id)) % 100
        return 'A' if hash_val < split * 100 else 'B'
    
    def log_prediction(self, user_id, features, actual_outcome):
        """Log prediction and actual outcome"""
        variant = self.assign_traffic(user_id)
        
        if variant == 'A':
            prediction = self.model_a.predict([features])[0]
            self.results_a.append({
                'user_id': user_id,
                'prediction': prediction,
                'actual': actual_outcome,
                'correct': prediction == actual_outcome
            })
        else:
            prediction = self.model_b.predict([features])[0]
            self.results_b.append({
                'user_id': user_id,
                'prediction': prediction,
                'actual': actual_outcome,
                'correct': prediction == actual_outcome
            })
    
    def analyze_results(self, min_samples=100):
        """Analyze A/B test results"""
        if len(self.results_a) < min_samples or len(self.results_b) < min_samples:
            print(f"⚠️ Not enough samples yet (A: {len(self.results_a)}, B: {len(self.results_b)})")
            return None
        
        df_a = pd.DataFrame(self.results_a)
        df_b = pd.DataFrame(self.results_b)
        
        accuracy_a = df_a['correct'].mean()
        accuracy_b = df_b['correct'].mean()
        
        # Statistical test
        successes_a = df_a['correct'].sum()
        successes_b = df_b['correct'].sum()
        n_a = len(df_a)
        n_b = len(df_b)
        
        # Two-proportion z-test
        p_pooled = (successes_a + successes_b) / (n_a + n_b)
        se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_a + 1/n_b))
        z_score = (accuracy_a - accuracy_b) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        print(f"\n📊 A/B Test Results:")
        print(f"\n{self.name_a}:")
        print(f"  Samples: {n_a}")
        print(f"  Accuracy: {accuracy_a:.3f}")
        
        print(f"\n{self.name_b}:")
        print(f"  Samples: {n_b}")
        print(f"  Accuracy: {accuracy_b:.3f}")
        
        print(f"\nStatistical Test:")
        print(f"  Difference: {abs(accuracy_a - accuracy_b):.3f}")
        print(f"  Z-score: {z_score:.3f}")
        print(f"  P-value: {p_value:.4f}")
        
        if p_value < 0.05:
            winner = self.name_a if accuracy_a > accuracy_b else self.name_b
            print(f"\n✅ Statistically significant! Winner: {winner}")
        else:
            print(f"\n❌ No significant difference (p >= 0.05)")
        
        return {
            'accuracy_a': accuracy_a,
            'accuracy_b': accuracy_b,
            'p_value': p_value,
            'significant': p_value < 0.05
        }

# Example
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

# Two models
model_a = RandomForestClassifier(n_estimators=50, random_state=42)
model_b = RandomForestClassifier(n_estimators=100, random_state=42)

model_a.fit(X[:800], y[:800])
model_b.fit(X[:800], y[:800])

# Run A/B test
ab_test = ModelABTest(model_a, model_b, "RF-50", "RF-100")

# Simulate traffic
for i in range(200):
    user_id = f"user_{i}"
    features = X[800 + i]
    actual = y[800 + i]
    ab_test.log_prediction(user_id, features, actual)

# Analyze
results = ab_test.analyze_results(min_samples=50)'''
    st.code(lab4_code, language='python')
    
    st.markdown("### Lab 5: Automated Retraining Pipeline (75 min)")
    lab5_code = '''import mlflow
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import schedule
import time

class AutoRetrainingPipeline:
    def __init__(self, model_name, performance_threshold=0.80):
        self.model_name = model_name
        self.performance_threshold = performance_threshold
        self.current_model = None
        self.current_performance = None
    
    def check_performance_degradation(self, recent_predictions, recent_actuals):
        """Check if model performance has degraded"""
        if len(recent_predictions) < 100:
            return False, "Not enough data"
        
        current_accuracy = accuracy_score(recent_actuals, recent_predictions)
        
        if current_accuracy < self.performance_threshold:
            return True, f"Performance degraded: {current_accuracy:.3f} < {self.performance_threshold}"
        
        return False, f"Performance OK: {current_accuracy:.3f}"
    
    def fetch_new_data(self):
        """Fetch new training data (simulated)"""
        # In production, this would fetch from your data warehouse
        from sklearn.datasets import make_classification
        X, y = make_classification(n_samples=1000, n_features=20, random_state=int(time.time()))
        return X, y
    
    def train_new_model(self, X_train, y_train):
        """Train a new model version"""
        print(f"\n🔄 Training new model version...")
        
        with mlflow.start_run(run_name=f"{self.model_name}_retrain_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Train
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate
            train_score = model.score(X_train, y_train)
            
            # Log
            mlflow.log_param("retrain_timestamp", datetime.now().isoformat())
            mlflow.log_metric("train_accuracy", train_score)
            mlflow.sklearn.log_model(model, "model")
            
            print(f"✅ New model trained: {train_score:.3f} accuracy")
            
            return model, train_score
    
    def validate_new_model(self, new_model, X_val, y_val):
        """Validate new model before deployment"""
        new_score = new_model.score(X_val, y_val)
        
        if self.current_performance is None:
            return True, "First model"
        
        if new_score > self.current_performance:
            return True, f"Improvement: {new_score:.3f} > {self.current_performance:.3f}"
        else:
            return False, f"No improvement: {new_score:.3f} <= {self.current_performance:.3f}"
    
    def deploy_model(self, model, performance):
        """Deploy new model to production"""
        self.current_model = model
        self.current_performance = performance
        print(f"🚀 Model deployed with {performance:.3f} accuracy")
    
    def run_retraining_cycle(self):
        """Execute one retraining cycle"""
        print(f"\n{'='*60}")
        print(f"Retraining Cycle: {datetime.now()}")
        print(f"{'='*60}")
        
        # Fetch new data
        X_train, y_train = self.fetch_new_data()
        X_val, y_val = self.fetch_new_data()
        
        # Train new model
        new_model, train_score = self.train_new_model(X_train, y_train)
        
        # Validate
        should_deploy, reason = self.validate_new_model(new_model, X_val, y_val)
        
        if should_deploy:
            print(f"✅ Validation passed: {reason}")
            self.deploy_model(new_model, new_model.score(X_val, y_val))
        else:
            print(f"❌ Validation failed: {reason}")
            print("Keeping current model")
    
    def start_scheduled_retraining(self, interval_hours=24):
        """Start scheduled retraining"""
        print(f"🔄 Starting automated retraining every {interval_hours} hours")
        
        # Schedule retraining
        schedule.every(interval_hours).hours.do(self.run_retraining_cycle)
        
        # Run immediately
        self.run_retraining_cycle()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)

# Example usage
mlflow.set_experiment("auto_retraining")

pipeline = AutoRetrainingPipeline(
    model_name="churn_predictor",
    performance_threshold=0.80
)

# Run one cycle (in production, use start_scheduled_retraining)
pipeline.run_retraining_cycle()

print("\n✅ Automated retraining pipeline configured!")
print("In production: pipeline.start_scheduled_retraining(interval_hours=24)")'''
    st.code(lab5_code, language='python')
    
    st.markdown("### 🎯 MLOps Best Practices")
    st.markdown("""**Production MLOps Checklist:**
✅ Experiment tracking (MLflow)
✅ Data drift monitoring
✅ Model performance dashboards
✅ A/B testing framework
✅ Automated alerts
✅ Incident response plan
✅ Model retraining pipeline
✅ Feature store
✅ Model registry
✅ Comprehensive logging""")
    
    st.success("✅ Unit 6 Labs Complete: Production monitoring mastered!")


def _render_unit7_labs():
    """Labs for Unit 7: Capstone Project"""
    st.markdown("---")
    st.markdown("## 🎯 Unit 7: Capstone Templates")
    
    st.markdown("### Template: Project Structure")
    template = '''capstone_project/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   └── 03_evaluation.ipynb
├── src/
│   ├── train.py
│   ├── predict.py
│   └── evaluate.py
├── models/
└── results/'''
    st.code(template, language='text')
    
    st.markdown("### Template: Training Script")
    train_code = '''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    # Load data
    df = pd.read_csv("data/processed/clean_data.csv")
    X = df.drop("target", axis=1)
    y = df["target"]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save
    joblib.dump(model, "models/model.pkl")
    print(f"Test Accuracy: {model.score(X_test, y_test):.3f}")

if __name__ == "__main__":
    main()'''
    st.code(train_code, language='python')
    
    st.markdown("## 🎯 Capstone Project Options")
    st.markdown("**Choose one of these comprehensive projects to demonstrate your ML skills:**")
    
    st.markdown("### Option 1: Customer Churn Prediction System")
    st.markdown("""**Objective:** Build an end-to-end churn prediction system with monitoring

**Requirements:**
- Data: Customer transactions, demographics, support tickets
- Model: Classification (Random Forest, XGBoost, or Neural Network)
- Features: RFM analysis, engagement metrics, support history
- Deployment: REST API with Docker
- Monitoring: Performance dashboard, drift detection
- A/B Testing: Compare model versions

**Deliverables:**
1. EDA notebook with insights
2. Feature engineering pipeline
3. Model training with MLflow tracking
4. Deployed API with health checks
5. Monitoring dashboard
6. Final report with business recommendations""")
    
    st.markdown("### Option 2: Demand Forecasting Pipeline")
    st.markdown("""**Objective:** Create a production forecasting system for retail/supply chain

**Requirements:**
- Data: Historical sales, inventory, promotions, weather
- Model: Time-series (ARIMA, Prophet, LSTM, or ensemble)
- Features: Lag features, rolling statistics, seasonality
- Deployment: Batch prediction pipeline
- Monitoring: Forecast accuracy tracking
- Automation: Scheduled retraining

**Deliverables:**
1. Time-series analysis notebook
2. Multiple model comparison
3. Production forecasting class
4. Automated pipeline with scheduling
5. Accuracy monitoring system
6. Business impact analysis""")
    
    st.markdown("### Option 3: Recommendation Engine")
    st.markdown("""**Objective:** Build a scalable recommendation system

**Requirements:**
- Data: User interactions, product catalog, ratings
- Model: Collaborative filtering, content-based, or hybrid
- Features: User embeddings, item similarity, interaction history
- Deployment: Real-time API with caching
- Monitoring: Click-through rate, conversion tracking
- A/B Testing: Compare recommendation strategies

**Deliverables:**
1. User behavior analysis
2. Multiple recommendation algorithms
3. Hybrid recommendation system
4. Scalable API with Redis caching
5. A/B testing framework
6. Performance metrics dashboard""")
    
    st.markdown("### Option 4: Fraud Detection System")
    st.markdown("""**Objective:** Real-time fraud detection with explainability

**Requirements:**
- Data: Transaction history, user profiles, device info
- Model: Anomaly detection + classification
- Features: Transaction patterns, velocity checks, network analysis
- Deployment: Low-latency API (<100ms)
- Monitoring: False positive/negative rates
- Explainability: SHAP values for decisions

**Deliverables:**
1. Fraud pattern analysis
2. Anomaly detection + supervised model
3. Real-time scoring API
4. Explainability dashboard
5. Alert system for high-risk transactions
6. Model performance report""")
    
    st.markdown("### Option 5: NLP Sentiment Analysis Platform")
    st.markdown("""**Objective:** Multi-class sentiment analysis with deployment

**Requirements:**
- Data: Customer reviews, social media, support tickets
- Model: BERT, RoBERTa, or custom transformer
- Features: Text embeddings, sentiment scores, topic modeling
- Deployment: Batch + real-time API
- Monitoring: Model drift on text data
- Visualization: Sentiment trends dashboard

**Deliverables:**
1. Text preprocessing pipeline
2. Fine-tuned transformer model
3. Deployed API with batch processing
4. Sentiment trends dashboard
5. Topic modeling analysis
6. Business insights report""")
    
    st.markdown("## 📝 Capstone Evaluation Rubric")
    st.markdown("""**Your capstone will be evaluated on:**

1. **Data Analysis (20%)**
   - Thorough EDA with visualizations
   - Data quality assessment
   - Feature importance analysis

2. **Model Development (25%)**
   - Multiple models compared
   - Proper train/validation/test split
   - Hyperparameter optimization
   - Cross-validation results

3. **Production Deployment (25%)**
   - Dockerized application
   - REST API with documentation
   - Error handling and logging
   - Health checks implemented

4. **MLOps & Monitoring (20%)**
   - Experiment tracking (MLflow)
   - Model versioning
   - Performance monitoring
   - Automated retraining or alerts

5. **Documentation (10%)**
   - Clear README with setup instructions
   - Code comments and docstrings
   - Architecture diagram
   - Business impact summary

**Bonus Points:**
- A/B testing implementation
- CI/CD pipeline
- Kubernetes deployment
- Advanced explainability (SHAP, LIME)""")
    
    st.success("✅ Choose your capstone project and build something amazing!")


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
        
        # Add labs for Unit 1
        _render_unit1_labs()

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
        
        # Add labs for Unit 2
        _render_unit2_labs()

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
        
        # Add labs for Unit 3
        _render_unit3_labs()

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

**Part A: Baseline Forecasts (30 min)**
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Generate sample sales data
np.random.seed(42)
dates = pd.date_range('2023-01-01', '2024-03-31', freq='D')
trend = np.linspace(100, 150, len(dates))
seasonality = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)  # Weekly
noise = np.random.normal(0, 5, len(dates))
sales = trend + seasonality + noise

df = pd.DataFrame({'date': dates, 'sales': sales})
df.set_index('date', inplace=True)

# Train/test split
train = df[:'2024-02-28']
test = df['2024-03-01':]

print(f"Train: {len(train)} days")
print(f"Test: {len(test)} days")

# Baseline 1: Naive forecast (last value)
naive_pred = [train['sales'].iloc[-1]] * len(test)

# Baseline 2: Seasonal naive (same day last week)
seasonal_naive_pred = train['sales'].iloc[-7:].values
seasonal_naive_pred = list(seasonal_naive_pred) * (len(test) // 7 + 1)
seasonal_naive_pred = seasonal_naive_pred[:len(test)]

# Baseline 3: Moving average
window = 7
ma_pred = [train['sales'].iloc[-window:].mean()] * len(test)

# Evaluate
baselines = {
    'Naive': naive_pred,
    'Seasonal Naive': seasonal_naive_pred,
    'Moving Avg (7d)': ma_pred
}

print("\nBaseline Performance:")
for name, pred in baselines.items():
    mae = mean_absolute_error(test['sales'], pred)
    rmse = np.sqrt(mean_squared_error(test['sales'], pred))
    print(f"  {name}: MAE={mae:.2f}, RMSE={rmse:.2f}")
```

**Part B: ARIMA Model (30 min)**
```python
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Check stationarity
adf_result = adfuller(train['sales'])
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.4f}")
if adf_result[1] < 0.05:
    print("✅ Series is stationary")
else:
    print("⚠️ Series is non-stationary - differencing needed")

# Plot ACF/PACF
fig, axes = plt.subplots(1, 2, figsize=(14, 4))
plot_acf(train['sales'], lags=30, ax=axes[0])
plot_pacf(train['sales'], lags=30, ax=axes[1])
plt.tight_layout()
plt.show()

# Fit ARIMA model
model = ARIMA(train['sales'], order=(1, 1, 1))  # (p, d, q)
model_fit = model.fit()

print("\nARIMA Model Summary:")
print(model_fit.summary())

# Forecast
arima_pred = model_fit.forecast(steps=len(test))
arima_mae = mean_absolute_error(test['sales'], arima_pred)
arima_rmse = np.sqrt(mean_squared_error(test['sales'], arima_pred))

print(f"\nARIMA Performance: MAE={arima_mae:.2f}, RMSE={arima_rmse:.2f}")
```

**Part C: Prophet for Trend + Seasonality (30 min)**
```python
from prophet import Prophet

# Prepare data for Prophet
df_prophet = train.reset_index().rename(columns={'date': 'ds', 'sales': 'y'})

# Fit Prophet model
model = Prophet(
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=False
)
model.fit(df_prophet)

# Create future dataframe
future = model.make_future_dataframe(periods=len(test), freq='D')
forecast = model.predict(future)

# Extract predictions for test period
prophet_pred = forecast.iloc[-len(test):]['yhat'].values
prophet_mae = mean_absolute_error(test['sales'], prophet_pred)
prophet_rmse = np.sqrt(mean_squared_error(test['sales'], prophet_pred))

print(f"Prophet Performance: MAE={prophet_mae:.2f}, RMSE={prophet_rmse:.2f}")

# Visualize all forecasts
plt.figure(figsize=(14, 6))
plt.plot(test.index, test['sales'], 'k-', label='Actual', linewidth=2)
plt.plot(test.index, naive_pred, '--', label='Naive')
plt.plot(test.index, arima_pred, '-', label='ARIMA')
plt.plot(test.index, prophet_pred, '-', label='Prophet')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.title('Forecast Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("\n- ☐ Built 5 baseline models")
print("- ☐ Fitted ARIMA with diagnostics")
print("- ☐ Implemented Prophet")
print("- ☐ Compared all forecasts")
```
"""
        )

        st.markdown("---")
        st.markdown("## Lab 2: ML for Time-Series (75 min)")
        st.markdown(
            """**Objective:** Use XGBoost with lag features

**Part A: Create Lag & Rolling Features (25 min)**
```python
import xgboost as xgb

def create_features(df, lags=[1, 2, 3, 7, 14], windows=[7, 14, 30]):
    df_features = df.copy()
    
    # Lag features
    for lag in lags:
        df_features[f'lag_{lag}'] = df_features['sales'].shift(lag)
    
    # Rolling window features
    for window in windows:
        df_features[f'rolling_mean_{window}'] = df_features['sales'].rolling(window).mean()
        df_features[f'rolling_std_{window}'] = df_features['sales'].rolling(window).std()
    
    # Time features
    df_features['day_of_week'] = df_features.index.dayofweek
    df_features['month'] = df_features.index.month
    df_features['day_of_month'] = df_features.index.day
    
    # Drop NaN rows
    df_features = df_features.dropna()
    
    return df_features

# Create features for train
train_features = create_features(train)

print(f"Original features: 1 (sales)")
print(f"Engineered features: {len(train_features.columns)}")
print(f"\nFeature columns: {train_features.columns.tolist()}")
```

**Part B: Train XGBoost Regressor (25 min)**
```python
# Prepare data
X_train = train_features.drop('sales', axis=1)
y_train = train_features['sales']

# Train XGBoost
model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

# Feature importance
importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("Top 10 Features:")
print(importance.head(10))

plt.figure(figsize=(10, 6))
plt.barh(importance['feature'][:10], importance['importance'][:10])
plt.xlabel('Importance')
plt.title('Feature Importance')
plt.gca().invert_yaxis()
plt.show()
```

**Part C: Multi-Step Ahead Forecasting (25 min)**
```python
# Recursive forecasting
def forecast_recursive(model, last_known, n_steps):
    forecasts = []
    current_data = last_known.copy()
    
    for step in range(n_steps):
        # Prepare features for next prediction
        X_next = current_data.drop('sales').values.reshape(1, -1)
        
        # Predict
        next_pred = model.predict(X_next)[0]
        forecasts.append(next_pred)
        
        # Update features (shift lags, update rolling stats)
        # Simplified: in practice, properly update all features
        current_data['sales'] = next_pred
    
    return forecasts

# Get last known state from training data
last_known = train_features.iloc[-1:]

# Forecast test period
xgb_predictions = []
for i in range(len(test)):
    # Use actual features from test set (in production, would use recursive)
    if i < len(test) - max(lags) - max(windows):
        # Create features for this test point
        test_window = pd.concat([train, test.iloc[:i+1]])
        test_features = create_features(test_window)
        if len(test_features) > 0:
            X_test = test_features.iloc[-1:].drop('sales', axis=1)
            pred = model.predict(X_test)[0]
            xgb_predictions.append(pred)

# Evaluate
if len(xgb_predictions) > 0:
    test_subset = test['sales'].iloc[:len(xgb_predictions)]
    xgb_mae = mean_absolute_error(test_subset, xgb_predictions)
    xgb_rmse = np.sqrt(mean_squared_error(test_subset, xgb_predictions))
    
    print(f"\nXGBoost Performance: MAE={xgb_mae:.2f}, RMSE={xgb_rmse:.2f}")
    
    plt.figure(figsize=(14, 6))
    plt.plot(test_subset.index, test_subset.values, 'k-', label='Actual', linewidth=2)
    plt.plot(test_subset.index, xgb_predictions, 'r-', label='XGBoost', linewidth=2)
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('XGBoost Forecast')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

print("\n- ☐ Created lag & rolling features")
print("- ☐ Trained XGBoost regressor")
print("- ☐ Multi-step forecasting")
```
"""
        )

        st.markdown("---")
        st.markdown("## Lab 3: Demand Forecasting Mini-Project (90 min)")
        st.markdown("**Objective:** Build production-ready demand forecasting system")
        
        st.markdown("### Part A: Load and Explore Retail Data (30 min)")
        st.code('''import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import matplotlib.pyplot as plt

# Simulate retail sales data
np.random.seed(42)
dates = pd.date_range('2022-01-01', '2024-03-31', freq='D')

# Components: base + trend + seasonality + noise
base = 1000
trend = np.linspace(0, 500, len(dates))
seasonality_yearly = 200 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
seasonality_weekly = 100 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
promotions = np.random.choice([0, 300], size=len(dates), p=[0.9, 0.1])
noise = np.random.normal(0, 50, len(dates))

demand = base + trend + seasonality_yearly + seasonality_weekly + promotions + noise

df_retail = pd.DataFrame({
    'date': dates,
    'demand': demand
})
df_retail.set_index('date', inplace=True)

print(df_retail.head())
print(f"\\nDate range: {df_retail.index.min()} to {df_retail.index.max()}")
print(f"Average daily demand: {df_retail['demand'].mean():.2f}")

# Visualize
plt.figure(figsize=(14, 6))
plt.plot(df_retail.index, df_retail['demand'])
plt.title('Retail Demand Over Time')
plt.xlabel('Date')
plt.ylabel('Demand')
plt.grid(True, alpha=0.3)
plt.show()
''', language='python')
        
        st.markdown("### Part B: Build ARIMA and Prophet Models (30 min)")
        st.code('''# Split data
train_retail = df_retail[:'2023-12-31']
test_retail = df_retail['2024-01-01':]

print(f"Train: {len(train_retail)} days")
print(f"Test: {len(test_retail)} days")

# ARIMA Model
model_arima = ARIMA(train_retail['demand'], order=(7, 1, 7))
model_arima_fit = model_arima.fit()
print("\\nARIMA Model Summary:")
print(model_arima_fit.summary())

# Forecast
arima_forecast = model_arima_fit.forecast(steps=len(test_retail))

# Prophet Model
df_prophet = train_retail.reset_index()
df_prophet.columns = ['ds', 'y']

model_prophet = Prophet(yearly_seasonality=True, weekly_seasonality=True)
model_prophet.fit(df_prophet)

future = model_prophet.make_future_dataframe(periods=len(test_retail))
prophet_forecast = model_prophet.predict(future)
prophet_forecast = prophet_forecast[['ds', 'yhat']].tail(len(test_retail))

print("\\nProphet forecast ready!")
''', language='python')
        
        st.markdown("### Part C: Evaluate and Deploy (30 min)")
        st.code('''from sklearn.metrics import mean_absolute_error, mean_squared_error

# Evaluate ARIMA
mae_arima = mean_absolute_error(test_retail['demand'], arima_forecast)
rmse_arima = np.sqrt(mean_squared_error(test_retail['demand'], arima_forecast))

# Evaluate Prophet
mae_prophet = mean_absolute_error(test_retail['demand'], prophet_forecast['yhat'])
rmse_prophet = np.sqrt(mean_squared_error(test_retail['demand'], prophet_forecast['yhat']))

print("Model Comparison:")
print(f"ARIMA  - MAE: {mae_arima:.2f}, RMSE: {rmse_arima:.2f}")
print(f"Prophet - MAE: {mae_prophet:.2f}, RMSE: {rmse_prophet:.2f}")

# Visualize forecasts
plt.figure(figsize=(14, 6))
plt.plot(test_retail.index, test_retail['demand'], 'k-', label='Actual', linewidth=2)
plt.plot(test_retail.index, arima_forecast, 'b--', label='ARIMA')
plt.plot(test_retail.index, prophet_forecast['yhat'].values, 'r--', label='Prophet')
plt.xlabel('Date')
plt.ylabel('Demand')
plt.title('Demand Forecast Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Save best model
import joblib
best_model = model_prophet if mae_prophet < mae_arima else model_arima_fit
joblib.dump(best_model, 'demand_forecast_model.pkl')
print("\\nBest model saved!")
''', language='python')
        
        st.success("✅ Lab 3 Complete: You've built a production-ready demand forecasting system!")

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
"""
        )
        
        st.markdown("#### 🚀 Deployment patterns")
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

**Part A: Create Dockerfile (30 min)**
```dockerfile
# Dockerfile for ML model serving
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and application code
COPY model.pkl .
COPY app.py .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.2
pandas==2.1.3
joblib==1.3.2
pydantic==2.5.0
```

**app.py (FastAPI Model Serving):**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI(title="ML Model API", version="1.0.0")

# Load model at startup
model = joblib.load('model.pkl')

class PredictionRequest(BaseModel):
    features: dict

class PredictionResponse(BaseModel):
    prediction: float
    probability: float

@app.get("/")
def root():
    return {"message": "ML Model API is running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        # Convert features to DataFrame
        df = pd.DataFrame([request.features])
        
        # Make prediction
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
        
        return PredictionResponse(
            prediction=float(prediction),
            probability=float(probability)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
def model_info():
    return {
        "model_type": type(model).__name__,
        "features": list(model.feature_names_in_) if hasattr(model, 'feature_names_in_') else []
    }
```

**Build and run:**
```bash
# Build image
docker build -t ml-model:v1 .

# Run container
docker run -d -p 8000:8000 --name ml-api ml-model:v1

# Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"features": {"age": 35, "income": 50000}}'
```

**Part B: Docker Compose Multi-Container (30 min)**
```yaml
# docker-compose.yml
version: '3.8'

services:
  ml-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_VERSION=v1
      - LOG_LEVEL=info
    volumes:
      - ./logs:/app/logs
    depends_on:
      - redis
    networks:
      - ml-network
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - ml-network
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    networks:
      - ml-network

volumes:
  redis-data:
  prometheus-data:

networks:
  ml-network:
    driver: bridge
```

**Enhanced app.py with caching:**
```python
import redis
import json
import hashlib

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Create cache key
    cache_key = hashlib.md5(
        json.dumps(request.features, sort_keys=True).encode()
    ).hexdigest()
    
    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return PredictionResponse(**json.loads(cached))
    
    # Make prediction
    df = pd.DataFrame([request.features])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    response = PredictionResponse(
        prediction=float(prediction),
        probability=float(probability)
    )
    
    # Cache result (1 hour TTL)
    redis_client.setex(cache_key, 3600, response.json())
    
    return response
```

**Start all services:**
```bash
docker-compose up -d
docker-compose logs -f ml-api
docker-compose ps
```

**Part C: Push to Registry (30 min)**
```bash
# Tag for Docker Hub
docker tag ml-model:v1 yourusername/ml-model:v1
docker tag ml-model:v1 yourusername/ml-model:latest

# Login and push
docker login
docker push yourusername/ml-model:v1
docker push yourusername/ml-model:latest

# Verify
docker pull yourusername/ml-model:v1
```

**Production deployment:**
```bash
# On production server
docker pull yourusername/ml-model:v1
docker run -d \\
  -p 80:8000 \\
  --name ml-api-prod \\
  --restart unless-stopped \\
  -e MODEL_VERSION=v1 \\
  yourusername/ml-model:v1
```

- ☐ Dockerized ML API with FastAPI
- ☐ Multi-container setup with Redis caching
- ☐ Pushed to Docker registry
- ☐ Production-ready deployment
"""
        )

        st.markdown("---")
        st.markdown("## Lab 2: GitHub Actions CI/CD (75 min)")
        st.markdown(
            """**Objective:** Automate testing and deployment

**Part A: Setup pytest for ML Code (25 min)**
```python
# tests/test_model.py
import pytest
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

@pytest.fixture
def model():
    return joblib.load('model.pkl')

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'age': [25, 35, 45],
        'income': [30000, 50000, 70000],
        'credit_score': [650, 720, 800]
    })

def test_model_loads(model):
    assert model is not None
    assert hasattr(model, 'predict')

def test_model_prediction_shape(model, sample_data):
    predictions = model.predict(sample_data)
    assert len(predictions) == len(sample_data)
    assert predictions.dtype in [np.int64, np.float64]

def test_model_probability(model, sample_data):
    probabilities = model.predict_proba(sample_data)
    assert probabilities.shape == (len(sample_data), 2)
    assert np.all((probabilities >= 0) & (probabilities <= 1))
    assert np.allclose(probabilities.sum(axis=1), 1.0)

def test_model_accuracy(model):
    # Load test set
    X_test = pd.read_csv('data/X_test.csv')
    y_test = pd.read_csv('data/y_test.csv').values.ravel()
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    assert accuracy > 0.75, f"Model accuracy {accuracy:.2f} below threshold"

def test_feature_names(model, sample_data):
    if hasattr(model, 'feature_names_in_'):
        assert list(model.feature_names_in_) == list(sample_data.columns)
```

**tests/test_api.py:**
```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict():
    response = client.post(
        "/predict",
        json={"features": {"age": 35, "income": 50000, "credit_score": 720}}
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert 0 <= data["probability"] <= 1

def test_model_info():
    response = client.get("/model/info")
    assert response.status_code == 200
    assert "model_type" in response.json()
```

**Run tests:**
```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=. --cov-report=html
```

**Part B: GitHub Actions Workflow (25 min)**
```yaml
# .github/workflows/ci-cd.yml
name: ML Model CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/ml-model:latest
          ${{ secrets.DOCKER_USERNAME }}/ml-model:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.PROD_HOST }}
        username: ${{ secrets.PROD_USER }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          docker pull ${{ secrets.DOCKER_USERNAME }}/ml-model:latest
          docker stop ml-api || true
          docker rm ml-api || true
          docker run -d -p 80:8000 \\
            --name ml-api \\
            --restart unless-stopped \\
            ${{ secrets.DOCKER_USERNAME }}/ml-model:latest
```

**Part C: Auto-Deploy Setup (25 min)**
```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches: [ develop ]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to staging
      run: |
        # Deploy to staging environment
        echo "Deploying to staging..."
```

**GitHub Secrets Setup:**
```
DOCKER_USERNAME
DOCKER_TOKEN
PROD_HOST
PROD_USER
SSH_KEY
```

**Branch protection rules:**
```yaml
# Configure in GitHub Settings > Branches
Protected branches:
- main:
  - Require pull request reviews
  - Require status checks (test, build)
  - Require branches to be up to date
```

**Workflow:**
```
1. Developer creates PR to main
2. GitHub Actions runs tests
3. Code review + approval
4. Merge to main triggers:
   a. Tests run again
   b. Docker image built and pushed
   c. Auto-deploy to production
5. Monitor deployment
```

- ☐ Comprehensive pytest suite
- ☐ GitHub Actions CI/CD pipeline
- ☐ Auto-deploy on merge
- ☐ Production deployment automated
"""
        )

        st.markdown("---")
        st.markdown("## 🧪 Labs for Unit 5: Packaging & Deployment")
        
        st.markdown("### Lab 1: Create requirements.txt and Virtual Environment (45 min)")
        st.code('''# Step 1: Create virtual environment
python -m venv ml_project_env

# Step 2: Activate it
# Windows:
ml_project_env\\Scripts\\activate
# Mac/Linux:
source ml_project_env/bin/activate

# Step 3: Install packages
pip install pandas scikit-learn matplotlib joblib

# Step 4: Generate requirements.txt
pip freeze > requirements.txt

# Step 5: Share with team - they can install with:
pip install -r requirements.txt
''', language='bash')
        
        st.markdown("### Lab 2: Package Your Model as a Python Module (60 min)")
        st.code('''# File structure:
# my_ml_package/
#   __init__.py
#   model.py
#   preprocessing.py
#   setup.py

# model.py
import joblib
import pandas as pd

class ChurnPredictor:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)
    
    def predict(self, features):
        """Predict churn probability"""
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        return self.model.predict_proba(features)[:, 1]
    
    def predict_batch(self, df):
        """Batch predictions"""
        return self.model.predict_proba(df)[:, 1]

# setup.py
from setuptools import setup, find_packages

setup(
    name="my_ml_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "joblib>=1.0.0"
    ]
)

# Install your package:
# pip install -e .
''', language='python')
        
        st.markdown("### Lab 3: Dockerize Your ML Application (75 min)")
        st.code('''# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
''', language='dockerfile')
        
        st.code('''# Build and run:
docker build -t ml-app .
docker run -p 8000:8000 ml-app

# Push to registry:
docker tag ml-app myregistry/ml-app:v1.0
docker push myregistry/ml-app:v1.0
''', language='bash')
        
        st.success("✅ Unit 5 Labs Complete: Your ML models are now packaged and deployable!")
        st.markdown("---")
        st.markdown("## 📊 Labs for Unit 6: MLOps & Monitoring")
        
        st.markdown("### Lab 1: Model Versioning with MLflow (60 min)")
        st.code('''import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

# Start MLflow tracking
mlflow.set_experiment("churn_prediction")

with mlflow.start_run(run_name="rf_v1"):
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    print(f"Model logged with accuracy: {accuracy:.3f}")

# View experiments:
# mlflow ui
# Then open http://localhost:5000
''', language='python')
        
        st.markdown("### Lab 2: Data Drift Detection (60 min)")
        st.code('''import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

def detect_drift(reference_data, current_data, threshold=0.05):
    """Detect distribution drift using Kolmogorov-Smirnov test"""
    drift_report = {}
    
    for column in reference_data.columns:
        if reference_data[column].dtype in [np.float64, np.int64]:
            statistic, p_value = ks_2samp(
                reference_data[column].dropna(),
                current_data[column].dropna()
            )
            
            drift_detected = p_value < threshold
            drift_report[column] = {
                'p_value': p_value,
                'drift_detected': drift_detected
            }
    
    return drift_report

# Example usage
reference = pd.read_csv('training_data.csv')
current = pd.read_csv('production_data_today.csv')

drift = detect_drift(reference, current)

for col, result in drift.items():
    if result['drift_detected']:
        print(f"\u26a0\ufe0f DRIFT DETECTED in {col}: p-value={result['p_value']:.4f}")
    else:
        print(f"\u2705 {col}: No drift (p-value={result['p_value']:.4f})")
''', language='python')
        
        st.markdown("### Lab 3: Production Monitoring Dashboard (90 min)")
        st.code('''import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.title("📊 ML Model Monitoring Dashboard")

# Load production logs
logs = pd.read_csv('production_logs.csv')
logs['timestamp'] = pd.to_datetime(logs['timestamp'])

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Predictions Today", f"{len(logs):,}")

with col2:
    avg_confidence = logs['confidence'].mean()
    st.metric("Avg Confidence", f"{avg_confidence:.2%}")

with col3:
    avg_latency = logs['latency_ms'].mean()
    st.metric("Avg Latency", f"{avg_latency:.0f}ms")

with col4:
    error_rate = (logs['error'].sum() / len(logs)) * 100
    st.metric("Error Rate", f"{error_rate:.2f}%")

# Prediction volume over time
fig = px.line(logs.groupby('timestamp').size().reset_index(name='count'),
              x='timestamp', y='count', title='Prediction Volume Over Time')
st.plotly_chart(fig)

# Confidence distribution
fig = px.histogram(logs, x='confidence', nbins=50,
                   title='Prediction Confidence Distribution')
st.plotly_chart(fig)

# Alerts
if error_rate > 5:
    st.error(f"⚠\ufe0f HIGH ERROR RATE: {error_rate:.2f}% (threshold: 5%)")

if avg_latency > 100:
    st.warning(f"⚠\ufe0f HIGH LATENCY: {avg_latency:.0f}ms (threshold: 100ms)")
''', language='python')
        
        st.success("✅ Unit 6 Labs Complete: You can now monitor and maintain production ML systems!")

    elif unit_number == 6:
        st.markdown("#### 📘 Why MLOps matters")
        st.markdown(
            """Machine learning in production requires **operational discipline**.
MLOps brings DevOps practices to ML:

- **Version control** for models, data, and code
- **Automated testing** for model quality
- **Continuous deployment** for rapid iteration
- **Monitoring** to detect issues early
- **Reproducibility** for debugging and compliance

This unit covers the essential MLOps practices for production ML systems.
"""
        )

        st.markdown("#### 🔄 Model Lifecycle Management")
        st.markdown(
            """**Managing models from training to retirement:**

**1. Experimentation Phase:**
- Track experiments with MLflow/Weights & Biases
- Version datasets and code
- Document hyperparameters and results

**2. Model Registry:**
- Register production-ready models
- Tag versions (staging, production, archived)
- Store model metadata and lineage

**3. Deployment:**
- A/B testing new models
- Canary deployments (gradual rollout)
- Blue-green deployments (instant switch)

**4. Monitoring:**
- Track prediction quality
- Detect data drift
- Monitor system performance

**5. Retraining:**
- Trigger on performance degradation
- Automate retraining pipelines
- Validate before deployment
"""
        )

        st.markdown("#### 📊 Monitoring Production ML")
        st.markdown(
            """**What to monitor in production:**

**Model Performance:**
- Prediction accuracy (if ground truth available)
- Confidence scores distribution
- Prediction drift over time

**Data Quality:**
- Missing values
- Out-of-range values
- Distribution shifts (data drift)
- Feature correlations

**System Metrics:**
- Prediction latency (p50, p95, p99)
- Throughput (predictions/second)
- Error rates
- Resource usage (CPU, memory)

**Business Metrics:**
- Impact on KPIs
- Cost per prediction
- User satisfaction
- Revenue impact
"""
        )

        st.markdown("#### 🚨 Handling Model Failures")
        st.markdown(
            """**Strategies for robust ML systems:**

**1. Graceful Degradation:**
- Fallback to simpler model
- Return cached predictions
- Use rule-based defaults

**2. Circuit Breakers:**
- Stop calling failing models
- Alert on-call engineers
- Automatic rollback

**3. Shadow Mode:**
- Run new model alongside old
- Compare predictions
- Deploy only if better

**4. Feature Store:**
- Consistent feature computation
- Cached features for low latency
- Feature versioning
"""
        )

    elif unit_number == 7:
        st.markdown("#### 📘 Capstone Project Overview")
        st.markdown(
            """**Build a complete end-to-end ML system** that demonstrates all skills
from Pathways 1, 2, and 3.

**Project Requirements:**

1. **Problem Definition**
   - Clear business objective
   - Success metrics defined
   - Stakeholder requirements

2. **Data Pipeline**
   - Data collection and validation
   - Feature engineering
   - Train/test/validation splits

3. **Model Development**
   - Multiple algorithms tested
   - Hyperparameter tuning
   - Cross-validation
   - Model selection with justification

4. **Deployment**
   - Packaged as Python module
   - Dockerized application
   - REST API or batch scoring

5. **Monitoring**
   - Logging predictions
   - Performance dashboard
   - Alerting system

6. **Documentation**
   - README with setup instructions
   - Model card (performance, limitations)
   - API documentation
   - Deployment guide
"""
        )

        st.markdown("#### 🎯 Suggested Capstone Projects")
        st.markdown(
            """**Choose one or design your own:**

**1. Customer Churn Prevention System**
- Predict which customers will churn
- Deploy as real-time API
- Monitor prediction quality
- A/B test retention strategies

**2. Demand Forecasting Platform**
- Multi-step time-series forecasting
- Handle seasonality and promotions
- Inventory optimization recommendations
- Automated retraining pipeline

**3. Fraud Detection System**
- Real-time transaction scoring
- Handle class imbalance
- Low-latency requirements (<100ms)
- Explainable predictions

**4. Recommendation Engine**
- Collaborative filtering
- Content-based recommendations
- Cold-start handling
- A/B testing framework

**5. Predictive Maintenance**
- Sensor data analysis
- Failure prediction
- Maintenance scheduling optimization
- Cost-benefit analysis
"""
        )

        st.markdown("#### 📋 Capstone Deliverables")
        st.markdown(
            """**What to submit:**

**1. Code Repository (GitHub)**
- Clean, documented code
- requirements.txt or pyproject.toml
- Dockerfile
- CI/CD configuration
- Tests (unit and integration)

**2. Model Artifacts**
- Trained model files
- Feature engineering pipeline
- Model metadata
- Performance benchmarks

**3. Documentation**
- Project README
- Model card
- API documentation
- Deployment guide
- Architecture diagram

**4. Presentation**
- Problem and solution overview
- Technical approach
- Results and impact
- Lessons learned
- Future improvements

**5. Demo**
- Working application
- Sample predictions
- Monitoring dashboard
- Live or recorded demo
"""
        )

        st.markdown("#### 🏆 Evaluation Criteria")
        st.markdown(
            """**Your capstone will be evaluated on:**

**Technical Excellence (40%)**
- Model performance
- Code quality
- System design
- Best practices followed

**Completeness (30%)**
- All requirements met
- Documentation complete
- Tests included
- Deployment working

**Innovation (15%)**
- Creative problem-solving
- Advanced techniques used
- Novel approaches

**Communication (15%)**
- Clear documentation
- Effective presentation
- Business impact articulated
- Technical decisions justified
"""
        )

        st.markdown("---")
        st.markdown("## 🚀 Capstone Project Resources")
        
        st.markdown("### Datasets for Capstone Projects")
        st.code('''# Recommended public datasets:

# 1. Customer Churn
# - Telco Customer Churn (Kaggle)
# - Bank Customer Churn (Kaggle)

# 2. Demand Forecasting
# - Store Sales Forecasting (Kaggle)
# - Walmart Sales (Kaggle)

# 3. Fraud Detection
# - Credit Card Fraud (Kaggle)
# - IEEE-CIS Fraud Detection (Kaggle)

# 4. Recommendations
# - MovieLens (GroupLens)
# - Amazon Product Reviews (Kaggle)

# 5. Predictive Maintenance
# - NASA Turbofan Engine Degradation
# - Microsoft Azure Predictive Maintenance
''', language='python')
        
        st.markdown("### Project Template Structure")
        st.code('''my_capstone_project/
├── README.md
├── requirements.txt
├── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_modeling.ipynb
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── load.py
│   │   └── preprocess.py
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── evaluate.py
│   └── api/
│       └── app.py
├── tests/
│   ├── test_data.py
│   ├── test_features.py
│   └── test_models.py
├── models/
│   └── model_v1.pkl
├── reports/
│   ├── model_card.md
│   └── figures/
└── deployment/
    ├── docker-compose.yml
    └── kubernetes/
''', language='text')
        
        st.success("✅ Unit 7: Ready to build your capstone project!")


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
            # Add executable code labs
            _render_unit1_labs()
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
            # Add executable code labs
            _render_unit2_labs()
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
            # Add executable code labs
            _render_unit3_labs()
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
            # Add executable code labs
            _render_unit4_labs()
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
            # Add executable code labs
            _render_unit5_labs()
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
            # Add executable code labs
            _render_unit6_labs()
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
            # Add executable code labs
            _render_unit7_labs()
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
