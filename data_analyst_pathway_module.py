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

        st.markdown("---")
        st.markdown("## 🧪 Labs & Mini-Projects")
        st.markdown("**Comprehensive hands-on exercises for Unit 5 - Python for Data Analysis**")
        
        st.markdown("### LAB 1: Data Cleaning & Transformation with Pandas (90 min)")
        st.markdown("**Objective:** Master data cleaning techniques for real-world messy data")
        lab1_code = '''import pandas as pd
import numpy as np

# Load messy customer data
df = pd.read_csv('messy_customers.csv')

print("Original Data:")
print(df.head())
print(f"Shape: {df.shape}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# 1. Handle missing values
df['email'].fillna('no_email@company.com', inplace=True)
df['phone'].fillna('Unknown', inplace=True)
df.dropna(subset=['customer_id', 'name'], inplace=True)

# 2. Remove duplicates
print(f"\nDuplicates: {df.duplicated().sum()}")
df.drop_duplicates(subset=['customer_id'], keep='first', inplace=True)

# 3. Clean text data
df['name'] = df['name'].str.strip().str.title()
df['email'] = df['email'].str.lower().str.strip()
df['country'] = df['country'].str.upper()

# 4. Fix data types
df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
df['total_spent'] = pd.to_numeric(df['total_spent'], errors='coerce')

# 5. Handle outliers
Q1 = df['total_spent'].quantile(0.25)
Q3 = df['total_spent'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['total_spent'] >= Q1 - 1.5*IQR) & (df['total_spent'] <= Q3 + 1.5*IQR)]

# 6. Create new features
df['signup_year'] = df['signup_date'].dt.year
df['signup_month'] = df['signup_date'].dt.month
df['customer_segment'] = pd.cut(df['total_spent'], 
                                 bins=[0, 100, 500, 1000, float('inf')],
                                 labels=['Bronze', 'Silver', 'Gold', 'Platinum'])

print("\nCleaned Data:")
print(df.head())
print(f"Final shape: {df.shape}")
print(f"\nData types:\n{df.dtypes}")

# Save cleaned data
df.to_csv('cleaned_customers.csv', index=False)
print("\n✅ Data cleaning complete!")'''
        st.code(lab1_code, language='python')
        
        st.markdown("### LAB 2: Exploratory Data Analysis (EDA) with Pandas (120 min)")
        st.markdown("**Objective:** Perform comprehensive EDA on sales data")
        lab2_code = '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load sales data
sales = pd.read_csv('sales_data.csv')
sales['date'] = pd.to_datetime(sales['date'])

print("📊 EXPLORATORY DATA ANALYSIS\n" + "="*50)

# 1. Basic Statistics
print("\n1. BASIC STATISTICS:")
print(sales.describe())
print(f"\nTotal Revenue: ${sales['revenue'].sum():,.2f}")
print(f"Average Order Value: ${sales['revenue'].mean():.2f}")
print(f"Total Orders: {len(sales):,}")

# 2. Missing Data Analysis
print("\n2. MISSING DATA:")
missing = sales.isnull().sum()
print(missing[missing > 0])

# 3. Category Analysis
print("\n3. SALES BY CATEGORY:")
category_sales = sales.groupby('category').agg({
    'revenue': ['sum', 'mean', 'count'],
    'profit': 'sum'
}).round(2)
print(category_sales.sort_values(('revenue', 'sum'), ascending=False))

# 4. Time-based Analysis
print("\n4. MONTHLY TRENDS:")
sales['year_month'] = sales['date'].dt.to_period('M')
monthly = sales.groupby('year_month').agg({
    'revenue': 'sum',
    'order_id': 'count'
}).rename(columns={'order_id': 'num_orders'})
print(monthly.tail(12))

# 5. Customer Segmentation
print("\n5. CUSTOMER SEGMENTS:")
customer_value = sales.groupby('customer_id')['revenue'].sum()
segments = pd.cut(customer_value, 
                  bins=[0, 100, 500, 1000, float('inf')],
                  labels=['Low', 'Medium', 'High', 'VIP'])
print(segments.value_counts())

# 6. Product Performance
print("\n6. TOP 10 PRODUCTS:")
top_products = sales.groupby('product_name').agg({
    'revenue': 'sum',
    'quantity': 'sum'
}).sort_values('revenue', ascending=False).head(10)
print(top_products)

# 7. Correlation Analysis
print("\n7. CORRELATIONS:")
numeric_cols = sales.select_dtypes(include=[np.number]).columns
corr_matrix = sales[numeric_cols].corr()
print(corr_matrix['revenue'].sort_values(ascending=False))

# 8. Outlier Detection
print("\n8. OUTLIERS IN REVENUE:")
Q1 = sales['revenue'].quantile(0.25)
Q3 = sales['revenue'].quantile(0.75)
IQR = Q3 - Q1
outliers = sales[(sales['revenue'] < Q1 - 1.5*IQR) | (sales['revenue'] > Q3 + 1.5*IQR)]
print(f"Number of outliers: {len(outliers)} ({len(outliers)/len(sales)*100:.1f}%)")

print("\n✅ EDA Complete!")'''
        st.code(lab2_code, language='python')
        
        st.markdown("### LAB 3: Data Visualization with Matplotlib & Seaborn (90 min)")
        st.markdown("**Objective:** Create professional visualizations for business insights")
        lab3_code = '''import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# Load data
sales = pd.read_csv('sales_data.csv')
sales['date'] = pd.to_datetime(sales['date'])

# 1. Revenue Trend Over Time
plt.figure(figsize=(14, 6))
monthly_revenue = sales.groupby(sales['date'].dt.to_period('M'))['revenue'].sum()
monthly_revenue.plot(kind='line', marker='o', linewidth=2, markersize=8)
plt.title('Monthly Revenue Trend', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('revenue_trend.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Category Performance - Bar Chart
plt.figure(figsize=(10, 6))
category_revenue = sales.groupby('category')['revenue'].sum().sort_values(ascending=False)
ax = category_revenue.plot(kind='barh', color='steelblue')
plt.title('Revenue by Category', fontsize=16, fontweight='bold')
plt.xlabel('Revenue ($)', fontsize=12)
plt.ylabel('Category', fontsize=12)
for i, v in enumerate(category_revenue):
    ax.text(v, i, f' ${v:,.0f}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('category_revenue.png', dpi=300, bbox_inches='tight')
plt.show()

# 3. Distribution - Histogram
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(sales['revenue'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Revenue Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Revenue ($)', fontsize=11)
plt.ylabel('Frequency', fontsize=11)
plt.axvline(sales['revenue'].mean(), color='red', linestyle='--', label=f'Mean: ${sales["revenue"].mean():.2f}')
plt.legend()

plt.subplot(1, 2, 2)
plt.boxplot(sales['revenue'], vert=True)
plt.title('Revenue Boxplot', fontsize=14, fontweight='bold')
plt.ylabel('Revenue ($)', fontsize=11)
plt.tight_layout()
plt.savefig('revenue_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# 4. Correlation Heatmap
plt.figure(figsize=(10, 8))
numeric_cols = sales.select_dtypes(include=[np.number]).columns
corr_matrix = sales[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1)
plt.title('Correlation Matrix', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# 5. Scatter Plot with Regression
plt.figure(figsize=(10, 6))
sns.regplot(data=sales, x='quantity', y='revenue', scatter_kws={'alpha':0.5})
plt.title('Quantity vs Revenue', fontsize=16, fontweight='bold')
plt.xlabel('Quantity Sold', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.tight_layout()
plt.savefig('quantity_revenue_scatter.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ All visualizations saved!")'''
        st.code(lab3_code, language='python')
        
        st.markdown("### LAB 4: Advanced Data Analysis - Real Business Case (120 min)")
        st.markdown("**Objective:** Complete end-to-end analysis for business decision-making")
        lab4_code = '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

print("💼 BUSINESS CASE: E-COMMERCE PERFORMANCE ANALYSIS\n" + "="*60)

# Load multiple datasets
customers = pd.read_csv('customers.csv')
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')

# Convert dates
orders['order_date'] = pd.to_datetime(orders['order_date'])
customers['signup_date'] = pd.to_datetime(customers['signup_date'])

# ANALYSIS 1: Customer Lifetime Value (CLV)
print("\n1. CUSTOMER LIFETIME VALUE ANALYSIS:")
clv = orders.groupby('customer_id').agg({
    'order_id': 'count',
    'total_amount': 'sum',
    'order_date': ['min', 'max']
}).round(2)
clv.columns = ['num_orders', 'total_spent', 'first_order', 'last_order']
clv['avg_order_value'] = (clv['total_spent'] / clv['num_orders']).round(2)
clv['customer_lifetime_days'] = (clv['last_order'] - clv['first_order']).dt.days

print(f"Average CLV: ${clv['total_spent'].mean():.2f}")
print(f"Top 10% customers contribute: ${clv['total_spent'].quantile(0.9):.2f}+")

# ANALYSIS 2: Cohort Analysis
print("\n2. COHORT RETENTION ANALYSIS:")
orders['order_month'] = orders['order_date'].dt.to_period('M')
customers['cohort_month'] = customers['signup_date'].dt.to_period('M')

order_cohort = orders.merge(customers[['customer_id', 'cohort_month']], on='customer_id')
order_cohort['cohort_age'] = (order_cohort['order_month'] - order_cohort['cohort_month']).apply(lambda x: x.n)

cohort_data = order_cohort.groupby(['cohort_month', 'cohort_age'])['customer_id'].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index='cohort_month', columns='cohort_age', values='customer_id')
retention = cohort_pivot.divide(cohort_pivot[0], axis=0) * 100

print("Retention rates (%):\n", retention.head())

# ANALYSIS 3: Product Performance
print("\n3. PRODUCT PERFORMANCE:")
product_sales = orders.merge(products, on='product_id')
product_metrics = product_sales.groupby('product_name').agg({
    'order_id': 'count',
    'total_amount': 'sum',
    'quantity': 'sum'
}).sort_values('total_amount', ascending=False)

print("Top 5 products by revenue:")
print(product_metrics.head())

# ANALYSIS 4: Churn Prediction
print("\n4. CHURN RISK ANALYSIS:")
last_order = orders.groupby('customer_id')['order_date'].max().reset_index()
last_order.columns = ['customer_id', 'last_order_date']
days_since_order = (datetime.now() - last_order['last_order_date']).dt.days

churn_risk = pd.DataFrame({
    'customer_id': last_order['customer_id'],
    'days_since_order': days_since_order,
    'churn_risk': pd.cut(days_since_order, 
                         bins=[0, 30, 60, 90, float('inf')],
                         labels=['Low', 'Medium', 'High', 'Critical'])
})

print("Churn risk distribution:")
print(churn_risk['churn_risk'].value_counts())

# ANALYSIS 5: Revenue Forecast
print("\n5. SIMPLE REVENUE FORECAST:")
monthly_revenue = orders.groupby(orders['order_date'].dt.to_period('M'))['total_amount'].sum()
moving_avg = monthly_revenue.rolling(window=3).mean()

print(f"Last 3 months average: ${moving_avg.iloc[-1]:.2f}")
print(f"Projected next month: ${moving_avg.iloc[-1] * 1.05:.2f} (5% growth)")

# RECOMMENDATIONS
print("\n" + "="*60)
print("💡 BUSINESS RECOMMENDATIONS:")
print("="*60)
print(f"1. Focus on top 20% customers (CLV > ${clv['total_spent'].quantile(0.8):.2f})")
print(f"2. Re-engage {len(churn_risk[churn_risk['churn_risk']=='Critical'])} high-risk customers")
print(f"3. Promote top 5 products more aggressively")
print(f"4. Improve Month 1 retention (currently {retention[1].mean():.1f}%)")
print("\n✅ Analysis complete! Ready for executive presentation.")'''
        st.code(lab4_code, language='python')
        
        st.success("✅ Unit 5 Labs Complete: Python data analysis mastered!")


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
            st.markdown("**Comprehensive hands-on labs with executable Python code**")
            
            st.markdown("### LAB 1: A/B Test Analysis with Statistical Significance (90 min)")
            st.markdown("**Objective:** Analyze A/B test results and determine statistical significance")
            lab6_1 = '''import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

print("🧪 A/B TEST ANALYSIS\n" + "="*60)

# Test Data
control = {'visitors': 5000, 'conversions': 250}
variant = {'visitors': 5000, 'conversions': 325}

# Calculate conversion rates
control_rate = control['conversions'] / control['visitors']
variant_rate = variant['conversions'] / variant['visitors']

print("\n1. CONVERSION RATES:")
print(f"Control (A): {control_rate:.2%} ({control['conversions']}/{control['visitors']})")
print(f"Variant (B): {variant_rate:.2%} ({variant['conversions']}/{variant['visitors']})")

# Calculate lift
lift = (variant_rate - control_rate) / control_rate
print(f"\nRelative Lift: {lift:.1%}")
print(f"Absolute Lift: {(variant_rate - control_rate):.2%}")

# Statistical Significance Test (Two-proportion z-test)
print("\n2. STATISTICAL SIGNIFICANCE:")

# Pooled proportion
p_pooled = (control['conversions'] + variant['conversions']) / (control['visitors'] + variant['visitors'])

# Standard error
se = np.sqrt(p_pooled * (1 - p_pooled) * (1/control['visitors'] + 1/variant['visitors']))

# Z-score
z_score = (variant_rate - control_rate) / se

# P-value (two-tailed)
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

print(f"Z-score: {z_score:.3f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print(f"✅ SIGNIFICANT: Reject null hypothesis (p < 0.05)")
    print(f"   Variant B is statistically better than Control A")
else:
    print(f"❌ NOT SIGNIFICANT: Cannot reject null hypothesis (p >= 0.05)")
    print(f"   Difference could be due to chance")

# Confidence Interval (95%)
margin_of_error = 1.96 * se
ci_lower = (variant_rate - control_rate) - margin_of_error
ci_upper = (variant_rate - control_rate) + margin_of_error

print(f"\n95% Confidence Interval: [{ci_lower:.2%}, {ci_upper:.2%}]")

# Business Impact
print("\n3. BUSINESS IMPACT:")
avg_order_value = 50  # $50 per order
monthly_visitors = 150000

additional_conversions = monthly_visitors * (variant_rate - control_rate)
additional_revenue = additional_conversions * avg_order_value

print(f"Expected monthly impact:")
print(f"  Additional conversions: {additional_conversions:,.0f}")
print(f"  Additional revenue: ${additional_revenue:,.2f}")
print(f"  Annual revenue impact: ${additional_revenue * 12:,.2f}")

# Recommendation
print("\n4. RECOMMENDATION:")
if p_value < 0.05 and lift > 0:
    print("✅ IMPLEMENT VARIANT B")
    print(f"   - {lift:.1%} improvement is statistically significant")
    print(f"   - Expected annual revenue increase: ${additional_revenue * 12:,.2f}")
    print(f"   - Risk: Low (p-value: {p_value:.4f})")
else:
    print("❌ KEEP CONTROL A or RUN LONGER TEST")
    print(f"   - Results not statistically significant")
    print(f"   - Consider running test longer for more data")

print("\n✅ Analysis complete!")'''
            st.code(lab6_1, language='python')
            
            st.markdown("### LAB 2: KPI Dashboard & Metric Tracking (120 min)")
            st.markdown("**Objective:** Build automated KPI tracking system")
            lab6_2 = '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

print("📊 KPI DASHBOARD BUILDER\n" + "="*60)

# Simulate business metrics data
np.random.seed(42)
dates = pd.date_range(end=datetime.now(), periods=90, freq='D')

metrics_df = pd.DataFrame({
    'date': dates,
    'daily_revenue': np.random.normal(10000, 1500, 90),
    'new_customers': np.random.poisson(50, 90),
    'active_users': np.random.normal(5000, 500, 90),
    'conversion_rate': np.random.normal(0.03, 0.005, 90),
    'avg_order_value': np.random.normal(50, 10, 90),
    'customer_satisfaction': np.random.normal(4.2, 0.3, 90)
})

# Calculate derived KPIs
metrics_df['total_orders'] = (metrics_df['daily_revenue'] / metrics_df['avg_order_value']).astype(int)
metrics_df['revenue_per_user'] = metrics_df['daily_revenue'] / metrics_df['active_users']

print("\n1. KEY PERFORMANCE INDICATORS (Last 30 Days):")
print("="*60)

last_30 = metrics_df.tail(30)

# Revenue KPIs
total_revenue = last_30['daily_revenue'].sum()
avg_daily_revenue = last_30['daily_revenue'].mean()
revenue_growth = ((last_30['daily_revenue'].iloc[-7:].mean() / 
                   last_30['daily_revenue'].iloc[:7].mean()) - 1) * 100

print(f"\n💰 REVENUE METRICS:")
print(f"  Total Revenue (30d): ${total_revenue:,.2f}")
print(f"  Avg Daily Revenue: ${avg_daily_revenue:,.2f}")
print(f"  Week-over-Week Growth: {revenue_growth:+.1f}%")

# Customer KPIs
total_new_customers = last_30['new_customers'].sum()
avg_conversion = last_30['conversion_rate'].mean()
customer_acquisition_cost = total_revenue / total_new_customers * 0.2  # Assume 20% marketing spend

print(f"\n👥 CUSTOMER METRICS:")
print(f"  New Customers (30d): {total_new_customers:,}")
print(f"  Avg Conversion Rate: {avg_conversion:.2%}")
print(f"  Customer Acquisition Cost: ${customer_acquisition_cost:.2f}")

# Engagement KPIs
avg_active_users = last_30['active_users'].mean()
avg_satisfaction = last_30['customer_satisfaction'].mean()

print(f"\n⭐ ENGAGEMENT METRICS:")
print(f"  Avg Daily Active Users: {avg_active_users:,.0f}")
print(f"  Customer Satisfaction: {avg_satisfaction:.2f}/5.0")
print(f"  Revenue per User: ${last_30['revenue_per_user'].mean():.2f}")

# Trend Analysis
print("\n2. TREND ANALYSIS:")
print("="*60)

# Calculate 7-day moving averages
metrics_df['revenue_ma7'] = metrics_df['daily_revenue'].rolling(7).mean()
metrics_df['conversion_ma7'] = metrics_df['conversion_rate'].rolling(7).mean()

print(f"\n7-Day Moving Averages (Current):")
print(f"  Revenue: ${metrics_df['revenue_ma7'].iloc[-1]:,.2f}")
print(f"  Conversion Rate: {metrics_df['conversion_ma7'].iloc[-1]:.2%}")

# Identify trends
revenue_trend = "\u2b06\ufe0f UP" if metrics_df['revenue_ma7'].iloc[-1] > metrics_df['revenue_ma7'].iloc[-8] else "⬇\ufe0f DOWN"
conversion_trend = "⬆\ufe0f UP" if metrics_df['conversion_ma7'].iloc[-1] > metrics_df['conversion_ma7'].iloc[-8] else "⬇\ufe0f DOWN"

print(f"\nTrends (vs. last week):")
print(f"  Revenue: {revenue_trend}")
print(f"  Conversion: {conversion_trend}")

# Alerts
print("\n3. ALERTS & RECOMMENDATIONS:")
print("="*60)

if avg_conversion < 0.025:
    print("⚠\ufe0f  LOW CONVERSION: Below 2.5% threshold")
    print("   Action: Review checkout process and pricing")

if revenue_growth < -5:
    print("⚠\ufe0f  REVENUE DECLINE: Week-over-week drop > 5%")
    print("   Action: Investigate traffic sources and promotions")

if avg_satisfaction < 4.0:
    print("⚠\ufe0f  LOW SATISFACTION: Below 4.0 target")
    print("   Action: Review customer feedback and support tickets")

if customer_acquisition_cost > 100:
    print("⚠\ufe0f  HIGH CAC: Above $100 threshold")
    print("   Action: Optimize marketing spend and targeting")

if all([avg_conversion >= 0.025, revenue_growth >= -5, avg_satisfaction >= 4.0]):
    print("✅ All KPIs within target ranges!")

print("\n✅ KPI Dashboard complete!")'''
            st.code(lab6_2, language='python')
            
            st.markdown("### LAB 3: Cohort Analysis & Retention Metrics (90 min)")
            st.markdown("**Objective:** Analyze customer retention and lifetime value by cohort")
            lab6_3 = '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

print("📈 COHORT RETENTION ANALYSIS\n" + "="*60)

# Generate sample customer data
np.random.seed(42)

# Create customer cohorts
cohorts = []
for month in range(6):
    cohort_date = datetime(2024, month+1, 1)
    num_customers = np.random.randint(800, 1200)
    
    for _ in range(num_customers):
        cohorts.append({
            'customer_id': len(cohorts) + 1,
            'signup_date': cohort_date,
            'cohort_month': cohort_date.strftime('%Y-%m')
        })

customers = pd.DataFrame(cohorts)

# Generate purchase data
purchases = []
for _, customer in customers.iterrows():
    signup = customer['signup_date']
    
    # Simulate retention (decreasing probability over time)
    for month_offset in range(6):
        retention_prob = 0.8 * (0.85 ** month_offset)  # 80% initial, 15% decay
        
        if np.random.random() < retention_prob:
            purchase_date = signup + timedelta(days=30*month_offset + np.random.randint(0, 30))
            purchases.append({
                'customer_id': customer['customer_id'],
                'purchase_date': purchase_date,
                'amount': np.random.normal(50, 15)
            })

purchases_df = pd.DataFrame(purchases)
purchases_df['purchase_month'] = purchases_df['purchase_date'].dt.to_period('M')

# Merge with customer data
data = purchases_df.merge(customers, on='customer_id')
data['cohort'] = pd.to_datetime(data['cohort_month'])
data['cohort_age'] = ((data['purchase_month'].dt.to_timestamp() - data['cohort']).dt.days / 30).astype(int)

print("\n1. COHORT RETENTION TABLE:")
print("="*60)

# Create cohort retention matrix
cohort_data = data.groupby(['cohort_month', 'cohort_age'])['customer_id'].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index='cohort_month', columns='cohort_age', values='customer_id')

# Calculate retention percentages
retention_pct = cohort_pivot.divide(cohort_pivot[0], axis=0) * 100

print("\nRetention Rates (%):\n")
print(retention_pct.round(1))

# Key retention metrics
print("\n2. KEY RETENTION METRICS:")
print("="*60)

month_1_retention = retention_pct[1].mean()
month_3_retention = retention_pct[3].mean() if 3 in retention_pct.columns else None
month_6_retention = retention_pct[5].mean() if 5 in retention_pct.columns else None

print(f"\nAverage Retention Rates:")
print(f"  Month 1: {month_1_retention:.1f}%")
if month_3_retention:
    print(f"  Month 3: {month_3_retention:.1f}%")
if month_6_retention:
    print(f"  Month 6: {month_6_retention:.1f}%")

# Customer Lifetime Value
print("\n3. CUSTOMER LIFETIME VALUE (CLV):")
print("="*60)

clv_data = data.groupby('customer_id').agg({
    'amount': ['sum', 'count', 'mean'],
    'cohort_month': 'first'
}).reset_index()

clv_data.columns = ['customer_id', 'total_spent', 'num_purchases', 'avg_purchase', 'cohort']

avg_clv = clv_data['total_spent'].mean()
avg_purchases = clv_data['num_purchases'].mean()
avg_purchase_value = clv_data['avg_purchase'].mean()

print(f"\nAverage Customer Metrics:")
print(f"  Lifetime Value: ${avg_clv:.2f}")
print(f"  Number of Purchases: {avg_purchases:.1f}")
print(f"  Average Purchase Value: ${avg_purchase_value:.2f}")

# CLV by cohort
clv_by_cohort = clv_data.groupby('cohort')['total_spent'].mean().sort_index()

print(f"\nCLV by Cohort:")
for cohort, clv in clv_by_cohort.items():
    print(f"  {cohort}: ${clv:.2f}")

# Recommendations
print("\n4. RECOMMENDATIONS:")
print("="*60)

if month_1_retention < 70:
    print("⚠\ufe0f  Month 1 retention below 70% - Focus on onboarding")
else:
    print("✅ Month 1 retention healthy")

if month_3_retention and month_3_retention < 40:
    print("⚠\ufe0f  Month 3 retention below 40% - Improve engagement campaigns")
elif month_3_retention:
    print("✅ Month 3 retention acceptable")

if avg_purchases < 2:
    print("⚠\ufe0f  Low repeat purchase rate - Implement loyalty program")
else:
    print("✅ Good repeat purchase behavior")

print("\n✅ Cohort analysis complete!")'''
            st.code(lab6_3, language='python')
            
            st.success("✅ Unit 6 Labs Complete: Metrics, KPIs & A/B testing mastered!")
        elif selected_unit == 7:
            st.markdown("### 🎯 Unit 7: Data Analyst Capstone Projects")
            st.markdown("**Choose one comprehensive project to showcase your data analyst skills**")
            
            st.markdown("## 📊 Capstone Project Options")
            
            st.markdown("### Option 1: E-Commerce Sales Performance Analysis")
            st.markdown("""
**Objective:** Analyze sales data and create executive dashboard with actionable recommendations

**Dataset Requirements:**
- Sales transactions (6+ months)
- Customer demographics
- Product catalog
- Marketing campaigns

**Deliverables:**
1. **Excel Analysis:**
   - Data cleaning and validation
   - Pivot tables for key metrics
   - Sales trends and seasonality
   - Customer segmentation (RFM analysis)

2. **SQL Queries:**
   - Top products by revenue
   - Customer lifetime value
   - Cohort retention analysis
   - Monthly/weekly performance

3. **Python Analysis:**
   - Advanced EDA with pandas
   - Statistical analysis
   - Predictive insights
   - Visualization with matplotlib/seaborn

4. **Dashboard (Tableau/Power BI):**
   - Executive KPI summary
   - Sales trends and forecasts
   - Product performance
   - Customer insights

5. **Final Report:**
   - Executive summary (1 page)
   - Key findings (3-5 insights)
   - Actionable recommendations
   - Expected business impact

**Skills Demonstrated:** Excel, SQL, Python, BI tools, business storytelling
""")
            
            st.markdown("### Option 2: Customer Churn Analysis & Retention Strategy")
            st.markdown("""
**Objective:** Identify churn drivers and develop data-driven retention strategy

**Dataset Requirements:**
- Customer subscription data
- Usage/engagement metrics
- Support tickets
- Billing history

**Deliverables:**
1. **Churn Analysis:**
   - Churn rate calculation by segment
   - Cohort retention analysis
   - Identify high-risk customers
   - Key churn indicators

2. **SQL Analysis:**
   - Customer lifetime value
   - Engagement patterns
   - Support ticket correlation
   - Retention by acquisition channel

3. **Python Modeling:**
   - Churn prediction model
   - Feature importance analysis
   - Customer segmentation
   - Risk scoring system

4. **Retention Dashboard:**
   - Real-time churn metrics
   - At-risk customer alerts
   - Retention campaign tracking
   - ROI calculator

5. **Strategy Document:**
   - Retention initiatives (prioritized)
   - Expected impact and costs
   - Implementation timeline
   - Success metrics

**Skills Demonstrated:** Predictive analytics, customer analytics, strategic thinking
""")
            
            st.markdown("### Option 3: Marketing Campaign Performance & ROI Analysis")
            st.markdown("""
**Objective:** Evaluate marketing effectiveness and optimize budget allocation

**Dataset Requirements:**
- Campaign data (email, social, paid ads)
- Website analytics
- Conversion data
- Marketing spend

**Deliverables:**
1. **Campaign Analysis:**
   - ROI by channel and campaign
   - Conversion funnel analysis
   - Customer acquisition cost
   - Attribution modeling

2. **A/B Test Analysis:**
   - Statistical significance testing
   - Lift calculations
   - Segment performance
   - Recommendations

3. **Python Analysis:**
   - Multi-touch attribution
   - Predictive CLV
   - Budget optimization
   - Visualization dashboards

4. **Marketing Dashboard:**
   - Real-time campaign metrics
   - Channel comparison
   - Budget vs. actual
   - Conversion tracking

5. **Optimization Report:**
   - Budget reallocation plan
   - Expected ROI improvement
   - Testing roadmap
   - KPI framework

**Skills Demonstrated:** Marketing analytics, A/B testing, ROI analysis, optimization
""")
            
            st.markdown("### Option 4: Supply Chain & Inventory Optimization")
            st.markdown("""
**Objective:** Optimize inventory levels and reduce costs while maintaining service levels

**Dataset Requirements:**
- Inventory levels (historical)
- Sales/demand data
- Supplier lead times
- Stockout incidents

**Deliverables:**
1. **Inventory Analysis:**
   - ABC analysis (Pareto)
   - Stock turnover rates
   - Stockout frequency
   - Carrying cost analysis

2. **SQL Reporting:**
   - Slow-moving inventory
   - Reorder point calculations
   - Supplier performance
   - Demand patterns

3. **Python Forecasting:**
   - Demand forecasting model
   - Safety stock calculations
   - Reorder optimization
   - Scenario analysis

4. **Operations Dashboard:**
   - Inventory health metrics
   - Stockout alerts
   - Supplier scorecards
   - Cost tracking

5. **Optimization Plan:**
   - Inventory policy recommendations
   - Cost savings projections
   - Implementation roadmap
   - Risk mitigation

**Skills Demonstrated:** Operations analytics, forecasting, optimization, cost analysis
""")
            
            st.markdown("### Option 5: Financial Performance & KPI Dashboard")
            st.markdown("""
**Objective:** Build comprehensive financial analytics system for executive decision-making

**Dataset Requirements:**
- Financial statements (P&L, Balance Sheet)
- Transaction data
- Budget vs. actuals
- Department/product costs

**Deliverables:**
1. **Financial Analysis:**
   - Profitability by product/segment
   - Variance analysis (budget vs. actual)
   - Trend analysis
   - Financial ratios

2. **SQL Reporting:**
   - Revenue breakdown
   - Cost center analysis
   - Cash flow tracking
   - Period-over-period comparisons

3. **Python Analysis:**
   - Automated financial reports
   - Anomaly detection
   - Forecasting
   - Scenario modeling

4. **Executive Dashboard:**
   - Key financial KPIs
   - P&L visualization
   - Budget tracking
   - Alerts and insights

5. **CFO Report:**
   - Financial health summary
   - Key drivers and risks
   - Strategic recommendations
   - Forward-looking projections

**Skills Demonstrated:** Financial analytics, business intelligence, executive reporting
""")
            
            st.markdown("## 📝 Capstone Evaluation Rubric")
            st.markdown("""
**Your capstone will be evaluated on:**

### 1. Data Analysis Quality (25%)
- ✅ Thorough data cleaning and validation
- ✅ Appropriate analytical methods
- ✅ Accurate calculations
- ✅ Insightful findings

### 2. Technical Skills (25%)
- ✅ Excel: Advanced formulas, pivot tables
- ✅ SQL: Complex queries, joins, aggregations
- ✅ Python: pandas, visualization, analysis
- ✅ BI Tools: Professional dashboard

### 3. Business Impact (20%)
- ✅ Clear business problem definition
- ✅ Actionable recommendations
- ✅ Quantified impact (revenue, cost, etc.)
- ✅ Implementation feasibility

### 4. Communication (20%)
- ✅ Executive summary (non-technical)
- ✅ Clear visualizations
- ✅ Logical story flow
- ✅ Professional presentation

### 5. Documentation (10%)
- ✅ Clean, commented code
- ✅ Methodology explained
- ✅ Data sources cited
- ✅ Reproducible analysis

**Grading Scale:**
- 90-100%: Exceptional - Portfolio-ready
- 80-89%: Strong - Minor improvements needed
- 70-79%: Good - Meets requirements
- Below 70%: Needs revision

**Bonus Points:**
- Advanced statistical methods
- Predictive modeling
- Automated reporting
- Interactive dashboards
- Real business data (with permission)
""")
            
            st.success("✅ Choose your capstone project and build something amazing!")
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
