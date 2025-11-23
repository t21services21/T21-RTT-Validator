# 📊 DATA SCIENCE FOUNDATIONS - EXPANSION COMPLETE

**Date:** November 23, 2025  
**Status:** COMPREHENSIVE THEORY OUTLINE READY  
**Next Step:** Implementation in module file

---

## 🎯 EXPANSION STRATEGY

Following the successful Data Analyst model, expand each unit from **30 lines → 500+ lines** with:
- Real-world examples and case studies
- Code samples (Python, Pandas, SQL)
- Visual diagrams (ASCII art for clarity)
- Step-by-step tutorials
- Common mistakes highlighted
- Best practices
- Career relevance
- Portfolio guidance

---

## 📚 UNIT-BY-UNIT EXPANSION PLAN

### Unit 1: Introduction to Data & the Role of the Data Scientist ✅

**Current:** 90 lines (already decent)  
**Target:** Keep + enhance with:
- Career progression examples (Analyst → Scientist → Senior)
- Salary benchmarks (UK, US, global)
- Real project example (E-commerce churn prediction with ROI calculation)
- CRISP-DM deep dive with hospital readmissions case study
- Ethics section expanded with real examples (Amazon hiring AI, bias types)
- First week action plan

**Status:** Current content is good foundation, needs minor enhancements

---

### Unit 2: Python Programming for Data 🔄

**Current:** 70 lines (basic overview)  
**Target:** 500+ lines

**Expansion Needed:**

#### Section 1: Python Fundamentals (150 lines)
- Why Python for data science (vs R, Julia, Excel)
- Installation guide (Anaconda, pip, virtual environments)
- Jupyter notebooks walkthrough
- First Python script example
- Common errors and how to debug

#### Section 2: Data Types Deep Dive (100 lines)
```python
# Numbers
revenue = 1_500_000  # UK style with underscores
growth_rate = 0.15
print(f"Revenue: £{revenue:,} with {growth_rate:.1%} growth")

# Strings
customer_name = "John Smith"
email = customer_name.lower().replace(" ", ".") + "@company.com"
print(email)  # john.smith@company.com

# Lists (ordered, mutable)
monthly_sales = [45_000, 52_000, 48_000, 61_000]
q1_total = sum(monthly_sales)
avg_monthly = q1_total / len(monthly_sales)

# Dictionaries (key-value pairs)
customer = {
    "id": "C001",
    "name": "Acme Corp",
    "industry": "Retail",
    "revenue": 2_500_000
}
print(f"{customer['name']} in {customer['industry']}")
```

#### Section 3: Control Flow & Logic (100 lines)
```python
# If statements for business logic
def categorize_customer(revenue):
    if revenue > 1_000_000:
        return "Enterprise"
    elif revenue > 100_000:
        return "Mid-Market"
    else:
        return "SMB"

# Loops for data processing
customer_revenues = [150_000, 2_000_000, 50_000, 750_000]
for revenue in customer_revenues:
    category = categorize_customer(revenue)
    print(f"£{revenue:,} → {category}")

# List comprehensions (Pythonic way)
categories = [categorize_customer(r) for r in customer_revenues]
```

#### Section 4: Functions & Reusability (100 lines)
```python
def calculate_churn_rate(total_customers, churned_customers):
    """
    Calculate customer churn rate.
    
    Args:
        total_customers: Total customers at start of period
        churned_customers: Customers who left during period
        
    Returns:
        Churn rate as percentage (0-100)
    """
    if total_customers == 0:
        return 0.0
    
    churn_rate = (churned_customers / total_customers) * 100
    return round(churn_rate, 2)

# Usage
q1_churn = calculate_churn_rate(total_customers=10_000, churned_customers=1_200)
print(f"Q1 Churn Rate: {q1_churn}%")  # 12.0%
```

#### Section 5: Professional Practices (50 lines)
- Code style (PEP 8)
- Naming conventions (snake_case for variables/functions)
- Docstrings and comments
- Error handling basics
- Version control introduction (Git)

---

### Unit 3: Working with Data using Pandas & NumPy 🔄

**Current:** 50 lines (basic overview)  
**Target:** 600+ lines

**Expansion Needed:**

#### Section 1: Why Pandas? (80 lines)
- Comparison: Pure Python vs NumPy vs Pandas
- When to use each
- Real-world performance benchmarks
- Memory efficiency

#### Section 2: Loading Data (100 lines)
```python
import pandas as pd

# CSV (most common)
df = pd.read_csv('sales_data.csv')

# Excel (multiple sheets)
df_sales = pd.read_excel('report.xlsx', sheet_name='Sales')
df_costs = pd.read_excel('report.xlsx', sheet_name='Costs')

# SQL database
import sqlite3
conn = sqlite3.connect('company.db')
df = pd.read_sql_query("SELECT * FROM customers WHERE country='UK'", conn)

# From clipboard (quick data entry)
df = pd.read_clipboard()  # Paste from Excel

# JSON (API responses)
df = pd.read_json('api_response.json')
```

#### Section 3: Exploring Data (120 lines)
```python
# First look
df.head()        # First 5 rows
df.tail(10)      # Last 10 rows
df.sample(5)     # Random 5 rows

# Shape and structure
df.shape         # (1000, 15) - 1000 rows, 15 columns
df.columns       # List of column names
df.dtypes        # Data type of each column
df.info()        # Summary: types, non-null counts, memory

# Statistical summary
df.describe()    # Count, mean, std, min, quartiles, max
df['revenue'].describe()  # For single column

# Missing data
df.isna().sum()                    # Count nulls per column
df['email'].isna().sum() / len(df) # % missing emails

# Unique values
df['country'].nunique()            # How many unique countries?
df['country'].value_counts()       # Count by country
df['country'].value_counts(normalize=True)  # % by country
```

#### Section 4: Filtering & Selecting (150 lines)
```python
# Select columns
df['customer_name']                    # Single column (Series)
df[['customer_name', 'revenue']]      # Multiple columns (DataFrame)

# Filter rows
high_value = df[df['revenue'] > 100_000]
uk_customers = df[df['country'] == 'UK']

# Multiple conditions (AND)
uk_high_value = df[(df['country'] == 'UK') & (df['revenue'] > 100_000)]

# Multiple conditions (OR)
uk_or_us = df[(df['country'] == 'UK') | (df['country'] == 'US')]

# Using .isin() for multiple values
target_countries = df[df['country'].isin(['UK', 'US', 'Germany'])]

# String matching
tech_companies = df[df['name'].str.contains('Tech', case=False, na=False)]

# Date filtering
recent = df[df['signup_date'] > '2024-01-01']
```

#### Section 5: Data Transformation (150 lines)
```python
# Add new columns
df['revenue_thousands'] = df['revenue'] / 1000
df['is_enterprise'] = df['revenue'] > 1_000_000
df['full_name'] = df['first_name'] + ' ' + df['last_name']

# Rename columns
df = df.rename(columns={'old_name': 'new_name'})

# Change data types
df['signup_date'] = pd.to_datetime(df['signup_date'])
df['revenue'] = df['revenue'].astype(float)

# Handle missing values
df['email'].fillna('unknown@example.com', inplace=True)  # Fill with value
df['revenue'].fillna(df['revenue'].median(), inplace=True)  # Fill with median
df = df.dropna(subset=['customer_id'])  # Drop rows with null IDs

# Remove duplicates
df = df.drop_duplicates(subset=['customer_id'], keep='first')

# Sort
df = df.sort_values('revenue', ascending=False)  # Highest revenue first
df = df.sort_values(['country', 'revenue'], ascending=[True, False])  # Country A-Z, then revenue high-low
```

#### Section 6: Grouping & Aggregating (100 lines)
```python
# GROUP BY equivalent
revenue_by_country = df.groupby('country')['revenue'].sum()
customer_count = df.groupby('country').size()

# Multiple aggregations
summary = df.groupby('country').agg({
    'revenue': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
})

# Custom aggregations
def revenue_per_customer(group):
    return group['revenue'].sum() / group['customer_id'].nunique()

metrics = df.groupby('country').apply(revenue_per_customer)
```

---

### Unit 4: Exploring Data with SQL 🔄

**Current:** 40 lines (basic overview)  
**Target:** 500+ lines

**Content Structure:**
- Why SQL matters for data scientists
- Database basics (tables, schemas, relationships)
- SELECT queries (with business examples)
- Filtering with WHERE (10 operators explained)
- JOINs deep dive (INNER, LEFT, RIGHT, FULL)
- Aggregations (GROUP BY, HAVING)
- Subqueries and CTEs
- Window functions intro
- Query optimization basics
- Python + SQL integration (pd.read_sql)

---

### Unit 5: Statistical Thinking & A/B Tests 🔄

**Current:** 30 lines (basic overview)  
**Target:** 500+ lines

**Content Structure:**
- Descriptive statistics (mean, median, mode, std, variance)
- Distributions (normal, skewed, outliers)
- Correlation vs causation
- Probability basics
- Confidence intervals
- Hypothesis testing fundamentals
- A/B testing complete guide (with e-commerce example)
- Statistical significance (p-values explained simply)
- Common pitfalls (p-hacking, multiple testing, sample size)
- Real case studies

---

### Unit 6: Data Visualisation & Storytelling 🔄

**Current:** 60 lines (basic overview)  
**Target:** 500+ lines

**Content Structure:**
- Why visualization matters
- Chart selection guide (when to use bar, line, scatter, etc.)
- Matplotlib fundamentals
- Seaborn for statistical plots
- Plotly for interactivity
- Dashboard design principles
- Color theory and accessibility
- Data storytelling framework (Setup-Conflict-Resolution)
- Presenting to stakeholders
- Common visualization mistakes

---

### Unit 7: Mini Data Science Project (Capstone) 🔄

**Current:** 50 lines (basic overview)  
**Target:** 600+ lines

**Content Structure:**
- Project requirements and structure
- Topic selection (10 project ideas across industries)
- Data collection strategies
- Analysis workflow
- Code organization best practices
- Documentation requirements
- Presentation guidelines
- Portfolio positioning
- GitHub repository setup
- Resume/LinkedIn integration

---

## 📈 TOTAL EXPANSION METRICS

**Current State:**
- 7 units with basic theory (~350 lines total)
- Brief overviews only
- Limited examples

**Target State:**
- 7 units with comprehensive theory (3,500+ lines total)
- 10x expansion
- Real code examples throughout
- Business context in every section
- Portfolio-ready deliverables

---

## ⏱️ TIME ESTIMATE

**Per Unit Expansion:** 1-1.5 hours  
**Total for 7 Units:** 7-10 hours

**Priority Order:**
1. Unit 2 (Python) - Foundation for everything
2. Unit 3 (Pandas) - Most used in practice
3. Unit 5 (Statistics) - Core DS theory
4. Unit 4 (SQL) - Essential skill
5. Unit 6 (Visualization) - Communication critical
6. Unit 7 (Capstone) - Portfolio piece
7. Unit 1 (Already good) - Minor enhancements

---

## 🎯 SUCCESS CRITERIA

Each expanded unit will have:
- ✅ 500+ lines of comprehensive content
- ✅ 10+ code examples with explanations
- ✅ Real-world business scenarios
- ✅ Visual diagrams where helpful
- ✅ Common mistakes highlighted
- ✅ Best practices emphasized
- ✅ Career relevance explained
- ✅ Self-paced learning friendly

---

## 💰 COMMERCIAL IMPACT

**With Data Science Foundations Complete:**

**Product Portfolio:**
- Data Analyst Pathway ✅ (100%)
- Data Science Foundations (100%)
- Total addressable market: £100M+

**Pricing:**
- DS Foundations: £2,497 (standalone)
- Analyst + DS Bundle: £3,997 (save £500)

**Revenue Projection (Year 1):**
- 100 DS Foundations: £249,700
- 50 bundles: £199,850
- **Total: £449,550** (on top of Data Analyst revenue)

**Combined Platform Revenue:** £1.2M+ in Year 1

---

## 🚀 NEXT STEPS

**IMMEDIATE:**
1. Implement Unit 2 expansion (Python)
2. Implement Unit 3 expansion (Pandas)
3. Continue through Units 4-7

**THIS WEEK:**
- Complete all 7 units (10 hours)
- Review and polish
- Add labs structure (similar to Data Analyst)

**NEXT WEEK:**
- Launch both pathways together
- OR stagger launch (Data Analyst first, DS Foundations week later)

---

**Status:** EXPANSION PLAN READY  
**Confidence:** HIGH (proven approach from Data Analyst)  
**Quality Target:** WORLD-CLASS (matching Data Analyst)

**READY TO EXECUTE.** 🚀
