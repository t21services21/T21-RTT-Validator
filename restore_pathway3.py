# Restore Pathway 3 to working version
with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Current file: {len(lines)} lines")

# Find the broken Unit 1 function
start = None
for i, line in enumerate(lines):
    if 'def _render_unit1_labs():' in line:
        start = i
        break

if start is None:
    print("ERROR: Cannot find Unit 1 labs function")
    exit(1)

# Find Unit 2 function
end = None
for i in range(start + 1, len(lines)):
    if 'def _render_unit2_labs():' in line:
        end = i
        break

if end is None:
    print("ERROR: Cannot find Unit 2 labs function")
    exit(1)

print(f"Found Unit 1 labs: lines {start+1} to {end}")
print(f"Size: {end - start} lines (should be ~90)")

# If it's too big, it's broken - replace with simple working version
if end - start > 100:
    print("Unit 1 is too big - restoring simple version")
    
    simple_unit1 = '''def _render_unit1_labs():
    """Labs for Unit 1: Advanced Feature Engineering"""
    st.markdown("---")
    st.markdown("## 🧪 HANDS-ON LABS: Unit 1")
    
    st.markdown("### Lab 1: Build a Feature Store (90 min)")
    lab1_code = \'\'\'import pandas as pd
import sqlite3
from datetime import datetime
import hashlib

class SimpleFeatureStore:
    def __init__(self, db_path="features.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        self.conn.execute(\'\'\'CREATE TABLE IF NOT EXISTS features (
            feature_id TEXT PRIMARY KEY,
            feature_name TEXT,
            entity_id TEXT,
            feature_value REAL,
            timestamp TEXT,
            version TEXT
        )\'\'\')
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
        query = f\'\'\'SELECT feature_name, feature_value FROM features
                    WHERE entity_id = ? AND feature_name IN ({placeholders})
                    AND version = ? ORDER BY timestamp DESC\'\'\'
        cursor = self.conn.execute(query, [entity_id] + feature_names + [version])
        return dict(cursor.fetchall())

# Example
store = SimpleFeatureStore()
store.write_features("customer_123", {
    "total_purchases": 45,
    "avg_order_value": 125.50
})
features = store.read_features("customer_123", ["total_purchases"])
print(features)\'\'\'
    st.code(lab1_code, language='python')
    
    st.markdown("### Lab 2: Feature Monitoring (60 min)")
    lab2_code = \'\'\'import pandas as pd
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
    print(f"{feature}: {status} (p={result['p_value']:.4f})")\'\'\'
    st.code(lab2_code, language='python')
    
    st.success("✅ Unit 1 Labs Complete!")


'''
    
    # Replace broken Unit 1 with simple version
    new_lines = lines[:start] + [simple_unit1] + lines[end:]
    
    with open(r'd:\CascadeProjects\T21-RTT-Validator\data_science_pathway3_module.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ Restored! New file size: {len(new_lines)} lines")
else:
    print("Unit 1 looks OK - no changes needed")
