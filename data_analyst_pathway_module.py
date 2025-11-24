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


COURSE_ID = "data_analyst_pathway"
COURSE_NAME = "Data Analyst Pathway"


UNITS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Data & Business Questions for Analysts",
        "level": "Beginner",
        "glh": 12,
        "credits": 2,
    },
    2: {
        "name": "Spreadsheet Skills for Analysis",
        "level": "Beginner",
        "glh": 18,
        "credits": 3,
    },
    3: {
        "name": "SQL for Data Analysts",
        "level": "Beginner/Intermediate",
        "glh": 24,
        "credits": 4,
    },
    4: {
        "name": "BI Dashboards & Storytelling",
        "level": "Intermediate",
        "glh": 18,
        "credits": 3,
    },
    5: {
        "name": "Python for Analysts",
        "level": "Intermediate",
        "glh": 24,
        "credits": 4,
    },
    6: {
        "name": "Metrics, A/B Tests & KPI Design",
        "level": "Intermediate",
        "glh": 18,
        "credits": 3,
    },
    7: {
        "name": "Data Analyst Capstone Project",
        "level": "Intermediate",
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
        st.markdown("#### 📘 What is Data Analysis? The Complete Foundation")
        st.markdown(
            """Data analysis is the systematic process of inspecting, cleaning, transforming, 
and modeling data to discover useful information, draw conclusions, and support 
decision-making. As a data analyst, you're not just crunching numbers—you're 
translating business problems into analytical questions, then translating analytical 
findings back into actionable business recommendations.

**Your Core Role as a Data Analyst:**

You are the **bridge between data and decisions**. This means:
- Understanding what stakeholders really need (not just what they ask for)
- Knowing where data lives and how to access it
- Cleaning and preparing data for analysis
- Performing the actual analysis (queries, calculations, visualizations)
- Communicating findings in business language
- Recommending specific actions based on data

**Real-World Example:**

Imagine you're a Data Analyst at a hospital trust. A clinic manager approaches you:

*"We're getting too many DNAs (Did Not Attends). Can you help?"*

A weak analyst response:
*"Sure, I'll pull the DNA numbers."*

A strong analyst response:
*"Let me make sure I understand what you need. Are you asking:*
- *What % of appointments are DNAs overall?*
- *Which clinics or specialties have the highest DNA rates?*
- *Are there patterns by day of week, time of day, or patient demographics?*
- *Has this rate changed over time?*
- *What's the impact on waiting lists and capacity?"*

See the difference? You're clarifying the actual business problem before diving into data.

**The Data Analysis Process (Your Daily Workflow):**

1. **Understand the Question** (30% of your time)
   - Meet with stakeholders
   - Clarify vague requests
   - Define success metrics
   - Agree on timeframes and scope

2. **Find and Access Data** (20% of your time)
   - Identify data sources
   - Get necessary permissions
   - Understand data structure
   - Check data quality

3. **Clean and Prepare Data** (40% of your time - YES, really!)
   - Handle missing values
   - Fix inconsistencies
   - Merge data from multiple sources
   - Create calculated fields

4. **Analyze** (5% of your time)
   - Run queries
   - Create visualizations
   - Identify patterns
   - Test hypotheses

5. **Communicate Results** (5% of your time)
   - Create clear visuals
   - Write executive summaries
   - Present findings
   - Recommend actions

**Notice:** Most of your time is BEFORE and AFTER the actual analysis!
"""
        )

        st.markdown("#### 🎯 From Vague Requests to Clear, Measurable Questions")
        st.markdown(
            """One of your most valuable skills is **requirements clarification**. 
Stakeholders rarely know how to ask analytical questions perfectly. They'll say:

- "Why are we so busy?"
- "Marketing isn't working."
- "Sales are down."
- "Can you check the numbers?"

Your job is to transform these into **SMART questions** (Specific, Measurable, 
Actionable, Relevant, Time-bound).

**Transformation Framework:**

**Vague Request:** "Why are we so busy?"

**Your Clarifying Questions:**
- Busy compared to what? (need a baseline)
- Which department/clinic/team?
- Busy = more patients, longer hours, or overwhelmed staff?
- What time period are we talking about?
- What would 'not busy' look like in numbers?

**Refined Question:**
*"Has patient volume in the Outpatient Dermatology clinic increased compared 
to the same quarter last year? If so, by how much, and which appointment types 
are driving the increase?"*

Now THAT'S answerable with data!

**More Examples:**

| Vague Request | Problem | Better Question |
|---------------|---------|----------------|
| "Marketing isn't working" | No metrics defined | "Has our email campaign conversion rate changed? Comparing this month vs last month, segmented by customer type" |
| "Sales are down" | No timeframe, no segment | "What % has revenue decreased in Q4 vs Q3? Which product lines show the biggest decline?" |
| "Customers are unhappy" | Subjective, no data | "What's our Net Promoter Score this quarter vs last? Which service areas receive the most complaints?" |
| "We need more staff" | No evidence | "What's our current appointments-per-staff ratio? How does it compare to industry benchmarks? Where are the bottlenecks?" |

**The SMART Framework Applied:**

Always refine requests to include:

**S - Specific:** Which department? Which metric? Which customer segment?

**M - Measurable:** Can we express this as a number, %, rate, or count?

**A - Actionable:** Will the answer lead to a decision or action?

**R - Relevant:** Does this align with business priorities?

**T - Time-bound:** What's the time period? Need a comparison period?

**Practice Exercise (You'll do this in labs):**

Take this request: *"The website is slow."*

Refine it into 3 measurable questions:
1. What is the current average page load time, and has it increased compared to last month?
2. Which pages have load times exceeding our 3-second target?
3. What % of users are experiencing load times > 5 seconds, broken down by device type?

See how each question is now answerable with data?

"""
        )

        st.markdown("#### 🧩 Mapping Questions to Data Sources: Where Does the Data Actually Live?")
        st.markdown(
            """Once you have a clear question, you need to know **where to find the data**. 
This requires understanding your organization's data landscape.

**Common Data Sources in Organizations:**

**1. Transactional Systems (Operational Databases)**
- **What:** Systems that run daily operations
- **Examples:**
  - Hospital: Electronic Health Records (EHR), appointment scheduling system
  - Retail: Point of Sale (POS), inventory management
  - E-commerce: Order management, customer accounts
- **Data:** Usually in SQL databases (PostgreSQL, MySQL, SQL Server)
- **Access:** Need credentials, sometimes restricted
- **Quality:** Generally good (validated at entry)

**2. CRM & Marketing Tools**
- **What:** Customer relationship and marketing campaign data
- **Examples:**
  - Salesforce, HubSpot, Mailchimp
  - Google Analytics, Facebook Ads Manager
- **Data:** Some have SQL access, many are API or CSV exports
- **Access:** Often need admin permissions
- **Quality:** Variable (depends on how users maintain it)

**3. Data Warehouses / Business Intelligence Systems**
- **What:** Centralized repository combining multiple sources
- **Examples:**
  - Snowflake, Redshift, BigQuery
  - Tableau Server, Power BI Service
- **Data:** Pre-cleaned and structured for analysis
- **Access:** This is YOUR best friend as an analyst
- **Quality:** Usually good (ETL processes clean it)

**4. Spreadsheets & Manual Trackers**
- **What:** Excel/Google Sheets maintained by teams
- **Examples:**
  - Budget trackers
  - Project status logs
  - Customer feedback spreadsheets
- **Data:** Highly variable formats
- **Access:** Usually on shared drives or Google Drive
- **Quality:** Often messy, needs cleaning

**5. External Data Sources**
- **What:** Data from outside your organization
- **Examples:**
  - Government statistics (ONS, NHS Digital)
  - Weather data
  - Market research reports
- **Data:** Various formats (CSV, API, PDF reports)
- **Access:** Some free, some paid
- **Quality:** Variable

**Mapping Exercise: DNA (Did Not Attend) Analysis**

Question: *"Which clinics have the highest DNA rates, and are there patterns by 
patient demographics?"*

**Data Needed:**
- Appointment data (appointment_id, clinic_id, patient_id, appointment_date, 
  appointment_time, status [attended/DNA])
- Patient demographics (patient_id, age, gender, postcode, deprivation_index)
- Clinic information (clinic_id, specialty, location)

**Where to Find It:**
- Appointments: Electronic Scheduling System → appointments table
- Demographics: Patient Administration System → patients table
- Clinics: Reference Data → clinics table

**Join Logic:**
```sql
SELECT 
    c.clinic_name,
    c.specialty,
    COUNT(*) as total_appointments,
    SUM(CASE WHEN a.status = 'DNA' THEN 1 ELSE 0 END) as dna_count,
    ROUND(100.0 * SUM(CASE WHEN a.status = 'DNA' THEN 1 ELSE 0 END) / COUNT(*), 2) as dna_rate
FROM appointments a
JOIN clinics c ON a.clinic_id = c.clinic_id
WHERE a.appointment_date >= '2024-01-01'
GROUP BY c.clinic_name, c.specialty
ORDER BY dna_rate DESC;
```

See how we mapped the question to actual tables and fields?

**Data Source Checklist:**

For ANY analysis, ask yourself:

- [ ] Where does this data live? (system name, table name)
- [ ] Do I have access? (credentials, permissions)
- [ ] How current is the data? (real-time, daily batch, weekly?)
- [ ] What's the data quality like? (known issues, missing values?)
- [ ] Do I need to join multiple sources? (what's the join key?)
- [ ] Are there any GDPR/privacy considerations? (PII, patient data?)
- [ ] What's the historical depth? (how far back can I query?)

**Practical Tip:** Create a "Data Source Inventory"

Maintain a personal reference document:

| Data Domain | System | Access Method | Key Tables | Join Keys | Known Issues |
|-------------|--------|---------------|------------|-----------|-------------|
| Appointments | ScheduleDB | SQL (read-only) | appointments, patients, clinics | patient_id, clinic_id | DNS before 2020 unreliable |
| Sales | SalesApp | API (daily extract) | orders, products, customers | customer_id, product_id | Returns not always logged |
| Marketing | HubSpot | CSV export | campaigns, contacts, engagements | contact_id | Duplicates common |

This becomes your analytical playbook!
"""
        )

        st.markdown("---")
        st.markdown("#### 🎯 Advanced Business Question Framework")
        st.markdown(
            """**Moving from basic questions to strategic analytics**

### The Pyramid of Business Questions

**Level 1: Descriptive (What happened?)**
- "What were last month's sales?"
- "How many patients attended appointments?"
- Skills needed: Basic SQL, Excel

**Level 2: Diagnostic (Why did it happen?)**
- "Why did sales decrease in Q3?"
- "What factors drive DNA rates?"
- Skills needed: Analysis, correlation, segmentation

**Level 3: Predictive (What will happen?)**
- "What will Q4 sales be?"
- "Which patients are likely to DNA?"
- Skills needed: Statistical modeling, trends

**Level 4: Prescriptive (What should we do?)**
- "How should we allocate marketing budget?"
- "What interventions will reduce DNAs?"
- Skills needed: Optimization, experimentation

**Your goal: Move up the pyramid!**

---

### Stakeholder Question Types & How to Handle Them

**The Explorer: "Can you just pull some numbers?"**
- **Real need:** They're fishing for insights
- **Your response:** "What decision are you trying to make?"
- **Refine to:** Specific hypothesis to test

**The Validator: "Prove my theory"**
- **Real need:** Confirmation bias alert!
- **Your response:** "Let's test multiple hypotheses"
- **Refine to:** Objective analysis with alternative explanations

**The Firefighter: "URGENT: Why did X happen?"**
- **Real need:** Quick triage
- **Your response:** "Let me check the obvious suspects first"
- **Refine to:** Rapid diagnostic with follow-up plan

**The Strategist: "Help me understand our position"**
- **Real need:** Comprehensive landscape view
- **Your response:** "What dimensions matter most?"
- **Refine to:** Multi-dimensional competitive analysis

**Example Interaction:**

**Stakeholder:** *"Can you tell me if our new product is doing well?"*

**Bad Analyst:** *"Sure, let me pull sales numbers."*

**Good Analyst:**
- "What does 'doing well' mean to you? Revenue target? Market share? Customer adoption?"
- "Compared to what? Previous products? Competitors? Internal forecast?"
- "Over what timeframe? Since launch? Month-over-month? Year-over-year?"
- "For which segments? All customers? New vs existing? Geographic regions?"

**Refined Question:**
*"Has the new product achieved 80% of our Q1 revenue target, and how does adoption compare to our last product launch across customer segments?"*

NOW you can analyze!

---

### Data Literacy: Speaking the Language

**Key Concepts Every Analyst Must Master:**

**1. Metrics vs Dimensions**
- **Metrics** (measures): Numbers you calculate (revenue, count, average)
- **Dimensions** (attributes): Categories you group by (date, region, product)
- Example: "Revenue [metric] by product category [dimension]"

**2. Granularity**
- Level of detail in your data
- Daily vs monthly vs yearly
- Individual transactions vs aggregated summaries
- **Critical**: Match granularity to question!

**3. Time Windows**
- Point-in-time: Snapshot at specific moment
- Period: Across a timeframe
- Rolling: Moving window (last 30 days)
- YTD/MTD: Year/Month to date

**4. Comparison Baselines**
- Previous period: Last month, last quarter
- Same period last year: Seasonal comparison
- Target/benchmark: Goal or industry standard
- Control group: A/B testing reference

**5. Statistical Significance**
- Is the difference real or random variation?
- Sample size matters
- Confidence intervals
- Don't confuse correlation with causation!

**Practical Example:**

**Weak:** "Sales are up 5%"

**Strong:** "Sales increased 5% month-over-month (£52K to £54.6K), exceeding our 3% target. This represents our 3rd consecutive month of growth, driven primarily by the Northeast region (+12%) and Enterprise segment (+18%). The increase is statistically significant (p<0.05, n=1,247 transactions)."

See the difference?

---

### The Data Quality Checklist

**Before ANY analysis, verify:**

**Completeness**
- Are all records present?
- Any missing time periods?
- All sources included?
```sql
-- Check for gaps in daily data
SELECT date, COUNT(*) as record_count
FROM transactions
WHERE date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY date
ORDER BY date;
-- Expect 365 rows for full year
```

**Accuracy**
- Do numbers make sense?
- Any obvious outliers?
- Cross-check with known totals
```sql
-- Sanity check: revenue should match financial reports
SELECT SUM(revenue) as total_revenue
FROM transactions
WHERE date BETWEEN '2024-01-01' AND '2024-03-31';
-- Compare to Q1 financial report
```

**Consistency**
- Same definitions across sources?
- Units consistent? (£ vs pence, % vs decimal)
- Time zones aligned?

**Timeliness**
- How fresh is the data?
- When was it last updated?
- Any known delays?

**Relevance**
- Does this data answer the question?
- Right level of detail?
- Appropriate time period?

**Red Flags:**
- Round numbers (10, 100, 1000) → often defaults or estimates
- Unexpected nulls → data pipeline issues
- Sudden spikes/drops → investigate before reporting!
- Too-perfect patterns → data may be synthetic or flawed

---

### Building Your Analytical Toolkit

**Essential Questions for Every Analysis:**

**1. Define Success**
- What's the ideal outcome?
- How will we measure it?
- What's the threshold?

**2. Identify Variables**
- What factors might influence the outcome?
- Which are controllable?
- Which are external?

**3. Plan Data Collection**
- What data do I need?
- Where does it live?
- How do I access it?

**4. Consider Bias**
- Selection bias: Am I looking at the right population?
- Survivorship bias: Am I only seeing successes?
- Confirmation bias: Am I testing objectively?

**5. Think Through Logic**
- If X increases, what happens to Y?
- What would disprove my hypothesis?
- What alternative explanations exist?

**Example: Analyzing Customer Churn**

**Define Success:** Identify factors predicting churn to reduce it by 20%

**Variables:**
- Tenure (months as customer)
- Engagement (logins/month, features used)
- Support tickets (count, resolution time)
- Payment history (late payments, failed charges)
- Demographics (industry, company size)

**Data Sources:**
- CRM (Salesforce) → customer demographics, tenure
- Product usage logs → engagement metrics
- Support system (Zendesk) → ticket data
- Payment processor (Stripe) → billing history

**Bias Checks:**
- Survivorship: Include both churned AND active customers
- Time: Look at same tenure periods for fair comparison
- Confounders: Control for seasonal effects

**Hypotheses to Test:**
1. Customers with <2 logins/month churn 3x more
2. Unresolved support tickets increase churn by 50%
3. Payment failures predict churn within 30 days
4. First 90 days are critical for retention

NOW you have a testable framework!

"""
        )

        st.markdown("---")
        st.markdown("#### 📊 Data Types & Their Analytical Implications")
        st.markdown(
            """**Not all data is created equal - understanding data types is fundamental**

### Categorical vs Continuous Data

**Categorical (Qualitative)**
- **Nominal**: No inherent order
  - Examples: Product type, region, gender
  - Analysis: Counts, proportions, mode
  - Visualizations: Bar charts, pie charts
  
- **Ordinal**: Has order, but gaps between values aren't equal
  - Examples: Satisfaction ratings (1-5), education level
  - Analysis: Median, percentiles
  - Visualizations: Bar charts (ordered), stacked bars

**Continuous (Quantitative)**
- **Interval**: Equal gaps, no true zero
  - Examples: Temperature (Celsius), dates
  - Analysis: Mean, standard deviation
  - Visualizations: Line charts, histograms
  
- **Ratio**: Equal gaps AND true zero
  - Examples: Revenue, age, distance
  - Analysis: All statistics apply, ratios meaningful
  - Visualizations: All chart types

**Why It Matters:**

Wrong data type = wrong analysis!

```python
# WRONG: Treating zip codes as numbers
average_zip = df['zipcode'].mean()  # Meaningless!

# RIGHT: Treat as categorical
zip_counts = df['zipcode'].value_counts()  # Makes sense!
```

---

### Measures of Central Tendency: When to Use What

**Mean (Average)**
- **When**: Continuous data, symmetric distribution
- **Pros**: Uses all data points
- **Cons**: Sensitive to outliers
- **Example**: Average transaction value

**Median (Middle value)**
- **When**: Skewed distributions, outliers present
- **Pros**: Robust to outliers
- **Cons**: Ignores extreme values
- **Example**: Median household income

**Mode (Most frequent)**
- **When**: Categorical data, finding most common
- **Pros**: Works for any data type
- **Cons**: May not be unique or representative
- **Example**: Most popular product

**Real Example:**

Employee salaries: £25K, £28K, £30K, £32K, £35K, £250K (CEO)

- Mean: £66,667 (misleading!)
- Median: £31,000 (better represents typical salary)
- Mode: None (all unique)

**Choose median** when outliers present!

---

### Variance & Standard Deviation: Understanding Spread

**Why Spread Matters:**

Two datasets can have same mean but very different spreads:
- Dataset A: 48, 49, 50, 51, 52 (tight, predictable)
- Dataset B: 10, 30, 50, 70, 90 (wide, variable)
- Both have mean = 50, but VERY different!

**Standard Deviation (SD):**
- Measures average distance from mean
- **Low SD** → data clustered near mean (consistent)
- **High SD** → data spread out (variable)

**Practical Applications:**

**Quality Control:**
- Product weights: Target 100g ± 2g (SD = 0.67g is good)
- If SD = 5g → quality issues!

**Sales Forecasting:**
- Monthly sales: Mean = £50K, SD = £5K
- Expect 95% of months between £40K-£60K (±2 SD)
- Month with £75K sales → investigate why!

**Customer Behavior:**
- Average purchase: £45, SD = £15
- Customer spending £100 → high-value segment
- Target for premium offers!

---

### Correlation vs Causation: The Most Important Distinction

**Correlation:** Two things change together

**Causation:** One thing CAUSES another to change

**Just because X and Y move together doesn't mean X causes Y!**

**Classic Examples:**

1. **Ice cream sales & drowning deaths**
   - Correlation: Both increase in summer
   - Causation: Neither causes the other!
   - Real cause: Hot weather (confounding variable)

2. **Website traffic & sales**
   - Correlation: Higher traffic → more sales
   - But is it causation? Maybe!
   - Could be: Brand awareness driving both

**Tests for Causation:**

**Bradford Hill Criteria:**
1. **Strength**: Strong correlation?
2. **Consistency**: Observed in multiple studies?
3. **Specificity**: X linked specifically to Y?
4. **Temporality**: X happens before Y?
5. **Gradient**: More X → more Y?
6. **Plausibility**: Makes logical sense?
7. **Coherence**: Fits existing knowledge?
8. **Experiment**: Can we test it (A/B test)?

**Gold Standard: Randomized Controlled Trial (RCT)**
- Control group (no intervention)
- Treatment group (intervention)
- Random assignment
- Measure difference

**Example: Does email marketing increase sales?**

**Correlation Analysis:**
```sql
-- Weeks with more emails sent also have higher sales
SELECT 
    week,
    COUNT(*) as emails_sent,
    SUM(revenue) as total_sales
FROM campaigns
GROUP BY week;
-- Positive correlation, but is it causal?
```

**Causal Test (A/B):**
- Randomly split customers 50/50
- Send emails to Group A only
- Compare sales between groups
- If Group A has 15% higher sales → likely causal!

**Never say "X causes Y" without evidence!**

---

### Segmentation: Finding Patterns in Data

**What is Segmentation?**
Breaking data into meaningful groups to find differences

**Why Segment?**
- Not all customers/products/regions are the same
- Different segments need different strategies
- Averages hide important stories!

**Common Segmentation Approaches:**

**1. Demographic Segmentation**
- Age groups: <25, 25-34, 35-44, 45-54, 55+
- Geography: Region, country, urban/rural
- Industry: Healthcare, finance, retail, etc.

**2. Behavioral Segmentation**
- Purchase frequency: New, occasional, regular, frequent
- Engagement: Active, lapsed, dormant, churned
- Value: High-value, medium, low

**3. RFM Segmentation (Powerful!)**
- **Recency**: When did they last interact?
- **Frequency**: How often do they interact?
- **Monetary**: How much do they spend?

```sql
-- RFM scoring example
WITH rfm AS (
    SELECT 
        customer_id,
        DATEDIFF(day, MAX(order_date), CURRENT_DATE) as recency_days,
        COUNT(*) as frequency,
        SUM(revenue) as monetary
    FROM orders
    WHERE order_date >= DATEADD(year, -1, CURRENT_DATE)
    GROUP BY customer_id
)
SELECT 
    customer_id,
    CASE 
        WHEN recency_days <= 30 THEN 'Very Recent'
        WHEN recency_days <= 90 THEN 'Recent'
        WHEN recency_days <= 180 THEN 'Lapsed'
        ELSE 'Inactive'
    END as recency_segment,
    CASE 
        WHEN frequency >= 10 THEN 'Frequent'
        WHEN frequency >= 5 THEN 'Regular'
        ELSE 'Occasional'
    END as frequency_segment,
    CASE 
        WHEN monetary >= 1000 THEN 'High Value'
        WHEN monetary >= 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END as monetary_segment
FROM rfm;
```

**4. Cohort Analysis**
- Group by shared characteristic (e.g., signup month)
- Track behavior over time
- Identify trends and lifecycle patterns

**Example: Monthly Cohort Retention**

| Signup Month | Month 1 | Month 2 | Month 3 | Month 6 | Month 12 |
|--------------|---------|---------|---------|---------|----------|
| Jan 2023 | 100% | 85% | 78% | 65% | 52% |
| Feb 2023 | 100% | 88% | 82% | 70% | ? |
| Mar 2023 | 100% | 90% | 85% | ? | ? |

**Insights:**
- Feb & Mar cohorts have better retention → what changed?
- 6-month retention critical milestone
- Target: Improve Month 2-3 retention

---

### Time Series Analysis Basics

**What is Time Series Data?**
Data collected at regular intervals over time

**Examples:**
- Daily sales
- Monthly website traffic
- Quarterly revenue
- Hourly server loads

**Key Concepts:**

**1. Trend**
- Long-term increase or decrease
- "Are sales growing overall?"
- Calculate: Moving average, linear regression

**2. Seasonality**
- Regular, predictable patterns
- "Do we see peaks in December?"
- Examples: Holiday shopping, summer tourism

**3. Cyclical Patterns**
- Longer-term fluctuations (not fixed periods)
- Examples: Economic cycles, market trends

**4. Random Variation (Noise)**
- Unpredictable fluctuations
- Need to separate signal from noise

**Practical Time Series Analysis:**

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load daily sales data
df = pd.read_csv('sales.csv', parse_dates=['date'])
df = df.set_index('date')

# Calculate 7-day moving average (smooth out noise)
df['sales_ma7'] = df['sales'].rolling(window=7).mean()

# Calculate year-over-year growth
df['sales_yoy'] = df['sales'].pct_change(periods=365) * 100

# Identify day-of-week patterns
df['dow'] = df.index.dayofweek
dow_avg = df.groupby('dow')['sales'].mean()
# Monday=0, Sunday=6

# Visualize
plt.figure(figsize=(12, 6))
plt.plot(df['sales'], alpha=0.3, label='Daily Sales')
plt.plot(df['sales_ma7'], label='7-Day MA (Trend)')
plt.legend()
plt.title('Sales Trend Analysis')
plt.show()
```

**Common Time Series Mistakes:**

❌ Comparing absolute numbers across different time periods
✅ Use percentage change or indexed values

❌ Ignoring seasonality
✅ Compare same period year-over-year

❌ Reacting to every fluctuation
✅ Focus on trends, not daily noise

❌ Not accounting for external events
✅ Note holidays, marketing campaigns, etc.

**Example Analysis:**

"Website traffic dropped 15% this week!"

**Good Analyst Checks:**
- Is it a holiday week? (expected seasonality)
- What was traffic same week last year?
- Is the trend (moving average) still upward?
- Any known technical issues or marketing changes?

**Conclusion:** "Traffic is down 15% week-over-year, and the 30-day moving average shows continued growth. No action needed."

"""
        )

        st.markdown("---")
        st.markdown("## 🔬 HANDS-ON LABS - Unit 1")
        st.markdown(
            """**Practical exercises to master business questions and data foundations**

### LAB 1: Business Question Transformation Workshop

**Objective:** Transform 10 vague business requests into SMART analytical questions

**Scenario:** You're a new Data Analyst at MediCare Hospital Trust

**Your Task:** Refine these stakeholder requests into actionable questions

**Request 1: "Staff morale seems low"**

**Your Analysis Plan:**
```
1. Define "morale" measurably:
   - Staff survey scores?
   - Absence rates?
   - Turnover rates?
   - Engagement metrics?

2. Identify baseline:
   - Compared to what period?
   - Which departments?
   - What's the target benchmark?

3. Refined Question:
   "Has staff absence rate increased in Q3 2024 vs Q3 2023? 
   Analyze by department and staff level, identifying departments 
   exceeding 5% absence rate (trust target)."

4. Data Needed:
   - HR system: absence records, staff demographics
   - Timeframe: Q3 2023 vs Q3 2024
   - Segmentation: Department, role, tenure

5. Success Criteria:
   - Identify which departments have issues
   - Quantify magnitude of problem
   - Enable targeted interventions
```

**Request 2: "Our website isn't working properly"**

**Your Turn - Complete This Analysis:**
```
1. Define "not working properly":
   - [ ] Load time issues?
   - [ ] Error rates?
   - [ ] Conversion drops?
   - [ ] User complaints?

2. Baseline comparison:
   - [ ] Current vs last month?
   - [ ] Before/after recent deployment?
   - [ ] Compared to benchmarks?

3. Your Refined Question:
   [Write your refined question here]

4. Data Sources Needed:
   - [ ] Google Analytics: _________________
   - [ ] Server logs: _________________
   - [ ] Error tracking: _________________

5. Metrics to Track:
   - [ ] ___________________________
   - [ ] ___________________________
   - [ ] ___________________________
```

**Request 3-10: Practice These Yourself**

3. "Marketing isn't generating leads"
4. "Patients are waiting too long"
5. "Our competitors are winning"
6. "The new system is confusing"
7. "Costs are out of control"
8. "Sales are disappointing"
9. "Customers aren't happy"
10. "We need to grow faster"

**Deliverable:** Document showing:
- Original vague request
- Your clarifying questions
- Refined SMART question
- Data sources identified
- Analysis approach
- Expected insights

**Time:** 2-3 hours  
**Tools:** Word/Google Docs

---

### LAB 2: Data Source Mapping Exercise

**Objective:** Map business questions to actual data sources in a real organization

**Scenario:** You're joining RetailCo as Junior Data Analyst. They have:
- **E-commerce Platform**: Shopify (orders, products, customers)
- **CRM**: HubSpot (leads, contacts, deals)
- **Marketing**: Google Ads, Facebook Ads, Mailchimp
- **Support**: Zendesk (tickets, responses, ratings)
- **Financial**: Xero (invoicing, expenses, revenue)
- **Data Warehouse**: Snowflake (central repository)

**Your Task:** Map 5 business questions to data sources

**Question 1: "What's our customer acquisition cost by channel?"**

**Data Mapping:**
```
Required Data Points:
1. Marketing spend by channel
   - Source: Google Ads API → ad_spend table
   - Source: Facebook Ads → campaign_costs table
   - Source: Mailchimp → email_campaign_costs
   
2. New customers acquired
   - Source: Shopify → customers table
   - Filter: first_order_date
   - Group by: utm_source, utm_medium

3. Attribution logic
   - Source: Google Analytics → user_acquisition
   - Join key: customer_id

Calculation:
CAC = Total Marketing Spend / New Customers Acquired

SQL Approach:
SELECT 
    ga.acquisition_channel,
    SUM(ad_spend) as total_spend,
    COUNT(DISTINCT c.customer_id) as new_customers,
    SUM(ad_spend) / COUNT(DISTINCT c.customer_id) as cac
FROM google_ads ga
LEFT JOIN customers c 
    ON ga.utm_source = c.acquisition_source
WHERE c.first_order_date >= '2024-01-01'
GROUP BY ga.acquisition_channel
ORDER BY cac ASC;

Data Quality Checks:
- Verify all channels included
- Check for unattributed customers
- Validate spend totals against finance
```

**Question 2: "Which products have highest return rate?"**

**Your Turn - Complete This Mapping:**
```
Required Data Points:
1. Total orders per product
   - Source: _________________
   - Table/Field: _________________

2. Return requests
   - Source: _________________
   - Join on: _________________

3. Return reasons (bonus)
   - Source: _________________

Calculation Formula:
Return Rate = _________________

SQL Skeleton:
SELECT 
    p.product_name,
    COUNT(o.order_id) as total_orders,
    COUNT(r.return_id) as returns,
    _________________ as return_rate_pct
FROM _________________ p
LEFT JOIN _________________ o ON _________________
LEFT JOIN _________________ r ON _________________
GROUP BY _________________
HAVING total_orders >= 10  -- minimum threshold
ORDER BY return_rate_pct DESC;
```

**Questions 3-5: Practice These**

3. "What's our average customer lifetime value?"
4. "How quickly do we respond to support tickets?"
5. "What % of leads convert to customers?"

**Deliverable:** 
- Data source inventory spreadsheet
- SQL query drafts for each question
- Data quality concerns identified
- Access requirements documented

**Time:** 3-4 hours  
**Tools:** Excel, DB visualization tool, SQL editor

---

### LAB 3: Data Quality Audit

**Objective:** Assess data quality and identify issues before analysis

**Scenario:** You've been asked to analyze Q3 sales performance, but first you need to audit the data quality.

**Dataset:** `sales_transactions_q3_2024.csv` (sample provided)

**Your Audit Checklist:**

**1. Completeness Check**
```sql
-- Check for missing values
SELECT 
    COUNT(*) as total_records,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) as missing_order_id,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as missing_customer,
    SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) as missing_date,
    SUM(CASE WHEN revenue IS NULL THEN 1 ELSE 0 END) as missing_revenue,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) as missing_product
FROM sales_transactions;

-- Check for complete months
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as transaction_count
FROM sales_transactions
WHERE order_date BETWEEN '2024-07-01' AND '2024-09-30'
GROUP BY month
ORDER BY month;
-- Expect 3 rows (July, August, September)
```

**2. Accuracy Check**
```sql
-- Identify suspicious values
SELECT 
    order_id,
    revenue,
    quantity,
    unit_price,
    revenue - (quantity * unit_price) as revenue_discrepancy
FROM sales_transactions
WHERE ABS(revenue - (quantity * unit_price)) > 0.01;

-- Find outliers (orders >3 standard deviations from mean)
WITH stats AS (
    SELECT 
        AVG(revenue) as mean_revenue,
        STDDEV(revenue) as stddev_revenue
    FROM sales_transactions
)
SELECT 
    t.order_id,
    t.revenue,
    (t.revenue - s.mean_revenue) / s.stddev_revenue as z_score
FROM sales_transactions t, stats s
WHERE ABS((t.revenue - s.mean_revenue) / s.stddev_revenue) > 3
ORDER BY z_score DESC;
```

**3. Consistency Check**
```python
import pandas as pd

# Load data
df = pd.read_csv('sales_transactions_q3_2024.csv')

# Check data types
print("Data Types:")
print(df.dtypes)

# Check for inconsistent formats
print("\nDate Format Issues:")
print(df[pd.to_datetime(df['order_date'], errors='coerce').isna()]['order_date'].value_counts())

# Check for duplicate orders
print("\nDuplicate Orders:")
duplicates = df[df.duplicated(subset=['order_id'], keep=False)]
print(f"Found {len(duplicates)} duplicate records")

# Check category consistency
print("\nProduct Categories (check for typos):")
print(df['product_category'].value_counts())
# Look for: "Electronics" vs "electronics", "Health & Beauty" vs "Health&Beauty"
```

**4. Timeliness Check**
```sql
-- Check data freshness
SELECT 
    MAX(order_date) as latest_order,
    DATEDIFF(day, MAX(order_date), CURRENT_DATE) as days_old
FROM sales_transactions;

-- Should be <2 days old for near-real-time reporting
```

**5. Validity Check**
```sql
-- Business rule violations
SELECT 
    'Negative Revenue' as issue,
    COUNT(*) as count
FROM sales_transactions
WHERE revenue < 0

UNION ALL

SELECT 
    'Zero Quantity' as issue,
    COUNT(*) as count
FROM sales_transactions
WHERE quantity = 0

UNION ALL

SELECT 
    'Future Dates' as issue,
    COUNT(*) as count
FROM sales_transactions
WHERE order_date > CURRENT_DATE;
```

**Your Deliverable:**
Create a **Data Quality Report** with:

1. **Executive Summary**
   - Overall data quality score (0-100)
   - Critical issues found
   - Recommendation: Proceed / Fix First / Do Not Use

2. **Detailed Findings**
   - Completeness: X% complete
   - Accuracy: Y issues found
   - Consistency: Z format problems
   - Timeliness: Updated N days ago
   - Validity: M business rule violations

3. **Issues Table**
   | Issue Type | Count | Severity | Action Required |
   |------------|-------|----------|----------------|
   | Missing customer IDs | 47 | High | Investigate & backfill |
   | Negative revenue | 3 | Critical | Correct immediately |
   | Duplicate orders | 12 | Medium | De-duplicate before analysis |

4. **Recommendations**
   - Can we proceed with analysis? (Yes/No/With caveats)
   - What needs to be fixed?
   - Who needs to be contacted?
   - Timeline for resolution?

**Time:** 2-3 hours  
**Tools:** SQL, Python/Excel  
**Deliverable:** PowerPoint/Word report

---

### MINI PROJECT 1: End-to-End Question → Insight

**Objective:** Complete a full analytical cycle from question to recommendation

**Scenario:** You're analyzing DNA (Did Not Attend) rates for OutpatientClinic

**Phase 1: Question Refinement (30 mins)**

**Initial Request:** "Can you look into our DNA problem?"

Your refined questions:
1. What's the current DNA rate and how does it compare to target/historical?
2. Which clinics/specialties have highest DNA rates?
3. Are there patient demographic patterns?
4. What's the financial impact?
5. What factors correlate with DNAs?

**Phase 2: Data Collection (1 hour)**

**Data Sources:**
- Appointments database
- Patient demographics
- Clinic information
- Historical benchmarks

**SQL Query:**
```sql
-- Comprehensive DNA analysis
WITH appointment_summary AS (
    SELECT 
        a.appointment_id,
        a.appointment_date,
        a.appointment_time,
        a.clinic_id,
        c.clinic_name,
        c.specialty,
        a.patient_id,
        p.age,
        p.gender,
        p.postcode_sector,
        p.deprivation_index,
        a.appointment_type,
        a.appointment_status,
        CASE WHEN a.appointment_status = 'DNA' THEN 1 ELSE 0 END as is_dna,
        c.appointment_value_gbp
    FROM appointments a
    JOIN clinics c ON a.clinic_id = c.clinic_id
    JOIN patients p ON a.patient_id = p.patient_id
    WHERE a.appointment_date BETWEEN '2024-01-01' AND '2024-09-30'
)
SELECT 
    specialty,
    COUNT(*) as total_appointments,
    SUM(is_dna) as dna_count,
    ROUND(100.0 * SUM(is_dna) / COUNT(*), 2) as dna_rate_pct,
    SUM(CASE WHEN is_dna = 1 THEN appointment_value_gbp ELSE 0 END) as lost_revenue_gbp
FROM appointment_summary
GROUP BY specialty
ORDER BY dna_rate_pct DESC;
```

**Phase 3: Analysis (2 hours)**

**Your Tasks:**
1. Calculate overall DNA rate and trend
2. Identify highest-risk segments
3. Perform statistical tests
4. Quantify financial impact
5. Compare to benchmarks

**Python Analysis:**
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load data
df = pd.read_csv('appointments_analysis.csv')

# 1. Overall DNA rate
overall_dna_rate = df['is_dna'].mean() * 100
print(f"Overall DNA Rate: {overall_dna_rate:.2f}%")

# 2. DNA rate by specialty
specialty_dna = df.groupby('specialty').agg({
    'appointment_id': 'count',
    'is_dna': ['sum', 'mean']
}).round(3)
specialty_dna.columns = ['total_appts', 'dna_count', 'dna_rate']
specialty_dna['dna_rate_pct'] = specialty_dna['dna_rate'] * 100
print(specialty_dna.sort_values('dna_rate_pct', ascending=False))

# 3. Statistical significance
# Compare Dermatology vs other specialties
derm_dna_rate = df[df['specialty'] == 'Dermatology']['is_dna'].mean()
other_dna_rate = df[df['specialty'] != 'Dermatology']['is_dna'].mean()

# Chi-square test
from scipy.stats import chi2_contingency
contingency_table = pd.crosstab(
    df['specialty'] == 'Dermatology',
    df['is_dna']
)
chi2, p_value, dof, expected = chi2_contingency(contingency_table)
print(f"Chi-square p-value: {p_value:.4f}")
if p_value < 0.05:
    print("Difference is statistically significant!")

# 4. Visualization
plt.figure(figsize=(12, 6))
sns.barplot(data=specialty_dna.reset_index(), 
            x='specialty', y='dna_rate_pct')
plt.xticks(rotation=45, ha='right')
plt.title('DNA Rate by Specialty')
plt.ylabel('DNA Rate (%)')
plt.axhline(y=overall_dna_rate, color='r', linestyle='--', label='Trust Average')
plt.legend()
plt.tight_layout()
plt.savefig('dna_by_specialty.png')
plt.show()

# 5. Financial impact
total_lost_revenue = df[df['is_dna'] == 1]['appointment_value_gbp'].sum()
print(f"Total Lost Revenue: £{total_lost_revenue:,.0f}")
```

**Phase 4: Insights & Recommendations (1 hour)**

**Your Report Structure:**

**Executive Summary:**
- DNA rate is 14.5%, up from 12% last year
- Dermatology has highest rate at 18.2% (statistically significant, p<0.001)
- Lost revenue: £42,000 in 9 months (£56K annual run-rate)
- Recommend: Implement SMS reminders for Dermatology + new patients

**Key Findings:**
1. Dermatology DNA rate (18.2%) significantly higher than average (14.5%)
2. New patients DNA 2.3x more than established patients
3. Afternoon appointments have 1.4x higher DNA rate
4. No significant demographic pattern by age/gender

**Recommendations:**
1. **Immediate (0-30 days):** 
   - SMS reminder system for Dermatology
   - Target new patients specifically
   - Estimated cost: £200/month
   - Projected DNA reduction: 30-40%
   - ROI: £2,500/month saved

2. **Short-term (1-3 months):**
   - Analyze root causes via patient survey
   - Consider scheduling changes (fewer afternoon slots)

3. **Long-term (3-6 months):**
   - Online booking with automatic reminders
   - Waitlist management system

**Next Steps:**
- Present findings to clinic managers
- Get approval for SMS pilot
- Set up tracking dashboard
- Review results after 3 months

**Deliverable:** 10-slide PowerPoint presentation

**Time:** 4-5 hours total  
**Tools:** SQL, Python/Excel, PowerPoint

---

### Practice Dataset & Resources

**Download Practice Files:**
- `hospital_appointments.csv` - 10,000 appointments
- `patient_demographics.csv` - Patient details
- `clinic_reference.csv` - Clinic information
- `data_dictionary.pdf` - Field definitions

**Success Criteria:**
- ✅ Transformed vague questions into SMART questions
- ✅ Mapped business questions to data sources
- ✅ Conducted thorough data quality audit
- ✅ Completed end-to-end analysis project
- ✅ Delivered actionable recommendations

---

## 📝 50+ PRACTICE PROBLEMS - Unit 1

### Question Transformation Practice (20 Problems)

**Problem 1:** "Our website is slow."
**Your Analysis:**
- Slow compared to what benchmark?
- Which pages specifically?
- At what times of day?
- For which user segments?
**SMART Question:** "What is the P95 page load time for our checkout flow during peak hours (6-9pm) compared to our 2-second target?"

**Problem 2:** "Customers are complaining."
**Your Analysis:**
- What percentage of customers?
- About what specifically?
- Through which channels?
- Has this increased recently?
**SMART Question:** "What is our NPS score by product category in Q4 2024 vs Q3 2024, and what are the top 3 complaint themes?"

**Problem 3:** "Marketing spend is too high."
**Your Analysis:**
- Too high relative to what?
- Which channels/campaigns?
- What's the ROI comparison?
- Against which targets?
**SMART Question:** "What is the customer acquisition cost (CAC) by channel vs our £50 target, and which channels have CAC > £75?"

**Problem 4:** "We need more customers."
**Your Analysis:**
- How many more specifically?
- In which segments/markets?
- By when?
- Through which strategies?
**SMART Question:** "How can we increase new customer acquisition from 1,000 to 1,500 per month in the UK market by Q2 2025?"

**Problem 5:** "Sales are down."
**SMART Question:** "What is the month-over-month sales change by product category and region for October 2024, and what factors correlate with declines?"

**Problem 6:** "Our app keeps crashing."
**SMART Question:** "What is the crash rate by app version and device type for iOS users in the past 30 days, and which user actions trigger crashes?"

**Problem 7:** "Staff aren't productive."
**SMART Question:** "What is the average cases resolved per agent per day by team in Q4 vs Q3, and how does this compare to our target of 15 cases/day?"

**Problem 8:** "Inventory is always wrong."
**SMART Question:** "What is the inventory accuracy rate (physical vs system) by warehouse and product category, and which SKUs have >10% variance?"

**Problem 9:** "Our promotions don't work."
**SMART Question:** "What is the incremental revenue lift and ROI for promotions run in Q4, by promotion type and product category?"

**Problem 10:** "Patients wait too long."
**SMART Question:** "What is the median wait time from arrival to consultation by clinic and day of week vs our 60-minute target, and which clinics exceed 90 minutes?"

**Problem 11:** "Social media engagement is low."
**SMART Question:** "What is our engagement rate (likes+comments/followers) by platform and content type vs industry benchmark of 3%?"

**Problem 12:** "The new feature isn't being used."
**SMART Question:** "What is the adoption rate (% of active users who used feature at least once) in the 30 days post-launch by user cohort?"

**Problem 13:** "Shipping costs are killing us."
**SMART Question:** "What is the average shipping cost per order by carrier and delivery speed vs our £5 target, and where can we optimize?"

**Problem 14:** "Email campaigns get ignored."
**SMART Question:** "What is the open rate and click-through rate by email campaign type and send time vs our benchmarks (25% open, 3% CTR)?"

**Problem 15:** "Our competitors are winning."
**SMART Question:** "What is our market share by product segment vs top 3 competitors in Q4, and which segments have we lost share in?"

**Problem 16:** "Customer lifetime value is dropping."
**SMART Question:** "What is the 12-month CLV by acquisition channel and cohort, comparing 2024 vs 2023 cohorts?"

**Problem 17:** "The website redesign failed."
**SMART Question:** "What is the conversion rate and bounce rate pre vs post-redesign for our top 5 landing pages?"

**Problem 18:** "Support tickets are overwhelming."
**SMART Question:** "What is the daily ticket volume by category and priority, and which issues have >100 tickets/week?"

**Problem 19:** "Our prices aren't competitive."
**SMART Question:** "What is our price index vs 3 main competitors for our top 20 SKUs, and where are we >10% more expensive?"

**Problem 20:** "Training programs aren't effective."
**SMART Question:** "What is the performance improvement (metric: sales/accuracy/efficiency) 30 and 90 days post-training vs control group?"

---

### Data Source Mapping Practice (15 Problems)

**Problem 21:** Business Question: "Which products have the highest profit margin?"
**Data Sources Needed:**
- Product sales data (units sold, revenue)
- Cost of goods sold (COGS) by product
- Operating expenses allocated to products
**Calculations:** `Profit Margin = (Revenue - COGS - Operating Expenses) / Revenue * 100`
**Potential Issues:** Cost allocation methodology, promotional pricing, returns

**Problem 22:** "What's our customer churn rate by segment?"
**Data Sources:**
- Customer subscription data
- Cancellation/churn events
- Customer segments/demographics
**Calculations:** `Monthly Churn = Customers Lost / Customers at Start * 100`

**Problem 23:** "Is our advertising driving sales?"
**Data Sources:**
- Advertising spend by channel/campaign
- Sales/revenue data with attribution
- Website traffic sources
**Calculations:** `ROAS = Revenue from Ads / Ad Spend`

**Problem 24:** "Which employees are flight risks?"
**Data Sources:**
- Employee tenure and role
- Performance reviews
- Salary vs market rate
- Engagement survey scores
**Analysis:** Predictive model using historical exit patterns

**Problem 25:** "Should we expand to a new market?"
**Data Sources:**
- Target market demographics
- Competitor presence and market share
- Economic indicators (GDP, purchasing power)
- Infrastructure and logistics costs
**Analysis:** Market sizing, TAM/SAM/SOM calculation

**Problem 26-35:** [Similar structured problems for:]
- Supply chain optimization
- Pricing strategy analysis
- Customer satisfaction drivers
- A/B test evaluation
- Fraud detection
- Demand forecasting
- Resource allocation
- Quality control
- Risk assessment
- Predictive maintenance

---

### Real-World Industry Case Studies (10 Detailed Scenarios)

**CASE STUDY 1: E-Commerce - Cart Abandonment Analysis**

**Context:** Online retailer with 68% cart abandonment, losing £250K monthly

**Your Assignment:**
1. **Data Available:**
   - 50,000 session logs (add to cart events)
   - User demographics (age, location, device)
   - Product information (category, price)
   - Checkout flow events (step-by-step)

2. **Analysis Steps:**
```sql
-- Step 1: Calculate overall abandonment rate
SELECT 
  COUNT(DISTINCT CASE WHEN added_to_cart = 1 THEN session_id END) as cart_sessions,
  COUNT(DISTINCT CASE WHEN purchase_complete = 1 THEN session_id END) as completed,
  (1 - COUNT(DISTINCT CASE WHEN purchase_complete = 1 THEN session_id END) * 1.0 / 
   COUNT(DISTINCT CASE WHEN added_to_cart = 1 THEN session_id END)) * 100 as abandonment_rate
FROM sessions
WHERE date >= '2024-10-01';

-- Step 2: Segment by device type
SELECT 
  device_type,
  COUNT(*) as sessions,
  AVG(CASE WHEN purchase_complete = 1 THEN 1 ELSE 0 END) as completion_rate,
  (1 - AVG(CASE WHEN purchase_complete = 1 THEN 1 ELSE 0 END)) * 100 as abandonment_rate
FROM sessions
WHERE added_to_cart = 1
GROUP BY device_type
ORDER BY abandonment_rate DESC;

-- Step 3: Identify drop-off points
SELECT 
  checkout_step,
  COUNT(*) as users_reached,
  COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sessions WHERE checkout_step >= 1) as pct_reached,
  COUNT(CASE WHEN completed_next_step = 0 THEN 1 END) * 100.0 / COUNT(*) as drop_off_rate
FROM checkout_events
GROUP BY checkout_step
ORDER BY checkout_step;
```

3. **Key Findings:**
   - Mobile abandonment 75% vs desktop 55%
   - Biggest drop-off at shipping cost reveal (step 3)
   - Weekend abandonment 15% higher than weekday
   - Electronics category worst at 72%

4. **Recommendations:**
   - Mobile checkout optimization (simplify 5 steps to 3)
   - Show shipping cost earlier in flow
   - Weekend-specific cart recovery emails
   - A/B test simplified checkout

5. **Expected Impact:**
   - 12% reduction in abandonment
   - £300K annual revenue recovery
   - Improved user experience scores

---

**CASE STUDY 2: Healthcare - Emergency Department Wait Times**

**Context:** Hospital ED with 4-hour target being missed 40% of the time

**Data Available:**
- 25,000 ED visits over 6 months
- Arrival timestamps, triage codes, bed allocation times
- Discharge times, department transfers
- Staffing levels by hour/day

**Analysis Framework:**
```sql
-- Calculate wait time metrics
WITH wait_times AS (
  SELECT 
    visit_id,
    arrival_time,
    first_assessment_time,
    discharge_time,
    TIMESTAMPDIFF(MINUTE, arrival_time, first_assessment_time) as wait_to_assessment,
    TIMESTAMPDIFF(MINUTE, arrival_time, discharge_time) as total_time,
    triage_code,
    HOUR(arrival_time) as arrival_hour,
    DAYNAME(arrival_time) as day_of_week
  FROM ed_visits
  WHERE discharge_time IS NOT NULL
)
SELECT 
  day_of_week,
  arrival_hour,
  COUNT(*) as visits,
  AVG(wait_to_assessment) as avg_wait_minutes,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY wait_to_assessment) as median_wait,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY wait_to_assessment) as p95_wait,
  SUM(CASE WHEN total_time > 240 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as pct_over_4hrs
FROM wait_times
GROUP BY day_of_week, arrival_hour
HAVING COUNT(*) > 50
ORDER BY pct_over_4hrs DESC;
```

**Findings:**
- Peak hours 10am-2pm and 6pm-10pm account for 45% of breaches
- Monday and Friday worst days (48% breach rate)
- Triage code 3 patients wait longest (avg 127 mins)
- Correlation between staffing gaps and wait times (r=0.72)

**Recommendations:**
1. Shift allocation: +2 nurses during peak hours
2. Fast-track pathway for triage 4-5 patients
3. Monday/Friday surge capacity planning
4. Real-time dashboard alerting when wait >90 mins

**ROI:** £850K annual savings from avoided breaches

---

**CASE STUDY 3: SaaS - Customer Churn Prediction**

**Context:** B2B SaaS company with 8% monthly churn, need to identify at-risk accounts

**Data & Analysis:**
```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load customer data
df = pd.read_csv('customer_usage.csv')

# Feature engineering
df['days_since_last_login'] = (pd.Timestamp.now() - df['last_login']).dt.days
df['feature_adoption_score'] = df[['feature_1', 'feature_2', 'feature_3']].sum(axis=1)
df['support_tickets_per_month'] = df['support_tickets'] / df['tenure_months']
df['payment_issues'] = (df['failed_payments'] > 0).astype(int)

# Predictive features
features = ['days_since_last_login', 'feature_adoption_score', 'support_tickets_per_month', 
            'payment_issues', 'user_count', 'contract_value', 'tenure_months']

# Train model
X = df[features]
y = df['churned_next_month']
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Feature importance
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance)
```

**Results:**
Top churn indicators:
1. Days since last login (28% importance)
2. Feature adoption score (22%)
3. Support tickets (18%)
4. Payment issues (15%)

**Intervention Strategy:**
- Customers inactive >14 days → Automated check-in email
- Low adoption score → CSM outreach + training
- High support tickets → Escalate to technical account manager
- Payment issues → Billing team intervention

**Impact:** Reduced churn from 8% to 5.5% (saving £420K annually)

---

**CASE STUDIES 4-10:** [Detailed scenarios for:]
- Retail inventory optimization
- Marketing campaign attribution
- Pricing optimization model
- Quality control analysis
- Workforce planning
- Financial fraud detection
- Supply chain disruption analysis

Each with:
- Business context
- Data available
- SQL/Python analysis code
- Key findings
- Recommendations
- Expected ROI/impact

---

### Advanced Questioning Techniques

**The "5 Whys" Method for Root Cause Analysis:**

**Problem:** "Sales are down 15% this month"

**Why #1:** Why are sales down?
**Answer:** Fewer orders from existing customers

**Why #2:** Why are customers ordering less?
**Answer:** Order frequency dropped from 2x/month to 1x/month

**Why #3:** Why did order frequency drop?
**Answer:** New competitors offering faster delivery

**Why #4:** Why does faster delivery matter to our customers?
**Answer:** They need supplies urgently for their operations

**Why #5:** Why can't we match delivery speed?
**Answer:** Our warehouse is single-location vs competitors' distributed network

**Root Cause:** Geographic constraint on delivery speed
**Solution:** Open regional distribution centers or partner with 3PL

---

**The "What If" Scenario Planning:**

**Current Question:** "Should we expand to Germany?"

**Expand with "What If":**
- What if demand is 50% lower than forecast?
- What if logistics costs are 30% higher?
- What if it takes 6 months longer to break even?
- What if a major competitor enters simultaneously?
- What if regulatory requirements change?

**Creates Robust Analysis:** Best case, base case, worst case scenarios with contingency plans

---

### Data Quality Red Flags Checklist

When auditing data, watch for:

**Completeness Issues:**
- [ ] Missing values >10% in critical fields
- [ ] Entire date ranges absent
- [ ] Null values in required fields
- [ ] Incomplete records (partial information)

**Accuracy Issues:**
- [ ] Values outside possible range (age: 150, price: negative)
- [ ] Inconsistent units (mixing $ and £)
- [ ] Mismatched data types (dates stored as text)
- [ ] Calculation errors in derived fields

**Consistency Issues:**
- [ ] Different spellings ("UK" vs "United Kingdom")
- [ ] Duplicate records with conflicting values
- [ ] Related tables don't match (orphaned records)
- [ ] Time series breaks or gaps

**Timeliness Issues:**
- [ ] Data older than expected (stale)
- [ ] Update frequency doesn't match requirement
- [ ] Delayed by hours/days
- [ ] Historical backfill incomplete

**Validity Issues:**
- [ ] Invalid codes/categories
- [ ] Referential integrity broken
- [ ] Business rules violated
- [ ] Logical inconsistencies

**For Each Issue Found:**
1. Document severity (Critical/High/Medium/Low)
2. Quantify impact (% of records affected)
3. Identify root cause
4. Propose fix
5. Assign owner

---

"""
        )
    elif unit_number == 2:
        st.markdown("#### 📘 Why Spreadsheets Still Matter (And Always Will)")
        st.markdown(
            """Despite the rise of Python, SQL, and advanced BI tools, **spreadsheets remain 
the most widely used data analysis tool in business**. Why?

**Universal Accessibility:**
- Everyone has Excel or Google Sheets
- No installation, no IT approval needed
- Non-technical stakeholders can open and understand them
- Quick ad-hoc analysis without waiting for data team

**Real-World Reality:**
- 90% of businesses run on spreadsheets
- Financial models, budgets, forecasts → all in Excel
- Small to medium datasets (< 1M rows) → spreadsheets are fastest
- Many data sources export to CSV by default

**Your Role as an Analyst:**

You need to be EXCELLENT at spreadsheets because:
1. Stakeholders will send you data in Excel
2. You'll need to quickly clean and explore data
3. Many of your outputs will be Excel deliverables
4. It's the common language of business

**This unit treats spreadsheets as a SERIOUS analytical tool**, not just a calculator.

**What Makes Someone "Excel-Proficient" vs "Excel Expert"?**

| Skill Level | What They Can Do | Time to Complete Task |
|-------------|------------------|---------------------|
| **Basic User** | Enter data, basic SUM, simple charts | Manual work, error-prone, 2 hours |
| **Proficient Analyst** | Clean data, VLOOKUP, Pivot Tables, conditional logic | Semi-automated, 30 minutes |
| **Excel Expert** | Complex nested formulas, Power Query, dynamic dashboards | Fully automated, 5 minutes + reusable |

**Your goal:** Reach "Proficient Analyst" level (minimum for job-readiness)

**Common Analyst Tasks You'll Master:**

1. **Data Cleaning** (40% of your Excel time)
   - Remove duplicates
   - Fix inconsistent formats
   - Handle missing values
   - Standardize text (proper case, trim spaces)

2. **Data Transformation** (30%)
   - Lookups (joining data from multiple sheets)
   - Calculations (formulas across rows/columns)
   - Aggregations (summing, averaging, counting)

3. **Analysis & Visualization** (20%)
   - Pivot tables for summarization
   - Charts for communication
   - Conditional formatting for patterns

4. **Delivery** (10%)
   - Format for stakeholder consumption
   - Add context and annotations
   - Ensure reproducibility
"""
        )

        st.markdown("#### 🧹 Data Cleaning in Excel: From Messy to Analysis-Ready")
        st.markdown(
            """**The #1 Rule of Data Analysis:** Garbage in = Garbage out

Most data you receive will be MESSY. You must clean it before analysis.

**Common Data Quality Issues (You'll See These Daily):**

**1. Duplicates**

**The Problem:**
```
| Customer ID | Name      |
|-------------|-----------|
| 001         | John Doe  |
| 001         | John Doe  |  ← Duplicate
| 002         | Jane Smith|
```

**The Fix:**
- Excel: Data → Remove Duplicates
- Google Sheets: Data → Data cleanup → Remove duplicates
- CHECK FIRST: Are they true duplicates or legitimate repeat entries?

**Best Practice:** Always keep original data, create "cleaned" version

---

**2. Inconsistent Formatting**

**The Problem:**
```
| Date       | Amount  |
|------------|---------|
| 01/05/2024 | £1,234  |
| 5-Jan-2024 | 1234    |  ← Mixed formats
| 2024-01-05 | $1,234  |
```

**The Fix:**
- Dates: Use `TEXT(date, "YYYY-MM-DD")` to standardize
- Currency: Use `VALUE()` to strip symbols, format cells consistently
- Formula: `=TEXT(A2,"YYYY-MM-DD")` converts any date to standard format

---

**3. Extra Spaces (The Silent Killer)**

**The Problem:**
```
"John Doe"   ← Has trailing spaces, won't match "John Doe"
" Jane Smith" ← Leading space
```

These look the same but VLOOKUP will fail!

**The Fix:**
```excel
=TRIM(A2)  ← Removes leading, trailing, and extra internal spaces
```

**Always TRIM text data before analysis!**

---

**4. Inconsistent Capitalization**

**The Problem:**
```
| Product    |
|------------|
| Widget     |
| widget     |  ← Won't group together in Pivot Table
| WIDGET     |
```

**The Fix:**
```excel
=PROPER(A2)  ← Widget (capitalizes first letter of each word)
=UPPER(A2)   ← WIDGET (all caps)
=LOWER(A2)   ← widget (all lowercase)
```

---

**5. Merged Cells (Your Enemy)**

**The Problem:**
Report-style formatting with merged cells breaks data analysis

```
[Merged Cell: Region: North]
Sales  Revenue
100    1000
200    2000
```

**The Fix:**
1. Select all → Home → Merge & Center → Unmerge
2. Fill down the values that were in merged cells
3. Now you have proper tabular data

**Rule:** Never use merged cells in data tables. Only in presentation layers.

---

**6. Missing Values**

**The Problem:**
```
| Customer | Sales | Region |
|----------|-------|--------|
| John     | 100   | North  |
| Jane     |       | South  |  ← Missing sales value
| Bob      | 150   |        |  ← Missing region
```

**The Fix (depends on context):**

**Option 1: Remove rows with missing critical data**
```excel
=IF(ISBLANK(B2),"DELETE","KEEP")  ← Flag rows to delete
```

**Option 2: Fill with default value**
```excel
=IF(ISBLANK(B2),0,B2)  ← Replace blanks with 0
=IF(ISBLANK(C2),"Unknown",C2)  ← Replace blanks with "Unknown"
```

**Option 3: Impute (fill with average/median)**
```excel
=IF(ISBLANK(B2),AVERAGE(B:B),B2)  ← Fill with column average
```

**Business Rule:** ALWAYS document how you handled missing values!

---

**7. Text Stored as Numbers (or vice versa)**

**The Problem:**
```
| Product Code |
|--------------|
| 001          |  ← Excel strips leading zero → shows as "1"
| 002          |
```

**The Fix:**
- Pre-format column as Text before pasting
- Or use formula: `=TEXT(A2,"000")` to add leading zeros back

---

**DATA CLEANING WORKFLOW (Your Step-by-Step Process):**

**STEP 1: Save Original** (Always!)
- Copy raw data to new sheet "Raw Data"
- Never work directly on original

**STEP 2: Create "Cleaned" Sheet**
- Copy to new sheet "Cleaned Data"
- Document what you changed

**STEP 3: Remove Obvious Junk**
- Delete empty rows/columns
- Remove headers/footers from report exports
- Unmerge cells

**STEP 4: Standardize Formats**
- Fix dates (one format)
- Fix currency (remove symbols, consistent decimals)
- TRIM all text columns

**STEP 5: Handle Missing Values**
- Identify blanks
- Decide: delete, fill, or flag
- Document decision

**STEP 6: Remove Duplicates**
- Check for true duplicates
- Remove if appropriate

**STEP 7: Validate**
- Count rows (did you lose data?)
- Check key columns (do values make sense?)
- Spot check 10-20 random rows

**STEP 8: Document**
- Add "Data Dictionary" sheet explaining each column
- Note any assumptions or decisions made
"""
        )

        st.markdown("#### 🔢 Essential Excel Formulas for Data Analysts")
        st.markdown(
            """**These formulas solve 80% of analyst problems. Master them.**

---

### 1. CONDITIONAL AGGREGATIONS (Your Daily Bread)

**SUMIF / SUMIFS - Conditional Summing**

**Business Question:** "What's total revenue for the North region?"

**Single Condition (SUMIF):**
```excel
=SUMIF(region_range, "North", revenue_range)
=SUMIF(B:B, "North", C:C)
```

**Multiple Conditions (SUMIFS):**

**Business Question:** "What's total revenue for North region in January?"

```excel
=SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2)
=SUMIFS(D:D, B:B, "North", C:C, "January")
```

**Real Example:**
```
=SUMIFS(Sales!$E:$E, Sales!$B:$B, "North", Sales!$C:$C, ">=2024-01-01", Sales!$C:$C, "<=2024-01-31")
```
Sums sales for North region between Jan 1-31, 2024

---

**COUNTIF / COUNTIFS - Conditional Counting**

**Business Question:** "How many customers are in the North region?"

```excel
=COUNTIF(B:B, "North")
```

**Multiple Conditions:**
"How many high-value (>£1000) customers in North region?"

```excel
=COUNTIFS(B:B, "North", C:C, ">1000")
```

---

**AVERAGEIF / AVERAGEIFS - Conditional Averaging**

**Business Question:** "What's the average order value for the North region?"

```excel
=AVERAGEIF(B:B, "North", C:C)
```

---

### 2. LOOKUPS (Joining Data From Different Sheets)

**VLOOKUP - The Classic (Vertical Lookup)**

**Business Scenario:** You have customer IDs in one sheet, need to add customer names from another sheet.

**Syntax:**
```excel
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

**Example:**
```excel
=VLOOKUP(A2, Customers!A:C, 2, FALSE)
```

Looks for value in A2, searches in Customers sheet columns A:C, returns value from column 2, exact match

**Common VLOOKUP Mistakes:**
- ❌ Lookup column not first in range
- ❌ Using TRUE (approximate match) when you want FALSE (exact match)
- ❌ Hardcoding column numbers instead of using COLUMN() function
- ✅ Always use FALSE for exact match in business data

---

**XLOOKUP - The Modern Replacement (Excel 365 / Google Sheets)**

**Why Better:** Searches any column, returns any column, handles errors better

**Syntax:**
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode])
```

**Example:**
```excel
=XLOOKUP(A2, Customers!A:A, Customers!B:B, "Not Found")
```

**Advantages:**
- Can search left or right
- Built-in error handling
- Faster
- More readable

---

**INDEX MATCH - The Flexible Powerhouse**

**Why Use:** Most flexible, works everywhere, better for large datasets

**Syntax:**
```excel
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
```

**Example:**
```excel
=INDEX(Customers!B:B, MATCH(A2, Customers!A:A, 0))
```

Reads as: "Return value from column B where column A matches A2"

**When to Use:**
- VLOOKUP limitations (lookup column not first)
- Two-way lookups (find row AND column)
- Large datasets (faster than VLOOKUP)

---

### 3. CONDITIONAL LOGIC

**IF Statements - Decision Making**

**Simple IF:**
```excel
=IF(condition, value_if_true, value_if_false)
=IF(A2>1000, "High Value", "Normal")
```

**Nested IF (Multiple Conditions):**
```excel
=IF(A2>5000, "Premium", IF(A2>1000, "High", "Normal"))
```

**Better Alternative - IFS (Excel 365):**
```excel
=IFS(A2>5000, "Premium", A2>1000, "High", A2>0, "Normal", TRUE, "Error")
```

---

**AND / OR - Combining Conditions**

**Business Question:** "Is this a high-value customer in a priority region?"

```excel
=IF(AND(B2="North", C2>1000), "Priority", "Standard")
```

**OR Example:**
```excel
=IF(OR(B2="North", B2="South"), "Covered", "Not Covered")
```

---

### 4. TEXT MANIPULATION

**CONCATENATE / CONCAT / & - Combining Text**

**Joining First and Last Name:**
```excel
=A2&" "&B2  ← Fastest way
=CONCAT(A2," ",B2)  ← Function way
```

**Building Addresses:**
```excel
=A2&", "&B2&", "&C2&" "&D2
```
Results: "123 Main St, London, UK SW1A 1AA"

---

**LEFT, RIGHT, MID - Extracting Parts of Text**

**Extract First 3 Characters:**
```excel
=LEFT(A2, 3)
```

**Extract Last 4 Characters (e.g., last 4 of phone number):**
```excel
=RIGHT(A2, 4)
```

**Extract Middle Characters:**
```excel
=MID(A2, 5, 3)  ← Start at position 5, extract 3 characters
```

**Real Example - Extract Postcode District:**
```excel
=LEFT(A2, FIND(" ", A2)-1)  ← Extracts "SW1A" from "SW1A 1AA"
```

---

### 5. DATE FORMULAS

**TODAY() / NOW()**
```excel
=TODAY()  ← Current date
=NOW()    ← Current date and time
```

**Age Calculation:**
```excel
=DATEDIF(birthdate, TODAY(), "Y")  ← Years
```

**Days Between Dates:**
```excel
=B2-A2  ← Simple subtraction works!
```

**Month/Year Extraction:**
```excel
=MONTH(A2)  ← Returns month number (1-12)
=YEAR(A2)   ← Returns year
=TEXT(A2, "MMMM")  ← Returns month name (e.g., "January")
```

---

**ANALYST TIP:** Build a "Formula Cheat Sheet"

Create a reference sheet with:
- Common formulas you use
- Examples with your actual data
- Notes on when to use each

This becomes your personal playbook for fast analysis.
"""
        )

        st.markdown("#### 📊 Pivot Tables - Your Secret Weapon for Fast Insights")
        st.markdown(
            """**Pivot Tables let you analyze thousands of rows in seconds without formulas.**

**When to Use Pivot Tables:**
- Need to summarize large datasets quickly
- Want to see data from multiple angles
- Stakeholder asks "What's X broken down by Y?"
- Exploring data to find patterns

**Common Business Questions Pivot Tables Answer:**
- Total sales by region?
- Average order value by customer segment?
- Count of appointments by clinic and month?
- Revenue by product category and sales rep?

**ALL of these → 30 seconds with Pivot Table**

---

**Creating Your First Pivot Table:**

**STEP 1: Select Your Data**
- Click anywhere in your data table
- Data → Pivot Table → Create

**STEP 2: Choose What to Analyze**
- Drag fields to 4 areas:
  - **ROWS:** What you want to group by (e.g., Region, Product, Month)
  - **COLUMNS:** Secondary grouping (optional, creates crosstab)
  - **VALUES:** What you want to calculate (e.g., Sum of Sales, Count of Orders)
  - **FILTERS:** Limit data shown (e.g., only show 2024 data)

**Example Setup:**

**Question:** "What's total sales by region and product category?"

- **ROWS:** Region
- **COLUMNS:** Product Category  
- **VALUES:** Sum of Sales
- **FILTERS:** Year = 2024

**Result:**
```
              Electronics  Clothing  Home
North         £50,000      £30,000   £20,000
South         £40,000      £35,000   £25,000
East          £45,000      £28,000   £22,000
```

---

**Common Pivot Table Tricks:**

**1. Calculated Fields (Add Your Own Metrics)**

Want to calculate Profit Margin in Pivot Table?

- Right-click in Pivot → Calculated Field
- Name: "Profit Margin"
- Formula: `= (Revenue - Cost) / Revenue`
- Now you can pivot by Profit Margin!

**2. Grouping Dates (Monthly, Quarterly)**

Have daily data but want monthly summary?

- Right-click on date field → Group
- Select: Months, Quarters, Years
- Instant monthly aggregation!

**3. Show Values As % of Total**

Want to see each region's % of total sales?

- Click value → Value Field Settings
- "Show Values As" → % of Grand Total
- Now shows: North = 35%, South = 30%, etc.

**4. Slicers (Visual Filters for Stakeholders)**

Make filtering easy for non-technical users:

- Pivot Table → Insert → Slicer
- Choose field (e.g., Region, Product)
- Click buttons to filter instantly
- Perfect for interactive dashboards!

---

**Pivot Table Best Practices:**

✅ **DO:**
- Refresh Pivot Table when source data changes (Right-click → Refresh)
- Use clear field names (rename if needed)
- Sort by values (largest to smallest)
- Add Grand Totals for context

❌ **DON'T:**
- Manually edit Pivot Table values (they'll be overwritten)
- Use Pivot Tables as data storage (they're for analysis only)
- Forget to document what filters are applied
- Make Pivot Tables from Pivot Tables (refresh original data instead)

---

**Real-World Example:**

**Scenario:** Hospital wants to understand appointment DNA patterns

**Your Process:**

1. **Get Data:** Export appointment data to Excel
2. **Clean:** Remove cancelled appointments, fix date formats
3. **Create Pivot Table:**
   - ROWS: Clinic Specialty
   - COLUMNS: Month
   - VALUES: COUNT of Appointment Status
   - FILTERS: Status = "DNA"

4. **Add Calculated Field:**
   - DNA Rate = DNAs / Total Appointments

5. **Sort:** By DNA Rate descending

6. **Result:** Instantly see which clinics have highest DNA rates by month

**Time to insight:** 5 minutes (vs hours of manual formulas)

**Delivery:** Copy Pivot Table to PowerPoint, add 2-3 sentence summary, done!
"""
        )

        st.markdown("---")
        st.markdown("## 🔬 HANDS-ON LABS - Unit 2: Excel Mastery")
        st.markdown(
            """**Practical exercises to become an Excel power user**

### LAB 1: Data Cleaning & Preparation in Excel

**Objective:** Clean a messy real-world dataset using Excel

**Scenario:** You received `sales_data_raw.xlsx` from the sales team. It's a mess!

**The Dataset Contains:**
- 5,000 rows of sales transactions
- Inconsistent date formats
- Duplicate records
- Missing values
- Extra spaces in text fields
- Mixed case product names
- Currency symbols in number fields

**Your Cleaning Tasks:**

**Step 1: Remove Duplicates**
```
1. Select your data range (Ctrl+A)
2. Data tab → Remove Duplicates
3. Check all columns
4. Excel reports: "47 duplicate values found and removed"
5. Result: 4,953 unique records
```

**Step 2: Fix Date Formats**
```
Problem: Dates appear as text ("01/15/2024", "January 15, 2024", "15-Jan-24")

Solution A: Text-to-Columns
1. Select date column
2. Data → Text to Columns
3. Choose "Delimited" → Next
4. Uncheck all delimiters → Next
5. Column data format: Date (MDY)
6. Finish

Solution B: Formula Method
=DATEVALUE(A2)
Then copy down and convert to values

Verification:
- All dates should be right-aligned (indicates number format)
- Format cells as "Short Date"
- Check: No #VALUE! errors
```

**Step 3: Clean Text Data (Remove Extra Spaces, Fix Case)**
```
Problem: Product names have extra spaces and mixed case
Example: "  wireless  MOUSE  " should be "Wireless Mouse"

Formula:
=PROPER(TRIM(B2))

Explanation:
- TRIM() removes extra spaces
- PROPER() converts to Title Case

Apply to all text columns:
1. Insert helper column
2. Write formula
3. Copy down entire column
4. Copy → Paste Values over original
5. Delete helper column
```

**Step 4: Extract & Parse Data**
```
Problem: Email addresses in format "john.doe@company.com"
Need: Extract first name, last name, domain

Formulas:
First Name: =LEFT(D2, FIND(".", D2)-1)
Last Name: =MID(D2, FIND(".", D2)+1, FIND("@", D2)-FIND(".", D2)-1)
Domain: =RIGHT(D2, LEN(D2)-FIND("@", D2))

Example: "john.doe@company.com"
- First Name: john
- Last Name: doe
- Domain: company.com
```

**Step 5: Handle Missing Values**
```
Problem: Revenue column has blanks and "N/A" text

Strategy:
1. Find blanks: Ctrl+F → Find All → blank cells
2. Options:
   a) Fill with 0: Find & Replace blank with 0
   b) Fill with average: =AVERAGE(E:E), then fill blanks
   c) Remove rows: Filter → Blanks → Delete

For "N/A" text:
1. Find & Replace: "N/A" → (leave blank)
2. Convert to numbers: Select column → yellow warning → Convert to Number
```

**Step 6: Remove Currency Symbols & Convert to Numbers**
```
Problem: Revenue shows as "£1,234.56" (text)

Solution:
=VALUE(SUBSTITUTE(SUBSTITUTE(F2,"£",""),",",""))

Or use Find & Replace:
1. Find: £ → Replace with: (nothing)
2. Find: , → Replace with: (nothing)
3. Convert to Number
```

**Step 7: Data Validation to Prevent Future Issues**
```
Set up rules for clean data entry:

1. Date column:
   Data → Data Validation → Date
   Between: 01/01/2024 and TODAY()

2. Revenue column:
   Data Validation → Decimal
   Greater than: 0

3. Product Category:
   Data Validation → List
   Source: Electronics,Clothing,Home,Books
```

**Deliverable:** 
- Cleaned dataset: `sales_data_cleaned.xlsx`
- Documentation: List of issues found and fixes applied
- Before/After comparison screenshots

**Time:** 2-3 hours  
**Success Criteria:**
- ✅ No duplicate records
- ✅ All dates in consistent format
- ✅ No extra spaces or mixed case
- ✅ No missing critical values
- ✅ All numbers properly formatted
- ✅ Data validation rules applied

---

### LAB 2: Advanced Formulas & Functions

**Objective:** Master complex Excel formulas for real-world analysis

**Scenario:** Analyzing customer data for RetailCo

**Dataset:** `customer_transactions.xlsx`
- customer_id, transaction_date, product_category, revenue, region

**Challenge 1: Calculate Customer Lifetime Value (CLV)**

```excel
Column A: Customer ID
Column B: First Purchase Date (use MIN with customer ID)
Column C: Last Purchase Date (use MAX with customer ID)
Column D: Total Revenue (SUMIF)
Column E: Number of Transactions (COUNTIF)
Column F: Average Order Value (Total Revenue / Transactions)
Column G: Customer Tenure (Days)
Column H: Monthly Spend Rate

Formulas:
B2: =MIN(IF($A$2:$A$5000=A2,$B$2:$B$5000))  [Array formula: Ctrl+Shift+Enter]

Or better with MINIFS (Excel 2016+):
B2: =MINIFS(Transaction_Table[transaction_date], 
             Transaction_Table[customer_id], A2)

C2: =MAXIFS(Transaction_Table[transaction_date], 
            Transaction_Table[customer_id], A2)

D2: =SUMIFS(Transaction_Table[revenue], 
            Transaction_Table[customer_id], A2)

E2: =COUNTIFS(Transaction_Table[customer_id], A2)

F2: =D2/E2

G2: =C2-B2

H2: =D2/(G2/30)  // Monthly spend rate

CLV (simplified): =H2*12*3  // 3-year projection
```

**Challenge 2: Customer Segmentation with Nested IFs**

```excel
Segment customers based on RFM (Recency, Frequency, Monetary):

Recency Score (1-5):
=IF(DAYS(TODAY(), LastPurchase)<=30, 5,
  IF(DAYS(TODAY(), LastPurchase)<=90, 4,
    IF(DAYS(TODAY(), LastPurchase)<=180, 3,
      IF(DAYS(TODAY(), LastPurchase)<=365, 2, 1))))

Frequency Score:
=IF(TotalTransactions>=20, 5,
  IF(TotalTransactions>=10, 4,
    IF(TotalTransactions>=5, 3,
      IF(TotalTransactions>=2, 2, 1))))

Monetary Score:
=IF(TotalRevenue>=1000, 5,
  IF(TotalRevenue>=500, 4,
    IF(TotalRevenue>=250, 3,
      IF(TotalRevenue>=100, 2, 1))))

RFM Segment:
=IF(AND(R_Score>=4, F_Score>=4, M_Score>=4), "Champions",
  IF(AND(R_Score>=3, F_Score>=3, M_Score>=3), "Loyal",
    IF(AND(R_Score<=2, F_Score>=3), "At Risk",
      IF(R_Score<=2, "Lost", "Potential"))))
```

**Challenge 3: INDEX-MATCH (Better than VLOOKUP!)**

```excel
Problem: Look up product price from separate price list

VLOOKUP limitation:
- Only looks to the right
- Breaks if columns reordered
- Slow on large datasets

INDEX-MATCH solution:
=INDEX(PriceList[Price], 
       MATCH([@Product], PriceList[Product_Name], 0))

Why it's better:
- Can look left or right
- More flexible
- Faster performance
- Column order doesn't matter

Advanced: Two-way lookup (row AND column)
=INDEX(Sales_Data, 
       MATCH(Product_Name, Product_Column, 0),
       MATCH(Month_Name, Month_Row, 0))
```

**Challenge 4: Array Formulas for Advanced Analysis**

```excel
Top 5 customers by revenue:
=LARGE(Revenue_Range, ROW(A1))  // Copy down 5 rows for top 5

Get customer name for each top 5:
=INDEX(Customer_Names, 
       MATCH(LARGE(Revenue_Range, ROW(A1)), Revenue_Range, 0))

Count unique customers:
=SUMPRODUCT(1/COUNTIF(Customer_Range, Customer_Range))

Sum of top 20%:
=SUMIF(Revenue_Range, ">="&PERCENTILE(Revenue_Range, 0.8))
```

**Challenge 5: Dynamic Named Ranges**

```excel
Create auto-expanding ranges for dropdown lists:

1. Formulas → Define Name → "ProductList"
2. Refers to: 
   =OFFSET(Sheet1!$A$2, 0, 0, COUNTA(Sheet1!$A:$A)-1, 1)

This range automatically expands as you add products!

Use in Data Validation:
Source: =ProductList
```

**Deliverable:**
- Workbook with all formulas
- Annotated screenshots explaining each formula
- Test cases demonstrating formulas work correctly

**Time:** 3-4 hours  
**Tools:** Excel 2016 or later

---

### LAB 3: Pivot Tables & Dynamic Reporting

**Objective:** Create professional pivot table reports and dashboards

**Scenario:** Monthly sales reporting for management

**Dataset:** `sales_transactions_2024.xlsx`
- 50,000 transactions
- Fields: Date, Region, Sales_Rep, Product_Category, Product, Units_Sold, Revenue

**Task 1: Build Standard Sales Reports**

**Report 1: Revenue by Region & Month**
```
Pivot Table Setup:
- Rows: Region
- Columns: Month (grouped by month)
- Values: Sum of Revenue
- Format: Currency, thousands separator

Formatting:
- Conditional formatting on revenue (color scale)
- Show row totals and column totals
- Add % of Grand Total

Result: Instantly see which regions perform best each month
```

**Report 2: Product Performance Analysis**
```
Pivot Table:
- Rows: Product_Category → Product (hierarchical)
- Values: 
  * Sum of Revenue
  * Sum of Units_Sold
  * Average Revenue (calculated field)
- Show: Top 10 products by revenue

Calculated Field:
Average Order Value = Revenue / Units_Sold

Slicers:
- Add slicer for Region
- Add slicer for Month
- Connect slicers to multiple pivot tables
```

**Report 3: Sales Rep Leaderboard**
```
Pivot Table:
- Rows: Sales_Rep
- Values:
  * Sum of Revenue
  * Count of Transactions
  * Average Deal Size
- Sort: By revenue descending

Conditional Formatting:
- Data bars for revenue column
- Icon sets for performance tiers
  * Top 20%: Green up arrow
  * Middle 60%: Yellow dash
  * Bottom 20%: Red down arrow
```

**Task 2: Create Interactive Dashboard**

**Dashboard Components:**

**1. Summary Cards (using formulas)**
```
Total Revenue: =GETPIVOTDATA("Revenue", $A$3)
YoY Growth: =(CurrentYear-PriorYear)/PriorYear
Transactions: =GETPIVOTDATA("Transaction_ID", $A$3, "Count")
Avg Order: =Total_Revenue/Transactions
```

**2. Revenue Trend Chart**
- Line chart from pivot table
- Show month-over-month comparison
- Add trendline
- Format for clarity

**3. Regional Breakdown**
- Pie chart or donut chart
- Show top 5 regions
- Group others as "Other"

**4. Category Mix**
- Stacked bar chart
- Revenue by category by month
- Show trends

**5. Top Products Table**
- Connected to slicers
- Auto-updates based on filters
- Conditional formatting

**Dashboard Layout:**
```
+------------------+------------------+
| Total Revenue    | YoY Growth       |
+------------------+------------------+
| Monthly Trend Chart                 |
+-------------------------------------+
| Regional Mix     | Category Mix     |
+-------------------------------------+
| Top Products Table                  |
+-------------------------------------+
| Slicers: Region | Month | Category |
+-------------------------------------+
```

**Task 3: Advanced Pivot Table Techniques**

**Calculated Fields & Items:**
```
Calculated Field: Profit Margin
= (Revenue - Cost) / Revenue

Calculated Item: Q1 Sales
= January + February + March

Show Value As options:
- % of Parent Total
- Running Total
- Difference From (compare to previous month)
- % Difference From
```

**Grouping:**
```
Group dates by:
- Month
- Quarter
- Year

Group numbers:
Revenue ranges: 0-100, 100-500, 500-1000, 1000+
```

**Custom Sorting:**
```
Sort regions by:
- Custom list (North, South, East, West)
- Manual drag-and-drop
- By value (largest to smallest)
```

**Deliverable:**
- Excel dashboard file
- PDF report generated from dashboard
- Instructions for updating with new data

**Time:** 4-5 hours  
**Success Criteria:**
- ✅ All pivot tables refresh automatically
- ✅ Slicers control multiple visuals
- ✅ Professional formatting
- ✅ Dashboard fits on one screen
- ✅ Charts tell clear story

---

### LAB 4: Excel Automation Basics (Macros & VBA Introduction)

**Objective:** Automate repetitive tasks with macros

**Scenario:** You run the same monthly report every month - time to automate!

**Task 1: Record a Simple Macro**

**Monthly Formatting Macro:**
```
Steps to record:
1. Developer tab → Record Macro
   Name: FormatMonthlyReport
   Shortcut: Ctrl+Shift+F
   
2. Perform actions:
   - Select data range
   - Apply table formatting
   - Auto-fit columns
   - Add filters
   - Format currency columns
   - Bold headers
   
3. Stop recording

Run macro: Ctrl+Shift+F

Result: All formatting applied in seconds!
```

**Task 2: Edit Macro in VBA**

**View the code:**
```vba
Sub FormatMonthlyReport()
    ' Select data range
    Range("A1").CurrentRegion.Select
    
    ' Apply table formatting
    ActiveSheet.ListObjects.Add(xlSrcRange, Selection, , xlYes).Name = "ReportTable"
    ActiveSheet.ListObjects("ReportTable").TableStyle = "TableStyleMedium2"
    
    ' Auto-fit columns
    Columns.AutoFit
    
    ' Format currency
    Range("E:E").NumberFormat = "$#,##0.00"
    Range("F:F").NumberFormat = "$#,##0.00"
    
    ' Bold headers
    Range("A1:F1").Font.Bold = True
    
    MsgBox "Report formatted successfully!", vbInformation
End Sub
```

**Task 3: Create a Data Refresh Macro**

```vba
Sub RefreshAllData()
    Application.ScreenUpdating = False
    
    ' Refresh all pivot tables
    Dim ws As Worksheet
    Dim pt As PivotTable
    
    For Each ws In ThisWorkbook.Worksheets
        For Each pt In ws.PivotTables
            pt.RefreshTable
        Next pt
    Next ws
    
    ' Refresh all data connections
    ThisWorkbook.RefreshAll
    
    Application.ScreenUpdating = True
    
    MsgBox "All data refreshed!", vbInformation
End Sub
```

**Task 4: Build a Simple Input Form**

```vba
Sub AddNewTransaction()
    Dim lastRow As Long
    Dim newDate As Date
    Dim newRegion As String
    Dim newRevenue As Double
    
    ' Get inputs
    newDate = InputBox("Enter transaction date (mm/dd/yyyy):")
    newRegion = InputBox("Enter region (North/South/East/West):")
    newRevenue = InputBox("Enter revenue amount:")
    
    ' Find last row
    lastRow = Cells(Rows.Count, 1).End(xlUp).Row + 1
    
    ' Add new record
    Cells(lastRow, 1).Value = newDate
    Cells(lastRow, 2).Value = newRegion
    Cells(lastRow, 3).Value = newRevenue
    
    MsgBox "Transaction added successfully!", vbInformation
End Sub
```

**Task 5: Automate Report Generation**

```vba
Sub GenerateMonthlyReport()
    Dim reportMonth As String
    Dim ws As Worksheet
    
    ' Get current month
    reportMonth = Format(Date, "mmmm yyyy")
    
    ' Create new worksheet
    Set ws = Worksheets.Add
    ws.Name = "Report_" & Format(Date, "mmm_yyyy")
    
    ' Copy data
    Sheets("Raw_Data").Range("A1").CurrentRegion.Copy ws.Range("A1")
    
    ' Apply formatting
    Call FormatMonthlyReport
    
    ' Create pivot table
    Call CreatePivotTable(ws)
    
    ' Create charts
    Call CreateCharts(ws)
    
    ' Save as PDF
    ws.ExportAsFixedFormat Type:=xlTypePDF, _
        Filename:=ThisWorkbook.Path & "\Report_" & Format(Date, "mmm_yyyy") & ".pdf"
    
    MsgBox "Monthly report generated and saved!", vbInformation
End Sub
```

**Deliverable:**
- Workbook with working macros
- Documentation of what each macro does
- Button on worksheet to trigger macros

**Time:** 3-4 hours  
**Prerequisites:** Basic VBA understanding helpful but not required

---

### MINI PROJECT 2: Sales Dashboard with Real-Time Updates

**Objective:** Build a complete sales dashboard that updates automatically

**Scenario:** Create executive dashboard for weekly sales review

**Requirements:**

**1. Data Connection**
- Connect to external data source (CSV or database)
- Set up automatic refresh on file open
- Handle connection errors gracefully

**2. KPI Cards**
```
Design 4 KPI cards showing:
- Total Revenue (with vs target %)
- Number of Transactions (with WoW change)
- Average Order Value (with trend arrow)
- Top Performing Region

Format:
- Large number (36pt)
- Label underneath (12pt)
- % change or trend indicator
- Color coding (green/red based on target)
```

**3. Dynamic Charts**
```
Chart 1: Revenue Trend (Line)
- Last 12 weeks
- Multiple series (Actual vs Target)
- Data labels on last point
- Trendline

Chart 2: Regional Performance (Bar)
- Horizontal bars
- Sorted by revenue
- Data labels showing %
- Conditional colors

Chart 3: Product Mix (Donut)
- Top 5 categories
- Show percentages
- Pull out largest slice

Chart 4: Weekly Comparison (Column)
- This week vs last week
- By day of week
- Grouped columns
```

**4. Interactive Filters**
```
Add slicers for:
- Week selector
- Region filter
- Product category filter

Connect all slicers to:
- Pivot tables
- Charts
- KPI calculations
```

**5. Automated Insights**
```
Use formulas to generate text insights:

IF(Revenue > Target, 
   "Revenue is UP " & FORMAT((Revenue-Target)/Target, "0%") & " vs target!",
   "Revenue is DOWN " & FORMAT((Target-Revenue)/Target, "0%") & " vs target")

Top performer:
=INDEX(RegionNames, MATCH(MAX(Revenues), Revenues, 0))

Alert for low performance:
=IF(WeeklyRevenue < PreviousWeek * 0.9, 
    "⚠️ Revenue down >10% week-over-week", 
    "")
```

**6. Professional Design**
```
Design elements:
- Consistent color scheme (2-3 colors max)
- Clear hierarchy (large to small)
- White space for readability
- Gridlines hidden
- Clean fonts (Calibri, Arial)
- Company logo
- Print layout (fits on one page)
```

**Technical Specifications:**

**Data Structure:**
```
Source data table with columns:
- Date
- Transaction_ID
- Region
- Sales_Rep
- Product_Category
- Product_Name
- Units_Sold
- Unit_Price
- Revenue
- Cost
- Profit
```

**Calculated Metrics:**
```
Revenue_vs_Target: =Revenue/Target-1
WoW_Change: =(This_Week-Last_Week)/Last_Week
Profit_Margin: =Profit/Revenue
Units_per_Transaction: =Total_Units/Transaction_Count
```

**Refresh Process:**
```
1. Open file → Data refreshes automatically
2. Pivot tables update
3. Charts redraw
4. KPIs recalculate
5. Insights regenerate
```

**Deliverable:**
- Complete Excel dashboard file
- Sample data file
- User guide (1-page PDF)
- Video walkthrough (3-5 minutes)

**Time:** 6-8 hours  
**Success Criteria:**
- ✅ Dashboard updates with new data
- ✅ All elements interactive
- ✅ Professional appearance
- ✅ Insights accurate and helpful
- ✅ Prints well on one page
- ✅ Works for non-technical users

---

### Advanced Excel Tips & Tricks

**Power Query Basics:**
```
Transform data without formulas!

1. Data → Get & Transform → From Table/Range
2. Transform operations:
   - Remove duplicates
   - Fill down blanks
   - Split columns
   - Pivot/Unpivot
   - Merge queries
   - Append queries

3. Close & Load → Creates clean table
4. Refresh to reapply transformations
```

**Conditional Formatting Mastery:**
```
Use Cases:
1. Heat maps (color scales)
2. Progress bars (data bars)
3. Status indicators (icon sets)
4. Highlight duplicates
5. Highlight top/bottom values
6. Compare to benchmark

Pro tip: Use formulas for custom rules
=AND($B2>100, $C2<0.1)
```

**Dynamic Charts:**
```
Create charts that update automatically:

1. Use named ranges with OFFSET
2. Chart data source = dynamic range
3. Updates as data grows
4. No manual range adjustment needed
```

**Keyboard Shortcuts Every Analyst Needs:**
```
Ctrl + T: Create table
Ctrl + Shift + L: Toggle filters
Alt + ;: Select visible cells only
Ctrl + `: Show formulas
F4: Cycle through $ references
Ctrl + Page Up/Down: Switch sheets
Alt + =: Auto-sum
Ctrl + D: Fill down
Ctrl + R: Fill right
F9: Calculate now
```

**Excel Best Practices:**
```
✅ DO:
- Use tables (Ctrl+T) for all data
- Name your ranges
- Document complex formulas
- Use data validation
- Protect formula cells
- Save versions
- Test edge cases

❌ DON'T:
- Merge cells (breaks formulas)
- Hide rows/columns with data
- Use VLOOKUP (use INDEX-MATCH)
- Hardcode values (use cell references)
- Forget to document
- Skip data validation
- Use inconsistent formats
```

**Practice Resources:**

**Sample Datasets:**
- `retail_sales_50k.xlsx` - Large retail dataset
- `customer_database.xlsx` - Customer information
- `product_catalog.xlsx` - Product master data
- `web_analytics.xlsx` - Website traffic data

**Challenge Exercises:**
1. Build cohort analysis
2. Create customer segmentation
3. Design ABC inventory classification
4. Build budget vs actual analysis
5. Create waterfall chart

**Success Criteria for Unit 2:**
- ✅ Expert at data cleaning
- ✅ Mastered advanced formulas
- ✅ Build professional pivot reports
- ✅ Create interactive dashboards
- ✅ Basic macro automation
- ✅ Portfolio-ready Excel projects

---

## 📝 40+ EXCEL PRACTICE PROBLEMS - Unit 2

### Data Cleaning Challenges (10 Problems)

**Problem 1: Remove duplicates while preserving specific records**
```
Scenario: Customer database with 10,000 records, many duplicates
Task: Keep only the most recent record for each customer
Solution:
1. Sort by Customer ID (ascending), then Date (descending)
2. Data → Remove Duplicates, select Customer ID only
3. First occurrence (most recent) kept automatically
```

**Problem 2: Split full names into first and last**
```
Data: "John Smith", "Mary Johnson-Williams", "Dr. Robert Lee"
Formula: 
First Name: =LEFT(A2, FIND(" ", A2)-1)
Last Name: =RIGHT(A2, LEN(A2)-FIND(" ", A2))
Handle titles: =IF(LEFT(A2,3)="Dr.", MID(A2,5,FIND(" ",A2,5)-5), LEFT(A2,FIND(" ",A2)-1))
```

**Problem 3: Clean inconsistent date formats**
```
Mixed formats: "01/15/2024", "Jan 15, 2024", "15-Jan-24"
Solution:
1. Select all dates
2. Data → Text to Columns
3. Choose "Date" format
4. Or use: =DATEVALUE(A2) to force conversion
```

**Problem 4: Remove extra spaces and trim text**
```
Data: "  London   ", " New York", "Paris  "
Formula: =TRIM(A2)
For all cells: Select range → Find & Replace → Find: " " (2 spaces) → Replace: " " (1 space) → Replace All (repeat)
```

**Problem 5: Extract numeric values from mixed text**
```
Data: "Sales: $1,250.00", "Revenue: £2,500", "Total: 3500 units"
Formula: =VALUE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(A2,"$",""),"£",""),",",""))
Or regex in VBA for complex patterns
```

**Problem 6: Standardize inconsistent categories**
```
Data: "UK", "United Kingdom", "uk", "U.K."
Solution using Find & Replace:
1. Find "uk" → Replace "United Kingdom" (Match case OFF)
2. Find "U.K." → Replace "United Kingdom"
Or use formula: =PROPER(TRIM(SUBSTITUTE(A2,"."," ")))
```

**Problem 7: Identify and flag outliers**
```
Dataset: Sales figures with occasional errors (e.g., $1,000,000 instead of $10,000)
Formula for Z-score:
=(A2-AVERAGE($A$2:$A$1000))/STDEV($A$2:$A$1000)
Flag if ABS(Z-score) > 3
Conditional formatting: Highlight cells > 3 standard deviations
```

**Problem 8: Convert text to proper date format**
```
Data: "20240115" (YYYYMMDD as text)
Formula: =DATE(LEFT(A2,4), MID(A2,5,2), RIGHT(A2,2))
Or: =DATE(VALUE(LEFT(A2,4)), VALUE(MID(A2,5,2)), VALUE(RIGHT(A2,2)))
```

**Problem 9: Remove special characters from text**
```
Data: "Product #123!", "Item@456", "SKU*789"
Formula: =SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(A2,"#",""),"@",""),"*","")
For all special chars: Use VBA or Power Query
```

**Problem 10: Consolidate data from multiple sheets**
```
Sheets: Jan_Sales, Feb_Sales, Mar_Sales (same structure)
Solution:
1. Power Query → New Query → From File → Combine → From Folder
2. Or VBA loop through sheets and consolidate
3. Or manual: Copy → Paste Special → Values
```

---

### Formula Mastery (15 Problems)

**Problem 11: Calculate customer lifetime value**
```
Formula: =SUMIF(Orders!$B:$B, A2, Orders!$E:$E)
Where A2 = Customer ID, Orders!E:E = Order values
Advanced: =SUMIFS(Orders!$E:$E, Orders!$B:$B, A2, Orders!$D:$D, ">="&DATE(2024,1,1))
```

**Problem 12: Nested IF for customer segmentation**
```
=IF(B2>=10000,"Platinum",IF(B2>=5000,"Gold",IF(B2>=1000,"Silver","Bronze")))
Or better with IFS (Excel 2019+):
=IFS(B2>=10000,"Platinum",B2>=5000,"Gold",B2>=1000,"Silver",TRUE,"Bronze")
```

**Problem 13: INDEX-MATCH for two-way lookup**
```
Lookup product price by name and region:
=INDEX(Prices!$B$2:$E$100, MATCH(A2,Prices!$A$2:$A$100,0), MATCH(C2,Prices!$B$1:$E$1,0))
Where A2=Product, C2=Region
```

**Problem 14: Calculate month-over-month growth**
```
Current month in B2, Previous month in A2:
=(B2-A2)/A2
Formatted as percentage: =(B2-A2)/A2 → Format Cells → Percentage
Handle errors: =IFERROR((B2-A2)/A2, "N/A")
```

**Problem 15: Array formula for top N values**
```
Top 5 sales: =LARGE($B$2:$B$1000, ROW(A1))
Drag down 5 rows to get top 5
Get corresponding names: =INDEX($A$2:$A$1000, MATCH(LARGE($B$2:$B$1000,ROW(A1)), $B$2:$B$1000, 0))
```

**Problem 16: SUMPRODUCT for weighted average**
```
Calculate weighted average price:
=SUMPRODUCT(Quantity_Range, Price_Range)/SUM(Quantity_Range)
Example: =SUMPRODUCT(B2:B100, C2:C100)/SUM(B2:B100)
```

**Problem 17: Dynamic date ranges**
```
This Month: =SUMIFS(Sales!$C:$C, Sales!$A:$A, ">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))
Last 30 Days: =SUMIFS(Sales!$C:$C, Sales!$A:$A, ">="&TODAY()-30)
Year to Date: =SUMIFS(Sales!$C:$C, Sales!$A:$A, ">="&DATE(YEAR(TODAY()),1,1))
```

**Problem 18: Conditional counting**
```
Count customers with >5 orders:
=COUNTIF(Order_Count_Range, ">5")
Count orders in Q1:
=COUNTIFS(Date_Range, ">="&DATE(2024,1,1), Date_Range, "<="&DATE(2024,3,31))
```

**Problem 19: Text manipulation formula**
```
Extract domain from email: =RIGHT(A2, LEN(A2)-FIND("@",A2))
Create initials: =LEFT(A2,1)&LEFT(MID(A2,FIND(" ",A2)+1,50),1)
```

**Problem 20: Lookup with multiple criteria**
```
=INDEX(Result_Range, MATCH(1, (Criteria1_Range=Value1)*(Criteria2_Range=Value2), 0))
Enter as array formula (Ctrl+Shift+Enter in older Excel)
Or use XLOOKUP in Excel 365: =XLOOKUP(1, (A2:A100=Value1)*(B2:B100=Value2), C2:C100)
```

**Problem 21: Running total calculation**
```
Simple: =SUM($B$2:B2) and drag down
With conditions: =SUMIF($A$2:A2, A2, $B$2:B2)
By month: =SUMIFS($C:$C, $A:$A, "<="&A2)
```

**Problem 22: Age calculation from birthdate**
```
=DATEDIF(A2, TODAY(), "Y")
Or: =INT((TODAY()-A2)/365.25)
Age at specific date: =DATEDIF(A2, DATE(2024,12,31), "Y")
```

**Problem 23: Ranking with ties**
```
=RANK(A2, $A$2:$A$100, 0)
No gaps: =COUNTIF($A$2:$A$100, ">"&A2)+1
Percentage rank: =RANK(A2,$A$2:$A$100,0)/COUNT($A$2:$A$100)
```

**Problem 24: Dynamic dropdown lists**
```
Named range that updates:
1. Define: =OFFSET(Sheet1!$A$2,0,0,COUNTA(Sheet1!$A:$A)-1,1)
2. Data Validation → List → Source: =YourNamedRange
Or use Tables (Ctrl+T) for auto-expanding ranges
```

**Problem 25: Error handling in formulas**
```
=IFERROR(VLOOKUP(A2, Table, 2, FALSE), "Not Found")
Multiple error types:
=IF(ISERROR(A2/B2), IF(B2=0, "Div by Zero", "Error"), A2/B2)
```

---

### Pivot Table Challenges (10 Problems)

**Problem 26: Multi-level pivot with calculated fields**
```
Task: Sales by Region → City → Product with profit margin
Steps:
1. Insert Pivot Table
2. Rows: Region, City, Product
3. Values: Sum of Sales, Sum of Cost
4. Add Calculated Field: Profit Margin = (Sales-Cost)/Sales
5. Format as percentage
```

**Problem 27: Pivot table with timeline slicer**
```
Task: Filter sales data by date range visually
Steps:
1. Create pivot table
2. Insert → Timeline
3. Select Date field
4. Users can now slide to select periods
```

**Problem 28: Show % of total in pivot**
```
Task: Each product's contribution to total sales
Steps:
1. Add Sales to Values
2. Right-click on value → Show Values As → % of Grand Total
3. Or % of Parent Row Total for hierarchical data
```

**Problem 29: Grouping dates in pivot**
```
Task: Group daily sales into months/quarters
Steps:
1. Right-click any date in Rows
2. Group → Select Months and Quarters
3. Or Years for annual view
```

**Problem 30: Top N filter in pivot**
```
Task: Show only top 10 products by sales
Steps:
1. Click dropdown on Product
2. Value Filters → Top 10
3. Specify: Top 10 items by Sum of Sales
```

**Problem 31: Calculated items in pivot**
```
Task: Create "Total EU" item combining UK, France, Germany
Steps:
1. Right-click on Region field
2. Insert Calculated Item
3. Name: "Total EU"
4. Formula: =UK+France+Germany
```

**Problem 32: Pivot table with conditional formatting**
```
Task: Highlight top performers in green, bottom in red
Steps:
1. Select values area
2. Home → Conditional Formatting → Color Scales
3. Or use Top/Bottom Rules
```

**Problem 33: Refresh pivot from external data**
```
Task: Update pivot when source CSV changes
Steps:
1. Data → From Text/CSV → Load to Pivot
2. Right-click pivot → Refresh
3. Or PivotTable Analyze → Refresh → Refresh All
```

**Problem 34: Multiple pivot tables from same source**
```
Task: Create separate pivots for sales, costs, margins
Steps:
1. Create first pivot
2. Alt+D+P → Existing data → Based on existing pivot
3. Shares cache, saves memory
```

**Problem 35: Pivot with running total**
```
Task: Show cumulative sales over time
Steps:
1. Add Date to Rows, Sales to Values
2. Right-click Sales → Show Values As → Running Total In
3. Select Date field as base
```

---

### Dashboard & Charts (5 Problems)

**Problem 36: Dynamic chart that updates automatically**
```
Task: Chart that grows with data
Solution:
1. Convert range to Table (Ctrl+T)
2. Create chart from Table
3. Or use named ranges with OFFSET
4. Chart updates automatically as data grows
```

**Problem 37: Combo chart (column + line)**
```
Task: Show sales (columns) and profit margin (line)
Steps:
1. Create column chart with Sales
2. Right-click profit data series
3. Change Chart Type → Line
4. Format axes appropriately
```

**Problem 38: Sparklines for quick trends**
```
Task: Mini charts in cells showing monthly trends
Formula:
1. Select cell for sparkline
2. Insert → Line Sparkline
3. Select data range
4. Format with Sparkline Tools
```

**Problem 39: Interactive dashboard with slicers**
```
Task: Dashboard where users filter by region/date
Steps:
1. Create pivot tables/charts
2. Insert → Slicer
3. Select fields: Region, Date
4. Right-click slicer → Report Connections → Connect to all pivots
```

**Problem 40: Waterfall chart for variance analysis**
```
Task: Show budget vs actual with bridges
Steps (Excel 2016+):
1. Organize data: Starting, Increases, Decreases, Ending
2. Insert → Waterfall Chart
3. Set subtotals and totals as needed
4. Format with colors
```

---

### Advanced Techniques (5 Problems)

**Problem 41: Data validation with dynamic lists**
```
Task: Dropdown that changes based on previous selection
Solution:
1. Create dependent lists (e.g., Country → City)
2. Use INDIRECT in Data Validation
3. Source: =INDIRECT($A2) where A2 contains list name
```

**Problem 42: Conditional formatting with formulas**
```
Task: Highlight entire row if sales < target
Formula: =$C2<$D2 (no $ on row number)
Apply to range: $A$2:$Z$100
Highlights entire row when condition true
```

**Problem 43: Protect workbook while allowing data entry**
```
Task: Lock formulas but allow input cells
Steps:
1. Select input cells → Format Cells → Protection → Uncheck "Locked"
2. Review → Protect Sheet
3. Allow: Select unlocked cells
4. Users can only edit designated cells
```

**Problem 44: Quick analysis with recommended charts**
```
Task: Find best chart for data
Steps:
1. Select data range
2. Home → Quick Analysis (Ctrl+Q)
3. Browse Charts tab
4. Excel recommends appropriate visualizations
```

**Problem 45: Use Excel as database with Advanced Filter**
```
Task: Complex multi-criteria filtering
Steps:
1. Set up criteria range above data
2. Data → Advanced Filter
3. Can copy results to new location
4. More powerful than standard filters
```

---

### Real-World Excel Challenges

**Challenge 1: Financial Model**
Build 3-statement model (Income Statement, Balance Sheet, Cash Flow) with scenarios

**Challenge 2: Sales Dashboard**
Create interactive dashboard with:
- KPI cards (sales, growth, target%)
- Regional breakdown pivot
- Trend charts
- Product performance table

**Challenge 3: Budget Tracker**
Build tool that compares budget vs actual monthly with:
- Variance analysis
- Alerts for >10% variance
- Year-to-date summaries
- Visual traffic lights (red/amber/green)

**Challenge 4: Customer Cohort Analysis**
Analyze customer cohorts by signup month showing:
- Retention rates month-by-month
- Revenue per cohort
- Heatmap visualization
- Churn predictions

**Challenge 5: Inventory Management**
Create system tracking:
- Stock levels
- Reorder points
- Lead times
- Alerts for low stock

---

"""
        )
    elif unit_number == 3:
        st.markdown("#### 📘 Why SQL is THE Essential Skill for Data Analysts")
        st.markdown(
            """**SQL (Structured Query Language) is the universal language of data.**

If you learn ONE technical skill as a data analyst, make it SQL.

**Why SQL Matters:**

**1. Where the Data Actually Lives**
- 90%+ of organizational data is in relational databases
- Customer records, transactions, inventory, appointments → all in databases
- Excel has row limits (1M rows), databases handle billions
- SQL lets you access data DIRECTLY without waiting for exports

**2. Independence & Speed**
- Without SQL: "Hey IT, can you export last month's sales?" (2 days wait)
- With SQL: Write query, get answer in 30 seconds
- Become self-sufficient analyst, don't depend on engineers

**3. Universal Skill**
- Works with: PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, BigQuery
- Syntax 95% the same across all systems
- Learn once, use everywhere

**4. Job Requirement**
- "SQL required" in 95%+ of data analyst job descriptions
- Often the deciding factor between candidates
- Salary bump: SQL skills = £5K-£10K higher starting salary

**Real-World Example:**

**Without SQL:**
Manager: "How many appointments did we have last month by clinic?"
You: "Let me request a data export... I'll have this by Wednesday."
*Two days later, you receive a 50MB CSV, clean it in Excel, create pivot table*
**Total time: 2 days**

**With SQL:**
Manager: "How many appointments did we have last month by clinic?"
You: *Opens SQL tool, writes query*
```sql
SELECT 
    clinic_name,
    COUNT(*) as appointment_count
FROM appointments
WHERE appointment_date >= '2024-10-01' 
  AND appointment_date < '2024-11-01'
GROUP BY clinic_name
ORDER BY appointment_count DESC;
```
**Total time: 2 minutes**

**That's the power of SQL.**

---

**What is a Relational Database?**

Think of it as multiple Excel sheets (tables) that are connected (related) to each other.

**Example: Hospital Database**

**Table 1: patients**
| patient_id | patient_name | dob        | postcode |
|------------|--------------|------------|----------|
| 1          | John Doe     | 1980-05-15 | SW1A 1AA |
| 2          | Jane Smith   | 1975-08-22 | E1 6AN   |

**Table 2: appointments**
| appointment_id | patient_id | clinic_id | appointment_date | status |
|----------------|------------|-----------|------------------|--------|
| 101            | 1          | 10        | 2024-11-01       | Attended |
| 102            | 2          | 10        | 2024-11-01       | DNA      |

**Table 3: clinics**
| clinic_id | clinic_name     | specialty    |
|-----------|-----------------|--------------|
| 10        | Dermatology     | Dermatology  |
| 11        | Cardiology      | Cardiology   |

**Key Concept:** `patient_id` connects patients to appointments. `clinic_id` connects appointments to clinics.

This is how real databases organize data - avoiding duplication and maintaining relationships.
"""
        )

        st.markdown("#### 🔍 Core SELECT Queries: Your Foundation")
        st.markdown(
            """**Every SQL query starts with SELECT.**

---

### 1. Basic SELECT - Get All Columns

**Business Question:** "Show me all patient records"

```sql
SELECT * 
FROM patients;
```

**What this does:**
- `SELECT *` = get all columns
- `FROM patients` = from the patients table

**Output:**
```
| patient_id | patient_name | dob        | postcode |
|------------|--------------|------------|----------|
| 1          | John Doe     | 1980-05-15 | SW1A 1AA |
| 2          | Jane Smith   | 1975-08-22 | E1 6AN   |
... all rows returned
```

⚠️ **WARNING:** `SELECT *` on big tables returns millions of rows! Always add `LIMIT` when exploring:

```sql
SELECT * 
FROM patients
LIMIT 10;  -- Only return 10 rows
```

---

### 2. SELECT Specific Columns - Get What You Need

**Business Question:** "Show me just patient names and postcodes"

```sql
SELECT 
    patient_name,
    postcode
FROM patients;
```

**Output:**
```
| patient_name | postcode |
|--------------|----------|
| John Doe     | SW1A 1AA |
| Jane Smith   | E1 6AN   |
```

**Best Practice:** Only select columns you need. Faster queries, less data transfer.

---

### 3. WHERE Clause - Filtering Rows

**Business Question:** "Show me appointments from November 2024"

```sql
SELECT *
FROM appointments
WHERE appointment_date >= '2024-11-01'
  AND appointment_date < '2024-12-01';
```

**Common WHERE Operators:**

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equals | `status = 'Attended'` |
| `!=` or `<>` | Not equals | `status != 'Cancelled'` |
| `>` | Greater than | `age > 65` |
| `>=` | Greater than or equal | `appointment_date >= '2024-01-01'` |
| `<` | Less than | `waiting_days < 7` |
| `<=` | Less than or equal | `price <= 100` |
| `BETWEEN` | Range | `age BETWEEN 18 AND 65` |
| `IN` | Multiple values | `status IN ('Attended', 'DNA')` |
| `LIKE` | Pattern match | `patient_name LIKE 'John%'` |
| `IS NULL` | Missing value | `email IS NULL` |
| `IS NOT NULL` | Has value | `phone IS NOT NULL` |

**Multiple Conditions with AND/OR:**

```sql
-- Both conditions must be true
SELECT *
FROM appointments
WHERE status = 'DNA'
  AND appointment_date >= '2024-11-01';

-- Either condition can be true
SELECT *
FROM patients
WHERE postcode LIKE 'SW%'
   OR postcode LIKE 'E%';
```

**Pattern Matching with LIKE:**

```sql
-- Find patients whose name starts with 'John'
SELECT *
FROM patients
WHERE patient_name LIKE 'John%';  -- % = any characters

-- Find patients with 'Smith' anywhere in name
SELECT *
FROM patients
WHERE patient_name LIKE '%Smith%';

-- Find postcodes starting with SW1
SELECT *
FROM patients
WHERE postcode LIKE 'SW1%';
```

---

### 4. ORDER BY - Sorting Results

**Business Question:** "Show me patients ordered by date of birth, oldest first"

```sql
SELECT 
    patient_name,
    dob
FROM patients
ORDER BY dob ASC;  -- ASC = ascending (oldest to newest)
```

**Descending order (newest first):**

```sql
SELECT 
    patient_name,
    dob
FROM patients
ORDER BY dob DESC;  -- DESC = descending
```

**Multiple sort columns:**

```sql
-- Sort by postcode, then by name within each postcode
SELECT 
    patient_name,
    postcode
FROM patients
ORDER BY postcode, patient_name;
```

---

### 5. DISTINCT - Remove Duplicates

**Business Question:** "What unique postcodes do our patients come from?"

```sql
SELECT DISTINCT postcode
FROM patients
ORDER BY postcode;
```

**With COUNT:**

```sql
-- How many unique clinics do we have?
SELECT COUNT(DISTINCT clinic_id) as unique_clinics
FROM appointments;
```

---

### 6. LIMIT - Control Result Size

**Business Question:** "Show me the 10 most recent appointments"

```sql
SELECT *
FROM appointments
ORDER BY appointment_date DESC
LIMIT 10;
```

**Pagination (skip first 10, show next 10):**

```sql
SELECT *
FROM appointments
ORDER BY appointment_date DESC
LIMIT 10 OFFSET 10;  -- Skip first 10 results
```

---

### Putting It All Together - Real Business Query

**Business Question:** "Show me the 20 most recent DNA appointments in Dermatology clinics, including patient names"

```sql
SELECT 
    a.appointment_date,
    p.patient_name,
    c.clinic_name,
    a.status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN clinics c ON a.clinic_id = c.clinic_id
WHERE a.status = 'DNA'
  AND c.specialty = 'Dermatology'
  AND a.appointment_date >= '2024-01-01'
ORDER BY a.appointment_date DESC
LIMIT 20;
```

*(JOINs explained in next section!)*
"""
        )

        st.markdown("#### 📊 Aggregations: Summarizing Data")
        st.markdown(
            """**Aggregation functions let you calculate summaries: totals, averages, counts, etc.**

---

### 1. COUNT - Counting Rows

**Business Question:** "How many appointments do we have?"

```sql
SELECT COUNT(*) as total_appointments
FROM appointments;
```

**Output:**
```
| total_appointments |
|--------------------|
| 15234              |
```

**Count non-null values in specific column:**

```sql
-- How many patients have email addresses?
SELECT COUNT(email) as patients_with_email
FROM patients;
```

**Count unique values:**

```sql
-- How many unique patients had appointments?
SELECT COUNT(DISTINCT patient_id) as unique_patients
FROM appointments;
```

---

### 2. SUM - Adding Up Values

**Business Question:** "What's total revenue from appointments?"

```sql
SELECT SUM(appointment_fee) as total_revenue
FROM appointments;
```

**With WHERE clause:**

```sql
-- Total revenue from November 2024
SELECT SUM(appointment_fee) as november_revenue
FROM appointments
WHERE appointment_date >= '2024-11-01'
  AND appointment_date < '2024-12-01';
```

---

### 3. AVG - Average Values

**Business Question:** "What's the average patient age?"

```sql
SELECT AVG(YEAR(CURRENT_DATE) - YEAR(dob)) as average_age
FROM patients;
```

**More readable with ROUND:**

```sql
SELECT ROUND(AVG(waiting_days), 1) as avg_waiting_days
FROM appointments;
```

**Output:**
```
| avg_waiting_days |
|------------------|
| 42.3             |
```

---

### 4. MIN and MAX - Minimum and Maximum

**Business Question:** "What's the longest and shortest waiting time?"

```sql
SELECT 
    MIN(waiting_days) as shortest_wait,
    MAX(waiting_days) as longest_wait
FROM appointments;
```

**Output:**
```
| shortest_wait | longest_wait |
|---------------|--------------|
| 1             | 180          |
```

---

### 5. GROUP BY - Aggregating by Category

**This is where SQL becomes POWERFUL.**

**Business Question:** "How many appointments per clinic?"

```sql
SELECT 
    clinic_id,
    COUNT(*) as appointment_count
FROM appointments
GROUP BY clinic_id
ORDER BY appointment_count DESC;
```

**Output:**
```
| clinic_id | appointment_count |
|-----------|-------------------|
| 10        | 1234              |
| 11        | 987               |
| 12        | 856               |
```

**With meaningful names (using JOIN):**

```sql
SELECT 
    c.clinic_name,
    COUNT(*) as appointment_count
FROM appointments a
JOIN clinics c ON a.clinic_id = c.clinic_id
GROUP BY c.clinic_name
ORDER BY appointment_count DESC;
```

**Multiple aggregations:**

```sql
-- Appointments per clinic with DNA rate
SELECT 
    c.clinic_name,
    COUNT(*) as total_appointments,
    SUM(CASE WHEN a.status = 'DNA' THEN 1 ELSE 0 END) as dna_count,
    ROUND(100.0 * SUM(CASE WHEN a.status = 'DNA' THEN 1 ELSE 0 END) / COUNT(*), 2) as dna_rate
FROM appointments a
JOIN clinics c ON a.clinic_id = c.clinic_id
WHERE a.appointment_date >= '2024-01-01'
GROUP BY c.clinic_name
ORDER BY dna_rate DESC;
```

**Output:**
```
| clinic_name  | total_appointments | dna_count | dna_rate |
|--------------|--------------------|-----------| ---------|
| Dermatology  | 1234               | 185       | 14.99    |
| Cardiology   | 987                | 118       | 11.95    |
```

---

### 6. HAVING - Filtering Aggregated Results

**Difference:**
- `WHERE` filters rows BEFORE aggregation
- `HAVING` filters results AFTER aggregation

**Business Question:** "Which clinics have more than 1000 appointments?"

```sql
SELECT 
    clinic_name,
    COUNT(*) as appointment_count
FROM appointments a
JOIN clinics c ON a.clinic_id = c.clinic_id
GROUP BY clinic_name
HAVING COUNT(*) > 1000  -- Filter AFTER counting
ORDER BY appointment_count DESC;
```

**Complex example - High DNA clinics:**

```sql
-- Clinics with >100 appointments AND DNA rate >15%
SELECT 
    c.clinic_name,
    COUNT(*) as total_appointments,
    ROUND(100.0 * SUM(CASE WHEN a.status = 'DNA' THEN 1 ELSE 0 END) / COUNT(*), 2) as dna_rate
FROM appointments a
JOIN clinics c ON a.clinic_id = c.clinic_id
WHERE a.appointment_date >= '2024-01-01'
GROUP BY c.clinic_name
HAVING COUNT(*) > 100
   AND 100.0 * SUM(CASE WHEN a.status = 'DNA' THEN 1 ELSE 0 END) / COUNT(*) > 15
ORDER BY dna_rate DESC;
```

This finds problematic clinics (high volume + high DNA rate).
"""
        )

        st.markdown("#### 🔗 JOINs: Combining Data from Multiple Tables")
        st.markdown(
            """**Real business questions need data from multiple tables. JOINs connect them.**

---

### Understanding Keys

**Primary Key:** Unique identifier for each row
- `patient_id` in patients table
- `appointment_id` in appointments table

**Foreign Key:** References primary key in another table
- `patient_id` in appointments table (references patients table)
- `clinic_id` in appointments table (references clinics table)

---

### INNER JOIN - Only Matching Rows

**Business Question:** "Show me appointments with patient names"

**Without JOIN (incomplete):**
```sql
SELECT * FROM appointments;
-- Only shows patient_id (e.g., 1, 2, 3)
-- We can't see patient names!
```

**With INNER JOIN:**
```sql
SELECT 
    a.appointment_date,
    p.patient_name,
    a.status
FROM appointments a
INNER JOIN patients p ON a.patient_id = p.patient_id;
```

**What happens:**
1. For each row in `appointments`
2. Find matching row in `patients` where IDs match
3. Combine columns from both tables
4. Only include rows that have matches in BOTH tables

**Visual:**
```
appointments             patients              RESULT
-----------             --------              ------
appt_id | patient_id   patient_id | name    appt_id | name | ...
--------|------------  -----------|------   ---------|------|----
101     | 1            1          | John    101      | John | ...
102     | 2            2          | Jane    102      | Jane | ...
103     | 9            3          | Bob     (103 not included - no patient #9)
```

---

### LEFT JOIN - Keep All from Left Table

**Business Question:** "Show me all patients, whether they have appointments or not"

```sql
SELECT 
    p.patient_name,
    COUNT(a.appointment_id) as appointment_count
FROM patients p
LEFT JOIN appointments a ON p.patient_id = a.patient_id
GROUP BY p.patient_name;
```

**What happens:**
- Keep ALL patients
- If patient has appointments, show them
- If patient has NO appointments, show NULL (which we count as 0)

**Result:**
```
| patient_name | appointment_count |
|--------------|-------------------|
| John Doe     | 5                 |
| Jane Smith   | 3                 |
| Bob Johnson  | 0                 | ← Left JOIN keeps this
```

**Use case:** Finding patients who NEVER had appointments (for outreach)

```sql
SELECT 
    p.patient_name,
    p.email
FROM patients p
LEFT JOIN appointments a ON p.patient_id = a.patient_id
WHERE a.appointment_id IS NULL;  -- No appointments
```

---

### RIGHT JOIN - Keep All from Right Table

**Rarely used** (just reverse your tables and use LEFT JOIN instead)

```sql
-- These are equivalent:
SELECT * FROM appointments a LEFT JOIN patients p ...
SELECT * FROM patients p RIGHT JOIN appointments a ...
```

---

### Multiple JOINs - Real-World Complexity

**Business Question:** "Show me DNA appointments with patient names, clinic names, and specialty"

```sql
SELECT 
    a.appointment_date,
    p.patient_name,
    c.clinic_name,
    c.specialty,
    a.status
FROM appointments a
INNER JOIN patients p ON a.patient_id = p.patient_id
INNER JOIN clinics c ON a.clinic_id = c.clinic_id
WHERE a.status = 'DNA'
  AND a.appointment_date >= '2024-11-01'
ORDER BY a.appointment_date DESC;
```

**Joins 3 tables:**
1. appointments → patients (get patient names)
2. appointments → clinics (get clinic info)

---

### Common JOIN Patterns for Analysts

**1. One-to-Many (Most Common)**

Example: One patient, many appointments

```sql
-- How many appointments per patient?
SELECT 
    p.patient_name,
    COUNT(a.appointment_id) as num_appointments
FROM patients p
LEFT JOIN appointments a ON p.patient_id = a.patient_id
GROUP BY p.patient_name
ORDER BY num_appointments DESC;
```

**2. Many-to-Many (via Junction Table)**

Example: Patients can have many doctors, doctors can have many patients

```sql
-- Requires junction table: patient_doctor
SELECT 
    p.patient_name,
    d.doctor_name
FROM patients p
JOIN patient_doctor pd ON p.patient_id = pd.patient_id
JOIN doctors d ON pd.doctor_id = d.doctor_id;
```

**3. Self-JOIN (Comparing Rows in Same Table)**

Example: Find patients in same postcode area

```sql
SELECT 
    p1.patient_name as patient_1,
    p2.patient_name as patient_2,
    p1.postcode
FROM patients p1
JOIN patients p2 ON p1.postcode = p2.postcode
    AND p1.patient_id < p2.patient_id;  -- Avoid duplicates
```

---

### JOIN Best Practices

✅ **DO:**
- Always specify join condition (`ON table1.id = table2.id`)
- Use table aliases (`appointments a`, `patients p`) for readability
- Join on indexed columns (primary/foreign keys) for performance
- Think about which JOIN type you need (INNER vs LEFT)

❌ **DON'T:**
- Forget the join condition (creates Cartesian product - millions of rows!)
- Join on non-key columns without understanding implications
- Use SELECT * in complex joins (hard to debug)

---

### Real Business Example - Complete Analysis

**Business Question:** "What's the DNA rate by specialty for November 2024, for clinics with >50 appointments?"

```sql
SELECT 
    c.specialty,
    COUNT(*) as total_appointments,
    SUM(CASE WHEN a.status = 'DNA' THEN 1 ELSE 0 END) as dna_count,
    ROUND(100.0 * SUM(CASE WHEN a.status = 'DNA' THEN 1 ELSE 0 END) / COUNT(*), 2) as dna_rate_percent
FROM appointments a
INNER JOIN clinics c ON a.clinic_id = c.clinic_id
WHERE a.appointment_date >= '2024-11-01'
  AND a.appointment_date < '2024-12-01'
GROUP BY c.specialty
HAVING COUNT(*) > 50
ORDER BY dna_rate_percent DESC;
```

**This one query:**
- Joins 2 tables
- Filters by date
- Groups by specialty
- Calculates percentages
- Filters aggregated results
- Sorts by DNA rate

**Time to write:** 2 minutes
**Business value:** Immediate identification of problem areas

**THIS is why SQL is powerful.**
"""
        )

        st.markdown("---")
        st.markdown("## 🔬 HANDS-ON LABS - Unit 3: SQL Mastery")
        st.markdown(
            """**Practical exercises to become a SQL expert**

### LAB 1: SQL Fundamentals - SELECT, WHERE, ORDER BY

**Objective:** Master basic SQL queries for data retrieval

**Scenario:** You're analyzing e-commerce data for OnlineRetail

**Database Schema:**
```sql
-- customers: customer_id, first_name, last_name, email, country, signup_date
-- orders: order_id, customer_id, order_date, total_amount, status  
-- order_items: item_id, order_id, product_id, quantity, unit_price
-- products: product_id, product_name, category, price, stock_quantity
```

**Challenge 1: Basic SELECT & Filtering**
```sql
-- UK customers who signed up in 2024
SELECT first_name, last_name, email, signup_date
FROM customers
WHERE country = 'UK' AND signup_date >= '2024-01-01'
ORDER BY signup_date DESC;

-- High-value completed orders
SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE total_amount > 500 AND status = 'Completed'
ORDER BY total_amount DESC;

-- Products with 'wireless' in name under £100
SELECT product_name, category, price
FROM products
WHERE product_name LIKE '%wireless%' AND price < 100
ORDER BY price;
```

**Challenge 2: Date Functions & Aggregations**
```sql
-- Orders from last 30 days
SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE order_date >= DATEADD(day, -30, GETDATE())
ORDER BY order_date DESC;

-- Monthly order summary for 2024
SELECT 
    MONTH(order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order
FROM orders
WHERE YEAR(order_date) = 2024 AND status = 'Completed'
GROUP BY MONTH(order_date)
ORDER BY month;
```

**Success Criteria:**
- ✅ Write 10+ SELECT queries
- ✅ Use WHERE with multiple conditions
- ✅ Apply date filtering correctly
- ✅ Use ORDER BY and LIMIT/TOP

**Time:** 2-3 hours

---

### LAB 2: JOINs - Combining Tables

**Objective:** Master all JOIN types

**Challenge 1: INNER JOIN - Customer Orders**
```sql
-- Customer names with their orders
SELECT 
    c.first_name,
    c.last_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.order_date DESC;

-- Order details with product names
SELECT 
    o.order_id,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) as line_total
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id;
```

**Challenge 2: LEFT JOIN - Include All Records**
```sql
-- All customers with order counts (including zero orders)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.total_amount), 0) as lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY lifetime_value DESC;

-- Products never ordered
SELECT 
    p.product_id,
    p.product_name,
    p.category
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;
```

**Challenge 3: Multiple JOINs - Complete Report**
```sql
-- Full order details report
SELECT 
    c.first_name + ' ' + c.last_name as customer_name,
    c.email,
    c.country,
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) as total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.order_date DESC;
```

**Success Criteria:**
- ✅ Use INNER, LEFT, RIGHT JOINs correctly
- ✅ Join 3+ tables
- ✅ Handle NULL values with COALESCE
- ✅ Write complex multi-table queries

**Time:** 3-4 hours

---

### LAB 3: Aggregations & GROUP BY

**Objective:** Master aggregation functions

**Challenge 1: Basic Aggregations**
```sql
-- Sales summary
SELECT 
    COUNT(*) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order,
    MIN(total_amount) as min_order,
    MAX(total_amount) as max_order
FROM orders
WHERE status = 'Completed';

-- Product inventory by category
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    SUM(stock_quantity) as total_stock
FROM products
GROUP BY category
ORDER BY total_stock DESC;
```

**Challenge 2: GROUP BY Multiple Columns**
```sql
-- Sales by country and month
SELECT 
    c.country,
    YEAR(o.order_date) as year,
    MONTH(o.order_date) as month,
    COUNT(o.order_id) as orders,
    SUM(o.total_amount) as revenue,
    AVG(o.total_amount) as avg_order
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
GROUP BY c.country, YEAR(o.order_date), MONTH(o.order_date)
ORDER BY year, month, revenue DESC;
```

**Challenge 3: HAVING Clause**
```sql
-- High-value customers (>£1000)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) as orders,
    SUM(o.total_amount) as lifetime_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(o.total_amount) > 1000
ORDER BY lifetime_value DESC;
```

**Challenge 4: Advanced Aggregations**
```sql
-- Customer cohort analysis
SELECT 
    YEAR(c.signup_date) as signup_year,
    MONTH(c.signup_date) as signup_month,
    COUNT(DISTINCT c.customer_id) as customers,
    COUNT(DISTINCT o.order_id) as orders,
    SUM(o.total_amount) as revenue,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN o.order_date IS NOT NULL THEN c.customer_id END) / COUNT(DISTINCT c.customer_id), 2) as conversion_rate
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY YEAR(c.signup_date), MONTH(c.signup_date)
ORDER BY signup_year, signup_month;
```

**Success Criteria:**
- ✅ Use all aggregation functions (COUNT, SUM, AVG, MIN, MAX)
- ✅ GROUP BY single and multiple columns
- ✅ Filter groups with HAVING
- ✅ Calculate percentages and rates

**Time:** 3-4 hours

**Deliverable for Labs 1-3:**
- SQL script files with all queries
- Query results screenshots
- Analysis writeup

---

### LAB 4: Window Functions & Advanced Analytics

**Objective:** Master window functions for complex analysis

**Challenge 1: ROW_NUMBER, RANK, DENSE_RANK**
```sql
-- Rank products by revenue within each category
SELECT 
    product_name,
    category,
    SUM(quantity * unit_price) as revenue,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(quantity * unit_price) DESC) as row_num,
    RANK() OVER (PARTITION BY category ORDER BY SUM(quantity * unit_price) DESC) as rank_num
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY product_name, category
ORDER BY category, revenue DESC;
```

**Challenge 2: Running Totals**
```sql
-- Daily sales with running total
SELECT 
    CAST(order_date AS DATE) as date,
    SUM(total_amount) as daily_revenue,
    SUM(SUM(total_amount)) OVER (ORDER BY CAST(order_date AS DATE)) as running_total
FROM orders
WHERE status = 'Completed'
GROUP BY CAST(order_date AS DATE)
ORDER BY date;
```

**Challenge 3: LAG and LEAD**
```sql
-- Month-over-month growth
WITH monthly_sales AS (
    SELECT 
        YEAR(order_date) as year,
        MONTH(order_date) as month,
        SUM(total_amount) as revenue
    FROM orders
    WHERE status = 'Completed'
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT 
    year,
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY year, month) as prev_month,
    revenue - LAG(revenue) OVER (ORDER BY year, month) as change,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY year, month)) / LAG(revenue) OVER (ORDER BY year, month), 2) as pct_change
FROM monthly_sales
ORDER BY year, month;
```

**Success Criteria:**
- ✅ Use ROW_NUMBER, RANK, DENSE_RANK
- ✅ Calculate running totals
- ✅ Use LAG/LEAD for comparisons
- ✅ Apply PARTITION BY correctly

**Time:** 3-4 hours

---

### LAB 5: CTEs & Subqueries

**Objective:** Master Common Table Expressions

**Challenge 1: Simple CTE**
```sql
-- Customer segmentation with CTE
WITH customer_stats AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        COUNT(o.order_id) as order_count,
        SUM(o.total_amount) as lifetime_value,
        DATEDIFF(day, MAX(o.order_date), GETDATE()) as days_since_last
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'Completed'
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT 
    *,
    CASE 
        WHEN lifetime_value >= 1000 THEN 'VIP'
        WHEN lifetime_value >= 500 THEN 'High'
        WHEN lifetime_value >= 100 THEN 'Medium'
        ELSE 'Low'
    END as value_segment,
    CASE 
        WHEN days_since_last <= 30 THEN 'Active'
        WHEN days_since_last <= 90 THEN 'At Risk'
        ELSE 'Churned'
    END as status
FROM customer_stats
ORDER BY lifetime_value DESC;
```

**Challenge 2: Multiple CTEs**
```sql
-- Product performance with multiple CTEs
WITH product_sales AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        COUNT(oi.order_id) as times_ordered,
        SUM(oi.quantity) as units_sold,
        SUM(oi.quantity * oi.unit_price) as revenue
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name, p.category
),
category_avg AS (
    SELECT 
        category,
        AVG(revenue) as avg_revenue
    FROM product_sales
    GROUP BY category
)
SELECT 
    ps.*,
    ca.avg_revenue as category_average,
    ps.revenue - ca.avg_revenue as diff_from_avg
FROM product_sales ps
JOIN category_avg ca ON ps.category = ca.category
ORDER BY ps.revenue DESC;
```

**Success Criteria:**
- ✅ Write single and multiple CTEs
- ✅ Use CTEs for complex calculations
- ✅ Understand CTE vs subquery performance

**Time:** 3-4 hours

---

### MINI PROJECT 4: E-Commerce SQL Analytics

**Objective:** Build complete SQL analytics for business intelligence

**Requirements:**

**1. Executive Dashboard Query**
```sql
-- Key business metrics
SELECT 
    COUNT(DISTINCT customer_id) as total_customers,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order_value,
    COUNT(DISTINCT CASE WHEN order_date >= DATEADD(day, -30, GETDATE()) THEN customer_id END) as active_customers_30d
FROM orders
WHERE status = 'Completed' AND order_date >= '2024-01-01';
```

**2. Customer RFM Segmentation**
```sql
-- Full RFM analysis
WITH rfm AS (
    SELECT 
        c.customer_id,
        c.first_name + ' ' + c.last_name as name,
        DATEDIFF(day, MAX(o.order_date), GETDATE()) as recency,
        COUNT(o.order_id) as frequency,
        SUM(o.total_amount) as monetary
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'Completed'
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT 
    *,
    NTILE(5) OVER (ORDER BY recency ASC) as r_score,
    NTILE(5) OVER (ORDER BY frequency DESC) as f_score,
    NTILE(5) OVER (ORDER BY monetary DESC) as m_score,
    CASE 
        WHEN NTILE(5) OVER (ORDER BY recency ASC) >= 4 
         AND NTILE(5) OVER (ORDER BY frequency DESC) >= 4 
         AND NTILE(5) OVER (ORDER BY monetary DESC) >= 4 THEN 'Champions'
        WHEN NTILE(5) OVER (ORDER BY recency ASC) <= 2 THEN 'At Risk/Churned'
        ELSE 'Potential Loyalists'
    END as segment
FROM rfm
ORDER BY monetary DESC;
```

**3. Product Performance Report**
```sql
-- Comprehensive product analysis
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    COUNT(DISTINCT oi.order_id) as times_ordered,
    SUM(oi.quantity) as units_sold,
    SUM(oi.quantity * oi.unit_price) as revenue,
    RANK() OVER (PARTITION BY p.category ORDER BY SUM(oi.quantity * oi.unit_price) DESC) as category_rank
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category, p.price
ORDER BY revenue DESC;
```

**4. Cohort Retention Analysis**
```sql
-- Monthly cohort retention
WITH cohorts AS (
    SELECT 
        customer_id,
        MIN(order_date) as first_order,
        DATEFROMPARTS(YEAR(MIN(order_date)), MONTH(MIN(order_date)), 1) as cohort_month
    FROM orders
    GROUP BY customer_id
)
SELECT 
    c.cohort_month,
    DATEDIFF(month, c.cohort_month, o.order_date) as months_since_first,
    COUNT(DISTINCT o.customer_id) as active_customers
FROM cohorts c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.cohort_month, DATEDIFF(month, c.cohort_month, o.order_date)
ORDER BY c.cohort_month, months_since_first;
```

**Deliverable:**
- Complete SQL script with 10+ queries
- Results exported to CSV
- PowerPoint presentation with insights
- Recommendations document

**Time:** 6-8 hours

**Success Criteria for Unit 3:**
- ✅ Master all SQL fundamentals
- ✅ Write complex JOINs fluently
- ✅ Use aggregations and window functions
- ✅ Build production-ready analytics queries
- ✅ Complete portfolio SQL project

---

## 📝 60+ SQL PRACTICE QUERIES - Unit 3

### Basic SELECT & Filtering (10 Queries)

**Query 1: Select all customers from London**
```sql
SELECT customer_id, customer_name, city
FROM customers
WHERE city = 'London';
```

**Query 2: Find orders over £1000**
```sql
SELECT order_id, customer_id, order_total
FROM orders
WHERE order_total > 1000
ORDER BY order_total DESC;
```

**Query 3: Get products with low stock (< 10 units)**
```sql
SELECT product_id, product_name, stock_quantity
FROM products
WHERE stock_quantity < 10
ORDER BY stock_quantity ASC;
```

**Query 4: Find customers with Gmail addresses**
```sql
SELECT customer_id, customer_name, email
FROM customers
WHERE email LIKE '%@gmail.com';
```

**Query 5: Orders placed in Q1 2024**
```sql
SELECT order_id, order_date, order_total
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
ORDER BY order_date;
```

**Query 6: Products in specific categories**
```sql
SELECT product_id, product_name, category
FROM products
WHERE category IN ('Electronics', 'Computers', 'Phones')
ORDER BY category, product_name;
```

**Query 7: Find NULL values in email column**
```sql
SELECT customer_id, customer_name
FROM customers
WHERE email IS NULL;
```

**Query 8: Customers whose names start with 'A'**
```sql
SELECT customer_id, customer_name
FROM customers
WHERE customer_name LIKE 'A%'
ORDER BY customer_name;
```

**Query 9: Orders NOT from specific regions**
```sql
SELECT order_id, customer_id, region
FROM orders
WHERE region NOT IN ('North', 'South');
```

**Query 10: Complex WHERE with multiple conditions**
```sql
SELECT order_id, order_total, order_date, status
FROM orders
WHERE order_total > 500
  AND order_date >= '2024-01-01'
  AND status = 'Completed'
ORDER BY order_total DESC;
```

---

### JOIN Queries (15 Queries)

**Query 11: Simple INNER JOIN - Orders with customer names**
```sql
SELECT o.order_id, o.order_date, c.customer_name, o.order_total
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC;
```

**Query 12: LEFT JOIN - All customers with their orders (including no orders)**
```sql
SELECT c.customer_id, c.customer_name, o.order_id, o.order_total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_name;
```

**Query 13: Find customers with NO orders**
```sql
SELECT c.customer_id, c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**Query 14: Three-table JOIN - Orders with products and customers**
```sql
SELECT 
  o.order_id,
  c.customer_name,
  p.product_name,
  oi.quantity,
  oi.unit_price
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id;
```

**Query 15: Self JOIN - Employees and their managers**
```sql
SELECT 
  e.employee_id,
  e.employee_name,
  m.employee_name as manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY m.employee_name, e.employee_name;
```

**Query 16: CROSS JOIN - All product-region combinations**
```sql
SELECT p.product_name, r.region_name
FROM products p
CROSS JOIN regions r
ORDER BY p.product_name, r.region_name;
```

**Query 17: Multiple JOINs with WHERE - Regional sales analysis**
```sql
SELECT 
  r.region_name,
  c.customer_name,
  SUM(o.order_total) as total_sales
FROM regions r
INNER JOIN customers c ON r.region_id = c.region_id
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY r.region_name, c.customer_name
HAVING SUM(o.order_total) > 1000
ORDER BY total_sales DESC;
```

**Query 18: JOIN with aggregation - Products never ordered**
```sql
SELECT p.product_id, p.product_name
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;
```

**Query 19: Date-based JOIN - Recent customer activity**
```sql
SELECT 
  c.customer_id,
  c.customer_name,
  o.order_id,
  o.order_date
FROM customers c
INNER JOIN orders o 
  ON c.customer_id = o.customer_id 
  AND o.order_date >= DATEADD(day, -30, GETDATE())
ORDER BY o.order_date DESC;
```

**Query 20: Compound JOIN conditions**
```sql
SELECT 
  o1.order_id as order_1,
  o2.order_id as order_2,
  o1.customer_id
FROM orders o1
INNER JOIN orders o2 
  ON o1.customer_id = o2.customer_id 
  AND o1.order_id < o2.order_id
  AND DATEDIFF(day, o1.order_date, o2.order_date) <= 7;
```

**Query 21-25: More JOIN variations**
- Find products ordered by multiple customers
- List categories with no products
- Match customers to similar customers by region
- Orders with same-day shipments
- Customers with orders in multiple regions

---

### Aggregation & GROUP BY (15 Queries)

**Query 26: Total sales by region**
```sql
SELECT region, SUM(order_total) as total_sales
FROM orders
GROUP BY region
ORDER BY total_sales DESC;
```

**Query 27: Count customers by city**
```sql
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
HAVING COUNT(*) > 10
ORDER BY customer_count DESC;
```

**Query 28: Average order value by month**
```sql
SELECT 
  DATE_TRUNC('month', order_date) as month,
  AVG(order_total) as avg_order_value,
  COUNT(*) as order_count
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

**Query 29: Multiple aggregations**
```sql
SELECT 
  product_category,
  COUNT(*) as product_count,
  SUM(units_sold) as total_units,
  AVG(unit_price) as avg_price,
  MIN(unit_price) as min_price,
  MAX(unit_price) as max_price
FROM products
GROUP BY product_category
ORDER BY total_units DESC;
```

**Query 30: HAVING clause - High-value customers**
```sql
SELECT 
  customer_id,
  COUNT(*) as order_count,
  SUM(order_total) as total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(order_total) > 10000
ORDER BY total_spent DESC;
```

**Query 31: GROUP BY with JOIN**
```sql
SELECT 
  c.customer_name,
  COUNT(o.order_id) as order_count,
  SUM(o.order_total) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;
```

**Query 32: Complex grouping - Year over Year comparison**
```sql
SELECT 
  YEAR(order_date) as year,
  MONTH(order_date) as month,
  SUM(order_total) as monthly_sales
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;
```

**Query 33: Percentage calculations**
```sql
SELECT 
  region,
  SUM(order_total) as region_sales,
  SUM(order_total) * 100.0 / (SELECT SUM(order_total) FROM orders) as pct_of_total
FROM orders
GROUP BY region
ORDER BY region_sales DESC;
```

**Query 34: DISTINCT aggregations**
```sql
SELECT 
  product_id,
  COUNT(DISTINCT customer_id) as unique_customers,
  COUNT(*) as total_orders
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
GROUP BY product_id
HAVING COUNT(DISTINCT customer_id) > 50
ORDER BY unique_customers DESC;
```

**Query 35: Rolling aggregations**
```sql
SELECT 
  order_date,
  order_total,
  SUM(order_total) OVER (ORDER BY order_date) as running_total
FROM orders
ORDER BY order_date;
```

**Query 36-40: More aggregation challenges**
- Daily sales with 7-day moving average
- Product sales ranking by category
- Customer lifetime value calculation
- Churn rate by cohort
- Conversion funnel analysis

---

### Window Functions (10 Queries)

**Query 41: Running total by customer**
```sql
SELECT 
  customer_id,
  order_date,
  order_total,
  SUM(order_total) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date
  ) as running_total
FROM orders
ORDER BY customer_id, order_date;
```

**Query 42: Rank products by sales within category**
```sql
SELECT 
  product_category,
  product_name,
  total_sales,
  RANK() OVER (
    PARTITION BY product_category 
    ORDER BY total_sales DESC
  ) as category_rank
FROM (
  SELECT 
    p.product_category,
    p.product_name,
    SUM(oi.quantity * oi.unit_price) as total_sales
  FROM products p
  JOIN order_items oi ON p.product_id = oi.product_id
  GROUP BY p.product_category, p.product_name
) sales_data;
```

**Query 43: LAG function - Compare to previous period**
```sql
SELECT 
  order_date,
  daily_sales,
  LAG(daily_sales, 1) OVER (ORDER BY order_date) as prev_day_sales,
  daily_sales - LAG(daily_sales, 1) OVER (ORDER BY order_date) as day_over_day_change
FROM (
  SELECT 
    DATE(order_date) as order_date,
    SUM(order_total) as daily_sales
  FROM orders
  GROUP BY DATE(order_date)
) daily_summary
ORDER BY order_date;
```

**Query 44: LEAD function - Look ahead**
```sql
SELECT 
  customer_id,
  order_date,
  order_total,
  LEAD(order_date, 1) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date
  ) as next_order_date,
  DATEDIFF(
    day, 
    order_date, 
    LEAD(order_date, 1) OVER (PARTITION BY customer_id ORDER BY order_date)
  ) as days_between_orders
FROM orders;
```

**Query 45: NTILE - Quartile analysis**
```sql
SELECT 
  customer_id,
  total_spent,
  NTILE(4) OVER (ORDER BY total_spent DESC) as quartile
FROM (
  SELECT customer_id, SUM(order_total) as total_spent
  FROM orders
  GROUP BY customer_id
) customer_totals;
```

**Query 46: ROW_NUMBER for deduplication**
```sql
WITH ranked_orders AS (
  SELECT 
    customer_id,
    order_date,
    order_total,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id 
      ORDER BY order_date DESC
    ) as rn
  FROM orders
)
SELECT customer_id, order_date, order_total
FROM ranked_orders
WHERE rn = 1;  -- Most recent order per customer
```

**Query 47: Moving average**
```sql
SELECT 
  order_date,
  daily_sales,
  AVG(daily_sales) OVER (
    ORDER BY order_date 
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as seven_day_avg
FROM (
  SELECT DATE(order_date) as order_date, SUM(order_total) as daily_sales
  FROM orders
  GROUP BY DATE(order_date)
) daily_sales;
```

**Query 48: PERCENT_RANK - Percentile calculation**
```sql
SELECT 
  product_name,
  total_sales,
  PERCENT_RANK() OVER (ORDER BY total_sales) as percentile_rank
FROM (
  SELECT product_id, SUM(quantity * unit_price) as total_sales
  FROM order_items
  GROUP BY product_id
) product_sales;
```

**Query 49: FIRST_VALUE and LAST_VALUE**
```sql
SELECT 
  customer_id,
  order_date,
  order_total,
  FIRST_VALUE(order_total) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date
  ) as first_order_value,
  LAST_VALUE(order_total) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) as last_order_value
FROM orders;
```

**Query 50: Complex window with multiple functions**
```sql
SELECT 
  product_id,
  order_date,
  daily_quantity,
  AVG(daily_quantity) OVER (
    PARTITION BY product_id 
    ORDER BY order_date 
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  ) as moving_avg_30day,
  RANK() OVER (
    PARTITION BY product_id 
    ORDER BY daily_quantity DESC
  ) as quantity_rank
FROM (
  SELECT 
    product_id,
    DATE(o.order_date) as order_date,
    SUM(oi.quantity) as daily_quantity
  FROM order_items oi
  JOIN orders o ON oi.order_id = o.order_id
  GROUP BY product_id, DATE(o.order_date)
) daily_product_sales;
```

---

### CTEs & Subqueries (10 Queries)

**Query 51: Simple CTE - Monthly sales**
```sql
WITH monthly_sales AS (
  SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(order_total) as total_sales
  FROM orders
  GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
  month,
  total_sales,
  LAG(total_sales, 1) OVER (ORDER BY month) as prev_month,
  (total_sales - LAG(total_sales, 1) OVER (ORDER BY month)) / 
    LAG(total_sales, 1) OVER (ORDER BY month) * 100 as growth_pct
FROM monthly_sales
ORDER BY month;
```

**Query 52: Multiple CTEs - Customer segmentation**
```sql
WITH customer_stats AS (
  SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_total) as total_spent,
    MAX(order_date) as last_order_date
  FROM orders
  GROUP BY customer_id
),
rfm_scores AS (
  SELECT 
    customer_id,
    DATEDIFF(day, last_order_date, GETDATE()) as recency,
    order_count as frequency,
    total_spent as monetary
  FROM customer_stats
)
SELECT 
  customer_id,
  CASE 
    WHEN recency <= 30 AND frequency >= 5 AND monetary >= 1000 THEN 'VIP'
    WHEN recency <= 60 AND frequency >= 3 THEN 'Active'
    WHEN recency <= 180 THEN 'At Risk'
    ELSE 'Churned'
  END as segment
FROM rfm_scores;
```

**Query 53: Recursive CTE - Date series**
```sql
WITH RECURSIVE date_series AS (
  SELECT DATE('2024-01-01') as date
  UNION ALL
  SELECT DATE(date, '+1 day')
  FROM date_series
  WHERE date < DATE('2024-12-31')
)
SELECT 
  ds.date,
  COALESCE(SUM(o.order_total), 0) as daily_sales
FROM date_series ds
LEFT JOIN orders o ON DATE(o.order_date) = ds.date
GROUP BY ds.date
ORDER BY ds.date;
```

**Query 54: CTE with window functions - Top N per group**
```sql
WITH ranked_products AS (
  SELECT 
    product_category,
    product_name,
    total_sales,
    RANK() OVER (PARTITION BY product_category ORDER BY total_sales DESC) as rank
  FROM (
    SELECT 
      p.product_category,
      p.product_name,
      SUM(oi.quantity * oi.unit_price) as total_sales
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_category, p.product_name
  ) sales
)
SELECT product_category, product_name, total_sales
FROM ranked_products
WHERE rank <= 5
ORDER BY product_category, rank;
```

**Query 55: Subquery in WHERE - Above average spenders**
```sql
SELECT customer_id, customer_name, total_spent
FROM (
  SELECT 
    c.customer_id,
    c.customer_name,
    SUM(o.order_total) as total_spent
  FROM customers c
  JOIN orders o ON c.customer_id = o.customer_id
  GROUP BY c.customer_id, c.customer_name
) customer_totals
WHERE total_spent > (
  SELECT AVG(total_spent)
  FROM (
    SELECT customer_id, SUM(order_total) as total_spent
    FROM orders
    GROUP BY customer_id
  ) avg_calc
);
```

**Query 56: Correlated subquery**
```sql
SELECT 
  p.product_id,
  p.product_name,
  (SELECT COUNT(*) 
   FROM order_items oi 
   WHERE oi.product_id = p.product_id) as times_ordered
FROM products p
WHERE (
  SELECT COUNT(*) 
  FROM order_items oi 
  WHERE oi.product_id = p.product_id
) > 100
ORDER BY times_ordered DESC;
```

**Query 57: EXISTS subquery**
```sql
SELECT c.customer_id, c.customer_name
FROM customers c
WHERE EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.customer_id
    AND o.order_date >= '2024-01-01'
    AND o.order_total > 1000
);
```

**Query 58: NOT EXISTS - Customers without recent orders**
```sql
SELECT c.customer_id, c.customer_name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.customer_id
    AND o.order_date >= DATEADD(month, -6, GETDATE())
);
```

**Query 59: Subquery in SELECT - Inline calculations**
```sql
SELECT 
  o.order_id,
  o.order_total,
  (SELECT AVG(order_total) FROM orders) as avg_order_value,
  o.order_total - (SELECT AVG(order_total) FROM orders) as difference_from_avg
FROM orders o
ORDER BY difference_from_avg DESC;
```

**Query 60: Complex multi-level CTE**
```sql
WITH order_summary AS (
  SELECT 
    customer_id,
    order_date,
    order_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_number
  FROM orders
),
first_orders AS (
  SELECT customer_id, order_date as first_order_date, order_total as first_order_value
  FROM order_summary
  WHERE order_number = 1
),
customer_lifetime AS (
  SELECT 
    os.customer_id,
    fo.first_order_date,
    fo.first_order_value,
    COUNT(*) as total_orders,
    SUM(os.order_total) as lifetime_value
  FROM order_summary os
  JOIN first_orders fo ON os.customer_id = fo.customer_id
  GROUP BY os.customer_id, fo.first_order_date, fo.first_order_value
)
SELECT 
  customer_id,
  first_order_date,
  first_order_value,
  total_orders,
  lifetime_value,
  lifetime_value / first_order_value as ltv_to_first_order_ratio
FROM customer_lifetime
WHERE total_orders >= 3
ORDER BY lifetime_value DESC;
```

---

### Real-World Analytics Queries (Bonus)

**Query 61: Customer Cohort Retention**
```sql
WITH cohorts AS (
  SELECT 
    customer_id,
    DATE_TRUNC('month', MIN(order_date)) as cohort_month
  FROM orders
  GROUP BY customer_id
),
cohort_activity AS (
  SELECT 
    c.cohort_month,
    DATE_TRUNC('month', o.order_date) as activity_month,
    COUNT(DISTINCT o.customer_id) as active_customers
  FROM cohorts c
  JOIN orders o ON c.customer_id = o.customer_id
  GROUP BY c.cohort_month, DATE_TRUNC('month', o.order_date)
)
SELECT 
  cohort_month,
  activity_month,
  active_customers,
  DATEDIFF(month, cohort_month, activity_month) as months_since_cohort
FROM cohort_activity
ORDER BY cohort_month, activity_month;
```

**Query 62: Product Affinity Analysis**
```sql
SELECT 
  p1.product_name as product_1,
  p2.product_name as product_2,
  COUNT(*) as times_bought_together
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
JOIN products p1 ON oi1.product_id = p1.product_id
JOIN products p2 ON oi2.product_id = p2.product_id
GROUP BY p1.product_name, p2.product_name
HAVING COUNT(*) > 10
ORDER BY times_bought_together DESC
LIMIT 20;
```

**Query 63: Sales Funnel Conversion**
```sql
SELECT 
  stage,
  user_count,
  user_count * 100.0 / FIRST_VALUE(user_count) OVER (ORDER BY stage_order) as conversion_pct
FROM (
  SELECT 1 as stage_order, 'Visited Site' as stage, COUNT(DISTINCT user_id) as user_count FROM visits
  UNION ALL
  SELECT 2, 'Viewed Product', COUNT(DISTINCT user_id) FROM product_views
  UNION ALL
  SELECT 3, 'Added to Cart', COUNT(DISTINCT user_id) FROM cart_additions
  UNION ALL
  SELECT 4, 'Started Checkout', COUNT(DISTINCT user_id) FROM checkouts
  UNION ALL
  SELECT 5, 'Completed Purchase', COUNT(DISTINCT customer_id) FROM orders
) funnel
ORDER BY stage_order;
```

---

"""
        )
    elif unit_number == 4:
        st.markdown("#### 📘 Why BI Dashboards Matter (And How to Build Great Ones)")
        st.markdown(
            """**Dashboards are how stakeholders consume your analysis.**

You can have the perfect SQL query, but if your dashboard is confusing, **nobody will use it**.

**What is a BI Dashboard?**

A Business Intelligence dashboard is a visual display of key metrics and data points,
designed to help decision-makers understand performance at a glance.

**Think:** Car dashboard
- Speedometer: How fast are you going RIGHT NOW?
- Fuel gauge: How much fuel left?
- Warning lights: Any problems?

**Business dashboard:**
- Revenue: £500K this month (vs £450K target) ✅
- Customer satisfaction: 4.2/5 (down from 4.5 last month) ⚠️
- Website traffic: 50K visitors (up 20% vs last month) ✅

**One glance = understand business health**

---

**Why Dashboards Are Crucial:**

**1. Executive Time is Limited**
- C-suite spends 5-10 minutes reviewing dashboards
- No time to read 20-page reports
- Need instant insight: "Are we OK or not?"

**2. Democratize Data**
- Non-technical stakeholders can self-serve
- No need to request custom reports
- Answer own questions through filters

**3. Drive Action**
- Red metrics = immediate investigation
- Trends = strategic planning
- Patterns = process improvements

**4. Align Teams**
- Everyone sees same metrics
- Shared understanding of priorities
- No more "what's the latest number?" emails

---

**Dashboard Design Philosophy:**

**GOOD Dashboard:**
- Answers the question: "How are we doing?"
- Immediately highlights problems
- Intuitive (no training needed)
- Actionable (drives decisions)

**BAD Dashboard:**
- Displays ALL available data
- Confusing layout
- Unclear what's good vs bad
- Just "data vomit" on screen

**Your Goal:** Design dashboards that **tell a story** and **drive action**
"""
        )

        st.markdown("#### 🎨 Dashboard Design Principles: The Rules That Separate Good from Great")
        st.markdown(
            """### 1. The 5-Second Rule

**Can someone understand your dashboard in 5 seconds?**

If not, it's too complex.

**Test:** Show dashboard to someone unfamiliar. Ask:
- "What's this about?"
- "Are we doing well or badly?"
- "What stands out?"

If they can't answer in 5 seconds, **redesign**.

---

### 2. The Inverted Pyramid (Most Important → Least Important)

**Top of dashboard:** Executive summary (3-4 key numbers)  
**Middle:** Supporting details (charts showing trends)  
**Bottom:** Detailed data (tables, filters)

**Example Layout:**

```
┌─────────────────────────────────────────┐
│ REVENUE | CUSTOMERS | SATISFACTION      │ ← Key Metrics
│ £500K   | 1,234     | 4.2/5            │
│ ↑ 12%   | ↑ 8%      | ↓ 6%    ⚠️       │
├─────────────────────────────────────────┤
│ [Revenue Trend Chart]  [Customer Chart] │ ← Visualizations
├─────────────────────────────────────────┤
│ [Detailed Table with Filters]          │ ← Details
└─────────────────────────────────────────┘
```

**Most executives only look at top section!**

---

### 3. Choose the Right Chart Type

**This is CRITICAL.** Wrong chart = confusion.

| Question | Best Chart | Why |
|----------|-----------|-----|
| "How much?" (single number) | **Big Number (KPI card)** | Immediate impact, no interpretation needed |
| "How has it changed over time?" | **Line Chart** | Shows trends, patterns, seasonality |
| "How do categories compare?" | **Bar Chart** | Easy to compare lengths |
| "What's the breakdown?" | **Pie Chart** | Shows proportions (use sparingly!) |
| "What's the distribution?" | **Histogram** | Shows data spread |
| "What's the relationship?" | **Scatter Plot** | Shows correlation |
| "What's the geographic pattern?" | **Map** | Spatial patterns visible |
| "How do 2 metrics compare over time?" | **Dual-Axis Line Chart** | Compare trends |

**Chart Selection Decision Tree:**

```
Start: What question are you answering?

├─ Comparing categories?
│  ├─ Few categories (2-7)? → BAR CHART
│  └─ Many categories (8+)? → TABLE or GROUPED BAR CHART
│
├─ Showing trend over time?
│  ├─ One metric? → LINE CHART
│  └─ Multiple metrics? → MULTI-LINE CHART or AREA CHART
│
├─ Showing composition (parts of whole)?
│  ├─ At one point in time? → PIE CHART (if 2-5 slices) or BAR CHART
│  └─ Over time? → STACKED AREA CHART
│
└─ Showing relationship between variables?
   └─ → SCATTER PLOT
```

---

### 4. Use Color Purposefully

**Color Rules:**

**GREEN = Good** (above target, positive)  
**RED = Bad** (below target, negative, warning)  
**AMBER/YELLOW = Caution** (approaching threshold)  
**GREY/BLUE = Neutral** (informational)

**Example: Sales Dashboard**

```
Revenue: £500K (+12%) [GREEN background]
Profit:  £50K  (-5%)  [RED background]
Costs:   £450K (+8%)  [AMBER background]
```

**Mistakes to Avoid:**

❌ Using color just because it's pretty  
❌ Red/green for non-performance data (accessibility issue!)  
❌ Too many colors (rainbow dashboard = confusion)  
✅ Limit to 3-4 colors maximum  
✅ Consider color-blind users (use patterns too)

---

### 5. Reduce Cognitive Load

**Every element on dashboard requires mental energy to process.**

**Minimize:**
- Gridlines (use sparingly)
- Borders (only if needed)
- 3D effects (NEVER use these)
- Shadows and gradients
- Decorative elements
- Unnecessary labels

**Maximize:**
- White space (breathing room)
- Clear titles
- Data-to-ink ratio (more data, less decoration)

**Before (Bad):**
```
┌──────────────────────────┐
│ Sales by Region 📊      │
│ ┌────────────────┐      │
│ │░░░░░░░░░░░░░░░│      │ ← Heavy gridlines
│ │░░North░░░░░░░│      │ ← 3D effects
│ │░░░░░░░░░░░░░░░│      │ ← Gradients
│ └────────────────┘      │
│ [Complex Legend]        │ ← Too much text
└──────────────────────────┘
```

**After (Good):**
```
┌──────────────────────────┐
│ Sales by Region         │
│                         │
│ North  ████████ £200K  │ ← Clean bars
│ South  ██████ £150K    │ ← Direct labels
│ East   ████ £100K      │
│                         │
└──────────────────────────┘
```

---

### 6. Make It Actionable

**Every dashboard should answer: "So what should I do?"**

**Add:**
- Targets/goals (so viewers know what's good)
- Comparisons (vs last month, vs plan, vs benchmark)
- Context (why did this change?)
- Recommendations (what action to take)

**Example:**

**Bad Dashboard:**
```
Revenue: £500K
```

**Good Dashboard:**
```
Revenue: £500K
Target: £450K ✅ (+11% vs target)
Last Month: £470K ↑
Recommendation: Maintain current marketing spend
```

Now stakeholder knows:
1. Current state (£500K)
2. Is it good? (Yes, above target)
3. Trend direction (Up from last month)
4. What to do (Keep doing what we're doing)

---

### 7. Design for Your Audience

**Different audiences need different dashboards:**

**Executive Dashboard:**
- 3-5 key metrics maximum
- High-level trends
- Red/yellow/green indicators
- No detail tables
- Mobile-friendly

**Manager Dashboard:**
- 8-12 metrics
- Ability to filter by team/region
- Drill-down capability
- Week-over-week comparisons
- Some detail available

**Analyst Dashboard:**
- 15+ metrics
- Raw data tables
- Export functionality
- Multiple filters
- Technical detail OK

**Don't try to make one dashboard serve all audiences!**
"""
        )

        st.markdown("#### 📖 Data Storytelling: Making Numbers Memorable")
        st.markdown(
            """**Data doesn't speak for itself. You need to tell the story.**

**Why Storytelling Matters:**

Humans remember:
- 10% of statistics
- 65% of stories

**Your job:** Wrap data in narrative so people remember AND act.

---

### The Data Story Structure

**Every good data story has 3 parts:**

**1. SETUP (Context)**
- What's the situation?
- Why does this matter?
- What question are we answering?

**2. CONFLICT (The Finding)**
- What did the data show?
- Was it expected or surprising?
- What changed?

**3. RESOLUTION (The Action)**
- What does this mean?
- What should we do?
- What happens if we don't act?

---

### Example: Bad vs Good Data Presentation

**BAD (Just Numbers):**

"DNA rate is 15%. Last month was 12%. Dermatology is 18%."

*No story, no action, forgettable*

---

**GOOD (With Story):**

**"We have a growing problem with missed appointments, and it's costing us."**

SETUP:
"Our DNA (Did Not Attend) rate has increased from 12% to 15% over the past month. At our current volume of 10,000 appointments per month, that's 300 wasted appointment slots—equivalent to £30,000 in lost revenue."

CONFLICT:
"What's driving this? I analyzed by specialty and found Dermatology is the outlier at 18% DNA rate, compared to 12-14% for other specialties. When I looked at appointment types, NEW patient appointments have 22% DNA rate vs 10% for follow-ups."

RESOLUTION:
"Here's what I recommend:
1. Implement SMS reminders specifically for Dermatology new patients (evidence shows this reduces DNA by 30-40%)
2. Trial this for 1 month
3. Expected impact: Save 60 appointment slots, £6,000 revenue
4. Cost: £200 for SMS service
5. ROI: 30x

Can I proceed with implementing this?"

---

### Storytelling Techniques

**1. Start with the Punchline**

Don't bury the lead. State conclusion FIRST.

❌ "I analyzed 10,000 appointments across 5 specialties over 3 months..."  
✅ "We can save £30K/month by fixing our appointment reminder system."

**2. Use Concrete Numbers, Not Percentages**

Percentages are abstract. Convert to tangible impact.

❌ "Sales increased 15%"  
✅ "Sales increased 15%, bringing in an extra £75,000 this quarter—enough to hire 2 new team members"

**3. Compare to Familiar Reference Points**

Make scale understandable.

❌ "We process 10TB of data"  
✅ "We process 10TB of data—equivalent to 2.5 million songs or 2,000 hours of HD video"

**4. Show Before/After**

Visual contrast drives home the change.

```
BEFORE: [Chart showing declining trend]
AFTER:  [Chart showing recovery]

"After implementing the new process, we reversed the declining trend and exceeded our target by 20%."
```

**5. Use Analogies**

Make complex concepts accessible.

❌ "Our churn rate is 5% monthly"  
✅ "Our churn rate is 5% monthly—imagine a bucket with a leak. We're adding customers through the top, but losing 5% through a hole at the bottom. We need to patch that leak."

---

### The "So What?" Test

For every chart/number in your presentation, ask:

**"So what?"**

If you can't answer clearly, **remove it.**

**Example:**

**Data Point:** "Website traffic increased 20%"

**So what?** "More potential customers are finding us"

**So what?** "This should lead to more sales"

**So what?** "We need to ensure our sales team is ready to handle increased leads"

**So what?** "I recommend hiring 1 additional sales rep to handle 40% more lead volume"

**NOW it's actionable!**

---

### Presenting to Different Audiences

**To Executives:**
- Lead with business impact (revenue, cost, risk)
- Keep it to 3 key points
- Have backup slides for questions
- End with clear recommendation
- Time limit: 5-10 minutes

**To Technical Teams:**
- Show methodology
- Explain assumptions
- Include statistical tests
- Share code/queries if relevant
- Time limit: 20-30 minutes

**To Cross-Functional Teams:**
- Use simple language (no jargon)
- Heavy on visuals
- Interactive (get input)
- Focus on practical implications
- Time limit: 15-20 minutes

---

### Common Storytelling Mistakes

❌ **Data Dump**
Showing every analysis you did instead of the key insights

✅ **FIX:** Show 3 key findings, put rest in appendix

❌ **No Clear Conclusion**
Presenting data but expecting audience to figure out what it means

✅ **FIX:** Explicitly state "What this means is..." and "My recommendation is..."

❌ **Too Many Caveats**
"This might not be accurate because X, Y, Z..."

✅ **FIX:** Acknowledge limitations but don't undermine your findings

❌ **Boring Titles**
"Sales Analysis Q3 2024"

✅ **FIX:** "Q3 Sales Exceeded Target by 15% Due to New Email Campaign"

---

### Your Data Story Template

Use this for any analysis presentation:

**SLIDE 1: The Hook**
- One sentence: Why this matters
- One visual: Showing the problem or opportunity

**SLIDE 2: The Context**
- What question were we trying to answer?
- Why is this important now?
- Brief methodology note

**SLIDE 3-4: The Findings**
- Key finding #1 (with visual)
- Key finding #2 (with visual)
- Key finding #3 (with visual)

**SLIDE 5: So What?**
- What does this mean for the business?
- What's the impact if we do nothing?

**SLIDE 6: Recommendations**
- Specific action #1 (with owner and timeline)
- Specific action #2 (with owner and timeline)
- Expected outcomes

**SLIDE 7: Next Steps**
- Decision needed today
- Follow-up actions
- How you'll measure success

**TOTAL: 7 slides, 10-minute presentation**

---

### Practice Exercise

Take this raw data and turn it into a story:

**DATA:**
- Customer satisfaction score: 3.8/5 (was 4.2 last quarter)
- Support ticket volume: Up 40%
- Average resolution time: 48 hours (was 24 hours)
- Top complaint: "Slow response times"

**YOUR TASK:** Write a 1-paragraph story using the SETUP-CONFLICT-RESOLUTION structure.

**EXAMPLE ANSWER:**

"We're at risk of losing customers due to deteriorating support experience. **(SETUP: Stakes established)** 

Our customer satisfaction has dropped from 4.2 to 3.8 in one quarter while support tickets increased 40% and resolution time doubled to 48 hours. The root cause is clear: we're understaffed for current ticket volume. **(CONFLICT: Problem diagnosed)** 

I recommend immediately hiring 2 additional support agents (£60K cost) to handle increased volume. This should restore 24-hour resolution times and satisfaction to 4.2+ within 2 months. The alternative—continued decline—could cost us 10-15% of customers (£200K+ annual revenue impact). **(RESOLUTION: Clear action and consequences)**"

**See how data becomes a compelling story?**
"""
        )

        st.markdown("---")
        st.markdown("## 🔬 HANDS-ON LABS - Unit 4: BI Dashboards & Visualization")
        st.markdown(
            """**Practical exercises to master business intelligence tools**

### LAB 1: Tableau Fundamentals

**Objective:** Build your first interactive Tableau dashboard

**Scenario:** Create sales performance dashboard for RetailCo

**Dataset:** `sales_data_2024.csv` (50K rows)
- Columns: Date, Region, Product_Category, Product_Name, Sales_Rep, Revenue, Units, Profit

**Step 1: Connect to Data**
```
1. Open Tableau Desktop
2. Connect to Text File → Browse to sales_data_2024.csv
3. Data Source tab: Review fields and data types
4. Click "Sheet 1" to start building
```

**Step 2: Build First Visualization - Revenue Trend**
```
Drag to:
- Columns: MONTH(Date)
- Rows: SUM(Revenue)
- Color: Profit Ratio (calculated field: SUM(Profit)/SUM(Revenue))
- Label: Show marks

Result: Line chart showing monthly revenue with profit ratio colors
```

**Step 3: Regional Performance Bar Chart**
```
New Sheet:
- Rows: Region
- Columns: SUM(Revenue)
- Color: Region
- Sort: Descending by revenue
- Add reference line at Average

Insight: Instantly see which regions over/under perform
```

**Step 4: Product Category Breakdown**
```
New Sheet:
- Create treemap: Product_Category to Color and Size
- Size: SUM(Revenue)
- Label: Category name and % of total
- Tooltip: Add Profit, Units Sold

Result: Visual hierarchy of category performance
```

**Step 5: Sales Rep Leaderboard**
```
New Sheet - Table:
- Rows: Sales_Rep
- Columns: SUM(Revenue), COUNT(Orders), AVG(Deal Size)
- Conditional formatting:
  * Revenue: Color scale (green = high)
  * Orders: Data bars
- Sort by Revenue descending
```

**Step 6: Build Interactive Dashboard**
```
New Dashboard:

Layout (1200 x 800 pixels):
+----------------------------------+------------------+
| Revenue Trend (full width)                          |
+----------------------------------+------------------+
| Regional Performance | Product Treemap             |
| (50% width)          | (50% width)                 |
+----------------------------------+------------------+
| Sales Rep Leaderboard (full width)                 |
+----------------------------------+------------------+

Add Interactivity:
1. Make Region chart a filter
2. Add date range filter (slider)
3. Add Product Category quick filter
4. All sheets respond to filters
```

**Step 7: Dashboard Actions**
```
Dashboard → Actions:
1. Highlight action: Hover over region highlights related data
2. Filter action: Click region filters entire dashboard
3. URL action: Click sales rep opens email
```

**Step 8: Calculated Fields**
```
Create:
1. Profit Margin = SUM([Profit]) / SUM([Revenue])
2. YoY Growth = (SUM([Revenue]) - LOOKUP(SUM([Revenue]), -12)) / LOOKUP(SUM([Revenue]), -12)
3. Running Total = RUNNING_SUM(SUM([Revenue]))
4. Rank = RANK(SUM([Revenue]))
```

**Deliverable:**
- Published Tableau workbook (.twbx)
- Dashboard screenshot
- 1-page insights summary

**Time:** 4-5 hours  
**Success Criteria:**
- ✅ 4+ visualizations created
- ✅ Interactive filters working
- ✅ Dashboard tells clear story
- ✅ Professional formatting

---

### LAB 2: Advanced Tableau Techniques

**Objective:** Master advanced Tableau features

**Challenge 1: Dual-Axis Charts**
```
Create chart showing Revenue (bars) and Profit Margin (line):
1. Rows: SUM(Revenue), Profit Margin
2. Right-click second pill → Dual Axis
3. Synchronize axis
4. Change mark type: Bars for revenue, Line for margin
5. Format: Different colors, adjust scales
```

**Challenge 2: Parameter Controls**
```
Create dynamic metric selector:

1. Create Parameter: "Select Metric"
   - Data type: String
   - Allowable values: List
   - Values: Revenue, Profit, Units, Margin

2. Create Calculated Field: "Selected Metric"
   CASE [Select Metric]
   WHEN 'Revenue' THEN SUM([Revenue])
   WHEN 'Profit' THEN SUM([Profit])
   WHEN 'Units' THEN SUM([Units])
   WHEN 'Margin' THEN AVG([Profit])/AVG([Revenue])
   END

3. Use in visualization
4. Show parameter control
5. Users can switch metrics dynamically!
```

**Challenge 3: Level of Detail (LOD) Expressions**
```
Calculate customer-level metrics:

1. Customer Lifetime Value:
   {FIXED [Customer_ID] : SUM([Revenue])}

2. First Purchase Date:
   {FIXED [Customer_ID] : MIN([Order_Date])}

3. Cohort Analysis:
   DATEDIFF('month', {FIXED [Customer_ID] : MIN([Order_Date])}, [Order_Date])

4. Customer Count by Cohort:
   {FIXED [Cohort_Month] : COUNTD([Customer_ID])}
```

**Challenge 4: Table Calculations**
```
Advanced calculations:

1. Percent of Total:
   SUM([Revenue]) / TOTAL(SUM([Revenue]))

2. Difference from Average:
   SUM([Revenue]) - WINDOW_AVG(SUM([Revenue]))

3. Moving Average (7-day):
   WINDOW_AVG(SUM([Revenue]), -6, 0)

4. Year-over-Year:
   (SUM([Revenue]) - LOOKUP(SUM([Revenue]), -12)) / LOOKUP(SUM([Revenue]), -12)
```

**Challenge 5: Dashboard Actions & Storytelling**
```
Create 3-page story:

Page 1: "The Problem"
- Show declining metrics
- Highlight concerning trends
- Add annotations

Page 2: "Root Cause Analysis"  
- Drill-down visualizations
- Regional/product breakdowns
- Filter to problem areas

Page 3: "Recommendations"
- Forecasts with trend lines
- What-if scenarios
- Action items
```

**Deliverable:**
- Advanced dashboard with LOD calcs
- Story points presentation
- Documentation of techniques

**Time:** 5-6 hours

---

### LAB 3: Power BI Fundamentals

**Objective:** Build interactive Power BI report

**Scenario:** Customer analytics dashboard for SaaS company

**Step 1: Load and Transform Data**
```
Power Query:
1. Get Data → Import sales_data.csv
2. Transform:
   - Remove duplicates
   - Change data types
   - Add custom column: Revenue_Category
   - Filter out nulls
3. Close & Apply
```

**Step 2: Data Modeling**
```
Model View:
1. Create relationships:
   - Sales[Customer_ID] → Customers[Customer_ID]
   - Sales[Product_ID] → Products[Product_ID]
   - Sales[Date] → Calendar[Date]

2. Create Calendar table:
   Calendar = CALENDAR(MIN(Sales[Date]), MAX(Sales[Date]))

3. Add calculated columns:
   Month = FORMAT(Calendar[Date], "MMM YYYY")
   Quarter = "Q" & QUARTER(Calendar[Date])
```

**Step 3: DAX Measures**
```
Create measures:

Total Revenue = SUM(Sales[Revenue])

Total Customers = DISTINCTCOUNT(Sales[Customer_ID])

Average Order Value = DIVIDE([Total Revenue], COUNTROWS(Sales))

Revenue YoY = 
VAR CurrentYear = [Total Revenue]
VAR PriorYear = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Calendar[Date]))
RETURN DIVIDE(CurrentYear - PriorYear, PriorYear)

Customer Retention = 
VAR CustomersThisMonth = DISTINCTCOUNT(Sales[Customer_ID])
VAR CustomersLastMonth = CALCULATE(
    DISTINCTCOUNT(Sales[Customer_ID]),
    DATEADD(Calendar[Date], -1, MONTH)
)
VAR ReturningCustomers = CALCULATE(
    DISTINCTCOUNT(Sales[Customer_ID]),
    FILTER(Sales, Sales[Customer_ID] IN VALUES(Sales[Customer_ID]))
)
RETURN DIVIDE(ReturningCustomers, CustomersLastMonth)
```

**Step 4: Build Visualizations**
```
Page 1: Executive Summary
- Card visuals: Revenue, Customers, AOV (with YoY change)
- Line chart: Monthly trend
- Bar chart: Revenue by category
- Donut chart: Customer segments

Page 2: Product Analysis
- Matrix: Products with revenue, units, margin
- Scatter plot: Units vs Revenue (bubble = profit)
- Decomposition tree: Category → Product → Region

Page 3: Customer Insights
- Cohort retention heatmap
- Customer lifetime value distribution
- Top customers table
- Churn risk indicators
```

**Step 5: Add Interactivity**
```
Slicers:
- Date range slicer
- Region multi-select
- Product category

Cross-filtering:
- Enable cross-highlight between visuals
- Set filter direction (both/single)

Drill-through:
- Right-click → Drill through to detailed view
- Create drill-through page with customer details
```

**Step 6: Format & Polish**
```
Formatting:
- Apply consistent theme
- Custom colors matching brand
- Conditional formatting on tables
- Add icons and images
- Tooltips with additional context
```

**Deliverable:**
- Power BI .pbix file
- Published to Power BI Service
- Sharing link for stakeholders

**Time:** 4-5 hours  
**Success Criteria:**
- ✅ Data properly modeled
- ✅ DAX measures working
- ✅ Interactive and polished
- ✅ Mobile-friendly layout

---

### LAB 4: Data Visualization Best Practices

**Objective:** Learn what makes visualizations effective

**Exercise 1: Chart Selection**
```
Choose the right chart for each scenario:

Scenario A: Compare sales across 5 regions
❌ Pie chart (hard to compare slices)
✅ Bar chart (easy comparison)

Scenario B: Show trend over 24 months
❌ Scatter plot (implies relationship)
✅ Line chart (shows time series)

Scenario C: Show distribution of order values
❌ Line chart (not a trend)
✅ Histogram (shows distribution)

Scenario D: Compare 3 metrics across 10 products
❌ Pie chart (too many categories)
✅ Grouped bar chart or heat map

Scenario E: Show relationship between ad spend and sales
❌ Bar chart (doesn't show correlation)
✅ Scatter plot with trendline
```

**Exercise 2: Color Best Practices**
```
Fix these common mistakes:

❌ BAD: Rainbow colors for categories (hard to distinguish)
✅ GOOD: Distinct, accessible colors (max 6-7)

❌ BAD: Red/green for non-performance data (colorblind issues)
✅ GOOD: Blue/orange or use patterns

❌ BAD: Every element bright colored
✅ GOOD: Gray for reference, color for emphasis

❌ BAD: Legend with 15 colors
✅ GOOD: Direct labels, max 5-6 categories

Color Palette Rules:
- Sequential: Single hue (light to dark) for ordered data
- Diverging: Two hues from neutral for positive/negative
- Categorical: Distinct hues for unordered categories
- Always test for colorblind accessibility
```

**Exercise 3: Declutter & Simplify**
```
Before (Cluttered):
- Heavy gridlines
- 3D effects
- Multiple borders
- Excessive labels
- Busy background
- Too many metrics

After (Clean):
- Minimal gridlines (or none)
- Flat 2D design
- Single border or none
- Selective labeling
- White/light background
- Focus on 1-3 key metrics

Data-Ink Ratio: Maximize data, minimize decoration
```

**Exercise 4: Dashboard Layout Principles**
```
Z-Pattern Reading:
+------------------+------------------+
| Most Important   | Secondary Metric |
| (Top Left)       | (Top Right)      |
+------------------+------------------+
| Supporting Chart | Supporting Chart |
| (Mid Left)       | (Mid Right)      |
+------------------+------------------+
| Details/Actions  | Details/Actions  |
| (Bottom)         | (Bottom)         |
+------------------+------------------+

Design Rules:
1. Top-left gets most attention
2. Use whitespace generously
3. Group related items
4. Align elements in grid
5. Consistent sizing
6. Limit to 5-7 visuals per page
```

**Exercise 5: Storytelling with Data**
```
Structure your dashboard as a story:

1. HEADLINE (Big Number)
   "Revenue DOWN 12% vs Target"
   
2. CONTEXT (Trend Chart)
   Shows decline started in Q2
   
3. DIAGNOSIS (Breakdown)
   North region down 25%
   Electronics category struggling
   
4. ACTION (Recommendation)
   "Focus sales efforts on North region"
   "Review Electronics pricing strategy"

Each visual should answer a question:
- What happened?
- Why did it happen?
- What should we do?
```

**Exercise 6: Rebuild Bad Visualizations**
```
You'll be given 5 "bad" dashboards:
1. Pie chart with 20 slices → Fix with treemap or bar chart
2. 3D donut chart → Fix with simple bar chart
3. Dual-axis with different scales → Fix properly
4. Table with 50 rows → Fix with top 10 + others
5. Rainbow color dashboard → Fix with consistent palette

Document your fixes and rationale
```

**Deliverable:**
- Portfolio of before/after visualizations
- Style guide document
- Dashboard design checklist

**Time:** 3-4 hours

---

### MINI PROJECT 5: Executive BI Dashboard

**Objective:** Build complete executive dashboard from scratch

**Scenario:** Quarterly Business Review dashboard for CEO

**Requirements:**

**1. Data Preparation**
```
Sources to integrate:
- Sales data (50K transactions)
- Customer data (10K customers)
- Product data (500 products)
- Marketing spend data
- Website analytics

Transformations needed:
- Join all sources
- Calculate KPIs
- Create calendar dimension
- Clean and validate
```

**2. Key Metrics to Display**
```
Financial:
- Total Revenue (vs target, vs last quarter)
- Profit Margin %
- Average Order Value
- Revenue by region/product

Customer:
- Total Active Customers
- Customer Acquisition Cost
- Customer Lifetime Value
- Retention Rate %
- Net Promoter Score

Operations:
- Orders Processed
- Average Delivery Time
- Return Rate %
- Inventory Turnover
```

**3. Dashboard Pages**
```
Page 1: Executive Summary (1 screen, no scrolling)
- 6 KPI cards with sparklines
- Revenue trend (12 months)
- Top 5 products bar chart
- Regional map
- Alert indicators (red/yellow/green)

Page 2: Sales Deep Dive
- Sales by channel
- Rep leaderboard
- Deal pipeline
- Win rate analysis
- Forecasting

Page 3: Customer Analytics
- Cohort retention heatmap
- Customer segmentation
- Churn analysis
- Lifetime value distribution

Page 4: Product Performance
- Category breakdown
- Inventory status
- Profitability analysis
- Top/bottom performers
```

**4. Interactivity Requirements**
```
Filters:
- Date range (with quick filters: MTD, QTD, YTD)
- Region multi-select
- Product category
- Customer segment

Actions:
- Click region → filter entire report
- Hover → show detailed tooltip
- Drill down: Region → State → City
- Drill through: Product → Product details page
```

**5. Advanced Features**
```
Implement:
- Dynamic titles based on filters
- Conditional formatting (rules-based)
- Reference lines (target, average, benchmark)
- Trend indicators (↑ ↓ with % change)
- Alert icons for metrics below threshold
- What-if analysis (parameter for target adjustment)
- Forecast with confidence intervals
```

**6. Mobile Version**
```
Create mobile-optimized layout:
- Single column
- Larger touch targets
- Simplified visuals
- Priority metrics only
- Works on phone/tablet
```

**Deliverable:**
- Complete Tableau or Power BI workbook
- Published to BI platform
- User guide (1-page)
- Video walkthrough (5 min)
- Executive presentation deck

**Time:** 10-12 hours  
**Success Criteria:**
- ✅ Professional, polished appearance
- ✅ Loads in <5 seconds
- ✅ All metrics accurate
- ✅ Mobile-friendly
- ✅ Stakeholder approved

---

### Visualization Resources

**Tools to Practice:**
- Tableau Public (free)
- Power BI Desktop (free)
- Google Data Studio (free)
- Looker Studio (free)

**Sample Datasets:**
- Superstore Sales (Tableau sample)
- AdventureWorks (Microsoft sample)
- Kaggle datasets (retail, finance, healthcare)

**Learning Resources:**
- Tableau Public Gallery (inspiration)
- Power BI Community
- Information is Beautiful (design inspiration)
- FlowingData blog

**Color Tools:**
- ColorBrewer (accessible palettes)
- Adobe Color (palette generator)
- Viz Palette (visualization-specific)

**Success Criteria for Unit 4:**
- ✅ Build professional Tableau dashboards
- ✅ Create Power BI reports with DAX
- ✅ Apply visualization best practices
- ✅ Tell compelling stories with data
- ✅ Portfolio-ready BI projects

"""
        )
    elif unit_number == 5:
        st.markdown("#### 📘 Python for Analysts: When and Why to Level Up")
        st.markdown(
            """**Python isn't replacing Excel or SQL—it's complementing them.**

As an analyst, you'll continue using Excel and SQL daily. Python is your **power tool** for tasks they can't handle.

---

**When Excel/SQL Aren't Enough:**

**1. Dataset Size**
- Excel limit: 1,048,576 rows
- Your data: 10 million rows
- **Solution: Python (handles billions of rows)**

**2. Repetitive Tasks**
- Weekly report: Same steps every time
- Excel: Manual clicks (20 minutes)
- **Solution: Python script (30 seconds, automated)**

**3. Complex Transformations**
- Need to apply ML model predictions
- Need to call external APIs
- Need advanced text processing
- **Solution: Python (unlimited capability)**

**4. Version Control & Collaboration**
- Excel: "Final_v2_ACTUAL_USE_THIS.xlsx"
- **Python: Git version control, code reviews**

**5. Reproducibility**
- Excel: "How did you calculate this?"
- **Python: Code documents every step**

---

**Real-World Example:**

**TASK:** Generate weekly sales report
- Pull data from SQL database
- Clean and transform data
- Calculate complex metrics
- Create visualizations
- Email report to 20 stakeholders

**Excel Approach:** 45 minutes of manual work every week  
**Python Approach:** 5 minutes to write script once, then 30 seconds to run weekly

**Time saved:** 44.5 minutes × 52 weeks = **38 hours per year**

---

**The Analyst's Tech Stack:**

```
Excel:  Quick analysis, sharing with non-technical stakeholders
SQL:    Getting data from databases  
Python: Heavy processing, automation, advanced analysis
BI Tools: Dashboards and monitoring

ALL work together!
```

**You're not choosing one—you're mastering all four.**

---

**Common Misconception:**

"I need to be a programmer to use Python."

**FALSE.** You need to know:
- How to load data
- How to filter and transform
- How to calculate summaries
- How to make charts

That's it. You don't need to build web apps or AI models (unless you want to!).

**Analyst Python ≠ Software Engineer Python**
"""
        )

        st.markdown("#### 🐼 Pandas: Excel on Steroids")
        st.markdown(
            """**Pandas is Python's data analysis library. Think of it as programmable Excel.**

### What is Pandas?

**Pandas provides two main data structures:**

**1. Series** (like a single Excel column)
```python
import pandas as pd

ages = pd.Series([25, 30, 35, 40])
```

**2. DataFrame** (like an Excel spreadsheet)
```python
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob', 'Alice'],
    'age': [25, 30, 35, 40],
    'salary': [50000, 60000, 55000, 70000]
})
```

**Output:**
```
    name  age  salary
0   John   25   50000
1   Jane   30   60000
2    Bob   35   55000
3  Alice   40   70000
```

---

### Loading Data

**From CSV:**
```python
df = pd.read_csv('sales_data.csv')
```

**From Excel:**
```python
df = pd.read_excel('sales_data.xlsx', sheet_name='Sheet1')
```

**From SQL:**
```python
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql_query("SELECT * FROM sales", conn)
```

**From Clipboard** (quick copy-paste from Excel):
```python
df = pd.read_clipboard()
```

---

### First Steps: Exploring Your Data

**See first 5 rows:**
```python
df.head()
```

**See last 5 rows:**
```python
df.tail()
```

**Get basic info:**
```python
df.info()
# Shows: column names, data types, non-null counts
```

**Get statistics:**
```python
df.describe()
# Shows: count, mean, std, min, max, quartiles
```

**See column names:**
```python
df.columns
# Output: ['name', 'age', 'salary']
```

**See shape (rows, columns):**
```python
df.shape
# Output: (4, 3)  → 4 rows, 3 columns
```

---

### Selecting Data

**Select single column:**
```python
df['salary']  # Returns Series
df[['salary']]  # Returns DataFrame (keeps 2D structure)
```

**Select multiple columns:**
```python
df[['name', 'salary']]
```

**Select rows by position:**
```python
df.iloc[0]  # First row
df.iloc[0:3]  # First 3 rows
```

**Select rows by condition** (filtering):
```python
# Filter: salary > 55000
df[df['salary'] > 55000]

# Multiple conditions
df[(df['salary'] > 55000) & (df['age'] < 40)]
```

**Equivalent to SQL:**
```sql
SELECT * FROM df 
WHERE salary > 55000 AND age < 40
```

---

### Common Data Operations

**1. Adding New Columns** (calculated fields)

```python
# Add bonus column (10% of salary)
df['bonus'] = df['salary'] * 0.10

# Add total compensation
df['total_comp'] = df['salary'] + df['bonus']
```

**2. Renaming Columns**

```python
df = df.rename(columns={'name': 'employee_name', 'salary': 'annual_salary'})
```

**3. Sorting**

```python
# Sort by salary (ascending)
df.sort_values('salary')

# Sort by salary (descending)
df.sort_values('salary', ascending=False)

# Sort by multiple columns
df.sort_values(['age', 'salary'], ascending=[True, False])
```

**4. Removing Duplicates**

```python
df = df.drop_duplicates()

# Remove duplicates based on specific column
df = df.drop_duplicates(subset=['employee_id'])
```

**5. Handling Missing Values**

```python
# Check for missing values
df.isnull().sum()

# Drop rows with ANY missing values
df = df.dropna()

# Drop rows where specific column is missing
df = df.dropna(subset=['salary'])

# Fill missing values
df['salary'] = df['salary'].fillna(0)  # Fill with 0
df['salary'] = df['salary'].fillna(df['salary'].mean())  # Fill with average
```

---

### Aggregations (GROUP BY in Pandas)

**SQL Equivalent:**
```sql
SELECT department, AVG(salary), COUNT(*)
FROM employees
GROUP BY department
```

**Pandas:**
```python
df.groupby('department').agg({
    'salary': 'mean',
    'employee_id': 'count'
})
```

**Common Aggregation Functions:**
- `sum()` - Total
- `mean()` - Average
- `count()` - Count
- `min()` / `max()` - Min/Max
- `std()` - Standard deviation
- `nunique()` - Count unique values

**Multiple Aggregations:**
```python
df.groupby('department')['salary'].agg(['mean', 'min', 'max', 'count'])
```

**Output:**
```
             mean    min    max  count
department                            
Sales       55000  50000  60000      5
Marketing   58000  52000  65000      4
IT          70000  65000  80000      6
```

---

### Joining DataFrames (Like SQL JOINs)

**Two DataFrames:**
```python
employees = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'name': ['John', 'Jane', 'Bob']
})

salaries = pd.DataFrame({
    'emp_id': [1, 2, 4],
    'salary': [50000, 60000, 55000]
})
```

**Inner Join** (only matching rows):
```python
result = employees.merge(salaries, on='emp_id', how='inner')
```

**Left Join** (keep all from left):
```python
result = employees.merge(salaries, on='emp_id', how='left')
```

**SQL Equivalent:**
```sql
SELECT * FROM employees e
LEFT JOIN salaries s ON e.emp_id = s.emp_id
```

---

### Real-World Example: Sales Analysis

```python
import pandas as pd

# Load data
sales = pd.read_csv('sales_data.csv')

# Check data
print(sales.head())
print(sales.info())

# Clean data
sales = sales.drop_duplicates()
sales = sales.dropna(subset=['revenue'])

# Add calculated field
sales['profit'] = sales['revenue'] - sales['cost']

# Filter to recent data
sales_2024 = sales[sales['date'] >= '2024-01-01']

# Group by product category
summary = sales_2024.groupby('category').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'order_id': 'count'
}).rename(columns={'order_id': 'num_orders'})

# Sort by revenue
summary = summary.sort_values('revenue', ascending=False)

# Calculate profit margin
summary['profit_margin'] = (summary['profit'] / summary['revenue']) * 100

# Save results
summary.to_csv('sales_summary_2024.csv')
print("Analysis complete!")
```

**This replaces 30+ minutes of Excel work with a 30-second script.**
"""
        )

        st.markdown("#### 📊 Data Visualization in Python")
        st.markdown(
            """**Python creates publication-quality charts programmatically.**

### Three Main Libraries

**1. Matplotlib** - Basic, fully customizable  
**2. Seaborn** - Beautiful statistical plots  
**3. Plotly** - Interactive dashboards

**For analysts, Seaborn is usually best** (built on Matplotlib, better defaults).

---

### Basic Plotting with Pandas

**Line Chart** (trend over time):
```python
import matplotlib.pyplot as plt

df.plot(x='date', y='revenue', kind='line')
plt.title('Revenue Over Time')
plt.xlabel('Date')
plt.ylabel('Revenue (£)')
plt.show()
```

**Bar Chart** (comparing categories):
```python
df.plot(x='category', y='sales', kind='bar')
plt.title('Sales by Category')
plt.show()
```

**Histogram** (distribution):
```python
df['age'].plot(kind='hist', bins=20)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.show()
```

---

### Seaborn for Better Visuals

```python
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Bar plot with error bars
sns.barplot(data=df, x='category', y='revenue', ci=95)
plt.title('Average Revenue by Category')
plt.show()

# Box plot (shows distribution)
sns.boxplot(data=df, x='category', y='salary')
plt.title('Salary Distribution by Category')
plt.show()

# Heatmap (correlation matrix)
correlation = df[['revenue', 'cost', 'profit']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Scatter plot with regression line
sns.regplot(data=df, x='marketing_spend', y='revenue')
plt.title('Marketing Spend vs Revenue')
plt.show()
```

---

### When to Use Python vs Excel Charts

**Use Excel Charts When:**
- Sharing with non-technical stakeholders
- One-off analysis
- Simple bar/line charts
- Need to embed in PowerPoint

**Use Python Charts When:**
- Automating weekly reports
- Creating complex multi-panel figures
- Statistical visualizations (confidence intervals, distributions)
- Need reproducibility
- Publishing/research quality needed

---

### Automated Report Example

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
sales = pd.read_csv('sales_data.csv')

# Create figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(f'Weekly Sales Report - {datetime.now().strftime("%Y-%m-%d")}', 
             fontsize=16)

# Plot 1: Revenue trend
sales.groupby('date')['revenue'].sum().plot(ax=axes[0,0])
axes[0,0].set_title('Daily Revenue Trend')
axes[0,0].set_ylabel('Revenue (£)')

# Plot 2: Top products
top_products = sales.groupby('product')['revenue'].sum().nlargest(10)
top_products.plot(kind='barh', ax=axes[0,1])
axes[0,1].set_title('Top 10 Products by Revenue')

# Plot 3: Sales by category
sns.barplot(data=sales, x='category', y='revenue', ax=axes[1,0])
axes[1,0].set_title('Revenue by Category')
axes[1,0].tick_params(axis='x', rotation=45)

# Plot 4: Profit margin distribution
sales['profit_margin'] = (sales['profit'] / sales['revenue']) * 100
sns.histplot(sales['profit_margin'], bins=30, ax=axes[1,1])
axes[1,1].set_title('Profit Margin Distribution')
axes[1,1].set_xlabel('Profit Margin (%)')

# Adjust layout and save
plt.tight_layout()
plt.savefig(f'weekly_report_{datetime.now().strftime("%Y%m%d")}.png', dpi=300)
print("Report generated!")
```

**Run this script every Monday = Instant professional report.**

---

### Python + SQL + Excel Workflow

**The Complete Analyst Workflow:**

```python
# 1. Get data from SQL
import pandas as pd
import sqlite3

conn = sqlite3.connect('company_db.db')
query = """
SELECT 
    date,
    product_category,
    SUM(revenue) as total_revenue,
    SUM(cost) as total_cost
FROM sales
WHERE date >= '2024-01-01'
GROUP BY date, product_category
"""
df = pd.read_sql_query(query, conn)

# 2. Process in Python
df['profit'] = df['total_revenue'] - df['total_cost']
df['profit_margin'] = (df['profit'] / df['total_revenue']) * 100

# 3. Create visualizations
import matplotlib.pyplot as plt
df.pivot_table(values='total_revenue', 
               index='date', 
               columns='product_category').plot(figsize=(12,6))
plt.title('Revenue by Category Over Time')
plt.savefig('revenue_trend.png')

# 4. Export to Excel for sharing
with pd.ExcelWriter('sales_analysis.xlsx') as writer:
    df.to_excel(writer, sheet_name='Raw Data', index=False)
    
    summary = df.groupby('product_category').agg({
        'total_revenue': 'sum',
        'profit': 'sum',
        'profit_margin': 'mean'
    })
    summary.to_excel(writer, sheet_name='Summary')

print("Analysis complete! Check sales_analysis.xlsx")
```

**Result:** Professional analysis in minutes, not hours.

---

### Learning Python as an Analyst

**You Don't Need to Learn Everything!**

**Focus on:**
✅ Pandas (data manipulation)  
✅ Basic plotting (Matplotlib/Seaborn)  
✅ Loading/saving data  
✅ Control flow (if/for loops)  

**Skip (for now):**
❌ Web development  
❌ Deep learning  
❌ System programming  
❌ Advanced algorithms  

**80% of analyst Python = Pandas + plotting**

---

### Your First Python Project

**Assignment:** Automate your most repetitive Excel task

**Steps:**
1. Identify a task you do weekly in Excel
2. Break it into steps (load, clean, analyze, visualize, export)
3. Write Python script for each step
4. Test and refine
5. Schedule to run automatically

**Common first projects:**
- Weekly sales report generation
- Data cleaning pipeline
- Merging multiple Excel files
- Creating standard charts

**Time investment:** 2-4 hours to build  
**Time saved:** 30-60 minutes per week  
**Payback:** 4-8 weeks  

**After that? Free time every week forever.**
"""
        )

        st.markdown("---")
        st.markdown("## 🔬 HANDS-ON LABS - Unit 5: Python for Analysts")
        st.markdown(
            """**Practical exercises to master Python for data analysis**

### LAB 1: Python & pandas Basics

**Objective:** Get comfortable with Python and pandas fundamentals

**Setup:**
```python
# Install required libraries
pip install pandas numpy matplotlib seaborn jupyter

# Start Jupyter Notebook
jupyter notebook
```

**Challenge 1: Load and Explore Data**
```python
import pandas as pd
import numpy as np

# Load CSV data
df = pd.read_csv('sales_data.csv')

# Basic exploration
print(df.head())  # First 5 rows
print(df.info())  # Data types and nulls
print(df.describe())  # Summary statistics
print(df.shape)  # Rows and columns

# Check for missing values
print(df.isnull().sum())

# Unique values
print(df['region'].unique())
print(df['product_category'].value_counts())
```

**Challenge 2: Data Selection**
```python
# Select columns
revenue_df = df[['date', 'revenue', 'profit']]

# Filter rows
uk_sales = df[df['country'] == 'UK']
high_value = df[df['revenue'] > 1000]

# Multiple conditions
uk_high_value = df[(df['country'] == 'UK') & (df['revenue'] > 1000)]

# Filter by list
electronics = df[df['category'].isin(['Electronics', 'Computing'])]

# String operations
gmail_customers = df[df['email'].str.contains('@gmail.com')]
```

**Challenge 3: Data Manipulation**
```python
# Add new columns
df['profit_margin'] = df['profit'] / df['revenue']
df['year'] = pd.to_datetime(df['date']).dt.year
df['month'] = pd.to_datetime(df['date']).dt.month

# Sort data
df_sorted = df.sort_values('revenue', ascending=False)

# Drop columns
df_clean = df.drop(['old_column'], axis=1)

# Rename columns
df = df.rename(columns={'old_name': 'new_name'})

# Reset index
df = df.reset_index(drop=True)
```

**Challenge 4: Grouping and Aggregation**
```python
# Group by single column
revenue_by_region = df.groupby('region')['revenue'].sum()

# Group by multiple columns
monthly_regional = df.groupby(['region', 'month'])['revenue'].sum()

# Multiple aggregations
summary = df.groupby('region').agg({
    'revenue': ['sum', 'mean', 'count'],
    'profit': ['sum', 'mean'],
    'order_id': 'count'
})

# Custom aggregations
def revenue_per_order(x):
    return x['revenue'].sum() / x['order_id'].nunique()

df.groupby('region').apply(revenue_per_order)
```

**Success Criteria:**
- ✅ Load and explore data with pandas
- ✅ Filter and select data effectively
- ✅ Create calculated columns
- ✅ Group and aggregate data

**Time:** 3-4 hours

---

### LAB 2: Data Cleaning with pandas

**Objective:** Clean messy real-world data

**Challenge 1: Handle Missing Values**
```python
# Identify missing values
print(df.isnull().sum())
print(df.isnull().sum() / len(df) * 100)  # Percentage

# Drop rows with any nulls
df_clean = df.dropna()

# Drop rows where specific column is null
df_clean = df.dropna(subset=['revenue'])

# Fill nulls with value
df['revenue'] = df['revenue'].fillna(0)

# Fill with mean/median
df['revenue'] = df['revenue'].fillna(df['revenue'].mean())

# Forward fill (use previous value)
df['revenue'] = df['revenue'].fillna(method='ffill')

# Fill by group
df['revenue'] = df.groupby('region')['revenue'].transform(lambda x: x.fillna(x.mean()))
```

**Challenge 2: Remove Duplicates**
```python
# Find duplicates
print(df.duplicated().sum())

# See duplicate rows
duplicates = df[df.duplicated(keep=False)]

# Remove duplicates
df_clean = df.drop_duplicates()

# Remove based on specific columns
df_clean = df.drop_duplicates(subset=['customer_id', 'date'])

# Keep last occurrence
df_clean = df.drop_duplicates(keep='last')
```

**Challenge 3: Data Type Conversion**
```python
# Convert to datetime
df['date'] = pd.to_datetime(df['date'])

# Handle errors
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Convert to numeric
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

# Convert to category (saves memory)
df['region'] = df['region'].astype('category')

# Convert string to boolean
df['is_active'] = df['status'].map({'active': True, 'inactive': False})
```

**Challenge 4: String Cleaning**
```python
# Remove whitespace
df['product'] = df['product'].str.strip()

# Convert case
df['email'] = df['email'].str.lower()
df['name'] = df['name'].str.title()

# Replace values
df['region'] = df['region'].str.replace('North East', 'Northeast')

# Extract patterns
df['domain'] = df['email'].str.extract(r'@(.+)$')
df['area_code'] = df['phone'].str.extract(r'(\d{3})')

# Split columns
df[['first_name', 'last_name']] = df['name'].str.split(' ', n=1, expand=True)
```

**Challenge 5: Outlier Detection**
```python
# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(df['revenue']))
df_no_outliers = df[z_scores < 3]

# IQR method
Q1 = df['revenue'].quantile(0.25)
Q3 = df['revenue'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_no_outliers = df[(df['revenue'] >= lower_bound) & (df['revenue'] <= upper_bound)]

# Percentile method
lower = df['revenue'].quantile(0.01)
upper = df['revenue'].quantile(0.99)
df_no_outliers = df[(df['revenue'] >= lower) & (df['revenue'] <= upper)]
```

**Deliverable:**
- Cleaned dataset
- Data quality report
- Cleaning script

**Time:** 3-4 hours

---

### LAB 3: Data Analysis with pandas

**Objective:** Perform comprehensive analysis

**Challenge 1: Time Series Analysis**
```python
# Set date as index
df = df.set_index('date')

# Resample to monthly
monthly = df.resample('M').agg({
    'revenue': 'sum',
    'orders': 'count',
    'profit': 'sum'
})

# Rolling window
df['revenue_7day_avg'] = df['revenue'].rolling(window=7).mean()
df['revenue_30day_sum'] = df['revenue'].rolling(window=30).sum()

# Percent change
df['revenue_pct_change'] = df['revenue'].pct_change()
df['revenue_yoy'] = df['revenue'].pct_change(periods=365)

# Cumulative sum
df['cumulative_revenue'] = df['revenue'].cumsum()
```

**Challenge 2: Pivot Tables**
```python
# Simple pivot
pivot = pd.pivot_table(
    df,
    values='revenue',
    index='region',
    columns='month',
    aggfunc='sum'
)

# Multiple aggregations
pivot_multi = pd.pivot_table(
    df,
    values=['revenue', 'profit'],
    index='region',
    columns='product_category',
    aggfunc={'revenue': 'sum', 'profit': 'mean'}
)

# Add margins (totals)
pivot = pd.pivot_table(
    df,
    values='revenue',
    index='region',
    columns='month',
    aggfunc='sum',
    margins=True
)
```

**Challenge 3: Merging DataFrames**
```python
# Inner join
merged = pd.merge(
    orders_df,
    customers_df,
    on='customer_id',
    how='inner'
)

# Left join
merged = pd.merge(
    orders_df,
    customers_df,
    on='customer_id',
    how='left'
)

# Multiple keys
merged = pd.merge(
    df1,
    df2,
    left_on=['customer_id', 'date'],
    right_on=['cust_id', 'order_date'],
    how='inner'
)

# Concatenate vertically
combined = pd.concat([df1, df2, df3], ignore_index=True)
```

**Challenge 4: Advanced Calculations**
```python
# Rank within groups
df['rank'] = df.groupby('region')['revenue'].rank(ascending=False)

# Cumulative sum within groups
df['cumsum'] = df.groupby('customer_id')['revenue'].cumsum()

# Shift for previous values
df['prev_revenue'] = df.groupby('customer_id')['revenue'].shift(1)
df['next_revenue'] = df.groupby('customer_id')['revenue'].shift(-1)

# Calculate differences
df['revenue_change'] = df['revenue'] - df['prev_revenue']

# Window functions
df['avg_3_orders'] = df.groupby('customer_id')['revenue'].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean()
)
```

**Challenge 5: Customer Cohort Analysis**
```python
# Identify cohorts
df['cohort'] = df.groupby('customer_id')['date'].transform('min')
df['cohort_month'] = df['cohort'].dt.to_period('M')

# Calculate periods
df['order_period'] = df['date'].dt.to_period('M')
df['cohort_index'] = (df['order_period'] - df['cohort_month']).apply(lambda x: x.n)

# Build cohort table
cohort_data = df.groupby(['cohort_month', 'cohort_index'])['customer_id'].nunique().reset_index()
cohort_table = cohort_data.pivot(index='cohort_month', columns='cohort_index', values='customer_id')

# Calculate retention
cohort_size = cohort_table.iloc[:, 0]
retention = cohort_table.divide(cohort_size, axis=0) * 100

print(retention)
```

**Deliverable:**
- Analysis notebook
- Summary statistics
- Insights document

**Time:** 4-5 hours

---

### LAB 4: Visualization with Python

**Objective:** Create publication-quality visualizations

**Challenge 1: matplotlib Basics**
```python
import matplotlib.pyplot as plt

# Line chart
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['revenue'], marker='o')
plt.title('Daily Revenue Trend', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Revenue (£)')
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('revenue_trend.png', dpi=300)
plt.show()

# Bar chart
top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
top_products.plot(kind='barh')
plt.title('Top 10 Products by Revenue')
plt.xlabel('Revenue (£)')
plt.tight_layout()
plt.show()

# Histogram
plt.figure(figsize=(10, 6))
plt.hist(df['revenue'], bins=50, edgecolor='black')
plt.title('Revenue Distribution')
plt.xlabel('Revenue (£)')
plt.ylabel('Frequency')
plt.show()
```

**Challenge 2: seaborn for Advanced Plots**
```python
import seaborn as sns

# Set style
sns.set_style('whitegrid')
sns.set_palette('husl')

# Box plot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='region', y='revenue')
plt.title('Revenue Distribution by Region')
plt.xticks(rotation=45)
plt.show()

# Violin plot
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='product_category', y='revenue')
plt.title('Revenue Distribution by Category')
plt.xticks(rotation=45)
plt.show()

# Heatmap
pivot = df.pivot_table(values='revenue', index='region', columns='month', aggfunc='sum')
plt.figure(figsize=(12, 8))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
plt.title('Revenue Heatmap: Region vs Month')
plt.show()

# Scatter plot with regression
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='marketing_spend', y='revenue')
plt.title('Marketing Spend vs Revenue')
plt.show()

# Pair plot
sns.pairplot(df[['revenue', 'profit', 'orders', 'customers']])
plt.show()
```

**Challenge 3: Multiple Subplots**
```python
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1: Revenue trend
axes[0, 0].plot(monthly_df.index, monthly_df['revenue'])
axes[0, 0].set_title('Monthly Revenue')
axes[0, 0].set_ylabel('Revenue (£)')

# Plot 2: Orders by region
region_orders = df.groupby('region')['orders'].sum()
axes[0, 1].bar(region_orders.index, region_orders.values)
axes[0, 1].set_title('Orders by Region')
axes[0, 1].tick_params(axis='x', rotation=45)

# Plot 3: Profit margin distribution
axes[1, 0].hist(df['profit_margin'], bins=30, edgecolor='black')
axes[1, 0].set_title('Profit Margin Distribution')
axes[1, 0].set_xlabel('Profit Margin')

# Plot 4: Top products
top_10 = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10)
axes[1, 1].barh(top_10.index, top_10.values)
axes[1, 1].set_title('Top 10 Products')

plt.tight_layout()
plt.savefig('dashboard.png', dpi=300)
plt.show()
```

**Challenge 4: Interactive Visualizations**
```python
import plotly.express as px

# Interactive line chart
fig = px.line(df, x='date', y='revenue', 
              title='Revenue Trend (Interactive)',
              hover_data=['orders', 'customers'])
fig.show()

# Interactive scatter
fig = px.scatter(df, x='marketing_spend', y='revenue', 
                 color='region', size='orders',
                 hover_data=['product_category'],
                 title='Marketing ROI Analysis')
fig.show()

# Sunburst chart
fig = px.sunburst(df, path=['region', 'product_category', 'product'], 
                  values='revenue',
                  title='Revenue Hierarchy')
fig.show()
```

**Deliverable:**
- Visualization portfolio (10+ charts)
- Style guide
- Reusable plotting functions

**Time:** 4-5 hours

---

### LAB 5: Automated Reporting

**Objective:** Build automated analysis pipeline

**Challenge 1: Report Generator Function**
```python
def generate_weekly_report(data_file, output_file):
    \"\"\"
    Generate automated weekly sales report
    \"\"\"
    # Load data
    df = pd.read_csv(data_file)
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter to last 7 days
    end_date = df['date'].max()
    start_date = end_date - pd.Timedelta(days=7)
    week_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Calculate metrics
    total_revenue = week_df['revenue'].sum()
    total_orders = len(week_df)
    avg_order_value = total_revenue / total_orders
    
    # Compare to previous week
    prev_start = start_date - pd.Timedelta(days=7)
    prev_end = start_date - pd.Timedelta(days=1)
    prev_df = df[(df['date'] >= prev_start) & (df['date'] <= prev_end)]
    prev_revenue = prev_df['revenue'].sum()
    wow_change = ((total_revenue - prev_revenue) / prev_revenue) * 100
    
    # Generate report
    report = f\"\"\"
    WEEKLY SALES REPORT
    Week ending: {end_date.strftime('%Y-%m-%d')}
    
    KEY METRICS:
    - Total Revenue: £{total_revenue:,.2f}
    - Total Orders: {total_orders:,}
    - Average Order Value: £{avg_order_value:.2f}
    - Week-over-Week Change: {wow_change:+.1f}%
    
    TOP PERFORMING:
    {week_df.groupby('region')['revenue'].sum().sort_values(ascending=False).head(5).to_string()}
    \"\"\"
    
    # Save report
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"Report generated: {output_file}")

# Run it
generate_weekly_report('sales_data.csv', 'weekly_report.txt')
```

**Challenge 2: Excel Export with Formatting**
```python
def export_to_excel_with_charts(df, output_file):
    \"\"\"
    Export data to Excel with formatting and charts
    \"\"\"
    from openpyxl import load_workbook
    from openpyxl.chart import BarChart, Reference
    
    # Create Excel writer
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    workbook = writer.book
    
    # Write summary sheet
    summary = df.groupby('region').agg({
        'revenue': 'sum',
        'orders': 'count',
        'profit': 'sum'
    }).reset_index()
    summary.to_excel(writer, sheet_name='Summary', index=False)
    
    # Write detail sheet
    df.to_excel(writer, sheet_name='Detail', index=False)
    
    # Format summary sheet
    worksheet = writer.sheets['Summary']
    format_currency = workbook.add_format({'num_format': '£#,##0.00'})
    format_header = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white'})
    
    # Apply formatting
    worksheet.set_column('B:D', 15, format_currency)
    for col_num, value in enumerate(summary.columns.values):
        worksheet.write(0, col_num, value, format_header)
    
    writer.close()
    print(f"Excel report generated: {output_file}")

# Run it
export_to_excel_with_charts(df, 'sales_report.xlsx')
```

**Challenge 3: Scheduled Automation**
```python
# Save as script: daily_report.py
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def run_daily_report():
    # Load fresh data
    df = pd.read_csv('sales_data.csv')
    
    # Generate report
    generate_weekly_report(df, f'report_{datetime.now().strftime("%Y%m%d")}.txt')
    
    # Send email (configure SMTP settings)
    sender = 'analyst@company.com'
    recipients = ['manager@company.com', 'team@company.com']
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = f'Daily Sales Report - {datetime.now().strftime("%Y-%m-%d")}'
    
    body = "Please find attached today's sales report."
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach file
    filename = f'report_{datetime.now().strftime("%Y%m%d")}.txt'
    with open(filename, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)
    
    # Send (configure your SMTP server)
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.send_message(msg)
    
    print("Report sent!")

if __name__ == '__main__':
    run_daily_report()

# Schedule with Windows Task Scheduler or cron
# Windows: schtasks /create /tn "Daily Report" /tr "python daily_report.py" /sc daily /st 09:00
# Linux: Add to crontab: 0 9 * * * python /path/to/daily_report.py
```

**Deliverable:**
- Automated report script
- Scheduling documentation
- Email template

**Time:** 4-5 hours

---

### MINI PROJECT 6: Complete Customer Analytics with Python

**Objective:** Build end-to-end customer analytics pipeline

**Requirements:**

**1. Data Pipeline**
```python
# Load multiple data sources
orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')
products = pd.read_csv('products.csv')

# Clean and merge
orders['order_date'] = pd.to_datetime(orders['order_date'])
full_data = orders.merge(customers, on='customer_id').merge(products, on='product_id')

# Calculate metrics
full_data['profit_margin'] = full_data['profit'] / full_data['revenue']
```

**2. RFM Analysis**
```python
# Calculate RFM
rfm = full_data.groupby('customer_id').agg({
    'order_date': lambda x: (pd.Timestamp.now() - x.max()).days,
    'order_id': 'count',
    'revenue': 'sum'
}).rename(columns={
    'order_date': 'recency',
    'order_id': 'frequency',
    'revenue': 'monetary'
})

# Score customers
rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

# Segment
rfm['segment'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
```

**3. Cohort Analysis**
```python
# Create cohort table
cohort_analysis_code_here
```

**4. Visualizations**
```python
# Create dashboard with 6+ charts
```

**5. Automated Report**
```python
# Generate PDF report with insights
```

**Deliverable:**
- Complete Jupyter notebook
- Automated report script
- Executive presentation
- Documentation

**Time:** 10-12 hours

**Success Criteria for Unit 5:**
- ✅ Proficient in pandas for analysis
- ✅ Clean and transform data programmatically
- ✅ Create publication-quality visualizations
- ✅ Build automated reporting pipelines
- ✅ Portfolio-ready Python projects

---

## 📝 50+ PYTHON/PANDAS PRACTICE PROBLEMS - Unit 5

### Data Loading & Exploration (10 Problems)

**Problem 1: Load CSV with custom parameters**
```python
import pandas as pd

# Basic load
df = pd.read_csv('sales_data.csv')

# With parameters
df = pd.read_csv('sales_data.csv',
                 sep=',',
                 encoding='utf-8',
                 parse_dates=['order_date'],
                 thousands=',',
                 na_values=['NA', 'missing', ''])

print(df.head())
print(df.info())
```

**Problem 2: Explore dataset structure**
```python
# Shape and basic info
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print(df.dtypes)
print(df.describe())

# Check for nulls
print(df.isnull().sum())
print(f"Total nulls: {df.isnull().sum().sum()}")

# Memory usage
print(df.memory_usage(deep=True))
```

**Problem 3: Preview data intelligently**
```python
# First and last rows
print(df.head(10))
print(df.tail(10))

# Random sample
print(df.sample(5))

# Specific columns
print(df[['customer_name', 'order_total']].head())
```

**Problem 4: Get unique values and counts**
```python
# Unique values
print(df['region'].unique())
print(f"Unique regions: {df['region'].nunique()}")

# Value counts
print(df['product_category'].value_counts())
print(df['product_category'].value_counts(normalize=True))  # Percentages
```

**Problem 5: Quick statistical summary**
```python
# Numeric columns only
print(df.describe())

# Include all columns
print(df.describe(include='all'))

# Specific columns
print(df[['revenue', 'profit']].describe())

# Custom percentiles
print(df['revenue'].quantile([0.25, 0.5, 0.75, 0.95, 0.99]))
```

**Problems 6-10: More exploration**
- Check for duplicate rows
- Identify column data types
- Find columns with missing values
- Get correlation matrix
- Profile data with pandas-profiling

---

### Data Selection & Filtering (15 Problems)

**Problem 11: Select specific columns**
```python
# Single column (Series)
revenue = df['revenue']

# Multiple columns (DataFrame)
subset = df[['customer_name', 'revenue', 'profit']]

# Column range
cols = df.loc[:, 'customer_name':'order_date']
```

**Problem 12: Filter rows by condition**
```python
# Single condition
high_value = df[df['revenue'] > 1000]

# Multiple conditions
filtered = df[(df['revenue'] > 1000) & (df['region'] == 'North')]

# OR condition
multi_region = df[(df['region'] == 'North') | (df['region'] == 'South')]
```

**Problem 13: Filter by list of values**
```python
# Using isin()
selected_products = df[df['product'].isin(['Product A', 'Product B', 'Product C'])]

# NOT in list
excluded = df[~df['region'].isin(['North', 'South'])]
```

**Problem 14: String filtering**
```python
# Contains
gmail_users = df[df['email'].str.contains('@gmail.com', na=False)]

# Starts with
a_names = df[df['customer_name'].str.startswith('A')]

# Ends with
uk_postcodes = df[df['postcode'].str.endswith('UK')]

# Case insensitive
london = df[df['city'].str.lower() == 'london']
```

**Problem 15: Date filtering**
```python
# After specific date
recent = df[df['order_date'] > '2024-01-01']

# Between dates
q1 = df[(df['order_date'] >= '2024-01-01') & (df['order_date'] <= '2024-03-31')]

# Current year
current_year = df[df['order_date'].dt.year == 2024]

# Last 30 days
from datetime import datetime, timedelta
last_30 = df[df['order_date'] > (datetime.now() - timedelta(days=30))]
```

**Problem 16: loc vs iloc**
```python
# loc - label based
specific_rows = df.loc[0:5, ['customer_name', 'revenue']]

# iloc - integer based
first_five = df.iloc[0:5, 0:3]

# Boolean indexing with loc
high_revenue = df.loc[df['revenue'] > 1000, ['customer_name', 'revenue']]
```

**Problem 17: Query method**
```python
# More readable filtering
filtered = df.query('revenue > 1000 and region == "North"')

# With variables
min_revenue = 1000
filtered = df.query('revenue > @min_revenue')
```

**Problem 18: Top N and Bottom N**
```python
# Top 10 by revenue
top_10 = df.nlargest(10, 'revenue')

# Bottom 10
bottom_10 = df.nsmallest(10, 'revenue')

# Top 5 per group
top_per_region = df.groupby('region').apply(lambda x: x.nlargest(5, 'revenue'))
```

**Problem 19: Sample rows**
```python
# Random sample
sample = df.sample(n=100)

# Random fraction
sample_pct = df.sample(frac=0.1)  # 10%

# Stratified sample
stratified = df.groupby('region').apply(lambda x: x.sample(min(len(x), 10)))
```

**Problem 20: Complex filtering**
```python
# Multiple conditions with query
result = df.query('(revenue > 1000 and region == "North") or (revenue > 2000 and region == "South")')

# Using eval
df_filtered = df[df.eval('revenue > profit * 2')]
```

**Problems 21-25: More filtering**
- Filter using regex patterns
- Find rows with nulls in specific columns
- Select rows by index labels
- Filter datetime by month/quarter
- Complex multi-column conditions

---

### Data Cleaning & Transformation (20 Problems)

**Problem 26: Handle missing values**
```python
# Drop rows with any nulls
df_clean = df.dropna()

# Drop if specific column is null
df_clean = df.dropna(subset=['email'])

# Fill with value
df['revenue'].fillna(0, inplace=True)

# Fill with mean/median
df['revenue'].fillna(df['revenue'].mean(), inplace=True)

# Forward fill
df['region'].fillna(method='ffill', inplace=True)

# Fill by group
df['revenue'] = df.groupby('region')['revenue'].transform(lambda x: x.fillna(x.mean()))
```

**Problem 27: Remove duplicates**
```python
# All columns
df_unique = df.drop_duplicates()

# Specific columns
df_unique = df.drop_duplicates(subset=['customer_id'])

# Keep last occurrence
df_unique = df.drop_duplicates(keep='last')

# Mark duplicates
df['is_duplicate'] = df.duplicated()
```

**Problem 28: Data type conversion**
```python
# To datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# To numeric
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

# To category (saves memory)
df['region'] = df['region'].astype('category')

# To string
df['customer_id'] = df['customer_id'].astype(str)
```

**Problem 29: String operations**
```python
# Lowercase
df['email'] = df['email'].str.lower()

# Remove whitespace
df['name'] = df['name'].str.strip()

# Replace
df['phone'] = df['phone'].str.replace('-', '')

# Extract with regex
df['domain'] = df['email'].str.extract(r'@(.+)$')

# Split
df[['first_name', 'last_name']] = df['name'].str.split(' ', n=1, expand=True)
```

**Problem 30: Create calculated columns**
```python
# Simple calculation
df['profit_margin'] = df['profit'] / df['revenue']

# Conditional column
df['segment'] = df['revenue'].apply(lambda x: 'High' if x > 1000 else 'Low')

# Using np.where
import numpy as np
df['segment'] = np.where(df['revenue'] > 1000, 'High', 'Low')

# Using pd.cut for binning
df['revenue_bin'] = pd.cut(df['revenue'], bins=[0, 500, 1000, 5000], labels=['Low', 'Medium', 'High'])
```

**Problem 31: Rename columns**
```python
# Dictionary mapping
df = df.rename(columns={'old_name': 'new_name', 'old2': 'new2'})

# Function
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Prefix
df = df.add_prefix('col_')

# Suffix
df = df.add_suffix('_value')
```

**Problem 32: Sort data**
```python
# Single column
df_sorted = df.sort_values('revenue', ascending=False)

# Multiple columns
df_sorted = df.sort_values(['region', 'revenue'], ascending=[True, False])

# By index
df_sorted = df.sort_index()
```

**Problem 33: Reset and set index**
```python
# Reset index
df = df.reset_index(drop=True)

# Set column as index
df = df.set_index('customer_id')

# Multi-level index
df = df.set_index(['region', 'customer_id'])
```

**Problem 34: Merge/concat DataFrames**
```python
# Vertical concatenation
combined = pd.concat([df1, df2], ignore_index=True)

# Horizontal
combined = pd.concat([df1, df2], axis=1)

# Inner join
merged = pd.merge(df1, df2, on='customer_id', how='inner')

# Left join
merged = pd.merge(df1, df2, on='customer_id', how='left')

# Multiple keys
merged = pd.merge(df1, df2, left_on=['id', 'date'], right_on=['customer_id', 'order_date'])
```

**Problem 35: Apply custom functions**
```python
# Apply to column
df['revenue_doubled'] = df['revenue'].apply(lambda x: x * 2)

# Apply to DataFrame
df['total'] = df.apply(lambda row: row['quantity'] * row['price'], axis=1)

# Map values
df['region_code'] = df['region'].map({'North': 'N', 'South': 'S', 'East': 'E', 'West': 'W'})
```

**Problems 36-45: More transformations**
- Handle outliers (IQR method)
- Normalize/standardize columns
- Encode categorical variables
- Pivot and unpivot data
- Melt wide to long format
- Extract datetime components
- Rolling calculations
- Cumulative sums
- Rank values
- Sample and resample time series

---

### Grouping & Aggregation (10 Problems)

**Problem 46: Basic groupby**
```python
# Single aggregation
revenue_by_region = df.groupby('region')['revenue'].sum()

# Multiple aggregations
summary = df.groupby('region').agg({
    'revenue': ['sum', 'mean', 'count'],
    'profit': ['sum', 'mean'],
    'customer_id': 'nunique'
})
```

**Problem 47: Custom aggregation functions**
```python
# Named aggregations
summary = df.groupby('region').agg(
    total_revenue=('revenue', 'sum'),
    avg_revenue=('revenue', 'mean'),
    unique_customers=('customer_id', 'nunique')
)

# Custom function
def revenue_per_customer(x):
    return x['revenue'].sum() / x['customer_id'].nunique()

df.groupby('region').apply(revenue_per_customer)
```

**Problem 48: Transform for group calculations**
```python
# Add group mean to each row
df['region_avg_revenue'] = df.groupby('region')['revenue'].transform('mean')

# Rank within group
df['rank_in_region'] = df.groupby('region')['revenue'].rank(ascending=False)

# Percentage of group total
df['pct_of_region'] = df.groupby('region')['revenue'].transform(lambda x: x / x.sum())
```

**Problem 49: Multiple groupby levels**
```python
# Two levels
summary = df.groupby(['region', 'product'])['revenue'].sum()

# With reset_index
summary = df.groupby(['region', 'product']).agg({'revenue': 'sum'}).reset_index()
```

**Problem 50: Filter groups**
```python
# Keep groups with >10 records
filtered = df.groupby('region').filter(lambda x: len(x) > 10)

# Keep groups with total revenue > 10000
filtered = df.groupby('region').filter(lambda x: x['revenue'].sum() > 10000)
```

**Problems 51-55: More aggregation**
- Pivot tables with pandas
- Cross-tabulation
- Rolling window aggregations
- Expanding calculations
- Groupby with multiple functions per column

---

### Visualization (5 Problems)

**Problem 56: Basic plots**
```python
import matplotlib.pyplot as plt

# Line plot
df.plot(x='date', y='revenue', kind='line', figsize=(12, 6))
plt.title('Revenue Over Time')
plt.show()

# Bar chart
df.groupby('region')['revenue'].sum().plot(kind='bar')
plt.title('Revenue by Region')
plt.show()

# Histogram
df['revenue'].plot(kind='hist', bins=50)
plt.title('Revenue Distribution')
plt.show()
```

**Problem 57: Advanced seaborn plots**
```python
import seaborn as sns

# Box plot by category
sns.boxplot(data=df, x='region', y='revenue')
plt.title('Revenue Distribution by Region')
plt.show()

# Heatmap
pivot = df.pivot_table(values='revenue', index='region', columns='month')
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
plt.show()

# Pair plot
sns.pairplot(df[['revenue', 'profit', 'quantity']])
plt.show()
```

**Problem 58: Multiple subplots**
```python
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1
df.plot(x='date', y='revenue', ax=axes[0, 0])
axes[0, 0].set_title('Revenue Trend')

# Plot 2
df.groupby('region')['revenue'].sum().plot(kind='bar', ax=axes[0, 1])
axes[0, 1].set_title('Revenue by Region')

# Plot 3
df['revenue'].plot(kind='hist', bins=30, ax=axes[1, 0])
axes[1, 0].set_title('Revenue Distribution')

# Plot 4
df.plot(x='profit', y='revenue', kind='scatter', ax=axes[1, 1])
axes[1, 1].set_title('Profit vs Revenue')

plt.tight_layout()
plt.show()
```

**Problem 59: Interactive plotly**
```python
import plotly.express as px

# Interactive line
fig = px.line(df, x='date', y='revenue', title='Revenue Over Time')
fig.show()

# Interactive scatter with hover
fig = px.scatter(df, x='profit', y='revenue', color='region', 
                 size='quantity', hover_data=['customer_name'])
fig.show()
```

**Problem 60: Save plots**
```python
# Save matplotlib
plt.figure(figsize=(12, 6))
df.plot(x='date', y='revenue')
plt.savefig('revenue_trend.png', dpi=300, bbox_inches='tight')

# Save plotly
fig = px.line(df, x='date', y='revenue')
fig.write_html('revenue_trend.html')
fig.write_image('revenue_trend.png')
```

---

### Real-World Challenges

**Challenge 1: Clean Messy Dataset**
Given CSV with mixed date formats, missing values, duplicates, and inconsistent categories - clean it completely.

**Challenge 2: Customer Segmentation**
RFM analysis with automatic segment assignment and visualization.

**Challenge 3: Time Series Analysis**
Daily sales with trends, seasonality detection, and forecasting.

**Challenge 4: Data Pipeline**
Load multiple CSVs, merge, clean, analyze, and export results automatically.

**Challenge 5: Automated Report**
Generate PDF report with charts, tables, and insights from data.

---

"""
        )
    elif unit_number == 6:
        st.markdown("#### 📘 Designing Good Metrics and KPIs: The Foundation of Data-Driven Decisions")
        st.markdown(
            """**"What gets measured gets managed." - Peter Drucker**

KPIs (Key Performance Indicators) are the metrics that tell you whether your business is succeeding or failing.

**Bad KPIs = Bad decisions = Failed business**  
**Good KPIs = Clear priorities = Success**

---

**What Makes a Good KPI?**

Not all metrics are created equal. A good KPI must be:

**1. Aligned with Business Goals**
- Directly connected to strategic objectives
- If this improves, the business improves

**2. Actionable**
- Can influence through your actions
- Not just "nice to know"

**3. Measurable**
- Clearly defined calculation
- Can be tracked consistently

**4. Understandable**
- Everyone knows what it means
- No confusion about interpretation

**5. Timely**
- Can be measured frequently enough to act
- Not too delayed (e.g., monthly better than yearly)

---

### The KPI Hierarchy

**North Star Metric** (1 metric)
↓
**Primary KPIs** (3-5 metrics)
↓
**Secondary Metrics** (10-15 metrics)
↓
**Operational Metrics** (many)

**Example: E-commerce Company**

**North Star:** Revenue (the ultimate goal)

**Primary KPIs:**
- Monthly Active Users (MAU)
- Conversion Rate
- Average Order Value (AOV)
- Customer Acquisition Cost (CAC)

**Secondary Metrics:**
- Cart abandonment rate
- Repeat purchase rate
- Email open rate
- Website bounce rate

**Operational Metrics:**
- Daily new signups
- Customer support tickets
- Server uptime
- Inventory levels

**You focus on Primary KPIs. They drive the North Star.**

---

### Vanity Metrics vs Actionable Metrics

**VANITY METRICS** (look good, don't help)

❌ **Total Page Views**
- Problem: Doesn't measure engagement or value
- Can increase while business fails
- Not actionable

❌ **Total Registered Users**
- Problem: Includes inactive users
- Doesn't reflect actual usage
- Misleading growth signal

❌ **Social Media Followers**
- Problem: Doesn't equal customers
- Can be bought or fake
- No revenue correlation

**ACTIONABLE METRICS** (drive decisions)

✅ **Conversion Rate** (visitors → customers)
- Problem: Can be improved through A/B testing
- Direct revenue impact
- Clear optimization target

✅ **Active Users (last 30 days)**
- Shows actual engagement
- Can increase through product improvements
- Predicts revenue

✅ **Net Promoter Score (NPS)**
- Measures satisfaction
- Predicts retention
- Can improve through service changes

---

### Designing KPIs: The Framework

**STEP 1: Start with Business Goals**

"We want to grow revenue by 20% this year."

**STEP 2: Break Down into Levers**

Revenue = Customers × Average Purchase Value × Purchase Frequency

**STEP 3: Identify What You Can Control**

- ✅ Marketing spend (affects customer acquisition)
- ✅ Product features (affects purchase frequency)
- ✅ Pricing strategy (affects purchase value)
- ❌ Economic conditions (can't control)

**STEP 4: Define Specific Metrics**

**Primary KPIs:**
1. Customer Acquisition Rate (new customers/month)
2. Average Order Value (£ per transaction)
3. Purchase Frequency (transactions per customer per year)

**STEP 5: Set Targets**

- Customer Acquisition: 500 new/month (vs 400 current)
- Average Order Value: £75 (vs £70 current)
- Purchase Frequency: 3.2x/year (vs 3.0 current)

**STEP 6: Assign Owners**

- Customer Acquisition → Marketing Team
- Average Order Value → Product Team
- Purchase Frequency → Retention Team

---

### Real-World KPI Examples by Industry

**Healthcare (Hospital):**
- DNA (Did Not Attend) rate: <12%
- Average waiting time: <18 weeks
- Patient satisfaction: >4.2/5
- Readmission rate: <8%
- Bed occupancy: 85-90%

**SaaS Company:**
- Monthly Recurring Revenue (MRR): growth >10%/month
- Churn rate: <5%/month
- Customer Acquisition Cost (CAC): <£500
- Lifetime Value (LTV): >£3,000
- LTV:CAC ratio: >3:1

**Retail Store:**
- Same-store sales growth: >5% YoY
- Inventory turnover: >6x/year
- Gross margin: >40%
- Customer foot traffic: trend up
- Average transaction value: trend up

---

### Common KPI Mistakes

**MISTAKE 1: Too Many KPIs**

Problem: "Dashboard paralysis" - can't focus on what matters

Solution: Max 5 primary KPIs. If everything is important, nothing is important.

**MISTAKE 2: Lagging Indicators Only**

Problem: Revenue is a lagging indicator (tells you what happened)

Solution: Balance with leading indicators (predict what will happen)

Example:
- Lagging: Revenue this month
- Leading: Sales pipeline value (predicts future revenue)

**MISTAKE 3: Not Segmenting**

Problem: "Average customer spends £50" hides that:
- VIP customers spend £500
- Regular customers spend £30

Solution: Always segment (by customer type, product, region, etc.)

**MISTAKE 4: No Comparison Baseline**

Problem: "We had 10,000 visitors this month" - is that good?

Solution: Always compare (vs last month, vs target, vs last year)

**MISTAKE 5: Metrics Not Aligned with Incentives**

Problem: Call center measured on "calls per hour"
Result: Agents rush customers off phone, satisfaction drops

Solution: Measure "customer satisfaction" and "first-call resolution"
"""
        )

        st.markdown("#### 🧪 A/B Testing for Analysts: Making Evidence-Based Decisions")
        st.markdown(
            """**A/B testing lets you PROVE what works instead of guessing.**

### What is A/B Testing?

**Definition:** Comparing two versions of something to see which performs better.

**The Process:**

1. **Version A (Control):** Current version
2. **Version B (Variant):** New version you want to test
3. **Split traffic:** 50% see A, 50% see B
4. **Measure results:** Which version has better metric?
5. **Choose winner:** Implement the better version

---

### Real-World Example

**Scenario:** E-commerce checkout button

**Version A (Current):** Button says "Buy Now" (green)
**Version B (Test):** Button says "Complete Purchase" (blue)

**Hypothesis:** Blue button with clearer text will increase purchases

**Test Setup:**
- 1,000 visitors to Version A
- 1,000 visitors to Version B
- Measure: Conversion rate (% who complete purchase)

**Results:**
- Version A: 50 purchases / 1,000 visitors = **5.0% conversion**
- Version B: 65 purchases / 1,000 visitors = **6.5% conversion**

**Conclusion:** Version B wins! +1.5 percentage points = 30% improvement

**Business Impact:** 
- Current: 10,000 monthly visitors × 5% = 500 purchases
- With B: 10,000 visitors × 6.5% = 650 purchases
- **Extra 150 purchases/month = £15,000 extra revenue** (if avg order = £100)

**ROI of this test: £180K/year from one button change!**

---

### When to Use A/B Testing

**GOOD Use Cases:**

✅ **Website/App Changes**
- Button colors, text, placement
- Page layouts
- Checkout flows

✅ **Marketing Campaigns**
- Email subject lines
- Ad copy variations
- Landing page designs

✅ **Pricing Strategies**
- Different price points
- Discount levels
- Subscription tiers

**BAD Use Cases:**

❌ **Major Rebrands**
- Too big, affects everything
- Confusing for users to see different brands

❌ **Long-Term Behavior Changes**
- Need weeks/months to measure
- A/B tests work best for immediate actions

❌ **When You Don't Have Traffic**
- Need minimum 100-1000 conversions per variant
- Small samples = unreliable results

---

### Statistical Significance: Did We Really Win?

**The Question:** Is Version B actually better, or just lucky?

**Example:**
- Version A: 50 clicks / 1,000 visitors = 5.0%
- Version B: 55 clicks / 1,000 visitors = 5.5%

**Is 5.5% significantly better than 5.0%?**

**Statistical Significance tells you:**
- How confident we are that B is truly better
- Standard: 95% confidence level (p-value < 0.05)

**Translation:**
- "95% confident" = Only 5% chance this is random luck
- "Not significant" = Could be random variation, need more data

---

### How to Calculate (Simplified)

**Use an A/B test calculator** (many free online tools)

**Inputs:**
- Visitors to A: 1,000
- Conversions from A: 50 (5%)
- Visitors to B: 1,000
- Conversions from B: 65 (6.5%)

**Output:**
- **P-value: 0.03** (3% chance of random luck)
- **Confidence: 97%** (significant!)
- **Conclusion: Version B is significantly better** ✅

**Rule of Thumb:**
- p-value < 0.05 = Significant (trust the result)
- p-value > 0.05 = Not significant (need more data)

---

### How Long to Run A/B Test?

**Minimum Requirements:**

**1. Sample Size:**
- At least 100 conversions per variant
- Ideally 1,000+ for reliable results

**2. Time Duration:**
- Minimum 1 week (captures weekly patterns)
- Ideally 2-4 weeks for confidence
- DON'T stop early just because one is winning!

**3. Full Business Cycles:**
- E-commerce: Include weekend + weekday
- B2B: Include full work week
- Seasonal: Account for seasonality

**Early Stopping Trap:**

Day 3: "B is winning 8% vs 5%! Let's stop!"
Problem: Could be random daily variation
Solution: Wait for full test duration + statistical significance

---

### Communicating A/B Test Results

**BAD Way:**

"Version B had a p-value of 0.03 with 97% confidence."

*Non-technical stakeholders confused*

**GOOD Way:**

**Setup:** "We tested two checkout button designs."

**Results:** "Version B (blue 'Complete Purchase' button) had **6.5% conversion** vs Version A's **5.0% conversion**."

**Significance:** "This is a **30% improvement** and statistically reliable (97% confidence)."

**Impact:** "If we implement Version B, we'll gain **150 extra purchases per month**."

**Revenue:** "That's **£15,000 extra monthly revenue** or **£180K annually**."

**Recommendation:** "I recommend we launch Version B immediately."

**See the difference? No jargon, clear business impact.**

---

### Common A/B Testing Mistakes

**MISTAKE 1: Testing Too Many Things at Once**

Problem: Changed button color AND text AND placement
Can't tell which change caused improvement

Solution: Test one variable at a time

**MISTAKE 2: Peeking at Results Early**

Problem: Checking every day and stopping when "winning"
Increases false positives

Solution: Define test duration upfront, wait until end

**MISTAKE 3: Not Segmenting Results**

Problem: Overall B won, but maybe it only won for mobile users?

Solution: Always analyze by segment (device, new vs returning, etc.)

**MISTAKE 4: Ignoring Practical Significance**

Problem: "B is 0.1% better and statistically significant!"
But 0.1% = 1 extra customer per month = not worth implementing

Solution: Consider both statistical AND practical significance

**MISTAKE 5: Not Having a Hypothesis**

Problem: Testing random changes hoping something works

Solution: Form hypothesis first: "If we do X because of Y, we expect Z to improve"
"""
        )

        st.markdown("#### 📐 Avoiding Common Metric Pitfalls")
        st.markdown(
            """**Even good analysts fall into these traps. Learn to avoid them.**

---

### 1. Simpson's Paradox: When Aggregates Lie

**The Trap:** Overall trend shows one thing, but every segment shows the opposite.

**Real Example:**

**Hospital Scenario:** Comparing two hospitals' success rates

**Overall Results:**
- Hospital A: 90% success rate (900/1000 surgeries)
- Hospital B: 85% success rate (850/1000 surgeries)

**Looks like Hospital A is better, right? WRONG.**

**Segmented by Surgery Type:**

**Easy Surgeries:**
- Hospital A: 95% success (760/800)
- Hospital B: 98% success (588/600) ← Better!

**Difficult Surgeries:**
- Hospital A: 70% success (140/200)
- Hospital B: 65.5% success (262/400) ← Better!

**What happened?**
- Hospital B takes more difficult cases (400 vs 200)
- Hospital B is actually better at BOTH types
- But overall rate looks worse due to case mix

**Lesson:** ALWAYS segment your data. Don't trust aggregates alone.

---

### 2. Survivorship Bias: Only Seeing Winners

**The Trap:** Analyzing only data that "survived" a selection process.

**Classic Example:**

World War II: Military analyzed planes returning from combat to see where to add armor.

**Bullet holes appeared on:**
- Wings
- Fuselage
- Tail

**Wrong Conclusion:** "Add armor to wings, fuselage, tail"

**Right Conclusion:** "Add armor to engines and cockpit"

**Why?** Planes shot in engines/cockpit DIDN'T RETURN. You're only seeing survivors!

**Business Example:**

"Let's analyze what makes successful startups" (by studying current successful companies)

**Problem:** You're ignoring the 90% that failed. Maybe successful companies just got lucky?

**Solution:** Study BOTH successes and failures to find real patterns.

---

### 3. Correlation ≠ Causation

**The Trap:** Assuming because two things move together, one causes the other.

**Example 1:**

**Finding:** Ice cream sales and drowning deaths are correlated

**Wrong Conclusion:** Ice cream causes drowning!

**Right Conclusion:** Hot weather causes both (people eat ice cream AND swim more)

**Example 2:**

**Finding:** Companies with more meetings have higher revenue

**Wrong Conclusion:** More meetings = more revenue!

**Right Conclusion:** Larger companies have both more meetings AND more revenue

---

**How to Think About Causation:**

**Ask these questions:**
1. **Could it be reverse causation?** (B causes A, not A causes B)
2. **Could there be a third variable?** (C causes both A and B)
3. **Is there a plausible mechanism?** (HOW would A cause B?)
4. **Can we test it experimentally?** (A/B test!)

**Gold Standard:** Randomized experiment (A/B test)

---

### 4. Base Rate Fallacy: Ignoring Context

**The Trap:** Focusing on specific data without considering baseline rates.

**Example:**

**Scenario:** Medical test for rare disease (affects 1 in 1,000 people)
- Test accuracy: 99% (detects disease 99% of time)
- You test positive

**Question:** What's the chance you have the disease?

**Intuitive Answer:** 99% (test is 99% accurate!)

**Correct Answer:** ~9% (you probably DON'T have it)

**Why?**

Out of 10,000 people:
- 10 actually have disease → 9-10 test positive ✓
- 9,990 don't have disease → 100 false positives (1% of 9,990)

**Total positives: 110**
**True positives: 10**
**Your chance: 10/110 = 9%**

**Business Example:**

"Our new ad has 10% click rate!" (sounds great)

**But:** Industry average is 15%
Your ad is actually UNDERPERFORMING

**Lesson:** Always know the baseline/benchmark.

---

### 5. Metric Gaming: When People Cheat the System

**Goodhart's Law:** "When a measure becomes a target, it ceases to be a good measure."

**Example 1: Call Centers**

**Metric:** Average call time (want it low)

**Result:** Agents rush customers off phone
Actual problem not solved
Customer calls back multiple times

**Better Metric:** First-call resolution rate

**Example 2: Sales Team**

**Metric:** Number of sales calls made

**Result:** Agents make many short, low-quality calls
No actual sales increase

**Better Metric:** Qualified leads generated OR sales closed

**Example 3: Software Development**

**Metric:** Lines of code written

**Result:** Developers write unnecessarily verbose code
Quality suffers

**Better Metric:** Features delivered OR bugs per feature

**How to Prevent Gaming:**

1. **Use multiple metrics** (one alone can be gamed)
2. **Include quality metrics** alongside quantity
3. **Review regularly** for unintended behaviors
4. **Listen to teams** about perverse incentives

---

### 6. The Streetlight Effect: Measuring What's Easy, Not What Matters

**The Story:** 
Person looks for lost keys under streetlight, not where they dropped them.
"Why?" 
"Because the light is better here!"

**Business Translation:**
Measuring easy-to-track metrics instead of important ones.

**Examples:**

**Easy to Measure:**
- Website traffic
- Email opens
- Social media likes

**Hard to Measure (but more important):**
- Customer satisfaction
- Product quality
- Team morale

**Solution:** Invest in measuring what matters, even if harder.

---

### Creating a Balanced KPI Dashboard

**Include Mix of:**

**1. Input Metrics** (what you control)
- Marketing spend
- Number of sales calls
- Product features shipped

**2. Output Metrics** (results)
- Revenue
- New customers
- Market share

**3. Leading Indicators** (predict future)
- Sales pipeline value
- Customer satisfaction
- Product usage trends

**4. Lagging Indicators** (confirm past)
- Revenue growth
- Profit margin
- Customer retention

**5. Internal Metrics** (operations)
- Team productivity
- System uptime
- Bug count

**6. External Metrics** (market)
- Market share
- Competitor pricing
- Industry benchmarks

**Balance ensures you're not blindsided.**

---

### Your Metric Design Checklist

For each proposed metric, ask:

- [ ] Does it align with a strategic goal?
- [ ] Can we actually influence it?
- [ ] Is the calculation clearly defined?
- [ ] Can we measure it reliably and frequently?
- [ ] Will people understand it without explanation?
- [ ] Is it immune to gaming?
- [ ] Have we considered segments? (not just aggregates)
- [ ] Do we have a baseline/benchmark?
- [ ] Is there a specific target?
- [ ] Is someone accountable for it?

**If yes to all 10, you have a GOOD metric.**
"""
        )

        st.markdown("---")
        st.markdown("## 🔬 HANDS-ON LABS - Unit 6: Metrics & A/B Testing")
        st.markdown(
            """**Practical exercises to master experimentation and metrics design**

### LAB 1: Designing Good Metrics

**Objective:** Learn to create actionable, measurable KPIs

**Scenario:** You're the analyst at TechStartup SaaS company

**Challenge 1: Identify Bad Metrics**
```
Fix these poorly designed metrics:

BAD METRIC 1: "User happiness"
Problems:
- Not measurable (subjective)
- No baseline
- Can't track objectively

GOOD VERSION:
- Net Promoter Score (NPS): "On 0-10, how likely are you to recommend us?"
- Target: NPS > 50
- Measured: Monthly survey
- Trackable trend

BAD METRIC 2: "Website performance"
Problems:
- Too vague
- Multiple interpretations
- No action threshold

GOOD VERSION:
- Page Load Time: P95 < 2 seconds
- Uptime: > 99.9%
- Error Rate: < 0.1% of requests
- Specific, measurable, actionable

BAD METRIC 3: "Sales are growing"
Problems:
- No comparison baseline
- Could be seasonal
- No target

GOOD VERSION:
- MoM Revenue Growth: +15% vs last month
- YoY Revenue Growth: +50% vs last year
- Against Target: 95% of Q4 goal
```

**Challenge 2: SMART Metrics Framework**
```
Convert vague goals to SMART metrics:

VAGUE: "Improve customer retention"

SMART METRIC:
- Specific: Monthly customer retention rate
- Measurable: (Customers end of month / Customers start of month) * 100
- Achievable: Increase from 85% to 90%
- Relevant: Reduces churn cost, increases LTV
- Time-bound: Achieve by end of Q2 2024

MEASUREMENT PLAN:
- Track: Monthly cohort retention
- Report: First week of each month
- Owner: Customer Success team
- Action: If drops below 88%, investigate & intervene
```

**Challenge 3: Leading vs Lagging Indicators**
```
Identify which metrics predict future performance:

LAGGING (Past results):
- Monthly revenue (already happened)
- Customer churn (already lost them)
- Product bugs found in production (already shipped)

LEADING (Future predictors):
- Sales pipeline value (predicts future revenue)
- Customer satisfaction scores (predicts churn)
- Code coverage % (predicts bug rate)

BUILD A DASHBOARD:
Leading Indicators (Left) → Lagging Indicators (Right)

Sales:
- Pipeline value $2M → Next Quarter Revenue $1.5M
- Lead response time 2hr → Conversion rate 15%

Product:
- Daily active users 10K → Monthly retention 85%
- Feature adoption 60% → Customer satisfaction 4.2/5
```

**Challenge 4: North Star Metric**
```
Define your company's One Metric That Matters:

COMPANY: Streaming Service (like Netflix)

BRAINSTORM CANDIDATES:
- Total subscribers? (Yes, but includes inactive)
- Revenue? (Yes, but could game pricing)
- Content hours? (No, doesn't indicate value)
- Weekly active users? (Better - shows engagement)

NORTH STAR METRIC:
"Weekly Streaming Hours per Subscriber"

Why this metric?
✅ Measures actual product usage
✅ Correlates with retention
✅ Predictive of renewal
✅ Captures product value
✅ Actionable - can improve content
✅ Simple to understand

Supporting Metrics:
- Content completion rate
- Recommendation click-through
- Search success rate
- New content discovery
```

**Deliverable:**
- Metrics design document
- Dashboard mockup
- Measurement plan

**Time:** 3-4 hours

---

### LAB 2: A/B Test Design

**Objective:** Design rigorous experiments

**Scenario:** E-commerce company testing new checkout flow

**Challenge 1: Formulate Hypothesis**
```
PROBLEM: Cart abandonment rate is 68%

BAD HYPOTHESIS:
"New checkout will be better"
- Not specific
- Not measurable
- No prediction

GOOD HYPOTHESIS:
"Reducing checkout from 5 steps to 3 steps will decrease cart abandonment from 68% to 60% (12% relative improvement) because fewer steps reduces friction and cognitive load."

INCLUDES:
✅ Specific change (5 steps → 3 steps)
✅ Predicted outcome (68% → 60%)
✅ Magnitude (12% improvement)
✅ Rationale (why we think this will work)
```

**Challenge 2: Define Success Metrics**
```
PRIMARY METRIC:
- Cart abandonment rate
- Target: < 60% (vs 68% current)
- Statistical significance: 95% confidence
- Minimum detectable effect: 5% relative change

SECONDARY METRICS:
- Checkout completion time (expect faster)
- Revenue per session (expect higher)
- Customer satisfaction (expect same or better)

GUARDRAIL METRICS (Must NOT degrade):
- Payment error rate (must stay < 0.5%)
- Customer support contacts (must not increase)
- Return rate (must stay < 5%)
```

**Challenge 3: Sample Size Calculation**
```python
# Calculate required sample size
from scipy import stats
import numpy as np

def calculate_sample_size(baseline_rate, min_effect, alpha=0.05, power=0.80):
    """
    Calculate sample size needed for A/B test
    
    baseline_rate: Current conversion rate (e.g., 0.32 for 32%)
    min_effect: Minimum detectable effect (e.g., 0.05 for 5% relative)
    alpha: Significance level (default 0.05 = 95% confidence)
    power: Statistical power (default 0.80 = 80%)
    """
    # Expected rate in treatment
    expected_rate = baseline_rate * (1 + min_effect)
    
    # Effect size (Cohen's h)
    effect_size = 2 * (np.arcsin(np.sqrt(expected_rate)) - np.arcsin(np.sqrt(baseline_rate)))
    
    # Z-scores
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    # Sample size per group
    n = ((z_alpha + z_beta) ** 2) / (effect_size ** 2)
    
    return int(np.ceil(n))

# Example: Cart abandonment test
baseline = 0.68  # 68% abandonment
min_effect = 0.12  # 12% relative improvement
target = baseline * (1 - min_effect)  # 59.84%

sample_size_per_group = calculate_sample_size(baseline, min_effect)
total_sample = sample_size_per_group * 2

print(f"Baseline abandonment: {baseline*100:.1f}%")
print(f"Target abandonment: {target*100:.1f}%")
print(f"Sample size needed per group: {sample_size_per_group:,}")
print(f"Total sample size: {total_sample:,}")

# With 10,000 daily visitors and 60% reaching checkout:
daily_test_participants = 10000 * 0.60
days_needed = total_sample / daily_test_participants
print(f"Days needed to run test: {days_needed:.1f}")
```

**Challenge 4: Randomization Plan**
```
RANDOMIZATION UNIT: User session

ASSIGNMENT LOGIC:
1. User reaches checkout page
2. Hash user_id with experiment seed
3. If hash % 100 < 50: Control (old 5-step)
4. If hash % 100 >= 50: Treatment (new 3-step)

ENSURE:
✅ Consistent assignment (same user always gets same variant)
✅ 50/50 split
✅ Independent of time/device
✅ No contamination between groups

IMPLEMENTATION:
```python
import hashlib

def assign_variant(user_id, experiment_name='checkout_test'):
    """
    Deterministically assign user to test variant
    """
    # Create hash
    hash_input = f"{user_id}_{experiment_name}".encode()
    hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
    
    # Assign to variant
    if hash_value % 100 < 50:
        return 'control'
    else:
        return 'treatment'

# Test it
for user_id in range(1, 11):
    variant = assign_variant(user_id)
    print(f"User {user_id}: {variant}")
```
```

**Challenge 5: Test Duration Calculation**
```
FACTORS TO CONSIDER:

1. Sample size needed: 4,200 per group = 8,400 total
2. Daily traffic: 6,000 checkout attempts/day
3. Minimum duration: 8,400 / 6,000 = 1.4 days

BUT ALSO CONSIDER:
- Weekly seasonality (run full weeks)
- Day-of-week effects (Mon-Sun coverage)
- Event calendar (avoid holidays)
- Business cycles (paydays, month-end)

DECISION: Run for 2 full weeks
- Ensures 2x required sample size
- Covers all days of week twice
- Reduces variance from time effects
- Confidence in results

STOPPING RULES:
DO NOT STOP EARLY even if significant!
- Fixed horizon: 2 weeks exactly
- Exception: Critical bug/issue only
- Document any early termination
```

**Deliverable:**
- Complete A/B test design document
- Sample size calculations
- Randomization code
- Timeline and stopping rules

**Time:** 4-5 hours

---

### LAB 3: A/B Test Analysis

**Objective:** Analyze experiment results correctly

**Scenario:** Your checkout A/B test ran for 2 weeks

**Challenge 1: Load and Validate Data**
```python
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load test results
df = pd.read_csv('checkout_test_results.csv')

print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# Validate experiment integrity
print("\n=== EXPERIMENT VALIDATION ===")

# 1. Check sample ratio
variant_counts = df['variant'].value_counts()
print(f"\nSample sizes:")
print(variant_counts)
print(f"\nRatio: {variant_counts['treatment'] / variant_counts['control']:.2f}")
# Should be close to 1.0 (50/50 split)

# 2. Check for sample ratio mismatch (SRM)
from scipy.stats import chisquare
total = len(df)
expected = [total/2, total/2]
observed = [variant_counts['control'], variant_counts['treatment']]
chi2, p_value = chisquare(observed, expected)
print(f"\nSRM p-value: {p_value:.4f}")
if p_value < 0.05:
    print("⚠️ WARNING: Sample Ratio Mismatch detected!")
else:
    print("✅ No SRM detected")

# 3. Check for time imbalance
df['date'] = pd.to_datetime(df['date'])
daily_split = df.groupby(['date', 'variant']).size().unstack()
print("\nDaily participant counts:")
print(daily_split)
```

**Challenge 2: Calculate Primary Metric**
```python
# Calculate abandonment rates
results = df.groupby('variant').agg({
    'user_id': 'count',
    'abandoned': 'sum'
}).rename(columns={'user_id': 'users', 'abandoned': 'abandoned_count'})

results['abandonment_rate'] = results['abandoned_count'] / results['users']
results['completion_rate'] = 1 - results['abandonment_rate']

print("\n=== PRIMARY METRIC RESULTS ===")
print(results)

# Calculate absolute and relative change
control_rate = results.loc['control', 'abandonment_rate']
treatment_rate = results.loc['treatment', 'abandonment_rate']

absolute_change = treatment_rate - control_rate
relative_change = (treatment_rate - control_rate) / control_rate

print(f"\nControl abandonment: {control_rate*100:.2f}%")
print(f"Treatment abandonment: {treatment_rate*100:.2f}%")
print(f"Absolute change: {absolute_change*100:.2f} percentage points")
print(f"Relative change: {relative_change*100:.2f}%")
```

**Challenge 3: Statistical Significance Test**
```python
# Prepare data for hypothesis test
control_abandoned = results.loc['control', 'abandoned_count']
control_total = results.loc['control', 'users']
treatment_abandoned = results.loc['treatment', 'abandoned_count']
treatment_total = results.loc['treatment', 'users']

# Two-proportion z-test
from statsmodels.stats.proportion import proportions_ztest

counts = np.array([treatment_abandoned, control_abandoned])
nobs = np.array([treatment_total, control_total])

z_stat, p_value = proportions_ztest(counts, nobs)

print("\n=== STATISTICAL SIGNIFICANCE ===")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print(f"✅ SIGNIFICANT at {alpha} level (p={p_value:.4f})")
    print("We can reject the null hypothesis")
else:
    print(f"❌ NOT SIGNIFICANT at {alpha} level (p={p_value:.4f})")
    print("Cannot reject the null hypothesis")

# Calculate confidence interval
from statsmodels.stats.proportion import proportion_confint

treatment_rate_ci = proportion_confint(treatment_abandoned, treatment_total, alpha=0.05, method='wilson')
control_rate_ci = proportion_confint(control_abandoned, control_total, alpha=0.05, method='wilson')

print(f"\n95% Confidence Intervals:")
print(f"Control: {control_rate_ci[0]*100:.2f}% - {control_rate_ci[1]*100:.2f}%")
print(f"Treatment: {treatment_rate_ci[0]*100:.2f}% - {treatment_rate_ci[1]*100:.2f}%")
```

**Challenge 4: Check Secondary Metrics**
```python
# Analyze secondary metrics
secondary_metrics = df.groupby('variant').agg({
    'checkout_time_seconds': 'mean',
    'revenue_per_session': 'mean',
    'satisfaction_score': 'mean'
})

print("\n=== SECONDARY METRICS ===")
print(secondary_metrics)

# T-tests for continuous metrics
from scipy.stats import ttest_ind

for metric in ['checkout_time_seconds', 'revenue_per_session', 'satisfaction_score']:
    control_values = df[df['variant'] == 'control'][metric].dropna()
    treatment_values = df[df['variant'] == 'treatment'][metric].dropna()
    
    t_stat, p_val = ttest_ind(control_values, treatment_values)
    
    mean_control = control_values.mean()
    mean_treatment = treatment_values.mean()
    pct_change = ((mean_treatment - mean_control) / mean_control) * 100
    
    print(f"\n{metric}:")
    print(f"  Control: {mean_control:.2f}")
    print(f"  Treatment: {mean_treatment:.2f}")
    print(f"  Change: {pct_change:+.2f}%")
    print(f"  P-value: {p_val:.4f}")
    print(f"  Significant: {'Yes' if p_val < 0.05 else 'No'}")
```

**Challenge 5: Visualize Results**
```python
# Create comprehensive results visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Plot 1: Abandonment rates with confidence intervals
ax1 = axes[0, 0]
variants = ['Control', 'Treatment']
rates = [control_rate, treatment_rate]
ci_lower = [control_rate_ci[0], treatment_rate_ci[0]]
ci_upper = [control_rate_ci[1], treatment_rate_ci[1]]
errors = [[rates[i] - ci_lower[i] for i in range(2)],
          [ci_upper[i] - rates[i] for i in range(2)]]

ax1.bar(variants, [r*100 for r in rates], yerr=[[e*100 for e in errors[0]], [e*100 for e in errors[1]]], 
        capsize=10, color=['#FF6B6B', '#4ECDC4'])
ax1.set_ylabel('Abandonment Rate (%)')
ax1.set_title('Cart Abandonment: Control vs Treatment')
ax1.axhline(y=control_rate*100, color='red', linestyle='--', alpha=0.5, label='Control baseline')

# Plot 2: Daily trend
ax2 = axes[0, 1]
daily_rates = df.groupby(['date', 'variant']).apply(
    lambda x: (x['abandoned'].sum() / len(x)) * 100
).unstack()
daily_rates.plot(ax=ax2, marker='o')
ax2.set_ylabel('Abandonment Rate (%)')
ax2.set_title('Daily Abandonment Rates')
ax2.legend(['Control', 'Treatment'])
ax2.grid(alpha=0.3)

# Plot 3: Distribution of checkout times
ax3 = axes[1, 0]
df.boxplot(column='checkout_time_seconds', by='variant', ax=ax3)
ax3.set_title('Checkout Time Distribution')
ax3.set_xlabel('Variant')
ax3.set_ylabel('Time (seconds)')

# Plot 4: Sample size by variant
ax4 = axes[1, 1]
ax4.bar(['Control', 'Treatment'], [control_total, treatment_total], color=['#FF6B6B', '#4ECDC4'])
ax4.set_ylabel('Number of Users')
ax4.set_title('Sample Sizes')
for i, v in enumerate([control_total, treatment_total]):
    ax4.text(i, v, f'{v:,}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('ab_test_results.png', dpi=300)
plt.show()
```

**Deliverable:**
- Complete analysis notebook
- Statistical test results
- Visualization dashboard
- Recommendation document

**Time:** 4-5 hours

---

### LAB 4: Common A/B Testing Pitfalls

**Objective:** Learn to avoid experiment mistakes

**Challenge 1: Peeking Problem**
```
SCENARIO: You check test results after 3 days

Day 3 results:
- Control: 70% abandonment (n=1,200)
- Treatment: 63% abandonment (n=1,200)
- P-value: 0.03 (significant!)

TEMPTATION: "It's working! Let's stop and ship it!"

WHY THIS IS WRONG:
- Random early fluctuations
- Regression to the mean
- Inflated false positive rate
- Multiple testing problem

CORRECT APPROACH:
- Run full 2 weeks as planned
- Don't peek at p-values
- Use sequential testing if must monitor
- Document any early looks

FINAL RESULTS (Day 14):
- Control: 68% abandonment (n=8,400)
- Treatment: 66% abandonment (n=8,400)
- P-value: 0.15 (NOT significant!)

Early stop would have been WRONG DECISION!
```

**Challenge 2: Multiple Comparisons**
```
SCENARIO: You test 20 different button colors

Results:
- 19 variants: No significant difference
- 1 variant (Yellow): P-value = 0.04 (significant!)

TEMPTATION: "Yellow is the winner!"

WHY THIS IS WRONG:
- With 20 tests at α=0.05, expect 1 false positive
- 20 * 0.05 = 1 spurious result expected by chance
- This is likely that false positive!

CORRECT APPROACH:
- Bonferroni correction: α / number_of_tests
- Adjusted α = 0.05 / 20 = 0.0025
- Yellow p=0.04 is NOT significant at α=0.0025

OR:
- Primary hypothesis: Best guess color
- Secondary exploratory: Other colors (don't act on these)
```

**Challenge 3: Selection Bias**
```
SCENARIO: Mobile vs Desktop test

WRONG APPROACH:
- Run test on desktop only
- See positive results
- Ship to all users (desktop + mobile)

PROBLEM:
- Mobile users may behave differently
- Desktop results don't generalize
- Could hurt mobile experience

CORRECT APPROACH:
- Stratified randomization
- Test on ALL user segments
- Analyze results by segment
- Ship only where proven effective

ANALYSIS:
Control  → Treatment  | Change | Significant?
Desktop:  70% → 62%  | -8% ✅  | Yes (p=0.02)
Mobile:   65% → 66%  | +1% ❌  | No (p=0.82)

DECISION: Ship to desktop only, keep testing mobile
```

**Challenge 4: Novelty Effects**
```
SCENARIO: New design shows 15% improvement in Week 1

Week 1: +15% improvement ✅
Week 2: +8% improvement 
Week 3: +2% improvement
Week 4: -1% degradation ❌

EXPLANATION:
- Novelty effect: Users try new things
- Wears off as users habituate
- Long-term effect is negative!

CORRECT APPROACH:
- Run tests for multiple weeks/months
- Watch for decay in effect
- Segment new vs returning users
- Consider long-term impact
```

**Challenge 5: Simpson's Paradox**
```
SCENARIO: Overall results vs segmented results

OVERALL:
Treatment wins! 45% conversion vs 40% control

BY SEGMENT:
Mobile:   Control 50% > Treatment 48% ❌
Desktop:  Control 35% > Treatment 33% ❌

HOW IS THIS POSSIBLE?
- Simpson's Paradox
- Segment sizes differ between variants
- Treatment had more mobile users (higher converting)
- Within each segment, control actually wins!

CORRECT APPROACH:
- Always analyze by key segments
- Check for imbalanced segment distribution
- Use stratified analysis
- Don't rely on overall metrics alone
```

**Deliverable:**
- Pitfalls checklist
- Analysis playbook
- Decision framework

**Time:** 3-4 hours

---

### MINI PROJECT 7: Complete A/B Test Execution

**Objective:** Design, run, and analyze a complete A/B test

**Scenario:** E-commerce company wants to test new product recommendation algorithm

**Phase 1: Planning (2 hours)**
1. Define hypothesis
2. Choose primary & secondary metrics
3. Calculate sample size
4. Plan randomization
5. Set test duration
6. Document stopping rules

**Phase 2: Implementation (2 hours)**
1. Write randomization code
2. Build tracking system
3. Implement both variants
4. Set up monitoring dashboard
5. Create QA checklist

**Phase 3: Data Collection (Simulated - 1 hour)**
1. Generate realistic test data
2. Simulate 2 weeks of traffic
3. Include realistic noise/variance
4. Add edge cases

**Phase 4: Analysis (3 hours)**
1. Validate experiment integrity
2. Calculate all metrics
3. Run statistical tests
4. Create visualizations
5. Check for segments/interactions

**Phase 5: Reporting (2 hours)**
1. Executive summary (1 page)
2. Detailed analysis (5 pages)
3. Recommendation with rationale
4. Implementation plan
5. Next steps/follow-up tests

**Deliverable:**
- Complete test design doc
- Analysis code (Jupyter notebook)
- Results presentation (PowerPoint)
- Recommendation memo

**Time:** 10-12 hours

**Success Criteria for Unit 6:**
- ✅ Design rigorous experiments
- ✅ Calculate proper sample sizes
- ✅ Analyze results correctly
- ✅ Avoid common pitfalls
- ✅ Make data-driven decisions
- ✅ Portfolio-ready A/B test project

"""
        )
    elif unit_number == 7:
        st.markdown("#### 📘 Data Analyst Capstone Project: Your Portfolio Showpiece")
        st.markdown(
            """**The capstone is your chance to prove you can do the job.**

This isn't a theoretical exercise—it's a **real-world analysis project** that demonstrates 
every skill you've learned. Done well, this project becomes your **portfolio centerpiece** 
that gets you hired.

---

**What is the Capstone?**

An end-to-end data analysis project where you:
1. Define a business problem
2. Gather and clean data
3. Perform analysis
4. Create visualizations
5. Tell the story
6. Make recommendations

**Duration:** 2-4 weeks  
**Output:** Professional analysis deliverable

---

**Why It Matters:**

**For Learning:**
- Synthesizes all skills (SQL, Excel, Python, visualization, storytelling)
- Builds confidence in your abilities
- Identifies knowledge gaps to address

**For Job Search:**
- Portfolio piece to show employers
- Talking point in interviews
- Proof you can deliver results

**Hiring managers want to see:**
- "Can this person solve our problems?"
- Capstone answers: "YES, here's proof."

---

**Capstone vs Coursework:**

| Coursework | Capstone |
|------------|----------|
| Prescribed problem | You choose the problem |
| Clean data provided | You find and clean data |
| Single skill focus | All skills integrated |
| Short (1-2 hours) | Extended (2-4 weeks) |
| Grade-focused | Portfolio-focused |

**Capstone is YOUR project. Own it.**
"""
        )

        st.markdown("#### 🧱 Capstone Structure: The Framework for Success")
        st.markdown(
            """**Follow this structure for a professional deliverable:**

---

### 1. EXECUTIVE SUMMARY (1 page)

**Purpose:** Busy stakeholders read ONLY this. Make it count.

**Include:**
- **Business Problem** (2 sentences): What question are you answering? Why does it matter?
- **Key Findings** (3 bullet points): What did you discover?
- **Recommendation** (1 paragraph): What should be done?
- **Impact** (1 sentence): What's the expected outcome?

**Example:**

*"Hospital DNA (Did Not Attend) rates have increased from 12% to 15% over 6 months, 
costing approximately £30,000 in lost revenue monthly. Analysis reveals Dermatology 
and new patient appointments drive this increase. Implementing SMS reminders for 
these segments is projected to reduce DNAs by 30-40%, recovering £9,000-£12,000 
monthly at a cost of only £200. Immediate implementation recommended."*

---

### 2. BUSINESS CONTEXT (1-2 pages)

**Purpose:** Frame the problem and its importance

**2.1 Problem Statement**
- What's the specific question?
- Why is this important NOW?
- Who are the stakeholders?
- What decision will this inform?

**2.2 Success Criteria**
- What would "good" look like?
- What's the target/benchmark?
- How will we measure success?

**2.3 Scope & Constraints**
- What's included? (time period, departments, etc.)
- What's excluded?
- Any data limitations?
- Timeline for this analysis

**Example Section:**

*"The Outpatient Department has seen DNA rates increase from 12% to 15% between 
January and June 2024. This represents 300 wasted appointment slots monthly and 
approximately £30,000 in lost revenue. The Head of Operations needs to understand:*

*1. Which clinics/specialties are most affected?*
*2. Are there patterns (day of week, appointment type, patient demographics)?*
*3. What interventions would be most effective?*

*This analysis will inform a £10,000 investment in appointment reminder systems. 
Success means reducing DNA rates to <12% within 3 months of implementation."*

---

### 3. DATA & METHODOLOGY (2-3 pages)

**Purpose:** Document your approach (reproducibility!)

**3.1 Data Sources**
- Where did data come from? (databases, files, APIs)
- Date range covered
- Number of records
- Key fields used

**3.2 Data Quality Assessment**
- Missing values found (how handled?)
- Duplicates (removed?)
- Outliers (investigated?)
- Data transformations applied

**3.3 Analytical Approach**
- What methods did you use? (SQL queries, Python scripts, Excel)
- Why these methods?
- Any assumptions made?

**Include code snippets or query examples** to show technical competence

**Example:**

*"Data extracted from hospital appointment database covering Jan-Jun 2024:*
- *23,456 total appointments across 12 specialties*
- *Key fields: appointment_date, specialty, patient_age, appointment_type, status*
- *Removed 234 cancelled appointments (1% of total)*
- *Found 12 duplicate records due to rebooking (removed)*
- *No missing values in critical fields*

*Analysis performed using:*
- *SQL for data extraction and grouping*
- *Python (Pandas) for deeper segmentation analysis*
- *Excel for final visualizations and dashboard"*

---

### 4. ANALYSIS & FINDINGS (3-5 pages)

**Purpose:** Show what you discovered

**Organize by Key Questions/Findings** (not by method!)

**For Each Finding:**
- Visualization (chart/graph)
- Interpretation (what does it mean?)
- Supporting data (numbers/percentages)

**Finding Format:**

**FINDING 1: DNA rates vary significantly by specialty**

[INSERT CHART: Bar chart of DNA rate by specialty]

*"Dermatology shows the highest DNA rate at 18%, significantly above the hospital 
average of 15%. Cardiology (14%) and Orthopedics (12%) are closer to average. 
This represents a 6 percentage point difference between highest and lowest, 
suggesting specialty-specific factors at play."*

**Why this matters:** *Dermatology handles 2,000 appointments monthly, so 18% DNA rate = 
360 wasted slots vs 240 if at hospital average. Targeting Dermatology could recover 
120 appointment slots monthly.*

**Do this for 3-5 key findings.**

---

### 5. DASHBOARD / VISUAL SUMMARY (1-2 pages)

**Purpose:** Interactive or static dashboard summarizing key metrics

**Include:**
- KPI cards (main numbers)
- Trend charts (over time)
- Comparison charts (by category)
- Filters (if interactive)

**This becomes your** ***visual portfolio piece***

---

### 6. RECOMMENDATIONS & NEXT STEPS (1-2 pages)

**Purpose:** Turn insights into action

**For Each Recommendation:**

**RECOMMENDATION 1: Implement SMS reminders for Dermatology new patients**

**Rationale:** This segment shows highest DNA rate (22%)

**Expected Impact:**
- Research shows SMS reminders reduce DNA by 30-40%
- Applied to Dermatology: 18% → 11-13% DNA rate
- Recovers 100-140 appointment slots monthly
- Revenue impact: £10,000-£14,000/month

**Implementation:**
- Cost: £200/month for SMS service
- Timeline: 2 weeks to set up
- Owner: Dermatology Department Manager

**ROI:** 50-70x (£12,000 benefit vs £200 cost monthly)

**Do this for 2-4 recommendations** (prioritized)

---

### 7. LIMITATIONS & FUTURE WORK (1 page)

**Purpose:** Show critical thinking

**Acknowledge:**
- What couldn't you analyze? (missing data, time constraints)
- What assumptions did you make?
- What would you do differently with more time/data?
- What future questions emerged?

**Example:**

*"This analysis has limitations:*

*1. Only 6 months of data available; longer time series would reveal seasonal patterns*
*2. Patient demographic data limited (no deprivation index, ethnicity)*
*3. No data on reminder method currently used (SMS vs phone vs none)*
*4. Couldn't analyze travel time/distance to hospital*

*Future work should:*
- *A/B test SMS reminders vs current approach*
- *Analyze geographic patterns using full postcode data*
- *Survey patients who DNA to understand reasons"*

---

### 8. APPENDIX (Optional)

**Include:**
- Full SQL queries
- Python code
- Detailed tables
- Additional charts
- Data dictionary

---

**Total Length:** 10-15 pages (not including appendix)

**Format:** PDF for portfolio, PowerPoint for presentation
"""
        )

        st.markdown("#### 🎯 Capstone Project Ideas & Examples")
        st.markdown(
            """**Choose a project that showcases your skills AND interests a potential employer.**

---

### Healthcare Projects

**1. Emergency Department Wait Time Analysis**
- Question: What factors contribute to long ED wait times?
- Data: ED visits, arrival times, triage codes, discharge times
- Analysis: Identify bottlenecks, peak periods, staffing gaps
- Recommendation: Staffing optimization plan

**2. Readmission Rate Reduction**
- Question: Which patients are most likely to be readmitted?
- Data: Patient demographics, diagnoses, length of stay, readmissions
- Analysis: Identify high-risk profiles
- Recommendation: Targeted follow-up program

---

### Retail/E-commerce Projects

**3. Customer Segmentation & Targeting**
- Question: How should we segment customers for marketing?
- Data: Purchase history, demographics, browsing behavior
- Analysis: RFM analysis (Recency, Frequency, Monetary value)
- Recommendation: Segment-specific marketing strategy

**4. Product Performance Analysis**
- Question: Which products drive profitability? Which should we discontinue?
- Data: Sales, costs, inventory, returns
- Analysis: Profit margin by product, inventory turnover
- Recommendation: Product portfolio optimization

---

### SaaS/Technology Projects

**5. Churn Prediction & Prevention**
- Question: Why are customers canceling subscriptions?
- Data: Usage logs, customer support tickets, payment history
- Analysis: Identify churn signals, usage patterns
- Recommendation: At-risk customer intervention plan

**6. Feature Adoption Analysis**
- Question: Which new features are users actually using?
- Data: Feature usage logs, user cohorts, feedback
- Analysis: Adoption rates, correlation with retention
- Recommendation: Product roadmap priorities

---

### Financial Services Projects

**7. Loan Default Risk Analysis**
- Question: Which applicant profiles are high-risk for default?
- Data: Credit scores, income, employment, loan history
- Analysis: Default rates by segment, risk factors
- Recommendation: Lending criteria refinement

---

### Marketing Projects

**8. Campaign Performance Optimization**
- Question: Which marketing channels deliver best ROI?
- Data: Campaign spend, conversions, customer acquisition cost
- Analysis: ROI by channel, audience segment performance
- Recommendation: Budget reallocation plan

---

**How to Choose YOUR Project:**

1. **Pick your target industry** (where do you want to work?)
2. **Choose realistic data** (publicly available or simulatable)
3. **Ensure it showcases ALL skills** (SQL, visualization, storytelling)
4. **Make it impressive** (real business impact, clear recommendations)
"""
        )

        st.markdown("#### ✅ Capstone Assessment Rubric")
        st.markdown(
            """**Use this to self-assess before submission:**

---

| Criteria | Excellent (A) | Good (B) | Needs Improvement (C) |
|----------|---------------|----------|----------------------|
| **Business Problem** | Clearly defined, relevant, impactful | Defined but could be more specific | Vague or unclear |
| **Data Quality** | Comprehensive cleaning documented, all issues addressed | Adequate cleaning, minor gaps | Insufficient cleaning or undocumented |
| **Analysis Depth** | Multiple angles explored, segmented, insightful | Basic analysis done, some depth | Surface-level only |
| **Visualizations** | Professional, clear, tell story | Adequate but could be better | Confusing or amateur |
| **Insights** | Novel, actionable, well-supported | Solid but predictable | Obvious or not supported |
| **Recommendations** | Specific, prioritized, ROI calculated | General but reasonable | Vague or impractical |
| **Communication** | Executive summary perfect, flows logically | Good structure, minor improvements needed | Hard to follow |
| **Technical Skill** | Advanced techniques, efficient code | Solid fundamentals demonstrated | Basic skills only |
| **Professionalism** | Portfolio-ready, no errors | Minor polish needed | Sloppy or incomplete |

---

**Target:** All criteria at "Excellent" or "Good" level

**This is your portfolio piece—make it PERFECT.**
"""
        )

        st.markdown("#### 💼 Turning Your Capstone into Job Offers")
        st.markdown(
            """**Your capstone should directly lead to interviews. Here's how:**

---

### 1. Portfolio Presentation

**Create:**
- **GitHub repository** with code and README
- **PDF report** (polished, professional)
- **Presentation deck** (10-15 slides)
- **2-minute video** walkthrough (optional but powerful)

**Portfolio Website:**
- Dedicate a page to this project
- Include visualizations
- Link to GitHub
- Show the impact

---

### 2. Resume Entry

**BEFORE (weak):**
*"Completed data analysis capstone project"*

**AFTER (strong):**
*"Analyzed 20,000+ hospital appointment records to identify DNA rate drivers, resulting in recommendation projected to save £180,000 annually through SMS reminder optimization"*

**Format:**
- Lead with impact/result
- Include scale (data size, timeframe)
- Mention methods (SQL, Python)
- Quantify benefit

---

### 3. LinkedIn Post

**Announce your project:**

*"I just completed a deep-dive analysis of hospital appointment DNA (Did Not Attend) rates 📊*

*Using SQL and Python, I analyzed 23,000 appointments and uncovered that Dermatology new patient appointments have 22% DNA rates—costing £15,000/month in lost revenue.*

*My recommendation: Implement targeted SMS reminders, projected to reduce DNAs by 35% and save £180K annually at minimal cost.*

*This project taught me that data analysis isn't just about numbers—it's about driving real business impact.*

*Full analysis: [link to GitHub]*

*#DataAnalytics #Healthcare #DataScience"*

**Include:** Chart or dashboard image

---

### 4. Interview Talking Points

**Prepare to discuss:**
- **Problem:** "The hospital was losing £30K monthly..."
- **Approach:** "I used SQL to extract data, Python for segmentation..."
- **Challenge:** "The data had duplicates from rebookings, so I..."
- **Finding:** "I discovered that 22% of new Dermatology appointments..."
- **Impact:** "My recommendation could save £180K annually..."
- **Learning:** "This taught me the importance of segmentation..."

**Practice this story until smooth (2-3 minutes)**

---

### 5. Follow-Up After Applications

**If applying to similar industry (e.g., healthcare analytics):**

*"I noticed your company works with hospital data. I recently completed an analysis of appointment DNA rates that identified opportunities to save £180K annually. I'd love to discuss how similar analysis could benefit [Company Name]. May I share my findings?"*

**Attach your capstone PDF**

**Response rate:** 10-20% (vs <1% for generic applications)

---

**Your capstone isn't just coursework—it's your BEST SALES TOOL for landing your first data analyst role.**

**Make it count.**

---

## 🔬 HANDS-ON LABS - Unit 7: Capstone Success

### LAB 1: Capstone Planning & Scoping

**Objective:** Define compelling capstone project (2-3 hours)

**Step 1: Choose Domain** - Select industry (healthcare, e-commerce, SaaS)
**Step 2: Identify Problem** - Brainstorm 5 potential business questions
**Step 3: Problem Statement** - Write clear, measurable problem
**Step 4: Success Metrics** - Define primary & secondary metrics
**Step 5: Data Sourcing** - Confirm data availability (10K+ records)

**Deliverable:** 1-page project proposal

---

### LAB 2: Data Collection & Preparation

**Objective:** Gather and clean capstone dataset (4-6 hours)

```python
# Generate synthetic e-commerce data
from faker import Faker
import random, pandas as pd

fake = Faker()
data = []
for i in range(20000):
    record = {
        'order_id': f'ORD{i:05d}',
        'customer_id': f'CUST{random.randint(1,5000):04d}',
        'order_date': fake.date_between(start_date='-1y'),
        'product': random.choice(['Electronics','Clothing','Home']),
        'quantity': random.randint(1,5),
        'price': round(random.uniform(5,200),2),
        'abandoned': random.random() < 0.68
    }
    data.append(record)

df = pd.DataFrame(data)
df.to_csv('capstone_data.csv', index=False)
```

**Data Quality Assessment:**
- Check missing values: `df.isnull().sum()`
- Find duplicates: `df.duplicated().sum()`
- Validate ranges: `df.describe()`

**Cleaning Steps:**
1. Remove duplicates
2. Handle missing values (fill/drop)
3. Fix data types
4. Remove outliers (IQR method)
5. Add derived fields (year, month, day_of_week)

**Deliverable:** Cleaned dataset + quality report

---

### LAB 3: Analysis & Visualization

**Objective:** Generate insights from data (6-8 hours)

**Key Analyses:**
1. Descriptive statistics (mean, median, distribution)
2. Segmentation analysis (by device, region, category)
3. Time series patterns (daily/weekly trends)
4. Statistical testing (chi-square, t-tests)

**Visualizations to Create:**
- Abandonment rate by segment (bar chart)
- Daily trend over time (line chart)
- Heatmap of patterns
- Distribution plots

**Statistical Tests:**
```python
from scipy.stats import chi2_contingency, ttest_ind

# Test mobile vs desktop abandonment
contingency = pd.crosstab(df['device'], df['abandoned'])
chi2, p_value, dof, exp = chi2_contingency(contingency)
print(f"Chi-square: {chi2:.2f}, p-value: {p_value:.4f}")
```

**Deliverable:** Analysis notebook + 10+ visualizations

---

### LAB 4: Final Report & Presentation

**Objective:** Create professional deliverables (4-6 hours)

**Outputs Required:**
1. **Executive Summary** (1 page) - Problem, findings, recommendation
2. **PowerPoint Presentation** (10-12 slides) - Story format
3. **PDF Report** (10-15 pages) - Complete analysis
4. **GitHub Repository** - Code, data, documentation
5. **Interactive Dashboard** - Plotly or Tableau

**GitHub Structure:**
```
capstone-project/
├── README.md
├── data/ (raw + cleaned)
├── notebooks/ (analysis code)
├── reports/ (PDF + PPT)
├── images/ (visualizations)
└── requirements.txt
```

**Deliverable:** Complete portfolio-ready project

---

### 💼 DATA ANALYST INTERVIEW PREP

**100+ Technical & Behavioral Questions**

**SQL Questions (Sample 10):**

1. **Difference between INNER JOIN and LEFT JOIN?**
   INNER: matching records only. LEFT: all from left + matches from right.

2. **Find duplicate records?**
```sql
SELECT column, COUNT(*)
FROM table
GROUP BY column
HAVING COUNT(*) > 1;
```

3. **WHERE vs HAVING?**
   WHERE filters before grouping. HAVING filters after aggregation.

4. **Running total?**
```sql
SELECT date, revenue,
  SUM(revenue) OVER (ORDER BY date) as running_total
FROM sales;
```

5. **Window functions?**
   Calculations across rows related to current row.
```sql
SELECT customer_id, revenue,
  RANK() OVER (PARTITION BY customer_id ORDER BY revenue DESC) as rank
FROM orders;
```

**Python/Pandas Questions (Sample 10):**

1. **Read CSV?**
```python
df = pd.read_csv('data.csv')
```

2. **Handle missing values?**
```python
df.isnull().sum()  # Check
df.fillna(0)  # Fill with 0
df.dropna()  # Drop rows
df['col'].fillna(df['col'].mean())  # Fill with mean
```

3. **loc vs iloc?**
   loc: label-based. iloc: position-based.

4. **Group and aggregate?**
```python
df.groupby('category').agg({
    'revenue': ['sum', 'mean'],
    'orders': 'count'
})
```

5. **Merge DataFrames?**
```python
pd.merge(df1, df2, on='customer_id', how='inner')
```

**Statistics Questions (Sample 10):**

1. **p-value meaning?**
   Probability of observing results if null hypothesis is true. p<0.05 = significant.

2. **Type I vs Type II error?**
   Type I: False positive (reject true null). Type II: False negative (accept false null).

3. **Confidence interval?**
   Range where true parameter likely falls. 95% CI = 95% chance contains true value.

4. **Correlation vs causation?**
   Correlation: variables move together. Causation: one causes the other.

5. **Sample size calculation?**
   Depends on: effect size, significance level, power, baseline rate.

**Behavioral Questions (Sample 10):**

1. **Tell me about a time you used data to solve a problem.**
   Use STAR method (Situation, Task, Action, Result).

2. **How do you prioritize multiple analyses?**
   By business impact, urgency, stakeholder needs, data availability.

3. **Describe a time you had messy data.**
   Explain cleaning process: assess, clean, validate, document.

4. **How do you explain technical concepts to non-technical stakeholders?**
   Use analogies, visualizations, focus on business impact.

5. **Disagreement with stakeholder?**
   Listen, understand concerns, present data, find compromise.

**Success Criteria for Unit 7:**
- ✅ Complete capstone project
- ✅ Professional portfolio (GitHub)
- ✅ Interview-ready presentation
- ✅ Technical knowledge tested
- ✅ Career materials ready

"""
        )

        st.markdown("---")
        st.markdown("## 🏥 INDUSTRY MODULE: HEALTHCARE ANALYTICS")
        st.markdown(
            """**Complete healthcare data analytics scenarios with real datasets and solutions**

### Healthcare Analytics Overview

Healthcare generates MASSIVE amounts of data:
- 30% of world's data volume
- Patient records, appointments, diagnoses, prescriptions
- Hospital operations, staffing, capacity
- Financial data, claims, reimbursements
- Clinical trials, outcomes, quality metrics

**Key Healthcare Analytics Challenges:**
- Patient privacy (HIPAA compliance)
- Data quality and integration
- Real-time operational analytics
- Predictive modeling (readmissions, no-shows)
- Cost optimization
- Clinical outcome measurement

---

### Scenario 1: Emergency Department Wait Time Analysis

**Business Problem:** ED wait times exceed 4-hour target 42% of the time, risking regulatory penalties

**Dataset:** 50,000 ED visits over 12 months

```sql
-- ED Visits Table Structure
CREATE TABLE ed_visits (
    visit_id INT PRIMARY KEY,
    patient_id INT,
    arrival_datetime DATETIME,
    triage_time DATETIME,
    doctor_seen_time DATETIME,
    discharge_datetime DATETIME,
    triage_category VARCHAR(10),  -- 1 (critical) to 5 (minor)
    chief_complaint VARCHAR(100),
    department VARCHAR(50),
    admitted BOOLEAN,
    left_without_treatment BOOLEAN
);

-- Sample queries
-- 1. Calculate wait times and breach rate
SELECT 
    DATE(arrival_datetime) as date,
    COUNT(*) as visits,
    AVG(TIMESTAMPDIFF(MINUTE, arrival_datetime, doctor_seen_time)) as avg_wait_mins,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY TIMESTAMPDIFF(MINUTE, arrival_datetime, doctor_seen_time)) as median_wait,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY TIMESTAMPDIFF(MINUTE, arrival_datetime, doctor_seen_time)) as p95_wait,
    SUM(CASE WHEN TIMESTAMPDIFF(MINUTE, arrival_datetime, discharge_datetime) > 240 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as breach_rate_pct
FROM ed_visits
WHERE discharge_datetime IS NOT NULL
GROUP BY DATE(arrival_datetime)
ORDER BY date;

-- 2. Analyze by triage category
SELECT 
    triage_category,
    COUNT(*) as visits,
    AVG(TIMESTAMPDIFF(MINUTE, arrival_datetime, doctor_seen_time)) as avg_wait,
    SUM(CASE WHEN TIMESTAMPDIFF(MINUTE, arrival_datetime, discharge_datetime) > 240 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as breach_rate
FROM ed_visits
GROUP BY triage_category
ORDER BY triage_category;

-- 3. Peak hours analysis
SELECT 
    HOUR(arrival_datetime) as hour,
    COUNT(*) as arrivals,
    AVG(TIMESTAMPDIFF(MINUTE, arrival_datetime, doctor_seen_time)) as avg_wait
FROM ed_visits
GROUP BY HOUR(arrival_datetime)
ORDER BY hour;

-- 4. Day of week patterns
SELECT 
    DAYNAME(arrival_datetime) as day_of_week,
    COUNT(*) as visits,
    AVG(TIMESTAMPDIFF(MINUTE, arrival_datetime, doctor_seen_time)) as avg_wait,
    SUM(CASE WHEN TIMESTAMPDIFF(MINUTE, arrival_datetime, discharge_datetime) > 240 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as breach_rate
FROM ed_visits
GROUP BY DAYNAME(arrival_datetime), DAYOFWEEK(arrival_datetime)
ORDER BY DAYOFWEEK(arrival_datetime);
```

**Python Analysis:**
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('ed_visits.csv')
df['arrival_datetime'] = pd.to_datetime(df['arrival_datetime'])
df['doctor_seen_time'] = pd.to_datetime(df['doctor_seen_time'])
df['discharge_datetime'] = pd.to_datetime(df['discharge_datetime'])

# Calculate wait times
df['wait_to_doctor_mins'] = (df['doctor_seen_time'] - df['arrival_datetime']).dt.total_seconds() / 60
df['total_time_mins'] = (df['discharge_datetime'] - df['arrival_datetime']).dt.total_seconds() / 60
df['breach'] = df['total_time_mins'] > 240

# Key metrics
print(f"Total visits: {len(df):,}")
print(f"Average wait to doctor: {df['wait_to_doctor_mins'].mean():.1f} minutes")
print(f"Median wait: {df['wait_to_doctor_mins'].median():.1f} minutes")
print(f"95th percentile: {df['wait_to_doctor_mins'].quantile(0.95):.1f} minutes")
print(f"Breach rate: {df['breach'].mean()*100:.1f}%")

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Wait time distribution
axes[0, 0].hist(df['wait_to_doctor_mins'], bins=50, edgecolor='black')
axes[0, 0].axvline(df['wait_to_doctor_mins'].median(), color='red', linestyle='--', label='Median')
axes[0, 0].set_xlabel('Wait Time (minutes)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Wait Time Distribution')
axes[0, 0].legend()

# 2. Breach rate by triage
triage_analysis = df.groupby('triage_category').agg({
    'breach': 'mean',
    'visit_id': 'count'
}).reset_index()
triage_analysis['breach_pct'] = triage_analysis['breach'] * 100
axes[0, 1].bar(triage_analysis['triage_category'], triage_analysis['breach_pct'])
axes[0, 1].set_xlabel('Triage Category')
axes[0, 1].set_ylabel('Breach Rate (%)')
axes[0, 1].set_title('Breach Rate by Triage Category')

# 3. Hourly arrival patterns
hourly = df.groupby(df['arrival_datetime'].dt.hour)['visit_id'].count()
axes[1, 0].plot(hourly.index, hourly.values, marker='o')
axes[1, 0].set_xlabel('Hour of Day')
axes[1, 0].set_ylabel('Arrivals')
axes[1, 0].set_title('Arrivals by Hour')
axes[1, 0].grid(True, alpha=0.3)

# 4. Day of week patterns
daily = df.groupby(df['arrival_datetime'].dt.day_name())['breach'].mean() * 100
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily = daily.reindex(day_order)
axes[1, 1].bar(range(7), daily.values)
axes[1, 1].set_xticks(range(7))
axes[1, 1].set_xticklabels(day_order, rotation=45)
axes[1, 1].set_ylabel('Breach Rate (%)')
axes[1, 1].set_title('Breach Rate by Day of Week')

plt.tight_layout()
plt.savefig('ed_wait_time_analysis.png', dpi=300)
plt.show()
```

**Key Findings:**
- Triage 3 patients have longest waits (avg 127 mins)
- Peak hours 10am-2pm and 6pm-10pm = 45% of breaches
- Monday and Friday worst days (48% breach rate)
- Strong correlation (r=0.72) between staffing gaps and wait times

**Recommendations:**
1. Add 2 nurses during peak hours (10am-2pm, 6pm-10pm) - Cost: £80K annually
2. Fast-track pathway for triage 4-5 patients - Estimated 15% breach reduction
3. Monday/Friday surge capacity planning - Additional locum cover
4. Real-time dashboard with alerts when wait >90 minutes

**Expected Impact:** £850K annual savings from avoided breaches

---

### Scenario 2: Appointment DNA (Did Not Attend) Rate Reduction

**Business Problem:** 18% DNA rate costing £250K monthly in lost capacity

**Dataset:** 120,000 appointments over 12 months

```sql
-- Appointments Table
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    clinic VARCHAR(50),
    specialty VARCHAR(50),
    appointment_date DATE,
    appointment_time TIME,
    appointment_type VARCHAR(20),  -- New, Follow-up, Urgent
    booking_date DATE,
    attended BOOLEAN,
    cancelled BOOLEAN,
    patient_age INT,
    patient_gender VARCHAR(10),
    patient_postcode VARCHAR(10),
    previous_dna_count INT,
    days_notice INT
);

-- Analysis queries
-- 1. Overall DNA rate
SELECT 
    COUNT(*) as total_appointments,
    SUM(CASE WHEN attended = 0 AND cancelled = 0 THEN 1 ELSE 0 END) as dna_count,
    SUM(CASE WHEN attended = 0 AND cancelled = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as dna_rate_pct
FROM appointments
WHERE appointment_date < CURDATE();

-- 2. DNA rate by specialty
SELECT 
    specialty,
    COUNT(*) as appointments,
    SUM(CASE WHEN attended = 0 AND cancelled = 0 THEN 1 ELSE 0 END) as dna_count,
    SUM(CASE WHEN attended = 0 AND cancelled = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as dna_rate_pct,
    AVG(days_notice) as avg_days_notice
FROM appointments
WHERE appointment_date < CURDATE()
GROUP BY specialty
ORDER BY dna_rate_pct DESC;

-- 3. DNA rate by appointment type and days notice
SELECT 
    appointment_type,
    CASE 
        WHEN days_notice <= 7 THEN '0-7 days'
        WHEN days_notice <= 14 THEN '8-14 days'
        WHEN days_notice <= 30 THEN '15-30 days'
        ELSE '30+ days'
    END as notice_period,
    COUNT(*) as appointments,
    SUM(CASE WHEN attended = 0 AND cancelled = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as dna_rate_pct
FROM appointments
WHERE appointment_date < CURDATE()
GROUP BY appointment_type, notice_period
ORDER BY appointment_type, dna_rate_pct DESC;

-- 4. Repeat DNA offenders
SELECT 
    patient_id,
    COUNT(*) as total_appointments,
    SUM(CASE WHEN attended = 0 AND cancelled = 0 THEN 1 ELSE 0 END) as dna_count,
    SUM(CASE WHEN attended = 0 AND cancelled = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as dna_rate_pct
FROM appointments
WHERE appointment_date < CURDATE()
GROUP BY patient_id
HAVING COUNT(*) >= 5 AND SUM(CASE WHEN attended = 0 AND cancelled = 0 THEN 1 ELSE 0 END) >= 2
ORDER BY dna_count DESC;
```

**Python Predictive Model:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# Prepare data
df = pd.read_csv('appointments.csv')
df['dna'] = ((df['attended'] == 0) & (df['cancelled'] == 0)).astype(int)

# Features
features = ['patient_age', 'previous_dna_count', 'days_notice', 'appointment_type_encoded', 
            'specialty_encoded', 'day_of_week', 'hour_of_day']

# Encode categoricals
df['appointment_type_encoded'] = df['appointment_type'].astype('category').cat.codes
df['specialty_encoded'] = df['specialty'].astype('category').cat.codes
df['day_of_week'] = pd.to_datetime(df['appointment_date']).dt.dayofweek

# Split data
X = df[features]
y = df['dna']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print("Classification Report:")
print(classification_report(y_test, y_pred))
print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")

# Feature importance
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(importance)

# High-risk appointments
df['dna_probability'] = model.predict_proba(X)[:, 1]
high_risk = df[df['dna_probability'] > 0.3].sort_values('dna_probability', ascending=False)

print(f"\nHigh-risk appointments: {len(high_risk):,}")
print(f"Expected DNAs in high-risk group: {high_risk['dna_probability'].sum():.0f}")
```

**Recommendations:**
1. SMS reminders for high-risk appointments (DNA prob >30%) - Reduces DNA by 35%
2. Automated calls for Dermatology new patients - Target: £15K monthly savings
3. Earlier rebooking for long-notice appointments - Reduce >30 day notice DNAs
4. Flagging system for repeat DNA patients - Special handling protocol

**Expected ROI:** £180K annual savings for £200/month SMS service = 900x ROI

---

### Scenario 3: Bed Capacity & Patient Flow Optimization

**Business Problem:** Bed occupancy averaging 92%, causing elective surgery cancellations

```sql
-- Bed occupancy analysis
WITH daily_occupancy AS (
    SELECT 
        date,
        ward,
        bed_capacity,
        patients_admitted,
        patients_discharged,
        LAG(census, 1) OVER (PARTITION BY ward ORDER BY date) + patients_admitted - patients_discharged as census
    FROM ward_daily_stats
)
SELECT 
    ward,
    AVG(census * 100.0 / bed_capacity) as avg_occupancy_pct,
    MAX(census * 100.0 / bed_capacity) as max_occupancy_pct,
    SUM(CASE WHEN census >= bed_capacity THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as days_at_capacity_pct
FROM daily_occupancy
GROUP BY ward
ORDER BY avg_occupancy_pct DESC;

-- Length of stay analysis
SELECT 
    ward,
    diagnosis_category,
    COUNT(*) as admissions,
    AVG(DATEDIFF(discharge_date, admission_date)) as avg_los_days,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY DATEDIFF(discharge_date, admission_date)) as median_los,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY DATEDIFF(discharge_date, admission_date)) as p90_los
FROM admissions
WHERE discharge_date IS NOT NULL
GROUP BY ward, diagnosis_category
HAVING COUNT(*) > 50
ORDER BY avg_los_days DESC;
```

---

### Scenario 4: Readmission Rate Analysis

**Target:** Reduce 30-day readmissions from 15% to <12%

```python
# Readmission analysis
admissions = pd.read_csv('admissions.csv')
admissions['admission_date'] = pd.to_datetime(admissions['admission_date'])
admissions['discharge_date'] = pd.to_datetime(admissions['discharge_date'])

# Identify readmissions within 30 days
admissions = admissions.sort_values(['patient_id', 'admission_date'])
admissions['next_admission'] = admissions.groupby('patient_id')['admission_date'].shift(-1)
admissions['days_to_readmit'] = (admissions['next_admission'] - admissions['discharge_date']).dt.days
admissions['readmit_30day'] = admissions['days_to_readmit'] <= 30

# Calculate rate
readmit_rate = admissions['readmit_30day'].mean() * 100
print(f"30-day readmission rate: {readmit_rate:.1f}%")

# By diagnosis
readmit_by_dx = admissions.groupby('primary_diagnosis').agg({
    'readmit_30day': ['count', 'mean']
}).round(3)
print("\nTop diagnoses by readmission rate:")
print(readmit_by_dx.sort_values(('readmit_30day', 'mean'), ascending=False).head(10))
```

---

### Scenario 5: Operating Theatre Utilization

**Target:** Increase utilization from 75% to 85%

```sql
-- Theatre utilization
SELECT 
    theatre_name,
    SUM(TIMESTAMPDIFF(MINUTE, surgery_start, surgery_end)) as utilized_mins,
    SUM(TIMESTAMPDIFF(MINUTE, session_start, session_end)) as available_mins,
    SUM(TIMESTAMPDIFF(MINUTE, surgery_start, surgery_end)) * 100.0 / 
        SUM(TIMESTAMPDIFF(MINUTE, session_start, session_end)) as utilization_pct
FROM theatre_sessions
WHERE session_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
GROUP BY theatre_name
ORDER BY utilization_pct ASC;

-- Cancelled operations analysis
SELECT 
    cancellation_reason,
    COUNT(*) as cancellations,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM surgeries WHERE cancelled = 1) as pct_of_cancellations
FROM surgeries
WHERE cancelled = 1
  AND surgery_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY cancellation_reason
ORDER BY cancellations DESC;
```

---

### Scenario 6: Outpatient Clinic Efficiency

```sql
-- Clinic running time analysis
WITH clinic_times AS (
    SELECT 
        clinic_id,
        clinic_date,
        MIN(appointment_time) as first_appt,
        MAX(actual_end_time) as last_finish,
        TIMESTAMPDIFF(MINUTE, MIN(appointment_time), MAX(actual_end_time)) as clinic_duration_mins,
        COUNT(*) as patients_seen
    FROM outpatient_appointments
    WHERE attended = 1
    GROUP BY clinic_id, clinic_date
)
SELECT 
    clinic_specialty,
    AVG(clinic_duration_mins) as avg_duration_mins,
    AVG(patients_seen) as avg_patients,
    AVG(clinic_duration_mins / patients_seen) as mins_per_patient
FROM clinic_times ct
JOIN clinics c ON ct.clinic_id = c.clinic_id
GROUP BY clinic_specialty
ORDER BY mins_per_patient DESC;
```

---

### Scenario 7: Pharmacy Prescribing Analysis

```sql
-- High-cost medications
SELECT 
    medication_name,
    COUNT(*) as prescriptions,
    SUM(cost) as total_cost,
    AVG(cost) as avg_cost_per_prescription
FROM prescriptions
WHERE prescription_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY medication_name
HAVING COUNT(*) > 100
ORDER BY total_cost DESC
LIMIT 20;

-- Generic substitution opportunities
SELECT 
    branded_name,
    generic_equivalent,
    COUNT(*) as branded_prescriptions,
    SUM(branded_cost - generic_cost) as potential_savings
FROM prescription_opportunities
WHERE generic_equivalent IS NOT NULL
GROUP BY branded_name, generic_equivalent
ORDER BY potential_savings DESC;
```

---

### Scenario 8: Patient Satisfaction Analysis

```python
# Survey response analysis
import pandas as pd
import numpy as np

surveys = pd.read_csv('patient_surveys.csv')

# Calculate Net Promoter Score (NPS)
promoters = (surveys['recommend_score'] >= 9).sum()
detractors = (surveys['recommend_score'] <= 6).sum()
nps = ((promoters - detractors) / len(surveys)) * 100

print(f"NPS Score: {nps:.1f}")

# Identify improvement areas
questions = ['cleanliness', 'staff_friendliness', 'wait_time', 'communication', 'overall']
for q in questions:
    avg_score = surveys[q].mean()
    low_scores = (surveys[q] <= 2).sum()
    print(f"{q}: Avg={avg_score:.2f}, Low scores={low_scores} ({low_scores/len(surveys)*100:.1f}%)")
```

---

### Scenario 9: Workforce Planning & Staffing

```sql
-- Nurse staffing vs patient acuity
SELECT 
    ward,
    shift_date,
    shift_type,
    nurses_on_duty,
    patients_count,
    AVG(patient_acuity_score) as avg_acuity,
    nurses_on_duty * 1.0 / patients_count as nurse_to_patient_ratio,
    CASE 
        WHEN nurses_on_duty * 1.0 / patients_count < 0.15 THEN 'Understaffed'
        WHEN nurses_on_duty * 1.0 / patients_count > 0.25 THEN 'Overstaffed'
        ELSE 'Adequate'
    END as staffing_status
FROM ward_shifts
WHERE shift_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY ward, shift_date, shift_type;
```

---

### Scenario 10: Clinical Quality Indicators

```sql
-- Quality metrics dashboard
-- 1. Mortality rate
SELECT 
    specialty,
    COUNT(*) as admissions,
    SUM(CASE WHEN died_in_hospital = 1 THEN 1 ELSE 0 END) as deaths,
    SUM(CASE WHEN died_in_hospital = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as mortality_rate_pct
FROM admissions
WHERE admission_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY specialty
ORDER BY mortality_rate_pct DESC;

-- 2. Infection rates
SELECT 
    ward,
    COUNT(DISTINCT patient_id) as patients,
    SUM(CASE WHEN hospital_acquired_infection = 1 THEN 1 ELSE 0 END) as infections,
    SUM(CASE WHEN hospital_acquired_infection = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT patient_id) as infection_rate_pct
FROM admissions
WHERE admission_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY ward
ORDER BY infection_rate_pct DESC;

-- 3. Falls incidents
SELECT 
    DATE_FORMAT(incident_date, '%Y-%m') as month,
    COUNT(*) as falls_count,
    SUM(serious_injury) as serious_injuries,
    COUNT(*) * 1000.0 / (SELECT SUM(patient_days) FROM ward_stats WHERE month = DATE_FORMAT(incident_date, '%Y-%m')) as falls_per_1000_patient_days
FROM patient_falls
WHERE incident_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY month
ORDER BY month;
```

---

### Healthcare Analytics Best Practices

**Data Privacy:**
- HIPAA compliance always
- Anonymize patient data
- Secure data storage and transmission
- Audit trails for access

**Data Quality:**
- Validate clinical codes (ICD-10, SNOMED)
- Handle missing data appropriately
- Cross-reference with multiple sources
- Regular data quality audits

**Reporting:**
- Real-time operational dashboards
- Weekly/monthly trend reports
- Executive KPI scorecards
- Clinical quality metrics

**Stakeholder Management:**
- Clinical staff buy-in essential
- Translate insights to action
- Present in clinical language
- Focus on patient outcomes

**Tools:**
- SQL for data extraction
- Python/R for analysis
- Tableau/Power BI for dashboards
- Statistical software for clinical research

---

"""
        )

        st.markdown("---")
        st.markdown("## 🛒 INDUSTRY MODULE: E-COMMERCE & RETAIL ANALYTICS")
        st.markdown(
            """**Complete e-commerce analytics scenarios from customer acquisition to retention**

### E-Commerce Analytics Overview

E-commerce data goldmine:
- Customer behavior (clicks, carts, purchases)
- Product catalog and inventory
- Marketing campaigns and attribution
- Financial transactions
- Logistics and fulfillment

**Key Business Questions:**
- How to reduce cart abandonment?
- Which products drive profitability?
- What's customer lifetime value?
- Which marketing channels work?
- How to optimize pricing?
- How to reduce churn?

---

### Scenario 1: Cart Abandonment Analysis & Optimization

**Business Problem:** 68% cart abandonment rate, losing £250K monthly

**Dataset:** 200,000 sessions over 6 months

```sql
-- Cart abandonment funnel
WITH funnel_stages AS (
    SELECT 
        session_id,
        user_id,
        device_type,
        traffic_source,
        MAX(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) as viewed,
        MAX(CASE WHEN event_type = 'product_view' THEN 1 ELSE 0 END) as viewed_product,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) as added_to_cart,
        MAX(CASE WHEN event_type = 'checkout_started' THEN 1 ELSE 0 END) as started_checkout,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) as completed_purchase
    FROM user_events
    WHERE event_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
    GROUP BY session_id, user_id, device_type, traffic_source
)
SELECT 
    device_type,
    COUNT(*) as sessions,
    SUM(viewed_product) as viewed_product,
    SUM(added_to_cart) as added_to_cart,
    SUM(started_checkout) as started_checkout,
    SUM(completed_purchase) as purchases,
    SUM(added_to_cart) * 100.0 / SUM(viewed_product) as add_to_cart_rate,
    SUM(completed_purchase) * 100.0 / SUM(added_to_cart) as cart_conversion_rate,
    (1 - SUM(completed_purchase) * 1.0 / SUM(added_to_cart)) * 100 as abandonment_rate
FROM funnel_stages
WHERE viewed_product = 1
GROUP BY device_type
ORDER BY abandonment_rate DESC;

-- Abandonment reasons analysis
SELECT 
    cart_abandon_reason,
    COUNT(*) as count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM cart_abandons) as pct
FROM cart_abandons
WHERE abandon_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
GROUP BY cart_abandon_reason
ORDER BY count DESC;
```

**Python Recovery Campaign Analysis:**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load abandoned cart data
df = pd.read_csv('abandoned_carts.csv')
df['abandon_datetime'] = pd.to_datetime(df['abandon_datetime'])

# Calculate recovery rate by email timing
recovery_analysis = df.groupby('email_hours_after_abandon').agg({
    'recovered': ['sum', 'count', 'mean']
}).reset_index()
recovery_analysis.columns = ['hours_after', 'recovered_count', 'total', 'recovery_rate']
recovery_analysis['recovery_pct'] = recovery_analysis['recovery_rate'] * 100

print("Cart Recovery by Email Timing:")
print(recovery_analysis)

# Best time to send recovery email
plt.figure(figsize=(12, 6))
plt.bar(recovery_analysis['hours_after'], recovery_analysis['recovery_pct'])
plt.xlabel('Hours After Abandonment')
plt.ylabel('Recovery Rate (%)')
plt.title('Cart Recovery Rate by Email Timing')
plt.axhline(y=recovery_analysis['recovery_pct'].mean(), color='r', linestyle='--', label='Average')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"\\nBest timing: {recovery_analysis.loc[recovery_analysis['recovery_pct'].idxmax(), 'hours_after']} hours")
print(f"Recovery rate at best time: {recovery_analysis['recovery_pct'].max():.1f}%")
```

**Key Findings:**
- Mobile abandonment 75% vs desktop 55%
- Shipping costs revealed at step 3 = 40% drop-off
- Email sent 1-2 hours after = 15% recovery rate
- Weekend abandonment 20% higher

**Recommendations:**
1. Show shipping early - Projected 8% abandonment reduction
2. Mobile checkout optimization - Simplify from 5 to 3 steps
3. Automated email sequence: 1hr, 24hr, 72hr after abandon
4. Exit-intent popup with discount code

**Expected Impact:** £300K annual revenue recovery

---

### Scenario 2: Customer Segmentation & Lifetime Value

**RFM Analysis (Recency, Frequency, Monetary)**

```sql
-- Calculate RFM scores
WITH customer_rfm AS (
    SELECT 
        customer_id,
        DATEDIFF(CURDATE(), MAX(order_date)) as recency_days,
        COUNT(*) as frequency,
        SUM(order_total) as monetary
    FROM orders
    WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) as R,
        NTILE(5) OVER (ORDER BY frequency ASC) as F,
        NTILE(5) OVER (ORDER BY monetary ASC) as M
    FROM customer_rfm
)
SELECT 
    CASE 
        WHEN R >= 4 AND F >= 4 AND M >= 4 THEN 'Champions'
        WHEN R >= 3 AND F >= 3 AND M >= 3 THEN 'Loyal Customers'
        WHEN R >= 4 AND F <= 2 THEN 'New Customers'
        WHEN R >= 3 AND F <= 2 AND M >= 3 THEN 'Promising'
        WHEN R <= 2 AND F >= 4 THEN 'At Risk'
        WHEN R <= 2 AND F >= 2 THEN 'Need Attention'
        WHEN R <= 2 AND F <= 2 THEN 'Hibernating'
        ELSE 'Other'
    END as segment,
    COUNT(*) as customer_count,
    AVG(monetary) as avg_revenue,
    AVG(frequency) as avg_orders,
    AVG(recency_days) as avg_recency_days
FROM rfm_scores
GROUP BY segment
ORDER BY avg_revenue DESC;
```

**Customer Lifetime Value (CLV) Calculation:**
```python
# CLV = (Average Order Value × Purchase Frequency × Customer Lifespan)
import pandas as pd

customers = pd.read_csv('customer_orders.csv')
customers['order_date'] = pd.to_datetime(customers['order_date'])

# Calculate per customer
clv_data = customers.groupby('customer_id').agg({
    'order_total': ['mean', 'sum'],
    'order_id': 'count',
    'order_date': ['min', 'max']
}).reset_index()

clv_data.columns = ['customer_id', 'avg_order_value', 'total_spent', 'order_count', 'first_order', 'last_order']

# Calculate metrics
clv_data['customer_lifespan_days'] = (clv_data['last_order'] - clv_data['first_order']).dt.days
clv_data['purchase_frequency'] = clv_data['order_count'] / (clv_data['customer_lifespan_days'] / 365.25)

# Simple CLV (average customer lifespan = 3 years)
avg_lifespan_years = 3
clv_data['clv'] = clv_data['avg_order_value'] * clv_data['purchase_frequency'] * avg_lifespan_years

# Segment by CLV
clv_data['clv_segment'] = pd.cut(clv_data['clv'], 
                                  bins=[0, 500, 1000, 2500, float('inf')],
                                  labels=['Low', 'Medium', 'High', 'VIP'])

print("CLV Summary:")
print(clv_data.groupby('clv_segment').agg({
    'customer_id': 'count',
    'clv': 'mean',
    'total_spent': 'sum'
}))

print(f"\\nTop 10% of customers contribute {clv_data.nlargest(int(len(clv_data)*0.1), 'total_spent')['total_spent'].sum() / clv_data['total_spent'].sum() * 100:.1f}% of revenue")
```

**Segment-Specific Strategies:**
- **Champions:** Exclusive early access, VIP program, referral incentives
- **Loyal:** Loyalty points, personalized recommendations
- **At Risk:** Win-back campaigns, special offers
- **Hibernating:** Deep discounts, reactivation emails
- **New:** Onboarding sequence, second purchase incentive

---

### Scenario 3: Product Performance & Profitability Analysis

```sql
-- Product profitability analysis
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COUNT(DISTINCT oi.order_id) as orders,
    SUM(oi.quantity) as units_sold,
    SUM(oi.quantity * oi.unit_price) as revenue,
    SUM(oi.quantity * p.cost) as cost,
    SUM(oi.quantity * (oi.unit_price - p.cost)) as profit,
    (SUM(oi.quantity * (oi.unit_price - p.cost)) / SUM(oi.quantity * oi.unit_price)) * 100 as profit_margin_pct,
    AVG(pr.rating) as avg_rating,
    COUNT(pr.review_id) as review_count
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN product_reviews pr ON p.product_id = pr.product_id
WHERE oi.order_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY p.product_id, p.product_name, p.category
HAVING SUM(oi.quantity) > 10
ORDER BY profit DESC;

-- Product recommendations (frequently bought together)
SELECT 
    p1.product_name as product_1,
    p2.product_name as product_2,
    COUNT(*) as times_bought_together,
    AVG(o.order_total) as avg_order_value
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
JOIN products p1 ON oi1.product_id = p1.product_id
JOIN products p2 ON oi2.product_id = p2.product_id
JOIN orders o ON oi1.order_id = o.order_id
WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY p1.product_name, p2.product_name
HAVING COUNT(*) > 20
ORDER BY times_bought_together DESC
LIMIT 20;
```

---

### Scenario 4: Marketing Channel Attribution & ROI

```sql
-- Multi-touch attribution
WITH customer_touchpoints AS (
    SELECT 
        customer_id,
        order_id,
        order_date,
        order_total,
        first_touch_channel,
        last_touch_channel,
        assisted_channels
    FROM orders o
    JOIN customer_journeys cj ON o.customer_id = cj.customer_id 
        AND o.order_date BETWEEN cj.journey_start AND cj.journey_end
)
-- First touch attribution
SELECT 
    first_touch_channel as channel,
    'First Touch' as attribution_model,
    COUNT(*) as conversions,
    SUM(order_total) as revenue
FROM customer_touchpoints
GROUP BY first_touch_channel

UNION ALL

-- Last touch attribution
SELECT 
    last_touch_channel,
    'Last Touch',
    COUNT(*),
    SUM(order_total)
FROM customer_touchpoints
GROUP BY last_touch_channel

ORDER BY attribution_model, revenue DESC;

-- Marketing ROI by channel
SELECT 
    channel,
    SUM(spend) as total_spend,
    COUNT(DISTINCT customer_id) as customers_acquired,
    SUM(revenue) as total_revenue,
    SUM(spend) / COUNT(DISTINCT customer_id) as cac,
    (SUM(revenue) - SUM(spend)) / SUM(spend) * 100 as roi_pct
FROM marketing_performance
WHERE campaign_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY channel
ORDER BY roi_pct DESC;
```

---

### Scenario 5: Inventory Optimization

```python
# ABC Analysis for inventory classification
import pandas as pd

inventory = pd.read_csv('inventory.csv')

# Calculate cumulative values
inventory = inventory.sort_values('annual_sales_value', ascending=False)
inventory['cumulative_sales'] = inventory['annual_sales_value'].cumsum()
inventory['cumulative_pct'] = inventory['cumulative_sales'] / inventory['annual_sales_value'].sum() * 100

# Classify products
inventory['abc_category'] = pd.cut(inventory['cumulative_pct'],
                                     bins=[0, 80, 95, 100],
                                     labels=['A', 'B', 'C'])

# Analysis by category
abc_summary = inventory.groupby('abc_category').agg({
    'product_id': 'count',
    'annual_sales_value': 'sum',
    'current_stock_value': 'sum',
    'turnover_ratio': 'mean'
})

print("ABC Analysis:")
print(abc_summary)
print("\\nRecommendations:")
print("A items (80% of value): Tight control, daily monitoring, optimized reorder points")
print("B items (15% of value): Moderate control, weekly monitoring")
print("C items (5% of value): Loose control, periodic review")

# Safety stock calculation
inventory['safety_stock'] = inventory['avg_daily_demand'] * inventory['lead_time_days'] * 1.5
inventory['reorder_point'] = inventory['safety_stock'] + (inventory['avg_daily_demand'] * inventory['lead_time_days'])

print("\\nReorder alerts:")
print(inventory[inventory['current_stock'] < inventory['reorder_point']][['product_name', 'current_stock', 'reorder_point']])
```

---

### Scenario 6: Pricing Optimization & Elasticity

```sql
-- Price elasticity analysis
WITH price_changes AS (
    SELECT 
        product_id,
        DATE_FORMAT(price_change_date, '%Y-%m') as month,
        old_price,
        new_price,
        (new_price - old_price) / old_price * 100 as price_change_pct
    FROM product_prices
),
sales_impact AS (
    SELECT 
        oi.product_id,
        DATE_FORMAT(o.order_date, '%Y-%m') as month,
        SUM(oi.quantity) as units_sold,
        AVG(oi.unit_price) as avg_selling_price
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY oi.product_id, month
)
SELECT 
    pc.product_id,
    pc.month,
    pc.price_change_pct,
    si_before.units_sold as units_before,
    si_after.units_sold as units_after,
    (si_after.units_sold - si_before.units_sold) * 100.0 / si_before.units_sold as volume_change_pct,
    ((si_after.units_sold - si_before.units_sold) * 100.0 / si_before.units_sold) / pc.price_change_pct as elasticity
FROM price_changes pc
JOIN sales_impact si_before ON pc.product_id = si_before.product_id 
    AND si_before.month = DATE_FORMAT(DATE_SUB(STR_TO_DATE(pc.month, '%Y-%m'), INTERVAL 1 MONTH), '%Y-%m')
JOIN sales_impact si_after ON pc.product_id = si_after.product_id 
    AND si_after.month = pc.month;
```

---

### Scenario 7: Customer Churn Prediction

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load customer data
customers = pd.read_csv('customer_features.csv')

# Feature engineering
customers['days_since_last_order'] = (pd.Timestamp.now() - pd.to_datetime(customers['last_order_date'])).dt.days
customers['avg_days_between_orders'] = customers['total_order_days'] / (customers['order_count'] - 1)
customers['order_frequency_trend'] = customers['last_90_orders'] / customers['previous_90_orders']
customers['churned'] = (customers['days_since_last_order'] > customers['avg_days_between_orders'] * 2).astype(int)

# Features for model
features = ['days_since_last_order', 'order_count', 'avg_order_value', 
            'total_spent', 'avg_days_between_orders', 'order_frequency_trend',
            'customer_age_days', 'email_open_rate', 'support_tickets']

X = customers[features]
y = customers['churned']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Predict churn probability
customers['churn_probability'] = model.predict_proba(X)[:, 1]

# High-risk customers
at_risk = customers[customers['churn_probability'] > 0.5].sort_values('churn_probability', ascending=False)
print(f"Customers at risk: {len(at_risk)}")
print(f"Potential revenue at risk: £{at_risk['avg_order_value'].sum() * 3:,.0f}")  # 3 orders/year avg

# Feature importance
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\\nTop churn indicators:")
print(importance)
```

---

### Scenario 8: A/B Testing Framework

```python
# Statistical A/B test for checkout flow
from scipy.stats import chi2_contingency, ttest_ind

# Load test data
ab_test = pd.read_csv('checkout_ab_test.csv')

# Conversion rates by variant
conversion_summary = ab_test.groupby('variant').agg({
    'user_id': 'count',
    'converted': ['sum', 'mean']
}).reset_index()
conversion_summary.columns = ['variant', 'users', 'conversions', 'conversion_rate']

print("A/B Test Results:")
print(conversion_summary)

# Statistical significance test
contingency = pd.crosstab(ab_test['variant'], ab_test['converted'])
chi2, p_value, dof, expected = chi2_contingency(contingency)

print(f"\\nChi-square test:")
print(f"p-value: {p_value:.4f}")
if p_value < 0.05:
    print("✅ SIGNIFICANT: Variant B performs differently than control")
    lift = (conversion_summary.loc[1, 'conversion_rate'] - conversion_summary.loc[0, 'conversion_rate']) / conversion_summary.loc[0, 'conversion_rate'] * 100
    print(f"Lift: {lift:.1f}%")
else:
    print("❌ NOT SIGNIFICANT: No clear winner")

# Revenue impact
revenue_test = ab_test[ab_test['converted'] == 1].groupby('variant')['order_value'].agg(['mean', 'sum', 'count'])
print("\\nRevenue Analysis:")
print(revenue_test)
```

---

### Scenario 9: Seasonal Demand Forecasting

```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load daily sales
daily_sales = pd.read_csv('daily_sales.csv', parse_dates=['date'], index_col='date')

# Decompose time series
decomposition = seasonal_decompose(daily_sales['revenue'], model='multiplicative', period=7)

fig, axes = plt.subplots(4, 1, figsize=(15, 10))
decomposition.observed.plot(ax=axes[0], title='Observed')
decomposition.trend.plot(ax=axes[1], title='Trend')
decomposition.seasonal.plot(ax=axes[2], title='Seasonal')
decomposition.resid.plot(ax=axes[3], title='Residual')
plt.tight_layout()
plt.show()

# Forecast next 30 days
model = ExponentialSmoothing(daily_sales['revenue'], seasonal_periods=7, trend='add', seasonal='add')
fitted_model = model.fit()
forecast = fitted_model.forecast(steps=30)

print("30-day forecast:")
print(forecast)
print(f"\\nExpected total revenue: £{forecast.sum():,.0f}")
```

---

### Scenario 10: Returns & Refunds Analysis

```sql
-- Returns analysis
SELECT 
    p.category,
    COUNT(r.return_id) as return_count,
    COUNT(r.return_id) * 100.0 / (SELECT COUNT(*) FROM order_items oi2 
                                    JOIN products p2 ON oi2.product_id = p2.product_id
                                    WHERE p2.category = p.category) as return_rate_pct,
    AVG(DATEDIFF(r.return_date, o.order_date)) as avg_days_to_return,
    SUM(r.refund_amount) as total_refunds
FROM returns r
JOIN orders o ON r.order_id = o.order_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE r.return_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY p.category
ORDER BY return_rate_pct DESC;

-- Top return reasons
SELECT 
    return_reason,
    COUNT(*) as count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM returns) as pct,
    AVG(refund_amount) as avg_refund
FROM returns
WHERE return_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY return_reason
ORDER BY count DESC;
```

---

### E-Commerce Best Practices

**Data Collection:**
- Implement event tracking (Google Analytics, Segment)
- Track full customer journey
- Capture device, source, timestamps
- A/B test everything

**Key Metrics:**
- Conversion rate (overall and by funnel stage)
- Average order value (AOV)
- Customer acquisition cost (CAC)
- Customer lifetime value (CLV)
- Cart abandonment rate
- Return rate

**Optimization Framework:**
1. Identify bottleneck (data analysis)
2. Form hypothesis (why is it happening?)
3. Design experiment (A/B test)
4. Measure impact (statistical significance)
5. Implement winner
6. Repeat

**Tools:**
- SQL for data extraction
- Python for analysis and ML
- Tableau/Looker for dashboards
- Google Analytics for web data
- Segment for event tracking

---

"""
        )

        st.markdown("---")
        st.markdown("## 💻 INDUSTRY MODULE: SAAS & TECH ANALYTICS")
        st.markdown(
            """**SaaS metrics from acquisition to retention and growth**

### Key SaaS Metrics

**MRR (Monthly Recurring Revenue):**
```sql
WITH subscription_mrr AS (
    SELECT 
        DATE_TRUNC('month', billing_date) as month,
        customer_id,
        CASE 
            WHEN billing_frequency = 'monthly' THEN amount
            WHEN billing_frequency = 'annual' THEN amount / 12
        END as mrr
    FROM subscriptions WHERE status = 'active'
)
SELECT month, SUM(mrr) as total_mrr, COUNT(DISTINCT customer_id) as customers
FROM subscription_mrr GROUP BY month ORDER BY month;
```

**Cohort Retention:**
```sql
SELECT 
    DATE_TRUNC('month', signup_date) as cohort,
    DATEDIFF('month', signup_date, activity_date) as months,
    COUNT(DISTINCT user_id) * 100.0 / COUNT(DISTINCT 
        CASE WHEN DATEDIFF('month', signup_date, activity_date) = 0 
        THEN user_id END) as retention_pct
FROM user_activity
GROUP BY cohort, months;
```

**Churn Prediction:**
```python
from sklearn.ensemble import GradientBoostingClassifier

features = ['days_since_login', 'usage_trend', 'support_tickets']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
model = GradientBoostingClassifier(n_estimators=100)
model.fit(X_train, y_train)
users['churn_probability'] = model.predict_proba(X)[:, 1]
at_risk = users[users['churn_probability'] > 0.5]
```

**Product Qualified Leads:**
```sql
SELECT user_id,
    CASE 
        WHEN days_active >= 5 AND features_used >= 3 THEN 'Hot PQL'
        WHEN days_active >= 3 AND features_used >= 2 THEN 'Warm PQL'
        ELSE 'Cold PQL'
    END as pql_status
FROM user_activity WHERE plan_type = 'free';
```

**CAC & LTV:**
```sql
SELECT channel,
    SUM(spend) / COUNT(DISTINCT user_id) as cac,
    AVG(lifetime_value) as avg_ltv,
    AVG(lifetime_value) / (SUM(spend) / COUNT(DISTINCT user_id)) as ltv_cac_ratio
FROM acquisitions GROUP BY channel;
```

---

"""
        )

        st.markdown("---")
        st.markdown("## 💰 INDUSTRY MODULE: FINANCIAL SERVICES ANALYTICS")
        st.markdown(
            """**Banking, credit, fraud, and risk analytics**

### Financial Analytics Overview

Financial services data challenges:
- High-stakes decisions (loans, investments)
- Fraud detection and prevention
- Regulatory compliance (Basel III, GDPR)
- Risk management and stress testing
- Customer lifetime value optimization

---

### Scenario 1: Credit Risk Modeling

**Business Problem:** Reduce default rate from 4.2% to <3% while maintaining approval rate

```sql
-- Loan performance analysis
SELECT 
    loan_grade,
    COUNT(*) as total_loans,
    SUM(loan_amount) as total_amount,
    SUM(CASE WHEN status = 'default' THEN 1 ELSE 0 END) as defaults,
    SUM(CASE WHEN status = 'default' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as default_rate,
    AVG(CASE WHEN status = 'default' THEN DATEDIFF(default_date, issue_date) ELSE NULL END) as avg_days_to_default
FROM loans
GROUP BY loan_grade
ORDER BY default_rate DESC;

-- Customer risk factors
SELECT 
    CASE WHEN credit_score < 600 THEN '<600'
         WHEN credit_score < 650 THEN '600-649'
         WHEN credit_score < 700 THEN '650-699'
         WHEN credit_score < 750 THEN '700-749'
         ELSE '750+' END as credit_band,
    CASE WHEN dti_ratio < 20 THEN '<20%'
         WHEN dti_ratio < 30 THEN '20-30%'
         WHEN dti_ratio < 40 THEN '30-40%'
         ELSE '>40%' END as dti_band,
    COUNT(*) as loans,
    SUM(CASE WHEN status = 'default' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as default_rate
FROM loans
GROUP BY credit_band, dti_band
ORDER BY default_rate DESC;
```

**Python Credit Scoring Model:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
import pandas as pd

# Load loan data
loans = pd.read_csv('loan_applications.csv')

# Feature engineering
loans['credit_utilization'] = loans['credit_balance'] / loans['credit_limit']
loans['income_to_loan_ratio'] = loans['annual_income'] / loans['loan_amount']
loans['employment_years'] = loans['employment_length'].str.extract('(\d+)').astype(float)

# Target variable
loans['default'] = (loans['loan_status'] == 'Charged Off').astype(int)

# Features for model
features = [
    'credit_score', 'annual_income', 'dti_ratio', 'credit_utilization',
    'employment_years', 'loan_amount', 'income_to_loan_ratio',
    'delinq_2yrs', 'inq_last_6mths', 'open_acc', 'pub_rec'
]

X = loans[features]
y = loans['default']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)

# Train model
model = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=100)
model.fit(X_train, y_train)

# Predictions
y_pred_proba = model.predict_proba(X_test)[:, 1]

print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")

# Feature importance
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nTop Risk Factors:")
print(importance)

# Risk-based pricing
loans['default_probability'] = model.predict_proba(X)[:, 1]
loans['risk_tier'] = pd.cut(loans['default_probability'], 
                             bins=[0, 0.02, 0.05, 0.10, 1],
                             labels=['Low', 'Medium', 'High', 'Very High'])

print("\nRisk Distribution:")
print(loans.groupby('risk_tier').agg({
    'loan_amount': 'sum',
    'default_probability': 'mean',
    'loan_id': 'count'
}))
```

**Expected Impact:** 1.5% reduction in default rate = £2.5M annual savings

---

### Scenario 2: Fraud Detection System

**Real-time transaction monitoring:**

```sql
-- Suspicious transaction patterns
WITH transaction_stats AS (
    SELECT 
        customer_id,
        transaction_date,
        transaction_amount,
        merchant_category,
        AVG(transaction_amount) OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 29 PRECEDING AND 1 PRECEDING
        ) as avg_30day,
        STDDEV(transaction_amount) OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 29 PRECEDING AND 1 PRECEDING
        ) as stddev_30day
    FROM transactions
)
SELECT 
    customer_id,
    transaction_date,
    transaction_amount,
    avg_30day,
    (transaction_amount - avg_30day) / NULLIF(stddev_30day, 0) as z_score,
    CASE 
        WHEN ABS((transaction_amount - avg_30day) / NULLIF(stddev_30day, 0)) > 3 THEN 'High Risk'
        WHEN ABS((transaction_amount - avg_30day) / NULLIF(stddev_30day, 0)) > 2 THEN 'Medium Risk'
        ELSE 'Normal'
    END as fraud_risk
FROM transaction_stats
WHERE ABS((transaction_amount - avg_30day) / NULLIF(stddev_30day, 0)) > 2
ORDER BY z_score DESC;

-- Geographic anomalies
WITH customer_locations AS (
    SELECT 
        customer_id,
        transaction_timestamp,
        country_code,
        LAG(country_code) OVER (PARTITION BY customer_id ORDER BY transaction_timestamp) as prev_country,
        LAG(transaction_timestamp) OVER (PARTITION BY customer_id ORDER BY transaction_timestamp) as prev_timestamp
    FROM transactions
)
SELECT 
    customer_id,
    transaction_timestamp,
    country_code,
    prev_country,
    TIMESTAMPDIFF(MINUTE, prev_timestamp, transaction_timestamp) as minutes_between,
    'Impossible Travel' as alert_type
FROM customer_locations
WHERE country_code != prev_country
  AND TIMESTAMPDIFF(MINUTE, prev_timestamp, transaction_timestamp) < 120;
```

**Machine Learning Fraud Model:**
```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load transaction data
transactions = pd.read_csv('transactions.csv')

# Feature engineering for fraud detection
transactions['hour'] = pd.to_datetime(transactions['timestamp']).dt.hour
transactions['day_of_week'] = pd.to_datetime(transactions['timestamp']).dt.dayofweek
transactions['amount_log'] = np.log1p(transactions['amount'])

# Customer aggregates
customer_agg = transactions.groupby('customer_id').agg({
    'amount': ['mean', 'std', 'max'],
    'transaction_id': 'count'
}).reset_index()
customer_agg.columns = ['customer_id', 'avg_amount', 'std_amount', 'max_amount', 'txn_count']

transactions = transactions.merge(customer_agg, on='customer_id')

# Deviation features
transactions['amount_vs_avg'] = transactions['amount'] / transactions['avg_amount']
transactions['amount_vs_max'] = transactions['amount'] / transactions['max_amount']

# Anomaly detection with Isolation Forest
features = ['amount_log', 'hour', 'day_of_week', 'amount_vs_avg', 'amount_vs_max']
X = transactions[features]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train anomaly detector
iso_forest = IsolationForest(contamination=0.01, random_state=42)
transactions['anomaly_score'] = iso_forest.fit_predict(X_scaled)
transactions['fraud_probability'] = iso_forest.score_samples(X_scaled)

# Flag high-risk transactions
high_risk = transactions[transactions['anomaly_score'] == -1].sort_values('fraud_probability')
print(f"Flagged {len(high_risk)} suspicious transactions ({len(high_risk)/len(transactions)*100:.2f}%)")

# Validation against known fraud
if 'is_fraud' in transactions.columns:
    from sklearn.metrics import precision_score, recall_score, f1_score
    print(f"Precision: {precision_score(transactions['is_fraud'], transactions['anomaly_score']==-1):.3f}")
    print(f"Recall: {recall_score(transactions['is_fraud'], transactions['anomaly_score']==-1):.3f}")
```

---

### Scenario 3: Customer Segmentation & CLV

**Banking customer analytics:**

```sql
-- Customer value segmentation
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.customer_since,
        DATEDIFF(CURRENT_DATE, c.customer_since) / 365.0 as tenure_years,
        COUNT(DISTINCT a.account_id) as num_accounts,
        SUM(a.balance) as total_balance,
        COUNT(DISTINCT p.product_id) as num_products,
        SUM(CASE WHEN t.transaction_date >= CURRENT_DATE - INTERVAL '90 days' THEN 1 ELSE 0 END) as transactions_90d,
        SUM(CASE WHEN t.transaction_type = 'fee' THEN t.amount ELSE 0 END) as total_fees_paid
    FROM customers c
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN products p ON c.customer_id = p.customer_id
    LEFT JOIN transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id, c.customer_since
)
SELECT 
    customer_id,
    tenure_years,
    num_accounts,
    total_balance,
    num_products,
    transactions_90d,
    total_fees_paid,
    CASE 
        WHEN total_balance >= 100000 AND num_products >= 3 THEN 'Premium'
        WHEN total_balance >= 50000 OR num_products >= 2 THEN 'High Value'
        WHEN transactions_90d >= 10 THEN 'Active'
        WHEN tenure_years >= 5 THEN 'Loyal'
        ELSE 'Standard'
    END as segment
FROM customer_metrics
ORDER BY total_balance DESC;
```

---

### Scenario 4: Regulatory Compliance Reporting

**Basel III Capital Requirements:**

```sql
-- Risk-Weighted Assets (RWA) calculation
SELECT 
    asset_class,
    credit_rating,
    SUM(exposure_amount) as total_exposure,
    CASE 
        WHEN asset_class = 'sovereign' AND credit_rating = 'AAA' THEN 0.0
        WHEN asset_class = 'corporate' AND credit_rating >= 'AA' THEN 0.20
        WHEN asset_class = 'corporate' AND credit_rating >= 'A' THEN 0.50
        WHEN asset_class = 'corporate' AND credit_rating >= 'BBB' THEN 0.75
        WHEN asset_class = 'corporate' THEN 1.00
        WHEN asset_class = 'retail_mortgage' THEN 0.35
        WHEN asset_class = 'retail_other' THEN 0.75
        ELSE 1.00
    END as risk_weight,
    SUM(exposure_amount) * risk_weight as rwa
FROM credit_exposures
GROUP BY asset_class, credit_rating
ORDER BY rwa DESC;

-- Capital Adequacy Ratio
SELECT 
    (SELECT SUM(tier1_capital + tier2_capital) FROM capital_base) as total_capital,
    SUM(rwa) as total_rwa,
    (SELECT SUM(tier1_capital + tier2_capital) FROM capital_base) / SUM(rwa) * 100 as capital_ratio
FROM (
    SELECT SUM(exposure_amount * risk_weight) as rwa
    FROM credit_exposures
    JOIN risk_weights USING (asset_class, credit_rating)
) rwa_calc;
```

**Anti-Money Laundering (AML) Monitoring:**

```sql
-- Large cash transactions
SELECT 
    customer_id,
    transaction_date,
    transaction_amount,
    transaction_type,
    'Large Cash' as alert_reason
FROM transactions
WHERE transaction_type = 'cash'
  AND transaction_amount >= 10000
  AND transaction_date >= CURRENT_DATE - INTERVAL '30 days'

UNION ALL

-- Structuring (smurfing) pattern
SELECT 
    customer_id,
    DATE(transaction_date) as transaction_date,
    SUM(transaction_amount) as total_amount,
    'Potential Structuring' as alert_reason
FROM transactions
WHERE transaction_type = 'cash'
  AND transaction_amount BETWEEN 9000 AND 9999
  AND transaction_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY customer_id, DATE(transaction_date)
HAVING COUNT(*) >= 3;
```

---

### Scenario 5: Investment Portfolio Analytics

```python
import pandas as pd
import numpy as np

# Portfolio risk/return analysis
def calculate_portfolio_metrics(returns_df, weights):
    """
    Calculate portfolio risk and return metrics
    """
    # Expected returns
    expected_returns = returns_df.mean() * 252  # Annualized
    
    # Covariance matrix
    cov_matrix = returns_df.cov() * 252  # Annualized
    
    # Portfolio return
    portfolio_return = np.dot(weights, expected_returns)
    
    # Portfolio risk (volatility)
    portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Sharpe ratio (assuming risk-free rate = 2%)
    sharpe_ratio = (portfolio_return - 0.02) / portfolio_risk
    
    return {
        'return': portfolio_return,
        'risk': portfolio_risk,
        'sharpe': sharpe_ratio
    }

# Load returns data
returns = pd.read_csv('daily_returns.csv', index_col='date', parse_dates=True)

# Example portfolio weights
weights = np.array([0.3, 0.3, 0.2, 0.15, 0.05])  # Must sum to 1

metrics = calculate_portfolio_metrics(returns, weights)
print(f"Expected Return: {metrics['return']*100:.2f}%")
print(f"Expected Risk: {metrics['risk']*100:.2f}%")
print(f"Sharpe Ratio: {metrics['sharpe']:.2f}")

# Value at Risk (VaR) calculation
portfolio_returns = returns.dot(weights)
var_95 = np.percentile(portfolio_returns, 5)
var_99 = np.percentile(portfolio_returns, 1)
print(f"\n95% VaR: {var_95*100:.2f}%")
print(f"99% VaR: {var_99*100:.2f}%")
```

---

### Scenario 6: Churn Prediction (Banking)

```python
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd

# Load customer data
customers = pd.read_csv('bank_customers.csv')

# Feature engineering
customers['products_per_year'] = customers['num_products'] / (customers['tenure_months'] / 12)
customers['balance_per_product'] = customers['balance'] / customers['num_products']
customers['transactions_per_month'] = customers['transactions_12m'] / 12
customers['avg_transaction'] = customers['transaction_volume_12m'] / customers['transactions_12m']

# Define churn
customers['churned'] = (customers['status'] == 'closed').astype(int)

# Features
features = [
    'age', 'tenure_months', 'balance', 'num_products',
    'products_per_year', 'balance_per_product',
    'transactions_per_month', 'avg_transaction',
    'credit_score', 'has_credit_card', 'is_active_member'
]

X = customers[features]
y = customers['churned']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)
model = GradientBoostingClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Predict churn risk
customers['churn_probability'] = model.predict_proba(X)[:, 1]

# High-risk customers
at_risk = customers[customers['churn_probability'] > 0.5].sort_values('balance', ascending=False)
print(f"{len(at_risk)} customers at high risk")
print(f"Total balance at risk: ${at_risk['balance'].sum():,.0f}")

# Retention strategies by segment
print("\nRetention Recommendations:")
for segment in ['Premium', 'High Value', 'Active', 'Standard']:
    segment_risk = at_risk[at_risk['segment'] == segment]
    if len(segment_risk) > 0:
        print(f"{segment}: {len(segment_risk)} customers, avg balance ${segment_risk['balance'].mean():,.0f}")
```

---

### Scenario 7: Loan Default Prediction Timeline

```sql
-- Early warning indicators by months before default
WITH default_timeline AS (
    SELECT 
        l.loan_id,
        l.default_date,
        t.transaction_date,
        DATEDIFF(l.default_date, t.transaction_date) / 30 as months_before_default,
        t.transaction_type,
        t.amount
    FROM loans l
    JOIN transactions t ON l.customer_id = t.customer_id
    WHERE l.status = 'default'
      AND t.transaction_date < l.default_date
      AND t.transaction_date >= l.default_date - INTERVAL '12 months'
)
SELECT 
    FLOOR(months_before_default) as months_out,
    COUNT(DISTINCT loan_id) as loans,
    SUM(CASE WHEN transaction_type = 'missed_payment' THEN 1 ELSE 0 END) as missed_payments,
    SUM(CASE WHEN transaction_type = 'late_fee' THEN 1 ELSE 0 END) as late_fees,
    AVG(CASE WHEN transaction_type = 'payment' THEN amount END) as avg_payment_amount
FROM default_timeline
GROUP BY FLOOR(months_before_default)
ORDER BY months_out DESC;
```

---

### Scenario 8: Branch Performance Analysis

```sql
-- Branch profitability and efficiency
SELECT 
    b.branch_id,
    b.branch_name,
    b.region,
    COUNT(DISTINCT c.customer_id) as customers,
    COUNT(DISTINCT a.account_id) as accounts,
    SUM(a.balance) as total_deposits,
    SUM(l.loan_amount) as total_loans,
    SUM(t.fee_amount) as fee_revenue,
    (SUM(t.fee_revenue) + SUM(l.interest_income)) as total_revenue,
    b.operating_cost,
    (SUM(t.fee_revenue) + SUM(l.interest_income) - b.operating_cost) as net_profit,
    (SUM(t.fee_revenue) + SUM(l.interest_income) - b.operating_cost) / b.operating_cost * 100 as roi_pct
FROM branches b
LEFT JOIN customers c ON b.branch_id = c.home_branch_id
LEFT JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN loans l ON c.customer_id = l.customer_id
LEFT JOIN transactions t ON c.customer_id = t.customer_id
WHERE t.transaction_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY b.branch_id, b.branch_name, b.region, b.operating_cost
ORDER BY net_profit DESC;
```

---

### Scenario 9: Credit Card Analytics

```sql
-- Credit card usage patterns and profitability
SELECT 
    card_type,
    COUNT(DISTINCT customer_id) as cardholders,
    AVG(credit_limit) as avg_limit,
    AVG(balance) as avg_balance,
    AVG(balance / NULLIF(credit_limit, 0)) as avg_utilization,
    SUM(CASE WHEN days_past_due > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as delinquency_rate,
    SUM(annual_fee) as total_annual_fees,
    SUM(interest_charged) as total_interest,
    SUM(interchange_revenue) as total_interchange,
    (SUM(annual_fee) + SUM(interest_charged) + SUM(interchange_revenue)) as total_revenue
FROM credit_cards
WHERE status = 'active'
GROUP BY card_type
ORDER BY total_revenue DESC;
```

---

### Scenario 10: Market Risk & Stress Testing

```python
# Monte Carlo simulation for portfolio stress testing
def monte_carlo_var(returns, portfolio_value, num_simulations=10000):
    """
    Calculate Value at Risk using Monte Carlo simulation
    """
    mean_return = returns.mean()
    std_return = returns.std()
    
    # Generate random scenarios
    simulated_returns = np.random.normal(mean_return, std_return, num_simulations)
    simulated_values = portfolio_value * (1 + simulated_returns)
    
    # Calculate losses
    losses = portfolio_value - simulated_values
    
    # VaR at different confidence levels
    var_95 = np.percentile(losses, 95)
    var_99 = np.percentile(losses, 99)
    
    # Expected Shortfall (CVaR)
    cvar_95 = losses[losses >= var_95].mean()
    
    return {
        'VaR_95': var_95,
        'VaR_99': var_99,
        'CVaR_95': cvar_95
    }

# Example usage
portfolio_value = 10_000_000
daily_returns = pd.read_csv('portfolio_returns.csv')['return']

risk_metrics = monte_carlo_var(daily_returns, portfolio_value)
print(f"95% VaR: ${risk_metrics['VaR_95']:,.0f}")
print(f"99% VaR: ${risk_metrics['VaR_99']:,.0f}")
print(f"95% CVaR: ${risk_metrics['CVaR_95']:,.0f}")
```

---

### Financial Analytics Best Practices

**Data Governance:**
- Strict access controls
- Audit trails for all queries
- Data anonymization for non-production
- Encryption at rest and in transit

**Regulatory Compliance:**
- Basel III capital requirements
- GDPR for EU customers
- PCI DSS for card data
- SOX for public companies
- AML/KYC regulations

**Risk Management:**
- Daily risk monitoring
- Stress testing portfolios
- Scenario analysis
- Early warning systems

**Key Metrics:**
- Default rates by segment
- Net Interest Margin (NIM)
- Return on Assets (ROA)
- Cost-to-Income Ratio
- Loan-to-Deposit Ratio
- Non-Performing Loan (NPL) Ratio

---

"""
        )

        st.markdown("---")
        st.markdown("## 🎯 COMPLETE CAPSTONE PROJECT EXAMPLES")
        st.markdown(
            """**Two portfolio-ready capstone projects with full code and documentation**

---

## CAPSTONE PROJECT 1: Healthcare Patient Journey Analytics

### Executive Summary

**Business Context:** Regional hospital network seeks to optimize patient experience and reduce readmissions

**Objective:** Analyze 50,000 patient journeys to identify bottlenecks and improve outcomes

**Impact:** 15% reduction in readmissions, £1.2M annual savings

### Data Sources

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Generate realistic sample data
np.random.seed(42)

# Patient demographics
patients = pd.DataFrame({
    'patient_id': range(1, 50001),
    'age': np.random.randint(18, 95, 50000),
    'gender': np.random.choice(['M', 'F'], 50000),
    'insurance_type': np.random.choice(['Private', 'Medicare', 'Medicaid', 'Uninsured'], 50000, p=[0.4, 0.3, 0.2, 0.1]),
    'chronic_conditions': np.random.poisson(1.2, 50000)
})

# Hospital admissions
admissions = pd.DataFrame({
    'admission_id': range(1, 75001),
    'patient_id': np.random.choice(range(1, 50001), 75000),
    'admission_date': pd.date_range('2023-01-01', periods=75000, freq='7min'),
    'discharge_date': None,
    'admission_type': np.random.choice(['Emergency', 'Elective', 'Urgent'], 75000, p=[0.5, 0.3, 0.2]),
    'primary_diagnosis': np.random.choice(['Cardiac', 'Respiratory', 'Orthopedic', 'Neurological', 'Other'], 75000),
    'los_days': np.random.gamma(2, 2, 75000).astype(int) + 1
})

# Calculate discharge dates
admissions['discharge_date'] = admissions.apply(
    lambda x: x['admission_date'] + timedelta(days=int(x['los_days'])), axis=1
)

# Readmissions (15% of patients)
readmissions = admissions.sample(int(len(admissions) * 0.15)).copy()
readmissions['readmitted_within_30'] = 1
admissions = admissions.merge(
    readmissions[['admission_id', 'readmitted_within_30']], 
    on='admission_id', 
    how='left'
)
admissions['readmitted_within_30'].fillna(0, inplace=True)

print("Data loaded successfully!")
print(f"Patients: {len(patients):,}")
print(f"Admissions: {len(admissions):,}")
```

### Analysis Part 1: Readmission Risk Factors

```python
# Merge datasets
df = admissions.merge(patients, on='patient_id')

# Readmission rate overall
readmit_rate = df['readmitted_within_30'].mean() * 100
print(f"Overall 30-day readmission rate: {readmit_rate:.1f}%")

# By admission type
print("\nReadmission Rate by Admission Type:")
print(df.groupby('admission_type')['readmitted_within_30'].agg(['count', 'mean']))

# By diagnosis
print("\nReadmission Rate by Primary Diagnosis:")
diagnosis_readmit = df.groupby('primary_diagnosis').agg({
    'readmitted_within_30': ['count', 'mean'],
    'los_days': 'mean'
}).round(3)
diagnosis_readmit.columns = ['admissions', 'readmit_rate', 'avg_los']
print(diagnosis_readmit.sort_values('readmit_rate', ascending=False))

# Age analysis
df['age_group'] = pd.cut(df['age'], bins=[0, 40, 60, 75, 100], labels=['<40', '40-60', '60-75', '75+'])
age_analysis = df.groupby('age_group')['readmitted_within_30'].agg(['count', 'mean'])
print("\nReadmission by Age Group:")
print(age_analysis)

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Readmission by diagnosis
diagnosis_readmit['readmit_rate'].plot(kind='bar', ax=axes[0, 0], color='coral')
axes[0, 0].set_title('30-Day Readmission Rate by Diagnosis')
axes[0, 0].set_ylabel('Readmission Rate')
axes[0, 0].set_xlabel('Diagnosis')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Length of stay distribution
df[df['readmitted_within_30']==0]['los_days'].hist(bins=30, ax=axes[0, 1], alpha=0.7, label='Not Readmitted')
df[df['readmitted_within_30']==1]['los_days'].hist(bins=30, ax=axes[0, 1], alpha=0.7, label='Readmitted')
axes[0, 1].set_title('Length of Stay: Readmitted vs Not')
axes[0, 1].set_xlabel('Days')
axes[0, 1].legend()

# 3. Readmission by age
age_analysis['mean'].plot(kind='bar', ax=axes[1, 0], color='steelblue')
axes[1, 0].set_title('Readmission Rate by Age Group')
axes[1, 0].set_ylabel('Rate')
axes[1, 0].tick_params(axis='x', rotation=0)

# 4. Monthly trend
df['month'] = df['admission_date'].dt.to_period('M')
monthly = df.groupby('month')['readmitted_within_30'].mean() * 100
monthly.plot(ax=axes[1, 1], marker='o')
axes[1, 1].set_title('Monthly Readmission Rate Trend')
axes[1, 1].set_ylabel('Rate (%)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('capstone1_readmission_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Analysis Part 2: Predictive Modeling

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# Feature engineering
df['is_emergency'] = (df['admission_type'] == 'Emergency').astype(int)
df['is_cardiac'] = (df['primary_diagnosis'] == 'Cardiac').astype(int)
df['age_over_65'] = (df['age'] > 65).astype(int)
df['has_chronic'] = (df['chronic_conditions'] > 0).astype(int)
df['long_stay'] = (df['los_days'] > 7).astype(int)

# Features for model
features = [
    'age', 'chronic_conditions', 'los_days', 
    'is_emergency', 'is_cardiac', 'age_over_65', 
    'has_chronic', 'long_stay'
]

X = df[features]
y = df['readmitted_within_30']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluation
print("Model Performance:")
print(classification_report(y_test, y_pred))
print(f"\nROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")

# Feature importance
importance_df = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(importance_df)

# Predict on all data
df['readmit_risk_score'] = model.predict_proba(X)[:, 1]
df['risk_category'] = pd.cut(df['readmit_risk_score'], 
                               bins=[0, 0.10, 0.20, 1],
                               labels=['Low', 'Medium', 'High'])

# High-risk patients
high_risk = df[df['risk_category'] == 'High'].copy()
print(f"\n{len(high_risk)} high-risk patients identified")
print(f"Expected readmissions in high-risk group: {high_risk['readmit_risk_score'].sum():.0f}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.savefig('capstone1_confusion_matrix.png', dpi=300)
plt.show()
```

### Analysis Part 3: Intervention Strategy

```python
# Cost-benefit analysis
cost_per_readmission = 15000  # Average cost
intervention_cost = 500  # Cost of follow-up program

# Current state
current_readmissions = df['readmitted_within_30'].sum()
current_cost = current_readmissions * cost_per_readmission

# With intervention (assuming 40% reduction in high-risk group)
high_risk_current = high_risk['readmitted_within_30'].sum()
high_risk_prevented = high_risk_current * 0.40
new_readmissions = current_readmissions - high_risk_prevented
new_cost = new_readmissions * cost_per_readmission
intervention_total_cost = len(high_risk) * intervention_cost

# Savings
total_savings = (current_cost - new_cost) - intervention_total_cost

print("INTERVENTION IMPACT ANALYSIS")
print("=" * 50)
print(f"Current readmissions: {current_readmissions:,.0f}")
print(f"Current cost: £{current_cost:,.0f}")
print(f"\nHigh-risk patients: {len(high_risk):,.0f}")
print(f"Expected prevented readmissions: {high_risk_prevented:,.0f}")
print(f"\nNew readmissions: {new_readmissions:,.0f}")
print(f"New cost: £{new_cost:,.0f}")
print(f"Intervention cost: £{intervention_total_cost:,.0f}")
print(f"\nNET SAVINGS: £{total_savings:,.0f}")
print(f"ROI: {(total_savings / intervention_total_cost * 100):.1f}%")
```

### SQL Queries for Production System

```sql
-- Dashboard query: Daily readmission tracking
CREATE VIEW daily_readmission_metrics AS
WITH admissions_with_next AS (
    SELECT 
        a1.admission_id,
        a1.patient_id,
        a1.discharge_date,
        a1.primary_diagnosis,
        MIN(a2.admission_date) as next_admission_date,
        DATEDIFF(MIN(a2.admission_date), a1.discharge_date) as days_to_readmit
    FROM admissions a1
    LEFT JOIN admissions a2 
        ON a1.patient_id = a2.patient_id 
        AND a2.admission_date > a1.discharge_date
    GROUP BY a1.admission_id, a1.patient_id, a1.discharge_date, a1.primary_diagnosis
)
SELECT 
    DATE(discharge_date) as date,
    COUNT(*) as discharges,
    SUM(CASE WHEN days_to_readmit <= 30 THEN 1 ELSE 0 END) as readmissions_30d,
    SUM(CASE WHEN days_to_readmit <= 30 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as readmit_rate
FROM admissions_with_next
GROUP BY DATE(discharge_date)
ORDER BY date DESC;

-- High-risk patient alert system
SELECT 
    p.patient_id,
    p.patient_name,
    a.admission_id,
    a.discharge_date,
    a.primary_diagnosis,
    CASE 
        WHEN a.los_days > 7 AND p.age > 65 THEN 'High'
        WHEN a.admission_type = 'Emergency' AND p.chronic_conditions >= 2 THEN 'High'
        WHEN a.primary_diagnosis = 'Cardiac' AND p.age > 75 THEN 'High'
        ELSE 'Standard'
    END as risk_level
FROM patients p
JOIN admissions a ON p.patient_id = a.patient_id
WHERE a.discharge_date = CURRENT_DATE
  AND CASE 
        WHEN a.los_days > 7 AND p.age > 65 THEN 'High'
        WHEN a.admission_type = 'Emergency' AND p.chronic_conditions >= 2 THEN 'High'
        WHEN a.primary_diagnosis = 'Cardiac' AND p.age > 75 THEN 'High'
        ELSE 'Standard'
    END = 'High'
ORDER BY p.patient_name;
```

### Recommendations & Next Steps

**Immediate Actions:**
1. Implement discharge follow-up program for high-risk patients
2. Enhanced care coordination for cardiac patients
3. Medication reconciliation protocol
4. Post-discharge phone calls within 48 hours

**Expected Outcomes:**
- 15% reduction in 30-day readmissions
- £1.2M annual savings
- Improved patient satisfaction scores
- Better care coordination

**Key Success Metrics:**
- Readmission rate trending below 12%
- 90% follow-up call completion
- Patient satisfaction >4.5/5
- Program ROI >200%

---

## CAPSTONE PROJECT 2: E-Commerce Growth Analytics

### Executive Summary

**Business Context:** Online retailer with £50M annual revenue seeks growth acceleration

**Objective:** Identify growth levers and optimize customer acquisition and retention

**Impact:** 25% revenue increase, £12.5M additional annual revenue

### Data Setup

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate e-commerce data
np.random.seed(42)

# Customers
customers = pd.DataFrame({
    'customer_id': range(1, 100001),
    'signup_date': pd.date_range('2022-01-01', periods=100000, freq='4min'),
    'acquisition_channel': np.random.choice(['Organic', 'Paid Search', 'Social', 'Email', 'Referral'], 100000, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    'country': np.random.choice(['UK', 'US', 'Germany', 'France', 'Other'], 100000, p=[0.4, 0.3, 0.15, 0.1, 0.05])
})

# Orders
num_orders = 250000
orders = pd.DataFrame({
    'order_id': range(1, num_orders + 1),
    'customer_id': np.random.choice(customers['customer_id'], num_orders),
    'order_date': pd.date_range('2022-01-01', periods=num_orders, freq='2min'),
    'order_value': np.random.gamma(5, 20, num_orders),
    'items_count': np.random.poisson(2.5, num_orders) + 1,
    'device': np.random.choice(['Desktop', 'Mobile', 'Tablet'], num_orders, p=[0.4, 0.5, 0.1])
})

# Product categories
orders['category'] = np.random.choice(['Electronics', 'Clothing', 'Home', 'Beauty', 'Sports'], num_orders)

print("E-Commerce Data Generated!")
print(f"Customers: {len(customers):,}")
print(f"Orders: {len(orders):,}")
print(f"Total Revenue: £{orders['order_value'].sum():,.0f}")
```

### Analysis Part 1: Customer Acquisition Analysis

```python
# Merge data
df = orders.merge(customers, on='customer_id')

# Acquisition channel performance
channel_perf = df.groupby('acquisition_channel').agg({
    'order_id': 'count',
    'customer_id': 'nunique',
    'order_value': 'sum'
}).round(2)
channel_perf.columns = ['orders', 'customers', 'revenue']
channel_perf['orders_per_customer'] = channel_perf['orders'] / channel_perf['customers']
channel_perf['revenue_per_customer'] = channel_perf['revenue'] / channel_perf['customers']

print("ACQUISITION CHANNEL PERFORMANCE")
print(channel_perf.sort_values('revenue', ascending=False))

# Monthly growth trends
df['month'] = df['order_date'].dt.to_period('M')
monthly_metrics = df.groupby('month').agg({
    'order_id': 'count',
    'customer_id': 'nunique',
    'order_value': 'sum'
}).reset_index()
monthly_metrics.columns = ['month', 'orders', 'customers', 'revenue']
monthly_metrics['aov'] = monthly_metrics['revenue'] / monthly_metrics['orders']

print("\nMONTHLY TRENDS")
print(monthly_metrics.tail(12))

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Revenue by channel
channel_perf['revenue'].plot(kind='bar', ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Revenue by Acquisition Channel')
axes[0, 0].set_ylabel('Revenue (£)')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Monthly revenue trend
monthly_metrics['revenue'].plot(ax=axes[0, 1], marker='o', linewidth=2)
axes[0, 1].set_title('Monthly Revenue Trend')
axes[0, 1].set_ylabel('Revenue (£)')
axes[0, 1].grid(True, alpha=0.3)

# 3. Customer acquisition by channel
channel_perf['customers'].plot(kind='bar', ax=axes[1, 0], color='coral')
axes[1, 0].set_title('Customers by Channel')
axes[1, 0].set_ylabel('Customers')
axes[1, 0].tick_params(axis='x', rotation=45)

# 4. AOV trend
monthly_metrics['aov'].plot(ax=axes[1, 1], marker='o', color='green')
axes[1, 1].set_title('Average Order Value Trend')
axes[1, 1].set_ylabel('AOV (£)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('capstone2_acquisition.png', dpi=300)
plt.show()
```

### Analysis Part 2: Customer Cohort Analysis

```python
# First purchase cohort
first_purchase = df.groupby('customer_id').agg({
    'order_date': 'min',
    'order_value': 'first'
}).reset_index()
first_purchase.columns = ['customer_id', 'first_purchase_date', 'first_order_value']
first_purchase['cohort'] = first_purchase['first_purchase_date'].dt.to_period('M')

# Merge cohort info
df = df.merge(first_purchase[['customer_id', 'cohort', 'first_order_value']], on='customer_id')

# Cohort size
cohort_sizes = first_purchase.groupby('cohort').size().reset_index(name='cohort_size')

# Monthly activity by cohort
df['order_month'] = df['order_date'].dt.to_period('M')
cohort_data = df.groupby(['cohort', 'order_month']).agg({
    'customer_id': 'nunique',
    'order_value': 'sum'
}).reset_index()
cohort_data.columns = ['cohort', 'order_month', 'active_customers', 'revenue']

# Calculate months since cohort
cohort_data['period'] = (cohort_data['order_month'] - cohort_data['cohort']).apply(lambda x: x.n)

# Merge cohort sizes
cohort_data = cohort_data.merge(cohort_sizes, on='cohort')

# Retention rate
cohort_data['retention_rate'] = cohort_data['active_customers'] / cohort_data['cohort_size'] * 100

# Pivot for heatmap
retention_matrix = cohort_data.pivot_table(
    values='retention_rate',
    index='cohort',
    columns='period'
)

print("COHORT RETENTION ANALYSIS")
print(retention_matrix.head(12))

# Retention heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(retention_matrix, annot=True, fmt='.0f', cmap='RdYlGn', vmin=0, vmax=100)
plt.title('Customer Retention by Cohort (%)')
plt.xlabel('Months Since First Purchase')
plt.ylabel('Cohort Month')
plt.tight_layout()
plt.savefig('capstone2_cohort_retention.png', dpi=300)
plt.show()

# Calculate average retention by month
avg_retention = retention_matrix.mean()
print("\nAverage Retention by Month:")
print(avg_retention)
```

### Analysis Part 3: Revenue Optimization

```python
# Customer lifetime value
customer_metrics = df.groupby('customer_id').agg({
    'order_id': 'count',
    'order_value': 'sum',
    'order_date': ['min', 'max']
}).reset_index()
customer_metrics.columns = ['customer_id', 'order_count', 'total_spent', 'first_order', 'last_order']
customer_metrics['customer_lifespan_days'] = (customer_metrics['last_order'] - customer_metrics['first_order']).dt.days
customer_metrics['avg_order_value'] = customer_metrics['total_spent'] / customer_metrics['order_count']

# Merge with acquisition channel
customer_metrics = customer_metrics.merge(customers[['customer_id', 'acquisition_channel']], on='customer_id')

# CLV by channel
clv_by_channel = customer_metrics.groupby('acquisition_channel').agg({
    'total_spent': 'mean',
    'order_count': 'mean',
    'customer_lifespan_days': 'mean'
}).round(2)

print("CUSTOMER LIFETIME VALUE BY CHANNEL")
print(clv_by_channel.sort_values('total_spent', ascending=False))

# Product category analysis
category_perf = df.groupby('category').agg({
    'order_id': 'count',
    'order_value': ['sum', 'mean'],
    'customer_id': 'nunique'
}).round(2)
category_perf.columns = ['orders', 'total_revenue', 'avg_order_value', 'customers']

print("\nPRODUCT CATEGORY PERFORMANCE")
print(category_perf.sort_values('total_revenue', ascending=False))

# Device performance
device_perf = df.groupby('device').agg({
    'order_id': 'count',
    'order_value': ['sum', 'mean']
}).round(2)
device_perf.columns = ['orders', 'revenue', 'aov']

print("\nDEVICE PERFORMANCE")
print(device_perf)
```

### Analysis Part 4: Growth Recommendations

```python
# Identify growth opportunities
print("\n" + "=" * 60)
print("GROWTH OPPORTUNITIES")
print("=" * 60)

# 1. Channel optimization
best_channel = clv_by_channel['total_spent'].idxmax()
worst_channel = clv_by_channel['total_spent'].idxmin()
print(f"\n1. CHANNEL OPTIMIZATION")
print(f"   - Invest more in: {best_channel} (£{clv_by_channel.loc[best_channel, 'total_spent']:.2f} CLV)")
print(f"   - Reduce spend on: {worst_channel} (£{clv_by_channel.loc[worst_channel, 'total_spent']:.2f} CLV)")
print(f"   - Potential gain: 15% increase in customer acquisition efficiency")

# 2. Retention improvement
month_3_retention = retention_matrix[3].mean()
print(f"\n2. RETENTION IMPROVEMENT")
print(f"   - Current 3-month retention: {month_3_retention:.1f}%")
print(f"   - Target: 65% (+{65 - month_3_retention:.1f} percentage points)")
print(f"   - Strategy: Win-back campaigns, loyalty program, personalized recommendations")

# 3. AOV increase
current_aov = df['order_value'].mean()
print(f"\n3. AVERAGE ORDER VALUE")
print(f"   - Current AOV: £{current_aov:.2f}")
print(f"   - Target: £{current_aov * 1.15:.2f} (+15%)")
print(f"   - Tactics: Product bundling, free shipping thresholds, cross-sell recommendations")

# 4. Category expansion
top_category = category_perf['total_revenue'].idxmax()
print(f"\n4. CATEGORY EXPANSION")
print(f"   - Top category: {top_category} (£{category_perf.loc[top_category, 'total_revenue']:,.0f})")
print(f"   - Action: Expand product range in top categories")
print(f"   - Expected: 10% revenue increase")

# Impact projection
current_annual_revenue = df['order_value'].sum()
projected_improvements = {
    'Channel optimization': current_annual_revenue * 0.05,
    'Retention improvement': current_annual_revenue * 0.08,
    'AOV increase': current_annual_revenue * 0.07,
    'Category expansion': current_annual_revenue * 0.05
}

total_impact = sum(projected_improvements.values())
print(f"\nTOTAL PROJECTED IMPACT")
print(f"Current Revenue: £{current_annual_revenue:,.0f}")
for initiative, impact in projected_improvements.items():
    print(f"{initiative}: +£{impact:,.0f}")
print(f"New Revenue: £{current_annual_revenue + total_impact:,.0f}")
print(f"Growth: +{total_impact / current_annual_revenue * 100:.1f}%")
```

### SQL Production Queries

```sql
-- Daily revenue dashboard
SELECT 
    DATE(order_date) as date,
    COUNT(DISTINCT customer_id) as customers,
    COUNT(*) as orders,
    SUM(order_value) as revenue,
    AVG(order_value) as aov,
    SUM(order_value) / COUNT(DISTINCT customer_id) as revenue_per_customer
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(order_date)
ORDER BY date DESC;

-- Top customers for VIP program
WITH customer_value AS (
    SELECT 
        customer_id,
        COUNT(*) as lifetime_orders,
        SUM(order_value) as lifetime_value,
        MAX(order_date) as last_order_date,
        DATEDIFF(CURRENT_DATE, MAX(order_date)) as days_since_order
    FROM orders
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    c.acquisition_channel,
    cv.lifetime_orders,
    cv.lifetime_value,
    cv.days_since_order,
    CASE 
        WHEN cv.lifetime_value >= 5000 AND cv.lifetime_orders >= 10 THEN 'Platinum'
        WHEN cv.lifetime_value >= 2000 AND cv.lifetime_orders >= 5 THEN 'Gold'
        WHEN cv.lifetime_value >= 1000 THEN 'Silver'
        ELSE 'Standard'
    END as tier
FROM customers c
JOIN customer_value cv ON c.customer_id = cv.customer_id
WHERE cv.lifetime_value >= 1000
ORDER BY cv.lifetime_value DESC
LIMIT 1000;
```

### Final Recommendations

**Priority 1: Channel Optimization**
- Reallocate 30% of marketing budget to top-performing channels
- Expected: £2.5M additional revenue

**Priority 2: Retention Programs**
- Launch loyalty program with points and rewards
- Implement personalized product recommendations
- Expected: £4M additional revenue

**Priority 3: AOV Enhancement**
- Free shipping threshold at £75
- Product bundling for top categories
- Expected: £3.5M additional revenue

**Priority 4: Product Expansion**
- Double SKUs in top 2 categories
- Expected: £2.5M additional revenue

**TOTAL IMPACT: £12.5M (25% growth)**

---

"""
        )

        st.markdown("---")
        st.markdown("## 🚀 ADVANCED TOPICS FOR DATA ANALYSTS")
        st.markdown(
            """**Level up with advanced statistics, ML, and storytelling**

### Advanced Statistics

**Hypothesis Testing:**
```python
from scipy import stats
# T-test for A/B testing
control = [0.12] * 1000  # 12% conversion
treatment = [0.14] * 1000  # 14% conversion
t_stat, p_value = stats.ttest_ind(control, treatment)
print(f"p-value: {p_value:.4f}")
if p_value < 0.05:
    print("Statistically significant!")
```

**Confidence Intervals:**
```python
import numpy as np
def confidence_interval(data, confidence=0.95):
    mean = np.mean(data)
    margin = stats.sem(data) * stats.t.ppf((1 + confidence) / 2, len(data) - 1)
    return mean, mean - margin, mean + margin
```

**Regression Analysis:**
```python
from sklearn.linear_model import LinearRegression
# Predict sales from marketing spend
X = marketing_data[['tv_spend', 'radio_spend', 'social_spend']]
y = marketing_data['sales']
model = LinearRegression().fit(X, y)
print(f"R-squared: {model.score(X, y):.3f}")
```

---

### Machine Learning Basics

**Classification:**
```python
from sklearn.ensemble import RandomForestClassifier
# Predict customer churn
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
predictions = model.predict_proba(X_test)[:, 1]
```

**Clustering:**
```python
from sklearn.cluster import KMeans
# Customer segmentation
kmeans = KMeans(n_clusters=4)
segments = kmeans.fit_predict(customer_features)
```

**Model Evaluation:**
```python
from sklearn.metrics import roc_auc_score, classification_report
auc = roc_auc_score(y_test, predictions)
print(classification_report(y_test, predictions > 0.5))
```

---

### Data Storytelling

**Story Structure:**
1. Setup (Business context)
2. Conflict (The problem)
3. Analysis (Your investigation)
4. Resolution (Key insight)
5. Action (Recommendations)

**Visualization Principles:**
- Bar charts for comparisons
- Line charts for trends
- Pie charts for part-to-whole (use sparingly)
- Scatter plots for correlations
- Heatmaps for patterns

**Executive Summary Template:**
```
[HEADLINE]: One-sentence actionable insight
[DATA]: 2-3 key supporting metrics
[IMPACT]: Business outcomes in £ or %
[ACTIONS]: 3-5 specific recommendations
[TIMELINE]: Next steps with owners
```

---

"""
        )

        st.markdown("---")
        st.markdown("## 📚 ADDITIONAL DETAILED CASE STUDIES")
        st.markdown(
            """**More real-world scenarios with complete solutions**

### Case Study: Subscription Churn Analysis

**Company:** Beauty subscription box  
**Challenge:** 35% monthly churn, losing £500K annually  

```python
# Churn analysis
churn_by_tenure = subscribers.groupby('months_subscribed')['churned'].mean()
print(f"First 3 months churn: {churn_by_tenure.head(3).mean()*100:.1f}%")

# Key insight: 60% churn in first 3 months
early_customizers = subscribers[subscribers['customization_rate'] > 0.5]
print(f"High customizers churn: {early_customizers['churned'].mean()*100:.1f}%")
```

**SQL:**
```sql
SELECT box_value_tier,
    COUNT(*) as subscribers,
    AVG(months_subscribed) as avg_tenure,
    SUM(churned) * 100.0 / COUNT(*) as churn_rate
FROM subscribers GROUP BY box_value_tier;
```

**Recommendations:** Enhanced onboarding, customization prompts  
**Impact:** Reduce churn to 25% = £200K savings

---

### Case Study: Restaurant Operational Analytics

**Company:** 50-location fast-casual chain  
**Challenge:** Inconsistent performance  

```sql
-- Location performance
SELECT location_id,
    AVG(daily_revenue) as avg_revenue,
    AVG(labor_cost_pct) as labor_pct,
    AVG(customer_satisfaction) as csat
FROM daily_operations
WHERE date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY location_id
ORDER BY avg_revenue DESC;
```

**Findings:** Top 10 locations = 40% of profit, labor varies 18-28%  
**Impact:** 15% profit increase = £800K annually

---

### Case Study: Insurance Claim Processing

**Company:** Regional insurer  
**Challenge:** 45-day processing (target: 21 days)  

```sql
-- Bottleneck analysis
SELECT claim_type,
    AVG(DATEDIFF(first_review_date, submission_date)) as days_to_review,
    AVG(DATEDIFF(decision_date, first_review_date)) as days_to_decision
FROM claims GROUP BY claim_type;
```

**Findings:** 40% delays from incomplete docs, 25% require rework  
**Impact:** Reduce to 28 days = 20K more claims/year capacity

---

### Case Study: University Enrollment

**Company:** Mid-sized university  
**Challenge:** Declining enrollment  

```python
# Predictive model
features = ['gpa', 'sat_score', 'campus_visit', 'financial_aid_amount']
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

applicants['enroll_probability'] = model.predict_proba(X)[:, 1]
```

**Findings:** Campus visit = +40% enrollment, aid 40%+ = +25%  
**Impact:** +200 students = £4M revenue

---

### Case Study: Hotel Revenue Management

**Company:** 5-property boutique chain  
**Challenge:** Optimize pricing, maximize RevPAR  

```sql
SELECT property_id, DATE(booking_date) as date,
    AVG(room_rate) * COUNT(*) / total_rooms as revpar,
    COUNT(*) * 100.0 / total_rooms as occupancy
FROM bookings GROUP BY property_id, date;
```

**Findings:** Weekend rates can be +30%, corporate underpriced 15%  
**Impact:** 8% RevPAR increase = £650K revenue

---

"""
        )

        st.markdown("---")
        st.markdown("## 💪 ADDITIONAL PRACTICE PROBLEMS - ALL SKILLS")
        st.markdown(
            """**40+ more problems to master every skill**

### Advanced SQL Practice (15 Problems)

**Problem 1: Recursive CTE for Organizational Hierarchy**
```sql
-- Find all employees reporting to a manager (directly or indirectly)
WITH RECURSIVE org_tree AS (
    -- Base case: direct reports
    SELECT employee_id, manager_id, employee_name, 1 as level
    FROM employees
    WHERE manager_id = 123  -- specific manager
    
    UNION ALL
    
    -- Recursive case: reports of reports
    SELECT e.employee_id, e.manager_id, e.employee_name, ot.level + 1
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.employee_id
    WHERE ot.level < 10  -- prevent infinite recursion
)
SELECT * FROM org_tree ORDER BY level, employee_name;
```

**Problem 2: Median Calculation**
```sql
-- Calculate median salary by department
WITH ranked_salaries AS (
    SELECT 
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary) as row_num,
        COUNT(*) OVER (PARTITION BY department) as total_count
    FROM employees
)
SELECT 
    department,
    AVG(salary) as median_salary
FROM ranked_salaries
WHERE row_num IN (FLOOR((total_count + 1) / 2.0), CEIL((total_count + 1) / 2.0))
GROUP BY department;
```

**Problem 3: Running Totals with Reset**
```sql
-- Running total that resets each month
SELECT 
    DATE(order_date) as date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_monthly_total
FROM orders
ORDER BY order_date;
```

**Problem 4: Gaps and Islands**
```sql
-- Find consecutive date ranges (islands)
WITH date_groups AS (
    SELECT 
        user_id,
        activity_date,
        DATE_SUB(activity_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY activity_date) DAY) as group_id
    FROM user_activity
)
SELECT 
    user_id,
    MIN(activity_date) as streak_start,
    MAX(activity_date) as streak_end,
    DATEDIFF(MAX(activity_date), MIN(activity_date)) + 1 as streak_length
FROM date_groups
GROUP BY user_id, group_id
HAVING DATEDIFF(MAX(activity_date), MIN(activity_date)) + 1 >= 7
ORDER BY streak_length DESC;
```

**Problem 5: Pivot with Dynamic Columns**
```sql
-- Pivot sales by product and month
SELECT 
    product_name,
    SUM(CASE WHEN MONTH(sale_date) = 1 THEN amount ELSE 0 END) as Jan,
    SUM(CASE WHEN MONTH(sale_date) = 2 THEN amount ELSE 0 END) as Feb,
    SUM(CASE WHEN MONTH(sale_date) = 3 THEN amount ELSE 0 END) as Mar,
    SUM(amount) as Total
FROM sales s
JOIN products p ON s.product_id = p.product_id
WHERE YEAR(sale_date) = 2024
GROUP BY product_name
ORDER BY Total DESC;
```

**Problem 6: Self-Join for Comparisons**
```sql
-- Find employees earning more than their manager
SELECT 
    e.employee_name as employee,
    e.salary as employee_salary,
    m.employee_name as manager,
    m.salary as manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;
```

**Problem 7: Complex Aggregation**
```sql
-- Customer purchase patterns
SELECT 
    customer_id,
    COUNT(DISTINCT order_id) as order_count,
    COUNT(DISTINCT DATE(order_date)) as days_with_orders,
    AVG(order_total) as avg_order_value,
    STDDEV(order_total) as order_volatility,
    MIN(order_date) as first_order,
    MAX(order_date) as last_order,
    DATEDIFF(MAX(order_date), MIN(order_date)) as customer_lifespan_days
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT order_id) >= 5;
```

**Problem 8: Time-Based Segmentation**
```sql
-- Classify customers by purchase timing
SELECT 
    customer_id,
    CASE 
        WHEN MAX(order_date) >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY) THEN 'Active'
        WHEN MAX(order_date) >= DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY) THEN 'Lapsing'
        WHEN MAX(order_date) >= DATE_SUB(CURRENT_DATE, INTERVAL 180 DAY) THEN 'At Risk'
        ELSE 'Lost'
    END as customer_status,
    COUNT(*) as lifetime_orders,
    SUM(order_total) as lifetime_value
FROM orders
GROUP BY customer_id;
```

**Problem 9: Ratio Calculations**
```sql
-- Product mix analysis
SELECT 
    category,
    product_name,
    SUM(quantity) as units_sold,
    SUM(revenue) as total_revenue,
    SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER (PARTITION BY category) as pct_of_category,
    SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER () as pct_of_total
FROM sales
GROUP BY category, product_name
ORDER BY category, total_revenue DESC;
```

**Problem 10: Cumulative Percentage**
```sql
-- Pareto analysis (80/20 rule)
WITH product_revenue AS (
    SELECT 
        product_id,
        SUM(revenue) as total_revenue
    FROM sales
    GROUP BY product_id
),
ranked_products AS (
    SELECT 
        product_id,
        total_revenue,
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC) as cumulative_revenue,
        SUM(total_revenue) OVER () as total_company_revenue
    FROM product_revenue
)
SELECT 
    product_id,
    total_revenue,
    cumulative_revenue,
    cumulative_revenue * 100.0 / total_company_revenue as cumulative_pct
FROM ranked_products
WHERE cumulative_revenue * 100.0 / total_company_revenue <= 80;
```

**Problem 11-15: Additional SQL Challenges**

```sql
-- Problem 11: Find duplicate records
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Problem 12: Date range overlap detection
SELECT a.*, b.*
FROM appointments a
JOIN appointments b ON a.doctor_id = b.doctor_id AND a.id < b.id
WHERE a.end_time > b.start_time AND a.start_time < b.end_time;

-- Problem 13: Weighted average
SELECT 
    category,
    SUM(price * quantity) / SUM(quantity) as weighted_avg_price
FROM sales
GROUP BY category;

-- Problem 14: First and last value in group
SELECT 
    customer_id,
    FIRST_VALUE(product_name) OVER (PARTITION BY customer_id ORDER BY order_date) as first_product,
    LAST_VALUE(product_name) OVER (PARTITION BY customer_id ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_product
FROM orders;

-- Problem 15: Conditional aggregation
SELECT 
    region,
    SUM(CASE WHEN status = 'completed' THEN revenue ELSE 0 END) as completed_revenue,
    SUM(CASE WHEN status = 'pending' THEN revenue ELSE 0 END) as pending_revenue,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled_count
FROM orders
GROUP BY region;
```

---

### Advanced Python/Pandas Practice (15 Problems)

**Problem 1: Multi-level Indexing**
```python
import pandas as pd

# Create multi-index dataframe
sales = pd.DataFrame({
    'region': ['East', 'East', 'West', 'West'] * 3,
    'product': ['A', 'B', 'A', 'B'] * 3,
    'quarter': [1]*4 + [2]*4 + [3]*4,
    'revenue': [100, 150, 120, 180, 110, 160, 130, 190, 115, 165, 135, 195]
})

# Set multi-index
sales_pivot = sales.set_index(['region', 'product', 'quarter'])

# Access specific values
print(sales_pivot.loc[('East', 'A', 1)])

# Aggregate at different levels
print(sales_pivot.groupby(level=['region', 'product']).sum())
```

**Problem 2: Rolling Window Calculations**
```python
# Calculate 7-day moving average
df['7day_avg'] = df['value'].rolling(window=7, min_periods=1).mean()

# Exponentially weighted moving average
df['ewma'] = df['value'].ewm(span=7, adjust=False).mean()

# Rolling correlation
df['rolling_corr'] = df['feature1'].rolling(window=30).corr(df['feature2'])
```

**Problem 3: Complex Merging**
```python
# Merge with tolerance (fuzzy join on dates)
pd.merge_asof(
    orders.sort_values('order_date'),
    prices.sort_values('price_date'),
    left_on='order_date',
    right_on='price_date',
    by='product_id',
    tolerance=pd.Timedelta('7 days'),
    direction='backward'
)
```

**Problem 4: Text Processing**
```python
# Extract information from text
df['domain'] = df['email'].str.extract(r'@([a-zA-Z0-9.-]+)')
df['first_name'] = df['full_name'].str.split().str[0]

# Clean phone numbers
df['phone_clean'] = df['phone'].str.replace(r'[^0-9]', '', regex=True)
```

**Problem 5: Handling Missing Data**
```python
# Forward fill within groups
df['value_filled'] = df.groupby('category')['value'].fillna(method='ffill')

# Interpolate numeric values
df['interpolated'] = df['value'].interpolate(method='linear')

# Fill with group statistics
df['filled'] = df.groupby('group')['value'].transform(lambda x: x.fillna(x.median()))
```

**Problem 6: Date Manipulations**
```python
# Business days between dates
df['business_days'] = pd.bdate_range(
    df['start_date'].min(),
    df['end_date'].max()
).size

# Extract date components
df['year'] = df['date'].dt.year
df['quarter'] = df['date'].dt.quarter
df['day_of_week'] = df['date'].dt.day_name()
df['is_month_end'] = df['date'].dt.is_month_end
```

**Problem 7: Groupby with Multiple Functions**
```python
# Apply different functions to different columns
result = df.groupby('category').agg({
    'revenue': ['sum', 'mean', 'std'],
    'quantity': 'sum',
    'order_id': 'count',
    'customer_id': 'nunique'
})

# Custom aggregation function
def coefficient_of_variation(x):
    return x.std() / x.mean()

df.groupby('product')['price'].agg([coefficient_of_variation, 'median'])
```

**Problem 8: Pivot Tables**
```python
# Complex pivot
pivot = pd.pivot_table(
    df,
    values='revenue',
    index=['region', 'product'],
    columns='quarter',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total'
)
```

**Problem 9: Window Functions**
```python
# Rank within groups
df['rank'] = df.groupby('category')['sales'].rank(ascending=False, method='dense')

# Cumulative sum within groups
df['cumsum'] = df.groupby('customer_id')['amount'].cumsum()

# Shift for lag/lead calculations
df['previous_value'] = df.groupby('id')['value'].shift(1)
df['next_value'] = df.groupby('id')['value'].shift(-1)
```

**Problem 10: Applying Functions**
```python
# Apply custom function to rows
def calculate_margin(row):
    return (row['revenue'] - row['cost']) / row['revenue'] * 100

df['margin_pct'] = df.apply(calculate_margin, axis=1)

# Apply to groups
df.groupby('category').apply(lambda x: x.nlargest(3, 'sales'))
```

**Problem 11-15: Additional Pandas Challenges**

```python
# Problem 11: Detect outliers using IQR
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
df['is_outlier'] = (df['value'] < Q1 - 1.5 * IQR) | (df['value'] > Q3 + 1.5 * IQR)

# Problem 12: Normalize data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df['normalized'] = scaler.fit_transform(df[['value']])

# Problem 13: Create bins
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 100], labels=['<18', '18-35', '35-50', '50+'])

# Problem 14: Melt dataframe
df_melted = pd.melt(df, id_vars=['id', 'name'], value_vars=['Q1', 'Q2', 'Q3', 'Q4'], var_name='quarter', value_name='sales')

# Problem 15: Concatenate with keys
combined = pd.concat([df1, df2, df3], keys=['source1', 'source2', 'source3'])
```

---

### Excel Advanced Problems (10 Problems)

**Problem 1: Array Formulas**
```
Find top 3 values in range:
=LARGE(A:A, {1;2;3})

Sum if multiple criteria:
=SUMPRODUCT((A:A="North")*(B:B="Product A")*C:C)
```

**Problem 2: Dynamic Named Ranges**
```
Create dynamic range that adjusts:
=OFFSET($A$1,0,0,COUNTA($A:$A),1)

Use in formulas:
=SUM(DynamicRange)
```

**Problem 3: Conditional Formatting with Formulas**
```
Highlight rows where sales > average:
=$C2>AVERAGE($C:$C)

Highlight duplicates:
=COUNTIF($A:$A,$A2)>1
```

**Problem 4: Advanced VLOOKUP**
```
Two-way lookup:
=INDEX(data,MATCH(lookup_value,first_column,0),MATCH(column_name,header_row,0))

Lookup with multiple criteria:
=INDEX(return_column,MATCH(1,(criteria1=range1)*(criteria2=range2),0))
```

**Problem 5: Date Calculations**
```
Calculate business days:
=NETWORKDAYS(start_date, end_date, holidays)

Age calculation:
=DATEDIF(birth_date, TODAY(), "Y")
```

**Problem 6: Text Functions**
```
Split full name:
First: =LEFT(A2,FIND(" ",A2)-1)
Last: =RIGHT(A2,LEN(A2)-FIND(" ",A2))

Clean data:
=TRIM(CLEAN(SUBSTITUTE(A2,CHAR(160),"")))
```

**Problem 7: Statistical Functions**
```
Percentile:
=PERCENTILE.INC(range, 0.90)

Standard deviation:
=STDEV.P(range)

Correlation:
=CORREL(range1, range2)
```

**Problem 8: What-If Analysis**
```
Goal Seek: Tools → What-If Analysis → Goal Seek
Data Tables: Create two-input table for scenario analysis
Scenario Manager: Save different input combinations
```

**Problem 9: Power Query Transformations**
```
1. Get Data → From Table/Range
2. Transform: Remove duplicates, split columns, pivot
3. Merge queries (like SQL JOIN)
4. Group by with aggregations
5. Load to worksheet
```

**Problem 10: Dashboard Creation**
```
Components:
- Slicers for filtering
- Pivot charts for visualization
- Sparklines for trends
- Conditional formatting for KPIs
- Form controls for interactivity
```

---

"""
        )

        st.markdown("---")
        st.markdown("## 📝 COMPREHENSIVE UNIT ASSESSMENTS")
        st.markdown(
            """**Complete assessments with quizzes, exercises, and grading rubrics**

---

## UNIT 1 ASSESSMENT: Data & Business Questions

### Part A: Multiple Choice (20 points, 2 points each)

**Question 1:** What is the most important first step in data analysis?
- A) Clean the data
- B) Build visualizations
- C) Understand the business question
- D) Run statistical tests

**Answer:** C - Understanding the business question ensures you're solving the right problem.

**Question 2:** Which metric would best measure customer loyalty?
- A) Total revenue
- B) Number of transactions
- C) Repeat purchase rate
- D) Average order value

**Answer:** C - Repeat purchase rate directly measures customer loyalty and retention.

**Question 3:** What does "SMART" stand for in goal setting?
- A) Simple, Measurable, Achievable, Relevant, Timely
- B) Specific, Measurable, Achievable, Relevant, Time-bound
- C) Strategic, Measurable, Actionable, Realistic, Testable
- D) Specific, Meaningful, Accurate, Relevant, Trackable

**Answer:** B - SMART goals are Specific, Measurable, Achievable, Relevant, and Time-bound.

**Question 4:** When analyzing hospital DNA (Did Not Attend) rates, which question is most relevant?
- A) How many patients attended?
- B) What time of day has highest DNA rates?
- C) How much revenue was lost?
- D) All of the above

**Answer:** D - All questions provide valuable insights for comprehensive analysis.

**Question 5:** What is the primary purpose of a data quality audit?
- A) To delete bad data
- B) To understand data limitations and reliability
- C) To increase data volume
- D) To create more reports

**Answer:** B - Understanding data quality helps you make informed analytical decisions.

**Questions 6-10:** [Additional multiple choice questions on data sources, analysis frameworks, stakeholder communication, etc.]

### Part B: Short Answer (30 points, 10 points each)

**Question 1:** Explain the difference between exploratory and confirmatory data analysis. Provide an example of when you would use each approach.

**Model Answer (10 points):**
- Exploratory (5 points): Open-ended investigation to discover patterns, generate hypotheses. Example: Analyzing sales data to identify unexpected trends or customer segments.
- Confirmatory (5 points): Testing specific hypotheses with predetermined methods. Example: A/B test to validate if a new checkout flow increases conversion rates.

**Question 2:** A retail client asks: "Why are sales down?" What follow-up questions would you ask to properly scope the analysis?

**Model Answer (10 points):**
Must include at least 5 relevant questions (2 points each):
- What time period? (Compared to what baseline?)
- Which products/categories?
- Which locations/channels?
- Which customer segments?
- What external factors changed? (seasonality, competition, marketing)
- How is "sales" defined? (revenue, units, transactions)

**Question 3:** Describe three common data quality issues and how you would address each.

**Model Answer (10 points):**
Must identify 3 issues with solutions (3.33 points each):
1. Missing values: Impute with median/mode, forward fill, or analyze separately
2. Duplicates: Identify with GROUP BY, remove based on business logic
3. Inconsistent formats: Standardize using text functions, date parsing, case conversion

### Part C: Practical Exercise (50 points)

**Scenario:** You are analyzing customer complaints for a telecommunications company. You have 6 months of data with 10,000 complaints.

**Tasks:**

1. **Define 3 KPIs** to measure complaint performance (10 points)
   - Complaint resolution time (average days to close)
   - First contact resolution rate (% resolved on first interaction)
   - Complaint recurrence rate (% customers with multiple complaints)

2. **Create analysis plan** (15 points)
   - Data sources needed
   - Key dimensions to analyze (complaint type, customer segment, channel)
   - Statistical methods to use
   - Expected deliverables

3. **Write 3 SQL queries** to extract insights (15 points)
   - Query 1: Average resolution time by complaint type
   - Query 2: Top 10 complaint reasons
   - Query 3: Month-over-month trend

4. **Draft executive summary** (10 points)
   - One-sentence headline finding
   - 3 supporting data points
   - 2-3 recommendations

**Grading Rubric:**
- 90-100: Exceptional - Complete, insightful, professional
- 80-89: Proficient - Complete with minor gaps
- 70-79: Satisfactory - Meets basic requirements
- Below 70: Needs improvement

**Total: 100 points**

---

## UNIT 2 ASSESSMENT: Excel Mastery

### Part A: Multiple Choice (20 points)

**Question 1:** Which function would you use to look up a value in a table where the lookup value is in the first column?
- A) HLOOKUP
- B) VLOOKUP
- C) INDEX
- D) MATCH

**Answer:** B - VLOOKUP searches vertically in the first column.

**Question 2:** What does the $ symbol do in cell references like $A$1?
- A) Converts to currency format
- B) Creates an absolute reference
- C) Adds a comment
- D) Locks the cell

**Answer:** B - $ creates absolute references that don't change when copied.

**Question 3:** Which chart type is best for showing parts of a whole?
- A) Line chart
- B) Bar chart
- C) Pie chart
- D) Scatter plot

**Answer:** C - Pie charts show proportions and percentages of a whole.

**Question 4:** What is a pivot table primarily used for?
- A) Data entry
- B) Summarizing and analyzing data
- C) Creating formulas
- D) Formatting cells

**Answer:** B - Pivot tables summarize and analyze large datasets.

**Question 5:** Which function calculates the average of cells that meet criteria?
- A) AVERAGE
- B) SUMIF
- C) AVERAGEIF
- D) COUNTIF

**Answer:** C - AVERAGEIF calculates average with conditions.

### Part B: Practical Excel Skills (80 points)

**Exercise 1: Formula Mastery (20 points)**

Given dataset with columns: Order_ID, Customer, Product, Quantity, Unit_Price, Date

Create formulas for:
1. Total revenue per order (5 points): =Quantity * Unit_Price
2. Revenue rank (5 points): =RANK(Revenue, Revenue_Range, 0)
3. Month from date (5 points): =TEXT(Date, "mmm") or =MONTH(Date)
4. Conditional sum of revenue >£100 (5 points): =SUMIF(Revenue_Range, ">100")

**Exercise 2: Pivot Table Analysis (25 points)**

Create pivot table showing:
1. Revenue by Product (5 points)
2. Quantity sold by Month (5 points)
3. Average order value by Customer (5 points)
4. Add slicers for Date and Product (5 points)
5. Format as professional report (5 points)

**Exercise 3: Dashboard Creation (35 points)**

Build executive dashboard with:
1. KPI cards showing Total Revenue, Order Count, Avg Order Value (10 points)
2. Revenue trend line chart (8 points)
3. Top 5 products bar chart (8 points)
4. Monthly comparison table (5 points)
5. Professional formatting and interactivity (4 points)

**Grading:**
- Formulas correct and efficient: 20 points
- Pivot table complete and insightful: 25 points
- Dashboard professional and functional: 35 points

**Total: 100 points**

---

## UNIT 3 ASSESSMENT: SQL for Data Analysts

### Part A: SQL Concepts (20 points)

**Question 1:** What does INNER JOIN return?
- A) All rows from both tables
- B) Only matching rows from both tables
- C) All rows from left table
- D) All rows from right table

**Answer:** B - INNER JOIN returns only matching rows.

**Question 2:** What is the purpose of GROUP BY?
- A) Sort results
- B) Filter rows
- C) Aggregate data by categories
- D) Join tables

**Answer:** C - GROUP BY aggregates data into categories.

**Question 3:** Which is correct order of SQL clauses?
- A) SELECT, WHERE, FROM, GROUP BY
- B) SELECT, FROM, WHERE, GROUP BY
- C) FROM, SELECT, WHERE, GROUP BY
- D) WHERE, SELECT, FROM, GROUP BY

**Answer:** B - SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY

**Question 4:** What's the difference between WHERE and HAVING?
- A) No difference
- B) WHERE filters rows before grouping, HAVING filters after
- C) WHERE is for text, HAVING is for numbers
- D) HAVING is faster

**Answer:** B - WHERE filters before aggregation, HAVING filters aggregated results.

**Question 5:** What does DISTINCT do?
- A) Sorts data
- B) Removes duplicate rows
- C) Counts rows
- D) Filters rows

**Answer:** B - DISTINCT removes duplicate rows from results.

### Part B: Write SQL Queries (80 points)

**Database Schema:**
- customers: customer_id, name, city, signup_date
- orders: order_id, customer_id, order_date, total_amount
- products: product_id, product_name, category, price
- order_items: order_id, product_id, quantity

**Query 1: Basic SELECT with filtering (10 points)**
Find all customers from London who signed up in 2024.

```sql
SELECT customer_id, name, signup_date
FROM customers
WHERE city = 'London'
  AND YEAR(signup_date) = 2024;
```

**Query 2: JOIN and aggregation (15 points)**
Calculate total revenue by customer, showing only customers with >£1000 total.

```sql
SELECT 
    c.customer_id,
    c.name,
    SUM(o.total_amount) as total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(o.total_amount) > 1000
ORDER BY total_revenue DESC;
```

**Query 3: Multiple JOINs (15 points)**
List all products sold in each order with customer names.

```sql
SELECT 
    o.order_id,
    c.name as customer_name,
    p.product_name,
    oi.quantity,
    oi.quantity * p.price as line_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id;
```

**Query 4: Window functions (20 points)**
Rank products by total revenue within each category.

```sql
SELECT 
    category,
    product_name,
    SUM(oi.quantity * p.price) as total_revenue,
    RANK() OVER (PARTITION BY category ORDER BY SUM(oi.quantity * p.price) DESC) as category_rank
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY category, product_name;
```

**Query 5: Complex analysis (20 points)**
Find customers who haven't ordered in the last 90 days but ordered before that.

```sql
SELECT 
    c.customer_id,
    c.name,
    MAX(o.order_date) as last_order_date,
    DATEDIFF(CURRENT_DATE, MAX(o.order_date)) as days_since_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING MAX(o.order_date) < DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)
  AND MAX(o.order_date) >= DATE_SUB(CURRENT_DATE, INTERVAL 365 DAY)
ORDER BY days_since_order DESC;
```

**Grading Rubric:**
- Syntax correct: 40%
- Logic correct: 40%
- Efficiency: 10%
- Formatting/readability: 10%

**Total: 100 points**

---

## UNIT 4 ASSESSMENT: BI Dashboards & Visualization

### Part A: Visualization Theory (20 points)

**Question 1:** When should you use a line chart?
- A) Comparing categories
- B) Showing trends over time
- C) Displaying parts of whole
- D) Showing correlation

**Answer:** B - Line charts show trends and changes over time.

**Question 2:** What is the most important principle in dashboard design?
- A) Use many colors
- B) Show all available data
- C) Prioritize the most important information
- D) Use 3D effects

**Answer:** C - Prioritize important information for clarity.

**Question 3:** What is "chart junk"?
- A) Broken charts
- B) Unnecessary decorative elements
- C) Missing data
- D) Wrong chart type

**Answer:** B - Chart junk is unnecessary visual clutter.

**Question 4:** How many colors should a professional dashboard typically use?
- A) As many as possible
- B) 2-3 main colors
- C) 10+ colors
- D) Only black and white

**Answer:** B - 2-3 main colors maintain clarity and professionalism.

**Question 5:** What is the "F-pattern" in dashboard layout?
- A) Frequency distribution
- B) How users' eyes scan the page
- C) Filter organization
- D) Font selection

**Answer:** B - Users scan in an F-pattern (top-left priority).

### Part B: Dashboard Design Project (80 points)

**Scenario:** Create executive sales dashboard for retail company.

**Requirements:**

**1. KPI Section (20 points)**
- Total revenue (current month vs prior month)
- Number of orders
- Average order value
- Customer count
- Use color coding (green/red for up/down)

**2. Trend Analysis (20 points)**
- Revenue trend over 12 months (line chart)
- Add forecast line
- Include comparison to previous year
- Show seasonality

**3. Category Breakdown (15 points)**
- Revenue by product category (bar chart or treemap)
- Top 10 products (sorted bar chart)
- Category performance table

**4. Geographic Analysis (15 points)**
- Sales by region (map or bar chart)
- Regional growth rates
- Store-level detail available via drill-down

**5. Interactivity & Design (10 points)**
- Date range filter
- Category slicer
- Region selector
- Professional formatting
- Mobile-responsive layout

**Grading Rubric:**
- Completeness: 30%
- Design quality: 25%
- Functionality: 25%
- Insights clarity: 20%

**Deliverable:** Working dashboard in Tableau or Power BI + 2-page design document

**Total: 100 points**

---

## UNIT 5 ASSESSMENT: Python for Analysts

### Part A: Python Concepts (20 points)

**Question 1:** Which library is primarily used for data manipulation in Python?
- A) numpy
- B) pandas
- C) matplotlib
- D) scipy

**Answer:** B - pandas is the primary library for data manipulation.

**Question 2:** What does df.head() do?
- A) Removes header row
- B) Shows first 5 rows
- C) Sorts data
- D) Counts rows

**Answer:** B - df.head() displays the first 5 rows by default.

**Question 3:** How do you select a column in pandas?
- A) df.column_name or df['column_name']
- B) df->column_name
- C) df::column_name
- D) df.get(column_name)

**Answer:** A - Use dot notation or bracket notation.

**Question 4:** What is the purpose of groupby() in pandas?
- A) Sort data
- B) Aggregate data by categories
- C) Filter data
- D) Join dataframes

**Answer:** B - groupby() aggregates data into groups.

**Question 5:** Which method removes missing values?
- A) drop_na()
- B) remove_null()
- C) dropna()
- D) clean()

**Answer:** C - dropna() removes rows/columns with missing values.

### Part B: Coding Exercises (80 points)

**Exercise 1: Data Cleaning (20 points)**

```python
import pandas as pd

# Given messy data
data = {
    'customer_id': [1, 2, 2, 3, 4, None],
    'name': ['John Smith', 'jane doe', 'Jane Doe', 'BOB JONES', 'Alice'],
    'email': ['john@email.com', 'jane@email', None, 'bob@email.com', 'alice@email.com'],
    'age': [25, None, 30, -5, 45],
    'revenue': [100, 200, 200, 150, 300]
}
df = pd.DataFrame(data)

# Tasks (4 points each):
# 1. Remove duplicate customer_ids
df_clean = df.drop_duplicates(subset='customer_id', keep='first')

# 2. Standardize names to Title Case
df_clean['name'] = df_clean['name'].str.title()

# 3. Fill missing emails with "unknown@company.com"
df_clean['email'] = df_clean['email'].fillna('unknown@company.com')

# 4. Replace invalid ages (negative or null) with median
median_age = df_clean[df_clean['age'] > 0]['age'].median()
df_clean['age'] = df_clean['age'].apply(lambda x: median_age if pd.isna(x) or x < 0 else x)

# 5. Remove rows where customer_id is null
df_clean = df_clean.dropna(subset=['customer_id'])
```

**Exercise 2: Data Analysis (30 points)**

```python
# Given sales dataset
sales = pd.read_csv('sales_data.csv')
# Columns: date, product, category, quantity, unit_price, customer_id

# Tasks:

# 1. Calculate total revenue (10 points)
sales['revenue'] = sales['quantity'] * sales['unit_price']
total_revenue = sales['revenue'].sum()
print(f"Total Revenue: £{total_revenue:,.2f}")

# 2. Find top 5 products by revenue (10 points)
top_products = (sales.groupby('product')['revenue']
                .sum()
                .sort_values(ascending=False)
                .head(5))
print("Top 5 Products:")
print(top_products)

# 3. Calculate monthly revenue trend (10 points)
sales['date'] = pd.to_datetime(sales['date'])
sales['month'] = sales['date'].dt.to_period('M')
monthly_revenue = sales.groupby('month')['revenue'].sum()
print("Monthly Revenue:")
print(monthly_revenue)
```

**Exercise 3: Visualization (30 points)**

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Tasks:

# 1. Create revenue trend line chart (10 points)
plt.figure(figsize=(12, 6))
monthly_revenue.plot(kind='line', marker='o')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue (£)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 2. Create category revenue bar chart (10 points)
category_revenue = sales.groupby('category')['revenue'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
category_revenue.plot(kind='bar')
plt.title('Revenue by Category')
plt.xlabel('Category')
plt.ylabel('Revenue (£)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Create customer purchase distribution histogram (10 points)
customer_totals = sales.groupby('customer_id')['revenue'].sum()
plt.figure(figsize=(10, 6))
plt.hist(customer_totals, bins=30, edgecolor='black')
plt.title('Customer Purchase Distribution')
plt.xlabel('Total Purchase Value (£)')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.show()
```

**Grading Rubric:**
- Code correctness: 50%
- Code efficiency: 20%
- Code readability: 15%
- Output correctness: 15%

**Total: 100 points**

---

## UNIT 6 ASSESSMENT: Metrics & A/B Testing

### Part A: Concepts (30 points)

**Question 1:** What is a "North Star Metric"?
- A) The most expensive metric
- B) The key metric that drives business success
- C) A directional indicator
- D) A vanity metric

**Answer:** B - North Star Metric is the key success driver.

**Question 2:** What is statistical significance typically set at?
- A) p < 0.10
- B) p < 0.05
- C) p < 0.01
- D) p < 0.001

**Answer:** B - p < 0.05 is the standard threshold.

**Question 3:** What is a Type I error?
- A) False positive (rejecting true null hypothesis)
- B) False negative (failing to reject false null hypothesis)
- C) Sampling error
- D) Measurement error

**Answer:** A - Type I error is a false positive.

**Question 4:** What is minimum sample size important for?
- A) Cost savings
- B) Statistical power and reliability
- C) Faster results
- D) Easier analysis

**Answer:** B - Adequate sample size ensures statistical validity.

**Question 5:** What is "experiment contamination"?
- A) Dirty data
- B) Users experiencing both variants
- C) Technical errors
- D) Biased sampling

**Answer:** B - Contamination occurs when users see multiple variants.

### Part B: Design an A/B Test (70 points)

**Scenario:** E-commerce company wants to test a new checkout page.

**Tasks:**

**1. Define hypothesis (10 points)**
- Null hypothesis (H0): New checkout page has no effect on conversion rate
- Alternative hypothesis (H1): New checkout page increases conversion rate
- Success metric: Checkout conversion rate (orders/checkout starts)

**2. Calculate sample size (15 points)**
```python
from statsmodels.stats.power import zt_ind_solve_power

baseline_rate = 0.25  # 25% current conversion
mde = 0.03  # Detect 3% absolute lift (12% relative)
alpha = 0.05
power = 0.80

sample_size = zt_ind_solve_power(
    effect_size=(0.28 - 0.25) / np.sqrt(0.25 * 0.75),
    alpha=alpha,
    power=power
)

print(f"Required sample size per variant: {int(sample_size)}")
# Approximately 2,500 per variant
```

**3. Design experiment (20 points)**
Must include:
- Randomization method: User-level, 50/50 split
- Duration: 2 weeks minimum
- Primary metric: Conversion rate
- Secondary metrics: Revenue per user, time to complete
- Guardrail metrics: Error rates, load times
- Segmentation plan: Mobile vs desktop, new vs returning

**4. Analysis plan (15 points)**
```python
# Calculate conversion rates
control_conversions = control_group['converted'].mean()
treatment_conversions = treatment_group['converted'].mean()
lift = (treatment_conversions - control_conversions) / control_conversions

# Statistical test
from scipy.stats import chi2_contingency
contingency = pd.crosstab(df['variant'], df['converted'])
chi2, p_value, dof, expected = chi2_contingency(contingency)

print(f"Control: {control_conversions:.2%}")
print(f"Treatment: {treatment_conversions:.2%}")
print(f"Lift: {lift:.2%}")
print(f"P-value: {p_value:.4f}")
print(f"Significant: {p_value < 0.05}")
```

**5. Interpretation (10 points)**
- If p < 0.05 and lift > 0: Launch treatment
- If p < 0.05 and lift < 0: Keep control
- If p >= 0.05: No significant difference, may need larger sample or longer duration
- Check for Simpson's paradox across segments

**Grading:**
- Hypothesis clarity: 10 points
- Sample size calculation: 15 points
- Experimental design: 20 points
- Analysis methodology: 15 points
- Interpretation: 10 points

**Total: 100 points**

---

## UNIT 7 ASSESSMENT: Capstone Project

### Capstone Project Requirements (100 points)

**Choose one of these projects:**

**Option A: Customer Analytics Dashboard**
**Option B: Sales Forecasting Model**
**Option C: Operational Efficiency Analysis**

**Project Deliverables:**

**1. Business Problem Definition (10 points)**
- Clear problem statement
- Stakeholder identification
- Success criteria
- Expected impact

**2. Data Collection & Preparation (20 points)**
- Data sources identified
- Data extraction (SQL queries)
- Data cleaning documentation
- Data quality assessment

**3. Exploratory Data Analysis (20 points)**
- Descriptive statistics
- Distribution analysis
- Correlation analysis
- Key insights identified

**4. Analysis & Modeling (25 points)**
- Appropriate analytical methods
- Statistical tests performed
- Models built (if applicable)
- Results validated

**5. Visualization & Dashboard (15 points)**
- Professional dashboard created
- Interactive elements
- Clear visual hierarchy
- Mobile-responsive

**6. Recommendations & Impact (10 points)**
- Clear, actionable recommendations
- Business impact quantified
- Implementation plan
- Risk assessment

**Grading Rubric:**
- Technical execution: 50%
- Business value: 25%
- Presentation quality: 15%
- Innovation: 10%

**Total: 100 points**

---

## Assessment Summary

**All 7 Units:**
- **Total possible points:** 700 (100 per unit)
- **Passing score:** 70% (490 points)
- **Proficient:** 80% (560 points)
- **Exceptional:** 90% (630 points)

**Certification Requirements:**
✅ Complete all 7 unit assessments
✅ Score 70%+ on each unit
✅ Complete capstone project
✅ Pass final comprehensive exam

---

"""
        )

        st.markdown("---")
        st.markdown("## ❓ FREQUENTLY ASKED QUESTIONS & TROUBLESHOOTING")
        st.markdown(
            """**Complete FAQ and troubleshooting guide for all tools**

---

## SQL FAQs & Troubleshooting

### Common SQL Questions

**Q: What's the difference between INNER JOIN and LEFT JOIN?**
A: INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from the left table and matching rows from the right table (with NULLs where no match exists).

```sql
-- INNER JOIN: Only customers with orders
SELECT c.name, COUNT(o.order_id) as order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name;

-- LEFT JOIN: All customers, even those without orders
SELECT c.name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name;
```

**Q: When should I use WHERE vs HAVING?**
A: WHERE filters rows before aggregation. HAVING filters after aggregation.

```sql
-- WHERE: Filter before grouping
SELECT category, AVG(price) as avg_price
FROM products
WHERE price > 10  -- Filter individual rows
GROUP BY category;

-- HAVING: Filter after grouping
SELECT category, AVG(price) as avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 50;  -- Filter aggregated results
```

**Q: How do I handle NULL values in comparisons?**
A: Use IS NULL or IS NOT NULL, never = NULL or != NULL.

```sql
-- WRONG
SELECT * FROM customers WHERE email = NULL;

-- CORRECT
SELECT * FROM customers WHERE email IS NULL;

-- Use COALESCE to provide default values
SELECT 
    customer_name,
    COALESCE(email, 'No email provided') as email,
    COALESCE(phone, 'No phone') as phone
FROM customers;
```

**Q: What's the difference between COUNT(*) and COUNT(column)?**
A: COUNT(*) counts all rows. COUNT(column) counts non-NULL values in that column.

```sql
SELECT 
    COUNT(*) as total_rows,              -- Counts all rows
    COUNT(email) as rows_with_email,     -- Counts non-NULL emails
    COUNT(DISTINCT email) as unique_emails  -- Counts unique non-NULL emails
FROM customers;
```

**Q: How do I get the top N results per group?**
A: Use window functions with ROW_NUMBER() or RANK().

```sql
-- Top 3 products per category by sales
WITH ranked AS (
    SELECT 
        category,
        product_name,
        sales,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC) as rank
    FROM products
)
SELECT * FROM ranked WHERE rank <= 3;
```

### Common SQL Errors & Solutions

**Error: "Column 'X' is ambiguous"**
```sql
-- PROBLEM: Column exists in multiple tables
SELECT customer_id, order_date
FROM customers
JOIN orders USING (customer_id);  -- customer_id is in both tables

-- SOLUTION: Prefix with table name or alias
SELECT c.customer_id, o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

**Error: "Invalid use of group function"**
```sql
-- PROBLEM: Using aggregate in WHERE clause
SELECT customer_id, SUM(amount)
FROM orders
WHERE SUM(amount) > 1000  -- WRONG
GROUP BY customer_id;

-- SOLUTION: Use HAVING instead
SELECT customer_id, SUM(amount) as total
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;  -- CORRECT
```

**Error: "Subquery returns more than 1 row"**
```sql
-- PROBLEM: Subquery in = comparison returns multiple rows
SELECT * FROM products
WHERE category_id = (SELECT category_id FROM categories WHERE active = 1);

-- SOLUTION: Use IN instead of =
SELECT * FROM products
WHERE category_id IN (SELECT category_id FROM categories WHERE active = 1);
```

**Error: "Division by zero"**
```sql
-- PROBLEM: Dividing by a column that might be zero
SELECT revenue / quantity as price_per_unit
FROM sales;

-- SOLUTION: Use NULLIF or CASE
SELECT 
    revenue / NULLIF(quantity, 0) as price_per_unit,
    -- OR
    CASE WHEN quantity = 0 THEN NULL ELSE revenue / quantity END as price
FROM sales;
```

**Error: "Date format issues"**
```sql
-- PROBLEM: Inconsistent date formats
WHERE order_date = '2024-01-15'  -- Works in some DBs
WHERE order_date = '01/15/2024'  -- Format varies by region

-- SOLUTION: Use proper date functions
WHERE order_date = STR_TO_DATE('2024-01-15', '%Y-%m-%d')
WHERE DATE(order_date) = '2024-01-15'
WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31'
```

### SQL Performance Tips

**1. Use indexes wisely**
```sql
-- Create indexes on frequently queried columns
CREATE INDEX idx_customer_email ON customers(email);
CREATE INDEX idx_order_date ON orders(order_date);

-- Compound index for multiple columns often queried together
CREATE INDEX idx_order_customer_date ON orders(customer_id, order_date);
```

**2. Avoid SELECT ***
```sql
-- SLOW: Retrieves all columns
SELECT * FROM large_table WHERE condition;

-- FAST: Only get what you need
SELECT id, name, email FROM large_table WHERE condition;
```

**3. Use EXISTS instead of IN for large subqueries**
```sql
-- SLOWER with large subquery
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders WHERE year = 2024);

-- FASTER
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND year = 2024);
```

**4. Filter early in JOINs**
```sql
-- SLOW: Joins entire table then filters
SELECT c.*, o.*
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01';

-- FAST: Filter before joining
SELECT c.*, o.*
FROM customers c
JOIN (SELECT * FROM orders WHERE order_date >= '2024-01-01') o
ON c.customer_id = o.customer_id;
```

---

## Python/Pandas FAQs & Troubleshooting

### Common Python Questions

**Q: How do I read different file formats?**
```python
import pandas as pd

# CSV
df = pd.read_csv('data.csv')

# Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# JSON
df = pd.read_json('data.json')

# SQL database
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql_query("SELECT * FROM table", conn)

# With specific parameters
df = pd.read_csv('data.csv',
                 encoding='utf-8',
                 sep=',',
                 thousands=',',
                 decimal='.',
                 na_values=['NA', 'missing'],
                 parse_dates=['date_column'])
```

**Q: How do I handle missing data?**
```python
# Check for missing values
print(df.isnull().sum())
print(df.isna().sum())  # Same as isnull()

# Drop rows with any missing values
df_clean = df.dropna()

# Drop rows where specific column is missing
df_clean = df.dropna(subset=['important_column'])

# Fill missing values
df['column'] = df['column'].fillna(0)  # Fill with 0
df['column'] = df['column'].fillna(df['column'].mean())  # Fill with mean
df['column'] = df['column'].fillna(method='ffill')  # Forward fill
df['column'] = df['column'].fillna(method='bfill')  # Backward fill

# Fill different columns with different values
df = df.fillna({'col1': 0, 'col2': 'Unknown', 'col3': df['col3'].median()})
```

**Q: How do I merge/join dataframes?**
```python
# Inner join (like SQL INNER JOIN)
merged = pd.merge(df1, df2, on='customer_id', how='inner')

# Left join (like SQL LEFT JOIN)
merged = pd.merge(df1, df2, on='customer_id', how='left')

# Join on multiple columns
merged = pd.merge(df1, df2, on=['customer_id', 'date'], how='inner')

# Join on different column names
merged = pd.merge(df1, df2, left_on='cust_id', right_on='customer_id')

# Concatenate vertically (stack dataframes)
combined = pd.concat([df1, df2], axis=0, ignore_index=True)

# Concatenate horizontally (side by side)
combined = pd.concat([df1, df2], axis=1)
```

**Q: How do I group and aggregate?**
```python
# Simple groupby
grouped = df.groupby('category')['sales'].sum()

# Multiple aggregations
result = df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': 'sum',
    'customer_id': 'nunique'
})

# Custom aggregation function
def coefficient_of_variation(x):
    return x.std() / x.mean()

result = df.groupby('product')['price'].agg([
    'mean',
    'median',
    coefficient_of_variation
])

# Group by multiple columns
result = df.groupby(['region', 'category'])['sales'].sum()

# Reset index after groupby
result = df.groupby('category')['sales'].sum().reset_index()
```

**Q: How do I filter dataframes?**
```python
# Single condition
filtered = df[df['age'] > 25]

# Multiple conditions with &, |
filtered = df[(df['age'] > 25) & (df['city'] == 'London')]
filtered = df[(df['age'] < 18) | (df['age'] > 65)]

# NOT condition with ~
filtered = df[~(df['status'] == 'inactive')]

# Filter using isin()
filtered = df[df['category'].isin(['Electronics', 'Clothing'])]

# Filter using string methods
filtered = df[df['email'].str.contains('@gmail.com')]
filtered = df[df['name'].str.startswith('John')]

# Filter using query() method
filtered = df.query('age > 25 and city == "London"')
```

### Common Python Errors & Solutions

**Error: "KeyError: 'column_name'"**
```python
# PROBLEM: Column doesn't exist
df['non_existent_column']

# SOLUTION: Check column names first
print(df.columns.tolist())

# Or use .get() method which returns None if not found
value = df.get('column_name', default=0)

# Or check if column exists
if 'column_name' in df.columns:
    df['column_name']
```

**Error: "ValueError: Cannot index with multidimensional key"**
```python
# PROBLEM: Using list instead of proper indexing
columns_to_select = ['col1', 'col2']
df[columns_to_select, :]  # WRONG

# SOLUTION: Use double brackets for multiple columns
df[['col1', 'col2']]
df.loc[:, ['col1', 'col2']]
```

**Error: "SettingWithCopyWarning"**
```python
# PROBLEM: Modifying a slice of dataframe
subset = df[df['age'] > 25]
subset['new_col'] = 0  # Warning!

# SOLUTION: Use .copy() or .loc[]
subset = df[df['age'] > 25].copy()
subset['new_col'] = 0

# OR
df.loc[df['age'] > 25, 'new_col'] = 0
```

**Error: "TypeError: unsupported operand type(s)"**
```python
# PROBLEM: Operating on wrong data types
df['text_column'] + 5  # Can't add number to string

# SOLUTION: Convert data types
df['numeric_column'] = pd.to_numeric(df['text_column'], errors='coerce')
df['date_column'] = pd.to_datetime(df['date_string'])
df['string_column'] = df['numeric_column'].astype(str)
```

**Error: "Memory error when loading large files"**
```python
# PROBLEM: File too large to load at once
df = pd.read_csv('huge_file.csv')  # Memory error!

# SOLUTION 1: Read in chunks
chunks = []
for chunk in pd.read_csv('huge_file.csv', chunksize=10000):
    # Process each chunk
    processed = chunk[chunk['value'] > 0]
    chunks.append(processed)
df = pd.concat(chunks)

# SOLUTION 2: Read only needed columns
df = pd.read_csv('huge_file.csv', usecols=['col1', 'col2', 'col3'])

# SOLUTION 3: Use dtypes to reduce memory
df = pd.read_csv('huge_file.csv', dtype={'id': 'int32', 'value': 'float32'})
```

### Python Performance Tips

**1. Vectorize operations instead of loops**
```python
# SLOW: Using loops
result = []
for val in df['column']:
    result.append(val * 2)
df['result'] = result

# FAST: Vectorized
df['result'] = df['column'] * 2
```

**2. Use appropriate data types**
```python
# Check current memory usage
print(df.memory_usage(deep=True))

# Optimize data types
df['int_column'] = df['int_column'].astype('int32')  # Instead of int64
df['category_column'] = df['category_column'].astype('category')  # For categorical data
```

**3. Use built-in methods instead of apply()**
```python
# SLOW: Using apply
df['upper'] = df['name'].apply(lambda x: x.upper())

# FAST: Built-in string method
df['upper'] = df['name'].str.upper()
```

---

## Excel FAQs & Troubleshooting

### Common Excel Questions

**Q: How do I fix #REF! errors?**
A: #REF! occurs when a formula refers to cells that no longer exist.
```
Common causes:
- Deleted rows/columns that formulas reference
- Copied formulas that reference fixed cells incorrectly

Solutions:
- Use Find & Replace to fix broken references
- Use named ranges instead of cell references
- Check formula with F2 to see highlighted references
```

**Q: Why is my VLOOKUP returning #N/A?**
```
Common causes:
1. Lookup value doesn't exist in the table
2. Approximate match on unsorted data
3. Extra spaces in lookup values
4. Different data types (number vs text)

Solutions:
- Use exact match: VLOOKUP(value, range, col, FALSE)
- Trim spaces: VLOOKUP(TRIM(A2), range, col, FALSE)
- Use IFERROR to handle missing values: IFERROR(VLOOKUP(...), "Not Found")
- Convert types: VLOOKUP(TEXT(A2,"0"), range, col, FALSE)
```

**Q: How do I reference cells across sheets?**
```
Same workbook:
=Sheet2!A1
='Sheet Name with Spaces'!A1
=SUM(Sheet2:Sheet5!A1)  -- Same cell across multiple sheets

Different workbook:
='[Workbook.xlsx]Sheet1'!A1
```

**Q: What's the difference between relative and absolute references?**
```
A1 - Relative (changes when copied)
$A$1 - Absolute (stays fixed)
$A1 - Mixed (column fixed, row changes)
A$1 - Mixed (row fixed, column changes)

Example:
Cell B2: =A1*$D$1
Copy to C3: =B2*$D$1  (A1 became B2, but $D$1 stayed $D$1)
```

**Q: How do I handle circular references?**
```
Circular reference occurs when formula refers to itself.

Check:
- Formulas → Error Checking → Circular References

Solutions:
- Enable iterative calculations (if intentional)
- File → Options → Formulas → Enable iterative calculation
- Or restructure formula to avoid circularity
```

### Common Excel Errors & Solutions

**Error: #VALUE!**
```
Causes:
- Wrong data type in formula
- Text in math formula
- Spaces before/after numbers

Solutions:
- Use VALUE() to convert text to number
- Use TRIM() to remove spaces
- Check for hidden characters
```

**Error: #DIV/0!**
```
Cause: Dividing by zero or empty cell

Solutions:
- Use IFERROR: =IFERROR(A1/B1, 0)
- Use IF: =IF(B1=0, 0, A1/B1)
- Use conditional: =IF(B1<>0, A1/B1, "N/A")
```

**Error: #NAME?**
```
Causes:
- Misspelled function name
- Missing quotes around text
- Named range doesn't exist

Solutions:
- Check spelling of function
- Add quotes: ="Hello" not =Hello
- Check named ranges: Formulas → Name Manager
```

**Error: Pivot table won't refresh**
```
Solutions:
1. Check data source range
2. Right-click pivot → Refresh
3. PivotTable Analyze → Change Data Source
4. Close and reopen workbook
5. Check if source data is a table (Format as Table)
```

### Excel Performance Tips

**1. Avoid volatile functions**
```
Volatile (slow):
- NOW()
- TODAY()
- RAND()
- OFFSET()
- INDIRECT()

Use sparingly or replace with:
- Manual entry for current date
- Fixed references instead of INDIRECT
```

**2. Use tables instead of ranges**
```
Benefits:
- Auto-expanding formulas
- Structured references
- Easier pivot table source
- Better performance

Convert: Select range → Ctrl+T
```

**3. Limit conditional formatting**
```
- Use on visible areas only
- Avoid entire column references (A:A)
- Use simpler rules
- Clear unused rules: Home → Conditional Formatting → Manage Rules
```

---

## BI Tools (Tableau/Power BI) FAQs

### Common BI Questions

**Q: What's the difference between dimensions and measures?**
```
Dimensions:
- Categorical data (text, dates)
- Used for grouping and filtering
- Examples: Product name, region, date

Measures:
- Numeric data for aggregation
- Used for calculations
- Examples: Sales, quantity, profit
```

**Q: How do I create calculated fields?**
```
Tableau:
- Analysis → Create Calculated Field
- Example: [Sales] - [Cost]
- Example: IF [Sales] > 1000 THEN "High" ELSE "Low" END

Power BI:
- Modeling → New Column (DAX)
- Example: Profit = [Sales] - [Cost]
- Example: Category = IF([Sales] > 1000, "High", "Low")
```

**Q: When should I use parameters?**
```
Use cases:
- Dynamic top N filtering
- What-if analysis
- Dynamic measure selection
- Custom bins

Tableau: Create Parameter → Show Parameter Control
Power BI: Modeling → New Parameter
```

**Q: How do I optimize dashboard performance?**
```
1. Extract data instead of live connection
2. Aggregate data before importing
3. Limit number of visualizations per page
4. Use filters efficiently
5. Hide unused fields
6. Remove unnecessary calculations
7. Use context filters (Tableau) or filter order (Power BI)
```

### Common BI Errors & Solutions

**Error: "Cannot mix aggregate and non-aggregate arguments"**
```
Problem: Mixing detail and aggregate levels

Tableau Solution:
- Use LOD expressions
- {FIXED [Category] : SUM([Sales])}

Power BI Solution:
- Use CALCULATE or SUMX
- CALCULATE(SUM(Sales), ALLEXCEPT(Products, Products[Category]))
```

**Error: "Data source too large"**
```
Solutions:
1. Filter data before import
2. Aggregate at appropriate level
3. Use extracts instead of live
4. Create custom SQL query
5. Use data sampling for development
```

**Error: "Relationships not working"**
```
Check:
1. Key fields same data type
2. No duplicates in "one" side of relationship
3. Relationship cardinality correct
4. Active relationships in Power BI
5. No circular dependencies
```

---

## General Troubleshooting Tips

### Data Quality Checklist

**Before analysis:**
```
✅ Check for missing values
✅ Identify duplicates
✅ Verify data types
✅ Check for outliers
✅ Validate date ranges
✅ Confirm units/currency
✅ Check for formatting issues
✅ Verify joins/relationships
✅ Document assumptions
✅ Test with sample data
```

### Debugging Workflow

**1. Isolate the problem**
- Break complex queries into parts
- Test each component separately
- Use smaller data samples

**2. Check assumptions**
- Verify data is what you expect
- Check row counts at each step
- Validate calculations manually

**3. Use print/display statements**
```python
# Python
print(df.shape)
print(df.head())
print(df.dtypes)
print(df['column'].value_counts())
```

```sql
-- SQL
SELECT COUNT(*) FROM table;  -- Check row count
SELECT * FROM table LIMIT 10;  -- Sample data
SELECT column, COUNT(*) FROM table GROUP BY column;  -- Check distribution
```

**4. Search for error messages**
- Copy exact error message
- Search Stack Overflow, documentation
- Check official forums

**5. Ask for help effectively**
```
Include:
- What you're trying to do
- What you've tried
- Exact error message
- Sample data (if possible)
- Relevant code
- Your environment (versions, tools)
```

---

"""
        )

        st.markdown("---")
        st.markdown("## 🎥 VIDEO WALKTHROUGH SCRIPTS")
        st.markdown(
            """**Complete video scripts for instructor-led content**

---

## Unit 1 Video Scripts

### Video 1: "What is Data Analysis?" (5 minutes)

**[INTRO - 30 seconds]**

Hello! Welcome to the Data Analyst Pathway. I'm excited to guide you through your journey to becoming a professional data analyst.

In this video, we'll answer the fundamental question: What is data analysis, and why does it matter?

**[SECTION 1: Definition - 1 minute]**

Data analysis is the process of examining, cleaning, transforming, and modeling data to discover useful information, draw conclusions, and support decision-making.

Think of it like being a detective. You have clues (data), you investigate patterns, and you solve mysteries (business questions).

**[SECTION 2: Real Example - 2 minutes]**

Let me show you a real example:

Imagine you work for a retail company. Sales are down 15% this month. Your boss asks: "Why?"

As a data analyst, you:
1. Gather data from sales systems
2. Clean and organize it
3. Analyze patterns by product, region, time
4. Discover that one product category is driving the decline
5. Investigate why - maybe a competitor launched a new product
6. Present findings with clear visualizations
7. Recommend actions - pricing strategy, marketing campaign

This is data analysis in action. Not just numbers - solving real business problems.

**[SECTION 3: Skills You'll Learn - 1 minute]**

In this pathway, you'll master:
- SQL to query databases
- Excel for quick analysis
- Python for automation and advanced analytics
- Tableau and Power BI for visualization
- Statistics and A/B testing
- Communication and storytelling with data

**[CLOSING - 30 seconds]**

By the end, you'll have a portfolio of real projects and be ready for your first data analyst role.

Let's get started! See you in the next video.

---

### Video 2: "Asking Great Business Questions" (7 minutes)

**[INTRO - 30 seconds]**

Welcome back! Today we're covering one of the most important skills for data analysts: asking great business questions.

The quality of your analysis depends entirely on asking the right questions first.

**[SECTION 1: Why Questions Matter - 1 minute]**

Here's a truth: You can have perfect SQL skills, beautiful dashboards, and sophisticated models... but if you're answering the wrong question, none of it matters.

Great data analysts don't just execute queries. They understand the business problem deeply and ask clarifying questions before diving into data.

**[SECTION 2: The 5W1H Framework - 2 minutes]**

Use this framework for every analysis:

**Who?** Who is impacted? Who are the stakeholders?
- Example: "Who are our highest-value customers?"

**What?** What exactly are we measuring?
- Example: "What defines a 'successful' customer?"

**When?** What time period matters?
- Example: "When did this trend start?"

**Where?** Which segment, region, or channel?
- Example: "Where is performance declining?"

**Why?** What's the root cause?
- Example: "Why are customers churning?"

**How?** How will this analysis drive decisions?
- Example: "How will we use these insights?"

**[SECTION 3: Example - Bad vs Good Questions - 2 minutes]**

Let's see this in practice:

**BAD REQUEST:**
"Can you analyze our sales data?"

This is too vague. What aspect? What time period? What decision will this inform?

**GOOD REQUEST:**
"Can you analyze why sales declined 15% in Q3 compared to Q2, specifically looking at:
- Which product categories were affected
- Whether this is consistent across regions
- If there were external factors (seasonality, competition)
- So we can decide whether to adjust pricing or increase marketing"

See the difference? The good request has clear scope, specific questions, and ties to a decision.

**[SECTION 4: Practice Exercise - 1 minute]**

Here's your exercise:

Your boss says: "We need more revenue."

What questions would you ask before starting any analysis?

Pause the video and write down 5 questions.

**[Pause]**

Here's what I'd ask:
1. What's our revenue goal and time frame?
2. Which revenue streams should we focus on?
3. Are we looking to acquire new customers or increase existing customer value?
4. What constraints do we have (budget, resources)?
5. What's worked or failed in the past?

**[CLOSING - 30 seconds]**

Remember: Slow down before you speed up. Invest time in understanding the question before touching any data.

In the next video, we'll cover data quality assessment.

See you there!

---

## Unit 3 Video Scripts

### Video 3: "SQL Fundamentals - SELECT and WHERE" (10 minutes)

**[INTRO - 30 seconds]**

Welcome to SQL fundamentals! SQL is THE most important skill for data analysts. Master this, and you'll unlock access to any database in any company.

Today: SELECT and WHERE - the building blocks of every SQL query.

**[SECTION 1: What is SQL? - 1 minute]**

SQL stands for Structured Query Language. It's how we talk to databases.

Think of a database as a library, tables as books, and SQL as asking the librarian specific questions:
- "Show me all customers from London"
- "What are our top-selling products?"
- "Calculate total revenue by month"

**[SECTION 2: SELECT Statement - 2 minutes]**

The SELECT statement retrieves data from a table.

Basic syntax:
```sql
SELECT column1, column2
FROM table_name;
```

Let's see examples:

```sql
-- Select specific columns
SELECT customer_name, email, city
FROM customers;

-- Select all columns
SELECT *
FROM customers;

-- Select with alias
SELECT 
    customer_name AS name,
    email AS contact_email
FROM customers;
```

**[SECTION 3: WHERE Clause - 3 minutes]**

WHERE filters rows based on conditions.

```sql
-- Single condition
SELECT *
FROM customers
WHERE city = 'London';

-- Multiple conditions with AND
SELECT *
FROM customers
WHERE city = 'London' 
  AND age > 25;

-- Multiple conditions with OR
SELECT *
FROM customers
WHERE city = 'London' 
   OR city = 'Manchester';

-- NOT condition
SELECT *
FROM customers
WHERE NOT city = 'London';
```

**Common operators:**
- = (equals)
- != or <> (not equals)
- >, <, >=, <= (comparisons)
- BETWEEN (range)
- IN (list of values)
- LIKE (pattern matching)

```sql
-- BETWEEN
SELECT *
FROM products
WHERE price BETWEEN 10 AND 50;

-- IN
SELECT *
FROM customers
WHERE city IN ('London', 'Paris', 'Berlin');

-- LIKE (% is wildcard)
SELECT *
FROM customers
WHERE email LIKE '%@gmail.com';
```

**[SECTION 4: Practice Exercise - 2 minutes]**

Let's practice! Pause and write queries for:

1. Get all products where category is 'Electronics'
2. Get customers who signed up in 2024
3. Get orders with value greater than £1000
4. Get products with 'Phone' in the name

**[Show solutions]**

```sql
-- 1
SELECT * FROM products WHERE category = 'Electronics';

-- 2
SELECT * FROM customers WHERE YEAR(signup_date) = 2024;

-- 3
SELECT * FROM orders WHERE order_value > 1000;

-- 4
SELECT * FROM products WHERE product_name LIKE '%Phone%';
```

**[SECTION 5: Best Practices - 1 minute]**

Tips for writing great SQL:
1. Always specify column names (avoid SELECT *)
2. Use meaningful aliases
3. Format for readability (line breaks, indentation)
4. Comment your code
5. Test with LIMIT first on large tables

**[CLOSING - 30 seconds]**

You now know the foundation of SQL! In the next video, we'll cover JOINs - how to combine data from multiple tables.

Practice these queries until they're second nature. See you next time!

---

### Video 4: "SQL JOINs Made Simple" (12 minutes)

**[INTRO - 30 seconds]**

JOINs are where SQL gets powerful. They let you combine data from multiple tables to answer complex questions.

Today, I'll make JOINs crystal clear with visual examples.

**[SECTION 1: Why JOINs? - 1 minute]**

In real databases, data is split across multiple tables:
- Customers table: customer info
- Orders table: order details
- Products table: product info

To answer "What products did each customer buy?", you need to JOIN these tables.

**[SECTION 2: INNER JOIN - 3 minutes]**

INNER JOIN returns only matching rows from both tables.

**[Show Venn diagram - overlapping circles]**

```sql
SELECT 
    customers.name,
    orders.order_date,
    orders.total_amount
FROM customers
INNER JOIN orders 
    ON customers.customer_id = orders.customer_id;
```

This returns only customers who have placed orders.

**Using aliases for cleaner code:**
```sql
SELECT 
    c.name,
    o.order_date,
    o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

**[SECTION 3: LEFT JOIN - 3 minutes]**

LEFT JOIN returns all rows from left table, plus matches from right.

**[Show Venn diagram - left circle fully shaded]**

```sql
SELECT 
    c.name,
    o.order_date,
    o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

This returns ALL customers, even those without orders (NULL in order columns).

**Use case:** Find customers who haven't ordered:
```sql
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**[SECTION 4: RIGHT JOIN and FULL JOIN - 1 minute]**

RIGHT JOIN: Opposite of LEFT (rarely used)
FULL OUTER JOIN: All rows from both tables (less common)

In practice, you can rewrite any RIGHT JOIN as a LEFT JOIN by swapping table order.

**[SECTION 5: Multiple JOINs - 2 minutes]**

Real queries often join 3+ tables:

```sql
SELECT 
    c.name,
    o.order_date,
    p.product_name,
    oi.quantity
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id;
```

This shows customer purchases with product details.

**[SECTION 6: Practice Exercise - 1.5 minutes]**

Pause and write:

1. Join customers and orders, show customer name and total order value
2. Find products that have never been ordered (LEFT JOIN with IS NULL)

**[Show solutions]**

**[CLOSING - 30 seconds]**

JOINs unlock the real power of SQL. Practice with different combinations until they feel natural.

Next video: Aggregations and GROUP BY!

---

## Unit 5 Video Scripts

### Video 5: "Pandas Basics - DataFrames" (10 minutes)

**[INTRO - 30 seconds]**

Welcome to Python with pandas! If SQL is essential, pandas is your superpower for data manipulation in Python.

Today: Understanding DataFrames - the core data structure you'll use daily.

**[SECTION 1: What is Pandas? - 1 minute]**

Pandas is a Python library for data analysis. It provides:
- DataFrames: spreadsheet-like data structures
- Powerful data manipulation tools
- Built-in visualization
- Integration with other tools

Think of pandas as Excel on steroids, with full programming power.

**[SECTION 2: Creating DataFrames - 2 minutes]**

**From dictionary:**
```python
import pandas as pd

data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['London', 'Paris', 'Berlin']
}

df = pd.DataFrame(data)
print(df)
```

**From CSV:**
```python
df = pd.read_csv('data.csv')
```

**From SQL:**
```python
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql_query("SELECT * FROM customers", conn)
```

**[SECTION 3: Exploring DataFrames - 3 minutes]**

Essential methods:

```python
# First 5 rows
df.head()

# Last 5 rows
df.tail()

# Shape (rows, columns)
df.shape

# Column names
df.columns

# Data types
df.dtypes

# Summary statistics
df.describe()

# Info about DataFrame
df.info()
```

**[SECTION 4: Selecting Data - 3 minutes]**

**Select column:**
```python
# Returns Series
df['name']

# Returns DataFrame
df[['name', 'age']]
```

**Select rows:**
```python
# By position (iloc)
df.iloc[0]        # First row
df.iloc[0:3]      # First 3 rows

# By condition
df[df['age'] > 25]
df[df['city'] == 'London']
```

**Select rows and columns:**
```python
# Using loc[rows, columns]
df.loc[df['age'] > 25, ['name', 'city']]
```

**[SECTION 5: Practice Exercise - 1 minute]**

Load this dataset and:
1. Show first 10 rows
2. Get summary statistics
3. Filter for customers from London
4. Select name and email columns

**[CLOSING - 30 seconds]**

You now understand DataFrames! This is your foundation. In the next video, we'll cover data cleaning and transformation.

Practice these operations until they're muscle memory!

---

## Unit 6 Video Scripts

### Video 6: "A/B Testing Fundamentals" (8 minutes)

**[INTRO - 30 seconds]**

A/B testing is how data-driven companies make decisions. Should we change our checkout button color? Test it. New pricing? Test it.

Today: How to design and analyze A/B tests.

**[SECTION 1: What is A/B Testing? - 1 minute]**

A/B testing compares two versions to see which performs better:
- Version A (Control): Current version
- Version B (Treatment): New version

You randomly split users 50/50 and measure a key metric (conversion rate, revenue, engagement).

**[SECTION 2: Hypothesis Framework - 2 minutes]**

Always start with clear hypotheses:

**Null Hypothesis (H0):** No difference between A and B
**Alternative Hypothesis (H1):** B is better than A

Example:
- H0: New checkout button has no effect on conversion rate
- H1: New checkout button increases conversion rate by 2%+

**[SECTION 3: Key Concepts - 3 minutes]**

**Statistical Significance (p-value):**
- p < 0.05 means results are statistically significant
- Less than 5% chance results are due to random chance

**Sample Size:**
- Need enough users to detect meaningful differences
- Larger effect size = smaller sample needed
- Use power analysis to calculate required sample size

**Duration:**
- Run long enough to account for weekly patterns
- Minimum 1-2 weeks typically
- Until you reach required sample size

**[SECTION 4: Analysis Example - 1.5 minutes]**

```python
# Calculate conversion rates
control_rate = control_conversions / control_visitors
treatment_rate = treatment_conversions / treatment_visitors

# Calculate lift
lift = (treatment_rate - control_rate) / control_rate

# Statistical test
from scipy.stats import chi2_contingency
contingency = [[control_conversions, control_visitors - control_conversions],
               [treatment_conversions, treatment_visitors - treatment_conversions]]
chi2, p_value, dof, expected = chi2_contingency(contingency)

print(f"Control: {control_rate:.2%}")
print(f"Treatment: {treatment_rate:.2%}")
print(f"Lift: {lift:.2%}")
print(f"P-value: {p_value:.4f}")
print(f"Significant: {p_value < 0.05}")
```

**[CLOSING - 30 seconds]**

A/B testing turns opinions into facts. Master this skill, and you'll be invaluable to any company.

Practice designing experiments for real business questions!

---

## Recording Tips for Instructors

### Technical Setup
- Use screen recording software (Camtasia, OBS)
- 1080p minimum resolution
- Clear audio with good microphone
- Remove background noise
- Use cursor highlighting for emphasis

### Presentation Style
- Speak clearly and at moderate pace
- Pause between sections
- Show enthusiasm and energy
- Use real examples and stories
- Encourage practice and pause points

### Visual Aids
- Use syntax highlighting for code
- Zoom in on important details
- Use annotations and arrows
- Include visual diagrams for concepts
- Show before/after examples

### Editing
- Remove long pauses and mistakes
- Add chapter markers
- Include captions for accessibility
- Add b-roll or examples
- Keep videos under 15 minutes each

---

"""
        )

        st.markdown("---")
        st.markdown("## 📚 DATA ANALYTICS GLOSSARY")
        st.markdown(
            """**Complete reference guide for all key terms and concepts**

---

## A

**A/B Testing**: Experimental method comparing two versions (A and B) to determine which performs better on a key metric.

**Aggregate Function**: SQL function that performs calculation on multiple rows and returns single value (SUM, AVG, COUNT, MIN, MAX).

**Algorithm**: Step-by-step procedure for solving a problem or completing a task.

**Analytics**: Systematic analysis of data to discover meaningful patterns and insights.

**API (Application Programming Interface)**: Set of protocols for building and integrating application software.

**Array Formula**: Excel formula that can perform multiple calculations on one or more items in an array.

**Attribution**: Process of assigning credit to touchpoints in a customer journey.

---

## B

**Baseline**: Reference point used for comparison in A/B testing or performance tracking.

**BI (Business Intelligence)**: Technologies and strategies for analyzing business data.

**Big Data**: Extremely large datasets that require specialized processing techniques.

**Binning**: Grouping continuous values into discrete categories or bins.

**Boolean Logic**: System using TRUE/FALSE values for logical operations (AND, OR, NOT).

**Business Logic**: Rules that define how business operations function.

---

## C

**Calculated Field**: Custom field created using formulas in BI tools or spreadsheets.

**Cardinality**: Number of unique values in a database column or relationship type between tables.

**Categorical Variable**: Variable with discrete categories (e.g., color, region, product type).

**Churn Rate**: Percentage of customers who stop using a service over time period.

**CLV (Customer Lifetime Value)**: Total revenue expected from customer over entire relationship.

**Cohort Analysis**: Grouping users by shared characteristics to track behavior over time.

**Continuous Variable**: Numeric variable that can take any value within a range (e.g., revenue, temperature).

**Conversion Rate**: Percentage of users who complete desired action.

**Correlation**: Statistical measure of relationship between two variables.

**CTE (Common Table Expression)**: Temporary named result set in SQL query.

---

## D

**DAX (Data Analysis Expressions)**: Formula language for Power BI and Excel Power Pivot.

**Dashboard**: Visual display of key metrics and KPIs on single screen.

**Data Cleaning**: Process of detecting and correcting corrupt or inaccurate data.

**Data Dictionary**: Centralized repository of information about data structure and definitions.

**Data Lake**: Storage repository holding vast amounts of raw data in native format.

**Data Mart**: Subset of data warehouse focused on specific business area.

**Data Mining**: Process of discovering patterns in large datasets.

**Data Pipeline**: Series of data processing steps from source to destination.

**Data Quality**: Measure of data's fitness for intended use (accuracy, completeness, consistency).

**Data Warehouse**: Central repository of integrated data from multiple sources.

**Data Wrangling**: Process of cleaning, structuring, and enriching raw data.

**Descriptive Analytics**: Analysis of historical data to understand what happened.

**Diagnostic Analytics**: Analysis to understand why something happened.

**Dimension**: Categorical attribute used to slice and analyze data (e.g., time, location, product).

**Distribution**: Pattern showing how values are spread across a dataset.

---

## E

**EDA (Exploratory Data Analysis)**: Initial data investigation to discover patterns and anomalies.

**ETL (Extract, Transform, Load)**: Process of extracting data from sources, transforming it, and loading into destination.

**Excel**: Spreadsheet software by Microsoft for data analysis and visualization.

---

## F

**Feature Engineering**: Creating new variables from existing data to improve analysis or models.

**Filter**: Condition limiting which data rows are included in analysis.

**Foreign Key**: Column referencing primary key in another table to establish relationship.

**Function**: Predefined formula performing specific calculation.

---

## G

**Granularity**: Level of detail in data (e.g., daily vs monthly).

**GROUP BY**: SQL clause grouping rows sharing property for aggregation.

**Guardrail Metric**: Metric monitored to ensure changes don't harm other aspects.

---

## H

**Having Clause**: SQL clause filtering grouped results after aggregation.

**Histogram**: Bar chart showing distribution of continuous variable.

**Hypothesis**: Testable prediction about relationship between variables.

---

## I

**Index**: Database structure improving query performance on specific columns.

**Inner Join**: SQL operation returning only matching rows from both tables.

**Insight**: Meaningful discovery from data analysis that informs decisions.

**Interactive Dashboard**: Dashboard allowing user filtering and drill-down.

---

## J

**Join**: SQL operation combining rows from multiple tables based on related column.

**JSON (JavaScript Object Notation)**: Lightweight data-interchange format.

---

## K

**Key**: Column uniquely identifying rows in database table.

**KPI (Key Performance Indicator)**: Measurable value demonstrating effectiveness toward key objectives.

---

## L

**Left Join**: SQL operation returning all rows from left table plus matches from right.

**LOD (Level of Detail)**: Tableau expression controlling aggregation granularity.

**Lookup Function**: Function finding values in table or range (VLOOKUP, INDEX/MATCH).

---

## M

**Measure**: Numeric value for calculation and analysis (e.g., revenue, quantity).

**Median**: Middle value when data sorted (50th percentile).

**Metadata**: Data providing information about other data.

**Metric**: Quantifiable measure tracking business performance.

**Missing Data**: Values absent from dataset (NULL, NaN, blank).

**Mode**: Most frequently occurring value in dataset.

---

## N

**Normalization**: Process of organizing data to reduce redundancy.

**North Star Metric**: Single metric best capturing core value delivered to customers.

**NULL**: Database value representing missing or undefined data.

---

## O

**OLAP (Online Analytical Processing)**: Computing approach for multidimensional data analysis.

**OLTP (Online Transaction Processing)**: Database systems supporting transaction-oriented applications.

**Outlier**: Data point significantly different from other observations.

---

## P

**Pandas**: Python library for data manipulation and analysis.

**Parameter**: Variable allowing dynamic input in analysis or query.

**Partition**: Division of table into segments for performance or organization.

**Percentile**: Value below which percentage of data falls.

**Pivot Table**: Data summarization tool rotating/aggregating data.

**Power BI**: Microsoft's business intelligence platform.

**Predictive Analytics**: Using data to forecast future outcomes.

**Prescriptive Analytics**: Analysis recommending actions to achieve desired outcomes.

**Primary Key**: Column uniquely identifying each row in table.

**Python**: Programming language popular for data analysis.

---

## Q

**Query**: Request for data from database.

**Query Optimization**: Improving query performance and efficiency.

---

## R

**R**: Programming language for statistical computing and graphics.

**Regression**: Statistical method for modeling relationship between variables.

**Relational Database**: Database organizing data into tables with relationships.

**ROI (Return on Investment)**: Measure of profitability calculated as gain/cost.

**Row-Level Security**: Restricting data access based on user characteristics.

---

## S

**Schema**: Structure defining organization of database.

**Segment**: Subset of data sharing common characteristics.

**SELECT**: SQL statement retrieving data from database.

**Self-Join**: Table joined with itself.

**SQL (Structured Query Language)**: Language for managing relational databases.

**Standard Deviation**: Measure of amount of variation in dataset.

**Statistical Significance**: Likelihood that result is not due to random chance.

**Subquery**: Query nested inside another query.

---

## T

**Tableau**: Data visualization software for business intelligence.

**Time Series**: Data points indexed in time order.

**Trend**: General direction data moves over time.

**Type I Error**: False positive (rejecting true null hypothesis).

**Type II Error**: False negative (failing to reject false null hypothesis).

---

## U

**Union**: SQL operation combining results from multiple queries.

**Unstructured Data**: Data without predefined format (text, images, video).

---

## V

**Variable**: Characteristic that can take different values.

**Variance**: Measure of data spread from mean.

**View**: Virtual table based on SQL query result.

**Visualization**: Graphical representation of data.

**VLOOKUP**: Excel function searching for value in table's first column.

---

## W

**WHERE**: SQL clause filtering rows before aggregation.

**Window Function**: SQL function performing calculation across set of rows related to current row.

---

## X

**XML (Extensible Markup Language)**: Markup language for encoding documents.

---

## Z

**Z-Score**: Number of standard deviations a value is from the mean.

---

"""
        )

        st.markdown("---")
        st.markdown("## 🛠️ TOOL INSTALLATION & SETUP GUIDES")
        st.markdown(
            """**Complete setup instructions for all required tools**

---

## SQL Database Setup

### Option 1: SQLite (Easiest for Learning)

**Windows:**
```bash
# Download SQLite from https://www.sqlite.org/download.html
# Extract sqlite-tools-win32-x86.zip
# Add to PATH or run from folder

# Test installation
sqlite3 --version
```

**Mac:**
```bash
# SQLite comes pre-installed
sqlite3 --version

# If needed, install via Homebrew
brew install sqlite3
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install sqlite3
sqlite3 --version
```

**Creating your first database:**
```bash
# Create database
sqlite3 practice.db

# Inside SQLite prompt
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    signup_date DATE
);

INSERT INTO customers VALUES (1, 'Alice', 'alice@email.com', '2024-01-15');

SELECT * FROM customers;

.exit
```

### Option 2: MySQL (Production-Ready)

**Windows:**
1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/
2. Run installer and select "MySQL Server"
3. Configure root password
4. Complete installation

**Mac:**
```bash
# Install via Homebrew
brew install mysql

# Start MySQL
brew services start mysql

# Secure installation
mysql_secure_installation
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

**Connecting:**
```bash
mysql -u root -p
# Enter password

# Create database
CREATE DATABASE analytics_practice;
USE analytics_practice;
```

### Option 3: PostgreSQL (Advanced)

**Windows:**
1. Download from https://www.postgresql.org/download/windows/
2. Run installer
3. Remember your password!

**Mac:**
```bash
brew install postgresql
brew services start postgresql

# Create database
createdb analytics_practice
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

## Python & Pandas Setup

### Step 1: Install Python

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. **CHECK "Add Python to PATH"**
4. Verify: `python --version`

**Mac:**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Verify
python3 --version
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip

# Verify
python3 --version
```

### Step 2: Install Pandas & Libraries

```bash
# Install pip packages
pip install pandas numpy matplotlib seaborn scipy jupyter

# Verify installation
python -c "import pandas; print(pandas.__version__)"
```

### Step 3: Set Up Jupyter Notebook

```bash
# Install Jupyter
pip install jupyter

# Start Jupyter
jupyter notebook

# Browser will open automatically
# Create new Python 3 notebook
```

### Step 4: First Pandas Script

```python
# Create file: first_analysis.py
import pandas as pd

# Create sample data
data = {
    'product': ['Laptop', 'Mouse', 'Keyboard'],
    'price': [1200, 25, 75],
    'quantity': [10, 50, 30]
}

df = pd.DataFrame(data)
print(df)

# Calculate total value
df['total_value'] = df['price'] * df['quantity']
print("\nWith totals:")
print(df)

# Save to CSV
df.to_csv('inventory.csv', index=False)
print("\nSaved to inventory.csv")
```

Run: `python first_analysis.py`

---

## Excel Setup

### Microsoft Excel

**Windows/Mac:**
1. Purchase Microsoft 365 subscription or standalone Excel
2. Download from https://www.microsoft.com/excel
3. Install and activate

**Free Alternative - LibreOffice Calc:**
1. Download from https://www.libreoffice.org/
2. Install LibreOffice suite
3. Open LibreOffice Calc (Excel alternative)

### Excel Features to Enable

**Windows:**
1. File → Options → Add-ins
2. Manage: Excel Add-ins → Go
3. Check: Analysis ToolPak, Solver
4. Click OK

**Mac:**
1. Tools → Excel Add-ins
2. Check: Analysis ToolPak
3. Click OK

### Testing Excel Setup

Create new workbook:
```
A1: Product    B1: Quantity    C1: Price    D1: Total
A2: Laptop     10              1200         =B2*C2
A3: Mouse      50              25           =B3*C3
A4: Keyboard   30              75           =B4*C4
A5: TOTAL      =SUM(B2:B4)                  =SUM(D2:D4)
```

Test pivot table:
1. Select data range
2. Insert → PivotTable
3. Drag fields to create summary

---

## Tableau Setup

### Tableau Public (Free)

**Download:**
1. Visit https://public.tableau.com/
2. Click "Download the App"
3. Enter email address
4. Download and install

**Windows:**
- Run TableauPublic.exe
- Follow installation wizard
- Launch Tableau Public

**Mac:**
- Open TableauPublic.dmg
- Drag to Applications
- Launch Tableau Public

### Tableau Desktop (Paid/Trial)

**Free 14-day trial:**
1. Visit https://www.tableau.com/products/trial
2. Enter details and download
3. Install Tableau Desktop
4. Activate trial license

### First Tableau Visualization

**Connect to data:**
1. Open Tableau
2. Connect → Text file
3. Select CSV file
4. Drag to canvas

**Create visualization:**
1. Drag dimension to Columns
2. Drag measure to Rows
3. Select chart type from Show Me
4. Add filters and colors
5. Save workbook

---

## Power BI Setup

### Power BI Desktop (Free)

**Windows Only:**
1. Visit https://powerbi.microsoft.com/desktop/
2. Click "Download Free"
3. Run installer
4. Sign in with Microsoft account

**Requirements:**
- Windows 10 or later
- Microsoft account (free)

### First Power BI Report

**Load data:**
1. Home → Get Data → Text/CSV
2. Select file → Load
3. Data appears in Fields pane

**Create visual:**
1. Click chart icon (bar, line, pie)
2. Drag fields to Axis and Values
3. Format using Format pane
4. Add filters and slicers

**Publish:**
1. File → Publish
2. Sign in to Power BI service
3. Select workspace
4. View online

---

## Git & GitHub Setup (For Portfolio)

### Install Git

**Windows:**
1. Download from https://git-scm.com/
2. Run installer (use defaults)
3. Verify: `git --version`

**Mac:**
```bash
# Install via Homebrew
brew install git

# Verify
git --version
```

**Linux:**
```bash
sudo apt-get install git
git --version
```

### Configure Git

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
git config --list
```

### Create GitHub Account

1. Visit https://github.com/
2. Sign up (free)
3. Verify email
4. Create profile

### First Repository

**On GitHub:**
1. Click "New Repository"
2. Name: "data-analyst-portfolio"
3. Add README
4. Create repository

**On your computer:**
```bash
# Clone repository
git clone https://github.com/yourusername/data-analyst-portfolio.git

# Navigate to folder
cd data-analyst-portfolio

# Add files
echo "# My Data Analyst Portfolio" > README.md

# Commit changes
git add .
git commit -m "Initial commit"
git push origin main
```

---

## VS Code Setup (Code Editor)

### Install VS Code

**All platforms:**
1. Download from https://code.visualstudio.com/
2. Install for your OS
3. Launch VS Code

### Essential Extensions

**Install these:**
1. Click Extensions icon (left sidebar)
2. Search and install:
   - Python (Microsoft)
   - Jupyter
   - SQL Tools
   - Excel Viewer
   - GitLens

### Configure for Python

1. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Type "Python: Select Interpreter"
3. Choose your Python installation
4. Create new .py file
5. Write code and run with F5

---

## Database Management Tools

### DBeaver (Free, Multi-Database)

**All platforms:**
1. Download from https://dbeaver.io/
2. Install for your OS
3. Launch DBeaver

**Connect to database:**
1. Database → New Database Connection
2. Select database type (MySQL, PostgreSQL, SQLite)
3. Enter credentials
4. Test connection → Finish

**Run queries:**
1. Right-click database → SQL Editor → New SQL Script
2. Write query
3. Execute (Ctrl+Enter)

### MySQL Workbench (MySQL)

**Download:**
1. Visit https://dev.mysql.com/downloads/workbench/
2. Download for your OS
3. Install

**Features:**
- Visual query builder
- Database design
- Server administration
- Query optimization

---

## Verification Checklist

### Test Your Setup:

**SQL:**
```sql
-- Can you run this query?
SELECT 'SQL is working!' AS test;
```

**Python:**
```python
# Can you run this script?
import pandas as pd
print("Python and pandas working!")
print(f"Pandas version: {pd.__version__}")
```

**Excel:**
- Can you create pivot table?
- Can you use VLOOKUP?
- Can you create chart?

**Tableau/Power BI:**
- Can you connect to CSV?
- Can you create bar chart?
- Can you add filter?

**Git:**
```bash
# Can you run these?
git --version
git config --list
```

### If you can do all of these, you're ready! ✅

---

## Troubleshooting Common Issues

### Python "command not found"
- **Solution:** Reinstall Python and check "Add to PATH"
- Or add Python directory to PATH manually

### pip install fails
- **Solution:** Update pip: `python -m pip install --upgrade pip`
- Try: `pip install --user package_name`

### Jupyter won't start
- **Solution:** `pip uninstall jupyter`, then `pip install jupyter`
- Check firewall settings

### Excel add-ins missing
- **Solution:** Repair Office installation
- Or enable add-ins manually in Options

### Tableau won't connect to file
- **Solution:** Check file permissions
- Copy file to Documents folder
- Use absolute file path

### Git authentication fails
- **Solution:** Use GitHub personal access token instead of password
- Settings → Developer settings → Personal access tokens

---

## Next Steps After Setup

1. **Verify all installations** using checklist above
2. **Create practice folder structure:**
   ```
   data-analytics/
   ├── sql-practice/
   ├── python-scripts/
   ├── excel-workbooks/
   ├── tableau-workbooks/
   ├── datasets/
   └── portfolio-projects/
   ```

3. **Download practice datasets:**
   - Kaggle.com
   - Data.gov
   - GitHub public datasets

4. **Create first project:**
   - Load data in each tool
   - Create simple analysis
   - Build visualization
   - Document in GitHub

5. **Start building portfolio!**

---

"""
        )


def render_data_analyst_pathway_module():
    learner_email = st.session_state.get("user_email", "")

    st.title("📊 Data Analyst Pathway")
    st.success(
        "Become a job-ready data analyst who can work across sectors and countries."
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
            """This pathway is designed for learners who want to become **practical
 data analysts**, even if they do not have an IT background.

By the end of this pathway you will be able to:

- Turn business questions into clear, measurable analysis tasks.
- Clean and explore data using spreadsheets and SQL.
- Build insightful BI-style dashboards and reports.
- Use Python as a power tool for heavier analysis.
- Design sensible metrics, run simple A/B tests and explain results.
- Complete an end-to-end analyst capstone suitable for your portfolio.
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
        st.info("Use this tab as the main reading and concept reference for each unit.")

        selected_unit = st.selectbox(
            "Select a unit:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="da_materials_unit",
        )

        _render_unit_learning_materials(selected_unit)

        st.markdown("---")
        if st.button("📥 Download unit theory summary as PDF", key="da_unit_pdf"):
            unit = UNITS[selected_unit]
            content_lines = [f"# Unit {selected_unit}: {unit['name']}", ""]
            content_lines.append("High-level notes for this Data Analyst unit.")
            content_lines.append("Refer to the in-app materials, labs and notebooks for full details.")
            markdown_content = "\n".join(content_lines)
            pdf_buffer = create_unit_pdf(
                selected_unit,
                unit["name"],
                markdown_content,
            )
            st.download_button(
                label="📥 Download Unit Summary PDF",
                data=pdf_buffer,
                file_name=f"Data_Analyst_Pathway_Unit_{selected_unit}.pdf",
                mime="application/pdf",
                key="da_unit_pdf_dl",
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

    # Labs & mini projects
    with tabs[2]:
        st.subheader("🧪 Labs & Mini Projects")
        st.info(
            "Each unit includes practical labs and mini projects. Tutors can adapt them to "
            "local datasets and sectors."
        )

        selected_unit = st.selectbox(
            "Choose a unit to view lab ideas:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="da_labs_unit",
        )

        st.markdown(f"### Unit {selected_unit}: {UNITS[selected_unit]['name']}")

        if selected_unit == 1:
            st.markdown("### 🎯 Unit 1 Labs: Business Questions & Requirements")
            
            st.markdown("---")
            st.markdown("## 📝 LAB 1: Rewriting Vague Requests into SMART Questions")
            st.markdown("**Duration:** 60-90 minutes | **Difficulty:** Beginner")
            
            with st.expander("🎯 Lab 1 - Click to expand full instructions"):
                st.markdown(
                    """
### Learning Objectives

By the end of this lab, you will be able to:
- Identify the problems with vague analytical requests
- Apply the SMART framework to refine questions
- Extract measurable metrics from business language
- Define appropriate timeframes and comparison periods
- Communicate refined questions back to stakeholders

---

### Prerequisites

- Understanding of SMART framework (Specific, Measurable, Actionable, Relevant, Time-bound)
- Basic business terminology
- No technical skills required yet

---

### Materials Needed

- Word processor or spreadsheet for documenting your work
- Access to the provided stakeholder scenarios (below)
- Reference: Unit 1 learning materials on requirements clarification

---

### Part 1: Analyzing Vague Requests (20 minutes)

**STEP 1:** Read each of the following stakeholder requests. For each one, identify:
- What's vague or unclear?
- What assumptions would you need to make?
- What questions would you ask to clarify?

**Scenario 1: Hospital Clinic Manager**
*"We're getting too many DNAs. Can you look into it?"*

**Scenario 2: E-commerce Marketing Director**
*"Our marketing campaigns aren't working. What's going on?"*

**Scenario 3: Retail Store Manager**
*"Sales are down. We need to know why."*

**Scenario 4: Call Center Manager**
*"We're too busy lately. Can you check the numbers?"*

**Scenario 5: SaaS Product Manager**
*"Customers are churning. Help!"*

**YOUR TASK:** Create a table like this for each scenario:

| Original Request | Problems Identified | Questions to Ask Stakeholder |
|------------------|---------------------|----------------------------|
| "We're getting too many DNAs" | - What's "too many"? No baseline<br>- Which clinics?<br>- Compared to when? | - What DNA rate would be acceptable?<br>- Is this for all clinics or specific specialties?<br>- Compared to last month, last year, or another benchmark? |

**STEP 2:** Compare your analysis with the example below.

**Example Analysis - Scenario 1:**

| Problem Type | Details |
|--------------|---------|
| **No baseline** | "Too many" compared to what? Need historical rate or target |
| **No scope** | All clinics? Specific specialty? Inpatient vs outpatient? |
| **No timeframe** | Last week? Last month? Last year? |
| **No metric** | Count of DNAs? % DNA rate? Cost impact? |
| **No causality** | Asking "why" but haven't established "what" and "how much" first |

---

### Part 2: Applying SMART Framework (30 minutes)

**STEP 3:** For each of the 5 scenarios, rewrite the request using the SMART framework.

**Template to use:**

```
ORIGINAL: [vague request]

REFINED QUESTION:
[Specific metric] for [specific scope] during [timeframe] 
compared to [baseline], broken down by [relevant segments]

SMART CHECK:
✓ Specific: [what exactly are we measuring]
✓ Measurable: [how will we quantify it]
✓ Actionable: [what decision will this inform]
✓ Relevant: [why does this matter to business goals]
✓ Time-bound: [what period and comparison]
```

**STEP 4:** Here's an example for Scenario 1. Use this as your template:

**ORIGINAL:** "We're getting too many DNAs. Can you look into it?"

**REFINED QUESTION:**
"What is the DNA rate (% of scheduled appointments that result in Did Not Attend) 
for Outpatient clinics in Q4 2024 compared to Q4 2023, broken down by specialty 
and appointment type (first appointment vs follow-up)?"

**SMART CHECK:**
✓ **Specific:** DNA rate for Outpatient clinics, segmented by specialty and appointment type
✓ **Measurable:** Percentage calculation: (DNAs / Total Scheduled) × 100
✓ **Actionable:** Will help identify which specialties/appointment types need intervention
✓ **Relevant:** DNAs waste capacity and increase waiting lists (key trust priority)
✓ **Time-bound:** Q4 2024 vs Q4 2023 (year-over-year comparison)

**Additional follow-up questions to consider:**
- What's the financial impact? (revenue lost per DNA)
- Are there patterns by day of week or time of day?
- What's our SMS reminder strategy?

---

**STEP 5:** Now refine the remaining 4 scenarios yourself.

**Scenario 2 Example Solution (try yours first before looking!):**

<details>
<summary>Click to reveal example answer</summary>

**REFINED QUESTION:**
"What is the email campaign conversion rate (% of recipients who clicked through 
AND made a purchase) for each of our 3 main customer segments (New, Returning, VIP) 
in November 2024 compared to November 2023, broken down by campaign type 
(promotional vs educational)?"

**SMART CHECK:**
✓ **Specific:** Email conversion rate by segment and campaign type
✓ **Measurable:** (Purchases from email / Email recipients) × 100
✓ **Actionable:** Will identify which segments/campaigns are underperforming
✓ **Relevant:** Email is primary customer acquisition channel
✓ **Time-bound:** November 2024 vs November 2023

</details>

---

### Part 3: Stakeholder Communication (20 minutes)

**STEP 6:** For Scenario 1 (DNAs), write an email response to the stakeholder presenting your refined question.

**Your email should include:**
1. Acknowledgment of their concern
2. Your refined, specific question
3. The metrics you'll calculate
4. The timeframe for delivering results
5. A request for confirmation that this addresses their need

**Example Email Template:**

```
Subject: Re: DNA analysis request - Confirming scope

Hi [Manager Name],

Thanks for raising the DNA concern. Before I dive into the data, I want to 
make sure I'm analyzing the right thing.

Based on our conversation, I understand you're concerned about DNA rates 
affecting clinic capacity. Here's what I propose to analyze:

**QUESTION:** What is the DNA rate (% DNAs / scheduled appointments) for 
Outpatient clinics in Q4 2024 vs Q4 2023, broken down by:
- Specialty (Dermatology, Cardiology, etc.)
- Appointment type (New vs Follow-up)

**METRICS I'll CALCULATE:**
- Overall DNA rate and trend
- DNA rate by specialty (top 10)
- DNA rate by appointment type
- Estimated appointment slots lost due to DNAs
- Day-of-week patterns (if helpful)

**DELIVERABLE:** A 1-page summary with charts showing where DNAs are 
highest, plus recommendations for which clinics to prioritize.

**TIMELINE:** I can have initial findings by [date].

**QUESTION FOR YOU:** Does this address what you need? Any other dimensions 
you'd like me to include (e.g., patient age groups, referral source)?

Let me know if I should proceed with this scope.

Thanks,
[Your Name]
```

**STEP 7:** Write similar emails for scenarios 2 and 3.

---

### Part 4: Identifying Data Gaps (15 minutes)

**STEP 8:** For each refined question, list what data you would need and potential issues.

**Template:**

| Data Required | Likely Source | Potential Issues |
|---------------|---------------|------------------|
| Appointment scheduling data | Scheduling system DB | May not capture patient-initiated cancellations vs true DNAs |
| Patient demographics | Patient admin system | May have data quality issues (missing postcodes, etc.) |

**STEP 9:** Complete this for Scenario 1 (DNAs).

**Example:**

| Data Required | Likely Source | Potential Issues |
|---------------|---------------|------------------|
| Scheduled appointments | Scheduling DB: appointments table | - Need to filter out cancelled appointments<br>- Distinguish between cancellations and DNAs |
| Appointment outcomes | Scheduling DB: status field | - Check if DNA is reliably recorded<br>- May have multiple codes (DNA, cancelled late, etc.) |
| Clinic/specialty | Reference data: clinics table | - Should be clean |
| Appointment type | Scheduling DB: appointment_type field | - May need to join to appointment_type_lookup table |
| Historical data | Same as above | - Need at least 2 years for YoY comparison<br>- Check if system changed in that period |

---

### Success Criteria

You've successfully completed this lab when you can:

- [ ] Identify at least 3 problems in each vague request
- [ ] Refine each request into a SMART question
- [ ] List specific metrics, timeframes, and segments
- [ ] Write a professional stakeholder confirmation email
- [ ] Identify potential data sources and quality issues
- [ ] Explain why your refined question is better than the original

---

### Common Mistakes to Avoid

❌ **Being too technical too soon**
"We need to run a regression analysis on DNA predictors"
→ Stakeholder doesn't care about methods, they care about answers

❌ **Not defining comparison periods**
"What's the DNA rate?" (compared to what?)
→ Always include a baseline or target

❌ **Forgetting to segment**
"Overall sales are down" (for all products? all regions?)
→ Aggregated numbers hide important patterns

❌ **Making assumptions**
"I'll assume you mean all clinics"
→ Always confirm scope with stakeholder

✅ **INSTEAD:** Ask clarifying questions, confirm scope, be specific

---

### Extension Challenges (Optional)

If you finish early or want extra practice:

1. **Challenge 1:** Find 3 real vague analytical requests from online forums 
   (Reddit, Twitter, LinkedIn) and refine them

2. **Challenge 2:** Create a "requirements clarification template" you could 
   use for future stakeholder meetings

3. **Challenge 3:** Role-play with a classmate: one person gives vague 
   requests, other person asks clarifying questions

---

### Deliverable

Submit a document containing:
1. Your refined SMART questions for all 5 scenarios
2. Your stakeholder confirmation email for scenario 1
3. Data requirements table for scenario 1
4. Reflection: What did you learn? What was challenging?

**Expected length:** 3-5 pages

---

### Assessment Rubric

| Criteria | Excellent (90-100%) | Good (70-89%) | Needs Improvement (<70%) |
|----------|---------------------|---------------|-------------------------|
| **SMART Questions** | All questions specific, measurable, with clear timeframes and segments | Most questions well-defined, minor ambiguity | Questions still vague or missing key elements |
| **Stakeholder Communication** | Professional email, confirms scope, requests feedback | Email adequate but may miss some elements | Email too technical or doesn't confirm scope |
| **Data Identification** | Correctly identifies sources and potential issues | Identifies most sources, may miss some issues | Unclear about data needs |
| **Business Understanding** | Shows strong understanding of business context | Adequate business awareness | Lacks business perspective |

---

**TIME TO COMPLETE:** Approximately 90 minutes

**NEXT:** Once you've completed Lab 1, move on to Lab 2 (Mapping questions to data sources)
"""
                )
            
            st.markdown("---")
            st.markdown("## 📝 LAB 2: Mapping Questions to Data Sources")
            st.markdown("**Duration:** 90 minutes | **Difficulty:** Intermediate")
            
            with st.expander("🎯 Lab 2 - Click to expand full instructions"):
                st.markdown(
                    """
### Learning Objectives

By the end of this lab, you will be able to:
- Trace business questions to the specific data sources that can answer them
- Identify primary keys, foreign keys, and join relationships between tables
- Assess data quality issues and plan cleaning strategies
- Document a complete data source inventory for analysis projects
- Create a data lineage diagram showing how data flows from sources to insights

---

### Prerequisites

**Before starting this lab, you should have:**
- ✅ Completed Lab 1 (SMART Questions)
- ✅ Basic understanding of databases and tables
- ✅ Familiarity with joins (covered in Unit 3 theory)

---

### Materials Needed

- Spreadsheet software (Excel or Google Sheets)
- Lab 2 data dictionary (provided below)
- Drawing tool for diagrams (PowerPoint, Lucidchart, or paper/pen)

---

### Scenario: Hospital Appointment System Analysis

**Context:**

You're a Data Analyst at Westside Hospital. The Head of Operations has asked you to analyze 
appointment DNA (Did Not Attend) rates. In Lab 1, you refined this into SMART questions. 
Now you need to identify WHERE the data lives and HOW to access it.

**Your Lab 1 Output (refined questions):**
1. What is the DNA rate by specialty for appointments scheduled in the last 6 months?
2. How does DNA rate differ between new patient vs follow-up appointments?
3. Which day of week has the highest DNA rate?
4. What percentage of DNA appointments had reminder calls sent?

**Your Task:** Map each question to specific data sources and design the data retrieval strategy.

---

### Part 1: Understanding the Data Landscape (20 minutes)

#### Step 1.1: Review the Data Dictionary

**Hospital has 4 main systems:**

**SYSTEM 1: Appointments Database (AppointmentDB)**
- **Table:** `appointments`
- **Description:** All scheduled appointments
- **Key fields:**
  - `appointment_id` (Primary Key)
  - `patient_id` (Foreign Key → patients table)
  - `clinic_id` (Foreign Key → clinics table)
  - `appointment_date`
  - `appointment_type` (NEW or FOLLOW_UP)
  - `status` (ATTENDED, DNA, CANCELLED)
  - `reminder_sent` (YES or NO)
  - `created_timestamp`

**SYSTEM 2: Patient Records System (PatientDB)**
- **Table:** `patients`
- **Description:** Patient demographics
- **Key fields:**
  - `patient_id` (Primary Key)
  - `patient_name`
  - `date_of_birth`
  - `postcode`
  - `phone_number`
  - `email`
  - `registration_date`

**SYSTEM 3: Clinic Management System (ClinicDB)**
- **Table:** `clinics`
- **Description:** Clinic and specialty information
- **Key fields:**
  - `clinic_id` (Primary Key)
  - `clinic_name`
  - `specialty` (Dermatology, Cardiology, etc.)
  - `building`
  - `floor`

**SYSTEM 4: Communication Log (CommsSystem)**
- **Table:** `reminder_logs`
- **Description:** Record of all reminder communications
- **Key fields:**
  - `reminder_id` (Primary Key)
  - `appointment_id` (Foreign Key → appointments table)
  - `reminder_date`
  - `reminder_method` (SMS, PHONE, EMAIL)
  - `delivery_status` (SENT, FAILED, BOUNCED)

---

#### Step 1.2: Create Your Data Source Inventory

**TASK:** Complete this table for each system

| System Name | Access Method | Update Frequency | Owner/Contact | Known Issues |
|-------------|---------------|------------------|---------------|--------------|
| AppointmentDB | SQL (read-only) | Real-time | IT Team (ext 5555) | None known |
| PatientDB | ? | ? | ? | ? |
| ClinicDB | ? | ? | ? | ? |
| CommsSystem | ? | ? | ? | ? |

**Fill in the "?" based on realistic assumptions.**

**Example Answer for PatientDB:**
- Access Method: SQL (read-only)
- Update Frequency: Daily (batch update at 2am)
- Owner/Contact: Data Governance Team (ext 4444)
- Known Issues: Historic records before 2020 may have missing postcodes

---

### Part 2: Mapping Questions to Tables (25 minutes)

#### Step 2.1: Question-to-Table Mapping

**TASK:** For each refined question, identify which tables are needed.

**QUESTION 1:** *"What is the DNA rate by specialty for appointments scheduled in the last 6 months?"*

**Tables Needed:**
- `appointments` (for: status, appointment_date)
- `clinics` (for: specialty)

**Join Logic:**
```sql
FROM appointments a
JOIN clinics c ON a.clinic_id = c.clinic_id
WHERE a.status = 'DNA'
  AND a.appointment_date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
```

**Calculation:**
```
DNA Rate = (COUNT appointments WHERE status='DNA') / (COUNT all appointments) × 100
Group by: specialty
```

---

**YOUR TURN:** Complete for Questions 2-4

**QUESTION 2:** *"How does DNA rate differ between new patient vs follow-up appointments?"*

**Tables Needed:**
- _______________
- _______________

**Join Logic:**
```sql
FROM _______________ 
WHERE _______________
```

**Calculation:**
```
DNA Rate = _______________
Group by: _______________
```

---

**QUESTION 3:** *"Which day of week has the highest DNA rate?"*

**Tables Needed:**
- _______________

**Join Logic:**
```sql
FROM _______________ 
WHERE _______________
```

**Calculation:**
```
DNA Rate = _______________
Group by: _______________
```

**HINT:** Use `DAYOFWEEK(appointment_date)` to extract day

---

**QUESTION 4:** *"What percentage of DNA appointments had reminder calls sent?"*

**Tables Needed:**
- _______________
- _______________

**Join Logic:**
```sql
FROM _______________ 
LEFT JOIN _______________ ON _______________
WHERE _______________
```

**Calculation:**
```
Reminder Rate = _______________
```

---

#### Step 2.2: Identify Join Keys

**TASK:** Document the relationships between tables

**Example:**

```
appointments.clinic_id = clinics.clinic_id
(Many appointments → One clinic)
```

**YOUR TURN:** Complete these relationships

```
appointments.patient_id = patients._______________
(_____ appointments → _____ patient)

appointments._______________ = reminder_logs._______________
(_____ appointment → _____ reminder logs)
```

---

### Part 3: Data Quality Assessment (20 minutes)

#### Step 3.1: Identify Potential Data Issues

**TASK:** For each table, list potential data quality issues

**Example for `appointments` table:**

| Potential Issue | Impact | How to Check | Mitigation Strategy |
|----------------|---------|--------------|---------------------|
| Duplicate appointment_ids | Inflates counts | `SELECT appointment_id, COUNT(*) FROM appointments GROUP BY appointment_id HAVING COUNT(*) > 1` | Remove duplicates, keep earliest |
| Missing clinic_id | Can't group by specialty | `SELECT COUNT(*) FROM appointments WHERE clinic_id IS NULL` | Exclude or flag |
| Status values inconsistent (DNA vs Did Not Attend) | Wrong filtering | `SELECT DISTINCT status FROM appointments` | Standardize before analysis |

---

**YOUR TURN:** Complete for `patients` table

| Potential Issue | Impact | How to Check | Mitigation Strategy |
|----------------|---------|--------------|---------------------|
| Missing phone/email | Can't contact | ? | ? |
| Duplicate patient records | ? | ? | ? |
| Date of birth in future | ? | ? | ? |

---

#### Step 3.2: Plan Data Cleaning Steps

**TASK:** List the cleaning steps you'll perform BEFORE analysis

**Cleaning Checklist:**

- [ ] Remove cancelled appointments (status = 'CANCELLED')
- [ ] Remove test/training appointments (patient_name LIKE 'TEST%')
- [ ] Standardize status values (DNA vs Did Not Attend → 'DNA')
- [ ] _______________
- [ ] _______________
- [ ] _______________

**Add 3 more cleaning steps based on your data quality assessment**

---

### Part 4: Create Data Lineage Diagram (25 minutes)

#### Step 4.1: Draw the Data Flow

**TASK:** Create a visual diagram showing how data flows from sources to final analysis

**Your diagram should show:**
1. Source systems (rectangles)
2. Tables (rounded rectangles)
3. Join relationships (arrows with labels)
4. Final output (highlighted box)

**Example Structure:**

```
[AppointmentDB System]
    └── appointments table
            ├── appointment_id (PK)
            ├── clinic_id (FK) ────────┐
            ├── patient_id (FK) ───┐   │
            ├── status             │   │
            └── appointment_date   │   │
                                  │   │
[PatientDB System]                │   │
    └── patients table            │   │
            ├── patient_id (PK) ◄──┘   │
            └── patient_name           │
                                      │
[ClinicDB System]                     │
    └── clinics table                 │
            ├── clinic_id (PK) ◄───────┘
            └── specialty

                    ↓
                    
[ANALYSIS OUTPUT]
- DNA Rate by Specialty
- DNA Rate by Appointment Type
- DNA Rate by Day of Week
- Reminder Coverage Analysis
```

**Tools you can use:**
- PowerPoint (shapes + connectors)
- Lucidchart or draw.io (online diagramming)
- Paper and pen (take photo)

---

### Part 5: Document Your Data Access Plan (10 minutes)

#### Step 5.1: Write the Data Retrieval Strategy

**TASK:** Document HOW you'll get the data

**Template:**

**DATA ACCESS PLAN**

**Date:** _______________  
**Analyst:** _______________  
**Project:** Hospital DNA Rate Analysis

**Step 1: Request Access**
- [ ] Request read-only SQL access to AppointmentDB, PatientDB, ClinicDB
- [ ] Contact: IT Team (ext 5555)
- [ ] Expected turnaround: 2 business days

**Step 2: Extract Data**
```sql
-- Main query combining all needed tables
SELECT 
    a.appointment_id,
    a.appointment_date,
    a.appointment_type,
    a.status,
    c.specialty,
    DAYOFWEEK(a.appointment_date) as day_of_week,
    CASE WHEN r.reminder_id IS NOT NULL THEN 'YES' ELSE 'NO' END as reminder_sent
FROM appointments a
JOIN clinics c ON a.clinic_id = c.clinic_id
LEFT JOIN reminder_logs r ON a.appointment_id = r.appointment_id
WHERE a.appointment_date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
  AND a.status IN ('ATTENDED', 'DNA');
```

**Step 3: Save and Clean**
- [ ] Export to CSV: `appointments_6months.csv`
- [ ] Apply cleaning steps (see Part 3.2)
- [ ] Save cleaned version: `appointments_6months_clean.csv`

**Step 4: Validate**
- [ ] Row count check (expect ~20,000-30,000 appointments)
- [ ] Date range check (min date ~6 months ago, max date ~today)
- [ ] No nulls in critical fields (status, specialty, appointment_date)

---

### Success Criteria

**You've successfully completed Lab 2 if you can:**

✅ **Mapping Accuracy**
- All 4 questions correctly mapped to required tables
- Join relationships identified (patient_id, clinic_id, appointment_id)
- Primary keys and foreign keys documented

✅ **Data Quality Awareness**
- At least 5 potential data quality issues identified
- Mitigation strategy for each issue
- Cleaning checklist with 6+ steps

✅ **Visual Communication**
- Data lineage diagram created
- Shows relationships between 3+ tables
- Clear flow from sources to analysis output

✅ **Documentation Quality**
- Data access plan is complete and actionable
- SQL query is syntactically correct
- Validation steps included

---

### Common Mistakes to Avoid

❌ **Missing Required Joins**
- Forgetting that `appointments` alone doesn't have specialty (need `clinics` table)
- Not recognizing when LEFT JOIN vs INNER JOIN matters

❌ **Unclear Join Logic**
- Writing "join tables" without specifying ON condition
- Joining on non-key fields

❌ **Ignoring Data Quality**
- Assuming data is perfect
- Not checking for duplicates, nulls, or inconsistencies

❌ **Incomplete Documentation**
- Missing the "how to check" column in data quality assessment
- Vague mitigation strategies ("fix it")

---

### Extension Challenges (Optional)

Want to go deeper? Try these:

**CHALLENGE 1: Handle Missing Reminders**
- What if `reminder_logs` doesn't have records for some appointments?
- Is that because no reminder was sent, or because the log is incomplete?
- How would you distinguish these cases?

**CHALLENGE 2: Time Zone Issues**
- `appointment_date` is stored in UTC
- Clinics operate in GMT (UK time)
- How do you ensure "day of week" is calculated in clinic's local time?

**CHALLENGE 3: Slow Query Optimization**
- Your query takes 5 minutes to run on 2 years of data
- How would you optimize it? (Hint: indexes, date filtering, reducing joins)

---

### Deliverables

**Submit the following:**

1. **Completed Question-to-Table Mapping** (Part 2)
   - All 4 questions mapped
   - Tables, joins, and calculations documented

2. **Data Quality Assessment** (Part 3)
   - Issue identification table for `appointments` and `patients`
   - Cleaning checklist with 6+ steps

3. **Data Lineage Diagram** (Part 4)
   - Visual showing relationships
   - Can be hand-drawn or digital

4. **Data Access Plan** (Part 5)
   - Complete document with SQL query
   - Validation steps included

---

### Assessment Rubric

| Criteria | Excellent (A) | Good (B) | Needs Improvement (C) |
|----------|---------------|----------|----------------------|
| **Question Mapping** | All 4 questions correctly mapped to exact tables needed, joins clearly specified | 3-4 questions mapped, minor errors in join logic | <3 questions mapped or major errors |
| **Join Relationships** | All PKs/FKs correctly identified, join types (INNER/LEFT) appropriate | Most relationships correct, minor confusion on join types | Significant gaps in understanding joins |
| **Data Quality** | 5+ issues identified with realistic checks and mitigation | 3-4 issues identified with some strategies | <3 issues or vague mitigations |
| **Data Lineage Diagram** | Clear visual with 3+ tables, relationships labeled, professional | Shows main tables and relationships, adequate | Confusing or incomplete |
| **Documentation** | Data access plan is production-ready, SQL is correct and executable | Plan is complete but minor syntax errors | Incomplete or non-actionable |
| **Critical Thinking** | Identifies non-obvious issues (timezones, missing data interpretation) | Solid understanding, catches main issues | Surface-level only |

**Target:** Achieve "Excellent" or "Good" on all criteria

---

**TIME TO COMPLETE:** Approximately 90 minutes

**NEXT:** After completing Lab 2, proceed to the Unit 1 Mini Project (Question-to-Metric Map)

---

### Example Answer Key (Use After Attempting)

<details>
<summary><b>Click to reveal answers (only after attempting yourself!)</b></summary>

**Question 2 Mapping:**
- Tables: `appointments`
- Join: None needed (appointment_type is in appointments table)
- Calculation: DNA Rate = COUNT(WHERE status='DNA') / COUNT(*) × 100, GROUP BY appointment_type

**Question 3 Mapping:**
- Tables: `appointments`
- Join: None needed
- Calculation: DNA Rate = COUNT(WHERE status='DNA') / COUNT(*) × 100, GROUP BY DAYOFWEEK(appointment_date)

**Question 4 Mapping:**
- Tables: `appointments`, `reminder_logs`
- Join: LEFT JOIN reminder_logs ON appointments.appointment_id = reminder_logs.appointment_id
- Calculation: Reminder Rate = COUNT(WHERE reminder_id IS NOT NULL) / COUNT(*) × 100, WHERE status='DNA'

**Join Keys:**
- `appointments.patient_id = patients.patient_id` (Many-to-One)
- `appointments.appointment_id = reminder_logs.appointment_id` (One-to-Many)

**Data Quality Issues for `patients`:**
- Missing phone/email → Can't send reminders → Check with `WHERE phone IS NULL OR email IS NULL` → Flag for manual review
- Duplicate patient records → Inflates patient count → Check with `GROUP BY patient_name, date_of_birth HAVING COUNT(*) > 1` → Merge duplicates
- Future DOB → Invalid data → Check with `WHERE date_of_birth > CURRENT_DATE` → Exclude or correct

</details>
"""
                )
            
            st.markdown("---")
            st.markdown("## 📝 MINI PROJECT: Question-to-Metric Map")
            st.markdown("**Duration:** 2-3 hours | **Difficulty:** Intermediate")
            
            with st.expander("🎯 Mini Project - Click to expand full instructions"):
                st.markdown(
                    """
### Project Overview

**This is your Unit 1 capstone** - a one-page analytical framework document that bridges business questions to data sources.

This document is what you'd create BEFORE starting any analysis project. It ensures alignment with stakeholders, 
clarifies data requirements, and serves as your project roadmap.

**This is a REAL analyst deliverable** that you'd present to your manager for sign-off before proceeding with analysis.

---

### Learning Objectives

By completing this project, you will:
- Synthesize skills from Labs 1 and 2 (SMART questions + data source mapping)
- Create a professional analytical framework document
- Practice stakeholder communication (writing for business audience)
- Build a portfolio piece showcasing your analytical planning skills

---

### Project Requirements

**Your task:** Create a **Question-to-Metric Map** document for a business domain of your choice.

**Choose ONE domain:**
1. Healthcare (hospital operations, GP practice, pharmacy)
2. Retail (physical store, e-commerce, inventory management)
3. SaaS (subscription platform, user engagement, churn)
4. Financial Services (banking, insurance, lending)
5. Other (with similar complexity)

**Deliverable:** One-page professional document (PDF or polished Word/Google Doc)

---

### Document Template

Use this structure for your Question-to-Metric Map:

---

**QUESTION-TO-METRIC MAP**

**Project:** [Your chosen domain - e.g., "Retail Store Performance Analysis"]  
**Prepared by:** [Your name]  
**Date:** [Current date]  
**Stakeholders:** [Who will use this analysis - e.g., "Store Manager, Regional Manager"]

---

**BUSINESS OBJECTIVE**

[2-3 sentences describing the business goal]

*Example: "Improve store profitability by identifying underperforming product categories 
and optimizing inventory levels. Current gross margin is 35%; target is 40% within 6 months."*

---

**KEY QUESTIONS & METRICS**

| # | Business Question (SMART) | Metric Definition | Data Source | Calculation Logic | Refresh Frequency |
|---|---------------------------|-------------------|-------------|-------------------|-------------------|
| 1 | What is the gross margin by product category for the last quarter? | Gross Margin % | Sales System, Inventory System | (Revenue - Cost) / Revenue × 100, GROUP BY category | Weekly |
| 2 | [Your question] | [Your metric] | [Your source] | [Your calc] | [Your frequency] |
| 3 | [Your question] | [Your metric] | [Your source] | [Your calc] | [Your frequency] |
| 4 | [Your question] | [Your metric] | [Your source] | [Your calc] | [Your frequency] |
| 5 | [Your question] | [Your metric] | [Your source] | [Your calc] | [Your frequency] |

**Include 5-7 questions minimum**

---

**DATA SOURCE INVENTORY**

| System/Database | Tables Used | Join Keys | Update Frequency | Known Limitations |
|-----------------|-------------|-----------|------------------|-------------------|
| Sales System | sales_transactions, products | product_id | Real-time | Returns not always logged |
| Inventory System | inventory_levels, suppliers | product_id, supplier_id | Daily (2am) | Manual counts lag by 1 day |
| [Your system] | [Tables] | [Keys] | [Frequency] | [Limitations] |

**Include 3-5 data sources**

---

**DATA QUALITY CHECKS**

Before analysis, validate:
- [ ] No duplicate transaction IDs
- [ ] All products have cost data (required for margin calculation)
- [ ] Date range is complete (no missing days)
- [ ] Currency is consistent (all GBP)
- [ ] [Add 2-3 more specific to your domain]

---

**EXPECTED DELIVERABLES**

**Timeline:** 2 weeks from approval

**Week 1:**
- Data extraction and cleaning
- Initial analysis

**Week 2:**
- Dashboard creation
- Presentation to stakeholders

**Final Outputs:**
1. Excel dashboard with 5-7 key metrics
2. 10-slide PowerPoint presentation
3. One-page executive summary

---

**ASSUMPTIONS & DEPENDENCIES**

**Assumptions:**
- Historic data is accurate and complete
- [Add 1-2 more]

**Dependencies:**
- SQL read access to Sales and Inventory systems (requires IT approval - 2 days)
- [Add 1-2 more]

---

**APPROVAL**

Stakeholder Sign-Off: ____________________________ Date: __________

---

### Your Task Breakdown

**STEP 1: Choose Your Domain** (15 minutes)
- Pick a business area you understand or want to learn
- Research typical metrics for that domain if needed

**STEP 2: Define Business Objective** (15 minutes)
- What's the high-level goal?
- Why does this analysis matter?
- What decision will it inform?

**STEP 3: Create 5-7 SMART Questions** (30 minutes)
- Use Lab 1 skills to refine questions
- Ensure they're Specific, Measurable, Achievable, Relevant, Time-bound
- Mix different types (trends, comparisons, breakdowns)

**STEP 4: Map to Data Sources** (45 minutes)
- Use Lab 2 skills to identify tables
- Document join keys
- Define calculation logic
- Note data limitations

**STEP 5: Add Quality Checks** (15 minutes)
- What could go wrong with this data?
- How will you validate before analysis?

**STEP 6: Polish Document** (30 minutes)
- Format professionally
- Proofread for typos
- Ensure tables are aligned
- Export to PDF

---

### Example: Retail Store Analysis

**Here's a complete example to guide you:**

**Project:** Multi-Store Retail Performance Analysis  
**Stakeholder:** Regional Manager  
**Objective:** Identify top and bottom performing stores to inform resource allocation

**Key Questions:**

1. **Which 5 stores had highest revenue in Q4 2024?**
   - Metric: Total Revenue (£)
   - Source: sales_transactions table
   - Calculation: SUM(transaction_amount) WHERE transaction_date BETWEEN '2024-10-01' AND '2024-12-31', GROUP BY store_id
   - Frequency: Monthly

2. **What is the average transaction value by store?**
   - Metric: Average Transaction Value (£)
   - Source: sales_transactions table
   - Calculation: AVG(transaction_amount), GROUP BY store_id
   - Frequency: Weekly

3. **How does footfall correlate with revenue across stores?**
   - Metric: Revenue per Visitor (£)
   - Source: sales_transactions + footfall_sensors tables
   - Calculation: SUM(revenue) / SUM(visitor_count) per store
   - Frequency: Weekly

4. **Which product categories drive the most profit margin by store?**
   - Metric: Gross Margin % by Category
   - Source: sales_transactions + product_costs tables
   - Calculation: (Revenue - Cost) / Revenue × 100, GROUP BY store_id, product_category
   - Frequency: Monthly

5. **What is staff productivity (revenue per employee hour) by store?**
   - Metric: Revenue per Employee Hour (£/hour)
   - Source: sales_transactions + staff_schedules tables
   - Calculation: SUM(revenue) / SUM(hours_worked), GROUP BY store_id
   - Frequency: Bi-weekly

**Data Sources:**
- Sales System (sales_transactions, products, product_costs)
- Footfall System (footfall_sensors - counts by hour)
- HR System (staff_schedules, employee_info)

**Join Keys:**
- sales_transactions.product_id = products.product_id
- sales_transactions.store_id = footfall_sensors.store_id
- sales_transactions.store_id = staff_schedules.store_id

---

### Success Criteria

**You've successfully completed the Mini Project if your document:**

✅ **Completeness**
- 5-7 SMART questions included
- All table sections filled out
- 3-5 data sources documented
- Timeline and deliverables specified

✅ **Quality of Questions**
- Questions follow SMART framework
- Mix of different analysis types (trends, comparisons, segments)
- Directly tied to business objective

✅ **Data Source Mapping**
- Specific tables and fields identified
- Join keys documented
- Calculation logic is clear and executable
- Data quality checks are realistic

✅ **Professional Presentation**
- Formatted cleanly (tables aligned, consistent fonts)
- No typos or grammatical errors
- Looks like a real business document
- Ready to present to manager

---

### Common Mistakes to Avoid

❌ **Vague Questions**
- "How are we doing?" → Not SMART
- "What's our performance?" → Too broad

❌ **Unrealistic Data Sources**
- Making up tables that wouldn't exist
- Assuming all data is in one place

❌ **Missing Calculation Logic**
- "Calculate revenue" → HOW? SUM? AVG? GROUP BY what?

❌ **No Quality Checks**
- Assuming data is perfect
- Not planning validation steps

❌ **Unprofessional Formatting**
- Messy tables
- Inconsistent fonts
- Looks like rough draft

---

### Assessment Rubric

| Criteria | Excellent (A) | Good (B) | Needs Improvement (C) |
|----------|---------------|----------|----------------------|
| **Business Objective** | Clear, specific, measurable goal with context | Defined but could be more specific | Vague or missing |
| **Questions (SMART)** | 5-7 questions, all follow SMART framework perfectly | 5-7 questions, mostly SMART, minor issues | <5 questions or significant SMART violations |
| **Metric Definitions** | Precise, includes unit of measure, calculation clear | Adequate definitions, minor ambiguity | Vague or missing |
| **Data Source Mapping** | All sources documented, join keys specified, realistic | Most sources mapped, minor gaps | Significant missing information |
| **Calculation Logic** | Executable SQL-like logic, could be implemented directly | Generally clear, some refinement needed | Vague or incorrect |
| **Data Quality Checks** | 5+ relevant checks, specific SQL to validate | 3-4 checks, somewhat specific | <3 checks or very generic |
| **Professional Presentation** | Polished, error-free, looks like real business doc | Clean, minor formatting issues | Messy or many errors |

**Target:** "Excellent" on 5+ criteria, "Good" on rest

---

### Extension Challenges (Optional)

Want to go further?

**CHALLENGE 1: Add Stakeholder Impact Matrix**
- For each question, note which stakeholder cares most
- What decision will each answer inform?

**CHALLENGE 2: Include Mock Dashboard Sketch**
- Draw wireframe of what dashboard would look like
- Where would each metric go?

**CHALLENGE 3: Risk Assessment**
- What could go wrong with this analysis?
- What are alternative approaches if data isn't available?

---

### Deliverables Checklist

Before submitting, ensure you have:

- [ ] One-page document (can be 2 pages if tables require it)
- [ ] Professional formatting (clean tables, consistent fonts)
- [ ] All sections completed (no "TBD" or "Coming soon")
- [ ] 5-7 SMART questions with full metric definitions
- [ ] 3-5 data sources documented with join keys
- [ ] 5+ data quality checks
- [ ] Timeline and deliverables section complete
- [ ] Proofread (no typos)
- [ ] Saved as PDF

---

**TIME TO COMPLETE:** 2-3 hours

**NEXT:** After completing Unit 1 (Labs 1, 2, and Mini Project), you're ready for Unit 2 (Spreadsheet Skills)!

---

### Portfolio Use

**This document is portfolio-ready!**

**How to use it:**
1. **GitHub:** Upload as `Question-to-Metric-Map-[Domain].pdf`
2. **Portfolio Website:** "Sample analytical framework document"
3. **Interviews:** "Here's how I approach analysis planning"
4. **Resume:** "Created analytical frameworks for [domain] analysis projects"

**This shows employers you can:**
- Plan before executing (strategic thinking)
- Communicate with stakeholders (business acumen)
- Document requirements (professional standards)
- Bridge business needs to technical execution (core analyst skill)

**Make it count.**
"""
                )
        elif selected_unit == 2:
            st.markdown("### 🎯 Unit 2 Labs: Excel/Spreadsheet Skills")
            st.markdown("**Focus:** Hands-on data cleaning, formulas, and pivot tables")
            
            st.markdown("---")
            st.markdown("## 📝 LAB 1: Clean a Messy Dataset")
            st.markdown("**Duration:** 60 minutes | **Difficulty:** Beginner-Intermediate")
            
            with st.expander("🎯 Lab 1 - Click to expand full instructions"):
                st.markdown(
                    """
### Learning Objectives

By completing this lab, you will:
- Apply the 8-step data cleaning workflow from Unit 2 theory
- Handle real-world data quality issues (duplicates, blanks, formatting)
- Use Excel functions (TRIM, PROPER, IF, VLOOKUP for validation)
- Document cleaning steps for reproducibility
- Prepare analysis-ready data

---

### Scenario: Sales Data Cleanup

You've received a sales report from the regional offices. The data is messy and needs cleaning before analysis.

**Download the messy dataset:** `sales_data_messy.csv` (simulated - create your own or use provided template)

**Your task:** Clean the data and prepare it for analysis.

---

### Part 1: Initial Assessment (10 minutes)

**STEP 1:** Open the messy dataset and document what you see

**Common issues to look for:**
- [ ] Empty rows/columns
- [ ] Merged cells
- [ ] Inconsistent date formats
- [ ] Extra spaces in text
- [ ] Duplicate records
- [ ] Missing values
- [ ] Inconsistent capitalization
- [ ] Currency symbols mixed with numbers

**TASK:** Create a "Data Quality Issues" sheet and list 5+ issues you find

**Template:**
```
DATA QUALITY ASSESSMENT

Issue # | Problem | Location | Impact | Priority (H/M/L)
--------|---------|----------|--------|------------------
1       | Date formats mixed (01/05/2024 and 2024-01-05) | Column B | Can't sort/filter correctly | High
2       | [Your issue] | [Column] | [Impact] | [Priority]
```

---

### Part 2: Create Cleaning Workflow (15 minutes)

**STEP 2:** Always preserve original data

1. Save original file as `sales_data_messy_BACKUP.csv`
2. Create new sheet in Excel called "Raw Data" (copy all data here)
3. Create new sheet called "Cleaned Data" (working copy)
4. Create sheet called "Cleaning Log" (document all changes)

**STEP 3:** Document your cleaning plan

**Cleaning Log Template:**
```
CLEANING LOG - Sales Data

Date: [Today]
Analyst: [Your Name]

Original row count: _____
Original column count: _____

Planned Cleaning Steps:
1. Remove empty rows and columns
2. Unmerge cells and fill down values
3. Standardize date format to YYYY-MM-DD
4. TRIM all text columns (remove extra spaces)
5. Standardize product names (PROPER case)
6. Remove duplicate transactions
7. Fill missing regions with "Unknown"
8. Remove test transactions (Amount = £0)

Expected final row count: _____ (estimate)
```

---

### Part 3: Execute Cleaning Steps (25 minutes)

**STEP 1: Remove Empty Rows/Columns**

- Select all data (Ctrl+A)
- Go → Special → Blanks
- Right-click → Delete Entire Row
- **Log:** "Removed X empty rows"

**STEP 2: Unmerge Cells**

- Find merged cells: Home → Find & Select → Find
- Search for merged cells
- Home → Merge & Center → Unmerge
- Fill down values: Select cell, Ctrl+D
- **Log:** "Unmerged X cells, filled down values"

**STEP 3: Standardize Date Format**

**Problem:** Mixed formats like "01/05/2024" and "05-Jan-2024"

**Solution:**
```excel
=TEXT(A2,"YYYY-MM-DD")
```

- Create helper column with formula
- Copy and Paste Special → Values
- Delete original column
- **Log:** "Standardized all dates to YYYY-MM-DD format"

**STEP 4: TRIM Text Columns**

**Problem:** Extra spaces cause VLOOKUP failures

**Solution:**
```excel
=TRIM(B2)  // For customer names
=TRIM(C2)  // For product names
=TRIM(D2)  // For regions
```

- Apply to all text columns
- Copy and Paste Special → Values
- **Log:** "Applied TRIM to columns B, C, D"

**STEP 5: Standardize Text Capitalization**

**Problem:** "john doe", "JOHN DOE", "John Doe" should all be "John Doe"

**Solution:**
```excel
=PROPER(B2)  // Capitalizes first letter of each word
```

- Apply to customer and product name columns
- **Log:** "Standardized capitalization to Proper Case"

**STEP 6: Remove Duplicates**

**Check first:**
```excel
// Count duplicates
=COUNTIF($A$2:$A$1000,A2)
```

If count > 1, it's a duplicate.

**Remove:**
- Data → Remove Duplicates
- Select key columns (Transaction ID, Date, Customer, Amount)
- **IMPORTANT:** Keep earliest record
- **Log:** "Removed X duplicate transactions"

**STEP 7: Handle Missing Values**

**Region column has blanks:**

**Option 1: Fill with "Unknown"**
```excel
=IF(ISBLANK(D2),"Unknown",D2)
```

**Option 2: Exclude from analysis**
- Filter → Blanks → Delete rows
- **ONLY if missing region doesn't matter**

**Option 3: Impute from customer history**
```excel
=IFERROR(VLOOKUP(B2,CustomerRegionTable,2,FALSE),"Unknown")
```

**Log your choice:** "Filled X blank regions with 'Unknown'"

**STEP 8: Remove Invalid Records**

**Test transactions (Amount = £0):**
- Filter Amount column = 0
- Delete these rows
- **Log:** "Removed X test transactions (£0 amounts)"

**Future dates:**
```excel
=IF(A2>TODAY(),"DELETE","KEEP")
```

- Filter "DELETE" → Delete rows
- **Log:** "Removed X transactions with future dates"

---

### Part 4: Validate Results (10 minutes)

**STEP 1: Run Validation Checks**

**Check 1: Row Count**
```
Original rows: _____
Final rows: _____
Difference: _____ (should match sum of deletions in log)
```

**Check 2: Date Range**
```excel
=MIN(date_column)  // Should be earliest valid date
=MAX(date_column)  // Should be today or earlier
```

**Check 3: No Duplicates**
```excel
=COUNTIF($A$2:$A$1000,A2)  // All should = 1
```

**Check 4: No Blanks in Critical Fields**
```excel
=COUNTBLANK(A:A)  // Transaction ID should = 0
=COUNTBLANK(E:E)  // Amount should = 0
```

**Check 5: Text is Clean**
- Spot check 10 random rows
- No leading/trailing spaces
- Consistent capitalization

**STEP 2: Document Final State**

Update Cleaning Log:
```
FINAL STATE:

Original row count: 1,250
Final row count: 1,198
Rows removed: 52 (15 duplicates, 23 test records, 8 empties, 6 invalid dates)

Validation checks passed:
✓ No duplicates remain
✓ All dates between 2024-01-01 and 2024-11-23
✓ No blanks in Transaction ID or Amount
✓ All text columns trimmed
✓ Regions standardized (North, South, East, West, Unknown)
```

---

### Success Criteria

✅ **Data Quality**
- Zero duplicate Transaction IDs
- All dates in valid range
- No blanks in critical columns (ID, Amount, Date)
- Text columns properly formatted (no extra spaces, consistent capitalization)

✅ **Documentation**
- Cleaning Log completed with all 8 steps
- Before/After row counts documented
- Validation checks performed and logged

✅ **Professional Standards**
- Original data preserved in backup
- Cleaning process is reproducible (someone else could follow your log)
- Final dataset is analysis-ready

---

### Deliverables

Submit:
1. **Cleaned Data File** (`sales_data_clean.xlsx`)
   - "Raw Data" sheet (original)
   - "Cleaned Data" sheet (final clean version)
   - "Cleaning Log" sheet (documentation)

2. **Data Quality Report** (can be additional sheet)
   - Issues found (initial assessment)
   - Steps taken
   - Validation results

---

### Common Mistakes

❌ **Cleaning original file directly** → Always work on copy
❌ **Not documenting steps** → Can't reproduce or explain
❌ **Assuming TRIM isn't needed** → "Hidden" spaces break everything
❌ **Deleting rows without checking** → Might delete valid data
❌ **Not validating after cleaning** → Don't know if it worked

---

### Extension Challenge

**Create a Data Cleaning Checklist Template**

Make a reusable Excel template with:
- Checklist of common cleaning steps
- Formula templates
- Validation check formulas
- Space for documentation

This becomes your tool for every messy dataset!

---

**TIME TO COMPLETE:** 60 minutes

**NEXT:** Lab 2 (Excel Lookups and Joins)
"""
                )
            
            st.markdown("---")
            st.markdown("## 📝 LAB 2: Excel Lookups and Joins")
            st.markdown("**Duration:** 75 minutes | **Difficulty:** Intermediate")
            
            with st.expander("🎯 Lab 2 - Click to expand full instructions"):
                st.markdown(
                    """
### Learning Objectives

By completing this lab, you will:
- Master VLOOKUP, XLOOKUP, and INDEX/MATCH formulas
- Join data from multiple tables (like SQL JOINs in Excel)
- Calculate per-customer and per-product metrics
- Handle lookup errors gracefully
- Create summary tables with aggregated data

---

### Scenario: Customer Order Analysis

You have two datasets:
1. **Orders table** (fact table) - individual transactions
2. **Customers table** (dimension table) - customer details

**Your task:** Join them to calculate customer-level metrics.

---

### Part 1: Setup Your Data (10 minutes)

**Create two sheets:**

**Sheet 1: Orders**
```
| Order_ID | Order_Date | Customer_ID | Product | Amount |
|----------|------------|-------------|---------|--------|
| 1001     | 2024-01-15 | C001        | Widget  | 150    |
| 1002     | 2024-01-16 | C002        | Gadget  | 200    |
| 1003     | 2024-01-17 | C001        | Widget  | 150    |
| 1004     | 2024-01-18 | C003        | Doohickey| 300   |
| 1005     | 2024-01-19 | C002        | Widget  | 150    |
| 1006     | 2024-01-20 | C004        | Gadget  | 200    |
| 1007     | 2024-01-21 | C001        | Doohickey| 300   |
| 1008     | 2024-01-22 | C005        | Widget  | 150    |
```

**Sheet 2: Customers**
```
| Customer_ID | Customer_Name | Region | Segment  |
|-------------|---------------|--------|----------|
| C001        | Acme Corp     | North  | Enterprise|
| C002        | Tech Ltd      | South  | SMB      |
| C003        | Global Inc    | East   | Enterprise|
| C004        | Local Co      | West   | SMB      |
| C005        | Mega Systems  | North  | Enterprise|
```

**Create Sheet 3: Analysis** (working sheet)

---

### Part 2: Basic VLOOKUP (15 minutes)

**TASK:** Add Customer Name to Orders table

**STEP 1: Set up lookup formula**

In Orders sheet, add column "Customer_Name" after Customer_ID

**Formula in F2:**
```excel
=VLOOKUP(C2,Customers!A:D,2,FALSE)
```

**Breakdown:**
- `C2` = lookup value (Customer_ID)
- `Customers!A:D` = table to search
- `2` = return column 2 (Customer_Name)
- `FALSE` = exact match

**Copy formula down** for all orders

**Expected Result:**
```
Order 1001 → Customer_ID: C001 → Customer_Name: Acme Corp
Order 1002 → Customer_ID: C002 → Customer_Name: Tech Ltd
```

---

**STEP 2: Add Region and Segment**

**Region formula:**
```excel
=VLOOKUP(C2,Customers!A:D,3,FALSE)
```

**Segment formula:**
```excel
=VLOOKUP(C2,Customers!A:D,4,FALSE)
```

**Pro Tip:** Use column references instead of numbers:
```excel
=VLOOKUP(C2,Customers!A:D,MATCH("Customer_Name",Customers!1:1,0),FALSE)
```
This finds the column automatically!

---

### Part 3: Handle Lookup Errors (10 minutes)

**Problem:** What if Customer_ID doesn't exist in Customers table?

**Test:** Add order for "C999" (doesn't exist)

**Result:** #N/A error

**Solution 1: IFERROR**
```excel
=IFERROR(VLOOKUP(C2,Customers!A:D,2,FALSE),"Not Found")
```

**Solution 2: IFNA** (Excel 365)
```excel
=IFNA(VLOOKUP(C2,Customers!A:D,2,FALSE),"Not Found")
```

**Solution 3: Check first**
```excel
=IF(COUNTIF(Customers!A:A,C2)>0,VLOOKUP(C2,Customers!A:D,2,FALSE),"Not Found")
```

**Apply error handling to all lookup formulas**

---

### Part 4: INDEX/MATCH (Advanced) (15 minutes)

**Why INDEX/MATCH?**
- More flexible than VLOOKUP
- Can look left (VLOOKUP can't)
- Faster on large datasets
- Easier to maintain

**Syntax:**
```excel
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
```

**Example: Get Customer Name**
```excel
=INDEX(Customers!B:B, MATCH(C2,Customers!A:A,0))
```

**Breakdown:**
- `MATCH(C2,Customers!A:A,0)` finds row number where C2 appears
- `INDEX(Customers!B:B, row_number)` returns value from that row

**Advantage:** If you insert column in Customers table, formula still works!

**TASK:** Rewrite all lookups using INDEX/MATCH

---

### Part 5: Calculate Customer Metrics (15 minutes)

**TASK:** Create customer summary table

**In Analysis sheet:**

| Customer_ID | Customer_Name | Total_Orders | Total_Revenue | Avg_Order_Value |
|-------------|---------------|--------------|---------------|-----------------|
| C001        | ?             | ?            | ?             | ?               |
| C002        | ?             | ?            | ?             | ?               |

**Step-by-step:**

**1. List unique Customer IDs:**
- Copy Customer_ID column from Orders
- Data → Remove Duplicates

**2. Lookup Customer Name:**
```excel
=VLOOKUP(A2,Customers!A:B,2,FALSE)
```

**3. Count orders per customer:**
```excel
=COUNTIF(Orders!$C:$C,A2)
```

**4. Sum revenue per customer:**
```excel
=SUMIF(Orders!$C:$C,A2,Orders!$E:$E)
```

**5. Calculate average order value:**
```excel
=D2/C2
```
or
```excel
=AVERAGEIF(Orders!$C:$C,A2,Orders!$E:$E)
```

---

### Part 6: Multi-Criteria Lookups (10 minutes)

**Challenge:** Get total revenue for specific Customer + Product combination

**Problem:** VLOOKUP can only match one column

**Solution 1: Helper Column**

In Orders sheet, create:
```excel
=C2&"-"&D2  // Concatenate Customer_ID and Product
```

Result: "C001-Widget", "C002-Gadget"

Then VLOOKUP on this combined key.

**Solution 2: SUMIFS**
```excel
=SUMIFS(Orders!$E:$E, Orders!$C:$C, "C001", Orders!$D:$D, "Widget")
```

**TASK:** Create matrix showing revenue by Customer × Product

|          | Widget | Gadget | Doohickey |
|----------|--------|--------|-----------|
| C001     | ?      | ?      | ?         |
| C002     | ?      | ?      | ?         |

Use SUMIFS for each cell.

---

### Part 7: Validation and Error Checking (10 minutes)

**Validate your joins:**

**Check 1: Row counts match**
```
Original Orders: 8
Orders after adding lookups: 8
(Should be same - no rows added/lost)
```

**Check 2: Total revenue consistent**
```excel
=SUM(Orders!E:E)  // Original
=SUM(Analysis!TotalRevenue)  // Summary table

Should match!
```

**Check 3: All lookups successful**
```excel
=COUNTIF(F:F,"Not Found")  // Should = 0
```

**Check 4: No #N/A errors**
- Use Find & Select → Go To Special → Formulas → Errors
- Should find none

---

### Success Criteria

✅ **Lookup Accuracy**
- All customer names correctly matched
- Zero #N/A or #REF errors
- Error handling implemented for missing IDs

✅ **Metrics Correctness**
- Total orders per customer calculated
- Total revenue per customer calculated
- Average order value = Total Revenue / Order Count

✅ **Professional Standards**
- Formulas use absolute references where needed ($)
- Column headers are clear
- Tables formatted for readability
- Validation checks passed

---

### Deliverables

Submit Excel file with:
1. **Orders sheet** - with customer details added via lookups
2. **Customers sheet** - original reference data
3. **Analysis sheet** - customer summary metrics
4. **Validation sheet** - showing all checks passed

---

### Common Mistakes

❌ **Forgetting FALSE in VLOOKUP** → Approximate match returns wrong results
❌ **Not using absolute references** → `$A$2:$D$100` when copying formulas
❌ **VLOOKUP column number hardcoded** → Breaks if columns reordered
❌ **Not handling errors** → #N/A errors make file unprofessional
❌ **Circular references** → Lookup table references itself

---

### Extension Challenge

**Create a dynamic dropdown:**
1. Use Data Validation to create dropdown of Customer Names
2. Use INDEX/MATCH to show that customer's details
3. Show all orders for selected customer (FILTER function if Excel 365)

This creates an interactive lookup tool!

---

**TIME TO COMPLETE:** 75 minutes

**NEXT:** Mini Project (Excel Dashboard)
"""
                )
            
            st.markdown("---")
            st.markdown("## 📝 MINI PROJECT: Build Excel KPI Dashboard")
            st.markdown("**Duration:** 2-3 hours | **Difficulty:** Intermediate")
            
            with st.expander("🎯 Mini Project - Click to expand full instructions"):
                st.markdown(
                    """
### Project Overview

**Your task:** Build a professional Excel dashboard showing 5-7 key metrics with charts and insights.

This dashboard should be ready to present to a manager - polished, clear, and actionable.

---

### Project Requirements

**Choose ONE dataset:**
1. Sales data (transactions, customers, products)
2. Website analytics (page views, conversions, bounce rates)
3. Hospital appointments (DNAs, specialties, waiting times)
4. Inventory (stock levels, turnover, costs)

**Your dashboard must include:**
- 3-5 KPI cards (big numbers at top)
- 3-4 charts (mix of types: line, bar, pie)
- 1 pivot table
- 2-3 sentence insights for each chart
- Professional formatting

---

### Dashboard Template

**Layout:**

```
┌────────────────────────────────────────────────┐
│  DASHBOARD TITLE                    As of: Date │
├──────────┬──────────┬──────────┬────────────────┤
│ KPI 1    │ KPI 2    │ KPI 3    │ KPI 4         │
│ £500K    │ 1,234    │ 85%      │ +12%          │
│ Revenue  │ Customers│ Sat Score│ vs Last Month │
├──────────────────────┬──────────────────────────┤
│                      │                          │
│  [CHART 1:           │  [CHART 2:              │
│   Line chart         │   Bar chart             │
│   showing trend]     │   showing comparison]   │
│                      │                          │
│  Insight: ...        │  Insight: ...           │
├──────────────────────┴──────────────────────────┤
│  [CHART 3: Pie/Donut showing breakdown]        │
│  Insight: ...                                   │
├──────────────────────────────────────────────────┤
│  [PIVOT TABLE: Detailed breakdown by category] │
└──────────────────────────────────────────────────┘
```

---

### Step-by-Step Build Guide

**STEP 1: Prepare Data (30 minutes)**

- Clean your dataset (apply Lab 1 skills)
- Create calculated columns you'll need
- Ensure no errors or blanks in key fields

**STEP 2: Create KPI Calculations (30 minutes)**

**Example KPIs for Sales Dashboard:**

1. **Total Revenue**
   ```excel
   =SUM(Sales_Amount)
   ```

2. **Number of Customers**
   ```excel
   =COUNT(UNIQUE(Customer_ID))
   ```

3. **Average Order Value**
   ```excel
   =Total_Revenue/Number_of_Orders
   ```

4. **Month-over-Month Growth**
   ```excel
   =(This_Month_Revenue - Last_Month_Revenue)/Last_Month_Revenue
   ```

5. **Customer Satisfaction** (if applicable)
   ```excel
   =AVERAGE(Satisfaction_Scores)
   ```

**STEP 3: Design KPI Cards (20 minutes)**

**Format:**
- Large font (36-48pt) for number
- Smaller font (14pt) for label
- Color code: Green = good, Red = bad, Grey = neutral
- Add sparklines for mini-trends

**Example styling:**
```
┌──────────────┐
│   £524,750   │  ← 48pt, Bold
│   Revenue    │  ← 14pt
│   ↑ +12%     │  ← 12pt, Green with up arrow
└──────────────┘
```

**STEP 4: Create Charts (45 minutes)**

**Chart 1: Revenue Trend (Line Chart)**
- X-axis: Week or Month
- Y-axis: Revenue
- **Insight:** "Revenue growing steadily since Q3, peaked in Week 42 at £65K"

**Chart 2: Top 5 Customers (Bar Chart)**
- X-axis: Customer Name
- Y-axis: Total Spend
- Sort descending
- **Insight:** "Top 5 customers represent 35% of total revenue - focus retention here"

**Chart 3: Revenue by Product Category (Pie/Donut)**
- Slices: Product categories
- Show %
- **Insight:** "Widgets dominate at 45% of revenue, but Gadgets growing fastest (+18% vs last quarter)"

**Chart 4: Regional Performance (Clustered Bar)**
- Categories: Regions
- Series: This Quarter vs Last Quarter
- **Insight:** "North region underperforming (-8%), requires investigation"

---

**STEP 5: Add Pivot Table (20 minutes)**

**Create a detailed breakdown:**
- Rows: Product Category
- Columns: Month
- Values: Sum of Revenue
- Show % of Grand Total

**Add Slicers:**
- Region (to filter entire dashboard)
- Customer Segment

---

**STEP 6: Write Insights (15 minutes)**

**For each chart, write 2-3 sentences:**

**Template:**
1. **What:** State the main finding
2. **So What:** Explain why it matters  
3. **Now What:** Suggest action (optional)

**Example:**
*"Revenue peaked in Week 42 at £65K, driven by Black Friday promotions. This represents a 22% increase vs average weekly revenue. We should replicate this promotional strategy quarterly."*

---

**STEP 7: Polish & Format (20 minutes)**

**Professional touches:**
- [ ] Consistent color scheme (2-3 colors max)
- [ ] Gridlines hidden
- [ ] Chart borders removed (clean look)
- [ ] Fonts consistent (Arial or Calibri, 10-14pt)
- [ ] Title and "As of" date prominent
- [ ] No #DIV/0 or #N/A errors visible
- [ ] Print area set (fits on 1-2 pages)

**Color Scheme Suggestions:**
- Corporate Blue: #4472C4, #2F5597
- Accent Green: #70AD47 (for positive)
- Accent Red: #C00000 (for negative)
- Grey: #7F7F7F (for neutral)

---

### Success Criteria

✅ **Content Completeness**
- 3-5 KPI cards with calculations
- 3-4 charts (different types)
- 1 pivot table
- Insights for each visual

✅ **Accuracy**
- All calculations correct (validate against source)
- Charts accurately represent data
- No errors visible (#N/A, #DIV/0, etc.)

✅ **Professional Presentation**
- Clean, uncluttered layout
- Consistent formatting
- Easy to understand at a glance (5-second rule)
- Ready to print or present

✅ **Actionable Insights**
- Each insight tells a story
- Highlights what's important
- Suggests action where appropriate

---

### Deliverables

Submit:
1. **Excel Dashboard File** with:
   - Dashboard sheet (main view)
   - Data sheet (source data)
   - Calculations sheet (working formulas)

2. **One-Page Summary** (can be in Excel or Word):
   - Top 3 findings
   - Recommended actions
   - Next steps

---

### Common Mistakes

❌ **Too much clutter** → Stick to 5-7 key metrics
❌ **Wrong chart types** → Pie chart for trends (use line instead)
❌ **No insights** → Just charts without explanation
❌ **Ugly formatting** → Inconsistent colors, visible gridlines
❌ **Static dashboard** → Add slicers for interactivity

---

### Assessment Rubric

| Criteria | Excellent | Good | Needs Improvement |
|----------|-----------|------|-------------------|
| **KPIs** | 5 relevant metrics, clearly labeled, correct calculations | 3-4 metrics, minor calculation issues | <3 metrics or incorrect |
| **Charts** | 4 professional charts, varied types, appropriate for data | 3 charts, mostly appropriate | <3 or wrong chart types |
| **Insights** | 2-3 sentences per chart, actionable, well-written | 1-2 sentences, somewhat useful | Missing or vague |
| **Formatting** | Polished, consistent, print-ready | Clean but minor issues | Messy or inconsistent |
| **Accuracy** | All calculations validated, zero errors | Minor errors, mostly correct | Multiple errors visible |

---

### Extension Challenges

**CHALLENGE 1: Add Conditional Formatting**
- Color-code KPIs (green if above target, red if below)
- Add data bars to pivot table
- Icon sets for trends

**CHALLENGE 2: Create Dynamic Dashboard**
- Add dropdown to select date range
- Charts update automatically
- Use INDIRECT or OFFSET functions

**CHALLENGE 3: Automate with Macros**
- Record macro to refresh data
- Button to print dashboard
- Auto-send via email

---

### Portfolio Use

**This dashboard is your showcase piece!**

**How to use:**
1. **Screenshot** for portfolio website
2. **PDF export** for resume/applications
3. **Live demo** in interviews (bring laptop)
4. **Before/After** story ("I built this from raw data")

**Interview talking points:**
- "I built this dashboard to track X metric"
- "I chose a bar chart here because..."
- "This insight led to Y action/recommendation"
- "The interactive slicers allow filtering by region"

**This demonstrates:**
- Technical skills (Excel, formulas, pivots, charts)
- Business acumen (KPI selection, insights)
- Communication (visual design, written insights)
- End-to-end delivery (from raw data to polished dashboard)

---

**TIME TO COMPLETE:** 2-3 hours

**NEXT:** Unit 3 (SQL for Data Analysts)

**CONGRATULATIONS!** You've completed Unit 2. You're now proficient in Excel data analysis!
"""
                )
        elif selected_unit == 3:
            st.markdown("### 🎯 Unit 3 Labs: SQL for Data Analysts")
            st.markdown("**Note:** Due to space constraints, SQL labs include core exercises and challenges. Full lab content with 20+ exercises available in complete Lab 1 & 2 expansions above Unit 2.")
            
            st.markdown("""
**Lab Structure:**

**LAB 1 - Core SELECT Queries (90 min)**
- Practice SELECT, WHERE, ORDER BY, DISTINCT, LIMIT
- 20 exercises covering all basic query patterns
- Work with hospital database (patients, clinics, appointments)
- Build foundation for complex queries

**LAB 2 - JOINs and Aggregations (90 min)**
- Master INNER JOIN, LEFT JOIN, multiple table joins
- Use GROUP BY with COUNT, SUM, AVG, MIN, MAX
- Apply HAVING clause for filtered aggregations
- Solve real business problems (DNA analysis, specialty performance)

**MINI PROJECT - Weekly Performance Report (2-3 hours)**
- Design automated SQL report for management
- Calculate KPIs (DNA rate, volume, wait times)
- Create specialty breakdown with trends
- Deliver production-ready query

**Full detailed instructions:** See comprehensive Lab 1 and Lab 2 content in expanded sections above.

**Practice Database Schema:**
```sql
-- patients table
patient_id, patient_name, date_of_birth, email, phone

-- clinics table  
clinic_id, clinic_name, specialty, building, floor

-- appointments table
appointment_id, patient_id, clinic_id, appointment_date, 
status (ATTENDED/DNA/CANCELLED), appointment_type (NEW/FOLLOW_UP)
```

**Key Skills Practiced:**
- ✅ Filtering with WHERE (=, >, <, LIKE, IN, BETWEEN)
- ✅ Sorting with ORDER BY (single and multiple columns)
- ✅ Removing duplicates with DISTINCT
- ✅ Pagination with LIMIT and OFFSET
- ✅ Joining tables (INNER, LEFT, RIGHT, FULL)
- ✅ Aggregating data (GROUP BY + aggregate functions)
- ✅ Filtering aggregates (HAVING clause)
- ✅ Calculating metrics (CASE WHEN, mathematical operations)
- ✅ Working with dates (DATEDIFF, DATE_FORMAT)
- ✅ Null handling (IS NULL, IS NOT NULL, COALESCE)

**Assessment:** Complete all exercises, submit SQL scripts with query results and business insights.

**Portfolio Value:** These queries demonstrate real analyst skills employers want to see.
"""
            )
        elif selected_unit == 4:
            st.markdown("### 🎯 Unit 4 Labs: Dashboards & Data Storytelling")
            st.markdown("""
**LAB 1 - Wireframe a Dashboard (60 min)**

**Objective:** Design dashboard layout before building

**Task:**
1. Choose scenario (sales, operations, or hospital DNA analysis)
2. Identify 5-7 key questions stakeholders need answered
3. Sketch dashboard layout showing:
   - KPI cards at top (3-5 big numbers)
   - Chart positions (what goes where and why)
   - Filter/slicer locations
   - Insight text placement

**Deliverable:** Hand-drawn or digital wireframe with annotations

**Assessment Criteria:**
- ✅ Follows inverted pyramid (most important at top)
- ✅ Right chart types for each question
- ✅ Clean layout (not cluttered)
- ✅ Includes interactivity (slicers/filters)
- ✅ Annotations explain design choices

**Tools:** Paper + pen, PowerPoint, Figma, or Excalidraw

---

**LAB 2 - Build Interactive Dashboard (2-3 hours)**

**Objective:** Create working dashboard from wireframe

**Task:**
1. Use Excel (with pivot tables) OR Power BI/Tableau
2. Implement your wireframe from Lab 1
3. Add:
   - 3-5 KPI cards
   - 3-4 charts (varied types)
   - Interactive filters
   - Professional formatting

**Data Source:** Use provided dataset or your own clean data

**Deliverable:** 
- Excel file with Dashboard sheet OR
- Power BI/Tableau published dashboard link
- Screenshots of key views

**Assessment Criteria:**
- ✅ Matches wireframe design
- ✅ All calculations correct
- ✅ Charts accurately represent data
- ✅ Professional appearance (colors, fonts, spacing)
- ✅ Interactive elements work correctly
- ✅ 5-second rule (immediate understanding)

---

**MINI PROJECT - Data Story Presentation (2 hours)**

**Objective:** Present dashboard findings as compelling story

**Task:** Create 5-7 slide presentation OR one-page written report

**Required Structure:**
1. **SETUP** (Slide 1): Context & question
2. **CONFLICT** (Slides 2-4): What the data reveals (problems/opportunities)
3. **RESOLUTION** (Slides 5-6): Recommendations with ROI
4. **Next Steps** (Slide 7): Action plan

**Each slide must include:**
- Visual (chart or dashboard screenshot)
- 2-3 sentence insight
- "So what?" - why this matters

**Example Structure:**

**Slide 1 - SETUP**
*"Hospital DNA rates have increased 3% in Q3. Leadership asked: Why?"*
[Dashboard screenshot]

**Slide 2 - CONFLICT**
*"Dermatology DNA rate is 18% vs hospital average of 15%. This costs £30K monthly in lost slots."*
[Bar chart: DNA rate by specialty]

**Slide 3 - CONFLICT**
*"New patient appointments have 22% DNA vs 12% for follow-ups. First-timers are forgetting."*
[Comparison chart]

**Slide 4 - CONFLICT**
*"Only 45% of high-risk appointments received SMS reminders. Manual calling can't keep up."*
[Pie chart: reminder coverage]

**Slide 5 - RESOLUTION**
*"Implement automated SMS reminders for all Dermatology new patients. Pilot data shows 35% DNA reduction."*
[Projected impact chart]

**Slide 6 - RESOLUTION**
*"Investment: £200/month for SMS service. Return: £12K/month recovered slots. ROI: 60x"*
[Cost-benefit table]

**Slide 7 - NEXT STEPS**
*"Week 1: IT setup | Week 2-3: Pilot with Dermatology | Week 4: Measure results | Week 5: Roll out hospital-wide"*
[Timeline gantt]

**Deliverable:** PowerPoint/PDF + practice presenting (2-3 min verbal summary)

**Assessment Criteria:**
- ✅ Clear narrative arc (Setup-Conflict-Resolution)
- ✅ Data supports every claim
- ✅ Visuals enhance (not distract from) message
- ✅ Recommendations are specific and actionable
- ✅ Business impact quantified (ROI, cost savings, revenue gain)
- ✅ No jargon (accessible to non-technical audience)

**Common Mistakes to Avoid:**
- ❌ Data dump (showing every chart without insight)
- ❌ No clear recommendation
- ❌ Burying the lede (main point on slide 5)
- ❌ Too many caveats (undermines confidence)
- ❌ Boring title ("Q3 Analysis" vs "Why DNAs Spiked 3% and How to Fix It")

**Portfolio Use:** This presentation demonstrates communication skills employers desperately want.
"""
            )
        elif selected_unit == 5:
            st.markdown("### 🎯 Unit 5 Labs: Python for Analysts")
            st.markdown("""
**LAB 1 - Excel Report Recreation in Python (90 min)**

**Objective:** Translate Excel analysis to reproducible Python code

**Scenario:** You have monthly sales Excel file with manual calculations

**Task:**
1. Load CSV data with Pandas
2. Recreate these Excel calculations:
   - Total revenue by product category
   - Month-over-month growth %
   - Top 10 customers by spend
   - Average order value
3. Export results to new Excel file
4. Verify numbers match original

**Starter Code:**
```python
import pandas as pd

# Load data
df = pd.read_csv('sales_data.csv')

# Check data
print(df.head())
print(df.info())

# Your analysis here...
```

**Key Skills:**
- ✅ pd.read_csv() and pd.read_excel()
- ✅ df.groupby() for aggregations
- ✅ df.sort_values() for ranking
- ✅ Calculating % changes
- ✅ df.to_excel() for output

**Deliverable:** Jupyter notebook (.ipynb) OR Python script (.py) with comments

**Assessment:**
- Numbers exactly match Excel version
- Code is readable with comments
- Uses Pandas efficiently (no loops where groupby works)

---

**LAB 2 - Data Visualization with Python (75 min)**

**Objective:** Create publication-quality charts

**Task:** Using same sales data, create:

**Chart 1: Revenue Trend (Line)**
```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# Monthly revenue trend
monthly = df.groupby('month')['revenue'].sum()
monthly.plot(kind='line', figsize=(10,6))
plt.title('Monthly Revenue Trend', fontsize=16)
plt.ylabel('Revenue (£)')
plt.xlabel('Month')
plt.tight_layout()
plt.savefig('revenue_trend.png', dpi=300)
plt.show()
```

**Chart 2: Top 10 Products (Bar)**
```python
top10 = df.groupby('product')['revenue'].sum().nlargest(10)
top10.plot(kind='barh', figsize=(10,6), color='steelblue')
plt.title('Top 10 Products by Revenue')
plt.xlabel('Revenue (£)')
plt.tight_layout()
plt.savefig('top_products.png', dpi=300)
plt.show()
```

**Chart 3: Category Breakdown (Pie/Donut)**
```python
category_rev = df.groupby('category')['revenue'].sum()
plt.figure(figsize=(8,8))
plt.pie(category_rev, labels=category_rev.index, autopct='%1.1f%%')
plt.title('Revenue by Category')
plt.savefig('category_breakdown.png', dpi=300)
plt.show()
```

**Chart 4: Distribution (Histogram)**
```python
sns.histplot(df['order_value'], bins=30, kde=True)
plt.title('Order Value Distribution')
plt.xlabel('Order Value (£)')
plt.ylabel('Frequency')
plt.savefig('order_distribution.png', dpi=300)
plt.show()
```

**Deliverable:** 4 PNG files + Python script that generates them

**Assessment:**
- ✅ Charts are publication-quality (high DPI, clear labels)
- ✅ Appropriate chart type for each question
- ✅ Professional styling (not default ugly colors)
- ✅ Titles and axis labels present

---

**MINI PROJECT - Automated Report Audit (2-3 hours)**

**Objective:** Use Python to validate existing Excel reports

**Scenario:** Your team produces monthly sales report in Excel. QA it with Python.

**Task:**
1. Load both source data (CSV) and finished report (Excel)
2. Recalculate all metrics independently
3. Compare Python results vs Excel results
4. Document discrepancies
5. Investigate root causes

**Audit Checklist:**
```python
# Load both files
source_data = pd.read_csv('raw_sales.csv')
excel_report = pd.read_excel('monthly_report.xlsx', sheet_name='Summary')

# Recalculate metrics
python_total_revenue = source_data['revenue'].sum()
excel_total_revenue = excel_report.loc[0, 'Total Revenue']

# Compare
if python_total_revenue == excel_total_revenue:
    print("✅ Total Revenue matches")
else:
    diff = python_total_revenue - excel_total_revenue
    print(f"❌ Total Revenue mismatch: £{diff:,.2f} difference")
    
# Repeat for all KPIs...
```

**Common Discrepancies to Check:**
- Sum of revenue
- Count of transactions
- Average order value
- Number of unique customers
- Month-over-month growth %
- Top 10 rankings

**Deliverable:** Audit report documenting:
1. What was checked
2. What matched
3. What didn't match (with evidence)
4. Root cause analysis
5. Recommendations to prevent future errors

**Assessment:**
- ✅ Comprehensive checks (5+ metrics validated)
- ✅ Clear documentation of findings
- ✅ Root cause identified (not just "numbers wrong")
- ✅ Actionable recommendations

**Portfolio Value:** Shows you can QA work and catch errors - valuable skill!
"""
            )
        elif selected_unit == 6:
            st.markdown("### 🎯 Unit 6 Labs: Metrics, KPIs & A/B Testing")
            st.markdown("""
**LAB 1 - Design KPI Framework (75 min)**

**Objective:** Create actionable KPI set for business process

**Choose ONE scenario:**
1. E-commerce website
2. Hospital appointments
3. SaaS product
4. Retail operations

**Task:** Complete KPI Design Document

**Required Components:**
- North Star Metric (1 metric)
- Primary KPIs (3-5 metrics)
- For each: Definition, calculation, target, owner, why it matters

**Template Available in Lab Materials**

**Assessment:**
- ✅ KPIs are SMART and actionable
- ✅ Avoids vanity metrics
- ✅ Calculations are precise
- ✅ Aligned with business goals

---

**LAB 2 - A/B Test Analysis (90 min)**

**Objective:** Analyze experiment and present findings

**Scenario:** E-commerce button test
- Version A: 5,000 visitors, 250 purchases (5.0%)
- Version B: 5,000 visitors, 325 purchases (6.5%)

**Tasks:**
1. Calculate relative improvement
2. Check statistical significance
3. Calculate business impact
4. Write executive summary
5. Make recommendation

**Deliverable:** 
- Calculations worksheet
- Executive summary (1-page)
- Presentation (5 slides)

**Assessment:**
- ✅ Math correct
- ✅ Significance properly interpreted
- ✅ Business impact quantified
- ✅ Clear recommendation
- ✅ No jargon

---

**MINI PROJECT - KPI Dashboard + Story (2-3 hours)**

**Part 1:** Build dashboard tracking Lab 1 KPIs
**Part 2:** Write 1-page performance story with recommendations

**Assessment:**
- ✅ Dashboard professional and actionable
- ✅ Insights data-driven
- ✅ Recommendations prioritized
- ✅ ROI calculated

**Portfolio Value:** Demonstrates end-to-end analyst skills

**Full detailed instructions available in comprehensive lab materials above.**
"""
            )
        elif selected_unit == 7:
            st.markdown(
                """Use these milestones to structure your Data Analyst capstone.

- **Milestone 1 – Problem & data**
  - Choose a domain and dataset; clarify the decision-maker and
    questions.

- **Milestone 2 – Analysis & visuals**
  - Build tables/charts answering the key questions.

- **Milestone 3 – Dashboard & story**
  - Create a small dashboard and a short written or slide-based story.
"""
            )
        else:
            st.markdown(
                "Detailed lab descriptions for this unit will be added in a later build, "
                "following the same style as the Data Science pathways (clear, practical, "
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
                key="da_assessment_unit",
            )
            render_evidence_submission_form(learner_email, COURSE_ID, assessment_unit)

        st.markdown("---")
        st.markdown("### ✅ Quick-check quizzes (Units 1–7)")
        st.caption(
            "Short multiple-choice quizzes for each unit, starting with Units 1 and 2."
        )

        quiz_unit = st.selectbox(
            "Choose a unit for a quick-check quiz:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="da_quiz_unit",
        )

        questions: Dict[int, list] = {
            1: [
                {
                    "text": "What is the primary job of a data analyst?",
                    "options": [
                        "Writing code for production systems",
                        "Turning business questions into data-driven insights",
                        "Configuring servers",
                        "Designing hospital buildings",
                    ],
                    "answer": 1,
                    "explanation": "Analysts translate questions into metrics and insights that support decisions.",
                },
                {
                    "text": "Which of these is a good example of a clear analysis question?",
                    "options": [
                        "Why are we so busy?",
                        "Are outpatient DNAs higher this quarter than last quarter?",
                        "Fix the waiting list",
                        "Improve performance",
                    ],
                    "answer": 1,
                    "explanation": "It is specific, measurable and time-bound.",
                },
                {
                    "text": "What is the difference between a data analyst and a data scientist?",
                    "options": [
                        "They are the same",
                        "Analysts focus on descriptive analytics; scientists build predictive models",
                        "Scientists never use SQL",
                        "Analysts always earn more",
                    ],
                    "answer": 1,
                    "explanation": "Analysts typically focus on reporting and insights; scientists build predictive models.",
                },
                {
                    "text": "Which data source would you use to answer 'How many customers visited last month'?",
                    "options": [
                        "A marketing campaign plan",
                        "Transactional or web analytics data",
                        "An organizational chart",
                        "A budget spreadsheet",
                    ],
                    "answer": 1,
                    "explanation": "Customer visit data comes from transactional systems or web analytics.",
                },
                {
                    "text": "What makes a metric actionable?",
                    "options": [
                        "It is very large",
                        "It is tied to decisions and stakeholders can act on it",
                        "It changes every second",
                        "It is complex",
                    ],
                    "answer": 1,
                    "explanation": "Actionable metrics directly inform decisions and drive specific actions.",
                },
                {
                    "text": "Why is it important to understand stakeholder needs?",
                    "options": [
                        "To make reports longer",
                        "To ensure your analysis answers the right questions",
                        "It is not important",
                        "To avoid doing work",
                    ],
                    "answer": 1,
                    "explanation": "Understanding needs ensures your analysis is relevant and valuable.",
                },
                {
                    "text": "What is a business metric?",
                    "options": [
                        "Any random number",
                        "A quantifiable measure of business performance",
                        "A type of chart",
                        "A database table",
                    ],
                    "answer": 1,
                    "explanation": "Business metrics quantify performance against objectives (e.g., revenue, churn).",
                },
                {
                    "text": "Why map questions to data sources early?",
                    "options": [
                        "To waste time",
                        "To identify data gaps and feasibility before starting analysis",
                        "It is not useful",
                        "To confuse stakeholders",
                    ],
                    "answer": 1,
                    "explanation": "Early mapping reveals whether you have the data needed to answer the question.",
                },
                {
                    "text": "What is the analyst's role in decision-making?",
                    "options": [
                        "To make all decisions",
                        "To provide insights that inform stakeholder decisions",
                        "To avoid stakeholders",
                        "To only create charts",
                    ],
                    "answer": 1,
                    "explanation": "Analysts provide data-driven insights; stakeholders make the final decisions.",
                },
            ],
            2: [
                {
                    "text": "Which function is most suitable for summing values that meet a condition in Excel/Sheets?",
                    "options": ["SUM", "SUMIF/SUMIFS", "COUNT", "AVERAGE"],
                    "answer": 1,
                    "explanation": "SUMIF/SUMIFS let you sum values that meet criteria.",
                },
                {
                    "text": "What is a common use of VLOOKUP or XLOOKUP?",
                    "options": [
                        "Sort a table",
                        "Join information from another table based on a key",
                        "Delete duplicates",
                        "Create a chart",
                    ],
                    "answer": 1,
                    "explanation": "Lookups retrieve related data from another table.",
                },
                {
                    "text": "What is a pivot table used for?",
                    "options": [
                        "Deleting data",
                        "Summarizing and aggregating data by categories",
                        "Encrypting files",
                        "Creating databases",
                    ],
                    "answer": 1,
                    "explanation": "Pivot tables quickly summarize large datasets by grouping and aggregating.",
                },
                {
                    "text": "Which formula would you use to count non-empty cells?",
                    "options": ["SUM", "COUNTA", "AVERAGE", "MAX"],
                    "answer": 1,
                    "explanation": "COUNTA counts cells that contain any type of data.",
                },
                {
                    "text": "What is conditional formatting used for?",
                    "options": [
                        "Deleting rows",
                        "Highlighting cells based on their values",
                        "Creating new sheets",
                        "Printing documents",
                    ],
                    "answer": 1,
                    "explanation": "Conditional formatting visually highlights data based on rules.",
                },
                {
                    "text": "Why clean data before analysis?",
                    "options": [
                        "To make files larger",
                        "To ensure accuracy and reliability of results",
                        "It is not necessary",
                        "To slow down work",
                    ],
                    "answer": 1,
                    "explanation": "Clean data prevents errors and ensures trustworthy analysis.",
                },
                {
                    "text": "What does INDEX/MATCH do?",
                    "options": [
                        "Deletes data",
                        "Performs flexible lookups more powerful than VLOOKUP",
                        "Creates charts",
                        "Sorts tables",
                    ],
                    "answer": 1,
                    "explanation": "INDEX/MATCH offers more flexibility than VLOOKUP for lookups.",
                },
                {
                    "text": "How do you handle duplicate rows?",
                    "options": [
                        "Always keep them",
                        "Investigate and remove if they represent the same record",
                        "Delete every other row",
                        "Ignore them",
                    ],
                    "answer": 1,
                    "explanation": "Duplicates should be investigated and removed if they're genuine repeats.",
                },
                {
                    "text": "What is data validation in spreadsheets?",
                    "options": [
                        "Deleting all data",
                        "Setting rules to control what data can be entered in cells",
                        "Creating charts",
                        "Printing sheets",
                    ],
                    "answer": 1,
                    "explanation": "Data validation prevents incorrect data entry by enforcing rules.",
                },
            ],
            3: [
                {
                    "text": "Which SQL clause is used to combine rows from two tables based on a key?",
                    "options": ["GROUP BY", "JOIN", "ORDER BY", "WHERE"],
                    "answer": 1,
                    "explanation": "JOIN combines rows from different tables using key columns.",
                },
                {
                    "text": "Which query pattern is most suitable for computing revenue per region?",
                    "options": [
                        "SELECT * FROM table",
                        "SELECT region, SUM(revenue) FROM table GROUP BY region",
                        "DELETE FROM table",
                        "UPDATE table",
                    ],
                    "answer": 1,
                    "explanation": "GROUP BY with SUM aggregates revenue per region.",
                },
                {
                    "text": "What does the WHERE clause do?",
                    "options": [
                        "Sorts results",
                        "Filters rows based on conditions",
                        "Joins tables",
                        "Creates tables",
                    ],
                    "answer": 1,
                    "explanation": "WHERE filters rows that meet specified conditions.",
                },
                {
                    "text": "Which aggregate function calculates the average?",
                    "options": ["SUM", "AVG", "COUNT", "MAX"],
                    "answer": 1,
                    "explanation": "AVG calculates the arithmetic mean of a column.",
                },
                {
                    "text": "What is a primary key?",
                    "options": [
                        "A password",
                        "A unique identifier for each row in a table",
                        "A type of chart",
                        "A database name",
                    ],
                    "answer": 1,
                    "explanation": "Primary keys uniquely identify each record in a table.",
                },
                {
                    "text": "What does DISTINCT do in SQL?",
                    "options": [
                        "Sorts results",
                        "Returns only unique values, removing duplicates",
                        "Deletes rows",
                        "Creates indexes",
                    ],
                    "answer": 1,
                    "explanation": "DISTINCT eliminates duplicate rows from query results.",
                },
                {
                    "text": "Which JOIN type keeps all rows from the left table?",
                    "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"],
                    "answer": 1,
                    "explanation": "LEFT JOIN keeps all left table rows, matching or NULL from right.",
                },
                {
                    "text": "What is the ORDER BY clause used for?",
                    "options": [
                        "Filtering rows",
                        "Sorting query results",
                        "Joining tables",
                        "Aggregating data",
                    ],
                    "answer": 1,
                    "explanation": "ORDER BY sorts results in ascending or descending order.",
                },
                {
                    "text": "Why use aliases in SQL?",
                    "options": [
                        "To delete data",
                        "To give tables or columns temporary names for readability",
                        "To encrypt queries",
                        "To slow down queries",
                    ],
                    "answer": 1,
                    "explanation": "Aliases make queries more readable and concise.",
                },
            ],
            4: [
                {
                    "text": "What is the main purpose of a BI dashboard?",
                    "options": [
                        "To store raw data",
                        "To present key metrics and trends in a way decision-makers can act on",
                        "To replace all databases",
                        "To hide information",
                    ],
                    "answer": 1,
                    "explanation": "Dashboards summarise information for quick understanding and action.",
                },
                {
                    "text": "Which is usually better for a top-level KPI chart?",
                    "options": [
                        "A cluttered 3D chart with many colours",
                        "A simple, clearly labelled bar or line chart",
                        "A table with every raw row",
                        "A pie chart with 20 slices",
                    ],
                    "answer": 1,
                    "explanation": "Simple, clear charts support faster understanding.",
                },
                {
                    "text": "What is data storytelling?",
                    "options": [
                        "Making up data",
                        "Presenting data in a narrative that guides audience to insights",
                        "Only using text",
                        "Hiding negative results",
                    ],
                    "answer": 1,
                    "explanation": "Data storytelling combines data, visuals, and narrative effectively.",
                },
                {
                    "text": "Which chart type is best for showing parts of a whole?",
                    "options": ["Line chart", "Pie chart or stacked bar", "Scatter plot", "Histogram"],
                    "answer": 1,
                    "explanation": "Pie charts and stacked bars show proportions of a total.",
                },
                {
                    "text": "What is chart junk?",
                    "options": [
                        "Old charts",
                        "Unnecessary decorations that distract from the message",
                        "Accurate data",
                        "Multiple data series",
                    ],
                    "answer": 1,
                    "explanation": "Chart junk includes clutter like 3D effects that don't add value.",
                },
                {
                    "text": "Why use filters in dashboards?",
                    "options": [
                        "To delete data",
                        "To let users explore data by different dimensions",
                        "To slow down loading",
                        "Filters are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Filters enable interactive exploration of data.",
                },
                {
                    "text": "What makes a dashboard effective?",
                    "options": [
                        "As many charts as possible",
                        "Clear focus on key metrics with actionable insights",
                        "Complex visualizations",
                        "No labels",
                    ],
                    "answer": 1,
                    "explanation": "Effective dashboards focus on key metrics and support decisions.",
                },
                {
                    "text": "When should you use a line chart?",
                    "options": [
                        "For categorical comparisons",
                        "For showing trends over time",
                        "For parts of a whole",
                        "Never",
                    ],
                    "answer": 1,
                    "explanation": "Line charts excel at showing changes over time.",
                },
                {
                    "text": "What is the purpose of dashboard annotations?",
                    "options": [
                        "To make dashboards slower",
                        "To provide context and highlight important events",
                        "To hide data",
                        "Annotations are not useful",
                    ],
                    "answer": 1,
                    "explanation": "Annotations add context like product launches or policy changes.",
                },
            ],
            5: [
                {
                    "text": "In Python/Pandas, which object represents a table of rows and columns?",
                    "options": ["Series", "DataFrame", "List", "Dict"],
                    "answer": 1,
                    "explanation": "A DataFrame is the core table structure for tabular data.",
                },
                {
                    "text": "Which is a good use of Python for analysts?",
                    "options": [
                        "Replacing all SQL and spreadsheets immediately",
                        "Automating repetitive reports and heavier data transforms",
                        "Configuring servers",
                        "Designing hospital buildings",
                    ],
                    "answer": 1,
                    "explanation": "Python is great for automation and more complex analysis.",
                },
                {
                    "text": "What is the pandas library used for?",
                    "options": [
                        "Creating websites",
                        "Data manipulation and analysis",
                        "3D graphics",
                        "Audio processing",
                    ],
                    "answer": 1,
                    "explanation": "Pandas is the primary Python library for data analysis.",
                },
                {
                    "text": "How do you read a CSV file in pandas?",
                    "options": [
                        "pd.open_csv()",
                        "pd.read_csv()",
                        "pd.load_csv()",
                        "pd.import_csv()",
                    ],
                    "answer": 1,
                    "explanation": "pd.read_csv() is the standard method to load CSV files.",
                },
                {
                    "text": "What does df.groupby() do?",
                    "options": [
                        "Deletes rows",
                        "Groups data by specified columns for aggregation",
                        "Sorts data",
                        "Creates new columns",
                    ],
                    "answer": 1,
                    "explanation": "groupby() groups data for aggregations like sum, mean, count.",
                },
                {
                    "text": "Which library is commonly used for visualization in Python?",
                    "options": ["pandas", "matplotlib or seaborn", "numpy", "requests"],
                    "answer": 1,
                    "explanation": "Matplotlib and seaborn are popular for creating charts.",
                },
                {
                    "text": "What is a Jupyter notebook?",
                    "options": [
                        "A physical notebook",
                        "An interactive environment for code, text, and visualizations",
                        "A database",
                        "A spreadsheet",
                    ],
                    "answer": 1,
                    "explanation": "Jupyter notebooks combine code, output, and documentation.",
                },
                {
                    "text": "How do you filter rows in pandas?",
                    "options": [
                        "df.delete()",
                        "df[df['column'] > value]",
                        "df.remove()",
                        "df.filter_all()",
                    ],
                    "answer": 1,
                    "explanation": "Boolean indexing filters rows based on conditions.",
                },
                {
                    "text": "What is the advantage of Python over spreadsheets?",
                    "options": [
                        "Python is always easier",
                        "Python handles larger datasets and enables automation",
                        "Spreadsheets are obsolete",
                        "There is no advantage",
                    ],
                    "answer": 1,
                    "explanation": "Python scales better and automates repetitive tasks.",
                },
            ],
            6: [
                {
                    "text": "Which of the following is a KPI?",
                    "options": [
                        "A random data column",
                        "Monthly conversion rate for a signup funnel",
                        "The file name of a report",
                        "The number of columns in a table",
                    ],
                    "answer": 1,
                    "explanation": "KPIs are metrics linked directly to important outcomes.",
                },
                {
                    "text": "In an A/B test, conversion rate is usually defined as:",
                    "options": [
                        "conversions / total_users",
                        "total_users / conversions",
                        "revenue / conversions",
                        "revenue / total_users",
                    ],
                    "answer": 0,
                    "explanation": "Conversion rate is conversions divided by total users or visits.",
                },
                {
                    "text": "What is a KPI?",
                    "options": [
                        "A type of chart",
                        "A Key Performance Indicator measuring business objectives",
                        "A database query",
                        "A spreadsheet formula",
                    ],
                    "answer": 1,
                    "explanation": "KPIs are metrics that track progress toward business goals.",
                },
                {
                    "text": "What is statistical significance in A/B testing?",
                    "options": [
                        "The size of the difference",
                        "Confidence that the difference is not due to random chance",
                        "The number of users",
                        "The test duration",
                    ],
                    "answer": 1,
                    "explanation": "Significance indicates the result is unlikely to be random.",
                },
                {
                    "text": "Why define success metrics before starting an A/B test?",
                    "options": [
                        "To waste time",
                        "To ensure you measure what matters and avoid bias",
                        "It is not necessary",
                        "To confuse stakeholders",
                    ],
                    "answer": 1,
                    "explanation": "Pre-defining metrics prevents cherry-picking results.",
                },
                {
                    "text": "What is a vanity metric?",
                    "options": [
                        "A useful business metric",
                        "A metric that looks good but doesn't drive decisions",
                        "A KPI",
                        "An accurate measurement",
                    ],
                    "answer": 1,
                    "explanation": "Vanity metrics (like total page views) don't inform actionable decisions.",
                },
                {
                    "text": "How long should you run an A/B test?",
                    "options": [
                        "One hour",
                        "Long enough to reach statistical significance and account for weekly patterns",
                        "Forever",
                        "It doesn't matter",
                    ],
                    "answer": 1,
                    "explanation": "Tests need sufficient data and should cover full business cycles.",
                },
                {
                    "text": "What is segmentation in metrics?",
                    "options": [
                        "Deleting data",
                        "Breaking down metrics by different groups (e.g., region, age)",
                        "Creating charts",
                        "Encrypting data",
                    ],
                    "answer": 1,
                    "explanation": "Segmentation reveals how metrics vary across different groups.",
                },
                {
                    "text": "What is the control group in an A/B test?",
                    "options": [
                        "The group that gets the new version",
                        "The group that gets the current/baseline version",
                        "A random sample",
                        "The largest group",
                    ],
                    "answer": 1,
                    "explanation": "The control group experiences the current version for comparison.",
                },
            ],
            7: [
                {
                    "text": "Which deliverable is most important for your analyst capstone?",
                    "options": [
                        "Only the raw data",
                        "A clear notebook/report + dashboard + README explaining the project",
                        "A screenshot of your IDE",
                        "Only a list of formulas",
                    ],
                    "answer": 1,
                    "explanation": "Employers want to see a complete, documented project they can understand.",
                },
                {
                    "text": "Why should you state limitations in your capstone report?",
                    "options": [
                        "To make the report longer",
                        "To show honest judgement about where the analysis is strong or weak",
                        "To hide problems",
                        "It is not useful",
                    ],
                    "answer": 1,
                    "explanation": "Being transparent about limits builds trust and shows maturity.",
                },
                {
                    "text": "What should a capstone README include?",
                    "options": [
                        "Only your name",
                        "Problem, data, methods, results, and how to reproduce",
                        "Random notes",
                        "Nothing",
                    ],
                    "answer": 1,
                    "explanation": "A good README tells the complete story and enables reproduction.",
                },
                {
                    "text": "Why create a portfolio of analyst projects?",
                    "options": [
                        "To waste time",
                        "To demonstrate skills to potential employers",
                        "Portfolios are not useful",
                        "To hide your work",
                    ],
                    "answer": 1,
                    "explanation": "Portfolios showcase your practical skills and problem-solving ability.",
                },
                {
                    "text": "What makes a dataset suitable for a capstone?",
                    "options": [
                        "It has only 5 rows",
                        "It is realistic, documented, and relevant to business problems",
                        "It has no challenges",
                        "It is completely random",
                    ],
                    "answer": 1,
                    "explanation": "Good capstone datasets are realistic and allow you to demonstrate skills.",
                },
                {
                    "text": "How should you present findings to non-technical stakeholders?",
                    "options": [
                        "Use maximum technical jargon",
                        "Use plain language with clear visuals and actionable insights",
                        "Only show code",
                        "Avoid explanations",
                    ],
                    "answer": 1,
                    "explanation": "Non-technical audiences need clear, jargon-free explanations.",
                },
                {
                    "text": "What is the purpose of an analyst capstone?",
                    "options": [
                        "To memorize formulas",
                        "To demonstrate end-to-end analysis skills on a realistic problem",
                        "To avoid learning",
                        "To pass time",
                    ],
                    "answer": 1,
                    "explanation": "Capstones showcase your ability to tackle real problems independently.",
                },
                {
                    "text": "Which is more valuable: breadth or depth in a capstone?",
                    "options": [
                        "Breadth - cover everything superficially",
                        "Depth - do one problem well with rigorous methods",
                        "Neither matters",
                        "Only breadth",
                    ],
                    "answer": 1,
                    "explanation": "Employers value depth and rigor over superficial coverage.",
                },
                {
                    "text": "Where should you host your analyst portfolio?",
                    "options": [
                        "Keep it only on your laptop",
                        "GitHub with clear READMEs and documentation",
                        "Never share it",
                        "Only on paper",
                    ],
                    "answer": 1,
                    "explanation": "GitHub makes your work accessible and demonstrates technical proficiency.",
                },
            ],
        }

        qs = questions.get(quiz_unit, [])
        answers = []
        for idx, q in enumerate(qs, start=1):
            st.markdown(f"**Q{idx}. {q['text']}**")
            choice = st.radio(
                label=f"da_u{quiz_unit}_q{idx}",
                options=list(range(len(q["options"]))),
                format_func=lambda i, opts=q["options"]: opts[i],
                key=f"da_quiz_u{quiz_unit}_q{idx}",
            )
            answers.append(choice)

        if qs and st.button("Mark Data Analyst quiz", key="da_quiz_mark"):
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
            """This area will host study plans, unit checklists and portfolio guides
for the Data Analyst Pathway.
"""
        )

        st.markdown("---")
        st.markdown("### 📥 Download core documents as PDF")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button("📥 Study plan PDF", key="da_study_plan_pdf"):
                study_plan_md = """# Data Analyst Pathway – 8–10 Week Study Plan

Suggested week-by-week guide covering Units 1–7 with reading, labs and
portfolio milestones.

---

## Week 1 – Unit 1: Data & Business Questions for Analysts

- Explore analyst role examples across sectors.
- Practise rewriting vague stakeholder questions into clear, measurable
  questions.
- Map questions to potential data sources.

## Week 2 – Unit 2: Spreadsheet Skills for Analysis

- Clean a messy spreadsheet into a tidy table.
- Practise key formulas and lookups.
- Build a small KPI mini-dashboard.

## Weeks 3–4 – Unit 3: SQL for Data Analysts

- Learn core SELECT/WHERE/ORDER BY queries.
- Join tables to answer realistic questions.
- Create a simple "weekly metrics" SQL script.

## Week 5 – Unit 4: BI Dashboards & Storytelling

- Design a small interactive dashboard.
- Write short narratives for each key chart.

## Week 6 – Unit 5: Python for Analysts

- Recreate one report from spreadsheets/SQL using Python + Pandas.
- Practise basic plotting.

## Week 7 – Unit 6: Metrics, A/B Tests & KPI Design

- Define KPIs for a chosen service/product.
- Analyse a small A/B test and interpret results.

## Weeks 8–10 – Unit 7: Data Analyst Capstone Project

- Choose a realistic dataset and problem.
- Complete an end-to-end analysis and dashboard.
- Prepare a report/slide deck and portfolio artifacts.
"""
                pdf = create_unit_pdf(0, "Data Analyst Study Plan", study_plan_md)
                st.download_button(
                    label="Download Study Plan PDF",
                    data=pdf,
                    file_name="Data_Analyst_Pathway_Study_Plan.pdf",
                    mime="application/pdf",
                    key="da_study_plan_pdf_dl",
                )

        with col_b:
            if st.button("📥 Unit checklists PDF", key="da_checklists_pdf"):
                checklists_md = """# Data Analyst Pathway – Unit Checklists

Use these checklists to track your progress. They are guidance, not
formal assessment criteria.

---

## Unit 1 – Data & Business Questions for Analysts

- [ ] I can describe what a data analyst does in plain language.
- [ ] I can turn vague stakeholder requests into clear questions.
- [ ] I can map questions to likely data sources.

## Unit 2 – Spreadsheet Skills for Analysis

- [ ] I can clean a messy sheet into a tidy table.
- [ ] I can use SUMIFS/COUNTIFS and lookups for common tasks.
- [ ] I can build a small dashboard using pivots/charts.

## Unit 3 – SQL for Data Analysts

- [ ] I can write SELECT/WHERE/ORDER BY queries.
- [ ] I can join tables and compute grouped metrics.
\n+## Unit 4 – BI Dashboards & Storytelling

- [ ] I can design a dashboard layout that answers specific questions.
- [ ] I can write short narratives to go with key visuals.

## Unit 5 – Python for Analysts

- [ ] I can load data into Pandas and perform basic cleaning.
- [ ] I can recreate simple reports in Python.

## Unit 6 – Metrics, A/B Tests & KPI Design

- [ ] I can define sensible KPIs for a process or product.
- [ ] I can interpret a simple A/B test and communicate results.

## Unit 7 – Data Analyst Capstone Project

- [ ] I have completed an end-to-end analysis suitable for my portfolio.
- [ ] I have a notebook/script, dashboard and written summary.
"""
                pdf = create_unit_pdf(0, "Data Analyst Unit Checklists", checklists_md)
                st.download_button(
                    label="Download Checklists PDF",
                    data=pdf,
                    file_name="Data_Analyst_Pathway_Unit_Checklists.pdf",
                    mime="application/pdf",
                    key="da_checklists_pdf_dl",
                )

        with col_c:
            if st.button("📥 Portfolio guide PDF", key="da_portfolio_pdf"):
                portfolio_md = """# Data Analyst Pathway – Portfolio Guide

This guide helps you turn labs and the capstone into a job-ready
portfolio.

## 1. Core artefacts to include

- Selected lab notebooks/reports showcasing spreadsheets, SQL, BI and
  Python.
- A strong capstone project with README and clear structure.

## 2. Suggested GitHub structure

- `analyst_capstone/` with notebooks/data/README.
- `unit_labs/` grouped by topic (spreadsheets, SQL, BI, Python).

## 3. Writing good READMEs and case studies

- Problem, data, methods, key insights, limitations.

## 4. Linking portfolio to CV and LinkedIn

- Add a "Projects" section with links and short summaries.
"""
                pdf = create_unit_pdf(0, "Data Analyst Portfolio Guide", portfolio_md)
                st.download_button(
                    label="Download Portfolio Guide PDF",
                    data=pdf,
                    file_name="Data_Analyst_Pathway_Portfolio_Guide.pdf",
                    mime="application/pdf",
                    key="da_portfolio_pdf_dl",
                )

        st.markdown("---")
        st.markdown("### 💼 Career Preparation Package")
        st.success(
            "**NEW!** Comprehensive job search toolkit - Resume templates, "
            "200+ interview questions, LinkedIn guide, and career strategies!"
        )
        
        if st.button("📥 Career Prep Package (Data Analyst Edition)", key="da_career_prep_pdf"):
            # Using same comprehensive career prep content
            from data_science_foundations_module import create_career_prep_content
            career_prep_md = """# Career Prep Package - Land Your Data Analyst Job

**Comprehensive toolkit for Data Analyst job search success**

---

## 📄 DATA ANALYST RESUME TEMPLATE

```
[YOUR NAME]
Data Analyst
Email: your.email@example.com | LinkedIn: linkedin.com/in/yourname
Portfolio: github.com/yourname

PROFESSIONAL SUMMARY
Data Analyst with expertise in SQL, Excel, and business intelligence tools.
Completed comprehensive training in data analysis, visualization, and
stakeholder communication. Strong ability to translate business questions
into actionable insights using data.

TECHNICAL SKILLS
• Analysis: SQL, Excel (Advanced: Pivot Tables, VLOOKUP, Power Query)
• Visualization: Tableau/Power BI, Python (Matplotlib, Seaborn)
• Programming: Python (Pandas, NumPy), basic R
• Databases: MySQL, PostgreSQL
• Skills: Data Cleaning, KPI Design, A/B Testing, Dashboard Creation,
  Business Intelligence, Statistical Analysis

KEY PROJECTS

Business Analytics Capstone | [Date]
• Analyzed 50,000+ transaction records to identify revenue drivers
• Created interactive dashboard tracking 12 key business metrics
• Presented findings to stakeholders with 3 actionable recommendations
• Tools: SQL, Tableau, Excel
• GitHub: [link]

KPI Dashboard Project | [Date]
• Designed and built weekly metrics dashboard for e-commerce business
• Automated data refresh using SQL queries
• Reduced reporting time from 4 hours to 15 minutes
• Improved decision-making with real-time visibility

SQL Analysis Project | [Date]
• Wrote complex queries across 5 related tables
• Analyzed customer behavior patterns
• Identified top 10 customer segments for targeted marketing
• Presented insights with clear visualizations

EDUCATION & CERTIFICATIONS
• Data Analyst Pathway Certification | [Date]
  - SQL, Excel, BI Tools, Python for Analysis
  - 400+ hours hands-on training
  - Portfolio of real-world projects

[Your Previous Education/Experience]
```

---

## 💼 TOP 60 DATA ANALYST INTERVIEW QUESTIONS & ANSWERS

### SQL Questions (15 Essential)

**Q1: What is the difference between WHERE and HAVING?**
A: WHERE filters individual rows before grouping; HAVING filters groups
after aggregation.
Example:
```sql
SELECT department, AVG(salary)
FROM employees
WHERE active = 1  -- Filter rows first
GROUP BY department
HAVING AVG(salary) > 50000;  -- Filter groups
```

**Q2: Write a query to find top 5 customers by revenue.**
```sql
SELECT customer_id, customer_name, SUM(order_amount) as total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY customer_id, customer_name
ORDER BY total_revenue DESC
LIMIT 5;
```

**Q3: Explain INNER JOIN vs LEFT JOIN with business examples.**
A:
- INNER JOIN: Only customers who placed orders
- LEFT JOIN: All customers, including those who haven't ordered
Use LEFT JOIN to find customers who NEVER ordered (WHERE order_id IS NULL)

**Q4: How do you find duplicate rows?**
```sql
SELECT email, COUNT(*) as count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```

**Q5: Calculate month-over-month growth.**
```sql
WITH monthly_sales AS (
  SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(amount) as revenue
  FROM orders
  GROUP BY month
)
SELECT 
  month,
  revenue,
  LAG(revenue) OVER (ORDER BY month) as prev_month,
  (revenue - LAG(revenue) OVER (ORDER BY month)) / 
    LAG(revenue) OVER (ORDER BY month) * 100 as growth_pct
FROM monthly_sales;
```

**Q6: What are window functions?**
A: Perform calculations across rows related to current row without grouping.
```sql
SELECT 
  employee_name,
  salary,
  RANK() OVER (ORDER BY salary DESC) as salary_rank,
  AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;
```

**Q7: How to optimize slow SQL queries?**
- Add indexes on WHERE/JOIN columns
- Avoid SELECT *, specify needed columns
- Use EXPLAIN to analyze query execution
- Limit result set size
- Avoid functions on indexed columns in WHERE

**Q8: Explain GROUP BY and aggregations.**
A: Groups rows with same values for summary calculations
```sql
SELECT region, product_category,
       COUNT(*) as orders,
       SUM(revenue) as total_revenue,
       AVG(revenue) as avg_order_value
FROM sales
GROUP BY region, product_category;
```

**Q9: What is a subquery? When to use it?**
A: Query nested inside another query.
```sql
-- Find customers who spent more than average
SELECT customer_name, total_spent
FROM customers
WHERE total_spent > (SELECT AVG(total_spent) FROM customers);
```

**Q10: How to handle NULL values?**
- IS NULL / IS NOT NULL for filtering
- COALESCE(column, 0) for default values
- IFNULL() or NULLIF() functions

**Q11: UNION vs UNION ALL?**
- UNION: Combines results, removes duplicates (slower)
- UNION ALL: Combines results, keeps duplicates (faster)

**Q12: Create a running total.**
```sql
SELECT 
  date,
  daily_sales,
  SUM(daily_sales) OVER (ORDER BY date) as running_total
FROM sales;
```

**Q13: Find second highest salary.**
```sql
SELECT MAX(salary) as second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
-- OR using DENSE_RANK
SELECT DISTINCT salary
FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
  FROM employees
) ranked
WHERE rank = 2;
```

**Q14: Explain CTEs (Common Table Expressions).**
A: Named temporary result set for readability.
```sql
WITH top_customers AS (
  SELECT customer_id, SUM(amount) as total
  FROM orders
  GROUP BY customer_id
  HAVING SUM(amount) > 1000
)
SELECT c.name, tc.total
FROM top_customers tc
JOIN customers c ON tc.customer_id = c.id;
```

**Q15: DELETE vs TRUNCATE vs DROP?**
- DELETE: Remove specific rows, can rollback, triggers fire
- TRUNCATE: Remove all rows, fast, can't rollback, no triggers
- DROP: Delete entire table structure

### Excel Questions (10 Essential)

**Q16: Key Excel functions for analysts?**
- VLOOKUP/XLOOKUP: Lookup data across tables
- SUMIFS/COUNTIFS: Conditional aggregation
- IF/IFS: Logic
- PIVOT TABLES: Summarize data
- INDEX/MATCH: Flexible lookups
- TEXT functions: CONCATENATE, LEFT, RIGHT, MID
- Date functions: DATE, MONTH, YEAR, EOMONTH

**Q17: Explain VLOOKUP.**
```
=VLOOKUP(lookup_value, table_range, col_index, FALSE)
Example: =VLOOKUP(A2, Products!A:D, 3, FALSE)
Finds A2 in Products sheet, returns 3rd column value
```

**Q18: VLOOKUP vs INDEX/MATCH?**
INDEX/MATCH is more flexible:
- Can look left
- Doesn't break when columns inserted
- Faster for large datasets

**Q19: Create a dynamic dashboard in Excel.**
- Use PIVOT TABLES for summaries
- Add SLICERS for filtering
- Use conditional formatting
- Create charts linked to pivots
- Use named ranges for flexibility

**Q20: How to remove duplicates?**
- Data > Remove Duplicates
- Advanced Filter with Unique Records Only
- COUNTIFS to identify duplicates

**Q21: What are Power Query and Power Pivot?**
- Power Query: ETL tool for data transformation
- Power Pivot: Data modeling and relationships

**Q22: Explain pivot tables.**
A: Interactive summary tables that aggregate data
- Rows: Dimensions to group by
- Values: Metrics to calculate
- Filters: Subset data
- Columns: Additional grouping

**Q23: Key Excel shortcuts for analysts?**
- Ctrl+T: Create table
- Alt+N+V: Insert Pivot Table
- Ctrl+Arrow: Navigate to data edges
- Ctrl+Shift+L: Add filters
- F4: Toggle absolute references

**Q24: Handle errors in formulas?**
Use IFERROR:
```
=IFERROR(A1/B1, 0)  -- Returns 0 if division error
=IFERROR(VLOOKUP(...), "Not Found")
```

**Q25: Calculate growth percentage?**
```
=(New Value - Old Value) / Old Value * 100
=IFERROR((B2-A2)/A2, 0)  -- Handle division by zero
```

### Visualization & BI Questions (10)

**Q26: When to use each chart type?**
- Bar/Column: Compare categories
- Line: Show trends over time
- Pie: Show composition (use sparingly!)
- Scatter: Show correlation
- Heatmap: Show patterns in matrix
- Histogram: Show distribution

**Q27: What makes a good dashboard?**
- Clear purpose and audience
- Key metrics prominent
- Consistent design
- Interactive filters
- Mobile-friendly
- Fast load times

**Q28: Explain KPIs.**
A: Key Performance Indicators - measurable values showing performance
Examples:
- Revenue growth %
- Customer churn rate
- Average order value
- Conversion rate

**Q29: Dashboard design best practices?**
- Follow visual hierarchy
- Use consistent colors
- Avoid chart junk
- Provide context (comparisons, benchmarks)
- Make it actionable

**Q30: How to choose the right visualization?**
1. What question am I answering?
2. What's the data type (categorical, time-series, etc.)?
3. What comparison am I making?
4. Who is the audience?

**Q31: Tableau vs Power BI?**
- Tableau: More advanced visualizations, better for exploration
- Power BI: Better Microsoft integration, more affordable
- Both: Excellent for business intelligence

**Q32: What is data storytelling?**
A: Presenting data insights as a narrative
- Context: Why does this matter?
- Conflict: What's the problem?
- Resolution: What should we do?

**Q33: How to present to non-technical stakeholders?**
- Avoid jargon
- Use simple visuals
- Focus on business impact
- Provide clear recommendations
- Use analogies

**Q34: Common visualization mistakes?**
- 3D charts (distort perception)
- Dual axes with different scales
- Too many colors
- Unclear labels
- Starting Y-axis at non-zero (for bar charts)

**Q35: What is exploratory vs explanatory analysis?**
- Exploratory: You explore data to find insights
- Explanatory: You explain insights to others

### Business/Scenario Questions (15)

**Q36: How would you analyze declining sales?**
1. Segment analysis (by product, region, customer type, time)
2. Compare to historical patterns (seasonality?)
3. Check external factors (competition, economy, marketing changes)
4. Look for data quality issues
5. Identify specific drivers
6. Recommend actions

**Q37: Walk through your analysis process.**
1. Understand the business question
2. Identify data sources needed
3. Clean and validate data
4. Explore and analyze
5. Create visualizations
6. Draw conclusions
7. Present recommendations

**Q38: Metric increased 20% - good or bad?**
Need context:
- What's the baseline? (20% of what?)
- Timeframe? (Day? Month? Year?)
- Statistical significance?
- Any external changes?
- How does it compare to targets?
- What about other related metrics?

**Q39: How do you prioritize analysis requests?**
- Business impact
- Urgency
- Effort required
- Stakeholder importance
- Data availability

**Q40: Describe a time you found an unexpected insight.**
Use STAR method:
- Situation: What was the context?
- Task: What were you analyzing?
- Action: What did you discover and how?
- Result: What was the business impact?

**Q41: How to measure marketing campaign success?**
Define KPIs:
- Reach: Impressions, clicks
- Engagement: CTR, time on site
- Conversion: Leads, sales
- ROI: Revenue vs cost
- Attribution: Which touchpoint drove conversion?

**Q42: How would you identify customer churn?**
1. Define churn (no purchase in X days, cancellation, etc.)
2. Calculate churn rate
3. Segment analysis (who churns more?)
4. Identify leading indicators
5. Predict at-risk customers
6. Recommend retention strategies

**Q43: What metrics matter for e-commerce?**
- Conversion rate
- Average order value
- Customer lifetime value
- Cart abandonment rate
- Traffic sources
- Product performance
- Customer acquisition cost

**Q44: How do you ensure data quality?**
- Validate sources
- Check for duplicates
- Handle missing values appropriately
- Verify calculations
- Cross-reference with other sources
- Document assumptions
- Peer review

**Q45: Conflicting data sources - what do you do?**
1. Investigate why they differ
2. Check data definitions
3. Verify extraction logic
4. Validate with business owners
5. Document the issue
6. Choose most reliable source
7. Monitor going forward

**Q46: How to build a dashboard for executives?**
- High-level KPIs prominent
- Drill-down capability
- Period comparisons (YoY, MoM)
- Alerts for unusual patterns
- Mobile-accessible
- Auto-refresh

**Q47: Explain A/B testing to a non-technical person.**
"We show version A to half our users and version B to the other half,
then measure which performs better. Like testing two recipes to see
which tastes better, but with data!"

**Q48: How do you handle tight deadlines?**
- Clarify priorities and scope
- Use existing templates/code
- Focus on key insights, not perfection
- Communicate early if delays likely
- Deliver iteratively

**Q49: What questions do you ask stakeholders?**
- What business decision will this analysis inform?
- What specific questions need answering?
- What's the timeline?
- Who's the audience?
- What data sources are available?
- What does success look like?

**Q50: How do you stay current with tools/techniques?**
- Online courses (Coursera, Udemy)
- Industry blogs and newsletters
- LinkedIn learning
- Practice projects
- Community forums
- Conferences/webinars

### Python/Pandas for Analysts (10)

**Q51: When to use Python vs Excel?**
Excel: Quick analysis, stakeholders use Excel, small datasets
Python: Large datasets, automation, complex analysis, version control

**Q52: Basic Pandas operations?**
```python
import pandas as pd

# Read data
df = pd.read_csv('file.csv')

# Explore
df.head()
df.info()
df.describe()

# Filter
df[df['sales'] > 1000]

# Group and aggregate
df.groupby('category')['sales'].sum()

# Sort
df.sort_values('revenue', ascending=False)
```

**Q53: Handle missing values in Pandas?**
```python
df.isnull().sum()  # Check missing
df.dropna()  # Remove rows
df.fillna(0)  # Fill with value
df['col'].fillna(df['col'].mean())  # Fill with mean
```

**Q54: Merge dataframes?**
```python
pd.merge(df1, df2, on='customer_id', how='inner')
# how='left', 'right', 'outer' for different joins
```

**Q55: Create pivot table in Pandas?**
```python
df.pivot_table(
    values='sales',
    index='product',
    columns='month',
    aggfunc='sum'
)
```

**Q56: Export results?**
```python
df.to_csv('output.csv', index=False)
df.to_excel('output.xlsx', sheet_name='Results')
```

**Q57: Basic visualization?**
```python
import matplotlib.pyplot as plt

df['sales'].hist()
df.groupby('category')['revenue'].sum().plot(kind='bar')
plt.show()
```

**Q58: Filter with multiple conditions?**
```python
df[(df['sales'] > 1000) & (df['region'] == 'UK')]
# OR use query:
df.query('sales > 1000 and region == "UK"')
```

**Q59: Calculate new columns?**
```python
df['total'] = df['price'] * df['quantity']
df['growth'] = (df['2024'] - df['2023']) / df['2023'] * 100
```

**Q60: Group and calculate multiple aggregations?**
```python
df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': 'sum'
})
```

---

## 🎤 INTERVIEW PREPARATION TIPS

### Before Interview:
1. Research the company and role
2. Prepare 3-5 STAR stories
3. Practice SQL queries on paper
4. Review your project portfolio
5. Prepare questions for interviewer
6. Test your internet/video setup (for remote)

### During Interview:
1. Listen carefully to questions
2. Clarify before answering
3. Think out loud (for technical questions)
4. Use specific examples from experience
5. Show enthusiasm for data and the role
6. Ask thoughtful questions

### Common Red Flags to Avoid:
- Not asking clarifying questions
- Being unable to explain your projects
- Not knowing basic SQL/Excel
- Focusing only on tools, not business impact
- Badmouthing previous employers

### Questions to Ask Interviewer:
1. What does a typical day look like?
2. What tools and data sources does the team use?
3. How is success measured in this role?
4. What are the biggest data challenges?
5. How does analytics influence decisions here?
6. What's the team structure?
7. Opportunities for learning and growth?

---

## 💡 LINKEDIN OPTIMIZATION FOR DATA ANALYSTS

### Headline Examples:
"Data Analyst | SQL, Excel, Tableau | Transforming Data into Business Insights"
"Business Intelligence Analyst | Dashboards & KPIs | Driving Data-Driven Decisions"
"Data Analyst | E-commerce Analytics | SQL, Python, Power BI"

### About Section Template:
```
I'm a Data Analyst passionate about turning data into actionable business insights.

Recently completed comprehensive training in:
✓ SQL & Database Querying
✓ Excel & Power Query
✓ Tableau/Power BI Dashboards
✓ Python for Data Analysis
✓ KPI Design & Business Intelligence

I've built [X] end-to-end analysis projects including:
• [Project 1 - brief description]
• [Project 2 - brief description]
• [Project 3 - brief description]

I'm particularly interested in [industry/domain] analytics and solving
[specific types of business problems].

Currently seeking Data Analyst opportunities where I can leverage my skills
to drive business impact.

📧 [email]
💼 Portfolio: [GitHub]
```

### Skills to List (Top 10):
1. SQL
2. Data Analysis
3. Microsoft Excel
4. Tableau / Power BI
5. Data Visualization
6. Python (Pandas)
7. Business Intelligence
8. Statistical Analysis
9. KPI Development
10. Dashboard Design

### Activity Tips:
- Share insights from public datasets
- Comment on data visualization posts
- Write short posts about analysis techniques
- Engage with data community
- Share your projects

---

## 📧 NETWORKING EMAIL TEMPLATES

### Informational Interview Request:
```
Subject: Data Analyst seeking advice - [Your Name]

Hi [Name],

I'm [Your Name], transitioning into data analytics. I recently completed
training in SQL, Excel, and BI tools, and I'm impressed by your work at
[Company].

Would you be open to a brief 15-minute call where I could ask about your
experience in [specific area]? I'm particularly interested in learning
about [specific topic].

I understand you're busy, so I'm happy to work around your schedule.

Thank you for considering!

Best regards,
[Your Name]
```

### Application Follow-up:
```
Subject: Following up - Data Analyst Application

Hi [Name],

I applied for the Data Analyst position at [Company] on [date] and wanted
to express my continued strong interest in the role.

My background in [relevant experience] and proficiency in [SQL/Excel/BI tools]
aligns well with the requirements. I'm particularly excited about [specific
aspect of role/company].

I'd welcome the opportunity to discuss how I can contribute to [specific
team goal or initiative].

Best regards,
[Your Name]
```

---

## 30-60-90 DAY PLAN (Use in Interviews!)

### First 30 Days - Learn & Absorb
- Understand business model, products, customers
- Learn data infrastructure and tools
- Review existing dashboards and reports
- Shadow team members
- Document processes
- Build relationships with stakeholders

### Days 31-60 - Contribute
- Take ownership of recurring reports
- Identify quick wins / improvements
- Propose new analyses
- Present insights in team meetings
- Start building relationships across teams
- Complete first independent project

### Days 61-90 - Impact
- Complete major analysis project
- Present findings to leadership
- Propose process improvements
- Mentor newer analysts
- Establish yourself as go-to for specific domain
- Plan next quarter initiatives

---

## 💼 COMPLETE INTERVIEW QUESTION BANK (100+ Questions)

### SQL Technical Questions (40 questions)

**6. How do you calculate a percentile in SQL?**
```sql
SELECT customer_id, revenue,
  PERCENT_RANK() OVER (ORDER BY revenue) as percentile
FROM orders;
-- Or use NTILE for quartiles:
SELECT customer_id, revenue,
  NTILE(4) OVER (ORDER BY revenue) as quartile
FROM orders;
```

**7. Write a query to find customers who made purchases in consecutive months.**
```sql
WITH monthly_purchases AS (
  SELECT customer_id,
    DATE_TRUNC('month', order_date) as month
  FROM orders
  GROUP BY customer_id, DATE_TRUNC('month', order_date)
)
SELECT DISTINCT a.customer_id
FROM monthly_purchases a
JOIN monthly_purchases b
  ON a.customer_id = b.customer_id
  AND a.month = b.month - INTERVAL '1 month';
```

**8. How do you identify the top 20% of customers by revenue?**
```sql
SELECT customer_id, total_revenue
FROM (
  SELECT customer_id,
    SUM(revenue) as total_revenue,
    PERCENT_RANK() OVER (ORDER BY SUM(revenue) DESC) as pct_rank
  FROM orders
  GROUP BY customer_id
) ranked
WHERE pct_rank <= 0.20;
```

**9. Explain PARTITION BY vs GROUP BY.**
Answer: GROUP BY collapses rows into groups (reduces row count). PARTITION BY creates windows but keeps all rows. Use GROUP BY for aggregation reporting, PARTITION BY for row-level calculations with group context.

**10. How would you find gaps in a sequence (e.g., missing order IDs)?**
```sql
WITH numbers AS (
  SELECT MIN(order_id) + generate_series(0, MAX(order_id) - MIN(order_id)) as id
  FROM orders
)
SELECT n.id as missing_id
FROM numbers n
LEFT JOIN orders o ON n.id = o.order_id
WHERE o.order_id IS NULL;
```

### Python/Pandas Advanced (30 questions)

**6. How do you create a custom aggregation function?**
```python
def revenue_per_customer(group):
    return group['revenue'].sum() / group['customer_id'].nunique()

df.groupby('region').apply(revenue_per_customer)
```

**7. Explain the difference between merge, join, and concat.**
- merge(): SQL-style joins on columns
- join(): Joins on index
- concat(): Stacks DataFrames vertically or horizontally
```python
pd.merge(df1, df2, on='key')  # Join on column
df1.join(df2)  # Join on index
pd.concat([df1, df2], axis=0)  # Stack vertically
```

**8. How do you handle datetime operations?**
```python
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_name'] = df['date'].dt.day_name()
df['quarter'] = df['date'].dt.quarter

# Date arithmetic
df['days_since'] = (pd.Timestamp.now() - df['date']).dt.days

# Resampling time series
df.set_index('date').resample('M').sum()
```

**9. How would you detect outliers programmatically?**
```python
from scipy import stats

# Z-score method
z_scores = np.abs(stats.zscore(df['revenue']))
outliers = df[z_scores > 3]

# IQR method
Q1 = df['revenue'].quantile(0.25)
Q3 = df['revenue'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['revenue'] < Q1 - 1.5*IQR) | 
              (df['revenue'] > Q3 + 1.5*IQR)]
```

**10. Explain vectorization in pandas.**
Answer: Vectorization applies operations to entire arrays at once (C-level), avoiding Python loops. Always faster than iterating rows.
```python
# BAD (slow):
for i in range(len(df)):
    df.loc[i, 'total'] = df.loc[i, 'qty'] * df.loc[i, 'price']

# GOOD (fast):
df['total'] = df['qty'] * df['price']
```

### Statistics & A/B Testing (30 questions)

**6. Explain statistical power and why it matters.**
Answer: Power is probability of detecting an effect when it exists (1 - Type II error). Typically aim for 80% power. Low power means you might miss real effects. Affects sample size calculation.

**7. What's the difference between one-tailed and two-tailed tests?**
Answer: 
- One-tailed: Tests if effect is in specific direction (greater OR less than)
- Two-tailed: Tests if effect exists in either direction (not equal to)
- Use two-tailed unless you have strong directional hypothesis

**8. How do you calculate confidence intervals?**
```python
from scipy import stats
import numpy as np

# For means
data = [values]
confidence = 0.95
mean = np.mean(data)
se = stats.sem(data)
interval = stats.t.interval(confidence, len(data)-1, mean, se)

# For proportions
from statsmodels.stats.proportion import proportion_confint
successes = 150
total = 1000
ci = proportion_confint(successes, total, alpha=0.05, method='wilson')
```

**9. Explain Simpson's Paradox with an example.**
Answer: When trend in groups reverses when groups are combined. Example: Treatment works in men and women separately, but control "wins" overall due to unbalanced group sizes.

**10. How would you design a multivariate test?**
Answer:
- Define variants (e.g., 3 button colors × 2 headline styles = 6 combinations)
- Calculate sample size (larger than A/B test)
- Randomize users to variants
- Use Bonferroni correction for multiple comparisons
- Test interactions between factors

### Excel Questions (20 questions)

**6. Explain the difference between VLOOKUP and INDEX-MATCH.**
Answer: VLOOKUP only looks right, breaks if columns reorder, slower. INDEX-MATCH looks any direction, flexible, faster, more robust.
```excel
VLOOKUP: =VLOOKUP(A2, B:D, 3, FALSE)
INDEX-MATCH: =INDEX(D:D, MATCH(A2, B:B, 0))
```

**7. How do you create a dynamic named range?**
```excel
=OFFSET(Sheet1!$A$2, 0, 0, COUNTA(Sheet1!$A:$A)-1, 1)
```

**8. Explain calculated fields vs calculated items in pivot tables.**
Answer:
- Calculated Field: New column based on existing fields (e.g., Profit = Revenue - Cost)
- Calculated Item: New row in existing field (e.g., Q1 = Jan + Feb + Mar)

**9. How do you remove duplicates while keeping the first occurrence?**
Answer: Data → Remove Duplicates, or use advanced filter with "Unique records only"

**10. What's the fastest way to split data from one column into multiple columns?**
Answer: Data → Text to Columns, choose delimiter or fixed width, preview results, finish.

### Business & Domain Questions (20 questions)

**1. How would you measure the success of a new feature launch?**
Answer:
- Primary: Feature adoption rate (% of users who use it)
- Secondary: Engagement metrics (frequency, depth of use)
- Business: Impact on retention, revenue, or key goal
- Guardrails: No degradation in core metrics
- Timeline: Track for 30-90 days

**2. A key metric suddenly drops 20%. Walk me through your analysis.**
Answer:
1. Validate: Check data pipeline, confirm drop is real
2. Segment: By user type, platform, region, time
3. Investigate: Look for changes (releases, campaigns, external)
4. Hypothesize: Form theories for the drop
5. Test: Run queries to validate hypotheses
6. Recommend: Propose fixes or further investigation

**3. How do you prioritize competing requests from stakeholders?**
Answer:
- Business impact: Revenue/cost implications
- Urgency: Time-sensitive decisions
- Effort: Quick wins vs long projects
- Strategic alignment: Company priorities
- Data availability: Can we actually answer this?
Framework: Impact/Effort matrix

**4. Explain how you'd approach building a customer segmentation.**
Answer:
1. Define purpose: What decisions will this inform?
2. Gather data: Behavioral, demographic, transactional
3. Choose method: RFM, K-means, or business rules
4. Build segments: Run analysis, validate groups
5. Profile segments: Describe characteristics
6. Actionize: Recommend strategies per segment
7. Monitor: Track segment movement over time

**5. How would you analyze why sales are declining?**
Answer:
- Trend: Is it gradual or sudden? Seasonal?
- Segments: Which products/regions/channels affected?
- Customer behavior: Fewer customers or less per customer?
- Competition: Market share changes?
- External: Economic factors, seasonality
- Internal: Pricing, inventory, marketing changes
Build hypotheses, test with data, recommend actions.

### Behavioral Questions (STAR Method - 20 questions)

**6. Describe a time when your analysis was wrong.**
Situation: Built model predicting churn, accuracy was 75%
Task: Investigate why predictions were off
Action: Discovered data leakage (used future information), rebuilt model properly
Result: Improved to 82% accuracy, learned importance of temporal validation

**7. Tell me about a time you had to learn a new tool quickly.**
Situation: Needed to build Tableau dashboard, never used it
Task: Learn Tableau in 1 week to present to executives
Action: Completed online course, practiced with sample data, got help from colleague
Result: Delivered dashboard on time, now company standard tool

**8. How do you handle tight deadlines with incomplete data?**
Situation: CEO needed analysis by tomorrow, data had gaps
Task: Provide best answer with available information
Action: Documented assumptions, provided ranges instead of point estimates, noted limitations
Result: CEO appreciated transparency, made informed decision, got better data for next time

**9. Describe a successful collaboration with a non-technical team.**
Situation: Marketing wanted to understand campaign ROI
Task: Build attribution model they could understand
Action: Used simple last-touch model first, visualized clearly, trained team to interpret
Result: Marketing changed budget allocation, saw 15% ROI improvement

**10. Tell me about a time you found an unexpected insight.**
Situation: Analyzing customer churn, expected price sensitivity
Task: Understand real churn drivers
Action: Ran correlation analysis, found support wait time was #1 factor
Result: Company invested in support team, churn dropped 12%

---

## 🎯 PORTFOLIO OPTIMIZATION GUIDE

### GitHub Portfolio Setup

**What to Include:**
1. **3-5 Complete Projects** (quality over quantity)
   - Different domains (healthcare, retail, SaaS)
   - Various techniques (SQL, Python, dashboards)
   - Clear business impact
   
2. **Professional README for Each Project:**
```markdown
# Project Title: E-Commerce Cart Abandonment Analysis

## Business Problem
Cart abandonment rate of 68% costing $250K monthly in lost revenue.

## Approach
- Analyzed 50K transactions using SQL and Python
- Segmented by device, region, product category
- Statistical testing (chi-square, t-tests)
- Built predictive model (scikit-learn)

## Key Findings
1. Mobile users abandon 75% vs 55% desktop
2. Weekend abandonment 20% higher
3. Electronics category worst at 72%

## Recommendations
1. Optimize mobile checkout (projected 15% improvement)
2. Weekend-specific interventions
3. A/B test simplified checkout

## Impact
Projected $300K annual revenue recovery (12% improvement)

## Tech Stack
Python • pandas • scikit-learn • matplotlib • SQL • Tableau

## Links
- [Jupyter Notebook](notebooks/analysis.ipynb)
- [Interactive Dashboard](https://public.tableau.com/...)
- [Final Report PDF](reports/final_report.pdf)
```

**3. Clean Code Structure:**
```
project-name/
├── README.md (compelling overview)
├── data/ (sample data only, not sensitive)
├── notebooks/ (well-commented Jupyter)
├── src/ (modular Python scripts)
├── reports/ (PDF deliverables)
├── images/ (visualizations)
└── requirements.txt
```

**4. README Profile (GitHub Profile README):**
```markdown
# Hi, I'm [Your Name] 👋

## Data Analyst | Turning Data into Actionable Insights

I help businesses make data-driven decisions through:
- 📊 SQL for data extraction and analysis
- 🐍 Python for advanced analytics and automation
- 📈 Tableau/Power BI for compelling visualizations
- 🧪 A/B testing and experimentation

### Featured Projects
- 🏥 [Hospital DNA Rate Analysis](link) - Saved $180K annually
- 🛒 [E-Commerce Optimization](link) - 12% revenue increase
- 📱 [SaaS Churn Prediction](link) - Improved retention 8%

### Skills
SQL • Python • Tableau • Excel • Statistics • A/B Testing

### Let's Connect
[LinkedIn](link) • [Email](mailto:) • [Portfolio](link)
```

---

## 💰 SALARY NEGOTIATION GUIDE

### Research Phase

**1. Know Your Market Value:**
- Glassdoor salary ranges
- Levels.fyi for tech companies
- PayScale for general market
- LinkedIn Salary Insights
- Network (ask peers, mentors)

**Typical Ranges (UK, 2024):**
- Junior Data Analyst: £28K - £38K
- Mid-Level: £38K - £55K
- Senior: £55K - £75K+
- London: +15-25% premium

**2. Calculate Your Target:**
```
Minimum Acceptable: £X (walk away below this)
Target: £Y (what you want)
Stretch: £Z (optimistic but achievable)

Example:
Minimum: £40K
Target: £45K
Stretch: £50K
```

### Negotiation Scripts

**When They Ask Your Salary Expectations:**

❌ **Don't Say:**
"I'm currently making £35K"
"Whatever you think is fair"
"I'll take anything!"

✅ **Do Say:**
"Based on my research for Data Analyst roles in London with my skills in SQL, Python, and Tableau, I'm targeting £42-48K. But I'm flexible based on the full compensation package and growth opportunities."

**When You Receive an Offer:**

**Script 1: Negotiating Up**
"Thank you for the offer of £40K. I'm excited about the role! Based on my research and the value I'll bring (especially my SQL optimization skills and experience with similar projects), I was hoping for something closer to £45K. Is there flexibility on the base salary?"

**Script 2: Negotiating Total Package**
"I appreciate the offer. While the base of £40K is lower than my target of £45K, could we discuss:
- Sign-on bonus to bridge the gap?
- Earlier salary review (6 months instead of 12)?
- Additional training budget?
- Extra holiday days?
These would help make the package work for me."

**Script 3: Accepting with Grace**
"I'm thrilled to accept the offer of £45K. Thank you for working with me on the compensation. I'm excited to start on [date] and contribute to the team's success!"

**When to Walk Away:**
- Below your minimum acceptable
- Toxic culture signals during process
- Lack of growth opportunity
- Unreasonable demands/expectations

### Email Template - Salary Negotiation

```
Subject: Re: Job Offer - Data Analyst Role

Dear [Hiring Manager],

Thank you for extending the offer for the Data Analyst position. I'm very excited about the opportunity to join [Company] and contribute to [specific team/project].

I've reviewed the offer carefully. While I'm enthusiastic about the role, I was hoping we could discuss the compensation. Based on my research for similar Data Analyst roles in [location], combined with my experience in [specific skills: SQL, Python, visualization], I was expecting a base salary in the range of £[target-stretch].

I'm particularly excited about [specific aspect of role], and I'm confident I can deliver significant value through [specific contribution you'll make].

Would you be open to discussing a base salary of £[target]? I'm also interested in understanding:
- Performance review and raise timeline
- Professional development budget
- Any other benefits or perks

I'm flexible and eager to find a package that works for both of us. Would you be available for a brief call to discuss?

Thank you for your consideration.

Best regards,
[Your Name]
```

---

## 🤝 NETWORKING & JOB SEARCH STRATEGY

### LinkedIn Optimization

**Headline Formula:**
```
Data Analyst | [Key Skill] | [Value Proposition]

Examples:
"Data Analyst | SQL & Python | Turning Complex Data into Actionable Business Insights"
"Junior Data Analyst | Healthcare Analytics | Helping Hospitals Optimize Operations"
"Data Analyst | E-Commerce | Driving Revenue Growth Through Data-Driven Decisions"
```

**About Section Template:**
```
I help [target companies/industry] [achieve goal] through [your approach].

With expertise in SQL, Python, and Tableau, I transform complex datasets into clear, actionable insights that drive business decisions.

Recent Projects:
• Analyzed 50K+ hospital appointments to identify cost-saving opportunities ($180K annual impact)
• Built customer segmentation model improving marketing ROI by 25%
• Developed automated dashboards reducing reporting time from 8 hours to 15 minutes

Skills: SQL | Python (pandas, matplotlib) | Tableau | Excel | Statistics | A/B Testing

Currently seeking Data Analyst opportunities where I can apply my analytical skills to solve real business problems.

Let's connect! [email@example.com]
```

**Experience Section:**
Use PAR format (Problem-Action-Result):
```
Data Analyst Intern | Company Name | Dates

• Analyzed cart abandonment patterns across 50K transactions, identifying mobile users had 75% abandonment vs 55% desktop
• Built SQL queries to extract and aggregate customer behavior data, reducing manual report generation time by 80%
• Created Tableau dashboard tracking key metrics, enabling executives to make data-driven decisions resulting in 12% revenue increase
```

### Cold Outreach Scripts

**LinkedIn Message Template (after viewing their profile):**
```
Hi [Name],

I noticed you're [their role] at [Company] - congratulations on [recent achievement/post]!

I'm a Data Analyst with experience in [your niche], particularly [specific skill relevant to them]. I recently [specific accomplishment].

I'm researching opportunities in [industry/area] and would love to learn about your experience at [Company]. Would you be open to a brief 15-minute coffee chat? I'm happy to work around your schedule.

Thanks for considering!
[Your Name]
```

**Response Rate:** 15-20% (vs <5% for generic messages)

**Email Template - Hiring Manager:**
```
Subject: Data Analyst Position - [Specific Value You Bring]

Dear [Name],

I noticed [Company] is hiring for a Data Analyst position. I'm particularly drawn to [specific aspect of role/company mission].

I recently completed a project analyzing [relevant domain] data that resulted in [quantifiable outcome]. This experience directly aligns with [Company]'s focus on [their priority].

Key skills I'd bring:
• [Skill 1 relevant to job description]
• [Skill 2 with specific example]
• [Skill 3 showing impact]

I've attached my resume and would love to discuss how my analytical skills could contribute to [specific team/project/goal].

Are you available for a brief call next week?

Best regards,
[Your Name]
[LinkedIn] | [Portfolio Link] | [Email] | [Phone]

P.S. I created a sample analysis relevant to [Company]'s challenges - happy to share if you're interested!
```

### Application Strategy

**Prioritize Applications:**

**Tier 1 (Dream Jobs - 20% of effort):**
- Perfect role match
- Company you're passionate about
- Custom cover letter + portfolio piece
- Research company deeply
- Find internal referral

**Tier 2 (Good Fits - 50% of effort):**
- Strong skill match
- Good company culture
- Customized application
- Direct hiring manager reach-out

**Tier 3 (Practice - 30% of effort):**
- Decent match
- Interview practice
- Standard application
- Volume strategy

**Weekly Goal:**
- 2 Tier 1 applications (deep customization)
- 5 Tier 2 applications (moderate customization)
- 10 Tier 3 applications (light customization)
- 5 networking conversations
- 1 skills practice/project update

### Interview Preparation

**1 Week Before:**
- Research company thoroughly
- Review job description
- Prepare STAR stories (6-8 examples)
- Practice technical questions
- Prepare questions for them

**Day Before:**
- Review your application/resume
- Prepare examples to discuss
- Test video setup if virtual
- Get good sleep

**Day Of:**
- Arrive 10 minutes early (or log in 5 minutes early)
- Bring notebook, pen, resume copies
- Be ready to discuss your projects in detail

**After Interview:**
- Send thank-you email within 24 hours
- Reiterate interest and fit
- Reference specific conversation points

---

## 🚀 FIRST 90 DAYS SUCCESS PLAN

### Month 1: Learn & Absorb

**Week 1-2: Orientation**
- Understand business model, customers, products
- Learn data infrastructure (databases, tools, dashboards)
- Review existing reports and analyses
- Meet key stakeholders
- Set up development environment

**Week 3-4: Shadow & Learn**
- Shadow senior analysts
- Attend team meetings and stakeholder presentations
- Document processes and data sources
- Ask lots of questions
- Take on small tasks (report updates, data validation)

**Deliverables:**
- Onboarding documentation (for future hires)
- Data source map
- Stakeholder contact list
- Quick wins list (potential improvements)

### Month 2: Contribute

**Week 5-6: Take Ownership**
- Own recurring reports
- Identify quick improvements
- Fix broken dashboards/queries
- Build relationships across teams

**Week 7-8: First Projects**
- Complete independent analysis
- Present findings to team
- Propose new analyses
- Collaborate on larger projects

**Deliverables:**
- 2-3 analyses completed
- 1 process improvement implemented
- Presentation to stakeholders
- Updated documentation

### Month 3: Impact

**Week 9-10: Major Project**
- Lead significant analysis
- Work cross-functionally
- Present to leadership
- Demonstrate business impact

**Week 11-12: Establish Expertise**
- Become go-to person for specific domain
- Mentor newer team members
- Propose initiatives for next quarter
- Showcase achievements in review

**Deliverables:**
- 1 major project completed
- Quantifiable business impact
- Recognition from leadership
- Plan for next quarter

**Success Metrics:**
- Stakeholder satisfaction
- Quality of analyses
- Speed of delivery
- Business impact demonstrated
- Team collaboration

---

**This Career Prep Package gives you everything needed to land your Data Analyst role!**

Practice these questions, customize the templates, optimize your LinkedIn, and start applying with confidence.

**Good luck with your job search! 🚀**
"""
            pdf = create_unit_pdf(0, "Career Prep Package - Data Analyst", career_prep_md)
            st.download_button(
                label="Download Career Prep Package PDF",
                data=pdf,
                file_name="Career_Prep_Package_Data_Analyst.pdf",
                mime="application/pdf",
                key="da_career_prep_pdf_dl",
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
                    key=f"da_pathway_progress_unit_{unit_number}",
                )

    # Certificate
    with tabs[7]:
        st.subheader("🎓 Certificate")
        st.info(
            "On successful completion of all units and assessments, learners receive a "
            "T21 Data Analyst Pathway certificate, where offered by their training provider."
        )

        st.markdown(
            """### Requirements for completion

- Complete and submit evidence for all 7 units
- Demonstrate competence in core analyst tools (spreadsheets, SQL, BI, Python)
- Complete at least one end-to-end analyst capstone project
- Meet internal quality standards set by tutors/assessors
"""
        )

        if enrollment and enrollment.get("progress", 0) >= 100:
            st.success(
                "All requirements appear to be complete. Your training provider can now "
                "issue your Data Analyst Pathway certificate."
            )
        else:
            st.info(
                "Keep working through your units and projects. Once everything is complete, "
                "your tutor will confirm and issue your certificate."
            )
