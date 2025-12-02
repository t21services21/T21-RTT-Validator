# This script will expand Unit 1 labs to ~400 lines
with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find Unit 1 labs function (starts at line 111, ends at line 196)
start_line = 110  # 0-indexed
end_line = 196

# New expanded content
expanded_unit1 = '''def _render_unit1_labs():
    """Labs for Unit 1: Advanced Feature Engineering - EXPANDED"""
    st.markdown("---")
    st.markdown("## 🧪 HANDS-ON LABS: Unit 1 - Production Feature Engineering")
    st.markdown("**Build production-ready feature pipelines with versioning and monitoring**")
    
    st.markdown("---")
    st.markdown("### Lab 1: Production Feature Store (120 min)")
    st.markdown("#### Part A: Feature Store with Versioning (40 min)")
    
    lab1a = """import pandas as pd
import sqlite3
from datetime import datetime
import hashlib
import json

class ProductionFeatureStore:
    def __init__(self, db_path="features.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        self.conn.execute(\"\"\"CREATE TABLE IF NOT EXISTS features (
            feature_id TEXT PRIMARY KEY,
            entity_id TEXT,
            feature_name TEXT,
            feature_value REAL,
            event_timestamp TEXT,
            created_timestamp TEXT,
            version TEXT,
            metadata TEXT
        )\"\"\")
        
        self.conn.execute(\"\"\"CREATE TABLE IF NOT EXISTS feature_definitions (
            feature_name TEXT PRIMARY KEY,
            description TEXT,
            data_type TEXT,
            source TEXT,
            owner TEXT
        )\"\"\")
        self.conn.commit()
    
    def register_feature(self, name, description, data_type, source, owner):
        self.conn.execute(
            "INSERT OR REPLACE INTO feature_definitions VALUES (?, ?, ?, ?, ?)",
            (name, description, data_type, source, owner)
        )
        self.conn.commit()
        print(f"✅ Registered: {name}")
    
    def write_features(self, entity_id, features, event_time=None, version="v1.0", metadata=None):
        if event_time is None:
            event_time = datetime.now()
        
        created_time = datetime.now().isoformat()
        
        for name, value in features.items():
            feature_id = hashlib.md5(
                f"{entity_id}_{name}_{event_time}_{created_time}".encode()
            ).hexdigest()
            
            meta_json = json.dumps(metadata) if metadata else None
            
            self.conn.execute(
                "INSERT INTO features VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (feature_id, entity_id, name, value, 
                 event_time.isoformat(), created_time, version, meta_json)
            )
        self.conn.commit()
    
    def read_features_point_in_time(self, entity_id, feature_names, as_of_time, version="v1.0"):
        results = {}
        for fname in feature_names:
            cursor = self.conn.execute(
                \"\"\"SELECT feature_value FROM features
                   WHERE entity_id = ? AND feature_name = ? 
                   AND version = ? AND event_timestamp <= ?
                   ORDER BY event_timestamp DESC LIMIT 1\"\"\",
                (entity_id, fname, version, as_of_time.isoformat())
            )
            row = cursor.fetchone()
            if row:
                results[fname] = row[0]
        return results

# Example
store = ProductionFeatureStore()

# Register features
store.register_feature(
    "total_purchases", 
    "Total customer purchases",
    "integer",
    "transactions table",
    "data-team"
)

# Write features with timestamps
from datetime import timedelta
base = datetime(2024, 1, 1)
for day in range(30):
    event_time = base + timedelta(days=day)
    store.write_features(
        "customer_123",
        {"total_purchases": 10 + day, "avg_order_value": 100.0 + day * 2},
        event_time=event_time,
        metadata={"pipeline": "daily", "day": day}
    )

print("✅ Wrote 30 days of history")

# Point-in-time read
as_of = datetime(2024, 1, 15)
features = store.read_features_point_in_time(
    "customer_123",
    ["total_purchases", "avg_order_value"],
    as_of
)
print(f"\\nFeatures as of {as_of.date()}: {features}")"""
    
    st.code(lab1a, language='python')
    
    st.markdown("#### Part B: Feature Validation (40 min)")
    lab1b = """import pandas as pd
import numpy as np

class FeatureValidator:
    def __init__(self):
        self.rules = {}
    
    def add_rule(self, feature, rule_type, **kwargs):
        if feature not in self.rules:
            self.rules[feature] = []
        self.rules[feature].append({'type': rule_type, 'params': kwargs})
    
    def validate(self, df):
        results = []
        for feature, rules in self.rules.items():
            if feature not in df.columns:
                results.append({
                    'feature': feature,
                    'rule': 'existence',
                    'passed': False,
                    'message': f"Missing: {feature}"
                })
                continue
            
            for rule in rules:
                result = self._check_rule(df[feature], rule)
                result['feature'] = feature
                results.append(result)
        
        return pd.DataFrame(results)
    
    def _check_rule(self, series, rule):
        rtype = rule['type']
        params = rule['params']
        
        if rtype == 'range':
            min_val = params.get('min', -np.inf)
            max_val = params.get('max', np.inf)
            passed = series.between(min_val, max_val).all()
            return {
                'rule': f'range({min_val},{max_val})',
                'passed': passed,
                'message': 'OK' if passed else 'Out of range'
            }
        
        elif rtype == 'not_null':
            passed = series.notna().all()
            return {
                'rule': 'not_null',
                'passed': passed,
                'message': 'OK' if passed else f'{series.isna().sum()} nulls'
            }
        
        elif rtype == 'unique':
            passed = series.nunique() == len(series)
            return {
                'rule': 'unique',
                'passed': passed,
                'message': 'OK' if passed else 'Duplicates found'
            }
        
        return {'rule': rtype, 'passed': False, 'message': 'Unknown rule'}

# Example
validator = FeatureValidator()
validator.add_rule('age', 'range', min=0, max=120)
validator.add_rule('age', 'not_null')
validator.add_rule('customer_id', 'unique')
validator.add_rule('total_purchases', 'range', min=0, max=10000)

# Test data
test_df = pd.DataFrame({
    'customer_id': ['C001', 'C002', 'C003'],
    'age': [25, 35, 150],  # One invalid
    'total_purchases': [10, 50, 100]
})

results = validator.validate(test_df)
print("\\n⚠️ Validation Results:")
print(results.to_string(index=False))

failures = results[~results['passed']]
if len(failures) > 0:
    print(f"\\n❌ {len(failures)} failures:")
    for _, row in failures.iterrows():
        print(f"  - {row['feature']}: {row['message']}")
else:
    print("\\n✅ All validations passed!")"""
    
    st.code(lab1b, language='python')
    
    st.markdown("#### Part C: Feature Drift Monitoring (40 min)")
    lab1c = """import pandas as pd
import numpy as np
from scipy import stats

class FeatureMonitor:
    def __init__(self):
        self.baselines = {}
    
    def set_baseline(self, feature_name, data):
        self.baselines[feature_name] = {
            'mean': data.mean(),
            'std': data.std(),
            'distribution': data.values
        }
    
    def check_drift(self, feature_name, current_data, threshold=0.05):
        if feature_name not in self.baselines:
            return {'error': 'No baseline'}
        
        baseline = self.baselines[feature_name]
        
        # KS test
        ks_stat, ks_pval = stats.ks_2samp(
            baseline['distribution'],
            current_data.values
        )
        
        # Mean shift
        current_mean = current_data.mean()
        mean_shift = abs(current_mean - baseline['mean']) / baseline['std']
        
        drift = ks_pval < threshold
        
        return {
            'feature': feature_name,
            'drift_detected': drift,
            'ks_pvalue': ks_pval,
            'baseline_mean': baseline['mean'],
            'current_mean': current_mean,
            'mean_shift_sigma': mean_shift,
            'alert': '🔴 CRITICAL' if ks_pval < 0.01 else '🟡 WARNING' if drift else '🟢 OK'
        }

# Example
monitor = FeatureMonitor()

# Set baseline
np.random.seed(42)
baseline = pd.Series(np.random.normal(100, 15, 1000))
monitor.set_baseline('customer_value', baseline)

# Check current (shifted)
current = pd.Series(np.random.normal(110, 20, 500))
result = monitor.check_drift('customer_value', current)

print("\\n📊 Drift Detection:")
print(f"Feature: {result['feature']}")
print(f"Alert: {result['alert']}")
print(f"Drift: {result['drift_detected']}")
print(f"p-value: {result['ks_pvalue']:.6f}")
print(f"Baseline mean: {result['baseline_mean']:.2f}")
print(f"Current mean: {result['current_mean']:.2f}")
print(f"Shift: {result['mean_shift_sigma']:.2f} sigma")"""
    
    st.code(lab1c, language='python')
    st.success("✅ Lab 1 Complete: Production feature store!")
    
    st.markdown("---")
    st.markdown("### Lab 2: Point-in-Time Correctness (90 min)")
    st.markdown("**Prevent data leakage with time-travel features**")
    
    lab2 = """import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TimeSeriesFeatureEngine:
    def __init__(self, transactions_df):
        self.transactions = transactions_df.copy()
        self.transactions['date'] = pd.to_datetime(self.transactions['date'])
    
    def compute_features_pit(self, customer_id, as_of_date, lookback_days=90):
        # Only use data BEFORE as_of_date
        cutoff = pd.to_datetime(as_of_date)
        lookback_start = cutoff - timedelta(days=lookback_days)
        
        customer_txns = self.transactions[
            (self.transactions['customer_id'] == customer_id) &
            (self.transactions['date'] < cutoff) &
            (self.transactions['date'] >= lookback_start)
        ]
        
        return {
            'as_of_date': as_of_date,
            'customer_id': customer_id,
            'total_transactions': len(customer_txns),
            'total_revenue': customer_txns['amount'].sum() if len(customer_txns) > 0 else 0,
            'avg_transaction': customer_txns['amount'].mean() if len(customer_txns) > 0 else 0,
            'days_since_last': (
                (cutoff - customer_txns['date'].max()).days 
                if len(customer_txns) > 0 else lookback_days
            )
        }
    
    def create_training_dataset(self, prediction_dates):
        rows = []
        for pred_date in prediction_dates:
            for cust_id in self.transactions['customer_id'].unique():
                features = self.compute_features_pit(cust_id, pred_date)
                rows.append(features)
        
        df = pd.DataFrame(rows)
        print(f"✅ Created {len(df)} training examples (point-in-time correct)")
        return df

# Generate synthetic data
np.random.seed(42)
transactions = []
for cust in range(1, 51):
    n_txns = np.random.randint(5, 30)
    for _ in range(n_txns):
        date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
        amount = np.random.lognormal(4, 1)
        transactions.append({
            'customer_id': cust,
            'date': date,
            'amount': amount
        })

txns_df = pd.DataFrame(transactions)

# Create engine
engine = TimeSeriesFeatureEngine(txns_df)

# Compute features for specific date
features = engine.compute_features_pit(
    customer_id=1,
    as_of_date=datetime(2023, 6, 1),
    lookback_days=90
)

print("\\n📅 Point-in-Time Features (Customer 1, as of 2023-06-01):")
for key, val in features.items():
    print(f"  {key}: {val}")

# Create training dataset
pred_dates = pd.date_range('2023-03-01', '2023-06-01', freq='MS')
training_df = engine.create_training_dataset(pred_dates)

print(f"\\n📊 Training Dataset: {training_df.shape}")
print(training_df.head())

print("\\n✅ Point-in-time correctness guaranteed:")
print("  - No future information leaked")
print("  - Safe for time-series CV")"""
    
    st.code(lab2, language='python')
    st.success("✅ Lab 2 Complete: Time-travel features!")
    
    st.markdown("---")
    st.success("✅✅✅ Unit 1 COMPLETE: Production-grade feature engineering!")


'''

# Replace old Unit 1 with expanded version
new_lines = lines[:start_line] + [expanded_unit1 + '\n'] + lines[end_line:]

# Write back
with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"✅ Expanded Unit 1 labs from {end_line - start_line} lines to ~400 lines")
print(f"New total file lines: {len(new_lines)}")
