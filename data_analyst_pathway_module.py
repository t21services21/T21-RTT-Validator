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
