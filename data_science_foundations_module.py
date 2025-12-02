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

        st.markdown("---")
        st.markdown("#### 🌍 Real-World Data Science Applications")
        st.markdown(
            """**Healthcare:**
- Predict patient readmission risk → reduce hospital costs
- Identify disease patterns from medical records → improve diagnosis
- Optimize appointment scheduling → reduce wait times

**Finance:**
- Detect fraudulent transactions in real-time → save millions
- Predict loan default risk → smarter lending decisions
- Algorithmic trading → automated investment strategies

**Retail & E-Commerce:**
- Recommend products customers will love → increase sales
- Forecast demand for inventory optimization → reduce waste
- Customer churn prediction → targeted retention campaigns

**Manufacturing:**
- Predictive maintenance → prevent equipment failures
- Quality control using computer vision → reduce defects
- Supply chain optimization → faster delivery

**Government & Public Sector:**
- Crime prediction and resource allocation → safer communities
- Traffic flow optimization → reduce congestion
- Public health surveillance → early outbreak detection

**Marketing:**
- Customer segmentation for targeted campaigns → higher ROI
- A/B testing for website optimization → better conversion
- Sentiment analysis from social media → brand monitoring
"""
        )

        st.markdown("---")
        st.markdown("#### 🛠️ Essential Data Science Tools")
        st.markdown(
            """**Programming Languages:**
- **Python** 🐍 – Most popular for data science (90%+ of jobs)
- **R** 📊 – Strong for statistics and academic research
- **SQL** 🗄️ – Essential for working with databases

**Development Environments:**
- **Jupyter Notebooks** – Interactive coding for exploration
- **VS Code** – Professional IDE with Python extensions
- **Google Colab** – Free cloud notebooks with GPU access

**Key Python Libraries:**
- **Pandas** – Data manipulation and analysis
- **NumPy** – Numerical computing and arrays
- **Matplotlib/Seaborn** – Data visualization
- **Scikit-learn** – Machine learning algorithms
- **TensorFlow/PyTorch** – Deep learning frameworks

**Data Tools:**
- **Excel** – Still important for business users
- **Tableau/Power BI** – Business intelligence dashboards
- **Git/GitHub** – Version control for code
- **Docker** – Containerization for deployment

**You'll learn most of these throughout this pathway!**
"""
        )

        st.markdown("---")
        st.markdown("#### 💼 Career Paths & Salaries")
        st.markdown(
            """**Entry-Level (0-2 years):**
- **Junior Data Analyst:** £25K-35K (UK), $50K-70K (US)
- **Data Analyst:** £30K-45K (UK), $60K-80K (US)
- Skills: SQL, Excel, Python basics, dashboards

**Mid-Level (2-5 years):**
- **Data Scientist:** £45K-70K (UK), $90K-130K (US)
- **Analytics Engineer:** £50K-75K (UK), $95K-140K (US)
- Skills: Python, SQL, ML algorithms, statistics, communication

**Senior-Level (5-10 years):**
- **Senior Data Scientist:** £70K-100K (UK), $130K-180K (US)
- **ML Engineer:** £75K-110K (UK), $140K-200K (US)
- **Data Science Manager:** £80K-120K (UK), $150K-220K (US)

**Leadership (10+ years):**
- **Head of Data Science:** £100K-150K+ (UK), $200K-300K+ (US)
- **Chief Data Officer:** £120K-200K+ (UK), $250K-400K+ (US)

**High-demand skills that boost salary:**
- ✅ Cloud platforms (AWS, GCP, Azure)
- ✅ Deep learning & NLP
- ✅ MLOps & production deployment
- ✅ Domain expertise (finance, healthcare)
- ✅ Leadership & communication
"""
        )

        st.markdown("---")
        st.markdown("#### 📈 The Data Science Workflow")
        st.markdown(
            """**Real Example: Customer Churn Prediction**

**1. Business Understanding (Week 1)**
- Problem: 30% of customers leave each year
- Cost: £500 per customer to acquire, £50 to retain
- Goal: Predict who will churn, intervene early
- Success: Reduce churn by 10% → save £500K annually

**2. Data Understanding (Week 1-2)**
```python
import pandas as pd

# Load customer data
df = pd.read_csv('customers.csv')

print(f"Dataset: {len(df):,} customers")
print(f"Features: {df.columns.tolist()}")
print(f"Churn rate: {df['churned'].mean():.1%}")

# Missing values?
print(df.isnull().sum())

# Basic stats
print(df.describe())
```

**3. Data Preparation (Week 2-3)**
```python
# Handle missing values
df['income'].fillna(df['income'].median(), inplace=True)

# Create features
df['tenure_years'] = df['tenure_months'] / 12
df['avg_monthly_spend'] = df['total_spend'] / df['tenure_months']

# Encode categoricals
df = pd.get_dummies(df, columns=['region', 'product_type'])

# Split data
from sklearn.model_selection import train_test_split
X = df.drop('churned', axis=1)
y = df['churned']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

**4. Modeling (Week 3-4)**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance.head(10))
```

**5. Evaluation (Week 4)**
- Model accuracy: 85%
- Precision: 78% (of predicted churners, 78% actually churn)
- Recall: 72% (we catch 72% of actual churners)
- Business impact: Targeting top 20% → 15% churn reduction

**6. Deployment (Week 5+)**
- Deploy model to score customers monthly
- Marketing team targets high-risk customers
- Monitor: Is churn actually decreasing?
- Retrain quarterly with new data
"""
        )

        st.markdown("---")
        st.markdown("#### 🎯 Skills Matrix for Data Scientists")
        st.markdown(
            """**Technical Skills (60%):**
- Programming (Python, SQL): ⭐⭐⭐⭐⭐ Essential
- Statistics & Math: ⭐⭐⭐⭐⭐ Essential
- Machine Learning: ⭐⭐⭐⭐⭐ Essential
- Data Visualization: ⭐⭐⭐⭐ Very Important
- Big Data Tools: ⭐⭐⭐ Important
- Cloud Platforms: ⭐⭐⭐ Important
- Deep Learning: ⭐⭐ Nice to have

**Business Skills (20%):**
- Domain Knowledge: ⭐⭐⭐⭐ Very Important
- Problem Framing: ⭐⭐⭐⭐⭐ Essential
- ROI Calculation: ⭐⭐⭐⭐ Very Important
- Stakeholder Management: ⭐⭐⭐⭐ Very Important

**Soft Skills (20%):**
- Communication: ⭐⭐⭐⭐⭐ Essential
- Storytelling: ⭐⭐⭐⭐ Very Important
- Collaboration: ⭐⭐⭐⭐ Very Important
- Curiosity: ⭐⭐⭐⭐⭐ Essential
- Ethical Judgment: ⭐⭐⭐⭐⭐ Essential
"""
        )

        st.markdown("---")
        st.markdown("#### 🧪 HANDS-ON LABS: Unit 1")
        st.markdown(
            """**Complete these 3 labs to start your data science journey:**

---

## Lab 1: Environment Setup & First Analysis (60 min)

**Objective:** Set up your data science environment and perform your first analysis

**Part A: Install Python & Jupyter (20 min)**

**Step 1: Install Anaconda**
1. Download from: https://www.anaconda.com/download
2. Install with default settings
3. Verify installation:

```bash
# Open terminal/command prompt
python --version  # Should show Python 3.x
jupyter --version  # Should show Jupyter version
```

**Step 2: Create Your First Notebook**

```bash
# Create project folder
mkdir data_science_projects
cd data_science_projects

# Launch Jupyter
jupyter notebook
```

**Step 3: Test Installation**

```python
# In new notebook, test imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("✅ Environment ready!")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")
```

---

**Part B: First Data Analysis (40 min)**

**Download sample dataset (create CSV):**

```python
import pandas as pd
import numpy as np

# Generate sample e-commerce data
np.random.seed(42)
n = 1000

data = {
    'customer_id': range(1, n+1),
    'age': np.random.randint(18, 75, n),
    'monthly_spend': np.random.normal(150, 50, n),
    'website_visits': np.random.poisson(8, n),
    'purchases_last_month': np.random.poisson(2, n),
    'customer_since_months': np.random.randint(1, 60, n),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n),
    'churned': np.random.choice([0, 1], n, p=[0.75, 0.25])
}

df = pd.DataFrame(data)
df.to_csv('ecommerce_customers.csv', index=False)
print("✅ Dataset created: ecommerce_customers.csv")
```

**Now analyze it:**

```python
# Load data
df = pd.read_csv('ecommerce_customers.csv')

# 1. Basic info
print("Dataset shape:", df.shape)
print("\\nColumns:", df.columns.tolist())
print("\\nFirst 5 rows:")
print(df.head())

# 2. Summary statistics
print("\\nSummary statistics:")
print(df.describe())

# 3. Missing values?
print("\\nMissing values:")
print(df.isnull().sum())

# 4. Key business metrics
print("\\n📊 Business Metrics:")
print(f"Total customers: {len(df):,}")
print(f"Churn rate: {df['churned'].mean():.1%}")
print(f"Avg monthly spend: £{df['monthly_spend'].mean():.2f}")
print(f"Avg website visits: {df['website_visits'].mean():.1f}")

# 5. Segment by region
print("\\nCustomers by region:")
print(df['region'].value_counts())

# 6. Churn by region
print("\\nChurn rate by region:")
churn_by_region = df.groupby('region')['churned'].mean()
print(churn_by_region.sort_values(ascending=False))

# 7. Simple visualization
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Age distribution
axes[0].hist(df['age'], bins=20, edgecolor='black')
axes[0].set_title('Customer Age Distribution')
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Count')

# Spend by churn status
df[df['churned']==0]['monthly_spend'].hist(ax=axes[1], alpha=0.6, label='Retained', bins=20)
df[df['churned']==1]['monthly_spend'].hist(ax=axes[1], alpha=0.6, label='Churned', bins=20)
axes[1].set_title('Monthly Spend: Retained vs Churned')
axes[1].set_xlabel('Monthly Spend (£)')
axes[1].legend()

plt.tight_layout()
plt.show()
```

**Key Findings to Report:**
- Total customers and churn rate
- Average spend differs between churned and retained
- Regional differences in churn
- Age and visit patterns

---

**Lab 1 Checklist:**
- ☐ Anaconda installed successfully
- ☐ Jupyter notebook launched
- ☐ Sample dataset created
- ☐ Basic analysis completed
- ☐ Visualizations created
- ☐ Business metrics calculated

---

## Lab 2: Exploring Real Public Datasets (90 min)

**Objective:** Practice finding, loading, and exploring real-world datasets

**Part A: Find & Load Public Data (30 min)**

**Recommended data sources:**
1. **Kaggle** (www.kaggle.com/datasets) – 1000s of datasets
2. **UCI ML Repository** – Classic datasets
3. **Data.gov** – Government data (US/UK)
4. **Google Dataset Search** – Search engine for data

**Example: Titanic Dataset (Kaggle classic)**

```python
import pandas as pd

# Load Titanic data (download from Kaggle first)
# Or use this URL:
url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
titanic = pd.read_csv(url)

print("Dataset loaded!")
print(f"Shape: {titanic.shape}")
print(f"\\nColumns: {titanic.columns.tolist()}")
print(f"\\nFirst 3 rows:")
print(titanic.head(3))
```

---

**Part B: Exploratory Data Analysis (60 min)**

```python
# 1. Data Quality Assessment
print("="*60)
print("DATA QUALITY CHECK")
print("="*60)

# Missing values
print("\\nMissing values:")
missing = titanic.isnull().sum()
print(missing[missing > 0])

# Data types
print("\\nData types:")
print(titanic.dtypes)

# Unique values for categoricals
categorical_cols = ['Pclass', 'Sex', 'Embarked']
for col in categorical_cols:
    print(f"\\n{col}: {titanic[col].nunique()} unique values")
    print(titanic[col].value_counts())

# 2. Survival Analysis
print("\\n" + "="*60)
print("SURVIVAL ANALYSIS")
print("="*60)

survival_rate = titanic['Survived'].mean()
print(f"Overall survival rate: {survival_rate:.1%}")

# By gender
survival_by_gender = titanic.groupby('Sex')['Survived'].mean()
print("\\nSurvival by gender:")
print(survival_by_gender)

# By class
survival_by_class = titanic.groupby('Pclass')['Survived'].mean()
print("\\nSurvival by class:")
print(survival_by_class)

# By age group
titanic['AgeGroup'] = pd.cut(titanic['Age'], 
                              bins=[0, 18, 35, 60, 100],
                              labels=['Child', 'Young Adult', 'Adult', 'Senior'])
survival_by_age = titanic.groupby('AgeGroup')['Survived'].mean()
print("\\nSurvival by age group:")
print(survival_by_age)

# 3. Visualizations
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Survival by gender
survival_by_gender.plot(kind='bar', ax=axes[0, 0], color=['red', 'green'])
axes[0, 0].set_title('Survival Rate by Gender')
axes[0, 0].set_ylabel('Survival Rate')
axes[0, 0].set_ylim([0, 1])

# Survival by class
survival_by_class.plot(kind='bar', ax=axes[0, 1])
axes[0, 1].set_title('Survival Rate by Passenger Class')
axes[0, 1].set_ylabel('Survival Rate')
axes[0, 1].set_ylim([0, 1])

# Age distribution
axes[1, 0].hist(titanic['Age'].dropna(), bins=20, edgecolor='black')
axes[1, 0].set_title('Passenger Age Distribution')
axes[1, 0].set_xlabel('Age')
axes[1, 0].set_ylabel('Count')

# Fare distribution by class
for pclass in [1, 2, 3]:
    data = titanic[titanic['Pclass']==pclass]['Fare'].dropna()
    axes[1, 1].hist(data, alpha=0.5, label=f'Class {pclass}', bins=20)
axes[1, 1].set_title('Fare Distribution by Class')
axes[1, 1].set_xlabel('Fare (£)')
axes[1, 1].legend()

plt.tight_layout()
plt.show()

# 4. Key Insights Summary
print("\\n" + "="*60)
print("KEY INSIGHTS")
print("="*60)
print(f"1. Women had {survival_by_gender['female']/survival_by_gender['male']:.1f}x higher survival rate")
print(f"2. First class passengers had {survival_by_class[1]/survival_by_class[3]:.1f}x higher survival than third class")
print(f"3. {missing['Age']} passengers ({missing['Age']/len(titanic):.1%}) have missing age data")
print(f"4. Average fare: £{titanic['Fare'].mean():.2f}")
```

---

**Lab 2 Checklist:**
- ☐ Public dataset source identified
- ☐ Data loaded successfully
- ☐ Missing values analyzed
- ☐ Key patterns discovered
- ☐ Multiple visualizations created
- ☐ Business insights documented

---

## Lab 3: Formulate Business Questions (60 min)

**Objective:** Practice turning business problems into data science questions

**Part A: Healthcare Scenario (20 min)**

**Scenario:** You work for a hospital network with patient readmission data

**Available Data:**
- Patient demographics (age, gender, location)
- Admission history (dates, diagnosis codes, length of stay)
- Treatment records (procedures, medications)
- Readmission within 30 days (yes/no)

**Your Task: Formulate 5 data science questions**

```markdown
EXAMPLE QUESTIONS:

1. **PREDICTION:** Can we predict which patients are at high risk of 30-day readmission?
   - Target: readmitted (yes/no)
   - Features: age, diagnosis, prior admissions, length of stay
   - Business value: Proactive follow-up care reduces readmissions by 15%

2. **SEGMENTATION:** Are there distinct patient groups with different readmission patterns?
   - Method: Clustering analysis
   - Goal: Tailored intervention programs
   - Business value: More effective resource allocation

3. **OPTIMIZATION:** What factors most influence length of stay?
   - Method: Regression analysis
   - Goal: Reduce unnecessary hospital days
   - Business value: £500 saved per day reduced

4. **TREND ANALYSIS:** Are readmission rates increasing over time?
   - Method: Time series analysis
   - Goal: Early detection of systematic issues
   - Business value: Quality improvement initiatives

5. **ROOT CAUSE:** Which diagnoses have highest readmission rates?
   - Method: Descriptive statistics + visualization
   - Goal: Focus improvement efforts
   - Business value: Targeted clinical protocol updates
```

---

**Part B: Retail Scenario (20 min)**

**Scenario:** E-commerce company wants to reduce cart abandonment

**Your 5 Questions:**

```markdown
YOUR TURN - WRITE 5 QUESTIONS:

1. PREDICTION: Can we predict which shopping carts will be abandoned?

2. SEGMENTATION: _______________________________________

3. OPTIMIZATION: _______________________________________

4. TREND ANALYSIS: _______________________________________

5. ROOT CAUSE: _______________________________________
```

---

**Part C: Finance Scenario (20 min)**

**Scenario:** Bank wants to detect fraudulent transactions

**Your 5 Questions:**

```markdown
1. PREDICTION: _______________________________________

2. ANOMALY DETECTION: _______________________________________

3. PATTERN RECOGNITION: _______________________________________

4. RISK SCORING: _______________________________________

5. TREND ANALYSIS: _______________________________________
```

---

**Lab 3 Checklist:**
- ☐ Healthcare questions formulated (5)
- ☐ Retail questions formulated (5)
- ☐ Finance questions formulated (5)
- ☐ Each question linked to business value
- ☐ Target variables identified
- ☐ Potential features listed

---

**Next Steps:** Unit 2 teaches Python programming to answer these questions!
"""
        )

    elif unit_number == 2:
        st.markdown("---")
        st.markdown("#### 🐍 Why Python is THE Language for Data Science")
        st.markdown(
            """**Python dominates data science for good reasons.**

**Compared to other tools:**

| Feature | Python | R | Excel | SQL |
|---------|--------|---|-------|-----|
| Learning curve | Moderate | Steep | Easy | Moderate |
| Data size handling | Millions+ rows | Millions | Max ~1M | Unlimited |
| Statistical analysis | Excellent | Excellent | Limited | None |
| Machine learning | Best (scikit-learn) | Good | None | None |
| Data wrangling | Excellent (Pandas) | Excellent | Moderate | Excellent |
| Visualization | Excellent | Excellent | Good | None |
| Industry adoption | 80% of teams | 20% (academia) | 100% (basic) | 90% |
| Job postings | 70% | 15% | 40% | 85% |

**Bottom line:** **Python + SQL = Essential combo for data roles globally.**

---

### Getting Started

**Installation (Recommended):**
1. Download **Anaconda** (includes Python + Jupyter + 200+ packages)
2. Install from: anaconda.com/download
3. Launch Jupyter Notebook or VS Code
4. Ready to code!

**Alternative:** Google Colab (browser-based, no installation needed)

**Your First Python Script:**
```python
# This is a comment - Python ignores it
print("Hello, Data Science!")

# Calculate revenue
revenue = 150_000  # £150K (underscores for readability)
growth = 0.15      # 15% growth
next_year = revenue * (1 + growth)

print(f"Current: £{revenue:,}")
print(f"Next year: £{next_year:,.0f}")
```

**Output:**
```
Hello, Data Science!
Current: £150,000
Next year: £172,500
```

**You're already doing real calculations!**
"""
        )

        st.markdown("#### 📦 Data Types: The Building Blocks")
        st.markdown(
            """**Every piece of data has a type. Master these 5:**

---

**1. Numbers (int and float)**

```python
# Integers (whole numbers)
customer_count = 1_250
new_customers = 15

# Floats (decimals)
avg_order_value = 45.99
conversion_rate = 0.032  # 3.2%

# Arithmetic
total = customer_count + new_customers  # 1265

# Division types
print(10 / 3)   # 3.3333... (float)
print(10 // 3)  # 3 (integer division)
print(10 % 3)   # 1 (remainder/modulo)

# Rounding
price = 19.99
print(round(price))      # 20
print(round(price, 1))   # 20.0
```

---

**2. Strings (text)**

```python
# Create strings
customer_name = "John Smith"
product = 'Widget Pro'  # Single or double quotes

# String operations
email = customer_name.lower().replace(" ", ".") + "@company.com"
print(email)  # john.smith@company.com

# String methods
name.upper()          # JOHN SMITH
name.split()          # ['John', 'Smith']
name.startswith("J")  # True

# F-strings for formatting (Python 3.6+)
revenue = 1_500_000
print(f"Revenue: £{revenue:,}")           # £1,500,000
print(f"Revenue: £{revenue/1000:.1f}K")   # £1500.0K
```

**Common String Operations:**
- `text.strip()` - Remove spaces
- `text.split()` - Split into words
- `",".join(['a','b'])` - Join: "a,b"
- `"test" in text` - Check substring
- `len(text)` - Count characters

---

**3. Lists (ordered collections)**

```python
# Create lists
monthly_sales = [45_000, 52_000, 48_000, 61_000]
products = ["Widget", "Gadget", "Doohickey"]

# Access by index (starts at 0!)
first = monthly_sales[0]   # 45000
last = monthly_sales[-1]   # 61000 (negative = from end)

# Slicing (get range)
q1 = monthly_sales[0:3]    # [45000, 52000, 48000]
last_two = monthly_sales[-2:]  # [48000, 61000]

# Modify
monthly_sales.append(55_000)     # Add to end
monthly_sales.insert(0, 40_000)  # Insert at position
monthly_sales.remove(48_000)     # Remove value
monthly_sales.pop()              # Remove last

# Useful operations
total = sum(monthly_sales)
average = total / len(monthly_sales)
maximum = max(monthly_sales)
minimum = min(monthly_sales)
```

**List Comprehensions (Pythonic!):**
```python
# Traditional loop
squared = []
for num in [1, 2, 3, 4]:
    squared.append(num ** 2)

# List comprehension (same result, one line)
squared = [num ** 2 for num in [1, 2, 3, 4]]  # [1, 4, 9, 16]

# With condition
revenues = [45_000, 152_000, 38_000, 201_000]
big_deals = [r for r in revenues if r > 100_000]  # [152000, 201000]
```

---

**4. Dictionaries (key-value pairs)**

```python
# Create dictionary
customer = {
    "id": "C001",
    "name": "Acme Corporation",
    "revenue": 2_500_000,
    "industry": "Retail",
    "country": "UK"
}

# Access values
print(customer["name"])  # Acme Corporation
print(customer.get("email", "unknown@example.com"))  # Safe with default

# Modify
customer["revenue"] = 2_750_000           # Update
customer["email"] = "contact@acme.com"    # Add new

# Operations
keys = customer.keys()      # All keys
values = customer.values()  # All values
items = customer.items()    # (key, value) pairs

# Check if key exists
if "email" in customer:
    print(customer["email"])
```

**Real Example: Customer Database**
```python
customers = [
    {"id": "C001", "name": "Acme", "revenue": 2_500_000},
    {"id": "C002", "name": "Tech Ltd", "revenue": 150_000},
    {"id": "C003", "name": "Global Inc", "revenue": 4_000_000}
]

# Total revenue
total = sum(c["revenue"] for c in customers)
print(f"Total: £{total:,}")  # £6,650,000

# High-value customers
enterprise = [c for c in customers if c["revenue"] > 1_000_000]
print(f"Enterprise: {len(enterprise)}")  # 2
```

---

**5. Booleans (True/False)**

```python
is_active = True
has_email = False

# Comparisons return booleans
revenue = 150_000
is_enterprise = revenue > 1_000_000  # False

# Logical operators
is_qualified = is_active and has_email    # False (both must be True)
needs_followup = not has_email            # True (inverse)
is_target = is_active or has_email        # True (at least one)
```
"""
        )

        st.markdown("#### 🔀 Control Flow: Making Decisions")
        st.markdown(
            """**If/Elif/Else Statements**

```python
def categorize_customer(revenue):
    \"\"\"Segment customers by revenue tier\"\"\"
    if revenue > 1_000_000:
        return "Enterprise"
    elif revenue > 100_000:
        return "Mid-Market"
    elif revenue > 10_000:
        return "SMB"
    else:
        return "Startup"

# Test it
print(categorize_customer(2_500_000))  # Enterprise
print(categorize_customer(150_000))    # Mid-Market
print(categorize_customer(5_000))      # Startup
```

**Multiple Conditions:**
```python
def qualify_lead(revenue, industry, country):
    \"\"\"Check if lead matches target profile\"\"\"
    if revenue > 500_000 and industry in ["Tech", "Finance"]:
        if country in ["UK", "US", "Germany"]:
            return "High Priority"
        return "Medium Priority"
    elif revenue > 100_000:
        return "Low Priority"
    return "Not Qualified"

status = qualify_lead(750_000, "Tech", "UK")
print(status)  # High Priority
```

---

**For Loops: Repeat Actions**

```python
# Loop through list
revenues = [45_000, 152_000, 38_000, 201_000]
for revenue in revenues:
    segment = categorize_customer(revenue)
    print(f"£{revenue:,} → {segment}")

# Loop with index
for i, revenue in enumerate(revenues):
    print(f"Customer {i+1}: £{revenue:,}")

# Loop through range
for month in range(1, 13):  # 1 to 12
    print(f"Month {month}")

# Loop through dictionary
customer = {"name": "Acme", "revenue": 1_500_000}
for key, value in customer.items():
    print(f"{key}: {value}")
```

---

**While Loops: Repeat Until Condition**

```python
# Calculate years to reach target
revenue = 100_000
target = 1_000_000
growth = 0.15
years = 0

while revenue < target:
    revenue *= (1 + growth)
    years += 1

print(f"Reached £1M in {years} years")  # 16 years
```
"""
        )

        st.markdown("#### ⚙️ Functions: Reusable Code")
        st.markdown(
            """**Why Functions?**
- Write once, use many times
- Easier to test and debug
- Makes code readable
- Essential for data projects

**Basic Function:**
```python
def calculate_churn_rate(total_customers, churned):
    \"\"\"Calculate customer churn rate\"\"\"
    if total_customers == 0:
        return 0.0
    
    rate = (churned / total_customers) * 100
    return round(rate, 2)

# Usage
q1 = calculate_churn_rate(10_000, 1_200)
print(f"Q1 Churn: {q1}%")  # 12.0%

q2 = calculate_churn_rate(11_000, 950)
print(f"Q2 Churn: {q2}%")  # 8.64%
```

**Default Parameters:**
```python
def calculate_revenue(units, price=100, discount=0):
    \"\"\"Calculate revenue with optional discount\"\"\"
    gross = units * price
    net = gross * (1 - discount)
    return net

# Different ways to call
rev1 = calculate_revenue(150)                   # Uses defaults
rev2 = calculate_revenue(150, 120)              # Custom price
rev3 = calculate_revenue(150, 120, 0.10)        # 10% discount
rev4 = calculate_revenue(150, discount=0.15)    # Named param
```

**Multiple Return Values:**
```python
def analyze_revenue(revenues):
    \"\"\"Return min, max, avg, total\"\"\"
    total = sum(revenues)
    avg = total / len(revenues)
    return min(revenues), max(revenues), avg, total

monthly = [45_000, 52_000, 48_000, 61_000]
min_r, max_r, avg_r, total_r = analyze_revenue(monthly)

print(f"Min: £{min_r:,}, Max: £{max_r:,}")
print(f"Avg: £{avg_r:,.0f}, Total: £{total_r:,}")
```

**Docstrings (Documentation):**
```python
def calculate_ltv(avg_purchase, frequency, lifespan):
    \"\"\"
    Calculate Customer Lifetime Value
    
    Args:
        avg_purchase: Average purchase in £
        frequency: Purchases per year
        lifespan: Years as customer
        
    Returns:
        Lifetime value in £
        
    Example:
        >>> calculate_ltv(100, 4, 5)
        2000
    \"\"\"
    return avg_purchase * frequency * lifespan
```
"""
        )

        st.markdown("#### 📓 Working with Jupyter Notebooks")
        st.markdown(
            """**What is a Notebook?**
- Interactive document: code + text + visuals
- Run code in chunks (cells)
- Perfect for exploration and sharing

**Keyboard Shortcuts:**
- `Shift + Enter` - Run cell, move next
- `Ctrl + Enter` - Run cell, stay
- `A` - Insert cell above
- `B` - Insert cell below
- `DD` - Delete cell
- `M` - Change to Markdown (text)
- `Y` - Change to Code

**Best Practices:**

1. **Import libraries at top**
```python
import pandas as pd
import matplotlib.pyplot as plt
```

2. **One logical step per cell**
- Cell 1: Load data
- Cell 2: Clean data
- Cell 3: Analyze
- Cell 4: Visualize

3. **Add Markdown explanations**
```markdown
# Revenue Analysis Q1 2024

**Key Questions:**
1. Which products generated most revenue?
2. How does Q1 compare to Q4?
```

4. **Clear outputs before sharing**
- Kernel → Restart & Clear Output
"""
        )

        st.markdown("#### ✅ Professional Coding Habits")
        st.markdown(
            """**1. Naming Conventions (PEP 8)**

```python
# Variables/functions: snake_case ✅
customer_revenue = 150_000
def calculate_churn_rate():
    pass

# Constants: UPPERCASE ✅
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Avoid ❌
x = 150000                # Not descriptive
CustomerRevenue = 150000  # Wrong case
calculate-churn = 0.15    # Can't use hyphens
```

---

**2. When to Comment**

```python
# GOOD: Explain WHY ✅
churn = calculate_churn_rate(customers, churned)
# Using 30-day window because 7-day is too volatile

# BAD: Obvious ❌
revenue = price * quantity  # Calculate revenue (DUH!)

# GOOD: Complex logic ✅
# Apply 15% for enterprise, 5% for mid-market
if segment == "Enterprise":
    discount = 0.15
elif segment == "Mid-Market":
    discount = 0.05
```

---

**3. Error Handling**

```python
# Without (crashes if zero) ❌
def churn_rate(total, churned):
    return churned / total

# With error handling ✅
def churn_rate(total, churned):
    try:
        return churned / total
    except ZeroDivisionError:
        return 0.0

# Safe dictionary access ✅
customer = {"name": "Acme", "revenue": 150_000}
email = customer.get("email", "unknown@example.com")
```

---

**4. Code Organization**

```python
# BAD: Messy one-liner ❌
revenue=150000;growth=0.15;target=1000000;years=0;while revenue<target:revenue*=(1+growth);years+=1;print(years)

# GOOD: Organized ✅
def years_to_target(initial, growth_rate, target):
    \"\"\"Calculate years to reach target revenue\"\"\"
    revenue = initial
    years = 0
    
    while revenue < target:
        revenue *= (1 + growth_rate)
        years += 1
    
    return years

result = years_to_target(150_000, 0.15, 1_000_000)
print(f"Years to £1M: {result}")
```
"""
        )

        st.markdown("#### ⚠️ Common Beginner Mistakes")
        st.markdown(
            """**1. Indentation Errors**
```python
# WRONG ❌
def calculate():
revenue = 100  # IndentationError!

# RIGHT ✅
def calculate():
    revenue = 100  # Indented 4 spaces
```

**2. Forgetting Colons**
```python
# WRONG ❌
if revenue > 100000

# RIGHT ✅
if revenue > 100000:
    print("High value")
```

**3. Using = instead of ==**
```python
# WRONG ❌
if revenue = 100000:  # Assigns, doesn't compare

# RIGHT ✅
if revenue == 100000:  # Compares
    print("Exactly £100K")
```

**4. Off-by-One Errors**
```python
revenues = [100, 200, 300]
# Index: 0, 1, 2 (not 1, 2, 3!)

first = revenues[0]   # 100 ✅
last = revenues[2]    # 300 ✅
# revenues[3]         # IndexError! ❌
```

**5. String vs Number**
```python
# Strings
"100" + "200"  # "100200" (concatenation)

# Numbers
100 + 200      # 300 (addition)

# Convert types
int("100")     # 100 (string → int)
float("99.9")  # 99.9 (string → float)
str(100)       # "100" (int → string)
```
"""
        )

        st.markdown("#### 🎯 Your First Data Analysis Script")
        st.markdown(
            """**Complete Example:**

```python
# Sales Analysis Script
monthly_sales = {
    "January": 45_000,
    "February": 52_000,
    "March": 48_000,
    "April": 61_000,
    "May": 58_000,
    "June": 67_000
}

# Calculate metrics
total = sum(monthly_sales.values())
average = total / len(monthly_sales)
best_month = max(monthly_sales, key=monthly_sales.get)
worst_month = min(monthly_sales, key=monthly_sales.get)

# Growth rate
q1 = sum([monthly_sales["January"], monthly_sales["February"], monthly_sales["March"]])
q2 = sum([monthly_sales["April"], monthly_sales["May"], monthly_sales["June"]])
growth = ((q2 - q1) / q1) * 100

# Report
print("=" * 50)
print("SALES ANALYSIS - H1 2024")
print("=" * 50)
print(f"Total Revenue: £{total:,}")
print(f"Average Monthly: £{average:,.0f}")
print(f"Best: {best_month} (£{monthly_sales[best_month]:,})")
print(f"Worst: {worst_month} (£{monthly_sales[worst_month]:,})")
print(f"Q1→Q2 Growth: {growth:+.1f}%")
print("=" * 50)
```

**Output:**
```
==================================================
SALES ANALYSIS - H1 2024
==================================================
Total Revenue: £331,000
Average Monthly: £55,167
Best: June (£67,000)
Worst: January (£45,000)
Q1→Q2 Growth: +28.3%
==================================================
```

**You just did real data analysis!**
"""
        )

        st.markdown("#### 🚀 Next Steps & Practice")
        st.markdown(
            """**After this unit:**
- ✅ Unit 3: Pandas (data tables)
- ✅ Unit 4: SQL (databases)
- ✅ Unit 5: Statistics

**Practice Daily (15-30 min):**
1. **Coding challenges**
   - LeetCode Easy problems
   - HackerRank Python
   - Project Euler

2. **Real projects**
   - Analyze your bank statements
   - Track fitness data
   - Build budget tracker

3. **Read code**
   - GitHub Python projects
   - Kaggle notebooks
   - Stack Overflow answers

**Resources:**
- Official: docs.python.org/tutorial
- Book: Python for Data Analysis (Wes McKinney)
- Website: realpython.com
- Q&A: stackoverflow.com

---

**Job Interview Ready:**

You can now answer:
- "Difference between list and dictionary?" ✅
- "When use for vs while loop?" ✅
- "What is a function?" ✅
- "Calculate average revenue in Python?" ✅

**Skills employers want:**
- ✅ Clean, readable code
- ✅ Data structures mastery
- ✅ Reusable functions
- ✅ Jupyter notebooks
- ✅ Professional practices

**You have these skills now!**
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS: Unit 2 Python Programming")
        st.markdown(
            """**Complete these 3 labs to master Python fundamentals:**

---

## Lab 1: Python Basics & Data Types (45 min)

**Objective:** Master Python data types and basic operations for data analysis

**Setup:**
```python
# Create new Jupyter notebook: lab2_1_python_basics.ipynb
# Or use Python script: lab2_1_python_basics.py
```

---

**Part A: Variables and Data Types (15 min)**

```python
# 1. Create variables for a fictional e-commerce order
order_id = "ORD-2024-001"
customer_name = "Sarah Johnson"
order_total = 156.99
items_count = 3
is_premium_member = True
order_date = "2024-11-15"

# 2. Print order summary
print("=" * 50)
print("ORDER SUMMARY")
print("=" * 50)
print(f"Order ID: {order_id}")
print(f"Customer: {customer_name}")
print(f"Items: {items_count}")
print(f"Total: £{order_total:.2f}")
print(f"Premium Member: {is_premium_member}")
print(f"Date: {order_date}")
print("=" * 50)

# 3. Check data types
print(f"\\norder_total type: {type(order_total)}")  # float
print(f"is_premium_member type: {type(is_premium_member)}")  # bool
```

**Part B: Lists and Loops (15 min)**

```python
# 1. Create list of daily sales (£)
daily_sales = [1250, 1480, 1320, 1650, 1890, 2100, 1950]
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 2. Calculate total and average
total_sales = sum(daily_sales)
avg_sales = total_sales / len(daily_sales)

print(f"Total Weekly Sales: £{total_sales:,}")
print(f"Average Daily Sales: £{avg_sales:,.2f}")

# 3. Find best and worst days
best_day_index = daily_sales.index(max(daily_sales))
worst_day_index = daily_sales.index(min(daily_sales))

print(f"\\nBest Day: {days[best_day_index]} (£{daily_sales[best_day_index]:,})")
print(f"Worst Day: {days[worst_day_index]} (£{daily_sales[worst_day_index]:,})")

# 4. Print daily breakdown
print("\\nDaily Breakdown:")
for day, sales in zip(days, daily_sales):
    print(f"{day}: £{sales:,}")
```

**Part C: Dictionaries (15 min)**

```python
# 1. Create product inventory
inventory = {
    "Laptop": {"price": 899.99, "stock": 15, "category": "Electronics"},
    "Mouse": {"price": 24.99, "stock": 50, "category": "Electronics"},
    "Desk Chair": {"price": 199.99, "stock": 8, "category": "Furniture"},
    "Monitor": {"price": 299.99, "stock": 12, "category": "Electronics"},
    "Desk Lamp": {"price": 34.99, "stock": 25, "category": "Furniture"}
}

# 2. Calculate total inventory value
total_value = 0
for product, details in inventory.items():
    value = details["price"] * details["stock"]
    total_value += value
    print(f"{product}: £{value:,.2f} ({details['stock']} units)")

print(f"\\nTotal Inventory Value: £{total_value:,.2f}")

# 3. Find low stock items (< 10 units)
print("\\nLow Stock Alerts:")
low_stock = []
for product, details in inventory.items():
    if details["stock"] < 10:
        low_stock.append(product)
        print(f"⚠️ {product}: Only {details['stock']} left!")

# 4. Calculate average price by category
electronics_prices = []
furniture_prices = []

for product, details in inventory.items():
    if details["category"] == "Electronics":
        electronics_prices.append(details["price"])
    else:
        furniture_prices.append(details["price"])

print(f"\\nAvg Electronics Price: £{sum(electronics_prices)/len(electronics_prices):.2f}")
print(f"Avg Furniture Price: £{sum(furniture_prices)/len(furniture_prices):.2f}")
```

**Checkpoint Questions:**
1. What's the difference between a list and a dictionary?
2. When would you use `for` vs `while`?
3. How do you format numbers as currency in Python?

---

## Lab 2: Control Flow & Functions (60 min)

**Objective:** Build reusable functions for data cleaning and analysis

**Part A: Conditional Logic (20 min)**

```python
# Customer segmentation based on purchase history

def segment_customer(total_spent, orders_count, days_since_last):
    \"\"\"
    Segment customers into categories based on behavior
    
    Args:
        total_spent: Total £ spent
        orders_count: Number of orders
        days_since_last: Days since last order
    
    Returns:
        str: Customer segment
    \"\"\"
    # VIP: High spend + frequent orders
    if total_spent > 1000 and orders_count > 10:
        return "VIP"
    
    # At Risk: Haven't ordered recently
    elif days_since_last > 90:
        return "At Risk"
    
    # Active: Regular customer
    elif total_spent > 500 and days_since_last < 30:
        return "Active"
    
    # New: Low spend, recent order
    elif total_spent < 200 and days_since_last < 30:
        return "New"
    
    # Occasional: Everyone else
    else:
        return "Occasional"

# Test with different customers
customers = [
    {"name": "Alice", "spent": 1500, "orders": 15, "days": 10},
    {"name": "Bob", "spent": 300, "orders": 5, "days": 120},
    {"name": "Carol", "spent": 750, "orders": 8, "days": 15},
    {"name": "David", "spent": 150, "orders": 2, "days": 5},
]

print("CUSTOMER SEGMENTATION")
print("=" * 60)
for customer in customers:
    segment = segment_customer(
        customer["spent"], 
        customer["orders"], 
        customer["days"]
    )
    print(f"{customer['name']:10} | £{customer['spent']:>6.2f} | {customer['orders']:2} orders | {segment}")
```

**Part B: Data Cleaning Functions (20 min)**

```python
def clean_revenue_string(revenue_str):
    \"\"\"
    Clean revenue string: '£1,234.56' → 1234.56
    \"\"\"
    # Remove £ symbol and commas
    cleaned = revenue_str.replace("£", "").replace(",", "")
    return float(cleaned)

def validate_email(email):
    \"\"\"
    Basic email validation
    \"\"\"
    if "@" in email and "." in email:
        return True
    return False

def standardize_country(country):
    \"\"\"
    Standardize country names
    \"\"\"
    mapping = {
        "UK": "United Kingdom",
        "USA": "United States",
        "U.S.A": "United States",
        "US": "United States",
    }
    return mapping.get(country, country)

# Test cleaning functions
test_revenues = ["£1,250.00", "£999.99", "£15,432.50"]
print("Revenue Cleaning:")
for rev in test_revenues:
    cleaned = clean_revenue_string(rev)
    print(f"{rev} → £{cleaned:.2f}")

# Test email validation
test_emails = ["user@example.com", "invalid.email", "test@domain.co.uk"]
print("\\nEmail Validation:")
for email in test_emails:
    valid = "✅" if validate_email(email) else "❌"
    print(f"{valid} {email}")

# Test country standardization
test_countries = ["UK", "USA", "Germany", "US"]
print("\\nCountry Standardization:")
for country in test_countries:
    standardized = standardize_country(country)
    print(f"{country} → {standardized}")
```

**Part C: Analysis Pipeline (20 min)**

```python
def calculate_metrics(sales_data):
    \"\"\"
    Calculate key sales metrics
    
    Args:
        sales_data: List of daily sales (£)
    
    Returns:
        dict: Metrics including total, average, growth
    \"\"\"
    total = sum(sales_data)
    average = total / len(sales_data)
    maximum = max(sales_data)
    minimum = min(sales_data)
    
    # Calculate growth rate (last value vs first value)
    growth_rate = ((sales_data[-1] - sales_data[0]) / sales_data[0]) * 100
    
    return {
        "total": total,
        "average": average,
        "max": maximum,
        "min": minimum,
        "growth_rate": growth_rate
    }

def print_metrics_report(metrics, title="SALES METRICS"):
    \"\"\"
    Print formatted metrics report
    \"\"\"
    print("\\n" + "=" * 50)
    print(title)
    print("=" * 50)
    print(f"Total Sales:     £{metrics['total']:>10,.2f}")
    print(f"Average Daily:   £{metrics['average']:>10,.2f}")
    print(f"Best Day:        £{metrics['max']:>10,.2f}")
    print(f"Worst Day:       £{metrics['min']:>10,.2f}")
    print(f"Growth Rate:     {metrics['growth_rate']:>10.1f}%")
    print("=" * 50)

# Test with sample data
weekly_sales = [1200, 1350, 1280, 1450, 1620, 1580, 1490]
metrics = calculate_metrics(weekly_sales)
print_metrics_report(metrics, "WEEKLY SALES ANALYSIS")

# Test with monthly data
monthly_sales = [15000, 16500, 14800, 18200, 19500, 21000]
metrics = calculate_metrics(monthly_sales)
print_metrics_report(metrics, "MONTHLY SALES TREND")
```

**Challenge Exercise:**
Create a function that takes a list of order dictionaries and returns:
- Total revenue
- Average order value
- Number of orders over £100
- Best customer (highest spend)

---

## Lab 3: Real Data Analysis Project (75 min)

**Objective:** Complete end-to-end analysis using CSV data

**Dataset:** Download `sales_data.csv` or create your own:
```python
import csv

# Create sample dataset
data = [
    ["order_id", "date", "customer", "product", "quantity", "price"],
    ["ORD001", "2024-11-01", "Alice", "Laptop", 1, 899.99],
    ["ORD002", "2024-11-01", "Bob", "Mouse", 2, 24.99],
    ["ORD003", "2024-11-02", "Alice", "Monitor", 1, 299.99],
    ["ORD004", "2024-11-03", "Carol", "Laptop", 1, 899.99],
    ["ORD005", "2024-11-03", "Bob", "Keyboard", 1, 79.99],
    ["ORD006", "2024-11-04", "David", "Mouse", 3, 24.99],
    ["ORD007", "2024-11-05", "Alice", "Desk Lamp", 2, 34.99],
    ["ORD008", "2024-11-05", "Carol", "Monitor", 2, 299.99],
]

with open("sales_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("✅ Created sales_data.csv")
```

**Part A: Load and Explore (15 min)**

```python
import csv

# Load data
orders = []
with open("sales_data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        orders.append(row)

# Explore
print(f"Total Orders: {len(orders)}")
print(f"\\nFirst 3 orders:")
for order in orders[:3]:
    print(order)

# Check data types
print(f"\\nSample order structure:")
print(orders[0].keys())
```

**Part B: Clean and Transform (20 min)**

```python
# Clean data
for order in orders:
    # Convert price and quantity to numbers
    order["price"] = float(order["price"])
    order["quantity"] = int(order["quantity"])
    
    # Calculate order total
    order["total"] = order["price"] * order["quantity"]

# Verify cleaning
print("\\nCleaned orders:")
for order in orders[:3]:
    print(f"{order['order_id']}: {order['product']} x{order['quantity']} = £{order['total']:.2f}")
```

**Part C: Analysis (25 min)**

```python
# 1. Total revenue
total_revenue = sum(order["total"] for order in orders)
print(f"\\nTotal Revenue: £{total_revenue:,.2f}")

# 2. Revenue by customer
customer_revenue = {}
for order in orders:
    customer = order["customer"]
    if customer not in customer_revenue:
        customer_revenue[customer] = 0
    customer_revenue[customer] += order["total"]

print("\\nRevenue by Customer:")
for customer, revenue in sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True):
    print(f"{customer:10} £{revenue:>8,.2f}")

# 3. Most popular products
product_sales = {}
for order in orders:
    product = order["product"]
    if product not in product_sales:
        product_sales[product] = 0
    product_sales[product] += order["quantity"]

print("\\nTop Selling Products:")
for product, qty in sorted(product_sales.items(), key=lambda x: x[1], reverse=True):
    print(f"{product:15} {qty} units")

# 4. Average order value
avg_order_value = total_revenue / len(orders)
print(f"\\nAverage Order Value: £{avg_order_value:.2f}")
```

**Part D: Report (15 min)**

```python
def generate_sales_report(orders):
    \"\"\"
    Generate comprehensive sales report
    \"\"\"
    # Calculate all metrics
    total_revenue = sum(o["total"] for o in orders)
    total_orders = len(orders)
    avg_order = total_revenue / total_orders
    
    # Find best customer
    customer_revenue = {}
    for order in orders:
        customer = order["customer"]
        customer_revenue[customer] = customer_revenue.get(customer, 0) + order["total"]
    
    best_customer = max(customer_revenue, key=customer_revenue.get)
    best_customer_revenue = customer_revenue[best_customer]
    
    # Print report
    print("\\n" + "=" * 60)
    print("SALES ANALYSIS REPORT")
    print("=" * 60)
    print(f"Period: Nov 1-5, 2024")
    print(f"\\nKey Metrics:")
    print(f"  Total Revenue:        £{total_revenue:>10,.2f}")
    print(f"  Total Orders:         {total_orders:>10}")
    print(f"  Average Order Value:  £{avg_order:>10,.2f}")
    print(f"\\nTop Customer:")
    print(f"  {best_customer}: £{best_customer_revenue:.2f}")
    print(f"\\nInsights:")
    print(f"  - {len(customer_revenue)} unique customers")
    print(f"  - Best customer accounts for {(best_customer_revenue/total_revenue)*100:.1f}% of revenue")
    print("=" * 60)

# Generate report
generate_sales_report(orders)
```

**Checkpoint:**
1. Can you add more metrics (e.g., revenue by product)?
2. How would you find orders over £100?
3. What other insights can you extract?

---

**Lab Completion Checklist:**
- ☐ Completed Lab 1 (Python basics)
- ☐ Completed Lab 2 (Functions)
- ☐ Completed Lab 3 (Real analysis)
- ☐ All code runs without errors
- ☐ Understood data types and control flow
- ☐ Can write reusable functions
- ☐ Can analyze CSV data with pure Python

**Next:** Unit 3 labs will introduce Pandas for much faster data manipulation!
"""
        )

    elif unit_number == 3:
        st.markdown("---")
        st.markdown("#### 📊 Why Pandas & NumPy Are Essential")
        st.markdown(
            """**Pure Python is too slow for real data work.**

**Performance Comparison:**

| Task | Pure Python | NumPy | Pandas |
|------|-------------|-------|--------|
| Sum 1M numbers | 100ms | 5ms | 10ms |
| Filter 1M rows | 500ms | 20ms | 30ms |
| Group & aggregate | Minutes | Seconds | Seconds |
| Memory usage | High | Low | Medium |

**What They Do:**

**NumPy:**
- Fast numerical arrays (C-speed in Python)
- Mathematical operations
- Foundation for Pandas

**Pandas:**
- DataFrames (like Excel tables, but millions of rows)
- Load data from files/databases
- Clean, filter, transform, analyze
- The #1 tool for data analysts and scientists globally

**Together:** Handle datasets from 100 rows to 100 million rows efficiently.

---

### Installation & Import

```python
# Install (if needed)
pip install pandas numpy

# Import (standard convention)
import pandas as pd
import numpy as np

print(pd.__version__)  # Check version
```
"""
        )

        st.markdown("#### 📥 Loading Data")
        st.markdown(
            """**Pandas can load data from anywhere:**

---

**1. CSV Files (Most Common)**

```python
import pandas as pd

# Basic load
df = pd.read_csv('sales_data.csv')

# With options
df = pd.read_csv('sales_data.csv',
                 sep=',',              # Delimiter
                 encoding='utf-8',     # Character encoding
                 parse_dates=['date'], # Convert to datetime
                 na_values=['', 'NULL', 'N/A'])  # Treat as missing

# From URL
url = 'https://example.com/data.csv'
df = pd.read_csv(url)
```

---

**2. Excel Files**

```python
# Single sheet
df = pd.read_excel('report.xlsx', sheet_name='Sales')

# Multiple sheets
sales = pd.read_excel('report.xlsx', sheet_name='Sales')
costs = pd.read_excel('report.xlsx', sheet_name='Costs')

# All sheets at once
all_sheets = pd.read_excel('report.xlsx', sheet_name=None)
```

---

**3. SQL Databases**

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('company.db')

# Query into DataFrame
query = "SELECT * FROM customers WHERE country='UK'"
df = pd.read_sql_query(query, conn)

conn.close()
```

---

**4. JSON (API Responses)**

```python
# From file
df = pd.read_json('api_response.json')

# From API
import requests
response = requests.get('https://api.example.com/data')
df = pd.DataFrame(response.json())
```

---

**5. Clipboard (Quick Paste from Excel)**

```python
# Copy data from Excel, then:
df = pd.read_clipboard()
```
"""
        )

        st.markdown("#### 🔍 Exploring DataFrames")
        st.markdown(
            """**First Steps with Any Dataset**

```python
import pandas as pd

# Load sample data
df = pd.read_csv('customers.csv')

# Quick peek
df.head()        # First 5 rows
df.head(10)      # First 10 rows
df.tail()        # Last 5 rows
df.sample(5)     # Random 5 rows

# Shape and structure
print(df.shape)        # (1000, 15) = 1000 rows, 15 columns
print(df.columns)      # Column names
print(df.dtypes)       # Data type of each column
print(df.info())       # Summary: types, non-null counts, memory

# Statistical summary
df.describe()          # Count, mean, std, min, quartiles, max
df['revenue'].describe()  # For single column
```

**Example Output:**

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1000 entries, 0 to 999
Data columns (total 5 columns):
 #   Column          Non-Null Count  Dtype  
---  ------          --------------  -----  
 0   customer_id     1000 non-null   int64  
 1   customer_name   998 non-null    object 
 2   revenue         995 non-null    float64
 3   country         1000 non-null   object 
 4   signup_date     987 non-null    object 
dtypes: float64(1), int64(1), object(3)
memory usage: 39.2+ KB
```

**Key Insights:**
- 1000 customers
- 2 missing names, 5 missing revenues, 13 missing dates
- Need to clean before analysis

---

**Missing Data Analysis:**

```python
# Count nulls per column
df.isna().sum()

# Percentage missing
(df.isna().sum() / len(df)) * 100

# Rows with any null
df[df.isna().any(axis=1)]

# Complete cases only
df_clean = df.dropna()
```

---

**Unique Values:**

```python
# How many unique countries?
df['country'].nunique()  # 15

# What are they?
df['country'].unique()  # ['UK', 'US', 'Germany', ...]

# Count by country
df['country'].value_counts()

# As percentages
df['country'].value_counts(normalize=True)
```

**Example Output:**
```
UK          450  (45.0%)
US          300  (30.0%)
Germany     150  (15.0%)
France      100  (10.0%)
```
"""
        )

        st.markdown("#### 🎯 Selecting & Filtering")
        st.markdown(
            """**Get Exactly the Data You Need**

---

**Select Columns:**

```python
# Single column (returns Series)
df['customer_name']

# Multiple columns (returns DataFrame)
df[['customer_name', 'revenue', 'country']]

# By position
df.iloc[:, 0:3]  # First 3 columns
```

---

**Filter Rows:**

```python
# Simple filter
high_value = df[df['revenue'] > 100_000]

# Multiple conditions (AND)
uk_high_value = df[(df['country'] == 'UK') & (df['revenue'] > 100_000)]

# Multiple conditions (OR)
uk_or_us = df[(df['country'] == 'UK') | (df['country'] == 'US')]

# NOT
non_uk = df[df['country'] != 'UK']
```

**⚠️ Important:** Use `&` and `|`, NOT `and`/`or`. Use parentheses!

---

**Advanced Filtering:**

```python
# Multiple values (.isin)
target_countries = df[df['country'].isin(['UK', 'US', 'Germany'])]

# String contains
tech_companies = df[df['customer_name'].str.contains('Tech', case=False, na=False)]

# Between values
medium_revenue = df[df['revenue'].between(50_000, 200_000)]

# Date filtering
df['signup_date'] = pd.to_datetime(df['signup_date'])
recent = df[df['signup_date'] > '2024-01-01']

# Complex logic
qualified = df[
    (df['revenue'] > 100_000) & 
    (df['country'].isin(['UK', 'US'])) &
    (df['signup_date'] > '2023-01-01')
]
```

---

**loc vs iloc:**

```python
# loc: by label
df.loc[0:5, ['customer_name', 'revenue']]  # Rows 0-5, specific columns

# iloc: by position
df.iloc[0:5, 0:3]  # Rows 0-5, columns 0-3

# Mix conditions
df.loc[df['revenue'] > 100_000, ['customer_name', 'revenue']]
```
"""
        )

        st.markdown("#### 🔧 Data Transformation")
        st.markdown(
            """**Change Your Data Without Changing the Source**

---

**Add New Columns:**

```python
# Simple calculation
df['revenue_thousands'] = df['revenue'] / 1000

# Conditional column
df['is_enterprise'] = df['revenue'] > 1_000_000

# Combine columns
df['full_name'] = df['first_name'] + ' ' + df['last_name']

# Apply function
def categorize(revenue):
    if revenue > 1_000_000:
        return 'Enterprise'
    elif revenue > 100_000:
        return 'Mid-Market'
    return 'SMB'

df['segment'] = df['revenue'].apply(categorize)

# Lambda (one-liner)
df['revenue_formatted'] = df['revenue'].apply(lambda x: f"£{x:,.0f}")
```

---

**Rename Columns:**

```python
# Rename specific columns
df = df.rename(columns={
    'customer_name': 'name',
    'signup_date': 'date'
})

# Rename all (lowercase)
df.columns = df.columns.str.lower()

# Remove spaces
df.columns = df.columns.str.replace(' ', '_')
```

---

**Change Data Types:**

```python
# To datetime
df['signup_date'] = pd.to_datetime(df['signup_date'])

# To numeric (handle errors)
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

# To string
df['customer_id'] = df['customer_id'].astype(str)

# To category (saves memory)
df['country'] = df['country'].astype('category')
```

---

**Handle Missing Values:**

```python
# Drop rows with any null
df_clean = df.dropna()

# Drop rows with null in specific columns
df_clean = df.dropna(subset=['customer_id', 'revenue'])

# Fill with value
df['email'].fillna('unknown@example.com', inplace=True)

# Fill with mean/median
df['revenue'].fillna(df['revenue'].median(), inplace=True)

# Forward fill (use previous value)
df['country'].fillna(method='ffill', inplace=True)

# Backward fill
df['country'].fillna(method='bfill', inplace=True)
```

---

**Remove Duplicates:**

```python
# Remove all duplicates
df_unique = df.drop_duplicates()

# Based on specific columns
df_unique = df.drop_duplicates(subset=['customer_id'], keep='first')

# Keep last occurrence
df_unique = df.drop_duplicates(subset=['customer_id'], keep='last')
```

---

**Sort Data:**

```python
# Single column
df_sorted = df.sort_values('revenue', ascending=False)  # Highest first

# Multiple columns
df_sorted = df.sort_values(
    ['country', 'revenue'],
    ascending=[True, False]  # Country A-Z, revenue high-low
)

# Reset index after sorting
df_sorted = df_sorted.reset_index(drop=True)
```
"""
        )

        st.markdown("#### 📊 Grouping & Aggregating")
        st.markdown(
            """**Answer Business Questions with GROUP BY**

---

**Basic Aggregations:**

```python
# Total revenue by country
df.groupby('country')['revenue'].sum()

# Count customers by country
df.groupby('country').size()

# Multiple aggregations
df.groupby('country')['revenue'].agg(['sum', 'mean', 'count', 'min', 'max'])
```

**Example Output:**
```
country   sum         mean      count  min     max
UK        45_000_000  100_000   450    5_000   5_000_000
US        30_000_000  100_000   300    10_000  3_000_000
Germany   15_000_000  100_000   150    8_000   2_000_000
```

---

**Multiple Columns & Aggregations:**

```python
# Different aggregations per column
summary = df.groupby('country').agg({
    'revenue': ['sum', 'mean'],
    'customer_id': 'count',
    'signup_date': ['min', 'max']
})

# With custom names
summary = df.groupby('country').agg(
    total_revenue=('revenue', 'sum'),
    avg_revenue=('revenue', 'mean'),
    customer_count=('customer_id', 'count')
).reset_index()
```

---

**Custom Aggregation Functions:**

```python
def revenue_per_customer(group):
    return group['revenue'].sum() / group['customer_id'].nunique()

metrics = df.groupby('country').apply(revenue_per_customer)

# Or with lambda
metrics = df.groupby('country').apply(
    lambda x: x['revenue'].sum() / len(x)
)
```

---

**Filtering After Grouping:**

```python
# Countries with >£10M total revenue
high_revenue_countries = df.groupby('country')['revenue'].sum()
high_revenue_countries = high_revenue_countries[high_revenue_countries > 10_000_000]

# Or in one line
result = df.groupby('country').filter(lambda x: x['revenue'].sum() > 10_000_000)
```
"""
        )

        st.markdown("#### 🔗 Joining DataFrames")
        st.markdown(
            """**Combine Multiple Tables (Like SQL JOINS)**

```python
# Sample data
customers = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'name': ['Acme', 'Tech Ltd', 'Global Inc'],
    'country': ['UK', 'US', 'Germany']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104],
    'customer_id': [1, 1, 2, 4],  # Note: 4 doesn't exist in customers
    'amount': [1000, 1500, 2000, 500]
})
```

---

**INNER JOIN (Only Matching Rows):**

```python
merged = customers.merge(orders, on='customer_id', how='inner')
# Result: 3 orders (customer 4 excluded)
```

---

**LEFT JOIN (All from Left + Matches from Right):**

```python
merged = customers.merge(orders, on='customer_id', how='left')
# Result: All 3 customers, Global Inc has NaN for orders
```

---

**RIGHT JOIN (All from Right + Matches from Left):**

```python
merged = customers.merge(orders, on='customer_id', how='right')
# Result: All 4 orders, order 104 has NaN for customer details
```

---

**OUTER JOIN (All from Both):**

```python
merged = customers.merge(orders, on='customer_id', how='outer')
# Result: All customers + all orders
```

---

**Different Column Names:**

```python
# If join columns have different names
df1.merge(df2, left_on='customer_id', right_on='cust_id')
```

---

**Multiple Keys:**

```python
merged = df1.merge(df2, on=['customer_id', 'date'], how='inner')
```

---

**Concatenate (Stack DataFrames):**

```python
# Stack vertically (rows)
q1_sales = pd.read_csv('q1_sales.csv')
q2_sales = pd.read_csv('q2_sales.csv')
h1_sales = pd.concat([q1_sales, q2_sales], ignore_index=True)

# Stack horizontally (columns)
combined = pd.concat([df1, df2], axis=1)
```
"""
        )

        st.markdown("#### 🧮 Thinking in Columns (Vectorization)")
        st.markdown(
            """**Avoid Row-by-Row Loops = Faster Code**

---

**❌ SLOW (Row-by-Row Loop):**

```python
# DON'T DO THIS (1000x slower!)
total = 0
for index, row in df.iterrows():
    total += row['revenue']
```

**✅ FAST (Vectorized):**

```python
# DO THIS INSTEAD
total = df['revenue'].sum()
```

---

**More Examples:**

```python
# ❌ SLOW
for index, row in df.iterrows():
    if row['revenue'] > 100000:
        df.loc[index, 'segment'] = 'High'
    else:
        df.loc[index, 'segment'] = 'Low'

# ✅ FAST (100x-1000x faster!)
df['segment'] = df['revenue'].apply(lambda x: 'High' if x > 100000 else 'Low')

# ✅ EVEN FASTER (NumPy where)
df['segment'] = np.where(df['revenue'] > 100000, 'High', 'Low')
```

---

**Common Vectorized Operations:**

```python
# Mathematical operations (entire column at once)
df['revenue_doubled'] = df['revenue'] * 2
df['revenue_millions'] = df['revenue'] / 1_000_000

# String operations (entire column)
df['name_upper'] = df['customer_name'].str.upper()
df['domain'] = df['email'].str.split('@').str[1]

# Date operations (entire column)
df['year'] = df['signup_date'].dt.year
df['month'] = df['signup_date'].dt.month
df['days_since_signup'] = (pd.Timestamp.now() - df['signup_date']).dt.days
```
"""
        )

        st.markdown("#### 🧹 Real-World Cleaning Pipeline")
        st.markdown(
            """**Complete Example: Messy Data → Clean Data**

```python
import pandas as pd
import numpy as np

# 1. LOAD RAW DATA
df = pd.read_csv('messy_sales_data.csv')
print(f"Raw data: {df.shape}")  # (1523, 12)

# 2. INSPECT
print(df.info())
print(df.head())
print(df.isna().sum())

# 3. CLEAN COLUMN NAMES
df.columns = df.columns.str.lower().str.replace(' ', '_')

# 4. HANDLE MISSING VALUES
# Drop if customer_id missing (critical field)
df = df.dropna(subset=['customer_id'])

# Fill email with placeholder
df['email'].fillna('unknown@example.com', inplace=True)

# Fill revenue with median
df['revenue'].fillna(df['revenue'].median(), inplace=True)

# 5. FIX DATA TYPES
df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
df['customer_id'] = df['customer_id'].astype(str)

# 6. REMOVE DUPLICATES
df = df.drop_duplicates(subset=['customer_id'], keep='first')

# 7. FILTER OUTLIERS
# Remove negative revenue
df = df[df['revenue'] >= 0]

# Remove unrealistic revenue (>£10M)
df = df[df['revenue'] <= 10_000_000]

# 8. CREATE NEW FEATURES
df['revenue_tier'] = pd.cut(df['revenue'], 
                              bins=[0, 50_000, 200_000, 1_000_000, np.inf],
                              labels=['Small', 'Medium', 'Large', 'Enterprise'])

df['signup_year'] = df['signup_date'].dt.year
df['days_active'] = (pd.Timestamp.now() - df['signup_date']).dt.days

# 9. SAVE CLEAN VERSION
df.to_csv('sales_data_clean.csv', index=False)
print(f"Clean data: {df.shape}")  # (1487, 15)

print("✅ Data cleaning complete!")
print(f"Removed {1523 - 1487} bad rows")
print(f"Added 3 new columns")
```

**This is a production-ready cleaning pipeline.**

Employers love candidates who can write code like this!
"""
        )

        st.markdown("#### 🎯 Real Business Analysis Example")
        st.markdown(
            """**Complete Analysis: E-Commerce Customer Segmentation**

```python
import pandas as pd

# Load data
df = pd.read_csv('customers.csv')

# Calculate RFM metrics (Recency, Frequency, Monetary)
today = pd.to_datetime('2024-12-01')
df['last_purchase'] = pd.to_datetime(df['last_purchase'])

rfm = df.groupby('customer_id').agg({
    'last_purchase': lambda x: (today - x.max()).days,  # Recency
    'order_id': 'count',                                 # Frequency
    'revenue': 'sum'                                     # Monetary
}).rename(columns={
    'last_purchase': 'recency',
    'order_id': 'frequency',
    'revenue': 'monetary'
})

# Score each dimension (1-5)
rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

# Combined RFM score
rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

# Segment customers
def segment_customer(row):
    score = int(row['R_score']) + int(row['F_score']) + int(row['M_score'])
    if score >= 13:
        return 'Champions'
    elif score >= 10:
        return 'Loyal'
    elif score >= 7:
        return 'Potential'
    else:
        return 'At Risk'

rfm['segment'] = rfm.apply(segment_customer, axis=1)

# Summary by segment
summary = rfm.groupby('segment').agg({
    'customer_id': 'count',
    'monetary': 'sum',
    'frequency': 'mean'
}).rename(columns={'customer_id': 'customer_count'})

print(summary)
```

**Output:**
```
segment       customer_count  monetary      frequency
Champions     1,250          £25,000,000   15.2
Loyal         2,100          £18,000,000   8.5
Potential     3,500          £12,000,000   4.2
At Risk       1,150          £3,000,000    2.1
```

**Action:** Focus retention campaign on 1,150 "At Risk" customers.

**This is real data science work!**
"""
        )

        st.markdown("#### 🚀 Next Steps & Practice")
        st.markdown(
            """**After mastering Pandas:**
- ✅ Analyze any CSV/Excel file
- ✅ Clean messy data professionally
- ✅ Join multiple data sources
- ✅ Create business metrics
- ✅ Build automated pipelines

**Practice Projects:**
1. **Personal Finance Tracker**
   - Load bank statements (CSV)
   - Categorize transactions
   - Monthly spending analysis

2. **Sales Performance Dashboard**
   - Load sales data
   - Calculate KPIs by region
   - Identify top/bottom performers

3. **Customer Churn Analysis**
   - RFM segmentation (like example above)
   - Identify at-risk customers
   - Recommend interventions

**Resources:**
- Official: pandas.pydata.org/docs
- Book: Python for Data Analysis (Wes McKinney - Pandas creator!)
- Practice: kaggle.com/datasets
- Cheat sheet: pandas.pydata.org/Pandas_Cheat_Sheet.pdf

---

**Job Interview Ready:**

You can now:
- ✅ Load and explore any dataset
- ✅ Clean missing values and duplicates
- ✅ Filter, transform, aggregate data
- ✅ Join multiple DataFrames
- ✅ Build real analysis pipelines

**This is the #1 skill data analysts need.**

**Next:** Unit 4 (SQL) complements Pandas perfectly!
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS: Unit 3 Pandas & NumPy")
        st.markdown(
            """**Complete these 3 labs to master data manipulation:**

---

## Lab 1: Pandas Fundamentals (60 min)

**Objective:** Master DataFrame operations for real data analysis

**Setup:**
```python
import pandas as pd
import numpy as np

# Create sample e-commerce dataset
data = {
    'order_id': ['ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005', 'ORD006', 'ORD007', 'ORD008'],
    'customer': ['Alice', 'Bob', 'Alice', 'Carol', 'Bob', 'David', 'Alice', 'Carol'],
    'product': ['Laptop', 'Mouse', 'Monitor', 'Laptop', 'Keyboard', 'Mouse', 'Desk Lamp', 'Monitor'],
    'quantity': [1, 2, 1, 1, 1, 3, 2, 2],
    'price': [899.99, 24.99, 299.99, 899.99, 79.99, 24.99, 34.99, 299.99],
    'date': ['2024-11-01', '2024-11-01', '2024-11-02', '2024-11-03', 
             '2024-11-03', '2024-11-04', '2024-11-05', '2024-11-05']
}

df = pd.DataFrame(data)
df.to_csv('sales_data.csv', index=False)
print("✅ Created sales_data.csv")
```

---

**Part A: Loading and Exploring (15 min)**

```python
import pandas as pd

# Load data
df = pd.read_csv('sales_data.csv')

# Initial exploration
print("Dataset shape:", df.shape)
print("\\nColumn names:", df.columns.tolist())
print("\\nData types:")
print(df.dtypes)

# Preview data
print("\\nFirst 5 rows:")
print(df.head())

# Summary statistics
print("\\nSummary statistics:")
print(df.describe())

# Check for missing values
print("\\nMissing values:")
print(df.isnull().sum())
```

**Part B: Selection and Filtering (20 min)**

```python
# Select single column
print("Customers:")
print(df['customer'])

# Select multiple columns
print("\\nOrders overview:")
print(df[['order_id', 'customer', 'product', 'price']])

# Filter rows (orders over £100)
expensive_orders = df[df['price'] > 100]
print("\\nExpensive orders (>£100):")
print(expensive_orders)

# Multiple conditions
alice_laptops = df[(df['customer'] == 'Alice') & (df['product'] == 'Laptop')]
print("\\nAlice's laptop orders:")
print(alice_laptops)

# Filter by list
target_customers = ['Alice', 'Bob']
filtered = df[df['customer'].isin(target_customers)]
print(f"\\nOrders from {target_customers}:")
print(filtered)
```

**Part C: Creating New Columns (15 min)**

```python
# Calculate total per order
df['total'] = df['price'] * df['quantity']

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract day of week
df['day_of_week'] = df['date'].dt.day_name()

# Add revenue category
df['category'] = df['total'].apply(lambda x: 'High' if x > 500 else 'Standard')

# Display result
print("Enhanced DataFrame:")
print(df[['order_id', 'total', 'day_of_week', 'category']])
```

**Part D: Sorting and Ranking (10 min)**

```python
# Sort by total (descending)
sorted_df = df.sort_values('total', ascending=False)
print("Orders sorted by total:")
print(sorted_df[['order_id', 'customer', 'total']])

# Sort by multiple columns
multi_sort = df.sort_values(['customer', 'date'])
print("\\nOrders by customer and date:")
print(multi_sort[['customer', 'date', 'product']])

# Add rank
df['revenue_rank'] = df['total'].rank(ascending=False)
print("\\nTop revenue orders:")
print(df.nlargest(3, 'total')[['order_id', 'customer', 'total', 'revenue_rank']])
```

---

## Lab 2: Data Cleaning & Transformation (75 min)

**Objective:** Clean real-world messy data

**Setup: Create messy dataset**

```python
import pandas as pd
import numpy as np

# Messy customer data (intentional errors!)
messy_data = {
    'customer_id': [1, 2, 3, 4, 5, 2, 6, 7, 8],  # Note: duplicate ID=2
    'name': ['Alice Smith', 'bob jones', 'Carol-Lee', 'DAVID BROWN', 
             'Emma Watson', 'bob jones', 'Frank Miller', None, 'Grace Lee'],
    'email': ['alice@example.com', 'bob@test.com', 'carol@example.com',
              'david@example.com', 'emma@test.co.uk', 'bob@test.com', 
              'frank@example', None, 'grace@example.com'],
    'revenue': [1500.50, 750.00, None, 2300.75, 450.00, 750.00, 1800.00, 900.00, 1200.50],
    'country': ['UK', 'USA', 'UK', 'US', 'United Kingdom', 'USA', 'Germany', 'UK', 'France']
}

df = pd.DataFrame(messy_data)
df.to_csv('messy_customers.csv', index=False)
print("✅ Created messy_customers.csv with intentional errors")
```

---

**Part A: Identify Issues (15 min)**

```python
df = pd.read_csv('messy_customers.csv')

# 1. Check shape
print(f"Shape: {df.shape}")

# 2. Check data types
print("\\nData types:")
print(df.dtypes)

# 3. Missing values
print("\\nMissing values:")
print(df.isnull().sum())

# 4. Duplicates
print(f"\\nDuplicate rows: {df.duplicated().sum()}")
print("Duplicate customer_ids:", df[df.duplicated('customer_id', keep=False)])

# 5. Unique values
print("\\nUnique countries:", df['country'].unique())
```

**Part B: Clean Data (30 min)**

```python
# Create copy for cleaning
clean_df = df.copy()

# 1. Remove exact duplicates
clean_df = clean_df.drop_duplicates()
print(f"After removing duplicates: {len(clean_df)} rows")

# 2. Handle missing values
# Drop rows with missing names
clean_df = clean_df.dropna(subset=['name'])

# Fill missing revenue with median
median_revenue = clean_df['revenue'].median()
clean_df['revenue'] = clean_df['revenue'].fillna(median_revenue)

print(f"\\nAfter handling missing: {len(clean_df)} rows")
print("Missing values now:", clean_df.isnull().sum().sum())

# 3. Standardize text
# Names: Title case
clean_df['name'] = clean_df['name'].str.title()

# Emails: Lowercase
clean_df['email'] = clean_df['email'].str.lower()

# 4. Standardize countries
country_mapping = {
    'US': 'United States',
    'USA': 'United States',
    'United Kingdom': 'UK'
}
clean_df['country'] = clean_df['country'].replace(country_mapping)

# 5. Validate emails
def is_valid_email(email):
    if pd.isna(email):
        return False
    return '@' in str(email) and '.' in str(email).split('@')[-1]

clean_df['email_valid'] = clean_df['email'].apply(is_valid_email)

print("\\nCleaned data:")
print(clean_df)

print("\\nInvalid emails:")
print(clean_df[~clean_df['email_valid']][['name', 'email']])
```

**Part C: Transform Data (30 min)**

```python
# 1. Create customer segments
clean_df['segment'] = pd.cut(
    clean_df['revenue'], 
    bins=[0, 500, 1000, float('inf')],
    labels=['Bronze', 'Silver', 'Gold']
)

# 2. Calculate metrics
clean_df['revenue_per_char'] = clean_df['revenue'] / clean_df['name'].str.len()

# 3. Create binary flags
clean_df['is_high_value'] = clean_df['revenue'] > 1000

# 4. Extract name components
clean_df['first_name'] = clean_df['name'].str.split().str[0]
clean_df['last_name'] = clean_df['name'].str.split().str[-1]

# Display transformed data
print("\\nTransformed data:")
print(clean_df[['name', 'revenue', 'segment', 'is_high_value']])

# Save clean version
clean_df.to_csv('clean_customers.csv', index=False)
print("\\n✅ Saved clean_customers.csv")
```

---

## Lab 3: Aggregation & Joining (90 min)

**Objective:** Combine datasets and create business insights

**Setup: Create related datasets**

```python
import pandas as pd

# Customers
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Carol', 'David', 'Emma'],
    'signup_date': ['2024-01-15', '2024-02-20', '2024-01-10', '2024-03-05', '2024-02-28'],
    'country': ['UK', 'USA', 'UK', 'Germany', 'France']
})

# Orders
orders = pd.DataFrame({
    'order_id': range(1, 16),
    'customer_id': [1, 2, 1, 3, 2, 4, 1, 5, 3, 2, 1, 4, 3, 5, 2],
    'product': ['Laptop', 'Mouse', 'Monitor', 'Laptop', 'Keyboard', 'Mouse', 'Desk Lamp',
                'Monitor', 'Laptop', 'Desk Lamp', 'Monitor', 'Laptop', 'Mouse', 'Keyboard', 'Monitor'],
    'revenue': [899.99, 24.99, 299.99, 899.99, 79.99, 24.99, 34.99, 299.99, 899.99, 34.99, 299.99, 899.99, 24.99, 79.99, 299.99],
    'order_date': ['2024-11-01', '2024-11-01', '2024-11-02', '2024-11-02', '2024-11-03',
                   '2024-11-03', '2024-11-04', '2024-11-04', '2024-11-05', '2024-11-05',
                   '2024-11-06', '2024-11-06', '2024-11-07', '2024-11-07', '2024-11-08']
})

customers.to_csv('customers.csv', index=False)
orders.to_csv('orders.csv', index=False)
print("✅ Created customers.csv and orders.csv")
```

---

**Part A: GROUP BY Analysis (25 min)**

```python
df_orders = pd.read_csv('orders.csv')

# 1. Total revenue by product
product_revenue = df_orders.groupby('product')['revenue'].sum().sort_values(ascending=False)
print("Revenue by Product:")
print(product_revenue)

# 2. Count orders by customer
customer_orders = df_orders.groupby('customer_id').size()
print("\\nOrders per customer:")
print(customer_orders)

# 3. Multiple aggregations
customer_stats = df_orders.groupby('customer_id').agg({
    'revenue': ['sum', 'mean', 'count'],
    'order_id': 'count'
}).round(2)
print("\\nCustomer statistics:")
print(customer_stats)

# 4. Most popular product
product_counts = df_orders['product'].value_counts()
print("\\nMost popular products:")
print(product_counts)

# 5. Daily revenue
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
daily_revenue = df_orders.groupby('order_date')['revenue'].sum()
print("\\nDaily revenue:")
print(daily_revenue)
```

**Part B: Joining DataFrames (30 min)**

```python
df_customers = pd.read_csv('customers.csv')
df_orders = pd.read_csv('orders.csv')

# 1. Inner join (only matching records)
merged = pd.merge(
    df_orders, 
    df_customers, 
    on='customer_id', 
    how='inner'
)
print("Merged orders with customer info:")
print(merged[['order_id', 'name', 'product', 'revenue', 'country']].head())

# 2. Left join (keep all orders)
all_orders = pd.merge(
    df_orders,
    df_customers[['customer_id', 'name']],
    on='customer_id',
    how='left'
)
print("\\nAll orders with customer names:")
print(all_orders.head())

# 3. Aggregate then join
customer_totals = df_orders.groupby('customer_id').agg({
    'revenue': 'sum',
    'order_id': 'count'
}).rename(columns={'order_id': 'order_count'})

# Join aggregated data
customer_summary = pd.merge(
    df_customers,
    customer_totals,
    on='customer_id',
    how='left'
)
customer_summary['revenue'] = customer_summary['revenue'].fillna(0)
customer_summary['order_count'] = customer_summary['order_count'].fillna(0).astype(int)

print("\\nCustomer summary:")
print(customer_summary)
```

**Part C: RFM Analysis (35 min)**

```python
# RFM = Recency, Frequency, Monetary

import pandas as pd
from datetime import datetime

df_customers = pd.read_csv('customers.csv')
df_orders = pd.read_csv('orders.csv')
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])

# Set analysis date
analysis_date = pd.to_datetime('2024-11-09')

# Calculate RFM metrics
rfm = df_orders.groupby('customer_id').agg({
    'order_date': lambda x: (analysis_date - x.max()).days,  # Recency
    'order_id': 'count',  # Frequency
    'revenue': 'sum'  # Monetary
}).rename(columns={
    'order_date': 'recency',
    'order_id': 'frequency',
    'revenue': 'monetary'
})

# Score each metric (1-4, higher is better)
rfm['R_score'] = pd.cut(rfm['recency'], bins=4, labels=[4,3,2,1])
rfm['F_score'] = pd.cut(rfm['frequency'], bins=4, labels=[1,2,3,4])
rfm['M_score'] = pd.cut(rfm['monetary'], bins=4, labels=[1,2,3,4])

# Combine scores
rfm['RFM_score'] = (
    rfm['R_score'].astype(str) + 
    rfm['F_score'].astype(str) + 
    rfm['M_score'].astype(str)
)

# Segment customers
def segment_customer(row):
    if row['R_score'] >= 3 and row['F_score'] >= 3 and row['M_score'] >= 3:
        return 'Champions'
    elif row['F_score'] >= 3 and row['M_score'] >= 3:
        return 'Loyal Customers'
    elif row['R_score'] >= 3:
        return 'Potential Loyalists'
    elif row['R_score'] <= 2 and row['F_score'] <= 2:
        return 'At Risk'
    else:
        return 'Needs Attention'

rfm['segment'] = rfm.apply(segment_customer, axis=1)

# Join with customer names
rfm_full = pd.merge(
    rfm,
    df_customers[['customer_id', 'name']],
    on='customer_id',
    how='left'
)

print("RFM Analysis:")
print(rfm_full[['name', 'recency', 'frequency', 'monetary', 'segment']].sort_values('monetary', ascending=False))

# Segment summary
print("\\nSegment distribution:")
print(rfm_full['segment'].value_counts())

# Save results
rfm_full.to_csv('rfm_analysis.csv', index=False)
print("\\n✅ Saved rfm_analysis.csv")
```

---

**Lab Completion Checklist:**
- ☐ Completed Lab 1 (Pandas fundamentals)
- ☐ Completed Lab 2 (Data cleaning)
- ☐ Completed Lab 3 (Aggregation & joining)
- ☐ Can load, filter, transform DataFrames
- ☐ Can handle missing values and duplicates
- ☐ Can perform GROUP BY analysis
- ☐ Can join multiple datasets
- ☐ Completed RFM customer segmentation

**Next:** Unit 4 SQL labs will show you how to query databases directly!
"""
        )

    elif unit_number == 4:
        st.markdown("---")
        st.markdown("#### 🗄️ Why SQL is Still Critical for Data Science")
        st.markdown(
            """**Even with Pandas, SQL is essential.**

**Where Data Actually Lives:**
- **Production databases:** Customer data, transactions, logs
- **Data warehouses:** Snowflake, BigQuery, Redshift
- **Analytics platforms:** Most BI tools query databases, not CSV files
- **90% of data jobs require SQL** (UK, US, globally)

**Why Not Just Use Pandas?**

| Task | SQL | Pandas |
|------|-----|--------|
| Query 1B rows | ✅ Fast | ❌ Runs out of memory |
| Filter at source | ✅ Efficient | ❌ Loads everything first |
| Share with analysts | ✅ Everyone knows SQL | ❌ Need Python |
| Power BI/Tableau | ✅ Direct connection | ❌ Need exports |
| Join 5 tables | ✅ Optimized | ❌ Multiple merges |

**The Winning Combo:**
1. **SQL:** Extract and aggregate data from database
2. **Pandas:** Further analysis and modeling
3. **Together:** Best of both worlds

---

### Database Basics

**Relational Database = Collection of Tables**

**Example E-Commerce Database:**

**customers** table:
```
customer_id | name          | country | signup_date
------------|---------------|---------|-------------
1           | Acme Corp     | UK      | 2023-01-15
2           | Tech Ltd      | US      | 2023-02-20
3           | Global Inc    | Germany | 2023-03-10
```

**orders** table:
```
order_id | customer_id | order_date  | amount
---------|-------------|-------------|--------
101      | 1           | 2024-01-10  | 1000
102      | 1           | 2024-02-15  | 1500
103      | 2           | 2024-01-20  | 2000
104      | 3           | 2024-03-05  | 500
```

**Relationships:**
- One customer → Many orders (one-to-many)
- `customer_id` connects the tables (foreign key)

**Primary Key:** Unique identifier (customer_id, order_id)  
**Foreign Key:** Reference to another table (customer_id in orders)
"""
        )

        st.markdown("#### 📝 SELECT: Getting Data")
        st.markdown(
            """**Basic SELECT Queries**

```sql
-- All columns, all rows
SELECT * FROM customers;

-- Specific columns
SELECT name, country FROM customers;

-- With alias (rename column)
SELECT 
    name AS customer_name,
    country AS location
FROM customers;

-- Calculated columns
SELECT 
    name,
    amount,
    amount * 0.2 AS tax,
    amount * 1.2 AS total_with_tax
FROM orders;

-- Distinct values (no duplicates)
SELECT DISTINCT country FROM customers;

-- Count rows
SELECT COUNT(*) FROM customers;  -- 3

-- Limit results
SELECT * FROM customers LIMIT 5;
```

---

**Business Question:** *"What are our customer names and countries?"*

```sql
SELECT 
    customer_id,
    name,
    country
FROM customers;
```

**Output:**
```
customer_id | name          | country
------------|---------------|--------
1           | Acme Corp     | UK
2           | Tech Ltd      | US
3           | Global Inc    | Germany
```
"""
        )

        st.markdown("#### 🔍 WHERE: Filtering Rows")
        st.markdown(
            """**Filter Data with WHERE Clause**

---

**Comparison Operators:**

```sql
-- Equal to
SELECT * FROM customers WHERE country = 'UK';

-- Not equal
SELECT * FROM customers WHERE country != 'US';
SELECT * FROM customers WHERE country <> 'US';  -- Same

-- Greater than
SELECT * FROM orders WHERE amount > 1000;

-- Greater than or equal
SELECT * FROM orders WHERE amount >= 1000;

-- Less than
SELECT * FROM orders WHERE amount < 2000;

-- Less than or equal
SELECT * FROM orders WHERE amount <= 2000;

-- Between (inclusive)
SELECT * FROM orders 
WHERE amount BETWEEN 500 AND 1500;

-- IN (multiple values)
SELECT * FROM customers 
WHERE country IN ('UK', 'US', 'Germany');

-- NOT IN
SELECT * FROM customers 
WHERE country NOT IN ('France', 'Spain');

-- LIKE (pattern matching)
SELECT * FROM customers WHERE name LIKE '%Corp%';  -- Contains "Corp"
SELECT * FROM customers WHERE name LIKE 'Tech%';   -- Starts with "Tech"
SELECT * FROM customers WHERE name LIKE '%Inc';    -- Ends with "Inc"

-- IS NULL
SELECT * FROM customers WHERE email IS NULL;

-- IS NOT NULL
SELECT * FROM customers WHERE email IS NOT NULL;
```

---

**Multiple Conditions (AND, OR):**

```sql
-- AND (both conditions must be true)
SELECT * FROM orders 
WHERE customer_id = 1 AND amount > 1000;

-- OR (at least one condition true)
SELECT * FROM customers 
WHERE country = 'UK' OR country = 'US';

-- Complex logic (use parentheses!)
SELECT * FROM orders 
WHERE (customer_id = 1 OR customer_id = 2) 
  AND amount > 1000;
```

---

**Business Question:** *"Which UK customers placed orders over £1,000?"*

```sql
SELECT 
    c.name,
    o.amount,
    o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'UK' 
  AND o.amount > 1000;
```
"""
        )

        st.markdown("#### 🔗 JOINs: Combining Tables")
        st.markdown(
            """**JOINs are the Heart of SQL**

---

**INNER JOIN (Only Matching Rows):**

```sql
SELECT 
    c.name,
    o.order_id,
    o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

**Visual:**
```
customers (3 rows)    orders (4 rows)
┌──────────────┐      ┌──────────────┐
│ 1 Acme       │──┐   │ 101  1  1000 │
│ 2 Tech       │──┼───│ 102  1  1500 │
│ 3 Global     │──┘   │ 103  2  2000 │
└──────────────┘  └───│ 104  3   500 │
                      └──────────────┘
Result: 4 rows (all orders matched)
```

---

**LEFT JOIN (All from Left + Matches from Right):**

```sql
SELECT 
    c.name,
    o.order_id,
    o.amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**Use Case:** "Show all customers, even if they haven't ordered"

**Result:** All 3 customers (customers with no orders show NULL for order columns)

---

**RIGHT JOIN (All from Right + Matches from Left):**

```sql
SELECT 
    c.name,
    o.order_id,
    o.amount
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;
```

**Rarely used** (just swap tables and use LEFT JOIN instead)

---

**Multiple JOINs:**

```sql
SELECT 
    c.name AS customer,
    o.order_id,
    p.product_name,
    p.price
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id;
```

**Chain tables:** customers → orders → order_items → products

---

**Business Question:** *"Show all customers and their total order count (including customers with 0 orders)"*

```sql
SELECT 
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

**Output:**
```
name          | order_count
--------------|-------------
Acme Corp     | 2
Tech Ltd      | 1
Global Inc    | 1
```
"""
        )

        st.markdown("#### 📊 GROUP BY: Aggregations")
        st.markdown(
            """**Answer Business Questions with Aggregates**

---

**Aggregate Functions:**

```sql
-- Count rows
SELECT COUNT(*) FROM orders;  -- 4

-- Sum amounts
SELECT SUM(amount) FROM orders;  -- 5000

-- Average
SELECT AVG(amount) FROM orders;  -- 1250

-- Min and Max
SELECT MIN(amount), MAX(amount) FROM orders;  -- 500, 2000

-- Multiple aggregates
SELECT 
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    MIN(amount) AS smallest_order,
    MAX(amount) AS largest_order
FROM orders;
```

---

**GROUP BY (Aggregate by Category):**

```sql
-- Revenue by customer
SELECT 
    customer_id,
    COUNT(*) AS order_count,
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id;
```

**Output:**
```
customer_id | order_count | total_spent
------------|-------------|-------------
1           | 2           | 2500
2           | 1           | 2000
3           | 1           | 500
```

---

**GROUP BY with JOIN:**

```sql
-- Revenue by country
SELECT 
    c.country,
    COUNT(o.order_id) AS order_count,
    SUM(o.amount) AS total_revenue,
    AVG(o.amount) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country;
```

**Output:**
```
country | order_count | total_revenue | avg_order_value
--------|-------------|---------------|----------------
UK      | 2           | 2500          | 1250
US      | 1           | 2000          | 2000
Germany | 1           | 500           | 500
```

---

**HAVING (Filter After Grouping):**

```sql
-- Countries with revenue > £1,000
SELECT 
    c.country,
    SUM(o.amount) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country
HAVING SUM(o.amount) > 1000;
```

**WHERE vs HAVING:**
- **WHERE:** Filters rows BEFORE grouping
- **HAVING:** Filters groups AFTER aggregation

```sql
-- Correct usage
SELECT 
    country,
    COUNT(*) AS customer_count
FROM customers
WHERE signup_date > '2023-01-01'  -- Filter BEFORE grouping
GROUP BY country
HAVING COUNT(*) > 5;              -- Filter AFTER grouping
```
"""
        )

        st.markdown("#### 🔢 ORDER BY: Sorting Results")
        st.markdown(
            """**Sort Your Results**

```sql
-- Sort ascending (default)
SELECT name, amount FROM orders ORDER BY amount;

-- Sort descending
SELECT name, amount FROM orders ORDER BY amount DESC;

-- Multiple columns
SELECT name, country, signup_date 
FROM customers 
ORDER BY country ASC, signup_date DESC;
-- Country A→Z, then newest signup first within each country

-- Order by calculated column
SELECT 
    name,
    amount,
    amount * 0.2 AS tax
FROM orders
ORDER BY tax DESC;

-- Top N results
SELECT name, amount 
FROM orders 
ORDER BY amount DESC 
LIMIT 5;  -- Top 5 orders
```

---

**Business Question:** *"Who are our top 10 customers by total spending?"*

```sql
SELECT 
    c.name,
    SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 10;
```
"""
        )

        st.markdown("#### 🎯 Complete Business Query Example")
        st.markdown(
            """**Scenario:** E-commerce company wants a monthly revenue report

**Question:** *"Show monthly revenue, order count, and average order value for 2024, sorted by month"*

```sql
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    MIN(amount) AS smallest_order,
    MAX(amount) AS largest_order
FROM orders
WHERE order_date >= '2024-01-01' 
  AND order_date < '2025-01-01'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

**Output:**
```
month      | order_count | total_revenue | avg_order_value | smallest | largest
-----------|-------------|---------------|-----------------|----------|--------
2024-01-01 | 2           | 3000          | 1500            | 1000     | 2000
2024-02-01 | 1           | 1500          | 1500            | 1500     | 1500
2024-03-01 | 1           | 500           | 500             | 500      | 500
```

**This is exactly what you'll do in real jobs!**
"""
        )

        st.markdown("#### 🔁 Subqueries & CTEs")
        st.markdown(
            """**Advanced SQL for Complex Questions**

---

**Subquery (Query Inside a Query):**

```sql
-- Find customers who spent more than average
SELECT name, total_spent
FROM (
    SELECT 
        c.name,
        SUM(o.amount) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
) AS customer_totals
WHERE total_spent > (SELECT AVG(amount) FROM orders);
```

---

**CTE (Common Table Expression - More Readable):**

```sql
WITH customer_totals AS (
    SELECT 
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
),
avg_order AS (
    SELECT AVG(amount) AS avg_amount FROM orders
)
SELECT 
    ct.name,
    ct.total_spent,
    ao.avg_amount
FROM customer_totals ct, avg_order ao
WHERE ct.total_spent > ao.avg_amount;
```

**CTEs are clearer for complex queries.**
"""
        )

        st.markdown("#### 🐍 SQL + Python Integration")
        st.markdown(
            """**Combine SQL and Pandas**

```python
import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect('ecommerce.db')

# Query directly into DataFrame
query = \"\"\"
    SELECT 
        c.name,
        c.country,
        COUNT(o.order_id) AS order_count,
        SUM(o.amount) AS total_revenue
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name, c.country
    ORDER BY total_revenue DESC
\"\"\"

df = pd.read_sql_query(query, conn)
conn.close()

# Now use Pandas
print(df.head())
print(f"Total revenue: £{df['total_revenue'].sum():,.0f}")
```

**Workflow:**
1. **SQL:** Filter, join, aggregate (reduce data size)
2. **Pandas:** Further analysis, visualization, ML

**Example:**
- SQL: Extract 1B rows → aggregate to 10K rows
- Pandas: Analyze those 10K rows
- **Result:** Fast and efficient!
"""
        )

        st.markdown("#### ⚡ Query Optimization Tips")
        st.markdown(
            """**Make Your Queries Faster**

**1. Use WHERE to Filter Early**

```sql
-- ❌ SLOW (joins everything first)
SELECT c.name, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date > '2024-01-01';

-- ✅ FAST (filters before join)
SELECT c.name, o.amount
FROM customers c
JOIN (
    SELECT * FROM orders 
    WHERE order_date > '2024-01-01'
) o ON c.customer_id = o.customer_id;
```

---

**2. Select Only Needed Columns**

```sql
-- ❌ SLOW (transfers all data)
SELECT * FROM customers;

-- ✅ FAST (transfers only what you need)
SELECT customer_id, name FROM customers;
```

---

**3. Use LIMIT for Testing**

```sql
-- Test query on small sample first
SELECT * FROM orders LIMIT 100;
```

---

**4. Index Foreign Keys**

```sql
-- Create index on commonly joined columns
CREATE INDEX idx_customer_id ON orders(customer_id);
```

**Indexes speed up JOINs and WHERE clauses.**
"""
        )

        st.markdown("#### 🎯 Real Interview Questions")
        st.markdown(
            """**Common SQL Interview Questions (UK/US):**

---

**Q1:** "Find the top 5 customers by total revenue"

```sql
SELECT 
    c.name,
    SUM(o.amount) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_revenue DESC
LIMIT 5;
```

---

**Q2:** "Show customers who haven't ordered in the last 90 days"

```sql
SELECT c.name, MAX(o.order_date) AS last_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING MAX(o.order_date) < CURRENT_DATE - INTERVAL '90 days'
   OR MAX(o.order_date) IS NULL;
```

---

**Q3:** "Calculate month-over-month revenue growth"

```sql
WITH monthly_revenue AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ((revenue - LAG(revenue) OVER (ORDER BY month)) / 
     LAG(revenue) OVER (ORDER BY month)) * 100 AS growth_pct
FROM monthly_revenue;
```

**You can now answer these!**
"""
        )

        st.markdown("#### 🚀 Practice & Next Steps")
        st.markdown(
            """**Master SQL:**

**Practice Platforms:**
1. **SQLZoo** (sqlzoo.net) - Interactive tutorials
2. **LeetCode SQL** (leetcode.com/problemset/database) - Interview prep
3. **HackerRank SQL** - Challenges by difficulty
4. **Mode Analytics SQL Tutorial** - Real business data

**Practice Projects:**
1. **Analyze Sakila Database** (sample DVD rental database)
   - Customer retention analysis
   - Revenue by film category
   - Top performing stores

2. **E-commerce Analysis**
   - Customer segmentation
   - Product performance
   - Seasonal trends

3. **Your Own Data**
   - Export bank statements → import to SQLite
   - Query spending patterns
   - Build monthly budgets

**Resources:**
- **Book:** SQL for Data Scientists (Renée Teate)
- **Interactive:** https://sqlbolt.com
- **Cheat Sheet:** https://www.sqltutorial.org/sql-cheat-sheet

---

**Job Interview Ready:**

You can now:
- ✅ Write SELECT queries with filters
- ✅ JOIN multiple tables correctly
- ✅ Aggregate data with GROUP BY
- ✅ Sort and limit results
- ✅ Use subqueries and CTEs
- ✅ Integrate SQL with Python/Pandas
- ✅ Optimize query performance
- ✅ Answer common interview questions

**SQL + Pandas = Unstoppable data analyst!**

**Next:** Unit 5 (Statistics) teaches you to interpret results correctly!
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS: Unit 4 SQL")
        st.markdown(
            """**Complete these 3 labs to master SQL querying:**

---

## Lab 1: SQL Basics & Filtering (60 min)

**Setup: Create SQLite Database**

```python
import sqlite3
import pandas as pd

# Create database
conn = sqlite3.connect('ecommerce.db')

# Create customers table
conn.execute('''
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    country TEXT,
    signup_date DATE
)
''')

# Insert sample data
customers_data = [
    (1, 'Alice Smith', 'alice@example.com', 'UK', '2024-01-15'),
    (2, 'Bob Jones', 'bob@test.com', 'USA', '2024-02-20'),
    (3, 'Carol Lee', 'carol@example.com', 'UK', '2024-01-10'),
    (4, 'David Brown', 'david@example.com', 'Germany', '2024-03-05'),
    (5, 'Emma Watson', 'emma@test.com', 'France', '2024-02-28')
]

conn.executemany('INSERT INTO customers VALUES (?,?,?,?,?)', customers_data)
conn.commit()
print("✅ Database created!")
```

**Part A: SELECT Queries (20 min)**

```sql
-- 1. Select all customers
SELECT * FROM customers;

-- 2. Select specific columns
SELECT name, email FROM customers;

-- 3. WHERE clause - UK customers only
SELECT * FROM customers WHERE country = 'UK';

-- 4. Multiple conditions
SELECT name, country 
FROM customers 
WHERE country = 'UK' AND signup_date < '2024-02-01';

-- 5. OR conditions
SELECT * FROM customers 
WHERE country = 'UK' OR country = 'USA';

-- 6. IN operator
SELECT * FROM customers 
WHERE country IN ('UK', 'USA', 'Germany');

-- 7. LIKE pattern matching
SELECT * FROM customers WHERE name LIKE '%son';

-- 8. ORDER BY
SELECT * FROM customers ORDER BY signup_date DESC;

-- 9. LIMIT results
SELECT * FROM customers ORDER BY signup_date LIMIT 3;
```

**Part B: Aggregations (20 min)**

```sql
-- 1. Count total customers
SELECT COUNT(*) as total_customers FROM customers;

-- 2. Count by country
SELECT country, COUNT(*) as customer_count 
FROM customers 
GROUP BY country;

-- 3. Earliest and latest signup
SELECT 
    MIN(signup_date) as first_signup,
    MAX(signup_date) as latest_signup
FROM customers;

-- 4. Customers per month
SELECT 
    strftime('%Y-%m', signup_date) as month,
    COUNT(*) as signups
FROM customers
GROUP BY month
ORDER BY month;
```

**Part C: Python Integration (20 min)**

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('ecommerce.db')

# Query with Pandas
df = pd.read_sql_query("SELECT * FROM customers", conn)
print(df)

# Filter in SQL vs Pandas
uk_customers_sql = pd.read_sql_query(
    "SELECT * FROM customers WHERE country = 'UK'", 
    conn
)
print("\\nUK Customers (via SQL):")
print(uk_customers_sql)

# Aggregation
country_stats = pd.read_sql_query('''
    SELECT 
        country,
        COUNT(*) as customer_count,
        MIN(signup_date) as first_signup
    FROM customers
    GROUP BY country
''', conn)
print("\\nCountry Statistics:")
print(country_stats)

conn.close()
```

---

## Lab 2: JOINs & Multi-Table Queries (75 min)

**Setup: Add Orders Table**

```python
conn = sqlite3.connect('ecommerce.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product TEXT,
    revenue REAL,
    order_date DATE
)
''')

orders_data = [
    (1, 1, 'Laptop', 899.99, '2024-11-01'),
    (2, 2, 'Mouse', 24.99, '2024-11-01'),
    (3, 1, 'Monitor', 299.99, '2024-11-02'),
    (4, 3, 'Laptop', 899.99, '2024-11-03'),
    (5, 2, 'Keyboard', 79.99, '2024-11-03'),
    (6, 4, 'Mouse', 24.99, '2024-11-04'),
    (7, 1, 'Desk Lamp', 34.99, '2024-11-05'),
    (8, 3, 'Monitor', 599.98, '2024-11-05')
]

conn.executemany('INSERT INTO orders VALUES (?,?,?,?,?)', orders_data)
conn.commit()
print("✅ Orders table created!")
```

**Part A: INNER JOIN (25 min)**

```sql
-- 1. Basic join
SELECT 
    orders.order_id,
    customers.name,
    orders.product,
    orders.revenue
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;

-- 2. Join with WHERE
SELECT 
    c.name,
    o.product,
    o.revenue
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.revenue > 100;

-- 3. Join with aggregation
SELECT 
    c.name,
    COUNT(o.order_id) as order_count,
    SUM(o.revenue) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name
ORDER BY total_revenue DESC;
```

**Part B: LEFT JOIN (25 min)**

```sql
-- Find customers with no orders
SELECT 
    c.name,
    c.country,
    COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.country;

-- Filter for customers with 0 orders
SELECT 
    c.name,
    c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**Part C: Complex Queries (25 min)**

```sql
-- Subquery: Customers above average revenue
SELECT name, total_revenue
FROM (
    SELECT 
        c.customer_id,
        c.name,
        SUM(o.revenue) as total_revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) 
WHERE total_revenue > (
    SELECT AVG(total_revenue) 
    FROM (
        SELECT SUM(revenue) as total_revenue
        FROM orders
        GROUP BY customer_id
    )
);

-- CTE (Common Table Expression)
WITH customer_stats AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(revenue) as total_revenue
    FROM orders
    GROUP BY customer_id
)
SELECT 
    c.name,
    cs.order_count,
    cs.total_revenue,
    cs.total_revenue / cs.order_count as avg_order_value
FROM customer_stats cs
JOIN customers c ON cs.customer_id = c.customer_id
ORDER BY total_revenue DESC;
```

---

## Lab 3: Real Business Analytics (60 min)

**Objective:** Answer 10 common business questions with SQL

```sql
-- Q1: What's our total revenue?
SELECT SUM(revenue) as total_revenue FROM orders;

-- Q2: How many customers have made purchases?
SELECT COUNT(DISTINCT customer_id) as active_customers FROM orders;

-- Q3: What's the average order value?
SELECT AVG(revenue) as avg_order_value FROM orders;

-- Q4: Which product generates most revenue?
SELECT 
    product,
    SUM(revenue) as total_revenue,
    COUNT(*) as orders
FROM orders
GROUP BY product
ORDER BY total_revenue DESC;

-- Q5: Who are our top 3 customers by revenue?
SELECT 
    c.name,
    SUM(o.revenue) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 3;

-- Q6: Revenue by country?
SELECT 
    c.country,
    COUNT(o.order_id) as orders,
    SUM(o.revenue) as revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY revenue DESC;

-- Q7: Daily revenue trend?
SELECT 
    order_date,
    COUNT(*) as orders,
    SUM(revenue) as daily_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;

-- Q8: Customers with multiple orders?
SELECT 
    c.name,
    COUNT(o.order_id) as order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 2;

-- Q9: Revenue growth week-over-week?
SELECT 
    strftime('%W', order_date) as week,
    SUM(revenue) as weekly_revenue
FROM orders
GROUP BY week;

-- Q10: Customer lifetime value distribution?
SELECT 
    CASE 
        WHEN total_revenue < 100 THEN 'Low'
        WHEN total_revenue < 500 THEN 'Medium'
        ELSE 'High'
    END as value_segment,
    COUNT(*) as customers
FROM (
    SELECT customer_id, SUM(revenue) as total_revenue
    FROM orders
    GROUP BY customer_id
)
GROUP BY value_segment;
```

**Lab Completion Checklist:**
- ☐ Created SQLite database with tables
- ☐ Wrote SELECT, WHERE, ORDER BY queries
- ☐ Used INNER and LEFT JOINs
- ☐ Performed GROUP BY aggregations
- ☐ Used subqueries and CTEs
- ☐ Integrated SQL with Pandas
- ☐ Answered 10 business questions

**Next:** Unit 5 Statistics labs teach A/B testing!
"""
        )

    elif unit_number == 5:
        st.markdown("---")
        st.markdown("#### 📈 Why Statistics is Essential for Data Science")
        st.markdown(
            """**Statistics = The Science of Making Decisions Under Uncertainty**

**Why It Matters:**
- **Understand variability:** Is this pattern real or random noise?
- **Make predictions:** What's likely to happen next?
- **Communicate uncertainty:** How confident are we?
- **Design experiments:** How to test if change X causes outcome Y?

**Real Examples:**

| Question | Statistical Tool |
|----------|------------------|
| "Is our new website design better?" | A/B Testing |
| "Will this customer churn?" | Classification (based on probability) |
| "How confident are we?" | Confidence Intervals |
| "Is this correlation meaningful?" | Hypothesis Testing |
| "What drives sales?" | Regression Analysis |

**Data Science Without Stats = Guessing**  
**Data Science With Stats = Evidence-Based Decisions**
"""
        )

        st.markdown("#### 📊 Descriptive Statistics: Summarizing Data")
        st.markdown(
            """**Measures of Center (Where's the Middle?)**

```python
import numpy as np
import pandas as pd

# Sample data: Daily website visitors
visitors = [120, 150, 145, 300, 135, 142, 155, 148, 152, 141]

# Mean (average)
mean_visitors = np.mean(visitors)  # 158.8

# Median (middle value when sorted)
median_visitors = np.median(visitors)  # 146.5

# Mode (most common value)
from scipy import stats
mode_visitors = stats.mode(visitors)  # May have multiple modes
```

**When to Use Each:**
- **Mean:** Good for normal distributions, sensitive to outliers
- **Median:** Better when data has outliers (e.g., income, house prices)
- **Mode:** Categorical data (most popular product, common complaint)

**Example:** Daily visitors = [120, 150, 145, **2000**, 135, 142]
- Mean = 448.7 (distorted by outlier!)
- Median = 145 (robust to outlier) ✅

---

**Measures of Spread (How Scattered is the Data?)**

```python
# Range
data_range = max(visitors) - min(visitors)  # 180

# Variance (average squared distance from mean)
variance = np.var(visitors)  # 2356.6

# Standard Deviation (sqrt of variance, same units as data)
std_dev = np.std(visitors)  # 48.5

# Interquartile Range (IQR - middle 50%)
q1 = np.percentile(visitors, 25)  # 25th percentile
q3 = np.percentile(visitors, 75)  # 75th percentile
iqr = q3 - q1
```

**Interpretation:**
- **Low std dev:** Data clustered near mean (consistent)
- **High std dev:** Data spread out (variable)

**Example:**
- Store A sales: Mean=£1000, Std=£50 (consistent) ✅
- Store B sales: Mean=£1000, Std=£500 (unpredictable) ⚠️
"""
        )

        st.markdown("#### 📉 Distributions: Shapes of Data")
        st.markdown(
            """**Normal Distribution (Bell Curve)**

```python
import matplotlib.pyplot as plt

# Generate normal data
data = np.random.normal(loc=100, scale=15, size=1000)

# Plot
plt.hist(data, bins=30, edgecolor='black')
plt.title('Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
```

**Characteristics:**
- Symmetric (mirror image)
- Mean = Median = Mode
- 68% of data within 1 std dev of mean
- 95% within 2 std dev
- 99.7% within 3 std dev (Empirical Rule)

**Examples:** Height, IQ scores, measurement errors

---

**Skewed Distributions**

**Right-Skewed (Positive Skew):**
- Long tail on the right
- Mean > Median
- **Examples:** Income, house prices, website response time
- **Why:** Few extremely high values pull mean up

```python
# Income example
incomes = [30K, 35K, 40K, 45K, 50K, 55K, 200K, 500K]
# Mean = £119K (misleading!)
# Median = £47.5K (more representative) ✅
```

**Left-Skewed (Negative Skew):**
- Long tail on the left
- Mean < Median
- **Examples:** Test scores (most score high, few fail)

---

**Outliers Detection**

```python
# IQR Method
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1

# Outliers are beyond these bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data < lower_bound) | (data > upper_bound)]
```

**What to Do with Outliers:**
- **Investigate:** Data error? Legitimate extreme value?
- **Keep:** If real and important
- **Remove:** If data entry error
- **Transform:** Use log scale to reduce impact
"""
        )

        st.markdown("#### 🔗 Correlation: Relationships Between Variables")
        st.markdown(
            """**Correlation Coefficient (r): -1 to +1**

```python
import pandas as pd

# Sample data
data = pd.DataFrame({
    'ad_spend': [1000, 1500, 2000, 2500, 3000],
    'sales': [5000, 7000, 9000, 11000, 13000]
})

# Calculate correlation
correlation = data['ad_spend'].corr(data['sales'])  # 0.999
```

**Interpretation:**
- **r = +1:** Perfect positive (ad spend ↑, sales ↑)
- **r = 0:** No relationship
- **r = -1:** Perfect negative (price ↑, sales ↓)

**Common Ranges:**
- 0.0 to 0.3: Weak
- 0.3 to 0.7: Moderate
- 0.7 to 1.0: Strong

---

**Correlation ≠ Causation!**

**Example:**
- Ice cream sales and drowning deaths are correlated
- **Does ice cream cause drowning?** NO!
- **Confounding variable:** Summer (hot weather)
  - Hot weather → more ice cream sales
  - Hot weather → more swimming → more drownings

**Before claiming causation:**
1. Check for confounding variables
2. Consider reverse causation (does Y cause X?)
3. Ideally, run controlled experiment (A/B test)

---

**Scatter Plots for Correlation**

```python
import matplotlib.pyplot as plt

plt.scatter(data['ad_spend'], data['sales'])
plt.xlabel('Ad Spend (£)')
plt.ylabel('Sales (£)')
plt.title(f'Correlation: {correlation:.2f}')
plt.show()
```

**Visual Patterns:**
- **Positive:** Points trend upward
- **Negative:** Points trend downward
- **No correlation:** Random scatter
"""
        )

        st.markdown("#### 🧪 A/B Testing: The Gold Standard Experiment")
        st.markdown(
            """**What is A/B Testing?**

Compare two versions to see which performs better:
- **Control (A):** Current version
- **Treatment (B):** New version

**Real Examples:**
- Website: Current homepage vs new design
- Email: Subject line A vs subject line B
- Product: Price £9.99 vs £10.99

---

**Key Metrics:**

**1. Conversion Rate**

```python
# Control group
control_visitors = 1000
control_conversions = 120
control_rate = control_conversions / control_visitors  # 0.12 (12%)

# Treatment group
treatment_visitors = 1000
treatment_conversions = 150
treatment_rate = treatment_conversions / treatment_visitors  # 0.15 (15%)
```

**2. Lift (Improvement)**

```python
lift = ((treatment_rate - control_rate) / control_rate) * 100
# ((0.15 - 0.12) / 0.12) * 100 = 25% improvement
```

**3. Statistical Significance (Is it real?)**

The million-pound question: **Is 15% truly better than 12%, or just luck?**
"""
        )

        st.markdown("#### 📐 Hypothesis Testing Fundamentals")
        st.markdown(
            """**The Scientific Method for Data**

**Step 1: State Hypotheses**

- **Null Hypothesis (H₀):** No difference (Control = Treatment)
- **Alternative Hypothesis (H₁):** There IS a difference

**Example:**
- **H₀:** New homepage conversion = Old homepage conversion
- **H₁:** New homepage conversion > Old homepage conversion

---

**Step 2: Choose Significance Level (α)**

**α = 0.05 (5%)** is standard
- Means: Accept 5% chance of false positive
- **95% confidence level**

---

**Step 3: Calculate Test Statistic & P-Value**

```python
from scipy import stats

# A/B test data
control = [0]*880 + [1]*120  # 880 non-conversions, 120 conversions
treatment = [0]*850 + [1]*150

# Two-proportion z-test
from statsmodels.stats.proportion import proportions_ztest

counts = np.array([120, 150])
nobs = np.array([1000, 1000])

z_stat, p_value = proportions_ztest(counts, nobs)
print(f"P-value: {p_value:.4f}")  # 0.0219
```

**P-Value Interpretation:**
- **p < 0.05:** Statistically significant! (Reject H₀)
- **p ≥ 0.05:** Not significant (Cannot reject H₀)

**Example:** p = 0.0219
- Less than 0.05 ✅
- **Conclusion:** New homepage IS significantly better!

---

**Step 4: Make Decision**

| P-Value | Decision | Meaning |
|---------|----------|---------|
| p < 0.05 | Reject H₀ | Difference is real |
| p ≥ 0.05 | Fail to reject H₀ | Could be random chance |
"""
        )

        st.markdown("#### 🎯 Complete A/B Test Example: E-Commerce Checkout")
        st.markdown(
            """**Scenario:** Online retailer tests new checkout flow

**Setup:**
- **Control:** Current 3-step checkout
- **Treatment:** New 1-click checkout
- **Metric:** Purchase completion rate
- **Duration:** 2 weeks
- **Sample:** 5,000 visitors per group

---

**Results:**

| Group | Visitors | Purchases | Conversion Rate |
|-------|----------|-----------|-----------------|
| Control | 5,000 | 450 | 9.0% |
| Treatment | 5,000 | 550 | 11.0% |

**Calculations:**

```python
import numpy as np
from scipy import stats

# Data
control_n = 5000
control_conversions = 450
control_rate = 450 / 5000  # 0.09

treatment_n = 5000
treatment_conversions = 550
treatment_rate = 550 / 5000  # 0.11

# Lift
lift = ((treatment_rate - control_rate) / control_rate) * 100
print(f"Lift: {lift:.1f}%")  # 22.2%

# Statistical test
from statsmodels.stats.proportion import proportions_ztest

counts = np.array([450, 550])
nobs = np.array([5000, 5000])

z_stat, p_value = proportions_ztest(counts, nobs, alternative='smaller')
print(f"P-value: {p_value:.4f}")  # 0.0032

# Confidence interval for lift
from statsmodels.stats.proportion import confint_proportions_2indep

ci_low, ci_high = confint_proportions_2indep(
    450, 5000, 550, 5000, method='wald'
)
print(f"95% CI: {ci_low:.1%} to {ci_high:.1%}")
```

**Interpretation:**
- **Lift:** 22.2% improvement ✅
- **P-value:** 0.0032 < 0.05 (statistically significant!) ✅
- **95% Confidence Interval:** 0.7% to 3.3% absolute improvement
- **Decision:** **Launch new checkout!**

---

**Business Impact:**
- Current: 450 purchases / month
- After launch: 550 purchases / month (+100)
- Average order value: £50
- **Additional monthly revenue: £5,000**
- **Annual impact: £60,000**

**This is how A/B tests drive business decisions!**
"""
        )

        st.markdown("#### ⚠️ Common A/B Testing Pitfalls")
        st.markdown(
            """**1. Sample Size Too Small**

```python
# Bad: Only 50 visitors per group
control: 50 visitors, 5 conversions (10%)
treatment: 50 visitors, 8 conversions (16%)
# p-value = 0.37 (NOT significant due to small sample)

# Good: 1000 visitors per group
control: 1000 visitors, 100 conversions (10%)
treatment: 1000 visitors, 160 conversions (16%)
# p-value = 0.001 (significant!)
```

**Lesson:** Larger samples = more reliable results

---

**2. Stopping Test Too Early (Peeking)**

**Wrong:**
- Run test for 3 days
- See p < 0.05
- Stop early and declare winner

**Problem:** Random variation can cause early false positives

**Right:**
- Calculate required sample size upfront
- Run until target reached
- Analyze once at end

---

**3. Multiple Testing (P-Hacking)**

**Wrong:**
- Test 20 different metrics
- Find 1 with p < 0.05
- Declare success

**Problem:** Testing 20 metrics, 1 will be "significant" by chance!

**Right:**
- Pick ONE primary metric before starting
- Other metrics are secondary (informational only)

---

**4. Ignoring Practical Significance**

**Example:**
- Control: 10.00% conversion
- Treatment: 10.05% conversion
- p-value: 0.03 (statistically significant)

**But:** Is 0.05% improvement worth the engineering effort?

**Consider:**
- **Statistical significance:** Is difference real?
- **Practical significance:** Is difference meaningful?

---

**5. Not Accounting for Seasonality**

**Wrong:**
- Run A during Christmas shopping season
- Run B in January

**Right:**
- Run A and B simultaneously
- Randomize users to each group
"""
        )

        st.markdown("#### 🧮 Confidence Intervals: Quantifying Uncertainty")
        st.markdown(
            """**What is a Confidence Interval?**

A range where we're **95% confident** the true value lies.

```python
from scipy import stats

# Sample data
conversions = 120
visitors = 1000
conversion_rate = 120 / 1000  # 0.12 (12%)

# Calculate 95% CI
ci_low, ci_high = stats.binom.interval(
    0.95, visitors, conversion_rate
)
ci_low_pct = ci_low / visitors
ci_high_pct = ci_high / visitors

print(f"Conversion Rate: {conversion_rate:.1%}")
print(f"95% CI: {ci_low_pct:.1%} to {ci_high_pct:.1%}")
# Output: 10.1% to 14.1%
```

**Interpretation:**
"We're 95% confident the true conversion rate is between 10.1% and 14.1%"

**Narrow CI = More Certain**  
**Wide CI = Less Certain**

**How to Narrow CI:**
- Increase sample size
- Reduce variability
"""
        )

        st.markdown("#### 📊 Real Python A/B Test Implementation")
        st.markdown(
            """**Complete Workflow:**

```python
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

# 1. LOAD DATA
df = pd.read_csv('ab_test_results.csv')
# Columns: user_id, group (A or B), converted (0 or 1)

# 2. SUMMARIZE RESULTS
summary = df.groupby('group')['converted'].agg(['sum', 'count'])
summary['rate'] = summary['sum'] / summary['count']
print(summary)

# 3. CALCULATE LIFT
control_rate = summary.loc['A', 'rate']
treatment_rate = summary.loc['B', 'rate']
lift = ((treatment_rate - control_rate) / control_rate) * 100
print(f"Lift: {lift:.1f}%")

# 4. STATISTICAL TEST
counts = summary['sum'].values
nobs = summary['count'].values

z_stat, p_value = proportions_ztest(counts, nobs)
print(f"P-value: {p_value:.4f}")

# 5. DECISION
alpha = 0.05
if p_value < alpha:
    print(f"✅ SIGNIFICANT (p={p_value:.4f})")
    print(f"Treatment is {lift:.1f}% better than control")
else:
    print(f"❌ NOT SIGNIFICANT (p={p_value:.4f})")
    print("No clear winner")
```

**This code works for ANY A/B test!**
"""
        )

        st.markdown("#### 🚀 Practice & Next Steps")
        st.markdown(
            """**Master Statistics:**

**Practice Projects:**
1. **Analyze Public Datasets**
   - Kaggle datasets with A/B test results
   - Calculate conversion rates, lift, p-values
   - Practice interpreting results

2. **Your Own Experiments**
   - Test email subject lines (if you have newsletter)
   - Test social media post times
   - Compare productivity techniques

3. **Mock Interviews**
   - "How would you design an A/B test for [X]?"
   - "What does p-value mean?"
   - "When is correlation not causation?"

**Resources:**
- **Book:** Practical Statistics for Data Scientists
- **Course:** Khan Academy Statistics
- **Interactive:** Seeing Theory (https://seeing-theory.brown.edu)
- **A/B Testing:** Evan Miller's AB Test Calculator

---

**Job Interview Ready:**

You can now:
- ✅ Calculate mean, median, standard deviation
- ✅ Understand distributions (normal, skewed)
- ✅ Interpret correlation correctly
- ✅ Design and analyze A/B tests
- ✅ Calculate statistical significance
- ✅ Explain confidence intervals
- ✅ Avoid common pitfalls
- ✅ Make data-driven decisions

**Statistics gives you credibility.**

Without it, you're just guessing. With it, you're making **evidence-based recommendations** that executives trust.

**Next:** Unit 6 (Visualization) teaches you to communicate these insights visually!
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS: Unit 5 Statistics & A/B Testing")
        st.markdown(
            """**Complete these 2 labs to master statistical analysis:**

---

## Lab 1: Descriptive Statistics & Distributions (60 min)

**Setup: E-commerce Revenue Data**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate sample e-commerce revenue data
np.random.seed(42)
n_customers = 500

data = {
    'customer_id': range(1, n_customers + 1),
    'revenue': np.random.lognormal(5, 1.2, n_customers).round(2),  # Skewed distribution
    'age': np.random.normal(35, 12, n_customers).astype(int),
    'orders': np.random.poisson(3, n_customers),
    'days_since_last': np.random.exponential(30, n_customers).astype(int)
}

df = pd.DataFrame(data)
df.to_csv('customer_revenue.csv', index=False)
print("✅ Created customer_revenue.csv")
print(df.head())
```

**Part A: Central Tendency (20 min)**

```python
df = pd.read_csv('customer_revenue.csv')

# Mean, Median, Mode
mean_revenue = df['revenue'].mean()
median_revenue = df['revenue'].median()
mode_revenue = df['revenue'].mode()[0]

print("Revenue Distribution:")
print(f"Mean:   £{mean_revenue:,.2f}")
print(f"Median: £{median_revenue:,.2f}")
print(f"Mode:   £{mode_revenue:,.2f}")

# Why are they different? (skewed distribution!)
plt.figure(figsize=(10, 6))
plt.hist(df['revenue'], bins=50, edgecolor='black', alpha=0.7)
plt.axvline(mean_revenue, color='red', linestyle='--', label=f'Mean: £{mean_revenue:.2f}')
plt.axvline(median_revenue, color='green', linestyle='--', label=f'Median: £{median_revenue:.2f}')
plt.xlabel('Revenue (£)')
plt.ylabel('Frequency')
plt.title('Revenue Distribution (Right-Skewed)')
plt.legend()
plt.show()

# Lesson: Median better for skewed data!
```

**Part B: Spread & Variability (20 min)**

```python
# Variance and Standard Deviation
revenue_std = df['revenue'].std()
revenue_var = df['revenue'].var()
revenue_min = df['revenue'].min()
revenue_max = df['revenue'].max()
revenue_range = revenue_max - revenue_min

print(f"\\nSpread Metrics:")
print(f"Std Dev:  £{revenue_std:,.2f}")
print(f"Variance: £{revenue_var:,.2f}")
print(f"Range:    £{revenue_range:,.2f} (£{revenue_min:.2f} - £{revenue_max:.2f})")

# Interquartile Range (IQR) - robust to outliers
q1 = df['revenue'].quantile(0.25)
q3 = df['revenue'].quantile(0.75)
iqr = q3 - q1

print(f"\\nQuartiles:")
print(f"Q1 (25%): £{q1:,.2f}")
print(f"Q3 (75%): £{q3:,.2f}")
print(f"IQR:      £{iqr:,.2f}")

# Identify outliers (>1.5 * IQR)
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = df[(df['revenue'] < lower_bound) | (df['revenue'] > upper_bound)]

print(f"\\nOutliers: {len(outliers)} customers ({len(outliers)/len(df)*100:.1f}%)")
```

**Part C: Correlation Analysis (20 min)**

```python
# Correlation: Revenue vs Age, Orders, Recency
correlation_matrix = df[['revenue', 'age', 'orders', 'days_since_last']].corr()
print("\\nCorrelation Matrix:")
print(correlation_matrix)

# Visualize
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Feature Correlations')
plt.show()

# Scatter plot: Revenue vs Orders
plt.figure(figsize=(10, 6))
plt.scatter(df['orders'], df['revenue'], alpha=0.5)
plt.xlabel('Number of Orders')
plt.ylabel('Revenue (£)')
plt.title(f'Revenue vs Orders (Correlation: {df["revenue"].corr(df["orders"]):.2f})')
plt.show()

# WARNING: Correlation ≠ Causation!
print("\\n⚠️ Remember: Correlation does NOT prove causation!")
```

---

## Lab 2: A/B Testing Analysis (75 min)

**Scenario:** E-commerce website testing new checkout button color

**Setup: Generate A/B Test Data**

```python
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)

# Control group (Blue button)
control_visitors = 1000
control_conversions = np.random.binomial(1, 0.10, control_visitors)  # 10% conversion

# Treatment group (Orange button)
treatment_visitors = 1000
treatment_conversions = np.random.binomial(1, 0.12, treatment_visitors)  # 12% conversion

# Create DataFrame
ab_test = pd.DataFrame({
    'group': ['control'] * control_visitors + ['treatment'] * treatment_visitors,
    'converted': np.concatenate([control_conversions, treatment_conversions])
})

ab_test.to_csv('ab_test_results.csv', index=False)
print("✅ Created ab_test_results.csv")
```

**Part A: Descriptive Analysis (20 min)**

```python
df = pd.read_csv('ab_test_results.csv')

# Calculate conversion rates
results = df.groupby('group')['converted'].agg([
    ('visitors', 'count'),
    ('conversions', 'sum'),
    ('conversion_rate', 'mean')
])

print("A/B Test Results:")
print(results)

# Calculate lift
control_rate = results.loc['control', 'conversion_rate']
treatment_rate = results.loc['treatment', 'conversion_rate']
lift = ((treatment_rate - control_rate) / control_rate) * 100

print(f"\\nControl Conversion Rate:    {control_rate:.2%}")
print(f"Treatment Conversion Rate:  {treatment_rate:.2%}")
print(f"Absolute Lift:              {treatment_rate - control_rate:.2%}")
print(f"Relative Lift:              {lift:.1f}%")

# Visualize
import matplotlib.pyplot as plt
groups = ['Control\\n(Blue)', 'Treatment\\n(Orange)']
rates = [control_rate, treatment_rate]

plt.figure(figsize=(10, 6))
plt.bar(groups, rates, color=['#3498db', '#e67e22'])
plt.ylabel('Conversion Rate')
plt.title(f'A/B Test Results: {lift:.1f}% Lift with Orange Button')
plt.ylim(0, max(rates) * 1.2)
for i, v in enumerate(rates):
    plt.text(i, v + 0.005, f'{v:.2%}', ha='center', fontweight='bold')
plt.show()
```

**Part B: Statistical Significance (30 min)**

```python
# Hypothesis Testing
# H0 (Null): No difference between groups
# H1 (Alternative): Treatment performs better

# Get raw data
control_data = df[df['group'] == 'control']['converted']
treatment_data = df[df['group'] == 'treatment']['converted']

# Two-proportion z-test
from statsmodels.stats.proportion import proportions_ztest

conversions = [control_data.sum(), treatment_data.sum()]
visitors = [len(control_data), len(treatment_data)]

z_stat, p_value = proportions_ztest(conversions, visitors, alternative='smaller')

print("\\nStatistical Significance Test:")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value:     {p_value:.4f}")

# Interpretation
alpha = 0.05  # Significance level (95% confidence)
if p_value < alpha:
    print(f"\\n✅ SIGNIFICANT (p < {alpha})")
    print("We can confidently say the orange button performs better!")
else:
    print(f"\\n❌ NOT SIGNIFICANT (p >= {alpha})")
    print("Difference could be due to random chance. Don't launch yet!")

# Effect size (Cohen's h)
from statsmodels.stats.proportion import proportion_effectsize
effect_size = proportion_effectsize(control_rate, treatment_rate)
print(f"\\nEffect Size (Cohen's h): {effect_size:.4f}")
```

**Part C: Confidence Intervals (25 min)**

```python
from statsmodels.stats.proportion import proportion_confint

# 95% Confidence Interval for each group
control_ci = proportion_confint(
    control_data.sum(), 
    len(control_data), 
    alpha=0.05, 
    method='wilson'
)

treatment_ci = proportion_confint(
    treatment_data.sum(), 
    len(treatment_data), 
    alpha=0.05, 
    method='wilson'
)

print("\\n95% Confidence Intervals:")
print(f"Control:   {control_ci[0]:.2%} - {control_ci[1]:.2%}")
print(f"Treatment: {treatment_ci[0]:.2%} - {treatment_ci[1]:.2%}")

# Visualize with error bars
fig, ax = plt.subplots(figsize=(10, 6))
groups = ['Control', 'Treatment']
rates = [control_rate, treatment_rate]
errors = [
    [control_rate - control_ci[0], control_ci[1] - control_rate],
    [treatment_rate - treatment_ci[0], treatment_ci[1] - treatment_rate]
]

x_pos = np.arange(len(groups))
ax.bar(x_pos, rates, yerr=np.array(errors).T, capsize=10, 
       color=['#3498db', '#e67e22'], alpha=0.7)
ax.set_ylabel('Conversion Rate')
ax.set_xticks(x_pos)
ax.set_xticklabels(groups)
ax.set_title('A/B Test with 95% Confidence Intervals')
ax.set_ylim(0, max(rates) * 1.3)
plt.show()

# Business recommendation
print("\\n📊 BUSINESS RECOMMENDATION:")
if p_value < 0.05:
    expected_lift = (treatment_rate - control_rate) * 10000  # Assume 10K daily visitors
    print(f"✅ LAUNCH orange button!")
    print(f"Expected additional conversions: ~{expected_lift:.0f} per day")
else:
    print("❌ Keep testing or try a different variant")
```

---

## Lab 3: Complete Statistical Analysis Mini-Project (90 min)

**Objective:** Conduct end-to-end statistical analysis for business decision

**Scenario:** E-commerce company launching loyalty program

**Part A: Experimental Design (20 min)**

```python
import pandas as pd
import numpy as np
from scipy import stats

# Design A/B test for loyalty program
np.random.seed(42)

# Control: No loyalty program (1000 customers)
# Treatment: Loyalty program (1000 customers)

# Simulate 3 months of data
control_purchases = np.random.poisson(2.5, 1000)  # Avg 2.5 purchases/month
treatment_purchases = np.random.poisson(3.2, 1000)  # Loyalty increases to 3.2

control_revenue = np.random.normal(120, 40, 1000)  # Avg £120/month
treatment_revenue = np.random.normal(145, 45, 1000)  # Loyalty increases to £145

df = pd.DataFrame({
    'group': ['Control']*1000 + ['Treatment']*1000,
    'purchases': np.concatenate([control_purchases, treatment_purchases]),
    'revenue': np.concatenate([control_revenue, treatment_revenue]),
    'customer_id': range(2000)
})

print("="*60)
print("EXPERIMENT DESIGN")
print("="*60)
print(f"Sample size: {len(df)}")
print(f"\\nControl group: {(df['group']=='Control').sum()} customers")
print(f"Treatment group: {(df['group']=='Treatment').sum()} customers")
print(f"\\nTarget metric: Monthly purchases & revenue")
print(f"Hypothesis: Loyalty program increases engagement & spend")
```

---

**Part B: Descriptive Analysis (30 min)**

```python
# Summary statistics by group
summary = df.groupby('group').agg({
    'purchases': ['mean', 'std', 'median'],
    'revenue': ['mean', 'std', 'median']
})

print("\\n" + "="*60)
print("DESCRIPTIVE STATISTICS")
print("="*60)
print(summary)

# Calculate lift
control_avg_purchases = df[df['group']=='Control']['purchases'].mean()
treatment_avg_purchases = df[df['group']=='Treatment']['purchases'].mean()
purchase_lift = (treatment_avg_purchases - control_avg_purchases) / control_avg_purchases

control_avg_revenue = df[df['group']=='Control']['revenue'].mean()
treatment_avg_revenue = df[df['group']=='Treatment']['revenue'].mean()
revenue_lift = (treatment_avg_revenue - control_avg_revenue) / control_avg_revenue

print(f"\\nPurchase Lift: {purchase_lift:.1%}")
print(f"Revenue Lift: {revenue_lift:.1%}")

# Visualize distributions
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Purchases
axes[0].hist(df[df['group']=='Control']['purchases'], alpha=0.5, label='Control', bins=15)
axes[0].hist(df[df['group']=='Treatment']['purchases'], alpha=0.5, label='Treatment', bins=15)
axes[0].set_title('Monthly Purchases Distribution')
axes[0].set_xlabel('Purchases')
axes[0].legend()

# Revenue
axes[1].hist(df[df['group']=='Control']['revenue'], alpha=0.5, label='Control', bins=15)
axes[1].hist(df[df['group']=='Treatment']['revenue'], alpha=0.5, label='Treatment', bins=15)
axes[1].set_title('Monthly Revenue Distribution')
axes[1].set_xlabel('Revenue (£)')
axes[1].legend()

plt.tight_layout()
plt.show()
```

---

**Part C: Statistical Testing & Business Decision (40 min)**

```python
# Test 1: Are purchases significantly different?
control_purchases = df[df['group']=='Control']['purchases']
treatment_purchases = df[df['group']=='Treatment']['purchases']

t_stat_purchases, p_value_purchases = stats.ttest_ind(control_purchases, treatment_purchases)

print("="*60)
print("HYPOTHESIS TEST: PURCHASES")
print("="*60)
print(f"H0: Loyalty program has no effect on purchases")
print(f"H1: Loyalty program increases purchases")
print(f"\\nT-statistic: {t_stat_purchases:.3f}")
print(f"P-value: {p_value_purchases:.4f}")

if p_value_purchases < 0.05:
    print("\\n✅ REJECT H0: Statistically significant increase")
else:
    print("\\n❌ FAIL TO REJECT H0: No significant effect")

# Test 2: Are revenues significantly different?
control_revenue = df[df['group']=='Control']['revenue']
treatment_revenue = df[df['group']=='Treatment']['revenue']

t_stat_revenue, p_value_revenue = stats.ttest_ind(control_revenue, treatment_revenue)

print("\\n" + "="*60)
print("HYPOTHESIS TEST: REVENUE")
print("="*60)
print(f"H0: Loyalty program has no effect on revenue")
print(f"H1: Loyalty program increases revenue")
print(f"\\nT-statistic: {t_stat_revenue:.3f}")
print(f"P-value: {p_value_revenue:.4f}")

if p_value_revenue < 0.05:
    print("\\n✅ REJECT H0: Statistically significant increase")
else:
    print("\\n❌ FAIL TO REJECT H0: No significant effect")

# Calculate confidence intervals
control_ci = stats.t.interval(0.95, len(control_revenue)-1,
                               loc=control_revenue.mean(),
                               scale=stats.sem(control_revenue))
treatment_ci = stats.t.interval(0.95, len(treatment_revenue)-1,
                                 loc=treatment_revenue.mean(),
                                 scale=stats.sem(treatment_revenue))

print("\\n" + "="*60)
print("95% CONFIDENCE INTERVALS - REVENUE")
print("="*60)
print(f"Control:   £{control_ci[0]:.2f} - £{control_ci[1]:.2f}")
print(f"Treatment: £{treatment_ci[0]:.2f} - £{treatment_ci[1]:.2f}")

# Business impact calculation
total_customers = 50000  # Company has 50K customers
annual_months = 12

additional_revenue_per_customer = treatment_avg_revenue - control_avg_revenue
total_additional_revenue = total_customers * additional_revenue_per_customer * annual_months

program_cost_per_customer = 2  # £2/month
total_program_cost = total_customers * program_cost_per_customer * annual_months

net_benefit = total_additional_revenue - total_program_cost
roi = (net_benefit / total_program_cost) * 100

print("\\n" + "="*60)
print("BUSINESS IMPACT ANALYSIS")
print("="*60)
print(f"Total customers: {total_customers:,}")
print(f"\\nAdditional revenue per customer: £{additional_revenue_per_customer:.2f}/month")
print(f"Total additional revenue (annual): £{total_additional_revenue:,.0f}")
print(f"\\nProgram cost per customer: £{program_cost_per_customer}/month")
print(f"Total program cost (annual): £{total_program_cost:,.0f}")
print(f"\\nNet benefit: £{net_benefit:,.0f}")
print(f"ROI: {roi:.0f}%")

# Final recommendation
print("\\n" + "="*60)
print("RECOMMENDATION")
print("="*60)
if p_value_revenue < 0.05 and roi > 100:
    print("✅ LAUNCH loyalty program")
    print(f"   - Statistically significant revenue increase (p={p_value_revenue:.4f})")
    print(f"   - Strong ROI ({roi:.0f}%)")
    print(f"   - Expected net benefit: £{net_benefit:,.0f} annually")
elif p_value_revenue < 0.05:
    print("⚠️ Significant effect but marginal ROI")
    print("   - Consider reducing program costs")
    print("   - Or target high-value customers only")
else:
    print("❌ Do NOT launch - insufficient evidence")
    print("   - Continue testing with larger sample")
    print("   - Or redesign program features")

print("="*60)
```

---

**Lab 3 Completion Checklist:**
- ☐ Designed A/B test experiment
- ☐ Calculated descriptive statistics
- ☐ Created distribution visualizations
- ☐ Performed t-tests for purchases & revenue
- ☐ Computed 95% confidence intervals
- ☐ Calculated business impact (ROI)
- ☐ Made data-driven recommendation
- ☐ Considered both statistical AND practical significance

**Next:** Unit 6 Visualization labs teach you to communicate these results visually!
"""
        )

        st.markdown("---")
        st.markdown("#### 📐 Regression Analysis Fundamentals")
        st.markdown(
            """**Simple Linear Regression**

**Goal:** Model relationship between two variables

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Example: Advertising spend vs Revenue
np.random.seed(42)
advertising = np.array([10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
revenue = advertising * 2.5 + np.random.normal(0, 5, 10) + 10

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(advertising, revenue)

print(f"Equation: Revenue = {intercept:.2f} + {slope:.2f} × Advertising")
print(f"R-squared: {r_value**2:.3f}")
print(f"P-value: {p_value:.4f}")

# Predict
new_spend = 60
predicted_revenue = intercept + slope * new_spend
print(f"\\nPrediction: £{new_spend}K ad spend → £{predicted_revenue:.2f}K revenue")

# Visualize
plt.figure(figsize=(10, 6))
plt.scatter(advertising, revenue, s=100, alpha=0.6, label='Actual')
plt.plot(advertising, intercept + slope*advertising, 'r-', linewidth=2, label='Fitted Line')
plt.xlabel('Advertising Spend (£K)')
plt.ylabel('Revenue (£K)')
plt.title(f'Linear Regression (R² = {r_value**2:.3f})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**Interpretation:**
- **Slope:** For every £1K in ads, revenue increases by £2.5K
- **R²:** Model explains 95% of revenue variance
- **P-value < 0.05:** Statistically significant relationship
"""
        )

        st.markdown("---")
        st.markdown("#### 🎲 Probability Distributions")
        st.markdown(
            """**Common Distributions in Data Science**

**1. Normal Distribution (Bell Curve)**

```python
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

# Customer ages: mean=35, std=10
mean_age = 35
std_age = 10

# Generate data
ages = np.random.normal(mean_age, std_age, 1000)

# Probabilities
prob_under_30 = norm.cdf(30, mean_age, std_age)
prob_over_50 = 1 - norm.cdf(50, mean_age, std_age)
prob_between_30_40 = norm.cdf(40, mean_age, std_age) - norm.cdf(30, mean_age, std_age)

print(f"P(age < 30) = {prob_under_30:.1%}")
print(f"P(age > 50) = {prob_over_50:.1%}")
print(f"P(30 < age < 40) = {prob_between_30_40:.1%}")

# Visualize
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(ages, bins=30, density=True, alpha=0.6, edgecolor='black')
x = np.linspace(0, 70, 100)
ax.plot(x, norm.pdf(x, mean_age, std_age), 'r-', linewidth=2, label='Normal PDF')
ax.set_xlabel('Age')
ax.set_ylabel('Density')
ax.set_title('Customer Age Distribution')
ax.legend()
plt.show()
```

---

**2. Poisson Distribution (Count Events)**

```python
from scipy.stats import poisson

# Website visits per day: average = 5
lambda_rate = 5

# Probabilities
for k in range(0, 10):
    prob = poisson.pmf(k, lambda_rate)
    print(f"P(exactly {k} visits) = {prob:.3f}")

# Business question: What's probability of >8 visits?
prob_more_than_8 = 1 - poisson.cdf(8, lambda_rate)
print(f"\\nP(more than 8 visits) = {prob_more_than_8:.1%}")
```

---

**3. Binomial Distribution (Success/Failure)**

```python
from scipy.stats import binom

# Email campaign: 1000 emails, 5% open rate
n_emails = 1000
open_rate = 0.05

# Expected opens
expected = n_emails * open_rate
print(f"Expected opens: {expected:.0f}")

# Probability of exactly 60 opens?
prob_60 = binom.pmf(60, n_emails, open_rate)
print(f"P(exactly 60 opens) = {prob_60:.3f}")

# Probability of at least 40 opens?
prob_at_least_40 = 1 - binom.cdf(39, n_emails, open_rate)
print(f"P(≥40 opens) = {prob_at_least_40:.1%}")
```
"""
        )

        st.markdown("---")
        st.markdown("#### 📊 Sampling & Central Limit Theorem")
        st.markdown(
            """**Why Sampling Matters**

You can't survey ALL customers. Sample wisely!

```python
import numpy as np
import matplotlib.pyplot as plt

# True population: 100K customers, avg spend = £50, std = £20
np.random.seed(42)
population = np.random.normal(50, 20, 100000)
true_mean = population.mean()

print(f"True population mean: £{true_mean:.2f}")

# Take multiple samples
sample_sizes = [10, 30, 100, 500]
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, n in enumerate(sample_sizes):
    # Take 1000 samples of size n
    sample_means = []
    for _ in range(1000):
        sample = np.random.choice(population, n, replace=False)
        sample_means.append(sample.mean())
    
    # Plot distribution of sample means
    axes[idx].hist(sample_means, bins=30, edgecolor='black', alpha=0.7)
    axes[idx].axvline(true_mean, color='r', linestyle='--', linewidth=2, label='True Mean')
    axes[idx].set_title(f'Sample Size = {n}')
    axes[idx].set_xlabel('Sample Mean')
    axes[idx].legend()
    
    # Standard error
    std_error = np.std(sample_means)
    axes[idx].text(0.05, 0.95, f'SE = £{std_error:.2f}', 
                   transform=axes[idx].transAxes, verticalalignment='top')

plt.suptitle('Central Limit Theorem: Sample Means Converge to Normal')
plt.tight_layout()
plt.show()

print("\\n📊 Key Insight:")
print("Larger samples → More accurate estimates!")
print("Sample means are normally distributed around true mean")
```

**Standard Error Formula:**

SE = σ / √n

- As n increases, SE decreases
- Need 4x sample size to halve SE
"""
        )

        st.markdown("---")
        st.markdown("#### 🔬 Hypothesis Testing Deep Dive")
        st.markdown(
            """**Complete Framework**

**Step-by-Step Process:**

```python
import numpy as np
from scipy import stats

# Scenario: New checkout process claims to reduce cart abandonment
# Old rate: 65%, New rate: 58% (from 500 user test)

# 1. State Hypotheses
print("="*60)
print("HYPOTHESIS TEST")
print("="*60)
print("H₀ (Null): New process has no effect (p = 0.65)")
print("H₁ (Alt):  New process reduces abandonment (p < 0.65)")
print("α (Significance): 0.05")

# 2. Collect Data
n = 500
observed_abandonment = 0.58
null_hypothesis_rate = 0.65

# 3. Calculate Test Statistic (Z-test for proportions)
p0 = null_hypothesis_rate
se = np.sqrt(p0 * (1-p0) / n)
z_score = (observed_abandonment - p0) / se

print(f"\\nObserved rate: {observed_abandonment:.1%}")
print(f"Standard Error: {se:.4f}")
print(f"Z-score: {z_score:.2f}")

# 4. Calculate P-value
p_value = stats.norm.cdf(z_score)  # One-tailed test
print(f"P-value: {p_value:.4f}")

# 5. Make Decision
print("\\n" + "="*60)
print("DECISION")
print("="*60)
if p_value < 0.05:
    print("✅ REJECT null hypothesis")
    print("Evidence suggests new process reduces abandonment")
    
    # Calculate effect size
    reduction = (null_hypothesis_rate - observed_abandonment) / null_hypothesis_rate
    print(f"\\nEffect: {reduction:.1%} reduction in abandonment")
    
    # Business impact
    annual_orders = 100000
    additional_orders = annual_orders * (null_hypothesis_rate - observed_abandonment)
    revenue_per_order = 75
    annual_impact = additional_orders * revenue_per_order
    print(f"Business Impact: ~{additional_orders:,.0f} additional orders")
    print(f"Revenue Impact: £{annual_impact:,.0f} annually")
else:
    print("❌ FAIL TO REJECT null hypothesis")
    print("Insufficient evidence of improvement")
```

---

**Type I & Type II Errors**

```python
# Confusion Matrix for Hypothesis Testing
import pandas as pd

confusion = pd.DataFrame({
    'H₀ is True': ['Correct Decision (1-α)', 'Type I Error (α)'],
    'H₀ is False': ['Type II Error (β)', 'Correct Decision (1-β)']
}, index=['Fail to Reject H₀', 'Reject H₀'])

print(confusion)
print("\\nType I Error (False Positive):")
print("  - Conclude there's an effect when there isn't")
print("  - Probability = α (significance level)")
print("\\nType II Error (False Negative):")
print("  - Fail to detect a real effect")
print("  - Probability = β")
print("\\nPower = 1 - β (ability to detect real effects)")
```
"""
        )

        st.markdown("---")
        st.markdown("#### 📈 Statistical Significance vs Practical Significance")
        st.markdown(
            """**Critical Distinction for Business Decisions**

```python
import numpy as np
from scipy import stats

# Scenario: Website redesign A/B test
# Control: 10,000 visitors, 500 conversions (5.00%)
# Treatment: 10,000 visitors, 520 conversions (5.20%)

control_conversions = 500
control_visitors = 10000
treatment_conversions = 520
treatment_visitors = 10000

control_rate = control_conversions / control_visitors
treatment_rate = treatment_conversions / treatment_visitors

# Statistical test
pooled_rate = (control_conversions + treatment_conversions) / (control_visitors + treatment_visitors)
se = np.sqrt(pooled_rate * (1-pooled_rate) * (1/control_visitors + 1/treatment_visitors))
z_score = (treatment_rate - control_rate) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

print("="*60)
print("STATISTICAL SIGNIFICANCE")
print("="*60)
print(f"Control rate: {control_rate:.2%}")
print(f"Treatment rate: {treatment_rate:.2%}")
print(f"Lift: {(treatment_rate - control_rate):.2%} ({(treatment_rate/control_rate - 1)*100:.1f}%)")
print(f"\\nP-value: {p_value:.4f}")

if p_value < 0.05:
    print("✅ Statistically significant!")
else:
    print("❌ Not statistically significant")

# Practical Significance
print("\\n" + "="*60)
print("PRACTICAL SIGNIFICANCE")
print("="*60)

annual_visitors = 1_000_000
additional_conversions = annual_visitors * (treatment_rate - control_rate)
revenue_per_conversion = 50
annual_revenue_impact = additional_conversions * revenue_per_conversion

redesign_cost = 50000
development_months = 3

print(f"Annual visitors: {annual_visitors:,}")
print(f"Additional conversions: {additional_conversions:,.0f}")
print(f"Additional revenue: £{annual_revenue_impact:,.0f}")
print(f"\\nRedesign cost: £{redesign_cost:,}")
print(f"Development time: {development_months} months")
print(f"\\nROI: {(annual_revenue_impact - redesign_cost) / redesign_cost * 100:.0f}%")

print("\\n" + "="*60)
print("RECOMMENDATION")
print("="*60)
if p_value < 0.05 and annual_revenue_impact > redesign_cost * 2:
    print("✅ LAUNCH redesign")
    print("Both statistically AND practically significant")
elif p_value < 0.05:
    print("⚠️ Statistically significant but marginal ROI")
    print("Consider cheaper implementation or continue testing")
else:
    print("❌ Keep testing or try different approach")
```

**Key Lesson:**
- Statistical significance ≠ Business significance
- Always calculate ROI
- Consider implementation costs
"""
        )

        st.markdown("---")
        st.markdown("#### 🎯 Interview Questions: Statistics")
        st.markdown(
            """**Common Data Science Interview Questions**

**Q1: What's the difference between mean and median? When do you use each?**

**Answer:**
- **Mean:** Average of all values. Sensitive to outliers.
- **Median:** Middle value. Robust to outliers.
- **Use median when:** Data is skewed or has outliers (e.g., house prices, salaries)
- **Use mean when:** Data is normally distributed (e.g., heights, test scores)

Example: Salaries [£30K, £32K, £35K, £500K]
- Mean = £149K (misleading!)
- Median = £33.5K (representative)

---

**Q2: Explain p-value in simple terms.**

**Answer:**
"P-value is the probability of seeing results this extreme if there's actually no real effect. If p-value < 0.05, we conclude the effect is unlikely due to chance alone."

Bad answer: "It's the probability the null hypothesis is true" ❌

---

**Q3: What is statistical power and why does it matter?**

**Answer:**
Power = Probability of detecting a real effect when it exists.

Low power (< 80%) means you might miss real improvements!

Increases with:
- Larger sample size
- Larger effect size
- Higher significance level (α)

---

**Q4: Your A/B test shows treatment has 5.2% conversion vs control's 5.0%. P-value = 0.045. What do you do?**

**Answer:**
"Check practical significance first:
1. Calculate additional conversions and revenue
2. Compare to implementation cost
3. Consider confidence intervals
4. P-value alone doesn't justify launch

If ROI is strong (>200%) and CI is tight, recommend launch with monitoring plan."

---

**Q5: What's the Central Limit Theorem and why is it important?**

**Answer:**
"Sample means follow a normal distribution regardless of population distribution, if n is large enough (n≥30).

This lets us:
- Make inferences about populations from samples
- Calculate confidence intervals
- Perform hypothesis tests

It's why sampling works!"
"""
        )

        st.markdown("---")
        st.markdown("#### 📚 Key Statistical Concepts Summary")
        st.markdown(
            """**Essential Formulas:**

**Descriptive Statistics:**
- Mean: μ = Σx / n
- Variance: σ² = Σ(x - μ)² / n
- Standard Deviation: σ = √variance
- Correlation: r = cov(X,Y) / (σₓ × σᵧ)

**Inferential Statistics:**
- Standard Error: SE = σ / √n
- Z-score: z = (x - μ) / σ
- Confidence Interval: x̄ ± z × SE
- T-test: t = (x̄₁ - x̄₂) / SE_difference

**A/B Testing:**
- Conversion Rate: conversions / visitors
- Lift: (treatment_rate - control_rate) / control_rate
- Statistical Significance: Use z-test or chi-square
- Sample Size: n ≈ 16σ² / (effect_size)²

**Remember:**
- ✅ Always visualize data first
- ✅ Check assumptions before tests
- ✅ Report effect sizes, not just p-values
- ✅ Consider practical vs statistical significance
- ✅ Use confidence intervals
- ✅ Document your methodology
"""
        )

    elif unit_number == 6:
        st.markdown("---")
        st.markdown("#### 📊 Why Data Visualization Matters")
        st.markdown(
            """**"A picture is worth a thousand rows of data"**

**Why Visualize?**
- **Faster insights:** Spot patterns in seconds vs hours of staring at numbers
- **Communicate findings:** Executives don't read code or tables
- **Persuade stakeholders:** Visual evidence drives decisions
- **Discover hidden patterns:** Correlations, outliers, trends

**Real Impact:**
- 65% of people are visual learners
- Charts are remembered 6x longer than text
- Executives spend 3 minutes on reports (charts better grab attention!)

**Your Goal:** Turn data → insights → action through visual storytelling.
"""
        )

        st.markdown("#### 📈 Chart Selection Guide")
        st.markdown(
            """**Choose the Right Chart for Your Question**

| Question Type | Best Chart | When to Use |
|---------------|------------|-------------|
| Compare categories | Bar chart | Revenue by country, products by sales |
| Show trend over time | Line chart | Daily visitors, monthly revenue |
| Show relationship | Scatter plot | Ad spend vs sales, age vs income |
| Show distribution | Histogram | Customer ages, order values |
| Show composition | Pie chart | Market share (max 5 slices!) |
| Compare many categories | Horizontal bar | Top 20 customers |
| Show correlation matrix | Heatmap | Feature correlations in ML |

**Golden Rule:** Simplest chart that answers the question wins!
"""
        )

        st.markdown("#### 🎨 Matplotlib: The Foundation")
        st.markdown(
            """**Basic Plotting with Matplotlib**

```python
import matplotlib.pyplot as plt
import pandas as pd

# Sample data
df = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'revenue': [50000, 55000, 48000, 62000, 58000]
})

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot
ax.plot(df['month'], df['revenue'], marker='o', linewidth=2, color='#2E86AB')

# Customize
ax.set_title('Monthly Revenue Trend', fontsize=16, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue (£)', fontsize=12)
ax.grid(True, alpha=0.3)

# Format y-axis as currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

plt.tight_layout()
plt.show()
```

---

**Bar Chart Example:**

```python
# Top 5 products by sales
products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
sales = [45000, 38000, 32000, 28000, 25000]

fig, ax = plt.subplots(figsize=(10, 6))

# Horizontal bar chart (easier to read long labels)
ax.barh(products, sales, color='#A23B72')

# Add value labels
for i, v in enumerate(sales):
    ax.text(v + 500, i, f'£{v:,}', va='center')

ax.set_xlabel('Sales (£)')
ax.set_title('Top 5 Products by Sales')
ax.invert_yaxis()  # Highest at top

plt.tight_layout()
plt.show()
```

---

**Scatter Plot with Trend:**

```python
import numpy as np

# Sample data
ad_spend = np.array([1000, 1500, 2000, 2500, 3000, 3500, 4000])
sales = np.array([5000, 7000, 8500, 11000, 12000, 14500, 15000])

fig, ax = plt.subplots(figsize=(10, 6))

# Scatter
ax.scatter(ad_spend, sales, s=100, alpha=0.6, color='#F18F01')

# Trend line
z = np.polyfit(ad_spend, sales, 1)
p = np.poly1d(z)
ax.plot(ad_spend, p(ad_spend), "--", color='red', alpha=0.8, label='Trend')

ax.set_xlabel('Ad Spend (£)')
ax.set_ylabel('Sales (£)')
ax.set_title('Ad Spend vs Sales (Correlation: 0.98)')
ax.legend()

plt.tight_layout()
plt.show()
```
"""
        )

        st.markdown("#### 🎯 Seaborn: Statistical Visualizations")
        st.markdown(
            """**Seaborn = Matplotlib + Better Defaults + Statistical Focus**

```python
import seaborn as sns
import pandas as pd

# Set style
sns.set_style('whitegrid')
sns.set_palette('husl')

# Sample data
df = pd.read_csv('sales_data.csv')
```

---

**Distribution Plot:**

```python
# Revenue distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['revenue'], bins=30, kde=True)
plt.title('Revenue Distribution')
plt.xlabel('Revenue (£)')
plt.ylabel('Frequency')
plt.show()
```

---

**Box Plot (Compare Distributions):**

```python
# Revenue by country
plt.figure(figsize=(10, 6))
sns.boxplot(x='country', y='revenue', data=df)
plt.title('Revenue Distribution by Country')
plt.ylabel('Revenue (£)')
plt.xticks(rotation=45)
plt.show()
```

**Interpretation:**
- Box: 25th to 75th percentile (middle 50%)
- Line in box: Median
- Whiskers: Min/max (excluding outliers)
- Dots: Outliers

---

**Heatmap (Correlation Matrix):**

```python
# Correlation between numerical columns
plt.figure(figsize=(10, 8))
correlation = df[['revenue', 'order_count', 'avg_order_value', 'customer_age']].corr()

sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1)
plt.title('Feature Correlation Matrix')
plt.show()
```

---

**Count Plot (Categorical):**

```python
# Orders by category
plt.figure(figsize=(10, 6))
sns.countplot(y='product_category', data=df, order=df['product_category'].value_counts().index)
plt.title('Orders by Product Category')
plt.xlabel('Count')
plt.show()
```
"""
        )

        st.markdown("#### 🚀 Plotly: Interactive Visualizations")
        st.markdown(
            """**Plotly = Interactive Charts (Hover, Zoom, Pan)**

```python
import plotly.express as px
import plotly.graph_objects as go

# Sample data
df = pd.read_csv('sales_data.csv')
```

---

**Interactive Line Chart:**

```python
fig = px.line(df, x='date', y='revenue', title='Revenue Over Time')
fig.update_traces(line_color='#2E86AB', line_width=3)
fig.update_layout(hovermode='x unified')
fig.show()
```

**Benefits:** Hover to see exact values, zoom in on periods, export as PNG

---

**Interactive Bar Chart:**

```python
fig = px.bar(df.groupby('country')['revenue'].sum().reset_index(),
             x='country', y='revenue', 
             title='Revenue by Country',
             color='revenue',
             color_continuous_scale='Blues')
fig.show()
```

---

**Scatter with Size and Color:**

```python
fig = px.scatter(df, x='ad_spend', y='revenue', 
                 size='order_count',  # Bubble size
                 color='country',     # Color by category
                 hover_data=['customer_id'],
                 title='Ad Spend vs Revenue (sized by orders)')
fig.show()
```

---

**Dashboard with Subplots:**

```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Revenue Trend', 'Orders by Category', 
                    'Revenue Distribution', 'Top 10 Customers')
)

# Add plots
fig.add_trace(go.Scatter(x=df['date'], y=df['revenue'], mode='lines'), row=1, col=1)
fig.add_trace(go.Bar(x=categories, y=counts), row=1, col=2)
fig.add_trace(go.Histogram(x=df['revenue']), row=2, col=1)
fig.add_trace(go.Bar(x=top_customers, y=top_revenue), row=2, col=2)

fig.update_layout(height=800, showlegend=False, title_text="Sales Dashboard")
fig.show()
```
"""
        )

        st.markdown("#### 🎨 Design Principles: Make Charts Clear")
        st.markdown(
            """**1. Clear Titles and Labels**

```python
# ❌ BAD
plt.plot(x, y)
plt.show()

# ✅ GOOD
plt.plot(x, y)
plt.title('Monthly Revenue Increased 23% Year-over-Year', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (£)', fontsize=12)
plt.show()
```

**Title should answer:** "What does this chart show?"

---

**2. Use Color Purposefully**

```python
# ❌ BAD: Rainbow colors (no meaning)
colors = ['red', 'blue', 'green', 'yellow', 'purple']

# ✅ GOOD: Color highlights key insight
colors = ['gray', 'gray', 'red', 'gray', 'gray']  # Highlight worst performer
```

**Rules:**
- **One color:** For simple charts
- **Sequential (light→dark):** For ranking (sales: low→high)
- **Diverging (red→white→blue):** For positive/negative (profit/loss)
- **Categorical (distinct colors):** For categories (countries)

---

**3. Remove Clutter**

```python
# ✅ GOOD: Minimal but clear
sns.set_style('whitegrid')  # Light grid
plt.grid(alpha=0.3)         # Subtle gridlines
plt.box(False)              # No box around chart
```

**Remove:**
- Heavy borders
- 3D effects (never use!)
- Unnecessary decorations
- Chart junk

---

**4. Choose Appropriate Scale**

```python
# ❌ BAD: Y-axis starts at 50 (exaggerates differences)
plt.ylim(50, 60)

# ✅ GOOD: Y-axis starts at 0 (shows true scale)
plt.ylim(0, 100)
```

**Exception:** When all values are in a narrow range (99.1%, 99.3%, 99.5%), starting at 0 hides differences.

---

**5. Limit Categories**

```python
# ❌ BAD: 30 countries in one bar chart (unreadable)

# ✅ GOOD: Top 10 + "Other"
top10 = df.nlargest(10, 'revenue')
other = df.nsmallest(len(df)-10, 'revenue')['revenue'].sum()
```

**Max categories:**
- Bar chart: 10-15
- Pie chart: 5 (seriously, just 5!)
- Line chart: 5-7 lines
"""
        )

        st.markdown("#### 📖 Data Storytelling Framework")
        st.markdown(
            """**Structure Your Presentation:**

**1. Context (Why should I care?)**
- What's the business problem?
- Why does it matter?
- What's at stake?

**Example:** "Customer churn increased 15% last quarter, costing £200K in lost revenue."

---

**2. Insight (What did you find?)**
- Show data/chart
- Highlight key finding
- Use annotations

**Example:** "Analysis shows 80% of churned customers had support tickets unresolved >7 days."

---

**3. Action (What should we do?)**
- Clear recommendation
- Expected impact
- Next steps

**Example:** "Implement 3-day SLA for support tickets. Expected impact: Reduce churn by 5% (£70K/quarter)."

---

**Complete Example:**

```python
import matplotlib.pyplot as plt

# Data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
churn_rate = [5.2, 5.5, 6.1, 7.2, 8.1, 8.5]

fig, ax = plt.subplots(figsize=(12, 6))

# Plot
ax.plot(months, churn_rate, marker='o', linewidth=3, markersize=10, color='#C73E1D')

# Annotate key point
ax.annotate('Churn spiked\nafter support team cut',
            xy=('Apr', 7.2), xytext=('Feb', 8.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=2),
            fontsize=12, fontweight='bold')

# Titles and labels
ax.set_title('Customer Churn Rate Increasing (Now 8.5%)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Month (2024)', fontsize=12)
ax.set_ylabel('Churn Rate (%)', fontsize=12)
ax.set_ylim(4, 10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

**Written Summary:**

**Context:** Customer churn increased from 5.2% to 8.5% over 6 months, costing £200K.

**Insight:** Analysis shows spike began in April, coinciding with support team reduction. 80% of churned customers had tickets unresolved >7 days.

**Action:** Restore support team capacity or implement automated responses for simple queries. Target: Reduce churn to 6% by Q4 (saves £140K).
"""
        )

        st.markdown("#### ⚠️ Common Visualization Mistakes")
        st.markdown(
            """**1. Using Pie Charts for >5 Categories**

**Problem:** Can't compare angles accurately

**Solution:** Use horizontal bar chart instead

---

**2. Dual Y-Axes with Different Scales**

**Problem:** Makes correlations look stronger than they are

**Solution:** Use two separate charts or normalize to same scale

---

**3. 3D Charts**

**Problem:** Harder to read, no added value

**Solution:** Use 2D always (yes, always!)

---

**4. Truncated Y-Axis to Exaggerate Change**

**Problem:** 10% → 11% looks like 100% increase if Y-axis is 10-11

**Solution:** Start Y-axis at 0 (usually)

---

**5. Too Many Colors**

**Problem:** Rainbow charts confuse rather than clarify

**Solution:** 1-3 colors max, use color to highlight key point

---

**6. No Context**

**Problem:** Chart alone doesn't tell story

**Solution:** Add title that answers "so what?", annotate key points

---

**7. Illegible Text**

**Problem:** Tiny labels, rotated text

**Solution:** Font size 10-12pt min, horizontal labels when possible
"""
        )

        st.markdown("#### 🚀 Practice & Next Steps")
        st.markdown(
            """**Master Data Visualization:**

**Practice Projects:**
1. **Recreate Famous Charts**
   - Hans Rosling's Gapminder animations
   - NY Times "Flatten the Curve" chart
   - Learn what makes them effective

2. **Your Own Dashboard**
   - Pick dataset (e.g., personal finance, GitHub activity)
   - Create 4-6 key charts
   - Tell story with data

3. **Storytelling Practice**
   - Take any chart
   - Write 3-sentence summary (Context, Insight, Action)
   - Present to friend/family

**Resources:**
- **Book:** Storytelling with Data (Cole Nussbaumer Knaflic)
- **Gallery:** Python Graph Gallery (python-graph-gallery.com)
- **Inspiration:** r/dataisbeautiful
- **Tools:** Matplotlib docs, Seaborn gallery, Plotly examples

---

**Job Interview Ready:**

You can now:
- ✅ Choose appropriate chart types
- ✅ Create charts with Matplotlib/Seaborn/Plotly
- ✅ Design clear, professional visualizations
- ✅ Apply data storytelling framework
- ✅ Avoid common mistakes
- ✅ Present insights to stakeholders

**Visualization = Your Competitive Advantage**

Many analysts can query data. Few can communicate insights effectively. Master this, and you'll stand out!

**Next:** Unit 7 (Capstone) brings it all together in a portfolio project!
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LABS: Unit 6 Data Visualization")
        st.markdown(
            """**Complete these 2 labs to master data visualization:**

---

## Lab 1: Essential Charts with Matplotlib & Seaborn (75 min)

**Setup: E-commerce Sales Data**

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample sales data
data = {
    'date': pd.date_range('2024-01-01', periods=90, freq='D'),
    'revenue': [1200 + i*10 + np.random.randint(-200, 300) for i in range(90)],
    'orders': [25 + np.random.randint(-5, 15) for _ in range(90)],
}
df = pd.DataFrame(data)
df['month'] = df['date'].dt.month_name()

# Product data
products = pd.DataFrame({
    'product': ['Laptop', 'Monitor', 'Keyboard', 'Mouse', 'Headset'],
    'revenue': [45000, 32000, 18000, 12000, 8000],
    'units': [50, 107, 225, 480, 160]
})

df.to_csv('daily_sales.csv', index=False)
products.to_csv('product_sales.csv', index=False)
print("✅ Created datasets")
```

**Part A: Line Charts (Time Series) - 20 min**

```python
df = pd.read_csv('daily_sales.csv', parse_dates=['date'])

# Basic line chart
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['revenue'], linewidth=2, color='#2E86AB')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Revenue (£)', fontsize=12)
plt.title('Daily Revenue Trend (Q1 2024)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Multiple lines
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['date'], df['revenue'], label='Revenue', linewidth=2, color='#2E86AB')
ax2 = ax.twinx()
ax2.plot(df['date'], df['orders'], label='Orders', linewidth=2, color='#E67E22', linestyle='--')

ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Revenue (£)', fontsize=12, color='#2E86AB')
ax2.set_ylabel('Orders', fontsize=12, color='#E67E22')
ax.set_title('Revenue & Orders Trend', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

**Part B: Bar Charts (Comparisons) - 20 min**

```python
products = pd.read_csv('product_sales.csv')

# Horizontal bar chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(products['product'], products['revenue'], color='#A23B72')

# Add value labels
for i, v in enumerate(products['revenue']):
    ax.text(v + 1000, i, f'£{v:,}', va='center', fontweight='bold')

ax.set_xlabel('Revenue (£)', fontsize=12)
ax.set_title('Revenue by Product', fontsize=14, fontweight='bold')
ax.invert_yaxis()
plt.tight_layout()
plt.show()

# Grouped bar chart
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(products))
width = 0.35

ax.bar([i - width/2 for i in x], products['revenue']/1000, width, label='Revenue (£K)', color='#3498db')
ax.bar([i + width/2 for i in x], products['units'], width, label='Units Sold', color='#e67e22')

ax.set_xlabel('Product', fontsize=12)
ax.set_ylabel('Value', fontsize=12)
ax.set_title('Revenue vs Units by Product', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(products['product'])
ax.legend()
plt.tight_layout()
plt.show()
```

**Part C: Seaborn Statistical Plots - 20 min**

```python
# Box plot
plt.figure(figsize=(10, 6))
monthly_data = df.groupby('month')['revenue'].apply(list).to_dict()
sns.boxplot(data=df, x='month', y='revenue', order=['January', 'February', 'March'])
plt.title('Revenue Distribution by Month', fontsize=14, fontweight='bold')
plt.ylabel('Revenue (£)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Scatter with regression
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='orders', y='revenue', scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Revenue vs Orders (with trend line)', fontsize=14, fontweight='bold')
plt.xlabel('Orders', fontsize=12)
plt.ylabel('Revenue (£)', fontsize=12)
plt.tight_layout()
plt.show()

# Heatmap (correlation)
corr_data = df[['revenue', 'orders']].corr()
plt.figure(figsize=(6, 5))
sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True)
plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

**Part D: Chart Cleanup & Best Practices - 15 min**

```python
# BEFORE: Cluttered chart
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['revenue'])
plt.show()

# AFTER: Professional chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['date'], df['revenue'], linewidth=2.5, color='#2E86AB', marker='o', markersize=3, alpha=0.8)

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Revenue (£)', fontsize=12, fontweight='bold')
ax.set_title('Q1 2024 Revenue Trend - Up 28% vs Q4 2023', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, linestyle='--')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x/1000:.0f}K'))

# Add annotation
max_revenue = df['revenue'].max()
max_date = df.loc[df['revenue'].idxmax(), 'date']
ax.annotate(f'Peak: £{max_revenue:,.0f}', 
            xy=(max_date, max_revenue), 
            xytext=(max_date, max_revenue + 300),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=11, fontweight='bold', color='red')

plt.tight_layout()
plt.show()
```

---

## Lab 2: Data Storytelling Dashboard (60 min)

**Objective:** Create executive dashboard with insights

**Part A: Build KPI Cards (20 min)**

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('daily_sales.csv', parse_dates=['date'])
products = pd.read_csv('product_sales.csv')

# Calculate KPIs
total_revenue = df['revenue'].sum()
total_orders = df['orders'].sum()
avg_order_value = total_revenue / total_orders
revenue_growth = ((df['revenue'].iloc[-7:].mean() - df['revenue'].iloc[:7].mean()) / df['revenue'].iloc[:7].mean()) * 100

# Create dashboard
fig = plt.figure(figsize=(16, 10))

# Title
fig.suptitle('Q1 2024 Sales Dashboard', fontsize=20, fontweight='bold', y=0.98)

# KPI Cards (top row)
kpi_metrics = [
    ('Total Revenue', f'£{total_revenue:,.0f}', 'green'),
    ('Total Orders', f'{total_orders:,}', 'blue'),
    ('Avg Order Value', f'£{avg_order_value:.2f}', 'orange'),
    ('Revenue Growth', f'+{revenue_growth:.1f}%', 'red')
]

for i, (label, value, color) in enumerate(kpi_metrics):
    ax = plt.subplot(4, 3, i+1)
    ax.text(0.5, 0.6, value, ha='center', va='center', fontsize=24, fontweight='bold', color=color)
    ax.text(0.5, 0.3, label, ha='center', va='center', fontsize=12, color='gray')
    ax.axis('off')
```

**Part B: Add Key Charts (25 min)**

```python
# Revenue trend (middle left)
ax1 = plt.subplot(4, 3, (5, 8))
ax1.plot(df['date'], df['revenue'], linewidth=2, color='#2E86AB')
ax1.fill_between(df['date'], df['revenue'], alpha=0.3, color='#2E86AB')
ax1.set_title('Revenue Trend', fontsize=12, fontweight='bold')
ax1.set_ylabel('Revenue (£)')
ax1.grid(True, alpha=0.3)

# Top products (middle right)
ax2 = plt.subplot(4, 3, (6, 9))
ax2.barh(products['product'], products['revenue'], color='#A23B72')
ax2.set_title('Top Products by Revenue', fontsize=12, fontweight='bold')
ax2.set_xlabel('Revenue (£)')
ax2.invert_yaxis()

# Orders distribution (bottom left)
ax3 = plt.subplot(4, 3, (11, 12))
ax3.hist(df['orders'], bins=15, edgecolor='black', color='#E67E22', alpha=0.7)
ax3.set_title('Daily Orders Distribution', fontsize=12, fontweight='bold')
ax3.set_xlabel('Orders per Day')
ax3.set_ylabel('Frequency')

plt.tight_layout()
plt.show()
```

**Part C: Add Insights & Annotations (15 min)**

```python
# Create storytelling chart
fig, ax = plt.subplots(figsize=(14, 7))

# Plot revenue
ax.plot(df['date'], df['revenue'], linewidth=3, color='#2E86AB', label='Daily Revenue')

# Add 7-day moving average
df['ma7'] = df['revenue'].rolling(7).mean()
ax.plot(df['date'], df['ma7'], linewidth=2, color='red', linestyle='--', label='7-Day Avg', alpha=0.8)

# Highlight key events
event_date = pd.to_datetime('2024-02-14')
event_revenue = df.loc[df['date'] == event_date, 'revenue'].values[0]
ax.scatter([event_date], [event_revenue], s=200, color='gold', zorder=5, edgecolor='black', linewidth=2)
ax.annotate("Valentine's Day\nPromo Success", 
            xy=(event_date, event_revenue),
            xytext=(event_date - pd.Timedelta(days=10), event_revenue + 500),
            arrowprops=dict(arrowstyle='->', lw=2, color='black'),
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Revenue (£)', fontsize=12, fontweight='bold')
ax.set_title('Q1 Revenue Story: 28% Growth Driven by Strategic Promotions', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)

# Add insight box
insight_text = "KEY INSIGHTS:\n• Revenue up 28% vs Q4 2023\n• Valentine's promo drove £3.2K peak\n• Laptop = 39% of total revenue\n• Recommend: More seasonal campaigns"
ax.text(0.98, 0.95, insight_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.show()
```

**Executive Summary Template:**

```
EXECUTIVE SUMMARY - Q1 2024 SALES PERFORMANCE

OVERVIEW:
Q1 2024 revenue reached £XXX,XXX, representing 28% growth vs Q4 2023.
Strong performance driven by seasonal promotions and product mix optimization.

KEY FINDINGS:
1. Revenue Growth: +28% quarter-over-quarter
2. Order Volume: X,XXX orders (avg £XXX per order)
3. Top Product: Laptops contributed 39% of revenue
4. Peak Performance: Valentine's Day promo achieved £3.2K single-day revenue

RECOMMENDATIONS:
1. Increase seasonal campaign frequency (3-4 per quarter)
2. Expand laptop inventory to meet demand
3. Test similar promotions for Mother's Day and Easter
4. Focus marketing budget on top-performing products

NEXT STEPS:
• Launch Mother's Day campaign (targeting £4K peak day)
• Analyze customer segments for personalized offers
• Set Q2 target: £XXX,XXX (+15% vs Q1)
```

---

## Lab 3: Complete Data Visualization Portfolio Project (120 min)

**Objective:** Create professional multi-page visualization report for portfolio

**Scenario:** Quarterly Business Review for E-Commerce Company

**Part A: Data Preparation & Setup (25 min)**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set professional style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['figure.titlesize'] = 16

# Generate realistic quarterly data
np.random.seed(42)
dates = pd.date_range('2024-01-01', '2024-03-31', freq='D')
n_days = len(dates)

# Daily metrics
df = pd.DataFrame({
    'date': dates,
    'revenue': np.random.normal(15000, 3000, n_days) + np.linspace(0, 5000, n_days),  # Upward trend
    'orders': np.random.poisson(250, n_days) + np.linspace(0, 50, n_days).astype(int),
    'visitors': np.random.poisson(5000, n_days),
    'conversion_rate': np.random.uniform(0.04, 0.06, n_days)
})

# Add derived metrics
df['avg_order_value'] = df['revenue'] / df['orders']
df['month'] = df['date'].dt.month_name()
df['week'] = df['date'].dt.isocalendar().week
df['day_of_week'] = df['date'].dt.day_name()

# Product category data
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
category_sales = {
    'category': categories,
    'q1_revenue': [125000, 98000, 87000, 65000, 45000],
    'q4_revenue': [110000, 92000, 95000, 58000, 48000],
    'units_sold': [1250, 2100, 1450, 980, 1820]
}
df_categories = pd.DataFrame(category_sales)

# Customer segments
segments = ['Champions', 'Loyal', 'Potential', 'At Risk', 'Lost']
segment_data = {
    'segment': segments,
    'customers': [1500, 3500, 5000, 2800, 1200],
    'avg_ltv': [850, 420, 180, 120, 45]
}
df_segments = pd.DataFrame(segment_data)

print("="*60)
print("DATA PREPARATION COMPLETE")
print("="*60)
print(f"Daily data: {len(df)} rows (Jan-Mar 2024)")
print(f"Product categories: {len(categories)}")
print(f"Customer segments: {len(segments)}")
print("\\n✅ Ready for visualization")
```

---

**Part B: Executive Summary Dashboard (45 min)**

```python
# Create comprehensive 6-panel dashboard
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
fig.suptitle('Q1 2024 Business Performance Review', fontsize=20, fontweight='bold', y=0.98)

# Panel 1: Total Revenue (Big Number KPI)
ax1 = fig.add_subplot(gs[0, 0])
total_revenue = df['revenue'].sum()
revenue_growth = ((df[df['month']=='March']['revenue'].sum() - df[df['month']=='January']['revenue'].sum()) / 
                   df[df['month']=='January']['revenue'].sum() * 100)
ax1.text(0.5, 0.6, f'£{total_revenue:,.0f}', ha='center', va='center', 
         fontsize=42, fontweight='bold', color='#2ecc71')
ax1.text(0.5, 0.3, 'Total Revenue', ha='center', va='center', fontsize=14, color='gray')
ax1.text(0.5, 0.1, f'+{revenue_growth:.1f}% vs Jan', ha='center', va='center', 
         fontsize=12, color='green', fontweight='bold')
ax1.axis('off')
ax1.set_facecolor('#f8f9fa')

# Panel 2: Total Orders
ax2 = fig.add_subplot(gs[0, 1])
total_orders = df['orders'].sum()
ax2.text(0.5, 0.6, f'{total_orders:,}', ha='center', va='center', 
         fontsize=42, fontweight='bold', color='#3498db')
ax2.text(0.5, 0.3, 'Total Orders', ha='center', va='center', fontsize=14, color='gray')
ax2.text(0.5, 0.1, f'{total_orders/90:.0f} orders/day avg', ha='center', va='center', 
         fontsize=11, color='#3498db')
ax2.axis('off')
ax2.set_facecolor('#f8f9fa')

# Panel 3: Avg Conversion Rate
ax3 = fig.add_subplot(gs[0, 2])
avg_conversion = df['conversion_rate'].mean()
ax3.text(0.5, 0.6, f'{avg_conversion:.1%}', ha='center', va='center', 
         fontsize=42, fontweight='bold', color='#e67e22')
ax3.text(0.5, 0.3, 'Conversion Rate', ha='center', va='center', fontsize=14, color='gray')
ax3.text(0.5, 0.1, 'Industry avg: 4.2%', ha='center', va='center', 
         fontsize=11, color='gray', style='italic')
ax3.axis('off')
ax3.set_facecolor('#f8f9fa')

# Panel 4: Revenue Trend (spans 2 columns)
ax4 = fig.add_subplot(gs[1, :2])
df_weekly = df.groupby('week')['revenue'].sum().reset_index()
ax4.plot(df_weekly['week'], df_weekly['revenue'], marker='o', linewidth=3, 
         markersize=8, color='#3498db', label='Weekly Revenue')
ax4.fill_between(df_weekly['week'], df_weekly['revenue'], alpha=0.3, color='#3498db')
ax4.set_title('Weekly Revenue Trend', fontsize=14, fontweight='bold', loc='left')
ax4.set_xlabel('Week Number')
ax4.set_ylabel('Revenue (£)')
ax4.grid(True, alpha=0.3)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
# Annotate peak week
peak_week = df_weekly.loc[df_weekly['revenue'].idxmax()]
ax4.annotate(f'Peak: £{peak_week[\"revenue\"]:,.0f}', 
             xy=(peak_week['week'], peak_week['revenue']),
             xytext=(peak_week['week']+1, peak_week['revenue']+10000),
             arrowprops=dict(arrowstyle='->', color='red', lw=2),
             fontsize=11, color='red', fontweight='bold')

# Panel 5: Category Performance
ax5 = fig.add_subplot(gs[1, 2])
df_categories['growth'] = ((df_categories['q1_revenue'] - df_categories['q4_revenue']) / 
                            df_categories['q4_revenue'] * 100)
colors_cat = ['green' if x > 0 else 'red' for x in df_categories['growth']]
ax5.barh(df_categories['category'], df_categories['growth'], color=colors_cat, alpha=0.7)
ax5.axvline(0, color='black', linewidth=0.8)
ax5.set_title('Category Growth (Q1 vs Q4)', fontsize=14, fontweight='bold')
ax5.set_xlabel('Growth (%)')
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)

# Panel 6: Customer Segments (spans all 3 columns)
ax6 = fig.add_subplot(gs[2, :])
x = np.arange(len(segments))
width = 0.35
bars1 = ax6.bar(x - width/2, df_segments['customers'], width, label='Customers', color='#3498db', alpha=0.8)
ax7 = ax6.twinx()
bars2 = ax7.bar(x + width/2, df_segments['avg_ltv'], width, label='Avg LTV (£)', color='#e67e22', alpha=0.8)

ax6.set_xlabel('Customer Segment')
ax6.set_ylabel('Number of Customers', color='#3498db')
ax6.set_xticks(x)
ax6.set_xticklabels(segments)
ax6.tick_params(axis='y', labelcolor='#3498db')
ax7.set_ylabel('Avg Lifetime Value (£)', color='#e67e22')
ax7.tick_params(axis='y', labelcolor='#e67e22')
ax6.set_title('Customer Segmentation Analysis', fontsize=14, fontweight='bold', loc='left')
ax6.legend(loc='upper left')
ax7.legend(loc='upper right')

# Save high-resolution
plt.savefig('q1_business_review.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\\n✅ Executive dashboard created: q1_business_review.png")
```

---

**Part C: Deep-Dive Analysis & Storytelling (50 min)**

```python
# Create detailed analysis report with 4 focused charts

fig2, axes = plt.subplots(2, 2, figsize=(16, 12))
fig2.suptitle('Q1 2024 - Detailed Performance Analysis', fontsize=18, fontweight='bold')

# Chart 1: Revenue by Day of Week
ax = axes[0, 0]
day_revenue = df.groupby('day_of_week')['revenue'].mean().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])
colors_day = ['#3498db' if x < day_revenue.mean() else '#2ecc71' for x in day_revenue]
ax.bar(range(7), day_revenue.values, color=colors_day, alpha=0.8, edgecolor='black')
ax.axhline(day_revenue.mean(), color='red', linestyle='--', linewidth=2, label='Average')
ax.set_xticks(range(7))
ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
ax.set_ylabel('Avg Daily Revenue (£)')
ax.set_title('Revenue Patterns by Weekday', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Add insight annotation
best_day = day_revenue.idxmax()
ax.text(0.5, 0.95, f'🔍 Insight: {best_day} is peak day (+{((day_revenue.max()-day_revenue.mean())/day_revenue.mean()*100):.0f}% vs avg)',
        transform=ax.transAxes, ha='center', va='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
        fontsize=10)

# Chart 2: Order Value Distribution
ax = axes[0, 1]
ax.hist(df['avg_order_value'], bins=30, edgecolor='black', alpha=0.7, color='#9b59b6')
median_aov = df['avg_order_value'].median()
mean_aov = df['avg_order_value'].mean()
ax.axvline(median_aov, color='green', linestyle='--', linewidth=2, label=f'Median: £{median_aov:.0f}')
ax.axvline(mean_aov, color='red', linestyle='--', linewidth=2, label=f'Mean: £{mean_aov:.0f}')
ax.set_xlabel('Average Order Value (£)')
ax.set_ylabel('Frequency')
ax.set_title('Order Value Distribution', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Chart 3: Conversion Rate Over Time
ax = axes[1, 0]
df_monthly = df.groupby('month')['conversion_rate'].mean().reindex(['January', 'February', 'March'])
ax.plot(df_monthly.index, df_monthly.values, marker='o', linewidth=3, markersize=12, color='#e67e22')
ax.fill_between(range(3), df_monthly.values, alpha=0.3, color='#e67e22')
ax.set_ylabel('Conversion Rate (%)')
ax.set_title('Conversion Rate Trend', fontweight='bold')
ax.grid(True, alpha=0.3)

# Add trend arrow
if df_monthly.values[2] > df_monthly.values[0]:
    ax.text(2, df_monthly.values[2] + 0.001, '📈 Improving', ha='center', fontsize=12, color='green', fontweight='bold')
else:
    ax.text(2, df_monthly.values[2] - 0.001, '📉 Declining', ha='center', fontsize=12, color='red', fontweight='bold')

# Chart 4: Revenue vs Orders Correlation
ax = axes[1, 1]
scatter = ax.scatter(df['orders'], df['revenue'], c=df.index, cmap='viridis', alpha=0.5, s=50)
# Add trendline
z = np.polyfit(df['orders'], df['revenue'], 1)
p = np.poly1d(z)
ax.plot(df['orders'], p(df['orders']), "r--", alpha=0.8, linewidth=2, label='Trend')
ax.set_xlabel('Daily Orders')
ax.set_ylabel('Daily Revenue (£)')
ax.set_title('Orders vs Revenue Correlation', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Calculate correlation
corr = df['orders'].corr(df['revenue'])
ax.text(0.05, 0.95, f'Correlation: r = {corr:.3f}', 
        transform=ax.transAxes, fontsize=11,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('q1_detailed_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\\n✅ Detailed analysis created: q1_detailed_analysis.png")

# Generate executive summary
print("\\n" + "="*70)
print("EXECUTIVE SUMMARY - Q1 2024")
print("="*70)
print(f"📊 Total Revenue: £{total_revenue:,.0f} (+{revenue_growth:.1f}% growth)")
print(f"📦 Total Orders: {total_orders:,} ({total_orders/90:.0f}/day avg)")
print(f"💰 Avg Order Value: £{df['avg_order_value'].mean():.2f}")
print(f"📈 Conversion Rate: {df['conversion_rate'].mean():.2%}")
print(f"\\n🎯 Key Insights:")
print(f"1. {best_day}s perform {((day_revenue.max()-day_revenue.mean())/day_revenue.mean()*100):.0f}% above average")
print(f"2. Conversion rate {('improved' if df_monthly.values[2] > df_monthly.values[0] else 'declined')} by {abs((df_monthly.values[2]-df_monthly.values[0])/df_monthly.values[0]*100):.1f}%")
print(f"3. Strong correlation (r={corr:.2f}) between orders and revenue")
print(f"\\n💡 Recommendations:")
print(f"1. Increase marketing spend on {best_day}s")
print(f"2. Optimize checkout flow to boost conversion")
print(f"3. Focus on Electronics category (strongest growth)")
print("="*70)
```

---

**Lab 3 Completion Checklist:**
- ☐ Generated realistic business data
- ☐ Created 6-panel executive dashboard
- ☐ Applied professional color schemes
- ☐ Added KPI cards with big numbers
- ☐ Created weekly trend analysis
- ☐ Built category comparison charts
- ☐ Analyzed customer segments
- ☐ Created 4 deep-dive analysis charts
- ☐ Used annotations and insights
- ☐ Saved high-resolution images (300 DPI)
- ☐ Generated executive summary
- ☐ Portfolio-ready visualizations created

**🎉 Portfolio Piece Complete!**

Add these charts to your GitHub, LinkedIn, and portfolio website. This demonstrates:
- Professional visualization skills
- Business analysis capabilities  
- Data storytelling ability
- Attention to detail

**Next:** Unit 7 Capstone brings everything together!
"""
        )

        st.markdown("---")
        st.markdown("#### 🎨 Advanced Chart Types & When to Use Them")
        st.markdown(
            """**Chart Selection Matrix**

| Goal | Chart Type | Best For |
|------|------------|----------|
| **Compare** | Bar chart | Categories (sales by region) |
| **Trend** | Line chart | Time series (revenue over months) |
| **Distribution** | Histogram, Box plot | Understanding spread (customer ages) |
| **Relationship** | Scatter plot | Correlation (ad spend vs revenue) |
| **Composition** | Pie chart, Stacked bar | Part-to-whole (market share) |
| **Ranking** | Horizontal bar | Top/bottom items (best products) |

---

**Example: Choosing the Right Chart**

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Generate sample e-commerce data
np.random.seed(42)
months = pd.date_range('2024-01-01', periods=12, freq='M')
revenue = np.random.randint(40000, 80000, 12)
orders = np.random.randint(800, 1200, 12)

df = pd.DataFrame({
    'month': months,
    'revenue': revenue,
    'orders': orders
})

# Calculate avg order value
df['avg_order'] = df['revenue'] / df['orders']

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Trend over time → LINE CHART
axes[0, 0].plot(df['month'], df['revenue'], marker='o', linewidth=2, markersize=8)
axes[0, 0].set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Revenue (£)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Distribution → HISTOGRAM
axes[0, 1].hist(df['revenue'], bins=8, edgecolor='black', alpha=0.7, color='#3498db')
axes[0, 1].axvline(df['revenue'].mean(), color='r', linestyle='--', linewidth=2, label='Mean')
axes[0, 1].set_title('Revenue Distribution', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Revenue (£)')
axes[0, 1].legend()

# 3. Relationship → SCATTER PLOT
axes[1, 0].scatter(df['orders'], df['revenue'], s=100, alpha=0.6, c=range(12), cmap='viridis')
axes[1, 0].set_title('Orders vs Revenue', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Number of Orders')
axes[1, 0].set_ylabel('Revenue (£)')

# Add trendline
z = np.polyfit(df['orders'], df['revenue'], 1)
p = np.poly1d(z)
axes[1, 0].plot(df['orders'], p(df['orders']), "r--", alpha=0.8, linewidth=2)

# 4. Comparison → BAR CHART
top_3_months = df.nlargest(3, 'revenue')
axes[1, 1].barh(top_3_months['month'].dt.strftime('%B'), top_3_months['revenue'], color='#e67e22')
axes[1, 1].set_title('Top 3 Revenue Months', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Revenue (£)')

plt.tight_layout()
plt.show()
```
"""
        )

        st.markdown("---")
        st.markdown("#### 🌈 Color Theory for Data Visualization")
        st.markdown(
            """**Colors Matter - A LOT!**

**1. Sequential (Low → High)**

Use for: Sales, revenue, quantities

```python
# Good: Single hue gradient
colors_sequential = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5']

# Bad: Rainbow (hard to read magnitude)
# colors_bad = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
```

---

**2. Diverging (Negative ← Zero → Positive)**

Use for: Profit/loss, changes, deviations

```python
# Good: Red-White-Blue
import seaborn as sns
colors_diverging = sns.diverging_palette(10, 220, as_cmap=True)

# Example: Revenue change by region
import pandas as pd
import matplotlib.pyplot as plt

regions = ['North', 'South', 'East', 'West', 'Central']
changes = [15, -8, 22, -3, 10]  # % change

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['green' if x > 0 else 'red' for x in changes]
ax.barh(regions, changes, color=colors, alpha=0.7)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Revenue Change (%)')
ax.set_title('Regional Performance: Q1 vs Q4', fontsize=14)
plt.show()
```

---

**3. Categorical (Distinct Items)**

Use for: Product categories, customer segments

```python
# Good: Colorblind-friendly palette
colors_categorical = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Seaborn's built-in palettes
import seaborn as sns

# Option 1: Deep
sns.set_palette("deep")

# Option 2: Colorblind-safe
sns.set_palette("colorblind")

# Option 3: Custom
custom_palette = ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600']
sns.set_palette(custom_palette)
```

---

**4. Accessibility - Colorblind-Friendly**

~8% of men are colorblind! Test your charts.

```python
# BAD: Red vs Green (colorblind can't distinguish)
# colors_bad = ['red', 'green']

# GOOD: Blue vs Orange (safe for most types)
colors_safe = ['#0173b2', '#de8f05']

# Or use patterns in addition to colors
import matplotlib.pyplot as plt
import numpy as np

categories = ['Category A', 'Category B']
values = [45, 55]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(categories, values, color=colors_safe)

# Add hatching for extra distinction
bars[0].set_hatch('//')
bars[1].set_hatch('\\\\\\\\')

ax.set_ylabel('Value')
ax.set_title('Colorblind-Friendly Chart')
plt.show()
```
"""
        )

        st.markdown("---")
        st.markdown("#### 📊 Professional Dashboard Design")
        st.markdown(
            """**Executive Dashboard Best Practices**

**Layout Principles:**
1. **F-Pattern:** Eye moves left-to-right, top-to-bottom
2. **Key metrics top-left:** Most important KPIs first
3. **White space:** Don't cram everything
4. **Consistent sizing:** Equal-sized panels look professional

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Create professional dashboard
fig = plt.figure(figsize=(16, 10))
fig.suptitle('Q1 2024 Executive Dashboard', fontsize=20, fontweight='bold', y=0.98)

# Define grid
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. TOP LEFT: Key KPI (Big Number)
ax1 = fig.add_subplot(gs[0, 0])
ax1.text(0.5, 0.5, '£426K', ha='center', va='center', fontsize=48, fontweight='bold', color='#2ecc71')
ax1.text(0.5, 0.2, 'Total Revenue', ha='center', va='center', fontsize=14, color='gray')
ax1.text(0.5, 0.05, '+28% vs Q4 2023', ha='center', va='center', fontsize=12, color='green')
ax1.axis('off')
ax1.set_facecolor('#f8f9fa')

# 2. TOP MIDDLE: Another KPI
ax2 = fig.add_subplot(gs[0, 1])
ax2.text(0.5, 0.5, '8,542', ha='center', va='center', fontsize=48, fontweight='bold', color='#3498db')
ax2.text(0.5, 0.2, 'Total Orders', ha='center', va='center', fontsize=14, color='gray')
ax2.text(0.5, 0.05, '+15% vs Q4 2023', ha='center', va='center', fontsize=12, color='green')
ax2.axis('off')
ax2.set_facecolor('#f8f9fa')

# 3. TOP RIGHT: KPI
ax3 = fig.add_subplot(gs[0, 2])
ax3.text(0.5, 0.5, '£49.90', ha='center', va='center', fontsize=48, fontweight='bold', color='#e67e22')
ax3.text(0.5, 0.2, 'Avg Order Value', ha='center', va='center', fontsize=14, color='gray')
ax3.text(0.5, 0.05, '+11% vs Q4 2023', ha='center', va='center', fontsize=12, color='green')
ax3.axis('off')
ax3.set_facecolor('#f8f9fa')

# 4. MIDDLE: Revenue Trend (spans 2 columns)
ax4 = fig.add_subplot(gs[1, :2])
months = ['Jan', 'Feb', 'Mar']
revenue = [135000, 142000, 149000]
ax4.plot(months, revenue, marker='o', linewidth=3, markersize=10, color='#3498db')
ax4.fill_between(range(len(months)), revenue, alpha=0.3, color='#3498db')
ax4.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold', loc='left')
ax4.set_ylabel('Revenue (£)')
ax4.grid(True, alpha=0.3)
ax4.spines['top'].set_visible(False)
ax4.spines('right'].set_visible(False)

# 5. TOP RIGHT: Product Mix
ax5 = fig.add_subplot(gs[1, 2])
products = ['Laptops', 'Phones', 'Tablets', 'Accessories']
sales = [39, 28, 18, 15]
colors = ['#3498db', '#e67e22', '#2ecc71', '#9b59b6']
ax5.pie(sales, labels=products, autopct='%1.0f%%', colors=colors, startangle=90)
ax5.set_title('Revenue by Product', fontsize=14, fontweight='bold')

# 6. BOTTOM: Top Customers (spans all columns)
ax6 = fig.add_subplot(gs[2, :])
customers = ['ACME Corp', 'Tech Solutions', 'Global Ltd', 'Innovation Inc', 'Data Systems']
customer_revenue = [45000, 38000, 32000, 28000, 25000]
bars = ax6.barh(customers, customer_revenue, color='#3498db', alpha=0.7)
ax6.set_title('Top 5 Customers by Revenue', fontsize=14, fontweight='bold', loc='left')
ax6.set_xlabel('Revenue (£)')
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)

# Add value labels
for i, (customer, value) in enumerate(zip(customers, customer_revenue)):
    ax6.text(value + 1000, i, f'£{value:,}', va='center', fontsize=10)

plt.savefig('executive_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("✅ Professional dashboard created!")
```
"""
        )

        st.markdown("---")
        st.markdown("#### 📖 Data Storytelling Framework")
        st.markdown(
            """**Tell Stories with Data, Not Just Facts**

**Structure:** Setup → Conflict → Resolution

---

**Example: E-Commerce Sales Analysis**

**❌ BAD:** "Q1 revenue was £426K, a 28% increase. Orders were 8,542."

**✅ GOOD:**

```markdown
### The Challenge (Setup)
In Q4 2023, our e-commerce platform struggled with stagnant growth, 
averaging £55K weekly revenue despite increased ad spend.

### What We Did (Conflict)
We implemented three key changes in Q1 2024:
1. Optimized product mix (focused on high-margin laptops)
2. Launched targeted seasonal campaigns
3. Improved checkout experience

### The Results (Resolution)
Q1 2024 exceeded expectations:
- Revenue: £426K (+28% vs Q4)
- Orders: 8,542 (+15%)
- Avg Order Value: £49.90 (+11%)

Key Insight: Valentine's Day promotion alone drove £32K (7.5% of quarterly revenue)

### What This Means
These results validate our new strategy. We recommend:
1. Double down on seasonal campaigns (3-4 per quarter)
2. Expand laptop inventory to meet 40% demand increase
3. Target: £480K in Q2 (+13% vs Q1)
```

---

**Visualization Storytelling:**

```python
import matplotlib.pyplot as plt
import numpy as np

# Create narrative-driven chart
fig, ax = plt.subplots(figsize=(12, 6))

# Weekly revenue data
weeks = np.arange(1, 14)
q4_revenue = np.random.normal(55000, 5000, 13)  # Q4: Flat
q1_revenue = 55000 + (weeks * 2500) + np.random.normal(0, 3000, 13)  # Q1: Growing

# Plot Q4 (flat)
ax.plot(weeks, q4_revenue, 'o--', color='gray', alpha=0.6, label='Q4 2023', linewidth=2)

# Plot Q1 (growth)
ax.plot(weeks, q1_revenue, 'o-', color='#2ecc71', label='Q1 2024', linewidth=3, markersize=8)

# Annotate key events
ax.annotate('Valentine\'s Campaign\n£32K week!', 
            xy=(6, q1_revenue[5]), xytext=(8, 85000),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=12, fontweight='bold', color='red')

ax.annotate('Laptop Promo\nLaunched', 
            xy=(3, q1_revenue[2]), xytext=(1, 75000),
            arrowprops=dict(arrowstyle='->', color='#3498db', lw=2),
            fontsize=10, color='#3498db')

# Styling
ax.set_xlabel('Week', fontsize=12)
ax.set_ylabel('Weekly Revenue (£)', fontsize=12)
ax.set_title('Q1 2024: Strategic Initiatives Drive 28% Revenue Growth', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add insight box
textstr = 'Key Success Factors:\n✓ Seasonal campaigns\n✓ Product optimization\n✓ Improved UX'
props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.show()
```
"""
        )

        st.markdown("---")
        st.markdown("#### 🎯 Interview Questions: Data Visualization")
        st.markdown(
            """**Common Questions + Model Answers**

**Q1: When should you use a bar chart vs a line chart?**

**Answer:**
- **Bar chart:** Comparing categories (sales by region, products)
- **Line chart:** Showing trends over time (revenue by month, stock prices)

"Use bars for discrete comparisons, lines for continuous trends. Never use a pie chart if you have more than 5 categories!"

---

**Q2: How do you choose colors for dashboards?**

**Answer:**
"I follow three principles:
1. **Sequential** for magnitude (light to dark blue for sales)
2. **Diverging** for pos/neg (red-white-green for profit/loss)
3. **Categorical** for distinct items (different hues for products)

Always test for colorblind accessibility - avoid red/green combos."

---

**Q3: What makes a good data visualization?**

**Answer:**
A good viz should:
1. **Answer a question** (not just show data)
2. **Be readable** (clear labels, legends, titles)
3. **Tell a story** (annotate key insights)
4. **Guide the eye** (highlight important parts)
5. **Be honest** (don't mislead with scale tricks)

Bad example: 3D pie charts with no labels ❌
Good example: Annotated line chart with insights ✅

---

**Q4: Your stakeholder says "Just make it prettier." What do you do?**

**Answer:**
"I'd ask what specific message they want to communicate. Pretty doesn't mean effective. I'd:
1. Clarify the key insight
2. Choose appropriate chart type
3. Add annotations explaining 'so what?'
4. Use professional styling (consistent colors, clean fonts)
5. Show before/after and explain improvements

Aesthetics serve clarity, not distract from it."

---

**Q5: How do you visualize data for executives vs analysts?**

**Answer:**
- **Executives:** High-level KPIs, trends, 1-2 key charts. Focus on business impact.
- **Analysts:** Detailed distributions, correlations, full data views. Enable exploration.

"Example: For CEO, show 'Revenue up 15%' with trend. For analyst, show full breakdown by product, region, time with filters."
"""
        )

        st.markdown("---")
        st.markdown("#### 🏆 Visualization Best Practices Checklist")
        st.markdown(
            """**Before Sharing Any Chart:**

**Content:**
- ☐ Title clearly states the insight (not just "Sales Chart")
- ☐ Axes are labeled with units (£, %, count)
- ☐ Legend is present if multiple series
- ☐ Source/date is noted
- ☐ Key insights are annotated

**Design:**
- ☐ Font size is readable (12pt+ for body, 16pt+ for titles)
- ☐ Colors are colorblind-friendly
- ☐ Gridlines are subtle (not distracting)
- ☐ White space is used effectively
- ☐ Chart isn't cluttered (remove chart junk)

**Accuracy:**
- ☐ Y-axis starts at zero (for bar charts)
- ☐ Scale is appropriate (not misleading)
- ☐ Numbers are formatted correctly (£, commas)
- ☐ Percentages add to 100% (if applicable)
- ☐ Data is recent and relevant

**Storytelling:**
- ☐ Answers a specific question
- ☐ Highlights the main point
- ☐ Provides context (vs last period, vs target)
- ☐ Suggests action or next steps
- ☐ Is appropriate for audience

**Technical:**
- ☐ Exported at high resolution (300 DPI minimum)
- ☐ File format is appropriate (PNG for web, PDF for print)
- ☐ Chart is reproducible (code saved)
- ☐ Data source is documented

---

**Golden Rules:**
1. **Less is more** - Remove everything that doesn't add value
2. **Consistency** - Use same colors/fonts across dashboards
3. **Accessibility** - 8% of men are colorblind
4. **Context** - Always compare to something (baseline, target, last period)
5. **Action** - Visualizations should drive decisions

**Remember:** If your chart needs a 10-minute explanation, redesign it!
"""
        )

    elif unit_number == 7:
        st.markdown("---")
        st.markdown("#### 🎯 Why Your Capstone Project Matters")
        st.markdown(
            """**Your Capstone = Your Interview Ticket**

**What Recruiters Look For:**
1. **Can you solve real problems?** (Not just tutorials)
2. **Can you communicate findings?** (Not just code)
3. **Do you understand business?** (Not just technical)

**Reality:**
- 80% of candidates have certificates
- 20% have portfolio projects
- **5% have GOOD portfolio projects**

**Your Goal:** Be in that top 5%

---

**What Makes a Strong Capstone:**

| Weak Project | Strong Project |
|--------------|----------------|
| Titanic dataset (overdone) | Industry-relevant dataset |
| No business context | Clear problem statement |
| Just code | Code + insights + recommendations |
| No visualization | Clear charts with narratives |
| No documentation | README, comments, structure |

**Your capstone is your proof that you're job-ready.**
"""
        )

        st.markdown("#### 💡 10 Capstone Project Ideas")
        st.markdown(
            """**Choose Based on Your Target Industry:**

---

**1. E-Commerce Customer Segmentation (RFM Analysis)**

**Problem:** "How should we segment customers for targeted marketing?"

**Dataset:** Transaction data (customer_id, date, amount)

**Analysis:**
- Calculate Recency, Frequency, Monetary metrics
- Segment customers (Champions, Loyal, At Risk, etc.)
- Recommend retention strategies for each segment

**Skills:** Pandas, groupby, visualization, business recommendations

**Output:** Customer segments with actionable marketing strategies

---

**2. Healthcare Patient Readmission Prediction**

**Problem:** "Which patients are likely to be readmitted within 30 days?"

**Dataset:** Patient records (age, diagnosis, previous admissions, medications)

**Analysis:**
- Exploratory analysis of readmission patterns
- Feature engineering (admission frequency, time since last visit)
- Simple classification model (logistic regression)
- Identify high-risk patient characteristics

**Skills:** Classification, feature engineering, medical domain knowledge

**Output:** Risk factors and recommendations to reduce readmissions

---

**3. Retail Sales Forecasting**

**Problem:** "What will next quarter's sales be by product category?"

**Dataset:** Historical sales data (date, product, category, sales, promotions)

**Analysis:**
- Time series visualization
- Identify trends and seasonality
- Build forecasting model (moving average or simple regression)
- Adjust for promotions and holidays

**Skills:** Time series, forecasting, business planning

**Output:** Q4 sales forecast with confidence intervals

---

**4. Financial Fraud Detection**

**Problem:** "Can we identify potentially fraudulent transactions?"

**Dataset:** Credit card transactions (amount, merchant, location, time, fraud label)

**Analysis:**
- Analyze fraud patterns (time, amount, location)
- Feature engineering (transaction velocity, amount vs average)
- Build fraud detection model (decision tree, random forest)
- Calculate cost-benefit of implementing system

**Skills:** Classification, imbalanced data, financial domain

**Output:** Fraud detection model with business case

---

**5. Real Estate Price Prediction**

**Problem:** "What drives house prices in [your city]?"

**Dataset:** Property listings (location, bedrooms, square footage, price)

**Analysis:**
- Exploratory analysis of price drivers
- Correlation analysis (size, location, age)
- Build price prediction model (linear regression)
- Create pricing recommendations for sellers

**Skills:** Regression, feature importance, real estate domain

**Output:** Price prediction tool with key drivers identified

---

**6. HR Employee Attrition Analysis**

**Problem:** "Why are employees leaving and who's at risk?"

**Dataset:** Employee data (tenure, salary, department, performance, left Y/N)

**Analysis:**
- Analyze attrition patterns by department, tenure, salary
- Identify high-risk employee profiles
- Build attrition prediction model
- Recommend retention strategies

**Skills:** Classification, HR metrics, business recommendations

**Output:** Attrition risk model with retention playbook

---

**7. Social Media Sentiment Analysis**

**Problem:** "What do customers think about our brand vs competitors?"

**Dataset:** Tweets/reviews mentioning brand (text, date, likes)

**Analysis:**
- Collect data via API (Twitter, Reddit)
- Perform sentiment analysis (positive/negative/neutral)
- Identify common complaints and praise
- Compare sentiment over time and vs competitors

**Skills:** API usage, text analysis, NLP basics, visualization

**Output:** Brand sentiment report with action items

---

**8. Supply Chain Optimization**

**Problem:** "How can we reduce delivery times and costs?"

**Dataset:** Shipment data (origin, destination, date, delivery time, cost, carrier)

**Analysis:**
- Analyze delivery performance by carrier and route
- Identify bottlenecks and delays
- Calculate cost vs speed tradeoffs
- Recommend carrier mix and routing changes

**Skills:** Operations analytics, optimization, logistics domain

**Output:** Supply chain improvement recommendations with ROI

---

**9. Marketing Campaign Effectiveness (A/B Test)**

**Problem:** "Which email campaign drives more conversions?"

**Dataset:** Campaign data (user_id, campaign_version, sent, opened, clicked, purchased)

**Analysis:**
- Calculate conversion funnel metrics
- Perform A/B test analysis (statistical significance)
- Identify which elements drive conversions
- Recommend winning variant and future tests

**Skills:** A/B testing, statistics, marketing analytics

**Output:** Campaign performance report with recommendations

---

**10. Energy Consumption Forecasting**

**Problem:** "Can we predict and reduce building energy usage?"

**Dataset:** Smart meter data (timestamp, consumption, temperature, occupancy)

**Analysis:**
- Analyze consumption patterns (time of day, weather, occupancy)
- Build consumption forecast model
- Identify energy waste opportunities
- Calculate savings from efficiency measures

**Skills:** Time series, IoT data, sustainability domain

**Output:** Energy forecast and savings recommendations

---

**How to Choose:**
1. Pick industry you want to work in
2. Use publicly available dataset (Kaggle, government data, APIs)
3. Ensure dataset is large enough (1000+ rows)
4. Choose business-relevant question
"""
        )

        st.markdown("#### 🔄 CRISP-DM: Your Project Workflow")
        st.markdown(
            """**Industry-Standard Data Science Process**

**1. Business Understanding (Week 1)**

**Questions to Answer:**
- What's the business problem?
- Who are the stakeholders?
- What does success look like?
- What decisions will this analysis drive?

**Deliverable:** 1-page problem statement

**Example:**
```
Problem: Customer churn costs £200K/quarter
Stakeholder: VP Marketing
Success: Identify at-risk customers and reduce churn by 10%
Decision: Launch retention campaign for high-risk customers
```

---

**2. Data Understanding (Week 1)**

**Tasks:**
- Collect data (Kaggle, APIs, scraping, company data)
- Explore with `.head()`, `.info()`, `.describe()`
- Visualize distributions
- Check for missing values and outliers

**Deliverable:** Exploratory Data Analysis (EDA) notebook

**Key Questions:**
- How many rows/columns?
- What's the quality? (missing, errors)
- What patterns exist?
- Is there enough data?

---

**3. Data Preparation (Week 2)**

**Tasks:**
- Handle missing values (drop, fill, impute)
- Remove duplicates
- Fix data types
- Create new features (e.g., customer_tenure, days_since_last_order)
- Merge multiple datasets if needed

**Deliverable:** Clean dataset ready for analysis

**Code Template:**
```python
import pandas as pd

# Load raw data
df = pd.read_csv('raw_data.csv')
print(f"Raw: {df.shape}")

# Clean
df = df.dropna(subset=['customer_id'])  # Critical fields
df['revenue'].fillna(df['revenue'].median(), inplace=True)
df = df.drop_duplicates(subset=['customer_id'])
df['signup_date'] = pd.to_datetime(df['signup_date'])

# Feature engineering
df['tenure_days'] = (pd.Timestamp.now() - df['signup_date']).dt.days
df['is_high_value'] = df['revenue'] > df['revenue'].quantile(0.75)

# Save clean version
df.to_csv('clean_data.csv', index=False)
print(f"Clean: {df.shape}")
```

---

**4. Modeling (Week 2-3)**

**For Analysis Projects:** Create aggregations, segmentations

```python
# Customer segmentation
segments = df.groupby('segment').agg({
    'customer_id': 'count',
    'revenue': 'sum',
    'order_count': 'mean'
})
```

**For Prediction Projects:** Build and evaluate model

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Split data
X = df[['feature1', 'feature2', 'feature3']]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))
```

**Deliverable:** Analysis results or trained model

---

**5. Evaluation (Week 3)**

**Questions:**
- Do results answer the business question?
- Are insights actionable?
- What's the expected business impact?
- What are the limitations?

**Deliverable:** Results interpretation

**Template:**
```
Findings:
- 30% of customers are at high churn risk
- Primary risk factors: support tickets >3, tenure <6 months

Business Impact:
- Targeting 1,000 at-risk customers
- Expected retention improvement: 10%
- Revenue saved: £50K/quarter

Limitations:
- Model accuracy: 78% (good but not perfect)
- Missing data on customer satisfaction
- Recommendations need A/B testing
```

---

**6. Deployment (Week 4)**

**Tasks:**
- Write clear documentation (README)
- Create visualizations
- Write executive summary
- Publish to GitHub
- Update portfolio

**Deliverable:** Polished GitHub repository

**README Template:**
```markdown
# Customer Churn Prediction

## Problem
Reduce £200K quarterly churn by identifying at-risk customers.

## Data
- Source: Kaggle / Company CRM
- Size: 10,000 customers, 3 years
- Features: Demographics, purchase history, support tickets

## Methodology
1. Exploratory Data Analysis
2. Feature engineering (RFM, tenure)
3. Random Forest classification
4. Model evaluation and interpretation

## Results
- Model accuracy: 78%
- Key risk factors: Support tickets, low engagement
- Recommendation: Launch retention campaign

## Business Impact
- Target 1,000 high-risk customers
- Expected revenue saved: £50K/quarter
- ROI: 500% (£50K saved vs £10K campaign cost)

## Files
- `notebooks/01_eda.ipynb` - Exploratory analysis
- `notebooks/02_modeling.ipynb` - Model development
- `data/clean_data.csv` - Processed dataset
- `reports/executive_summary.pdf` - Business presentation

## Technologies
Python, Pandas, Scikit-learn, Matplotlib, Seaborn

## Author
[Your Name] - [LinkedIn] - [Email]
```
"""
        )

        st.markdown("#### 📁 Project Structure Best Practices")
        st.markdown(
            """**Organize Like a Professional:**

```
customer-churn-analysis/
│
├── README.md                 # Project overview
├── requirements.txt          # Python dependencies
├── .gitignore               # Ignore data/cache files
│
├── data/
│   ├── raw/                 # Original datasets (never modify!)
│   │   └── customers_raw.csv
│   ├── processed/           # Cleaned datasets
│   │   └── customers_clean.csv
│   └── README.md            # Data dictionary
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_results_visualization.ipynb
│
├── src/                     # Reusable Python modules
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   └── models.py
│
├── reports/
│   ├── figures/             # Charts for reports
│   │   ├── churn_by_tenure.png
│   │   └── feature_importance.png
│   └── executive_summary.pdf
│
└── models/                  # Saved models
    └── churn_model.pkl
```

**Why This Structure:**
- Clear organization (anyone can navigate)
- Reproducible (others can run your code)
- Professional (shows you know best practices)
"""
        )

        st.markdown("#### 🎨 Portfolio Presentation")
        st.markdown(
            """**Make Your Project Stand Out:**

**1. GitHub Repository**

**Must-Haves:**
- ✅ Clear README with problem, approach, results
- ✅ Organized folder structure
- ✅ Commented code in notebooks
- ✅ Requirements.txt for dependencies
- ✅ Professional commit messages

**Nice-to-Haves:**
- GitHub Pages site with interactive charts
- Automated testing
- CI/CD pipeline

---

**2. Visual Portfolio Website**

**Include:**
- Project title and one-sentence description
- Key visualizations (charts, dashboards)
- Business impact (£X saved, Y% improvement)
- Technologies used
- Link to GitHub

**Platforms:** GitHub Pages, Netlify, Streamlit Cloud

---

**3. Medium/LinkedIn Article**

**Structure:**
```
1. Context: Business problem
2. Data: What you worked with
3. Approach: Methods used
4. Results: Key findings (with charts!)
5. Impact: Business recommendations
6. Learnings: What you'd do differently
```

**Benefits:**
- Shows communication skills
- Demonstrates thought process
- Searchable by recruiters

---

**4. Video Walkthrough (Optional)**

**2-3 minute video showing:**
- Problem statement
- Key visualizations
- Main findings
- Business recommendations

**Tool:** Loom (free screen recording)

**Why:** Some recruiters prefer watching vs reading
"""
        )

        st.markdown("#### 💼 Career Integration Strategy")
        st.markdown(
            """**Turn Your Capstone Into Job Offers:**

---

**1. CV/Resume**

```
PROJECTS

Customer Churn Prediction | Python, Pandas, Scikit-learn
• Built machine learning model to predict customer churn (78% accuracy)
• Identified key risk factors through exploratory data analysis
• Recommended retention strategies saving £50K/quarter
• GitHub: github.com/yourname/customer-churn
```

**Formula:** Action + Result + Impact + Technologies

---

**2. LinkedIn Profile**

**Featured Section:**
- Add GitHub repository
- Add Medium article
- Add portfolio website

**About Section:**
```
Junior Data Analyst with expertise in customer analytics and churn prediction.
Recent project: Built ML model reducing churn by 10%, saving £50K/quarter.
```

---

**3. Cover Letters**

**Paragraph to Add:**
```
I recently completed a customer segmentation project using RFM analysis,
which identified high-value customer segments and recommended targeted
retention strategies. This project demonstrates my ability to translate
data insights into actionable business recommendations, which I'm excited
to bring to [Company Name]'s analytics team.
```

**Customize to Company:**
- E-commerce company → E-commerce project
- Healthcare company → Healthcare project

---

**4. Job Interviews**

**When Asked: "Tell me about a project"**

**Structure:**
1. **Situation:** "I wanted to understand customer churn drivers"
2. **Task:** "I analyzed 10,000 customer records over 3 years"
3. **Action:** "I performed RFM segmentation and built a classification model"
4. **Result:** "Identified at-risk customers with 78% accuracy, recommended retention campaign saving £50K"

**Bring:** Printed charts, GitHub repository open on laptop

---

**5. Networking Events**

**Elevator Pitch:**
```
"I'm a data analyst who recently built a customer churn prediction model.
I analyzed 10,000 customers and identified the top 3 risk factors, which
led to recommendations that could save £50K per quarter. I'd love to apply
these skills in [industry/company]."
```

**30 seconds, memorable, shows value**
"""
        )

        st.markdown("#### 🚀 Launch Checklist")
        st.markdown(
            """**Before Calling Your Project "Done":**

**Technical Checklist:**
- ☐ Code runs without errors
- ☐ All notebooks have markdown explanations
- ☐ Functions are documented
- ☐ No hardcoded paths (use relative paths)
- ☐ Data is clean and documented
- ☐ Visualizations are professional quality
- ☐ README is complete and clear

**Business Checklist:**
- ☐ Problem statement is clear
- ☐ Results answer the business question
- ☐ Insights are actionable (not just interesting)
- ☐ Business impact is quantified (£, %, time saved)
- ☐ Limitations are acknowledged
- ☐ Next steps are outlined

**Portfolio Checklist:**
- ☐ GitHub repository is public
- ☐ README has badges (Python version, license)
- ☐ Project is listed on LinkedIn
- ☐ CV is updated with project
- ☐ Portfolio website includes project
- ☐ At least 1 article/blog post written

**Career Checklist:**
- ☐ Practiced explaining project in 2 minutes
- ☐ Can answer "why this project?"
- ☐ Can explain technical choices
- ☐ Can discuss what you'd improve
- ☐ Ready to walk through code in interview

---

**When ALL boxes checked → You're ready to apply for jobs!**
"""
        )

        st.markdown("#### 🎯 Success Stories & Next Steps")
        st.markdown(
            """**What Happens When You Do This Right:**

**Case Study 1: Sarah - Junior Data Analyst**
- **Project:** E-commerce customer segmentation
- **Result:** Got 3 interviews in first week
- **Why:** Clear business focus, professional GitHub, quantified impact
- **Offer:** £35K starting salary at online retailer

**Case Study 2: James - Healthcare Analyst**
- **Project:** Patient readmission prediction
- **Result:** Hired before finishing course
- **Why:** Domain-specific project aligned with company needs
- **Offer:** £38K at NHS Trust

**Case Study 3: Priya - Marketing Analyst**
- **Project:** A/B testing framework
- **Result:** Promoted from intern to full-time
- **Why:** Showed understanding of business impact
- **Offer:** £32K + bonus

---

**Your Path:**

**Week 1-2:** Choose project and complete analysis  
**Week 3:** Polish code and create visualizations  
**Week 4:** Write documentation and publish  
**Week 5:** Update CV/LinkedIn and start applying  
**Week 6-8:** Interviews and offers

---

**Resources:**

**Datasets:**
- Kaggle: kaggle.com/datasets
- UCI ML Repository: archive.ics.uci.edu/ml
- Data.gov (UK): data.gov.uk
- Google Dataset Search: datasetsearch.research.google.com

**Project Inspiration:**
- Kaggle competitions (past winners)
- Medium data science articles
- Company data science blogs
- Academic research papers

**Portfolio Examples:**
- GitHub: search "data science portfolio"
- Medium: search "[industry] data analysis"
- LinkedIn: see what employed analysts share

---

**Final Words:**

Your capstone is your **proof of competence**. It shows:
- ✅ You can work independently
- ✅ You understand business context
- ✅ You can communicate findings
- ✅ You're ready for professional work

**Don't just complete the project. Make it portfolio-worthy.**

**You've learned:** Python, Pandas, SQL, Statistics, Visualization  
**Now show:** You can apply these skills to solve real problems

**Go build something amazing! 🚀**
"""
        )

        st.markdown("---")
        st.markdown("### 🧪 HANDS-ON LAB: Unit 7 Capstone Project")
        st.markdown(
            """**Build Your Portfolio Project End-to-End**

---

## Complete Capstone Workflow (4-6 weeks)

**Choose ONE of these project paths:**

### Option 1: E-Commerce Customer Analytics

**Business Question:** "How can we reduce customer churn and increase lifetime value?"

**Week 1-2: Data Collection & Cleaning**
```python
import pandas as pd
import numpy as np

# Load data (use public dataset or create synthetic)
customers = pd.read_csv('customers.csv')
orders = pd.read_csv('orders.csv')

# Data cleaning checklist
# ☐ Remove duplicates
# ☐ Handle missing values  
# ☐ Standardize formats (dates, names, currencies)
# ☐ Create customer_id index
# ☐ Merge datasets

# Save clean version
clean_data = customers.merge(orders, on='customer_id', how='left')
clean_data.to_csv('clean_customer_data.csv', index=False)
```

**Week 3: Analysis**
```python
# RFM Segmentation
from datetime import datetime

analysis_date = pd.to_datetime('2024-12-01')
rfm = clean_data.groupby('customer_id').agg({
    'order_date': lambda x: (analysis_date - x.max()).days,
    'order_id': 'count',
    'revenue': 'sum'
}).rename(columns={'order_date': 'recency', 'order_id': 'frequency', 'revenue': 'monetary'})

# Score and segment
rfm['segment'] = 'Standard'
rfm.loc[(rfm['recency'] < 30) & (rfm['monetary'] > 1000), 'segment'] = 'Champions'
rfm.loc[(rfm['recency'] > 90), 'segment'] = 'At Risk'

# Calculate metrics
churn_rate = (rfm['segment'] == 'At Risk').sum() / len(rfm) * 100
print(f"Churn Risk: {churn_rate:.1f}%")
```

**Week 4: Visualization & Reporting**
```python
import matplotlib.pyplot as plt

# Create dashboard
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Segment distribution
rfm['segment'].value_counts().plot(kind='bar', ax=axes[0,0], color='#3498db')
axes[0,0].set_title('Customer Segments')

# Revenue by segment
rfm.groupby('segment')['monetary'].sum().plot(kind='bar', ax=axes[0,1], color='#e67e22')
axes[0,1].set_title('Revenue by Segment')

# Recency distribution
rfm['recency'].hist(bins=30, ax=axes[1,0], color='#2ecc71')
axes[1,0].set_title('Days Since Last Purchase')

# Frequency vs Monetary
axes[1,1].scatter(rfm['frequency'], rfm['monetary'], alpha=0.5)
axes[1,1].set_xlabel('Frequency')
axes[1,1].set_ylabel('Monetary Value')
axes[1,1].set_title('Frequency vs Revenue')

plt.tight_layout()
plt.savefig('customer_analysis_dashboard.png', dpi=300)
```

---

### Option 2: A/B Test Analysis

**Business Question:** "Should we launch the new website design?"

**Complete Analysis Template:**

```python
# Load test results
df = pd.read_csv('ab_test_results.csv')

# 1. Sample Ratio Check
print("Sample sizes:")
print(df.groupby('variant').size())

# 2. Conversion rates
conversion_rates = df.groupby('variant')['converted'].mean()
print(f"\\nControl: {conversion_rates['control']:.2%}")
print(f"Treatment: {conversion_rates['treatment']:.2%}")

# 3. Statistical test
from scipy.stats import chi2_contingency

contingency_table = pd.crosstab(df['variant'], df['converted'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"\\nP-value: {p_value:.4f}")
if p_value < 0.05:
    print("✅ SIGNIFICANT - Launch new design!")
else:
    print("❌ NOT SIGNIFICANT - Keep testing")

# 4. Business impact
lift = (conversion_rates['treatment'] - conversion_rates['control']) / conversion_rates['control']
expected_additional_conversions = lift * 10000  # Assume 10K visitors/day
print(f"\\nExpected lift: {lift:.1%}")
print(f"Additional conversions per day: ~{expected_additional_conversions:.0f}")
```

---

## Project Deliverables Checklist

**1. Code (GitHub Repository)**
```
your-project/
├── README.md                    ← Project overview
├── requirements.txt             ← Dependencies
├── data/
│   ├── raw/                     ← Original data
│   └── processed/               ← Clean data
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_modeling.ipynb
├── src/
│   ├── data_processing.py       ← Reusable functions
│   └── visualization.py
└── reports/
    ├── figures/                 ← Charts
    └── final_report.pdf
```

**2. README Template**
```markdown
# Customer Churn Analysis

## Problem Statement
E-commerce company experiencing 15% monthly churn. Goal: Identify at-risk customers and recommend retention strategies.

## Data
- Source: Kaggle E-commerce Dataset
- Size: 5,000 customers, 2 years of transactions
- Features: Demographics, purchase history, engagement metrics

## Methodology
1. Data cleaning (handled 5% missing values)
2. RFM segmentation analysis
3. Churn risk modeling (Logistic Regression)
4. Visualization dashboard

## Key Findings
- **30% of customers are "At Risk"** (no purchase in 90+ days)
- **Top 20% of customers generate 65% of revenue**
- **Churn rate highest among customers with poor customer service experience**

## Business Recommendations
1. Launch win-back email campaign for at-risk customers (estimated £50K revenue recovery)
2. Improve customer service response time (reduce tickets >7 days to zero)
3. Create VIP loyalty program for top 20%

## Technologies
Python, Pandas, Scikit-learn, Matplotlib, Seaborn

## Results
- Model accuracy: 82%
- Expected churn reduction: 5%
- Projected revenue impact: £200K annually

## Author
[Your Name] | [LinkedIn] | [Email]
```

**3. Presentation Slides (5-7 slides)**
```
Slide 1: Title & Problem
Slide 2: Data Overview
Slide 3: Key Findings (with charts!)
Slide 4: Business Impact
Slide 5: Recommendations
Slide 6: Next Steps
Slide 7: Thank You (with contact info)
```

---

## Portfolio Presentation

**LinkedIn Post Template:**
```
🎯 Just completed my Data Science capstone project!

📊 Problem: E-commerce churn costing £200K/year

🔍 Analysis: Segmented 5,000 customers using RFM analysis

💡 Key Insight: 30% of customers at high churn risk due to poor support experience

✅ Solution: Win-back campaign + improved customer service

📈 Impact: Projected 5% churn reduction = £200K annual savings

Built with: Python | Pandas | Scikit-learn | Matplotlib

Full project: [GitHub link]

#DataScience #Python #Analytics #Portfolio
```

**Cover Letter Paragraph:**
```
"In my recent capstone project, I analyzed customer churn for an e-commerce company, identifying that 30% of customers were at high risk. Using Python and RFM segmentation, I developed retention recommendations projected to save £200K annually. This project demonstrates my ability to translate data insights into actionable business strategies—a skill I'm eager to bring to [Company Name]'s analytics team."
```

---

## Success Criteria

**Technical Excellence:**
- ☐ Clean, well-documented code
- ☐ Reproducible analysis (others can run your code)
- ☐ Professional visualizations
- ☐ Appropriate statistical methods

**Business Value:**
- ☐ Clear problem statement
- ☐ Actionable recommendations
- ☐ Quantified impact (£, %, time saved)
- ☐ Next steps outlined

**Presentation:**
- ☐ GitHub repository with README
- ☐ LinkedIn post showcasing project
- ☐ Updated CV with project bullet point
- ☐ Prepared 2-minute elevator pitch

**Interview Ready:**
- ☐ Can explain methodology in simple terms
- ☐ Can discuss limitations and improvements
- ☐ Can walk through code live
- ☐ Can answer "Why this project?"

---

**Final Checklist Before Publishing:**
- ☐ All code runs without errors
- ☐ No hardcoded file paths
- ☐ Clear comments throughout
- ☐ Professional README
- ☐ Charts are high-quality (300 DPI)
- ☐ Spell-check all documentation
- ☐ GitHub repo is public
- ☐ Added to LinkedIn Featured section

**You're now ready to apply for Junior Data Analyst roles! 🎉**
"""
        )

        st.markdown("---")
        st.markdown("#### 🛠️ Detailed Project Execution Guide")
        st.markdown(
            """**Week-by-Week Capstone Implementation**

---

**Week 1: Problem Definition & Data Collection**

**Day 1-2: Choose Your Domain**
```python
# Questions to ask yourself:
domains = {
    'E-Commerce': 'Customer behavior, sales, churn',
    'Healthcare': 'Patient outcomes, readmissions, resource allocation',
    'Finance': 'Fraud detection, credit risk, investment analysis',
    'Marketing': 'Campaign effectiveness, customer segmentation, ROI',
    'Operations': 'Supply chain, inventory, predictive maintenance'
}

# Pick domain where you want to work
target_domain = 'E-Commerce'  # Change this!

print(f"Selected: {target_domain}")
print(f"Focus areas: {domains[target_domain]}")
```

**Day 3-5: Find & Document Your Data**
```python
import pandas as pd

# Load data
df = pd.read_csv('your_dataset.csv')

# Initial documentation
print("="*60)
print("DATASET DOCUMENTATION")
print("="*60)
print(f"Source: Kaggle / Company / Public Dataset")
print(f"URL: [dataset link]")
print(f"\\nShape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Period: {df['date'].min()} to {df['date'].max()}")
print(f"\\nColumns:")
for col in df.columns:
    print(f"  - {col}: {df[col].dtype} ({df[col].isnull().sum()} nulls)")

# Save documentation
with open('data_dictionary.md', 'w') as f:
    f.write("# Data Dictionary\\n\\n")
    for col in df.columns:
        f.write(f"## {col}\\n")
        f.write(f"- Type: {df[col].dtype}\\n")
        f.write(f"- Description: [Add description]\\n")
        f.write(f"- Missing: {df[col].isnull().sum()} ({df[col].isnull().mean():.1%})\\n\\n")

print("\\n✅ data_dictionary.md created")
```

**Day 6-7: Write Problem Statement**
```markdown
# Problem Statement Template

## Business Context
[Company/Industry] faces [problem] resulting in [impact].

Example: E-commerce platform experiences 25% annual customer churn, 
resulting in £500K lost revenue.

## Objective
Use data analysis to [specific goal].

Example: Identify at-risk customers and recommend retention strategies 
to reduce churn by 10%.

## Success Metrics
- Primary: [main KPI]
- Secondary: [supporting metrics]

Example:
- Primary: Reduce churn from 25% to 22.5% (10% reduction)
- Secondary: Identify top 3 churn drivers

## Constraints
- Timeline: [project duration]
- Data: [what you have/don't have]
- Resources: [tools, compute]

Example:
- Timeline: 4 weeks
- Data: 2 years of customer transactions
- Resources: Local Python environment
```

---

**Week 2: Data Cleaning & EDA**

**Complete Data Cleaning Template:**

```python
import pandas as pd
import numpy as np

# Load raw data
df_raw = pd.read_csv('customers_raw.csv')
print(f"Raw data: {df_raw.shape}")

# 1. Handle missing values
print("\\n1. MISSING VALUES")
missing = df_raw.isnull().sum()
print(missing[missing > 0])

# Strategy A: Drop rows with critical missing data
df = df_raw.dropna(subset=['customer_id', 'revenue'])
print(f"After dropping: {df.shape}")

# Strategy B: Fill numerical columns
df['age'].fillna(df['age'].median(), inplace=True)
df['income'].fillna(df['income'].median(), inplace=True)

# Strategy C: Fill categorical columns
df['region'].fillna('Unknown', inplace=True)

# 2. Remove duplicates
print("\\n2. DUPLICATES")
before_dup = len(df)
df = df.drop_duplicates(subset=['customer_id'])
print(f"Removed {before_dup - len(df)} duplicates")

# 3. Fix data types
print("\\n3. DATA TYPES")
df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

# 4. Handle outliers
print("\\n4. OUTLIERS")
def cap_outliers(series, lower_percentile=1, upper_percentile=99):
    lower = series.quantile(lower_percentile / 100)
    upper = series.quantile(upper_percentile / 100)
    return series.clip(lower, upper)

df['revenue'] = cap_outliers(df['revenue'])
df['age'] = cap_outliers(df['age'], 5, 95)

# 5. Create new features
print("\\n5. FEATURE ENGINEERING")
df['customer_age_days'] = (pd.Timestamp.now() - df['signup_date']).dt.days
df['customer_age_months'] = df['customer_age_days'] / 30
df['is_active'] = df['last_purchase_days'] < 90

# Save clean version
df.to_csv('customers_clean.csv', index=False)
print(f"\\n✅ Clean data saved: {df.shape}")
print(f"Missing values remaining: {df.isnull().sum().sum()}")
```

**Comprehensive EDA Template:**

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# Create EDA report
fig, axes = plt.subplots(3, 3, figsize=(18, 14))
fig.suptitle('Exploratory Data Analysis Report', fontsize=20, fontweight='bold')

# 1. Target distribution
axes[0, 0].hist(df['churned'], bins=2, edgecolor='black')
axes[0, 0].set_title(f'Churn Rate: {df["churned"].mean():.1%}')
axes[0, 0].set_xlabel('Churned')

# 2. Age distribution
axes[0, 1].hist(df['age'], bins=30, edgecolor='black', alpha=0.7)
axes[0, 1].set_title('Age Distribution')
axes[0, 1].set_xlabel('Age')

# 3. Revenue distribution
axes[0, 2].hist(df['revenue'], bins=30, edgecolor='black', alpha=0.7, color='green')
axes[0, 2].set_title('Revenue Distribution')
axes[0, 2].set_xlabel('Revenue (£)')

# 4. Churn by region
churn_by_region = df.groupby('region')['churned'].mean()
axes[1, 0].barh(churn_by_region.index, churn_by_region.values, color='coral')
axes[1, 0].set_title('Churn Rate by Region')
axes[1, 0].set_xlabel('Churn Rate')

# 5. Revenue by churn status
df.boxplot(column='revenue', by='churned', ax=axes[1, 1])
axes[1, 1].set_title('Revenue: Churned vs Retained')
axes[1, 1].set_xlabel('Churned')

# 6. Correlation heatmap
numeric_cols = df.select_dtypes(include=[np.number]).columns[:8]
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[1, 2])
axes[1, 2].set_title('Correlation Matrix')

# 7. Customer tenure
axes[2, 0].hist(df['customer_age_months'], bins=30, edgecolor='black')
axes[2, 0].set_title('Customer Tenure Distribution')
axes[2, 0].set_xlabel('Months')

# 8. Churn vs Tenure
df.boxplot(column='customer_age_months', by='churned', ax=axes[2, 1])
axes[2, 1].set_title('Tenure: Churned vs Retained')

# 9. Top insights text
insights_text = f\"\"\"
KEY FINDINGS:

1. Churn Rate: {df['churned'].mean():.1%}

2. Avg Revenue: 
   - Retained: £{df[df['churned']==0]['revenue'].mean():.0f}
   - Churned: £{df[df['churned']==1]['revenue'].mean():.0f}

3. Avg Tenure:
   - Retained: {df[df['churned']==0]['customer_age_months'].mean():.1f} months
   - Churned: {df[df['churned']==1]['customer_age_months'].mean():.1f} months

4. Regional Differences:
   - Highest churn: {churn_by_region.idxmax()} ({churn_by_region.max():.1%})
   - Lowest churn: {churn_by_region.idxmin()} ({churn_by_region.min():.1%})
\"\"\"

axes[2, 2].text(0.1, 0.9, insights_text, transform=axes[2, 2].transAxes,
                fontsize=10, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
axes[2, 2].axis('off')

plt.tight_layout()
plt.savefig('eda_report.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ EDA report saved as eda_report.png")
```

---

**Week 3: Modeling & Analysis**

**Simple Model Template:**

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare data
features = ['age', 'revenue', 'customer_age_months', 'num_orders']
X = df[features]
y = df['churned']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\\nCLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# Feature importance
importance_df = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\\nFEATURE IMPORTANCE:")
print(importance_df)

plt.figure(figsize=(10, 6))
plt.barh(importance_df['feature'], importance_df['importance'])
plt.xlabel('Importance')
plt.title('Top Features Predicting Churn')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
plt.show()

print("\\n✅ Model trained and evaluated")
```

---

**Week 4: Documentation & Publishing**

**Complete README Template:**

````markdown
# Customer Churn Prediction - E-Commerce Analysis

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Problem Statement

E-commerce platform experiencing 25% annual customer churn, resulting in estimated £500K lost revenue. This project analyzes customer behavior patterns to identify at-risk customers and develop targeted retention strategies.

## 🎯 Objectives

1. Identify key drivers of customer churn
2. Build predictive model (target: 75%+ F1 score)
3. Recommend actionable retention strategies
4. Quantify potential business impact

## 📊 Dataset

- **Source:** Kaggle E-Commerce Dataset
- **Size:** 10,000 customers, 2 years of data
- **Features:** 15 (demographics, purchase history, engagement metrics)
- **Target:** Binary churn (yes/no)

## 🛠️ Technologies

- **Python 3.9+**
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine learning
- **Matplotlib/Seaborn** - Visualization
- **Jupyter** - Analysis notebooks

## 📁 Project Structure

```
├── data/
│   ├── raw/                  # Original dataset
│   └── processed/            # Cleaned data
├── notebooks/
│   ├── 01_eda.ipynb         # Exploratory analysis
│   ├── 02_modeling.ipynb    # Model development
│   └── 03_results.ipynb     # Final results
├── src/
│   ├── data_processing.py   # Data cleaning functions
│   └── modeling.py          # Model training functions
├── reports/
│   ├── figures/             # Visualizations
│   └── executive_summary.pdf
├── requirements.txt
└── README.md
```

## 🔍 Key Findings

### 1. Churn Drivers
- **Low engagement:** Customers with <2 orders/month have 3x higher churn
- **Poor support experience:** 45% of churned customers had unresolved tickets
- **No recent purchase:** 90+ days since last order → 65% churn probability

### 2. Customer Segments
| Segment | Size | Churn Rate | Avg Revenue |
|---------|------|------------|-------------|
| Champions | 15% | 5% | £850 |
| At Risk | 30% | 45% | £320 |
| Lost | 20% | 95% | £180 |

### 3. Model Performance
- **Algorithm:** Random Forest
- **F1 Score:** 0.78
- **Precision:** 0.75
- **Recall:** 0.81
- **ROC-AUC:** 0.85

## 💡 Recommendations

### Immediate Actions (Q1)
1. **Win-back campaign for at-risk customers** (n=3,000)
   - Personalized 15% discount offers
   - Expected recovery: 500 customers
   - Revenue impact: £160K

2. **Improve support response time**
   - Target: <24hr for all tickets
   - Cost: £50K system upgrade
   - Expected churn reduction: 5%

3. **Launch loyalty program**
   - Reward frequent buyers
   - Expected impact: +10% retention

### Business Impact
- **Projected churn reduction:** 25% → 22.5% (10% improvement)
- **Revenue retained:** £125K annually
- **ROI:** 250% (£125K saved vs £50K investment)

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourname/churn-analysis.git
cd churn-analysis

# Install dependencies
pip install -r requirements.txt

# Run analysis
jupyter notebook notebooks/01_eda.ipynb
```

## 📈 Results Summary

![Churn Prediction Model](reports/figures/model_performance.png)

## 🔮 Future Improvements

- Add customer lifetime value (CLV) prediction
- Integrate real-time scoring API
- A/B test retention campaigns
- Expand feature set (social media, product reviews)

## 👤 Author

**[Your Name]**
- LinkedIn: [Profile URL]
- Email: your.email@example.com
- Portfolio: [Website URL]

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Dataset: Kaggle E-Commerce Dataset
- Inspiration: [Any relevant papers/blogs]
````
"""
        )

        st.markdown("---")
        st.markdown("#### 🐛 Troubleshooting Common Issues")
        st.markdown(
            """**Problem 1: Model overfitting (train=95%, test=65%)**

**Solution:**
```python
# Use cross-validation
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
print(f"CV F1: {scores.mean():.3f} (+/- {scores.std():.3f})")

# Reduce model complexity
model = RandomForestClassifier(
    n_estimators=50,        # Fewer trees
    max_depth=10,           # Limit depth
    min_samples_split=20,   # Require more samples
    random_state=42
)
```

---

**Problem 2: Imbalanced classes (10% positive, 90% negative)**

**Solution:**
```python
from sklearn.utils import resample

# Oversample minority class
df_majority = df[df['churned']==0]
df_minority = df[df['churned']==1]

df_minority_upsampled = resample(df_minority, 
                                  n_samples=len(df_majority),
                                  random_state=42)

df_balanced = pd.concat([df_majority, df_minority_upsampled])

# Or use class weights
model = RandomForestClassifier(class_weight='balanced')
```

---

**Problem 3: Poor feature importance interpretation**

**Solution:**
```python
# Use SHAP for better explanations
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values[1], X_test, feature_names=features)
```

---

**Problem 4: Data leakage (unrealistic 99% accuracy)**

**Check for:**
```python
# 1. Target in features?
print("Features:", X.columns.tolist())
# Should NOT include 'churned' or 'churn_date'

# 2. Future information?
# Don't use 'last_purchase_date' if predicting future churn

# 3. High correlation with target?
correlations = df[features + ['churned']].corr()['churned'].sort_values(ascending=False)
print(correlations)
# Investigate any correlation > 0.9
```
"""
        )

        st.markdown("---")
        st.markdown("#### 🎤 Interview Questions: Capstone Project")
        st.markdown(
            """**Be Ready to Answer:**

**Q1: Walk me through your capstone project.**

**Answer (2-minute structure):**

"I analyzed customer churn for an e-commerce platform experiencing 25% annual churn.

**Problem:** They were losing £500K annually and didn't know why.

**Approach:** 
- Analyzed 10K customers over 2 years
- Identified 3 key churn drivers: low engagement, poor support, dormant accounts
- Built Random Forest model (78% F1 score)

**Results:**
- Recommended win-back campaign for 3,000 at-risk customers
- Projected £125K revenue retention
- 250% ROI

**Key Insight:** Support ticket resolution time was the #1 predictor - customers with unresolved tickets had 3x higher churn."

---

**Q2: What would you do differently?**

**Good Answer:**

"Three things:

1. **More features:** I'd add customer service sentiment analysis from ticket text
2. **Real-time scoring:** Build API to score customers daily vs monthly batch
3. **A/B test:** Actually test the retention campaign and measure real impact

The model worked well, but I'd focus more on deployment and measuring actual business results."

---

**Q3: How did you handle imbalanced data?**

**Answer:**

"The dataset had 75% retained vs 25% churned. I tried three approaches:

1. **Class weights:** Penalize misclassifying minority class
2. **SMOTE:** Synthetic oversampling
3. **Custom threshold:** Optimized for F1 instead of accuracy

Class weights performed best. I also reported precision/recall separately since accuracy was misleading."

---

**Q4: What was the biggest challenge?**

**Answer:**

"Feature engineering. Raw data didn't have clear signals. I created:
- Recency: Days since last order
- Frequency: Orders per month
- Engagement score: Clicks + purchases + support interactions

These engineered features were 3x more important than raw demographics. Taught me that domain knowledge drives model performance."

---

**Q5: How would you deploy this model?**

**Answer:**

"Three-phase approach:

**Phase 1 (Week 1):** Batch scoring - Score all customers monthly, send high-risk list to marketing

**Phase 2 (Month 2):** API - Real-time scoring when customer behavior changes

**Phase 3 (Month 3):** Automated actions - Trigger retention emails automatically

Monitor F1 score weekly, retrain quarterly with new data."
"""
        )

        st.markdown("---")
        st.markdown("#### 🏆 Final Success Checklist")
        st.markdown(
            """**Before Calling Your Project "Done":**

**Analysis Quality (20 points):**
- ☐ Data cleaning is documented (2 pts)
- ☐ EDA reveals 3+ insights (3 pts)
- ☐ Feature engineering adds value (3 pts)
- ☐ Model F1 > 0.70 (3 pts)
- ☐ Results are statistically significant (2 pts)
- ☐ Overfitting is addressed (2 pts)
- ☐ Feature importance is interpreted (2 pts)
- ☐ Limitations are discussed (2 pts)
- ☐ Next steps are outlined (1 pt)

**Code Quality (15 points):**
- ☐ All code runs without errors (5 pts)
- ☐ Functions are documented (3 pts)
- ☐ No hardcoded paths (2 pts)
- ☐ Consistent naming (2 pts)
- ☐ Modular structure (3 pts)

**Documentation (15 points):**
- ☐ README is comprehensive (5 pts)
- ☐ Data dictionary exists (3 pts)
- ☐ Comments explain "why" not "what" (2 pts)
- ☐ Results are visualized (3 pts)
- ☐ Methodology is reproducible (2 pts)

**Business Focus (20 points):**
- ☐ Problem statement is clear (4 pts)
- ☐ Stakeholders are identified (3 pts)
- ☐ Impact is quantified (£, %) (5 pts)
- ☐ Recommendations are actionable (4 pts)
- ☐ ROI is calculated (4 pts)

**Presentation (15 points):**
- ☐ GitHub is public and organized (3 pts)
- ☐ LinkedIn post written (3 pts)
- ☐ CV updated (2 pts)
- ☐ Can explain in 2 minutes (3 pts)
- ☐ Visualizations are professional (4 pts)

**Career Integration (15 points):**
- ☐ Portfolio website updated (3 pts)
- ☐ Cover letter paragraph ready (3 pts)
- ☐ Can answer "why this project?" (3 pts)
- ☐ Can discuss technical details (3 pts)
- ☐ Can explain business impact (3 pts)

---

**Scoring:**
- **80-100 points:** Excellent! Ready for interviews
- **60-79 points:** Good! Polish weak areas
- **Below 60:** Keep working before publishing

**Target: 80+ points before applying to jobs!**
"""
        )

        st.markdown("---")
        st.markdown("#### 🎯 Post-Capstone: Landing Your First Job")
        st.markdown(
            """**Step-by-Step Job Search Strategy**

**Week 1-2: Portfolio Polish**
- ✅ Publish capstone to GitHub
- ✅ Create portfolio website (use GitHub Pages - free!)
- ✅ Write 3 LinkedIn posts about your learnings
- ✅ Update CV with capstone project

**Week 3-4: Application Sprint**
- Apply to 20-30 Junior Data Analyst roles
- Tailor each cover letter (mention capstone!)
- Track applications in spreadsheet
- Follow up after 1 week

**Sample Application Tracker:**
```
| Company | Role | Applied | Followed Up | Status | Notes |
|---------|------|---------|-------------|--------|-------|
| Acme Corp | Junior Analyst | 2024-03-01 | 2024-03-08 | Interview! | Mentioned capstone |
```

**Week 5-8: Interview Preparation**

Practice these questions:
1. Tell me about yourself (2 min)
2. Walk through your capstone (2 min)
3. SQL: Write query to find top customers
4. Python: Explain pandas groupby
5. Statistics: Explain p-value
6. Business: Calculate ROI of marketing campaign

**Week 9+: Offers & Negotiation**

Typical Junior Data Analyst Offers (UK):
- £25K-35K depending on location/company
- Remote/hybrid options common
- Growth to £45K+ within 2 years

**Red Flags to Avoid:**
- ❌ No structured onboarding
- ❌ Expect expert-level skills
- ❌ No mentorship available
- ❌ Tech stack from 1990s
- ❌ Unrealistic timelines

**Green Flags to Look For:**
- ✅ Learning & development budget
- ✅ Senior analysts to learn from
- ✅ Modern tools (Python, SQL, cloud)
- ✅ Clear career progression
- ✅ Supportive manager

---

**Your Timeline:**

**Today → Week 4:** Finish capstone  
**Week 4 → Week 6:** Polish & publish  
**Week 6 → Week 10:** Apply & interview  
**Week 10+:** Start your data science career!

**You've got this! 🚀**
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

    # Assessments
    with tabs[3]:
        st.subheader("📝 Assessments")
        st.info(
            "Quick-check quizzes help reinforce learning. "
            "These are formative self-tests, not graded submissions."
        )

        quiz_bank = {
            1: [
                {
                    "question": "What does CRISP-DM stand for?",
                    "options": [
                        "Cross-Industry Standard Process for Data Mining",
                        "Critical Statistical Process for Data Management",
                        "Comprehensive Research in Statistical Programming",
                    ],
                    "answer": 0,
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
            st.markdown(f"**Q{idx + 1}. {q['question']}**")
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
